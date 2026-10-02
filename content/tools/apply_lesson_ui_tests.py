#!/usr/bin/env python3
"""Bring tests/integration.js in line with the redesigned unit screen.

Three assertions encoded the old design and now fail for the right reason:

  1. "clicking a unit opens the vocabulary view" — a unit whose book has lessons
     now opens onto its lesson list; only a book without lessons starts the words
     directly. The test now walks unit -> lesson -> words.
  2. "the unit row shows its lesson chips" — the chips are gone. The row says how
     many lessons the unit has, and the lessons themselves are rows on the next
     screen.
  3. 'no unit ever claims "0 words"' — the check was a substring test, and
     "60 words" contains "0 words". It now looks at the number itself.

Also adds a check for the bug this round actually produced: a word taught by two
books must not leak into the other book's lesson.
"""
import sys

P = 'tests/integration.js'
s = open(P, encoding='utf-8').read()
n = 0


def sub(old, new, label):
    global s, n
    c = s.count(old)
    if c != 1:
        sys.exit(f'ABORT [{label}]: anchor matched {c} times, expected 1')
    s = s.replace(old, new)
    n += 1
    print('  -', label)


sub("""  const session = app.w.eval('S.lv.session');
  ok(app.live('S.lv.view') === 'vocab', 'clicking a unit opens the vocabulary view', app.live('S.lv.view'));
  ok(session.length === u1count, 'the session is every word of that unit', { got: session.length, want: u1count });""",
    """  // Beginner unit 1 has lessons, so the unit opens onto them rather than
  // straight into the words.
  ok(app.live('S.lv.view') === 'lessons', 'clicking a unit with lessons opens its lesson list', app.live('S.lv.view'));
  const lessonRows = app.$$('[data-ls]');
  ok(lessonRows.length === app.live('unitLessonList("beg",1).length'),
     'every lesson of the unit is a row of its own', { rows: lessonRows.length });
  ok(lessonRows[0].textContent.includes('A cappuccino, please'),
     'the lesson row names the lesson', lessonRows[0].textContent.replace(/\\s+/g, ' ').trim());
  click(app, lessonRows[0]);
  await tick(50);
  ok(app.live('S.lv.view') === 'vocab', 'clicking a lesson opens the vocabulary view', app.live('S.lv.view'));
  const session = app.w.eval('S.lv.session');
  const u1l1count = app.live('lessonWords("beg","1A").length');
  ok(session.length === u1l1count, 'the session is every word of that lesson', { got: session.length, want: u1l1count });
  // and the words of a whole unit still add up
  ok(app.live('unitWords("beg",1).length') === u1count,
     'the unit count is still the sum of its words', { got: app.live('unitWords("beg",1).length'), want: u1count });""",
    'unit -> lessons -> words',
)

sub("""  const rowHtml = app.$$('[data-un]')[0].innerHTML;
  ok(rowHtml.includes('>1A<') && rowHtml.includes('>1B<') && rowHtml.includes('>1C<'),
     'the unit row shows its lesson chips');""",
    """  const rowHtml = app.$$('[data-un]')[0].innerHTML;
  ok(rowHtml.includes('3 lessons'), 'the unit row says how many lessons it has',
     app.$$('[data-un]')[0].textContent.replace(/\\s+/g, ' ').trim());
  ok(!rowHtml.includes('>1A<'), 'the unit row no longer carries lesson chips',
     'chips were replaced by a lesson list on the unit screen');
  // a book that teaches whole units, with no lessons, must not grow an empty list
  app.w.eval('S.lv={view:"units",book:BOOKS.find(function(b){return b.id==="advp"}),unit:null,idx:0,session:[]};renderLearning()');
  await tick(50);
  ok(!app.$$('[data-un]')[0].textContent.includes('lessons'),
     'a book with no lessons does not claim to have any',
     app.$$('[data-un]')[0].textContent.replace(/\\s+/g, ' ').trim());
  app.w.eval('S.lv={view:"units",book:BOOKS[0],unit:null,idx:0,session:[]};renderLearning()');
  await tick(50);""",
    'lesson count instead of chips',
)

sub("""  ok(!eleRow.includes('0 words'), 'no unit ever claims "0 words"', eleRow);""",
    """  // A substring test would fail on "60 words", which contains "0 words".
  ok(!/(?:^|\\s)0 words/.test(eleRow), 'no unit ever claims "0 words"', eleRow);""",
    'the 0-words check reads the number, not a substring',
)

sub("""  ok(card.includes('A cappuccino, please'), 'the flashcard shows the lesson title', card.slice(0, 80));""",
    """  ok(card.includes('A cappuccino, please'), 'the flashcard shows the lesson title', card.slice(0, 80));

  /* ---- 7a2. a word two books teach does not leak into the other's lesson ---- */
  console.log('\\n[7a2] a word shared by two books stays in its own lesson per book');
  ok(app.live('unitLessonList("ele",1).join(",")') === '1A,1B,1C',
     'the Elementary book has its own lessons', app.live('unitLessonList("ele",1)'));
  ok(app.live('lessonWords("ele","1A").length') === app.live('LESSONS["ele|1A"].words'),
     'an Elementary lesson holds exactly the words its own book lists',
     { got: app.live('lessonWords("ele","1A").length'), want: app.live('LESSONS["ele|1A"].words') });
  ok(app.live('lessonWords("ele","1A").every(function(w){return (w.books||[]).some(function(b){return b.book==="ele" && b.lesson==="1A";});})'),
     'no other book\\'s word appears in an Elementary lesson');
  ok(app.live('lessonWords("beg","1A").every(function(w){return (w.books||[]).some(function(b){return b.book==="beg" && b.lesson==="1A";});})'),
     'and none in a Beginner lesson either');
  // the card labels itself from the book being studied, not the word's home book
  app.w.eval('S.lv={view:"vocab",book:BOOKS.find(function(b){return b.id==="ele"}),unit:1,lesson:"1A",idx:0,session:lessonWords("ele","1A")};renderLearning()');
  await tick(50);
  const eleCard = app.$('#lv').textContent.replace(/\\s+/g, ' ');
  ok(eleCard.includes('Welcome to the class'),
     'studying Elementary labels the card with the Elementary lesson', eleCard.slice(0, 80));
  ok(!eleCard.includes('A cappuccino, please'),
     'and not with the Beginner lesson the same word also belongs to', eleCard.slice(0, 80));""",
    'shared words stay in their own lesson per book',
)

open(P, 'w', encoding='utf-8').write(s)
print(f'{n} edits applied to {P}')
