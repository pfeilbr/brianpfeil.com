# AI radar (`/ai/`)

`radar.py` writes `data/ai.json`; `layouts/_default/ai.html` draws the page
from `/data/ai.json` in the browser. A GitHub Action
(`.github/workflows/ai-radar.yml`) runs it every morning at 10:17 UTC,
commits the file if it changed, and dispatches the deploy. The site stays
static: no server, no database, no keys.

```sh
make ai-refresh   # fetch everything now (python3 tools/ai-radar/radar.py)
python3 tools/ai-radar/radar.py --only hn simonw models   # just these
python3 tools/ai-radar/radar.py --dry-run                  # report only
make test-ai      # unit tests (no network) + i18n block is current
```

## Adding or removing a source

One entry in `config.json`. Fields: `id`, `section` (`people`, `labs`,
`tools`, `community`, `learning`), `name`, `home`, `feed`, and optionally
`kind` (`rss` default, `sitemap`, `hn`, `reddit`), `filter` (`ai`,
`bedrock`: keep only matching entries of a general-purpose feed), `stable`
(skip alpha/beta/rc/Insiders), `release`, `limit`, `x` (X handle),
`follow` (B follows them on X), `pin`.

A person also needs a one-line description, `ai_role_<id>`, in
`i18n_strings.py` in all nine languages, then `make ai-i18n`. Prose never
goes in `config.json`: it would render in English on the eight other sites.
"In my Feedly" is worked out from `data/feedly.yaml` by host.

Removing a source removes its items on the next run.

## The data file and its schema

`schema.json` is the contract; `radar.py` validates against it and refuses
to write a file that doesn't match, so a broken run commits nothing.

- Adding an **optional** field: add it to `schema.json` (every object is
  `additionalProperties: false`, so the tests fail until you do). No version
  bump; older pages ignore it.
- Renaming, removing, or changing the meaning of a field: bump
  `SCHEMA_VERSION` in `radar.py`, add a `MIGRATIONS[n]` step that upgrades a
  version-`n` file, update the `enum` in `schema.json`, and raise `SCHEMA`
  in the page script once it understands the new shape. The tests hold the
  three version numbers to each other. The page shows a "reload" message
  instead of rendering a file newer than it knows.

The file is merged run to run, not replaced: each item keeps its
`first_seen`, a source that fails keeps yesterday's items (its `status`
says `error`), and items age out after `window_days` — except that each
source in `people`, `learning` and `tools` keeps its latest three entries, so a quiet writer still has a card and a tool still shows its current version.

## What it cannot read

**X (Twitter).** The timeline needs a paid API. B's follows were read once
by hand (2026-09-26, 201 accounts, mostly AWS and serverless people); the
AI voices among them are marked `follow: true`.
**Reddit** rate-limits by IP; staggering helps, and a 429 just keeps
yesterday's threads.
