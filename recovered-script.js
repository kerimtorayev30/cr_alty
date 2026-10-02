
/* ================= CONTENT PACK (loader, inline) ================= */
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
   *   <script type="application/json" id="yatlaWords">…<\/script>
   * NOTE: the closing tag is written "<\/script>" on purpose. The HTML parser ends a
   * <script> element at the first "</" + "script" sequence it sees, even inside a JS
   * comment, so a literal closing tag here would truncate the host page's script block.
   * This is the highest-priority source: it needs no network and no storage, so a
   * Capacitor build or a sandboxed preview can ship the full dictionary inline while
   * still keeping the single-file rule.
   */
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
    if (cache && !opts.noCache) return Promise.resolve(cache);
    var key = opts.key || DEFAULT_KEY;
    var self = this;

    function done(words, source) {
      cache = words;
      return { words: words, source: source || 'seed' };
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

    var embedded = normalizePack(embeddedPack());
    // Must stay a Promise: callers do fetchWords(...).then(...). A bare early return
    // here would break them with "then is not a function".
    if (embedded.length) return Promise.resolve(done(embedded, 'embedded'));

    return localWords().then(function (w) {
      if (w) return done(w, 'cache');
      if (cache) return done(cache, 'seed');
      if (!opts.url) return done([], 'none');
      return fromURL(opts.url)
        .then(function (pack) {
          var words = normalizePack(pack);
          if (!words.length) return done(cache || [], 'none');
          // Best-effort persistence. Both calls are fire-and-forget and swallow errors:
          // a sandboxed iframe without storage must still get its words this session.
          var stored = lsSet(key, pack);
          if (!stored) {
            idbSet(key, pack).catch(function () { /* no IndexedDB either — fine */ });
          }
          return done(words, 'network');
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

/* ================= DATA ================= */
const BOOKS=[
 {id:"beg",t:"Beginner",lv:"A1",c:"linear-gradient(160deg,#FB923C,#F97316)",units:12,done:3,dl:1,mb:24},
 {id:"ele",t:"Elementary",lv:"A2",c:"linear-gradient(160deg,#FDE047,#EAB308)",dk:1,units:12,done:1,dl:1,mb:26},
 {id:"pre",t:"Pre-Intermediate",lv:"B1",c:"linear-gradient(160deg,#8ED968,#58BE2F)",units:12,done:0,dl:1,mb:28},
 {id:"int",t:"Intermediate",lv:"B2",c:"linear-gradient(160deg,#2DD4BF,#14B8A6)",units:12,done:0,dl:0,mb:30},
 {id:"upp",t:"Upper-Intermediate",lv:"C1",c:"linear-gradient(160deg,#60A5FA,#3B82F6)",units:12,done:0,dl:0,mb:31},
 {id:"adv",t:"Advanced",lv:"C2",c:"linear-gradient(160deg,#A78BFA,#8B5CF6)",units:12,done:0,dl:0,mb:33},
 {id:"intp",t:"Intermediate Plus",lv:"B2+",c:"linear-gradient(160deg,#34D399,#059669)",units:12,done:0,dl:0,mb:32},
 {id:"advp",t:"Advanced Plus",lv:"C2+",c:"linear-gradient(160deg,#F472B6,#DB2777)",units:12,done:0,dl:0,mb:34}];
const WORDS=[
 {en:"hello",ipa:"/həˈləʊ/",pos:"INTJ",tm:"salam",ru:"привет",def:"a word used to greet someone",ex:"Hello! How are you?",exTm:"Salam! Nähiň?",cefr:"A1",ox:"Oxford 3000",syn:"hi, greetings",coll:"say hello",stage:"Mastered"},
 {en:"name",ipa:"/neɪm/",pos:"N",tm:"at",ru:"имя",def:"the word that someone is called by",ex:"My name is Aria.",exTm:"Meniň adym Aria.",cefr:"A1",ox:"Oxford 3000",syn:"title",coll:"first name",stage:"Remembered"},
 {en:"country",ipa:"/ˈkʌntri/",pos:"N",tm:"ýurt",ru:"страна",def:"a nation with its own land",ex:"Türkiye is a beautiful country.",exTm:"Türkiýe owadan ýurt.",cefr:"A1",ox:"Oxford 3000",syn:"nation",coll:"home country",stage:"Practicing"},
 {en:"job",ipa:"/dʒɒb/",pos:"N",tm:"iş",ru:"работа",def:"the work you do to earn money",ex:"She has a new job.",exTm:"Onuň täze işi bar.",cefr:"A1",ox:"Oxford 3000",syn:"work, occupation",coll:"full-time job",stage:"Learning"},
 {en:"family",ipa:"/ˈfæməli/",pos:"N",tm:"maşgala",ru:"семья",def:"your parents, brothers and sisters",ex:"I love my family.",exTm:"Men maşgalamy söýýärin.",cefr:"A1",ox:"Oxford 3000",syn:"relatives",coll:"family member",stage:"New"},
 {en:"friend",ipa:"/frend/",pos:"N",tm:"dost",ru:"друг",def:"a person you like and trust",ex:"He is my best friend.",exTm:"Ol meniň iň gowy dostum.",cefr:"A1",ox:"Oxford 3000",syn:"pal, companion",coll:"best friend",stage:"Mastered"},
 {en:"water",ipa:"/ˈwɔːtə/",pos:"N",tm:"suw",ru:"вода",def:"the clear liquid you drink every day",ex:"Can I have some water?",exTm:"Biraz suw alyp bilerinmi?",cefr:"A1",ox:"Oxford 3000",syn:"—",coll:"glass of water",stage:"Remembered"},
 {en:"book",ipa:"/bʊk/",pos:"N",tm:"kitap",ru:"книга",def:"pages with words that you read",ex:"This book is interesting.",exTm:"Bu kitap gyzykly.",cefr:"A1",ox:"Oxford 3000",syn:"volume",coll:"read a book",stage:"Practicing"},
 {en:"teacher",ipa:"/ˈtiːtʃə/",pos:"N",tm:"mugallym",ru:"учитель",def:"a person who helps you learn",ex:"Our teacher is kind.",exTm:"Biziň mugallymymyz mähirli.",cefr:"A1",ox:"Oxford 3000",syn:"tutor",coll:"English teacher",stage:"Learning"},
 {en:"school",ipa:"/skuːl/",pos:"N",tm:"mekdep",ru:"школа",def:"the place where children learn",ex:"The school is big.",exTm:"Mekdep uly.",cefr:"A1",ox:"Oxford 3000",syn:"academy",coll:"at school",stage:"New"},
 {en:"morning",ipa:"/ˈmɔːnŋ/",pos:"N",tm:"ertir",ru:"утро",def:"the early part of the day",ex:"I drink tea every morning.",exTm:"Men her ertir çaý içýärin.",cefr:"A1",ox:"Oxford 3000",syn:"dawn",coll:"in the morning",stage:"Practicing"},
 {en:"thank",ipa:"/θæŋk/",pos:"V",tm:"sag bol",ru:"спасибо",def:"to say you are grateful",ex:"Thank you for your help!",exTm:"Kömegiň üçin sag bol!",cefr:"A1",ox:"Oxford 3000",syn:"appreciate",coll:"thank you",stage:"Mastered"}];
const STAGE_C={New:"#94A3B8",Learning:"#3B82F6",Practicing:"#EAB308",Remembered:"#14B8A6",Mastered:"#58BE2F"};
const I18N={
 en:{bk_intp:"Intermediate Plus",bk_advp:"Advanced Plus",all_w:"All words",recent_s:"Recent words",no_recent:"No words yet — open a word and it will show up here",done_lab:"Unit done",promo_week:"Weekly promotion",spots:"{n} spots",cutover:"Finish in the top {n} this week to move up",rank_m:"MONTHLY RANK",lm_sub:"Your place this month · the league table is hidden",lm_delta:"vs last month",top_n:"Top {n}",back_top:"Back to top",pack_on:"{n} words ready",home:"Home",learning:"Learning",search:"Search",league:"League",profile:"Profile",today:"What should I do today?",cont:"CONTINUE LEARNING",goal:"DAILY GOAL",streak:"Current Streak · keep it alive!",chal:"DAILY CHALLENGE",week:"WEEKLY PROGRESS",wotd:"WORD OF THE DAY",recent:"RECENT ACTIVITY",
 ob_t1:"Remember every word.",ob_t2:"For life.",ob_sub:"The premium offline companion for Oxford English File students.",ob_create:"Create an Account",ob_login:"Log In",ob_or:"or continue with",ob_terms:'By continuing, you agree to our<br><a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>',
 home_hi:"Hey, Aria!",home_unit:"English File Beginner · Unit 4",home_sub:"Everyday vocabulary · 6 words left",btn_continue:"Continue",today_words:"Today’s words",words:"words",day_streak:"day streak",chal1:"Learn {n} words",chal2:"Complete 2 reviews",start:"Start",lprev_t:"Silver League · Rank #4",lprev_s:"Promotion zone · ends in 2d 14h",open:"Open",act1:"Yesterday · Unit 3 completed",act1s:"12 words · 92% accuracy · +45 XP",
 learn_sub:"Oxford English File library",offline:"Offline ready",units_w:"units",not_dl:"Not downloaded",dl:"Download",dling:"Downloading…",dl_done:"✓ Downloaded",mem:"Memory stages",st_new:"New",st_learning:"Learning",st_practicing:"Practicing",st_remembered:"Remembered",st_mastered:"Mastered",unit_w:"Unit",rev_ready:"Review ready",in_prog:"In progress",review_chip:"REVIEW",start_chip:"START",prev_b:"← Prev",next_b:"Next →",finish_b:"Finish ✓",complete_t:"Unit {u} complete!",words_lab:"Words",acc_lab:"Accuracy",back_home:"Back Home",to_review:"Continue to Review",
 flash:"Flashcard",tapflip:"tap to flip",again:"↻ Again",knew:"✓ Knew it",fill:"Fill in the blank",type_en:"Type the English word…",hint:"Hint",check:"CHECK",continue_b:"CONTINUE",correct:"Correct!",answer:"Answer: ",sum_t:"Review summary",correct_lab:"Correct",
 search_sub:"Offline multilingual explorer · EN · TM · RU",placeholder:"Search EN, TM or RU…",favs_f:"♥ Favorites",results:"Results",turkmen_k:"TURKMEN",russian_k:"RUSSIAN",def_k:"DEFINITION",ex_k:"EXAMPLE",syn_k:"SYNONYMS",coll_k:"COLLOCATIONS",seen_k:"Times seen",learn_word:"Learn this word",
 league_sub:"Weekly season · fair competition",ends:"2d 14h",bronze:"Bronze",silver:"Silver",gold:"Gold",sapphire:"Sapphire",emerald:"Emerald",legend:"Legend",rank_line:"Rank #4 · 320 LP",wk_rewards:"WEEKLY REWARDS",wk_sub:"Top 3: champion badge + bonus league points",history:"League History",hist1:"Week 33 · Silver",hist1s:"#3 · promoted",hist2:"Week 32 · Bronze",hist2s:"#1 · promoted",hist3:"Week 31 · Bronze",hist3s:"#6",
 title_t:"Word Collector · Level 6",analytics:"ANALYTICS",time_learned:"Time learned",words_mast:"Words mastered",avg_acc:"Avg accuracy",ach_t:"ACHIEVEMENTS · 12/50",ach1:"On Fire",ach2:"Champion",ach3:"Quick Learner",ach4:"Polyglot",favorites:"Favorites",dl_books:"Downloaded Books",storage:"312 MB of 2 GB",prem_sub:"Advanced analytics · unlimited reviews · premium themes",manage:"Manage",settings:"Settings",lang_t:"Interface language",lang_sub:"Instant switch · learning stays English",dark_t:"Dark mode",dark_sub:"Eye-friendly study",cert_t:"Certificates",earned:"2 earned",logout:"Log out",
 rev_lab:"REVIEW · SELECT THE CORRECT TRANSLATION",nicely:"Nicely done!",notquite:"Not quite…",xpmsg:"Correct! · Streak extended 🔥",correct_ans:"Correct: “¿Hola, cómo estás?”",d0:"M",d1:"T",d2:"W",d3:"T",d4:"F",d5:"S",d6:"S",badge_beg:"A1 Beginner",badge_pr:"★ Premium",bk_beg:"Beginner",bk_ele:"Elementary",bk_pre:"Pre-Intermediate",bk_int:"Intermediate",bk_upp:"Upper-Intermediate",bk_adv:"Advanced",goal_t:"Set your daily goal",goal_sub:"You can change this anytime in Settings.",g_casual:"Casual",g_casual_s:"25 words / day",g_regular:"Regular",g_regular_s:"35 words / day",g_serious:"Serious",g_serious_s:"50 words / day",g_start:"Start learning",event_xp:"Weekend event · double league points on all reviews",share:"Share",shared:"Word card shared",auth_signup:"Create your account",auth_login:"Welcome back",a_name:"Name",a_email:"Email",a_pass:"Password (min 6)",a_pass2:"Repeat password",age_lbl:"I am 16+ or have guardian consent",auth_local:"Local-first account · stored on this device",btn_signup:"Create account",btn_login:"Log in",sw_login:"Already have an account? Log in",sw_signup:"New here? Create an account",err_email:"Enter a valid email",err_pass:"Password must be 6+ characters",err_match:"Passwords don't match",err_age:"Please confirm your age",err_exists:"Account exists — log in",err_nouser:"No account found — sign up",err_wrong:"Wrong password",acc_created:"Account created 🎉",wel_back:"Welcome back!",soc_stub:"Connect Firebase to enable social login",sound_t:"Sound effects",sound_sub:"Correct / wrong / clicks",notif_t:"Study reminders",notif_sub:"Streak & review alerts",notif_on:"Reminders on",notif_no:"Notifications unavailable",lprev_fmt:"Silver League · Rank #{p}",lp_next:"{lp} LP · {tier}",lp_max:"Max tier — stay on top!",prem_f1:"Unlimited reviews",prem_f2:"Advanced analytics",prem_f3:"Gold badge, crown & themes",prem_status:"Free plan · upgrade to unlock everything",prem_on_status:"✨ Premium active on this device",prem_cta:"✨ Get Premium",prem_active:"✓ PREMIUM MEMBER",prem_toast:"Welcome to Premium ✨",prem_thanks:"You're already Premium ✨",prem_cancel:"Cancel Premium (demo)",prem_off:"Premium cancelled",prem_rib:"Premium active · full dictionary, offline",xpmsg2:"Correct! · PREMIUM 🔥",lang_q:"App language"},
 tk:{bk_intp:"Orta plus",bk_advp:"Ösen plus",all_w:"Ähli sözler",recent_s:"Soňky sözler",no_recent:"Entek söz ýok — bir sözi açyň, ol şu ýerde görner",done_lab:"Bölüm tamam",promo_week:"Hepdelik ýokarlanma",spots:"{n} orun",cutover:"Ýokarlanmak üçin şu hepde ilkinji {n}-e giriň",rank_m:"AÝLYK ORUN",lm_sub:"Şu aýdaky ornuňyz · liga tablisasy gizlin",lm_delta:"geçen aýa görä",top_n:"Ilkinji {n}",back_top:"Ýokaryk",pack_on:"{n} söz taýýar",home:"Baş sahypa",learning:"Öwrenme",search:"Gözleg",league:"Liga",profile:"Profil",today:"Bu gün näme etmeli?",cont:"ÖWRENMEGI DOWAM ET",goal:"GÜNDÄKI MAKSAT",streak:"Häzirki seriýa · dowam et!",chal:"GÜNDÄKI SYNAG",week:"HEPDELIK ÖSÜŞ",wotd:"GÜNÜŇ SÖZI",recent:"SOŇKY IŞLER",
 ob_t1:"Her sözi ýatda sakla.",ob_t2:"Ömürlik.",ob_sub:"Oxford English File talyplary üçin premium offline ýardamçy.",ob_create:"Hasap aç",ob_login:"Gir",ob_or:"ýa-da şeýle dowam et",ob_terms:'Dowam etmek bilen, siz<br><a href="#">Ulanyş şertleri</a> we <a href="#">Gizlinlik syýasaty</a> bilen razylaşýarsyňyz',
 home_hi:"Salam, Aria!",home_unit:"English File Başlangyç · Bölüm 4",home_sub:"Gündelik sözler · 6 söz galdy",btn_continue:"Dowam et",today_words:"Şu günki sözler",words:"söz",day_streak:"günlik seriýa",chal1:"{n} söz öwren",chal2:"2 gaýtalaýyş tamamla",start:"Başla",lprev_t:"Kümüş Liga · #4 orun",lprev_s:"Ösüş zolagy · 2g 14s galdy",open:"Aç",act1:"Düýn · Bölüm 3 tamamlandy",act1s:"12 söz · 92% takyklyk · +45 XP",
 learn_sub:"Oxford English File kitaphanasy",offline:"Offline taýýar",units_w:"bölüm",not_dl:"Ýüklenmedik",dl:"Ýükle",dling:"Ýüklenýär…",dl_done:"✓ Ýüklendi",mem:"Ýat basgançaklary",st_new:"Täze",st_learning:"Öwrenilýär",st_practicing:"Türgenleşik",st_remembered:"Ýadyňyzda",st_mastered:"Kämil",unit_w:"Bölüm",rev_ready:"Gaýtalaýyş taýýar",in_prog:"Dowam edýär",review_chip:"GAÝTALA",start_chip:"BAŞLA",prev_b:"← Öňki",next_b:"Indiki →",finish_b:"Tamamla ✓",complete_t:"Bölüm {u} tamamlandy!",words_lab:"Söz",acc_lab:"Takyklyk",back_home:"Öýe dön",to_review:"Gaýtalaýyşa geç",
 flash:"Kartoçka",tapflip:"öwürmek üçin bas",again:"↻ Ýene",knew:"✓ Bildim",fill:"Boşlugy doldur",type_en:"Iňlis sözüni ýaz…",hint:"Maslahat",check:"BARLA",continue_b:"DOWAM",correct:"Dogry!",answer:"Jogap: ",sum_t:"Gaýtalaýyş netijesi",correct_lab:"Dogry",
 search_sub:"Offline köp dilli gözlegçi · EN · TM · RU",placeholder:"EN, TM ýa-da RU gözle…",favs_f:"♥ Halanlarym",results:"Netijeler",turkmen_k:"TÜRKMEN",russian_k:"RUS",def_k:"DÜŞÜNDIRIŞ",ex_k:"MYSAL",syn_k:"SINONIMLER",coll_k:"KOLOKASIÝALAR",seen_k:"Görülen gezek",learn_word:"Bu sözi öwren",
 league_sub:"Hepdelik möwsüm · adalatly bäsleşik",ends:"2g 14s",bronze:"Bürünç",silver:"Kümüş",gold:"Altyn",sapphire:"Sapfir",emerald:"Zumrud",legend:"Legenda",rank_line:"#4 orun · 320 LP",wk_rewards:"HEPDELIK SOWGATLAR",wk_sub:"Ilkinji 3: çempion nyşany + goşmaça liga utugy",history:"Liga taryhy",hist1:"Hepde 33 · Kümüş",hist1s:"#3 · ösdi",hist2:"Hepde 32 · Bürünç",hist2s:"#1 · ösdi",hist3:"Hepde 31 · Bürünç",hist3s:"#6",
 title_t:"Söz ýygnaýjy · Dereje 6",analytics:"ANALITIKA",time_learned:"Öwrenilen wagt",words_mast:"Özleşdirilen söz",avg_acc:"Orta takyklyk",ach_t:"ÜSTÜNLIKLER · 12/50",ach1:"Otly",ach2:"Çempion",ach3:"Çalt öwren",ach4:"Poliglot",favorites:"Halanlarym",dl_books:"Ýüklenen kitaplar",storage:"2 GB-dan 312 MB",prem_sub:"Giňişleýin analitika · çäksiz gaýtalaýyş · premium temalar",manage:"Dolandyryş",settings:"Sazlamalar",lang_t:"Interfeýs dili",lang_sub:"Çalt çalşyrma · sapak iňlisçe",dark_t:"Garaňky režim",dark_sub:"Göze ýeňil",cert_t:"Sertifikatlar",earned:"2 alyndy",logout:"Çyk",
 rev_lab:"GAÝTALAÝYŞ · DOGRY TERJIMÄNI SAÝLA",nicely:"Berekdi!",notquite:"Bolmady…",xpmsg:"Dogry! · Seriýa uzaldy 🔥",correct_ans:"Dogry: “¿Hola, cómo estás?”",d0:"Du",d1:"Si",d2:"Ça",d3:"Pe",d4:"An",d5:"Şe",d6:"Ýe",badge_beg:"A1 Başlangyç",badge_pr:"★ Premium",bk_beg:"Başlangyç",bk_ele:"Esasy",bk_pre:"Öň-orta",bk_int:"Orta",bk_upp:"Ýokary-orta",bk_adv:"Ösen",goal_t:"Gündäki maksadyňyzy saýlaň",goal_sub:"Muny Sazlamalarda islän wagtyňyz üýtgedip bilersiňiz.",g_casual:"Ýeňil",g_casual_s:"25 söz / gün",g_regular:"Adaty",g_regular_s:"35 söz / gün",g_serious:"Çynlakaý",g_serious_s:"50 söz / gün",g_start:"Öwrenmä başla",event_xp:"Hepde soňy çäresi · iki esse liga utugy",share:"Paýlaş",shared:"Söz kartasy paýlaşyldy",auth_signup:"Hasabyňyzy dörediň",auth_login:"Hoş geldiňiz",a_name:"At",a_email:"Email",a_pass:"Parol (iň az 6)",a_pass2:"Paroly gaýtalaň",age_lbl:"16+ ýa-da hossar razylygy bar",auth_local:"Ýerli hasap · enjamda saklanýar",btn_signup:"Hasap aç",btn_login:"Gir",sw_login:"Hasabyňyz barmy? Giriň",sw_signup:"Täzemi? Hasap açyň",err_email:"Dogry email giriziň",err_pass:"Parol 6+ belgi bolmaly",err_match:"Parollar gabat gelenok",err_age:"Ýaşyňyzy tassyklaň",err_exists:"Hasap bar — giriň",err_nouser:"Hasap tapylmady — ýazylyň",err_wrong:"Nädogry parol",acc_created:"Hasap döredildi 🎉",wel_back:"Hoş geldiňiz!",soc_stub:"Sosial giriş üçin Firebase gerek",sound_t:"Ses efektleri",sound_sub:"Dogry / ýalňyş / klik",notif_t:"Ýatlatmalar",notif_sub:"Seriýa we gaýtalaýyş habarlary",notif_on:"Ýatlatmalar açyk",notif_no:"Habarlara elýeterlilik ýok",lprev_fmt:"Kümüş Liga · #{p} orun",lp_next:"{lp} LP · {tier}",lp_max:"Iň ýokary liga — öňde galyň!",prem_f1:"Çäksiz gaýtalaýyş",prem_f2:"Giňişleýin statistika",prem_f3:"Altyn nyşan, täç we temalar",prem_status:"Mugt meýilnama · hemmesini açmak üçin ýazylyň",prem_on_status:"✨ Premium bu enjamda işjeň",prem_cta:"✨ Premium al",prem_active:"✓ PREMIUM AGZA",prem_toast:"Premium-a hoş geldiňiz ✨",prem_thanks:"Siz eýýäm Premium ✨",prem_cancel:"Premium-y ýatyr (demo)",prem_off:"Premium ýatyryldy",prem_rib:"Premium işjeň · doly sözlük, oflaýn",xpmsg2:"Dogry! · PREMIUM 🔥",lang_q:"Programma dili"},
 ru:{bk_intp:"Средний плюс",bk_advp:"Продвинутый плюс",all_w:"Все слова",recent_s:"Недавние слова",no_recent:"Пока нет слов — откройте слово, и оно появится здесь",done_lab:"Юнит пройден",promo_week:"Недельное повышение",spots:"{n} мест",cutover:"Войдите в топ-{n} на этой неделе, чтобы подняться",rank_m:"МЕСЯЧНЫЙ РЕЙТИНГ",lm_sub:"Ваше место за месяц · таблица лиги скрыта",lm_delta:"к прошлому месяцу",top_n:"Топ-{n}",back_top:"Наверх",pack_on:"Готово слов: {n}",home:"Главная",learning:"Обучение",search:"Поиск",league:"Лига",profile:"Профиль",today:"Что мне сделать сегодня?",cont:"ПРОДОЛЖИТЬ ОБУЧЕНИЕ",goal:"ЦЕЛЬ ДНЯ",streak:"Текущая серия · не прерывай!",chal:"ИСПЫТАНИЕ ДНЯ",week:"НЕДЕЛЬНЫЙ ПРОГРЕСС",wotd:"СЛОВО ДНЯ",recent:"НЕДАВНЯЯ АКТИВНОСТЬ",
 ob_t1:"Помни каждое слово.",ob_t2:"Навсегда.",ob_sub:"Премиальный офлайн-помощник для студентов Oxford English File.",ob_create:"Создать аккаунт",ob_login:"Войти",ob_or:"или продолжить через",ob_terms:'Продолжая, вы соглашаетесь с<br><a href="#">Условиями использования</a> и <a href="#">Политикой конфиденциальности</a>',
 home_hi:"Привет, Aria!",home_unit:"English File Начинающий · Юнит 4",home_sub:"Повседневная лексика · осталось 6 слов",btn_continue:"Продолжить",today_words:"Слова за сегодня",words:"слов",day_streak:"дней подряд",chal1:"Выучить {n} слов",chal2:"Пройти 2 повторения",start:"Старт",lprev_t:"Серебряная лига · #4 место",lprev_s:"Зона повышения · 2д 14ч",open:"Открыть",act1:"Вчера · Юнит 3 завершён",act1s:"12 слов · 92% точность · +45 XP",
 learn_sub:"Библиотека Oxford English File",offline:"Офлайн готов",units_w:"юнитов",not_dl:"Не загружено",dl:"Скачать",dling:"Загрузка…",dl_done:"✓ Загружено",mem:"Этапы памяти",st_new:"Новое",st_learning:"Изучение",st_practicing:"Практика",st_remembered:"Помню",st_mastered:"Освоено",unit_w:"Юнит",rev_ready:"Повторение готово",in_prog:"В процессе",review_chip:"ПОВТОР",start_chip:"СТАРТ",prev_b:"← Назад",next_b:"Далее →",finish_b:"Готово ✓",complete_t:"Юнит {u} завершён!",words_lab:"Слова",acc_lab:"Точность",back_home:"Домой",to_review:"К повторению",
 flash:"Карточка",tapflip:"нажми — перевернётся",again:"↻ Ещё",knew:"✓ Знал",fill:"Заполни пропуск",type_en:"Введи английское слово…",hint:"Подсказка",check:"ПРОВЕРИТЬ",continue_b:"ДАЛЬШЕ",correct:"Верно!",answer:"Ответ: ",sum_t:"Итоги повторения",correct_lab:"Верно",
 search_sub:"Офлайн мультиязычный поиск · EN · TM · RU",placeholder:"Поиск EN, TM или RU…",favs_f:"♥ Избранное",results:"Результаты",turkmen_k:"ТУРКМЕНСКИЙ",russian_k:"РУССКИЙ",def_k:"ОПРЕДЕЛЕНИЕ",ex_k:"ПРИМЕР",syn_k:"СИНОНИМЫ",coll_k:"СОЧЕТАНИЯ",seen_k:"Просмотров",learn_word:"Учить это слово",
 league_sub:"Недельный сезон · честная конкуренция",ends:"2д 14ч",bronze:"Бронза",silver:"Серебро",gold:"Золото",sapphire:"Сапфир",emerald:"Изумруд",legend:"Легенда",rank_line:"#4 место · 320 LP",wk_rewards:"НЕДЕЛЬНЫЕ НАГРАДЫ",wk_sub:"Топ-3: значок чемпиона + бонусные очки лиги",history:"История лиги",hist1:"Неделя 33 · Серебро",hist1s:"#3 · повышение",hist2:"Неделя 32 · Бронза",hist2s:"#1 · повышение",hist3:"Неделя 31 · Бронза",hist3s:"#6",
 title_t:"Коллекционер слов · Уровень 6",analytics:"АНАЛИТИКА",time_learned:"Время учёбы",words_mast:"Слов освоено",avg_acc:"Средняя точность",ach_t:"ДОСТИЖЕНИЯ · 12/50",ach1:"В огне",ach2:"Чемпион",ach3:"Быстрый старт",ach4:"Полиглот",favorites:"Избранное",dl_books:"Загруженные книги",storage:"312 МБ из 2 ГБ",prem_sub:"Расширенная аналитика · безлимитные повторения · премиум-темы",manage:"Управлять",settings:"Настройки",lang_t:"Язык интерфейса",lang_sub:"Мгновенно · уроки на английском",dark_t:"Тёмная тема",dark_sub:"Комфортно глазам",cert_t:"Сертификаты",earned:"2 получено",logout:"Выйти",
 rev_lab:"ПОВТОРЕНИЕ · ВЫБЕРИ ВЕРНЫЙ ПЕРЕВОД",nicely:"Отлично!",notquite:"Не совсем…",xpmsg:"Верно! · серия продлена 🔥",correct_ans:"Верно: “¿Hola, cómo estás?”",d0:"Пн",d1:"Вт",d2:"Ср",d3:"Чт",d4:"Пт",d5:"Сб",d6:"Вс",badge_beg:"A1 Начинающий",badge_pr:"★ Премиум",bk_beg:"Начинающий",bk_ele:"Базовый",bk_pre:"Средний",bk_int:"Уверенный",bk_upp:"Высокий",bk_adv:"Продвинутый",goal_t:"Выберите цель на день",goal_sub:"Можно изменить в настройках в любой момент.",g_casual:"Лайт",g_casual_s:"25 слов / день",g_regular:"Обычно",g_regular_s:"35 слов / день",g_serious:"Серьёзно",g_serious_s:"50 слов / день",g_start:"Начать учиться",event_xp:"Ивент выходного дня · двойные очки лиги",share:"Поделиться",shared:"Карточка слова отправлена",auth_signup:"Создайте аккаунт",auth_login:"С возвращением",a_name:"Имя",a_email:"Email",a_pass:"Пароль (мин. 6)",a_pass2:"Повторите пароль",age_lbl:"Мне 16+ или есть согласие родителей",auth_local:"Локальный аккаунт · хранится на устройстве",btn_signup:"Создать аккаунт",btn_login:"Войти",sw_login:"Уже есть аккаунт? Войти",sw_signup:"Новичок? Создать аккаунт",err_email:"Введите корректный email",err_pass:"Пароль от 6 символов",err_match:"Пароли не совпадают",err_age:"Подтвердите возраст",err_exists:"Аккаунт существует — войдите",err_nouser:"Аккаунт не найден — зарегистрируйтесь",err_wrong:"Неверный пароль",acc_created:"Аккаунт создан 🎉",wel_back:"С возвращением!",soc_stub:"Для соцвхода нужен Firebase",sound_t:"Звуковые эффекты",sound_sub:"Верно / ошибка / клики",notif_t:"Напоминания",notif_sub:"Стрик и повторения",notif_on:"Напоминания включены",notif_no:"Уведомления недоступны",lprev_fmt:"Серебряная лига · #{p} место",lp_next:"{lp} LP · {tier}",lp_max:"Макс. лига — держитесь в топе!",prem_f1:"Безлимитные повторения",prem_f2:"Расширенная аналитика",prem_f3:"Золотой значок, корона и темы",prem_status:"Бесплатный план · обновите, чтобы открыть всё",prem_on_status:"✨ Premium активен на этом устройстве",prem_cta:"✨ Получить Premium",prem_active:"✓ PREMIUM УЧАСТНИК",prem_toast:"Добро пожаловать в Premium ✨",prem_thanks:"Вы уже Premium ✨",prem_cancel:"Отключить Premium (демо)",prem_off:"Premium отключён",prem_rib:"Premium активен · весь словарь офлайн",xpmsg2:"Верно! · PREMIUM 🔥",lang_q:"Язык приложения"}};
const STAGE_K={New:"st_new",Learning:"st_learning",Practicing:"st_practicing",Remembered:"st_remembered",Mastered:"st_mastered"};
function t(k,o){let v=(I18N[S.lang]||{})[k]??I18N.en[k]??k;if(o)for(const x in o)v=v.replace("{"+x+"}",o[x]);return v;}
const S={words:7,goal:25,streak:7,lang:"en",theme:"light",favs:new Set(["friend","water"]),hist:[],premium:false,
 lv:{view:"books",book:null,unit:null,idx:0,session:[]},rev:null,filter:"hist",sound:true,events:{},user:null,avatar:null};
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];

/* ================= NAV / TABS ================= */
const TABS=[["home","home","#i-home"],["learning","learning","#i-book"],["search","search","#i-search"],["league","league","#i-medal"],["profile","profile","#i-user"]];
function buildTabs(){$$(".tb").forEach(tb=>{const a=tb.dataset.active;
 tb.innerHTML=TABS.map(([id,k,ic])=>`<button class="tbi${id===a?" on":""}" data-go="scr-${id}"><svg><use href="${ic}"/></svg><span>${I18N[S.lang][k]}</span></button>`).join("");});}
function go(id){$$(".screen").forEach(s=>s.classList.toggle("on",s.id===id));
 if(id==="scr-learning"){if(!["books","units","vocab"].includes(S.lv.view))S.lv.view="books";renderLearning();}
 if(id==="scr-search"){showList();filt();}
 if(id==="scr-league")renderLeague();
  const t=$("#"+id+" .scroll");if(t)t.scrollTop=0;resetLesson();}
document.addEventListener("click",e=>{const b=e.target.closest("[data-go]");if(b)go(b.dataset.go);});

/* ================= THEME / LANG ================= */
function setTheme(d){S.theme=d?"dark":"light";document.documentElement.dataset.theme=S.theme;
 ["thico1","thico2"].forEach(i=>document.getElementById(i).setAttribute("href",d?"#i-sun":"#i-moon"));
 $("#darkSw").classList.toggle("on",d);save();}
$("#themeBtn1").onclick=()=>setTheme(S.theme!=="dark");
$("#themeBtn2").onclick=()=>setTheme(S.theme!=="dark");
$("#darkSw").onclick=()=>setTheme(S.theme!=="dark");
function setLang(l){S.lang=l;buildTabs();
 $$("[data-i18n]").forEach(el=>{const k=el.dataset.i18n,v=I18N[l][k]??I18N.en[k];if(v!=null)el.innerHTML=v;});
 const di=$("#dinput");if(di)di.placeholder=t("placeholder");
 [["aName","a_name"],["aEmail","a_email"],["aPass","a_pass"],["aPass2","a_pass2"]].forEach(([id,k])=>{const el=document.getElementById(id);if(el)el.placeholder=t(k);});
 $$("#langSegTop button,#langSeg button,#langSegOb button").forEach(b=>b.classList.toggle("on",b.dataset.l===l));
 refreshHome();renderFavs();renderDlBooks();renderLearning();filt();renderLeague();applyPremium();if(S.detailWord)openWord(S.detailWord);
}
document.addEventListener("click",e=>{const b=e.target.closest("#langSegTop button,#langSeg button,#langSegOb button");if(b)setLang(b.dataset.l);});
$("#logout").onclick=()=>go("scr-onboard");
$("#setBtn").onclick=()=>{go("scr-profile");const s=$("#setSec");
 if(s&&s.scrollIntoView)setTimeout(()=>s.scrollIntoView({block:"start"}),60);sfx("click");};
$("#setTop").onclick=()=>{const s=$("#scr-profile .scroll");
 if(s&&s.scrollTo)s.scrollTo({top:0,behavior:"smooth"});else if(s)s.scrollTop=0;};

/* ================= HOME ================= */
function refreshHome(){$("#hstreak").textContent=S.streak;$("#streak2").textContent=S.streak;
 const p=Math.min(100,Math.round(S.words/S.goal*100));
 $("#goalTxt").textContent=`${S.words} / ${S.goal} ${t("words")}`;$("#goalBar").style.width=p+"%";$("#goalEm").style.left=p+"%";$("#goalEm").textContent=p+"%";
 if(S.words>=S.goal)$("#ck1").classList.add("done");
 $("#chal1Txt").textContent=t("chal1",{n:S.goal});$("#chal1P").textContent=S.words+"/"+S.goal;
 renderLeague();}
$("#homeCont").onclick=()=>{S.lv={view:"units",book:BOOKS[0],unit:null,idx:0,session:[]};go("scr-learning");};
$("#leaguePrev").onclick=()=>go("scr-league");
$("#wotdOpen").onclick=()=>{go("scr-search");openWord(WORDS[5]);};
$("#chalReview").onclick=startReview;
$("#goalStart").onclick=()=>go("scr-home");
document.addEventListener("click",e=>{
 const g=e.target.closest(".gsel");if(g){S.goal=+g.dataset.g;$$(".gsel").forEach(x=>x.classList.toggle("sel",x===g));refreshHome();return;}
 if(e.target.closest("[data-share]")){toast(t("shared"));return;}
});
function toast(m){const el=$("#toast");el.textContent=m;el.classList.add("show");clearTimeout(el._t);el._t=setTimeout(()=>el.classList.remove("show"),1700);}

/* ================= LEARNING ================= */
function renderLearning(){const v=S.lv.view,el=$("#lv");
 if(v==="books"){el.innerHTML=`
  <div class="row spread" style="padding:10px 2px 0"><div><h2 class="h2" style="font-size:22px">${t("learning")}</h2>
  <p class="sub">${t("learn_sub")}</p></div>
  <span class="chip" style="color:var(--green-d)"><svg style="width:14px;height:14px"><use href="#i-leaf"/></svg>${t("offline")}</span></div>`+
  BOOKS.map((b,i)=>`<div class="card brow row" data-bk="${i}" style="gap:13px">
   <div class="cov" style="background:${b.c}${b.dk?";color:#4A3B08":""}"><span class="ox">OXFORD</span><span class="t">English File</span><span class="lv">${b.lv}</span></div>
   <div style="flex:1"><b>English File · ${t("bk_"+b.id)}</b><div class="meta">${b.dl?`${Math.round(b.done/b.units*100)}% · ${b.done}/${b.units} ${t("units_w")} · ${b.mb} MB ✓`:`${t("not_dl")} · ${b.mb} MB`}</div>
   ${b.dl?`<div class="dlbar"><i style="width:${Math.round(b.done/b.units*100)}%;background:var(--green)"></i></div>`:`<button class="btn btn-s" style="padding:8px;font-size:12px;margin-top:8px" data-dl="${i}"><svg style="width:14px;height:14px"><use href="#i-dl"/></svg> ${t("dl")}</button>`}</div>
   <svg style="width:16px;height:16px;color:var(--muted)"><use href="#i-chev"/></svg></div>`).join("")+`
  <div class="sec row spread"><span class="h2">${t("mem")}</span></div>
  <div class="chips" style="margin-top:0">${Object.keys(STAGE_C).map(k=>`<span class="rchip" style="color:#fff;background:${STAGE_C[k]};border:0">${t(STAGE_K[k])}</span>`).join("")}</div>`;return;}
 if(v==="units"){const b=S.lv.book;el.innerHTML=`
  <div class="vtop"><button class="icobtn" data-lv="books"><svg style="color:var(--deep)"><use href="#i-back"/></svg></button>
  <div><h2 class="h2" style="font-size:19px">English File · ${t("bk_"+b.id)}</h2><p class="sub">${b.units} ${t("units_w")} · ${b.lv}</p></div></div>`+
  Array.from({length:b.units},(_,u)=>{const n=u+1,st=n<=b.done?"done":n===b.done+1?"cur":"lock";
   return `<div class="card urow row" data-un="${n}" style="gap:12px">
   <span class="unum" style="background:${st==="done"?"#8ED968":st==="cur"?"var(--green)":"var(--track)"};color:${st==="lock"?"var(--muted)":"#fff"}">${st==="done"?"✓":n}</span>
   <div style="flex:1"><b style="font-size:14px">${t("unit_w")} ${n}</b><div class="meta sub">${unitCount(b.id,n)||"—"} ${t("words")} · ${st==="done"?"100%":st==="cur"?"60%":"0%"} · ${st==="done"?t("rev_ready"):st==="cur"?t("in_prog"):"—"}</div></div>
   ${st==="lock"?`<svg style="width:17px;height:17px;color:var(--muted)"><use href="#i-lock"/></svg>`:`<span class="st" style="background:${st==="done"?"var(--mint)":"#FFF7DB"};color:${st==="done"?"var(--green-d)":"#A16207"}">${st==="done"?t("review_chip"):t("start_chip")}</span>`}</div>`;}).join("");return;}
 if(v==="vocab"){const w=S.lv.session[S.lv.idx];el.innerHTML=`
  <div class="vtop"><button class="icobtn" data-lv="units"><svg style="color:var(--deep)"><use href="#i-back"/></svg></button>
  <div class="pbar" style="flex:1;margin:0"><i style="width:${Math.round((S.lv.idx)/S.lv.session.length*100)}%"></i></div>
  <span class="chip">${S.lv.idx+1}/${S.lv.session.length}</span>
  <button class="favb ${S.favs.has(w.en)?"on":""}" data-fav="${w.en}" style="width:42px;height:42px;border-radius:14px"><svg><use href="#i-heart"/></svg></button></div>
  <div class="card vcard">
   <div class="vword">${w.en}</div><div class="vipa">${w.ipa}</div>
   <span class="vpos">${w.pos}</span><span class="vstage" style="background:${STAGE_C[w.stage]}">${t(STAGE_K[w.stage])}</span>
   <div style="display:flex;justify-content:center;margin-top:12px"><button class="spk2" style="width:46px;height:46px"><svg style="width:20px;height:20px"><use href="#i-head"/></svg></button></div>
   <div class="vtr">${w.tm}</div><div class="vru">${w.ru}</div>
   <div class="vdef">${w.def}</div>
   <div class="vex">“${w.ex}”<span>${w.exTm}</span></div>
  </div>
  <div class="vbtns"><button class="btn btn-s" data-vprev ${S.lv.idx===0?"disabled style='opacity:.4'":""}>${t("prev_b")}</button>
  <button class="btn btn-p" data-vnext>${S.lv.idx===S.lv.session.length-1?t("finish_b"):t("next_b")}</button></div>`;return;}
 if(v==="complete"){confetti();track("unit_complete");hz([30,40,30]);el.innerHTML=`
  <div style="text-align:center;padding:36px 10px 10px"><div style="font-size:52px">🎉</div>
  <h2 class="h2" style="font-size:22px;margin-top:10px">${t("complete_t",{u:S.lv.unit})}</h2>
  <p class="sub">English File ${S.lv.book.t}</p></div>
  <div class="achs" style="grid-template-columns:repeat(4,1fr)">
   <div class="card ach"><b style="font-size:16px;color:var(--ink)">6</b><b>${t("words_lab")}</b></div>
   <div class="card ach"><b style="font-size:16px;color:var(--ink)">100%</b><b>${t("acc_lab")}</b></div>
   <div class="card ach"><svg style="width:17px;height:17px;color:var(--green-d)"><use href="#i-check"/></svg><b>${t("done_lab")}</b></div>
   <div class="card ach"><b style="font-size:16px;color:var(--gold)">+12</b><b>LP</b></div></div>
  <div class="vbtns" style="padding:0 8px"><button class="btn btn-s" data-lv="home2">${t("back_home")}</button>
  <button class="btn btn-p" data-rev="start">${t("to_review")}</button></div>`;return;}
 if(v==="review"){renderReview();return;}
 if(v==="summary"){const r=S.rev,acc=Math.round(r.correct/r.steps.length*100),xp=(10+r.correct*5)*(S.premium?2:1);
  el.innerHTML=`<div style="text-align:center;padding:36px 10px 10px"><div style="font-size:52px">${acc>=60?"🏆":"💪"}</div>
  <h2 class="h2" style="font-size:22px;margin-top:10px">${t("sum_t")}</h2></div>
  <div class="achs" style="grid-template-columns:repeat(3,1fr)">
   <div class="card ach"><b style="font-size:16px;color:var(--ink)">${acc}%</b><b>${t("acc_lab")}</b></div>
   <div class="card ach"><b style="font-size:16px;color:var(--ink)">${r.correct}/${r.steps.length}</b><b>${t("correct_lab")}</b></div>
   <div class="card ach"><svg style="width:17px;height:17px;color:var(--green-d)"><use href="#i-check"/></svg><b>${t("done_lab")}</b></div></div>
  <div class="vbtns" style="padding:0 8px"><button class="btn btn-p" data-rev="done">${t("back_home")}</button></div>`;
  if(!r.counted){r.counted=true;S.words=Math.min(S.goal,S.words+(r.doneWords||0));refreshHome();}return;}}
$("#lv").addEventListener("click",e=>{
 const dl=e.target.closest("[data-dl]");
 if(dl){const b=BOOKS[+dl.dataset.dl];dl.disabled=true;dl.innerHTML=t("dling")+" 0%";let p=0;
  const tmr=setInterval(()=>{p+=25;dl.innerHTML=p<100?`${t("dling")} ${p}%`:t("dl_done");
   if(p>=100){clearInterval(tmr);b.dl=1;setTimeout(renderLearning,400);}},350);return;}
 const bk=e.target.closest("[data-bk]");
 if(bk){const b=BOOKS[+bk.dataset.bk];if(!b.dl)return;S.lv={view:"units",book:b,unit:null,idx:0,session:[]};renderLearning();return;}
 const un=e.target.closest("[data-un]");
 if(un){const n=+un.dataset.un,b=S.lv.book;if(n>b.done+1)return;
  const ws=unitWords(b.id,n);if(!ws.length)return;S.lv={view:"vocab",book:b,unit:n,idx:0,session:ws};renderLearning();return;}
 const lb=e.target.closest("[data-lv]");
 if(lb){if(lb.dataset.lv==="home2")go("scr-home");else{S.lv.view=lb.dataset.lv;renderLearning();}return;}
 const fv=e.target.closest("[data-fav]");
 if(fv){const w=fv.dataset.fav;const on=!S.favs.has(w);on?S.favs.add(w):S.favs.delete(w);
  fv.classList.toggle("on",on);sfx(on?"good":"bad");hz(on?[15,25,15]:20);renderFavs();save();return;}
 if(e.target.closest("[data-vprev]")){S.lv.idx--;renderLearning();return;}
 if(e.target.closest("[data-vnext]")){if(S.lv.idx===S.lv.session.length-1){S.lv.view="complete";refreshHome();}
  else S.lv.idx++;renderLearning();return;}
 const rv=e.target.closest("[data-rev]");
 if(rv){if(rv.dataset.rev==="start")startReview();else go("scr-home");return;}
 revClick(e);});

/* ================= REVIEW ================= */
function startReview(){const ws=[...WORDS].sort(()=>Math.random()-.5).slice(0,5);
 S.rev={steps:ws.map((w,i)=>({t:i<3?"flip":"blank",w})),i:0,correct:0,doneWords:5,counted:false,wait:false};
 S.lv.view="review";go2learning();}
function go2learning(){$$(".screen").forEach(s=>s.classList.toggle("on",s.id==="scr-learning"));
 $$(".tb .tbi").forEach(b=>b.classList.toggle("on",b.dataset.go==="scr-learning"));renderLearning();}
function renderReview(){const r=S.rev;if(!r){S.lv.view="books";renderLearning();return;}
 const st=r.steps[r.i],el=$("#lv");
 const dots=`<div class="dots">${r.steps.map((_,i)=>`<span class="dot ${i<r.i?"done":i===r.i?"cur":""}"></span>`).join("")}</div>`;
 if(st.t==="flip"){el.innerHTML=`<div class="vtop"><span class="chip">${t("flash")} ${r.i+1}/${r.steps.length}</span></div>${dots}
  <div class="flip" id="fc"><div class="fcard">
   <div class="fface f"><span class="w">${st.w.en}</span><span class="sub">${st.w.ipa} · ${t("tapflip")}</span></div>
   <div class="fface b"><span class="w">${st.w.tm}</span><span style="font-size:13px;opacity:.85">${st.w.ru}</span></div>
  </div></div>
  <div class="vbtns" id="flipBtns" style="display:none">
   <button class="btn btn-s" data-rf="0">${t("again")}</button><button class="btn btn-p" data-rf="1">${t("knew")}</button></div>`;
  $("#fc").onclick=()=>{$("#fc").classList.add("flipped");$("#flipBtns").style.display="flex";};}
 else{const blank=st.w.ex.replace(new RegExp(st.w.en,"i"),"____");
  el.innerHTML=`<div class="vtop"><span class="chip">${t("fill")} ${r.i+1}/${r.steps.length}</span></div>${dots}
  <div class="card vcard"><div class="vex" style="font-size:16px">“${blank}”<span>${st.w.exTm}</span></div>
  <div class="sub" style="margin-top:10px">${t("hint")}: ${st.w.tm} · ${st.w.pos}</div>
  <input class="blankin" id="bin" placeholder="${t("type_en")}" autocomplete="off"></div>
  <div class="fb" id="rfb"></div>
  <button class="btn btn-p" data-rb="1">${t("check")}</button>`;}}
function revClick(e){const r=S.rev;if(!r||S.lv.view!=="review")return;
 const rf=e.target.closest("[data-rf]");
 if(rf){if(+rf.dataset.rf)r.correct++;r.i++;r.i<r.steps.length?renderReview():(S.lv.view="summary",renderLearning());return;}
 const rb=e.target.closest("[data-rb]");
 if(rb){const st=r.steps[r.i];
  if(!r.wait){const val=($("#bin").value||"").trim().toLowerCase();
   const ok=val===st.w.en.toLowerCase();if(ok)r.correct++;
   $("#rfb").className="fb "+(ok?"ok":"no");
   $("#rfb").innerHTML=`<span class="fic"><svg><use href="#${ok?"i-check":"i-x"}"/></svg></span><div><b>${ok?t("correct"):t("answer")+st.w.en}</b></div>`;
   r.wait=true;rb.textContent=t("continue_b");return;}
  r.wait=false;r.i++;r.i<r.steps.length?renderReview():(S.lv.view="summary",renderLearning());return;}}

/* ================= SEARCH ================= */
function showList(){S.detailWord=null;$("#slist").style.display="";$("#sdetail").style.display="none";}
function filt(){const q=($("#dinput").value||"").trim().toLowerCase();let n=0;
 /* Filters are content-neutral on purpose: recent words, favourites, or everything.
    Book filtering was removed from Search, and so were the memory-stage chips. */
 $("#dictlist").innerHTML=WORDS.map((w,i)=>{
  const hitF=S.filter==="all"?true:S.filter==="fav"?S.favs.has(w.en):S.hist.includes(w.en);
  const hit=!q||w.en.includes(q)||w.tm.toLowerCase().includes(q)||w.ru.toLowerCase().includes(q);
  const show=hit&&hitF;if(show)n++;
  return `<div class="card wrow row spread" data-w="${i}" style="display:${show?"":"none"}">
   <div><b>${w.en}</b><span class="en">${w.tm} · ${w.ru}</span></div>
   <div class="row" style="gap:8px">${S.favs.has(w.en)?`<svg style="width:15px;height:15px;color:var(--red)"><use href="#i-heart"/></svg>`:""}</div></div>`;}).join("");
 if(!n&&!q&&S.filter==="hist")$("#dictlist").innerHTML=`<div class="card" style="text-align:center;color:var(--muted);font-size:13px">${t("no_recent")}</div>`;
 $("#dcount").textContent=n+" "+t("words");}
$("#dinput").addEventListener("input",filt);
$("#schips").addEventListener("click",e=>{const c=e.target.closest(".rchip");if(!c)return;
 if(c.dataset.q!==undefined){$("#dinput").value=c.dataset.q;filt();return;}
 if(c.dataset.f){S.filter=c.dataset.f;$$("#schips [data-f]").forEach(x=>x.classList.toggle("on",x===c));filt();}});
$("#dictlist").addEventListener("click",e=>{const w=e.target.closest("[data-w]");if(w)openWord(WORDS[+w.dataset.w]);});
function openWord(w){S.detailWord=w;S.hist=[w.en].concat(S.hist.filter(x=>x!==w.en)).slice(0,12);$("#slist").style.display="none";const d=$("#sdetail");d.style.display="";
 const seen=(w.en.length*7)%40+8,acc=80+(w.en.length%4)*5;
 d.innerHTML=`<div class="vtop"><button class="icobtn" data-sback><svg style="color:var(--deep)"><use href="#i-back"/></svg></button>
  <div><h2 class="h2" style="font-size:19px">${w.en}</h2><p class="sub">${w.ipa} · ${w.pos}</p></div>
  <button class="favb ${S.favs.has(w.en)?"on":""}" data-fav2="${w.en}" style="margin-left:auto;width:42px;height:42px;border-radius:14px"><svg><use href="#i-heart"/></svg></button></div>
 <div class="card" style="padding:16px">
  <div class="dline"><span class="k">${t("turkmen_k")}</span>${w.tm}</div>
  <div class="dline"><span class="k">${t("russian_k")}</span>${w.ru}</div>
  <div class="dline"><span class="k">${t("def_k")}</span>${w.def}</div>
  <div class="dline"><span class="k">${t("ex_k")}</span>“${w.ex}”<br><span class="sub">${w.exTm}</span></div>
  <div class="dline"><span class="k">${t("syn_k")}</span>${w.syn}</div>
  <div class="dline"><span class="k">${t("coll_k")}</span>${w.coll}</div>
  <div class="row" style="gap:8px;flex-wrap:wrap;margin-top:10px">
   <span class="pos">${w.cefr}</span><span class="pos" style="background:#FFF7DB;color:#A16207">${w.ox}</span>
   <span class="pos" style="background:var(--track);color:var(--muted)">${t("bk_beg")} · ${t("unit_w")} 1</span>
   <span class="vstage" style="background:${STAGE_C[w.stage]};margin:0">${t(STAGE_K[w.stage])}</span></div>
  <div class="dgrid">
   <div class="card dstat"><b>${seen}</b><span>${t("seen_k")}</span></div>
   <div class="card dstat"><b>${acc}%</b><span>${t("acc_lab")}</span></div></div>
  <div class="vbtns" style="margin-top:12px"><button class="spk2" style="width:46px;height:46px"><svg style="width:20px;height:20px"><use href="#i-head"/></svg></button>
  <button class="btn btn-p" data-slearn>${t("learn_word")}</button></div></div>`;
 d.querySelector("[data-sback]").onclick=showList;
 d.querySelector("[data-fav2]").onclick=ev=>{const k=ev.currentTarget.dataset.fav2;
  const on=!S.favs.has(k);on?S.favs.add(k):S.favs.delete(k);
  sfx(on?"good":"bad");hz(on?[15,25,15]:20);
  renderFavs();filt();openWord(w);save();};
 d.querySelector("[data-slearn]").onclick=()=>{const wb=wordBook(w);const ws=unitWords(wb.bk.id,wb.un);S.lv={view:"vocab",book:wb.bk,unit:wb.un,idx:Math.max(0,ws.indexOf(w)),session:ws.length?ws:[w]};go2learning();};}
function renderFavs(){$("#favcount").textContent=S.favs.size+" "+t("words");
 $("#favchips").innerHTML=[...S.favs].map(f=>`<span class="rchip on">♥ ${f}</span>`).join("")||'<span class="sub">No favorites yet</span>';}
function renderDlBooks(){$("#dlbooks").innerHTML=BOOKS.filter(b=>b.dl).map(b=>`<div class="mrow"><span class="mico" style="background:${b.c}"><svg><use href="#i-book"/></svg></span><b style="flex:1">English File · ${t("bk_"+b.id)}</b><span class="val">${b.mb} MB ✓</span></div>`).join("");}
renderDlBooks();

/* ================= LESSON MCQ ================= */
let sel=null,checked=false;
const opts=$$("#opts .opt"),btn=$("#btnCheck"),fb=$("#fb");
opts.forEach(o=>o.addEventListener("click",()=>{if(checked)return;sel=o.dataset.v;
 opts.forEach(x=>x.classList.toggle("sel",x===o));btn.disabled=false;}));
btn.addEventListener("click",()=>{if(!checked){checked=true;const ok=sel==="salam";
 fb.className="fb "+(ok?"ok":"no");$("#fbic").setAttribute("href",ok?"#i-check":"#i-x");
 $("#fbt").textContent=ok?t("nicely"):t("notquite");
 $("#fbs").textContent=ok?t(S.premium?"xpmsg2":"xpmsg"):t("correct_ans");
 if(ok){sfx("good");track("mcq_correct");refreshHome();}else sfx("bad");
 $("#lprog").style.width="60%";btn.textContent="CONTINUE";}else go("scr-home");});
function resetLesson(){sel=null;checked=false;opts.forEach(x=>x.classList.remove("sel"));
 btn.disabled=true;btn.textContent="CHECK";fb.className="fb";$("#lprog").style.width="40%";}

/* ================= REAL SYSTEMS (local-first) ================= */
function save(){try{localStorage.setItem("yatla_state",JSON.stringify({words:S.words,goal:S.goal,premium:S.premium,
 streak:S.streak,lang:S.lang,theme:S.theme,sound:S.sound,favs:[...S.favs],hist:S.hist,
 user:S.user,avatar:S.avatar,events:S.events}));}catch(e){}}
function load(){try{const o=JSON.parse(localStorage.getItem("yatla_state")||"null");
 if(o){delete o.gems;delete o.chest;delete o.freeze;/* legacy saves must not resurrect the removed currency */
  Object.assign(S,o);S.favs=new Set(o.favs||["friend","water"]);S.hist=Array.isArray(o.hist)?o.hist:[];}}catch(e){}}
setInterval(save,2000);
window.addEventListener("beforeunload",save);document.addEventListener("visibilitychange",save);
function track(n){S.events=S.events||{};S.events[n]=(S.events[n]||0)+1;
 const el=$("#anStats");if(el)el.textContent=Object.values(S.events).reduce((a,b)=>a+b,0)+" events · "+Object.keys(S.events).length+" types · local log";}
window.addEventListener("error",e=>{S.lastErr=String(e.message||"").slice(0,60);});
let AC=null;
function sfx(k){if(S.sound===false)return;try{AC=AC||new (window.AudioContext||window.webkitAudioContext)();
 const o=AC.createOscillator(),g=AC.createGain();o.connect(g);g.connect(AC.destination);
 o.frequency.value=k==="good"?880:k==="bad"?196:520;
 g.gain.setValueAtTime(.12,AC.currentTime);g.gain.exponentialRampToValueAtTime(.001,AC.currentTime+(k==="click"?.08:.28));
 o.start();o.stop(AC.currentTime+(k==="click"?.09:.3));}catch(e){}}
function hz(p){try{navigator.vibrate&&navigator.vibrate(p);}catch(e){}}
function speak(txt){try{if("speechSynthesis" in window){const u=new SpeechSynthesisUtterance(txt);u.lang="en-GB";u.rate=.9;
 speechSynthesis.cancel();speechSynthesis.speak(u);}}catch(e){}}
function confetti(){const host=$(".phone"),cols=["#58BE2F","#FACC15","#F97316","#EC4899","#3B82F6","#8B5CF6"];
 for(let i=0;i<36;i++){const c=document.createElement("i");c.className="cf";c.style.left=Math.random()*100+"%";
  c.style.background=cols[i%6];c.style.animationDuration=(0.9+Math.random()*0.8)+"s";c.style.animationDelay=Math.random()*0.2+"s";
  host.appendChild(c);setTimeout(()=>c.remove(),2100);}}
/* --- live league with bot opponents --- */
const BOTS=[["Maya G.","#EC4899"],["Arslan T.","#3B82F6"],["Jennet M.","#8B5CF6"],["Kerim B.","#F97316"],["Laura S.","#14B8A6"],["Omar P.","#64748B"],["Selbi A.","#EAB308"]];
const TIERS=[{k:"bz",key:"bronze",icon:"#i-tbz",min:0},{k:"sv",key:"silver",icon:"#i-tsv",min:300},{k:"gd",key:"gold",icon:"#i-tgd",min:500},{k:"sp",key:"sapphire",icon:"#i-tsp",min:700},{k:"em",key:"emerald",icon:"#i-tem",min:900},{k:"lg",key:"legend",icon:"#i-tlg",min:1100}];
function myTier(lp){let x=TIERS[0];for(const z of TIERS)if(lp>=z.min)x=z;return x;}
const TIER_Q={bz:50,sv:25,gd:12,sp:6,em:3,lg:1};/* weekly promotion spots, shrinking as the tier rises */
const TIER_EMB={bz:"#i-mbz",sv:"#i-msv",gd:"#i-mgd",sp:"#i-msp",em:"#i-mem",lg:"#i-mlg"};
function renderLeague(){
 /* League points are a ranking measure, not a currency: they come from the streak and
    the words done this week. Nothing here can be spent. */
 const lp=200+S.streak*12+S.words*3;
 const ti=TIERS.findIndex(z=>lp>=z.min),tix=ti<0?0:ti,tier=TIERS[tix],next=TIERS[tix+1];
 const quota=TIER_Q[tier.k]||1;
 $("#lhero").dataset.t=tier.k;
 $("#lheroUse").setAttribute("href",tier.icon);
 $("#lTierName").textContent=t(tier.key)+" · "+t("league");
 const band=next?next.min-tier.min:1;
 $("#lpFill").style.width=Math.min(100,Math.round((lp-tier.min)/band*100))+"%";
 $("#lpNext").textContent=next?t("lp_next",{lp:next.min-lp,tier:t(next.key)}):t("lp_max");
 $("#lquota").textContent=t("spots",{n:quota});
 $("#lcutover").textContent=t("cutover",{n:quota});
 /* Tier rail: emblem on every rank, its weekly promotion quota, locked states kept. */
 $("#tierRail").innerHTML=TIERS.map((x,i)=>`<div class="tier${i===tix?" on":i>tix?" lock":""}">
   <i><svg><use href="${x.icon}"/></svg><svg class="temb" style="position:absolute;inset:0;margin:auto;width:11px;height:11px;opacity:${i>tix?.45:1}"><use href="${TIER_EMB[x.k]}"/></svg></i>
   <span data-i18n="${x.key}">${t(x.key)}</span>
   <em style="display:block;font-style:normal;font-size:8.5px;opacity:.72">${t("spots",{n:TIER_Q[x.k]||1})}</em></div>`).join("");
 /* Monthly rank: only which band you reached and how far you moved. The league table
    itself is never rendered. */
 const band100=Math.max(1,Math.ceil(100-(lp-200)/6));
 $("#lmTop").textContent=t("top_n",{n:band100});
 const mseed=Math.floor(Date.now()/26298e5),prevPos=Math.max(1,band100+((mseed*7)%9)-3),delta=prevPos-band100;
 $("#lmDelta").textContent=(delta>0?"+":"")+delta;
 $("#lmDelta").style.color=delta>0?"var(--green-d)":delta<0?"var(--red)":"var(--muted)";
 $("#rankLine").textContent=t(tier.key)+" · "+lp+" LP";
 $("#lprevUse").setAttribute("href",tier.icon);
 $("#lprevTier").textContent=`${t(tier.key)} ${t("league")} · ${t("top_n",{n:band100})}`;}
/* --- local-first auth --- */
let authMode="signup";
function openAuth(m){authMode=m;go("scr-auth");applyAuth();}
function applyAuth(){const s=authMode==="signup";
 $("#authTitle").textContent=t(s?"auth_signup":"auth_login");
 $("#aName").style.display=s?"":"none";$("#aPass2").style.display=s?"":"none";
 $("#aAge").parentElement.style.display=s?"":"none";
 $("#aSubmit").textContent=t(s?"btn_signup":"btn_login");
 $("#aSwitch").textContent=t(s?"sw_login":"sw_signup");$("#aErr").textContent="";}
$("#aSwitch").onclick=()=>{authMode=authMode==="signup"?"login":"signup";applyAuth();sfx("click");};
async function hash(p){try{const b=await crypto.subtle.digest("SHA-256",new TextEncoder().encode("yatla:"+p));
 return [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,"0")).join("");}catch(e){let h=5381;for(const c of p)h=((h*33)^c.charCodeAt(0))>>>0;return "d"+h;}}
$("#aSubmit").onclick=async()=>{const em=$("#aEmail").value.trim().toLowerCase(),pw=$("#aPass").value;
 const U=JSON.parse(localStorage.getItem("yatla_users")||"{}");
 const err=m=>{$("#aErr").textContent=t(m);sfx("bad");hz(40);};
 if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em))return err("err_email");
 if(pw.length<6)return err("err_pass");
 if(authMode==="signup"){
  if($("#aName").value.trim().length<2)return err("a_name");
  if($("#aPass2").value!==pw)return err("err_match");
  if(!$("#aAge").checked)return err("err_age");
  if(U[em])return err("err_exists");
  U[em]={n:$("#aName").value.trim(),h:await hash(pw)};
  localStorage.setItem("yatla_users",JSON.stringify(U));
  S.user={name:U[em].n,email:em};track("signup");sfx("good");hz([30,40,30]);confetti();
  toast(t("acc_created"));applyProfile();save();go("scr-goal");
 }else{
  if(!U[em])return err("err_nouser");
  if(U[em].h!==await hash(pw))return err("err_wrong");
  S.user={name:U[em].n,email:em};track("login");sfx("good");toast(t("wel_back"));applyProfile();save();go("scr-home");}};
document.addEventListener("click",e=>{
 const a=e.target.closest("[data-auth]");if(a){openAuth(a.dataset.auth);return;}
 if(e.target.closest("[data-soc]")){toast(t("soc_stub"));return;}
 const sp=e.target.closest(".spk2");
 if(sp){let w=null;
  if($("#sdetail").style.display!=="none"&&S.detailWord)w=S.detailWord.en;
  else if($("#scr-learning").classList.contains("on")&&S.lv.session[S.lv.idx])w=S.lv.session[S.lv.idx].en;
  else if(sp.closest(".wotd"))w="friend";
  if(w)speak(w);sfx("click");return;}
 const m=[["[data-share]","share_wotd"],["#homeCont","lesson_open"],["#chalReview","review_open"]].find(([s])=>e.target.closest(s));
 if(m)track(m[1]);
 if(e.target.closest(".btn-p"))hz(20);});
function applyProfile(){if(S.avatar)$("#pfAv").src=S.avatar;applyPremium();}
function applyPremium(){const on=!!S.premium;
 $("#pfName").innerHTML=(S.user?S.user.name:"Aria Johnson")+(on?' <svg class="vb"><use href="#i-vb"/></svg> <span style="font-size:15px">👑</span>':"");
 $("#premCard").classList.toggle("act",on);
 $("#premBtn").textContent=t(on?"prem_active":"prem_cta");
 $("#premStatus").textContent=t(on?"prem_on_status":"prem_status");
 $("#premCancel").style.display=on?"":"none";
 $("#pfPrBadge").style.display=on?"":"none";
 document.querySelector(".avatar").classList.toggle("ring",on);
 document.documentElement.classList.toggle("premium",on);
 $("#premRibbon").style.display=on?"":"none";
 $("#lesX2").style.display=on?"":"none";
 renderLeague();}
$("#premBtn").onclick=()=>{if(!S.premium){S.premium=true;confetti();sfx("good");hz([30,40,30]);toast(t("prem_toast"));track("premium_on");applyPremium();save();}else toast(t("prem_thanks"));};
$("#premCancel").onclick=()=>{S.premium=false;applyPremium();save();toast(t("prem_off"));};
/* --- avatar upload --- */
const avIn=document.createElement("input");avIn.type="file";avIn.accept="image/*";avIn.style.display="none";document.body.appendChild(avIn);
document.querySelector(".avatar .cam").addEventListener("click",()=>avIn.click());
avIn.onchange=()=>{const f=avIn.files[0];if(!f)return;const r=new FileReader();
 r.onload=()=>{S.avatar=r.result;$("#pfAv").src=S.avatar;track("avatar_set");save();};r.readAsDataURL(f);};
/* --- settings switches --- */
$("#soundSw").onclick=function(){S.sound=S.sound===false;this.classList.toggle("on",S.sound!==false);sfx("good");save();};
$("#notifSw").onclick=function(){if(!("Notification" in window)){toast(t("notif_no"));return;}
 Notification.requestPermission().then(p=>{if(p==="granted"){this.classList.add("on");toast(t("notif_on"));
  try{new Notification("Ýatla 🔥",{body:t("streak")});}catch(e){}}else toast(t("notif_no"));});};

/* ================= INIT ================= */
load();
if(S.theme==="dark")setTheme(true);
document.querySelector(".avatar img").id="pfAv";
document.querySelector('[data-i18n="analytics"]').closest(".card").insertAdjacentHTML("beforeend",'<div class="sub" id="anStats" style="margin-top:10px"></div>');
$("#soundSw").classList.toggle("on",S.sound!==false);
buildTabs();setLang(S.lang||"en");refreshHome();renderFavs();renderLearning();filt();resetLesson();renderLeague();applyProfile();track("session_start");save();

/* ================= CONTENT PACK LOAD ================= */
/* Resolution order lives in YatlaContent: embedded <script id="yatlaWords"> →
   IndexedDB → localStorage → the 12 seed WORDS above → network fetch.
   fetchWords never rejects, so a sandboxed preview with no network simply keeps
   the seed words and nothing regresses. */
YatlaContent.fetchWords({url:"content/build/yatla-words.min.json"}).then(function(r){
  if(!r.words||!r.words.length)return;
  var have={};WORDS.forEach(function(w){have[w.en.toLowerCase()]=1;});
  var added=0;
  r.words.forEach(function(w){
    if(!w||!w.en||have[w.en.toLowerCase()])return;   // seed words keep their stages
    have[w.en.toLowerCase()]=1;
    WORDS.push(w);                                   // in-place: every existing
    added++;                                         // WORDS reference stays valid
  });
  if(!added)return;
  if(S.lv&&S.lv.view==="books")renderLearning();
  if($("#scr-search").classList.contains("on"))filt();
  refreshHome();
  track("pack_loaded");
  toast(t("pack_on",{n:WORDS.length}));
  save();
});
