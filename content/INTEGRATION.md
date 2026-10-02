# How the content pipeline is wired into `app-yatla.html`

**Status: applied and verified.** `./verify.sh` from the workspace root runs all five
stages; the last run reported `ALL CHECKS PASSED`.

This file records what the patch does and why, so the next change to either side can
be made safely. If you revert the app from `app-yatla.html.bak`, re-run
`python3 content/tools/apply_patch.py`.

## The three insertions

Applied by `content/tools/apply_patch.py`, which aborts unless each anchor occurs
exactly once.

1. **Loader IIFE** immediately before `/* ================= DATA ================= */`.
   Self-contained; only touches `globalThis.YatlaContent`, so it cannot collide with
   `$`, `$$`, `t()`, `go()`, `sfx()` or `hz()`.
2. **One i18n key**, added to all three dictionaries in the same edit (§4.2):

   | key | en | tk | ru |
   |---|---|---|---|
   | `pack_on` | `{n} words ready` | `{n} söz taýýar` | `Готово слов: {n}` |

3. **Pack load** at the end of `/* ================= INIT ================= */`, after
   `track("session_start");save();`.

## Pack resolution order

`embedded <script id="yatlaWords">` → IndexedDB → localStorage → the 12 seed `WORDS`
→ network fetch of `content/build/yatla-words.min.json`.

`fetchWords()` never rejects. In the owner's sandboxed preview (no network, no storage)
it resolves `source:"none"`, the app keeps its 12 seed words, and nothing regresses —
asserted by `tests/integration.js` section 8.

## Why words are appended in place

```js
WORDS.push(w);   // not WORDS = [...]
```

`WORDS` is a `const` binding that the renderers close over (`filt()` maps it,
`openWord()` indexes it, `startReview()` spreads it). Rebinding the name would leave
every one of them on the old array. Appending after the 12 seed entries also preserves
`WORDS[5]`, which `#wotdOpen` uses for the word of the day. Seed words are skipped when
they collide with a pack headword, so their memory stages survive.

## Two traps worth remembering

1. **A literal `</script>` inside a JS comment truncates the app.** The HTML parser
   ends a script element at the first `</`+`script` sequence, even inside a comment.
   This broke the first patched build. Write it `<\/script>`; `verify.sh` stage 5
   asserts the file contains exactly one literal `</script>`.
2. **`fetchWords` must return a Promise on every path.** The app calls `.then()`. An
   early `return done(...)` on the embedded path returned a plain object and threw
   `TypeError: …then is not a function`. `await` hides this bug — assert thenable-ness
   explicitly.

## Re-verifying after any change

```bash
./verify.sh                     # all five stages
./verify.sh path/to/other.html  # same suite against a different build
```

Stage 3 (`tests/baseline.js`) is the §8 regression net and must stay green for any
edit, whether or not it touches content. Stage 4 (`tests/integration.js`) is specific
to the pack.
