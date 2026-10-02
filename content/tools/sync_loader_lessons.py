#!/usr/bin/env python3
"""Sync the app's inlined loader with content/loader/yatla-content.js (lesson
metadata) and fix the lesson sort comparator.

The loader was changed to keep the pack's `lessons` list, but the app carries its
own copy of the loader inline, so the change has to be applied there too or the
app still sees zero lessons. Anchors are taken from the app's real bytes.
"""
import re
import sys

LOADER = 'content/loader/yatla-content.js'
APP = 'uploads/app-yatla.html'

src = open(LOADER, encoding='utf-8').read()
app = open(APP, encoding='utf-8').read()
edits = []


def grab(start, end):
    i = src.index(start)
    j = src.index(end, i) + len(end)
    return src[i:j]


def sub(old, new, label):
    global app
    n = app.count(old)
    if n != 1:
        sys.exit(f'ABORT [{label}]: anchor matched {n} times, expected 1')
    app = app.replace(old, new, 1)
    edits.append(label)


sub('  function embeddedPack() {',
    grab('  /* The pack carries a `lessons` list', '  function embeddedPack() {'),
    'pickLessons helper')

sub("""    function done(words, source) {
      cache = words;
      return { words: words, source: source || 'seed' };
    }""",
    grab('    function done(words, source, lessons) {', '    }'),
    'done() reports lessons')

sub("""    var embedded = normalizePack(embeddedPack());
    // Must stay a Promise: callers do fetchWords(...).then(...). A bare early return
    // here would break them with "then is not a function".
    if (embedded.length) return Promise.resolve(done(embedded, 'embedded'));""",
    grab('    var embeddedRaw = embeddedPack();', "pickLessons(embeddedRaw)));"),
    'embedded path passes lessons')

sub("""      return fromURL(opts.url)
        .then(function (pack) {
          var words = normalizePack(pack);
          if (!words.length) return done(cache || [], 'none');""",
    grab('      return fromURL(opts.url)', "if (!words.length) return done(cache || [], 'none', pickLessons(pack));"),
    'network path passes lessons (empty)')

sub('          return done(words, \'network\');',
    "          return done(words, 'network', pickLessons(pack));",
    'network path passes lessons')

# the comparator compared a string with a number, so "10A" sorted before "2A".
# Matched with a regex: hand-copied indentation has already burned this twice.
pat = re.compile(r"return out\.sort\(function\(a,b\)\{\s*\n\s*const na=parseInt\(a,10\),nb=parseInt\(b,10\);\s*\n\s*return na-nb\|\|\(a<nb\?-1:a>b\?1:0\);\s*\n\s*\}\);")
repl = ("return out.sort(function(a,b){\n"
        "  const na=parseInt(a,10),nb=parseInt(b,10);\n"
        "  if(na!==nb)return na-nb;\n"
        "  return a<b?-1:a>b?1:0;\n"
        " });")
if len(pat.findall(app)) != 1:
    sys.exit(f'ABORT [lesson sort comparator]: regex matched {len(pat.findall(app))} times, expected 1')
app = pat.sub(lambda m: repl, app, count=1)
edits.append('lesson sort comparator')

gates = {
    'pickLessons present in the app': app.count('pickLessons') >= 4,
    'exactly one app script': len(re.findall(r'<script\b[^>]*>', app)) == app.count('</script>'),
    'app code intact': 'function renderLearning' in app and '/* ================= INIT' in app,
}
for k, v in gates.items():
    print(f'  {"ok  " if v else "FAIL"} {k}')
if not all(gates.values()):
    sys.exit('ABORT: gate failed, nothing written')

open(APP, 'w', encoding='utf-8').write(app)
print(f'{len(edits)} edits applied')
for e in edits:
    print('  -', e)
