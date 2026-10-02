#!/usr/bin/env python3
"""
Ýatla — final gem-wording cleanup after the UX overhaul.

Removes the last user-visible mentions of the deleted currency (weekly reward blurb,
an achievement name), the now-orphaned promo_sub key, and the two SVG symbols that
only existed to draw a gem and a chest. Also corrects the desktop spec panel, which
documents the product and must not describe features that are gone.

Usage: python3 content/tools/apply_ux_cleanup.py [app-yatla.html]
"""
import re
import sys

APP = sys.argv[1] if len(sys.argv) > 1 else '/home/user/uploads/app-yatla.html'
h = open(APP, encoding='utf-8').read()
ORIG = len(h)
applied = []


def rep(old, new, label, count=1):
    global h
    n = h.count(old)
    if n != count:
        sys.exit(f'REFUSING [{label}]: anchor occurs {n} times, expected {count}\n---\n{old[:300]}')
    h = h.replace(old, new)
    applied.append(label)


def drop_key(key, label):
    global h
    h2, n = re.subn(rf'\b{re.escape(key)}:"(?:[^"\\]|\\.)*",?', '', h)
    if n != 3:
        sys.exit(f'REFUSING [{label}]: key "{key}" found {n} times, expected 3')
    h = h2
    applied.append(f'{label} ({n} dictionaries)')


# ------------------------------------------------- weekly rewards no longer pay gems
rep('wk_sub:"Top 3: gem bonus + champion badge"', 'wk_sub:"Top 3: champion badge + bonus league points"', 'i18n en: wk_sub')
rep('wk_sub:"Top 3: gem sowgady + çempion nyşany"', 'wk_sub:"Ilkinji 3: çempion nyşany + goşmaça liga utugy"', 'i18n tk: wk_sub')
rep('wk_sub:"Топ-3: гемы + значок чемпиона"', 'wk_sub:"Топ-3: значок чемпиона + бонусные очки лиги"', 'i18n ru: wk_sub')

# ------------------------------------------------------- achievement renamed
rep('ach3:"Gem Rush"', 'ach3:"Quick Learner"', 'i18n en: ach3')
rep('ach3:"Çalt gem"', 'ach3:"Çalt öwren"', 'i18n tk: ach3')
rep('ach3:"Гем-рывок"', 'ach3:"Быстрый старт"', 'i18n ru: ach3')

# ------------------------------------------------- orphaned key + dead SVG symbols
drop_key('promo_sub', 'i18n: removed orphaned promo_sub')

# remove both dead symbols by locating them, so the exact path data cannot drift
for sym, label in [('i-gem', 'svg: unused gem symbol removed'),
                   ('i-chest', 'svg: unused chest symbol removed')]:
    if re.search(r'href="#%s"' % sym, h):
        sys.exit(f'REFUSING [{label}]: #{"{"}{sym}{"}"} is still referenced somewhere')
    i = h.index('<symbol id="%s"' % sym)
    j = h.index('</symbol>', i) + len('</symbol>')
    h = h[:i] + h[j:]
    applied.append(label)

# ------------------------------------- desktop spec panel must describe reality
rep('<li><b>Home fixed order:</b> Continue Learning → Daily Goal → Streak → Da',
    '<li><b>Home fixed order:</b> Continue Learning → Daily Goal (25/35/50) → Streak → Da',
    'spec panel: goal options documented')

sub_pat = re.compile(r'<li><b>Smart review:</b>[^\n]*')
m = sub_pat.search(h)
if not m:
    sys.exit('REFUSING: spec panel Smart review line not found')
h = h[:m.start()] + '<li><b>Smart review:</b> flashcards + fill-in-the-blank, session summary, accuracy and LP — no spendable currency.</li>' + h[m.end():]
applied.append('spec panel: review rewards corrected')

open(APP, 'w', encoding='utf-8').write(h)
print(f'cleanup: {len(applied)} edits  ({ORIG} -> {len(h)} bytes)')
for a in applied:
    print('  -', a)
