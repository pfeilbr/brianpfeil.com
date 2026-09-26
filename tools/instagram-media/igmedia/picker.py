"""The Google Photos picker: a local web app for choosing what goes on /media/.

    make media-picker        # http://127.0.0.1:8790

It binds 127.0.0.1 only. Three jobs:

1. Receive harvests. `picker/harvest.js`, run on a Google Photos search page
   (as a bookmarklet, or driven by an agent), POSTs the results here. That is
   the only cross-origin request accepted, and only from photos.google.com.
2. Screen in the background: fetch a thumbnail and a 1600px copy (a 360p
   rendition for a video), run Apple Vision over it, and record the verdict
   from igmedia/screen.py. Blocked items are never offered.
3. Serve the picker page, save each decision to picks.yaml the moment it is
   made, and publish on request (encode, upload, write data/photos.yaml,
   commit and push).
"""

import json
import mimetypes
import queue
import shutil
import tempfile
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import derive, fetch, gphotos, gphotos_publish, publish, release, screen

HARVEST_ORIGIN = "https://photos.google.com"


class Picker:
    def __init__(self, tool_dir: Path, repo_root: Path, cfg: dict):
        self.tool_dir, self.repo_root, self.cfg = tool_dir, repo_root, cfg
        g = cfg["gphotos"]
        self.g = g
        self.work = tool_dir / cfg["work_dir"] / "gphotos"
        self.cands = gphotos.Candidates(self.work / "candidates.json")
        self.picks_path = tool_dir / g["picks"]
        self.picks = gphotos.load_picks(self.picks_path)
        self.categories = gphotos.load_categories(g)
        self.exclude = g.get("exclude_people") or []
        self.queries = gphotos.query_index(self.categories, g["person"], self.exclude)
        self.lock = threading.RLock()
        self.jobs: "queue.Queue[str]" = queue.Queue()
        self.vision_bin = screen.build_vision(tool_dir / "vision" / "screen.swift",
                                              tool_dir / cfg["work_dir"] / "bin" / "vision-screen")
        self.publish_log: list[str] = []
        self.publishing = False
        self.harvests: dict[str, dict] = {}
        self.port = 8790
        for c in self.cands.items.values():
            if not c.get("screen"):
                self.jobs.put(c["key"])

    # --- paths -----------------------------------------------------------------
    def small(self, key: str) -> Path:
        return self.work / "small" / f"{key}.jpg"

    def large(self, key: str) -> Path:
        return self.work / "large" / f"{key}.jpg"

    def preview(self, key: str) -> Path:
        return self.work / "preview" / f"{key}.mp4"

    def hq(self, key: str) -> Path:
        return self.work / "hq" / f"{key}.mp4"

    def final(self, key: str) -> Path:
        return self.work / "final" / f"{key}.jpg"

    def motion(self, key: str) -> Path:
        return self.work / "motion" / f"{key}.mp4"

    def path_for(self, key: str, variant: str) -> Path:
        return {"small": self.small, "large": self.large, "preview": self.preview,
                "hq": self.hq, "final": self.final, "motion": self.motion}[variant](key)

    # --- downloads, done by the browser ------------------------------------------
    # Google's image host only answers B's signed-in browser, so the page that
    # harvested a result also downloads it: it asks what is wanted, fetches each
    # file itself and POSTs the bytes here. No cookie ever leaves Chrome.
    def wanted(self, limit: int = 40) -> list[dict]:
        out = []
        with self.lock:
            included = {k for k, p in self.picks.items() if p.get("decision") == "include"}
            for c in self.cands.items.values():
                key, need = c["key"], []
                # The copy a pick is published from, fetched once it is picked.
                if key in included:
                    need.append("hq" if c["kind"] == "video" else "final")
                status = (c.get("screen") or {}).get("status")
                if not status or status == "error":
                    need.append("small")
                    need.append("preview" if c["kind"] == "video" else "large")
                stale = set()
                if c["kind"] == "photo" and (status in ("ok", "warn") or key in included):
                    # Thumbnails from before -no carry a fake play button.
                    for v in ("small", "large"):
                        if c.get("thumbs") != fetch.THUMBS_VERSION:
                            need.append(v)
                            stale.add(v)
                    # Whether it is a motion photo, and if so its clip, which
                    # is screened too: the clip can show who the still doesn't.
                    if c.get("motion") is None:
                        need.append("motion")
                for v in dict.fromkeys(need):
                    if v in stale or not self.path_for(key, v).exists():
                        out.append({"key": key, "variant": v, "url": c["url"],
                                    "suffixes": fetch.SUFFIXES[v]})
                if len(out) >= limit:
                    break
        # Screening material first, so suggestions appear while videos download.
        return sorted(out, key=lambda w: w["variant"] in ("hq", "final"))[:limit]

    def receive(self, key: str, variant: str, stream, length: int) -> dict:
        """Store one file the browser sent, streamed to disk (an hq video can
        be hundreds of MB), and check from its bytes that it is what was asked for."""
        c = self.cands.items.get(key)
        if c is None or variant not in fetch.SUFFIXES:
            stream.read(length)
            return {"ok": False, "error": "unknown key or variant"}
        dest = self.path_for(key, variant)
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_name(dest.name + ".part")
        with open(tmp, "wb") as f:
            left = length
            while left > 0:
                chunk = stream.read(min(left, 1 << 20))
                if not chunk:
                    break
                f.write(chunk)
                left -= len(chunk)
        with open(tmp, "rb") as f:
            got = fetch.sniff(f.read(16))
        want = "video" if variant in ("preview", "hq", "motion") else "image"
        # Google answers a refused request with a small placeholder PNG.
        if not left and dest.suffix == ".jpg" and tmp.stat().st_size < 2048:
            got = "a placeholder image"
        if left or got != want:
            tmp.unlink(missing_ok=True)
            return {"ok": False, "error": f"expected {want}, got {got}" if not left else "truncated"}
        tmp.replace(dest)
        with self.lock:
            if variant in ("small", "large") and c["kind"] == "photo":
                c.setdefault("fresh", [])
                if variant not in c["fresh"]:
                    c["fresh"].append(variant)
                if set(c["fresh"]) >= {"small", "large"}:
                    c["thumbs"] = fetch.THUMBS_VERSION
                    c.pop("fresh")
                self.cands.save()
                return {"ok": True}  # a refreshed thumbnail changes no verdict
            if variant == "motion":
                c["motion"] = True
                c.pop("screen", None)  # judge it again, clip included
                self.cands.save()
            elif variant in ("hq", "final"):
                return {"ok": True}
            elif (c.get("screen") or {}).get("status") == "error":
                c.pop("screen")
        self.jobs.put(key)
        return {"ok": True}

    def no_motion(self, key: str) -> dict:
        """The browser found no clip behind this photo: it is a plain one."""
        with self.lock:
            c = self.cands.items.get(key)
            if c is None or c["kind"] != "photo":
                return {"ok": False, "error": "unknown photo"}
            c["motion"] = False
            self.cands.save()
        return {"ok": True}

    # --- harvest ---------------------------------------------------------------
    def harvest(self, body: dict) -> dict:
        query = (body.get("query") or "").strip()
        hit = self.queries.get(query.lower())
        if hit is None:
            return {"ok": False, "error": f"'{query}' is not one of the configured searches",
                    "queries": sorted(self.queries)}
        category, tier = hit
        rows = body.get("items") or []
        if tier == "exclude":
            with self.lock:
                blocked = self.cands.exclude(rows)
                for k in blocked:  # re-judge: the verdict now includes the exclusion
                    self.cands.items[k].pop("screen", None)
                    self.jobs.put(k)
                self.cands.save()
                self.harvests[query] = {"count": len(rows), "new": 0, "at": time.strftime("%H:%M:%S")}
            return {"ok": True, "category": category, "tier": tier, "received": len(rows), "new": 0,
                    "blocked": len(blocked)}
        with self.lock:
            new = self.cands.add(rows, category, tier, query)
            self.cands.save()
            self.harvests[query] = {"count": len(rows), "new": new, "at": time.strftime("%H:%M:%S")}
        for r in rows:
            c = self.cands.items.get(r.get("key"))
            if c and not c.get("screen"):
                self.jobs.put(c["key"])
        rejected = {}
        for r in rows:
            why = gphotos.reject_reason(r)
            if why:
                rejected[why] = rejected.get(why, 0) + 1
        return {"ok": True, "category": category, "tier": tier, "received": len(rows), "new": new,
                "rejected": rejected}

    # --- screening -------------------------------------------------------------
    def worker(self) -> None:
        while True:
            key = self.jobs.get()
            try:
                self.screen_one(key)
            except Exception as exc:  # keep the worker alive; record why
                with self.lock:
                    c = self.cands.items.get(key)
                    if c is not None:
                        c["screen"] = {"status": "error", "reasons": [str(exc)[:200]]}
                        self.cands.save()

    def screen_one(self, key: str) -> None:
        with self.lock:
            c = dict(self.cands.items.get(key) or {})
        if not c or (c.get("screen") or {}).get("status") in ("ok", "warn", "blocked"):
            return
        needed = [self.small(key), self.preview(key) if c["kind"] == "video" else self.large(key)]
        if not all(p.exists() for p in needed):
            return  # the browser has not sent it yet; queued again when it does
        if c["kind"] == "video":
            with tempfile.TemporaryDirectory() as tmp:
                images = fetch.frames(self.preview(key), Path(tmp), count=10)
                results = screen.run_vision(self.vision_bin, images)
            dur = fetch.duration(self.preview(key))
        else:
            images = [self.large(key)]
            with tempfile.TemporaryDirectory() as tmp:
                if c.get("motion") and self.motion(key).exists():
                    images += fetch.frames(self.motion(key), Path(tmp), count=6)
                results = screen.run_vision(self.vision_bin, images)
            dur = None
        v = screen.verdict(results, c.get("tier", "me"), key in self.cands.excluded)
        labels = {}
        for r in results:
            for k, p in (r.get("labels") or {}).items():
                labels[k] = max(labels.get(k, 0), p)
        v["labels"] = [k for k, _ in sorted(labels.items(), key=lambda x: -x[1])[:6]]
        with self.lock:
            live = self.cands.items.get(key)
            if live is not None:
                live["screen"] = v
                if dur:
                    live["duration"] = round(dur, 1)
                self.cands.save()

    # --- state -----------------------------------------------------------------
    def state(self) -> dict:
        with self.lock:
            items = list(self.cands.items.values())
            leaders = {}
            for cat in self.categories:
                in_cat = [c for c in items if cat.key in c["categories"]
                          and (c.get("screen") or {}).get("status") in ("ok", "warn")]
                leaders.update(screen.similar_groups(in_cat))
            out = []
            for c in items:
                p = self.picks.get(c["key"], {})
                out.append({
                    "key": c["key"], "id": c["id"], "kind": c["kind"], "taken": c.get("taken"),
                    "orient": c.get("orient"), "categories": c["categories"], "tier": c.get("tier"),
                    "duration": c.get("duration"), "screen": c.get("screen"),
                    "motion": bool(c.get("motion")) and self.motion(c["key"]).exists(),
                    "leader": leaders.get(c["key"], c["key"]),
                    "decision": p.get("decision"), "category": p.get("category"),
                })
            return {
                "person": self.g["person"],
                "categories": [{"key": c.key, "query": c.query,
                                "searches": list(c.queries(self.g["person"], self.exclude))}
                               for c in self.categories],
                "items": out,
                "pending": self.jobs.qsize(),
                "waiting": len(waiting := self.wanted(limit=10_000)),
                "to_fetch": sum(1 for w in waiting if w["variant"] in ("hq", "final")),
                "harvests": self.harvests,
                "publishing": self.publishing,
                "log": self.publish_log[-200:],
            }

    def decide(self, body: dict) -> dict:
        decision = body.get("decision")
        category = body.get("category")
        valid = {c.key for c in self.categories}
        if decision not in ("include", "skip", None):
            return {"ok": False, "error": "decision must be include, skip or null"}
        if decision == "include" and category not in valid:
            return {"ok": False, "error": f"unknown category {category!r}"}
        with self.lock:
            for key in body.get("keys") or []:
                c = self.cands.items.get(key)
                if c is None:
                    continue
                if decision == "include" and (c.get("screen") or {}).get("status") not in ("ok", "warn"):
                    continue  # blocked or unscreened: never publishable
                if decision is None:
                    self.picks.pop(key, None)
                else:
                    self.picks[key] = {"key": key, "decision": decision,
                                       "category": category if decision == "include" else None}
            gphotos.save_picks(self.picks_path, self.picks)
        return {"ok": True}

    # --- publish ---------------------------------------------------------------
    def log(self, line: str) -> None:
        self.publish_log.append(f"{time.strftime('%H:%M:%S')} {line}")

    def publish(self, push: bool = True, dry: bool = False) -> None:
        """Encode, upload, write data/photos.yaml, commit and push.

        dry: encode only, and write the data file to build/gphotos/preview/
        pointing at this server's /web/, so the page can be tried locally
        with nothing uploaded or committed.
        """
        self.publishing = True
        self.publish_log = []
        try:
            cfg, g = self.cfg, self.g
            if not dry:
                self.log("checking AWS sign-in…")
                publish.check_credentials(cfg["bucket"])
            lock = derive.Lock(self.tool_dir / g["lock_file"])
            vision = lambda imgs: screen.run_vision(self.vision_bin, imgs)  # noqa: E731
            with self.lock:
                picks = {k: v for k, v in self.picks.items() if k not in self.cands.excluded}
                cands = dict(self.cands.items)
            cats = [c.key for c in self.categories]
            source = lambda c: self.hq(c["key"]) if c["kind"] == "video" else self.final(c["key"])  # noqa: E731
            entries, refused = gphotos_publish.build(picks, cands, cats, self.work, g["s3_prefix"],
                                                     lock, vision, source, log=self.log)
            if refused:
                with self.lock:
                    for k in refused:
                        self.picks[k] = {"key": k, "decision": "skip", "category": None}
                        self.cands.items[k]["screen"] = {"status": "blocked",
                                                         "reasons": ["refused at full resolution"]}
                    gphotos.save_picks(self.picks_path, self.picks)
                    self.cands.save()
            if dry:
                preview = self.work / "preview-data" / "photos.yaml"
                gphotos_publish.write(preview, f"http://127.0.0.1:{self.port}/web/", cats, entries)
                self.log(f"dry run: {len(entries)} items encoded; data file at {preview}")
                return
            self.log(f"uploading to s3://{cfg['bucket']}/{g['s3_prefix']}/ …")
            out = publish.sync(self.work / "web", cfg["bucket"], g["s3_prefix"])
            self.log(f"uploaded {sum(1 for l in out.splitlines() if l.startswith('upload:'))} files")
            data_path = self.repo_root / g["data_file"]
            gphotos_publish.write(data_path, cfg["base_url"], cats, entries)
            self.log(f"wrote {g['data_file']} ({len(entries)} items)")
            if push:
                sha = release.commit_and_push(
                    self.repo_root, [data_path, self.picks_path],
                    f"Publish {len(entries)} Google Photos item{'s' if len(entries) != 1 else ''} to /media/\n\n"
                    "Generated by the picker (make media-picker) from picks.yaml.\n")
                self.log(f"committed and pushed {sha}" if sha else "nothing changed; no commit")
            self.log("done — live in a minute or two")
        except Exception as exc:
            self.log(f"FAILED: {exc}")
            self.log(traceback.format_exc().splitlines()[-1])
        finally:
            self.publishing = False


