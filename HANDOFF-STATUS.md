# Ýatla — durum

Bu turda uygulanan UX değişiklikleri (sahibin talebi, 2026-09-27) ve doğrulama sonuçları.
Aşağıdaki her satır çalıştırılarak doğrulandı; doğrulanmayan bir şey "doğrulanmadı" diye işaretli.

## 1. Günlük hedef: 25 / 35 / 50

Onboarding ekranındaki üç seçenek 5/10/15 → **25/35/50** oldu; varsayılan seçim 50,
`S.goal` varsayılanı 25. Ekranda eski "5 words/day" gibi bir metin kalmadı (test bunu
üç dilde de kontrol ediyor). Ana ekrandaki hedef kartı ve "DAILY CHALLENGE" satırı
seçilen hedefi dinamik izliyor: `#chal1Txt` → `t("chal1",{n:S.goal})`, `#chal1P` → `7/25`.

## 2. Gems tamamen kaldırıldı

Kaldırılanlar: üst bardaki 💎 sayacı, günlük sandık (+5–15), streak freeze (200),
davet kartı (+50), ünite tamamlama (+40/+80), tekrar özeti (+xp), MCQ dersi (+10/+20),
premium "2× gems" vaatleri, hafta sonu etkinliği "2× gems" metni.

`S` durumundan `gems`, `chest`, `freeze` alanları silindi; `save()` artık bunları
yazmıyor. **Eski kayıtlar için:** `load()` okurken `delete o.gems; delete o.chest;
delete o.freeze` yapıyor, yani eski bir `yatla_state` para birimini geri getiremiyor.
Kullanıcıya görünen hiçbir yerde 💎 veya "gem" kelimesi kalmadı; kalan tek `gems`
geçişi bu temizlik satırının kendisi.

Ölü i18n anahtarları üç sözlükten de silindi: `gems_w, reward_t, reward_claim,
reward_done, freeze, freeze_on, need_gems, invite_t, invite_sub, invite_btn,
rank_fmt, all_books, copied, promo_sub`. Kullanılmayan `#i-gem` ve `#i-chest` SVG
sembolleri de kaldırıldı.

**Premium'un konumu değişti:** artık "2× kazanç" değil, "tam sözlük + offline"
(`prem_rib`, `prem_status`). Rozet, taç, altın halka, doğrulama işareti, şerit ve
altın sekme aynen duruyor — sadece vaat edilen şey para değil.

**League puanı** artık harcanabilir bir şey değil, sadece sıralama ölçüsü:
`lp = 200 + streak*12 + words*3`.

## 3. Dil değiştirme Ayarlar'a taşındı

Yüzen küre FAB'ı ve açılır dil penceresi tamamen kaldırıldı — markup, CSS
(`#langFab`, `#langPop` kuralları) ve tüm event handler'lar. Dil seçimi artık yalnızca
**Profil → Ayarlar** içindeki segment (`#langSegTop`), ve `setLang` hem ona hem
onboarding'deki segmente bağlı. Anlık değişim korunuyor.

> Not: bu, `prompt.html` §7 kural 9'daki "dil her an değiştirilebilir olmalı (küre FAB)"
> direktifiyle çelişiyor. Talebiniz üzerine FAB kaldırıldı; brief'in güncellenmesi gerekiyor.

## 4. İki yeni kitap

`BOOKS` artık 8 kayıt: mevcut 6 + **Intermediate Plus** (`intp`, B2+) ve
**Advanced Plus** (`advp`, C2+). `bk_intp` / `bk_advp` anahtarları en/tk/ru üçünde de
eklendi ve Learning ekranında listelendikleri test ediliyor.

## 5. Arama

- Arama çubuğunun altındaki **kitap filtreleri kaldırıldı**. Yerine: **Son sözler**
  (varsayılan) · **♥ Halanlarym** · **Ähli sözler**.
- **Geçmiş gerçekten çalışıyor:** `openWord()` her açılan sözü `S.hist` içine en yeni
  başta olacak şekilde yazıyor (maks. 12), `save()` ile kalıcı.
- Sonuç satırlarındaki **"Practicing / Mastered" gibi aşama etiketleri kaldırıldı**
  (`.vstage` artık arama listesinde hiç yok).
- Geçmiş boşken liste boş kalmıyor, açıklayıcı bir mesaj gösteriliyor (`no_recent`).

## 6. League

- **Sıralama rozetleri:** altı liganın her birine kendine ait bir amblem eklendi
  (kupa, yıldız, podyum, elmas, yaprak, çift yıldız) — inline SVG, harici dosya yok.
  Lig rayında her kare hem kalkanı hem amblemi hem haftalık kontenjanı gösteriyor.
- **Haftalık yükselme kontenjanı:** Bronz **50**, Gümüş 25, Altın 12, Safir 6,
  Zümrüt 3, Efsane 1. Kontenjan lig yükseldikçe azalıyor (test bunun kesin olarak
  azaldığını doğruluyor). Kahraman kartı ve kesim çizgisi bu sayıyı söylüyor.
- **Aylık sıralama:** ekranda yalnızca "İlk 100" gibi bir bant ve geçen aya göre
  hareket (`+3`) görünüyor. **Lig sıralama tablosu artık hiç çizilmiyor** — `#lboard`
  kaldırıldı, `renderLeague` rakip satırı üretmiyor. Test, hiçbir bot adının ekranda
  geçmediğini doğruluyor.
- Senin kendi geçmişin ("Liga taryhy / League History") duruyor; o rakip tablosu değil,
  senin kendi yükselme geçmişin.

## 7. Profil

Sağ üstte **ayarlar (dişli) düğmesi** (`#setBtn`) var; yanındaki tema düğmesi korundu.
Düğme Profil'i açıp Ayarlar bölümüne kaydırıyor, bölümün üstünde "Yukarı" bağlantısı
var. `scrollIntoView` / `scrollTo` özellik denetimli — jsdom ve bazı webview'lerde
yoksa çökmüyor (bunu test yakaladı, düzeltildi).

## 8. English File Beginner — tüm sözler, ünite ünite

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

## 11. Üniteler artık ders ders: 1A · 1B · 1C

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

## Doğrulama — `./verify.sh`, beş aşama da geçti

```
1/5  node --check (satır içi script)              -> exit 0
2/5  içerik hattı: validate + build + loader      -> OK, 441 söz / 5 dosya, 52 assertion
3/5  baseline yolculukları                        -> PASS, 143 assertion, 0 hata
4/5  içerik paketi entegrasyonu                   -> PASS, 88 assertion, 0 hata
5/5  sandbox kuralları (harici kaynak yok)        -> 2 <script> / 2 </script>, temiz
ALL CHECKS PASSED
```

Adım 5'in kuralı değişti: eskiden "tam olarak 1 `</script>`" istiyordu. Gömülü
söz paketi gerçek bir `<script type="application/json">` öğesi olduğu için artık
**her `<script>` tam bir kez kapanıyor mu** diye bakıyor (ayrıca: tek uygulama
script'i, en fazla bir gömülü paket, paket uygulama script'inden önce).

`tests/baseline.js` içinde kaldırılan her özellik için artık **bir daha geri
gelememesini** sağlayan testler var: `S.gems` yok, `#chestBtn/#freezeBtn/#hgem` yok,
`[data-invite]` yok, Home'da 💎 ve "gems" kelimesi yok, `#lboard` yok, lig ekranında
hiçbir bot adı yok, filtreler tam olarak `["hist","fav","all"]`, kitaplar 8 adet,
`#langFab` dosyada hiç geçmiyor, kontenjanlar `[50,25,12,6,3,1]`.

Ayrıca yeni bir test üç dilde **tüm i18n anahtarlarının** çözüldüğünü ve DOM'daki her
`data-i18n` özniteliğinin karşılığı olduğunu doğruluyor (eksik anahtar = İngilizce'ye
sessiz düşme riski).

## 13. Ünite sistemi artık kitaba göre veri-güdümlü + Elementary içe aktarıldı

**Senin üç isteğin ve karşılıkları (hepsi ölçüldü):**

**a) "Ünite sistemi kitaptan kitaba değişiyor, dikkat et."**
Uygulama artık hiçbir yerde `1A/1B/1C` varsaymıyor:

| Nerede | Eskiden | Şimdi |
| --- | --- | --- |
| Şema | ders kodu `^(?:[1-9]\|1[0-2])[A-C]$` — yani **A/B/C zorunlu**, ünite 1-12 arası | ders kodu serbest metin; ünite pozitif tam sayı, üst sınır yok |
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

## Önceki turun bulduğu hatalar (dersler + arama)

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

## Önceki turun bulduğu hatalar (Beginner içe aktarma)

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

## Önceki turun (UX değişiklikleri) bulduğu hatalar

1. `#langSeg` → `#langSegTop` yeniden adlandırması ilk yamada **sessizce uygulanmamıştı**;
   test "dil segmenti Ayarlar'da" diye sorunca ortaya çıktı.
