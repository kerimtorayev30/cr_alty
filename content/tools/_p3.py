LESSONS = {
    '1A': (1,  'Why did they call you that?', 'names', ['names']),
    '1B': (1,  'Life in colour', 'adjectives · adjective suffixes', ['adj_suffixes']),
    '2A': (2,  'Get ready! Get set! Go!', 'packing', ['packing']),
    '2B': (2,  'Go to checkout', 'shops and services', ['shops_services']),
    '3A': (3,  'Grow up!', 'stages of life', ['stages_life']),
    '3B': (3,  'Photo albums', 'photography', ['photography']),
    '4A': (4,  "Don't throw it away!", 'rubbish and recycling', ['recycling']),
    '4B': (4,  'Put it on your CV', 'study and work', ['study_work']),
    '5A': (5,  'Screen time', 'television', ['television']),
    '5B': (5,  'A quiet life?', 'the country', ['country']),
    '6A': (6,  'What the waiter really thinks', 'at a restaurant', ['restaurant']),
    '6B': (6,  'Do it yourself', 'DIY and repairs', ['diy']),
    '7A': (7,  'Take your cash', 'cash machines · phrasal verbs', ['money_phrasal']),
    '7B': (7,  'Shall we go out or stay in?', 'live entertainment', ['live_entertainment']),
    '8A': (8,  'Treat yourself', 'looking after yourself', ['looking_after']),
    '8B': (8,  'Sites and sights', 'wars and battles · historic buildings', ['historic']),
    '9A': (9,  'Total recall', 'word building', ['word_building3']),
    '9B': (9,  'Here comes the bride', 'weddings', ['weddings']),
    '10A': (10, 'The land of the free?', 'British and American English', ['brit_amer']),
    '10B': (10, 'Please turn over your papers', 'exams', ['exams']),
}

WORD_LESSON = {}


def lesson_for(topic, en, fallback):
    key = en.strip().lower()
    return WORD_LESSON.get(key, fallback)


# Intermediate Plus has ten units; the five Practical English episodes sit
# after units 1, 3, 5, 7 and 9 in the book. In the data they carry unit 11 so
# they do not collide with the real units, and the app shows each episode
# right after the unit it follows.
PE_UNIT = 11
for code, n, title, topic, key in (
    ('PE1', 11, 'Reporting lost luggage', 'practical English episode 1', 'pe_luggage'),
    ('PE2', 11, 'Renting a car', 'practical English episode 2', 'pe_rentcar'),
    ('PE3', 11, 'Making a police report', 'practical English episode 3', 'pe_police'),
    ('PE4', 11, 'Talking about house rules', 'practical English episode 4', 'pe_house_rules'),
    ('PE5', 11, 'Giving directions in a building', 'practical English episode 5', 'pe_directions'),
):
    LESSONS[code] = (PE_UNIT, title, topic, [key])


def lesson_sort_key(code):
    m = re.match(r'^(\d+)(.*)$', code)
    if m:
        return (int(m.group(1)), m.group(2))
    return (11, code)


def main():
    words, seen, dups = [], {}, []

    for lesson in sorted(LESSONS, key=lesson_sort_key):
        unit, title, topic, topics = LESSONS[lesson]
        if lesson[0].isdigit() and lesson[:-1] != str(unit):
            raise SystemExit(f'lesson {lesson} says unit {unit}')
        for t in topics:
            if t not in T:
                raise SystemExit(f'lesson {lesson} refers to unknown topic "{t}"')
            for e in T[t]:
                if lesson_for(t, e[0], lesson) != lesson:
                    continue   # this word belongs to another lesson
                en, ipa, pos, tm, ru, de, ex, exTm, cefr = e[:9]
                coll = e[9] if len(e) > 9 else ''
                key = en.strip().lower()
                if key in seen:
                    dups.append(f'{lesson}: "{en}" (already in {seen[key]})')
                    continue
                seen[key] = lesson
                words.append({
                    'en': en, 'ipa': ipa, 'pos': pos, 'tm': tm, 'ru': ru,
                    'def': de, 'ex': ex, 'exTm': exTm, 'cefr': cefr,
                    'ox': 'Oxford 3000' if cefr in ('A1', 'A2') else 'Oxford 5000',
                    'syn': '—', 'coll': coll or '—', 'stage': 'New',
                    'books': [{'book': 'intp', 'unit': unit, 'lesson': lesson}],
                    'proofread': False,
                })

    if dups:
        raise SystemExit('duplicate headwords:\n  ' + '\n  '.join(dups))

    used = set(t for ts in LESSONS.values() for t in ts[3])
    unused = sorted(set(T) - used)
    if unused:
        raise SystemExit('topics declared but never used by a lesson: ' + ', '.join(unused))

    lessons = []
    empty = []
    for lesson in sorted(LESSONS, key=lesson_sort_key):
        unit, title, topic, topics = LESSONS[lesson]
        n = sum(1 for w in words if w['books'][0]['lesson'] == lesson)
        if not n:
            empty.append(lesson)
            continue
        lessons.append({'lesson': lesson, 'unit': unit, 'title': title, 'topic': topic,
                        'words': n})
    if empty:
        raise SystemExit('lessons with no words — fill them: ' + ', '.join(empty))

    pack = {
        'book': 'intp',
        'title': 'English File Intermediate Plus (4th edition) — vocabulary, by lesson',
        'lessons': lessons,
        'words': words,
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(pack, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print(f'wrote {os.path.normpath(OUT)}: {len(words)} words, {len(lessons)} lessons')
    by_unit = {}
    for l in lessons:
        by_unit.setdefault(l['unit'], []).append(l)
    for unit in sorted(by_unit):
        print(f"\nunit {unit:>2} — {sum(l['words'] for l in by_unit[unit])} words")
        for l in by_unit[unit]:
            print(f"    {l['lesson']:<4} {l['words']:>3} words  {l['title']}")


if __name__ == '__main__':
    main()
