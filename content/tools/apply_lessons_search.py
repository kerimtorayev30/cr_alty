#!/usr/bin/env python3
"""Two owner-requested changes, in one patch.

A) LESSONS. English File units are taught as lessons 1A/1B/1C. The pack now
   carries books:[{book,unit,lesson}] plus a `lessons` metadata list, so the app
   can say which lesson a word belongs to and list a unit's lessons.

B) SEARCH. Search was broken in practice: the "Recent words" chip is the default
   filter and filt() intersected the query with it, so on a fresh install typing
   anything returned zero rows — you had to know to press "All words" first.
   Measured before this patch: "mug" -> 0 rows, "suw" -> 0, "вода" -> 0; after
   switching to All words, "mug" -> 1.
   Also the two suggestion chips (data-q="suw" / "teacher") had no click handler
   anywhere in the file, so they were dead buttons.

   Now: a non-empty query always searches the whole bank, in all three languages
   and across every field of the entry; the chips only scope the empty query.

Every anchor below was copied from the file's real bytes. The script aborts if an
anchor does not match exactly once.
"""
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


# ---------------------------------------------------------------- A. lessons --

# A1. helpers, appended to the UNITS block
sub(
    """/* the first book/unit that teaches this word, used by the dictionary's "learn" */""",
    """/* --- lessons: English File teaches each unit as 1A / 1B / 1C ---------------- */
/* LESSONS is filled from the pack's `lessons` list at load time. It is a map of
   "book|lesson" -> {lesson,unit,title,topic,words}. Without the pack it stays
   empty and every lesson label simply does not render — no fallback text needed. */
var LESSONS={};
function wordLesson(w){
 if(!w||!w.books||!w.books.length)return null;
 const b=w.books[0];
 return b.lesson?{lesson:b.lesson,book:b.book}:null;
}
function lessonInfo(book,lesson){return LESSONS[book+"|"+lesson]||null;}
/* the lessons of a unit, in order, so the unit row can show "1A 1B 1C" */
function unitLessonList(bid,un){
 const out=[];
 WORDS.forEach(function(w){
  const l=wordLesson(w);
  if(l&&l.book===bid&&l.unit===un&&out.indexOf(l.lesson)<0)out.push(l.lesson);
 });
 return out.sort(function(a,b){
  const na=parseInt(a,10),nb=parseInt(b,10);
  return na-nb||(a<nb?-1:a>b?1:0);
 });
}

/* the first book/unit that teaches this word, used by the dictionary's "learn" */""",
    'lesson helpers',
)

# A2. the unit row shows its lessons
sub(
    """</div></div>
   ${st===\"lock\"?`<svg style=\"width:17px;height:17px;color:var(--muted)\"><use href=\"#i-lock\"/></svg>`""",
    """</div>
   ${unitLessonList(b.id,n).length?`<div class="row" style="gap:5px;margin-top:5px;flex-wrap:wrap">${unitLessonList(b.id,n).map(function(l){return `<span class="chip" style="font-size:10px;padding:2px 7px">${l}</span>`;}).join("")}</div>`:""}</div>
   ${st===\"lock\"?`<svg style=\"width:17px;height:17px;color:var(--muted)\"><use href=\"#i-lock\"/></svg>`""",
    'unit row lists its lessons',
)

# A3. the flashcard says which lesson the word comes from
sub(
    """  <div class="card vcard">
   <div class="vword">${w.en}</div>""",
    """  ${(function(){const l=wordLesson(w);if(!l)return "";const inf=lessonInfo(l.book,l.lesson);
     return `<div class="row" style="justify-content:center;gap:7px;margin-bottom:8px"><span class="chip" style="background:var(--green);color:#fff;border:0;font-weight:800">${l.lesson}</span>${inf?`<span class="sub" style="font-size:11.5px">${inf.title}</span>`:""}</div>`;})()}
  <div class="card vcard">
   <div class="vword">${w.en}</div>""",
    'flashcard shows its lesson',
)

# A4. keep LESSONS in sync with the pack
sub(
    """YatlaContent.fetchWords({url:"content/build/yatla-words.min.json"}).then(function(r){
  if(!r.words||!r.words.length)return;""",
    """YatlaContent.fetchWords({url:"content/build/yatla-words.min.json"}).then(function(r){
  if(!r.words||!r.words.length)return;
  if(r.lessons&&r.lessons.length){
    LESSONS={};
    r.lessons.forEach(function(l){if(l&&l.lesson&&l.book)LESSONS[l.book+"|"+l.lesson]=l;});
  }""",
    'LESSONS filled from the pack',
)

