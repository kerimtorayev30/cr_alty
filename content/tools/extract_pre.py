#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract taught-vocabulary candidates for English File Pre-Intermediate from
the owner-supplied PDFs — and, unlike Beginner/Elementary, the Student's Book
itself has a text layer, so the primary source is the book:

  sb_vb   HIGH  the Student's Book Vocabulary Bank (SB pp.151-164): items are
                printed as "word /ipa/" inside example sentences — an explicit
                list with pronunciation, the strongest evidence there is.
  list    HIGH  comma-separated answer lists on the TG Vocabulary activity
                instruction pages (TG 253-256).
  key     HIGH  numbered answer keys in TG lesson plans.
  teach   HIGH  "teach/elicit X (/IPA/)" lines in TG lesson plans.
  notes   MEDIUM words explained in TG "Vocabulary notes" boxes.

Lesson attribution: SB VB pages map 1:1 onto Vocabulary Bank bands (the book
prints the VB page number on each lesson's cross-reference, e.g. 1B → p.151
"Describing people"); the map below is read off the SB pages themselves.
TG-side candidates are attributed by running head. Anagram masters (TG 257+)
are not mined.

Output: content/pdf/pre-sb-candidates.json (diffed against data/
preintermediate.json).
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SB_TXT = os.path.join(HERE, '..', 'pdf', 'pre-sb.txt')
TG_TXT = os.path.join(HERE, '..', 'pdf', 'pre-tg.txt')
EXISTING = os.path.join(HERE, '..', 'data', 'preintermediate.json')
OUT = os.path.join(HERE, '..', 'pdf', 'pre-sb-candidates.json')

# SB pdf page -> VB band topic (checked against the SB page headings)
SB_VB_PAGES = {
    151: 'describing_people', 152: 'clothes', 153: 'holidays',
    154: 'prepositions_time', 155: 'housework', 156: 'shopping',
    157: 'town_city', 158: 'opposite_verbs', 159: 'verb_forms',
    160: 'get', 161: 'confusing_verbs', 162: 'animals',
    163: 'movement', 164: 'phrasal_verbs',
}
PLAN_START, PLAN_END = 12, 166
VOCAB_INSTR = range(253, 257)

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


def load(tag, path):
    txt = open(path, encoding='utf-8').read()
    parts = re.split(r'(?m)^@@%s (\d+)@@$' % tag, txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def norm_word(w):
    w = unicodedata.normalize('NFC', w.strip())
    w = re.sub(r'^[•●\-\u2022\s]+', '', w)
    if re.match(r'^[Aa]n?\s+[a-z]', w):
        w = re.sub(r'^[Aa]n?\s+', '', w)
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


# word immediately followed by an IPA transcription: the book's own marker of
# a taught item (the SB prints /…/ after every new word)
IPA_ITEM = re.compile(r"\b([a-z][a-z'’\-]*(?:\s+[a-z][a-z'’\-]*){0,3}?)\s+/[^/\n]{2,22}/")
IPA_STOP = re.compile(r"\b(a|an|the|is|are|was|were|and|or|of|to|in|on|at|it|its|"
                      r"you|your|i|he|she|we|they|his|her|very|quite|bit|look|"
                      r"looks|like|has|have|with|for|do|does|does|not|no|yes)\b")


def extract_sb_vb(pm):
    out = []
    for p, band in SB_VB_PAGES.items():
        t = pm.get(p, '')
        for m in IPA_ITEM.finditer(t):
            phrase = m.group(1).strip()
            # keep only the head noun/verb chunk: cut leading function words
            toks = phrase.split()
            while toks and (toks[0].lower() in FUNCTION or IPA_STOP.match(toks[0])):
                toks.pop(0)
            if not toks:
                continue
            # trailing function words also go
            while toks and toks[-1].lower() in FUNCTION:
                toks.pop()
            w = norm_word(' '.join(toks))
            if plausible_head(w):
                out.append((w, band, p))
    return out


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
    code_re = r'(\d{1,2}[ABC]|PE\d)'
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
    sb = load('SBPAGE', SB_TXT)
    tg = load('PAGE', TG_TXT)
    cands = []

    for w, band, p in extract_sb_vb(sb):
        cands.append({'en': w, 'src': 'sb_vb', 'band': band, 'page': p,
                      'evidence': 'sb_vb'})

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
        marks = list(re.finditer(r'(?m)^[ \t]*(\d{1,2}[ABC]|PE\d)[\t ]', t))
        for i, m in enumerate(marks):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(t)
            body = t[m.end():end]
            for w in extract_instr_lists(body):
                cands.append({'en': w, 'src': m.group(1), 'page': p,
                              'evidence': 'list'})
            for w in extract_keys(body):
                cands.append({'en': w, 'src': m.group(1), 'page': p,
                              'evidence': 'key'})

    # dedupe: SB evidence wins, then TG order
    RANK = {'sb_vb': 0, 'list': 1, 'key': 2, 'teach': 3, 'notes': 4}
    best = {}
    for c in cands:
        k = c['en'].lower()
        if k not in best or RANK[c['evidence']] < RANK[best[k]['evidence']]:
            best[k] = c
    final = sorted(best.values(), key=lambda c: (c.get('band') or c['src'], c['en'].lower()))

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
    from collections import Counter
    print('candidates:', len(final), dict(Counter(c['evidence'] for c in final)))
    print('already in preintermediate.json:', len(final) - len(new))
    print('NEW candidates:', len(new))
    for c in new:
        loc = c.get('band') or c['src']
        print(f"  {loc:<18} [{c['evidence']:<6}] p.{c['page']:<3} {c['en']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
