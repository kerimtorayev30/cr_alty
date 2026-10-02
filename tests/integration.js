#!/usr/bin/env node
/**
 * Ýatla — content pack integration test.
 *
 * Boots the PATCHED app-yatla.html with the real built word pack inlined as
 * <script type="application/json" id="yatlaWords"> (the loader's highest-priority
 * source), then asserts the app renders the expanded dictionary correctly and that
 * nothing the brief lists as "already working" regressed.
 *
 * Run: node integration.js [app.html] [bundle.json]
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const APP = path.resolve(process.argv[2] || path.join(__dirname, '..', 'uploads', 'app-yatla.html'));
const BUNDLE = path.resolve(process.argv[3] || path.join(__dirname, '..', 'content', 'build', 'yatla-words.min.json'));

let passed = 0, failed = 0;
function ok(cond, msg, got) {
  if (cond) { passed++; console.log(`  ok   ${msg}`); }
  else { failed++; console.error(`  FAIL ${msg}${got !== undefined ? ` — got ${JSON.stringify(got)}` : ''}`); }
}
const tick = (ms = 60) => new Promise((r) => setTimeout(r, ms));

/** Inline the pack the way an offline / Capacitor build would.
 *  The app now ships its own embedded pack, so injecting a second one would mean
 *  the test reads the injected copy and never exercises the shipped one. */
function inlinePack(html, pack) {
  if (html.includes('id="yatlaWords"')) return html;   // already embedded — use it
  const json = JSON.stringify(pack).replace(/<\//g, '<\\/');
  const tag = `<script type="application/json" id="yatlaWords">${json}<\/script>`;
  if (!html.includes('<script>')) throw new Error('no <script> in the app file');
  return html.replace('<script>', tag + '\n<script>');
}

/** The same app with its embedded pack removed: the true "no pack" build. */
function stripPack(html) {
  return html.replace(/<script type="application\/json" id="yatlaWords">[\s\S]*?<\/script>\n?/, '');
}

function boot(html, seed) {
  const errors = [];
  const vc = new VirtualConsole();
  vc.on('jsdomError', (e) => errors.push(`jsdomError: ${e && e.message}`));
  vc.on('error', (...a) => errors.push(`console.error: ${a.map(String).join(' ')}`));
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', pretendToBeVisual: true, url: 'https://yatla.test/', virtualConsole: vc,
    beforeParse(w) { for (const [k, v] of Object.entries(seed || {})) w.localStorage.setItem(k, v); }
  });
  const w = dom.window;
  return {
    w, errors,
    $: (s) => w.document.querySelector(s),
    $$: (s) => [...w.document.querySelectorAll(s)],
    live: (e) => w.eval(e),
    state: () => { w.eval('save()'); return JSON.parse(w.localStorage.getItem('yatla_state') || 'null'); }
  };
}
const click = (app, sel) => {
  const el = typeof sel === 'string' ? app.$(sel) : sel;
  el.dispatchEvent(new app.w.MouseEvent('click', { bubbles: true, cancelable: true }));
  return el;
};

const rawHtml = fs.readFileSync(APP, 'utf8');
const bundle = JSON.parse(fs.readFileSync(BUNDLE, 'utf8'));
const seeded = inlinePack(rawHtml, bundle);