def make_handler(p: Picker, static: Path):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):  # quiet
            pass

        def _send(self, code: int, body: bytes, ctype: str, extra: dict | None = None):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            # JSON and the harvest script change under a running page; never cache them.
            self.send_header("Cache-Control", "max-age=3600" if ctype.startswith("image/") else "no-store")
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def _json(self, obj, code=200, extra=None):
            self._send(code, json.dumps(obj).encode(), "application/json", extra)

        def _file(self, path: Path):
            if not path.is_file():
                return self._send(404, b"not found", "text/plain")
            ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            size = path.stat().st_size
            rng = self.headers.get("Range")
            if rng and rng.startswith("bytes="):  # Safari will not play a video without ranges
                start_s, _, end_s = rng[6:].partition("-")
                start = int(start_s or 0)
                end = min(int(end_s) if end_s else size - 1, size - 1)
                with open(path, "rb") as f:
                    f.seek(start)
                    chunk = f.read(end - start + 1)
                self.send_response(206)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Length", str(len(chunk)))
                self.end_headers()
                self.wfile.write(chunk)
                return
            with open(path, "rb") as f:
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(size))
                self.send_header("Accept-Ranges", "bytes")
                self.end_headers()
                shutil.copyfileobj(f, self.wfile)

        def _cors(self) -> dict:
            if self.headers.get("Origin") != HARVEST_ORIGIN:
                return {}
            return {"Access-Control-Allow-Origin": HARVEST_ORIGIN,
                    "Access-Control-Allow-Methods": "GET, POST",
                    "Access-Control-Allow-Headers": "content-type",
                    "Access-Control-Allow-Private-Network": "true"}

        def _local(self) -> bool:
            """Requests that change things must come from the picker page."""
            origin = self.headers.get("Origin")
            return origin is None or origin.startswith(("http://127.0.0.1:", "http://localhost:"))

        def do_OPTIONS(self):
            self._send(204, b"", "text/plain", self._cors())

        def _blob(self):
            from urllib.parse import parse_qs, urlparse
            cors = self._cors()
            if not cors and not self._local():
                return self._json({"ok": False, "error": "origin"}, 403)
            q = parse_qs(urlparse(self.path).query)
            key, variant = (q.get("key") or [""])[0], (q.get("variant") or [""])[0]
            length = int(self.headers.get("Content-Length") or 0)
            if not gphotos.KEY.match(key) or length <= 0 or length > fetch.MAX_BYTES.get(variant, 0):
                return self._json({"ok": False, "error": "bad key, variant or size"}, 400, cors)
            return self._json(p.receive(key, variant, self.rfile, length), extra=cors)

        def do_GET(self):
            path = self.path.split("?")[0]
            if path == "/":
                return self._file(static / "index.html")
            if path == "/harvest.js":
                body = (static / "harvest.js").read_bytes()
                return self._send(200, body, "text/javascript", self._cors())
            if path == "/api/state":
                return self._json(p.state())
            if path == "/api/tier":
                from urllib.parse import parse_qs, urlparse
                q = (parse_qs(urlparse(self.path).query).get("q") or [""])[0]
                hit = p.queries.get(q.strip().lower())
                return self._json({"tier": hit[1] if hit else None}, extra=self._cors())
            if path == "/api/sleep":
                from urllib.parse import parse_qs, urlparse
                ms = int((parse_qs(urlparse(self.path).query).get("ms") or ["500"])[0])
                time.sleep(min(max(ms, 0), 5000) / 1000)
                return self._json({"ok": True}, extra=self._cors())
            if path == "/api/wanted":
                return self._json({"wanted": p.wanted()}, extra=self._cors())
            if path.startswith("/web/"):  # dry-run output, for trying the page locally
                rel = Path(path[len("/web/"):])
                if ".." in rel.parts:
                    return self._send(400, b"bad path", "text/plain")
                return self._file(p.work / "web" / rel.relative_to(p.g["s3_prefix"]) if rel.parts and rel.parts[0] == p.g["s3_prefix"] else p.work / "web" / rel)
            for prefix, fn in (("/small/", p.small), ("/large/", p.large), ("/preview/", p.preview), ("/hq/", p.hq), ("/final/", p.final),
                               ("/motion/", p.motion)):
                if path.startswith(prefix):
                    key = path[len(prefix):].rsplit(".", 1)[0]
                    if not gphotos.KEY.match(key):
                        return self._send(400, b"bad key", "text/plain")
                    return self._file(fn(key))
            self._send(404, b"not found", "text/plain")

        def do_POST(self):
            path = self.path.split("?")[0]
            if path == "/api/blob":
                return self._blob()
            if path == "/api/failed":
                # The browser could not fetch a variant. Only "motion" means
                # anything: a photo with no clip behind it.
                from urllib.parse import parse_qs, urlparse
                cors = self._cors()
                if not cors and not self._local():
                    return self._json({"ok": False, "error": "origin"}, 403)
                q = parse_qs(urlparse(self.path).query)
                if (q.get("variant") or [""])[0] == "motion":
                    return self._json(p.no_motion((q.get("key") or [""])[0]), extra=cors)
                return self._json({"ok": True}, extra=cors)
            length = int(self.headers.get("Content-Length") or 0)
            if length > 50_000_000:
                return self._send(413, b"too large", "text/plain")
            try:
                body = json.loads(self.rfile.read(length) or b"{}")
            except json.JSONDecodeError:
                return self._json({"ok": False, "error": "bad json"}, 400)
            if path == "/api/harvest":
                cors = self._cors()
                if not cors and not self._local():
                    return self._json({"ok": False, "error": "origin"}, 403)
                return self._json(p.harvest(body), extra=cors)
            if not self._local():
                return self._json({"ok": False, "error": "origin"}, 403)
            if path == "/api/decide":
                return self._json(p.decide(body))
            if path == "/api/publish":
                if p.publishing:
                    return self._json({"ok": False, "error": "already publishing"})
                threading.Thread(target=p.publish, kwargs={"push": body.get("push", True),
                                                           "dry": bool(body.get("dry"))},
                                 daemon=True).start()
                return self._json({"ok": True})
            self._send(404, b"not found", "text/plain")

    return H


def serve(tool_dir: Path, repo_root: Path, cfg: dict, port: int = 8790, workers: int = 3) -> None:
    p = Picker(tool_dir, repo_root, cfg)
    p.port = port
    for _ in range(workers):
        threading.Thread(target=p.worker, daemon=True).start()
    srv = ThreadingHTTPServer(("127.0.0.1", port), make_handler(p, tool_dir / "picker"))
    print(f"picker: http://127.0.0.1:{port}  ({len(p.cands.items)} candidates, "
          f"{p.jobs.qsize()} to screen)", flush=True)
    srv.serve_forever()
