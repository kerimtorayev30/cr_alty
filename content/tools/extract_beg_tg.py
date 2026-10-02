#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract taught-vocabulary candidates from the English File Beginner
Teacher's Guide PDF (text layer), with full source evidence.

WHY THE TEACHER'S GUIDE
-----------------------
The Student's Book PDFs the owner supplied are scans with NO text layer, and
this sandbox has no OCR binary. The Teacher's Guide has a real text layer and
is, per the owner, where most of the missing new words are visible. Every
candidate below therefore carries TG evidence — page, lesson, and the kind of
evidence — so nothing is invented (§12) and nothing is attributed by topic
guesswork (§13).

EVIDENCE TIERS (spec §14 / §16)
-------------------------------
  wordbank   HIGH   an explicit word list on a photocopiable VOCABULARY
                    worksheet for that exact lesson ("Egypt England France …")
  key        HIGH   the answer key of a numbered vocabulary exercise inside
                    that lesson's plan ("2 American   3 Chinese   4 Swiss")
  teach      HIGH   the plan says to teach/elicit the word, often with IPA
                    ("teach zero /ˈzɪərəʊ/")
  notes      MEDIUM the word is explained/illustrated in a "Vocabulary notes"
                    box (e.g. lists after "e.g.")
Everything else in the TG — teacher instructions, grammar sentence keys,
classroom management prose — is NOT scanned, because that language is spoken
TO teachers, not taught TO students.

LESSON ATTRIBUTION
------------------
Lesson-plan pages (TG 12-132) carry the lesson code in their running head;
photocopiables (133-225) carry "<code> VOCABULARY <topic>" page headers. File
boundaries come from the TG contents page. "Revise and Check" pages are
revision of earlier lessons (§7) and are skipped as a source.

Output: content/pdf/beg-tg-candidates.json + a diff against content/data/
beginner.json so curation only looks at genuinely NEW items.

Usage: python3 content/tools/extract_beg_tg.py
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TG_TXT = os.path.join(HERE, '..', 'pdf', 'beg-tg.txt')
EXISTING = os.path.join(HERE, '..', 'data', 'beginner.json')
OUT = os.path.join(HERE, '..', 'pdf', 'beg-tg-candidates.json')

# TG contents page: File -> first TG page of its lesson plans
FILE_START = {1: 12, 2: 25, 3: 35, 4: 45, 5: 54, 6: 65, 7: 75, 8: 87,
              9: 97, 10: 108, 11: 117, 12: 128}
PHOTOCOPY_START = 133

CODE_RE = r'(\d{1,2}[ABC]|PE\d)'


