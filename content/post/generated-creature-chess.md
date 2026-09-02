+++
author = "Brian Pfeil"
categories = ["JavaScript", "project"]
date = 2026-08-24
description = "Real chess, monster pieces. A friendly chess game for kids: full tournament rules, original creature artwork, legal-move helpers, hints, take-backs and trainer badges."
summary = " "
draft = false
slug = "creature-chess"
tags = ["javascript","game","web"]
title = "Creature Chess"
repoFullName = "pfeilbr/creature-chess"
repoHTMLURL = "https://github.com/pfeilbr/creature-chess"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/creature-chess" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/creature-chess</a>
</div>

<p align="center">
  <img src="https://raw.githubusercontent.com/pfeilbr/creature-chess/main/assets/lineup.svg" alt="Creature Chess — Leaflet the Pawn, Embercolt the Knight, Zapwing the Bishop, Boulderbud the Rook, Aquarina the Queen and Draxis the King" width="900">
</p>

<h1 align="center">Creature Chess</h1>

<p align="center">
  <strong>Real chess. Monster pieces.</strong><br>
  A friendly, monster-battle chess game for a kid who is learning the real game.
</p>

<p align="center">
  <a href="https://pfeilbr.github.io/creature-chess/"><strong>▶ Play it here</strong></a>
</p>

---

## What this is

A complete chess game that runs entirely in the browser — no server, no account, no
install. It plays by full tournament rules (castling, en passant, promotion,
stalemate, the fifty-move rule, threefold repetition), but every piece is a cartoon
creature and every message is written for a seven-year-old.

It was built for a kid who is at chess camp all summer and who loves monster-collecting
games. The design brief was simple: **make it look like the game he loves and teach the
game he is actually learning.** So each creature keeps the silhouette of the real chess
piece it stands for — Boulderbud has castle battlements, Zapwing wears the bishop's
mitre, Embercolt faces sideways like a knight — and the move list records real algebraic
notation. Everything here transfers to a wooden set at camp.

## What it does

- **Play the computer or a friend** on the same screen.
- **Five difficulty levels**, from *Baby Buddy* (loses a lot, on purpose) to *Champion*.
- **Shows every legal move** — tap a creature and green dots appear where it can go,
  red rings around what it can catch. Switchable off as the player gets stronger.
- **Take Back** any move, as many times as you like. Nobody rage-quits.
- **Hint button** — the engine suggests a good move and says why in plain words.
- **A coach line** that explains what each creature does the moment you pick it up —
  and warns you when one of your creatures is about to be taken.
- **Pawn promotion** as a full-screen "your Leaflet is evolving!" moment.
- **Trainer badges** for real chess achievements: castling, promoting, forking two
  pieces, winning without losing your Queen.
- **Chiptune sound effects**, synthesised at runtime with no audio files: a catch
  lands with a hit and a rising sparkle, check sets off a low-health alarm, and
  checkmate stops the battle before the victory fanfare plays.
- **Learns nothing about you.** All state lives in `localStorage` on the device.
- Works with **mouse, touch and keyboard**, and remembers your game if you close the tab.
- **Plays offline, and installs to the home screen.** A service worker caches the whole
  game on first visit, so it opens with no wifi — a car, a waiting room, camp.
  On a phone or tablet, use *Add to Home Screen* and it runs full-screen with its own icon.

## The team

Both sides field the same six creatures; Team Ember (orange) plays the White pieces and
moves first, Team Frost (blue) plays Black.

| Creature | Chess piece | Value | How it moves |
| --- | --- | :---: | --- |
| **Leaflet** | Pawn | 1 | One square forward, catches diagonally, may leap two on its first turn |
| **Embercolt** | Knight | 3 | An L shape — and the only one that jumps over other pieces |
| **Zapwing** | Bishop | 3 | Any distance diagonally; stays on its own square colour forever |
| **Boulderbud** | Rook | 5 | Any distance in straight lines; castles with the King |
| **Aquarina** | Queen | 9 | Any direction, any distance |
| **Draxis** | King | — | One square in any direction; trap it and the game is over |

## Running it locally

There is no build step and there are no dependencies. Any static file server works —
ES modules will not load over `file://`, so you do need a server.

```bash
npm start
```

Then open <http://localhost:8791>. That runs `scripts/dev-server.py`, which is
Python's `http.server` plus `Cache-Control: no-store` — browsers cache ES modules
hard by URL, so without it you can edit a file, reload, and still be running the
old code. Any other static server works too if you do not mind reaching for a
hard reload.

## Tests

The rules engine is verified with [perft](https://www.chessprogramming.org/Perft) —
it walks the entire legal move tree from six known positions and compares the leaf-node
counts against published values. Any bug in castling rights, en passant, pinned pieces
or promotion changes those numbers immediately.

```bash
npm test
```

The same suite runs in GitHub Actions on every push, and a failing run blocks the deploy.

## How it is put together

```
index.html            markup and dialogs
css/styles.css        all styling (one file, no framework)
js/engine.js          chess rules: 0x88 board, move generation, SAN, game status
js/ai.js              opponent: negamax + alpha-beta, quiescence, piece-square tables
js/pieces.js          creature artwork (inline SVG) and kid-facing piece descriptions
js/app.js             the UI: board rendering, input, coaching text, badges
js/sound.js           Web Audio sound effects, synthesised — no audio files
js/badges.js          achievement tracking in localStorage
tests/perft.mjs       move generator correctness suite
sw.js                 service worker: offline play and home-screen install
scripts/dev-server.py static file server for local development
scripts/make-icons.py regenerates the PNG app icons (standard library only)
```

`engine.js` knows nothing about the DOM and `app.js` contains no chess rules, so the
engine can be tested in Node and the interface can change without risking legality bugs.

The opponent searches with iterative deepening under a time budget, so even the hardest
level answers in about a second on a tablet instead of freezing the page. Easy levels
are weakened deliberately — they still play sensible-looking moves and simply miss
things, which is far less discouraging for a beginner than an opponent playing at random.

## Artwork

Every creature is hand-written SVG in [`js/pieces.js`](https://github.com/pfeilbr/creature-chess/blob/main/js/pieces.js) — original
characters made for this project. The game is *inspired by* the idea of collectible
monsters with elemental types, but it contains no Pokémon names, sprites or other
assets, and it is not affiliated with or endorsed by Nintendo, Game Freak or The
Pokémon Company.

Because the art is inline SVG, it is razor sharp at any size, themeable by changing six
colours per team, and the whole game works offline.

## Accessibility

Every square is a real focusable button with a label like "e4, Ember Leaflet (Pawn)",
the board is navigable with the arrow keys, all status changes are announced through ARIA
live regions, animation respects `prefers-reduced-motion`, and touch targets stay above
44 px on phones.

## License

[MIT](https://github.com/pfeilbr/creature-chess/blob/main/LICENSE).

