#!/usr/bin/env python3
"""Round 6 app patch — Advanced import + book ordering.

1. BOOKS adv: 12->10 real units + CE pe map, dl:1, mb:30.
2. Book order: Intermediate Plus (intp) moves to sit right after Intermediate
   and before Upper-Intermediate; Advanced Plus (advp) stays last. New order:
   beg, ele, pre, int, intp, upp, adv, advp.
3. ce_w label already keys off b.id==="upp"; extend it to adv too (both use CE).
"""
import re
import shutil

APP = '/home/user/uploads/app-yatla.html'
s = open(APP, encoding='utf-8').read()
orig_len = len(s)
n = 0


def rep(old, new, label, count=1):
    global s, n
    assert s.count(old) == count, f'{label}: anchor count {s.count(old)} != {count}'
    s = s.replace(old, new)
    n += 1
    print(f'  [{n:02}] {label}')


# 1. adv entry gets its real structure
rep('{id:"adv",t:"Advanced",lv:"C2",c:"linear-gradient(160deg,#A78BFA,#8B5CF6)",units:12,done:0,dl:0,mb:33}',
    '{id:"adv",t:"Advanced",lv:"C2",c:"linear-gradient(160deg,#A78BFA,#8B5CF6)",units:10,pe:{1:"CE1",3:"CE2",5:"CE3",7:"CE4",9:"CE5"},done:0,dl:1,mb:30}',
    'BOOKS adv: 10 real units + CE pe map, dl:1')

# 2. reorder — move the intp line to sit right after the int line
m = re.search(r'\n \{id:"intp"[^\n]*\},', s)
assert m, 'intp line not found'
intp_line = m.group(0)
s = s.replace(intp_line, '')          # pull intp out
n += 1
print('  [02] pulled intp out of its old slot')
# re-insert it right after the int entry line
mi = re.search(r'(\n \{id:"int",t:"Intermediate"[^\n]*\},)', s)
assert mi, 'int line not found'
s = s.replace(mi.group(0), mi.group(0) + intp_line, 1)
n += 1
print('  [03] re-inserted intp right after int')

# 3. ce_w now covers both upp and adv (both use CE episodes)
rep('b.id==="upp"?t("ce_w"):t("pe_w")',
    '(b.id==="upp"||b.id==="adv")?t("ce_w"):t("pe_w")',
    'CE row label per book (upp + adv)', count=2)

# order assertion
order = re.findall(r'\{id:"([a-z]+)",t:', s)
assert order[:8] == ['beg', 'ele', 'pre', 'int', 'intp', 'upp', 'adv', 'advp'], order[:8]
print('  book order now:', ' '.join(order[:8]))

for marker in ('function renderLearning', '/* ================= INIT', 'GLOBAL.YatlaContent = api'):
    assert marker in s, f'marker lost: {marker}'

shutil.copyfile(APP, APP + '.bak')
open(APP, 'w', encoding='utf-8').write(s)
print(f'\n{n} patches applied. {orig_len} -> {len(s)} bytes ({len(s)-orig_len:+d})')
