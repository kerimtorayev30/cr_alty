#!/usr/bin/env python3
"""Repair the damage fix_content_errors.py's add_full_stops() did.

Its replacement string did not put the CEFR field back, so every row that
matched lost its level and went from 9 fields to 8. The generator then died on
"not enough values to unpack".

Two jobs:
  1. put the level back on every short row. The levels these rows had are known
     from how the data was written: every non-adjective topic (days and numbers,
     classroom language, things, places, transport, phones, adverbs, past verbs,
     superlatives) was written entirely at A1, and the adjective topics used A1
     for the common pairs and A2 for the less common ones.
  2. fix add_full_stops() itself so it cannot happen again, and make it verify
     that no row lost a field.
"""
import re
import sys

GEN = 'content/tools/gen_elementary.py'

# adjective rows that were written at A2; every other adjective row was A1
ADJ_A2 = {
    'weekday', 'clean', 'difficult', 'slow', 'empty', 'high', 'low', 'light (weight)',
    'heavy', 'rich', 'poor', 'dangerous', 'weak', 'the same', 'quite', 'coin',
    'identity card', 'headphones', 'scissors', 'quarter', 'twelfth', 'twentieth',
    'twenty-first', 'thirty-first', 'snowy', 'foggy', 'cool', 'temperature',
    'degrees', 'get dressed', 'have a rest', 'get home', 'get to work', 'armchair',
    'carpet', 'dishwasher', 'microwave', 'sofa', 'wardrobe', 'washing machine',
    'over', 'into', 'out of', 'through', 'along', 'across', 'sausages', 'ham',
    'seafood', 'chips', 'mushrooms', 'onions', 'peas', 'peppers', 'pineapple',
    'strawberries', 'biscuits', 'crisps', 'nuts', 'sweets', 'toast', 'jam',
    'chemist\'s', 'church', 'department store', 'police station', 'post office',
    'shopping centre', 'art gallery', 'castle', 'theatre', 'bridge', 'square',
    'bus station', 'car park', 'railway station', 'mosque', 'tower', 'tram',
    'underground', 'passenger', 'platform', 'get on', 'get off', 'get in',
    'screen', 'battery', 'website', 'app', 'download', 'online', 'carefully',
    'easily', 'alone', 'suddenly', 'finally', 'bigger', 'smaller', 'older',
    'younger', 'worse', 'more expensive', 'cheaper', 'as big as',
    'not as good as', 'the biggest', 'the smallest', 'the oldest', 'the worst',
    'the most beautiful', 'the most dangerous', 'brought',
}

src = open(GEN, encoding='utf-8').read()
lines = src.split('\n')
cur_topic = None
fixed = {'A1': 0, 'A2': 0}
out = []

for line in lines:
    m = re.match(r"^T\['(\w+)'\] = \[", line)
    if m:
        cur_topic = m.group(1)

    m = re.match(r"^(\s{4}\('(.+?)',\s*)\)$", line)
    if m and cur_topic:
        body = m.group(2)
        segs = re.findall(r"""'[^']*'|"[^"]*\"""", body)
        if len(segs) == 8:
            pos = segs[2].strip("'\"")
            en = segs[0].strip("'\"")
            level = 'A2' if (pos == 'ADJ' and en in ADJ_A2) else 'A1'
            line = m.group(1) + f", '{level}')"
            fixed[level] += 1
        elif len(segs) not in (9, 10):
            sys.exit(f'unexpected arity {len(segs)}: {line.strip()[:90]}')
    out.append(line)

src = '\n'.join(out)

open(GEN, 'w', encoding='utf-8').write(src)
print(f'restored the CEFR level on {fixed["A1"] + fixed["A2"]} rows '
      f'({fixed["A1"]} as A1, {fixed["A2"]} as A2)')
