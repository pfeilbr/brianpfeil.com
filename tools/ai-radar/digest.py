#!/usr/bin/env python3
"""The daily AI briefing: one Claude call that reads the last day of
data/ai.json and writes a short, cited summary in all nine site languages.

  tools/ai-radar/.venv/bin/python tools/ai-radar/digest.py           # once a day
  tools/ai-radar/.venv/bin/python tools/ai-radar/digest.py --force   # again today
  tools/ai-radar/.venv/bin/python tools/ai-radar/digest.py --dry-run # show the prompt

It runs after radar.py in the daily Action. With no ANTHROPIC_API_KEY it
does nothing and exits 0, so the page simply shows no briefing. It never
invents sources: every point cites item ids from the file, and a point
whose citations don't resolve is dropped.

The briefing lands in data/ai.json as `digest`, and every day's briefing is
appended to data/ai-digests.json (the archive the page and the RSS feed
read). Needs the `anthropic` package (requirements.txt); radar.py does not.
"""
import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import radar  # noqa: E402

ARCHIVE = radar.ROOT / "data" / "ai-digests.json"
ARCHIVE_KEEP = 60
MODEL = "claude-opus-5"
LANGS = ["en", "zh", "es", "pt", "fr", "de", "it", "ja", "ko"]
LANG_NAMES = {
    "en": "English", "zh": "Simplified Chinese", "es": "Spanish (Spain)",
    "pt": "Portuguese (Brazil)", "fr": "French", "de": "German",
    "it": "Italian", "ja": "Japanese", "ko": "Korean",
}
LOOKBACK_HOURS = 30
MAX_ITEMS = 160
MIN_POINTS, MAX_POINTS = 4, 7

SYSTEM = """You write the daily AI briefing at the top of brianpfeil.com/ai/, a page that gathers AI news every morning for software engineers who want to keep up without reading everything.

Brian Pfeil, whose site it is, is a principal cloud architect and AWS Community Builder who builds with AI coding tools daily. His readers are practitioners: they want to know what changed, why it matters to someone building software, and where to read more.

You are given the items the page collected in the last day, each with an id. Write:
- headline: one sentence naming the day's most important development.
- points: between {min} and {max} bullet points, most important first. Each is one or two plain sentences: what happened, then why it matters to a builder. Group items about the same story into one point. Cite the items each point is based on by id in refs (one to four ids).

Only state what the items support; if the items are thin, write fewer points rather than padding. No hype words, no exclamation marks, no markdown. Keep product, model and company names as they are.

Write the English version first, then translate it faithfully into each of the other languages, keeping the same points in the same order with the same refs. Use natural, fluent phrasing for native readers of each language.""".format(min=MIN_POINTS, max=MAX_POINTS)

POINT = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "refs": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["text", "refs"],
    "additionalProperties": False,
}
VERSION = {
    "type": "object",
    "properties": {
        "headline": {"type": "string"},
        "points": {"type": "array", "items": POINT},
    },
    "required": ["headline", "points"],
    "additionalProperties": False,
}
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {lang: VERSION for lang in LANGS},
    "required": LANGS,
    "additionalProperties": False,
}


def recent_items(doc, now, hours=LOOKBACK_HOURS):
    """What the briefing may draw on: items published or first seen in the
    lookback window, the discussed ones first."""
    cutoff = radar.iso(now - dt.timedelta(hours=hours))
    src = {s["id"]: s for s in doc["sources"]}
    picked = [i for i in doc["items"] if max(i["published"], i.get("first_seen", "")) >= cutoff]
    picked.sort(key=lambda i: (len(i.get("also", [])), i.get("points", 0), i["published"]), reverse=True)
    out = []
    for i in picked[:MAX_ITEMS]:
        row = {"id": i["id"], "source": src.get(i["source"], {}).get("name", i["source"]),
               "section": i["section"], "title": i["title"], "published": i["published"]}
        if i.get("summary"):
            row["summary"] = i["summary"][:240]
        for k in ("points", "comments", "kind"):
            if i.get(k):
                row[k] = i[k]
        if i.get("also"):
            row["also_in"] = [src.get(s, {}).get("name", s) for s in i["also"]]
        out.append(row)
    return out


def recent_models(doc, now, hours=48):
    cutoff = radar.iso(now - dt.timedelta(hours=hours))
    return [{"id": "model:" + m["id"], "name": m["name"], "provider": m["provider"],
             "open_weights": bool(m.get("open_weights")), "context": m.get("context"),
             "usd_per_mtok_in": m["price_in"], "usd_per_mtok_out": m["price_out"]}
            for m in doc.get("models", {}).get("new", []) if m["created"] >= cutoff]


def build_prompt(doc, now):
    items, models = recent_items(doc, now), recent_models(doc, now)
    payload = {"date": now.strftime("%Y-%m-%d"), "items": items, "new_models": models}
    return (
        "Today's collected items as JSON. Cite items by their id; a new model can be cited as "
        "its id (\"model:...\").\n\n" + json.dumps(payload, ensure_ascii=False, indent=0)
    ), items, models


