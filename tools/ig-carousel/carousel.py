#!/usr/bin/env python3
"""Instagram text carousels of a post, as 1080x1350 PNGs for review.

Two outputs, both under tools/ig-carousel/build/ (gitignored):

  condensed/   one carousel, hand-written slides from condensed.md
  series/      the full post, split at its sections into parts of at most
               20 slides (Instagram's carousel limit), each with a cover
               and an end slide

plus review.html (every slide and caption on one page) and a contact
sheet PNG per carousel. Slides are laid out by headless Chrome's print
paginated in the browser (one PDF page = one slide) and rasterised with pdftoppm.

Needs Google Chrome and poppler (pdftoppm); ImageMagick for contact sheets.
"""
from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
POST = REPO / "content/post/living-with-bipolar/index.md"
CONDENSED = HERE / "condensed.md"
CAPTIONS = HERE / "captions.md"
OUT = HERE / "build"

W, H = 1080, 1350
MAX_SLIDES = 20
CAPTION_LIMIT = 2200
TITLE = "The highs, the lows, and everything in between"
SUBTITLE = "My life with bipolar"
HANDLE = "brianpfeil.com"

# Sections of the post (by "## " heading) that make up each part of the series.
PARTS = [
    ["", "Where it starts: my father", "The part that feels good", "The part that doesn't"],
    ["The people around me", "Getting help, and how long it took",
     "Medications: trial, error, and patience"],
    ["Work, brain fog, and leaves of absence", "The label, and whether it's right"],
    ["What I wish someone had told me", "If you're in it right now", "~closing"],
]

# Lines of the post that point at the web page; on a carousel they need other words.
REWRITES = {
    "If you are in crisis right now, skip to [the end](#if-youre-in-it-right-now). "
    "There are numbers there you can call or text tonight.":
        "If you are in crisis right now, call or text **988** (U.S.) tonight. "
        "More numbers are in Part 4.",
    "This site is mostly code: AWS experiments, architecture notes, side projects. "
    "This post is different. It's the first thing I've written here that's about me "
    "rather than about something I built.":
        "Most of what I share is code: AWS experiments, architecture notes, side projects. "
        "This is different. It's the first thing I've written that's about me "
        "rather than about something I built.",
    "reach out. My LinkedIn and X are on the [about page](/about/).":
        "message me here.",
}

CRISIS = "In crisis? Call or text 988 (U.S.) · findahelpline.com"

CHROME = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
          "google-chrome", "chromium", "chromium-browser"]


# --- Markdown (the small subset the post uses) ------------------------------

def inline(text: str) -> str:
    """Escape, then bold/italic; a link keeps only its text (nothing is clickable)."""
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: link_text(m[1], m[2]), text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return text


def link_text(label: str, url: str) -> str:
    """A site-relative link becomes its full address, since a slide can't be clicked."""
    return f"{HANDLE}{url.rstrip('/')}" if url.startswith("/") else label


def to_html(md: str) -> str:
    out, para, items = [], [], []

    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            items.clear()

    for raw in md.splitlines():
        line = raw.strip()
        if not line or line == "---" or line.startswith("<!--"):
            flush()
        elif m := re.match(r"(#{1,3}) (.*)", line):
            flush()
            out.append(f"<h{len(m[1])}>{inline(m[2])}</h{len(m[1])}>")
        elif line.startswith("- "):
            if para:
                flush()
            items.append(line[2:])
        else:
            if items:
                flush()
            para.append(line)
    flush()
    return "\n".join(out)


def post_body(path: Path = POST) -> str:
    text = path.read_text()
    body = text.split("+++", 2)[2] if text.startswith("+++") else text
    for old, new in REWRITES.items():
        if old not in body:
            raise SystemExit(f"rewrite no longer matches the post: {old[:60]}…")
        body = body.replace(old, new)
    return body


def sections(body: str) -> dict[str, str]:
    """Heading -> markdown. "" is the intro, "~closing" what follows the last "---"."""
    body, _, closing = body.rpartition("\n---\n")
    found, name, buf = {}, "", []
    for line in body.splitlines():
        if line.startswith("## "):
            found[name] = "\n".join(buf)
            name, buf = line[3:].strip(), [line]
        else:
            buf.append(line)
    found[name] = "\n".join(buf)
    found["~closing"] = closing
    return found


