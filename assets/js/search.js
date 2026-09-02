(function () {
  "use strict";

  var searchInput = document.getElementById("search-query");
  var resultsContainer = document.getElementById("search-results");
  var postList = document.getElementById("post-list");
  var template = document.getElementById("search-result-template");
  var indexCache = null;

  // User-facing strings come from the page (see layouts/partials/search.html)
  // so this file stays language-agnostic. "%d" is the count placeholder.
  var T = window.SEARCH_I18N || {
    placeholder: "Search posts\u2026",
    placeholderCount: "Search %d posts\u2026",
    failed: "Failed to load search index.",
    noMatches: "No matches found.",
    oneMatch: "1 match",
    nMatches: "%d matches",
    topMatches: "top %d matches"
  };

  function count(tpl, n) { return tpl.replace("%d", n); }

  if (!searchInput || !resultsContainer) return;

  // Update placeholder with post count
  if (typeof postCount !== "undefined") {
    searchInput.placeholder = count(T.placeholderCount, postCount);
  }

  function fetchIndex(cb) {
    if (indexCache) return cb(indexCache);
    fetch("/index.json")
      .then(function (r) { return r.json(); })
      .then(function (data) {
        indexCache = data;
        cb(data);
      })
      .catch(function () {
        resultsContainer.textContent = "";
        var err = document.createElement("p");
        err.className = "text-sm text-gray-500";
        err.textContent = T.failed;
        resultsContainer.appendChild(err);
      });
  }

  function search(query, data) {
    var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];

    var scored = [];
    for (var i = 0; i < data.length; i++) {
      var item = data[i];
      var title = (item.title || "").toLowerCase();
      var tags = (item.tags || []).join(" ").toLowerCase();
      var contents = (item.contents || "").toLowerCase();
      var score = 0;

      for (var t = 0; t < terms.length; t++) {
        var term = terms[t];
        if (title.indexOf(term) !== -1) score += 10;
        if (tags.indexOf(term) !== -1) score += 5;
        if (contents.indexOf(term) !== -1) score += 1;
      }

      if (score > 0) {
        scored.push({ item: item, score: score });
      }
    }

    scored.sort(function (a, b) { return b.score - a.score; });
    return scored.slice(0, 30);
  }

  var SNIPPET_LEN = 140;
  var SNIPPET_LEAD = 40;

  /* Treat every term as a literal string, never as a regex pattern. */
  function escapeRegExp(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  /* One case-insensitive alternation over all terms, longest first so that
     overlapping terms highlight the longest match. */
  function buildTermMatcher(terms) {
    var sorted = terms.slice().sort(function (a, b) { return b.length - a.length; });
    var parts = [];
    for (var i = 0; i < sorted.length; i++) {
      if (sorted[i]) parts.push(escapeRegExp(sorted[i]));
    }
    if (!parts.length) return null;
    return new RegExp(parts.join("|"), "gi");
  }

  /* Extract ~140 chars of context around the first term occurrence. */
  function buildSnippet(contents, terms) {
    if (!contents) return "";

    var lower = contents.toLowerCase();
    var first = -1;
    for (var i = 0; i < terms.length; i++) {
      var at = lower.indexOf(terms[i]);
      if (at !== -1 && (first === -1 || at < first)) first = at;
    }

    var start = first === -1 ? 0 : Math.max(0, first - SNIPPET_LEAD);
    var end = Math.min(contents.length, start + SNIPPET_LEN);

    // Trim to word boundaries so we don't cut mid-word.
    if (start > 0) {
      var sp = contents.indexOf(" ", start);
      if (sp !== -1 && sp < start + 20) start = sp + 1;
    }
    if (end < contents.length) {
      var lastSp = contents.lastIndexOf(" ", end);
      if (lastSp > start + 20) end = lastSp;
    }

    var text = contents.slice(start, end).replace(/\s+/g, " ").trim();
    if (!text) return "";
    if (start > 0) text = "…" + text;
    if (end < contents.length) text = text + "…";
    return text;
  }

  /* Build highlighted content as DOM nodes only — text never goes through
     innerHTML, so post content (raw HTML, code) can't inject markup. */
  function highlightInto(el, text, matcher) {
    el.textContent = "";
    if (!text) return;
    if (!matcher) {
      el.appendChild(document.createTextNode(text));
      return;
    }

    matcher.lastIndex = 0;
    var last = 0;
    var m;
    while ((m = matcher.exec(text)) !== null) {
      if (m[0] === "") { matcher.lastIndex++; continue; }
      if (m.index > last) {
        el.appendChild(document.createTextNode(text.slice(last, m.index)));
      }
      var mark = document.createElement("mark");
      mark.textContent = m[0]; // preserves the original casing
      el.appendChild(mark);
      last = m.index + m[0].length;
    }
    if (last < text.length) {
      el.appendChild(document.createTextNode(text.slice(last)));
    }
  }

  function renderResults(results, terms) {
    var matcher = buildTermMatcher(terms || []);
    resultsContainer.innerHTML = "";
    activeIndex = -1;

    if (!results.length) {
      var none = document.createElement("p");
      none.className = "text-sm text-gray-500 py-4";
      none.textContent = T.noMatches;
      resultsContainer.appendChild(none);
      return;
    }

    var meta = document.createElement("p");
    meta.className = "search-meta";
    meta.textContent = results.length === 1
      ? T.oneMatch
      : count(results.length === 30 ? T.topMatches : T.nMatches, results.length);
    resultsContainer.appendChild(meta);

    for (var i = 0; i < results.length; i++) {
      var item = results[i].item;
      var el = template.content.cloneNode(true);

      var link = el.querySelector(".search-result-link");
      link.href = item.permalink;
      highlightInto(link, item.title || "", matcher);

      var dateEl = el.querySelector(".search-result-date");
      dateEl.textContent = item.date || "";

      var snippetEl = el.querySelector(".search-result-snippet");
      var snippet = buildSnippet(item.contents || "", terms || []);
      if (snippet) {
        highlightInto(snippetEl, snippet, matcher);
      } else if (snippetEl && snippetEl.parentNode) {
        snippetEl.parentNode.removeChild(snippetEl);
      }

      resultsContainer.appendChild(el);
    }
  }

  function onInput() {
    var query = searchInput.value.trim();

    if (!query) {
      resultsContainer.innerHTML = "";
      if (postList) postList.style.display = "";
      return;
    }

    if (postList) postList.style.display = "none";

    fetchIndex(function (data) {
      var results = search(query, data);
      renderResults(results, query.toLowerCase().split(/\s+/).filter(Boolean));
    });
  }

  /* Keyboard navigation over the result list */
  var activeIndex = -1;

  function resultItems() {
    return resultsContainer.querySelectorAll("article");
  }

  function setActive(index) {
    var items = resultItems();
    if (!items.length) return;
    if (index < 0) index = items.length - 1;
    if (index >= items.length) index = 0;

    for (var i = 0; i < items.length; i++) {
      items[i].classList.toggle("is-active", i === index);
    }
    activeIndex = index;
    items[index].scrollIntoView({ block: "nearest" });
  }

  searchInput.addEventListener("keydown", function (e) {
    var items = resultItems();

    if (e.key === "Escape") {
      searchInput.value = "";
      onInput();
      searchInput.blur();
      return;
    }

    if (!items.length) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive(activeIndex + 1);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive(activeIndex - 1);
    } else if (e.key === "Enter") {
      var target = items[activeIndex] || items[0];
      var link = target && target.querySelector("a");
      if (link) {
        e.preventDefault();
        window.location.href = link.getAttribute("href");
      }
    }
  });

  var timer = null;
  searchInput.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(onInput, 300);
  });

  // Hide "/" hint on focus, show on blur
  var kbdHint = document.querySelector("#search-bar kbd");
  if (kbdHint) {
    searchInput.addEventListener("focus", function () { kbdHint.style.display = "none"; });
    searchInput.addEventListener("blur", function () {
      if (!searchInput.value) kbdHint.style.display = "";
    });
  }

  // Also hide sentinel/progress when searching, show when cleared
  var sentinel = document.getElementById("scroll-sentinel");
  var origOnInput = onInput;
  onInput = function () {
    var query = searchInput.value.trim();
    if (sentinel) sentinel.style.display = query ? "none" : "";
    origOnInput();
  };
})();
