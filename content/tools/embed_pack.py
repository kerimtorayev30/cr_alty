#!/usr/bin/env python3
"""Embed the built word pack into app-yatla.html so the app works with no network.

Why this exists: the app loads its vocabulary with
    YatlaContent.fetchWords({url:"content/build/yatla-words.min.json"})
which is a *relative path on disk*. The owner previews the app in a sandboxed
iframe with no network access (prompt.html §4.4), so that fetch always fails
there and the app silently falls back to the 12 seed words. The units screen
would then show every unit as empty.

YatlaContent.embeddedPack() reads <script id="yatlaWords"> via getElementById
and fetchWords() checks it FIRST, before IndexedDB/localStorage/network, so a
single embedded JSON script element makes the full bank available offline.

Re-runnable: it replaces an existing pack rather than adding a second one.

Usage: python3 content/tools/embed_pack.py [path/to/app-yatla.html]
"""
import json
import re
import shutil
import sys

APP = sys.argv[1] if len(sys.argv) > 1 else '/home/user/uploads/app-yatla.html'
PACK = '/home/user/content/build/yatla-words.min.json'
# The exact attribute order this script writes, so it can never match the
# documentation text inside the loader. No ^ anchor: a previous run may have left
# the tag mid-line, and missing it would embed a second copy.
TAG = re.compile(r'<script type="application/json" id="yatlaWords">.*?</script>\n?', re.S)

html = open(APP, encoding='utf-8').read()
pack = json.load(open(PACK, encoding='utf-8'))

# min.json is the compact format: {version,format,fields,count,rows:[[...],...]}.
# dev.json keeps full word objects under "words". Accept either — YatlaContent's
# normalizePack() expands the compact rows using "fields".
n = len(pack.get('rows') or pack.get('words') or [])
if not n:
    sys.exit('ABORT: the built pack has no words — run `cd content && node tools/build.js` first')
if 'count' in pack and pack['count'] != n:
    sys.exit(f"ABORT: pack header says count={pack['count']} but holds {n} rows — rebuild it")
if pack.get('format') == 5 and len(pack.get('fields', [])) < 10:
    sys.exit('ABORT: compact pack is missing its "fields" header, so rows cannot expand')

# The HTML parser ends a <script> element at the first "</script" it sees, even
# inside JSON. Nothing in this data contains that, but assert it rather than
# trust it: one stray occurrence truncates the whole app.
body = json.dumps(pack, ensure_ascii=False, separators=(',', ':'))
if '</script' in body.lower() or '<!--' in body:
    sys.exit('ABORT: pack JSON contains a sequence that would close the script tag')

tag = ('<!-- vocabulary bank, embedded so the app is fully functional offline (§4.4).\n'
       '     Regenerate with: cd content && node tools/build.js && python3 tools/embed_pack.py -->\n'
       '<script type="application/json" id="yatlaWords">' + body + '</script>\n')

before = html
shutil.copyfile(APP, APP + '.preembed.bak')

matches = list(TAG.finditer(before))
if len(matches) > 1:
    sys.exit(f'ABORT: {len(matches)} embedded packs found — refusing to guess which to replace')
if '</head>' not in before:
    sys.exit('ABORT: no </head> to insert before')

app_script = before.index('<script>')
strip_old = (before[:matches[0].start()] + before[matches[0].end():]) if matches else before

if matches and matches[0].start() < app_script:
    # Already ahead of the app script, so keep the position and only refresh the
    # contents. (An earlier version of this script returned the file untouched
    # here, which silently left a stale pack embedded after a rebuild.)
    html = before[:matches[0].start()] + tag + before[matches[0].end():]
    action = 'refreshed the embedded pack in place'
else:
    # Placement matters. The app script runs the moment the parser reaches it, and
    # YatlaContent reads the pack with document.getElementById — an element the
    # parser has not reached yet simply does not exist. Measured with jsdom: with
    # the pack before </body>, getElementById returned null during INIT and the
    # app silently kept its 12 seed words. The head is parsed before every script.
    html = strip_old.replace('</head>', tag + '</head>', 1)
    action = ('moved the embedded pack into <head> (it was after the app script)'
              if matches else 'inserted into <head> (before any script runs)')

# Not "grew": a rebuilt pack can legitimately be smaller. What must hold is
    # that the file changed by about the size difference of the pack itself —
    # a regex that ate code shows up as a large unexplained loss.
    # Byte lengths, not len(): the pack is full of Cyrillic and IPA, so one
    # character is often two or three bytes and a character count lies.
gates = {
    'file size change matches the pack swap': abs(
        (len(html.encode('utf-8')) - len(before.encode('utf-8')))
        - (len(tag.encode('utf-8')) - (len(matches[0].group(0).encode('utf-8')) if matches else 0))
    ) < 64,
    'every <script> closed exactly once': html.count('</script>') == len(re.findall(r'<script\b[^>]*>', html)),
    'application script survived': 'function renderLearning' in html and '/* ================= INIT' in html,
    'content loader survived': 'GLOBAL.YatlaContent = api' in html,
    'exactly one embedded pack now': len(TAG.findall(html)) == 1,
    # the app script reads the pack with getElementById, so the pack element must
    # come first in document order or INIT sees nothing
    'pack precedes the app script': html.index('id="yatlaWords"') < html.index('<script>'),
}
for k, v in gates.items():
    print(f'  {"ok  " if v else "FAIL"} {k}')
bad = [k for k, v in gates.items() if not v]
if bad:
    sys.exit('ABORT: gate(s) failed, nothing written: ' + ', '.join(bad))

open(APP, 'w', encoding='utf-8').write(html)
print(f'{action}')
print(f'  words embedded : {n}')
print(f'  pack bytes     : {len(body.encode("utf-8")):,}')
print(f'  app bytes      : {len(html.encode("utf-8")):,}')
print(f'  literal </script> in file: {html.count("</script>")} (= the {len(re.findall(r"<script" + chr(92) + r"b[^>]*>", html))} <script> opens)')
