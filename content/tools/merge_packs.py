#!/usr/bin/env python3
"""Merge content/data/*.json into one vocabulary pack.

Why this exists: favourites, history, review state and the word of the day all
key on the English headword, so one headword must exist exactly once. But the
same word is genuinely taught by more than one book — Elementary repeats 169 of
Beginner's words — so the merged entry carries every book that teaches it.

Which entry survives when two books teach the same word: the one from the file
listed first in ORDER. beginner.json and elementary.json hold the full curated
sets; ef2/ef2b/ef3/ef4 are the small starter files and lose. The losing entry is
not thrown away — its books[] is copied onto the survivor, and the merge is
reported so nothing disappears silently.

Run: python3 content/tools/merge_packs.py            (writes content/data/_pack.json)
     python3 content/tools/merge_packs.py --dry      (report only, writes nothing)
"""
import glob
import json
import os
import sys

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
# Written outside data/ on purpose: build.js reads every *.json in the data
# directory, and the merged pack must be the ONLY thing it sees, or every word
# would be counted twice (once per source file, once merged).
MERGED_DIR = os.path.join(os.path.dirname(DATA), 'merged')
OUT = os.path.join(MERGED_DIR, 'yatla-all.json')

# earliest book wins ties; within a level the full curated file comes first
ORDER = ['beginner.json', 'elementary.json', 'preintermediate.json',
    'intermediate.json',
    'intermediateplus.json',
    'upperintermediate.json',
    'advanced.json',
    'advancedplus.json',
         'ef2.json', 'ef2b.json', 'ef3.json', 'ef4.json']


def load_all():
    files = {os.path.basename(f): f for f in glob.glob(os.path.join(DATA, '*.json'))}
    unknown = sorted(set(files) - set(ORDER))
    if unknown:
        raise SystemExit('data files not in ORDER (add them or delete them): ' + ', '.join(unknown))
    return [(name, json.load(open(files[name], encoding='utf-8')))
            for name in ORDER if name in files]


def merge():
    packs = load_all()
    words, by_key, lessons, report = [], {}, [], []

    for fname, pack in packs:
        for w in pack.get('words', []):
            key = w['en'].strip().lower()
            if key in by_key:
                keep = by_key[key]
                have = {(b['book'], b.get('unit'), b.get('lesson')) for b in keep['books']}
                added = 0
                for b in w['books']:
                    if (b['book'], b.get('unit'), b.get('lesson')) not in have:
                        keep['books'].append(b)
                        added += 1
                report.append(f'{w["en"]:24} {fname:<16} -> merged into the entry '
                              f'from the earlier file ({added} book ref added)')
                continue
            by_key[key] = json.loads(json.dumps(w))
            words.append(by_key[key])

        for l in pack.get('lessons', []):
            l = dict(l)
            l['book'] = pack.get('book')
            if not l.get('words'):
                continue
            lessons.append(l)

    for w in words:
        w['books'].sort(key=lambda b: (ORDER_BOOK.index(b['book']) if b['book'] in ORDER_BOOK else 99,
                                       b.get('unit') or 0, str(b.get('lesson') or '')))

    return words, lessons, report, packs


ORDER_BOOK = ['beg', 'ele', 'pre', 'int', 'upp', 'adv', 'intp', 'advp']


def main():
    dry = '--dry' in sys.argv
    words, lessons, report, packs = merge()

    multi = [w for w in words if len(w['books']) > 1]
    print(f'files:      {", ".join(p[0] for p in packs)}')
    print(f'words:      {len(words)} unique headwords '
          f'({len(report)} absorbed as duplicates, {len(multi)} taught by 2+ books)')
    print(f'lessons:    {len(lessons)}')
    per_book = {}
    for w in words:
        for b in w['books']:
            per_book[b['book']] = per_book.get(b['book'], 0) + 1
    print('per book:   ' + ', '.join(f'{k}:{v}' for k, v in sorted(per_book.items(), key=lambda kv: ORDER_BOOK.index(kv[0]) if kv[0] in ORDER_BOOK else 99)))
    print()
    for r in report[:14]:
        print('  ', r)
    if len(report) > 14:
        print(f'   ... and {len(report) - 14} more')

    if dry:
        print('\n(dry run — nothing written)')
        return

    os.makedirs(MERGED_DIR, exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump({'book': 'all',
                   'title': 'Merged from content/data by tools/merge_packs.py',
                   'words': words, 'lessons': lessons}, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f'\nwrote {os.path.normpath(OUT)}')


if __name__ == '__main__':
    main()
