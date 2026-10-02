#!/usr/bin/env python3
"""Probe: can the Elementary Vocabulary Bank be machine-extracted?

Unlike the Beginner dump, this OCR kept the headwords legible:
    abathroom "ba:ru:m      an armchair /a:mtfea      a light /lart
    cook                    an accountant             a chemist's /'kemusts

So instead of reconstructing the word lists from memory (which is what the
Beginner import had to do), we can read the book's own lists.

This script only MEASURES. It segments the Vocabulary Bank body into topic
sections, pulls out plausible headwords, and reports what it found and what it
rejected, so the result can be checked by eye before anything is generated.

Usage: python3 content/tools/extract_elementary.py
"""
import json
import os
import re

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'uploads', 'elementary.txt')

# Section starts, in document order, from the "p.NNN <Topic> VOCABULARY BANK"
# headers plus the "N TOPIC" banners inside the body.
SECTIONS = [
    (14094, 14254, 'Days and numbers', 148),
    (14255, 14352, 'Classroom language', 150),
    (14353, 14400, 'Things', 151),
    (14401, 14454, 'Adjectives', 152),
    (14455, 14546, 'Verb phrases', 153),
    (14547, 14673, 'Jobs', 154),
    (14674, 14790, 'The family', 155),
    (14791, 14852, 'Daily routine', 156),
    (14853, 14984, 'Time', 157),
    (14985, 15060, 'More verb phrases', 158),
    (15061, 15090, 'The house', 161),
    (15091, 15110, 'Prepositions', 162),
    (15111, 15161, 'Food and drink', 163),
    (15162, 15205, 'Places and buildings', 164),
]

# Lines that are exercises, labels or audio cues rather than vocabulary.
NOISE = re.compile(
    r'^\s*(?:[a-d]\s|[a-d]\)|\d+\s+[A-Z]|ACTIVATION|Listen|Cover|Match|Write|Complete|'
    r'Choose|Ask|Test|Say|Work|Look|Put|Add|Circle|Underline|Check|Read|Fill|'
    r'VOCABULARY BANK|SOUND BANK|Pronunciation|Capital letters|Now |In pairs|'
    r'\W*$)', re.I)

# A headword: letters, spaces, hyphens, apostrophes, optional leading article,
# optional plural in brackets. Everything after it may be IPA.
HEAD = re.compile(
    r"""^\s*
        (?:an?\s+)?                       # article
        ([a-zA-Z][a-zA-Z'’\-]*(?:\s+[a-zA-Z'’\-]+){0,3})   # the word itself
        (?:\s*\((?:=|or|[^)]{0,24})\))?   # a parenthetical gloss
        \s*
        (?P<rest>.*)$
    """, re.X)

IPAISH = re.compile(r"[/\[(\"“‘'’].{1,28}[/\])\"”]\s*$|^\s*[/\[(].*")


def looks_like_ipa(s):
    return bool(IPAISH.search(s)) if s else False


def main():
    lines = open(SRC, encoding='utf-8', errors='replace').read().split('\n')
    report = []
    for start, end, topic, page in SECTIONS:
        found, rejected = [], []
        for i in range(start - 1, min(end, len(lines))):
            raw = lines[i].rstrip('\r')
            if NOISE.match(raw) or len(raw.strip()) < 2:
                continue
            # two-column pages put two entries on one line; split on a second IPA
            for chunk in re.split(r'\s{2,}', raw.strip()):
                m = HEAD.match(chunk)
                if not m:
                    rejected.append(chunk)
                    continue
                word = re.sub(r'\s+', ' ', m.group(1)).strip()
                if len(word) < 2 or word.lower() in {'the', 'a', 'an', 'and', 'or'}:
                    rejected.append(chunk)
                    continue
                found.append(word)
        report.append((topic, page, found, rejected))

    total = 0
    for topic, page, found, rejected in report:
        total += len(found)
        print(f'\n=== p.{page} {topic} — {len(found)} headwords, {len(rejected)} lines rejected')
        print('   ', ', '.join(found[:38]))
        if len(found) > 38:
            print(f'    ... +{len(found) - 38} more')
        if rejected:
            print('    rejected sample:', '; '.join(rejected[:6])[:200])
    print(f'\nTOTAL headwords: {total}')


if __name__ == '__main__':
    main()
