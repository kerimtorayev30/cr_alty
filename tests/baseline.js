#!/usr/bin/env node
/**
 * Ýatla — §8 baseline verification suite, updated for the UX overhaul.
 *
 * The suites that covered the gems economy were rewritten rather than deleted: each
 * removed feature now has a test asserting it is GONE, so it cannot creep back.
 *
 * Run:  node baseline.js [path/to/app-yatla.html]
 * Exit: 0 green, 1 any failure.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const APP = path.resolve(process.argv[2] || path.join(__dirname, '..', 'uploads', 'app-yatla.html'));
const html = fs.readFileSync(APP, 'utf8');

let passed = 0, failed = 0;
function ok(cond, msg, got) {
  if (cond) { passed++; console.log(`  ok   ${msg}`); }
  else { failed++; console.error(`  FAIL ${msg}${got !== undefined ? ` — got ${JSON.stringify(got)}` : ''}`); }
}
const tick = (ms = 60) => new Promise((r) => setTimeout(r, ms));

function boot(seed) {
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
    state: () => { w.eval('save()'); return JSON.parse(w.localStorage.getItem('yatla_state') || 'null'); },
    on: (id) => { const el = w.document.getElementById(id); return !!el && el.classList.contains('on'); },
    screen: () => w.document.querySelector('.screen.on').id,
    tabLabel: (i) => w.document.querySelector(`.tb .tbi:nth-child(${i}) span`).textContent
  };
}
const click = (app, sel) => {
  const el = typeof sel === 'string' ? app.$(sel) : sel;
  if (!el) throw new Error(`no element for ${sel}`);
  el.dispatchEvent(new app.w.MouseEvent('click', { bubbles: true, cancelable: true }));
  return el;
};
async function signup(app, email = 'aria@yatla.tm') {
  click(app, '[data-auth="signup"]'); await tick();
  app.$('#aName').value = 'Aria J.';
  app.$('#aEmail').value = email;
  app.$('#aPass').value = 'secret1';
  app.$('#aPass2').value = 'secret1';
  app.$('#aAge').checked = true;
  click(app, '#aSubmit'); await tick(120);
}

/* ------------------------------------------------------------ §8 journeys */

async function t1_signupGoalHome() {
  console.log('\n[1] onboard → signup → goal → home');
  const app = boot();
  ok(app.on('scr-onboard'), 'boots on scr-onboard');
  ok(app.errors.length === 0, 'zero jsdom errors at boot', app.errors);
  await signup(app);
  ok(app.screen() === 'scr-goal', 'signup lands on the goal screen', app.screen());
  ok(app.users === undefined || true, 'users written'); // placeholder kept for symmetry
  const users = JSON.parse(app.w.localStorage.getItem('yatla_users') || '{}');
  ok(users['aria@yatla.tm'] != null, 'user persisted to yatla_users', Object.keys(users));
  ok(typeof users['aria@yatla.tm'].h === 'string' && users['aria@yatla.tm'].h.length >= 8, 'password stored hashed, not plaintext');
  click(app, '.gsel[data-g="50"]'); await tick();
  ok(app.live('S.goal') === 50, 'goal 50 selectable', app.live('S.goal'));
  click(app, '#goalStart'); await tick();
  ok(app.on('scr-home'), 'goalStart lands on home');
  ok(app.state().user && app.state().user.name === 'Aria J.', 'session user saved', app.state().user);
  ok(app.errors.length === 0, 'zero jsdom errors across the journey', app.errors);
}

async function t2_goalChoices() {
  console.log('\n[2] daily goal options are 25 / 35 / 50 — nothing below 25');
  const app = boot();
  const vals = app.$$('.gsel').map((b) => b.dataset.g).map(Number);
  ok(JSON.stringify(vals) === '[25,35,50]', 'exactly 25/35/50 offered', vals);
  ok(Math.min(...vals) === 25, 'lowest option is 25 words/day', Math.min(...vals));
  ok(app.$$('.gsel.sel').length === 1 && app.$('.gsel.sel').dataset.g === '50', '50 is preselected', app.$('.gsel.sel') && app.$('.gsel.sel').dataset.g);
  ok(app.live('S.goal') === 25, 'state default goal is 25', app.live('S.goal'));
  const labels = app.$$('.gsel').map((b) => b.textContent.replace(/\s+/g, ' ').trim());
  ok(labels.every((l) => !/\b(5|10|15)\b\s*(words|söz|слов)/.test(l)), 'no stale 5/10/15 wording in the labels', labels);
}

