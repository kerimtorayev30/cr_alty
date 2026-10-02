#!/usr/bin/env bash
# Ýatla — full verification (prompt.html §8, extended).
# Usage: ./verify.sh
set -uo pipefail
cd "$(dirname "$0")"

APP="${1:-uploads/app-yatla.html}"
fail=0

step() { printf '\n\033[1m== %s\033[0m\n' "$1"; }
run()  { if "$@"; then echo "  -> exit 0"; else echo "  -> FAILED"; fail=1; fi }

step "1/5  extract the inline script and syntax-check it"
python3 -c "import re,sys;h=open('$APP',encoding='utf-8').read();open('/tmp/yatla-check.js','w').write(re.search(r'<script>(.*?)</script>',h,re.S).group(1))" \
  || { echo "  could not extract <script>"; exit 1; }
run node --check /tmp/yatla-check.js

step "2/5  content pipeline: validate + build + loader tests"
( cd content && npm run --silent check ) || fail=1

step "3/5  baseline journeys on $APP"
run node tests/baseline.js "$APP"

step "4/5  content pack integration on $APP"
run node tests/integration.js "$APP"

step "5/5  sandbox rules (prompt.html §4.4): no external resources"
python3 - "$APP" <<'PY'
import re, sys
h = open(sys.argv[1], encoding='utf-8').read()
bad = []
for m in re.finditer(r'<script[^>]*\bsrc\s*=', h):   bad.append('external <script src>')
for m in re.finditer(r'<link[^>]*\bhref\s*=\s*["\'](?!data:)', h): bad.append('external <link href>')
for m in re.finditer(r'<img[^>]*\bsrc\s*=\s*["\'](?!data:)', h):   bad.append('external <img src>')
for m in re.finditer(r'@import\s+url\((?!["\']?data:)', h):        bad.append('CSS @import')
for m in re.finditer(r'url\(\s*["\']?(?!data:)(https?:)?//', h):   bad.append('CSS url(//)')
# Every <script> must be closed exactly once, in order. A stray </script> inside
# the app script truncates the application, which is the failure this guards.
# The count is no longer hard-coded to 1: the embedded vocabulary pack is a real
# <script type="application/json"> element with a legitimate closing tag of its own.
opens = re.findall(r'<script\b[^>]*>', h)
lits = h.count('</script>')
app_scripts = [o for o in opens if 'application/json' not in o]
pack_scripts = [o for o in opens if 'application/json' in o]
print(f"  script/style blocks : {h.count('<script')}/{h.count('<style')}")
print(f"  <script> opens      : {len(opens)} ({len(app_scripts)} app + {len(pack_scripts)} json pack)")
print(f"  literal </script>   : {lits} (must equal the number of opens)")
if bad:
    print("  SANDBOX VIOLATIONS:", set(bad)); sys.exit(1)
if lits != len(opens):
    print(f"  STRAY OR MISSING </script>: {lits} closings for {len(opens)} openings"); sys.exit(1)
if len(app_scripts) != 1:
    print(f"  expected exactly 1 application script, found {len(app_scripts)}"); sys.exit(1)
if len(pack_scripts) > 2:
    print(f"  expected at most 2 embedded json packs (words + dictionary), found {len(pack_scripts)}"); sys.exit(1)
print("  ok — everything is inline or a data URI")
PY
[ $? -eq 0 ] || fail=1

printf '\n%s\n' "$([ $fail -eq 0 ] && echo 'ALL CHECKS PASSED' || echo 'SOME CHECKS FAILED')"
exit $fail