def series(body: str) -> list[str]:
    secs = sections(body)
    used = [s for part in PARTS for s in part]
    missing = set(secs) - set(used)
    unknown = set(used) - set(secs)
    if missing or unknown:
        raise SystemExit(f"PARTS is out of step with the post: missing {sorted(missing)}, "
                         f"unknown {sorted(unknown)}")
    return ["\n\n".join(secs[s] for s in part) for part in PARTS]


def condensed_slides(path: Path = CONDENSED) -> list[str]:
    text = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.S)
    return [s.strip() for s in re.split(r"(?m)^===\s*$", text) if s.strip()]


def captions(path: Path = CAPTIONS) -> dict[str, str]:
    """"## key" headings in captions.md -> caption text."""
    found, key = {}, None
    for line in path.read_text().splitlines():
        if m := re.match(r"## (\S+)$", line):
            key = m[1]
            found[key] = []
        elif key:
            found[key].append(line)
    return {k: "\n".join(v).strip() for k, v in found.items()}


# --- Slides ------------------------------------------------------------------

CSS = f"""
@page {{ size: {W}px {H}px; margin: 0; }}
* {{ box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin: 0; font-family: Inter, -apple-system, system-ui, sans-serif; color: #24211d;
       font-size: var(--fs); line-height: 1.48; }}
#src {{ display: none; }}
.slide {{ width: {W}px; height: {H}px; position: relative; overflow: hidden; background: #fbf8f3;
         break-after: page; display: flex; flex-direction: column; }}
.slide .body {{ flex: 1; padding: 120px 96px 0; overflow: hidden; min-height: 0; }}
.slide .foot {{ height: 150px; padding: 44px 96px 0; display: flex; justify-content: space-between;
               font-size: 24px; font-weight: 500; color: #8a8378; }}
p {{ margin: 0 0 0.7em; }}
ul {{ margin: 0 0 0.7em; padding-left: 1.1em; }}
li {{ margin: 0 0 0.3em; }}
li::marker {{ color: #b0573a; }}
strong {{ font-weight: 700; color: #000; }}
em {{ font-style: italic; }}
h2 {{ font-family: "Source Serif 4", Georgia, serif; font-weight: 700; font-size: 1.55em;
     line-height: 1.15; letter-spacing: -0.01em; margin: 0 0 0.75em; color: #1b1814; }}
h2::before {{ content: ""; display: block; width: 72px; height: 6px; background: #b0573a;
             margin-bottom: 36px; border-radius: 3px; }}
h3 {{ font-weight: 700; font-size: 1.08em; margin: 1.1em 0 0.4em; color: #b0573a; }}
.body > h3:first-child {{ margin-top: 0; }}
.cover {{ background: #1f2a33; color: #f4efe6; justify-content: center; padding: 0 110px; }}
.cover h1 {{ font-family: "Source Serif 4", Georgia, serif; font-size: 92px; line-height: 1.04;
            letter-spacing: -0.02em; margin: 0 0 40px; font-weight: 700; }}
.cover .sub {{ font-size: 40px; color: #e3a587; margin: 0; font-weight: 500; }}
.cover .part {{ font-size: 28px; letter-spacing: 0.14em; text-transform: uppercase; color: #9fb0bd;
               margin: 0 0 48px; font-weight: 600; }}
.cover .by, .cover .swipe {{ position: absolute; bottom: 90px; font-size: 28px; color: #9fb0bd; }}
.cover .by {{ left: 110px; }} .cover .swipe {{ right: 110px; }}
.end .body {{ display: flex; flex-direction: column; justify-content: center; padding-bottom: 60px; }}
.end .big {{ font-family: "Source Serif 4", Georgia, serif; font-size: 64px; line-height: 1.1;
            font-weight: 700; margin: 0 0 36px; }}
.end .crisis {{ font-size: 28px; color: #6b645a; border-top: 2px solid #e4ddd1; padding-top: 28px;
               margin-top: 40px; }}
"""

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Inter:ital,wght@0,400;0,500;0,600;0,700;1,400'
         '&family=Source+Serif+4:wght@700&display=block">')

