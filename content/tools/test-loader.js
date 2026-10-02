#!/usr/bin/env node
/**
 * jsdom test suite for content/loader/yatla-content.js.
 *
 * The loader is deliberately free of app globals ($, $$, t, go, sfx, hz) so it can be
 * exercised here before app-yatla.html is available. These tests therefore verify the
 * loader module itself — NOT its integration into the app. Integration tests belong in
 * the app's own suite and must be re-run once app-yatla.html is back in the workspace.
 *
 * Run: node test-loader.js
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const LOADER = path.join(__dirname, '..', 'loader', 'yatla-content.js');
const MIN_BUNDLE = path.join(__dirname, '..', 'build', 'yatla-words.min.json');
const src = fs.readFileSync(LOADER, 'utf8');

let passed = 0;
let failed = 0;

function assert(cond, msg, extra) {
  if (cond) {
    passed++;
    console.log(`  ok   ${msg}`);
  } else {
    failed++;
    console.error(`  FAIL ${msg}${extra !== undefined ? ` — got ${JSON.stringify(extra)}` : ''}`);
  }
}

function boot(seedLocalStorage) {
  const errors = [];
  const vc = new VirtualConsole();
  vc.on('jsdomError', (e) => errors.push(String(e && e.message)));
  vc.on('error', (...a) => errors.push(a.map(String).join(' ')));
  const dom = new JSDOM(
    '<!doctype html><html><body></body></html>',
    {
      runScripts: 'outside-only',
      pretendToBeVisual: true,
      url: 'https://yatla.test/',
      virtualConsole: vc,
      beforeParse(window) {
        if (seedLocalStorage) {
          for (const [k, v] of Object.entries(seedLocalStorage)) window.localStorage.setItem(k, v);
        }
      }
    }
  );
  dom.window.eval(src);
  return { dom, errors };
}

/* Minimal IndexedDB stub: records put() calls, returns a preset value from get(). */
function fakeIndexedDB(initial) {
  const store = new Map(Object.entries(initial || {}));
  const log = [];
  function request(value) {
    const req = {};
    setTimeout(() => {
      req.result = value;
      if (req.onsuccess) req.onsuccess();
    }, 0);
    return req;
  }
  return {
    log,
    store,
    open() {
      const open = {};
      setTimeout(() => {
        open.result = {
          objectStoreNames: { contains: () => true },
          createObjectStore: () => {},
          transaction(mode) {
            return {
              objectStore() {
                return {
                  get: (k) => request(store.has(k) ? store.get(k) : undefined),
                  put: (v, k) => {
                    log.push({ op: 'put', key: k });
                    store.set(k, v);
                    return request(undefined);
                  },
                  delete: (k) => {
                    log.push({ op: 'delete', key: k });
                    store.delete(k);
                    return request(undefined);
                  }
                };
              },
              oncomplete: null
            };
          }
        };
        if (open.onsuccess) open.onsuccess();
      }, 0);
      return open;
    }
  };
}

const tick = (ms = 40) => new Promise((r) => setTimeout(r, ms));

/** Every resolution path must return a Promise, since the app calls .then() on it. */
async function t0_alwaysThenable() {
  console.log('\n[0] fetchWords returns a thenable on every path');
  const cases = [
    ['no source at all', boot()],
    ['network', boot()],
    ['localStorage', boot({ yatla_words_v1: JSON.stringify({ words: [{ en: 'a', tm: 'b', ru: 'в', def: 'x', ex: 'y.', exTm: 'z.', cefr: 'A1', ox: 'Oxford 3000', syn: '—', coll: '—', stage: 'New' }] }) })]
  ];
  for (const [label, app] of cases) {
    const C = app.dom.window.YatlaContent;
    if (label === 'network') app.dom.window.fetch = () => Promise.resolve({ ok: false, status: 500, text: () => Promise.resolve('') });
    const p = C.fetchWords({ noCache: true, url: 'https://cdn.test/w.json' });
    assert(p && typeof p.then === 'function', `${label}: returns a thenable`, typeof p);
    await p;
    assert(app.errors.length === 0, `${label}: no jsdom errors`, app.errors);
  }
}

