#!/usr/bin/env python3
"""Owner round: unlock every unit, smooth the navigation, real book covers.

  1. UNITS ARE NOT LOCKED ANY MORE. The "lock" state is gone from the unit list:
     a unit is either done (review) or open (start). Books keep their honest
     progress — unlocking is not the same as pretending everything is finished.
  2. SMOOTH NAVIGATION. A sliding pill under the active tab, a soft entrance
     animation for every Learning view and for screen changes, press feedback
     on tabs.
  3. REAL COVERS. The eight coursebook rows and the unit header now show a
     photograph of the actual book, embedded as data URIs (content/assets).
  4. Elementary gained a Practical English unit, so its book lists 13 units.
"""
import json
import sys

P = 'uploads/app-yatla.html'
h = open(P, encoding='utf-8').read()
edits = []


def sub(old, new, label):
    global h
    c = h.count(old)
    if c != 1:
        sys.exit(f'ABORT [{label}]: matched {c}')
    h = h.replace(old, new)
    edits.append(label)


def slice_between(start_marker, end_marker, new, label):
    global h
    a = h.index(start_marker)
    b = h.index(end_marker)
    h = h[:a] + new + h[b:]
    edits.append(label)


# ---- 1. the covers -----------------------------------------------------------
covers = json.load(open('/tmp/covers.json'))
cov = 'const COVERS={' + ','.join(f'{k}:"data:image/jpeg;base64,{v}"' for k, v in covers.items()) + '};\n'
sub('const BOOKS=[', cov + 'const BOOKS=[', 'COVERS map embedded before BOOKS')

sub('{id:"ele",t:"Elementary",lv:"A2",c:"linear-gradient(160deg,#FDE047,#EAB308)",dk:1,units:12,done:1,dl:1,mb:26},',
    '{id:"ele",t:"Elementary",lv:"A2",c:"linear-gradient(160deg,#FDE047,#EAB308)",dk:1,units:13,done:1,dl:1,mb:26},',
    'Elementary now has 13 units (Practical English included)')

# ---- 2. books view: real covers, roomier rows --------------------------------
NEW_BOOKS = '''if(v==="books"){el.innerHTML=`
  <div class="row spread" style="padding:14px 2px 8px"><div><h2 class="h2" style="font-size:24px;letter-spacing:-.3px">${t("learning")}</h2>
  <p class="sub" style="font-size:12.5px;margin-top:3px">${t("learn_sub")}</p></div>
  <span class="chip" style="color:var(--green-d)"><svg style="width:14px;height:14px"><use href="#i-leaf"/></svg>${t("offline")}</span></div>`+
  BOOKS.map((b,i)=>`<div class="card brow row" data-bk="${i}" style="gap:14px;padding:14px 15px">
   <img class="covimg" src="${COVERS[b.id]}" alt="English File · ${t("bk_"+b.id)}">
   <div style="flex:1;min-width:0"><b style="font-size:15.5px">English File · ${t("bk_"+b.id)}</b>
   <div class="meta" style="font-size:12px;margin-top:3px">${b.lv} · ${b.units} ${t("units_w")}</div>
   ${b.dl?`<div class="meta" style="font-size:11.5px;margin-top:2px">${Math.round(b.done/b.units*100)}% · ${b.done}/${b.units} ${t("units_w")} · ${b.mb} MB ✓</div>
   <div class="dlbar"><i style="width:${Math.round(b.done/b.units*100)}%;background:var(--green)"></i></div>`
   :`<button class="btn btn-s" style="padding:8px 12px;font-size:12px;margin-top:9px" data-dl="${i}"><svg style="width:14px;height:14px"><use href="#i-dl"/></svg> ${t("dl")} · ${b.mb} MB</button>`}</div>
   <svg style="width:17px;height:17px;color:var(--muted)"><use href="#i-chev"/></svg></div>
  `).join("");return;}
'''
slice_between('if(v==="books"){', 'if(v==="units"){', NEW_BOOKS, 'books view: real covers')