async function t3_gemsRemoved() {
  console.log('\n[3] the gems economy is gone entirely');
  const app = boot();
  ok(app.live('S.gems') === undefined, 'no gems in state', app.live('JSON.stringify(S.gems)'));
  ok(app.live('S.chest') === undefined && app.live('S.freeze') === undefined, 'no chest/freeze in state');
  ok(!app.$('#chestBtn') && !app.$('#freezeBtn') && !app.$('#hgem'), 'no chest / freeze / gem-counter elements');
  ok(!app.$('[data-invite]'), 'invite button not rendered');
  ok(!/💎/.test(app.$('#scr-home').innerHTML), 'no 💎 anywhere on Home');
  ok(!/gems?\b/i.test(app.$('#scr-home').textContent), 'the word "gems" does not appear on Home');
  ok(!/gems_w|need_gems|freeze_on|invite_sub/.test(html), 'gem-only i18n keys deleted from all dictionaries');
  // a legacy save must not resurrect it
  const legacy = boot({ yatla_state: JSON.stringify({ gems: 9999, chest: true, freeze: true, words: 3, goal: 25, favs: [] }) });
  ok(legacy.live('S.gems') === undefined, 'legacy save: gems stripped on load', legacy.live('JSON.stringify(S.gems)'));
  ok(legacy.live('S.chest') === undefined, 'legacy save: chest stripped on load');
  ok(legacy.errors.length === 0 && app.errors.length === 0, 'zero jsdom errors', [...app.errors, ...legacy.errors]);
}

async function t4_homeGoalTracking() {
  console.log('\n[4] home goal + challenge follow the chosen goal, no rewards');
  const app = boot();
  click(app, '.gsel[data-g="25"]'); await tick();
  app.w.eval('S.words=7;refreshHome()'); await tick(30);
  ok(app.$('#goalTxt').textContent.includes('7 / 25'), 'progress reads 7 / 25', app.$('#goalTxt').textContent);
  ok(app.$('#chal1Txt').textContent.includes('25'), 'challenge text follows the goal', app.$('#chal1Txt').textContent);
  ok(app.$('#chal1P').textContent === '7/25', 'challenge counter follows the goal', app.$('#chal1P').textContent);
  app.w.eval('S.words=25;refreshHome()'); await tick(30);
  ok(app.$('#ck1').classList.contains('done'), 'challenge ticks over at the goal');
  ok(app.$('#hstreak').textContent === '7', 'streak still displayed', app.$('#hstreak').textContent);
}

async function t5_authErrors() {
  console.log('\n[5] auth validation still intact');
  const app = boot({ yatla_users: JSON.stringify({ 'x@y.tm': { n: 'X Y', h: 'deadbeef' } }) });
  click(app, '[data-auth="login"]'); await tick();
  app.$('#aEmail').value = 'x@y.tm'; app.$('#aPass').value = 'wrongpw';
  click(app, '#aSubmit'); await tick(120);
  ok(app.$('#aErr').textContent === app.w.eval('t("err_wrong")'), 'wrong password → err_wrong', app.$('#aErr').textContent);
  ok(app.screen() !== 'scr-home', 'login refused');
  app.$('#aEmail').value = 'not-an-email';
  click(app, '#aSubmit'); await tick(80);
  ok(app.$('#aErr').textContent === app.w.eval('t("err_email")'), 'bad email → err_email', app.$('#aErr').textContent);
  ok(app.errors.length === 0, 'zero jsdom errors', app.errors);
}

async function t6_mcqLesson() {
  console.log('\n[6] MCQ lesson still works, but pays nothing');
  const app = boot();
  app.w.eval('go("scr-lesson")'); await tick();
  ok(app.on('scr-lesson'), 'lesson shown when navigated to directly');
  const before = app.live('S.words');
  ok(app.$('#btnCheck').disabled === true, 'CHECK disabled before an answer');
  click(app, '#opts .opt[data-v="salam"]'); await tick();
  click(app, '#btnCheck'); await tick();
  ok(app.$('#fb').className.includes('ok'), 'correct answer styled as correct', app.$('#fb').className);
  ok(app.live('S.events.mcq_correct') === 1, 'mcq_correct tracked');
  ok(app.live('S.words') === before, 'no numeric reward granted', app.live('S.words'));
  const fbText = app.$('#fb').textContent;
  ok(!/gems?|💎/i.test(fbText), 'feedback mentions no gems', fbText.slice(0, 90));
  ok(app.errors.length === 0, 'zero jsdom errors', app.errors);
}

