#!/usr/bin/env python3
"""Undo the field shift in the generator's own source.

A row is written as (en, ipa, pos, tm, ru, def, ex, exTm, cefr[, coll]). The
faulty add_full_stops() matched "..., 'exTm', 'A1'" and replaced it without
putting the level back, so on rows that also carried a collocation the level
vanished and the collocation slid into its place — the generator then emitted
cefr: "by bus".

Fixing the emitted JSON is not enough: gen_elementary.py rewrites that file, so
the shift has to go from the source rows. A shifted row is recognisable as a
9-field row whose last field is not a CEFR level.
"""
import ast
import sys

GEN = 'content/tools/gen_elementary.py'
LEVELS = {'A1', 'A2', 'B1', 'B2', 'C1', 'C2'}

ADJ_A2 = {
    'clean', 'difficult', 'slow', 'empty', 'high', 'low', 'light (weight)', 'heavy',
    'rich', 'poor', 'dangerous', 'weak', 'the same', 'quite', 'bigger', 'smaller',
    'older', 'younger', 'worse', 'more expensive', 'cheaper', 'as big as',
    'not as good as', 'the biggest', 'the smallest', 'the oldest', 'the worst',
    'the most beautiful', 'the most dangerous',
}

lines = open(GEN, encoding='utf-8').read().split('\n')
out = []
fixed = 0
topic = None

for line in lines:
    if line.startswith("T['") and line.endswith("] = ["):
        topic = line[3:line.index("'] = [")]
        out.append(line)
        continue

    if line.startswith('    (') and line.rstrip().endswith('),'):
        literal = line.strip()[:-1]
        try:
            fields = list(ast.literal_eval(literal))
        except (ValueError, SyntaxError):
            out.append(line)
            continue
        if (len(fields) == 9 and all(isinstance(f, str) for f in fields)
                and fields[8] not in LEVELS):
            coll = fields[8]
            level = 'A2' if (fields[2] == 'ADJ' and fields[0] in ADJ_A2) else 'A1'
            # rebuild the row: the collocation goes back to the end
            parts = ["'" + f.replace("'", "\\'") + "'" for f in fields[:8]]
            parts.append("'" + level + "'")
            parts.append("'" + coll.replace("'", "\\'") + "'")
            line = '    (' + ', '.join(parts) + '),'
            fixed += 1
    out.append(line)

if fixed == 0:
    sys.exit('nothing to fix in the source — already repaired?')

open(GEN, 'w', encoding='utf-8').write('\n'.join(out))
print('unshifted ' + str(fixed) + ' rows in ' + GEN)
