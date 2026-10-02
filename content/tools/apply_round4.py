#!/usr/bin/env python3
"""Round 4 app patch — Intermediate import + 4 UX fixes.

1. BOOKS: ele 13->11, pre 13->12, int 12->10 (+dl:1), each with a pe map that
   says which Practical English episode follows which unit in the book.
2. Units view: PE episodes render as their own row right after their unit
   (data-pe), instead of a trailing unit 13.
3. Lessons-view header + vocab back button handle PE episodes.
4. Nav pill: inset ring removed -> soft drop shadow + gentle gradient.
5. League emblems: minimalist flat shields, one glyph per tier.
6. Daily Challenge #2 actually completes: S.revs counter, ck2 tick, x/2 chip.
7. i18n: pe_w + chal2d in en/tk/ru.

Every anchor is asserted exactly once; the file is backed up first; the three
survival markers are checked before writing.
"""
import os
import re
import shutil

APP = '/home/user/uploads/app-yatla.html'

s = open(APP, encoding='utf-8').read()
orig_len = len(s)
n = 0


def rep(old, new, label):
    global s, n
    assert s.count(old) == 1, f'{label}: anchor count {s.count(old)}'
    s = s.replace(old, new)
    n += 1
    print(f'  [{n:02}] {label}')


# ---- 1. BOOKS entries -------------------------------------------------
rep('units:13,done:1,dl:1,mb:26',
    'units:11,pe:{1:"PE1",3:"PE2",5:"PE3",7:"PE4",9:"PE5",11:"PE6"},done:1,dl:1,mb:26',
    'BOOKS ele 11 real units + pe map')
rep('units:13,done:0,dl:1,mb:28',
    'units:12,pe:{1:"PE1",3:"PE2",5:"PE3",7:"PE4",9:"PE5",11:"PE6"},done:0,dl:1,mb:28',
    'BOOKS pre 12 real units + pe map')
rep('units:12,done:0,dl:0,mb:30',
    'units:10,pe:{1:"PE1",3:"PE2",5:"PE3",7:"PE4",9:"PE5"},done:0,dl:1,mb:26',
    'BOOKS int 10 real units + pe map, dl:1')

# ---- 2. units view: interleave PE rows ---------------------------------
old_units = '''  Array.from({length:b.units},(_,u)=>{const n=u+1,done=n<=b.done;
   const ls=unitLessonList(b.id,n);
   return `<div class="card urow row" data-un="${n}" style="gap:14px;padding:15px 16px">
   <span class="unum" style="width:40px;height:40px;font-size:16px;background:${done?"#8ED968":"var(--green)"};color:#fff">${done?"\u2713":n}</span>
   <div style="flex:1"><b style="font-size:15px">${t("unit_w")} ${n}</b>
   <div class="meta sub" style="font-size:12px;margin-top:2px">${unitCount(b.id,n)?unitCount(b.id,n)+" "+t("words"):t("no_words")}${ls.length?" \u00b7 "+ls.length+" "+t("lessons_w"):""}</div></div>
   <span class="st" style="background:${done?"var(--mint)":"#FFF7DB"};color:${done?"var(--green-d)":"#A16207"}">${done?t("review_chip"):t("start_chip")}</span></div>`;}).join("");return;}'''
new_units = '''  (function(){const PU=(lessonInfo(b.id,"PE1")||{}).unit,out=[];
   for(let n=1;n<=b.units;n++){const done=n<=b.done,ls=unitLessonList(b.id,n);
    out.push(`<div class="card urow row" data-un="${n}" style="gap:14px;padding:15px 16px">
   <span class="unum" style="width:40px;height:40px;font-size:16px;background:${done?"#8ED968":"var(--green)"};color:#fff">${done?"\u2713":n}</span>
   <div style="flex:1"><b style="font-size:15px">${t("unit_w")} ${n}</b>
   <div class="meta sub" style="font-size:12px;margin-top:2px">${unitCount(b.id,n)?unitCount(b.id,n)+" "+t("words"):t("no_words")}${ls.length?" \u00b7 "+ls.length+" "+t("lessons_w"):""}</div></div>
   <span class="st" style="background:${done?"var(--mint)":"#FFF7DB"};color:${done?"var(--green-d)":"#A16207"}">${done?t("review_chip"):t("start_chip")}</span></div>`);
    const pc=b.pe&&b.pe[n]&&PU?b.pe[n]:null;
    if(pc){const inf=lessonInfo(b.id,pc),pw=lessonWords(b.id,pc).length;
     out.push(`<div class="card urow row" data-pe="${pc}" style="gap:14px;padding:13px 16px;border:1px solid rgba(250,204,21,.6);background:linear-gradient(135deg,#FFFDF4,#FFF8DF)">
     <span class="unum" style="width:40px;height:40px;font-size:12px;background:linear-gradient(160deg,#FDE047,#F59E0B);color:#7C4A03">${pc}</span>
     <div style="flex:1;min-width:0"><b style="font-size:14px">${inf&&inf.title?inf.title:pc}</b>
     <div class="meta sub" style="font-size:12px;margin-top:2px">${t("pe_w")}${inf&&inf.topic?" \u00b7 "+inf.topic:""} \u00b7 ${pw} ${t("words")}</div></div>
     <svg style="width:17px;height:17px;color:#C79A0B"><use href="#i-chev"/></svg></div>`);}}
   return out.join("");})();return;}'''
