"""Turn export originals into the web files the site serves.

Every derivative is named after the hash of its source plus the profile
version below, so a second run over the same export re-uses what is already on
disk and uploads nothing. Bump PROFILE_VERSION to force a re-encode of
everything (new sizes, different quality, a codec change).
"""

import contextlib
import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

PROFILE_VERSION = 1

IMAGE_MAX = 1600  # long edge of the full-size image the lightbox shows
THUMB_MAX = 600  # long edge of the grid thumbnail
IMAGE_QUALITY = 82
THUMB_QUALITY = 78

VIDEO_MAX_HEIGHT = 720
VIDEO_CRF = 23
VIDEO_AUDIO_BITRATE = "128k"


@dataclass
class Derived:
    """Web files for one source photo or video, as S3-relative keys."""

    kind: str
    key: str  # the image itself, or the video
    thumb_key: str
    poster_key: str | None
    width: int
    height: int
    duration: float | None


class ToolMissing(RuntimeError):
    pass


def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed: {proc.stderr.strip()[:500]}")


def ffprobe_video(path: Path) -> tuple[int, int, float]:
    """Return (width, height, seconds) for a video."""
    proc = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height:format=duration",
            "-of", "json", str(path),
        ],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {path.name}: {proc.stderr.strip()[:300]}")
    data = json.loads(proc.stdout)
    stream = (data.get("streams") or [{}])[0]
    duration = float((data.get("format") or {}).get("duration") or 0.0)
    return int(stream.get("width") or 0), int(stream.get("height") or 0), duration


@contextlib.contextmanager
def open_image(src: Path):
    """Open an image, falling back to ffmpeg for anything Pillow can't read.

    Instagram hands back whatever was uploaded, and an iPhone-era archive can
    contain HEIC. Pillow needs a plugin for that which isn't a dependency
    here, but ffmpeg already is, so it decodes to a temporary PNG first.
    """
    try:
        from PIL import Image
    except ImportError as exc:  # pragma: no cover - depends on the venv
        raise ToolMissing("Pillow is not installed; run `make media-deps`") from exc

    try:
        im = Image.open(src)
        im.load()
    except Exception:
        handle, tmp_name = tempfile.mkstemp(suffix=".png")
        os.close(handle)
        tmp = Path(tmp_name)
        try:
            _run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error",
                  "-i", str(src), "-map_metadata", "-1", str(tmp)])
            with Image.open(tmp) as im:
                im.load()
                yield im
        finally:
            tmp.unlink(missing_ok=True)
        return

    try:
        yield im
    finally:
        im.close()


def _save_image(src: Path, dest: Path, max_edge: int, quality: int) -> tuple[int, int]:
    """Resize with Pillow, dropping every scrap of metadata on the way.

    Stripping EXIF is the point as much as the resize is: export originals can
    still carry GPS coordinates, and these files end up on a public CDN.
    """
    from PIL import Image, ImageOps

    with open_image(src) as im:
        im = ImageOps.exif_transpose(im)  # bake in rotation before dropping EXIF
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        im.thumbnail((max_edge, max_edge), Image.LANCZOS)
        dest.parent.mkdir(parents=True, exist_ok=True)
        clean = Image.new(im.mode, im.size)
        clean.putdata(list(im.getdata()))
        clean.save(dest, format="JPEG", quality=quality, optimize=True, progressive=True)
        return im.size


def _encode_video(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    _run([
        "ffmpeg", "-nostdin", "-y", "-loglevel", "error",
        "-i", str(src),
        # Even dimensions, never upscaled, capped at 720 tall.
        "-vf", f"scale='trunc(iw*min(1,{VIDEO_MAX_HEIGHT}/ih)/2)*2':"
               f"'trunc(ih*min(1,{VIDEO_MAX_HEIGHT}/ih)/2)*2'",
        "-c:v", "libx264", "-preset", "medium", "-crf", str(VIDEO_CRF),
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", VIDEO_AUDIO_BITRATE,
        "-map_metadata", "-1",  # drops creation time and location
        "-movflags", "+faststart",  # first frame without fetching the whole file
        str(dest),
    ])


def _extract_frame(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    _run([
        "ffmpeg", "-nostdin", "-y", "-loglevel", "error",
        "-i", str(src), "-frames:v", "1", "-map_metadata", "-1", str(dest),
    ])


class Lock:
    """Remembers what has already been derived, keyed by source hash."""

    def __init__(self, path: Path):
        self.path = path
        self.data: dict[str, dict] = {}
        if path.exists():
            try:
                self.data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self.data = {}

    def key(self, sha256: str) -> str:
        return f"{sha256}:{PROFILE_VERSION}"

    def get(self, sha256: str) -> dict | None:
        return self.data.get(self.key(sha256))

    def put(self, sha256: str, record: dict) -> None:
        self.data[self.key(sha256)] = record

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self.data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


def derive(media, item_id: str, outdir: Path, prefix: str, lock: Lock) -> Derived:
    """Build (or re-use) the web files for one photo or video."""
    stem = media.sha256[:12]
    base = f"{prefix}/{item_id}"

    cached = lock.get(media.sha256)
    if cached is not None:
        files = [outdir / item_id / Path(k).name for k in cached["files"]]
        if all(f.exists() for f in files):
            return Derived(
                kind=cached["kind"],
                key=f"{base}/{cached['name']}",
                thumb_key=f"{base}/{cached['thumb']}",
                poster_key=f"{base}/{cached['poster']}" if cached.get("poster") else None,
                width=cached["width"],
                height=cached["height"],
                duration=cached.get("duration"),
            )

    dest_dir = outdir / item_id

    if media.kind == "photo":
        name, thumb = f"{stem}.jpg", f"{stem}-t.jpg"
        width, height = _save_image(media.path, dest_dir / name, IMAGE_MAX, IMAGE_QUALITY)
        _save_image(media.path, dest_dir / thumb, THUMB_MAX, THUMB_QUALITY)
        record = {
            "kind": "photo", "name": name, "thumb": thumb, "poster": None,
            "width": width, "height": height,
            "files": [name, thumb],
        }
    else:
        name = f"{stem}.mp4"
        poster, thumb = f"{stem}-p.jpg", f"{stem}-t.jpg"
        _encode_video(media.path, dest_dir / name)
        width, height, duration = ffprobe_video(dest_dir / name)

        frame = dest_dir / f"{stem}-frame.png"
        _extract_frame(dest_dir / name, frame)
        _save_image(frame, dest_dir / poster, IMAGE_MAX, IMAGE_QUALITY)
        _save_image(frame, dest_dir / thumb, THUMB_MAX, THUMB_QUALITY)
        frame.unlink(missing_ok=True)

        record = {
            "kind": "video", "name": name, "thumb": thumb, "poster": poster,
            "width": width, "height": height, "duration": round(duration, 2),
            "files": [name, thumb, poster],
        }

    lock.put(media.sha256, record)
    return Derived(
        kind=record["kind"],
        key=f"{base}/{record['name']}",
        thumb_key=f"{base}/{record['thumb']}",
        poster_key=f"{base}/{record['poster']}" if record.get("poster") else None,
        width=record["width"],
        height=record["height"],
        duration=record.get("duration"),
    )
