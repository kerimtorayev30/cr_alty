#!/usr/bin/env python3
"""Record the lessons + search round in HANDOFF-STATUS.md."""
import sys

P = 'HANDOFF-STATUS.md'
s = open(P, encoding='utf-8').read()
edits = []


def sub(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f'ABORT [{label}]: anchor matched {n} times, expected 1')
    s = s.replace(old, new, 1)
    edits.append(label)


NEW = '''## 11. Üniteler artık ders ders: 1A · 1B · 1C

Haklıydın, English File üniteleri üç ders olarak işleniyor ve Vocabulary Bank
ünitelere değil **derslere** oturuyor. Ders eşlemesini bu sefer **uydurmadım**:
kitabın içindekiler tablosu (OCR dökümü, satır 20–92) her dersi sayfası, başlığı,
grameri ve VOCABULARY sütunuyla listeliyor ve o tablo okunabilir durumda. Örneğin
`p.6 1A A cappuccino, please — numbers 0-10, days of the week, saying goodbye`.

Beginner yeniden yazıldı: **400 söz, 12 ünite, 29 ders**. Söz bankası toplamı
328 → **441** (44'i önceki turdaki yer tutuculardan).

| Ünite | Dersler | Söz |
|---|---|---|
| 1 | 1A A cappuccino, please · 1B World music · 1C Practical English 1 | 53 |
| 2 | 2A Are you on holiday? · 2B That's my bus! | 33 |
| 3 | 3A Where are my keys? · 3B Souvenirs · 3C Practical English 2 | 40 |
| 4 | 4A Meet the family · 4B The perfect car | 46 |
| 5 | 5A A big breakfast? · 5B A very long flight · 5C Practical English 3 | 47 |
| 6 | 6A A school reunion · 6B Good morning, goodnight | 33 |
| 7 | 7A Have a nice weekend! · 7B Lights, camera, action! · 7C Practical English 4 | 33 |
| 8 | 8A Can I park here? · 8B Do you like cooking? | 23 |
| 9 | 9A Everything's fine! · 9B Working undercover | 26 |
| 10 | 10A A room with a view · 10B Where were you? | 23 |
| 11 | 11A A new life in the USA · 11B How was your day? · 11C Practical English 6 | 28 |
| 12 | 12A Strangers on a train · 12B Revise the past | 15 |

Uygulamada: ünite satırı ders çiplerini gösteriyor (`Unit 1 · 52 words · [1A][1B][1C]`),
flashcard'ın üstünde ders rozeti ve dersin adı yazıyor (`1A · A cappuccino, please`).
Navigasyon derinliği değişmedi — ders ayrı bir ekran değil, etiket.

**§8'deki uyarı aynen geçerli:** ders→konu eşlemesi kitaptan doğrulandı ama
**sözlerin kendisi OCR'dan çıkarılmadı**, benim bilgimden yazıldı (dökümdeki
listeler okunamıyor). 441 sözün tamamı `proofread: false`.

Doğrulayıcı artık `books[].lesson` alanını denetliyor: harf A/B/C olmalı ve
başındaki sayı ünite numarasına eşit olmalı (yani `1A` sözü 2. üniteye yazılamaz).

## 12. Arama gerçekten çalışmıyor — sebebi ve çözümü

Ölçtüm, şikâyetin doğruydu. Taze kurulumda arama çubuğuna ne yazarsan yaz
**0 sonuç** dönüyordu:

```
taze kurulum, sorgu yok : 0 satır   (S.filter = hist)
"mug"  yaz              : 0 satır
"suw"  yaz              : 0 satır
"вода" yaz              : 0 satır
"All words"a bas, "mug" : 1 satır     <- ancak o zaman
```

Sebep: `filt()` sorguyu seçili çiple **kesiştiriyordu** ve varsayılan çip
"Recent words". Geçmiş boş olduğu için her şey eleniyordu. Yani arama bozuk
değildi, **görünmezdi** — "All words"a basmayı bilmen gerekiyordu.

Ayrıca `data-q="suw"` ve `data-q="teacher"` öneri çiplerinin dosyada **hiç tık
işleyicisi yoktu**; ikisi de ölü butondu.

Şimdi:

- **Sorgu varsa çip yok sayılıyor** — arama her zaman tüm söz bankasında.
  Çipler yalnızca sorgu **boşken** listeyi daraltıyor (Recent / Favorites / All).
- **Üç dilde ve her alanda** arıyor: `en`, `tm`, `ru`, `ipa`, `def`, `ex`, `syn`,
  `coll`. Yani "krujka" → *mug*, "кружка" → *mug*, "on the table" → *table*.
- **Diakritik duyarsız:** `yadaw` → *ýadaw*, `turkmen` → *Türkmen*,
  `sag bolun` → *sag boluň*. Kiril yazıyorsan Rusça aradığın anlaşılıyor.
- **Oxford sözlüğü gibi sıralama:** tam eşleşme > baştan eşleşme > içinde geçen.
- Sonuç satırında hangi dilde eşleştiği (`EN`/`TM`/`RU` rozeti), IPA, cins ve
  ders rozeti (`3B`) görünüyor.
- Öneri çipleri artık çalışıyor.
- Boş durumlar üç dilde: `no_res`, `no_favs`, `no_words_yet`.

Ölçülen sonuç (TK arayüzünde):

```
"mug"          -> 2 satır | mug  EN  krujka · кружка  /mʌɡ/ · N  3B
"suw"          -> 4 satır | water TM  suw · вода
"вода"         -> 3 satır | water RU  suw · вода
"on the table" -> 3 satır | table     (eşdizimden buldu)
"yadaw"        -> 1 satır | tired TM  ýadaw · усталый  (diakritiksiz)
"zzz"          -> 0 satır | "Hiç söz tapylmady..."
```

Loader'da bu yüzden bir hata daha çıktı: paketin `lessons` listesini
`normalizePack` görmezden geliyordu, yani ders adları uygulamaya hiç ulaşmıyordu
(`LESSONS: 0`). `pickLessons()` eklendi ve `fetchWords` artık her yolda
(gömülü / önbellek / ağ) `{words, source, lessons}` döndürüyor.

'''