def load_pages():
    txt = open(TG_TXT, encoding='utf-8').read()
    parts = re.split(r'(?m)^@@PAGE (\d+)@@$', txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def file_of_page(p):
    f = None
    for n, start in FILE_START.items():
        if p >= start:
            f = n
    return f


def lesson_map(pm):
    """pdf page -> lesson code, from running heads / lesson openers."""
    lm = {}
    current = None
    for p in range(12, PHOTOCOPY_START):
        t = pm.get(p, '')
        # lesson opener: "1A\n12\n 1A A cappuccino, please" or "20\nPE1\n"
        m = re.search(r'(?m)^\s*(%s)\s*$' % CODE_RE, t[:120])
        opener = re.search(r'(?m)^\s*(%s)\s+[A-Z#“"][^\n]{2,50}$' % CODE_RE, t[:400])
        head = re.search(r'(?m)^\s*\d{1,3}\s*\n\s*(%s)\s*$' % CODE_RE, t[:120])
        if opener:
            current = opener.group(1)
        elif head:
            current = head.group(1)
        elif m:
            current = m.group(1)
        # Revise and Check pages belong to no single lesson
        if re.search(r'Revise and Check', t[:300]):
            current = None
        if current:
            lm[p] = current
    return lm


def norm_word(w):
    w = unicodedata.normalize('NFC', w.strip())
    w = re.sub(r'^[•●\-\u2022\s]+', '', w)
    w = re.sub(r'^[Aa]n?\s+', '', w) if re.match(r'^[Aa]n?\s+[a-z]', w) else w
    w = w.strip(' .,;:!?()"“”‘’')
    w = re.sub(r'\s{2,}', ' ', w)
    return w


# TG prose is written TO teachers; these words are the furniture of lesson
# plans, not student vocabulary. Structural filters already keep prose out of
# keys/banks; this catches the residue inside teach/elicit/notes captures.
TEACHER_TALK = {
    'meaning', 'answer', 'answers', 'phrase', 'phrases', 'response', 'word',
    'words', 'number', 'numbers', 'day', 'days', 'vocabulary', 'contracted',
    'contraction', 'contractions', 'stress', 'pronunciation', 'question',
    'questions', 'form', 'forms', 'ending', 'endings', 'translation', 'board',
    'class', 'student', 'students', 'spelling', 'alphabet', 'sentence',
    'sentences', 'instruction', 'instructions', 'activity', 'activities',
    'support', 'idea', 'note', 'notes', 'key', 'example', 'examples', 'price',
    'exercise', 'exercises', 'sound', 'sounds', 'ending', 'lexis', 'drill',
    'model', 'choral', 'pairwork', 'worksheet', 'worksheets', 'audio', 'video',
    'photo', 'photos', 'picture', 'pictures', 'map', 'chart', 'dialogue',
    'text', 'title', 'topic', 'rule', 'rules', 'verb', 'verbs', 'noun',
    'nouns', 'adjective', 'adjectives', 'preposition', 'prepositions',
    'singular', 'plural', 'positive', 'negative', 'short answer', 'stress in',
    'just', 'only', 'any', 'which', 'who', 'whose', 'how', 'what', 'where',
    'when', 'why', 'that', 'this', 'these', 'those', 'from', 'onto', 'before',
    'after', 'first', 'second', 'here', 'there', 'too', 'name', 'sit', 'is',
    'isn', 'aren', 'thanks', 'you', 'yes', 'no', 'ese', 'ian', 'ish', 'an',
}


def plausible_head(w):
    if not w or len(w) < 2 or len(w) > 48:
        return False
    words = w.split()
    if len(words) > 5:
        return False
    # must be letters/digits/'-. /() only
    if not re.match(r"^[A-Za-z0-9'’\-\.\s/()]+$", w):
        return False
    low = w.lower()
    # no sentence-like content
    if re.search(r"\b(is|are|am|was|were|do|does|did|have|has|had|'m|'s|'re)\b", low) \
       and len(words) > 2:
        return False
    # no audio codes / page refs / numbers-only
    if re.match(r'^(e\s)?\d{1,2}\.\d+$', low) or re.match(r'^p?\.?\d+$', low):
        return False
    # at least one alphabetic char
    if not re.search(r'[A-Za-z]', w):
        return False
    if low in TEACHER_TALK or low in {
        'of', 'the', 'and', 'or', 'a', 'an', 'in', 'on', 'at', 'to', 'for',
        'with', 'by', 'up', 'down', 'out', 'off', 'as', 'be', 'been', 'being',
        'not', 'but', 'so', 'if', 'all', 'one', 'two', 'its', 'his', 'her',
    }:
        return False
    if any(t in TEACHER_TALK for t in low.split() if len(t) > 2) and len(words) > 1:
        return False
    return True


def extract_wordbank(t):
    """Explicit word lists on photocopiable VOCABULARY worksheets."""
    out = []
    body = t
    m = re.search(r'(?m)^\s*\d{1,2}[ABC]|PE\d\s+VOCABULARY', t)
    act = body.find('ACTIVATION')
    if act > 0:
        body = body[:act]
    for line in body.split('\n'):
        line = line.strip()
        if len(line) < 12 or len(line) > 200:
            continue
        # instruction sentences end with a period or start with a verb
        if line.endswith('.') or re.match(r'^(Look|Find|Write|Complete|Work|Cover|Test|Say|Match|Put|Choose|Add|Use)\b', line):
            continue
        if re.search(r'Photocopiable|Oxford|Copyright|Teacher’s Guide|English File', line):
            continue
        toks = line.split(' ')
        if len(toks) < 3:
            continue
        if any(len(x) < 2 for x in toks):
            continue
        # a word bank: mostly single-word tokens, no sentence glue
        if sum(1 for x in toks if re.match(r"^[A-Za-z][A-Za-z'’\-]*,?$", x)) >= len(toks) * 0.8:
            for x in toks:
                w = norm_word(x)
                if plausible_head(w):
                    out.append(w)
    return out


KEY_PAIR = re.compile(r'\b(\d{1,2})\s{1,3}([A-Za-z][^\d\n]{0,38}?)(?=\s{2,}\d{1,2}\s|\s*$)')


def extract_keys(t):
    """Answer keys of numbered exercises: '2 American   3 Chinese   4 Swiss'."""
    out = []
    for line in t.split('\n'):
        pairs = KEY_PAIR.findall(line.rstrip())
        if len(pairs) < 3:
            continue
        if re.search(r"\b(I|he|she|it|we|you|they)\b|[’'](?:m|s|re|ll|ve)|\?|\bWhat\b|\bWhere\b", line):
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
    """Words explained inside Vocabulary notes blocks."""
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


def photocopiable_code(t):
    """(lesson code, worksheet kind) from a photocopiable page header.

    Written out rather than built from CODE_RE on purpose: interpolating a
    pattern that already contains a capture group shifts every group index by
    one, which silently turned the kind into the code and skipped all 19
    vocabulary worksheets. `\\s*` is also wrong here — with MULTILINE, \\s
    matches the newline itself, so ^ anchors at the wrong line.
    """
    m = re.search(r'(?m)^[ \t]*(\d{1,2}[ABC]|PE\d)[ \t]+'
                  r'(VOCABULARY|GRAMMAR|PRONUNCIATION)\b', t)
    return (m.group(1), m.group(2)) if m else (None, None)


def main():
    pm = load_pages()
    lm = lesson_map(pm)
    cands = []

    def add(w, lesson, section, page, ev, ctx=''):
        cands.append({'en': w, 'lesson': lesson, 'section': section,
                      'page': page, 'evidence': ev, 'context': ctx[:140]})

    # ---- lesson plans (TG 12-132) ----
    for p, lesson in sorted(lm.items()):
        t = pm.get(p, '')
        section = 'vocabulary'
        for w in extract_keys(t):
            add(w, lesson, section, p, 'key')
        for w, ipa in extract_teach(t):
            add(w, lesson, section, p, 'teach', ipa or '')
        for w in extract_notes(t):
            add(w, lesson, section, p, 'notes')

    # ---- photocopiables (TG 133-225) ----
    # A PDF page can carry more than one worksheet (and the section cover page
    # quotes other sheets as examples), so attribution is per header region,
    # not per page: text between two headers belongs to the first one.
    hdr = re.compile(r'(?m)^[ \t]*(\d{1,2}[ABC]|PE\d)[ \t]+'
                     r'(VOCABULARY|GRAMMAR|PRONUNCIATION)\b')
    for p in range(PHOTOCOPY_START, 226):
        t = pm.get(p, '')
        ms = list(hdr.finditer(t))
        for i, m in enumerate(ms):
            code, kind = m.group(1), m.group(2)
            if kind != 'VOCABULARY':
                continue
            end = ms[i + 1].start() if i + 1 < len(ms) else len(t)
            # start below the header line: its topic ("Nationalities and
            # languages") is a title, not a bank of words to extract
            nl = t.find('\n', m.end())
            body = t[nl + 1:end] if nl != -1 else ''
            # a token that also occurs in the possessive ("Brenda's") is a
            # person's name in an example sentence, not target vocabulary
            names = {g.lower() for g in re.findall(r"\b([A-Z][a-z]{1,12})'s\b", body)}
            for w in extract_wordbank(body):
                if w.lower() in names or w.lower().rstrip("'s") in names:
                    continue
                add(w, code, 'vocabulary', p, 'wordbank')
            for w in extract_keys(body):
                if w.lower() in names:
                    continue
                add(w, code, 'vocabulary', p, 'key')

    # ---- dedupe: first occurrence per lesson, then earliest lesson (§6/§7) ----
    def lkey(c):
        m = re.match(r'(\d+)', c)
        return (int(m.group(1)) if m else 99, c)

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

    # ---- diff against the existing curated beginner pack ----
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
    print(f'candidates: {len(final)} distinct headwords '
          f'({len([c for c in final if c["evidence"] == "wordbank"])} wordbank, '
          f'{len([c for c in final if c["evidence"] == "key"])} key, '
          f'{len([c for c in final if c["evidence"] == "teach"])} teach, '
          f'{len([c for c in final if c["evidence"] == "notes"])} notes)')
    print(f'already in beginner.json (incl. syn/coll): {len(final) - len(new)}')
    print(f'NEW candidates: {len(new)} -> review these for curation')
    for c in new:
        print(f"  {c['lesson']:<4} [{c['evidence']:<8}] p.{c['page']:<3} {c['en']}"
              + (f"  {c['context']}" if c['context'] else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
