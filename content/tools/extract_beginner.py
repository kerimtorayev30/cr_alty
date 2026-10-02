#!/usr/bin/env python3
"""
Extract the Vocabulary Bank word lists from the OCR dump of
English File Beginner (4th ed.) Student's e-book.

The OCR interleaves columns and loses some items, so this script only REPORTS what it
finds. The resulting inventory is then reconciled by hand before any word is written
into content/data/.

Usage: python3 content/tools/extract_beginner.py [dump.txt]
"""
import re
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else '/home/user/uploads/beginner book databsae.txt'
raw = open(SRC, encoding='utf-8').read()

# The Vocabulary Bank lives after the last unit and before the credits.
start = raw.index('VOCABULARY BANK')
bank = raw[start:]

# Numbered list items: "1 the board", "12 acamera", "21 water /waortto"
ITEM = re.compile(r'(?<![\w.])(\d{1,2})\s+((?:an?|the)\s+)?([A-Za-z][A-Za-z\'\-\. ]{1,28}?)(?:\s+(/[^\s]+/|[a-z\':\.\s]{2,20}))?(?=\s{2,}|\s*\r?\n|$)')

sections = []
cur = None
for line in bank.split('\n'):
    ln = line.strip()
    if not ln:
        continue
    if 'VOCABULARY BANK' in ln:
        name = ln.replace('VOCABULARY BANK', '').strip(' ©@p.0123456789')
        cur = {'title': name or '(continuation)', 'items': {}, 'raw': []}
        sections.append(cur)
        continue
    if cur is None:
        continue
    cur['raw'].append(ln)
    for m in ITEM.finditer(ln):
        num, art, word = int(m.group(1)), (m.group(2) or '').strip(), m.group(3).strip()
        word = re.sub(r'\s+', ' ', word).strip(' ,.;:')
        if not word or len(word) < 2:
            continue
        if word.lower() in {'listen', 'repeat', 'cover', 'look', 'say', 'and', 'the', 'photo', 'photos', 'words', 'phrases'}:
            continue
        if num not in cur['items']:
            cur['items'][num] = (('a ' if art == 'a ' else 'an ' if art == 'an ' else '') + word)

print(f'Vocabulary Bank: {len(sections)} header blocks\n')
total = 0
for s in sections:
    nums = sorted(s['items'])
    total += len(nums)
    print(f'== {s["title"]}  ({len(nums)} numbered items: {nums[0] if nums else "-"}..{nums[-1] if nums else "-"})')
    print('   ' + ' | '.join(f'{n}:{s["items"][n]}' for n in nums))
    print()
print(f'total numbered items recovered: {total}')
