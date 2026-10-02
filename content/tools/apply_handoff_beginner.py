#!/usr/bin/env python3
"""Record the Beginner vocabulary import in HANDOFF-STATUS.md.

Every number in the new section is copied from a command that was actually run
this session (verify.sh, the generator's own output, the jsdom probes), not
estimated.
"""
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


# --- new section, inserted before the verification section -------------------
NEW_SECTION = '''## 8. English File Beginner — tüm sözler, ünite ünite

`uploads/beginner book databsae.txt` (kitabın OCR dökümü) içe aktarıldı: **283 söz,
12 ünite**, `content/data/beginner.json` olarak. Toplam söz bankası 70 → **328**.

| Ünite | Konu | Söz |
|---|---|---|
| 1 | Numbers 0–10 · days of the week (+ 1A selamlaşma) | 25 |
| 2 | Countries · numbers 11–100 | 39 |
| 3 | The classroom · souvenirs · small things | 29 |
| 4 | People and family | 17 |
| 5 | Colours · adjectives | 27 |
| 6 | Food and drink | 27 |
| 7 | Common verb phrases 1 | 14 |
| 8 | Jobs and places of work | 17 |
| 9 | A typical day | 10 |
| 10 | Free time · travel · films · months | 31 |
| 11 | Activities · clothes | 25 |
| 12 | Hotels · rooms · prepositions of place | 22 |

**Dürüst olmam gereken kısım:** OCR dökümündeki söz listeleri makineyle
okunabilir durumda değil. `content/tools/extract_beginner.py` ile denedim: 15
Vocabulary Bank başlığından yalnızca **60 numaralı madde** çıktı ve çoğu bozuktu
(`18:eighteen Cll`, `22:sinciep eis Itwentt`, `34:jclock`, `12:acamera`). Bölüm
başlıkları temiz, listeler değil. Bu yüzden **söz listeleri OCR'dan çıkarılmadı**;
kitabın bu ünitelerinde öğrettiği sözleri kendi bilgimden yazdım. Dökümden
güvenilir biçimde alınan tek şey ünite → konu eşlemesi (içindekiler tablosu,
satır 26–92) ve 15 Vocabulary Bank sayfasının kimliği.

Bunun pratik sonucu: liste büyük olasılıkla kitabın kendi listesiyle **birebir
değil** — eksik veya fazla söz olabilir. Kitap elindeyse ünite ünite karşılaştırıp
`content/tools/gen_beginner.py` içindeki `U[n]` demetlerini düzeltmek yeterli;
dosyayı yeniden çalıştırmak `beginner.json`'ı üretir. Ayrıca 328 sözün tamamı
`proofread: false` — TM/RU çevirileri ana dil kontrolünden geçmedi.

Eş sesliler için başlığa cins eklendi: `watch (n.)` = saat (ünite 3),
`watch (v.)` = izlemek (ünite 7). Sebep: uygulama favorileri ve geçmişi `w.en`
üzerinden anahtarlıyor, yani aynı başlık iki kez olamaz.

Geçen turun **sahte** `ef1.json` dosyası silindi (o dosya benim uydurduğum 20
sözdü, gerçek kitapla çakışıyordu). `ef2/ef2b/ef3/ef4` hâlâ duruyor ama onlar da
benim yer tutucum; gerçek Elementary/Pre-Int/Intermediate dökümlerini
gönderdiğinde aynı yöntemle değiştirilecekler. Çakışan 5 söz (`people, phone, eat,
drink, read`) tek söz bankasında bir kez durması gerektiği için yer tutuculardan
çıkarıldı — söz bankası düz bir küme, bir söz bir kez var.

## 9. Ünite ekranı artık gerçek

Önceden ünite listesi süs gibiydi: her ünite **"24 words"** yazıyordu ve üniteye
tıklayınca `WORDS.slice((n*2)%7, +6)` çalışıyordu — yani ne kitaba ne üniteye
bakan keyfî bir dilim. `BOOKS[0].units` de 10'du; kitap 12 ünite.

Şimdi:

- her sözde `books:[{book,unit}]` var; `unitWords(bid,un)` / `unitCount(bid,un)`
  tek yerden hesaplıyor,
- ünite satırı gerçek sayıyı gösteriyor (`Unit 6 · 27 words`),
- üniteye tıklayınca **o ünitenin tüm sözleri** açılıyor (doğrulandı: ünite 1 →
  24 kart, hepsi `beg/1`),
- sözlükteki "öğren" butonu sözün kendi ünitesine gidiyor (`opposite` → ünite 12,
  `breakfast` → ünite 6),
- henüz içe aktarılmamış bir kitabın ünitesi uydurma sayı yerine **"Not imported
  yet" / "Entek goşulmady" / "Ещё не добавлено"** diyor.

## 10. Söz paketi artık uygulamaya gömülü — ve bu iki gerçek hatayı ortaya çıkardı

Uygulama sözleri `fetchWords({url:"content/build/yatla-words.min.json"})` ile
alıyordu. Bu **diskteki göreli bir yol**; sen uygulamayı ağ erişimi olmayan
sandbox iframe'de önizlediğin için o istek her zaman başarısız oluyordu ve
uygulama sessizce 12 seed söze düşüyordu. Yani şimdiye dek gerçek kullanımda
70 sözün hiçbiri görünmüyordu.

`content/tools/embed_pack.py` paketi (75 KB) `<head>` içine gömüyor; uygulama
**312.850 bayt**. `YatlaContent` gömülü paketi her şeyden önce okuduğu için
uygulama artık tamamen çevrimdışı çalışıyor. INIT sonrası ölçülen: **336 söz**
(12 seed + 324 paket; 4'ü seed'de zaten vardı).

Bunu yaparken ölçümle bulunan iki hata:

1. **Paket `</body>`'den önceydi, yani uygulama script'inden sonra.** Uygulama
   script'i parser ona ulaştığı anda çalışıyor ve `getElementById` henüz
   okunmamış bir öğeyi bulamıyor. jsdom ile ölçtüm: INIT sırasında
   `el = false`, `WORDS.length = 12`. Paket `<head>`'e taşındı.
2. **Boş sonuç önbelleği zehirliyordu.** `if (cache && !opts.noCache)` satırında
   `[]` truthy olduğu için bir kez boş dönen `fetchWords` oturum boyunca boş
   dönmeye devam ediyordu — ve döndürdüğü şey belgelenen `{words,source}` değil
   çıplak diziydi. `cache && cache.length` oldu ve şekil düzeltildi.

'''

