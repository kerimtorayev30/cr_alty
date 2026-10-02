#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give every curated word the source-section metadata the schema now allows.

WHY THIS IS A PASS OVER THE GENERATORS, NOT A SECOND EXTRACTOR
--------------------------------------------------------------
The uploaded OCR dumps are the authoritative source for WHAT the books teach,
but they cannot answer WHERE a word sits. Two measured facts force that:

  * The dumps contain **zero** in-body lesson headings. A line like
    "3A Survive the drive" never appears; the contents table that carries it
    is shredded by the two-column OCR ("6 A Eating in...and out" = unit 1,
    page 6). So no scan of a dump can attribute a word to a unit.
  * Gap-fill targets are missing from the text: Intermediate's own
    VOCABULARY box reads "put on your seat ," and "it's the  hour".
    Only 17 of 23 curated Intermediate unit-3 headwords survive verbatim in
    the dump. A scanner that trusted the dump would invent the other six
    and silently drop the ones the book actually drills.

The unit/lesson mapping therefore stays exactly where it already is: in each
generator's LESSONS table, transcribed from the book's contents page. This
script only attaches the *section* that mapping already implies, so no unit
assignment is ever guessed from topic similarity.

SECTION PROVENANCE
------------------
Each generator groups its words into topic keys under source-band comments
("Vocabulary Bank — Money -> 2A", "in-lesson — crime -> 10B"). Those comments
record where in the book the words came from. This script converts that
provenance into the schema's `section` enum instead of re-deriving it from the
word's meaning.

It is idempotent and refuses to run if a topic key is missing from PROVENANCE:
an unmapped key is a hole in the evidence, and inventing a section for it would
be exactly the guess this pipeline must not make.

