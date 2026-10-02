#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract taught-vocabulary candidates for English File Intermediate Plus.

The four uploaded SB PDFs are SCANS (no text layer). Two sources:

  sb_vb   HIGH  the SB Vocabulary Bank as OCR'd into uploads/inter plus.txt
                (dump lines ~9088-10110 = SB pp.152-163, 12 sections). Headwords
                legible; IPA mojibake ignored.
  list    HIGH  comma-separated / numbered answer lists on the TG Vocabulary
                activity instruction pages (TG 202-205).
  key     HIGH  numbered answer keys in TG lesson plans (TG 12-148).
  teach   HIGH  "teach/elicit X (/IPA/)" lines in TG lesson plans.
  notes   MEDIUM words explained in TG "Vocabulary notes" boxes.

Vocabulary activity masters (TG 206+) are anagrams/word-searches — NOT mined.
Output: content/pdf/intp-candidates.json (diffed against data/
intermediateplus.json).
"""
import json
import os
import re
import sys
import unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
TG_TXT = os.path.join(HERE, '..', 'pdf', 'intp-tg.txt')
SB_DUMP = os.path.join(HERE, '..', '..', 'uploads', 'inter plus.txt')
EXISTING = os.path.join(HERE, '..', 'data', 'intermediateplus.json')
OUT = os.path.join(HERE, '..', 'pdf', 'intp-candidates.json')

# OCR-dump line ranges -> VB section -> lesson (SB pp.152-163)
VB_SECTIONS = [
    (9088, 9134, 'adj_suffixes', '1B'),
    (9135, 9194, 'packing', '2A'),
    (9195, 9254, 'shops_services', '2B'),
    (9255, 9329, 'photography', '3B'),
    (9330, 9454, 'recycling', '4A'),
    (9455, 9519, 'television', '5A'),
    (9520, 9603, 'country', '5B'),
    (9604, 9621, 'restaurant', '6A'),
    (9622, 9672, 'diy', '6B'),
    (9673, 9799, 'phrasal_verbs', '7A'),
    (9800, 10110, 'looking_after', '8A'),
]
PLAN_START, PLAN_END = 12, 148
VOCAB_INSTR = range(202, 206)

FUNCTION = {
    'of', 'the', 'and', 'or', 'a', 'an', 'in', 'on', 'at', 'to', 'for',
    'with', 'by', 'up', 'down', 'out', 'off', 'as', 'be', 'been', 'being',
    'not', 'but', 'so', 'if', 'all', 'its', 'his', 'her', 'am', 'are',
    'is', 'was', 'were', 'do', 'does', 'did', 'has', 'have', 'had',
    'will', 'would', 'can', 'could', 'must', 'should', 'may', 'might',
    'there', 'here', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
    'she', 'it', 'we', 'they', 'me', 'him', 'us', 'them', 'my', 'your',
    'our', 'their', 'mine', 'yours', 'one', 'two',
}
TEACHER_TALK = {
    'meaning', 'answer', 'answers', 'phrase', 'phrases', 'response', 'word',
    'words', 'number', 'numbers', 'vocabulary', 'stress', 'pronunciation',
    'question', 'questions', 'form', 'forms', 'ending', 'endings',
    'translation', 'board', 'class', 'student', 'students', 'spelling',
    'sentence', 'sentences', 'instruction', 'instructions', 'activity',
    'activities', 'support', 'idea', 'note', 'notes', 'key', 'example',
    'examples', 'exercise', 'exercises', 'sound', 'sounds', 'lexis',
    'drill', 'model', 'pairwork', 'worksheet', 'worksheets', 'audio',
    'video', 'photo', 'photos', 'picture', 'pictures', 'map', 'chart',
    'dialogue', 'text', 'title', 'topic', 'rule', 'rules', 'verb', 'verbs',
    'noun', 'nouns', 'adjective', 'adjectives', 'preposition',
    'prepositions', 'singular', 'plural', 'just', 'only', 'any', 'which',
    'who', 'whose', 'how', 'what', 'where', 'when', 'why', 'from', 'onto',
    'before', 'after', 'first', 'second', 'name', 'language',
}


def norm_word(w):
    w = unicodedata.normalize('NFC', w.strip())
    w = re.sub(r'^[•●\-\u2022\s]+', '', w)
    if re.match(r'^[Aa]n?\s+[a-z]', w):
        w = re.sub(r"^[Aa]n?\s+", '', w)
    w = w.strip(' .,;:!?()"“”‘’')
    w = re.sub(r'\s{2,}', ' ', w)
    return w


def plausible_head(w):
    if not w or len(w) < 2 or len(w) > 48:
        return False
    words = w.split()
    if len(words) > 5:
        return False
    if not re.match(r"^[A-Za-z0-9'’\-\.\s/()]+$", w):
        return False
    low = w.lower()
    if re.match(r'^(e\s)?\d{1,2}\.\d+$', low) or re.match(r'^p?\.?\d+$', low):
        return False
    if not re.search(r'[A-Za-z]', w):
        return False
    if low in TEACHER_TALK or low in FUNCTION:
        return False
    return True


VB_ITEM = re.compile(
    r"(?<![A-Za-z])\b([a-z][a-z'’\-]*(?:\s+[a-z][a-z'’\-]*){0,3}?)"
    r"\s+[/\"“(][^\s/\"“)\n]{2,24}")


def extract_sb_vb():
    out = []
    lines = open(SB_DUMP, encoding='utf-8', errors='replace').read().split('\n')
    for start, end, band, lesson in VB_SECTIONS:
        seen = set()
        for ln in lines[start - 1:end]:
            for m in VB_ITEM.finditer(ln):
                phrase = m.group(1).strip()
                toks = phrase.split()
                while toks and toks[0].lower() in FUNCTION:
                    toks.pop(0)
                while toks and toks[-1].lower() in FUNCTION:
                    toks.pop()
                w = norm_word(' '.join(toks))
                if plausible_head(w) and w.lower() not in seen:
                    seen.add(w.lower())
                    out.append((w, band, lesson))
    return out


def load(tag, path):
    txt = open(path, encoding='utf-8').read()
    parts = re.split(r'(?m)^@@%s (\d+)@@$' % tag, txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


KEY_PAIR = re.compile(r'\b(\d{1,2})\s{1,3}([A-Za-z][^\d\n]{0,38}?)(?=\s{2,}\d{1,2}\s|\s*$)')


def extract_keys(t):
    out = []
    for line in t.split('\n'):
        pairs = KEY_PAIR.findall(line.rstrip())
        if len(pairs) < 3:
            continue
        if re.search(r"\b(I|he|she|it|we|you|they)\b|[’'](?:m|s|re|ll|ve)|\?|\bWhat\b|\bWhere\b|…", line):
            continue
        for _n, val in pairs:
            w = norm_word(val)
            if plausible_head(w):
                out.append(w)
    return out


TEACH = re.compile(r'\b(?:teach|elicit)\s+(?:the\s+|them\s+)?'
                   r"([a-z][a-z'’\-]*(?:\s+[a-z][a-z'’\-]*)?)"
                   r'(\s*/[^/\n]{2,24}/)?')
EG = re.compile(r'\be\.g\.\s*([A-Za-z][^\n.]{2,80})')


def extract_teach(t):
    return [norm_word(m.group(1)) for m in TEACH.finditer(t)
            if plausible_head(norm_word(m.group(1)))]


def extract_notes(t):
    out = []
    for m in re.finditer(r'(?m)^Vocabulary notes\s*$', t):
        block = t[m.end():m.end() + 1800]
        stop = re.search(r'(?m)^(EXTRA|Grammar notes|\d\s+(GRAMMAR|VOCABULARY))', block)
        if stop:
            block = block[:stop.start()]
        for e in EG.finditer(block):
            for piece in re.split(r';|,| and ', e.group(1)):
                w = norm_word(piece)
                if plausible_head(w):
                    out.append(w)
    return out


INSTR_LINE = re.compile(r'(?m)^[a-z0-9]{1,2}[\t ]+([A-Za-z][^\n]{10,220})$')
INSTR_VERBS = re.compile(r'^(Give|Tell|Get|Check|Make|Put|Play|Ask|Use|Set|Go|Point|'
                         r'Write|Model|Elicit|Focus|Show|Explain|For|If|Then|When|'
                         r'Monitor|Drill|Books|Sts|Now|In|You|This|The)\b')


def extract_instr_lists(t):
    out = []
    for m in INSTR_LINE.finditer(t):
        body = m.group(1)
        if INSTR_VERBS.match(body) or 'Sts' in body or 'e.g.' in body:
            continue
        pieces = [p.strip() for p in body.split(',')]
        if len(pieces) < 4:
            continue
        good = [norm_word(p) for p in pieces]
        if sum(1 for g in good if plausible_head(g)) >= len(good) * 0.6:
            out.extend(g for g in good if plausible_head(g))
    return out


def tg_lesson_map(pm):
    lm = {}
    current = None
    code_re = r'(\d{1,2}[AB]|PE\d)'
    for p in range(PLAN_START, PLAN_END + 1):
        t = pm.get(p, '')
        opener = re.search(r'(?m)^\s*(%s)\s+[A-Z#“”"\t][^\n]{2,50}$' % code_re, t[:400])
        head = re.search(r'(?m)^\s*\d{1,3}\s*\n\s*(%s)\s*$' % code_re, t[:120])
        bare = re.search(r'(?m)^\s*(%s)\s*$' % code_re, t[:120])
        if opener:
            current = opener.group(1)
        elif head:
            current = head.group(1)
        elif bare:
            current = bare.group(1)
        if re.search(r'Revise and Check', t[:300]):
            current = None
        if current:
            lm[p] = current
    return lm


def main():
    tg = load('PAGE', TG_TXT)
    cands = []

    for w, band, lesson in extract_sb_vb():
        cands.append({'en': w, 'src': lesson, 'band': band,
                      'page': 0, 'evidence': 'sb_vb'})

    lm = tg_lesson_map(tg)
    for p, lesson in sorted(lm.items()):
        t = tg.get(p, '')
        for w in extract_keys(t):
            cands.append({'en': w, 'src': lesson, 'page': p, 'evidence': 'key'})
        for w in extract_teach(t):
            cands.append({'en': w, 'src': lesson, 'page': p, 'evidence': 'teach'})
        for w in extract_notes(t):
            cands.append({'en': w, 'src': lesson, 'page': p, 'evidence': 'notes'})

    for p in VOCAB_INSTR:
        t = tg.get(p, '')
        marks = list(re.finditer(r'(?m)^[ \t]*(\d{1,2}[AB]|PE\d)[\t ]', t))
        for i, m in enumerate(marks):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(t)
            body = t[m.end():end]
            for w in extract_instr_lists(body):
                cands.append({'en': w, 'src': m.group(1), 'page': p,
                              'evidence': 'list'})
            for w in extract_keys(body):
                cands.append({'en': w, 'src': m.group(1), 'page': p,
                              'evidence': 'key'})

    RANK = {'sb_vb': 0, 'list': 1, 'key': 2, 'teach': 3, 'notes': 4}
    best = {}
    for c in cands:
        k = c['en'].lower()
        if k not in best or RANK[c['evidence']] < RANK[best[k]['evidence']]:
            best[k] = c
    final = sorted(best.values(),
                   key=lambda c: (c.get('band') or c['src'], c['en'].lower()))

    d = json.load(open(EXISTING, encoding='utf-8'))
    ws = d['words'] if isinstance(d, dict) and 'words' in d else d
    have = set()
    for w in ws:
        have.add(w['en'].strip().lower())
        for extra in (w.get('syn', ''), w.get('coll', '')):
            for piece in str(extra).split(','):
                piece = piece.strip().lower()
                if piece and piece != '—':
                    have.add(piece)
    new = [c for c in final if c['en'].lower() not in have]

    json.dump(final, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('candidates:', len(final), dict(Counter(c['evidence'] for c in final)))
    print('already in intermediateplus.json:', len(final) - len(new))
    print('NEW candidates:', len(new))
    for c in new:
        loc = c.get('band') or c['src']
        print(f"  {loc:<16} [{c['evidence']:<6}] p.{c['page']:<3} {c['en']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