rep(old_units, new_units, 'units view interleaves PE rows')

# ---- 3. lessons-view header + vocab back -------------------------------
rep('<div><h2 class="h2" style="font-size:19px">${t("unit_w")} ${un}</h2>',
    '<div><h2 class="h2" style="font-size:19px">${un>b.units?t("pe_w"):t("unit_w")+" "+un}</h2>',
    'lessons header says Practical English for PE unit')
rep('data-lv="${S.lv.lesson?"lessons":(unitLessonList(S.lv.book.id,S.lv.unit).length?"lessons":"units")}"',
    'data-lv="${S.lv.unit>S.lv.book.units?"units":(S.lv.lesson?"lessons":(unitLessonList(S.lv.book.id,S.lv.unit).length?"lessons":"units"))}"',
    'vocab back from a PE episode returns to the unit list')

# ---- 3b. click handler for PE rows -------------------------------------
rep(''' const ls=e.target.closest("[data-ls]");
 if(ls){''',
    ''' const pe=e.target.closest("[data-pe]");
 if(pe){const code=pe.dataset.pe,b=S.lv.book,ws=lessonWords(b.id,code);
  if(!ws.length)return;const inf=lessonInfo(b.id,code);
  S.lv={view:"vocab",book:b,unit:inf&&inf.unit?inf.unit:b.units+1,lesson:code,idx:0,session:ws};renderLearning();return;}
 const ls=e.target.closest("[data-ls]");
 if(ls){''',
    'PE row click opens the episode session')

# ---- 4. nav pill: no frame, soft shadow --------------------------------
rep('''.tbpill{position:absolute;bottom:8px;height:34px;border-radius:12px;background:var(--mint);
 box-shadow:inset 0 0 0 1.5px rgba(88,190,47,.35);z-index:0;''',
    '''.tbpill{position:absolute;bottom:8px;height:34px;border-radius:12px;background:linear-gradient(180deg,#F2FAE6,var(--mint));
 box-shadow:0 3px 14px rgba(31,80,45,.13);z-index:0;''',
    'pill: inset ring -> soft drop shadow (light)')
rep('html[data-theme="dark"] .tbpill{background:#182012;box-shadow:inset 0 0 0 1.5px rgba(88,190,47,.5)}',
    'html[data-theme="dark"] .tbpill{background:linear-gradient(180deg,#1D2616,#182012);box-shadow:0 3px 14px rgba(0,0,0,.5)}',
    'pill: inset ring -> soft drop shadow (dark)')

# ---- 5. minimalist emblems ----------------------------------------------
SHIELD = 'M12 2.2 19.4 5v6.1c0 4.7-3.1 8.4-7.4 10.2C7.7 19.5 4.6 15.8 4.6 11.1V5z'
GLOSS = 'M12 4.4 17.2 6.4v4.7c0 3.4-2.1 6.2-5.2 7.7V4.4z'
GLYPHS = {
    'bz': '',
    'sv': '<path d="M9.4 11.4l2.6 2.6 2.6-2.6" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    'gd': '<path d="M12 8.4l1.2 2.4 2.6.4-1.9 1.8.5 2.6-2.4-1.3-2.4 1.3.5-2.6-1.9-1.8 2.6-.4z" fill="#fff"/>',
    'sp': '<path d="M12 8.6l2.7 3.4-2.7 3.4-2.7-3.4z" fill="#fff"/>',
    'em': '<circle cx="12" cy="12" r="2.1" fill="#fff"/>',
    'lg': '<path d="M8.4 14.6l-.9-5 2.7 1.7L12 8l1.8 3.3 2.7-1.7-.9 5z" fill="#fff"/>',
}
COLORS = {
    'bz': ('#E8B27C', '#B97A3D'), 'sv': ('#E2E8F0', '#9AA6B8'), 'gd': ('#FDE047', '#E58E0A'),
    'sp': ('#7DB9FF', '#2563EB'), 'em': ('#5EEAB0', '#059669'), 'lg': ('#C084FC', '#7C3AED'),
}
lines = s.split('\n')
for k, (c1, c2) in COLORS.items():
    sid = f'id="i-t{k}"'
    hits = [i for i, l in enumerate(lines) if sid in l and '<symbol' in l]
    assert len(hits) == 1, f'emblem {k}: {len(hits)} lines'
    lines[hits[0]] = (f'<symbol id="i-t{k}" viewBox="0 0 24 24"><defs>'
                      f'<linearGradient id="gt{k}" x1="0" y1="0" x2="0" y2="1">'
                      f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>'
                      f'</linearGradient></defs>'
                      f'<path d="{SHIELD}" fill="url(#gt{k})"/>'
                      f'<path d="{GLOSS}" fill="#fff" opacity=".14"/>{GLYPHS[k]}</symbol>')
    n += 1
    print(f'  [{n:02}] emblem i-t{k} -> minimalist flat shield')
