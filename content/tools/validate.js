#!/usr/bin/env node
/**
 * Ýatla content pipeline — validator.
 *
 * Usage:
 *   node validate.js [dir]        # default dir: ./data
 *
 * Exit codes:
 *   0  all files valid
 *   1  schema errors or hard errors (see "error:" lines)
 *   2  bad CLI usage / unreadable input
 *
 * Checks
 *   1. JSON parses.
 *   2. Envelope shape: { book, title?, words: [...] }.
 *   3. Every word validates against word-entry.schema.json (ajv, draft 2020-12, strict).
 *   4. Cross-file: `en` headwords are globally unique (case-insensitive).
 *   5. Script guards: `tm` must be Latin (no Cyrillic), `ru` must contain Cyrillic.
 *   6. IPA sanity: no uppercase Latin letters, no stray punctuation.
 *   7. `en` headwords are unique within a file (a file must not contradict itself).
 *
 * Warnings do not fail the build; they are reported as "warn:" and summarised.
 */
'use strict';

const fs = require('fs');
const path = require('path');
// Draft 2020-12 support lives in the /dist/2020 entry point of the same ajv package.
const Ajv = require('ajv/dist/2020');

const SCHEMA_PATH = path.join(__dirname, '..', 'word-entry.schema.json');

const CYRILLIC = /[\u0400-\u04FF]/;
// The ids app-yatla.html uses for its bk_* i18n keys. intp/advp were missing,
// so an envelope for either Plus book was rejected as invalid.
const BOOK_IDS = ['beg', 'ele', 'pre', 'int', 'upp', 'adv', 'intp', 'advp'];
// tools/merge_packs.py writes one envelope holding every book, because a word
// taught by two books must exist exactly once. Its words name their own books.
const MERGED = 'all';
// Letters, digits and the punctuation a gloss realistically uses. This guard
// exists to catch the wrong *script* (e.g. Cyrillic leaking in), not to police
// punctuation, so "/" and parentheses belong here.
const TM_ALLOWED = /^[\sA-Za-zÀ-ÖØ-öø-ÿÝýÄäŇňÖöÜüÇçŞş0-9'’.,;:!?\-()«»"/]+$/;

function loadSchema() {
  const ajv = new Ajv({ strict: true, allErrors: true });
  return ajv.compile(JSON.parse(fs.readFileSync(SCHEMA_PATH, 'utf8')));
}

function readWordFiles(dir) {
  if (!fs.existsSync(dir)) {
    console.error(`error: data directory not found: ${dir}`);
    process.exit(2);
  }
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith('.json'))
    .sort()
    .map((f) => path.join(dir, f));
}

