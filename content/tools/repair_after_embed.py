#!/usr/bin/env python3
"""Repair app-yatla.html after embed_pack.py's over-greedy regex.

What happened: the replacement regex
    <script type="application/json" id="yatlaWords">.*?</script>
was not anchored to the start of a tag, so it matched the *documentation comment*
inside the content loader ("Reads a pack inlined into the host page as
<script id=\"yatlaWords\">") and ran non-greedily to the first literal </script> —
the closing tag of the app's main script. Everything from that comment to the end
of the app script was deleted: the tail of the loader IIFE (from normalizePack's
"embedded" section onward) and the whole application script.

Two intact sources make a full rebuild possible:
  - content/loader/yatla-content.js — the loader source, never damaged
  - recovered-script.js — the complete main script, extracted by verify.sh
    stage 1 moments before the damage and including the five unit patches

Nothing is written unless every gate passes, and the result is copied to
app-yatla.good.html so there is always a restore point in the workspace.
"""
import shutil
import sys

APP = 'uploads/app-yatla.html'
SCRIPT = 'recovered-script.js'
LOADER = 'content/loader/yatla-content.js'
MARK = 'CONTENT PACK (loader, inline)'
DAMAGE = 'vocabulary bank, embedded so the app'

h = open(APP, encoding='utf-8').read()
script = open(SCRIPT, encoding='utf-8').read()
loader = open(LOADER, encoding='utf-8').read().strip()

if MARK not in h or h.count(MARK) != 1:
    sys.exit(f'ABORT: expected exactly one "{MARK}" marker, found {h.count(MARK)}')

head = h[: h.rindex('/*', 0, h.index(MARK))]

# --- gates on the inputs -----------------------------------------------------
input_gates = {
    'damaged region still present': DAMAGE in h,
    'head still holds the markup': all(x in head for x in ('<body', 'id="lv"', '<symbol id="i-lock"')),
    'head holds no leftover script code': 'function renderLearning' not in head,
    'loader source is complete': 'GLOBAL.YatlaContent = api' in loader and loader.endswith('})();'),
    'loader source has no literal </script>': '</script>' not in loader,
    'recovered script is complete': 'function renderLearning' in script and '/* ================= INIT' in script,
    'recovered script carries the unit patches': script.count('unitWords') >= 4,
    'recovered script has no literal </script>': '</script>' not in script,
}

new = (head
       + '/* ================= CONTENT PACK (loader, inline) ================= */\n'
       + loader + '\n\n'
       + '/* ================= UNITS ================= */'
       + script[script.index('/* ================= UNITS ================= */') + len('/* ================= UNITS ================= */'):]
       + '\n</script>\n</body>\n</html>\n')

# the UNITS block and everything after it comes from the recovered script; the
# DATA block must have come along with it
output_gates = {
    'main script present': 'function renderLearning' in new,
    'DATA block present': '/* ================= DATA ================= */' in new,
    'INIT block present': '/* ================= INIT' in new,
    'unit helpers present': 'function unitWords' in new and 'function wordBook' in new,
    'unit session wired': 'unitWords(b.id,n)' in new,
    'loader api present': 'GLOBAL.YatlaContent = api' in new,
    'exactly one literal </script>': new.count('</script>') == 1,
    'ends with </html>': new.rstrip().endswith('</html>'),
    'no base64 image lost': new.count('base64') >= h.count('base64'),
    'all three dictionaries present': all(new.count(k) >= 1 for k in ('en:{', 'tk:{', 'ru:{')) and new.count('pack_on:') == 3,
    'Beginner has 12 units': 'units:12' in new,
}

for k, v in {**input_gates, **output_gates}.items():
    print(f'  {"ok  " if v else "FAIL"} {k}')
bad = [k for k, v in {**input_gates, **output_gates}.items() if not v]
if bad:
    sys.exit('ABORT: gate(s) failed, nothing written: ' + ', '.join(bad))

open(APP, 'w', encoding='utf-8').write(new)
shutil.copyfile(APP, 'app-yatla.good.html')
print(f'\nrebuilt {APP}: {len(new.encode("utf-8")):,} bytes')
print('restore point written to app-yatla.good.html')
