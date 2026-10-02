# Ýatla content pipeline

Turns the 12 hard-coded demo `WORDS[]` entries into a buildable, validated, loadable
content pack — the "content scale" item from `prompt.html` §6.1.

**Status: wired into `app-yatla.html` and verified.** `INTEGRATION.md` records what the
patch does; `../HANDOFF-STATUS.md` records the session. Run `../verify.sh` from the
workspace root to re-check everything.

## Layout

```
content/
├── word-entry.schema.json     JSON Schema (draft 2020-12) for one word entry
├── data/                      source of truth, hand-authored, one file per book/batch
│   ├── ef1.json               20 words   (English File Beginner/Elementary)
│   ├── ef2.json               20 words   (Elementary — nouns & daily life)
│   ├── ef2b.json              10 words   (Elementary — verbs)
│   ├── ef3.json               10 words   (Pre-intermediate)
│   └── ef4.json               10 words   (Intermediate)
├── tools/
│   ├── validate.js            schema + semantic checks, exit 1 on any error
│   ├── build.js               runs validate, emits build/*.json
│   └── test-loader.js         jsdom suite for the loader (8 tests / 36 assertions)
├── loader/
│   └── yatla-content.js       the drop-in loader (browser + jsdom safe, no app globals)
├── build/                     generated — do not hand-edit
│   ├── yatla-words.dev.json   readable objects          (45.3 KB)
│   ├── yatla-words.min.json   compact row arrays        (20.3 KB — what the app ships)
│   └── yatla-words.stats.json per-book / per-CEFR counts and byte sizes
└── package.json               ajv + jsdom are devDependencies only
```

## Commands

```bash
cd content
npm install          # once — ajv, jsdom (node_modules is not committed)
npm run validate     # fail fast on bad content
npm run build        # validate + emit build/*.json
npm test             # build + jsdom loader suite
npm run check        # node --check on every script, then npm test
```

## Word fields

Identical to the object shape already in `app-yatla.html`, plus four optional pipeline
fields. Required: `en tm ru ipa pos def ex exTm cefr ox stage syn coll`.
Optional: `exRu books proofread tags`.

These are the app's real render formats — the schema enforces them because the app
prints several of them verbatim:

- `pos` — UPPERCASE: `N V ADJ ADV PREP CONJ PRON DET INTJ PHR` (printed next to the IPA)
- `stage` — one of `New Learning Practicing Remembered Mastered`. Anything else breaks
  the chip: the app does `STAGE_C[w.stage]` for the colour and `t(STAGE_K[w.stage])`
  for the label. New content should enter at `New`.
- `ox` — `"Oxford 3000"`, `"Oxford 5000"` or `"Academic"` (printed on the detail card)
- `syn`, `coll` — comma-separated **strings**, not arrays; use `"—"` for none
- `ipa` — slash-wrapped, e.g. `"/həˈləʊ/"`
- `def` — learner-friendly, lowercase start, no trailing full stop (matches demo data)
- `books` — `[{ "book": "beg", "unit": 3, "page": 42 }]`, using the app's book ids
  `beg / ele / pre / int / upp / adv` (these drive the `bk_*` i18n keys)
- `proofread` — flip to `true` only after a native TM/RU speaker has checked
  `tm`, `ru` and `exTm`. The validator prints the outstanding count.

## What the validator enforces

Hard errors (exit 1): unparseable JSON; bad envelope; an envelope `book` outside
`beg/ele/pre/int/upp/adv`; any schema violation; duplicate headword (checked
**globally across files**, case-insensitive); Cyrillic characters in `tm` (Turkmen is
Latin script); a `ru` value with no Cyrillic; Cyrillic in `en`; uppercase Latin letters
in `ipa`; an empty `exTm`.

Warnings (do not fail the build): characters outside the expected Turkmen set;
non-IPA punctuation in `ipa`; `ex` missing terminal punctuation; an empty `syn`; a word
with no `books` mapping; an A1 definition longer than 160 characters.

Schema errors never suppress the semantic checks — a word with a bad `cefr` still gets
its duplicate-headword and script checks run. That ordering is covered by a negative
fixture; see `../HANDOFF-STATUS.md`.

Schema errors never suppress the semantic checks — a word with a bad `cefr` still gets
its duplicate-headword and script checks run. That ordering is covered by the negative
test in `../HANDOFF-STATUS.md` §"validator negative test".

## Scaling to 2,500–3,500 words

The 70 words here are a **pipeline proof, not a word list**. To reach launch volume:

1. Author one `data/*.json` per book (or per 200-word batch — file size does not
   matter, the builder concatenates). Use the app's book ids in `books[].book`.
2. Keep `en` unique. The validator stops the build on a collision, so parallel
   contributors cannot silently duplicate a headword.
3. Run `npm run build`; check `build/yatla-words.stats.json` for per-CEFR balance.
   At the current density (≈290 bytes/word compact) 3,500 words ≈ **1.0 MB**, which
   is fine to fetch once and cache, and fine to shard later by book if you prefer.
4. Nothing in the app changes as the pack grows — `YatlaContent.fetchWords()` is the
   only read path.

## Proofreading (owner task)

All 70 seed entries are `"proofread": false`. The TM/RU strings were written to be
plausible, not authoritative — they need a native check before launch, which
`prompt.html` §6 already lists as an owner task. The validator's `proofread: 0/70`
line is your progress counter.
