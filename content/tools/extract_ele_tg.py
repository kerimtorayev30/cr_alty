#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract taught-vocabulary candidates from the English File Elementary
Teacher's Guide (two owner-supplied PDFs, continuous pages 1-275 →
content/pdf/ele-tg.txt).

Same evidence doctrine as extract_beg_tg.py (spec §12/§13/§14/§16):
  key      HIGH  numbered answer keys of vocabulary exercises in lesson plans
  teach    HIGH  "teach/elicit X (/IPA/)" lines
  list     HIGH  comma-separated answer lists on the Vocabulary activity
                 INSTRUCTION pages (TG 253-256): "a  eight, five, twelve, …"
  notes    MEDIUM words explained in "Vocabulary notes" boxes

Elementary-specific decisions:
- Lessons are A/B/C per file plus PE1-PE6 episodes; Revise & Check pages are
  revision and are skipped as a source (§7).
- The Vocabulary activity MASTERS (TG 257-275) are deliberately NOT scanned
  for word banks: they are anagrams and word-searches ("enidytit arcd"), so
  their letter soup would pass a plausibility filter as fake words. The
  instruction pages carry the real answers instead.
- Grammar answer keys ("1 are 2 is 3 am …") are the biggest noise source;
  the line filter rejects contractions/sentences and the function-word
  stoplist rejects be-forms.
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TG_TXT = os.path.join(HERE, '..', 'pdf', 'ele-tg.txt')
EXISTING = os.path.join(HERE, '..', 'data', 'elementary.json')
OUT = os.path.join(HERE, '..', 'pdf', 'ele-tg-candidates.json')
PLAN_START, PLAN_END = 12, 163
VOCAB_INSTR = range(253, 257)

CODE_RE = r'(\d{1,2}[ABC]|PE\d)'

FUNCTION = {
    'of', 'the', 'and', 'or', 'a', 'an', 'in', 'on', 'at', 'to', 'for',
    'with', 'by', 'up', 'down', 'out', 'off', 'as', 'be', 'been', 'being',
    'not', 'but', 'so', 'if', 'all', 'one', 'two', 'its', 'his', 'her',
    'am', 'are', 'is', 'was', 'were', 'do', 'does', 'did', 'has', 'have',
    'had', 'will', 'would', 'can', 'could', 'must', 'should', 'may',
    'might', 'there', 'here', 'this', 'that', 'these', 'those', 'i', 'you',
    'he', 'she', 'it', 'we', 'they', 'me', 'him', 'us', 'them', 'my',
    'your', 'our', 'their', 'mine', 'yours',
}
TEACHER_TALK = {
    'meaning', 'answer', 'answers', 'phrase', 'phrases', 'response', 'word',
    'words', 'number', 'numbers', 'day', 'days', 'vocabulary', 'contracted',
    'contraction', 'contractions', 'stress', 'pronunciation', 'question',
    'questions', 'form', 'forms', 'ending', 'endings', 'translation', 'board',
    'class', 'student', 'students', 'spelling', 'alphabet', 'sentence',
    'sentences', 'instruction', 'instructions', 'activity', 'activities',
    'support', 'idea', 'note', 'notes', 'key', 'example', 'examples',
    'exercise', 'exercises', 'sound', 'sounds', 'lexis', 'drill', 'model',
    'choral', 'pairwork', 'worksheet', 'worksheets', 'audio', 'video',
    'photo', 'photos', 'picture', 'pictures', 'map', 'chart', 'dialogue',
    'text', 'title', 'topic', 'rule', 'rules', 'verb', 'verbs', 'noun',
    'nouns', 'adjective', 'adjectives', 'preposition', 'prepositions',
    'singular', 'plural', 'positive', 'negative', 'just', 'only', 'any',
    'which', 'who', 'whose', 'how', 'what', 'where', 'when', 'why',
    'from', 'onto', 'before', 'after', 'first', 'second', 'name', 'sit',
    'thanks', 'yes', 'no', 'ese', 'ian', 'ish', 'language',
}


