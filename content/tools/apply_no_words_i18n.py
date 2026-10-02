#!/usr/bin/env python3
"""Add the no_words string (en + tk + ru together) and use it in the unit row.

A unit belonging to a book that has not been imported yet has no words. Showing
"— words" there reads like a bug, so the row says plainly that the book is not
imported. Per the brief, a new user-visible string must land in all three
dictionaries in the same change or the app silently falls back to English.
"""
import sys

P = 'uploads/app-yatla.html'
h = open(P, encoding='utf-8').read()
edits = []


def sub(old, new, label):
    global h
    n = h.count(old)
    if n != 1:
        sys.exit(f'ABORT [{label}]: anchor matched {n} times, expected 1')
    h = h.replace(old, new, 1)
    edits.append(label)


sub('pack_on:"{n} words ready",', 'pack_on:"{n} words ready",no_words:"Not imported yet",', 'en no_words')
sub('pack_on:"{n} söz taýýar",', 'pack_on:"{n} söz taýýar",no_words:"Entek goşulmady",', 'tk no_words')
sub('pack_on:"Готово слов: {n}",', 'pack_on:"Готово слов: {n}",no_words:"Ещё не добавлено",', 'ru no_words')

sub(
    '<div class="meta sub">${unitCount(b.id,n)||"—"} ${t("words")} · ${st===',
    '<div class="meta sub">${unitCount(b.id,n)?unitCount(b.id,n)+" "+t("words"):t("no_words")} · ${st===',
    'unit row shows the real count or an honest label',
)

open(P, 'w', encoding='utf-8').write(h)
print(f'{len(edits)} edits applied')
for e in edits:
    print('  -', e)
