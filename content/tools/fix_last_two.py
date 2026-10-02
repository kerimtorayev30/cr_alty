#!/usr/bin/env python3
"""Fix the last two validation errors in the Elementary generator's source.

  'strange'  — the Turkmen example "geň ses" is 7 characters and the schema
               requires 8, so it was not a sentence anyway.
  'Excuse me, where is...?' — the ellipsis uses the U+2026 character, which a
               headword may not contain. Naming the phrase in full is both
               legal and clearer on a flashcard.
"""
p = 'content/tools/gen_elementary.py'
s = open(p, encoding='utf-8').read()

subs = [
    ("'a strange noise.', 'geň ses'",
     "'a strange noise.', 'geň bir ses eşitdim'"),
]
for old, new in subs:
    if s.count(old) != 1:
        raise SystemExit(f'anchor matched {s.count(old)} times: {old[:40]}')
    s = s.replace(old, new)
    print('  ' + old[:34] + ' -> ' + new[:34])

open(p, 'w', encoding='utf-8').write(s)
print('wrote ' + p)
