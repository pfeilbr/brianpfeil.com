# AI radar (`/ai/`)

`radar.py` writes `data/ai.json`; `layouts/_default/ai.html` draws the page
from `/data/ai.json` in the browser. A GitHub Action
(`.github/workflows/ai-radar.yml`) runs it twice a day (10:17 and 22:17
UTC), commits the file if it changed, and dispatches the deploy. The site
stays static: no server, no database.

```sh
make ai-refresh   # fetch everything now (python3 tools/ai-radar/radar.py)
python3 tools/ai-radar/radar.py --only hn simonw models   # just these
python3 tools/ai-radar/radar.py --dry-run                  # report only
make ai-digest    # today's briefing (needs ANTHROPIC_API_KEY)
make test-ai      # unit tests (no network, no API key) + i18n block is current
make test-ai-page # build /ai/ from a fixture; check all nine languages
```

Don't commit a locally regenerated `data/ai.json` or `data/ai-digests.json`:
the Action owns them, and a local copy conflicts with its next commit.

## The daily briefing

`digest.py` runs after the morning refresh: one `claude-opus-5` request
(adaptive thinking, structured JSON output, `fallbacks: "default"` so a
declined request is retried on Anthropic's recommended fallback model)
reads the last 30 hours of items and new models and writes a headline plus
four to seven cited points, in English and translated into the other eight
site languages in the same response. Every point cites item ids; a point
whose ids don't resolve is dropped in every language, so a briefing can
only point at things the page actually collected.

It lands in `data/ai.json` as `digest` (the top of the page, the home
card, the page's meta description) and is appended to
`data/ai-digests.json` (the last 60 days: the page's "Earlier briefings"
and the per-language feed at `/ai/index.xml`, `/ja/ai/index.xml`, ...).

It needs the `ANTHROPIC_API_KEY` repository secret; without it the step
prints a line and exits 0, and the page shows no briefing. A failed
request never fails the refresh. It runs once a day: the evening run sees
today's briefing and skips.

## Source health

Each source carries `fail_streak` while it keeps failing. When any source
reaches three failed runs in a row, the Action opens (or updates) one issue,
"AI radar: sources failing", listing them with their errors (`health.py`),
and closes it once they recover. The page's source list shows the streak.

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

Fields added since v1 without a bump (all optional): `digest`, `topics`
(what the last two days keep mentioning; each item also lists its own),
an item's `hn` (the Hacker News thread for the same story, matched by URL
or near-identical headline) and a source's `fail_streak`.

The file is merged run to run, not replaced: each item keeps its
`first_seen`, a source that fails keeps yesterday's items (its `status`
says `error`), a busy source keeps at most ten items, and items age out after `window_days` — except that each
source in `people`, `learning` and `tools` keeps its latest three entries, so a quiet writer still has a card and a tool still shows its current version.

## What it cannot read

**X (Twitter).** The timeline needs a paid API, and B decided (2026-09-26) not to pay for it -- don't propose it again. B's follows were read once
by hand (2026-09-26, 201 accounts, mostly AWS and serverless people); the
AI voices among them are marked `follow: true`.
**Reddit** rate-limits by IP; staggering helps, and a 429 just keeps
yesterday's threads.
