#!/bin/bash
set -e

PORT=1414
PASS=0
FAIL=0
ERRORS=""

pass() {
  PASS=$((PASS + 1))
  echo "  PASS: $1"
}

fail() {
  FAIL=$((FAIL + 1))
  ERRORS="${ERRORS}\n  FAIL: $1"
  echo "  FAIL: $1"
}

echo "=== Verification ==="
echo ""

# 1. Build check
echo "[1/5] Build check..."
BUILD_OUTPUT=$(hugo --minify 2>&1)
PAGE_COUNT=$(echo "$BUILD_OUTPUT" | grep "Pages" | head -1 | grep -oE '[0-9]+' || echo "0")
if [ "$PAGE_COUNT" -gt 0 ]; then
  pass "Hugo build succeeded (${PAGE_COUNT} pages)"
else
  fail "Hugo build failed"
  echo "Aborting."
  exit 1
fi

# Page count sanity check
if [ "$PAGE_COUNT" -gt 300 ]; then
  pass "Page count > 300 (${PAGE_COUNT} pages)"
else
  fail "Page count too low: ${PAGE_COUNT} (expected > 300)"
fi

# 2. Start server
echo ""
echo "[2/5] Starting Hugo server on port ${PORT}..."
hugo server --port ${PORT} --disableLiveReload &>/dev/null &
SERVER_PID=$!
sleep 3

cleanup() {
  kill ${SERVER_PID} 2>/dev/null || true
}
trap cleanup EXIT

# 3. HTTP status checks
echo ""
echo "[3/5] HTTP status checks..."
for path in "/" "/about/" "/projects/" "/tags/" "/index.json" "/index.xml"; do
  if curl -sf -o /dev/null "http://localhost:${PORT}${path}"; then
    pass "GET ${path} -> 200"
  else
    fail "GET ${path} -> not 200"
  fi
done

# Check a known post
FIRST_POST=$(ls -d content/post/*/ 2>/dev/null | head -1 | sed 's|content/||' | sed 's|/$||')
if [ -n "${FIRST_POST}" ]; then
  if curl -sf -o /dev/null "http://localhost:${PORT}/${FIRST_POST}/"; then
    pass "GET /${FIRST_POST}/ -> 200"
  else
    fail "GET /${FIRST_POST}/ -> not 200"
  fi
fi

# 4. Content checks
echo ""
echo "[4/5] Content checks..."

if curl -s "http://localhost:${PORT}/" | grep -q "search-query"; then
  pass "Homepage has search input"
else
  fail "Homepage missing search input"
fi

if curl -s "http://localhost:${PORT}/" | grep -q "Brian Pfeil"; then
  pass "Homepage has site title"
else
  fail "Homepage missing site title"
fi

if curl -s "http://localhost:${PORT}/" | grep -q "post-preview"; then
  pass "Homepage has post previews"
else
  fail "Homepage missing post previews"
fi

if [ -n "${FIRST_POST}" ]; then
  if curl -s "http://localhost:${PORT}/${FIRST_POST}/" | grep -q 'class="prose"'; then
    pass "Post page has prose styling"
  else
    fail "Post page missing prose class"
  fi
fi

if curl -s "http://localhost:${PORT}/index.json" | grep -q '"title"'; then
  pass "Search index has title field"
else
  fail "Search index missing title field"
fi

if curl -s "http://localhost:${PORT}/index.xml" | grep -q "<item>"; then
  pass "RSS feed has entries"
else
  fail "RSS feed missing entries"
fi

# 5. Summary
echo ""
echo "=== Results ==="
echo "  Passed: ${PASS}"
echo "  Failed: ${FAIL}"
if [ ${FAIL} -gt 0 ]; then
  echo ""
  echo "Failures:"
  echo -e "${ERRORS}"
  exit 1
else
  echo ""
  echo "All checks passed!"
fi
