"""Original background music for videos that have no sound.

Every track here is composed by this code — chords, arpeggios, bass, drums
and reverb synthesised from sine waves and seeded noise — so it is owned
outright: royalty-free, no licence to track, no attribution, nothing
downloaded. Rendering is deterministic: the same TRACK_VERSION produces the
same WAV bytes, and the same clip always gets the same song at the same
offset.

    python3 -m igmedia.music build/music     # render the six original tracks
"""

import hashlib
import json
import math
import os
import wave
from dataclasses import dataclass
from pathlib import Path

import numpy as np

TRACK_VERSION = 2  # 2: seamless loop. Bump to re-render every track (and re-mix every clip)
RATE = 44_100


@dataclass(frozen=True)
class Track:
    id: str
    title: str
    root: int            # MIDI note of the key centre
    progression: tuple   # chords as (semitones above root, quality)
    bpm: int
    drums: bool
    arp: str             # "up" | "updown" | "broken"
    brightness: float    # 0..1, how open the pad's filter is
    seed: int


# The six tracks clips shared before every video got its own song; their
# chord progressions seed the per-video songs below.
TRACKS = (
    Track("t1", "Sunlit", 60, ((0, "maj"), (7, "maj"), (9, "min"), (5, "maj")), 96, True, "up", 0.55, 11),
    Track("t2", "Drift", 57, ((0, "min7"), (8, "maj7"), (3, "maj"), (10, "maj")), 80, False, "updown", 0.35, 23),
    Track("t3", "Harbor", 62, ((0, "maj7"), (4, "min7"), (5, "maj7"), (7, "dom7")), 100, True, "broken", 0.5, 37),
    Track("t4", "Night Ride", 64, ((0, "min"), (10, "maj"), (8, "maj"), (10, "maj")), 108, True, "up", 0.45, 41),
    Track("t5", "Slow Morning", 65, ((0, "maj7"), (-1, "min7"), (-3, "min7"), (-5, "maj7")), 78, True, "updown", 0.4, 53),
    Track("t6", "Open Road", 67, ((0, "maj"), (5, "maj"), (9, "min"), (7, "maj")), 104, True, "broken", 0.6, 67),
)

QUALITIES = {
    "maj": (0, 4, 7), "min": (0, 3, 7),
    "maj7": (0, 4, 7, 11), "min7": (0, 3, 7, 10), "dom7": (0, 4, 7, 10),
}

# Song form in bars: pad alone, then arpeggio and bass, then drums, then out.
# It opens and closes on the pad alone, so the loop point is gentle.
SECTIONS = (("intro", 8), ("verse", 16), ("chorus", 16), ("outro", 8))
BARS_PER_CHORD = 2


def midi_hz(note: float) -> float:
    return 440.0 * 2 ** ((note - 69) / 12)


def _env(n: int, attack: float, release: float) -> np.ndarray:
    """Linear attack, exponential tail — soft edges, no clicks."""
    t = np.arange(n) / RATE
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    r = np.exp(-np.maximum(t - attack, 0) / max(release, 1e-4))
    return a * r


def _tone(freq: float, seconds: float, harmonics=(1.0, 0.35, 0.12), detune=0.0) -> np.ndarray:
    t = np.arange(int(seconds * RATE)) / RATE
    out = np.zeros_like(t)
    for k, amp in enumerate(harmonics, start=1):
        out += amp * np.sin(2 * np.pi * freq * k * (1 + detune) * t)
    return out


def _add(buf: np.ndarray, start: int, sig: np.ndarray, pan: float = 0.0) -> None:
    """Mix a mono signal into the stereo buffer at a sample offset, with pan."""
    end = min(start + len(sig), buf.shape[0])
    if end <= start:
        return
    sig = sig[: end - start]
    left, right = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
    buf[start:end, 0] += sig * left
    buf[start:end, 1] += sig * right


def _lowpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    """A two-pole low-pass applied in the frequency domain — the response of
    two cascaded RC stages, without a per-sample Python loop."""
    size = 1 << len(x).bit_length()
    freqs = np.fft.rfftfreq(size, 1 / RATE)
    response = 1 / (1 + 1j * freqs / cutoff) ** 2
    return np.fft.irfft(np.fft.rfft(x, size, axis=0) * response[:, None], size, axis=0)[: len(x)]


