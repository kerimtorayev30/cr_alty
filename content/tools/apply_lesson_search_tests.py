#!/usr/bin/env python3
"""Cover the two new behaviours in the test suites, so they cannot regress silently.

Both features were broken in ways the old tests could not see:
  - Search returned zero rows for any query because the default "Recent words"
    chip intersected with the query. The old test set S.filter="all" first, which
    hid exactly the bug the owner hit.
  - Lessons are new, so nothing covered them at all.
"""
import sys

P = 'tests/integration.js'
s = open(P, encoding='utf-8').read()
edits = []


def sub(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f'ABORT [{label}]: anchor matched {n} times, expected 1')
    s = s.replace(old, new, 1)
    edits.append(label)


# ------------------------------------------------------------------ lessons --
sub(
    """  /* ---- 7b. units of books that are not imported yet stay honest ---- */""",
    """  /* ---- 7a. units are taught as lessons 1A / 1B / 1C ---- */
  console.log('\\n[7a] units break down into English File lessons');
  ok(app.live('Object.keys(LESSONS).length') > 20, 'the pack carries lesson metadata', app.live('Object.keys(LESSONS).length'));
  const u1lessons = app.w.eval('unitLessonList("beg",1)');
  ok(JSON.stringify(u1lessons) === '["1A","1B","1C"]', 'unit 1 has lessons 1A, 1B and 1C in order', u1lessons);
  ok(JSON.stringify(app.w.eval('unitLessonList("beg",10)')) === '["10A","10B"]',
     'unit 10 sorts 10A before 10B (a string sort would put 10A first by luck, 2A before 10A by accident)',
     app.w.eval('unitLessonList("beg",10)'));
  app.w.eval('S.lv={view:"units",book:BOOKS[0],unit:null,idx:0,session:[]};renderLearning()');
  await tick(50);
  const rowHtml = app.$$('[data-un]')[0].innerHTML;
  ok(rowHtml.includes('>1A<') && rowHtml.includes('>1B<') && rowHtml.includes('>1C<'),
     'the unit row shows its lesson chips');
  // every word of a unit carries a lesson, and it belongs to that unit
  const mismatched = app.w.eval(`WORDS.filter(function(w){
      return (w.books||[]).some(function(b){return b.book==="beg" && b.lesson && parseInt(b.lesson,10)!==b.unit;});
    }).map(function(w){return w.en;})`);
  ok(mismatched.length === 0, 'no word claims a lesson outside its own unit', mismatched);
  // the flashcard names the lesson it comes from
  app.w.eval('S.lv={view:"vocab",book:BOOKS[0],unit:1,idx:0,session:unitWords("beg",1)};renderLearning()');
  await tick(50);
  const card = app.$('#lv').textContent.replace(/\\s+/g, ' ');
  ok(card.includes('1A'), 'the flashcard labels its lesson', card.slice(0, 60));
  ok(card.includes('A cappuccino, please'), 'the flashcard shows the lesson title', card.slice(0, 80));

  /* ---- 7b. units of books that are not imported yet stay honest ---- */""",
    'test [7a] lessons',
)

# ------------------------------------------------------------------- search --
sub(
    """  /* ---- 8. with NO pack available, the app must fall back to the seed ---- */""",
    """  /* ---- 7c. Search is a trilingual dictionary, not a headword filter ---- */
  console.log('\\n[7c] search finds any word in EN, TM or RU');
  app.w.eval('go("scr-search")');
  await tick(50);
  const rows = () => app.$$('#dictlist .wrow').length;
  const shown = () => app.$('#dictlist').textContent.replace(/\\s+/g, ' ').trim();
  const search = async (q) => {
    app.$('#dinput').value = q;
    app.$('#dinput').dispatchEvent(new app.w.Event('input', { bubbles: true }));
    await tick(30);
    return rows();
  };
  // This is the bug the owner reported: the default chip is "Recent words", and
  // the query used to be intersected with it, so a fresh install found nothing.
  ok(app.live('S.filter') === 'hist', 'a fresh install still defaults to the Recent chip', app.live('S.filter'));
  ok(await search('mug') >= 1, 'typing a word finds it even while the Recent chip is on', rows());
  ok(await search('krujka') >= 1, 'a Turkmen gloss finds the word (TM -> EN)', rows());
  ok(await search('кружка') >= 1, 'a Russian gloss finds the word (RU -> EN)', rows());
  ok(await search('yadaw') >= 1, 'typing without Turkmen diacritics still matches "ýadaw"', rows());
  ok(await search('on the table') >= 1, 'a collocation phrase matches, not just headwords', rows());
  ok(await search('zzz') === 0, 'a word that does not exist returns nothing', rows());
  ok(shown().length > 0, 'and says so instead of showing an empty list', shown().slice(0, 60));
  // the suggestion chips had no click handler at all
  const chip = app.$('[data-q]');
  ok(chip !== null, 'the suggestion chips are still there');
  click(app, chip);
  await tick(30);
  ok(app.$('#dinput').value === chip.dataset.q, 'clicking a suggestion chip fills the search box', app.$('#dinput').value);
  ok(rows() >= 1, 'and runs the search', rows());
  // results must say which language matched
  await search('кружка');
  ok(app.$('#dictlist').innerHTML.includes('RU'), 'a Russian hit is labelled RU');
  await search('');
  ok(rows() === 0, 'clearing the query returns to the Recent list, which is empty on a fresh install', rows());

  /* ---- 8. with NO pack available, the app must fall back to the seed ---- */""",
    'test [7c] trilingual search',
)

open(P, 'w', encoding='utf-8').write(s)
print(f'{len(edits)} edits applied to {P}')
for e in edits:
    print('  -', e)
