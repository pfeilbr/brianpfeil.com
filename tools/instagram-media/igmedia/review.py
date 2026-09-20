"""A local contact sheet for deciding what goes public.

Written to build/review.html and opened in a browser. It never touches the
network and is not part of the site — it exists so the approve list can be
filled in by looking at the pictures rather than at filenames.
"""

import html
import subprocess
from pathlib import Path

THUMB_MAX = 320


def _thumb(src: Path, dest: Path, kind: str) -> bool:
    if dest.exists():
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        if kind == "video":
            # One frame is enough to recognise a clip, and -ss before -i makes
            # it a seek rather than a decode of the whole file.
            subprocess.run(
                ["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", "0",
                 "-i", str(src), "-frames:v", "1", "-vf", f"scale={THUMB_MAX}:-2",
                 "-map_metadata", "-1", str(dest)],
                check=True, capture_output=True,
            )
            return dest.exists()

        from PIL import Image, ImageOps

        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode not in ("RGB", "L"):
                im = im.convert("RGB")
            im.thumbnail((THUMB_MAX, THUMB_MAX), Image.LANCZOS)
            im.save(dest, format="JPEG", quality=70)
        return True
    except Exception:
        return False


PAGE = """<!doctype html>
<meta charset="utf-8">
<title>Instagram review — {count} items</title>
<style>
  body {{ font: 14px/1.5 system-ui, sans-serif; margin: 0; padding: 24px; background: #fafafa; color: #111; }}
  header {{ position: sticky; top: 0; background: #fafafa; padding-bottom: 12px; border-bottom: 1px solid #ddd; }}
  h1 {{ font-size: 18px; margin: 0 0 8px; }}
  .cmd {{ width: 100%; font-family: ui-monospace, monospace; font-size: 12px; padding: 8px; border: 1px solid #ccc; border-radius: 6px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; margin-top: 20px; }}
  figure {{ margin: 0; background: #fff; border: 1px solid #e3e3e3; border-radius: 8px; overflow: hidden; }}
  figure.on {{ outline: 3px solid #0d7ea8; }}
  img {{ width: 100%; height: 200px; object-fit: cover; display: block; background: #eee; }}
  figcaption {{ padding: 8px 10px; font-size: 12px; }}
  .meta {{ color: #666; display: flex; justify-content: space-between; gap: 8px; }}
  .cap {{ margin-top: 4px; max-height: 3.2em; overflow: hidden; }}
  label {{ display: flex; gap: 6px; align-items: center; padding: 6px 10px; border-top: 1px solid #eee; cursor: pointer; }}
  .missing {{ display: grid; place-items: center; height: 200px; color: #999; font-size: 12px; }}
</style>
<header>
  <h1>{count} items — {approved} approved</h1>
  <p>Tick what should be public, then run the command below. Nothing here is on the site yet.</p>
  <input class="cmd" id="cmd" readonly value="">
</header>
<div class="grid">
{cards}
</div>
<script>
  const cmd = document.getElementById("cmd");
  function refresh() {{
    const on = [...document.querySelectorAll("input[type=checkbox]:checked")].map(c => c.value);
    document.querySelectorAll("figure").forEach(f => {{
      f.classList.toggle("on", f.querySelector("input").checked);
    }});
    cmd.value = on.length
      ? "python3 tools/instagram-media/pull.py approve --id " + on.join(",")
      : "python3 tools/instagram-media/pull.py approve --none";
  }}
  document.addEventListener("change", refresh);
  refresh();
</script>
"""

CARD = """<figure{on}>
  {image}
  <figcaption>
    <div class="meta"><span>{date}</span><span>{kind}{count}</span></div>
    <div class="cap">{caption}</div>
  </figcaption>
  <label><input type="checkbox" value="{id}"{checked}> approve</label>
</figure>"""


def build(items, records: list[dict], workdir: Path) -> Path:
    """Render the contact sheet and return its path."""
    approved = {r["id"] for r in records if r.get("approved")}
    thumbs = workdir / "review" / "thumbs"
    cards = []

    for item in items:
        first = item.media[0]
        dest = thumbs / f"{first.sha256[:12]}.jpg"
        ok = _thumb(first.path, dest, first.kind)
        rel = dest.relative_to(workdir).as_posix()
        image = (
            f'<img src="{rel}" loading="lazy" alt="">'
            if ok
            else '<div class="missing">no preview</div>'
        )
        is_on = item.id in approved
        cards.append(
            CARD.format(
                on=' class="on"' if is_on else "",
                image=image,
                date=item.date,
                kind=item.kind,
                count=f" ×{len(item.media)}" if len(item.media) > 1 else "",
                caption=html.escape(item.caption[:180]) or "<em>no caption</em>",
                id=item.id,
                checked=" checked" if is_on else "",
            )
        )

    out = workdir / "review.html"
    out.write_text(
        PAGE.format(count=len(items), approved=len(approved), cards="\n".join(cards)),
        encoding="utf-8",
    )
    return out
