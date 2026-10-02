#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Embed the general search dictionary (content/dict-general.json) into the app
as an inline <script type="application/json" id="yatlaDict"> tag, mirroring how
the curated word pack (yatlaWords) is embedded. Idempotent: re-running replaces
the existing tag in place. Keeps the single-file, offline, no-network rule."""
import io, json, re, sys

APP = "uploads/app-yatla.html"
DATA = "content/dict-general.json"

def main():
    html = io.open(APP, encoding="utf-8").read()
    raw = io.open(DATA, encoding="utf-8").read().strip()
    obj = json.loads(raw)  # validate it parses
    n = len(obj.get("rows", []))
    # A JSON blob inside <script> must not contain a literal closing tag.
    assert "</script" not in raw.lower(), "dict JSON contains </script"
    tag = '<script type="application/json" id="yatlaDict">%s</script>' % raw
    pat = re.compile(r'<script type="application/json" id="yatlaDict">.*?</script>', re.S)
    if pat.search(html):
        html = pat.sub(lambda m: tag, html, count=1)
        action = "replaced"
    else:
        idx = html.index("</head>")
        html = html[:idx] + tag + "\n" + html[idx:]
        action = "inserted"
    io.open(APP, "w", encoding="utf-8").write(html)
    print("%s yatlaDict tag with %d general words; app now %d bytes"
          % (action, n, len(html.encode("utf-8"))))

if __name__ == "__main__":
    main()
