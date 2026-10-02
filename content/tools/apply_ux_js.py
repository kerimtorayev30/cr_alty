#!/usr/bin/env python3
"""
Ýatla — owner-requested UX overhaul (script + i18n phase).

Companion to apply_ux_patch.py (markup). Removes the gems currency and everything
priced in it, retargets the language switcher at Settings, rewrites the league screen
around weekly promotion quotas and a table-free monthly rank, and adds the two new
books to i18n.

Usage: python3 content/tools/apply_ux_js.py [app-yatla.html]
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
        sys.exit(f'REFUSING [{label}]: anchor occurs {n} times, expected {count}\n---\n{old[:400]}')
    h = h.replace(old, new)
    applied.append(label)


def sub(pattern, new, label, count=1):
    global h
    n = len(re.findall(pattern, h))
    if n != count:
        sys.exit(f'REFUSING [{label}]: pattern matched {n} times, expected {count}\n---\n{pattern[:200]}')
    h = re.sub(pattern, new, h)
    applied.append(label)


# ============================================= 1. STATE: no gems, add history

rep('const S={gems:320,chest:false,freeze:false,words:7,goal:10,streak:7,lang:"en",theme:"light",favs:new Set(["friend","water"]),premium:false,',
    'const S={words:7,goal:25,streak:7,lang:"en",theme:"light",favs:new Set(["friend","water"]),hist:[],premium:false,',
    'state: gems/chest/freeze dropped, word history added, default goal 25')

rep('rev:null,filter:"all",sound:true',
    'rev:null,filter:"hist",sound:true',
    'state: search defaults to recent words')

rep('function save(){try{localStorage.setItem("yatla_state",JSON.stringify({gems:S.gems,words:S.words,goal:S.goal,premium:S.premium,\n streak:S.streak,lang:S.lang,theme:S.theme,sound:S.sound,favs:[...S.favs],chest:S.chest,freeze:S.freeze,\n user:S.user,avatar:S.avatar,events:S.events}));}catch(e){}}',
    'function save(){try{localStorage.setItem("yatla_state",JSON.stringify({words:S.words,goal:S.goal,premium:S.premium,\n streak:S.streak,lang:S.lang,theme:S.theme,sound:S.sound,favs:[...S.favs],hist:S.hist,\n user:S.user,avatar:S.avatar,events:S.events}));}catch(e){}}',
    'save(): gems/chest/freeze out, history in')

rep('function load(){try{const o=JSON.parse(localStorage.getItem("yatla_state")||"null");\n if(o){Object.assign(S,o);S.favs=new Set(o.favs||["friend","water"]);}}catch(e){}}',
    'function load(){try{const o=JSON.parse(localStorage.getItem("yatla_state")||"null");\n if(o){delete o.gems;delete o.chest;delete o.freeze;/* legacy saves must not resurrect the removed currency */\n  Object.assign(S,o);S.favs=new Set(o.favs||["friend","water"]);S.hist=Array.isArray(o.hist)?o.hist:[];}}catch(e){}}',
    'load(): legacy gems/chest/freeze are stripped on read')

# ================================================== 2. LANGUAGE: Settings only

rep('const fab=$("#langFab"),pop=$("#langPop");\n fab.classList.toggle("on",!["scr-onboard","scr-goal","scr-auth"].includes(id));\n const hi=id==="scr-lesson";fab.classList.toggle("high",hi);pop.classList.toggle("high",hi);pop.classList.remove("open");\n',
    '', 'go(): language FAB handling removed')

rep('$("#langFab").onclick=e=>{e.stopPropagation();$("#langPop").classList.toggle("open");sfx("click");};\n$("#langPop").addEventListener("click",e=>{const b=e.target.closest("[data-lf]");if(!b)return;\n setLang(b.dataset.lf);$("#langPop").classList.remove("open");hz(15);sfx("good");});\ndocument.addEventListener("click",e=>{if(!e.target.closest("#langPop,#langFab"))$("#langPop").classList.remove("open");});\n',
    '', 'language: FAB and popover handlers removed')

rep(' $("#lfCode").textContent=l.toUpperCase();\n if(S.chest){const b=$("#chestBtn");b.textContent=t("reward_done");b.disabled=true;}\n if(S.freeze)$("#freezeBtn").textContent=t("freeze_on");}',
    '}', 'setLang(): FAB label and chest/freeze relabels removed')

sub(r'#langSeg button,#langSegOb button', '#langSegTop button,#langSeg button,#langSegOb button',
    'settings: language switcher (renamed id) is wired to setLang', count=2)

# ============================================ 3. HOME: no gems, goal-aware text

rep('function refreshHome(){$("#hgem").textContent=S.gems;$("#hstreak").textContent=S.streak;$("#streak2").textContent=S.streak;',
    'function refreshHome(){$("#hstreak").textContent=S.streak;$("#streak2").textContent=S.streak;',
    'home: gems counter removed')

rep(' if(S.words>=S.goal)$("#ck1").classList.add("done");renderLeague();}',
    ''' if(S.words>=S.goal)$("#ck1").classList.add("done");
 $("#chal1Txt").textContent=t("chal1",{n:S.goal});$("#chal1P").textContent=S.words+"/"+S.goal;
 renderLeague();}''',
    'home: daily challenge follows the chosen goal')

rep('<b style="font-size:13.5px" data-i18n="chal1">Learn 10 words</b><span class="sub" style="margin-left:auto">7/10</span>',
    '<b style="font-size:13.5px" id="chal1Txt" data-i18n="chal1">Learn 25 words</b><span class="sub" id="chal1P" style="margin-left:auto">7/25</span>',
    'home: challenge row made dynamic')

# the two handlers above are consecutive in the source; remove them as one block
i = h.index('$("#chestBtn").onclick=')
j = h.index('document.addEventListener("click",e=>{\n const g=e.target.closest(".gsel")')
block = h[i:j]
if 'freezeBtn' not in block or 'chestBtn' not in block:
    sys.exit('REFUSING: chest/freeze handler block not shaped as expected')
h = h[:i] + h[j:]
applied.append('home: chest and freeze handlers removed')

rep(' if(e.target.closest("[data-invite]")){toast(t("copied"));return;}});', '});',
    'home: invite handler removed')

rep(' const m=[["#chestBtn","chest_open"],["#freezeBtn","freeze_buy"],["[data-share]","share_wotd"],["[data-invite]","invite"],["#homeCont","lesson_open"],["#chalReview","review_open"]].find(([s])=>e.target.closest(s));',
    ' const m=[["[data-share]","share_wotd"],["#homeCont","lesson_open"],["#chalReview","review_open"]].find(([s])=>e.target.closest(s));',
    'analytics: chest/freeze/invite events removed')

# ==================================================== 4. GEM REWARDS REMOVED

rep('   <div class="card ach"><b style="font-size:16px;color:var(--green-d)">+${S.premium?80:40}</b><b>💎${S.premium?" ×2":""}</b></div>\n   <div class="card ach"><b style="font-size:16px;color:var(--gold)">+12</b><b>LP</b></div></div>',
    '   <div class="card ach"><svg style="width:17px;height:17px;color:var(--green-d)"><use href="#i-check"/></svg><b>${t("done_lab")}</b></div>\n   <div class="card ach"><b style="font-size:16px;color:var(--gold)">+12</b><b>LP</b></div></div>',
    'learning: unit-complete gem reward replaced')

rep('   <div class="card ach"><b style="font-size:16px;color:var(--green-d)">+${xp}</b><b>💎</b></div></div>',
    '   <div class="card ach"><svg style="width:17px;height:17px;color:var(--green-d)"><use href="#i-check"/></svg><b>${t("done_lab")}</b></div></div>',
    'review: gem reward replaced')

rep('if(!r.counted){r.counted=true;S.gems+=xp;S.words=Math.min(S.goal,S.words+ (r.doneWords||0));refreshHome();}',
    'if(!r.counted){r.counted=true;S.words=Math.min(S.goal,S.words+(r.doneWords||0));refreshHome();}',
    'review: no longer pays gems')

rep('if(S.lv.idx===S.lv.session.length-1){S.lv.view="complete";S.gems+=S.premium?80:40;refreshHome();}',
    'if(S.lv.idx===S.lv.session.length-1){S.lv.view="complete";refreshHome();}',
    'learning: unit completion no longer pays gems')

rep('if(ok){S.gems+=S.premium?20:10;sfx("good");track("mcq_correct");refreshHome();}else sfx("bad");',
    'if(ok){sfx("good");track("mcq_correct");refreshHome();}else sfx("bad");',
    'lesson: MCQ no longer pays gems')

for lang, a, b in [
    ('en', 'xpmsg:"+10 gems 💎 · Streak extended 🔥"', 'xpmsg:"Correct! · Streak extended 🔥"'),
    ('en', 'xpmsg2:"+20 gems 💎 · PREMIUM ×2 🔥"', 'xpmsg2:"Correct! · PREMIUM 🔥"'),
    ('tk', 'xpmsg:"+10 gem 💎 · Seriýa uzaldy 🔥"', 'xpmsg:"Dogry! · Seriýa uzaldy 🔥"'),
    ('tk', 'xpmsg2:"+20 gem 💎 · PREMIUM ×2 🔥"', 'xpmsg2:"Dogry! · PREMIUM 🔥"'),
    ('ru', 'xpmsg:"+10 гемов 💎 · серия продлена 🔥"', 'xpmsg:"Верно! · серия продлена 🔥"'),
]:
    rep(a, b, f'i18n {lang}: xpmsg gem wording removed')
rep('xpmsg2:"+20 гемов 💎 · PREMIUM ×2 🔥"', 'xpmsg2:"Верно! · PREMIUM 🔥"', 'i18n ru: xpmsg2 gem wording removed')

# ====================================== 5. SEARCH: history + favourites, no stages

rep('''function filt(){const q=($("#dinput").value||"").trim().toLowerCase();let n=0;
 $("#dictlist").innerHTML=WORDS.map((w,i)=>{
  const hitF=S.filter==="all"||S.filter==="fav"?true:(S.filter==="beg"?i<12:i>=6);
  const hitFav=S.filter!=="fav"||S.favs.has(w.en);
  const hit=!q||w.en.includes(q)||w.tm.toLowerCase().includes(q)||w.ru.toLowerCase().includes(q);
  const show=hit&&hitF&&hitFav;if(show)n++;
  return `<div class="card wrow row spread" data-w="${i}" style="display:${show?"":"none"}">
   <div><b>${w.en}</b><span class="en">${w.tm} · ${w.ru}</span></div>
   <div class="row" style="gap:8px">${S.favs.has(w.en)?`<svg style="width:15px;height:15px;color:var(--red)"><use href="#i-heart"/></svg>`:""}
   <span class="vstage" style="background:${STAGE_C[w.stage]};margin:0">${t(STAGE_K[w.stage])}</span></div></div>`;}).join("");
 $("#dcount").textContent=n+" "+t("words");}''',
    '''function filt(){const q=($("#dinput").value||"").trim().toLowerCase();let n=0;
 /* Filters are content-neutral on purpose: recent words, favourites, or everything.
    Book filtering was removed from Search, and so were the memory-stage chips. */
 $("#dictlist").innerHTML=WORDS.map((w,i)=>{
  const hitF=S.filter==="all"?true:S.filter==="fav"?S.favs.has(w.en):S.hist.includes(w.en);
  const hit=!q||w.en.includes(q)||w.tm.toLowerCase().includes(q)||w.ru.toLowerCase().includes(q);
  const show=hit&&hitF;if(show)n++;
  return `<div class="card wrow row spread" data-w="${i}" style="display:${show?"":"none"}">
   <div><b>${w.en}</b><span class="en">${w.tm} · ${w.ru}</span></div>
   <div class="row" style="gap:8px">${S.favs.has(w.en)?`<svg style="width:15px;height:15px;color:var(--red)"><use href="#i-heart"/></svg>`:""}</div></div>`;}).join("");
 if(!n&&!q&&S.filter==="hist")$("#dictlist").innerHTML=`<div class="card" style="text-align:center;color:var(--muted);font-size:13px">${t("no_recent")}</div>`;
 $("#dcount").textContent=n+" "+t("words");}''',
    'search: recent/favourites/all filters, stage chips removed')

rep('function openWord(w){S.detailWord=w;',
    'function openWord(w){S.detailWord=w;S.hist=[w.en].concat(S.hist.filter(x=>x!==w.en)).slice(0,12);',
    'search: opening a word records it in history')

# ==================================================== 6. LEAGUE REWRITE

i = h.index('function renderLeague(){')
j = h.index('/* --- local-first auth --- */')
old_league = h[i:j]
if '#lboard' not in old_league or 'TIERS.indexOf' not in old_league:
    sys.exit('REFUSING: renderLeague block not shaped as expected')

new_league = '''const TIER_Q={bz:50,sv:25,gd:12,sp:6,em:3,lg:1};/* weekly promotion spots, shrinking as the tier rises */
const TIER_EMB={bz:"#i-mbz",sv:"#i-msv",gd:"#i-mgd",sp:"#i-msp",em:"#i-mem",lg:"#i-mlg"};
function renderLeague(){
 /* League points are a ranking measure, not a currency: they come from the streak and
    the words done this week. Nothing here can be spent. */
 const lp=200+S.streak*12+S.words*3;
 const ti=TIERS.findIndex(z=>lp>=z.min),tix=ti<0?0:ti,tier=TIERS[tix],next=TIERS[tix+1];
 const quota=TIER_Q[tier.k]||1;
 $("#lhero").dataset.t=tier.k;
 $("#lheroUse").setAttribute("href",tier.icon);
 $("#lTierName").textContent=t(tier.key)+" · "+t("league");
 const band=next?next.min-tier.min:1;
 $("#lpFill").style.width=Math.min(100,Math.round((lp-tier.min)/band*100))+"%";
 $("#lpNext").textContent=next?t("lp_next",{lp:next.min-lp,tier:t(next.key)}):t("lp_max");
 $("#lquota").textContent=t("spots",{n:quota});
 $("#lcutover").textContent=t("cutover",{n:quota});
 /* Tier rail: emblem on every rank, its weekly promotion quota, locked states kept. */
 $("#tierRail").innerHTML=TIERS.map((x,i)=>`<div class="tier${i===tix?" on":i>tix?" lock":""}">
   <i><svg><use href="${x.icon}"/></svg><svg class="temb" style="position:absolute;inset:0;margin:auto;width:11px;height:11px;opacity:${i>tix?.45:1}"><use href="${TIER_EMB[x.k]}"/></svg></i>
   <span data-i18n="${x.key}">${t(x.key)}</span>
   <em style="display:block;font-style:normal;font-size:8.5px;opacity:.72">${t("spots",{n:TIER_Q[x.k]||1})}</em></div>`).join("");
 /* Monthly rank: only which band you reached and how far you moved. The league table
    itself is never rendered. */
 const band100=Math.max(1,Math.ceil(100-(lp-200)/6));
 $("#lmTop").textContent=t("top_n",{n:band100});
 const mseed=Math.floor(Date.now()/26298e5),prevPos=Math.max(1,band100+((mseed*7)%9)-3),delta=prevPos-band100;
 $("#lmDelta").textContent=(delta>0?"+":"")+delta;
 $("#lmDelta").style.color=delta>0?"var(--green-d)":delta<0?"var(--red)":"var(--muted)";
 $("#rankLine").textContent=t(tier.key)+" · "+lp+" LP";
 $("#lprevUse").setAttribute("href",tier.icon);
 $("#lprevTier").textContent=`${t(tier.key)} ${t("league")} · ${t("top_n",{n:band100})}`;}
'''
h = h[:i] + new_league + h[j:]
applied.append('league: rewritten (quotas, emblems, table-free monthly rank)')

# ---------------------------------------------- profile settings button wiring
rep('$("#logout").onclick=()=>go("scr-onboard");',
    '''$("#logout").onclick=()=>go("scr-onboard");
$("#setBtn").onclick=()=>{go("scr-profile");const s=$("#setSec");if(s)setTimeout(()=>s.scrollIntoView({block:"start"}),60);sfx("click");};
$("#setTop").onclick=()=>{const s=$("#scr-profile .scroll");if(s)s.scrollTo({top:0,behavior:"smooth"});};''',
    'profile: settings button + back-to-top wired')

rep('<div class="sec row spread"><span class="h2" data-i18n="settings">Settings</span><button class="link" id="setTop"',
    '<div class="sec row spread" id="setSec"><span class="h2" data-i18n="settings">Settings</span><button class="link" id="setTop"',
    'profile: settings section is scroll-targetable')

open(APP, 'w', encoding='utf-8').write(h)
print(f'script phase: {len(applied)} edits  ({ORIG} -> {len(h)} bytes)')
for a in applied:
    print('  -', a)
