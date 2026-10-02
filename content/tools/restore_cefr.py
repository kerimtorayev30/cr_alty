#!/usr/bin/env python3
"""Restore the CEFR level on the generator's data rows.

fix_content_errors.py's add_full_stops() replaced a matched span without putting
back the CEFR field it had matched, so rows in content/tools/gen_elementary.py
lost their level and the generator stopped with
"not enough values to unpack (expected 9, got 8)".

The levels are known: the adjective topics used A1 for the common pairs and A2
for the less common ones; every other topic was written entirely at A1.

Each row is parsed with ast.literal_eval instead of a hand-written splitter.
Three attempts at splitting a row by hand each failed differently (a regex that
matched nothing, a separator split that mis-counted a row quoting its example in
double quotes, then a character walker that collapsed a row to one field). The
rows are Python tuple literals, so let Python parse them.
"""
import ast
import sys

GEN = 'content/tools/gen_elementary.py'
START = "    ('"
END = "'),"
END_DQ = "),"          # rows whose last field is double-quoted

ADJ_A2 = {
    'clean', 'difficult', 'slow', 'empty', 'high', 'low', 'light (weight)', 'heavy',
    'rich', 'poor', 'dangerous', 'weak', 'the same', 'quite', 'bigger', 'smaller',
    'older', 'younger', 'worse', 'more expensive', 'cheaper', 'as big as',
    'not as good as', 'the biggest', 'the smallest', 'the oldest', 'the worst',
    'the most beautiful', 'the most dangerous',
}


def level_for(fields):
    """The level a row should have, from its part of speech and headword."""
    return 'A2' if (fields[2] == 'ADJ' and fields[0] in ADJ_A2) else 'A1'


src = open(GEN, encoding='utf-8').read()
lines = src.split('\n')
out = []
topic = None
fixed = {'A1': 0, 'A2': 0}
seen = 0

for line in lines:
    if line.startswith("T['") and line.endswith("] = ["):
        topic = line[3:line.index("'] = [")]
        out.append(line)
        continue

    if line.startswith('    (') and (line.endswith(END) or line.endswith(END_DQ)):
        literal = line.strip()
        if literal.endswith(','):
            literal = literal[:-1]
        try:
            fields = list(ast.literal_eval(literal))
        except (ValueError, SyntaxError) as e:
            sys.exit('cannot parse a row in ' + str(topic) + ': ' + e
                     + '\n  ' + line.strip()[:100])
        if not all(isinstance(f, str) for f in fields):
            sys.exit('a row in ' + str(topic) + ' has a non-string field')
        seen += 1
        if len(fields) == 8:                     # en ipa pos tm ru def ex exTm
            level = level_for(fields)
            # keep whatever trailed the row: every list entry ends in a comma and
            # dropping it turns the next row into a call on this tuple
            trail = ',' if line.rstrip().endswith(',') else ''
            line = line[:line.rindex(')')] + ", '" + level + "')" + trail
            fixed[level] += 1
        elif len(fields) not in (9, 10):
            sys.exit('unexpected field count ' + str(len(fields)) + ' in ' + str(topic)
                     + ': ' + line.strip()[:100])
    out.append(line)

if seen == 0:
    sys.exit('ABORT: no data rows recognised — the file shape has changed')

open(GEN, 'w', encoding='utf-8').write('\n'.join(out))
print('checked ' + str(seen) + ' data rows, restored the CEFR level on '
      + str(sum(fixed.values())) + ' (' + str(fixed['A1']) + ' as A1, '
      + str(fixed['A2']) + ' as A2)')
