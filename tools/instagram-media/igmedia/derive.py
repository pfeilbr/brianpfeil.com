"""Turn export originals into the web files the site serves.

Every derivative is named after the hash of its source plus the profile
version below, so a second run over the same export re-uses what is already on
disk and uploads nothing. Bump PROFILE_VERSION to force a re-encode of
everything (new sizes, different quality, a codec change).
"""

import contextlib
import json
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

PROFILE_VERSION = 2  # 2: cap video by long edge, remux when already web-ready

IMAGE_MAX = 1600  # long edge of the full-size image the lightbox shows
THUMB_MAX = 600  # long edge of the grid thumbnail
IMAGE_QUALITY = 82
THUMB_QUALITY = 78

# Grid tiles are square and display at about 110-162 CSS px, so the grid gets
# its own square WebP crops rather than the 600px JPEG thumbnail: 360px covers
# a phone at 3x or a desktop tile at 2x, 720px anything denser.
GRID_SIZES = (360, 720)
GRID_QUALITY = 72

# Long edge, not height: capping height at 720 turned Instagram's 720x960
# portrait clips into 540x720 — smaller than what Instagram itself serves.
VIDEO_MAX_EDGE = 1280
VIDEO_CRF = 23
VIDEO_AUDIO_BITRATE = "128k"
# Above this a clip is re-encoded even if it is otherwise web-ready; a few
# short phone clips arrive at 7-8 Mbps, which is fine, but nothing needs more.
VIDEO_MAX_REMUX_BITRATE = 8_000_000


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
    grid_keys: tuple = ()  # square WebP tiles, smallest first
    color: str | None = None  # average colour, shown while a tile loads
    music: str | None = None  # title of the track mixed into a silent video


# A clip is treated as silent — and given music — when it has no audio track,
# or one whose loudest moment is quieter than this.
SILENT_BELOW_DB = -45.0
MUSIC_BITRATE = "160k"
FADE_IN, FADE_OUT = 0.8, 1.5


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


def probe_streams(path: Path) -> dict:
    """Codec, size and bitrate — enough to decide whether to remux."""
    proc = subprocess.run(
        ["ffprobe", "-v", "error",
         "-show_entries", "stream=codec_type,codec_name,width,height:format=bit_rate",
         "-of", "json", str(path)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {path.name}: {proc.stderr.strip()[:300]}")
    data = json.loads(proc.stdout)
    streams = data.get("streams") or []
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), {})
    return {
        "video": video.get("codec_name"),
        "audio": audio.get("codec_name"),  # None for a silent clip
        "width": int(video.get("width") or 0),
        "height": int(video.get("height") or 0),
        "bit_rate": int((data.get("format") or {}).get("bit_rate") or 0),
    }


def can_remux(info: dict) -> bool:
    """True when the file is already what a browser wants and only needs its
    metadata removed: H.264 video, AAC or no audio, within the size cap and a
    sane bitrate. HEVC in particular does not play everywhere."""
    return (
        info["video"] == "h264"
        and info["audio"] in ("aac", None)
        and 0 < max(info["width"], info["height"]) <= VIDEO_MAX_EDGE
        and info["bit_rate"] <= VIDEO_MAX_REMUX_BITRATE
    )


# Both paths drop global and per-stream metadata: creation time and location
# can sit on the container and on each stream.
_STRIP = ["-map_metadata", "-1", "-map_metadata:s:v", "-1", "-map_metadata:s:a", "-1",
          "-map_chapters", "-1"]