# Lays the source chunks out as fixed-size slides. Every .chunk starts a new slide;
# a block that doesn't fit moves on, and a paragraph or list too long for the space
# left is split between sentences or items, never mid-sentence. A heading or a
# lead-in ending in a colon is never the last thing on a slide.
PAGINATE = """
<script>
(async () => {
  // Load every face up front: #src is hidden, so nothing would ask for them before measuring.
  await Promise.all(['400 40px Inter', 'italic 400 40px Inter', '500 40px Inter', '600 40px Inter',
                     '700 40px Inter', '700 40px "Source Serif 4"'].map(f => document.fonts.load(f)));
  await document.fonts.ready;
  const out = document.getElementById('out');
  const foot = () => `<div class="foot"><span>HANDLE</span><span class="n"></span></div>`;
  const newSlide = (cls = '') => {
    const s = document.createElement('section');
    s.className = 'slide ' + cls;
    s.innerHTML = '<div class="body"></div>' + foot();
    out.appendChild(s);
    return s.querySelector('.body');
  };
  const fits = b => b.scrollHeight <= b.clientHeight;
  // Split between sentences: end punctuation, whitespace, then a capital. "U.S., know" stays whole.
  const sentences = html => html.split(/(?<=[.!?]['"”’)]?)\\s+(?=["“(<]?[A-Z])/).map((t, i, a) => i < a.length - 1 ? t + ' ' : t);
  // Headings, and a line introducing a list ("…to spend:"), stay with what follows.
  const isHead = el => /^H[1-6]$/.test(el.tagName) || (el.tagName === 'P' && /:\\s*$/.test(el.textContent));

  const layout = (chunk, fs) => {
    const made = [];
    const fresh = (cls = '') => { const b = newSlide(cls); b.parentNode.style.fontSize = fs + 'px'; made.push(b.parentNode); return b; };
    let body = fresh(chunk.classList.contains('end') ? 'end' : '');
    for (const block of [...chunk.children].map(b => b.cloneNode(true))) {
      body.appendChild(block);
      if (fits(body)) continue;
      body.removeChild(block);
      // Split: fill what's left of this slide, carry the rest on.
      const parts = block.tagName === 'UL' ? [...block.children].map(li => li.outerHTML)
                  : block.tagName === 'P' ? sentences(block.innerHTML) : null;
      let rest = parts;
      // A slide holding only a heading must take part of the block, even one item.
      const onlyHeads = body.children.length > 0 && [...body.children].every(isHead);
      if (parts && body.children.length) {
        const piece = block.cloneNode(false);
        body.appendChild(piece);
        let i = 0;
        for (; i < parts.length; i++) {
          piece.insertAdjacentHTML('beforeend', parts[i]);
          if (!fits(body)) { piece.innerHTML = parts.slice(0, i).join(''); break; }
        }
        // Otherwise keep at least two sentences/items on each side, or don't split at all.
        if (i < (onlyHeads ? 1 : 2) || (!onlyHeads && parts.length - i < 2)) { body.removeChild(piece); i = 0; }
        rest = parts.slice(i);
      }
      // Don't leave a heading stranded at the bottom.
      const carry = [];
      let h = body.children.length;
      while (h > 0 && isHead(body.children[h - 1])) h--;
      if (h > 0) while (body.children.length > h) carry.unshift(body.removeChild(body.lastElementChild));
      body = fresh();
      carry.forEach(h => body.appendChild(h));
      const remaining = block.cloneNode(false);
      remaining.innerHTML = rest ? rest.join('') : block.innerHTML;
      body.appendChild(remaining);
      // Still too tall for a whole slide: split again, item by item / sentence by sentence.
      while (!fits(body) && rest && rest.length > 1) {
        let k = rest.length;
        while (k > 1) { remaining.innerHTML = rest.slice(0, --k).join(''); if (fits(body)) break; }
        body = fresh();
        rest = rest.slice(k);
        const next = block.cloneNode(false);
        next.innerHTML = rest.join('');
        body.appendChild(next);
      }
    }
    const last = made[made.length - 1].querySelector('.body');
    const used = last.lastElementChild ? last.lastElementChild.getBoundingClientRect().bottom - last.getBoundingClientRect().top : 0;
    return { made, fill: used / last.clientHeight };
  };

  // A section whose last slide is nearly empty is re-laid at a nearby size.
  const base = parseFloat(getComputedStyle(document.body).fontSize);
  for (const chunk of document.querySelectorAll('#src > *')) {
    if (chunk.classList.contains('cover')) { out.appendChild(chunk.cloneNode(true)).classList.add('slide'); continue; }
    let best = null;
    for (const d of [0, 2, -2, 4, -4, 6, -6]) {
      const r = layout(chunk, base + d);
      const ok = r.made.length === 1 || r.fill >= 0.4;
      if (!best || ok || r.fill > best.fill) { if (best) best.made.forEach(s => s.remove()); best = r; }
      else r.made.forEach(s => s.remove());
      if (ok) break;
    }
  }
  const slides = [...out.children];
  slides.forEach((s, i) => { const n = s.querySelector('.n'); if (n) n.textContent = `${i + 1} / ${slides.length}`; });
  document.title = 'ready';
})();
</script>
""".replace("HANDLE", HANDLE)


