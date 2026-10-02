#!/usr/bin/env python3
"""Give the remaining example sentences a full stop, in the generator's source.

Thirty-seven rows teach a noun phrase as their example ("a leather jacket",
"an espresso, please"). They are still sentences on a flashcard and need their
punctuation. Editing the emitted JSON is pointless — gen_elementary.py rewrites
it — so the source rows change.

The earlier version of this job replaced a matched span and forgot to put the
CEFR field back, which silently destroyed 371 rows. This one rewrites only the
inside of the two quotes it matched, leaves the level alone, and checks
afterwards that the level count did not move.
"""
import re
import sys

GEN = 'content/tools/gen_elementary.py'
LEVELS = ('A1', 'A2', 'B1', 'B2', 'C1', 'C2')

s = open(GEN, encoding='utf-8').read()
before = sum(s.count("'" + lv + "'") for lv in LEVELS)

# ex and exTm are the last two single-quoted fields before the CEFR level
pat = re.compile(r"', '([^']*)', '([^']*)', '(" + '|'.join(LEVELS) + r")'")
fixed = [0]


def repl(m):
    ex, exTm, lv = m.group(1), m.group(2), m.group(3)
    if ex and ex[-1] not in '.!?':
        ex += '.'
        fixed[0] += 1
    return "', '" + ex + "', '" + exTm + "', '" + lv + "'"


s = pat.sub(repl, s)
after = sum(s.count("'" + lv + "'") for lv in LEVELS)
if after < before:
    sys.exit(f'ABORT: CEFR levels fell from {before} to {after}')

# the three outright errors
subs = [
    # "?" is not allowed in a headword, and the phrase reads better without it
    ("'Excuse me, where is...?'", "'Excuse me, where is'"),
    ("'used to ask a stranger for a place', 'Excuse me, where is the station?', 'Bagyşlaň, menzil nirede?', 'A1'",
     "'used to ask a stranger where a place is', 'Excuse me, where is the station?', 'Bagyşlaň, menzil nirede?', 'A1'"),
    # a definition must say something (>= 8 chars)
    ("'a taxi', 'I called a cab.'", "'another word for a taxi', 'I called a cab.'"),
]
for old, new in subs:
    if s.count(old) != 1:
        sys.exit(f'ABORT: matched {s.count(old)} times: {old[:50]}')
    s = s.replace(old, new)

open(GEN, 'w', encoding='utf-8').write(s)
print('added a full stop to ' + str(fixed[0]) + ' example sentences')
print('CEFR levels before ' + str(before) + ', after ' + str(after))