s = '\n'.join(lines)

# ---- 6. Daily Challenge #2 ----------------------------------------------
rep('<b style="font-size:13.5px" data-i18n="chal2">Complete 2 reviews</b><button class="link" style="margin-left:auto" id="chalReview" data-i18n="start">Start</button>',
    '<b style="font-size:13.5px" data-i18n="chal2">Complete 2 reviews</b><span class="sub" id="chal2P" style="margin-left:auto">0/2</span><button class="link" id="chalReview" data-i18n="start">Start</button>',
    'challenge 2 gets an x/2 progress chip')
rep('favs:new Set(["friend","water"]),hist:[],premium:false,',
    'favs:new Set(["friend","water"]),hist:[],premium:false,revs:0,',
    'S.revs counter added')
rep('user:S.user,avatar:S.avatar,events:S.events}))',
    'user:S.user,avatar:S.avatar,events:S.events,revs:S.revs}))',
    'S.revs persisted with the state')
rep('if(!r.counted){r.counted=true;S.words=Math.min(S.goal,S.words+(r.doneWords||0));refreshHome();}return;}}',
    'if(!r.counted){r.counted=true;S.words=Math.min(S.goal,S.words+(r.doneWords||0));S.revs=(S.revs||0)+1;save();refreshHome();}return;}}',
    'each finished review counts toward challenge 2')
rep('if(S.words>=S.goal)$("#ck1").classList.add("done");',
    '''if(S.words>=S.goal)$("#ck1").classList.add("done");
 if((S.revs||0)>=2){$("#ck2").classList.add("done");const cr=$("#chalReview");cr.textContent=t("chal2d");cr.style.opacity=".55";cr.style.pointerEvents="none";}
 else{const cr=$("#chalReview");cr.textContent=t("start");cr.style.opacity="";cr.style.pointerEvents="";}
 if($("#chal2P"))$("#chal2P").textContent=Math.min(2,S.revs||0)+"/2";''',
    'refreshHome ticks ck2 and shows x/2')

# ---- 7. i18n -------------------------------------------------------------
rep('lessons_w:"lessons",no_lessons:',
    'lessons_w:"lessons",pe_w:"Practical English",chal2d:"Done today",no_lessons:',
    'i18n en: pe_w + chal2d')
rep('lessons_w:"ders",no_lessons:',
    'lessons_w:"ders",pe_w:"Praktiki i\u0148lis dili",chal2d:"\u015eu g\u00fcn tamam",no_lessons:',
    'i18n tk: pe_w + chal2d')
rep('lessons_w:"\u0443\u0440\u043e\u043a(\u0430)",no_lessons:',
    'lessons_w:"\u0443\u0440\u043e\u043a(\u0430)",pe_w:"\u041f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0430\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439",chal2d:"\u0413\u043e\u0442\u043e\u0432\u043e \u043d\u0430 \u0441\u0435\u0433\u043e\u0434\u043d\u044f",no_lessons:',
    'i18n ru: pe_w + chal2d')

# ---- survival markers + write -------------------------------------------
for marker in ('function renderLearning', '/* ================= INIT', 'GLOBAL.YatlaContent = api'):
    assert marker in s, f'marker lost: {marker}'
assert 'inset 0 0 0 1.5px rgba(88,190,47' not in s, 'pill ring still present'

shutil.copyfile(APP, APP + '.bak')
open(APP, 'w', encoding='utf-8').write(s)
print(f'\n{n} patches applied. {orig_len} -> {len(s)} bytes ({len(s)-orig_len:+d})')