async function t1_networkFetchAndNormalize() {
  console.log('\n[1] network fetch → compact rows normalise to word objects');
  const { dom, errors } = boot();
  const C = dom.window.YatlaContent;
  // jsdom ships no fetch implementation, so every network test must install one.
  const bundle = {
    version: 1,
    format: 'array',
    fields: C.FIELDS,
    rows: [
      ['hello', '/həˈləʊ/', 'INTJ', 'salam', 'привет', 'A greeting', 'Hello!', 'Salam!', 'A1', 'Oxford 3000', 'hi, hey', 'say hello', 'New', null],
      ['water', '/ˈwɔːtə/', 'N', 'suw', 'вода', 'A drink', 'I drink water.', 'Men suw içýärin.', 'A1', 'Oxford 3000', '—', 'a glass of water', 'Bogus', null]
    ]
  };
  dom.window.fetch = () => Promise.resolve({ ok: true, text: () => Promise.resolve(JSON.stringify(bundle)) });
  const r = await C.fetchWords({ noCache: true, url: 'https://cdn.test/w.json' });
  assert(r.source === 'network', 'reports source "network"', r.source);
  assert(r.words.length === 2, 'two words loaded', r.words.length);
  assert(r.words[0].en === 'hello' && r.words[0].tm === 'salam', 'row maps by FIELDS order', r.words[0]);
  assert(typeof r.words[0].syn === 'string' && r.words[0].syn === 'hi, hey', 'syn stays a display string', r.words[0].syn);
  assert(r.words[0].stage === 'New', 'stage label preserved', r.words[0].stage);
  assert(r.words[1].stage === 'New', 'unknown stage falls back to "New"', r.words[1].stage);
  assert(C.STAGES.length === 5 && C.STAGES.includes('Mastered'), 'STAGES mirrors the app\'s five labels', C.STAGES);
  assert(errors.length === 0, 'no jsdom errors', errors);
}

async function t2_localStoragePreferredOverNetwork() {
  console.log('\n[2] localStorage copy wins, network is never called');
  const stored = { version: 1, format: 'object', words: [{ en: 'book', tm: 'kitap', ru: 'книга', pos: 'n', def: 'x.', ex: 'y.', exTm: 'z.', cefr: 'A1', ox: 'core', stage: 1 }] };
  const { dom, errors } = boot({ yatla_words_v1: JSON.stringify(stored) });
  const C = dom.window.YatlaContent;
  let called = 0;
  dom.window.fetch = () => { called++; return Promise.resolve({ ok: true, text: () => Promise.resolve('{}') }); };
  const r = await C.fetchWords({ noCache: true, url: 'https://cdn.test/w.json' });
  assert(r.source === 'cache', 'reports source "cache"', r.source);
  assert(called === 0, 'fetch was not invoked', called);
  assert(r.words.length === 1 && r.words[0].en === 'book', 'stored word returned', r.words);
  assert(errors.length === 0, 'no jsdom errors', errors);
}

async function t3_indexedDbPreferredOverLocalStorage() {
  console.log('\n[3] IndexedDB copy wins over localStorage');
  const { dom, errors } = boot({ yatla_words_v1: JSON.stringify({ words: [{ en: 'from_ls', tm: 'a', ru: 'а', def: 'x.', ex: 'y.', exTm: 'z.', cefr: 'A1', ox: 'core', stage: 1 }] }) });
  const C = dom.window.YatlaContent;
  dom.window.indexedDB = fakeIndexedDB({ yatla_words_v1: { words: [{ en: 'from_idb', tm: 'b', ru: 'б', def: 'x.', ex: 'y.', exTm: 'z.', cefr: 'A1', ox: 'core', stage: 1 }] } });
  const r = await C.fetchWords({ noCache: true });
  assert(r.words.length === 1 && r.words[0].en === 'from_idb', 'IndexedDB entry used', r.words[0] && r.words[0].en);
  assert(r.source === 'cache', 'reports source "cache"', r.source);
  assert(errors.length === 0, 'no jsdom errors', errors);
}