def page(chunks: str, font_px: int) -> str:
    return (f"<!doctype html><html><head><meta charset=utf-8>{FONTS}"
            f"<style>{CSS}:root{{--fs:{font_px}px}}</style></head><body>"
            f'<div id="src">{chunks}</div><div id="out"></div>{PAGINATE}</body></html>')


def cover(kicker: str = "") -> str:
    kick = f'<p class="part">{html.escape(kicker)}</p>' if kicker else ""
    return (f'<section class="cover">{kick}<h1>{html.escape(TITLE)}</h1>'
            f'<p class="sub">{html.escape(SUBTITLE)}</p>'
            f'<span class="by">Brian Pfeil</span><span class="swipe">Swipe &rarr;</span></section>')


def end(big: str, line: str) -> str:
    return (f'<div class="end"><p class="big">{html.escape(big)}</p><p>{html.escape(line)}</p>'
            f'<p class="crisis">{html.escape(CRISIS)}</p></div>')


def series_html(part_md: str, n: int, total: int) -> str:
    chunks = [c for c in re.split(r"(?m)^(?=## )", part_md) if c.strip()]
    flow = "".join(f"<div>{to_html(c)}</div>" for c in chunks)
    last = (end(f"Continued in Part {n + 1}.", "Follow along, or message me if any of this sounds familiar.")
            if n < total else end("Thank you for reading.", "All four parts are on my profile."))
    return cover(f"Part {n} of {total}") + flow + last


def condensed_html(slides: list[str]) -> str:
    first, rest = slides[0], slides[1:]
    if not first.startswith("# "):
        raise SystemExit("condensed.md: the first slide must be the cover (# title)")
    return cover() + "".join(f"<div>{to_html(s)}</div>" for s in rest)


# --- Rendering ---------------------------------------------------------------

def chrome() -> str:
    for c in CHROME:
        if found := shutil.which(c) or (Path(c).exists() and c):
            return found
    raise SystemExit("Google Chrome not found")