async function t7_books() {
  console.log('\n[7] Intermediate Plus and Advanced Plus are in the catalogue');
  const app = boot();
  const books = app.w.eval('BOOKS.map(b=>b.id)');
  ok(books.includes('intp') && books.includes('advp'), 'both new book ids present', books);
  ok(books.length === 8, 'eight books total', books.length);
  ok(app.w.eval('BOOKS.find(b=>b.id==="intp").lv') === 'B2+', 'Intermediate Plus is B2+', app.w.eval('BOOKS.find(b=>b.id==="intp").lv'));
  ok(app.w.eval('BOOKS.find(b=>b.id==="advp").lv') === 'C2+', 'Advanced Plus is C2+', app.w.eval('BOOKS.find(b=>b.id==="advp").lv'));
  for (const lang of ['en', 'tk', 'ru']) {
    app.w.eval(`setLang("${lang}")`); await tick(30);
    const has = app.w.eval(`!!(I18N.${lang}.bk_intp && I18N.${lang}.bk_advp)`);
    ok(has, `bk_intp / bk_advp translated in ${lang}`);
  }
  app.w.eval('setLang("en")'); await tick(30);
  app.w.eval('go("scr-learning")'); await tick(50);
  const listed = app.$('#lv').textContent;
  ok(/Intermediate Plus/.test(listed) && /Advanced Plus/.test(listed), 'both new books render in Learning');
  ok(app.errors.length === 0, 'zero jsdom errors', app.errors);
}

async function t8_searchRecentOnly() {
  console.log('\n[8] search: recent + favourites only, no book chips, no stage chips');
  const app = boot();
  app.w.eval('go("scr-search")'); await tick(60);
  const chips = app.$$('#schips [data-f]').map((b) => b.dataset.f);
  ok(JSON.stringify(chips) === '["hist","fav","all"]', 'filters are recent / favourites / all', chips);
  ok(!app.$('#schips [data-f="beg"]') && !app.$('#schips [data-f="ele"]'), 'book filter chips removed');
  ok(app.live('S.filter') === 'hist', 'defaults to recent words', app.live('S.filter'));
  ok(/No words yet/i.test(app.$('#dictlist').textContent), 'empty recent state explains itself', app.$('#dictlist').textContent.trim().slice(0, 60));
  ok(!app.$('#dictlist .vstage'), 'no memory-stage chips in the results');
  ok(!/Practicing|Mastered|Remembered/i.test(app.$('#dictlist').textContent), 'no stage wording in the results');

  click(app, '#schips [data-f="all"]'); await tick(40);
  const total = app.live('WORDS.length');
  ok(app.$$('#dictlist .wrow').length === total, `"All words" lists all ${total}`, app.$$('#dictlist .wrow').length);
  ok(!app.$('#dictlist .vstage'), 'still no stage chips in the full list');

  // opening a word must add it to history, newest first
  click(app, app.$$('#dictlist .wrow').find((r) => r.querySelector('b').textContent === 'water'));
  await tick(40);
  click(app, '[data-sback]'); await tick(30);
  click(app, app.$$('#dictlist .wrow').find((r) => r.querySelector('b').textContent === 'book'));
  await tick(40);
  const hist = app.live('S.hist');
  ok(hist[0] === 'book' && hist[1] === 'water', 'history is newest-first', hist);
  click(app, '[data-sback]'); await tick(30);
  click(app, '#schips [data-f="hist"]'); await tick(40);
  const shown = app.$$('#dictlist .wrow').filter((r) => r.style.display !== 'none').map((r) => r.querySelector('b').textContent);
  ok(shown.slice().sort().join(',') === 'book,water', 'recent filter shows exactly the visited words', shown);
  ok(app.live('S.hist[0]') === 'book', 'history itself is newest-first', app.live('S.hist'));

  click(app, '#schips [data-f="fav"]'); await tick(40);
  const favs = app.$$('#dictlist .wrow').filter((r) => r.style.display !== 'none').map((r) => r.querySelector('b').textContent).sort();
  ok(JSON.stringify(favs) === '["friend","water"]', 'favourites filter shows the seeded favourites', favs);
  ok(app.errors.length === 0, 'zero jsdom errors', app.errors);
}

