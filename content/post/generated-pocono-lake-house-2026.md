+++
author = "Brian Pfeil"
categories = ["HTML", "project"]
date = 2026-08-03
description = "Installable trip app for a family lake house week at Midlake 301, Big Boulder / Lake Harmony PA. Live weather, works offline."
summary = " "
draft = false
slug = "pocono-lake-house"
tags = ["pwa","web","offline"]
title = "Pocono Lake House"
repoFullName = "pfeilbr/pocono-lake-house-2026"
repoHTMLURL = "https://github.com/pfeilbr/pocono-lake-house-2026"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/pocono-lake-house-2026" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/pocono-lake-house-2026</a>
</div>


A single-page, installable web app for three nights at **Midlake unit 301**, Big
Boulder / Lake Harmony, PA — Tue Aug 4 → Fri Aug 7, 2026. Five of us.

**Open it:** https://pfeilbr.github.io/pocono-lake-house-2026/

Add it to your home screen — iPhone: Share → *Add to Home Screen*. Android: menu
→ *Install app*. It then opens without a browser bar and works with no signal.

## What's in it

| Section | What it's for |
|---|---|
| **Stay** | The real listing facts, all 52 host photos with a lightbox, what's provided vs. what to bring, house rules, who sleeps where |
| **Weather** | Live forecast for the condo's own coordinates, fetched every time you open the page |
| **Mom** | The trip is built around her. Seats with a view, one outing a day, the practical file — meds, ER, urgent care |
| **Lake** | Big Boulder Lake is private. Read this before you put a kayak on the roof |
| **Do** | 16 options with drive times, tagged for who each one actually suits |
| **Craft** | Studios nearby, plus at-the-house ideas. Doubles as the rain plan |
| **Eat** | The host's own recommendations first, then Jim Thorpe, then groceries and gas |
| **Pack** | Checkboxes that persist on your phone. Towels are at the top, because the host doesn't supply them |
| **Plan** | Four day cards, each carrying its own live forecast |
| **Info** | Numbers, addresses, the six things nobody has confirmed yet, and every source |

## How the weather works

Client-side [Open-Meteo](https://open-meteo.com/) call — no API key, CORS-enabled,
free — against `41.0501, -75.5931`, the condo's coordinates. Nothing is baked in
at build time:

- Fetched fresh on every page open, and again on tab focus if the last one is
  over 15 minutes old.
- Last good response is kept in `localStorage` and rendered with a "saved
  forecast, N hours ago" label when there's no signal. Coverage genuinely dies in
  the Lehigh gorge and out at Boulder Field.
- **Interleaved, not bolted on.** Each day card in *Plan* carries its own
  forecast; the wettest trip day names itself and highlights the rain-plan rows
  in the *Do* table; a high UV day surfaces the sunscreen line; current wind
  speed shows up in the *Lake* section because chop matters in a kayak. It all
  degrades quietly once the trip dates are in the past.

## Offline

A service worker precaches the shell — HTML, manifest, the self-hosted fonts,
icons and the handful of photos that show before you scroll. The other 48 photos
fill in as you browse, or all at once via **"Save all 52 photos for offline"** in
the *Info* section (~8 MB, do it on wifi). The forecast call is never cached by
the worker; the page handles staleness itself.

Fonts are self-hosted in `fonts/` rather than loaded from Google, so nothing
about the design depends on a connection.

## Sourcing

Every factual claim on the page carries a click-through source link, and the
*Info* section lists all of them in one place. Where nothing published answers a
question — most importantly **whether there are stairs or an elevator up to unit
301**, and **whether a guest may launch a personally owned kayak at the Boulder
Lake Club** — the page says so plainly instead of guessing, and lists it as a
call to make before leaving.

## Layout

```
index.html          the whole app — markup, styles, script
app.webmanifest     installable PWA manifest
sw.js               service worker (offline shell + photo cache)
fonts/              self-hosted woff2 subsets, 383 KB
img/                52 photos from the live listing, 1200px wide
icons/              PWA icon set, 16 → 1024 px, plus maskable and og
research/           the Airbnb scrape this was all written from, kept verbatim
CLAUDE.md           project notes, sourcing rules, open questions
```

`research/airbnb-listing-state.json` is the parsed listing page state as of
2026-08-03. Prefer it over re-scraping — the live listing can change, and the
page's facts were written from this copy.

