/* Send the Google Photos search results on screen to the local picker, then
 * download whatever the picker still needs.
 *
 * Runs on a photos.google.com page, in B's own signed-in browser: as the
 * bookmarklet the picker page offers, or driven by an agent.
 *
 * 1. On a search page it scrolls the results to load them all (up to LIMIT),
 *    reads each tile's media key, label and image URL, and POSTs them to
 *    127.0.0.1:8790. The search text decides the category, so it has to be
 *    one of the searches the picker lists. Anywhere else this step is skipped.
 * 2. Google's image host only answers this signed-in browser, so the page
 *    also does the downloading: it asks the picker what it wants (thumbnails
 *    and screening copies for new results, full-size copies of picks), fetches
 *    each file and POSTs the bytes to the picker. Nothing goes anywhere but
 *    127.0.0.1, and no cookie leaves the browser.
 *
 * Chrome asks once whether photos.google.com may reach devices on the local
 * network; that has to be allowed for the POST to arrive.
 */
(function () {
  var LIMIT = 600, BASE = "http://127.0.0.1:8790", PICKER = BASE + "/api/harvest";
  var state = window.__pickerHarvest = { status: "running", n: 0 };

  function toast(text) {
    var t = document.getElementById("picker-toast");
    if (!t) {
      t = document.createElement("div");
      t.id = "picker-toast";
      t.style.cssText = "position:fixed;z-index:99999;right:16px;bottom:16px;max-width:360px;" +
        "padding:12px 16px;border-radius:10px;background:#1a73e8;color:#fff;font:14px system-ui;" +
        "box-shadow:0 4px 16px rgba(0,0,0,.4)";
      document.body.appendChild(t);
    }
    t.textContent = text;
  }

  function query() {
    var input = document.querySelector('input[aria-label*="Search"], input[type="text"]');
    var q = input && input.value ? input.value : document.title.replace(/\s*-\s*Google Photos\s*$/, "");
    return q.trim();
  }

  /* A tile's image URL only appears once Google has loaded its thumbnail,
     which lags behind in a background tab. Keys are kept without one (an
     exclusion search needs nothing more) and filled in on a later sweep. */
  var seen = new Map();
  function grab() {
    document.querySelectorAll('a[href*="photo/AF1Qip"]').forEach(function (a) {
      var key = a.getAttribute("href").split("/photo/")[1];
      var prev = key && seen.get(key);
      if (!key || (prev && prev.url)) return;
      var bg = a.querySelector("[data-latest-bg]");
      var url = bg && bg.getAttribute("data-latest-bg");
      seen.set(key, { key: key, label: a.getAttribute("aria-label") || "", url: url || null });
    });
  }
  function missing() {
    var n = 0;
    seen.forEach(function (v) { if (!v.url) n++; });
    return n;
  }

  function scroller() {
    var el = document.querySelector('a[href*="photo/AF1Qip"]');
    while (el && !(el.scrollHeight > el.clientHeight + 50 &&
                   /auto|scroll/.test(getComputedStyle(el).overflowY))) el = el.parentElement;
    return el || document.scrollingElement;
  }

  /* Chrome throttles timers in a background tab to about one a minute, so
     a wait is a request the picker answers after `ms` instead: network
     callbacks aren't throttled. Falls back to a timer if that fails. */
  function sleep(ms) {
    return fetch(BASE + "/api/sleep?ms=" + ms).catch(function () {
      return new Promise(function (r) { setTimeout(r, ms); });
    });
  }

  async function harvest() {
    var q = query();
    if (!/\/search\//.test(location.pathname) || !q) return null;
    toast("Picker: collecting results for \u201c" + q + "\u201d\u2026");
    /* A people-plus-activity search can take a while, longer still in a
       background tab. Wait for tiles, or for Google to say there are none. */
    for (var wait = 0; wait < 120; wait++) {
      if (document.querySelector('a[href*="photo/AF1Qip"]')) break;
      if (/no results|couldn.t find|no matching/i.test(document.body.innerText)) break;
      await sleep(500);
    }
    /* An exclusion search only needs keys, so it makes one sweep. */
    var tier = null;
    try { tier = (await (await fetch(BASE + "/api/tier?q=" + encodeURIComponent(q))).json()).tier; } catch (e) {}
    var passes = tier === "exclude" ? 1 : 3;
    var sc = scroller();
    for (var pass = 0; pass < passes; pass++) {
      if (pass) {
        if (!missing()) break;
        sc.scrollTo(0, 0);
        await sleep(1500);
      }
      var last = -1, still = 0;
      for (var i = 0; i < 400 && still < 6 && seen.size < LIMIT; i++) {
        grab();
        state.n = seen.size;
        toast("Picker: " + seen.size + " found for \u201c" + q + "\u201d" +
              (pass ? ", fetching " + missing() + " thumbnails" : "") + "\u2026");
        sc.scrollBy(0, sc.clientHeight * 0.9);
        await sleep(pass ? 1200 : 700);
        var progress = seen.size * 10000 + (seen.size - missing());
        if (progress === last) still++; else { still = 0; last = progress; }
      }
      grab();
    }
    var items = Array.from(seen.values()).slice(0, LIMIT);
    var r = await fetch(PICKER, { method: "POST", headers: { "content-type": "application/json" },
                                 body: JSON.stringify({ query: q, items: items }) });
    return r.json();
  }

  /* Fetch one wanted file, trying each size suffix in turn, and hand the
     bytes to the picker. */
  async function download(w) {
    for (var k = 0; k < w.suffixes.length; k++) {
      try {
        /* The image host is another origin; the session cookie only goes
           with it when asked for. */
        var r = await fetch(w.url + w.suffixes[k], { credentials: "include" });
        if (!r.ok) continue;
        var blob = await r.blob();
        if (!/^(image|video)\//.test(blob.type)) continue;
        /* A plain photo answers the motion-clip request with a picture. */
        if (w.variant === "motion" && !/^video\//.test(blob.type)) return false;
        var up = await fetch(BASE + "/api/blob?key=" + encodeURIComponent(w.key) + "&variant=" + w.variant,
                             { method: "POST", body: blob });
        var j = await up.json();
        if (j.ok) return true;
      } catch (e) { /* try the next suffix */ }
    }
    return false;
  }

  async function pump() {
    var done = 0, failed = new Set();
    for (;;) {
      var w = (await (await fetch(BASE + "/api/wanted")).json()).wanted
        .filter(function (x) { return !failed.has(x.key + x.variant); });
      if (!w.length) break;
      /* Four at a time: quick, without hammering Google. */
      for (var i = 0; i < w.length; i += 4) {
        await Promise.all(w.slice(i, i + 4).map(async function (x) {
          if (await download(x)) { done++; return; }
          failed.add(x.key + x.variant);
          /* Tell the picker, so a photo with no motion clip isn't asked for again. */
          try {
            await fetch(BASE + "/api/failed?key=" + encodeURIComponent(x.key) + "&variant=" + x.variant,
                        { method: "POST" });
          } catch (e) {}
        }));
        state.downloaded = done;
        toast("Picker: downloaded " + done + " file(s)\u2026" + (failed.size ? " (" + failed.size + " failed)" : ""));
      }
    }
    return { done: done, failed: failed.size };
  }

  (async function () {
    try {
      var j = await harvest();
      state.result = j;
      if (j && !j.ok) toast("Picker: " + j.error);
      var d = await pump();
      state.downloads = d;
      toast((j && j.ok ? "Picker: sent " + j.received + " (" + j.new + " new) to " + j.category + ". " : "Picker: ") +
            "Downloaded " + d.done + " file(s)" + (d.failed ? ", " + d.failed + " failed" : "") + ". Done.");
    } catch (e) {
      state.result = { ok: false, error: String(e) };
      toast("Picker not reachable \u2014 is `make media-picker` running, and local network access allowed?");
    }
    state.status = "done";
  })();
})();