async function t4_corruptCacheFallsBackToNetwork() {
  console.log('\n[4] corrupt localStorage JSON falls back to the network');
  const { dom, errors } = boot({ yatla_words_v1: '{not json' });
  const C = dom.window.YatlaContent;
  dom.window.fetch = () => Promise.resolve({
    ok: true,
    text: () => Promise.resolve(JSON.stringify({ format: 'object', words: [{ en: 'recovered', tm: 'r', ru: 'р', def: 'x.', ex: 'y.', exTm: 'z.', cefr: 'A1', ox: 'core', stage: 1 }] }))
  });
  const r = await C.fetchWords({ noCache: true, url: 'https://cdn.test/w.json' });
  assert(r.source === 'network', 'recovered from network', r.source);
  assert(r.words.length === 1 && r.words[0].en === 'recovered', 'recovered word present', r.words);
  assert(errors.length === 0, 'no jsdom errors', errors);
}

async function t5_networkFailureDegradesToEmpty() {
  console.log('\n[5] network failure resolves [] instead of rejecting (app keeps its seed words)');
  const { dom, errors } = boot();
  const C = dom.window.YatlaContent;
  dom.window.fetch = () => Promise.resolve({ ok: false, status: 503, text: () => Promise.resolve('') });
  const r = await C.fetchWords({ noCache: true, url: 'https://cdn.test/w.json' });
  assert(r.source === 'none', 'reports source "none"', r.source);
  assert(Array.isArray(r.words) && r.words.length === 0, 'empty array, not an exception', r.words);
  assert(errors.length === 0, 'no jsdom errors', errors);
}

async function t6_networkResultIsCached() {
  console.log('\n[6] after a network load the pack is cached for offline use');
  const { dom, errors } = boot();
  const C = dom.window.YatlaContent;
  const pack = { format: 'object', words: [{ en: 'cached', tm: 'c', ru: 'с', def: 'x.', ex: 'y.', exTm: 'z.', cefr: 'A1', ox: 'core', stage: 1 }] };
  let calls = 0;
  dom.window.fetch = () => { calls++; return Promise.resolve({ ok: true, text: () => Promise.resolve(JSON.stringify(pack)) }); };
  const first = await C.fetchWords({ noCache: true, url: 'https://cdn.test/w.json' });
  await tick();
  const second = await C.fetchWords({ noCache: true, url: 'https://cdn.test/w.json' });
  assert(first.source === 'network', 'first call hits the network', first.source);
  assert(calls === 1, 'fetch called exactly once', calls);
  assert(second.source === 'cache', 'second call served from cache', second.source);
  const raw = JSON.parse(dom.window.localStorage.getItem('yatla_words_v1'));
  assert(raw && raw.words && raw.words[0].en === 'cached', 'localStorage holds the pack', raw);
  assert(errors.length === 0, 'no jsdom errors', errors);
}

async function t7_realBuiltBundle() {
  console.log('\n[7] the real build/yatla-words.min.json loads and normalises');
  if (!fs.existsSync(MIN_BUNDLE)) {
    assert(false, 'build/yatla-words.min.json exists (run npm run build first)');
    return;
  }
  const bundle = JSON.parse(fs.readFileSync(MIN_BUNDLE, 'utf8'));
  const { dom, errors } = boot();
  const C = dom.window.YatlaContent;
  dom.window.fetch = () => Promise.resolve({ ok: true, text: () => Promise.resolve(JSON.stringify(bundle)) });
  const r = await C.fetchWords({ noCache: true, url: 'https://cdn.test/w.json' });
  assert(r.words.length === bundle.count, `all ${bundle.count} words load`, r.words.length);
  assert(r.words.every((w) => typeof w.en === 'string' && w.en.length > 0), 'every word has a headword');
  assert(r.words.every((w) => w.cefr && w.ox && w.pos), 'every word has cefr/ox/pos');
  assert(r.words.every((w) => C.STAGES.includes(w.stage)), 'every stage is one of the five app labels');
  assert(r.words.every((w) => typeof w.syn === 'string' && typeof w.coll === 'string'), 'syn/coll are strings, as the app renders them');
  assert(r.words.every((w) => /^\/.+\/$/.test(w.ipa)), 'every IPA is slash-wrapped like the demo data');
  assert(r.words.every((w) => w.ipa && !/[A-Z]/.test(w.ipa)), 'every word has lowercase IPA');
  assert(r.words.every((w) => w.exTm && w.exTm.length > 0), 'every word has a Turkmen example');
  assert(new Set(r.words.map((w) => w.en.toLowerCase())).size === r.words.length, 'headwords unique after normalisation');
  assert(errors.length === 0, 'no jsdom errors', errors);
}

