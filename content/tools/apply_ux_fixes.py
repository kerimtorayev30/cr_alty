#!/usr/bin/env python3
"""
Ýatla — fixes for what the updated test suite caught after the UX overhaul.

 1. #langSeg -> #langSegTop actually applied (the earlier rename silently missed)
 2. every remaining "2x gems" promise rewritten: premium ribbon, weekend event,
    lesson chip, static lesson feedback
 3. scrollIntoView guarded (jsdom and some webviews do not implement it)

Usage: python3 content/tools/apply_ux_fixes.py [app-yatla.html]
"""
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


# ======================= 1. language segment inside Settings gets its own id

rep('<div class="seg" id="langSeg">', '<div class="seg" id="langSegTop">',
    'settings: language segment id renamed')

# ============================ 2. remaining "2x gems" promises, in all three

rep('''          <b data-i18n="prem_rib">Premium · earning 2× gems</b>
          <span class="x2">×2 💎</span>''',
    '''          <b data-i18n="prem_rib">Premium active · full dictionary offline</b>
          <span class="x2">★</span>''',
    'ribbon: no gem promise')

rep('prem_rib:"Premium active · earning 2× gems"', 'prem_rib:"Premium active · full dictionary, offline"', 'i18n en: prem_rib')
rep('prem_rib:"Premium işjeň · 2× gem gazanýarsyň"', 'prem_rib:"Premium işjeň · doly sözlük, oflaýn"', 'i18n tk: prem_rib')
rep('prem_rib:"Premium активен · получаете 2× гемы"', 'prem_rib:"Premium активен · весь словарь офлайн"', 'i18n ru: prem_rib')

rep('event_xp:"Weekend event · 2× gems on all reviews"', 'event_xp:"Weekend event · double league points on all reviews"', 'i18n en: event_xp')
rep('event_xp:"Hepde soňy çäresi · 2× gem"', 'event_xp:"Hepde soňy çäresi · iki esse liga utugy"', 'i18n tk: event_xp')
rep('event_xp:"Ивент выходного дня · 2× гемы"', 'event_xp:"Ивент выходного дня · двойные очки лиги"', 'i18n ru: event_xp')
rep('<b style="font-size:12.5px" data-i18n="event_xp">Weekend event · 2× XP on all reviews</b>',
    '<b style="font-size:12.5px" data-i18n="event_xp">Weekend event · double league points</b>',
    'home: weekend event banner wording')

rep('<span class="x2chip" id="lesX2" style="display:none">×2 💎</span>',
    '<span class="x2chip" id="lesX2" style="display:none">×2 LP</span>',
    'lesson: premium chip is league points, not gems')

rep('<span id="fbs" style="display:block;font-size:12px;color:var(--muted);font-weight:700">+10 💎 · Streak extended 🔥</span>',
    '<span id="fbs" style="display:block;font-size:12px;color:var(--muted);font-weight:700">Streak extended 🔥</span>',
    'lesson: static feedback text carries no gems')

# ================================= 3. guard scrollIntoView for jsdom/webviews

rep('$("#setBtn").onclick=()=>{go("scr-profile");const s=$("#setSec");if(s)setTimeout(()=>s.scrollIntoView({block:"start"}),60);sfx("click");};',
    '$("#setBtn").onclick=()=>{go("scr-profile");const s=$("#setSec");\n if(s&&s.scrollIntoView)setTimeout(()=>s.scrollIntoView({block:"start"}),60);sfx("click");};',
    'profile: scrollIntoView feature-detected')

rep('$("#setTop").onclick=()=>{const s=$("#scr-profile .scroll");if(s)s.scrollTo({top:0,behavior:"smooth"});};',
    '$("#setTop").onclick=()=>{const s=$("#scr-profile .scroll");\n if(s&&s.scrollTo)s.scrollTo({top:0,behavior:"smooth"});else if(s)s.scrollTop=0;};',
    'profile: scrollTo feature-detected with a fallback')

open(APP, 'w', encoding='utf-8').write(h)
print(f'fixes: {len(applied)} edits  ({ORIG} -> {len(h)} bytes)')
for a in applied:
    print('  -', a)
