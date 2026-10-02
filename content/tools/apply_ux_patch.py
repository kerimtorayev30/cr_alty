#!/usr/bin/env python3
"""
Ýatla — owner-requested UX overhaul (markup phase).

 1. Daily goal raised to 25 / 35 / 50 words (min 25, default 25)
 2. Gems currency removed, with everything priced in gems: daily chest, streak
    freeze, invite bonus
 3. Language switcher moved into Settings; the floating globe FAB is gone
 4. Two new books: Intermediate Plus, Advanced Plus
 5. Search: book filter chips removed -> history / favourites / all
 6. League: rank emblems, weekly promotion quotas, monthly rank without the table
 7. Profile: settings button top-right

Every edit asserts its anchor occurs exactly once and aborts otherwise.
Usage: python3 content/tools/apply_ux_patch.py [app-yatla.html]
"""
import shutil
import sys

APP = sys.argv[1] if len(sys.argv) > 1 else '/home/user/uploads/app-yatla.html'
h = open(APP, encoding='utf-8').read()
ORIG = len(h)
shutil.copyfile(APP, APP + '.pre-ux.bak')

applied = []


def rep(old, new, label, count=1):
    global h
    n = h.count(old)
    if n != count:
        sys.exit(f'REFUSING [{label}]: anchor occurs {n} times, expected {count}\n---\n{old[:400]}')
    h = h.replace(old, new)
    applied.append(label)


# ==================================================== 1. HOME: gems chip gone

rep('            <span class="chip"><svg style="width:16px;height:16px;color:var(--gold)"><use href="#i-gem"/></svg><span id="hgem">320</span></span>\n',
    '', 'home: gems chip removed')

# ------------------------------------------------- chest card + freeze button
rep('''        <div class="card hcard row spread">
          <div class="row" style="gap:10px"><div class="gico" style="background:#FFF7DB"><svg style="color:var(--gold)"><use href="#i-gift"/></svg></div>
          <div><b style="font-size:12px;letter-spacing:.5px" data-i18n="reward_t">DAILY REWARD</b><br><span class="sub">+5–15 · <span data-i18n="gems_w">gems</span></span></div></div>
          <button class="btn btn-p" id="chestBtn" style="width:auto;padding:8px 13px;font-size:12px" data-i18n="reward_claim">Open chest</button>
        </div>
        <div class="card hcard row spread">
          <div class="row" style="gap:12px"><div class="gico" style="background:#FFF1E4"><svg style="color:var(--orange)"><use href="#i-flame"/></svg></div>
          <div><b style="font-size:13.5px"><span id="streak2">7</span> <span data-i18n="day_streak">day streak</span></b><br><span class="sub" data-i18n="streak">Current Streak · keep it alive!</span></div></div>
          <div style="text-align:center"><span style="font-size:17px">🔥</span><br><button class="link" id="freezeBtn" style="font-size:11px" data-i18n="freeze">Streak Freeze · 200</button></div>
        </div>''',
    '''        <div class="card hcard row spread">
          <div class="row" style="gap:12px"><div class="gico" style="background:#FFF1E4"><svg style="color:var(--orange)"><use href="#i-flame"/></svg></div>
          <div><b style="font-size:13.5px"><span id="streak2">7</span> <span data-i18n="day_streak">day streak</span></b><br><span class="sub" data-i18n="streak">Current Streak · keep it alive!</span></div></div>
          <span style="font-size:22px">🔥</span>
        </div>''', 'home: chest card + streak freeze removed')

# ------------------------------------------------------------- invite card
rep('''        <div class="card hcard row spread" style="margin-top:12px;background:linear-gradient(120deg,var(--mint),var(--card));border-color:#D8EDC4">
          <div class="row" style="gap:12px"><div class="gico"><svg><use href="#i-user"/></svg></div>
          <div><b style="font-size:14px" data-i18n="invite_t">Invite friends</b><br><span class="sub" data-i18n="invite_sub">+50 gems for each friend who joins</span></div></div>
          <button class="btn btn-p" style="width:auto;padding:10px 16px;font-size:13px" data-invite data-i18n="invite_btn">Invite</button>
        </div>
''', '', 'home: invite card removed')

