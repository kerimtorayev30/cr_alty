#!/usr/bin/env python3
"""Drop the three rows that duplicate a headword taught earlier in the book.

  'suddenly'  is taught in 10A (common adverbs); 7A's story list repeats it
  'abroad'    is taught in 9B (city holidays); 11B's travel list repeats it
  'check in'  is taught in PE1 (a hotel); PE6's airport list repeats it
"""
p = 'content/tools/gen_elementary.py'
lines = open(p, encoding='utf-8').read().split('\n')

targets = {
    "'quickly and without warning'": 'suddenly (kept in 10A)',
    "'in another country', 'He works abroad.'": 'abroad (kept in 9B)',
    "'to give your bags and get a seat at an airport'": 'check in (kept in PE1)',
}

out = []
dropped = []
for line in lines:
    hit = next((v for k, v in targets.items() if k in line), None)
    if hit:
        dropped.append(hit)
        continue
    out.append(line)

if len(dropped) != len(targets):
    raise SystemExit(f'expected {len(targets)} rows to drop, found {len(dropped)}: {dropped}')

open(p, 'w', encoding='utf-8').write('\n'.join(out))
print('dropped ' + str(len(dropped)) + ' duplicate rows: ' + ', '.join(dropped))
