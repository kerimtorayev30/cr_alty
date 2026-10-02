#!/usr/bin/env python3
"""Make the unit/lesson structure data-driven per book, and redesign the unit screen.

Why: the app hardcoded English File's shape. BOOKS says units:12 for all eight
books, every unit row rendered "1A 1B 1C" chips, and a word with no lesson still
had to fit that mould. The owner's point is that the unit system differs per
book — so the app must render whatever the book actually has, and say nothing
when the book has no lessons at all.

What changes:
  1. unitLessonList() no longer assumes three lessons or an A/B/C suffix. It
     returns the lessons that really exist, sorted naturally (2A before 10A).
  2. The tiny chip strip is replaced by lesson ROWS: each lesson of the opened
     unit gets its own line with the code, the lesson title, its topic and its
     word count, and tapping one starts just that lesson. A book whose words
     carry no lessons simply shows no rows — no empty chips.
  3. The flashcard keeps its lesson badge but drops the green pill look that the
     owner did not like; it is now a plain muted label.
  4. A unit's word count and the "N lessons" line come from the data.

Anchors are copied from the file's real bytes; the script aborts unless each
matches exactly once.
"""
import re
import sys

P = 'uploads/app-yatla.html'
h = open(P, encoding='utf-8').read()
edits = []


def sub(old, new, label):
    global h
    n = h.count(old)
    if n != 1:
        sys.exit(f'ABORT [{label}]: anchor matched {n} times, expected 1')
    h = h.replace(old, new, 1)
    edits.append(label)


# 1. natural sort, no assumption about the shape of a lesson code
sub(
    """/* the lessons of a unit, in order, so the unit row can show "1A 1B 1C" */
function unitLessonList(bid,un){
 const out=[];
 WORDS.forEach(function(w){
  const l=wordLesson(w);
  if(l&&l.book===bid&&l.unit===un&&out.indexOf(l.lesson)<0)out.push(l.lesson);
 });
 return out.sort(function(a,b){
  const na=parseInt(a,10),nb=parseInt(b,10);
  if(na!==nb)return na-nb;
  return a<b?-1:a>b?1:0;
 });
}""",
    """/* The lessons a unit really has. Nothing here assumes A/B/C or a fixed count —
   a book that teaches units as 1/2/3, or has no lessons at all, renders fine.
   Sorted naturally, so 2A comes before 10A. */
function lessonKey(s){
 const m=/^(\\d+)(.*)$/.exec(String(s));
 return m?[parseInt(m[1],10),m[2]]:[1e9,String(s)];
}
function cmpLessons(a,b){
 const ka=lessonKey(a),kb=lessonKey(b);
 if(ka[0]!==kb[0])return ka[0]-kb[0];
 return ka[1]<kb[1]?-1:ka[1]>kb[1]?1:0;
}
function unitLessonList(bid,un){
 const out=[];
 WORDS.forEach(function(w){
  const l=wordLesson(w);
  if(l&&l.book===bid&&l.unit===un&&out.indexOf(l.lesson)<0)out.push(l.lesson);
 });
 return out.sort(cmpLessons);
}
/* the words of one lesson, in the order the book lists them */
function lessonWords(bid,lesson){
 return WORDS.filter(function(w){
  const l=wordLesson(w);
  return !!l&&l.book===bid&&l.lesson===lesson;
 });
}""",
    'lesson helpers are shape-agnostic',
)

# 2. the unit row: no chip strip. The lessons live on the unit's own screen.
sub(
    """   ${unitLessonList(b.id,n).length?`<div class="row" style="gap:5px;margin-top:5px;flex-wrap:wrap">${unitLessonList(b.id,n).map(function(l){return `<span class="chip" style="font-size:10px;padding:2px 7px">${l}</span>`;}).join("")}</div>`:""}</div>""",
    """   ${unitLessonList(b.id,n).length?`<div class="meta sub" style="margin-top:3px">${unitLessonList(b.id,n).length} ${t("lessons_w")}</div>`:""}</div>""",
    'unit row: lesson count instead of chips',
)

# 3. the unit screen itself: one row per lesson
sub(
    """ if(v===\"vocab\"){const w=S.lv.session[S.lv.idx];""",
    """ if(v===\"lessons\"){const b=S.lv.book,un=S.lv.unit,ls=unitLessonList(b.id,un);
  el.innerHTML=`
  <div class="vtop"><button class="icobtn" data-lv="units"><svg style="color:var(--deep)"><use href="#i-back"/></svg></button>
  <div><h2 class="h2" style="font-size:19px">${t("unit_w")} ${un}</h2><p class="sub">${b.t} · ${unitCount(b.id,un)} ${t("words")}</p></div></div>`+
  (ls.length?ls.map(function(l){
   const inf=lessonInfo(b.id,l),n=lessonWords(b.id,l).length;
   return `<div class="card lrow row" data-ls="${l}" style="gap:12px;align-items:flex-start">
    <span class="lcode">${l}</span>
    <div style="flex:1;min-width:0">
     <b style="font-size:14px;display:block">${inf&&inf.title?inf.title:l}</b>
     <span class="meta sub">${inf&&inf.topic?inf.topic:t("no_words")}</span>
     <div class="meta sub" style="margin-top:3px;color:var(--green-d);font-weight:800">${n} ${t("words")}</div>
    </div>
    <svg style="width:17px;height:17px;color:var(--muted);flex-shrink:0"><use href="#i-chev"/></svg></div>`;}).join("")
   :`<div class="card" style="text-align:center;color:var(--muted);font-size:13px">${t("no_lessons")}</div>`);
  return;}
 if(v===\"vocab\"){const w=S.lv.session[S.lv.idx];""",
    'new lessons view',
)