# ================================================ 2. DAILY GOAL 25 / 35 / 50

rep('<button class="opt gsel" data-g="5"', '<button class="opt gsel" data-g="25"', 'goal: 5 -> 25')
rep('<button class="opt gsel sel" data-g="10"', '<button class="opt gsel" data-g="35"', 'goal: 10 -> 35, no longer default')
rep('<button class="opt gsel" data-g="15"', '<button class="opt gsel sel" data-g="50"', 'goal: 15 -> 50, new default')

# ========================================================== 3. SEARCH CHIPS

rep('''            <button class="rchip on" data-f="all" data-i18n="all_books">All books</button>
            <button class="rchip" data-f="beg" data-i18n="bk_beg">Beginner</button>
            <button class="rchip" data-f="ele" data-i18n="bk_ele">Elementary</button>
            <button class="rchip" data-f="fav" data-i18n="favs_f">♥ Favorites</button>''',
    '''            <button class="rchip on" data-f="hist" data-i18n="recent_s">🕘 Recent words</button>
            <button class="rchip" data-f="fav" data-i18n="favs_f">♥ Favorites</button>
            <button class="rchip" data-f="all" data-i18n="all_w">All words</button>''',
    'search: book chips -> recent / favourites / all')

# ========================================================== 4. TWO NEW BOOKS

rep(''' {id:"adv",t:"Advanced",lv:"C2",c:"linear-gradient(160deg,#A78BFA,#8B5CF6)",units:12,done:0,dl:0,mb:33}];''',
    ''' {id:"adv",t:"Advanced",lv:"C2",c:"linear-gradient(160deg,#A78BFA,#8B5CF6)",units:12,done:0,dl:0,mb:33},
 {id:"intp",t:"Intermediate Plus",lv:"B2+",c:"linear-gradient(160deg,#34D399,#059669)",units:12,done:0,dl:0,mb:32},
 {id:"advp",t:"Advanced Plus",lv:"C2+",c:"linear-gradient(160deg,#F472B6,#DB2777)",units:12,done:0,dl:0,mb:34}];''',
    'books: Intermediate Plus + Advanced Plus')

# ==================================================== 5. LEAGUE: quota, month

rep('''<div class="lsub" data-i18n="promo_sub">Top 10 promote · bottom 10 demote</div>''',
    '''<div class="lsub"><span data-i18n="promo_week">Weekly promotion</span> · <span id="lquota">50 spots</span></div>''',
    'league: hero shows the weekly promotion quota')

rep('''<div class="card menu" id="lboard" style="margin-top:12px"></div>
        <div class="cut"><i></i><span data-i18n="promo_sub">Top 10 promote · bottom 10 demote</span><i></i></div>''',
    '''<div class="card hcard" id="lmonthly" style="margin-top:12px">
          <span class="lab" data-i18n="rank_m">MONTHLY RANK</span>
          <div class="row spread" style="margin-top:10px;align-items:center">
            <div><b id="lmTop" style="font-size:26px;color:var(--deep)">Top 100</b><br><span class="sub" data-i18n="lm_sub">Your place this month · the league table is hidden</span></div>
            <div style="text-align:right"><b id="lmDelta" style="font-size:17px;color:var(--green-d)">+0</b><br><span class="sub" data-i18n="lm_delta">vs last month</span></div>
          </div>
        </div>
        <div class="cut"><i></i><span id="lcutover">Finish in the top 50 this week to move up</span><i></i></div>''',
    'league: table replaced by the monthly-rank card')

