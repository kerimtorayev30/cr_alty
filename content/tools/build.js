#!/usr/bin/env node
/**
 * Ýatla content pipeline — builder.
 *
 * Reads every content/data/*.json envelope and emits the bundles the app ships:
 *
 *   build/yatla-words.dev.json    readable, one object per word  (dev + import tooling)
 *   build/yatla-words.min.json    compact row arrays             (what the app fetches)
 *   build/yatla-words.stats.json  per-book / per-CEFR counts, byte sizes
 *
 * Compact row format (order is fixed and shared with the loader):
 *   ["en","tm","ru","ipa","pos","def","ex","exTm","syn","coll","cefr","ox","stage","books"]
 *
 * Usage:
 *   node build.js [--data ./data] [--out ./build]
 *
 * Exits non-zero if validation failed, so `npm run build` cannot ship bad content.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const FIELDS = ['en', 'ipa', 'pos', 'tm', 'ru', 'def', 'ex', 'exTm', 'cefr', 'ox', 'syn', 'coll', 'stage', 'books'];
const OPTIONAL_STRINGS = ['syn', 'coll'];

function arg(flag, fallback) {
  const i = process.argv.indexOf(flag);
  return i !== -1 && process.argv[i + 1] ? path.resolve(process.argv[i + 1]) : fallback;
}

function row(word) {
  return FIELDS.map((f) => {
    if (word[f] === undefined) return OPTIONAL_STRINGS.includes(f) ? '—' : null;
    return word[f];
  });
}

function main() {
  const dataDir = arg('--data', path.join(__dirname, '..', 'data'));
  const outDir = arg('--out', path.join(__dirname, '..', 'build'));

  // Never emit a bundle that has not passed validation.
  execFileSync(process.execPath, [path.join(__dirname, 'validate.js'), dataDir], { stdio: 'inherit' });

  const words = [];
  // Lesson metadata. Each entry is tagged with its book so two books can both
  // have a "1A". A merged pack holds lessons from several books, so a lesson
  // that already names its book keeps it.
  const lessons = [];
  const perBook = new Map();
  const perCefr = new Map();
  let proofread = 0;

  for (const file of fs.readdirSync(dataDir).filter((f) => f.endsWith('.json')).sort()) {
    const doc = JSON.parse(fs.readFileSync(path.join(dataDir, file), 'utf8'));
    for (const l of doc.lessons || []) {
      const book = l.book || doc.book || 'unassigned';
      lessons.push(Object.assign({}, l, { book }));
    }
    for (const w of doc.words) {
      const entry = Object.assign({ _src: file }, w);
      words.push(entry);
      // A word is often taught by two books, so count it under every book that
      // teaches it; counting only books[0] understated Elementary by 173.
      const bs = (entry.books && entry.books.length)
        ? entry.books.map((b) => b.book)
        : [doc.book || 'unassigned'];
      for (const b of new Set(bs)) {
        perBook.set(b, (perBook.get(b) || 0) + 1);
      }
      perCefr.set(entry.cefr, (perCefr.get(entry.cefr) || 0) + 1);
      if (entry.proofread) proofread++;
    }
  }

  fs.mkdirSync(outDir, { recursive: true });

  const dev = { version: 1, format: 'object', fields: FIELDS, count: words.length, lessons, words };
  const min = { version: 1, format: 'array', fields: FIELDS, count: words.length, lessons, rows: words.map(row) };

  const stats = {
    generatedAt: new Date().toISOString(),
    count: words.length,
    proofread,
    needsProofread: words.length - proofread,
    perBook: Object.fromEntries([...perBook.entries()].sort()),
    perCefr: Object.fromEntries(['A1', 'A2', 'B1', 'B2', 'C1', 'C2'].filter((c) => perCefr.has(c)).map((c) => [c, perCefr.get(c)])),
    sizes: {}
  };

  const devPath = path.join(outDir, 'yatla-words.dev.json');
  const minPath = path.join(outDir, 'yatla-words.min.json');
  const statsPath = path.join(outDir, 'yatla-words.stats.json');

  fs.writeFileSync(devPath, JSON.stringify(dev, null, 2));
  fs.writeFileSync(minPath, JSON.stringify(min));

  stats.sizes['yatla-words.dev.json'] = fs.statSync(devPath).size;
  stats.sizes['yatla-words.min.json'] = fs.statSync(minPath).size;
  const kb = (n) => `${(n / 1024).toFixed(1)} KB`;
  console.log(`\nwrote ${path.relative(process.cwd(), devPath)}  ${kb(stats.sizes['yatla-words.dev.json'])}`);
  console.log(`wrote ${path.relative(process.cwd(), minPath)}  ${kb(stats.sizes['yatla-words.min.json'])}`);

  fs.writeFileSync(statsPath, JSON.stringify(stats, null, 2));
  console.log(`wrote ${path.relative(process.cwd(), statsPath)}`);
  console.log(`per book: ${JSON.stringify(stats.perBook)}`);
  console.log(`per CEFR: ${JSON.stringify(stats.perCefr)}`);
  console.log(`proofread: ${proofread}/${words.length} (${words.length - proofread} still need a native TM/RU check)`);
}

main();
