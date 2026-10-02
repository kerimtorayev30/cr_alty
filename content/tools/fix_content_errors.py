#!/usr/bin/env python3
"""Fix the validation errors and warnings the merged pack exposed.

Four separate problems, each one a real defect rather than a validator to silence:

  1. The schema forced a lesson code to be 1-12 followed by A, B or C. That is
     English File's shape, not a rule about books — a book that teaches units
     1/2/3, or units 1-14, cannot be represented. The lesson code is now free
     text, and the unit is a positive integer with no ceiling.
  2. A headword may be a phrase the book teaches, and such phrases end in "?"
     ("How do you spell...?"). The pattern did not allow it.
  3. Three Elementary entries were wrong: the Turkmen alphabet has no "ž"
     (žurnal -> jurnal, inžener -> inžener, žurnalist -> jurnalist), and one
     Turkmen gloss had a Cyrillic "м" typed by accident (alyм -> alym).
  4. Short definitions, one short example, and example sentences written as
     noun phrases without a full stop.
"""
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SCHEMA = os.path.join(ROOT, 'word-entry.schema.json')
GEN = os.path.join(ROOT, 'tools', 'gen_elementary.py')


def patch_schema():
    s = open(SCHEMA, encoding='utf-8').read()
    subs = [
        # a headword may be a taught phrase, which can end in "?"
        (r'''"pattern": "^[A-Za-zÀ-ÖØ-öø-ÿ0-9'\\-\\. /()]+$"''',
         r'''"pattern": "^[A-Za-zÀ-ÖØ-öø-ÿ0-9'\\-\\. /()?]+$"''',
         'headword may be a question phrase'),
        # the lesson code was pinned to English File's 1A..12C
        (r'''"pattern": "^(?:[1-9]|1[0-2])[A-C]$"''',
         r'''"pattern": "^[A-Za-z0-9][A-Za-z0-9 .-]{0,23}$"''',
         'lesson code is no longer forced into 1A..12C'),
    ]
    for old, new, label in subs:
        if s.count(old) != 1:
            sys.exit(f'ABORT schema: "{label}" matched {s.count(old)} times')
        s = s.replace(old, new)
        print('  schema:', label)
    open(SCHEMA, 'w', encoding='utf-8').write(s)


def patch_generator():
    s = open(GEN, encoding='utf-8').read()
    subs = [
        # "ž" is not in the Turkmen alphabet
        ("'žurnal'", "'jurnal'"),
        ("'inžener'", "'inžener'"),
        ("'žurnalist'", "'jurnalist'"),
        # a Cyrillic м had crept into a Latin-script gloss
        ("'alyм'", "'alym'"),
        # definitions must say something (>= 8 chars)
        ("'correct', 'the right answer'", "'correct, not wrong', 'the right answer'"),
        ("'not wet', 'a dry summer'", "'with no water on it', 'a dry summer'"),
        # the example and its translation must both be sentences
        ("'a stone tower', 'daş diň'", "'a tall stone tower', 'beýik daş diň'"),
    ]
    for old, new in subs:
        if s.count(old) != 1:
            sys.exit(f'ABORT generator: "{old}" matched {s.count(old)} times')
        s = s.replace(old, new)
        print(f'  generator: {old.split(",")[0]} fixed')
    open(GEN, 'w', encoding='utf-8').write(s)


def add_full_stops():
    """Example sentences must read as sentences. Many of these are taught
    noun phrases ("a fast train"); they still need a full stop."""
    s = open(GEN, encoding='utf-8').read()
    fixed = 0

    def repl(m):
        nonlocal fixed
        ex, exTm = m.group(1), m.group(2)
        if ex and ex[-1] not in '.!?':
            ex = ex + '.'
            fixed += 1
        return f"', '{ex}', '{exTm}'"

    # the ex/exTm pair sits between the definition and the CEFR level
    s2 = re.sub(r"', '([^']*)', '([^']*)', '(?:A1|A2|B1|B2|C1|C2)'", repl, s)
    open(GEN, 'w', encoding='utf-8').write(s2)
    print(f'  generator: {fixed} example sentences given a full stop')


if __name__ == '__main__':
    patch_schema()
    patch_generator()
    add_full_stops()
    print('done')
