#!/usr/bin/env python3
"""Round 5 app patch — Upper-Intermediate import.

1. BOOKS: upp 12->10 real units + pe map (CE1-CE5 after units 1,3,5,7,9), dl:1.
2. Units view: the episode-unit lookup no longer hardcodes "PE1" — it scans
   LESSONS for any lesson whose unit number is above the book's real units,
   so both PE# and CE# codes interleave.
3. Row/lessons-header label picks ce_w ("Colloquial English") for upp.
4. i18n: ce_w in en/tk/ru.
"""
import shutil

APP = '/home/user/uploads/app-yatla.html'
s = open(APP, encoding='utf-8').read()
orig_len = len(s)
n = 0


def rep(old, new, label):
    global s, n
    assert s.count(old) == 1, f'{label}: anchor count {s.count(old)}'
    s = s.replace(old, new)
    n += 1
    print(f'  [{n:02}] {label}')


rep('units:12,done:0,dl:0,mb:31',
    'units:10,pe:{1:"CE1",3:"CE2",5:"CE3",7:"CE4",9:"CE5"},done:0,dl:1,mb:28',
    'BOOKS upp: 10 real units + pe map, dl:1')

rep('(function(){const PU=(lessonInfo(b.id,"PE1")||{}).unit,out=[];',
    '(function(){let PU=0;for(const k in LESSONS){if(k.slice(0,b.id.length+1)===b.id+"|"&&LESSONS[k].unit>b.units)PU=LESSONS[k].unit;}const out=[];',
    'episode-unit lookup works for PE# and CE# codes')

rep('${t("pe_w")}${inf&&inf.topic?" \u00b7 "+inf.topic:""}',
    '${b.id==="upp"?t("ce_w"):t("pe_w")}${inf&&inf.topic?" \u00b7 "+inf.topic:""}',
    'PE/CE row label per book')

rep('${un>b.units?t("pe_w"):t("unit_w")+" "+un}',
    '${un>b.units?(b.id==="upp"?t("ce_w"):t("pe_w")):t("unit_w")+" "+un}',
    'lessons header label per book')

rep('pe_w:"Practical English",chal2d:',
    'pe_w:"Practical English",ce_w:"Colloquial English",chal2d:',
    'i18n en: ce_w')
rep('pe_w:"Praktiki i\u0148lis dili",chal2d:',
    'pe_w:"Praktiki i\u0148lis dili",ce_w:"Geple\u015fik i\u0148lis dili",chal2d:',
    'i18n tk: ce_w')
rep('pe_w:"\u041f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0430\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439",chal2d:',
    'pe_w:"\u041f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0430\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439",ce_w:"\u0420\u0430\u0437\u0433\u043e\u0432\u043e\u0440\u043d\u044b\u0439 \u0430\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439",chal2d:',
    'i18n ru: ce_w')

for marker in ('function renderLearning', '/* ================= INIT', 'GLOBAL.YatlaContent = api'):
    assert marker in s, f'marker lost: {marker}'

shutil.copyfile(APP, APP + '.bak')
open(APP, 'w', encoding='utf-8').write(s)
print(f'\n{n} patches applied. {orig_len} -> {len(s)} bytes ({len(s)-orig_len:+d})')