def call_claude(prompt, client=None):
    """One structured-output request; returns (parsed JSON, model that served it)."""
    if client is None:
        import anthropic  # only this script needs the SDK
        client = anthropic.Anthropic()
    # Streaming: nine languages of output is long enough to risk a plain
    # request's HTTP timeout. fallbacks="default" re-runs a request the
    # model's safety classifiers decline on Anthropic's recommended fallback
    # model instead of failing the morning's briefing.
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=32000,
        system=SYSTEM,
        thinking={"type": "adaptive"},
        output_config={"effort": "high", "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        msg = stream.get_final_message()
    if msg.stop_reason == "refusal":
        raise RuntimeError("declined: %s" % getattr(msg.stop_details, "category", None))
    if msg.stop_reason == "max_tokens":
        raise RuntimeError("output cut off at max_tokens")
    text = next(b.text for b in msg.content if b.type == "text")
    return json.loads(text), msg.model


def clean(out, valid_ids):
    """Keep only points whose refs resolve; drop the unresolvable refs. The
    same point index is dropped in every language, so versions stay aligned."""
    en = out["en"]["points"]
    keep = []
    for n, p in enumerate(en):
        refs = [r for r in p["refs"] if r in valid_ids]
        if refs:
            keep.append((n, refs))
    if not keep:
        raise RuntimeError("no point cites a known item")
    langs = {}
    for lang in LANGS:
        v = out[lang]
        pts = v["points"]
        langs[lang] = {
            "headline": v["headline"].strip(),
            "points": [{"text": pts[n]["text"].strip() if n < len(pts) else en[n]["text"].strip(), "refs": refs}
                       for n, refs in keep],
        }
    return langs


def refs_index(doc, items, models):
    """id -> {title, url, source} for everything a briefing may cite, so the
    archive can render citations after the items themselves age out."""
    by_id = {i["id"]: i for i in doc["items"]}
    src = {s["id"]: s["name"] for s in doc["sources"]}
    out = {}
    for i in items:
        full = by_id[i["id"]]
        out[i["id"]] = {"title": full["title"], "url": full["url"], "source": src.get(full["source"], full["source"])}
    for m in doc.get("models", {}).get("new", []):
        key = "model:" + m["id"]
        if any(x["id"] == key for x in models):
            out[key] = {"title": m["name"], "url": m["url"], "source": m["provider"]}
    return out


def make_digest(doc, now, client=None):
    prompt, items, models = build_prompt(doc, now)
    if not items and not models:
        raise RuntimeError("nothing collected in the last %d hours" % LOOKBACK_HOURS)
    out, served_by = call_claude(prompt, client)
    index = refs_index(doc, items, models)
    langs = clean(out, set(index))
    cited = {r for p in langs["en"]["points"] for r in p["refs"]}
    return {
        "date": now.strftime("%Y-%m-%d"),
        "generated": radar.iso(now),
        "model": served_by,
        "lang": langs,
        "refs": {k: v for k, v in index.items() if k in cited},
    }


def load_archive(path=ARCHIVE):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return {"schema_version": 1, "digests": []}


def save(doc, digest, out=radar.OUT, archive=ARCHIVE):
    doc["digest"] = digest
    arch = load_archive(archive)
    arch["digests"] = [digest] + [d for d in arch["digests"] if d["date"] != digest["date"]]
    arch["digests"] = arch["digests"][:ARCHIVE_KEEP]
    schema = json.loads(radar.SCHEMA.read_text())
    errors = radar.validate(doc, schema)
    for n, d in enumerate(arch["digests"]):
        errors += radar.validate(d, schema["properties"]["digest"], "digests[%d]" % n)
    if errors:
        raise SystemExit("not written -- does not match schema.json:\n  " + "\n  ".join(errors[:20]))
    out.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    archive.write_text(json.dumps(arch, indent=1, ensure_ascii=False) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--force", action="store_true", help="write a new briefing even if today's exists")
    ap.add_argument("--dry-run", action="store_true", help="print the prompt and exit")
    a = ap.parse_args(argv)
    now = radar.now_utc()
    doc = json.loads(radar.OUT.read_text())
    if a.dry_run:
        prompt, items, models = build_prompt(doc, now)
        print(SYSTEM, "\n\n", prompt[:3000], "\n...\n%d items, %d models" % (len(items), len(models)))
        return 0
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("no ANTHROPIC_API_KEY: skipping the briefing")
        return 0
    if (doc.get("digest") or {}).get("date") == now.strftime("%Y-%m-%d") and not a.force:
        print("today's briefing already exists")
        return 0
    try:
        digest = make_digest(doc, now)
    except Exception as e:  # noqa: BLE001 -- a failed briefing must not fail the refresh
        print("briefing failed: %s: %s" % (type(e).__name__, e))
        return 0
    save(doc, digest)
    print("briefing: %s (%d points, %s)" % (digest["lang"]["en"]["headline"], len(digest["lang"]["en"]["points"]), digest["model"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