def _encode_video(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if can_remux(probe_streams(src)):
        # Copy the streams untouched: seconds instead of minutes, and no
        # generational loss on video Instagram has already compressed once.
        _run([
            "ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(src),
            "-map", "0:v:0", "-map", "0:a:0?", "-c", "copy", *_STRIP,
            "-movflags", "+faststart", str(dest),
        ])
        return

    # Even dimensions, never upscaled, long edge capped.
    scale = f"min(1,{VIDEO_MAX_EDGE}/max(iw,ih))"
    _run([
        "ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(src),
        "-map", "0:v:0", "-map", "0:a:0?",
        "-vf", f"scale='trunc(iw*{scale}/2)*2':'trunc(ih*{scale}/2)*2'",
        "-c:v", "libx264", "-preset", "medium", "-crf", str(VIDEO_CRF),
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", VIDEO_AUDIO_BITRATE,
        *_STRIP,
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


def _grid(source: Path, dest_dir: Path, stem: str) -> tuple[list[str], str]:
    """Square WebP grid tiles and the image's average colour.

    Cropped square at build time because the tile shows a square anyway —
    every pixel outside it was bytes downloaded to be hidden. Never upscaled:
    a 612px photo from 2011 gets a 612px tile, not a blurry 720.
    """
    from PIL import Image, ImageOps

    names = []
    with Image.open(source) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        side = min(im.size)
        left, top = (im.width - side) // 2, (im.height - side) // 2
        square = im.crop((left, top, left + side, top + side))
        # One pixel is the average; good enough to fill a tile while it loads.
        r, g, b = square.resize((1, 1), Image.LANCZOS).getpixel((0, 0))
        color = f"#{r:02x}{g:02x}{b:02x}"
        for size in GRID_SIZES:
            name = f"{stem}-g{size}.webp"
            tile = square.resize((min(size, side),) * 2, Image.LANCZOS) if side > size else square
            tile.save(dest_dir / name, format="WEBP", quality=GRID_QUALITY, method=6)
            names.append(name)
    return names, color


def _ensure_grid(record: dict, dest_dir: Path, stem: str) -> bool:
    """Add grid tiles to a record that predates them. True if it changed.

    Built from the full-size image (or a video's poster) already on disk, so
    adding tiles to an existing build never re-encodes a video.
    """
    if record.get("grid") and all((dest_dir / n).exists() for n in record["grid"]):
        return False
    source = dest_dir / (record["name"] if record["kind"] == "photo" else record["poster"])
    names, color = _grid(source, dest_dir, stem)
    record["grid"], record["color"] = names, color
    record["files"] = [f for f in record["files"] if f not in names] + names
    return True


def peak_db(path: Path) -> float | None:
    """Loudest moment of the first audio track, in dBFS; None if there isn't one."""
    if probe_streams(path)["audio"] is None:
        return None
    proc = subprocess.run(
        ["ffmpeg", "-nostdin", "-i", str(path), "-map", "0:a:0", "-af", "volumedetect",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    m = re.search(r"max_volume: (-?[\d.]+|-inf) dB", proc.stderr)
    if not m:
        return None
    return float("-inf") if m.group(1) == "-inf" else float(m.group(1))


_LIBRARY: dict[str, dict] = {}


def music_library(directory: Path) -> dict:
    """The rendered tracks, rendered once per run. Imported lazily so the
    photo path doesn't need numpy."""
    key = str(directory)
    if key not in _LIBRARY:
        from . import music
        paths = music.ensure_library(directory)
        _LIBRARY[key] = {"paths": paths, "seconds": {k: music.duration(v) for k, v in paths.items()}}
    return _LIBRARY[key]


def _mix_music(video: Path, track_wav: Path, offset: float, seconds: float, dest: Path) -> None:
    """Lay a looping track under a silent clip. The picture is copied untouched;
    only the audio is new, faded in and out, cut to the clip's length."""
    fade_out_at = max(0.0, seconds - FADE_OUT)
    _run([
        "ffmpeg", "-nostdin", "-y", "-loglevel", "error",
        "-i", str(video),
        "-stream_loop", "-1", "-ss", f"{offset:.1f}", "-i", str(track_wav),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", MUSIC_BITRATE,
        "-af", f"afade=t=in:st=0:d={FADE_IN},afade=t=out:st={fade_out_at:.2f}:d={FADE_OUT}",
        "-t", f"{seconds:.3f}",
        *_STRIP, "-movflags", "+faststart", str(dest),
    ])


def _ensure_sound(record: dict, dest_dir: Path, stem: str, key: str, music_dir: Path) -> bool:
    """Give a silent video music. True if the record changed.

    "Silent" is no audio track, or one that peaks below SILENT_BELOW_DB. The
    result gets a new file name: the silent version is cached for a year as
    immutable, so reusing its URL would leave visitors hearing nothing.
    """
    if record["kind"] != "video":
        return False
    current = dest_dir / record["name"]
    if record.get("sound") in ("original", "music") and current.exists():
        return False

    peak = peak_db(current)
    if peak is not None and peak >= SILENT_BELOW_DB:
        record["sound"] = "original"
        return True

    from . import music
    library = music_library(music_dir)
    track, offset = music.choose(key, library["seconds"])
    name = f"{stem}-m{track.id}v{music.TRACK_VERSION}.mp4"
    _mix_music(current, library["paths"][track.id], offset, float(record.get("duration") or 0)
               or ffprobe_video(current)[2], dest_dir / name)
    if name != record["name"]:
        current.unlink(missing_ok=True)  # the silent file; --prune drops it from the CDN
    record["files"] = [name if f == record["name"] else f for f in record["files"]]
    record["name"] = name
    record["sound"] = "music"
    record["music"] = track.title
    return True


def _derived(record: dict, base: str) -> "Derived":
    return Derived(
        kind=record["kind"],
        key=f"{base}/{record['name']}",
        thumb_key=f"{base}/{record['thumb']}",
        poster_key=f"{base}/{record['poster']}" if record.get("poster") else None,
        width=record["width"],
        height=record["height"],
        duration=record.get("duration"),
        grid_keys=tuple(f"{base}/{n}" for n in record.get("grid") or ()),
        color=record.get("color"),
        music=record.get("music"),
    )


def derive(media, item_id: str, outdir: Path, prefix: str, lock: Lock) -> Derived:
    """Build (or re-use) the web files for one photo or video."""
    stem = media.sha256[:12]
    base = f"{prefix}/{item_id}"

    dest_dir = outdir / item_id

    cached = lock.get(media.sha256)
    if cached is not None:
        base_files = [f for f in cached["files"] if f not in (cached.get("grid") or [])]
        if all((dest_dir / f).exists() for f in base_files):
            changed = _ensure_grid(cached, dest_dir, stem)
            changed = _ensure_sound(cached, dest_dir, stem, item_id, outdir.parent / "music") or changed
            if changed:
                lock.put(media.sha256, cached)
            return _derived(cached, base)

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

    _ensure_grid(record, dest_dir, stem)
    _ensure_sound(record, dest_dir, stem, item_id, outdir.parent / "music")
    lock.put(media.sha256, record)
    return _derived(record, base)
