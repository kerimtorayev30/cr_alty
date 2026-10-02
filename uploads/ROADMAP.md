# Ýatla — Ship-It Roadmap

The prototype (`app-yatla.html`) already contains: full EN/TM/RU i18n, dark mode, offline-ready
static bundle, learning engine (book → unit → vocab → review), search dictionary, league,
profile, gamification. Below is the fastest path from prototype to store.

## Phase 1 — Wrap & ship as a real app (≈1–2 weeks)  ← do this first

1. **Capacitor wrapper** (keeps this exact UI, ships to both stores):
   ```bash
   mkdir yatla && cd yatla && npm init -y
   npm i @capacitor/core @capacitor/cli @capacitor/android @capacitor/ios
   npx cap init "Ýatla" com.yatla.app --web-dir=www
   mkdir www && cp ../app-yatla.html www/index.html
   npx cap add android && npx cap add ios && npx cap sync
   npx cap open android   # or: npx cap open ios
   ```
2. **Persistence**: XP / favorites / progress currently live in memory.
   Save `S` to `localStorage` on every mutation; upgrade later to
   `@capacitor/preferences` or SQLite (`@capacitor-community/sqlite`).
3. **Content as data**: move `WORDS`, `BOOKS`, `I18N` out of the HTML into
   `www/data/words.json`, `books.json`, `i18n/{en,tk,ru}.json`, fetched at boot.
   Adding Oxford units then becomes a data task, not a code task.
4. **Audio**: real pronunciation per word — bundle an offline MP3 pack, or use
   the Web Speech API (`speechSynthesis`) as a zero-asset fallback.
5. **Icon / splash**: generate from `ui-assets/mascot-sticker.png`
   (`npx @capacitor/assets --iconColor 58BE2F`).
6. **Store submission**: signing keys, privacy-policy URL, data-safety form,
   Play internal testing track + TestFlight. The app is fully offline, so no
   server review issues.

## Phase 2 — Productize (2–4 weeks)

- **⚠️ Licensing**: Oxford English File word lists / audio are © Oxford University
  Press. Get a license, or ship with your own curated lists first and add OUP
  content after agreement. This is the only legal gate.
- **Smart Memory Engine** (spec Part 5): implement review intervals, memory score,
  difficulty detection as a pure JS module + unit tests.
- **Search index**: swap the 12-word demo for the full dictionary via MiniSearch
  (offline, instant, fuzzy) — the UI already supports it.
- **Native polish**: 150–300 ms animations per spec; confetti on celebrations.
- **Optional cloud sync** (spec Part 10): Supabase/Firebase auth + progress sync
  with an offline queue; app must stay 100% usable without it.
- **Native-speaker pass** over the TM/RU strings (currently machine-drafted).

## Phase 3 — Scale (only if needed)

- If you later need heavier native feel, rebuild the UI in React Native/Flutter
  **reusing this spec, palette, assets and i18n files** — but ship the Capacitor
  MVP first; it already meets the spec's UX rules.

## Pre-submission checklist

- [ ] Real-device QA: low-end Android + iOS, airplane mode end-to-end
- [ ] Dark-mode contrast + reduced-motion check
- [ ] Touch targets ≥44 px, aria-labels on icon buttons
- [ ] Language switch + theme persisted across restart
- [ ] Store assets: 5 screenshots per locale (TM/EN/RU), feature graphic
- [ ] Age rating + content declaration (education app → simple)