sub('## Doğrulama — `./verify.sh`, beş aşama da geçti', NEW_SECTION + '## Doğrulama — `./verify.sh`, beş aşama da geçti', 'new sections 8-10')

# --- refresh the verification numbers ---------------------------------------
sub('''```
1/5  node --check (satır içi script)              -> exit 0
2/5  içerik hattı: validate + build + loader      -> OK, 70 söz, 52 assertion
3/5  baseline yolculukları                        -> PASS, 141 assertion, 0 hata
4/5  içerik paketi entegrasyonu                   -> PASS, 50 assertion, 0 hata
5/5  sandbox kuralları (harici kaynak yok)        -> tek </script>, temiz
ALL CHECKS PASSED
```''',
'''```
1/5  node --check (satır içi script)              -> exit 0
2/5  içerik hattı: validate + build + loader      -> OK, 328 söz / 5 dosya, 52 assertion
3/5  baseline yolculukları                        -> PASS, 143 assertion, 0 hata
4/5  içerik paketi entegrasyonu                   -> PASS, 64 assertion, 0 hata
5/5  sandbox kuralları (harici kaynak yok)        -> 2 <script> / 2 </script>, temiz
ALL CHECKS PASSED
```

Adım 5'in kuralı değişti: eskiden "tam olarak 1 `</script>`" istiyordu. Gömülü
söz paketi gerçek bir `<script type="application/json">` öğesi olduğu için artık
**her `<script>` tam bir kez kapanıyor mu** diye bakıyor (ayrıca: tek uygulama
script'i, en fazla bir gömülü paket, paket uygulama script'inden önce).''',
    'verification numbers')