# ----------------------------------------------------------------- B. search --

# B1. the search itself
sub(
    """function filt(){const q=($(\"#dinput\").value||\"\").trim().toLowerCase();let n=0;
 /* Filters are content-neutral on purpose: recent words, favourites, or everything.
    Book filtering was removed from Search, and so were the memory-stage chips. */
 $(\"#dictlist\").innerHTML=WORDS.map((w,i)=>{
  const hitF=S.filter===\"all\"?true:S.filter===\"fav\"?S.favs.has(w.en):S.hist.includes(w.en);
  const hit=!q||w.en.includes(q)||w.tm.toLowerCase().includes(q)||w.ru.toLowerCase().includes(q);
  const show=hit&&hitF;if(show)n++;
  return `<div class=\"card wrow row spread\" data-w=\"${i}\" style=\"display:${show?\"\":\"none\"}\">
   <div><b>${w.en}</b><span class=\"en\">${w.tm} · ${w.ru}</span></div>
   <div class=\"row\" style=\"gap:8px\">${S.favs.has(w.en)?`<svg style=\"width:15px;height:15px;color:var(--red)\"><use href=\"#i-heart\"/></svg>`:\"\"}</div></div>`;}).join(\"\");
 if(!n&&!q&&S.filter===\"hist\")$(\"#dictlist\").innerHTML=`<div class=\"card\" style=\"text-align:center;color:var(--muted);font-size:13px\">${t(\"no_recent\")}</div>`;
 $(\"#dcount\").textContent=n+\" \"+t(\"words\");}""",
    """/* Diacritic folding, so "sag bolsun" finds "sag boluň" and "turkmen" finds
   "Türkmen". Turkmen and Russian both use letters an English keyboard lacks. */
function fold(s){return (s||"").toLowerCase().replace(/[\\u0300-\\u036f]/g,\"\")
 .replace(/ý/g,\"y\").replace(/ň/g,\"n\").replace(/ä/g,\"a\").replace(/ö/g,\"o\").replace(/ü/g,\"u\")
 .replace(/ş/g,\"s\").replace(/ç/g,\"c\").replace(/ž/g,\"z\").replace(/â/g,\"a\").replace(/î/g,\"i\").replace(/û/g,\"u\")
 .replace(/ё/g,\"е\").replace(/й/g,\"и\");}
/* Cyrillic input means the user is typing Russian; Latin means EN or TM. */
function isCyr(s){return /[\\u0400-\\u04FF]/.test(s||\"\");}
/* One entry, every field, all three languages. This is what makes Search a
   dictionary rather than a headword filter: a Russian speaker who only remembers
   part of a translation still finds the word. */
function searchScore(w,q){
 const fields=[[fold(w.en),3],[fold(w.tm),3],[fold(w.ru),3],[fold(w.ipa),1],
  [fold(w.def),1],[fold(w.ex),1],[fold(w.syn),2],[fold(w.coll),2]];
 let best=0,langs=[];
 fields.forEach(function(f,i){
  if(!f[0])return;
  const k=f[0].indexOf(q);
  if(k<0)return;
  const sc=f[1]+(k===0?2:0)+(f[0]===q?3:0);
  if(sc>best)best=sc;
  const lang=i===0?\"EN\":i===1?\"TM\":i===2?\"RU\":null;
  if(lang&&langs.indexOf(lang)<0)langs.push(lang);
 });
 return {score:best,langs:langs};
}
function filt(){const q=fold(($(\"#dinput\").value||\"\").trim());let n=0;
 /* A query is a dictionary lookup: it always searches the whole bank, in every
    language, whatever chip is selected. The chips only scope the EMPTY query —
    otherwise the default "Recent words" chip silently hides every result, which
    is exactly how Search looked broken. */
 const cyr=isCyr($(\"#dinput\").value||\"\");
 let list=WORDS.map(function(w,i){return {w:w,i:i};});
 if(q){
  list=list.map(function(o){const r=searchScore(o.w,q);return {w:o.w,i:o.i,s:r.score,langs:r.langs};})
   .filter(function(o){return o.s>0;})
   /* exact match first, then prefix, then the rest; ties keep dictionary order */
   .sort(function(a,b){return b.s-a.s||a.i-b.i;});
 }else{
  list=list.filter(function(o){
   return S.filter===\"all\"?true:S.filter===\"fav\"?S.favs.has(o.w.en):S.hist.includes(o.w.en);
  }).map(function(o){return {w:o.w,i:o.i,s:0,langs:[]};});
 }
 n=list.length;
 $(\"#dictlist\").innerHTML=list.map(function(o){
  const w=o.w;
  const badge=o.langs.length?`<span class="pos" style="margin-left:6px">${o.langs.join(" · ")}</span>`:"";
  const les=(function(){const l=wordLesson(w);return l?`<span class="pos" style="background:var(--mint)">${l.lesson}</span>`:"";})();
  return `<div class="card wrow row spread" data-w="${o.i}">
   <div style="min-width:0"><b>${w.en}</b>${badge}<span class="en">${w.tm} · ${w.ru}</span>
    <span class="en" style="font-weight:600;opacity:.75">${w.ipa} · ${w.pos}</span></div>
   <div class="row" style="gap:8px;flex-shrink:0">${les}${S.favs.has(w.en)?`<svg style="width:15px;height:15px;color:var(--red)"><use href="#i-heart"/></svg>`:""}</div></div>`;}).join("");
 if(!n){
  $(\"#dictlist\").innerHTML=`<div class="card" style="text-align:center;color:var(--muted);font-size:13px">${q?t("no_res"):S.filter===\"hist\"?t("no_recent"):S.filter===\"fav\"?t("no_favs"):t("no_words_yet")}</div>`;
 }
 $(\"#dcount\").textContent=n+\" \"+t(\"words\");
 /* While a query is active the chips would lie, so say what is being searched. */
 const sc=$(\"#schips\");
 if(sc)sc.querySelectorAll(\"[data-f]\").forEach(function(b){b.classList.toggle(\"on\",!q&&b.dataset.f===S.filter);});}""",
    'search: whole bank, three languages, every field',
)