def _reverb(buf: np.ndarray, seconds: float, mix: float, rng: np.random.Generator) -> np.ndarray:
    """Convolve with a synthetic room: decaying stereo noise, darkened."""
    n = int(seconds * RATE)
    decay = np.exp(-6.0 * np.arange(n) / n)
    ir = rng.standard_normal((n, 2)) * decay[:, None]
    ir = np.cumsum(ir, axis=0) * 0.02          # integrate: tilt toward low end
    ir -= ir.mean(axis=0)
    ir /= np.abs(ir).sum(axis=0).max() / 4
    size = 1 << (len(buf) + n).bit_length()
    wet = np.fft.irfft(np.fft.rfft(buf, size, axis=0) * np.fft.rfft(ir, size, axis=0),
                       size, axis=0)[: len(buf) + n]
    dry = np.vstack([buf, np.zeros((n, 2))])
    return (1 - mix) * dry + mix * wet


def render(track: Track) -> np.ndarray:
    """The whole track as float stereo in [-1, 1], ready to loop."""
    rng = np.random.default_rng(track.seed)
    beat = 60.0 / track.bpm
    bar = 4 * beat
    total_bars = sum(b for _, b in SECTIONS)
    length = int(total_bars * bar * RATE)
    # Room past the end for notes that are still ringing when the form ends;
    # it's folded back onto the start below, so nothing is ever cut off.
    room = length + int(3.0 * RATE)
    pad = np.zeros((room, 2))
    arp = np.zeros((room, 2))
    bass = np.zeros((room, 2))
    drums = np.zeros((room, 2))

    section_of_bar = []
    for name, bars in SECTIONS:
        section_of_bar += [name] * bars

    for bar_index in range(total_bars):
        chord_index = (bar_index // BARS_PER_CHORD) % len(track.progression)
        offset, quality = track.progression[chord_index]
        notes = [track.root + offset + i for i in QUALITIES[quality]]
        section = section_of_bar[bar_index]
        bar_start = int(bar_index * bar * RATE)

        # Pad: the chord, once per chord change, detuned left and right.
        if bar_index % BARS_PER_CHORD == 0:
            dur = BARS_PER_CHORD * bar + 1.2
            for k, note in enumerate(notes):
                f = midi_hz(note - 12 if k == 0 else note)
                env = _env(int(dur * RATE), 1.1, dur * 0.9)
                for pan, det in ((-0.6, -0.003), (0.6, 0.003)):
                    _add(pad, bar_start, _tone(f, dur, (1, 0.25, 0.08), det) * env * 0.09, pan)

        # Arpeggio: 8th notes over the chord, an octave up, from the verse on.
        if section in ("verse", "chorus", "outro"):
            pattern = {
                "up": [0, 1, 2, 3, 1, 2, 3, 2],
                "updown": [0, 1, 2, 3, 2, 1, 2, 3],
                "broken": [0, 2, 1, 3, 0, 2, 3, 1],
            }[track.arp]
            for step in range(8):
                idx = pattern[step] % len(notes)
                f = midi_hz(notes[idx] + 12)
                start = bar_start + int(step * beat / 2 * RATE)
                vel = 0.11 * (1.0 if step % 2 == 0 else 0.75) * (0.8 + 0.2 * rng.random())
                sig = _tone(f, 0.9, (1, 0.5, 0.2, 0.08)) * _env(int(0.9 * RATE), 0.004, 0.22)
                _add(arp, start, sig * vel, pan=(-0.35 if step % 2 else 0.35))

        # Bass: root on beats 1 and 3, from the verse on.
        if section in ("verse", "chorus"):
            for b in (0, 2):
                f = midi_hz(track.root + offset - 24)
                start = bar_start + int(b * beat * RATE)
                sig = _tone(f, beat * 1.9, (1, 0.3)) * _env(int(beat * 1.9 * RATE), 0.01, beat)
                _add(bass, start, sig * 0.22)

        # Drums in the chorus only: soft kick, clap, closed hat.
        if track.drums and section == "chorus":
            for b in range(4):
                start = bar_start + int(b * beat * RATE)
                if b in (0, 2):
                    n = int(0.35 * RATE)
                    t = np.arange(n) / RATE
                    sweep = 2 * np.pi * np.cumsum(45 + 75 * np.exp(-t * 30)) / RATE
                    _add(drums, start, np.sin(sweep) * np.exp(-t * 9) * 0.35)
                if b in (1, 3):
                    n = int(0.18 * RATE)
                    noise = rng.standard_normal(n) * np.exp(-np.arange(n) / RATE * 22)
                    _add(drums, start, np.diff(noise, prepend=0) * 0.05, pan=0.1)
                for half in (0, 1):
                    n = int(0.05 * RATE)
                    hat = np.diff(rng.standard_normal(n), prepend=0) * np.exp(-np.arange(n) / RATE * 70)
                    _add(drums, start + int(half * beat / 2 * RATE), hat * 0.025, pan=-0.3)

    # Warm the pad according to the track's brightness, then mix and verb.
    pad = _lowpass(pad, 900 + 2600 * track.brightness)
    mix = pad + arp + bass * 0.9 + drums
    wet = _reverb(mix, 2.4, 0.28, rng)

    # Fold everything past the end — ringing notes and the reverb tail —
    # back onto the start. The form opens on near-silence, so the start then
    # continues exactly where the end left off and the loop has no seam.
    tail = wet[length:]
    out = wet[:length].copy()
    out[: len(tail)] += tail

    out -= out.mean(axis=0)
    out = np.tanh(out * 1.4) / np.tanh(1.4)       # gentle limiting
    peak = np.abs(out).max()
    return out * (0.89 / peak) if peak > 0 else out  # -1 dBFS


def write_wav(path: Path, audio: np.ndarray) -> None:
    pcm = (np.clip(audio, -1, 1) * 32767).astype("<i2")
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm.tobytes())


