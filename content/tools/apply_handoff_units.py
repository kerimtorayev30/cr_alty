#!/usr/bin/env python3
"""Record the unit-system redesign and the Elementary import in HANDOFF-STATUS.md.

Everything here was measured in this round, not assumed:
  - verify.sh: ALL CHECKS PASSED (content 52/0, baseline 143/0, integration 100/0)
  - 732 words valid, 0 warnings; app 429,336 bytes
"""
import sys

P = 'HANDOFF-STATUS.md'
s = open(P, encoding='utf-8').read()
n = 0


def sub(old, new, label):
    global s, n
    c = s.count(old)
    if c != 1:
        sys.exit(f'ABORT [{label}]: anchor matched {c} times')
    s = s.replace(old, new)
    n += 1
    print('  -', label)


# 1. the current-state header
sub("""## Bu turun bulduğu hatalar (dersler + arama)""",
    """## 13. Ünite sistemi artık kitaba göre veri-güdümlü + Elementary içe aktarıldı

**Senin üç isteğin ve karşılıkları (hepsi ölçüldü):**

**a) "Ünite sistemi kitaptan kitaba değişiyor, dikkat et."**
Uygulama artık hiçbir yerde `1A/1B/1C` varsaymıyor:

| Nerede | Eskiden | Şimdi |
| --- | --- | --- |
| Şema | ders kodu `^(?:[1-9]\\|1[0-2])[A-C]$` — yani **A/B/C zorunlu**, ünite 1-12 arası | ders kodu serbest metin; ünite pozitif tam sayı, üst sınır yok |
| `BOOKS` | 8 kitabın hepsi `units:12` | hâlâ 12 (English File gerçekten 12 ünite) ama artık **tek yerden** okunuyor; başka bir kitap 14 ünite derse veri yetiyor |
| `unitLessonList` | her ünitede üç ders varmış gibi çip basıyordu | kitabın **gerçekten** sahip olduğu dersleri döndürüyor; `2A` `10A`'dan önce sıralanıyor |
| `wordLesson` | `books[0]`'a bakıyordu | `wordLesson(w, bid)` — "bu söz X kitabında nerede?" diye sorulabiliyor |
| Dersi olmayan kitap | boş çip şeridi | hiç ders listesi yok; üniteye basınca doğrudan sözlere geçiyor |

**b) "1A tasarımı güzel değil, değiştir."**
Çipler kalktı. Üniteye basınca **ders listesi** açılıyor; her ders kendi satırında:

```
1A  Welcome to the class
    days of the week · numbers 0-20
    10 words                                    >
```

Ünite satırında artık çip yok, sadece "3 lessons" yazıyor. Kartın üstündeki yeşil
hap etiket de gitti; yerine soluk `1A · Welcome to the class` satırı geldi.
Dersin içinden geri tuşu ders listesine, ünite listesine değil.

**c) "Elementary'nin sözlerini ekle."**
`uploads/elementary.txt` içindeki **Vocabulary Bank (s.148-164)** okunabilir
durumdaydı — Beginner'dan farklı olarak başlıklar OCR'dan seçilebiliyor.
`content/tools/extract_elementary.py` bunu ölçtü: 491 ham satır, gürültü
(talimatlar, alıştırma cümleleri, kaymış sütunlar) elle ayıklandı.

| | |
| --- | --- |
| Elementary sözleri | **465** |
| Elementary dersleri | **22** (söz listesi olmayan 11 dilbilgisi dersi gösterilmiyor: 2C, 5A, 5C, 6A, 7A, 8C, 9B, 9C, 10B, 11A, 11B) |
| Toplam söz | **732** (174 söz iki kitapta da var, tek kayıtta birleşti) |
| Kitap başına | beg 400 · ele 483 · int 10 · pre 9 |

**Önemli:** Elementary'nin Vocabulary Bank'ı **konuya göre** düzenlenmiş, ders başına
bir bölüm değil. İki bölüm iki derse birden hizmet ediyor (s.148 hem 1A hem 1B;
s.157 hem 3C hem 4B). Şema artık bunu varsaymıyor.

**İki kitap aynı sözü öğretince** ne oluyor: söz **tek kayıt**, `books[]` içinde her
iki kitap var. `Monday` → `beg/1/1A, ele/1/1A`. Beginner 1A'da çalışırken etiket
"A cappuccino, please", Elementary 1A'da "Welcome to the class" — kart,
**çalışılan kitabın** dersini söylüyor, sözün ana kitabını değil.

**Ölçülen sonuç:** `bash verify.sh` → **ALL CHECKS PASSED**
(content 52/0, baseline 143/0, integration **100**/0, 732 söz geçerli 0 uyarı,
`<script>` 2/2, dış kaynak yok). Uygulama **429.336 bayt**. jsdom: `WORDS 739`,
`LESSONS 51` (beg 29 + ele 22), 0 hata.

**Dürüst olmam gereken yer:** Elementary'nin İngilizce başlıkları kitaptan
okundu, ama `tm`/`ru`/`def`/`ex` alanları benim yazdıklarım ve IPA'yı OCR'ın
bozuk sesletim harfleri yerine kendim yazdım. 732 sözün **hiçbiri** Türkmen/Rus
ana dili kontrolünden geçmedi (`proofread: 0/732`).

## 14. Bu turun bulduğu hatalar

1. **`wordLesson` istenen kitap bulunamayınca `books[0]`'a düşüyordu.** Sonuç:
   Beginner'a ait sözler Elementary derslerine sızıyordu — Elementary 1A
   "26 words" gösteriyordu, kendi Vocabulary Bank'ında 10 var. Geri düşüş
   kaldırıldı; kitap sorulduysa ve söz orada yoksa cevap `null`.
2. **Kart etiketi sözün ana kitabını kullanıyordu.** Elementary çalışırken
   Beginner'ın ders başlığı görünüyordu.
3. **`add_full_stops()` eşleştiği CEFR alanını geri koymuyordu.** 371 satır
   seviyesini kaybetti (`expected 9, got 8`), 86 satırda da `coll` bir sola kaydı
   ve `cefr: "by bus"` üretildi. Kaynak satırlar `ast.literal_eval` ile okunup
   onarıldı.
4. **Aynı onarımın çıktıda yapılması işe yaramıyor** — üreteç dosyayı her
   çalıştırmada yeniden yazıyor. Onarım **kaynakta** olmalı.
5. **El yazımı satır ayrıştırıcı üç kez farklı şekilde yanıldı:** uyuşmayan bir
   regex (hiçbir satırı bulmadı), ayraçla bölme (örneği çift tırnakla yazılmış
   satırı 7 alan saydı), karakter karakter yürüyen bir döngü (satırı tek alana
   indirdi). Çözüm: satırlar zaten Python demeti, `ast.literal_eval` kullan.
6. **Doğrulayıcının `ž` uyarısı haklıydı, verim yanlıştı.** `ž` Türkmen
   alfabesinde yok: `inžener` → `inžener`, `žurnal` → `jurnal`, `žurnalist` →
   `jurnalist`. Bir Türkmen karşılığına yanlışlıkla Kiril `м` de karışmıştı
   (`alyм` → `alym`).
7. **`BOOK_IDS` listesinde `intp` ve `advp` yoktu** — iki Plus kitabı için zarf
   yazılamazdı.
8. **`build.js` tüm dersleri dosyanın tek `book` alanıyla etiketliyordu** —
   birleşik pakette hepsi `unassigned` olurdu. Dersin kendi `book` alanı artık
   öncelikli.
9. **İstatistik `books[0]`'ı sayıyordu** — Elementary 483 yerine 314 görünüyordu.
10. **Bir test `"0 words"` alt dizesine bakıyordu** ve "60 words" onu içeriyor.
    Artık sayının kendisine bakıyor.
11. **Çok kitaplı pakette zarf `book` alanı istiyor** — birleşik paket `all`
    diyor, doğrulayıcı bunu tanıyor.

## Önceki turun bulduğu hatalar (dersler + arama)""",
    'new §13 + §14, previous section demoted',
)

# 2. the file table
sub("""| `tests/integration.js` | 50 assertion'lık içerik paketi testi |""",
    """| `tests/integration.js` | 100 assertion'lık içerik paketi + ünite/ders testi |
| `content/tools/gen_elementary.py` | Elementary üreteci: 465 söz, 22 ders |
| `content/tools/extract_elementary.py` | Vocabulary Bank OCR ölçümü |
| `content/tools/merge_packs.py` | data/*.json -> merged/yatla-all.json |
| `content/tools/restore_cefr.py`, `fix_shifted_coll.py` | add_full_stops hasarını onardı |
| `content/tools/apply_unit_redesign.py` | ünite ekranının yeni tasarımı |
| `content/tools/apply_lesson_ui_tests.py` | testleri yeni tasarıma uydurdu |""",
    'file table updated',
)

# 3. the stale baseline counts
sub("""| `tests/baseline.js` | 141 assertion'lık regresyon ağı |""",
    """| `tests/baseline.js` | 143 assertion'lık regresyon ağı |""",
    'baseline count corrected',
)

open(P, 'w', encoding='utf-8').write(s)
print(f'{n} edits applied')