# --- the mistakes this round, honestly --------------------------------------
sub('## Değişmedi / hâlâ sende',
'''## Bu turun bulduğu hatalar (hepsi düzeltildi)

1. **`embed_pack.py` uygulama dosyasını sildi.** Değiştirme regex'i
   (`<script type="application/json" id="yatlaWords">.*?</script>`) bir etiketin
   başına bağlı değildi; loader'ın **belge yorumundaki** `<script id="yatlaWords">`
   metnini eşleştirdi ve uygulamanın gerçek `</script>`'üne kadar her şeyi sildi.
   Dosya 236.849 → 247.801 bayt olurken uygulama script'inin tamamı gitti.
   `verify.sh`'ın bir önceki çalıştırmada `/tmp`'ye çıkardığı script ve
   `content/loader/yatla-content.js` sayesinde dosya baştan kuruldu; çıkan sonuç
   kurtarılan script'le birebir aynı (yalnızca sondaki satır sonu farkı).
   Ders: bir daha aynı şey olmasın diye `embed_pack.py` artık yazmadan önce
   "dosya büyüdü mü / uygulama script'i duruyor mu" diye bakıyor ve loader'ın
   yorumlarında `<script` hecesi geçmiyor.
2. **Kendi düzeltmem aynı tuzağı yeniden kurdu.** Yorumu `a <script> element`
   diye yazdım; o metin de `<script>` diye sayıldı. `<script` hecesi hiç
   kullanılmadan yazıldı.
3. **İki test yanlış nedenden geçiyordu.** `[1]` "paket yokken 12 söz" iddiasını
   `fetchWords`'ün sözü tamamlanmadan, eşzamanlı okuyordu — dosyada ne olursa
   olsun 12 görüyordu. `[8]` "paket ulaşılamaz" senaryosunu hiç kurmuyordu,
   oysa uygulama artık paketle geliyor. İkisi de artık gerçekten ölçüyor.
4. **İki test kırılgandı.** `"вода" finds 1` gibi tam sayı bekleyen aramalar,
   içerik büyüdüğünde kırıldı (artık hem *mineral water* hem *factory worker*
   eşleşiyor). Sayı değil sonuç doğrulanıyor.
5. `watch` hem saat hem izlemek olarak iki ünitede geçiyordu; doğrulayıcı
   "duplicate headword" dedi. Eş sesliler cins etiketiyle ayrıldı.
6. `NUM` ve `ORD` cinsleri şemada yoktu; kitabın sayı ve sıra sayıları için eklendi.

## Değişmedi / hâlâ sende''',
    'mistakes section')

sub('- 70 sözün tamamı `proofread: false` — TM/RU metinleri ana dilde kontrol bekliyor.',
    '- 328 sözün tamamı `proofread: false` — TM/RU metinleri ana dilde kontrol bekliyor.\n'
    "- **Beginner söz listeleri OCR'dan çıkarılmadı**, benim bilgimden yazıldı (bkz. §8).\n"
    '  Kitap elindeyse karşılaştırıp düzeltmen gerekiyor.\n'
    '- `ef2/ef2b/ef3/ef4` hâlâ benim yer tutucum (45 söz). Gerçek kitap dökümlerini\n'
    '  gönderdiğinde aynı yöntemle değiştirilecekler.',
    'unchanged section')

sub('| `uploads/app-yatla.html` | ürün (232.122 bayt, tek dosya) |',
'''| `uploads/app-yatla.html` | ürün (312.850 bayt, tek dosya, 328 söz gömülü) |
| `content/data/beginner.json` | Beginner'ın 283 sözü, ünite bilgisiyle |
| `content/tools/gen_beginner.py` | ünite → konu eşlemesi + söz listeleri (tek kaynak) |
| `content/tools/embed_pack.py` | paketi `<head>`'e gömer; yazmadan önce kapı kontrolü |
| `content/tools/apply_units_patch.py` | ünite kablolaması (5 düzenleme) |
| `content/tools/extract_beginner.py` | OCR sondası — **çıktısı güvenilmez**, kanıt olarak duruyor |
| `package.json` | kök `jsdom` bağımlılığı (testler için; önceden yoktu) |''',
    'files table')

open(P, 'w', encoding='utf-8').write(s)
print(f'{len(edits)} edits applied to {P}')
for e in edits:
    print('  -', e)
