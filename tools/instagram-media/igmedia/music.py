"""Original background music for videos that have no sound.

Every track here is composed by this code — chords, arpeggios, bass, drums
and reverb synthesised from sine waves and seeded noise — so it is owned
outright: royalty-free, no licence to track, no attribution, nothing
downloaded. Rendering is deterministic: the same TRACK_VERSION produces the
same WAV bytes, and the same clip always gets the same track at the same
offset.

    python3 -m igmedia.music build/music     # render the library
"""

import hashlib
import math
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


# Six moods, so a page of clips doesn't all share one tune.
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


def ensure_library(directory: Path) -> dict[str, Path]:
    """Render any track not already on disk; return id -> path."""
    paths = {}
    for track in TRACKS:
        path = track_path(directory, track)
        if not path.exists():
            write_wav(path, render(track))
        paths[track.id] = path
    return paths


def duration(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()


def choose(key: str, track_seconds: dict[str, float]) -> tuple[Track, float]:
    """The same key always gets the same track, starting at the same point.

    Keyed on the post, so every silent clip in one album shares a tune; the
    offset spreads clips across the track so they don't all start on the intro.
    """
    h = int(hashlib.sha256(key.encode()).hexdigest(), 16)
    track = TRACKS[h % len(TRACKS)]
    span = max(track_seconds[track.id] - 8.0, 1.0)
    offset = round((h // len(TRACKS)) % int(span * 10) / 10, 1)
    return track, offset


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "build/music")
    for tid, p in ensure_library(out).items():
        print(f"{tid}: {p} ({duration(p):.0f}s)")