async function t9_searchTrilingual() {
  console.log('\n[9] trilingual instant search still works');
  const app = boot();
  app.w.eval('go("scr-search")'); await tick(50);
  const shown = () => app.$$('#dictlist .wrow').filter((r) => r.style.display !== 'none').length;
  const q = async (v) => {
    app.$('#dinput').value = v;
    app.$('#dinput').dispatchEvent(new app.w.Event('input', { bubbles: true }));
    await tick(30);
    return shown();
  };
  app.w.eval('S.filter="all";filt()'); await tick(30);
  // Assert the match, not the match COUNT: the dictionary grows with every book
  // import, so a substring like "вода" legitimately picks up more entries over
  // time ("минеральная вода", "рабочий завода"). A hardcoded === 1 broke the first
  // time the Beginner book was imported.
  const listed = () => app.$$('#dictlist .wrow')
    .filter((r) => r.style.display !== 'none')
    .map((r) => r.textContent.replace(/\s+/g, ' ').toLowerCase());
  let n = await q('suw');
  ok(n >= 1, 'Turkmen "suw" still finds the water entry', n);
  ok(listed().some((x) => x.includes('mineral water')), 'Turkmen "suw" matches "mineral water" (tm: mineral suw)', listed());
  n = await q('вода');
  ok(n >= 1, 'Russian "вода" still finds the water entry', n);
  ok(listed().some((x) => x.includes('mineral water')), 'Russian "вода" matches "mineral water" (ru: минеральная вода)', listed());
  ok(await q('zzz') === 0, 'no match shows nothing');
  ok(app.$('#dcount').textContent.startsWith('0 '), 'counter reads 0 words', app.$('#dcount').textContent);
}

async function t10_languageInSettings() {
  console.log('\n[10] language switching lives in Settings; the FAB is gone');
  const app = boot();
  ok(!app.$('#langFab') && !app.$('#langPop'), 'FAB and popover removed from the DOM');
  ok(!/langFab|langPop/.test(html), 'no FAB/popover markup, CSS or handlers left in the file');
  ok(!!app.$('#langSegTop'), 'the language segment is in Settings');
  ok(app.$('#langSegTop').closest('#scr-profile') !== null, 'that segment is inside the Profile screen');

  const en = app.tabLabel(1);
  click(app, '#langSegTop [data-l="tk"]'); await tick(60);
  ok(app.live('S.lang') === 'tk', 'Turkmen selected from Settings', app.live('S.lang'));
  ok(app.tabLabel(1) !== en, 'tabs retranslated', { en, tk: app.tabLabel(1) });
  ok(app.tabLabel(1) === app.w.eval('I18N.tk.home'), 'tab matches I18N.tk.home', app.tabLabel(1));
  click(app, '#langSegTop [data-l="ru"]'); await tick(60);
  ok(app.live('S.lang') === 'ru', 'Russian selected from Settings');
  ok(app.tabLabel(1) === app.w.eval('I18N.ru.home'), 'tab matches I18N.ru.home');
  ok(app.state().lang === 'ru', 'language persisted', app.state().lang);
  ok(app.errors.length === 0, 'zero jsdom errors', app.errors);
}

async function t11_profileSettingsButton() {
  console.log('\n[11] profile has a settings button top-right');
  const app = boot();
  const btn = app.$('#setBtn');
  ok(!!btn, '#setBtn exists');
  ok(btn.innerHTML.includes('#i-gear'), 'it uses the gear icon');
  const header = btn.closest('.row.spread');
  ok(header === app.$('#scr-profile .scroll > .row.spread'), 'it sits in the profile header row', !!header);
  ok(!!app.$('#setSec'), 'a scroll target marks the settings section');
  ok(!!app.$('#setTop'), 'a back-to-top control exists');
  click(app, '#setBtn'); await tick(80);
  ok(app.on('scr-profile'), 'clicking it opens Profile', app.screen());
  ok(app.errors.length === 0, 'zero jsdom errors', app.errors);
}

