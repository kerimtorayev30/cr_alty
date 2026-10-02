#!/usr/bin/env python3
"""
Wire the Ýatla content pipeline into app-yatla.html.

Three insertions, each made only after the anchor is confirmed unique:
  1. the content loader IIFE, immediately before the /* DATA */ section
  2. one i18n key (pack_on) added to en, tk and ru simultaneously
  3. the pack-load call at the end of /* INIT */

Deliberately does NOT touch:
  - the WORDS[] seed array (it stays as the offline fallback)
  - any base64 data URI
  - the fixed Home component order

Usage: python3 apply_patch.py [path/to/app-yatla.html]
"""
import re
import shutil
import sys

APP = sys.argv[1] if len(sys.argv) > 1 else '/home/user/uploads/app-yatla.html'
LOADER = '/home/user/content/loader/yatla-content.js'
PACK_URL = 'content/build/yatla-words.min.json'

html = open(APP, encoding='utf-8').read()
loader = open(LOADER, encoding='utf-8').read()
shutil.copyfile(APP, APP + '.bak')

EDITS = []

# --- 1. loader IIFE, before the DATA section --------------------------------
anchor = '/* ================= DATA ================= */'
insert = ('/* ================= CONTENT PACK (loader, inline) ================= */\n'
          + loader.strip() + '\n\n')
EDITS.append((anchor, insert + anchor, 'loader IIFE'))

# --- 2. one new i18n key in all three dictionaries --------------------------
STRINGS = {
    'en:{home:': 'en:{pack_on:"{n} words ready",home:',
    'tk:{home:': 'tk:{pack_on:"{n} söz taýýar",home:',
    'ru:{home:': 'ru:{pack_on:"Готово слов: {n}",home:',
}
for anchor, repl in STRINGS.items():
    EDITS.append((anchor, repl, f'i18n key for {anchor[:2]}'))

# --- 3. pack load at the end of INIT ----------------------------------------
anchor = 'track("session_start");save();'
insert = anchor + '''

/* ================= CONTENT PACK LOAD ================= */
/* Resolution order lives in YatlaContent: embedded <script id="yatlaWords"> →
   IndexedDB → localStorage → the 12 seed WORDS above → network fetch.
   fetchWords never rejects, so a sandboxed preview with no network simply keeps
   the seed words and nothing regresses. */
YatlaContent.fetchWords({url:"''' + PACK_URL + '''"}).then(function(r){
  if(!r.words||!r.words.length)return;
  var have={};WORDS.forEach(function(w){have[w.en.toLowerCase()]=1;});
  var added=0;
  r.words.forEach(function(w){
    if(!w||!w.en||have[w.en.toLowerCase()])return;   // seed words keep their stages
    have[w.en.toLowerCase()]=1;
    WORDS.push(w);                                   // in-place: every existing
    added++;                                         // WORDS reference stays valid
  });
  if(!added)return;
  if(S.lv&&S.lv.view==="books")renderLearning();
  if($("#scr-search").classList.contains("on"))filt();
  refreshHome();
  track("pack_loaded");
  toast(t("pack_on",{n:WORDS.length}));
  save();
});'''
EDITS.append((anchor, insert, 'pack load in INIT'))

# --- apply ------------------------------------------------------------------
for anchor, repl, label in EDITS:
    n = html.count(anchor)
    if n != 1:
        sys.exit(f'REFUSING: anchor "{anchor}" occurs {n} times (expected 1) — aborting, file unchanged')
    html = html.replace(anchor, repl, 1)
    print(f'  applied: {label}')

open(APP, 'w', encoding='utf-8').write(html)
print(f'\npatched {APP} ({len(html)} bytes); backup at {APP}.bak')
