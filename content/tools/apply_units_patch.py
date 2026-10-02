#!/usr/bin/env python3
"""Wire the Learning screen to the real book units.

Before this patch the units view was cosmetic:
  - every unit claimed "24 words"
  - opening unit n did WORDS.slice((n*2)%7, +6), i.e. an arbitrary slice of the
    whole word bank that ignored both the book and the unit
  - BOOKS[0] said the Beginner book had 10 units; it has 12
  - the dictionary's "learn" button always opened unit 1 of Beginner with the
    first six words, whatever word you were looking at

The content pack now carries books:[{book,unit}] per word (content/data/beginner.json),
so a session can be the actual words of the actual unit.

Idempotent-ish: it refuses to run twice by asserting each anchor matches exactly once.
Every anchor is copied from the file's real bytes, never re-typed.
"""
import sys

PATH = 'uploads/app-yatla.html'
h = open(PATH, encoding='utf-8').read()
start_len = len(h)
applied = []


def sub(old, new, label):
    global h
    n = h.count(old)
    if n != 1:
        sys.exit(f'ABORT [{label}]: anchor matched {n} times, expected 1')
    if new in h and old not in h:
        sys.exit(f'ABORT [{label}]: replacement already present')
    h = h.replace(old, new, 1)
    applied.append(label)


# 1. helpers, right after the content loader and before the DATA block
sub(
    """})();

/* ================= DATA ================= */""",
    """})();

/* ================= UNITS ================= */
/* Content words carry books:[{book,unit}]. unitWords() is the single place that
   turns that into a session, so the units list, the unit screen and the
   dictionary all agree. Words without a unit (the seed words, packs from books
   that are not imported yet) belong to no unit and are never dropped. */
function unitWords(bid,un){
 return WORDS.filter(function(w){
  const bs=w.books;
  if(!bs||!bs.length)return false;
  return bs.some(function(b){return b.book===bid&&b.unit===un;});
 });
}
function unitCount(bid,un){return unitWords(bid,un).length;}
/* the first book/unit that teaches this word, used by the dictionary's "learn" */
function wordBook(w){
 if(w.books&&w.books.length&&w.books[0].book)return {bk:BOOKS.find(function(b){return b.id===w.books[0].book;})||BOOKS[0],un:w.books[0].unit};
 return {bk:BOOKS[0],un:1};
}

/* ================= DATA ================= */""",
    'unit helpers',
)

# 2. real word count per unit instead of the hardcoded 24
sub(
    """<div class="meta sub">24 ${t("words")} · ${st===""",
    """<div class="meta sub">${unitCount(b.id,n)||"—"} ${t("words")} · ${st===""",
    'unit word count',
)

# 3. opening a unit starts that unit's words
sub(
    """  const off=(n*2)%7;S.lv={view:"vocab",book:b,unit:n,idx:0,session:WORDS.slice(off,off+6)};renderLearning();return;}""",
    """  const ws=unitWords(b.id,n);if(!ws.length)return;S.lv={view:"vocab",book:b,unit:n,idx:0,session:ws};renderLearning();return;}""",
    'unit session',
)

# 4. the book really has 12 units (the contents table lists 1–12)
sub(
    """{id:"beg",t:"Beginner",lv:"A1",c:"linear-gradient(160deg,#FB923C,#F97316)",units:10,""",
    """{id:"beg",t:"Beginner",lv:"A1",c:"linear-gradient(160deg,#FB923C,#F97316)",units:12,""",
    'beginner unit count',
)

# 5. the dictionary's "learn" button goes to the word's own unit
sub(
    """d.querySelector("[data-slearn]").onclick=()=>{S.lv={view:"vocab",book:BOOKS[0],unit:1,idx:WORDS.indexOf(w)%6,session:WORDS.slice(0,6)};go2learning();};""",
    """d.querySelector("[data-slearn]").onclick=()=>{const wb=wordBook(w);const ws=unitWords(wb.bk.id,wb.un);S.lv={view:"vocab",book:wb.bk,unit:wb.un,idx:Math.max(0,ws.indexOf(w)),session:ws.length?ws:[w]};go2learning();};""",
    'dictionary learn button',
)

open(PATH, 'w', encoding='utf-8').write(h)
print(f'{len(applied)} edits applied')
for a in applied:
    print('  -', a)
print(f'{start_len} -> {len(h)} chars')