async function t8_mergeAndDedupe() {
  console.log('\n[8] mergePacks de-duplicates headwords case-insensitively');
  const { dom, errors } = boot();
  const C = dom.window.YatlaContent;
  const a = { words: [{ en: 'Hello', tm: 'salam', ru: 'привет', def: 'x.', ex: 'y.', exTm: 'z.', cefr: 'A1', ox: 'core', stage: 1 }] };
  const b = { words: [{ en: 'hello', tm: 'salam', ru: 'привет', def: 'x.', ex: 'y.', exTm: 'z.', cefr: 'A1', ox: 'core', stage: 1 }, { en: 'water', tm: 'suw', ru: 'вода', def: 'x.', ex: 'y.', exTm: 'z.', cefr: 'A1', ox: 'core', stage: 1 }] };
  const merged = C.mergePacks(a, b);
  assert(merged.length === 2, 'duplicate headword collapsed', merged.length);
  assert(merged.map((w) => w.en).join(',') === 'Hello,water', 'first spelling wins', merged.map((w) => w.en));
  assert(C.normalizePack(null).length === 0, 'null pack → []', null);
  assert(C.normalizePack({ words: [{ en: '' }] }).length === 0, 'empty headword dropped');
  assert(errors.length === 0, 'no jsdom errors', errors);
}

async function t9_embeddedPackWins() {
  console.log('\n[9] an inlined <script id="yatlaWords"> pack beats the network');
  const pack = { format: 'object', words: [{ en: 'inlined', tm: 'i', ru: 'и', def: 'x', ex: 'y.', exTm: 'z.', cefr: 'A1', ox: 'Oxford 3000', syn: '—', coll: '—', stage: 'New' }] };
  const errors = [];
  const vc = new VirtualConsole();
  vc.on('jsdomError', (e) => errors.push(String(e && e.message)));
  const dom = new JSDOM(`<!doctype html><html><body><script type="application/json" id="yatlaWords">${JSON.stringify(pack).replace(/<\//g, '<\\/')}<\/script></body></html>`, {
    runScripts: 'outside-only', url: 'https://yatla.test/', virtualConsole: vc
  });
  dom.window.eval(src);
  const C = dom.window.YatlaContent;
  let called = 0;
  dom.window.fetch = () => { called++; return Promise.resolve({ ok: true, text: () => Promise.resolve('[]') }); };
  const p = C.fetchWords({ noCache: true, url: 'https://cdn.test/w.json' });
  assert(p && typeof p.then === 'function', 'fetchWords returns a thenable on the embedded path (callers use .then)', typeof p);
  const r = await p;
  assert(r.source === 'embedded', 'reports source "embedded"', r.source);
  assert(r.words.length === 1 && r.words[0].en === 'inlined', 'inlined word used', r.words);
  assert(called === 0, 'network not touched', called);
  assert(errors.length === 0, 'no jsdom errors', errors);
}

async function main() {
  console.log('Ýatla content loader — jsdom tests');
  const tests = [t0_alwaysThenable, t1_networkFetchAndNormalize, t2_localStoragePreferredOverNetwork, t3_indexedDbPreferredOverLocalStorage, t4_corruptCacheFallsBackToNetwork, t5_networkFailureDegradesToEmpty, t6_networkResultIsCached, t7_realBuiltBundle, t8_mergeAndDedupe, t9_embeddedPackWins];
  for (const t of tests) {
    try {
      await t();
    } catch (e) {
      failed++;
      console.error(`  FAIL ${t.name} threw — ${e && e.stack}`);
    }
  }
  console.log(`\n${failed === 0 ? 'PASS' : 'FAIL'} — ${passed} assertions passed, ${failed} failed.`);
  process.exit(failed === 0 ? 0 : 1);
}

main();