def load_pages():
    txt = open(TG_TXT, encoding='utf-8').read()
    parts = re.split(r'(?m)^@@PAGE (\d+)@@$', txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def lesson_map(pm):
    """pdf page -> lesson code from running heads inside the plan region."""
    lm = {}
    current = None
    for p in range(PLAN_START, PLAN_END + 1):
        t = pm.get(p, '')
        opener = re.search(r'(?m)^\s*(%s)\s+[A-Z#“”"\t][^\n]{2,50}$' % CODE_RE, t[:400])
        head = re.search(r'(?m)^\s*\d{1,3}\s*\n\s*(%s)\s*$' % CODE_RE, t[:120])
        bare = re.search(r'(?m)^\s*(%s)\s*$' % CODE_RE, t[:120])
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
    if re.search(r"\b(is|are|am|was|were|do|does|did|have|has|had|'m|'s|'re)\b", low) \
       and len(words) > 2:
        return False
    if re.match(r'^(e\s)?\d{1,2}\.\d+$', low) or re.match(r'^p?\.?\d+$', low):
        return False
    if not re.search(r'[A-Za-z]', w):
        return False
    if low in TEACHER_TALK or low in FUNCTION:
        return False
    if any(t in TEACHER_TALK or t in FUNCTION for t in low.split() if len(t) > 2) and len(words) > 1:
        return False
    return True


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
    out = []
    for m in TEACH.finditer(t):
        w = norm_word(m.group(1))
        if plausible_head(w):
            out.append((w, m.group(2).strip() if m.group(2) else None))
    return out


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
    """Comma-separated answer lists on Vocabulary activity instruction pages."""
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
            for g in good:
                if plausible_head(g):
                    out.append(g)
    return out


def main():
    pm = load_pages()
    lm = lesson_map(pm)
    cands = []

    def add(w, lesson, page, ev, ctx=''):
        cands.append({'en': w, 'lesson': lesson, 'page': page,
                      'evidence': ev, 'context': ctx[:140]})

    for p, lesson in sorted(lm.items()):
        t = pm.get(p, '')
        for w in extract_keys(t):
            add(w, lesson, p, 'key')
        for w, ipa in extract_teach(t):
            add(w, lesson, p, 'teach', ipa or '')
        for w in extract_notes(t):
            add(w, lesson, p, 'notes')

    # Vocabulary activity instruction pages: attribute each block by the
    # lesson code at its head ("2A  Things" / "PE1  …").
    for p in VOCAB_INSTR:
        t = pm.get(p, '')
        marks = list(re.finditer(r'(?m)^[ \t]*(\d{1,2}[ABC]|PE\d)[\t ]', t))
        for i, m in enumerate(marks):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(t)
            body = t[m.end():end]
            for w in extract_instr_lists(body):
                add(w, m.group(1), p, 'list')
            for w in extract_keys(body):
                add(w, m.group(1), p, 'key')

    def lkey(c):
        m = re.match(r'PE(\d+)', c)
        if m:
            return (int(m.group(1)) * 2, 'Z')
        m = re.match(r'(\d+)([ABC])', c)
        return (int(m.group(1)), m.group(2)) if m else (99, 'Z')

    best = {}
    for c in cands:
        k = (c['lesson'], c['en'].lower())
        if k not in best:
            best[k] = c
    per_word = {}
    for c in best.values():
        k = c['en'].lower()
        if k not in per_word or lkey(c['lesson']) < lkey(per_word[k]['lesson']):
            per_word[k] = c
    final = sorted(per_word.values(), key=lambda c: (lkey(c['lesson']), c['en'].lower()))

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
    print(f'candidates: {len(final)} distinct headwords', dict(Counter(c['evidence'] for c in final)))
    print(f'already in elementary.json (incl. syn/coll): {len(final) - len(new)}')
    print(f'NEW candidates: {len(new)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
