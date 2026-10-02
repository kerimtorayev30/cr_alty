#!/usr/bin/env python3
"""Let a taught phrase use a comma in its headword.

"Excuse me, where is the station" is a phrase the book teaches as a unit, and a
comma is ordinary punctuation in one. The headword pattern allowed letters,
digits, spaces, apostrophes, hyphens, dots, slashes, parentheses and question
marks — but not the comma, so the phrase was rejected as invalid.

The pattern is built from characters rather than written as a literal, because
it contains quotes that keep breaking any script that embeds it.
"""
import json
import sys

S = 'content/word-entry.schema.json'
doc = json.load(open(S, encoding='utf-8'))
node = doc['properties']['en']

pat = node.get('pattern', '')
if ',' in pat:
    sys.exit('the headword pattern already allows a comma')
if ']+$' not in pat:
    sys.exit('unexpected pattern shape: ' + pat)

node['pattern'] = pat.replace(']+$', ',]+$')
node['description'] = ('The English headword, or a phrase the book teaches as a '
                       'unit ("turn left", "Excuse me, where is the station").')

with open(S, 'w', encoding='utf-8') as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('headword pattern now: ' + node['pattern'])
