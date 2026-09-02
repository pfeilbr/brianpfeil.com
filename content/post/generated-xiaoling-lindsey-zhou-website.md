+++
author = "Brian Pfeil"
categories = ["CSS", "project"]
date = 2026-09-01
description = "Link-in-bio page for Lindsey (Xiaoling) Zhou"
summary = " "
draft = false
slug = "lindsey-zhou-link-page"
tags = ["css","web","github-pages"]
title = "Lindsey Zhou Link Page"
repoFullName = "pfeilbr/xiaoling-lindsey-zhou-website"
repoHTMLURL = "https://github.com/pfeilbr/xiaoling-lindsey-zhou-website"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/xiaoling-lindsey-zhou-website" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/xiaoling-lindsey-zhou-website</a>
</div>


A small, fast, dependency-free link-in-bio page for **Lindsey (Xiaoling) Zhou**, hosted on GitHub Pages.

**Live:** https://pfeilbr.github.io/xiaoling-lindsey-zhou-website/

## What's here

| File | Purpose |
| --- | --- |
| `index.html` | Markup, inline brand SVGs, OpenGraph/Twitter meta, `Person` JSON-LD |
| `styles.css` | Palette, layout, animations, light/dark themes |
| `script.js` | Theme toggle, WeChat copy-to-clipboard, Web Share |
| `gallery.html` | Photo gallery page (grid + lightbox) |
| `gallery.js` | Gallery rendering, lightbox, keyboard/swipe nav |
| `assets/gallery/` | `photos/`, `videos/`, generated `thumbs/`, `manifest.json` |
| `tools/build-gallery.py` | Builds thumbnails and the manifest |
| `assets/avatar.png` | Profile picture |
| `assets/favicon.svg` | Monogram favicon |

No build step, no framework, no external JS. The only network dependency is Google Fonts
(Fraunces + Inter), and the page degrades to system fonts if that fails.

## Links on the page

- LinkedIn — `in/xiaolingzhou`
- X (Twitter) — `@lindsey7926`
- Instagram — `@lindsey.zhou`
- Facebook — `lingling.zhou.96`
- WeChat — `ACL-beauty` (tap to copy; WeChat has no profile URL scheme)

## Features

- Responsive down to ~320px, laid out with fluid `clamp()` type
- Light + dark themes: follows the OS by default, overridable with the toggle, remembered in `localStorage`
- Animated gradient background, spinning avatar ring, staggered entrance
- Fully honours `prefers-reduced-motion`
- Keyboard accessible with visible focus rings; `aria-live` toast for copy feedback
- Clipboard fallback via `execCommand` for older/insecure contexts
- Print stylesheet

## Palette

Colours are pulled from the profile photo — caramel `#d59a55`, dusty rose `#d78e9e`,
olive `#7c8f6b`.

## Editing

Change a link or handle in `index.html` (each is one `<a class="link">` block). To swap the
profile picture, replace `assets/avatar.png` with a square image (400×400 or larger).

## Adding photos to the gallery

Drop full-size images into `assets/gallery/photos/` and videos into
`assets/gallery/videos/`, then:

```bash
python3 tools/build-gallery.py --album "Belmar Beach, July 2026"
```

That writes width-limited thumbnails to `assets/gallery/thumbs/` and regenerates
`assets/gallery/manifest.json` with dimensions, so the grid does not reflow as images
load. Video posters are extracted with `ffmpeg` if it is installed.

`gallery.html` is not linked from `index.html` yet — add a card once it has photos in it.

## Local preview

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Deploying

GitHub Pages serves the `main` branch root. Pushing to `main` publishes.
`.nojekyll` is present so Jekyll doesn't process the files.

