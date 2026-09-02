+++
author = "Brian Pfeil"
categories = ["JavaScript", "project"]
date = 2026-07-21
description = ""
summary = " "
draft = false
slug = "college-pilot"
tags = ["javascript","pwa","web"]
title = "College Pilot"
repoFullName = "pfeilbr/college-pilot"
repoHTMLURL = "https://github.com/pfeilbr/college-pilot"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/college-pilot" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/college-pilot</a>
</div>


A data-driven PWA for narrowing a college list to one: a full campus-visit
guide per school, a financial-aid estimator with divorced-parent handling, a
side-by-side comparison table, and a Decision Board that turns tour-day
ratings into a ranked shortlist.

**Live site:** https://pfeilbr.github.io/college-pilot/

## Schools covered

- University of Delaware (Newark, DE)
- Penn State — University Park (State College, PA)
- University of Pittsburgh (Pittsburgh, PA)
- Rutgers University–New Brunswick (New Brunswick, NJ)
- Ohio State University (Columbus, OH)
- Michigan State University (East Lansing, MI)
- Indiana University Bloomington (Bloomington, IN)
- University of South Carolina (Columbia, SC)
- UMass Amherst (Amherst, MA)
- Fordham University (New York, NY)
- Northeastern University (Boston, MA)
- Tufts University (Medford/Somerville, MA)
- Boston University (Boston, MA)

The five Big Ten / SEC business flagships (Rutgers, Ohio State, Michigan State,
Indiana, South Carolina) were added as "likely" peers to the two the student
favors — Penn State and Pitt — and are surfaced in a **Recommended matches**
section on the hub.

## Features

- 🏠 Hub with school cards + a 13-metric comparison table
- ⭐ **Decision Board** — per-school verdicts (shortlist/undecided/pass), 8-category
  star ratings, and visit notes, saved in localStorage and ranked on the hub
- 💰 **Aid Estimator** — income brackets × FAFSA-only vs CSS-both-parents rules,
  net-price planning ranges sorted cheapest-first, PA grant portability notes
- 📊 Per-school guides with identical sections for apples-to-apples comparison
- 💼 Business-program deep-dives with hiring rates and salaries
- 🗣️ Real student sentiment from archived Reddit threads, clearly labeled
- 📱 Responsive PWA: home-screen install, offline support, in-app update button

## Architecture (data-driven by design)

```
index.html        hub (Decision Board, Aid Estimator, cards, compare)
school.html       empty shell — renders any school from its data file
app.js            renderer + shared UI (drawer, ratings, spy, tooltips)
styles.css        the whole design system (per-school color via --sc)
data/<id>.js      one authored guide per school  ← add schools here
data/generated/   machine-fetched official stats  ← refresh via script
scripts/          deterministic data fetchers (no LLM needed)
```

Each `data/<id>.js` registers `window.SCHOOLS['<id>']` with: identity/colors,
hero stats, hub-card fields, contact links, and a `sections` array of
`{id, nav, kicker, title, lead, html}` — the renderer builds the page and
navigation from whatever sections exist, so schools can differ freely.

### Adding a school

1. Add its IPEDS UnitID to `scripts/fetch_school_data.py` (find IDs at
   nces.ed.gov/collegenavigator) and run the script — official stats land in
   `data/generated/scorecard.json` deterministically, no AI tokens needed.
2. Copy an existing `data/*.js` as a template; fill in the editorial sections
   using the generated stats + the school's official pages.
3. Add the id to `window.SCHOOL_ORDER` (in `data/delaware.js`), add a
   `<script>` tag in both HTML files and `sw.js`'s asset list, and add a row
   to the Aid Estimator `DATA` array in `index.html`.

### Refreshing stats (deterministic, free)

```sh
python3 scripts/fetch_school_data.py            # DEMO_KEY, rate-limited
API_KEY=... python3 scripts/fetch_school_data.py  # free key from api.data.gov
```

Pulls acceptance rate, SAT bands, enrollment, demographics, tuition, net price
by income bracket, debt, graduation/retention, and 10-year earnings from the
U.S. Dept. of Education College Scorecard API for every school in the list.

## Feature roadmap (researched against Niche, BigFuture, Scoir, Corsava, CollegeVine, Naviance)

- Weighted scoring matrix with sliders (re-rank live as priorities change)
- Corsava-style preference card sort (Must Have / Nice / Don't Care / No Way)
  that seeds the matrix weights
- Reach/target/safety badges + Naviance-style scattergram from stored GPA/SAT
  vs. each school's middle-50%
- Head-to-head elimination rounds with recorded "why" lines
- Visit-day journal with photos; student vs. parent dual gut-scores
- Deadline countdown board; printable decision report export

## Run locally

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

Data compiled July 2026 from public sources (Common Data Sets, official
admissions/aid pages, College Scorecard, U.S. News, Niche, Pullpush Reddit
archive). Verify current figures with official sources before decisions.