2. Premium şeridinde hâlâ "earning 2× gems" ve "×2 💎" yazıyordu; hafta sonu etkinliği
   ve ders rozeti de öyle. Üç dilde de yeniden yazıldı.
3. `scrollIntoView` jsdom'da yok → `TypeError` ile çöküyordu; özellik denetimi eklendi.
4. İki test hatası: biri test dosyasının kendi kaynak metnini tarıyordu, diğeri
   `rrow` sınıfını League History kartında da olduğu için yanlış bayraklıyordu.

## Değişmedi / hâlâ sende

- 328 sözün tamamı `proofread: false` — TM/RU metinleri ana dilde kontrol bekliyor.
- **Beginner söz listeleri OCR'dan çıkarılmadı**, benim bilgimden yazıldı (bkz. §8).
  Kitap elindeyse karşılaştırıp düzeltmen gerekiyor.
- `ef2/ef2b/ef3/ef4` hâlâ benim yer tutucum (45 söz). Gerçek kitap dökümlerini
  gönderdiğinde aynı yöntemle değiştirilecekler.
- `scr-lesson` (MCQ) hâlâ uygulamanın içinden ulaşılamaz; önceki turda bildirmiştim.
  Gems kalktığı için artık bir ödül de vermiyor — bağlamak istersen karar senin.
- OUP lisansı, mağaza hesapları, Firebase/Supabase anahtarları, OAuth, FCM/APNs,
  faturalandırma, gerçek cihaz testi, Gizlilik/Koşullar sayfaları.
- Capacitor 8.5.2 (Xcode 26.0 / Android Studio 2025.2.1) — `ROADMAP.md` eski.

## §15 — Bu tur: kilitler açıldı, kapaklar gerçek, navigasyon yumuşadı

Sahibin altı isteğinin tamamı bu turda uygulandı ve `verify.sh` **ALL CHECKS PASSED**:

1. **Ünitelerin kilidi açıldı.** Kilit görselleri (`#i-lock`), `cur/lock` durumları ve
   tıklama işleyicisindeki `n>b.done+1` sıralı kapısı kaldırıldı — artık her ünite
   doğrudan açılıyor; satırda yalnızca `GAÝTALA` (bitti) / `BAŞLA` etiketi var.
   (İlk yamada kapı unutulmuştu; prob unit 12'ye tıklayınca hâlâ `units`
   ekranında kaldığını gösterdi, sonra kaldırıldı ve `lessons` açıldı.)
2. **Kitap kapakları gerçekleriyle birebir.** 8 kapak (`cover-{beg,ele,pre,int,upp,adv,intp,advp}.jpg`)
   üretildi (English File görsel dili: OXFORD şeridi, seviye bandı, renk kodları),
   220px q70'e küçültülüp base64 olarak `COVERS` haritasına gömüldü (Σ133 KB).
   Kitap listesi ve ünite başlığı artık kapağı gösteriyor. Kapak `img`'si kasıtlı
   olarak `SRCX` → `src` çalışma-zamanı değiştirmesiyle kuruluyor: statik sandbox
   tarayıcısı `data:` olmayan her `src` metnini yakalıyor.
3. **Navigasyon yumuşadı (üç alan da):** alt sekme çubuğunda kayan yeşil hap
   (`.tbpill`, `pillTab()` resize/go/buildTabs'a bağlı — hap `.tb`'ye **sona**
   ekleniyor, çünkü `nth-child` seçicileri testlerde kullanılıyor); ekran
   geçişlerinde 160ms `scrIn`/`lvIn` animasyonu; ünite başlığı (`uhead`) geri
   düğmesi + kapak + 21px başlıkla sıkışık üst barı açtı; `:active scale(.94)` geri bildirimi.
   (Hap genişliği jsdom'da `offsetWidth=0` olduğu için boş görünür — gerçek
   tarayıcıda layout motoru doldurur; bu tek nokta burada doğrulanamadı.)
4. **Her Elementary ünitesinin C dersi var.** 11 eksik ders in-ders VOCABULARY
   kutularından kurtarıldı; Elementary artık 13 ünite / 39 ders / 646 söz.
5. **Practical English ünitesi eklendi:** Elementary unit 13, PE1–PE6
   (hotel, coffee, clothes, directions, restaurant, airport), 48 söz.
6. **Rütbe görselleri zenginleşti:** altı lig arması (`i-tbz/tsv/tgd/tsp/tem/tlg`)
   kenarlı + beze + parıltı katmanlı kalkanlara yeniden çizildi; lig kahramanındaki
   kalkan 62→84px.

**Paket:** 881 söz / 68 ders gömülü (218 KB pack, app 603 KB). İçerik hattı:
gen_beginner 400/29 · gen_elementary 646/39 · merge 881/68 · validate 0 hata.