# B2. the suggestion chips were dead — wire them
sub(
    """$(\"#dinput\").addEventListener(\"input\",filt);""",
    """$(\"#dinput\").addEventListener(\"input\",filt);
/* The suggestion chips had no handler at all, so they were dead buttons. */
$(\"#schips\").addEventListener(\"click\",function(e){
 const c=e.target.closest(\"[data-q]\");
 if(!c)return;
 $(\"#dinput\").value=c.dataset.q;filt();
 const dl=$(\"#dictlist .wrow\");
 if(dl&&dl.scrollIntoView)try{dl.scrollIntoView({block:\"nearest\"});}catch(err){}
});""",
    'suggestion chips work',
)

# B3. honest empty-state strings, in all three dictionaries at once
sub('no_words:"Not imported yet",', 'no_words:"Not imported yet",no_res:"No word matches that. Try part of a word, in English, Türkmen or Russian.",no_favs:"No favourites yet — tap the heart on any word.",no_words_yet:"The word bank is empty on this device.",', 'en: no_res / no_favs / no_words_yet')
sub('no_words:"Entek goşulmady",', 'no_words:"Entek goşulmady",no_res:"Hiç söz tapylmady. Sözüň bir bölegini iňlisçe, türkmençe ýa-da rusça synanyşyň.",no_favs:"Entek halanan söz ýok — islendik sözüň ýürejigine basyň.",no_words_yet:"Bu enjamda söz banky boş.",', 'tk: no_res / no_favs / no_words_yet')
sub('no_words:"Ещё не добавлено",', 'no_words:"Ещё не добавлено",no_res:"Ничего не найдено. Попробуйте часть слова — по-английски, по-туркменски или по-русски.",no_favs:"Избранного пока нет — нажмите на сердечко у любого слова.",no_words_yet:"На этом устройстве словарь пуст.",', 'ru: no_res / no_favs / no_words_yet')

open(P, 'w', encoding='utf-8').write(h)
print(f'{len(edits)} edits applied')
for e in edits:
    print('  -', e)
print(f'{len(h.encode("utf-8")):,} bytes')