def render(doc: str, dest: Path) -> list[Path]:
    """HTML -> PDF (Chrome) -> one PNG per page (pdftoppm). Returns the PNGs."""
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as tmp:
        src, pdf = Path(tmp) / "slides.html", Path(tmp) / "slides.pdf"
        src.write_text(doc)
        subprocess.run([chrome(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--virtual-time-budget=8000", f"--print-to-pdf={pdf}", src.as_uri()],
                       check=True, capture_output=True, timeout=180)
        missing_text(doc, pdf)
        subprocess.run(["pdftoppm", "-png", "-scale-to-x", str(W), "-scale-to-y", str(H),
                        str(pdf), str(dest / "slide")], check=True, stderr=subprocess.DEVNULL)
    pngs = sorted(dest.glob("slide-*.png"))
    for i, p in enumerate(pngs, 1):
        p.rename(dest / f"{i:02d}.png")
    return sorted(dest.glob("[0-9][0-9].png"))


def letters(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKC", text).lower())


def missing_text(doc: str, pdf: Path) -> None:
    """Every paragraph of the source must come out whole, in order, in the PDF."""
    got = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], check=True,
                         capture_output=True, text=True).stdout
    got = re.sub(rf"{re.escape(HANDLE)}[ \t]+\d+\s*/\s*\d+", "", got)  # slide footers
    got = letters(got)
    src = doc.split('<div id="src">', 1)[1].split('<div id="out">', 1)[0]
    for block in re.findall(r"<(?:p|li|h[1-3])[^>]*>(.*?)</(?:p|li|h[1-3])>", src, re.S):
        want = letters(html.unescape(re.sub(r"<[^>]+>", "", block)))
        if want and want not in got:
            raise SystemExit(f"text lost in layout: {html.unescape(re.sub(r'<[^>]+>', '', block))[:80]}…")


def contact_sheet(pngs: list[Path], dest: Path) -> None:
    if shutil.which("magick"):
        subprocess.run(["magick", "montage", *map(str, pngs), "-font", "/System/Library/Fonts/Helvetica.ttc", "-tile", "5x", "-geometry",
                        "324x405+12+12", "-background", "#d9d4cc", str(dest)], check=True)


def review_page(groups: list[tuple[str, list[Path], str]]) -> str:
    out = ["<!doctype html><meta charset=utf-8><title>Carousel review</title>",
           "<style>body{font:16px -apple-system,sans-serif;margin:24px;background:#eee}"
           "h2{margin:40px 0 8px}.row{display:flex;gap:10px;overflow-x:auto;padding-bottom:8px}"
           ".row img{width:300px;flex:none;box-shadow:0 1px 4px #0003}"
           "pre{white-space:pre-wrap;background:#fff;padding:16px;max-width:720px;"
           "font:15px/1.5 -apple-system,sans-serif}</style>",
           "<h1>Instagram carousels: review</h1>"]
    for name, pngs, caption in groups:
        out.append(f"<h2>{html.escape(name)} <small>({len(pngs)} slides, "
                   f"{len(caption)} caption chars)</small></h2><div class=row>")
        out += [f'<a href="{p.relative_to(OUT)}"><img src="{p.relative_to(OUT)}"></a>' for p in pngs]
        out.append(f"</div><pre>{html.escape(caption)}</pre>")
    return "\n".join(out)


def build() -> list[tuple[str, list[Path], str]]:
    caps = captions()
    for key, text in caps.items():
        if len(text) > CAPTION_LIMIT:
            raise SystemExit(f"caption {key} is {len(text)} chars (limit {CAPTION_LIMIT})")
    groups = []

    slides = condensed_slides()
    pngs = render(page(condensed_html(slides), 46), OUT / "condensed")
    if len(pngs) != len(slides):
        raise SystemExit(f"condensed: {len(slides)} slides came out as {len(pngs)} images; "
                         "one of them overflows, shorten it")
    groups.append(("Option 1: condensed carousel", pngs, caps.get("condensed", "")))

    parts = series(post_body())
    for n, md in enumerate(parts, 1):
        pngs = render(page(series_html(md, n, len(parts)), 38), OUT / f"series/part-{n}")
        if len(pngs) > MAX_SLIDES:
            raise SystemExit(f"series part {n} is {len(pngs)} slides (limit {MAX_SLIDES}); "
                             "move a section to another part")
        groups.append((f"Option 2: series, part {n} of {len(parts)}", pngs,
                       caps.get(f"part-{n}", "")))

    for name, pngs, _ in groups:
        contact_sheet(pngs, pngs[0].parent / "contact-sheet.png")
    (OUT / "review.html").write_text(review_page(groups))
    return groups


def main() -> int:
    for name, pngs, caption in build():
        print(f"{name}: {len(pngs)} slides, caption {len(caption)} chars  ->  "
              f"{pngs[0].parent.relative_to(REPO)}/")
    print(f"review: {(OUT / 'review.html').relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