# 4. opening a unit goes to its lessons; opening a lesson starts that lesson
sub(
    """  const ws=unitWords(b.id,n);if(!ws.length)return;S.lv={view:"vocab",book:b,unit:n,idx:0,session:ws};renderLearning();return;}""",
    """  const ws=unitWords(b.id,n);if(!ws.length)return;
  /* A unit with lessons opens onto them; a unit without lessons starts straight
     away, so books with a different structure are not forced through a screen
     they have no content for. */
  S.lv={view:unitLessonList(b.id,n).length?"lessons":"vocab",book:b,unit:n,idx:0,session:ws};renderLearning();return;}
 const ls=e.target.closest("[data-ls]");
 if(ls){const code=ls.dataset.ls,b=S.lv.book,ws=lessonWords(b.id,code);
  if(!ws.length)return;
  S.lv={view:"vocab",book:b,unit:S.lv.unit,lesson:code,idx:0,session:ws};renderLearning();return;}""",
    'unit -> lessons -> words',
)

# 5. from a word you go back to the lesson it belongs to, not over its head to
#    the unit list. Books without lessons still go straight back to the units.
sub(
    """  <div class="vtop"><button class="icobtn" data-lv="units"><svg style="color:var(--deep)"><use href="#i-back"/></svg></button>
  <div class="pbar" style="flex:1;margin:0">""",
    """  <div class="vtop"><button class="icobtn" data-lv="${S.lv.lesson||!unitLessonList(S.lv.book.id,S.lv.unit).length?"units":"lessons"}"><svg style="color:var(--deep)"><use href="#i-back"/></svg></button>
  <div class="pbar" style="flex:1;margin:0">""",
    'word view goes back to its lesson',
)

# 6. the flashcard label, without the green pill
sub(
    """  ${(function(){const l=wordLesson(w);if(!l)return "";const inf=lessonInfo(l.book,l.lesson);
     return `<div class="row" style="justify-content:center;gap:7px;margin-bottom:8px"><span class="chip" style="background:var(--green);color:#fff;border:0;font-weight:800">${l.lesson}</span>${inf?`<span class="sub" style="font-size:11.5px">${inf.title}</span>`:""}</div>`;})()}""",
    """  ${(function(){const l=wordLesson(w);if(!l)return "";const inf=lessonInfo(l.book,l.lesson);
     return `<div class="ltag"><span>${l.lesson}</span>${inf&&inf.title?`<i>${inf.title}</i>`:""}</div>`;})()}""",
    'flashcard label restyled',
)

# 7. styles for the new rows
sub(
    """.wrow{padding:13px 16px;margin-top:9px;cursor:pointer}""",
    """.wrow{padding:13px 16px;margin-top:9px;cursor:pointer}
.lrow{padding:13px 16px;margin-top:9px;cursor:pointer;transition:transform .12s}
.lrow:active{transform:scale(.985)}
.lcode{flex-shrink:0;min-width:38px;text-align:center;font-size:12.5px;font-weight:800;
 letter-spacing:.02em;color:var(--green-d);background:var(--mint);border-radius:9px;padding:5px 8px}
.ltag{text-align:center;margin-bottom:9px;font-size:11.5px;color:var(--muted);font-weight:700}
.ltag span{color:var(--deep);letter-spacing:.03em}
.ltag i{font-style:normal;opacity:.8}
.ltag span+i::before{content:" · "}""",
    'styles for lesson rows and the card label',
)

# 8. new strings, three dictionaries at once
sub('no_words:"Not imported yet",',
    'no_words:"Not imported yet",lessons_w:"lessons",no_lessons:"This book teaches whole units, not separate lessons.",',
    'en: lessons_w / no_lessons')
sub('no_words:"Entek goşulmady",',
    'no_words:"Entek goşulmady",lessons_w:"ders",no_lessons:"Bu kitap aýry derslere bölünmän, bitewi bölümler bilen öwredilýär.",',
    'tk: lessons_w / no_lessons')
sub('no_words:"Ещё не добавлено",',
    'no_words:"Ещё не добавлено",lessons_w:"урок(а)",no_lessons:"Эта книга изучается целыми юнитами, без отдельных уроков.",',
    'ru: lessons_w / no_lessons')

open(P, 'w', encoding='utf-8').write(h)
print(f'{len(edits)} edits applied')
for e in edits:
    print('  -', e)
print(f'{len(h.encode("utf-8")):,} bytes')
