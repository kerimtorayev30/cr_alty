#!/usr/bin/env python3
"""Make tests/integration.js assert the real behaviour instead of passing by accident.

Three defects found by measurement, not by reading:

1. inlinePack() always injected a second <script id="yatlaWords">. Since the app
   now ships its own embedded pack, the test was reading the injected copy and
   never exercised the shipped one. It now injects only when the app has no pack.

2. Test [1] measured the "unpatched seed dictionary" with
       boot(rawHtml).live('WORDS.length')
   read synchronously, before fetchWords' promise resolved — so it observed 12
   no matter what the app contains. With the embedded pack the bare app actually
   reaches 336. It now strips the pack and waits.

3. Test [8] claims "no pack reachable → app keeps the 12 seed words" but booted
   the untouched app, which does have a pack. It now really removes it.

Also adds test [9]: opening a unit must start that unit's own words, which is the
whole point of the unit import.
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


# 1. only inject when the app does not already carry a pack
sub(
    """/** Inline the pack into the page the way an offline / Capacitor build would. */
function inlinePack(html, pack) {
  const json = JSON.stringify(pack).replace(/<\\//g, '<\\\\/');
  const tag = `<script type="application/json" id="yatlaWords">${json}<\\/script>`;
  if (!html.includes('<script>')) throw new Error('no <script> in the app file');
  return html.replace('<script>', tag + '\\n<script>');
}""",
    """/** Inline the pack the way an offline / Capacitor build would.
 *  The app now ships its own embedded pack, so injecting a second one would mean
 *  the test reads the injected copy and never exercises the shipped one. */
function inlinePack(html, pack) {
  if (html.includes('id="yatlaWords"')) return html;   // already embedded — use it
  const json = JSON.stringify(pack).replace(/<\\//g, '<\\\\/');
  const tag = `<script type="application/json" id="yatlaWords">${json}<\\/script>`;
  if (!html.includes('<script>')) throw new Error('no <script> in the app file');
  return html.replace('<script>', tag + '\\n<script>');
}

/** The same app with its embedded pack removed: the true "no pack" build. */
function stripPack(html) {
  return html.replace(/<script type="application\\/json" id="yatlaWords">[\\s\\S]*?<\\/script>\\n?/, '');
}""",
    'inlinePack only injects when needed',
)

# 2. measure the seed dictionary on a build that really has no pack, and wait
sub(
    """  const seedCount = boot(rawHtml).live('WORDS.length');
  ok(seedCount === 12, 'unpatched seed dictionary is 12 words', seedCount);""",
    """  // Read after a tick: fetchWords resolves asynchronously, so a synchronous read
  // observes 12 whatever the file contains.
  const seedApp = boot(stripPack(rawHtml));
  await tick(120);
  const seedCount = seedApp.live('WORDS.length');
  ok(seedCount === 12, 'a build with no pack falls back to the 12 seed words', seedCount);""",
    'seed count measured on a pack-free build',
)

# 3. test [8] must actually remove the pack
sub(
    """  const bare = boot(rawHtml);
  await tick(120);
  ok(bare.live('WORDS.length') === 12, 'still 12 words', bare.live('WORDS.length'));""",
    """  const bare = boot(stripPack(rawHtml));
  await tick(120);
  ok(bare.$('#yatlaWords') === null, 'the embedded pack really is gone from this build');
  ok(bare.live('WORDS.length') === 12, 'still 12 words', bare.live('WORDS.length'));""",
    'test [8] boots a genuinely pack-free app',
)

# 4. test [7]: a unit session must be that unit's own words, reached through the UI
sub(
    """  app.w.eval('S.lv={view:"vocab",book:BOOKS[0],unit:1,idx:0,session:WORDS.slice(0,6)};renderLearning()');
  await tick(50);
  ok(app.live('S.lv.session.length') === 6, 'unit session has 6 cards', app.live('S.lv.session.length'));""",
    """  // Not a hand-built session: open the book and click the unit, the way a user does.
  app.w.eval('S.lv={view:"units",book:BOOKS[0],unit:null,idx:0,session:[]};renderLearning()');
  await tick(50);
  ok(app.live('BOOKS[0].units') === 12, 'the Beginner book lists its 12 units', app.live('BOOKS[0].units'));
  const rows = app.$$('[data-un]');
  ok(rows.length === 12, 'the units view renders 12 rows', rows.length);
  const u1count = app.live('unitCount("beg",1)');
  ok(u1count > 0, 'unit 1 has words from the imported book', u1count);
  ok(rows[0].textContent.includes(String(u1count)), 'the unit row shows the real word count, not a hardcoded 24', rows[0].textContent.replace(/\\s+/g, ' ').trim());
  click(app, rows[0]);
  await tick(50);
  const session = app.w.eval('S.lv.session');
  ok(app.live('S.lv.view') === 'vocab', 'clicking a unit opens the vocabulary view', app.live('S.lv.view'));
  ok(session.length === u1count, 'the session is every word of that unit', { got: session.length, want: u1count });
  ok(session.every((w) => (w.books || []).some((b) => b.book === 'beg' && b.unit === 1)),
     'every card in the session belongs to Beginner unit 1',
     session.filter((w) => !(w.books || []).some((b) => b.book === 'beg' && b.unit === 1)).map((w) => w.en));""",
    'unit sessions come from the unit itself',
)

# 5. a new test: words from a book that is not imported yet belong to no unit
sub(
    """  /* ---- 8. with NO pack available, the app must fall back to the seed ---- */""",
    """  /* ---- 7b. units of books that are not imported yet stay honest ---- */
  console.log('\\n[7b] a book with no imported words reports 0, not a fake count');
  ok(app.live('unitCount("ele",1)') !== undefined, 'unitCount tolerates a book with no imported words');
  app.w.eval('S.lv={view:"units",book:BOOKS.find(function(b){return b.id==="ele"}),unit:null,idx:0,session:[]};renderLearning()');
  await tick(50);
  const eleRows = app.$$('[data-un]');
  ok(eleRows.length === app.live('BOOKS.find(function(b){return b.id==="ele"}).units'), 'the Elementary book still renders its unit list', eleRows.length);
  ok(!eleRows[0].textContent.includes('undefined'), 'no "undefined" leaks into an empty unit row', eleRows[0].textContent.replace(/\\s+/g, ' ').trim());

  /* ---- 8. with NO pack available, the app must fall back to the seed ---- */""",
    'test [7b] for books without imported words',
)

open(P, 'w', encoding='utf-8').write(s)
print(f'{len(edits)} edits applied to {P}')
for e in edits:
    print('  -', e)