sub('## Doğrulama — `./verify.sh`, beş aşama da geçti', NEW + '## Doğrulama — `./verify.sh`, beş aşama da geçti', 'sections 11-12')

sub('''2/5  içerik hattı: validate + build + loader      -> OK, 328 söz / 5 dosya, 52 assertion
3/5  baseline yolculukları                        -> PASS, 143 assertion, 0 hata
4/5  içerik paketi entegrasyonu                   -> PASS, 64 assertion, 0 hata''',
'''2/5  içerik hattı: validate + build + loader      -> OK, 441 söz / 5 dosya, 52 assertion
3/5  baseline yolculukları                        -> PASS, 143 assertion, 0 hata
4/5  içerik paketi entegrasyonu                   -> PASS, 88 assertion, 0 hata''',
    'verification numbers')

sub('## Bu turun bulduğu hatalar (Beginner içe aktarma)',
'''## Bu turun bulduğu hatalar (dersler + arama)

1. **Arama çalışmıyordu** (yukarıda, §12). Test bunu görmüyordu çünkü test
   aramadan önce `S.filter="all"` yapıyordu — yani hatayı bilerek kapatıyordu.
   Yeni test taze bir örnekle, dokunulmamış varsayılanla sınanıyor.
2. **Öneri çipleri ölü butondu** — `data-q` için dosyada hiç işleyici yoktu.
3. **`wordLesson()` `unit` alanını döndürmüyordu**, ama `unitLessonList()` onu
   karşılaştırıyordu; sonuç her ünite için boş liste. Ölçmeden fark edilmezdi:
   `unitLessonList("beg",1)` → `[]`.
4. **Loader `lessons`'ı düşürüyordu** — `normalizePack` yalnızca sözlere bakıyor.
   Uygulama `LESSONS: 0` görüyordu, ders başlıkları hiç çizilmiyordu.
5. **`embed_pack.py` paketi tazelemiyordu.** Paket zaten doğru yerdeyse "dokunma"
   deyip **eski** paketi bırakıyordu; yani 441 söze geçtikten sonra uygulamada
   hâlâ 283 söz gömülüydü. Ayrıca "dosya büyüdü mü" kapısı karakter sayıyordu;
   paket Kiril ve IPA dolu olduğu için karakter ≠ bayt. İkisi de düzeltildi.
6. **Doğrulayıcı haklı çıktı, ben haksız:** "bagaž" yazdım, `ž` Türkmen
   alfabesinde yok → doğrusu `bagaj`. Uyarıyı susturmak yerine veriyi düzelttim.
7. Ders sıralaması dizeyle sayıyı karşılaştırıyordu (`a<nb`), yani `10A` ile `2A`
   şansa doğru sıralanıyordu. Test bunu sabitledi.
8. Üç test varsayımım ölçümle çürüdü ve testleri gerçeğe göre yeniden yazdım
   ("taze kurulumda çip hist'tir" — paylaşılan örnekte `all`'dı; "boş sorgu boş
   liste verir" — o örnekte geçmiş doluydu).

## Önceki turun bulduğu hatalar (Beginner içe aktarma)''',
    'mistakes section')

sub('| `content/data/beginner.json` | Beginner\'ın 283 sözü, ünite bilgisiyle |',
'''| `content/data/beginner.json` | Beginner: 400 söz, 29 ders, ders+ünite bilgisiyle |
| `content/tools/apply_lessons_search.py` | ders kablolaması + yeni arama (9 düzenleme) |
| `content/tools/sync_loader_lessons.py` | loader kopyasını senkronlar (6 düzenleme) |
| `content/tools/apply_lesson_search_tests.py` | ders + arama testleri |''',
    'files table')

sub('| `uploads/app-yatla.html` | ürün (312.850 bayt, tek dosya, 328 söz gömülü) |',
    '| `uploads/app-yatla.html` | ürün (351.616 bayt, tek dosya, 441 söz gömülü) |',
    'app size')

open(P, 'w', encoding='utf-8').write(s)
print(f'{len(edits)} edits applied to {P}')
for e in edits:
    print('  -', e)
