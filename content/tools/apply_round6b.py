#!/usr/bin/env python3
"""Round 6b — union book refs when a seed/earlier word wins the headword slot.

The content-pack merge keeps seed words for their stage/definition, but it
dropped the incoming pack word's book references, so a lesson could silently
lose a word (adv 10B lost "job" to the 12-word seed bank). Now, when an
existing word wins, we union the incoming word's book refs onto it. WORDS
length is unchanged (no new entries); only book refs are added, which makes
lessonWords/unitCount match the pack's recorded counts exactly.
"""
import shutil

APP = '/home/user/uploads/app-yatla.html'
s = open(APP, encoding='utf-8').read()
orig_len = len(s)

old = '''  var have={};WORDS.forEach(function(w){have[w.en.toLowerCase()]=1;});
  var added=0;
  r.words.forEach(function(w){
    if(!w||!w.en||have[w.en.toLowerCase()])return;   // seed words keep their stages
    have[w.en.toLowerCase()]=1;
    WORDS.push(w);                                   // in-place: every existing
    added++;                                         // WORDS reference stays valid
  });'''
new = '''  var have={},byEn={};
  WORDS.forEach(function(w){var k=w.en.toLowerCase();have[k]=1;byEn[k]=w;});
  var added=0,touched=0;
  r.words.forEach(function(w){
    if(!w||!w.en)return;
    var k=w.en.toLowerCase();
    if(have[k]){
      /* An earlier word (a seed, or an earlier pack row) keeps its stage and
         definition, but we union this row's book refs so no lesson silently
         loses a word when its headword also lives in the seed bank. */
      var ex=byEn[k];
      if(ex&&w.books&&w.books.length){
        if(!ex.books)ex.books=[];
        w.books.forEach(function(b){
          if(!ex.books.some(function(y){return y.book===b.book&&y.unit===b.unit&&y.lesson===b.lesson;})){ex.books.push(b);touched++;}
        });
      }
      return;
    }
    have[k]=1;byEn[k]=w;
    WORDS.push(w);                                   // in-place: every existing
    added++;                                         // WORDS reference stays valid
  });'''
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)

# the render guard must also fire when we only unioned refs (added may be 0)
old2 = '  if(!added)return;\n  if(S.lv&&S.lv.view===\"books\")renderLearning();'
assert s.count(old2) == 1, s.count(old2)
s = s.replace(old2, '  if(!added&&!touched)return;\n  if(S.lv&&S.lv.view===\"books\")renderLearning();')

for marker in ('function renderLearning', '/* ================= INIT', 'GLOBAL.YatlaContent = api'):
    assert marker in s, f'marker lost: {marker}'

shutil.copyfile(APP, APP + '.bak')
open(APP, 'w', encoding='utf-8').write(s)
print(f'round6b applied. {orig_len} -> {len(s)} bytes ({len(s)-orig_len:+d})')
