(function () {
  "use strict";

  var searchInput = document.getElementById("search-query");
  var resultsContainer = document.getElementById("search-results");
  var postList = document.getElementById("post-list");
  var template = document.getElementById("search-result-template");
  var indexCache = null;

  if (!searchInput || !resultsContainer) return;

  // Update placeholder with post count
  if (typeof postCount !== "undefined") {
    searchInput.placeholder = "Search " + postCount + " posts\u2026";
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
        resultsContainer.innerHTML = '<p class="text-sm text-gray-500">Failed to load search index.</p>';
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

  function renderResults(results) {
    resultsContainer.innerHTML = "";

    if (!results.length) {
      resultsContainer.innerHTML = '<p class="text-sm text-gray-500 py-4">No matches found.</p>';
      return;
    }

    for (var i = 0; i < results.length; i++) {
      var item = results[i].item;
      var el = template.content.cloneNode(true);

      var link = el.querySelector(".search-result-link");
      link.href = item.permalink;
      link.textContent = item.title;

      var dateEl = el.querySelector(".search-result-date");
      dateEl.textContent = item.date || "";

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
      renderResults(results);
    });
  }

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
