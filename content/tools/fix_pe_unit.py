#!/usr/bin/env python3
"""Put the six Practical English episodes in their own unit.

They were written with unit numbers 1-6 (their episode numbers), which scattered
PE1..PE6 across units 1-6. All six belong to the Practical English unit, 13.
"""
p = 'content/tools/gen_elementary.py'
s = open(p, encoding='utf-8').read()

subs = [
    ("('PE1', 1, 'Arriving in London'", "('PE1', 13, 'Arriving in London'"),
    ("('PE2', 2, 'Coffee to take away'", "('PE2', 13, 'Coffee to take away'"),
    ("('PE3', 3, 'In a clothes shop'", "('PE3', 13, 'In a clothes shop'"),
    ("('PE4', 4, 'Getting lost'", "('PE4', 13, 'Getting lost'"),
    ("('PE5', 5, 'At a restaurant'", "('PE5', 13, 'At a restaurant'"),
    ("('PE6', 6, 'Going home'", "('PE6', 13, 'Going home'"),
]
for old, new in subs:
    if s.count(old) != 1:
        raise SystemExit(f'anchor matched {s.count(old)} times: {old}')
    s = s.replace(old, new)

s = s.replace("for code, n, title, topic, key in (",
              "PE_UNIT = 13\nfor code, n, title, topic, key in (")
s = s.replace("    LESSONS[code] = (n, title, topic, [key])",
              "    LESSONS[code] = (PE_UNIT, title, topic, [key])")

open(p, 'w', encoding='utf-8').write(s)
print('all six Practical English episodes moved to unit ' + str(13))
