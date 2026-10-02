#!/usr/bin/env python3
"""
Ýatla — orphan CSS/markup cleanup + i18n update for the UX overhaul.

Removes the now-dead #langFab / #langPop rules and popover markup, then updates all
three dictionaries in one pass: the two new books, the new league strings, the 25/35/50
goal wording, and deletion of every key that only existed to price things in gems.

Usage: python3 content/tools/apply_ux_i18n.py [app-yatla.html]
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


def sub(pattern, new, label, count=1):
    global h
    n = len(re.findall(pattern, h))
    if n != count:
        sys.exit(f'REFUSING [{label}]: pattern matched {n} times, expected {count}\n---\n{pattern[:200]}')
    h = re.sub(pattern, new, h)
    applied.append(label)


# ================================================= 1. ORPHAN FAB / POPOVER CSS

rep("""#langFab{position:absolute;left:12px;bottom:78px;z-index:58;display:none;align-items:center;gap:5px;
 background:var(--deep);color:#fff;border-radius:999px;padding:8px 12px;font-weight:800;font-size:11.5px;
 box-shadow:0 6px 16px rgba(16,40,20,.35);transition:transform .15s}
#langFab.on{display:inline-flex}
#langFab:active{transform:scale(.92)}
#langFab.high{bottom:104px}
#langPop{position:absolute;left:12px;bottom:122px;z-index:59;display:none;flex-direction:column;gap:2px;
 background:var(--card);border:1px solid var(--line);border-radius:16px;padding:6px;
 box-shadow:0 14px 34px rgba(0,0,0,.28);animation:scr .18s ease}
#langPop.open{display:flex}
#langPop.high{bottom:148px}
""", '', 'css: #langFab / #langPop rules removed')

sub(r'#langPop button\{[^\n]*\}\n#langPop button:active\{[^\n]*\}\nhtml\[data-theme="dark"\] #langPop\{[^\n]*\}\n',
    '', 'css: remaining #langPop rules removed')

rep("""    <div id="langPop">
      <button data-lf="en">\U0001F1EC\U0001F1E7 English</button>
      <button data-lf="tk">\U0001F1F9\U0001F1F2 Türkmen</button>
      <button data-lf="ru">\U0001F1F7\U0001F1FA Русский</button>
    </div>
""", '', 'language: popover markup removed')

rep('.tier i{', '.tier i{position:relative;',
    'css: tier icon box becomes the positioning context for its emblem')

# ================================================================ 2. NEW KEYS

NEW = {
    'en': ('bk_intp:"Intermediate Plus",bk_advp:"Advanced Plus",all_w:"All words",recent_s:"Recent words",'
           'no_recent:"No words yet — open a word and it will show up here",'
           'done_lab:"Unit done",promo_week:"Weekly promotion",spots:"{n} spots",cutover:"Finish in the top {n} this week to move up",'
           'rank_m:"MONTHLY RANK",lm_sub:"Your place this month · the league table is hidden",lm_delta:"vs last month",'
           'top_n:"Top {n}",back_top:"Back to top",'),
    'tk': ('bk_intp:"Orta plus",bk_advp:"Ösen plus",all_w:"Ähli sözler",recent_s:"Soňky sözler",'
           'no_recent:"Entek söz ýok — bir sözi açyň, ol şu ýerde görner",'
           'done_lab:"Bölüm tamam",promo_week:"Hepdelik ýokarlanma",spots:"{n} orun",cutover:"Ýokarlanmak üçin şu hepde ilkinji {n}-e giriň",'
           'rank_m:"AÝLYK ORUN",lm_sub:"Şu aýdaky ornuňyz · liga tablisasy gizlin",lm_delta:"geçen aýa görä",'
           'top_n:"Ilkinji {n}",back_top:"Ýokaryk",'),
    'ru': ('bk_intp:"Средний плюс",bk_advp:"Продвинутый плюс",all_w:"Все слова",recent_s:"Недавние слова",'
           'no_recent:"Пока нет слов — откройте слово, и оно появится здесь",'
           'done_lab:"Юнит пройден",promo_week:"Недельное повышение",spots:"{n} мест",cutover:"Войдите в топ-{n} на этой неделе, чтобы подняться",'
           'rank_m:"МЕСЯЧНЫЙ РЕЙТИНГ",lm_sub:"Ваше место за месяц · таблица лиги скрыта",lm_delta:"к прошлому месяцу",'
           'top_n:"Топ-{n}",back_top:"Наверх",'),
}
for lang, block in NEW.items():
    anchor = f'{lang}:{{pack_on:'      # pack_on is the first key of each dictionary
    if h.count(anchor) != 1:
        sys.exit(f'REFUSING [i18n {lang}]: expected "{anchor}" once, found {h.count(anchor)}')
    rep(anchor, f'{lang}:{{{block}pack_on:', f'i18n {lang}: new keys added')

# ====================================================== 3. GOAL 25 / 35 / 50

GOALS = {
    'en': [('g_casual_s:"5 words / day"', 'g_casual_s:"25 words / day"'),
           ('g_regular_s:"10 words / day"', 'g_regular_s:"35 words / day"'),
           ('g_serious_s:"15 words / day"', 'g_serious_s:"50 words / day"'),
           ('chal1:"Learn 10 words"', 'chal1:"Learn {n} words"')],
    'tk': [('g_casual_s:"5 söz / gün"', 'g_casual_s:"25 söz / gün"'),
           ('g_regular_s:"10 söz / gün"', 'g_regular_s:"35 söz / gün"'),
           ('g_serious_s:"15 söz / gün"', 'g_serious_s:"50 söz / gün"'),
           ('chal1:"10 söz öwren"', 'chal1:"{n} söz öwren"')],
    'ru': [('g_casual_s:"5 слов / день"', 'g_casual_s:"25 слов / день"'),
           ('g_regular_s:"10 слов / день"', 'g_regular_s:"35 слов / день"'),
           ('g_serious_s:"15 слов / день"', 'g_serious_s:"50 слов / день"'),
           ('chal1:"Выучить 10 слов"', 'chal1:"Выучить {n} слов"')],
}
for lang, pairs in GOALS.items():
    for old, new in pairs:
        rep(old, new, f'i18n {lang}: {old.split(":")[0]}')

# ==================================== 4. LEAGUE WORDING (quota, no LP-to-tier)

rep('lp_next:"{lp} LP to {tier}"', 'lp_next:"{lp} LP · {tier}"', 'i18n en: lp_next')
rep('lp_next:"{tier} üçin {lp} LP"', 'lp_next:"{lp} LP · {tier}"', 'i18n tk: lp_next')
rep('lp_next:"{lp} LP до лиги {tier}"', 'lp_next:"{lp} LP · {tier}"', 'i18n ru: lp_next')

# ===================================== 5. DROP THE GEM-ONLY KEYS FROM ALL THREE

DEAD = ['gems_w', 'reward_t', 'reward_claim', 'reward_done', 'freeze', 'freeze_on',
        'need_gems', 'invite_t', 'invite_sub', 'invite_btn', 'rank_fmt', 'all_books', 'copied']
removed = 0
for key in DEAD:
    h2, n = re.subn(rf'\b{re.escape(key)}:"(?:[^"\\]|\\.)*",?', '', h)
    if n:
        removed += n
        h = h2
        applied.append(f'i18n: removed obsolete key "{key}" ({n} dictionary/dictionaries)')

open(APP, 'w', encoding='utf-8').write(h)
print(f'i18n + cleanup phase: {len(applied)} edits, {removed} obsolete keys removed  ({ORIG} -> {len(h)} bytes)')
for a in applied:
    print('  -', a)