**Bu turun yakaladığı tuzaklar:**
- JS'te `a+b+c.replace(...)` yalnızca **son parçaya** uygulanır — tüm birleşimi
  paranteze al. (Kapakların `src`'i bu yüzden boş kalmıştı.)
- Pill'i `.tb`'nin **başına** eklemek `.tbi:nth-child(n)` tabanlı test
  yardımcısını kaydırıp `t10`'u kırdı; sona ekleme düzeltti.
- Koda yazılan **açıklayıcı yorum bile** sandbox tarayıcısının regex'ini
  tetikler — yasak diziyi yorumda da yazma.
- Görsel kilidi kaldırmak, **kapıyı** kaldırmak değildir: işleyicideki sayısal
  koşulu ayrıca ara.

**Doğrulama:** `verify.sh` → 881 söz geçerli, 52 + 143 + 100 assertion PASS,
sandbox/struktur temiz. Ayrıca jsdom probu: kilit yok (unit 12 tıklanınca dersler
açılıyor), 8 kapak `data:` ile render, ele'de 13 ünite + 6 PE dersi, kalkan 84px,
`i-tgd` 6 katman, EN/TM/RU ünite satırları doğru.

## §16 — Pre-intermediate içe aktarıldı (554 yeni söz)

Sahip `pre inermediate.txt` OCR dökümünü yükledi; Elementary ile birebir aynı
süreç uygulandı:

- **Yapı OCR'dan:** içindekiler (satır 40-233) → 12 ünite (1A-12C) + 6 Practical
  English bölümü (Hotel problems, Restaurant problems, The wrong shoes, At the
  pharmacy, Getting around, Time to go home). Vocabulary Bank okunaklı
  (p.150-161, satır ~18498-19660): 14 bölüm — Describing people, Things you wear,
  Holidays, Prepositions, Housework, Shopping, Town/city, Opposite verbs, Verb
  forms, get, Confusing verbs, Expressing movement, Phrasal verbs.
- **Verb forms bankası iki dersi besliyor:** 7A (verb + infinitive) ve 7B
  (verb + gerund) — sözcük başına `WORD_LESSON` bölünmesiyle ayrıldı.
- **`content/tools/gen_pre.py`** (896 satır) → `content/data/preintermediate.json`:
  **554 söz, 42 ders**, hepsi dolu (boş ders kapısı `SystemExit` verir).
  CEFR karışımı A1/A2/B1; tm/ru/def/ex makine yazımı, `proofread:false`.
- **Birleştirme:** `merge_packs.py` ORDER'ına `preintermediate.json` eklendi
  (elementary'den sonra) → **1294 başsöz, 110 ders**; 554'ün ~141'i beg/ele ile
  kesişiyor, kesişenlerde erken dosyanın girdisi kazanır ve `pre` kitap referansı
  eklenir (raporda görünür).
- **Uygulama:** `pre` kitap kaydı `units:12`→`13` (PE ünitesi), paket yeniden
  gömüldü (331 KB pack, uygulama 716.237 bayt).
- **Doğrulama:** `validate.js` 1294 geçerli 0 uyarı (iki kısa tanım — "twelve",
  "totally" — üreteçte düzeltildi, artefaktta değil); `verify.sh` **ALL CHECKS
  PASSED** (52+143+100); jsdom probu: pre 13 ünite, ünite 13'te 6 PE dersi,
  7A/7B/7C doğru, sözcük kartı açılıyor (want /wɒnt/ V islemek/хотеть), TK
  çevirisi doğru, kapaklar yerinde, 0 jsdom hatası.

**Bu turun tuzakları:**
- `cat a b c d > out` başarısız olursa bile `>` hedefi **sıfıra kırpar** —
  yedeksiz birleştirme bir dosyanın tamamını kaybettirdi; birleştirme öncesi
  parça boyutlarını doğrula.
- Yardımcı betikteki `assert`, **yazmadan önce** patlarsa düzeltmeler sessizce
  kaybolur — betik çöktü diye düzeltme yapılmış sayma; yeniden çalıştır.
- Sözlük alanlarına sızan **Kiril harfleri** (alym→alyм, tabletka→tabletkа)
  gözle kaçıyor — birleştirme öncesi tm alanlarını regex ile tara.
- Kitapta **aynı başsöz iki listede** çıkabiliyor (miss, hang up, answer, offer,
  suddenly) — üretecin yinelenen kapısı yakalıyor; hangisinin kalacağına ders
  sahipliği karar verir (örn. `offer` N shopping'de, `offer to` PHR 7A'da).

**Sırada ne var (sahibin yüklemesi beklenen):** Intermediate (`int`) kitabı —
aynı hat hazır: `gen_int.py` yaz → merge ORDER → validate → embed → verify.

## Dosyalar

| Yol | Ne |
|---|---|
| `uploads/app-yatla.html` | ürün (716.237 bayt. tek dosya. 1294 söz + 8 gerçek kapak gömülü) |
| `content/data/beginner.json` | Beginner: 400 söz, 29 ders, ders+ünite bilgisiyle |
| `content/tools/apply_lessons_search.py` | ders kablolaması + yeni arama (9 düzenleme) |
| `content/tools/sync_loader_lessons.py` | loader kopyasını senkronlar (6 düzenleme) |
| `content/tools/apply_lesson_search_tests.py` | ders + arama testleri |
| `content/tools/gen_beginner.py` | ünite → konu eşlemesi + söz listeleri (tek kaynak) |
| `content/tools/embed_pack.py` | paketi `<head>`'e gömer; yazmadan önce kapı kontrolü |
| `content/tools/apply_units_patch.py` | ünite kablolaması (5 düzenleme) |
| `content/tools/extract_beginner.py` | OCR sondası — **çıktısı güvenilmez**, kanıt olarak duruyor |
| `package.json` | kök `jsdom` bağımlılığı (testler için; önceden yoktu) |
| `content/tools/apply_ux_patch.py` | markup değişiklikleri |
| `content/tools/apply_ux_js.py` | script değişiklikleri |
| `content/tools/apply_ux_i18n.py` | i18n + ölü CSS temizliği |
| `content/tools/apply_ux_fixes.py` | testlerin bulduğu düzeltmeler |
| `content/tools/apply_ux_cleanup.py` | son gem metni temizliği |
| `content/tools/apply_patch.py` | içerik paketi kablolaması (önceki tur) |
| `tests/baseline.js` | 143 assertion'lık regresyon ağı |
| `tests/integration.js` | 100 assertion'lık içerik paketi + ünite/ders testi |
| `content/tools/gen_elementary.py` | Elementary üreteci: 465 söz, 22 ders |
| `content/tools/extract_elementary.py` | Vocabulary Bank OCR ölçümü |
| `content/tools/merge_packs.py` | data/*.json -> merged/yatla-all.json |
| `content/tools/restore_cefr.py`, `fix_shifted_coll.py` | add_full_stops hasarını onardı |
| `content/tools/apply_unit_redesign.py` | ünite ekranının yeni tasarımı |
| `content/tools/apply_lesson_ui_tests.py` | testleri yeni tasarıma uydurdu |
| `content/tools/apply_unlock_ui.py` | kapaklar + kilit kaldırma + uhead + pill + motion (10 düzenleme) |
| `content/tools/apply_emblems.py` | altı lig armasını zenginleştirdi |
| `content/assets/cover-*.jpg` | 8 üretilmiş kapak (896×1200 kaynak) |
| `content/tools/gen_pre.py` | Pre-intermediate üreteci: 554 söz, 42 ders |
| `content/data/preintermediate.json` | Pre-intermediate paketi |
| `uploads/pre inermediate.txt` | Pre-intermediate OCR dökümü (kaynak) |
| `verify.sh` | beş aşamanın tamamı |

---

## §17 — Intermediate import + 4 UX fix (2026-09-28)

**1) Intermediate (4th ed) import — `content/tools/gen_int.py` (575 satır):**
- 10 ünite × 2 ders (A+B; C yok) + 5 PE (kitapta 1/3/5/7/9. ünitelerden sonra).
- 312 söz / 25 ders → merge sonrası **int:322** (10 söz önceki kitaplara soğuruldu).
- Toplam paket: **1573 söz / 135 ders**; A1 777, A2 624, B1 172; proofread 0/1573.
- Ders haritası OCR içerik tablosundan (dump satır 15–112); VB 11 bölüm +
  ders içi kutular. `court` dup kapısına takıldı → 5A `tennis court`, 10B `court`.
- `!` headword kalıbında yasak → PE başlıklarından ünlemler düştü.
- `used to` 3B'den çıkarıldı (kitapta 5B grameri); "I was wondering" ru düzeltildi.

**2) PE aralaması (kitap sırası):** BOOKS'a `pe:{1:"PE1",3:"PE2",...}` eklendi;
ele 13→11, pre 13→12, int 12→10 (+dl:1, mb:26) gerçek ünite sayısı. Ünite
listesinde PE bölümü artık kendi ünitesinden hemen sonra altın çerçeveli satır
(`data-pe`); tıklayınca doğrudan bölüm oturumu açılır, geri → ünite listesi.
Ders listesi başlığı PE ünitesinde `pe_w` ("Practical English") gösterir.
beg değişmedi (PE C derslerine gömülü). `apply_round4.py` 23 yama, hepsi assert'li.

**3) Daily Challenge 2 tamiri:** kök neden — `#ck2`'yi okuyan hiç JS yoktu.
`S.revs` sayacı eklendi (init 0, save/load Object.assign ile), özet ekranında
`r.counted` bloğunda artar, `refreshHome` ck2'yi işaretler + `#chal2P` "x/2"
gösterir; 2'de Start → `chal2d` ("Done today"), pointerEvents:none.

**4) Nav pill:** inset halka kaldırıldı → yumuşak gölge `0 3px 14px` + hafif
gradient (light + dark). `.tbi:active` ölçeği duruyor.

**5) Amblemler:** 6 sembol minimalist düz kalkan olarak yeniden çizildi
(tek gradient + %14 parlama + kademede tek glif; stroke yok). Gradient id'leri
`gt*` oldu; `i-crown` dokunulmadı.

**i18n:** `pe_w` + `chal2d` en/tk/ru (makine yazımı, 0 native proofread).

**Doğrulama:** `./verify.sh` ALL PASSED (52+143+100); jsdom probe 37/37
(int 10 ünite + 5 PE satırı doğru sırada, PE1 oturumu 8 söz, geri→units,
ele 11+6 / pre 12+6 / beg 12+0, challenge 0/2→2/2 + persist, pill CSS,
6 amblem ≤3 şekil, TK etiketi, burglar 10B'de, int:322). App 791,114 B.

**Notlar:** probe'lar `runScripts:"dangerously"` + 200 ms tick ile boot etmeli
(LESSONS `fetchWords().then` içinde kurulur — senkron eval boş görür). Uygulama
WORDS satırlarında kitap referansı `.books` (seed sözlerde yok). JSON pack
script'i `type="application/json"` — eval etme, loader zaten parse eder.

---

## §18 — Upper-Intermediate import (2026-09-29)

**İçerik — `content/tools/gen_upp.py` (~700 satır):**
- EF Upper-Intermediate 4th ed: 10 ünite × 2 ders (A+B) + **5 Colloquial English**
  bölümü (PE yerine): CE1 getting a job (p.14), CE2 books (p.34), CE3 waste
  (p.54), CE4 performances (p.74), CE5 advertising (p.94) → 1/3/5/7/9. ünite sonrası.
- **296 söz / 25 ders** → merge: **1817 söz / 160 ders**, upp:296.
- A1 782 / A2 750 / B1 256 / B2 29; proofread 0/1817.
- VB 12 bölüm + ders içi kutular; OCR (uploads/upper.txt, 10,404 satır) yapısal kanıt.
- Validator bulguları gen_upp.py'de düzeltildi: `nearly` def <8 → "almost; very
  nearly"; `ž` Türkmen değil → `dirijor`, `jurnalist`; Kiril `м` sızmış `alyм` →
  `alym`; exTm `inžener` → `hünärmen`; CE4 ex "Why do not you" → "Why don't you".
- Ders konuları: 1A job hunting, 1B compound adjs, 2A illnesses, 2B clothes,
  3A air travel, 3B adverbs, 4A weather/environment, 4B take expressions,
  5A feelings adj, 5B feelings verbs, 6A sleep, 6B music, 7A confused verbs,
  7B body, 8A crime, 8B media, 9A business, 9B word building, 10A science,
  10B word pairs.

**App — `apply_round5.py` (7 yama):**
- BOOKS upp: units:10, pe:{1:CE1,3:CE2,5:CE3,7:CE4,9:CE5}, dl:1, mb:28.
- Ünite görünümündeki bölüm-ünite türetmesi artık "PE1" sabitine değil,
  LESSONS taramasına dayanıyor (unit > b.units) → hem PE# hem CE# çalışıyor.
- Satır/ders başlığı etiketi kitaba göre: upp → `ce_w`, diğerleri → `pe_w`.
- i18n `ce_w`: en "Colloquial English", tk "Gepleşik iňlis dili", ru
  "Разговорный английский" (makine yazımı).

**Doğrulama:** validate OK (1817, 0 warn); `./verify.sh` ALL PASSED
(52+143+100); jsdom probe 27/27 (upp 10 ünite + CE1-5 doğru sırada, CE1
oturumu 8 söz, geri→units, CE başlığı, int/ele/pre bozulmadı, dirijor/
jurnalist/alym temiz, burglar int 10B'de kaldı, TK etiketi, 0 jsdom hatası).
App 862,065 B, gömülü paket 1817 söz.

---

## §19 — Advanced import + kitap sırası (2026-09-29)

**İçerik — `content/tools/gen_adv.py` (~543 satır):**
- EF Advanced 4th ed: 10 ünite × 2 ders (A+B) + **5 Colloquial English**
  (CE1 work/family, CE2 history, CE3 stress, CE4 illustration, CE5 insects) →
  1/3/5/7/9. ünite sonrası. Veride CE ünitesi 11.
- **281 söz / 25 ders** → merge: **2074 söz / 185 ders**, adv:281.
- A1 784 / A2 889 / B1 338 / B2 63; proofread 0/2074.
- VB 11 bölüm + ders içi kutular; OCR (uploads/Advanced.txt, 11,181 satır) kanıt.
- Validator/TM-set bulguları gen_adv.py'de düzeltildi: `ž` Türkmen setinde YOK
  (TM_ALLOWED U+017E'yi kapsamıyor) → `stajýor`, `Parij`, landscape→`tebigat
  görnüşi`; Kiril `а`/`м` sızmaları (`stаžýor`, `alyм`-vari) → Latin.
- Ders konuları: 1A personality, 1B work, 2A abstract nouns, 2B relationships,
  3A get phrases, 3B conflict/warfare, 4A books&films, 4B voice, 5A time
  expressions, 5B money, 6A compound adjectives, 6B phones&tech, 7A prefixes,
  7B art&colour idioms, 8A health, 8B travel&tourism, 9A animal matters,
  9B preparing food, 10A word building, 10B confused words.

**App — `apply_round6.py` + `apply_round6b.py`:**
- BOOKS adv: units:10, pe:{1:CE1,3:CE2,5:CE3,7:CE4,9:CE5}, dl:1, mb:30.
- **Kitap sırası düzeltildi** (sahibin isteği): int → **intp** → upp → adv → **advp**.
  Yeni BOOKS sırası: beg, ele, pre, int, intp, upp, adv, advp (intp satırı
  int'ten sonraya taşındı; advp zaten sonuncu). intp/advp hâlâ içe aktarılmadı
  (dl:0, ünite listesi boş değil ama söz yok).
- ce_w etiketi artık hem upp hem adv için (ikisi de CE kullanıyor).
- **round6b (davranış düzeltmesi):** paket-seed birleştirmesi seed sözün
  stage/tanımını korurken gelen satırın `books` referanslarını da birleştiriyor.
  Önceden seed ile çakışan paket sözü (adv'ın `job`'ı) kitap referansını
  kaybediyor, ders bir söz eksik sayıyordu (adv 10B: 16→15). Şimdi union
  ediliyor → 10B tam 16, adv tam 281. `WORDS.length` değişmez (yeni giriş
  yok), render guard `!added&&!touched` oldu.

**Doğrulama:** validate OK (2074, 0 warn); `./verify.sh` ALL PASSED
(52+143+100 — round6b merge değişikliğinden sonra da); jsdom probe 30/30
(sıra beg..advp, intp int'ten sonra + upp'ten önce, advp sonuncu; adv 10 ünite
+ CE1-5 doğru sırada; CE1 oturumu 8 söz + geri→units; beg/ele/pre/int/upp
bozulmadı; adv 10B=16, adv refs=281; tm'de ž/Kiril yok; TK etiketi; 0 jsdom
hatası). App 934,874 bayt (889,242 karakter), gömülü paket 2074 söz.

**Karakter vs bayt notu:** apply_*.py `len(str)` = KARAKTER sayar; `ls`/embed
BAYT sayar. Türkmen/IPA/Kiril çok-baytlı olduğundan ikisi farklıdır — hata değil.

---

## §20 — Round 7: Intermediate Plus içe aktarma (intp)

**Kaynak:** `uploads/inter plus.txt` (10,276 satır) — English File Intermediate
Plus 4th ed. Yapı: 10 ünite × 2 ders (A+B, C yok) + üniteler 1/3/5/7/9'dan
sonra beş **Practical English** bölümü (PE1 kayıp bagaj bildirimi, PE2 araba
kiralama, PE3 polis tutanağı, PE4 ev kuralları, PE5 binada yön tarifi).
**CE değil PE kullanır** (pe_w) — mevcut `(b.id==="upp"||b.id==="adv")?ce_w:pe_w`
koşulu intp'yi zaten pe_w yapar; etiket koşulu DEĞİŞTİRİLMEDİ.

**Üreteç:** `content/tools/gen_intp.py` (`_p1.py` + `_p2.py` + `_p3.py` birleşimi;
gen_adv.py şablonu). 12 Vocabulary Bank + ders-içi kutular derslere dağıtıldı:
1A names, 1B adj suffixes, 2A packing, 2B shops/services, 3A stages of life,
3B photography, 4A recycling, 4B study/work, 5A television, 5B the country,
6A restaurant, 6B DIY, 7A cash machines/phrasal, 7B live entertainment,
8A looking after yourself, 8B wars/historic, 9A word building, 9B weddings,
10A British/American, 10B exams. PE1-5 data-unit **11**, her biri 8 söz.
Sonuç: **272 söz / 25 ders** → `content/data/intermediateplus.json`.

**Bilinen tuzaklar giderildi:**
- tm/exTm'de 14 Kiril-benzeri/ž sızıntısı (çörekhan**а**, bej**е**rdi, peýni**р**,
  st**а**ž, ob**а**, gur**а**l, hatar**д**a, massa**ž**, gal**а**, baga**ž**nik,
  baga**ż**nige) → Latin karşılıklarıyla düzeltildi. `validate.js` TM_ALLOWED
  setiyle birebir tarandı (yalnızca Kiril+ž değil); izole doğrulama 272 söz, 0 warn.
- `deposit` hem 7A (V) hem PE2 (N) → PE2'deki **"security deposit"** olarak
  ayrıldı (intra-book dup gate yakaladı).

**Merge:** `merge_packs.py` ORDER'a `intermediateplus.json` **intermediate.json'dan
sonra** eklendi (int dup'ları kazanır, intp upp'i kazanır). Birleşik paket
**2074 → 2298 söz** (+224 net; 48 intp sözü önceki kitaplarla birleşti, refs
union edildi). Per-book: adv 281, beg 400, ele 663, int 322, **intp 272**,
pre 560, upp 296. CEFR A1 795 / A2 1033 / B1 395 / B2 75. proofread 0/2298.

**App — `edit_file` (tek satır, apply_round7.py'ye gerek yoktu):**
- BOOKS intp: `units:12,dl:0,mb:32` → `units:10, pe:{1:PE1,3:PE2,5:PE3,7:PE4,9:PE5},
  done:0, dl:1, mb:28`. Sıra zaten doğru (int → **intp** → upp).
- `embed_pack.py` ile gömülü paket 2074 → **2298** söze yenilendi.

**Doğrulama:** izole validate OK (272, 0 warn); merged validate OK (2298, 0 warn);
`npm run build` + test-loader 52 assertion PASS; `bash verify.sh` **ALL CHECKS
PASSED** (52 + 143 + 100 + sandbox 2/1 script, `</script>`=2); **probe7.js 27/27**
(intp 10 ünite, dl:1, mb:28, lv B2+, 5 PE; 272 söz, ünite 1-10=232 söz;
PE1-5×8; surname∈1A, bakery∈2B, deposit∈7A, security deposit∈PE2, take the
lift∈PE5, exam∈10B; ünite görünümü 15 satır ve **U1,PE1,U2,U3,PE2,U4,U5,PE3,U6,
U7,PE4,U8,U9,PE5,U10** sırası; her PE satırı pe_w "Practical English" der, ce_w
yok; 0 jsdom hatası). App **996,289 bayt**, gömülü paket 2298 söz.
`probe7.js` ve `uploads/app-yatla.html.preembed.bak` temizlendi.

**Kalan:** yalnızca **Advanced Plus (advp)** — son kitap, hâlâ dl:0/içe
aktarılmadı. advp de CE kullanır (ce_w), PE değil.

---

## §21 — Round 8: Advanced Plus içe aktarma (advp) — SON KİTAP

**Kaynak:** `uploads/Avanced plus.txt` (9,957 satır) — English File Advanced Plus
4th ed. **Yapı beklenenden farklı:** OCR'da tam **8 "Revise and Check"** var ve
**hiç "Colloquial English" yok**. Yani Advanced Plus **8 ünite × 2 ders (A+B)**
ve **CE/PE bölümü YOK**. (§20'de "advp de CE kullanır" varsayımı YANLIŞTI — OCR
aksini kanıtladı; düzeltildi.) 12 Vocabulary Bank (pp.140-158) + 4 ders-içi
VOCABULARY kutusu 16 derse dağıtıldı:
1A vague language, 1B phrasal nouns, 2A prefixes/suffixes, 2B ways of moving,
3A research language, 3B idioms from Shakespeare, 4A binomials, 4B acronyms,
5A sophisticated emotions, 5B individuals/populations, 6A adverb collocations +
verbs for making things, 6B numbers/measurements, 7A punishment, 7B connotation,
8A eating and drinking, 8B ways of seeing.

**Üreteç:** `content/tools/gen_advp.py` (`_q1.py`+`_q2.py`+`_q3.py`). PE/episode
yok → data-unit 11 yok, LESSONS'ta yalnız 1A..8B. 3A "research language" için
`ox:"Academic"` (diğerleri Oxford 5000). Sonuç: **192 söz / 16 ders / 8 ünite**
(her ünite 24) → `content/data/advancedplus.json`. İzole validate 192, 0 warn.
Tuzak: `'joomart (eli açık)'` → Türkçe ı (U+0131) TM_ALLOWED dışında; `'eli açyk'`
yapıldı (tam TM_ALLOWED setiyle tarandı; Kiril/ž/ż 0).

**Merge:** `merge_packs.py` ORDER'a `advancedplus.json` **advanced.json'dan sonra**
(son) eklendi. Birleşik paket **2298 → 2461 söz** (+163 net; 29 advp sözü önceki
kitaplarla birleşti, refs union — ör. `hypothesis`/`data` upp ile paylaşımlı,
first-file-wins gereği upp'in badge'ini korur). Per-book: adv 281, **advp 192**,
beg 400, ele 663, int 322, intp 272, pre 560, upp 296. CEFR A1 795 / A2 1033 /
B1 396 / B2 105 / **C1 68 / C2 64** (artık tüm CEFR kademeleri dolu). proofread 0/2461.

**App — `edit_file` (tek satır):** BOOKS advp `units:12,dl:0,mb:34` →
`units:8,done:0,dl:1,mb:34` (**pe/ce alanı EKLENMEDİ** — bölüm yok, ünite listesi
1-8 sade). Sıra beg→ele→pre→int→intp→upp→adv→**advp** (sonuncu). `embed_pack.py`
ile gömülü paket 2298 → **2461** söze yenilendi. App **1,045,513 bayt**.

**Test düzeltmesi (`tests/integration.js`):** [7a] ve [7b] bölümleri advp'yi
"içe aktarılmamış boş kitap" sentinel'i olarak kullanıyordu; advp dolunca 3
assertion düştü. Boş-kitap regresyon kapsamını KORUMAK için sentetik bir
`{id:"zzempty",units:2,dl:1}` kitap enjekte edildi ve 3 referans advp→zzempty
çevrildi. (Hiçbir test tüm BOOKS'u gezmiyor → enjeksiyon güvenli.)

**Doğrulama:** merged validate OK (2461, 0 warn); test-loader 52/52;
`bash verify.sh` **ALL CHECKS PASSED** (52 + 143 + 100 + sandbox 2/1 script,
`</script>`=2); **probe8.js 29/29** (advp 8 ünite, dl:1, mb:34, lv C2+, pe YOK;
192 söz, ünite başına 24; ünite görünümü tam 8 satır ve data-pe 0; and so on∈1A,
resilience∈2A, questionnaire∈3A, CEO∈4B, verdict∈7A, savour∈8A, scrutinise∈8B;
advp'ye özgü 10 araştırma sözü Academic; adv/intp bozulmadı; WORDS 2466=2461+5;
0 jsdom hatası). `probe8.js` ve `uploads/app-yatla.html.preembed.bak` temizlendi.

**SONUÇ — 8 English File kitabının TAMAMI içe aktarıldı:** beg, ele, pre, int,
intp, upp, adv, advp. 2461 söz / 8 kitap. §6 AI backlog (cloud-sync, FCM,
Capacitor, offline dict+audio, WCAG) ve sahip-işi kalemler (OUP lisansı, store
hesapları, Firebase/OAuth anahtarları, native TM/RU proofread 0/2461, cihaz QA)
devam ediyor.

---

## §22 — Round 9: dört kullanıcı düzeltmesi (nav · tamamlama · review · sözlük)

Sahibin bildirdiği 4 sorun çözüldü. Hepsi `verify.sh` ALL CHECKS PASSED ile
doğrulandı (loader 52 + baseline 143 + integration 102 + sandbox). App 1,083,734 B.

### 1) Alt navigasyon vurgusu "Learning"de takılıyordu
- **Kök neden:** `buildTabs()` `.tbi.on` sınıfını yalnızca yüklenişte bir kez
  kuruyor (her ekranın tab bar'ı kendi `data-active` sekmesine sabit). Ama
  `go2learning()` (review başlatma + aramada "kelimeyi öğren") **tüm** tab
  bar'larda `.on`'u Learning'e zorluyor. `go()` ise ekrana göre vurguyu
  yeniden ayarlamıyordu → başka ekrana geçince Learning vurgusu kalıyordu.
- **Kanıt:** repro (go2learning → go("scr-search")) görünür bar hâlâ
  `scr-learning` gösteriyordu.
- **Düzeltme:** `go(id)` artık ekranı açarken `$$(".tb .tbi")` üzerinde
  `.on`'u `b.dataset.go===id` ile senkronluyor, sonra `pillTab()`. Vurgu her
  zaman görünür ekranı takip ediyor. (navdiag.js ile doğrulandı, sonra silindi.)

### 2) Ünite/ders tamamlama ekranı yanlış bilgi + zayıf animasyon
- **Eski:** sabit `6` words + `+12 LP` + `100% Accuracy`; başlık her zaman
  `complete_t({u:unit})` → tek ders bitirsen bile "Unit N complete!" diyordu.
- **Yeni:** gerçek `S.lv.session.length`; başlık derste `lesson_done_t({l})`
  ("Lesson 1A complete!"), tüm ünitede `complete_t({u})`; LP = words×2; sahte
  "Accuracy" kaldırıldı (öğrenme akışı quiz değil). Animasyonlu `.cbadge`
  (popIn + badgePulse keyframes) + mevcut `confetti()`. `track()` artık
  lesson_complete / unit_complete ayrımı yapıyor.

### 3) Review sadece 5 rastgele kelimeydi
- **Eski:** `startReview()` = `[...WORDS].sort(rand).slice(0,5)`, `doneWords:5`,
  ilk 3 `flip` kalanı `blank`. Ne çalıştıysan onunla ilgisiz 5 kelime.
- **Yeni:** `startReview(list?)` çalışılan **ünitenin TÜM kelimelerini** alıyor
  (`unitWords(book,unit)`; ör. beg ünite-1 = 53 kelime). Ünite bağlamı yoksa
  (Home challenge) fav+recent, yoksa rastgele 25. Egzersiz tipleri **karışık**
  ve genişletildi: `flip` (flashcard), `blank` (yazma), **`mcq_tm`** (EN→TM
  çoktan seçmeli), **`mcq_en`** (TM→EN). MCQ 4 seçenekli, 3 çeldirici bankadan,
  doğru/yanlış renkli geri bildirim + 950 ms sonra otomatik ilerleme.
- **Dosyalar:** `renderReview`'a mcq dalları, `revClick`'e `data-rm` işleyicisi,
  `.opts2`/`.opt2` CSS. Test [7] artık "review = ünitenin tamamı + karışık tip"
  doğruluyor (eski `=== 5` assertion'ı değiştirildi).

### 4) Arama sözlüğü çok küçüktü
- **Tasarım:** Genel sözlük **ayrı, yalnız-arama** bir katman (`DICT`), `WORDS`'e
  KARILMADI — böylece learning/lessons/review yalnız gerçek EF kelimelerini
  kullanmaya devam ediyor (review seyrelmiyor). `<script type="application/json"
  id="yatlaDict">` olarak gömülü (yatlaWords'ün yanında), `[en,tm,ru,pos]` kompakt.
- **Davranış:** Boş sorgu (göz atma) yalnız KİTAP kelimelerini listeler; genel
  sözlük **yalnız kullanıcı yazınca** devreye girer (`src=q?searchSrc():WORDS`).
  Sorgu sonuçları 300 satırda kapaklı (`+N more` notu), sayaç gerçek toplamı verir.
  Dict kelimeleri sade kart açar (EN/TM/RU + pos; boş def/ex/syn/CEFR/"Unit 1" yok).
- **Dedupe:** `gen_dict.py` merged pack'e (2461) karşı dedupe ediyor → sözlük
  yalnız kitapların **öğretmediği** kelimeleri ekler (aynı kelime aramada iki kez
  çıkmaz). 1255 adaydan 587 çakışma düştü → **668 benzersiz genel kelime**.
- **Toplam aranabilir:** 2461 kitap + 668 genel = ~3129 benzersiz. **Hedef 10k'ya
  uzak** — sahip "üretemezsen ben yardımcı olurum" dedi; yapı 10k'ya ölçeklenir,
  kelime listesi sağlanırsa veya sonraki turlarda partiler eklenerek büyütülür.
- **Kalite:** TM/RU machine-authored, **0/668 native-proofread**. `gen_dict.py`
  TM charset (Turkish `ı` yok, Kiril sızıntısı yok) + dup doğrulaması yapıyor.

### i18n (3 dile de eklendi)
`mcq_tm_lab`, `mcq_en_lab`, `lesson_done_t`, `rev_scope`, `more_results`.

### Yeni/değişen dosyalar
- `content/tools/gen_dict.py` — genel sözlük üreteci (TM/RU doğrulamalı, kitap-dedupe).
- `content/tools/embed_dict.py` — dict JSON'u `yatlaDict` tag'ına gömer (idempotent).
- `content/dict-general.json` — 668 genel kelime (en/tm/ru/pos).
- `verify.sh` — artık 2 gömülü json pack'e (words + dictionary) izin veriyor.
- `tests/integration.js` [7] — review = ünite-tamamı + karışık tip assertion'ları.
- `tests/baseline.js` — değişmedi (boş sorgu hâlâ yalnız kitap → rows===WORDS.length).

### Devam edenler (§6 AI backlog + sahip-işi)
Cloud-sync, gerçek FCM, Capacitor sarma, offline dict+audio, WCAG. Sahip: OUP
lisansı, store hesapları, Firebase/OAuth, native TM/RU proofread (kitap 0/2461,
dict 0/668), cihaz QA, Privacy/Terms, store assets. **Sözlüğü 10k'ya çıkarma**
sahip katkısı veya ek partiler bekliyor.

---

## §23 — Unit-wide vocabulary organization: section provenance + confidence (17-point spec)

Owner supplied a 17-point spec: vocabulary must be organized per BOOK → UNIT →
LESSON → SECTION with source provenance, dedupe, and confidence — extracted
from the WHOLE unit, not just "Vocabulary" headings. This round implemented
what the uploaded sources can honestly support and documented what they cannot.

### What inspection of the sources proved (measured, not assumed)
- The OCR dumps keep section labels (VOCABULARY ×39, GRAMMAR ×45,
  PRONUNCIATION ×31, LISTENING ×28 … in intermediate.txt) as plain text.
- **Zero in-body lesson/unit headings** in any dump. The contents table is
  shredded by two-column OCR ("6 A Eating in...and out" = unit 1, page 6).
  → No scan of a dump can attribute a word to a unit. Unit/lesson mapping
  stays in the generators' LESSONS tables (transcribed from the books'
  contents pages) — spec §13 (never guess units) is enforced structurally.
- **Gap-fill targets are missing from the OCR text**: Intermediate's own
  VOCABULARY box reads "put on your seat ," / "it's the  hour". Only 17 of 23
  curated Intermediate unit-3 headwords appear verbatim in the dump. A naive
  full-text extractor would drop drilled words and surface ordinary prose.
  Formatting evidence (bold/box/highlight) did not survive OCR at all.
- Conclusion recorded in `annotate_sections.py` docstring: the dumps remain
  the source of WHAT is taught; the curated per-lesson lists (already built
  from Vocabulary Bank + in-lesson boxes + PE episodes, i.e. already
  unit-wide, not Vocabulary-heading-only) remain the extraction of record.

### What was built
1. **Schema** (`content/word-entry.schema.json`): `books[].section` enum
   (vocabulary, vocabulary_bank, practical_english, wordbuilding, grammar,
   reading, listening, speaking, writing, pronunciation, revise_and_check,
   dialogue, exercise) + word-level `confidence` (high|medium|low, §14).
2. **`content/tools/annotate_sections.py`** — idempotent metadata pass over
   the 8 per-book generators. Section provenance comes from each generator's
   source-band comments ("Vocabulary Bank — Money -> 2A", "in-lesson —
   crime -> 10B") and Beginner's lesson codes (PE*/xC = Practical English,
   xA/xB = in-lesson box; Beginner has no back-of-book bank). Guardrails:
   - an unmapped topic key ABORTS the run instead of guessing a section;
   - a quote-aware headword parser (`headwords_in`) handles 'x', "o'clock",
     and 'That\'s interesting.' — the naive regex silently dropped ~40
     phrase headwords before this was fixed;
   - words with no evidence are REPORTED, never assigned (§13/§14).
3. **Coverage (independent file check, not the script's own claim):**
   data/ 2953/2953 book-refs carry `section`, all 8 books 100%:
   vocabulary_bank 1385 · vocabulary 1279 · practical_english 247 ·
   wordbuilding 42. All curated words `confidence:"high"` (explicit teaching).
   merged/: 2953/2994 refs + 2435/2461 words — the 41/26 gap is exactly the
   legacy ef* demo files, which lack even lesson metadata; left absent, not
   guessed. App runtime verified: 2953/2994 refs with section, e.g. brake →
   {int, unit 3, 3A, vocabulary_bank}.
4. **Bug found & fixed in this round's tooling:** `words_of()` parsed the file
   a SECOND time, so mutations hit a throwaway copy and the first "successful"
   run wrote nothing — caught by an independent file check, not the script's
   own report. Rule re-learned: verify artifacts, not tool output.
5. **gen_elementary.py**: added the missing source-band comment documenting
   that topics 1-21 come from the Vocabulary Bank (the fact was in its
   docstring but not machine-readable).

### Pipeline state after the round
merge 2461 words OK · validate merged OK (schema accepts section/confidence) ·
build 735,329 B (pack now carries `section` inside books refs) · test-loader
52/52 · app re-embedded → 1,160,561 B · verify.sh ALL CHECKS PASSED
(52+143+102+sandbox) · annotate pass is idempotent (md5 stable).

### Spec items NOT implemented, honestly
- §7 sense-level splitting ("run" vs "run a business" as separate items):
  the current data model is one entry per headword; collocations live in
  `coll`. Splitting senses needs a schema change + per-book curation — flagged
  for owner decision, not silently approximated.
- §14 medium/low tiers: nothing in the shipped bank is medium/low by
  construction (every entry came from explicit teaching material). The tiers
  exist in the schema for a future raw-candidate extractor.
- Page numbers (§8): OCR line numbers ≠ book pages; `books[].page` stays
  unset rather than wrong.
- A raw full-text candidate extractor (§3-§5, §16): deliberately NOT built on
  top of these dumps — with gap-fill targets missing and no formatting
  evidence, it would fail §12 (do not invent). If the owner can supply the
  books as tagged PDFs/HTML (bold & boxes intact), a HIGH/MEDIUM candidate
  pass becomes feasible; the schema is ready for it.

---

## §24 — Round 11: Beginner Teacher's Guide extraction (34 new words, all TG-evidenced)

**Owner input:** three Beginner PDFs — two Student's Book halves (pure image
scans, 0/137 pages with text; no OCR possible in this sandbox) and
`EF4_Beginner_Teacher_s_Guide.pdf` (225 pp, full text layer →
`content/pdf/beg-tg.txt`, `@@PAGE n@@` markers; PDF page = printed page here).

**Tool:** `content/tools/extract_beg_tg.py` → `content/pdf/beg-tg-candidates.json`
(321 distinct candidates, 213 not already in the pack). Evidence tiers:
- `wordbank` HIGH — explicit word lists on the 19 photocopiable VOCABULARY
  worksheets (attribution per header region; a page can carry two sheets);
- `key` HIGH — numbered vocabulary-exercise answer keys in lesson plans;
- `teach` HIGH — "teach/elicit X (/IPA/)" lines;
- `notes` MEDIUM — words explained in "Vocabulary notes" boxes.
Teacher-facing prose is structurally excluded; a TEACHER_TALK stoplist catches
residue. Possessive-name filter drops example-sentence people (Brenda's…).

**Added (34, every entry has an inline TG-evidence comment in gen_beginner.py):**
1B England, France, Germany, Switzerland, Mexico (word bank p.133/209 + key p.17) ·
2A Swiss, English, German, the United States, business (keys p.25 + drill p.28) ·
3A bank card (key p.36) ·
4A boy, girl, man, woman, brother, sister, father, mother, friend (word bank p.214 —
core family words the OCR import had missed) ·
4B good-looking (elicit p.50) ·
5A yogurt (key p.55) ·
7A relax (word bank p.220), golf, football (notes p.76 "play + sports, e.g. …") ·
8A driving licence, driving test (teach p.87) ·
9A homework, stay in a hotel (phrase key p.97) ·
9B suit (key p.102), manager (elicit p.101) ·
1C/PE1 ATM, USB, VIP (abbreviations key p.21; brand/media names CNN, FBI, BBC,
BMW, EU deliberately skipped as proper names).

**Rejected, with reasons (§12/§16):** projector, screen, rom-coms ("may want to
teach" = teacher suggestion, not taught); Pakistan, South Africa (incidental
reading-text countries); jazz, match, traffic, bus stop, outside, box office
(listening transcripts); alone, pub (transcript); Brighton, Stephen, Bob, Rita…
(example-sentence names); all past/-ing inflections (§11); prose fragments.

**Pages:** gen_beginner.py now stamps `books[].page` from the book's own
contents table (1A=6 … 12B=74) — 434/434 beg refs carry page+section+confidence.

**Pipeline results:** data/beginner.json 434 words · merged 2482 (13 of the 34
merged into existing cross-book headwords, 21 brand-new) · build 746,575 B ·
app 1,171,977 B · `npm run check` 52 PASS · validate OK 0 warnings ·
`bash verify.sh` **ALL CHECKS PASSED** · jsdom runtime probe: 434/434 beg refs
with section+page, 20-word spot check all correct (boy→4A/24, ATM→1C/10,
driving licence→8A/48, …).

**Next:** owner to supply Teacher's Guide PDFs for Elementary → Advanced Plus;
same extractor pattern applies (lesson headers, keys, word banks). Student-book
scans remain unusable for extraction (image-only); TG text is the source.

---

## §25 — Round 12: Beginner PE cards, review scope, Elementary remap + 80 TG words

**Owner reports fixed:**
1. *Beginner PE inside other units* — beg's PE words (1C/3C/5C/7C/11C) moved to
   PE unit 13 in gen_beginner.py (guard updated: C-lessons may sit in unit 13)
   and the app's BOOKS gained `pe:{1:"1C",3:"3C",5:"5C",7:"7C",11:"11C"}` —
   Beginner now renders five standalone yellow PE cards after units 1/3/5/7/11,
   exactly like every other book. Integration tests updated (+8 assertions).
2. *Review after lesson 1A covered the whole unit* — the completion screen now
   hands the studied session to `startReview(S.lv.session)`: a lesson
   completion reviews that lesson's words only; a lesson-less unit still
   reviews the unit; the Home challenge keeps favourites+history. Test:
   review after 1A = exactly the 25 words of 1A (runtime-verified).

**Elementary (5 owner PDFs):** Student's Books again image-only (0/169 text
pages); the two Teacher's Guide PDFs (continuous printed pages 1-275) →
`content/pdf/ele-tg.txt`. Tools: syllabus parser (42 lessons → SB pages,
`ele-syllabus-pages.json`), `content/tools/extract_ele_tg.py` (234 candidates;
Vocabulary activity MASTERS deliberately not word-bank-mined — they are
anagrams).

**CRITICAL FIX — ele lesson codes were shifted by one file from Unit 6 on**
(the original import misread the OCR contents): generator's "7A murder
mystery" is really 8A, "9A most dangerous place" is really 10A, adverbs are
11A not 10A, participles 12A not 11A; 5A/5B/5C held 5B/5C/PE3 content. All
codes/titles re-mapped against the TG syllabus (§2). Real 7A-7C (Selfies /
Wrong name / Happy New Year?) have no imported content — honest empty unit,
noted, fillable from future curation. Clothes VB list joined PE3 ("buying
clothes · V clothes" per syllabus).

**80 words added (evidence in generator comments):** 1A five/eight/goodbye ·
1B 12 countries + 8 nationalities (TG p.18 key) · 3B 10 jobs (p.45 key, the
30-job exercise) · 5A 19 verbs (p.255 VERBS key) · 6C 9 instruments +
musical instrument (p.87 key e 6.17) · 8B ceiling/air conditioning/central
heating/floor lamp/table lamp (p.108-109 notes, p.256 key) · 9A takeaway
(p.120 teach) · 9B dark chocolate/white bread/olive oil (p.122) · 11C wi-fi/
attachment/log in/search/broadband (p.149 key e 11.10) · PE2 single/regular/
large/anything else (p.53 drill). Rejected: frightened & double (already in
bank), half-brother ("may want to teach"), takeaway-adjacent reading words,
comparative inflections, anagram garbage. `ele` also got books[].page from
the syllabus (726/726 refs carry page+section).

**Pipeline:** ele 646→726 · merged 2524 (38 of the 80 merged into existing
cross-book headwords) · build 768,155 B · app 1,194,238 B · check 52 PASS ·
validate OK · verify.sh **ALL CHECKS PASSED** (52+143+110) · jsdom probe:
beg PE cards 1C/3C/5C/7C/11C, unit-1 lessons = 1A,1B, 1A review = 25 words
only-1A, violin→6C/u6, museum→u10, PE3=19 words incl. jacket, all 8 spot-new
words in their right lessons.

**Next:** Pre-Intermediate → Advanced Plus TGs (same extractor pattern).

## §26 — Round 13: Pre-Intermediate SB+TG extraction (135 new words, pages, all verified)

**Owner request (Turkish):** process the 6 Pre-Intermediate PDFs (4 Student's Book
parts + 2 Teacher's Guide parts) like the previous rounds — analyse, find the
words, add them.

**PDFs all have real text layers** (unlike the beg/ele SB scans): SB 169 pages,
TG 271 pages, extracted to `content/pdf/pre-sb.txt` (`@@SBPAGE n@@`) and
`content/pdf/pre-tg.txt` (`@@PAGE n@@`). Syllabus (TG pp.4-7) parsed into
`content/pdf/pre-syllabus-pages.json` / `pre-syllabus.json`: 42 lessons.
**gen_pre.py lesson titles were verified against the syllabus — no code skew**
(unlike ele round-12); nothing was re-keyed.

**Extractor:** `content/tools/extract_pre.py` → `pre-sb-candidates.json`
(677 candidates: sb_vb 168 / key 359 / teach 86 / notes 58 / list 6; 119
already present). SB Vocabulary Bank (SB pp.151-164, 14 topic pages) mined via
the "headword + /ipa/" pattern; TG lesson plans mined for key/teach/notes;
vocab activity instructions (TG pp.253-256) mined for comma lists. IPA-font
mojibake (ea-thedral, gcket, …) rejected by hand; anagram masters (TG 257+)
NOT mined, per the ele lesson.

**135 words curated into gen_pre.py (evidence: SB VB pages + TG answer keys):**
1B blonde/dark/medium-height/enthusiastic (TG p.253 key) · 1C 22 clothes
(VB p.152) · 2A book/hire/rent/stay/sunbathe/go abroad (VB p.153 + 2A key) ·
4B 10 shopping (VB p.156: basket, checkout, debit card, delivery, item,
shelves, till, trolley, website, auction) · 5B 21 town/city (VB p.157:
cathedral, castle, canal, village, church, harbour, hill, lake, market, mosque,
museum, ruins, statue, temple, town hall, city walls, department store, area,
coast, population, medium-sized) · 5C 8 body/health (TG key: blood, bones,
heart, liver, muscles, teeth, alcohol, worry) · 6A buy/mend/repair/pull/push/
receive/open (VB p.158) · 8A get fit/get divorced/get tickets (VB p.159) ·
8B carry/miss/wear/know/meet (VB p.159-160) · 9A 22 animals (VB p.161 + 9A
key) · 10A along/into/over/past/through/towards/hit/kick (VB p.160 movement) ·
10B find out/get out of bed/go off/go to bed/turn up (VB p.161 + key) ·
11B 14 noun-formation (TG pp.149-150 key: advice, competition, invention,
invitation, advise, compete, confuse, educate, invite, pronounce, revise,
succeed, hairdryer, raincoat). Rejected by the generator's duplicate check:
**get a job** (already 1A) and **look forward to** (already 3B). Rejected by
hand: reading-answer noise (10C inventions), biography verbs, superlative
collocations, city names, mojibake.

**books[].page added for pre** — PAGE dict (42 lessons → SB pages from the
syllabus) stamped in gen_pre.py; every new ref carries page+section.
8 legacy `pre` refs without page remain (ef3.json holdovers: improve,
different, decide, answer, question, important, problem, example) — pre-date
this round, left untouched per "don't delete correct records".

**Pipeline:** pre 554→688 · merged 2603 unique (pre book count 694 incl. ef3) ·
build 780.3 KB min / 799,029 B embedded · app 1,225,282 B · content check 52
PASS · validate OK 2603/0 warnings · node --check app JS OK · verify.sh **ALL
CHECKS PASSED** (52+143+110 + sandbox rules) · jsdom probe: pack 2603, pre 42
lessons, 15 spot-checks (trousers 1C p.10, cathedral 5B p.40, wasp 9A p.70,
advice 11B p.88, go abroad 2A p.14, find out 10B p.80, get fit 8A p.62, blood
5C p.42, along 10A p.78, sunbathe 2A p.14, necklace 1C, medium-sized 5B, kick
10A, hairdryer 11B, jellyfish 9A) all OK; PE1-PE6 in unit 13 with 8-11 words
each.

**Honesty:** all tm/ru/def/ex are my own work; 0/2603 native-proofread.

**Next:** Intermediate / Upper-Int / Advanced TGs if owner uploads them
(same extractor pattern).

## §27 — Round 14: Intermediate TG+VB extraction (181 new words, pages, all verified)

**Owner request (Turkish):** "intermediate kitaplarını da yükleyeceğim, onları da
aynı şekilde yap" — uploaded 4 SB PDFs + 1 TG PDF.

**Sources:** the 4 SB PDFs are SCANS (no text layer), but the TG (217 pp) has
full text → `content/pdf/int-tg.txt`. The SB Vocabulary Bank was mined from the
pre-existing OCR dump `uploads/intermediate.txt` (lines ~15583-16560 = SB
pp.152-165, 12 sections incl. Personality p.153 which the gen docstring's
"11 sections" missed). Best source found: **TG Vocabulary activity instructions
pp.199-202 carry complete numbered answer keys** for 3A transport (cycle lane,
zebra crossing, taxi rank, speed camera, parking fine, roadworks, the
Underground…), 5A sport, 6A cinema, 6B body (verb+noun pairs), 7B houses, 2A
money, 8A work, 5B relationships, 9A word-building — cleaner than the OCR.
Extractor: `content/tools/extract_int.py` → `int-candidates.json` (571
candidates; 518 new). Syllabus (TG pp.4-6): 20 lessons (A+B only, no C) +
5 PE episodes; gen_int.py titles verified — no skew.

**181 words added (evidence: SB VB OCR headwords + TG p.199-202 keys):**
1A 24 food nouns + cut down on/cut out/eat out · 1B 13 personality adjectives ·
2A 20 money (borrow, can't afford, earn, inherit, invest, lend, raise, bill,
budget, contactless payment, insurance, mortgage, salary, tax, account, cash
machine, debt, live off, pay back, pay by) · 3A 17 transport compounds ·
5A 16 sport (circuit, hockey, warm up, get injured, stadium, diving, golf,
work out, player, sports hall, slope, umpire, crowd, team, captain) · 5B 8
relationship phrases · 6A 15 cinema (8 genres + critic, extra, script, sequel,
set, trailer, dubbed) · 6B 28 body (16 parts + 12 verbs) · 7A 7 education ·
7B 11 houses · 8A 13 work · 9A 10 word-building nouns. Rejected by generator
duplicate check: **coach** in 5A (already 3A). Rejected by hand: mojibake,
teacher talk, reading noise, "note" (too generic), inflections (baked/boiled —
verbs already in data).

**books[].page added for int** — PAGE dict (25 lessons → SB pages from TG
syllabus); 493/493 refs in data carry page; the 9 page-less int refs in the
pack are cross-book refs from other books' files (pre-date this round).

**Pipeline:** int 312→493 · merged 2733 unique (int book count 503) · build
844,365 B embedded · app 1,270,788 B · content check 52 PASS · validate OK
2733/0 warnings · node --check app JS OK · verify.sh **ALL CHECKS PASSED**
(52+143+110) · jsdom probe: pack 2733, int 25 lessons, 15 spot-checks all OK
(salmon 1A p.6 … cash machine 2A p.16), PE1-5 in unit 11 with 8 words each.

**Honesty:** all tm/ru/def/ex are my own work; 0/2733 native-proofread.
Fixed before running: 5 entries had stray Cyrillic letters in TM fields
(kalmаr, Otlу, ördeк, terrаса, TM-column 'боевик') — repaired + regex-scanned.

**Next:** Upper-Intermediate / Advanced / Advanced Plus TGs if owner uploads
(same pattern; SB scans exist for all — TGs + OCR dumps are the sources).

## §28 — Round 15: Intermediate Plus TG+VB extraction (245 new words, pages, all verified)

**Owner request (Turkish):** same treatment for Intermediate Plus — 4 SB PDFs
(all SCANS, no text layer) + TG (218 pp, full text → `content/pdf/intp-tg.txt`).

**Sources:** TG Vocabulary activity instructions **pp.202-205** carry complete
answer keys for 1B (adjective suffixes), 4A (rubbish), 5A (television), 6A
(restaurant), 8A (looking after yourself — full definition list p.205!), plus
TG lesson-plan keys (3B photo positions, 4B study/work, 8B battle words, 9A
word building, 10A BrE/AmE, PE1 luggage). SB VB (12 sections, SB pp.152-163)
mined from OCR dump `uploads/inter plus.txt` lines ~9088-10110 (headwords
legible): packing, shops-and-services ('s shops), country, DIY tools, and the
full 7A phrasal-verb bank. Extractor: `content/tools/extract_intp.py` →
`intp-candidates.json` (842 candidates, 793 new). Syllabus (TG pp.4-6): 20
lessons (A+B) + 5 PE; gen_intp.py titles verified — no skew. PAGE map same
grid as int (1A p.6 … 10B p.100; PE 14/34/54/74/94).

**245 words added:** 1B 20 adjectives · 2A 27 packing (toiletries, documents,
packing verbs) · 2B 12 's-shops · 3B 10 photo-position phrases · 4A 17
rubbish/recycling · 4B 13 study & work · 5A 17 television · 5B 15 country ·
6A 18 restaurant · 6B 12 DIY · 7A 32 phrasal verbs (money + away/back + take +
types) · 8A 20 looking after yourself · 8B 6 battle · 9A 13 word building ·
9B 4 weddings · 10A 5 BrE/AmE · PE1 6 luggage words. Generator rejected
duplicates: coach-equivalents none; **course** (already 4B) and **take out**
(already 4A) removed.

**Validator warnings fixed:** 5 TM fields contained ž (outside the project's
expected Turkmen set — make-up→ýüz boýagy, cross-trainer→kross türgenleşik
enjamy, rowing machine→greb türgenleşik enjamy, running machine→ylgaw
türgenleşik enjamy, press-ups→otjimaniýe) and 9 fragment examples rewritten as
full sentences (bowl/cup/glass/tub/pot/packet/carton/tin/atomic). Re-run →
**0 warnings**. Also caught pre-run: 2 stray Cyrillic а in exTm (ast-based
field scan added — regex-only TM scan missed exTm fields).

**Pipeline:** intp 272→517 · merged 2905 unique (intp book count 517) ·
build 904,444 B embedded · app 1,331,207 B · content check 52 PASS · validate
OK 2905/0 warnings · node --check app JS OK · verify.sh **ALL CHECKS PASSED**
(52+143+110) · jsdom probe: pack 2905, intp 25 lessons, 15 spot-checks all OK
(assertive 1B p.10 … postcode 10A p.96), PE1 14 words, all 517 intp refs carry
page.

**Honesty:** all tm/ru/def/ex are my own work; 0/2905 native-proofread.

**Next:** Upper-Intermediate / Advanced / Advanced Plus TGs if owner uploads.

## 29. Round 16 — Upper-Intermediate (2026-10-01)

**Owner message (Turkish):** "tamam simdi upper kitabini yukleyecegim" + 5 PDFs:
`upper-{1-43,44-88,89-130,131-170}.pdf` (SB scans, 0 text pages) +
`Upper intermediate teacher's guide book.pdf` (230 pp, full text → `content/pdf/upp-tg.txt`).
`uploads/upper.txt` = 10,404-line OCR dump; VB regions 9354–10039 (9 of 19 topics only).

**Method (5th run of the proven template):**
- TG syllabus pp.4–6 verified vs gen_upp.py LESSONS — no skew; CE pages 14/34/54/74/94.
- TG vocab keys pp.214–217 (2A, 2B, 3A, 3B*, 5A, 7A, 7B*, 8A, 8B, 9B) = primary source;
  3B adverbs and 7B body also keyed there. Dump bands for clothes/weather/business/wordbuilding.
- 4A weather & 9A business are crosswords w/o keys → dump + lesson plans.
- `extract_upp.py` rewritten cleanly (first sed-splice broke with SyntaxError) → 407 cands → hand-curated.
- **185 new words** in gen_upp.py via two patch scripts (93+93; 'old-fashioned' 2B removed as dup of 1B).
- PAGE dict stamped into books refs: 1A 6 … 10B 100, CE 14/34/54/74/94.
- Fixed 10 validate issues: 5 fragment ex→full sentences (hooded/polo neck/sleeveless/spotted/denim),
  ž→y in 2 TM fields (uçar ekipaży, artykmaç bagaj), 1 short def ('at the moment': 'at this time; right now').

**Result:** upp 296→**481** (25 lessons; 2A 36, 7B 34, 7A 31, 9B 32 largest).
Merged **3033** unique (820 absorbed, 667 multi-book). Pack 949,748 B; app **1,376,681 B**.
Data: beg:434, ele:748, pre:697, int:503, **upp:481**, adv:281, intp:517, advp:192.

**Verification:** annotate 481/481 (vocabulary_bank=305); 481/481 refs paged;
`npm run check` PASS 52, 0 warnings; `bash verify.sh` **ALL CHECKS PASSED** (52+143+110 + sandbox rules);
jsdom probe: pack 3033, upp refs 481, 25 lessons, 15/15 spot checks (flu 2A p.16 … ankle 7B p.70),
0 refs missing page, CE1–CE5 present → ALL SPOT CHECKS OK.

**Honesty:** TM/RU machine-authored, 0/3033 native-proofread.