def track_path(directory: Path, track: Track) -> Path:
    return Path(directory) / f"{track.id}-v{TRACK_VERSION}.wav"


def duration(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()


# --- one song per video -------------------------------------------------------
#
# Never the same song for two videos (B, 2026-10-06). The six TRACKS above are
# kept for the clips published before that rule; every clip given music since
# gets its own song, built from a seed, whose key + progression no other clip
# on this site has used. The choice is recorded in the music index shared by
# every project (pfeilbr/media's igc.produce.music uses the same file), with a
# conditional write so parallel sessions never pick the same one.

LEDGER = os.environ.get("MUSIC_LEDGER", "s3://com.brianpfeil.media/music/ledger.jsonl")
STYLE = "site-media"
ROOTS = tuple(range(55, 68))  # G3..G4: thirteen key centres
PROGRESSIONS = tuple(t.progression for t in TRACKS) + (
    ((0, "min7"), (5, "min7"), (10, "maj"), (3, "maj7")),
    ((0, "maj"), (9, "min"), (5, "maj"), (7, "dom7")),
    ((0, "min"), (8, "maj"), (10, "maj"), (7, "min")),
    ((0, "maj7"), (2, "min7"), (4, "min7"), (5, "maj7")),
)
_WORDS_A = ("Amber", "Quiet", "Golden", "Silver", "Low", "Bright", "Late", "Early", "Long",
            "Still", "Easy", "Blue", "Warm", "Clear", "Soft", "High")
_WORDS_B = ("Tide", "Trail", "Light", "Current", "Ridge", "Harbor", "Street", "Field",
            "Hour", "Air", "Line", "Shore", "Pines", "Water", "Season", "Signal")


def track_from_seed(seed: int) -> Track:
    """A whole song from one number: key, chords, tempo, arpeggio and tone."""
    rng = np.random.default_rng(seed)
    key = int(rng.integers(len(ROOTS)))
    prog = int(rng.integers(len(PROGRESSIONS)))
    return Track(
        id=f"t{seed:08x}",
        title=f"{_WORDS_A[int(rng.integers(len(_WORDS_A)))]} {_WORDS_B[int(rng.integers(len(_WORDS_B)))]}",
        root=ROOTS[key],
        progression=PROGRESSIONS[prog],
        bpm=int(rng.integers(76, 112)),
        drums=bool(rng.random() < 0.8),
        arp=("up", "updown", "broken")[int(rng.integers(3))],
        brightness=round(float(rng.uniform(0.3, 0.65)), 2),
        seed=seed,
    )


def signature(seed: int) -> tuple[int, int]:
    rng = np.random.default_rng(seed)
    return int(rng.integers(len(ROOTS))), int(rng.integers(len(PROGRESSIONS)))


def _s3_parts(url: str) -> tuple[str, str]:
    bucket, _, key = url[len("s3://"):].partition("/")
    return bucket, key


def _load(path) -> tuple[list[dict], str | None, str]:
    """Rows, a version tag for the conditional write, and the raw text."""
    path = str(path)
    if path.startswith("s3://"):
        import subprocess
        import tempfile
        bucket, key = _s3_parts(path)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "ledger.jsonl"
            proc = subprocess.run(["aws", "s3api", "get-object", "--bucket", bucket, "--key", key, str(out)],
                                  capture_output=True, text=True)
            if proc.returncode != 0:
                if "NoSuchKey" in proc.stderr:
                    return [], None, ""
                raise RuntimeError(f"music ledger {path}: {proc.stderr.strip()}")
            tag = json.loads(proc.stdout)["ETag"]
            raw = out.read_text()
    else:
        p = Path(path)
        raw = p.read_text() if p.exists() else ""
        tag = hashlib.sha256(raw.encode()).hexdigest() if p.exists() else None
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    return rows, tag, raw


def _save(path, raw: str, tag: str | None) -> bool:
    """Write only if nobody else wrote since we read; False means read again."""
    path = str(path)
    if path.startswith("s3://"):
        import subprocess
        import tempfile
        bucket, key = _s3_parts(path)
        with tempfile.TemporaryDirectory() as tmp:
            body = Path(tmp) / "ledger.jsonl"
            body.write_text(raw)
            cond = ["--if-match", tag] if tag else ["--if-none-match", "*"]
            proc = subprocess.run(["aws", "s3api", "put-object", "--bucket", bucket, "--key", key,
                                   "--body", str(body), "--content-type", "application/x-ndjson", *cond],
                                  capture_output=True, text=True)
        if proc.returncode == 0:
            return True
        if "PreconditionFailed" in proc.stderr or "ConditionalRequestConflict" in proc.stderr:
            return False
        raise RuntimeError(f"music ledger {path}: {proc.stderr.strip()}")
    p = Path(path)
    current = p.read_text() if p.exists() else None
    if (hashlib.sha256(current.encode()).hexdigest() if current is not None else None) != tag:
        return False
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(raw)
    return True


def assign(video: str, path=None) -> Track:
    """The song for one video (a stable name). A video keeps its song; a new
    one gets a seed whose key + progression no other site clip has used (once
    all are used, at least a seed nobody has, so melody and groove are new)."""
    path = path or LEDGER
    for _ in range(8):
        rows, tag, raw = _load(path)
        for r in rows:
            if r.get("video") == video and r.get("style") == STYLE:
                return track_from_seed(int(r["seed"]))
        used_sigs = {(r.get("key"), r.get("prog")) for r in rows if r.get("style") == STYLE}
        used_seeds = {r.get("seed") for r in rows if r.get("style") == STYLE}
        start = int(hashlib.sha256(f"{STYLE}:{video}".encode()).hexdigest()[:8], 16)
        seed = fallback = None
        for i in range(5000):
            s = (start + i) % 2**32
            if s in used_seeds:
                continue
            fallback = s if fallback is None else fallback
            if signature(s) not in used_sigs:
                seed = s
                break
        seed = fallback if seed is None else seed
        key, prog = signature(seed)
        import datetime as dt
        row = {"at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "key": key,
               "prog": prog, "seed": seed, "style": STYLE, "video": video}
        text = raw if not raw or raw.endswith("\n") else raw + "\n"
        if _save(path, text + json.dumps(row) + "\n", tag):
            return track_from_seed(seed)
    raise RuntimeError(f"music ledger {path}: too many concurrent writers")


def ensure_track(directory: Path, track: Track) -> Path:
    path = track_path(directory, track)
    if not path.exists():
        write_wav(path, render(track))
    return path


def offset_for(key: str, seconds: float) -> float:
    """Where in the song a clip starts, so it doesn't always open on the intro."""
    h = int(hashlib.sha256(key.encode()).hexdigest(), 16)
    span = max(seconds - 8.0, 1.0)
    return round(h % int(span * 10) / 10, 1)


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "build/music")
    for t in TRACKS:
        p = ensure_track(out, t)
        print(f"{t.id}: {p} ({duration(p):.0f}s)")
