#!/usr/bin/env python3
"""Take the remaining English File assumptions out of the validator and schema.

The owner's point was that the unit system differs from book to book, and the
validator still enforced English File's shape in three places:

  1. a lesson code had to end in A, B or C — so Practical English's PE1..PE6 were
     rejected outright;
  2. the number inside a lesson code had to equal the unit — so PE1, which lives
     in the Practical English unit, was rejected for not being unit 1;
  3. the schema capped a unit at 12 — no book could ever have a thirteenth unit.

What stays is the check that actually matters: a word's unit must be a positive
number, and a lesson code must not be empty.
"""
import json
import sys

V = 'content/tools/validate.js'
S = 'content/word-entry.schema.json'

s = open(V, encoding='utf-8').read()
old = """      (w.books || []).forEach((b, bi) => {
        if (b.lesson) {
          const num = parseInt(b.lesson, 10);
          const letter = b.lesson.replace(/^[0-9]+/, '');
          if (!/^[A-C]$/.test(letter)) {
            errors.push(`${where}: books[${bi}].lesson "${b.lesson}" must end in A, B or C`);
          }
          if (num !== b.unit) {
            errors.push(`${where}: books[${bi}].lesson "${b.lesson}" does not belong to unit ${b.unit}`);
          }
        }
      });"""
new = """      (w.books || []).forEach((b, bi) => {
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
      });"""
if s.count(old) != 1:
    sys.exit(f'ABORT: validator anchor matched {s.count(old)}')
s = s.replace(old, new)
open(V, 'w', encoding='utf-8').write(s)
print('validator: no A/B/C and no lesson-in-unit assumption')

d = json.load(open(S, encoding='utf-8'))
unit = d['properties']['books']['items']['properties']['unit']
if unit.get('maximum') != 12:
    sys.exit(f'ABORT: expected unit maximum 12, found {unit.get("maximum")}')
del unit['maximum']
unit['description'] = ('The unit this book teaches the word in. Positive whole '
                       'number; there is no ceiling, because not every book has '
                       'twelve units.')
with open(S, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('schema: unit has no ceiling')
