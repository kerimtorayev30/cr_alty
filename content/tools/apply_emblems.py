#!/usr/bin/env python3
"""Richer league emblems.

The old tier shields were flat: one gradient and a single glyph. Each tier now
gets a proper medal — darker rim, inner bezel line, a soft highlight, and a
distinct emblem with its own outline: bronze a star, silver two rising bars,
gold a crowned star, sapphire a diamond, emerald a laurel leaf, legend a crown.
The gradient ids stay the ones the old symbols used (gbz gsv ggd gsp gem2 glg)
so nothing else in the file has to change.
"""
import re
import sys

P = 'uploads/app-yatla.html'
h = open(P, encoding='utf-8').read()

SHIELD = ('<path d="M12 1.6 20.2 4.8v6.5c0 5.3-3.4 9.4-8.2 11.1C7.2 20.7 3.8 16.6 3.8 11.3V4.8z" '
          'fill="url(#%s)" stroke="%s" stroke-width=".7"/>'
          '<path d="M12 3.5 18.6 6v5.3c0 4.4-2.7 7.8-6.6 9.4-3.9-1.6-6.6-5-6.6-9.4V6z" '
          'fill="none" stroke="%s" stroke-width=".8"/>'
          '<ellipse cx="9.2" cy="6.2" rx="3.6" ry="1.6" fill="rgba(255,255,255,.32)" transform="rotate(-16 9.2 6.2)"/>')

SYMS = {
    'i-tbz': ('gbz', ['#F0AE74', '#C67B33', '#8A5222'], '#5F3D1B', 'rgba(255,240,220,.55)',
              '<path d="M12 6.8l1.7 3.3 3.6.5-2.6 2.6.6 3.6L12 15.1l-3.3 1.7.6-3.6-2.6-2.6 3.6-.5z" fill="#FFE9CF" stroke="#7A4A1D" stroke-width=".5"/>'),
    'i-tsv': ('gsv', ['#F5F8FB', '#AEB9C5', '#78838F'], '#4C565F', 'rgba(255,255,255,.6)',
              '<path d="M8.4 15.6v-4.4l2.2 1.4v4z M12.1 16.6V9.4l2.2 1.4v5.8z" fill="#F8FAFC" stroke="#5A6570" stroke-width=".5"/>'),
    'i-tgd': ('ggd', ['#FFEDA6', '#F5C33B', '#C88A12'], '#8F6206', 'rgba(255,250,220,.65)',
              '<path d="M12 6.4l1.8 3.5 3.9.6-2.8 2.7.7 3.9L12 15.2l-3.6 1.9.7-3.9-2.8-2.7 3.9-.6z" fill="#FFF6D8" stroke="#9A6A08" stroke-width=".55"/>'
              '<circle cx="12" cy="4.6" r="1" fill="#FFF6D8" stroke="#9A6A08" stroke-width=".4"/>'),
    'i-tsp': ('gsp', ['#A5D5FF', '#3B82F6', '#1E40AF'], '#12308F', 'rgba(230,245,255,.5)',
              '<path d="M12 6.6l4.2 4.7-4.2 5-4.2-5z" fill="#EAF5FF" stroke="#173E9E" stroke-width=".55"/>'
              '<path d="M12 6.6l4.2 4.7H7.8z" fill="rgba(255,255,255,.55)"/>'),
    'i-tem': ('gem2', ['#8DF0AC', '#22C55E', '#047857'], '#03543F', 'rgba(235,255,245,.5)',
              '<path d="M12 6.2c3.4 1.6 5 4.3 5 7.2-1.6 1.2-3.3 1.8-5 1.8s-3.4-.6-5-1.8c0-2.9 1.6-5.6 5-7.2z" fill="#E9FCEF" stroke="#04604A" stroke-width=".55"/>'
              '<path d="M12 7.4v6.8" stroke="#04604A" stroke-width=".6"/>'),
    'i-tlg': ('glg', ['#F0ABFC', '#A855F7', '#DB2777'], '#7A1B52', 'rgba(255,235,250,.55)',
              '<path d="M7.6 15.8l-.9-6.2 3.1 2L12 7.6l2.2 4 3.1-2-.9 6.2z" fill="#FFF0FA" stroke="#8C2160" stroke-width=".55"/>'
              '<circle cx="12" cy="5.6" r=".9" fill="#FFF0FA" stroke="#8C2160" stroke-width=".4"/>'),
}

for sid, (gid, stops, rim, bezel, glyph) in SYMS.items():
    pat = re.compile(r'<symbol id="' + sid + r'" viewBox="0 0 24 24">.*?</symbol>', re.S)
    defs = ('<defs><linearGradient id="%s" x1="0" y1="0" x2="%s" y2="1">%s</linearGradient></defs>'
            % (gid, '1' if sid == 'i-tlg' else '0',
               ''.join('<stop offset="%s" stop-color="%s"/>' % (off, c)
                       for off, c in zip(('0', '.55', '1'), stops))))
    body = SHIELD % (gid, rim, bezel) + glyph
    new = '<symbol id="%s" viewBox="0 0 24 24">%s%s</symbol>' % (sid, defs, body)
    h, n = pat.subn(new, h, count=1)
    if n != 1:
        sys.exit(f'ABORT: {sid} replaced {n} times')
    print('  -', sid)

open(P, 'w', encoding='utf-8').write(h)
print(f'{len(h.encode("utf-8")):,} bytes')