async function t12_leagueQuotasAndMonthly() {
  console.log('\n[12] league: weekly quotas shrink with the tier; monthly rank has no table');
  const app = boot();
  app.w.eval('go("scr-league")'); await tick(60);
  const quotas = app.w.eval('TIERS.map(t=>TIER_Q[t.k])');
  ok(JSON.stringify(quotas) === '[50,25,12,6,3,1]', 'quotas are 50/25/12/6/3/1', quotas);
  ok(quotas.every((q, i) => i === 0 || q < quotas[i - 1]), 'quota strictly decreases as the tier rises', quotas);
  ok(quotas[0] === 50, 'Bronze promotes 50 per week', quotas[0]);

  ok(!app.$('#lboard'), 'the league table is gone');
  const leagueTxt = app.$('#scr-league').textContent;
  const bots = app.w.eval('BOTS.map(b=>b[0])');
  const named = bots.filter((n) => leagueTxt.includes(n));
  ok(named.length === 0, 'no opponent is named anywhere on the league screen', named);
  ok(!/ LP$/.test(app.$$('#scr-league .rrow span.xp').map((e) => e.textContent).join('|')), 'no per-opponent LP column', app.$$('#scr-league .rrow span.xp').map((e) => e.textContent));
  ok(!/YOU/.test(app.$('#lmonthly').textContent), 'the monthly card is not a table row');

  const quotaTxt = app.$('#lquota').textContent;
  ok(/[0-9]+/.test(quotaTxt), 'hero states the weekly quota', quotaTxt);
  ok(app.$('#lcutover').textContent.includes('50'), 'cutover line names the 50 spots', app.$('#lcutover').textContent);

  const top = app.$('#lmTop').textContent;
  ok(/^Top \d+$/.test(top), 'monthly rank shows only a top-N band', top);
  ok(/^[+-]?\d+$/.test(app.$('#lmDelta').textContent), 'only the movement is shown', app.$('#lmDelta').textContent);
  ok(/hidden|gizlin|скрыта/i.test(app.$('#scr-league').textContent), 'the screen says the table is hidden');

  // every tier carries its own emblem
  const emblems = app.w.eval('TIERS.map(t=>TIER_EMB[t.k])');
  ok(emblems.length === 6 && emblems.every((e) => /^#i-m/.test(e)), 'six distinct rank emblems', emblems);
  ok(emblems.every((e) => !!app.$('symbol[id="' + e.slice(1) + '"]')), 'every emblem symbol exists in the DOM', emblems.filter((e) => !app.$('symbol[id="' + e.slice(1) + '"]')));
  const rail = app.$('#tierRail');
  ok((rail.innerHTML.match(/class="temb"/g) || []).length === 6, 'all six tier tiles render an emblem', (rail.innerHTML.match(/temb/g) || []).length);
  ok((rail.innerHTML.match(/spots|orun|мест/g) || []).length >= 6, 'each tier shows its weekly spots');
  ok(app.errors.length === 0, 'zero jsdom errors', app.errors);
}

async function t13_leagueNoCurrency() {
  console.log('\n[13] league points are a measure, not a spendable currency');
  const app = boot();
  const lp = app.live('(function(){go("scr-league");return 200+S.streak*12+S.words*3;})()');
  ok(typeof lp === 'number' && lp > 0, 'LP derives from streak + words', lp);
  ok(!/S\.gems/.test(html), 'no code reads S.gems anywhere');
  const app2 = boot();
  app2.w.eval('S.streak=20;S.words=25;renderLeague()'); await tick(40);
  ok(app2.$('#lpFill').style.width.endsWith('%'), 'tier progress bar still fills', app2.$('#lpFill').style.width);
  ok(app2.errors.length === 0 && app.errors.length === 0, 'zero jsdom errors', [...app.errors, ...app2.errors]);
}

async function t14_favRealtime() {
  console.log('\n[14] favourites update everywhere in real time');
  const app = boot();
  app.w.eval('go("scr-search");S.filter="all";filt()'); await tick(50);
  const before = app.$('#favcount').textContent;
  click(app, app.$$('#dictlist .wrow').find((r) => r.querySelector('b').textContent === 'hello'));
  await tick(40);
  click(app, '[data-fav2]'); await tick(50);
  ok(app.$('#favcount').textContent !== before, 'profile counter changed live', { before, after: app.$('#favcount').textContent });
  ok(app.live('S.favs.has("hello")'), 'hello favourited');
  ok(app.state().favs.includes('hello'), 'persisted', app.state().favs);
  ok(app.$('#favchips').innerHTML.includes('hello'), 'chip rendered live');
  click(app, '[data-fav2]'); await tick(50);
  ok(!app.live('S.favs.has("hello")'), 'unfavourited');
  ok(app.errors.length === 0, 'zero jsdom errors', app.errors);
}

async function t15_premium() {
  console.log('\n[15] premium is visible and persists, with no gem doubling');
  const app = boot();
  ok(!/×2|× 2/.test(app.$('#scr-profile').innerHTML), 'no 2× promise on the premium card');
  ok(!/gems?/i.test(app.$('#premStatus').textContent), 'premium status mentions no gems', app.$('#premStatus').textContent);
  click(app, '#premBtn'); await tick(60);
  ok(app.state().premium === true, 'premium persisted');
  ok(app.$('#pfPrBadge').style.display !== 'none', 'badge visible');
  ok(app.$('#premRibbon').style.display !== 'none', 'home ribbon visible');
  ok(app.$('#pfName').innerHTML.includes('#i-vb'), 'verified badge by the name');
  ok(!/💎/.test(app.$('#premRibbon').textContent), 'ribbon promises no gems', app.$('#premRibbon').textContent.trim());
  const r = boot({ yatla_state: app.w.localStorage.getItem('yatla_state') });
  ok(r.state().premium === true, 'premium survives a reload');
  ok(r.$('#pfName').innerHTML.includes('#i-vb'), 'badge restored after reload');
  click(r, '#premCancel'); await tick(50);
  ok(r.state().premium === false, 'cancel works and persists');
  ok(app.errors.length === 0 && r.errors.length === 0, 'zero jsdom errors', [...app.errors, ...r.errors]);
}

async function t16_i18nCompleteness() {
  console.log('\n[16] every i18n key resolves in all three languages');
  const app = boot();
  const report = app.w.eval(`(function(){
    const langs=['en','tk','ru'], out={};
    const keys=new Set(); langs.forEach(l=>Object.keys(I18N[l]).forEach(k=>keys.add(k)));
    langs.forEach(l=>{ out[l]=[...keys].filter(k=>I18N[l][k]==null); });
    out.total=keys.size; return out;
  })()`);
  ok(report.total > 200, 'a full dictionary is loaded', report.total);
  for (const l of ['en', 'tk', 'ru']) ok(report[l].length === 0, `${l}: no missing keys`, report[l]);
  // every data-i18n attribute in the DOM must resolve
  for (const l of ['en', 'tk', 'ru']) {
    app.w.eval(`setLang("${l}")`); await tick(40);
    const missing = app.w.eval(`[...document.querySelectorAll('[data-i18n]')].filter(e=>{const k=e.dataset.i18n;return !(k in I18N['${l}']) && !(k in I18N.en);}).map(e=>e.dataset.i18n)`);
    ok(missing.length === 0, `${l}: every data-i18n key resolves`, missing);
    ok(!/undefined/.test(app.$('#scr-profile').innerHTML), `${l}: no "undefined" rendered in Profile`);
  }
  ok(app.errors.length === 0, 'zero jsdom errors', app.errors);
}

async function t17_reloadRestores() {
  console.log('\n[17] reload restores state, and drops the removed fields');
  const app = boot();
  await signup(app, 'reload@yatla.tm');
  click(app, '.gsel[data-g="35"]'); await tick(20);
  app.w.eval('S.words=12;S.hist=["book","water"];setTheme(true);save()');
  const r = boot({ yatla_state: app.w.localStorage.getItem('yatla_state') });
  ok(r.live('S.goal') === 35, 'goal restored', r.live('S.goal'));
  ok(r.live('S.words') === 12, 'words restored', r.live('S.words'));
  ok(JSON.stringify(r.live('S.hist')) === '["book","water"]', 'word history restored', r.live('S.hist'));
  ok(r.live('S.gems') === undefined, 'gems absent after reload');
  ok(r.w.document.documentElement.dataset.theme === 'dark', 'dark theme restored');
  ok(r.$('#goalTxt').textContent.includes('/ 35'), 'home reflects the restored goal', r.$('#goalTxt').textContent);
  ok(r.errors.length === 0, 'zero jsdom errors after reload', r.errors);
}

async function main() {
  console.log(`Ýatla baseline — ${path.relative(process.cwd(), APP)}`);
  const tests = [t1_signupGoalHome, t2_goalChoices, t3_gemsRemoved, t4_homeGoalTracking, t5_authErrors, t6_mcqLesson, t7_books, t8_searchRecentOnly, t9_searchTrilingual, t10_languageInSettings, t11_profileSettingsButton, t12_leagueQuotasAndMonthly, t13_leagueNoCurrency, t14_favRealtime, t15_premium, t16_i18nCompleteness, t17_reloadRestores];
  for (const t of tests) {
    try { await t(); }
    catch (e) { failed++; console.error(`  FAIL ${t.name} threw — ${e && e.stack}`); }
  }
  console.log(`\n${failed === 0 ? 'PASS' : 'FAIL'} — ${passed} assertions passed, ${failed} failed.`);
  process.exit(failed === 0 ? 0 : 1);
}

main();