function main() {
  const dir = path.resolve(process.argv[2] || path.join(__dirname, '..', 'data'));
  const validateWord = loadSchema();
  const files = readWordFiles(dir);

  if (files.length === 0) {
    console.error(`error: no .json word files in ${dir}`);
    process.exit(2);
  }

  const errors = [];
  const warnings = [];
  const seen = new Map(); // lowercase headword -> file
  let total = 0;
  let proofread = 0;
  const perFile = [];

  for (const file of files) {
    const rel = path.relative(path.resolve(__dirname, '..'), file);
    let raw;
    try {
      raw = fs.readFileSync(file, 'utf8');
    } catch (e) {
      errors.push(`${rel}: unreadable (${e.message})`);
      continue;
    }

    let doc;
    try {
      doc = JSON.parse(raw);
    } catch (e) {
      errors.push(`${rel}: invalid JSON — ${e.message}`);
      continue;
    }

    if (typeof doc !== 'object' || doc === null || !Array.isArray(doc.words)) {
      errors.push(`${rel}: envelope must be { "book": "...", "words": [ ... ] }`);
      continue;
    }
    if (typeof doc.book !== 'string' || doc.book.length === 0) {
      errors.push(`${rel}: envelope is missing a non-empty "book" field`);
    } else if (doc.book !== MERGED && !BOOK_IDS.includes(doc.book)) {
      errors.push(`${rel}: envelope "book" is "${doc.book}" — must be one of ${BOOK_IDS.join(', ')} (the ids app-yatla.html uses for its bk_* i18n keys)`);
    }

    const inFile = new Set();
    let n = 0;

    doc.words.forEach((w, i) => {
      const where = `${rel} → words[${i}]${w && w.en ? ` (${w.en})` : ''}`;
      n++;

      // Schema errors are reported but must NOT abort the semantic checks below:
      // a word can fail the schema (e.g. bad cefr) and still carry a duplicate
      // headword or Cyrillic in its Turkmen field, both of which must surface too.
      if (!validateWord(w)) {
        for (const err of validateWord.errors) {
          const at = err.instancePath ? `${err.instancePath} ` : '';
          errors.push(`${where}: schema ${at}${err.message}`);
        }
      }

      const str = (v) => (typeof v === 'string' ? v : '');

      // global uniqueness of the headword
      if (typeof w.en === 'string' && w.en.trim().length) {
        const key = w.en.trim().toLowerCase();
        if (seen.has(key)) {
          errors.push(`${where}: duplicate headword "${w.en}" — already defined in ${seen.get(key)}`);
        } else {
          seen.set(key, rel);
        }
        if (inFile.has(key)) {
          errors.push(`${where}: headword "${w.en}" appears twice in the same file`);
        }
        inFile.add(key);
      }

      // script guards
      if (CYRILLIC.test(str(w.tm))) {
        errors.push(`${where}: "tm" contains Cyrillic — Turkmen uses the Latin alphabet`);
      }
      if (str(w.tm) && !TM_ALLOWED.test(w.tm)) {
        warnings.push(`${where}: "tm" uses a character outside the expected Turkmen set: ${JSON.stringify(w.tm)}`);
      }
      if (typeof w.ru === 'string' && w.ru.length && !CYRILLIC.test(w.ru)) {
        errors.push(`${where}: "ru" contains no Cyrillic`);
      }
      if (CYRILLIC.test(str(w.en))) {
        errors.push(`${where}: "en" contains Cyrillic`);
      }

      // IPA sanity
      if (/[A-Z]/.test(str(w.ipa))) {
        errors.push(`${where}: "ipa" contains an uppercase Latin letter: ${w.ipa}`);
      }
      if (/[;:,!?]/.test(str(w.ipa))) {
        warnings.push(`${where}: "ipa" contains punctuation that is not IPA: ${w.ipa}`);
      }

      // content quality
      if (str(w.ex) && !/[.!?]$/.test(w.ex.trim())) {
        warnings.push(`${where}: "ex" does not end with sentence punctuation`);
      }
      if (str(w.syn) === '' ) {
        warnings.push(`${where}: "syn" is empty — use "—" for none, as the demo data does`);
      }
      if ('exTm' in w && (!w.exTm || w.exTm.trim().length === 0)) {
        errors.push(`${where}: "exTm" is empty — every card needs a Turkmen example`);
      }
      (w.books || []).forEach((b, bi) => {
        // No shape is assumed here. English File numbers its lessons 1A/1B/1C,
        // but its Practical English episodes are PE1-PE6 inside their own unit,
        // and another book may number units differently altogether. A lesson
        // code's relationship to its unit is the book's business, not the
        // schema's.
        if ('lesson' in b && typeof b.lesson !== 'string') {
          errors.push(`${where}: books[${bi}].lesson must be a string`);
        }
        if (typeof b.unit !== 'number' || b.unit < 1 || !Number.isInteger(b.unit)) {
          errors.push(`${where}: books[${bi}].unit "${b.unit}" must be a positive whole number`);
        }
      });
      if (!w.books || w.books.length === 0) {
        warnings.push(`${where}: no "books" mapping — the word will not appear in any unit`);
      }
      if (w.cefr === 'A1' && str(w.def).length > 160) {
        warnings.push(`${where}: A1 definition is long (${w.def.length} chars) — simplify for beginners`);
      }
      if (w.proofread === true) proofread++;
    });

    total += n;
    perFile.push({ rel, n });
  }

  for (const f of perFile) console.log(`  ${f.rel}: ${f.n} words`);
  console.log(`  TOTAL: ${total} words in ${perFile.length} files`);
  console.log(`  proofread (native-checked): ${proofread}/${total}`);

  for (const w of warnings) console.log(`warn: ${w}`);
  for (const e of errors) console.error(`error: ${e}`);

  if (errors.length) {
    console.error(`\nFAIL — ${errors.length} error(s), ${warnings.length} warning(s).`);
    process.exit(1);
  }
  console.log(`\nOK — ${total} words valid, ${warnings.length} warning(s).`);
}

main();