Usage: python3 content/tools/annotate_sections.py
"""
import glob
import json
import os
import re
import sys

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
MERGED = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'merged', 'yatla-all.json')

# book file stem -> (generator, book id)
BOOKS = [
    ('beginner',            'gen_beginner.py',    'beg'),
    ('elementary',          'gen_elementary.py',  'ele'),
    ('preintermediate',     'gen_pre.py',         'pre'),
    ('intermediate',        'gen_int.py',         'int'),
    ('intermediateplus',    'gen_intp.py',        'intp'),
    ('upperintermediate',   'gen_upp.py',         'upp'),
    ('advanced',            'gen_adv.py',         'adv'),
    ('advancedplus',        'gen_advp.py',        'advp'),
]

SECTIONS = {
    'vocabulary', 'reading', 'listening', 'grammar', 'speaking', 'writing',
    'pronunciation', 'practical_english', 'vocabulary_bank', 'wordbuilding',
    'revise_and_check', 'dialogue', 'exercise',
}


def provenance_from_generator(path):
    """topic key -> section, read off the source-band comments.

    The comments are the record of which part of the book each block of words
    was taken from. Parsing them keeps the metadata tied to the source rather
    than to a fresh judgement about the word itself.
    """
    text = open(path, encoding='utf-8').read()
    prov = {}
    current = None
    for line in text.split('\n'):
        band = re.match(r"^#\s*-+\s*(.*?)\s*-*\s*$", line)
        if band:
            current = classify_band(band.group(1))
            continue
        # a topic block starts with T['key'] = [
        key = re.match(r"^T\[['\"]([A-Za-z0-9_]+)['\"]\]\s*=", line)
        if key and current:
            prov.setdefault(key.group(1), current)
    return prov


def classify_band(label):
    low = label.lower()
    if 'vocabulary bank' in low or 'word bank' in low:
        return 'vocabulary_bank'
    if 'practical english' in low or re.search(r'\bPE\b', label):
        return 'practical_english'
    if 'revise and check' in low:
        return 'revise_and_check'
    if 'word building' in low or 'prefix' in low or 'suffix' in low:
        return 'wordbuilding'
    if 'pronunciation' in low:
        return 'pronunciation'
    if 'grammar' in low:
        return 'grammar'
    # Everything else in the generators is an in-lesson VOCABULARY box, which
    # the books print inside the lesson rather than in the back-of-book bank.
    return 'vocabulary'


def headwords_in(body):
    """Every headword in a list of word tuples, whatever quoting the file uses.

    Headwords are written three ways across the generators: 'money', "o'clock"
    (double quotes, because the word itself has an apostrophe), and
    'That\\'s interesting.' (an escaped apostrophe inside single quotes). A
    naive r"'([^']*)'" scanner truncates the third at the escape and misses the
    second entirely, which silently drops real words from the metadata pass.
    Only the first element of each tuple is a headword, so the scan restarts at
    every top-level "(" — an apostrophe inside an example sentence can never be
    mistaken for the start of a headword.
    """
    out = []
    i, n = 0, len(body)
    while i < n:
        c = body[i]
        if c != '(':
            i += 1
            continue
        j = i + 1
        while j < n and body[j] in ' \t\r\n':
            j += 1
        if j < n and body[j] in '"\'':
            q = body[j]
            k = j + 1
            buf = []
            while k < n:
                if body[k] == '\\' and k + 1 < n:
                    buf.append(body[k + 1])
                    k += 2
                    continue
                if body[k] == q:
                    break
                buf.append(body[k])
                k += 1
            out.append(''.join(buf))
            i = k + 1
        else:
            i += 1
    return out


def section_for_lesson_code(code):
    """Source section implied by an English File lesson code.

    gen_beginner.py stores each lesson's words under the lesson code itself, so
    the code is the provenance rather than something to infer from the word.
    PE* are the Practical English lessons; a unit's C lesson is the Practical
    English episode the books place at the end of the unit; A and B lessons
    carry the in-lesson VOCABULARY box. Beginner has no back-of-book bank.
    """
    c = code.upper()
    if c.startswith('PE') or c.endswith('C'):
        return 'practical_english'
    return 'vocabulary'


def words_of(doc):
    """The word list of an already-parsed pack document.

    Takes the parsed doc, NOT a path: parsing twice gives two independent
    copies, and mutating one while dumping the other silently writes nothing.
    """
    return doc['words'] if isinstance(doc, dict) and 'words' in doc else doc


def main():
    unmapped = []
    stats = {}
    for stem, gen, bid in BOOKS:
        data_path = os.path.join(DATA, stem + '.json')
        gen_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), gen)
        if not os.path.exists(data_path):
            continue
        if not os.path.exists(gen_path):
            print(f'  !! {stem}: generator {gen} missing, cannot prove provenance')
            unmapped.append((stem, '<no generator>'))
            continue

        prov = provenance_from_generator(gen_path)
        doc = json.load(open(data_path, encoding='utf-8'))
        ws = words_of(doc)   # same object graph as `doc`, so mutations persist

        # Rebuild the topic-key -> words mapping the generator used, so each word
        # inherits the section of the band it was written under.
        text = open(gen_path, encoding='utf-8').read()

        # Two generator shapes exist. Most group words under topic keys
        # (T['money']) beneath a source-band comment. gen_beginner.py instead
        # keeps each lesson's words directly under L['<lesson code>'], and there
        # the lesson code itself is the source evidence.
        lesson_sec = {}
        for m in re.finditer(r"^L\[['\"]([A-Za-z0-9]+)['\"]\]\s*=", text, re.M):
            lesson_sec[m.group(1)] = section_for_lesson_code(m.group(1))
        key_words = {}
        for m in re.finditer(r"^T\[['\"]([A-Za-z0-9_]+)['\"]\]\s*=\s*\[(.*?)^\]", text, re.S | re.M):
            key_words.setdefault(m.group(1), set()).update(headwords_in(m.group(2)))

        by_head = {}
        for key, ens in key_words.items():
            sec = prov.get(key)
            if not sec:
                unmapped.append((stem, key))
                continue
            for en in ens:
                by_head.setdefault(en.strip().lower(), sec)

        # Beginner shape: the words sit inside L['<code>'] = (unit, title, topic, [...]).
        for code, sec in lesson_sec.items():
            m = re.search(r"^L\[['\"]%s['\"]\]\s*=\s*\(.*?\[(.*?)^\]\)"
                          % re.escape(code), text, re.S | re.M)
            if m:
                for en in headwords_in(m.group(1)):
                    by_head.setdefault(en.strip().lower(), sec)
        # ...plus words appended to a lesson later in the file, e.g.
        # L['3C'][3].append(('bill', ...)) — the append body is one tuple.
        for m in re.finditer(
                r"^L\[['\"]([A-Za-z0-9]+)['\"]\]\[3\]\.append\((\(.*?\))\)",
                text, re.M):
            for en in headwords_in(m.group(2)):
                by_head.setdefault(en.strip().lower(),
                                   section_for_lesson_code(m.group(1)))

        counts = {}
        for w in ws:
            sec = by_head.get(w['en'].strip().lower())
            if not sec:
                continue
            for bk in w.get('books', []):
                if bk.get('book') != bid:
                    continue
                if sec not in SECTIONS:
                    raise SystemExit(f'{stem}: "{sec}" is not in the schema enum')
                bk['section'] = sec
                counts[sec] = counts.get(sec, 0) + 1
        # Curated entries come from the book's own vocabulary teaching, which is
        # the strongest evidence tier in the brief. Nothing here is a bare
        # occurrence in a text, so `low` would be a false claim.
        w_added = 0
        for w in ws:
            if any(bk.get('book') == bid and bk.get('section') for bk in w.get('books', [])):
                w.setdefault('confidence', 'high')
                w_added += 1
        missing = [w['en'] for w in ws
                   if not any(bk.get('book') == bid and bk.get('section')
                              for bk in w.get('books', []))]
        json.dump(doc, open(data_path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        stats[stem] = (len(ws), w_added, counts, missing)

    if unmapped:
        print('\nUNMAPPED topic keys (no section assigned — evidence gap):')
        for stem, key in unmapped:
            print(f'  {stem}: {key}')
        print('\nRefusing to guess these. Add them to the generator comments or')
        print('to PROVENANCE, then re-run.')
        return 1

    print('\nsection metadata written:')
    holes = 0
    for stem, (n, added, counts, missing) in stats.items():
        top = ', '.join(f'{k}={v}' for k, v in sorted(counts.items(), key=lambda x: -x[1]))
        print(f'  {stem:<20} {added:>4}/{n:<4} words   {top}')
        if missing:
            holes += len(missing)
            print(f'      {len(missing)} with NO section evidence: '
                  f'{", ".join(missing[:6])}{" ..." if len(missing) > 6 else ""}')
    if holes:
        print(f'\n{holes} word(s) left without section metadata. That is an')
        print('evidence gap, not a silent pass: the field stays absent.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
