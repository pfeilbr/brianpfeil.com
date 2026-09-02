+++
author = "Brian Pfeil"
categories = ["JavaScript", "project"]
date = 2026-07-22
description = "AimForge — a free browser-based FPS aim trainer inspired by KovaaK's. Three.js, fully client-side."
summary = " "
draft = false
slug = "aimforge"
tags = ["javascript","threejs","game","web"]
title = "AimForge"
repoFullName = "pfeilbr/aim-trainer"
repoHTMLURL = "https://github.com/pfeilbr/aim-trainer"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aim-trainer" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aim-trainer</a>
</div>


A free, browser-based FPS aim trainer inspired by [KovaaK's](https://store.steampowered.com/app/824270/KovaaKs/). 100% client-side — no account, no server, no tracking. All progress and settings live in your browser's localStorage.

**Play it: https://pfeilbr.github.io/aim-trainer/**

## Features

- **15 built-in scenarios** across four categories:
  - *Clicking* — Gridshot, Tile Frenzy, Sixshot, Microshot, Spidershot, Motion Strike (juking movers), Popcorn (gravity-arc targets), Bounceshot (floor-bouncing targets)
  - *Flicking* — Flickshot (scored on flick speed), Dodgeshot (target dashes sideways in bursts)
  - *Tracking* — Strafe Track, Air Track, Ascended Track (strafing + jumping pill bot), Target Switch (three juking bots, track the glowing one)
  - *Reaction* — Reflex Shot (scored on reaction time)
- **Two playlists** — Daily Warmup (all skills) and Movement Mastery (moving targets only)
- **Benchmarks & ranks** — Iron → Grandmaster thresholds per scenario, with progress bars toward the next rank
- **Benchmark mode & skill profile** — a fixed 7-scenario gauntlet (standard settings enforced) that produces an overall rank (0–8 continuous skill scale), a category breakdown (Clicking / Tracking / Flicking / Reaction) with per-category ranks, benchmark history charting, and a one-click **Focus routine** targeting your weakest category, surfaced right on the Train screen
- **Progress tracking** — score history charts, personal bests, per-scenario averages, recent runs, lifetime stats
- **Custom scenario editor** — build your own scenarios (mode, target count/size, spawn area, speed, hits-to-kill, duration)
- **One-click guided first run** — new visitors get a single "Start shooting" button that drops them into a guided intro range (1s countdown, big targets, on-screen hints, ends at 10 kills) and then offers the Daily Warmup, browsing, or mouse fine-tuning. Tutorial runs don't touch your stats
- **Mouse calibration wizard** — measure your natural 180° flick (3 swipes, no numbers needed) and sensitivity is set for you, or copy your sens from a game. Detects polling rate, trackpad input, and missing raw input (OS pointer acceleration) while calibrating. In Settings and offered after the intro
- **Real sensitivity model** — CS/Apex-scale sensitivity (0.022°/count), cm/360 display, and importers for Valorant, Overwatch 2, Fortnite, and Quake sens
- **Crosshair editor** — style, color, size, gap, thickness, outline, with live preview
- **Data-driven themes** — five complete themes (Forge, Neon Vice, Arctic, Crimson Ops, Retro Terminal), each a single data object driving the UI palette, the 3D arena (walls, fog, grids, lighting, strip lights), target color, corner radius, typography (Retro goes monospace), and its own synthesized sound profile. Live-preview swatch picker in Settings; applies instantly
- **Customization** — FOV (horizontal), target color, run-duration override, synthesized hit sounds (WebAudio, no assets)
- **Data portability** — export/import all data as JSON

## Tech

- [Three.js](https://threejs.org/) for the 3D arena, pointer-lock mouse look, raycast hit detection
- [Vite](https://vitejs.dev/) for dev/build
- Vanilla JS + CSS — no UI framework
- localStorage for settings, run history, and custom scenarios

## Development

```bash
npm install
npm run dev     # dev server at http://localhost:5173
npm run build   # static build in dist/
```

Deployed to GitHub Pages automatically on push to `main` via GitHub Actions.

