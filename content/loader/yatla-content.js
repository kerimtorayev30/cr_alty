/*!
 * Ýatla — content loader (single-file-app compatible)
 *
 * Purpose: replace the hard-coded WORDS[] demo array with a loadable content pack,
 * while keeping app-yatla.html a single self-contained file (nothing is inlined
 * from here; the app fetches a small JSON pack and caches it locally).
 *
 * Resolution order (first hit wins):
 *   1. IndexedDB   (survives clearing site data less often than localStorage, no 5 MB cap)
 *   2. localStorage (works in the sandboxed preview iframe, which has no network)
 *   3. in-memory seed embedded in app-yatla.html (the 12 demo WORDS entries)
 *   4. network fetch of a compact bundle (only when the iframe/host allows it)
 *
 * Accepted bundle shapes:
 *   compact  { version, format:"array",  fields:[...], rows:[["hello","salam",...], ...] }
 *   dev      { version, format:"object", words:[{en:"hello", tm:"salam", ...}] }
 *   bare     [ {en:...}, ... ]
 *
 * No app globals are used ($, $$, t, go, sfx, hz are untouched). Every browser API
 * is feature-detected, so this runs unchanged under jsdom and in locked-down iframes.
 */
(function () {
  'use strict';

  var GLOBAL = typeof globalThis !== 'undefined' ? globalThis : window;

  /** Field order shared with content/tools/build.js — do not reorder without rebuilding bundles. */
  var FIELDS = ['en', 'ipa', 'pos', 'tm', 'ru', 'def', 'ex', 'exTm', 'cefr', 'ox', 'syn', 'coll', 'stage', 'books'];

  var DEFAULT_KEY = 'yatla_words_v1';
  var DB_NAME = 'yatla';
  var DB_VERSION = 1;
  var STORE = 'content';
  var NET_TIMEOUT_MS = 8000;

  /** Must mirror STAGE_C / STAGE_K in app-yatla.html. */
  var STAGES = ['New', 'Learning', 'Practicing', 'Remembered', 'Mastered'];

  /* ------------------------------------------------------------------ utils */

  function parseJSON(text) {
    try {
      return JSON.parse(text);
    } catch (e) {
      return null;
    }
  }

  function lsGet(key) {
    try {
      if (typeof localStorage === 'undefined' || !localStorage) return null;
      return parseJSON(localStorage.getItem(key));
    } catch (e) {
      return null; // private mode / disabled storage / sandboxed origin
    }
  }

  function lsSet(key, value) {
    try {
      if (typeof localStorage === 'undefined' || !localStorage) return false;
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (e) {
      return false; // quota exceeded
    }
  }

  /* ----------------------------------------------------------- normalisation */

  function normalizeWord(raw) {
    if (!raw || typeof raw !== 'object') return null;
    if (typeof raw.en !== 'string' || raw.en.length === 0) return null;
    // Defaults and shapes must match what app-yatla.html renders: syn/coll are
    // comma-separated strings, stage is one of the five STAGE_C labels, pos is uppercase.
    var w = {
      en: raw.en,
      ipa: raw.ipa || '',
      pos: raw.pos || 'N',
      tm: raw.tm || '',
      ru: raw.ru || '',
      def: raw.def || '',
      ex: raw.ex || '',
      exTm: raw.exTm || '',
      cefr: raw.cefr || 'A1',
      ox: raw.ox || 'Oxford 3000',
      syn: typeof raw.syn === 'string' ? raw.syn : (Array.isArray(raw.syn) && raw.syn.length ? raw.syn.join(', ') : '—'),
      coll: typeof raw.coll === 'string' ? raw.coll : (Array.isArray(raw.coll) && raw.coll.length ? raw.coll.join(', ') : '—'),
      stage: STAGES.indexOf(raw.stage) !== -1 ? raw.stage : 'New'
    };
    if (raw.books) w.books = raw.books;
    return w;
  }

  /** Accepts any of the three bundle shapes and returns a clean array, or [] on junk. */
  function normalizePack(data) {
    if (!data || typeof data !== 'object') return [];
    var rows = [];
    if (data.format === 'array' && Array.isArray(data.rows)) {
      var fields = Array.isArray(data.fields) && data.fields.length ? data.fields : FIELDS;
      rows = data.rows.map(function (r) {
        if (!Array.isArray(r)) return null;
        var o = {};
        for (var i = 0; i < fields.length; i++) o[fields[i]] = r[i];
        return o;
      });
    } else if (Array.isArray(data.words)) {
      rows = data.words;
    } else if (Array.isArray(data)) {
      rows = data;
    }
    var out = [];
    var seen = {};
    for (var j = 0; j < rows.length; j++) {
      var w = normalizeWord(rows[j]);
      if (!w) continue;
      var k = w.en.toLowerCase();
      if (seen[k]) continue; // a duplicate headword must not break the card deck
      seen[k] = 1;
      out.push(w);
    }
    return out;
  }

  /* --------------------------------------------------------------- embedded */

  /**
   * Reads a pack inlined into the host page as
   *   a JSON script element (type application/json) whose id is yatlaWords
   * NOTE: the closing tag is written "<\/script>" on purpose. The HTML parser ends a
   * script element at the first "</" + "script" sequence it sees, even inside a JS
   * comment, so a literal closing tag here would truncate the host page's script block.
   * This is the highest-priority source: it needs no network and no storage, so a
   * Capacitor build or a sandboxed preview can ship the full dictionary inline while
   * still keeping the single-file rule.
   */
  /* The pack carries a `lessons` list next to `words` (English File teaches each
     unit as lessons 1A/1B/1C). normalizePack only looks at words, so the metadata
     has to be picked up separately or it silently disappears. */
  function pickLessons(data) {
    if (!data || typeof data !== 'object') return [];
    var src = Array.isArray(data.lessons) ? data.lessons : [];
    var out = [];
    for (var i = 0; i < src.length; i++) {
      var l = src[i];
      if (l && l.lesson && l.book) out.push(l);
    }
    return out;
  }

  function embeddedPack() {
    try {
      if (typeof document === 'undefined' || !document) return null;
      var el = document.getElementById('yatlaWords');
      if (!el || !el.textContent) return null;
      return parseJSON(el.textContent);
    } catch (e) {
      return null;
    }
  }

  /* -------------------------------------------------------------- IndexedDB */

  function idbRequest(req) {
    return new Promise(function (resolve, reject) {
      req.onsuccess = function () {
        resolve(req.result);
      };
      req.onerror = function () {
        reject(req.error || new Error('IndexedDB request failed'));
      };
    });
  }

  function idbOpen() {
    return new Promise(function (resolve, reject) {
      if (typeof indexedDB === 'undefined' || !indexedDB) {
        reject(new Error('IndexedDB unavailable'));
        return;
      }
      var open = indexedDB.open(DB_NAME, DB_VERSION);
      open.onupgradeneeded = function () {
        var db = open.result;
        if (!db.objectStoreNames.contains(STORE)) db.createObjectStore(STORE);
      };
      open.onsuccess = function () {
        resolve(open.result);
      };
      open.onerror = function () {
        reject(open.error || new Error('IndexedDB open failed'));
      };
    });
  }

  function idbGet(key) {
    return idbOpen().then(function (db) {
      var tx = db.transaction(STORE, 'readonly');
      return idbRequest(tx.objectStore(STORE).get(key));
    });
  }

  function idbSet(key, value) {
    return idbOpen().then(function (db) {
      var tx = db.transaction(STORE, 'readwrite');
      tx.objectStore(STORE).put(value, key);
      return idbRequest(tx).then(function () {
        return true;
      });
    });
  }

  /* ----------------------------------------------------------------- network */

  function fetchWithTimeout(url, ms) {
    var controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
    var init = controller ? { signal: controller.signal } : undefined;
    var timer = controller ? setTimeout(function () { controller.abort(); }, ms) : null;
    return fetch(url, init).then(function (res) {
      if (timer) clearTimeout(timer);
      if (!res || !res.ok) throw new Error('HTTP ' + (res ? res.status : 'unknown'));
      return res.text();
    });
  }

  function fromURL(url) {
    if (typeof fetch !== 'function') return Promise.reject(new Error('fetch unavailable'));
    return fetchWithTimeout(url, NET_TIMEOUT_MS).then(parseJSON);
  }

  /* ------------------------------------------------------------------ public */

  var cache = null; // module-level memo so repeated renders do not re-parse

  /**
   * Load the word pack. Never rejects: on total failure it resolves [] and the app
   * must keep its embedded seed words.
   *
   * @param {object} [opts]
   * @param {string} [opts.key]     storage key (default "yatla_words_v1")
   * @param {string} [opts.url]     bundle URL to fetch when no local copy exists
   * @param {boolean} [opts.noCache] skip the module-level memo (used by tests)
   * @returns {Promise<Array>} normalised word objects
   */
  function fetchWords(opts) {
    opts = opts || {};
    // An empty array is truthy, so `cache &&` alone would serve a failed lookup
    // forever. Require actual words before trusting the cache.
    if (cache && cache.length && !opts.noCache) {
      return Promise.resolve({ words: cache, source: 'cache' });
    }
    var key = opts.key || DEFAULT_KEY;
    var self = this;

    function done(words, source, lessons) {
      cache = words;
      return { words: words, source: source || 'seed', lessons: lessons || [] };
    }

    function localWords() {
      return idbGet(key)
        .then(normalizePack)
        .catch(function () {
          return normalizePack(lsGet(key));
        })
        .then(function (w) {
          return w && w.length ? w : null;
        });
    }

    var embeddedRaw = embeddedPack();
    var embedded = normalizePack(embeddedRaw);
    // Must stay a Promise: callers do fetchWords(...).then(...). A bare early return
    // here would break them with "then is not a function".
    if (embedded.length) return Promise.resolve(done(embedded, 'embedded', pickLessons(embeddedRaw)));

    return localWords().then(function (w) {
      if (w) return done(w, 'cache');
      if (cache) return done(cache, 'seed');
      if (!opts.url) return done([], 'none');
      return fromURL(opts.url)
        .then(function (pack) {
          var words = normalizePack(pack);
          if (!words.length) return done(cache || [], 'none', pickLessons(pack));
          // Best-effort persistence. Both calls are fire-and-forget and swallow errors:
          // a sandboxed iframe without storage must still get its words this session.
          var stored = lsSet(key, pack);
          if (!stored) {
            idbSet(key, pack).catch(function () { /* no IndexedDB either — fine */ });
          }
          return done(words, 'network', pickLessons(pack));
        })
        .catch(function () {
          return done(cache || [], 'none');
        });
    });
  }

  /** Replace the cached pack (used after an in-app "download book" finishes). */
  function setWords(pack) {
    cache = normalizePack(pack);
    return cache;
  }

  /** Drop every cached copy. Returns a promise that always resolves. */
  function clearCache(key) {
    var k = key || DEFAULT_KEY;
    cache = null;
    try {
      if (typeof localStorage !== 'undefined' && localStorage) localStorage.removeItem(k);
    } catch (e) { /* ignore */ }
    return idbOpen()
      .then(function (db) {
        var tx = db.transaction(STORE, 'readwrite');
        return idbRequest(tx.objectStore(STORE).delete(k)).then(function () {
          return true;
        });
      })
      .catch(function () {
        return false;
      });
  }

  /** Merge new words into a pack without duplicating headwords. */
  function mergePacks(base, extra) {
    var out = normalizePack(base);
    var seen = {};
    out.forEach(function (w) { seen[w.en.toLowerCase()] = 1; });
    normalizePack(extra).forEach(function (w) {
      if (seen[w.en.toLowerCase()]) return;
      seen[w.en.toLowerCase()] = 1;
      out.push(w);
    });
    return out;
  }

  var api = {
    FIELDS: FIELDS,
    STAGES: STAGES,
    DEFAULT_KEY: DEFAULT_KEY,
    fetchWords: fetchWords,
    normalizePack: normalizePack,
    normalizeWord: normalizeWord,
    setWords: setWords,
    embeddedPack: embeddedPack,
    clearCache: clearCache,
    mergePacks: mergePacks
  };

  GLOBAL.YatlaContent = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})();
