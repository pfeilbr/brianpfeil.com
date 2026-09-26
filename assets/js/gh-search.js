/* The search behind /github/: query parsing, matching, scoring and sorting.
   No DOM, so node can test it (tools/github-repos/search.test.mjs); the page
   (layouts/_default/github.html) does the drawing.

   Free words must all match somewhere (name, description, tags, area,
   language; README text too unless switched off). Qualifiers follow
   GitHub's own search syntax, and any of them can be negated:
     lang:go  area:ai  tag:lambda  is:fork  has:article  -is:fork
     created:2019  created:2018..2020  pushed:>2023  stars:>2
     -word  "exact phrase" */
(function (root) {
  "use strict";

  /* Lowercase and accent-free, so "donnees" finds "Données" (area names are
     translated, and not every keyboard types accents easily). */
  function norm(s) {
    return String(s == null ? "" : s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  }

  function year(iso) { return +String(iso).slice(0, 4); }

  /* "2019" | "2018..2020" | ">2020" | ">=2020" | "<2015" | "<=2015" -> [lo, hi] */
  function range(v) {
    var m;
    if ((m = /^(\d{4})\.\.(\d{4})$/.exec(v))) return [+m[1], +m[2]];
    if ((m = /^>(=?)(\d{4})$/.exec(v))) return [+m[2] + (m[1] ? 0 : 1), 9999];
    if ((m = /^<(=?)(\d{4})$/.exec(v))) return [0, +m[2] - (m[1] ? 0 : 1)];
    if ((m = /^(\d{4})$/.exec(v))) return [+m[1], +m[1]];
    return null;
  }

  var LISTS = ["lang", "area", "tag", "is", "has"];
  var ALIAS = { language: "lang", topic: "tag", year: "created", updated: "pushed" };

  function parse(text) {
    var out = { words: [], phrases: [], nots: [], created: null, pushed: null, stars: 0, not: {} };
    LISTS.forEach(function (k) { out[k] = []; out.not[k] = []; });
    var re = /(-?)(?:(\w+):)?(?:"([^"]*)"|(\S+))/g, m;
    while ((m = re.exec(String(text || "")))) {
      var neg = m[1] === "-", key = (m[2] || "").toLowerCase();
      var val = norm(m[3] != null ? m[3] : m[4] || "");
      key = ALIAS[key] || key;
      if (!val) continue;
      if (LISTS.indexOf(key) >= 0) (neg ? out.not[key] : out[key]).push(val);
      else if (key === "created" || key === "pushed") out[key] = range(val);
      else if (key === "stars") out.stars = (+val.replace(/[^\d]/g, "") || 0) + (/^>\d/.test(val) ? 1 : 0);
      else {
        var w = (key ? key + ":" : "") + val;
        if (neg) out.nots.push(w);
        else if (m[3] != null) out.phrases.push(w);
        else out.words.push(w);
      }
    }
    return out;
  }

  /* Adds the lowercase copies matching reads, and fills in anything an older
     or partial github.json left out so one odd record can't break the page. */
  function prep(r, areaLabel, article) {
    r.tags = r.tags || [];
    r.langs = r.langs || [];
    r.areas = r.areas && r.areas.length ? r.areas : ["other"];
    r.desc = r.desc || "";
    r.lang = r.lang || "";
    r.stars = r.stars || 0;
    r.created = r.created || "1970-01-01";
    r.pushed = r.pushed || r.created;
    r._name = norm(r.name);
    r._nameWords = r._name.replace(/[-_.]+/g, " ");
    r._nameList = r._nameWords.split(" ");
    r._desc = norm(r.desc);
    r._tags = r.tags.map(norm);
    r._langs = [norm(r.lang)].concat(r.langs.map(function (x) { return norm(x[0]); }));
    r._areaLabels = r.areas.map(function (a) { return norm(areaLabel[a] || ""); });
    r._meta = [r._tags.join(" "), norm(r.lang), r.areas.join(" "), r._areaLabels.join(" ")].join(" ");
    r._readme = norm(r.readme);
    r._post = article || "";
    r._hay = r._name + " " + r._nameWords + " " + r._desc + " " + r._meta;
    r._hayRm = r._hay + " " + r._readme;
    r._cy = year(r.created);
    r._py = year(r.pushed);
    return r;
  }

  /* 0 = no match; higher is better. */
  function wordScore(r, w, readme) {
    if (r._name === w) return 100;
    if (r._nameList.indexOf(w) >= 0) return 40;
    if (r._name.indexOf(w) >= 0 || r._nameWords.indexOf(w) >= 0) return 25;
    if (r._tags.indexOf(w) >= 0) return 20;
    if (r._meta.indexOf(w) >= 0) return 12;
    if (r._desc.indexOf(w) >= 0) return 10;
    if (readme && r._readme.indexOf(w) >= 0) return 3;
    return 0;
  }

  function inRange(y, lo, hi) { return (!lo || y >= lo) && (!hi || y <= hi); }

  function has(r, what) {
    return what === "article" ? !!r._post
      : what === "demo" ? !!r.homepage
      : what === "license" ? !!r.license
      : false;
  }
  function isKind(r, k) { return r.kind === k || (k === "archived" && !!r.archived); }
  function inArea(r, a) {
    return r.areas.indexOf(a) >= 0 || r._areaLabels.some(function (l) { return l && l.indexOf(a) >= 0; });
  }
  function hasLang(r, l) { return r._langs.indexOf(l) >= 0; }

  /* The score of r against parsed query P and the page's filter state S, or
     -1 when it doesn't match. skip names one facet ("kind", "area", "lang")
     to ignore, so that facet's counts show what picking another value of it
     would give instead of collapsing to the current pick. */
  function match(r, P, S, skip) {
    var kinds = P.is.length ? P.is : (S.kind !== "all" ? [S.kind] : null);
    if (skip !== "kind") {
      if (kinds) { if (!kinds.some(function (k) { return isKind(r, k); })) return -1; }
      else if (r.kind === "fork" && !S.forks) return -1;
    }
    if (P.not.is.some(function (k) { return isKind(r, k); })) return -1;
    if (skip !== "area" && S.area.length && !S.area.some(function (a) { return r.areas.indexOf(a) >= 0; })) return -1;
    if (skip !== "lang" && S.lang.length && S.lang.indexOf(r.lang || "—") < 0) return -1;
    if (P.area.length && !P.area.some(function (a) { return inArea(r, a); })) return -1;
    if (P.not.area.some(function (a) { return inArea(r, a); })) return -1;
    if (P.lang.length && !P.lang.some(function (l) { return hasLang(r, l); })) return -1;
    if (P.not.lang.some(function (l) { return hasLang(r, l); })) return -1;
    if (!P.tag.every(function (t) { return r._tags.indexOf(t) >= 0; })) return -1;
    if (P.not.tag.some(function (t) { return r._tags.indexOf(t) >= 0; })) return -1;
    if (S.art && !has(r, "article")) return -1;
    if (S.demo && !has(r, "demo")) return -1;
    if (!P.has.every(function (h) { return has(r, h); })) return -1;
    if (P.not.has.some(function (h) { return has(r, h); })) return -1;
    if (!inRange(r._cy, S.cf, S.ct) || !inRange(r._py, S.pf, S.pt)) return -1;
    if (P.created && !inRange(r._cy, P.created[0], P.created[1])) return -1;
    if (P.pushed && !inRange(r._py, P.pushed[0], P.pushed[1])) return -1;
    var minStars = Math.max(S.stars || 0, P.stars || 0);
    if (minStars && r.stars < minStars) return -1;
    var hay = S.rm ? r._hayRm : r._hay;
    if (P.nots.some(function (w) { return hay.indexOf(w) >= 0; })) return -1;
    if (!P.phrases.every(function (w) { return hay.indexOf(w) >= 0; })) return -1;
    var score = 0;
    for (var i = 0; i < P.words.length; i++) {
      var s = wordScore(r, P.words[i], S.rm);
      if (!s) return -1;
      score += s;
    }
    return score + (r._post ? 2 : 0);
  }

  function byDesc(k) { return function (a, b) { return b[k] > a[k] ? 1 : b[k] < a[k] ? -1 : 0; }; }
  var SORTS = {
    best: function (a, b) { return b._score - a._score || SORTS.pushed(a, b); },
    pushed: byDesc("pushed"),
    created: byDesc("created"),
    oldest: function (a, b) { return SORTS.created(b, a); },
    stars: function (a, b) { return b.stars - a.stars || SORTS.pushed(a, b); },
    name: function (a, b) { return a._name.localeCompare(b._name); }
  };

  /* Only http(s) becomes a link, whatever the JSON says. */
  function safeHref(u) { return /^https?:\/\/[^\s]+$/i.test(u || "") ? u : ""; }

  var api = { norm: norm, year: year, range: range, parse: parse, prep: prep, wordScore: wordScore,
    match: match, inRange: inRange, SORTS: SORTS, safeHref: safeHref };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.GhSearch = api;
})(this);