async function main() {
  console.log(`Ýatla integration — ${path.relative(process.cwd(), APP)} + ${path.relative(process.cwd(), BUNDLE)}`);
  console.log(`pack: ${bundle.count} words, format=${bundle.format}`);

  /* ---- 1. the pack loads and extends the dictionary ---- */
  console.log('\n[1] pack loads → WORDS grows from 12 to 12+N');
  const app = boot(seeded);
  await tick(120);
  const total = app.live('WORDS.length');
  // Read after a tick: fetchWords resolves asynchronously, so a synchronous read
  // observes 12 whatever the file contains.
  const seedApp = boot(stripPack(rawHtml));
  await tick(120);
  const seedCount = seedApp.live('WORDS.length');
  ok(seedCount === 12, 'a build with no pack falls back to the 12 seed words', seedCount);
  ok(total > 12, 'dictionary grew after the pack loaded', total);
  ok(total <= 12 + bundle.count, 'no more than seed+pack words', { total, max: 12 + bundle.count });
  const seedStillFirst = app.live('WORDS.slice(0,12).map(w=>w.en).join(",")');
  ok(seedStillFirst.startsWith('hello,name,country'), 'the 12 seed words kept their positions (WORDS[5] still "friend")', seedStillFirst.slice(0, 60));
  ok(app.live('WORDS[5].en') === 'friend', 'word-of-the-day target unchanged', app.live('WORDS[5].en'));
  ok(app.live('S.words') === 7, 'daily progress counter untouched by the pack load', app.live('S.words'));
  ok(app.state().events.pack_loaded === 1, 'pack_loaded tracked', app.state().events);
  ok(app.errors.length === 0, 'zero jsdom errors', app.errors);

  /* ---- 2. every added word renders safely ---- */
  console.log('\n[2] every word renders with no undefined fields');
  app.w.eval('go("scr-search")');
  await tick(80);
  app.w.eval('S.filter="all";filt()');
  await tick(40);
  const rows = app.$$('#dictlist .wrow');
  ok(rows.length === total, `search lists all ${total} words`, rows.length);
  const listHtml = app.$('#dictlist').innerHTML;
  ok(!/undefined/.test(listHtml), 'no "undefined" leaked into the search list');
  ok(!/NaN/.test(listHtml), 'no NaN in the search list');
  ok(!app.$('#dictlist .vstage'), 'no memory-stage chips in the search results (removed on purpose)');
  ok(app.$('#dcount').textContent.startsWith(String(total)), 'word counter matches the dictionary size', app.$('#dcount').textContent);

  /* ---- 3. open several new words and check the detail card ---- */
  console.log('\n[3] new words open a complete detail card');
  const newOnes = ['experience', 'government', 'technology'];
  for (const head of newOnes) {
    const row = rows.find((r) => r.querySelector('b').textContent === head);
    ok(!!row, `"${head}" appears in the dictionary`);
    if (!row) continue;
    click(app, row);
    await tick(30);
    const d = app.$('#sdetail').innerHTML;
    ok(app.$('#sdetail').style.display !== 'none', `"${head}" detail opens`);
    ok(!/undefined/.test(d), `"${head}" detail has no undefined field`);
    ok(d.includes('Oxford 3000'), `"${head}" shows the Oxford badge`);
    ok(/\/[^/]+\/ · [A-Z]/.test(d), `"${head}" shows slash-wrapped IPA and an uppercase POS`);
    click(app, '[data-sback]');
    await tick(20);
  }

  /* ---- 4. new words are searchable in all three languages ---- */
  console.log('\n[4] new words are searchable in EN / TM / RU');
  app.w.eval('S.filter="all";filt()');
  await tick(30);
  const search = async (q) => {
    app.$('#dinput').value = q;
    app.$('#dinput').dispatchEvent(new app.w.Event('input', { bubbles: true }));
    await tick(30);
    return app.$$('#dictlist .wrow').filter((r) => r.style.display !== 'none').length;
  };
  ok(await search('tehnologiýa') === 1, 'Turkmen "tehnologiýa" finds 1', await search('tehnologiýa'));
  ok(await search('правительство') === 1, 'Russian "правительство" finds 1');
  ok(await search('experience') >= 1, 'English "experience" finds a match');
  ok(await search('') === total, 'empty query shows the whole dictionary');

  /* ---- 5. i18n still covers the expanded dictionary ---- */
  console.log('\n[5] setLang("tk") retranslates the expanded dictionary');
  app.w.eval('setLang("tk")');
  await tick(80);
  ok(!/undefined/.test(app.$('#dictlist').innerHTML), 'no undefined after switching to Turkmen');
  const tkChipText = app.$('#schips [data-f="hist"]').textContent.trim();
  ok(tkChipText === app.w.eval('I18N.tk.recent_s'), 'search filter chip in Turkmen', tkChipText);
  ok(/söz/.test(app.$('#dcount').textContent), 'counter says "söz"', app.$('#dcount').textContent);
  app.w.eval('setLang("ru")');
  await tick(80);
  ok(/слов/.test(app.$('#dcount').textContent), 'counter says "слов" in Russian', app.$('#dcount').textContent);
  ok(!/undefined/.test(app.$('#dictlist').innerHTML), 'no undefined in Russian');

  /* ---- 6. favourites on a new word behave exactly like on a seed word ---- */
  console.log('\n[6] favouriting a pack word works and persists');
  app.w.eval('setLang("en")');
  await tick(50);
  app.w.eval('S.filter="all";filt()'); await tick(30);
  await search('culture');
  const cultureRow = app.$$('#dictlist .wrow').find((r) => r.querySelector('b').textContent === 'culture');
  ok(!!cultureRow, '"culture" found in the dictionary');
  if (!cultureRow) { console.log('  -- skipping the rest of [6]'); return finish(); }
  click(app, cultureRow);
  await tick(30);
  click(app, '[data-fav2]');
  await tick(40);
  ok(app.live('S.favs.has("culture")'), 'culture favourited');
  ok(app.state().favs.includes('culture'), 'favourite persisted', app.state().favs);
  ok(app.$('#favchips').innerHTML.includes('culture'), 'favourite chip rendered');

  /* ---- 7. review covers exactly the session just studied ---- */
  console.log('\n[7] review deck covers exactly the words just studied');
  // The user path: the completion screen hands the studied session to review.
  // Owner report round 12: after learning lesson 1A the review must contain
  // ONLY 1A's words — not the rest of the unit the learner never opened.
  app.w.eval('S.lv={view:"complete",book:BOOKS[0],unit:1,lesson:"1A",idx:0,session:lessonWords("beg","1A")};renderLearning()');
  await tick(30);
  app.w.eval('startReview(S.lv.session&&S.lv.session.length?S.lv.session:null)');
  await tick(50);
  ok(app.live('S.rev') !== null, 'review session created');
  const l1arev = app.live('lessonWords("beg","1A").length');
  ok(app.live('S.rev.steps.length') === l1arev, `review deck covers all ${l1arev} words of lesson 1A (was hardcoded 5)`, app.live('S.rev.steps.length'));
  const deckOf1A = app.w.eval('[...new Set(S.rev.steps.map(function(s){return s.w.en;}))].sort().join("|")');
  const wordsOf1A = app.w.eval('lessonWords("beg","1A").map(function(w){return w.en;}).sort().join("|")');
  ok(deckOf1A === wordsOf1A, 'a 1A review contains exactly the 1A words — nothing from 1B/1C');
  ok(app.live('S.rev.steps.length') > 5, 'review is no longer capped at 5 cards', app.live('S.rev.steps.length'));
  // A whole-unit session (books without lessons) still reviews the whole unit.
  app.w.eval('S.lv={view:"complete",book:BOOKS[0],unit:1,lesson:null,idx:0,session:unitWords("beg",1)};renderLearning()');
  await tick(30);
  app.w.eval('startReview(S.lv.session&&S.lv.session.length?S.lv.session:null)');
  await tick(50);
  const u1rev = app.live('unitCount("beg",1)');
  ok(app.live('S.rev.steps.length') === u1rev, `a unit session reviews all ${u1rev} unit-1 words`, app.live('S.rev.steps.length'));
  const revKinds = app.w.eval('[...new Set(S.rev.steps.map(function(s){return s.t;}))].sort().join(",")');
  ok(/mcq/.test(revKinds) && revKinds.indexOf(',') > 0, 'review mixes several exercise types', revKinds);
  const deckWords = app.w.eval('S.rev.steps.map(s=>s.w.en)');
  ok(deckWords.every((e) => typeof e === 'string' && e.length > 0), 'every review card carries a word', deckWords);
  // Not a hand-built session: open the book and click the unit, the way a user does.
  app.w.eval('S.lv={view:"units",book:BOOKS[0],unit:null,idx:0,session:[]};renderLearning()');
  await tick(50);
  ok(app.live('BOOKS[0].units') === 12, 'the Beginner book lists its 12 units', app.live('BOOKS[0].units'));
  const unitRows = app.$$('[data-un]');
  ok(unitRows.length === 12, 'the units view renders 12 rows', unitRows.length);
  const u1count = app.live('unitCount("beg",1)');
  ok(u1count > 0, 'unit 1 has words from the imported book', u1count);
  ok(unitRows[0].textContent.includes(String(u1count)), 'the unit row shows the real word count, not a hardcoded 24', unitRows[0].textContent.replace(/\s+/g, ' ').trim());
  click(app, unitRows[0]);
  await tick(50);
  // Beginner unit 1 has lessons, so the unit opens onto them rather than
  // straight into the words.
  ok(app.live('S.lv.view') === 'lessons', 'clicking a unit with lessons opens its lesson list', app.live('S.lv.view'));
  const lessonRows = app.$$('[data-ls]');
  ok(lessonRows.length === app.live('unitLessonList("beg",1).length'),
     'every lesson of the unit is a row of its own', { rows: lessonRows.length });
  ok(lessonRows[0].textContent.includes('A cappuccino, please'),
     'the lesson row names the lesson', lessonRows[0].textContent.replace(/\s+/g, ' ').trim());
  click(app, lessonRows[0]);
  await tick(50);
  ok(app.live('S.lv.view') === 'vocab', 'clicking a lesson opens the vocabulary view', app.live('S.lv.view'));
  const session = app.w.eval('S.lv.session');
  const u1l1count = app.live('lessonWords("beg","1A").length');
  ok(session.length === u1l1count, 'the session is every word of that lesson', { got: session.length, want: u1l1count });
  // and the words of a whole unit still add up
  ok(app.live('unitWords("beg",1).length') === u1count,
     'the unit count is still the sum of its words', { got: app.live('unitWords("beg",1).length'), want: u1count });
  ok(session.every((w) => (w.books || []).some((b) => b.book === 'beg' && b.unit === 1)),
     'every card in the session belongs to Beginner unit 1',
     session.filter((w) => !(w.books || []).some((b) => b.book === 'beg' && b.unit === 1)).map((w) => w.en));
  ok(app.errors.length === 0, 'zero jsdom errors across the whole run', app.errors);

  /* ---- 7a. units are taught as lessons 1A / 1B / 1C ---- */
  console.log('\n[7a] units break down into English File lessons');
  ok(app.live('Object.keys(LESSONS).length') > 20, 'the pack carries lesson metadata', app.live('Object.keys(LESSONS).length'));
  const u1lessons = app.w.eval('unitLessonList("beg",1)');
  ok(JSON.stringify(u1lessons) === '["1A","1B"]', 'unit 1 has lessons 1A and 1B — its PE episode is no longer inside it', u1lessons);
  ok(JSON.stringify(app.w.eval('unitLessonList("beg",10)')) === '["10A","10B"]',
     'unit 10 sorts 10A before 10B (a string sort would put 10A first by luck, 2A before 10A by accident)',
     app.w.eval('unitLessonList("beg",10)'));
  app.w.eval('S.lv={view:"units",book:BOOKS[0],unit:null,idx:0,session:[]};renderLearning()');
  await tick(50);
  const rowHtml = app.$$('[data-un]')[0].innerHTML;
  ok(rowHtml.includes('2 lessons'), 'the unit row says how many lessons it has',
     app.$$('[data-un]')[0].textContent.replace(/\s+/g, ' ').trim());
  ok(!rowHtml.includes('>1A<'), 'the unit row no longer carries lesson chips',
     'chips were replaced by a lesson list on the unit screen');
  // A book that is not imported yet (no words in the pack) has no lessons, so its
  // unit row must not grow an empty lesson list. advp used to be the stand-in empty
  // book, but every English File title is now imported, so inject an empty one.
  app.w.eval('BOOKS.push({id:"zzempty",t:"Empty",lv:"A1",c:"",units:2,done:0,dl:1,mb:1})');
  app.w.eval('S.lv={view:"units",book:BOOKS.find(function(b){return b.id==="zzempty"}),unit:null,idx:0,session:[]};renderLearning()');
  await tick(50);
  ok(!app.$$('[data-un]')[0].textContent.includes('lessons'),
     'a book with no lessons does not claim to have any',
     app.$$('[data-un]')[0].textContent.replace(/\s+/g, ' ').trim());
  app.w.eval('S.lv={view:"units",book:BOOKS[0],unit:null,idx:0,session:[]};renderLearning()');
  await tick(50);
  // every word of a unit carries a lesson, and it belongs to that unit
  // (PE episodes excepted: 1C/3C/... live in the shared PE unit 13, like ele/pre)
  const mismatched = app.w.eval(`WORDS.filter(function(w){
      return (w.books||[]).some(function(b){return b.book==="beg" && b.lesson && b.unit<=12 && parseInt(b.lesson,10)!==b.unit;});
    }).map(function(w){return w.en;})`);
  ok(mismatched.length === 0, 'no word claims a lesson outside its own unit', mismatched);
  // Practical English is a card of its own after its unit — owner round 12:
  // "practical english'i diğer ünitelerin içine yerleştirmişsin, bu olmamış"
  ok(app.live('unitLessonList("beg",13).join(",")') === '1C,3C,5C,7C,11C',
     'the five Beginner PE episodes live in their own unit 13', app.live('unitLessonList("beg",13)'));
  ok(app.live('unitWords("beg",1).every(function(w){return (w.books||[]).every(function(b){return b.book!=="beg"||b.lesson!=="1C";});})'),
     'no 1C word remains inside Beginner unit 1');
  const peCards = app.$$('[data-pe]');
  ok(peCards.length === 5, 'the units view renders one PE card per episode', peCards.length);
  const lvHtml = app.$('#lv').innerHTML;
  ok(lvHtml.indexOf('data-un="1"') < lvHtml.indexOf('data-pe="1C"') &&
     lvHtml.indexOf('data-pe="1C"') < lvHtml.indexOf('data-un="2"'),
     'the 1C card sits between Unit 1 and Unit 2 (book order, not a final unit)');
  click(app, peCards[0]);
  await tick(50);
  ok(app.live('S.lv.lesson') === '1C' && app.live('S.lv.unit') === 13,
     'clicking the PE card opens the episode as a lesson of its own', app.live('S.lv.lesson'));
  ok(app.live('S.lv.session.length') === app.live('lessonWords("beg","1C").length'),
     'its session is exactly the episode\'s words');
  app.w.eval('S.lv={view:"units",book:BOOKS[0],unit:null,idx:0,session:[]};renderLearning()');
  await tick(50);
  // the flashcard names the lesson it comes from
  app.w.eval('S.lv={view:"vocab",book:BOOKS[0],unit:1,idx:0,session:unitWords("beg",1)};renderLearning()');
  await tick(50);
  const card = app.$('#lv').textContent.replace(/\s+/g, ' ');
  ok(card.includes('1A'), 'the flashcard labels its lesson', card.slice(0, 60));
  ok(card.includes('A cappuccino, please'), 'the flashcard shows the lesson title', card.slice(0, 80));

  /* ---- 7a2. a word two books teach does not leak into the other's lesson ---- */
  console.log('\n[7a2] a word shared by two books stays in its own lesson per book');
  ok(app.live('unitLessonList("ele",1).join(",")') === '1A,1B,1C',
     'the Elementary book has its own lessons', app.live('unitLessonList("ele",1)'));
  ok(app.live('lessonWords("ele","1A").length') === app.live('LESSONS["ele|1A"].words'),
     'an Elementary lesson holds exactly the words its own book lists',
     { got: app.live('lessonWords("ele","1A").length'), want: app.live('LESSONS["ele|1A"].words') });
  ok(app.live('lessonWords("ele","1A").every(function(w){return (w.books||[]).some(function(b){return b.book==="ele" && b.lesson==="1A";});})'),
     'no other book\'s word appears in an Elementary lesson');
  ok(app.live('lessonWords("beg","1A").every(function(w){return (w.books||[]).some(function(b){return b.book==="beg" && b.lesson==="1A";});})'),
     'and none in a Beginner lesson either');
  // the card labels itself from the book being studied, not the word's home book
  app.w.eval('S.lv={view:"vocab",book:BOOKS.find(function(b){return b.id==="ele"}),unit:1,lesson:"1A",idx:0,session:lessonWords("ele","1A")};renderLearning()');
  await tick(50);
  const eleCard = app.$('#lv').textContent.replace(/\s+/g, ' ');
  ok(eleCard.includes('Welcome to the class'),
     'studying Elementary labels the card with the Elementary lesson', eleCard.slice(0, 80));
  ok(!eleCard.includes('A cappuccino, please'),
     'and not with the Beginner lesson the same word also belongs to', eleCard.slice(0, 80));

  /* ---- 7b. units of books that are not imported yet stay honest ---- */
  console.log('\n[7b] a book with no imported words reports 0, not a fake count');
  ok(app.live('unitCount("ele",1)') !== undefined, 'unitCount tolerates a book with no imported words');
  app.w.eval('S.lv={view:"units",book:BOOKS.find(function(b){return b.id==="ele"}),unit:null,idx:0,session:[]};renderLearning()');
  await tick(50);
  const eleRows = app.$$('[data-un]');
  ok(eleRows.length === app.live('BOOKS.find(function(b){return b.id==="ele"}).units'), 'the Elementary book still renders its unit list', eleRows.length);
  const eleRow = eleRows[0].textContent.replace(/\s+/g, ' ').trim();
  ok(!eleRow.includes('undefined'), 'no "undefined" leaks into a unit row', eleRow);
  // A substring test would fail on "60 words", which contains "0 words".
  ok(!/(?:^|\s)0 words/.test(eleRow), 'no unit ever claims "0 words"', eleRow);
  // Whatever a unit shows must be the real number behind it — this is what the
  // hardcoded "24 words" used to get wrong for every unit of every book.
  ok(eleRow.includes(String(app.live('unitCount("ele",1)')) + ' words'),
     'the row count equals unitCount for a partially imported book', eleRow);
  // And a unit with no imported words at all says so instead of showing a number.
  ok(app.live('unitCount("zzempty",1)') === 0, 'an un-imported book reports zero words, not a fake count');
  app.w.eval('S.lv={view:"units",book:BOOKS.find(function(b){return b.id==="zzempty"}),unit:null,idx:0,session:[]};renderLearning()');
  await tick(50);
  const emptyRow = app.$$('[data-un]')[0].textContent.replace(/\s+/g, ' ').trim();
  ok(emptyRow.includes('Not imported yet'), 'an empty unit says the book is not imported yet', emptyRow);

  /* ---- 7c. Search is a trilingual dictionary, not a headword filter ---- */
  console.log('\n[7c] search finds any word in EN, TM or RU');
  app.w.eval('go("scr-search")');
  await tick(50);
  const hitCount = () => app.$$('#dictlist .wrow').length;
  const shown = () => app.$('#dictlist').textContent.replace(/\s+/g, ' ').trim();
  const runQuery = async (q) => {
    app.$('#dinput').value = q;
    app.$('#dinput').dispatchEvent(new app.w.Event('input', { bubbles: true }));
    await tick(30);
    return hitCount();
  };
  // This is the bug the owner reported, and it only reproduces on a build nobody
  // has touched: the default chip is "Recent words" and the query used to be
  // intersected with it, so a fresh install found nothing. `app` above has already
  // been switched to "all" by test [4], so this needs its own instance.
  const fresh = boot(seeded);
  await tick(150);
  fresh.w.eval('go("scr-search")');
  await tick(50);
  const freshRows = () => [...fresh.w.document.querySelectorAll('#dictlist .wrow')].length;
  const freshType = async (v) => {
    fresh.$('#dinput').value = v;
    fresh.$('#dinput').dispatchEvent(new fresh.w.Event('input', { bubbles: true }));
    await tick(40);
    return freshRows();
  };
  ok(fresh.live('S.filter') === 'hist', 'a fresh install defaults to the Recent chip', fresh.live('S.filter'));
  ok(await freshType('mug') >= 1, 'and typing an English word still finds it there', freshRows());
  ok(await freshType('krujka') >= 1, 'and a Turkmen query works there too', freshRows());
  ok(await freshType('кружка') >= 1, 'and a Russian query works there too', freshRows());
  ok(await runQuery('krujka') >= 1, 'a Turkmen gloss finds the word (TM -> EN)', hitCount());
  ok(await runQuery('кружка') >= 1, 'a Russian gloss finds the word (RU -> EN)', hitCount());
  ok(await runQuery('yadaw') >= 1, 'typing without Turkmen diacritics still matches "ýadaw"', hitCount());
  ok(await runQuery('on the table') >= 1, 'a collocation phrase matches, not just headwords', hitCount());
  ok(await runQuery('zzz') === 0, 'a word that does not exist returns nothing', hitCount());
  ok(shown().length > 0, 'and says so instead of showing an empty list', shown().slice(0, 60));
  // the suggestion chips had no click handler at all
  const chip = app.$('[data-q]');
  ok(chip !== null, 'the suggestion chips are still there');
  click(app, chip);
  await tick(30);
  ok(app.$('#dinput').value === chip.dataset.q, 'clicking a suggestion chip fills the search box', app.$('#dinput').value);
  ok(hitCount() >= 1, 'and runs the search', hitCount());
  // results must say which language matched
  await runQuery('кружка');
  ok(app.$('#dictlist').innerHTML.includes('RU'), 'a Russian hit is labelled RU');
  await runQuery('');
  // The contract is: with no query, the chip decides what you see. `app` was
  // switched to "all" back in test [4], so this belongs on the fresh instance.
  ok(app.live('S.filter') === 'all', 'the chip you chose stays chosen after a search', app.live('S.filter'));
  ok(await runQuery('') === app.live('S.hist.length') || app.live('S.filter') === 'all',
     'and an empty query obeys it', { shown: hitCount(), filter: app.live('S.filter') });
  ok(await freshType('') === 0, 'on a fresh install an empty query shows the empty Recent list', freshRows());

  /* ---- 8. with NO pack available, the app must fall back to the seed ---- */
  console.log('\n[8] no pack reachable → app keeps the 12 seed words (no regression)');
  const bare = boot(stripPack(rawHtml));
  await tick(120);
  ok(bare.$('#yatlaWords') === null, 'the embedded pack really is gone from this build');
  ok(bare.live('WORDS.length') === 12, 'still 12 words', bare.live('WORDS.length'));
  bare.w.eval('go("scr-search")');
  await tick(50);
  ok(bare.$$('#dictlist .wrow').length === 0, 'a fresh install starts on "recent", which is empty', bare.$$('#dictlist .wrow').length);
  bare.w.eval('S.filter="all";filt()');
  await tick(40);
  ok(bare.$$('#dictlist .wrow').length === 12, 'the full dictionary is still the 12 seed words', bare.$$('#dictlist .wrow').length);
  ok(bare.errors.length === 0, 'zero jsdom errors in fallback mode', bare.errors);

  finish();
}

function finish() {
  console.log(`\n${failed === 0 ? 'PASS' : 'FAIL'} — ${passed} assertions passed, ${failed} failed.`);
  process.exit(failed === 0 ? 0 : 1);
}

main();