# ---- 3. units view: cover header, no locks, roomier rows ---------------------
NEW_UNITS = '''if(v==="units"){const b=S.lv.book;el.innerHTML=`
  <div class="uhead"><button class="icobtn" data-lv="books"><svg style="color:var(--deep)"><use href="#i-back"/></svg></button>
  <img class="covimg" src="${COVERS[b.id]}" alt="">
  <div style="flex:1;min-width:0"><h2 class="h2" style="font-size:21px">English File · ${t("bk_"+b.id)}</h2>
  <p class="sub" style="font-size:12px;margin-top:2px">${b.lv} · ${b.units} ${t("units_w")}</p></div></div>`+
  Array.from({length:b.units},(_,u)=>{const n=u+1,done=n<=b.done;
   const ls=unitLessonList(b.id,n);
   return `<div class="card urow row" data-un="${n}" style="gap:14px;padding:15px 16px">
   <span class="unum" style="width:40px;height:40px;font-size:16px;background:${done?"#8ED968":"var(--green)"};color:#fff">${done?"✓":n}</span>
   <div style="flex:1"><b style="font-size:15px">${t("unit_w")} ${n}</b>
   <div class="meta sub" style="font-size:12px;margin-top:2px">${unitCount(b.id,n)?unitCount(b.id,n)+" "+t("words"):t("no_words")}${ls.length?" · "+ls.length+" "+t("lessons_w"):""}</div></div>
   <span class="st" style="background:${done?"var(--mint)":"#FFF7DB"};color:${done?"var(--green-d)":"#A16207"}">${done?t("review_chip"):t("start_chip")}</span></div>`;}).join("");return;}
'''
slice_between('if(v==="units"){', 'if(v==="lessons"){', NEW_UNITS, 'units view: no locks, cover header')

# ---- 4. smooth navigation css ------------------------------------------------
sub('.lrow{padding:13px 16px;margin-top:9px;cursor:pointer;transition:transform .12s}',
    '''.lrow{padding:13px 16px;margin-top:9px;cursor:pointer;transition:transform .12s}
/* --- real coursebook covers and the roomier unit screen --- */
.covimg{width:72px;height:96px;object-fit:cover;border-radius:5px 10px 10px 5px;flex:0 0 auto;
 background:#fff;box-shadow:2px 4px 10px rgba(31,80,45,.30)}
.uhead{display:flex;gap:12px;align-items:center;padding:12px 2px 6px}
/* --- motion: views settle in, screens cross-fade, tabs carry a sliding pill --- */
#lv>*{animation:lvIn .32s cubic-bezier(.2,.8,.2,1) both}
@keyframes lvIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.screen.on{animation:scrIn .3s cubic-bezier(.2,.8,.2,1)}
@keyframes scrIn{from{opacity:.35}to{opacity:1}}
.tb{position:relative}
.tbpill{position:absolute;bottom:8px;height:34px;border-radius:12px;background:var(--mint);
 box-shadow:inset 0 0 0 1.5px rgba(88,190,47,.35);z-index:0;
 transition:left .32s cubic-bezier(.3,.9,.35,1),width .32s cubic-bezier(.3,.9,.35,1)}
.tbi{position:relative;z-index:1;transition:color .25s,transform .12s}
.tbi:active{transform:scale(.94)}
html[data-theme="dark"] .tbpill{background:#182012;box-shadow:inset 0 0 0 1.5px rgba(88,190,47,.5)}''',
    'css: covers, header, motion, tab pill')

# bigger league shield
sub('.lshield{width:62px;height:62px;', '.lshield{width:84px;height:84px;', 'league shield 62 -> 84')
sub('.lshield svg{width:62px;height:62px}', '.lshield svg{width:84px;height:84px}', 'shield svg 62 -> 84')

# ---- 5. the sliding pill -----------------------------------------------------
sub('function buildTabs(){$$(".tb").forEach(tb=>{const a=tb.dataset.active;',
    '''function pillTab(){$$(".screen").forEach(function(scr){const tb=scr.querySelector(".tb");if(!tb)return;
 var p=tb.querySelector(".tbpill");if(!p){p=document.createElement("span");p.className="tbpill";tb.prepend(p);}
 if(!scr.classList.contains("on"))return;
 var on=tb.querySelector(".tbi.on");if(!on){p.style.width="0";return;}
 p.style.left=(on.offsetLeft+5)+"px";p.style.width=(on.offsetWidth-10)+"px";});}
addEventListener("resize",pillTab);
function buildTabs(){$$(".tb").forEach(tb=>{const a=tb.dataset.active;''',
    'pillTab defined and wired to resize')
sub('tb.innerHTML=TABS.map(([id,k,ic])=>`<button class="tbi${id===a?" on":""}" data-go="scr-${id}"><svg><use href="${ic}"/></svg><span>${I18N[S.lang][k]}</span></button>`).join("");});}',
    'tb.innerHTML=TABS.map(([id,k,ic])=>`<button class="tbi${id===a?" on":""}" data-go="scr-${id}"><svg><use href="${ic}"/></svg><span>${I18N[S.lang][k]}</span></button>`).join("");});pillTab();}',
    'buildTabs repositions the pill')
sub(' if(id==="scr-league")renderLeague();', ' if(id==="scr-league")renderLeague();pillTab();', 'go() repositions the pill')

open(P, 'w', encoding='utf-8').write(h)
print(f'{len(edits)} edits applied:')
for e in edits:
    print('  -', e)
print(f'{len(h.encode("utf-8")):,} bytes')