# ---------------------------------------------------- six tier rank emblems
EMBLEMS = '''<symbol id="i-mbz" viewBox="0 0 24 24"><path d="M12 4.7a3.1 3.1 0 0 1 1.6 5.7c-.5.3-.6.7-.6 1.2v.5h-2v-.5c0-.5-.1-.9-.6-1.2A3.1 3.1 0 0 1 12 4.7Z" fill="#fff" opacity=".93"/><rect x="9.5" y="13.4" width="5" height="1.8" rx=".9" fill="#fff" opacity=".93"/><rect x="10.2" y="15.9" width="3.6" height="1.6" rx=".8" fill="#fff" opacity=".72"/></symbol>
<symbol id="i-msv" viewBox="0 0 24 24"><path d="M12 3.2l1.5 4.7 4.9.1-4 2.9 1.5 4.8-3.9-2.9-3.9 2.9 1.5-4.8-4-2.9 4.9-.1z" fill="#fff" opacity=".93"/></symbol>
<symbol id="i-mgd" viewBox="0 0 24 24"><rect x="5.8" y="7.8" width="2.4" height="8" rx="1.2" fill="#fff" opacity=".93"/><rect x="9.4" y="6.3" width="2.4" height="9.5" rx="1.2" fill="#fff" opacity=".93"/><rect x="13" y="4.8" width="2.4" height="11" rx="1.2" fill="#fff" opacity=".93"/><rect x="16.6" y="8.8" width="2.4" height="7" rx="1.2" fill="#fff" opacity=".93"/><rect x="5.4" y="16.4" width="13.2" height="1.7" rx=".85" fill="#fff" opacity=".7"/></symbol>
<symbol id="i-msp" viewBox="0 0 24 24"><path d="M12 3.4 20.4 12 12 20.6 3.6 12z" fill="#fff" opacity=".3"/><path d="M12 6.4 17.4 12 12 17.6 6.6 12z" fill="#fff" opacity=".93"/></symbol>
<symbol id="i-mem" viewBox="0 0 24 24"><path d="M12 4.6c3.6 0 6.4 3 6.4 6.9 0 4-3.2 7.2-6.4 9.3-3.2-2.1-6.4-5.3-6.4-9.3 0-3.9 2.8-6.9 6.4-6.9z" fill="#fff" opacity=".93"/><path d="M12 9.1c1.1 1.8 2.6 2.5 2.6 4.1 0 1.5-1.2 2.7-2.6 3.6-1.4-.9-2.6-2.1-2.6-3.6 0-1.6 1.5-2.3 2.6-4.1z" fill="#10B981" opacity=".85"/></symbol>
<symbol id="i-mlg" viewBox="0 0 24 24"><path d="M12 2.6l1.8 4.2 4.5.5-3.4 3.1.9 4.5-3.8-2.3-3.8 2.3.9-4.5-3.4-3.1 4.5-.5z" fill="#fff" opacity=".95"/><path d="M12 12.2l1.1 2.6 2.8.3-2.1 1.9.6 2.8-2.4-1.4-2.4 1.4.6-2.8-2.1-1.9 2.8-.3z" fill="#fff" opacity=".72"/></symbol>
'''
rep('<symbol id="i-tbz"', EMBLEMS + '<symbol id="i-tbz"', 'league: six tier rank emblems added')

# =============================================== 6. PROFILE: settings button

rep('''<button class="icobtn" id="themeBtn2"><svg style="color:var(--deep)"><use href="#i-moon" id="thico2"/></svg></button>''',
    '''<div class="row" style="gap:8px">
            <button class="icobtn" id="themeBtn2"><svg style="color:var(--deep)"><use href="#i-moon" id="thico2"/></svg></button>
            <button class="icobtn" id="setBtn" aria-label="Settings"><svg style="color:var(--deep)"><use href="#i-gear"/></svg></button>
          </div>''', 'profile: settings button top-right')

# ================================================ 7. LANGUAGE FAB -> SETTINGS

rep('    <button id="langFab" aria-label="App language"><svg style="width:15px;height:15px"><use href="#i-globe"/></svg><span id="lfCode">EN</span></button>\n',
    '', 'language: floating globe FAB removed')

rep('''        <div class="sec row spread"><span class="h2" data-i18n="settings">Settings</span></div>''',
    '''        <div class="sec row spread"><span class="h2" data-i18n="settings">Settings</span><button class="link" id="setTop" style="font-size:12px" data-i18n="back_top">Back to top</button></div>''',
    'settings: back-to-top link')

open(APP, 'w', encoding='utf-8').write(h)
print(f'markup phase: {len(applied)} edits  ({ORIG} -> {len(h)} bytes)')
for a in applied:
    print('  -', a)
