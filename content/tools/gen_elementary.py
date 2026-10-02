#!/usr/bin/env python3
"""English File Elementary — vocabulary organised by the book's own structure.

WHERE THE WORDS COME FROM. Unlike the Beginner dump, this OCR kept the
Vocabulary Bank headwords legible, so the lists were read out of the book itself
(content/tools/extract_elementary.py measures how far that gets: 491 raw lines,
of which the real headwords are the ones used below). Exercise instructions,
audio cues and column bleed were rejected by hand.

Two things are NOT from the book and are flagged as such:
  - tm / ru / def / ex are my own work; the book is English-only. Every entry is
    proofread:false, so no native TM/RU check has happened.
  - the IPA below is written properly rather than copied from the OCR, whose
    phonetic characters are unreliable ("ba:ru:m" for /ˈbɑːruːm/).

STRUCTURE. Elementary's Vocabulary Bank is organised by TOPIC (16 sections,
p.148-164), not one-per-lesson, and two sections ("Verb phrases", "Time") are
used by more than one lesson. So the topics are declared once and then mapped
onto lessons; the mapping comes from the book's own cross-references
("p.149 Vocabulary Bank Countries" inside lesson 1B) and its contents table.

Unit and lesson layout, from the contents table (uploads/elementary.txt 18-190):
  1A Welcome to the class · 1B One world · 1C What's your email?
  2A Are you tidy or untidy? · 2B Made in America · 2C Slow down!
  3A Britain: the good and the bad · 3B YtoSd · 3C Love me, love my dog
  4A Family photos · 4B From morning to night · 4C Blue Zones
  5A Vote for me! · 5B A quiet life? · 5C A city for all seasons
  6A Selfies · 6B Wrong name, wrong place · 6C Happy New Year?
  7A A murder mystery · 7B A house with a history · 7C Room 333
  8A #mydinnerlastnight · 8B White gold · 8C Facts and figures
  9A The most dangerous place... · 9B Five continents in a day · 9C The fortune teller
  10A Culture shock · 10B Experiences or things? · 10C How smart is your phone?
  11A I've seen it ten times! · 11B He's been everywhere! · 11C The English File interview
  (units 1-10 also have a Practical English episode; those are communication
  lessons, so they carry no Vocabulary Bank words here)

Usage: python3 content/tools/gen_elementary.py
"""
import json
import os
import re
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'elementary.json')

# topic -> [ (en, ipa, pos, tm, ru, def, ex, exTm, cefr[, coll]) ]
T = {}

# ---- Vocabulary Bank p.148-164 — the topic sections, declared once and then
#      mapped onto lessons by the book's own cross-references (see STRUCTURE) ----
T['days_numbers'] = [
    ('Monday', '/ˈmʌndeɪ/', 'N', 'duşenbe', 'понедельник', 'the first day of the working week', 'The lesson is on Monday.', 'Sapak duşenbe güni.', 'A1', 'on Monday'),
    ('Tuesday', '/ˈtjuːzdeɪ/', 'N', 'sişenbe', 'вторник', 'the day after Monday', 'See you on Tuesday.', 'Sişenbe görüşeris.', 'A1', 'on Tuesday'),
    ('Wednesday', '/ˈwenzdeɪ/', 'N', 'çarşenbe', 'среда', 'the middle day of the working week', 'We meet on Wednesday.', 'Çarşenbe duşuşýarys.', 'A1', 'on Wednesday'),
    ('Thursday', '/ˈθɜːzdeɪ/', 'N', 'penşenbe', 'четверг', 'the day after Wednesday', 'She works on Thursday.', 'Penşenbe işleýär.', 'A1', 'on Thursday'),
    ('Friday', '/ˈfraɪdeɪ/', 'N', 'anna', 'пятница', 'the last day of the working week', 'It\'s Friday at last.', 'Ahyry anna geldi.', 'A1', 'on Friday'),
    ('Saturday', '/ˈsætədeɪ/', 'N', 'şenbe', 'суббота', 'the first day of the weekend', 'I sleep late on Saturday.', 'Şenbe giç turýaryn.', 'A1', 'on Saturday'),
    ('Sunday', '/ˈsʌndeɪ/', 'N', 'ýekşenbe', 'воскресенье', 'the last day of the week', 'Sunday is a quiet day.', 'Ýekşenbe asuda gün.', 'A1', 'on Sunday'),
    ('weekday', '/ˈwiːkdeɪ/', 'N', 'hepde güni', 'будний день', 'any day from Monday to Friday', 'I work on weekdays.', 'Hepde günleri işleýärin.', 'A1'),
    ('weekend', '/ˌwiːkˈend/', 'N', 'hepde ahyry', 'выходные', 'Saturday and Sunday', 'What do you do at the weekend?', 'Hepde ahyrynda näme edýärsiň?', 'A1', 'at the weekend'),
    ('zero', '/ˈzɪərəʊ/', 'NUM', 'nol', 'ноль', 'the number 0', 'It was five degrees below zero.', 'Noldan bäş gradus aşakdy.', 'A1'),
    ('eleven', '/ɪˈlevn/', 'NUM', 'on bir', 'одиннадцать', 'the number 11', 'The train leaves at eleven.', 'Otly on birde gidýär.', 'A1'),
    ('twelve', '/twelv/', 'NUM', 'on iki', 'двенадцать', 'the number 12', 'There are twelve months.', 'On iki aý bar.', 'A1'),
    ('thirteen', '/ˌθɜːˈtiːn/', 'NUM', 'on üç', 'тринадцать', 'the number 13', 'She is thirteen.', 'Ol on üç ýaşynda.', 'A1'),
    ('fourteen', '/ˌfɔːˈtiːn/', 'NUM', 'on dört', 'четырнадцать', 'the number 14', 'Fourteen people came.', 'On dört adam geldi.', 'A1'),
    ('fifteen', '/ˌfɪfˈtiːn/', 'NUM', 'on bäş', 'пятнадцать', 'the number 15', 'It takes fifteen minutes.', 'On bäş minut alýar.', 'A1'),
    ('sixteen', '/ˌsɪksˈtiːn/', 'NUM', 'on alty', 'шестнадцать', 'the number 16', 'He is sixteen.', 'Ol on alty ýaşynda.', 'A1'),
    ('seventeen', '/ˌsevnˈtiːn/', 'NUM', 'on ýedi', 'семнадцать', 'the number 17', 'My brother is seventeen.', 'Doganym on ýedi ýaşynda.', 'A1'),
    ('eighteen', '/ˌeɪˈtiːn/', 'NUM', 'on sekiz', 'восемнадцать', 'the number 18', 'She left school at eighteen.', 'On sekiz ýaşynda mekdebi gutardy.', 'A1'),
    ('nineteen', '/ˌnaɪnˈtiːn/', 'NUM', 'on dokuz', 'девятнадцать', 'the number 19', 'There are nineteen students.', 'On dokuz okuwçy bar.', 'A1'),
    ('twenty', '/ˈtwenti/', 'NUM', 'ýigrimi', 'двадцать', 'the number 20', 'I am twenty.', 'Men ýigrimi ýaşymda.', 'A1'),
    ('thirty', '/ˈθɜːti/', 'NUM', 'otuz', 'тридцать', 'the number 30', 'The film is thirty minutes late.', 'Film otuz minut giç.', 'A1'),
    ('forty', '/ˈfɔːti/', 'NUM', 'kyrk', 'сорок', 'the number 40', 'He is forty.', 'Ol kyrk ýaşynda.', 'A1'),
    ('fifty', '/ˈfɪfti/', 'NUM', 'elli', 'пятьдесят', 'the number 50', 'Fifty people were there.', 'Elli adam bardy.', 'A1'),
    ('sixty', '/ˈsɪksti/', 'NUM', 'altmyş', 'шестьдесят', 'the number 60', 'My mother is sixty.', 'Enem altmyş ýaşynda.', 'A1'),
    ('seventy', '/ˈsevnti/', 'NUM', 'ýetmiş', 'семьдесят', 'the number 70', 'Seventy years ago.', 'Ýetmiş ýyl öň.', 'A1'),
    ('eighty', '/ˈeɪti/', 'NUM', 'segsen', 'восемьдесят', 'the number 80', 'He is eighty.', 'Ol segsen ýaşynda.', 'A1'),
    ('ninety', '/ˈnaɪnti/', 'NUM', 'togsan', 'девяносто', 'the number 90', 'Ninety percent agreed.', 'Togsan göterimi razy boldy.', 'A1'),
    ('hundred', '/ˈhʌndrəd/', 'NUM', 'ýüz', 'сто', 'the number 100', 'A hundred and five people came.', 'Ýüz bäş adam geldi.', 'A1', 'a hundred and five'),
    ('thousand', '/ˈθaʊznd/', 'NUM', 'müň', 'тысяча', 'the number 1,000', 'Two thousand people live here.', 'Iki müň adam şu ýerde ýaşaýar.', 'A1'),
    ('million', '/ˈmɪljən/', 'NUM', 'million', 'миллион', 'the number 1,000,000', 'The city has three million people.', 'Şäherde üç million adam bar.', 'A1'),
    ('north', '/nɔːθ/', 'N', 'demirgazyk', 'север', 'the direction on your left when you face the rising sun', 'Sweden is in the north of Europe.', 'Şwesiýa Ýewropanyň demirgazygynda.', 'A1', 'in the north'),
    ('south', '/saʊθ/', 'N', 'günorta', 'юг', 'the direction opposite north', 'Italy is in the south.', 'Italiýa günortada.', 'A1', 'in the south'),
    ('east', '/iːst/', 'N', 'gündogar', 'восток', 'the direction where the sun rises', 'The sun rises in the east.', 'Gün gündogardan dogýar.', 'A1', 'in the east'),
    ('west', '/west/', 'N', 'günbatar', 'запад', 'the direction where the sun sets', 'The sun sets in the west.', 'Gün günbatarda ýaşýar.', 'A1', 'in the west'),
    ('continent', '/ˈkɒntɪnənt/', 'N', 'materik', 'континент', 'one of the seven large areas of land on Earth', 'Asia is the largest continent.', 'Aziýa iň uly materik.', 'A1'),
    ('Africa', '/ˈæfrɪkə/', 'N', 'Afrika', 'Африка', 'a continent south of Europe', 'Egypt is in Africa.', 'Müsür Afrikada.', 'A1'),
    ('Asia', '/ˈeɪʒə/', 'N', 'Aziýa', 'Азия', 'the largest continent', 'Turkmenistan is in Asia.', 'Türkmenistan Aziýada.', 'A1'),
    ('Australia', '/ɒˈstreɪliə/', 'N', 'Awstraliýa', 'Австралия', 'a continent and country in the south', 'Kangaroos live in Australia.', 'Kengurular Awstraliýada ýaşaýar.', 'A1'),
    ('Europe', '/ˈjʊərəp/', 'N', 'Ýewropa', 'Европа', 'a continent north of Africa', 'Spain is in Europe.', 'Ispaniýa Ýewropada.', 'A1'),
    ('North America', '/ˌnɔːθ əˈmerɪkə/', 'N', 'Demirgazyk Amerika', 'Северная Америка', 'the continent that contains the USA and Canada', 'Canada is in North America.', 'Kanada Demirgazyk Amerikada.', 'A1'),
    ('South America', '/ˌsaʊθ əˈmerɪkə/', 'N', 'Günorta Amerika', 'Южная Америка', 'the continent that contains Brazil', 'Brazil is in South America.', 'Braziliýa Günorta Amerikada.', 'A1'),
    ('African', '/ˈæfrɪkən/', 'ADJ', 'afrikaly', 'африканский', 'from Africa', 'African music is famous.', 'Afrika sazy meşhur.', 'A1'),
    ('Asian', '/ˈeɪʒn/', 'ADJ', 'aziýaly', 'азиатский', 'from Asia', 'Asian food is popular here.', 'Aziýa nahary meşhur.', 'A1'),
    ('Australian', '/ɒˈstreɪliən/', 'ADJ', 'awstraliýaly', 'австралийский', 'from Australia', 'He is Australian.', 'Ol awstraliýaly.', 'A1'),
    ('European', '/ˌjʊərəˈpiːən/', 'ADJ', 'ýewropaly', 'европейский', 'from Europe', 'a European country.', 'ýewropa ýurty', 'A1'),
    ('American', '/əˈmerɪkən/', 'ADJ', 'amerikan', 'американский', 'from the USA', 'an American film.', 'amerikan filmi', 'A1'),
    # five/eight — 1A activity key, TG p.253
    ('five', '/faɪv/', 'NUM', 'bäş', 'пять', 'the number 5', 'I get up at five.', 'Sagat bäşde turýaryn.', 'A1'),
    ('eight', '/eɪt/', 'NUM', 'sekiz', 'восемь', 'the number 8', 'We start at eight.', 'Sagat sekizde başlaýarys.', 'A1'),
]

# ---- Vocabulary Bank p.148 — countries & nationalities, Teacher's Guide round 12 key, TG p.18
#      ("2 a Argentina b England c Turkey d Scotland e the USA f Italy
#        3 a Germany b Spain c Ireland d Poland e Switzerland f Hungary",
#        "4 a Chinese b French c Czech d Russian e Brazilian f Mexican
#        g Egyptian h Japanese") — Vocabulary Bank p.148 material ----
T['countries'] = [
    ('Argentina', '/ˌɑːdʒənˈtiːnə/', 'N', 'Argentina', 'Аргентина', 'a country in South America', 'Messi is from Argentina.', 'Messi Argentinadan.', 'A1'),
    ('England', '/ˈɪŋɡlənd/', 'N', 'Angliýa', 'Англия', 'a country that is part of the UK', 'London is in England.', 'London Angliýada.', 'A1'),
    ('Turkey', '/ˈtɜːki/', 'N', 'Türkiýe', 'Турция', 'a country in Europe and Asia', 'They are from Turkey.', 'Olar Türkiýeden.', 'A1'),
    ('Scotland', '/ˈskɒtlənd/', 'N', 'Şotlandiýa', 'Шотландия', 'a country that is part of the UK', 'Edinburgh is in Scotland.', 'Edinburg Şotlandiýada.', 'A1'),
    ('the USA', '/ðə ˌjuː es ˈeɪ/', 'N', 'ABŞ', 'США', 'the United States of America', 'He is from the USA.', 'Ol ABŞ-dan.', 'A1'),
    ('Italy', '/ˈɪtəli/', 'N', 'Italiýa', 'Италия', 'a country in southern Europe', 'Rome is the capital of Italy.', 'Rim Italiýanyň paýtagty.', 'A1'),
    ('Germany', '/ˈdʒɜːməni/', 'N', 'Germaniýa', 'Германия', 'a country in central Europe', 'She is from Germany.', 'Ol Germaniýadan.', 'A1'),
    ('Spain', '/speɪn/', 'N', 'Ispaniýa', 'Испания', 'a country in south-west Europe', 'They speak Spanish in Spain.', 'Ispaniýada ispança gepleýärler.', 'A1'),
    ('Ireland', '/ˈaɪələnd/', 'N', 'Irlandiýa', 'Ирландия', 'an island country next to the UK', 'Dublin is in Ireland.', 'Dublin Irlandiýada.', 'A1'),
    ('Poland', '/ˈpəʊlənd/', 'N', 'Polşa', 'Польша', 'a country in central Europe', 'Warsaw is in Poland.', 'Warşawa Polşada.', 'A1'),
    ('Switzerland', '/ˈswɪtsələnd/', 'N', 'Şweýsariýa', 'Швейцария', 'a country in central Europe', 'Switzerland is famous for chocolate.', 'Şweýsariýa şokolady bilen meşhur.', 'A1'),
    ('Hungary', '/ˈhʌŋɡəri/', 'N', 'Wengeriýa', 'Венгрия', 'a country in central Europe', 'Budapest is in Hungary.', 'Budapeşt Wengeriýada.', 'A1'),
    ('Chinese', '/ˌtʃaɪˈniːz/', 'ADJ', 'hytaýly', 'китайский, китаец', 'from China', 'She is Chinese.', 'Ol hytaýly.', 'A1'),
    ('French', '/frentʃ/', 'ADJ', 'fransuz', 'французский, француз', 'from France', 'He is French.', 'Ol fransuz.', 'A1'),
    ('Czech', '/tʃek/', 'ADJ', 'çeh', 'чешский, чех', 'from the Czech Republic', 'Prague is a Czech city.', 'Praga çeh şäheri.', 'A1'),
    ('Russian', '/ˈrʌʃn/', 'ADJ', 'orus', 'русский', 'from Russia', 'She is Russian.', 'Ol orus.', 'A1'),
    ('Brazilian', '/brəˈzɪliən/', 'ADJ', 'braziliýaly', 'бразильский, бразилец', 'from Brazil', 'He is Brazilian.', 'Ol braziliýaly.', 'A1'),
    ('Mexican', '/ˈmeksɪkən/', 'ADJ', 'meksikaly', 'мексиканский, мексиканец', 'from Mexico', 'Mexican food is spicy.', 'Meksikan tagamlary ajy bolýar.', 'A1'),
    ('Egyptian', '/ɪˈdʒɪpʃn/', 'ADJ', 'müsürli', 'египетский, египтянин', 'from Egypt', 'The Egyptian museums are amazing.', 'Müsür muzeýleri haýran galdyryjy.', 'A1'),
    ('Japanese', '/ˌdʒæpəˈniːz/', 'ADJ', 'ýapon', 'японский, японец', 'from Japan', 'Japanese trains are very fast.', 'Ýapon otlulary gaty çalt.', 'A1'),
]

T['classroom'] = [
    ('open your books', '/ˈəʊpən jɔː bʊks/', 'PHR', 'kitaplaryňyzy açyň', 'откройте книги', 'what a teacher says to start reading', 'Open your books at page ten.', 'Kitaplaryňyzy onunjy sahypada açyň.', 'A1'),
    ('close the door', '/kləʊz ðə dɔː/', 'PHR', 'gapyny ýapyň', 'закройте дверь', 'what you say to shut a door', 'Close the door, please.', 'Gapyny ýapyň, haýyş.', 'A1'),
    ('answer the questions', '/ˈɑːnsə ðə ˈkwestʃənz/', 'PHR', 'soraglara jogap beriň', 'ответьте на вопросы', 'what a teacher asks you to do', 'Answer the questions in pairs.', 'Soraglara jübüt bolup jogap beriň.', 'A1'),
    ('stand up', '/stænd ʌp/', 'PHR', 'turuň', 'встаньте', 'to get to your feet', 'Stand up, please.', 'Turuň, haýyş.', 'A1'),
    ('sit down', '/sɪt daʊn/', 'PHR', 'oturyň', 'садитесь', 'to move onto a seat', 'Sit down and listen.', 'Oturyň we diňläň.', 'A1'),
    ('turn off your phone', '/tɜːn ɒf jɔː fəʊn/', 'PHR', 'telefonyňyzy öçüriň', 'выключите телефон', 'to stop a phone working', 'Turn off your phone in class.', 'Sapakda telefonyňyzy öçüriň.', 'A1'),
    ("I don't understand", '/aɪ dəʊnt ˌʌndəˈstænd/', 'PHR', 'düşünmeýärin', 'я не понимаю', 'what you say when something is not clear', "Sorry, I don't understand.", 'Bagyşlaň, düşünmeýärin.', 'A1'),
    ("I don't know", '/aɪ dəʊnt nəʊ/', 'PHR', 'bilmeýärin', 'я не знаю', 'what you say when you have no answer', "I'm afraid I don't know.", 'Gynansam-da bilmeýärin.', 'A1'),
    ('How do you spell...?', '/haʊ du ju spel/', 'PHR', 'nähili harplaýarys?', 'как это пишется по буквам?', 'used to ask for the letters of a word', 'How do you spell your name?', 'Adyňyzy nähili harplaýarys?', 'A1'),
    ('How do you say...?', '/haʊ du ju seɪ/', 'PHR', 'nähili aýdylýar?', 'как сказать...?', 'used to ask for a word in another language', 'How do you say "kitap" in English?', '"kitap" iňlisçe nähili aýdylýar?', 'A1'),
    ('Can you help me?', '/kæn ju help miː/', 'PHR', 'maňa kömek edip bilersiňizmi?', 'вы можете мне помочь?', 'used to ask for help politely', 'Can you help me with this exercise?', 'Bu maşka kömek edip bilersiňizmi?', 'A1'),
    ('What page is it?', '/wɒt peɪdʒ ɪz ɪt/', 'PHR', 'haýsy sahypa?', 'какая это страница?', 'used to ask which page to look at', 'What page is it? Page twelve.', 'Haýsy sahypa? On ikinji.', 'A1'),
]

T['things'] = [
    ('bag', '/bæɡ/', 'N', 'sumka', 'сумка', 'a soft container you carry things in', 'My bag is heavy.', 'Sumkam agyr.', 'A1'),
    ('coin', '/kɔɪn/', 'N', 'teňňe', 'монета', 'a flat round piece of metal money', 'I found a coin on the floor.', 'Ýerde bir teňňe tapdym.', 'A1'),
    ('credit card', '/ˈkredɪt kɑːd/', 'N', 'kredit kart', 'кредитная карта', 'a plastic card you use to pay later', 'Can I pay by credit card?', 'Kredit kart bilen töläp bilerinmi?', 'A1'),
    ('glasses', '/ˈɡlɑːsɪz/', 'N', 'äýnek', 'очки', 'two lenses in a frame you wear to see better', 'She wears glasses.', 'Ol äýnek geýýär.', 'A1', 'wear glasses'),
    ('headphones', '/ˈhedfəʊnz/', 'N', 'gulaklyk', 'наушники', 'a device you wear on your head to listen privately', 'I listen with headphones.', 'Gulaklyk bilen diňleýärin.', 'A1'),
    ('identity card', '/aɪˈdentəti kɑːd/', 'N', 'şahsyýetnama', 'удостоверение личности', 'an official card that shows who you are', 'Show your identity card.', 'Şahsyýetnamaňyzy görkeziň.', 'A1'),
    ('key', '/kiː/', 'N', 'açar', 'ключ', 'a shaped piece of metal that opens a lock', 'Where are my keys?', 'Açarlarym nirede?', 'A1', 'room key'),
    ('lamp', '/læmp/', 'N', 'çyra', 'лампа', 'an object that gives light', 'Turn on the lamp.', 'Çyrany ýak.', 'A1'),
    ('magazine', '/ˌmæɡəˈziːn/', 'N', 'jurnal', 'журнал', 'a thin book with articles and pictures', 'She reads a music magazine.', 'Saz jurnalyny okaýar.', 'A1'),
    ('pen', '/pen/', 'N', 'ruçka', 'ручка', 'an object you write with, using ink', 'Write in pen, please.', 'Ruçka bilen ýazyň, haýyş.', 'A1'),
    ('scissors', '/ˈsɪzəz/', 'N', 'gaýçy', 'ножницы', 'a tool with two blades used for cutting', 'Cut it with scissors.', 'Gaýçy bilen kesiň.', 'A1'),
    ('sunglasses', '/ˈsʌnɡlɑːsɪz/', 'N', 'gün äýnegi', 'солнечные очки', 'dark glasses worn in bright sun', 'I lost my sunglasses.', 'Gün äýnegimi ýitirdim.', 'A1', 'wear sunglasses'),
    ('umbrella', '/ʌmˈbrelə/', 'N', 'sätr', 'зонт', 'an object you hold above you to keep dry', 'Take an umbrella.', 'Sätr alyň.', 'A1'),
]

T['adjectives'] = [
    ('beautiful', '/ˈbjuːtɪfl/', 'ADJ', 'owadan', 'красивый', 'very pleasing to look at', 'What a beautiful view!', 'Nähili owadan görnüş!', 'A1'),
    ('big', '/bɪɡ/', 'ADJ', 'uly', 'большой', 'large in size', 'They live in a big flat.', 'Uly kwartirada ýaşaýarlar.', 'A1'),
    ('cheap', '/tʃiːp/', 'ADJ', 'arzan', 'дешёвый', 'costing little money', 'The tickets are cheap.', 'Biletler arzan.', 'A1'),
    ('clean', '/kliːn/', 'ADJ', 'arassa', 'чистый', 'not dirty', 'The room is clean.', 'Otag arassa.', 'A2'),
    ('dirty', '/ˈdɜːti/', 'ADJ', 'hapa', 'грязный', 'not clean', 'Your hands are dirty.', 'Elleriň hapa.', 'A1'),
    ('easy', '/ˈiːzi/', 'ADJ', 'aňsat', 'лёгкий', 'not difficult', 'The test was easy.', 'Synag aňsatdy.', 'A1'),
    ('difficult', '/ˈdɪfɪkəlt/', 'ADJ', 'kyn', 'трудный', 'not easy', 'This question is difficult.', 'Bu sorag kyn.', 'A2'),
    ('fast', '/fɑːst/', 'ADJ', 'çalt', 'быстрый', 'moving quickly', 'a fast train.', 'çalt otly', 'A1'),
    ('slow', '/sləʊ/', 'ADJ', 'haýal', 'медленный', 'not fast', 'The bus is slow.', 'Awtobus haýal.', 'A2'),
    ('full', '/fʊl/', 'ADJ', 'doly', 'полный', 'holding as much as possible', 'The bus is full.', 'Awtobus doly.', 'A1', 'full of'),
    ('empty', '/ˈempti/', 'ADJ', 'boş', 'пустой', 'holding nothing', 'The room was empty.', 'Otag boşdy.', 'A2'),
    ('good', '/ɡʊd/', 'ADJ', 'gowy', 'хороший', 'of a high standard', 'a good idea.', 'gowy pikir', 'A1'),
    ('bad', '/bæd/', 'ADJ', 'erbet', 'плохой', 'not good', 'The weather is bad.', 'Howa erbet.', 'A1'),
    ('high', '/haɪ/', 'ADJ', 'beýik, ýokary', 'высокий', 'tall or far up', 'a high wall.', 'beýik diwar', 'A2'),
    ('low', '/ləʊ/', 'ADJ', 'pes', 'низкий', 'not high', 'a low price.', 'pes baha', 'A2'),
    ('hot', '/hɒt/', 'ADJ', 'yssy', 'горячий', 'having a high temperature', 'The soup is hot.', 'Çorba gyzgyn.', 'A1'),
    ('cold', '/kəʊld/', 'ADJ', 'sowuk', 'холодный', 'having a low temperature', 'a cold drink.', 'sowuk içgi', 'A1'),
    ('light (weight)', '/laɪt/', 'ADJ', 'ýeňil', 'лёгкий (по весу)', 'not heavy', 'This bag is light.', 'Bu sumka ýeňil.', 'A2'),
    ('heavy', '/ˈhevi/', 'ADJ', 'agyr', 'тяжёлый', 'weighing a lot', 'a heavy box.', 'agyr guty', 'A2'),
    ('long', '/lɒŋ/', 'ADJ', 'uzyn', 'длинный', 'measuring a lot from end to end', 'a long journey.', 'uzyn ýol', 'A1'),
    ('short', '/ʃɔːt/', 'ADJ', 'gysga, kiçi boýly', 'короткий', 'not long, or not tall', 'a short film.', 'gysga film', 'A1'),
    ('old', '/əʊld/', 'ADJ', 'köne, garry', 'старый', 'not new', 'an old building.', 'köne bina', 'A1'),
    ('new', '/njuː/', 'ADJ', 'täze', 'новый', 'recently made', 'a new phone.', 'täze telefon', 'A1'),
    ('rich', '/rɪtʃ/', 'ADJ', 'baý', 'богатый', 'having a lot of money', 'a rich family.', 'baý maşgala', 'A2'),
    ('poor', '/pʊə/', 'ADJ', 'garyp', 'бедный', 'having little money', 'a poor village.', 'garyp oba', 'A2'),
    ('right', '/raɪt/', 'ADJ', 'dogry', 'правильный', 'correct, not wrong', 'the right answer.', 'dogry jogap', 'A1', 'the right answer'),
    ('wrong', '/rɒŋ/', 'ADJ', 'ýalňyş', 'неправильный', 'not correct', 'the wrong bus.', 'ýalňyş awtobus', 'A1', 'the wrong bus'),
    ('safe', '/seɪf/', 'ADJ', 'howpsuz', 'безопасный', 'not dangerous', 'The city is safe at night.', 'Şäher gije howpsuz.', 'A1'),
    ('dangerous', '/ˈdeɪndʒərəs/', 'ADJ', 'howply', 'опасный', 'able to hurt you', 'a dangerous road.', 'howply ýol', 'A2'),
    ('strong', '/strɒŋ/', 'ADJ', 'güýçli', 'сильный', 'having a lot of power', 'a strong wind.', 'güýçli şemal', 'A1'),
    ('weak', '/wiːk/', 'ADJ', 'gowşak', 'слабый', 'not strong', 'weak coffee.', 'gowşak kofe', 'A2'),
    ('tall', '/tɔːl/', 'ADJ', 'uzyn boýly', 'высокий (о росте)', 'having a lot of height', 'a tall man.', 'uzyn boýly adam', 'A1'),
    ('the same', '/ðə seɪm/', 'ADJ', 'meňzeş, şol bir', 'такой же', 'not different', 'We have the same bag.', 'Biziň sumkamyz meňzeş.', 'A2'),
    ('different', '/ˈdɪfrənt/', 'ADJ', 'dürli, başga', 'разный', 'not the same', 'two different answers.', 'iki dürli jogap', 'A1'),
    ('very', '/ˈveri/', 'ADV', 'örän, gaty', 'очень', 'used to make an adjective stronger', 'It is very cold.', 'Örän sowuk.', 'A1'),
    ('really', '/ˈrɪəli/', 'ADV', 'hakykatdan', 'действительно', 'used to say something is true or strong', 'It is really good.', 'Hakykatdan gowy.', 'A1'),
    ('quite', '/kwaɪt/', 'ADV', 'birneme, has', 'довольно', 'used to mean a little more than average', 'It is quite cold today.', 'Bu gün birneme sowuk.', 'A1'),
]

T['verbs'] = [
    ('cook', '/kʊk/', 'V', 'nahar bişirmek', 'готовить', 'to make food with heat', 'She cooks dinner every day.', 'Her gün agşamlyk bişirýär.', 'A1', 'cook dinner'),
    ('do', '/duː/', 'V', 'etmek', 'делать', 'to perform an action', 'I do my homework at night.', 'Öý işimi gije edýärin.', 'A1', 'do the housework'),
    ('drink', '/drɪŋk/', 'V', 'içmek', 'пить', 'to swallow liquid', 'I drink tea every morning.', 'Her irden çaý içýärin.', 'A1', 'drink water'),
    ('drive', '/draɪv/', 'V', 'sürmek', 'водить', 'to control a car', 'He drives to work.', 'Işe maşynly gidýär.', 'A1', 'drive a car'),
    ('eat', '/iːt/', 'V', 'iýmek', 'есть', 'to put food in your mouth and swallow it', 'We eat at one.', 'Sagat birde iýýäris.', 'A1'),
    ('go', '/ɡəʊ/', 'V', 'gitmek', 'идти', 'to move from one place to another', 'I go to school by bus.', 'Mektbe awtobusda gidýärin.', 'A1', 'go home'),
    ('have', '/hæv/', 'V', 'bolmak, bardy', 'иметь', 'to own or hold something', 'I have two brothers.', 'Iki agam bar.', 'A1', 'have a shower'),
    ('like', '/laɪk/', 'V', 'halamak', 'нравиться', 'to enjoy something', 'I like music.', 'Sazy halaýaryn.', 'A1', 'like doing'),
    ('listen', '/ˈlɪsn/', 'V', 'diňlemek', 'слушать', 'to pay attention to a sound', 'Listen to the teacher.', 'Mugallymy diňläň.', 'A1', 'listen to'),
    ('live', '/lɪv/', 'V', 'ýaşamak', 'жить', 'to have your home in a place', 'They live in London.', 'Londonda ýaşaýarlar.', 'A1', 'live in'),
    ('need', '/niːd/', 'V', 'zerur bolmak', 'нуждаться', 'to require something', 'I need a pen.', 'Maňa ruçka gerek.', 'A1', 'need to'),
    ('play', '/pleɪ/', 'V', 'oýnamak', 'играть', 'to do a game or sport', 'He plays tennis.', 'Tennis oýnaýar.', 'A1', 'play tennis'),
    ('read', '/riːd/', 'V', 'okamak', 'читать', 'to look at words and understand them', 'She reads the news.', 'Habarları okaýar.', 'A1', 'read a book'),
    ('say', '/seɪ/', 'V', 'aýtmak', 'сказать', 'to speak words', 'What did he say?', 'Ol näme aýtdy?', 'A1', 'say hello'),
    ('speak', '/spiːk/', 'V', 'gürlemek', 'говорить', 'to use words in a language', 'She speaks three languages.', 'Üç dilde gürleýär.', 'A1', 'speak English'),
    ('study', '/ˈstʌdi/', 'V', 'okamak, öwrenmek', 'учиться', 'to spend time learning', 'I study English.', 'Iňlis öwrenýärin.', 'A1', 'study English'),
    ('take', '/teɪk/', 'V', 'almak', 'брать', 'to get hold of something', 'Take your bag with you.', 'Sumkaňy özüň bilen al.', 'A1', 'take a photo'),
    ('want', '/wɒnt/', 'V', 'islemek', 'хотеть', 'to wish for something', 'I want a coffee.', 'Kofe isleýärin.', 'A1', 'want to'),
    ('watch', '/wɒtʃ/', 'V', 'seretmek', 'смотреть', 'to look at something for a time', 'We watch TV at night.', 'Gije telewizora seredýäris.', 'A1', 'watch TV'),
    ('wear', '/weə/', 'V', 'geýmek', 'носить', 'to have clothing on your body', 'She wears a blue coat.', 'Gök palto geýýär.', 'A1', 'wear a coat'),
    ('work', '/wɜːk/', 'V', 'işlemek', 'работать', 'to do a job', 'He works in a bank.', 'Bankda işleýär.', 'A1', 'work in'),
]

T['jobs'] = [
    ('accountant', '/əˈkaʊntənt/', 'N', 'hasapçy', 'бухгалтер', 'a person who keeps financial records', 'She is an accountant.', 'Ol hasapçy.', 'A1'),
    ('actor', '/ˈæktə/', 'N', 'aktýor', 'актёр', 'a person who acts in films or plays', 'He wants to be an actor.', 'Aktýor bolmak isleýär.', 'A1'),
    ('administrator', '/ədˈmɪnɪstreɪtə/', 'N', 'dolandyryjy', 'администратор', 'a person who organises a business or institution', 'She works as an administrator.', 'Dolandyryjy bolup işleýär.', 'A1'),
    ('architect', '/ˈɑːkɪtekt/', 'N', 'arhitektor', 'архитектор', 'a person who designs buildings', 'The architect designed this school.', 'Bu mekdebi arhitektor dizaýn etdi.', 'A1'),
    ('builder', '/ˈbɪldə/', 'N', 'gurluşykçy', 'строитель', 'a person whose job is building houses', 'My uncle is a builder.', 'Dayym gurluşykçy.', 'A1'),
    ('chef', '/ʃef/', 'N', 'aşpez', 'шеф-повар', 'a professional cook, especially in a restaurant', 'The chef made this dish.', 'Bu tagamy aşpez taýýarlady.', 'A1'),
    ('cleaner', '/ˈkliːnə/', 'N', 'arassalaýjy', 'уборщик', 'a person whose job is cleaning', 'The cleaner comes at six.', 'Arassalaýjy sagat altyda gelýär.', 'A1'),
    ('dentist', '/ˈdentɪst/', 'N', 'diş lukmany', 'стоматолог', 'a doctor for teeth', 'I go to the dentist twice a year.', 'Ýylda iki gezek diş lukmanyna barýaryn.', 'A1'),
    ('doctor', '/ˈdɒktə/', 'N', 'lukman', 'врач', 'a person who treats sick people', 'Call a doctor!', 'Lukman çagyryň!', 'A1'),
    ('driver', '/ˈdraɪvə/', 'N', 'sürüji', 'водитель', 'a person who drives a vehicle', 'The bus driver is friendly.', 'Awtobus sürüjisi mähirli.', 'A1', 'bus driver'),
    ('engineer', '/ˌendʒɪˈnɪə/', 'N', 'injener', 'инженер', 'a person who designs machines or structures', 'He is an engineer.', 'Ol injener.', 'A1'),
    ('farmer', '/ˈfɑːmə/', 'N', 'daýhan', 'фермер', 'a person who grows crops or keeps animals', 'The farmer has twenty cows.', 'Daýhanyň ýigrimi sygyry bar.', 'A1'),
    ('journalist', '/ˈdʒɜːnəlɪst/', 'N', 'jurnalist', 'журналист', 'a person who writes news reports', 'She is a journalist.', 'Ol jurnalist.', 'A1'),
    ('model', '/ˈmɒdl/', 'N', 'model', 'модель', 'a person whose job is showing clothes', 'She works as a model.', 'Model bolup işleýär.', 'A1'),
    ('musician', '/mjuˈzɪʃn/', 'N', 'sazanda', 'музыкант', 'a person who plays or writes music', 'He is a professional musician.', 'Hünärmen sazanda.', 'A1'),
    ('nurse', '/nɜːs/', 'N', 'şepagat uýasy', 'медсестра', 'a person who looks after sick people', 'The nurse helped me.', 'Şepagat uýasy kömek etdi.', 'A1'),
    ('photographer', '/fəˈtɒɡrəfə/', 'N', 'suratçy', 'фотограф', 'a person who takes photographs', 'The photographer took our picture.', 'Suratçy surata düşürdi.', 'A1'),
    ('pilot', '/ˈpaɪlət/', 'N', 'uçarman', 'пилот', 'a person who flies a plane', 'My cousin is a pilot.', 'Doganym uçarman.', 'A1'),
    ('police officer', '/pəˈliːs ˈɒfɪsə/', 'N', 'polisiýa işgäri', 'полицейский', 'a person whose job is to stop crime', 'A police officer stopped the car.', 'Polisiýa işgäri maşyny saklady.', 'A1'),
    ('receptionist', '/rɪˈsepʃənɪst/', 'N', 'resepsiýa işgäri', 'администратор', 'a person who welcomes guests', 'Ask the receptionist.', 'Resepsiýa işgärinden soraň.', 'A1'),
    ('sales assistant', '/seɪlz əˈsɪstənt/', 'N', 'satyjy', 'продавец', 'a person who serves customers in a shop', 'The sales assistant helped me.', 'Satyjy kömek etdi.', 'A1'),
    ('scientist', '/ˈsaɪəntɪst/', 'N', 'alym', 'учёный', 'a person who studies science', 'She is a scientist.', 'Ol alym.', 'A1'),
    ('teacher', '/ˈtiːtʃə/', 'N', 'mugallym', 'учитель', 'a person whose job is to teach', 'Our teacher is kind.', 'Mugallymymyz mähirli.', 'A1'),
    ('unemployed', '/ˌʌnɪmˈplɔɪd/', 'ADJ', 'işsiz', 'безработный', 'not having a job', 'He is unemployed at the moment.', 'Häzir işsiz.', 'A1'),
    ('writer', '/ˈraɪtə/', 'N', 'ýazyjy', 'писатель', 'a person who writes books or articles', 'She is a famous writer.', 'Meşhur ýazyjy.', 'A1'),
    # ---- jobs key e 3.10, TG p.45: "11 a factory worker 22 a flight
    #      attendant 13 a footballer 19 a hairdresser 12 a lawyer 14 a manager
    #      9 a soldier 29 a taxi driver 3 a vet 20 a waiter / a waitress" ----
    ('factory worker', '/ˈfæktri ˌwɜːkə/', 'N', 'fabrik işgäri', 'рабочий фабрики', 'a person who works in a factory', 'My uncle is a factory worker.', 'Daýym fabrik işgäri.', 'A2'),
    ('flight attendant', '/ˈflaɪt əˌtendənt/', 'N', 'uçar hyzmatdaşy', 'бортпроводник, стюардесса', 'a person who helps passengers on a plane', 'The flight attendant brought some water.', 'Uçar hyzmatdaşy biraz suw getirdi.', 'A2'),
    ('footballer', '/ˈfʊtbɔːlə/', 'N', 'futbolçy', 'футболист', 'a person who plays football', 'He wants to be a footballer.', 'Ol futbolçy bolmak isleýär.', 'A2'),
    ('hairdresser', '/ˈheədresə/', 'N', 'sertaraş', 'парикмахер', 'a person who cuts hair', 'The hairdresser cut my hair short.', 'Sertaraş saçymy gysga kesdi.', 'A2'),
    ('lawyer', '/ˈlɔːjə/', 'N', 'ýurist', 'юрист, адвокат', 'a person whose job is to help people with the law', 'She is a lawyer.', 'Ol ýurist.', 'A2'),
    ('manager', '/ˈmænɪdʒə/', 'N', 'müdir', 'менеджер, управляющий', 'the person in charge of a shop, office or hotel', 'The manager of the hotel is very friendly.', 'Myhmanhananyň müdiri gaty mähirli.', 'A2'),
    ('soldier', '/ˈsəʊldʒə/', 'N', 'esger', 'солдат', 'a person who serves in an army', 'The soldiers wear green uniforms.', 'Esgeler ýaşyl forma geýýärler.', 'A2'),
    ('taxi driver', '/ˈtæksi ˌdraɪvə/', 'N', 'taksi sürüjisi', 'таксист', 'a person who drives a taxi', 'The taxi driver knows every street.', 'Taksi sürüjisi ähli köçeleri bilýär.', 'A2'),
    ('vet', '/vet/', 'N', 'weterinar', 'ветеринар', 'a doctor for animals', 'The vet looked at our cat.', 'Weterinar pişigimize seretdi.', 'A2'),
    ('waitress', '/ˈweɪtrəs/', 'N', 'ofisantka', 'официантка', 'a woman who brings food in a restaurant', 'The waitress brought the bill.', 'Ofisantka hasaby getirdi.', 'A2'),
]

T['family'] = [
    ('father', '/ˈfɑːðə/', 'N', 'kaka', 'отец', 'a male parent', 'My father is a teacher.', 'Kakam mugallym.', 'A1'),
    ('mother', '/ˈmʌðə/', 'N', 'eje', 'мать', 'a female parent', 'My mother works at home.', 'Enem öýde işleýär.', 'A1'),
    ('brother', '/ˈbrʌðə/', 'N', 'aga, dogan', 'брат', 'a boy who has the same parents as you', 'My brother is ten.', 'Doganym on ýaşynda.', 'A1'),
    ('sister', '/ˈsɪstə/', 'N', 'uýa, aýal dogan', 'сестра', 'a girl who has the same parents as you', 'My sister is a student.', 'Uýam okuwçy.', 'A1'),
    ('son', '/sʌn/', 'N', 'ogul', 'сын', 'a male child', 'They have a son and a daughter.', 'Bir ogly we bir gyzy bar.', 'A1'),
    ('daughter', '/ˈdɔːtə/', 'N', 'gyz', 'дочь', 'a female child', 'Their daughter is at school.', 'Gyzy mekdepde.', 'A1'),
    ('grandfather', '/ˈɡrænfɑːðə/', 'N', 'ata', 'дедушка', 'the father of your parent', 'My grandfather is eighty.', 'Atam segsen ýaşynda.', 'A1'),
    ('grandmother', '/ˈɡrænmʌðə/', 'N', 'ene, mama', 'бабушка', 'the mother of your parent', 'My grandmother cooks well.', 'Enem gowy nahar bişirýär.', 'A1'),
    ('parents', '/ˈpeərənts/', 'N', 'ene-ata', 'родители', 'your mother and father', 'My parents live abroad.', 'Ene-atam daşary ýurtda.', 'A1'),
    ('aunt', '/ɑːnt/', 'N', 'bibi', 'тётя', 'the sister of your parent', 'My aunt lives in Turkey.', 'Bibim Türkiýede.', 'A1'),
    ('uncle', '/ˈʌŋkl/', 'N', 'daýy', 'дядя', 'the brother of your parent', 'My uncle is a driver.', 'Daýym sürüji.', 'A1'),
    ('cousin', '/ˈkʌzn/', 'N', 'dogan (bibi/daýy çagasy)', 'двоюродный брат/сестра', 'the child of your aunt or uncle', 'My cousin is my age.', 'Doganym meniň ýaşymda.', 'A1'),
    ('husband', '/ˈhʌzbənd/', 'N', 'äri', 'муж', 'the man a woman is married to', 'Her husband is a doctor.', 'Adamsy lukman.', 'A1'),
    ('wife', '/waɪf/', 'N', 'aýaly', 'жена', 'the woman a man is married to', 'His wife is a nurse.', 'Aýaly şepagat uýasy.', 'A1'),
    ('couple', '/ˈkʌpl/', 'N', 'jübüt', 'пара', 'two people who are married or in a relationship', 'An old couple walked past.', 'Garry jübüt geçdi.', 'A1'),
    ('stepfather', '/ˈstepfɑːðə/', 'N', 'öweý kaka', 'отчим', 'the new husband of your mother', 'My stepfather is kind.', 'Öweý kaka mähirli.', 'A1'),
    ('stepmother', '/ˈstepmʌðə/', 'N', 'öweý eje', 'мачеха', 'the new wife of your father', 'My stepmother cooks well.', 'Öweý ejem gowy bişirýär.', 'A1'),
    ('nephew', '/ˈnefjuː/', 'N', 'ýegen (oglan)', 'племянник', 'the son of your brother or sister', 'My nephew is five.', 'Ýegenim bäş ýaşynda.', 'A1'),
    ('niece', '/niːs/', 'N', 'ýegen (gyz)', 'племянница', 'the daughter of your brother or sister', 'My niece starts school.', 'Ýegenim mektbe başlaýar.', 'A1'),
    ('relative', '/ˈrelətɪv/', 'N', 'garyndaş', 'родственник', 'a member of your family', 'All my relatives live here.', 'Ähli garyndaşlarym şu ýerde.', 'A1'),
]

T['routine'] = [
    ('wake up', '/weɪk ʌp/', 'PHR', 'oýanmak', 'просыпаться', 'to stop sleeping', 'I wake up at six.', 'Sagat altyda oýanýaryn.', 'A1'),
    ('get up', '/ɡet ʌp/', 'PHR', 'turmak', 'вставать', 'to get out of bed', 'I get up at half past six.', 'Sagat altydan ýarymda turýaryn.', 'A1'),
    ('get dressed', '/ɡet drest/', 'PHR', 'egin-eşik geýmek', 'одеваться', 'to put clothes on', 'I get dressed quickly.', 'Çalt egin-eşik geýýärin.', 'A1'),
    ('have a shower', '/hæv ə ˈʃaʊə/', 'PHR', 'duş almak', 'принимать душ', 'to wash under a shower', 'I have a shower every morning.', 'Her irden duş alýaryn.', 'A1'),
    ('have breakfast', '/hæv ˈbrekfəst/', 'PHR', 'ertirlik iýmek', 'завтракать', 'to eat the first meal of the day', 'We have breakfast at seven.', 'Sagat ýedide ertirlik iýýäris.', 'A1'),
    ('start work', '/stɑːt wɜːk/', 'PHR', 'işe başlamak', 'начать работу', 'to begin your working day', 'I start work at nine.', 'Sagat dokuzda işe başlaýaryn.', 'A1'),
    ('finish work', '/ˈfɪnɪʃ wɜːk/', 'PHR', 'işi gutarmak', 'закончить работу', 'to stop working', 'She finishes work at five.', 'Sagat bäşde işi gutarýar.', 'A1'),
    ('have lunch', '/hæv lʌntʃ/', 'PHR', 'günortanlyk iýmek', 'обедать', 'to eat the middle meal', 'I have lunch at work.', 'Işde günortanlyk iýýärin.', 'A1'),
    ('do the housework', '/duː ðə ˈhaʊswɜːk/', 'PHR', 'öý işlerini etmek', 'заниматься домашней работой', 'to clean and tidy your home', 'I do the housework on Saturday.', 'Şenbe öý işlerini edýärin.', 'A1'),
    ('go shopping', '/ɡəʊ ˈʃɒpɪŋ/', 'PHR', 'bazara gitmek', 'ходить за покупками', 'to go out to buy things', 'We go shopping together.', 'Bile bazara gidýäris.', 'A1'),
    ('go to bed', '/ɡəʊ tə bed/', 'PHR', 'ýatmak', 'ложиться спать', 'to get into bed to sleep', 'I go to bed at eleven.', 'Sagat on birde ýatýaryn.', 'A1'),
]

T['time'] = [
    ("o'clock", '/əˈklɒk/', 'ADV', 'sagat', 'час (ровно)', 'used after a number for the exact hour', "It's six o'clock.", 'Sagat alty.', 'A1'),
    ('past', '/pɑːst/', 'PREP', 'geçen', 'после (о времени)', 'used for minutes after the hour', "It's ten past six.", 'Sagat altydan on geçen.', 'A2', 'ten past six'),
    ('to (time)', '/tuː/', 'PREP', 'çenli, galmak', 'до (о времени)', 'used for minutes before the hour', "It's five to seven.", 'Sagat ýedä bäş minut galdy.', 'A2', 'five to seven'),
    ('half past', '/ˌhɑːf ˈpɑːst/', 'PHR', 'ýarym', 'половина', 'thirty minutes after the hour', "It's half past six.", 'Sagat altydan ýarym.', 'A1'),
    ('quarter', '/ˈkwɔːtə/', 'N', 'çärýek', 'четверть', 'fifteen minutes', 'a quarter past six.', 'altydan çärýek geçen', 'A1'),
    ('first', '/fɜːst/', 'ORD', 'birinji', 'первый', 'coming before all others', 'the first of May.', 'birinji maý', 'A1'),
    ('second', '/ˈsekənd/', 'ORD', 'ikinji', 'второй', 'coming after the first', 'the second floor.', 'ikinji gat', 'A1'),
    ('third', '/θɜːd/', 'ORD', 'üçünji', 'третий', 'coming after the second', 'the third time.', 'üçünji gezek', 'A1'),
    ('fourth', '/fɔːθ/', 'ORD', 'dördünji', 'четвёртый', 'coming after the third', 'the fourth of July.', 'dördünji iýul', 'A1'),
    ('fifth', '/fɪfθ/', 'ORD', 'bäşinji', 'пятый', 'coming after the fourth', 'the fifth lesson.', 'bäşinji sapak', 'A1'),
    ('twelfth', '/twelfθ/', 'ORD', 'on ikinji', 'двенадцатый', 'coming after the eleventh', 'the twelfth of December.', 'on ikinji dekabr', 'A1'),
    ('twentieth', '/ˈtwentiəθ/', 'ORD', 'ýigriminji', 'двадцатый', 'coming after the nineteenth', 'the twentieth century.', 'ýigriminji asyr', 'A1'),
    ('twenty-first', '/ˌtwenti ˈfɜːst/', 'ORD', 'ýigrimi birinji', 'двадцать первый', 'coming after the twentieth', 'the twenty-first of March.', 'ýigrimi birinji mart', 'A1'),
    ('thirty-first', '/ˌθɜːti ˈfɜːst/', 'ORD', 'otuz birinji', 'тридцать первый', 'the last day of a 31-day month', 'the thirty-first of October.', 'otuz birinji oktýabr', 'A1'),
    ('date', '/deɪt/', 'N', 'sene', 'дата', 'the day, month and year', "What's the date today?", 'Bu gün nähili sene?', 'A1'),
    ('always', '/ˈɔːlweɪz/', 'ADV', 'elmydama', 'всегда', 'every time', 'I always walk to work.', 'Elmydama işe ýöräp barýaryn.', 'A1'),
    ('usually', '/ˈjuːʒuəli/', 'ADV', 'adatça', 'обычно', 'in most cases', 'I usually get up at seven.', 'Adatça ýedide turýaryn.', 'A1'),
    ('often', '/ˈɒfn/', 'ADV', 'köplenç', 'часто', 'many times', 'We often eat out.', 'Köplenç daşarda iýýäris.', 'A1'),
    ('sometimes', '/ˈsʌmtaɪmz/', 'ADV', 'käwagt', 'иногда', 'on some occasions', 'Sometimes I take the bus.', 'Käwagt awtobusda gidýärin.', 'A1'),
    ('hardly ever', '/ˈhɑːdli ˈevə/', 'ADV', 'diýen ýaly hiç', 'почти никогда', 'almost never', 'He hardly ever watches TV.', 'Diýen ýaly telewideniýe seretmeýär.', 'A1'),
    ('never', '/ˈnevə/', 'ADV', 'hiç haçan', 'никогда', 'not at any time', 'I never drink coffee at night.', 'Gije hiç haçan kofe içmeýärin.', 'A1'),
    ('once a week', '/wʌns ə wiːk/', 'PHR', 'hepdede bir gezek', 'раз в неделю', 'one time every week', 'I go swimming once a week.', 'Hepdede bir gezek ýüzmäge gidýärin.', 'A1'),
    ('twice a week', '/twaɪs ə wiːk/', 'PHR', 'hepdede iki gezek', 'два раза в неделю', 'two times every week', 'She goes to the gym twice a week.', 'Hepdede iki gezek sport zalyna gidýär.', 'A1'),
    ('every day', '/ˈevri deɪ/', 'PHR', 'her gün', 'каждый день', 'on all days', 'I study every day.', 'Her gün okaýaryn.', 'A1'),
    ('month', '/mʌnθ/', 'N', 'aý', 'месяц', 'one of the twelve parts of a year', 'this month.', 'şu aý', 'A1'),
    ('January', '/ˈdʒænjuəri/', 'N', 'ýanwar', 'январь', 'the first month', 'in January.', 'ýanwarda', 'A1'),
    ('February', '/ˈfebruəri/', 'N', 'fewral', 'февраль', 'the second month', 'in February.', 'fewralda', 'A1'),
    ('March', '/mɑːtʃ/', 'N', 'mart', 'март', 'the third month', 'in March.', 'martda', 'A1'),
    ('April', '/ˈeɪprəl/', 'N', 'aprel', 'апрель', 'the fourth month', 'in April.', 'aprelde', 'A1'),
    ('May', '/meɪ/', 'N', 'maý', 'май', 'the fifth month', 'in May.', 'maýda', 'A1'),
    ('June', '/dʒuːn/', 'N', 'iýun', 'июнь', 'the sixth month', 'in June.', 'iýunda', 'A1'),
    ('July', '/dʒuˈlaɪ/', 'N', 'iýul', 'июль', 'the seventh month', 'in July.', 'iýulda', 'A1'),
    ('August', '/ˈɔːɡəst/', 'N', 'awgust', 'август', 'the eighth month', 'in August.', 'awgustda', 'A1'),
    ('September', '/sepˈtembə/', 'N', 'sentýabr', 'сентябрь', 'the ninth month', 'in September.', 'sentýabrda', 'A1'),
    ('October', '/ɒkˈtəʊbə/', 'N', 'oktýabr', 'октябрь', 'the tenth month', 'in October.', 'oktýabrda', 'A1'),
    ('November', '/nəʊˈvembə/', 'N', 'noýabr', 'ноябрь', 'the eleventh month', 'in November.', 'noýabrda', 'A1'),
    ('December', '/dɪˈsembə/', 'N', 'dekabr', 'декабрь', 'the twelfth month', 'in December.', 'dekabrda', 'A1'),
]

T['weather'] = [
    ('weather', '/ˈweðə/', 'N', 'howa', 'погода', 'the condition of the air outside', "What's the weather like?", 'Howa nähili?', 'A1', "what's the weather like"),
    ('sunny', '/ˈsʌni/', 'ADJ', 'güneli', 'солнечный', 'with a lot of sun', 'a sunny day.', 'güneli gün', 'A1'),
    ('cloudy', '/ˈklaʊdi/', 'ADJ', 'bulutly', 'облачный', 'with a lot of clouds', 'It is cloudy today.', 'Bu gün bulutly.', 'A1'),
    ('rainy', '/ˈreɪni/', 'ADJ', 'ýagyşly', 'дождливый', 'with a lot of rain', 'a rainy afternoon.', 'ýagyşly günortan', 'A1'),
    ('windy', '/ˈwɪndi/', 'ADJ', 'şemally', 'ветреный', 'with a lot of wind', 'It is very windy.', 'Örän şemally.', 'A1'),
    ('snowy', '/ˈsnəʊi/', 'ADJ', 'garly', 'снежный', 'with a lot of snow', 'a snowy winter.', 'garly gyş', 'A1'),
    ('foggy', '/ˈfɒɡi/', 'ADJ', 'ümürli', 'туманный', 'with thick cloud near the ground', 'It is foggy this morning.', 'Bu irden ümürli.', 'A1'),
    ('warm', '/wɔːm/', 'ADJ', 'yljak', 'тёплый', 'pleasantly hot', 'a warm evening.', 'yljak agşam', 'A1'),
    ('cool', '/kuːl/', 'ADJ', 'salkyn', 'прохладный', 'pleasantly cold', 'a cool morning.', 'salkyn irden', 'A1'),
    ('wet', '/wet/', 'ADJ', 'ygally', 'мокрый', 'covered with water', 'The roads are wet.', 'Ýollar ygal.', 'A1'),
    ('dry', '/draɪ/', 'ADJ', 'gury', 'сухой', 'with no water on it', 'a dry summer.', 'gury tomus', 'A1'),
    ('season', '/ˈsiːzn/', 'N', 'pasyl', 'сезон, время года', 'one of the four parts of the year', 'Autumn is my favourite season.', 'Güýz iň halaýan paslym.', 'A1'),
    ('spring', '/sprɪŋ/', 'N', 'ýaz', 'весна', 'the season after winter', 'Flowers open in spring.', 'Ýazda güller açýar.', 'A1', 'in spring'),
    ('summer', '/ˈsʌmə/', 'N', 'tomus', 'лето', 'the hottest season', 'We swim in summer.', 'Tomusda ýüzýäris.', 'A1', 'in summer'),
    ('autumn', '/ˈɔːtəm/', 'N', 'güýz', 'осень', 'the season after summer', 'Leaves fall in autumn.', 'Güýzde ýapraklar gaçýar.', 'A1', 'in autumn'),
    ('winter', '/ˈwɪntə/', 'N', 'gyş', 'зима', 'the coldest season', 'It snows in winter.', 'Gyşda gar ýagýar.', 'A1', 'in winter'),
    ('temperature', '/ˈtemprətʃə/', 'N', 'temperatura', 'температура', 'how hot or cold something is', 'The temperature is twenty degrees.', 'Temperatura ýigrimi gradus.', 'A1'),
    ('degrees', '/dɪˈɡriːz/', 'N', 'gradus', 'градусы', 'units for measuring temperature', 'It is minus five degrees.', 'Minus bäş gradus.', 'A1'),
]

T['go_have_get'] = [
    ('go home', '/ɡəʊ həʊm/', 'PHR', 'öýe gitmek', 'идти домой', 'to travel to where you live', 'I go home at six.', 'Sagat altyda öýe gidýärin.', 'A1'),
    ('go out', '/ɡəʊ aʊt/', 'PHR', 'çykmak', 'выходить', 'to leave home for fun', 'We go out on Friday.', 'Anna güni gezme gidýäris.', 'A1'),
    ('go shopping', '/ɡəʊ ˈʃɒpɪŋ/', 'PHR', 'bazara gitmek', 'идти за покупками', 'to go out to buy things', 'She goes shopping on Saturday.', 'Şenbe bazara gidýär.', 'A1'),
    ('go to a restaurant', '/ɡəʊ tə ə ˈrestrɒnt/', 'PHR', 'restorana gitmek', 'идти в ресторан', 'to eat out', 'We went to a restaurant.', 'Restorana gitdik.', 'A1'),
    ('go by bus', '/ɡəʊ baɪ bʌs/', 'PHR', 'awtobusda gitmek', 'ехать на автобусе', 'to travel by bus', 'I go by bus.', 'Awtobusda gidýärin.', 'A1'),
    ('go by plane', '/ɡəʊ baɪ pleɪn/', 'PHR', 'uçarda gitmek', 'лететь самолётом', 'to travel by plane', 'We went by plane.', 'Uçarda gitdik.', 'A1'),
    ('have a coffee', '/hæv ə ˈkɒfi/', 'PHR', 'kofe içmek', 'выпить кофе', 'to drink a coffee', "Let's have a coffee.", 'Geliň kofe içeliň.', 'A1'),
    ('have a party', '/hæv ə ˈpɑːti/', 'PHR', 'toý/agşamçylyk geçirmek', 'устроить вечеринку', 'to hold a social event', 'They had a party.', 'Toý geçirdiler.', 'A1'),
    ('have a rest', '/hæv ə rest/', 'PHR', 'dynç almak', 'отдохнуть', 'to relax for a while', 'I had a rest after lunch.', 'Günortanlykdan soň dynç aldym.', 'A1'),
    ('have a good time', '/hæv ə ɡʊd taɪm/', 'PHR', 'gowy wagt geçirmek', 'хорошо провести время', 'to enjoy yourself', 'We had a good time.', 'Gowy wagt geçirdik.', 'A1'),
    ('get up', '/ɡet ʌp/', 'PHR', 'turmak', 'вставать', 'to get out of bed', 'I got up late.', 'Giç turdum.', 'A1'),
    ('get dressed', '/ɡet drest/', 'PHR', 'egin-eşik geýmek', 'одеться', 'to put clothes on', 'She got dressed quickly.', 'Çalt geýindi.', 'A1'),
    ('get home', '/ɡet həʊm/', 'PHR', 'öýe baryp ýetmek', 'добраться домой', 'to arrive home', 'I got home at nine.', 'Sagat dokuzda öýe bardym.', 'A1'),
    ('get to work', '/ɡet tə wɜːk/', 'PHR', 'işe baryp ýetmek', 'добраться до работы', 'to arrive at work', 'He gets to work at eight.', 'Sagat sekizde işe barýar.', 'A1'),
]

T['house'] = [
    ('bathroom', '/ˈbɑːθruːm/', 'N', 'ýuwunma otagy', 'ванная', 'a room with a bath and toilet', 'The bathroom is upstairs.', 'Ýuwunma otagy ýokarda.', 'A1'),
    ('bedroom', '/ˈbedruːm/', 'N', 'ýatylyş otagy', 'спальня', 'a room you sleep in', 'My bedroom is small.', 'Ýatylyş otagym kiçi.', 'A1'),
    ('dining room', '/ˈdaɪnɪŋ ruːm/', 'N', 'nahar otagy', 'столовая', 'a room where you eat meals', 'We eat in the dining room.', 'Nahar otagynda iýýäris.', 'A1'),
    ('garage', '/ˈɡærɑːʒ/', 'N', 'garazh', 'гараж', 'a building where you keep a car', 'The car is in the garage.', 'Maşyn garazhda.', 'A1'),
    ('garden', '/ˈɡɑːdn/', 'N', 'bag', 'сад', 'a piece of ground next to a house', 'We sit in the garden.', 'Bagda oturýarys.', 'A1'),
    ('hall', '/hɔːl/', 'N', 'girelge, zal', 'прихожая', 'the space just inside the front door', 'Leave your shoes in the hall.', 'Aýakgabyňyzy girelgede goýuň.', 'A1'),
    ('kitchen', '/ˈkɪtʃɪn/', 'N', 'aşhana', 'кухня', 'a room where you cook', 'She is in the kitchen.', 'Ol aşhanada.', 'A1'),
    ('living room', '/ˈlɪvɪŋ ruːm/', 'N', 'myhman otagy', 'гостиная', 'a room where you relax', 'We watch TV in the living room.', 'Myhman otagynda telewideniýe seredýäris.', 'A1'),
    ('study (room)', '/ˈstʌdi/', 'N', 'iş otagy', 'кабинет', 'a room used for working or reading', 'He works in his study.', 'Iş otagynda işleýär.', 'A1'),
    ('toilet', '/ˈtɔɪlət/', 'N', 'hajathana', 'туалет', 'a room with a toilet', 'Where is the toilet?', 'Hajathana nirede?', 'A1'),
    ('stairs', '/steəz/', 'N', 'merdiwan', 'лестница', 'steps that go up or down', 'The bedroom is up the stairs.', 'Ýatylyş otagy merdiwanyň ýokarsynda.', 'A1', 'up the stairs'),
    ('floor', '/flɔː/', 'N', 'pol, gat', 'пол, этаж', 'the surface you walk on, or a level of a building', 'the second floor.', 'ikinji gat', 'A1'),
    ('wall', '/wɔːl/', 'N', 'diwar', 'стена', 'a vertical side of a room or building', 'There is a picture on the wall.', 'Diwarda surat bar.', 'A1', 'on the wall'),
    ('armchair', '/ˈɑːmtʃeə/', 'N', 'kreslo', 'кресло', 'a comfortable chair with sides', 'He sat in the armchair.', 'Kresloda oturdy.', 'A1'),
    ('bath', '/bɑːθ/', 'N', 'wanna', 'ванна', 'a large container you wash in', 'I take a bath at night.', 'Gije wanna alýaryn.', 'A1', 'take a bath'),
    ('bed', '/bed/', 'N', 'düşek', 'кровать', 'a piece of furniture you sleep on', 'The bed is comfortable.', 'Düşek amatly.', 'A1', 'go to bed'),
    ('carpet', '/ˈkɑːpɪt/', 'N', 'haly', 'ковёр', 'thick material that covers a floor', 'a new carpet.', 'täze haly', 'A1'),
    ('cooker', '/ˈkʊkə/', 'N', 'plita', 'плита', 'a machine for cooking food', 'The cooker is new.', 'Plita täze.', 'A1'),
    ('cupboard', '/ˈkʌbəd/', 'N', 'şkaf', 'шкаф', 'furniture with doors for keeping things in', 'The cups are in the cupboard.', 'Pişgeler şkafda.', 'A1', 'in the cupboard'),
    ('dishwasher', '/ˈdɪʃwɒʃə/', 'N', 'gap ýuwýan maşyn', 'посудомоечная машина', 'a machine that washes plates and cups', 'Put it in the dishwasher.', 'Gap ýuwýan maşyna sal.', 'A1'),
    ('fireplace', '/ˈfaɪəpleɪs/', 'N', 'ojak', 'камин', 'a place in a wall where you make a fire', 'We sat by the fireplace.', 'Ojagyň ýanynda oturduk.', 'A1'),
    ('fridge', '/frɪdʒ/', 'N', 'sowadyjy', 'холодильник', 'a machine that keeps food cold', 'The milk is in the fridge.', 'Süýt sowadyjyda.', 'A1'),
    ('light', '/laɪt/', 'N', 'çyra', 'лампа, свет', 'a thing that gives light', 'Turn on the light.', 'Çyrany ýak.', 'A1', 'turn on the light'),
    ('microwave', '/ˈmaɪkrəweɪv/', 'N', 'mikrotolkunly bişiriji', 'микроволновая печь', 'a machine that heats food quickly', 'Heat it in the microwave.', 'Mikrotolkunly bişirijide gyzdyr.', 'A1'),
    ('mirror', '/ˈmɪrə/', 'N', 'aýna', 'зеркало', 'glass that shows your face', 'a large mirror.', 'uly aýna', 'A1'),
    ('plant', '/plɑːnt/', 'N', 'ösümlik', 'растение', 'a living thing that grows in soil', 'There are plants by the window.', 'Penjiräniň ýanynda ösümlikler bar.', 'A1'),
    ('shelf', '/ʃelf/', 'N', 'tekçe', 'полка', 'a flat board you put things on', 'The books are on the shelf.', 'Kitaplar tekçede.', 'A1'),
    ('shower', '/ˈʃaʊə/', 'N', 'duş', 'душ', 'a place where you wash under falling water', 'I had a shower.', 'Duş aldym.', 'A1', 'have a shower'),
    ('sofa', '/ˈsəʊfə/', 'N', 'diwan', 'диван', 'a long soft seat for several people', 'They sat on the sofa.', 'Diwanda oturdylar.', 'A1'),
    ('wardrobe', '/ˈwɔːdrəʊb/', 'N', 'eşik şkafy', 'гардероб', 'a tall cupboard for hanging clothes', 'My coat is in the wardrobe.', 'Paltom eşik şkafynda.', 'A1'),
    ('washing machine', '/ˈwɒʃɪŋ məʃiːn/', 'N', 'kir ýuwýan maşyn', 'стиральная машина', 'a machine that washes clothes', 'Put it in the washing machine.', 'Kir ýuwýan maşyna sal.', 'A1'),
]

T['prepositions'] = [
    ('in', '/ɪn/', 'PREP', 'içinde', 'в', 'inside something', 'in the kitchen.', 'aşhanada', 'A1'),
    ('on', '/ɒn/', 'PREP', 'üstünde', 'на', 'touching the top of something', 'on the table.', 'stoluň üstünde', 'A1'),
    ('under', '/ˈʌndə/', 'PREP', 'astynda', 'под', 'directly below', 'under the bed.', 'düşegiň astynda', 'A1'),
    ('above', '/əˈbʌv/', 'PREP', 'ýokarsynda', 'над', 'higher than', 'above the door.', 'gapynyň ýokarsynda', 'A1'),
    ('below', '/bɪˈləʊ/', 'PREP', 'aşagynda', 'ниже', 'lower than', 'below the window.', 'penjiräniň aşagynda', 'A1'),
    ('in front of', '/ɪn frʌnt əv/', 'PREP', 'öňünde', 'перед', 'directly ahead of', 'in front of the house.', 'öýüň öňünde', 'A1'),
    ('behind', '/bɪˈhaɪnd/', 'PREP', 'yzynda', 'за', 'at the back of', 'behind the sofa.', 'diwanyň yzynda', 'A1'),
    ('next to', '/nekst tuː/', 'PREP', 'ýanynda', 'рядом с', 'at the side of, very close', 'next to the bank.', 'bankyň ýanynda', 'A1'),
    ('opposite', '/ˈɒpəzɪt/', 'PREP', 'garşysynda', 'напротив', 'on the other side', 'opposite the park.', 'parkyň garşysynda', 'A1'),
    ('between', '/bɪˈtwiːn/', 'PREP', 'arasynda', 'между', 'separating two things', 'between the shop and the café.', 'dükan bilen kafeniň arasynda', 'A1'),
    ('over', '/ˈəʊvə/', 'PREP', 'üstünden, ýokarsynda', 'через, над', 'directly above, or across', 'a bridge over the river.', 'derýanyň üstünden köpri', 'A1'),
    ('into', '/ˈɪntə/', 'PREP', 'içine', 'в (направление)', 'to the inside of', 'He walked into the room.', 'Otagyň içine girdi.', 'A1'),
    ('out of', '/aʊt əv/', 'PREP', 'daşyna, içinden', 'из', 'from the inside to the outside', 'She came out of the shop.', 'Dükanyň daşyna çykdy.', 'A1'),
    ('through', '/θruː/', 'PREP', 'içinden, üsti bilen', 'через', 'from one side to the other', 'We walked through the park.', 'Parkyň içinden geçdik.', 'A1'),
    ('up', '/ʌp/', 'PREP', 'ýokary, ýokaryk', 'вверх', 'towards a higher place', 'up the stairs.', 'merdiwan bilen ýokary', 'A1'),
    ('down', '/daʊn/', 'PREP', 'aşak, aşaklyk', 'вниз', 'towards a lower place', 'down the street.', 'köçeden aşak', 'A1'),
    ('from', '/frɒm/', 'PREP', '-den', 'из, от', 'starting at a place', 'from Ashgabat.', 'Aşgabatdan', 'A1'),
    ('to', '/tuː/', 'PREP', '-e, -a', 'в, к', 'towards a place', 'to the station.', 'stansiýa', 'A1'),
    ('along', '/əˈlɒŋ/', 'PREP', 'boýuna', 'вдоль', 'following the length of', 'along the river.', 'derýanyň boýuna', 'A1'),
    ('across', '/əˈkrɒs/', 'PREP', 'üsti bilen, garşysyna', 'через', 'from one side to the other', 'across the road.', 'ýoluň garşysyna', 'A1'),
]

T['food'] = [
    ('bread', '/bred/', 'N', 'çörek', 'хлеб', 'a food made from flour and water', 'I bought some bread.', 'Biraz çörek aldym.', 'A1'),
    ('butter', '/ˈbʌtə/', 'N', 'ýag', 'сливочное масло', 'a soft yellow food made from cream', 'bread and butter.', 'çörek bilen ýag', 'A1'),
    ('cereal', '/ˈsɪəriəl/', 'N', 'gury ertirlik', 'хлопья', 'a breakfast food eaten with milk', 'cereal with milk.', 'süýt bilen gury ertirlik', 'A1'),
    ('coffee', '/ˈkɒfi/', 'N', 'kofe', 'кофе', 'a hot dark drink', 'a cup of coffee.', 'bir piýale kofe', 'A1'),
    ('eggs', '/eɡz/', 'N', 'ýumurtga', 'яйца', 'food laid by hens', 'two boiled eggs.', 'iki gaýnadylan ýumurtga', 'A1'),
    ('jam', '/dʒæm/', 'N', 'mürebbä', 'варенье', 'a sweet food made from fruit', 'jam on toast.', 'tostda mürebbä', 'A1'),
    ('milk', '/mɪlk/', 'N', 'süýt', 'молоко', 'a white drink from cows', 'a glass of milk.', 'bir stakan süýt', 'A1'),
    ('sugar', '/ˈʃʊɡə/', 'N', 'şeker', 'сахар', 'a sweet white substance', 'no sugar, please.', 'şekersiz, haýyş', 'A1'),
    ('tea', '/tiː/', 'N', 'çaý', 'чай', 'a hot drink made with leaves', 'a cup of tea.', 'bir piýale çaý', 'A1'),
    ('toast', '/təʊst/', 'N', 'gyzardylan çörek', 'тост', 'bread made warm and crisp', 'toast for breakfast.', 'ertirlik üçin tost', 'A1'),
    ('juice', '/dʒuːs/', 'N', 'şire', 'сок', 'a drink made from fruit', 'orange juice.', 'pytykal şiresi', 'A1'),
    ('fish', '/fɪʃ/', 'N', 'balyk', 'рыба', 'an animal from water eaten as food', 'fresh fish.', 'täze balyk', 'A1'),
    ('salmon', '/ˈsæmən/', 'N', 'losos', 'лосось', 'a large fish eaten as food', 'grilled salmon.', 'grillenen losos', 'A1'),
    ('herbs', '/hɜːbz/', 'N', 'ot-çöpler', 'травы, зелень', 'plants used to add flavour', 'fresh herbs.', 'täze ot-çöpler', 'A1'),
    ('meat', '/miːt/', 'N', 'et', 'мясо', 'flesh of animals eaten as food', 'He does not eat meat.', 'Et iýmeýär.', 'A1'),
    ('sausages', '/ˈsɒsɪdʒɪz/', 'N', 'kolbasa', 'сосиски', 'meat in a thin skin', 'sausages and eggs.', 'kolbasa bilen ýumurtga', 'A1'),
    ('ham', '/hæm/', 'N', 'windçina', 'ветчина', 'meat from a pig\'s leg', 'a ham sandwich.', 'windçina sendwiçi', 'A1'),
    ('pasta', '/ˈpæstə/', 'N', 'makaron', 'паста', 'an Italian food made from flour', 'pasta with cheese.', 'peýnirli makaron', 'A1'),
    ('rice', '/raɪs/', 'N', 'tüwi', 'рис', 'small grains cooked and eaten', 'rice and chicken.', 'tüwi bilen towuk', 'A1'),
    ('salad', '/ˈsæləd/', 'N', 'salat', 'салат', 'a dish of raw vegetables', 'a green salad.', 'ýaşyl salat', 'A1'),
    ('seafood', '/ˈsiːfuːd/', 'N', 'deňiz önümleri', 'морепродукты', 'fish and shellfish eaten as food', 'I love seafood.', 'Deňiz önümlerini gowy görýärin.', 'A1'),
    ('spices', '/ˈspaɪsɪz/', 'N', 'ysly ot-çöpler', 'специи', 'substances that give food flavour', 'Indian spices.', 'hin ysly otlary', 'A1'),
    ('carrots', '/ˈkærəts/', 'N', 'käşir', 'морковь', 'long orange vegetables', 'raw carrots.', 'çig käşir', 'A1'),
    ('chips', '/tʃɪps/', 'N', 'kartoşka fri', 'картофель фри', 'long pieces of fried potato', 'fish and chips.', 'balyk bilen kartoşka fri', 'A1'),
    ('lettuce', '/ˈletɪs/', 'N', 'salat ýapragy', 'салат', 'a plant with green leaves eaten raw', 'a lettuce.', 'bir salat ýapragy', 'A1'),
    ('mushrooms', '/ˈmʌʃruːmz/', 'N', 'kömelek', 'грибы', 'soft round things you eat', 'fried mushrooms.', 'gowrulan kömelek', 'A1'),
    ('onions', '/ˈʌnjənz/', 'N', 'sogan', 'лук', 'round vegetables with a strong smell', 'chopped onions.', 'dogranan sogan', 'A1'),
    ('peas', '/piːz/', 'N', 'noýba', 'горох', 'small green seeds you eat', 'peas and carrots.', 'noýba bilen käşir', 'A1'),
    ('peppers', '/ˈpepəz/', 'N', 'bolgar burçy', 'перец', 'hollow red or green vegetables', 'red peppers.', 'gyzyl bolgar burçy', 'A1'),
    ('potatoes', '/pəˈteɪtəʊz/', 'N', 'ýeralma', 'картофель', 'round vegetables that grow underground', 'boiled potatoes.', 'gaýnadylan ýeralma', 'A1'),
    ('tomatoes', '/təˈmɑːtəʊz/', 'N', 'pomidor', 'помидоры', 'soft red vegetables', 'tomatoes and cheese.', 'pomidor bilen peýnir', 'A1'),
    ('apples', '/ˈæplz/', 'N', 'alma', 'яблоки', 'round fruit with green or red skin', 'two apples.', 'iki alma', 'A1'),
    ('bananas', '/bəˈnɑːnəz/', 'N', 'banan', 'бананы', 'long yellow fruit', 'ripe bananas.', 'bişen banan', 'A1'),
    ('oranges', '/ˈɒrɪndʒɪz/', 'N', 'pytykal', 'апельсины', 'round orange fruit', 'sweet oranges.', 'süýji pytykal', 'A1'),
    ('pineapple', '/ˈpaɪnæpl/', 'N', 'ananas', 'ананас', 'a large tropical fruit', 'a slice of pineapple.', 'bir dilim ananas', 'A1'),
    ('strawberries', '/ˈstrɔːbəriz/', 'N', 'ýer tudana', 'клубника', 'small soft red fruit', 'strawberries and cream.', 'ýer tudana bilen gaýmak', 'A1'),
    ('cake', '/keɪk/', 'N', 'tort, köke', 'торт, пирожное', 'a sweet food made with flour and sugar', 'a birthday cake.', 'doglan gün torty', 'A1'),
    ('ice cream', '/ˌaɪs ˈkriːm/', 'N', 'dondurma', 'мороженое', 'a soft frozen sweet food', 'chocolate ice cream.', 'şokoladly dondurma', 'A1'),
    ('biscuits', '/ˈbɪskɪts/', 'N', 'peşenýe', 'печенье', 'small flat sweet cakes', 'tea and biscuits.', 'çaý bilen peşenýe', 'A1'),
    ('chocolate', '/ˈtʃɒklət/', 'N', 'şokolad', 'шоколад', 'a sweet brown food', 'a bar of chocolate.', 'bir plitka şokolad', 'A1'),
    ('crisps', '/krɪsps/', 'N', 'çips', 'чипсы', 'thin slices of fried potato', 'a packet of crisps.', 'bir bukja çips', 'A1'),
    ('nuts', '/nʌts/', 'N', 'hozy', 'орехи', 'hard-shelled things you eat', 'salted nuts.', 'duzly hoz', 'A1'),
    ('sandwich', '/ˈsænwɪdʒ/', 'N', 'sendwiç', 'сэндвич', 'two slices of bread with food between', 'a cheese sandwich.', 'peýnirli sendwiç', 'A1'),
    ('sweets', '/swiːts/', 'N', 'konfet', 'конфеты', 'small soft sweet foods', 'a bag of sweets.', 'bir bukja konfet', 'A1'),
    ('breakfast', '/ˈbrekfəst/', 'N', 'ertirlik', 'завтрак', 'the first meal of the day', 'Breakfast is at seven.', 'Ertirlik sagat ýedide.', 'A1', 'have breakfast'),
    ('lunch', '/lʌntʃ/', 'N', 'günortanlyk', 'обед', 'the meal in the middle of the day', 'a quick lunch.', 'çalt günortanlyk', 'A1', 'have lunch'),
    ('dinner', '/ˈdɪnə/', 'N', 'agşamlyk', 'ужин', 'the main meal in the evening', 'Dinner is ready.', 'Agşamlyk taýýar.', 'A1', 'have dinner'),
]

T['places'] = [
    ("chemist's", '/ˈkemɪsts/', 'N', 'dermanhana', 'аптека', 'a shop that sells medicine', "I bought it at the chemist's.", 'Dermanhanadan aldym.', 'A2'),
    ('pharmacy', '/ˈfɑːməsi/', 'N', 'dermanhana', 'аптека', 'a shop that sells medicine', 'The pharmacy is closed.', 'Dermanhana ýapyk.', 'A1'),
    ('church', '/tʃɜːtʃ/', 'N', 'buthana', 'церковь', 'a building where Christians pray', 'an old church.', 'köne buthana', 'A1'),
    ('department store', '/dɪˈpɑːtmənt stɔː/', 'N', 'uly dükan', 'универмаг', 'a large shop with many departments', 'We met at the department store.', 'Uly dükanada duşuşdyk.', 'A1'),
    ('hospital', '/ˈhɒspɪtl/', 'N', 'hassahana', 'больница', 'a place where sick people are treated', 'She is in hospital.', 'Hassahanada.', 'A1', 'in hospital'),
    ('market', '/ˈmɑːkɪt/', 'N', 'bazar', 'рынок', 'a place where food is sold outside', 'I buy fruit at the market.', 'Bazardan miwe alýaryn.', 'A1', 'at the market'),
    ('park', '/pɑːk/', 'N', 'seýilgäh', 'парк', 'a public area with grass and trees', 'We walk in the park.', 'Seýilgähde ýöreýäris.', 'A1', 'in the park'),
    ('police station', '/pəˈliːs ˌsteɪʃn/', 'N', 'polisiýa bölümi', 'полицейский участок', 'a building where police work', 'Go to the police station.', 'Polisiýa bölümine baryň.', 'A1'),
    ('post office', '/pəʊst ˈɒfɪs/', 'N', 'poçta', 'почта', 'a place where you send letters', 'I sent it from the post office.', 'Poçtadan ugratdym.', 'A1'),
    ('shopping centre', '/ˈʃɒpɪŋ ˌsentə/', 'N', 'söwda merkezi', 'торговый центр', 'a large building with many shops', 'The shopping centre opens at ten.', 'Söwda merkezi sagat onda açylýar.', 'A1'),
    ('supermarket', '/ˈsuːpəmɑːkɪt/', 'N', 'supermarket', 'супермаркет', 'a large shop selling food', 'I shop at the supermarket.', 'Supermarketden satyn alýaryn.', 'A1'),
    ('town hall', '/taʊn hɔːl/', 'N', 'şäher häkimligi', 'ратуша', 'the main public building of a town', 'The town hall is in the square.', 'Şäher häkimligi meýdançada.', 'A1'),
    ('art gallery', '/ɑːt ˈɡæləri/', 'N', 'sungat galereýasy', 'художественная галерея', 'a place where paintings are shown', 'We visited the art gallery.', 'Sungat galereýasyna bardyk.', 'A1'),
    ('castle', '/ˈkɑːsl/', 'N', 'gala', 'замок', 'a large strong old building', 'an old castle.', 'köne gala', 'A1'),
    ('museum', '/mjuˈziːəm/', 'N', 'muzeý', 'музей', 'a building with important old objects', 'The museum is free.', 'Muzeý mugt.', 'A1'),
    ('theatre', '/ˈθɪətə/', 'N', 'teatr', 'театр', 'a building where plays are performed', 'We went to the theatre.', 'Teatra gitdik.', 'A1'),
    ('zoo', '/zuː/', 'N', 'haýwanat bagy', 'зоопарк', 'a place where animals are kept', 'The children love the zoo.', 'Çagalar haýwanat bagyny gowy görýär.', 'A1'),
    ('bridge', '/brɪdʒ/', 'N', 'köpri', 'мост', 'a structure that carries a road over water', 'a bridge over the river.', 'derýanyň üstünden köpri', 'A1'),
    ('river', '/ˈrɪvə/', 'N', 'derýa', 'река', 'a large natural flow of water', 'The river is long.', 'Derýa uzyn.', 'A1'),
    ('road', '/rəʊd/', 'N', 'ýol', 'дорога', 'a wide way for vehicles', 'a busy road.', 'işlek ýol', 'A1'),
    ('square', '/skweə/', 'N', 'meýdança', 'площадь', 'an open area in a town', 'the main square.', 'baş meýdança', 'A1'),
    ('street', '/striːt/', 'N', 'köçe', 'улица', 'a road in a town with buildings beside it', 'a narrow street.', 'dar köçe', 'A1'),
    ('bus station', '/bʌs ˌsteɪʃn/', 'N', 'awtobus duralgasy', 'автовокзал', 'a place where buses start and end', 'The bus station is near the park.', 'Awtobus duralgasy seýilgähiň ýanynda.', 'A1'),
    ('car park', '/kɑː pɑːk/', 'N', 'awtoduralga', 'автостоянка', 'a place where you leave cars', 'The car park is full.', 'Awtoduralga doly.', 'A1'),
    ('railway station', '/ˈreɪlweɪ ˌsteɪʃn/', 'N', 'demir ýol menzili', 'железнодорожный вокзал', 'a place where trains stop', 'We met at the railway station.', 'Demir ýol menzilinde duşuşdyk.', 'A1'),
    ('cathedral', '/kəˈθiːdrəl/', 'N', 'uly buthana', 'собор', 'a very large important church', 'a famous cathedral.', 'meşhur uly buthana', 'A1'),
    ('mosque', '/mɒsk/', 'N', 'metjit', 'мечеть', 'a building where Muslims pray', 'The mosque is beautiful.', 'Metjit owadan.', 'A1'),
    ('temple', '/ˈtempl/', 'N', 'ybadathana', 'храм', 'a building used for prayer', 'an old temple.', 'köne ybadathana', 'A1'),
    ('tower', '/ˈtaʊə/', 'N', 'diň', 'башня', 'a tall narrow structure', 'a tall stone tower.', 'beýik daş diň', 'A1'),
    ('station', '/ˈsteɪʃn/', 'N', 'menzil, stansiýa', 'вокзал', 'a place where trains or buses stop', 'the central station.', 'merkezi menzil', 'A1'),
]

T['comparatives'] = [
    ('bigger', '/ˈbɪɡə/', 'ADJ', 'has uly', 'больше', 'more big', 'Moscow is bigger than Rome.', 'Moskwa Rimden uly.', 'A2', 'bigger than'),
    ('smaller', '/ˈsmɔːlə/', 'ADJ', 'has kiçi', 'меньше', 'more small', 'My flat is smaller.', 'Kwartiram has kiçi.', 'A2', 'smaller than'),
    ('older', '/ˈəʊldə/', 'ADJ', 'has garry', 'старше', 'more old', 'She is older than me.', 'Ol menden uly.', 'A2', 'older than'),
    ('younger', '/ˈjʌŋɡə/', 'ADJ', 'has ýaş', 'моложе', 'more young', 'My brother is younger.', 'Doganym has ýaş.', 'A2', 'younger than'),
    ('better', '/ˈbetə/', 'ADJ', 'has gowy', 'лучше', 'more good', 'This is better.', 'Bu has gowy.', 'A1', 'better than'),
    ('worse', '/wɜːs/', 'ADJ', 'has erbet', 'хуже', 'more bad', 'The weather is worse today.', 'Howa bu gün has erbet.', 'A2', 'worse than'),
    ('more expensive', '/mɔːr ɪkˈspensɪv/', 'ADJ', 'has gymmat', 'дороже', 'costing more', 'It is more expensive than the other.', 'Beýlekiden has gymmat.', 'A2'),
    ('cheaper', '/ˈtʃiːpə/', 'ADJ', 'has arzan', 'дешевле', 'costing less', 'This one is cheaper.', 'Bu has arzan.', 'A2', 'cheaper than'),
    ('as big as', '/æz bɪɡ æz/', 'PHR', '... ýaly uly', 'такой же большой, как', 'the same size as', 'It is as big as a bus.', 'Awtobus ýaly uly.', 'A1'),
    ('not as good as', '/nɒt æz ɡʊd æz/', 'PHR', '... ýaly gowy däl', 'не такой хороший, как', 'less good than', 'It is not as good as the first one.', 'Birinjisinden gowy däl.', 'A1'),
]

T['superlatives'] = [
    ('the biggest', '/ðə ˈbɪɡɪst/', 'ADJ', 'iň uly', 'самый большой', 'bigger than all others', 'the biggest city in Europe.', 'Ýewropanyň iň uly şäheri', 'A2'),
    ('the smallest', '/ðə ˈsmɔːlɪst/', 'ADJ', 'iň kiçi', 'самый маленький', 'smaller than all others', 'the smallest country.', 'iň kiçi ýurt', 'A2'),
    ('the oldest', '/ðə ˈəʊldɪst/', 'ADJ', 'iň köne', 'самый старый', 'older than all others', 'the oldest building in town.', 'şäherdäki iň köne bina', 'A2'),
    ('the best', '/ðə best/', 'ADJ', 'iň gowy', 'лучший', 'better than all others', 'the best restaurant.', 'iň gowy restoran', 'A1', 'the best'),
    ('the worst', '/ðə wɜːst/', 'ADJ', 'iň erbet', 'худший', 'worse than all others', 'the worst film ever.', 'taryhdaky iň erbet film', 'A2'),
    ('the most beautiful', '/ðə məʊst ˈbjuːtɪfl/', 'ADJ', 'iň owadan', 'самый красивый', 'more beautiful than all others', 'the most beautiful place.', 'iň owadan ýer', 'A2'),
    ('the most dangerous', '/ðə məʊst ˈdeɪndʒərəs/', 'ADJ', 'iň howply', 'самый опасный', 'more dangerous than all others', 'the most dangerous road.', 'iň howply ýol', 'A2'),
]

T['transport'] = [
    ('bus', '/bʌs/', 'N', 'awtobus', 'автобус', 'a large vehicle that carries passengers', 'I go by bus.', 'Awtobusda gidýärin.', 'A1', 'by bus'),
    ('train', '/treɪn/', 'N', 'otly', 'поезд', 'a vehicle that runs on rails', 'The train is late.', 'Otly giç.', 'A1', 'by train'),
    ('plane', '/pleɪn/', 'N', 'uçar', 'самолёт', 'a vehicle that flies', 'We went by plane.', 'Uçarda gitdik.', 'A1', 'by plane'),
    ('taxi', '/ˈtæksi/', 'N', 'taksi', 'такси', 'a car with a driver you pay', 'Take a taxi.', 'Taksi tutuň.', 'A1', 'take a taxi'),
    ('underground', '/ˈʌndəɡraʊnd/', 'N', 'metro', 'метро', 'a railway under a city', 'Go by underground.', 'Metroda gidiň.', 'A1', 'by underground'),
    ('bike', '/baɪk/', 'N', 'welosiped', 'велосипед', 'a vehicle with two wheels you pedal', 'I go to work by bike.', 'Işe welosipedde gidýärin.', 'A1', 'by bike'),
    ('tram', '/træm/', 'N', 'tramwaý', 'трамвай', 'a vehicle that runs on rails in a city', 'Take tram number five.', 'Bäşinji tramwaýa münüň.', 'A1'),
    ('ferry', '/ˈferi/', 'N', 'parom', 'паром', 'a boat that carries people across water', 'We took the ferry.', 'Paroma müňdük.', 'A1'),
    ('ticket', '/ˈtɪkɪt/', 'N', 'bilet', 'билет', 'a paper that allows you to travel', 'I bought two tickets.', 'Iki bilet aldym.', 'A1', 'buy a ticket'),
    ('passenger', '/ˈpæsɪndʒə/', 'N', 'ýolagçy', 'пассажир', 'a person travelling in a vehicle', 'The passengers got off.', 'Ýolagçy düşdi.', 'A1'),
    ('platform', '/ˈplætfɔːm/', 'N', 'platforma', 'платформа', 'the area beside a railway track', 'The train leaves from platform three.', 'Otly üçünji platformadan gidýär.', 'A1'),
    ('get on', '/ɡet ɒn/', 'PHR', 'münmek', 'сесть (в транспорт)', 'to enter a bus, train or plane', 'We got on the bus.', 'Awtobusa müňdük.', 'A1', 'get on the bus'),
    ('get off', '/ɡet ɒf/', 'PHR', 'düşmek', 'сойти (с транспорта)', 'to leave a bus, train or plane', 'Get off at the next stop.', 'Indeki duralgada düşüň.', 'A1', 'get off the bus'),
    ('get in', '/ɡet ɪn/', 'PHR', 'münmek (maşyna)', 'сесть (в машину)', 'to enter a car or taxi', 'Get in, I will take you.', 'Mün, alyp bararyn.', 'A1', 'get in the car'),
    ('arrive', '/əˈraɪv/', 'V', 'baryp ýetmek', 'прибывать', 'to reach a place', 'We arrived late.', 'Giç baryp ýetdik.', 'A1', 'arrive at'),
    ('leave', '/liːv/', 'V', 'gitmek, terk etmek', 'уезжать', 'to go away from a place', 'The train leaves at six.', 'Otly altyda gidýär.', 'A1', 'leave for'),
]

T['past_verbs'] = [
    ('was', '/wɒz/', 'V', 'boldy (bir)', 'был, была', 'the past form of "be" for I, he, she, it', 'I was at home.', 'Öýde boldum.', 'A1'),
    ('were', '/wɜː/', 'V', 'boldy (köp)', 'были', 'the past form of "be" for you, we, they', 'They were late.', 'Giç galdylar.', 'A1'),
    ('went', '/went/', 'V', 'gitdi', 'пошёл, поехал', 'the past form of "go"', 'We went to the sea.', 'Deňze gitdik.', 'A1'),
    ('had', '/hæd/', 'V', 'bardy', 'было, имел', 'the past form of "have"', 'I had a great day.', 'Ajaýyp gün geçirdim.', 'A1'),
    ('got', '/ɡɒt/', 'V', 'aldy', 'получил', 'the past form of "get"', 'She got a new job.', 'Täze iş tapdy.', 'A1'),
    ('did', '/dɪd/', 'V', 'etdi', 'сделал', 'the past form of "do"', 'He did his homework.', 'Öý işini etdi.', 'A1'),
    ('saw', '/sɔː/', 'V', 'gördi', 'видел', 'the past form of "see"', 'We saw a good film.', 'Gowy film gördük.', 'A1'),
    ('ate', '/eɪt/', 'V', 'iýdi', 'ел', 'the past form of "eat"', 'I ate too much.', 'Köp iýdim.', 'A1'),
    ('drank', '/dræŋk/', 'V', 'içdi', 'пил', 'the past form of "drink"', 'She drank two coffees.', 'Iki kofe içdi.', 'A1'),
    ('came', '/keɪm/', 'V', 'geldi', 'пришёл', 'the past form of "come"', 'He came home late.', 'Öýe giç geldi.', 'A1'),
    ('took', '/tʊk/', 'V', 'aldy, müňdi', 'взял', 'the past form of "take"', 'We took a taxi.', 'Taksi tutduk.', 'A1'),
    ('made', '/meɪd/', 'V', 'taýýarlady', 'сделал', 'the past form of "make"', 'She made dinner.', 'Agşamlyk taýýarlady.', 'A1'),
    ('bought', '/bɔːt/', 'V', 'satyn aldy', 'купил', 'the past form of "buy"', 'I bought a present.', 'Sowgat satyn aldym.', 'A1'),
    ('brought', '/brɔːt/', 'V', 'getirdi', 'принёс', 'the past form of "bring"', 'He brought flowers.', 'Gül getirdi.', 'A1'),
    ('said', '/sed/', 'V', 'aýtdy', 'сказал', 'the past form of "say"', 'She said goodbye.', 'Hoşlaşdy.', 'A1'),
    ('told', '/təʊld/', 'V', 'gürrüň berdi', 'рассказал', 'the past form of "tell"', 'He told me a story.', 'Bir hekaýa gürrüň berdi.', 'A1'),
    ('found', '/faʊnd/', 'V', 'tapdy', 'нашёл', 'the past form of "find"', 'I found my keys.', 'Açarlarymy tapdym.', 'A1'),
    ('wrote', '/rəʊt/', 'V', 'ýazdy', 'написал', 'the past form of "write"', 'She wrote an email.', 'E-poçta ýazdy.', 'A1'),
    ('yesterday', '/ˈjestədeɪ/', 'ADV', 'düýn', 'вчера', 'on the day before today', 'I was tired yesterday.', 'Düýn ýadawdym.', 'A1'),
    ('last night', '/lɑːst naɪt/', 'PHR', 'düýn agşam', 'вчера вечером', 'during the night before today', 'We stayed in last night.', 'Düýn agşam öýde galdyk.', 'A1'),
    ('last week', '/lɑːst wiːk/', 'PHR', 'geçen hepde', 'на прошлой неделе', 'during the week before this one', 'She called last week.', 'Geçen hepde jaň etdi.', 'A1'),
    ('ago', '/əˈɡəʊ/', 'ADV', 'öň', 'назад', 'how far back in the past', 'two days ago.', 'iki gün öň', 'A1', 'two days ago'),
    ('born', '/bɔːn/', 'ADJ', 'doglan', 'родившийся', 'used to say when someone started life', 'I was born in 1998.', '1998-nji ýylda doguldym.', 'A1', 'was born'),
]

T['phones'] = [
    ('phone', '/fəʊn/', 'N', 'telefon', 'телефон', 'a machine you use to talk to someone far away', 'Answer the phone.', 'Telefona jogap ber.', 'A1', 'answer the phone'),
    ('mobile phone', '/ˈməʊbaɪl fəʊn/', 'N', 'ykjam telefon', 'мобильный телефон', 'a phone you carry with you', 'My mobile phone is new.', 'Ykjam telefonum täze.', 'A1'),
    ('screen', '/skriːn/', 'N', 'ekran', 'экран', 'the flat part of a phone or computer you look at', 'The screen is broken.', 'Ekran döwük.', 'A1'),
    ('battery', '/ˈbætri/', 'N', 'batareý', 'батарея', 'the part that gives a device power', 'The battery is flat.', 'Batareý gutardy.', 'A1'),
    ('charger', '/ˈtʃɑːdʒə/', 'N', 'zarýadnik', 'зарядное устройство', 'a device that puts power into a battery', 'Where is my charger?', 'Zarýadnikim nirede?', 'A1'),
    ('message', '/ˈmesɪdʒ/', 'N', 'hat, habar', 'сообщение', 'a short piece of information you send', 'Send me a message.', 'Habar ugrat.', 'A1', 'send a message'),
    ('email', '/ˈiːmeɪl/', 'N', 'e-poçta', 'электронная почта', 'a message sent by computer', 'I sent an email.', 'E-poçta ugratdym.', 'A1', 'send an email'),
    ('internet', '/ˈɪntənet/', 'N', 'internet', 'интернет', 'the network that connects computers worldwide', 'I found it on the internet.', 'Internetden tapdym.', 'A1', 'on the internet'),
    ('website', '/ˈwebsaɪt/', 'N', 'web sahypa', 'веб-сайт', 'a set of pages on the internet', 'The website is useful.', 'Web sahypa peýdaly.', 'A1'),
    ('app', '/æp/', 'N', 'ylym programmas', 'приложение', 'a program on a phone or computer', 'Download the app.', 'Programmany ýükläň.', 'A1'),
    ('send', '/send/', 'V', 'ugratmak', 'отправлять', 'to make something go to someone', 'Send me the photo.', 'Suraty ugrat.', 'A1', 'send a message'),
    ('download', '/ˌdaʊnˈləʊd/', 'V', 'ýüklemek', 'скачивать', 'to copy data onto your device', 'I downloaded the app.', 'Programmany ýükledim.', 'A1'),
    ('share', '/ʃeə/', 'V', 'paýlaşmak', 'делиться', 'to let others see something', 'Share the photo with me.', 'Suraty meniň bilen paýlaş.', 'A1', 'share a photo'),
    ('post', '/pəʊst/', 'V', 'ýerleşdirmek', 'публиковать', 'to put something online for others to see', 'She posted a photo.', 'Surat ýerleşdirdi.', 'A1', 'post a photo'),
    ('online', '/ˌɒnˈlaɪn/', 'ADV', 'onlaýn', 'в сети', 'connected to the internet', 'I bought it online.', 'Onlaýn satyn aldym.', 'A1'),
    # ---- phones key e 11.10, TG p.149 ----
    ('wi-fi', '/ˈwaɪ faɪ/', 'N', 'waý-faý', 'вай-фай', 'a wireless way to connect to the internet', "The hotel's wi-fi is free.", 'Myhmanhananyň waý-faýy mugt.', 'A2'),
    ('attachment', '/əˈtætʃmənt/', 'N', 'goşundy faýl', 'вложение', 'a file sent with an email', 'I sent the photos as an attachment.', 'Suratlary goşundy faýl edip iberdim.', 'A2'),
    ('log in', '/ˌlɒɡ ˈɪn/', 'PHR', 'ulgama girmek', 'входить в систему', 'to enter your name and password to use a system', 'Log in with your email.', 'Emailiňiz bilen ulgama giriň.', 'A2'),
    ('search', '/sɜːtʃ/', 'V', 'gözlemek', 'искать (в интернете)', 'to look for information on the internet', 'Search for the answer online.', 'Jogaby onlaýn gözläň.', 'A2'),
    ('broadband', '/ˈbrɔːdbænd/', 'N', 'giň zolakly internet', 'широкополосный интернет', 'a fast internet connection', 'Broadband is fast but expensive.', 'Giň zolakly internet çalt, ýöne gymmat.', 'A2'),
]

T['adverbs'] = [
    ('quickly', '/ˈkwɪkli/', 'ADV', 'çalt', 'быстро', 'at a fast speed', 'She walked quickly.', 'Çalt ýöreýärdi.', 'A1'),
    ('slowly', '/ˈsləʊli/', 'ADV', 'haýal', 'медленно', 'not quickly', 'He spoke slowly.', 'Haýal gürledi.', 'A1'),
    ('well', '/wel/', 'ADV', 'gowy', 'хорошо', 'in a good way', 'She sings well.', 'Gowy aýdym aýdýar.', 'A1'),
    ('badly', '/ˈbædli/', 'ADV', 'erbet', 'плохо', 'not well', 'He played badly.', 'Erbet oýnady.', 'A1'),
    ('carefully', '/ˈkeəfəli/', 'ADV', 'üns bilen', 'осторожно', 'with a lot of attention', 'Drive carefully.', 'Üns bilen sür.', 'A1'),
    ('easily', '/ˈiːzɪli/', 'ADV', 'aňsatlyk bilen', 'легко', 'without difficulty', 'She won easily.', 'Aňsatlyk bilen utdy.', 'A1'),
    ('early', '/ˈɜːli/', 'ADV', 'irden', 'рано', 'before the expected time', 'We arrived early.', 'Ir baryp ýetdik.', 'A1'),
    ('late', '/leɪt/', 'ADV', 'giç', 'поздно', 'after the expected time', 'He came late.', 'Giç geldi.', 'A1'),
    ('hard', '/hɑːd/', 'ADV', 'gaty, yhlasly', 'усердно', 'with a lot of effort', 'She works hard.', 'Yhlasly işleýär.', 'A1', 'work hard'),
    ('too', '/tuː/', 'ADV', 'hem, aşa', 'тоже, слишком', 'also, or more than is good', 'It is too expensive.', 'Örän gymmat.', 'A1'),
    ('enough', '/ɪˈnʌf/', 'ADV', 'ýeterlik', 'достаточно', 'as much as is needed', 'It is warm enough.', 'Ýeterlik yssy.', 'A1'),
    ('together', '/təˈɡeðə/', 'ADV', 'bile', 'вместе', 'with each other', 'We went together.', 'Bile gitdik.', 'A1'),
    ('alone', '/əˈləʊn/', 'ADV', 'ýeke', 'один, в одиночестве', 'without other people', 'She lives alone.', 'Ýeke ýaşaýar.', 'A1'),
    ('suddenly', '/ˈsʌdənli/', 'ADV', 'birden', 'вдруг', 'quickly and unexpectedly', 'Suddenly it started to rain.', 'Birden ýagyş ýagdy.', 'A1'),
    ('finally', '/ˈfaɪnəli/', 'ADV', 'iň soňunda', 'наконец', 'after a long time', 'We finally arrived.', 'Iň soňunda bardyk.', 'A1'),
]

# ---- lessons whose words are in the lesson's own VOCABULARY box, not the Bank
T['feelings'] = [
    ('angry', '/ˈæŋɡri/', 'ADJ', 'gaharly', 'злой', 'feeling that you want to shout at someone', 'She was angry with me.', 'Maňa gaharlydy.', 'A2'),
    ('bored', '/bɔːd/', 'ADJ', 'gaharyňy basmak, bezgin', 'скучающий', 'unhappy because nothing interesting is happening', 'The children were bored.', 'Çagalar bezgindi.', 'A2'),
    ('frightened', '/ˈfraɪtnd/', 'ADJ', 'goran, gorkan', 'испуганный', 'afraid of something', 'He was frightened of the dark.', 'Garanlykdan gorkýardy.', 'A2', 'frightened of'),
    ('happy', '/ˈhæpi/', 'ADJ', 'şat, bagtly', 'счастливый', 'pleased and enjoying yourself', 'She looks happy today.', 'Bu gün şat görünýär.', 'A1'),
    ('sad', '/sæd/', 'ADJ', 'gamgyn', 'грустный', 'unhappy', 'He was sad to leave.', 'Gitmäge gamgyndy.', 'A1'),
    ('stressed', '/strest/', 'ADJ', 'dartgynly', 'в стрессе', 'worried and unable to relax', 'I feel stressed before exams.', 'Synaglardan öň dartgynly duýýaryn.', 'B1'),
    ('thirsty', '/ˈθɜːsti/', 'ADJ', 'susuz', 'испытывающий жажду', 'needing to drink', 'I am thirsty.', 'Susadym.', 'A2'),
    ('worried', '/ˈwʌrid/', 'ADJ', 'aladaly', 'обеспокоенный', 'unhappy because you think about problems', 'She is worried about the test.', 'Synag barada aladaly.', 'A2', 'worried about'),
]

T['noise'] = [
    ('noise', '/nɔɪz/', 'N', 'galmagal', 'шум', 'a loud unpleasant sound', 'What is that noise?', 'Ol näme galmagal?', 'A2', 'make a noise'),
    ('noisy', '/ˈnɔɪzi/', 'ADJ', 'galmagally', 'шумный', 'making a lot of noise', 'a noisy street.', 'galmagally köçe', 'A2'),
    ('quiet', '/ˈkwaɪət/', 'ADJ', 'asuda, sessiz', 'тихий', 'making little or no noise', 'a quiet village.', 'asuda oba', 'A2'),
    ('upstairs', '/ˌʌpˈsteəz/', 'ADV', 'ýokarky gatda', 'наверху', 'on a higher floor', 'The neighbours upstairs are noisy.', 'Ýokarky goňşular galmagally.', 'A2'),
    ('downstairs', '/ˌdaʊnˈsteəz/', 'ADV', 'aşaky gatda', 'внизу', 'on a lower floor', 'She went downstairs.', 'Aşaky gata düşdi.', 'A2'),
    ('next door', '/ˌnekst ˈdɔː/', 'ADV', 'gapdaldaky öýde', 'по соседству', 'in the building beside yours', 'The people next door have a dog.', 'Gapdaldaky goňşynyň iti bar.', 'A2'),
    ('neighbour', '/ˈneɪbə/', 'N', 'goňşy', 'сосед', 'a person who lives near you', 'Our neighbour is friendly.', 'Goňşumyz mähirli.', 'A2'),
    ('shout', '/ʃaʊt/', 'V', 'gygyrmak', 'кричать', 'to speak very loudly', "Don't shout at me.", 'Maňa gygyrma.', 'A2', 'shout at'),
    ('fight', '/faɪt/', 'V', 'dawa etmek', 'ссориться', 'to argue angrily', 'They fight every day.', 'Her gün dawa edýärler.', 'A2'),
    ('play music', '/pleɪ ˈmjuːzɪk/', 'PHR', 'saz çalmak', 'играть музыку', 'to make music', 'They play music late at night.', 'Gije saz çalýarlar.', 'A1'),
]

T['clothes'] = [
    ('jacket', '/ˈdʒækɪt/', 'N', 'kurtka', 'куртка', 'a short coat', 'a leather jacket.', 'deri kurtka', 'A1', 'wear a jacket'),
    ('jeans', '/dʒiːnz/', 'N', 'jinsi', 'джинсы', 'trousers made of denim', 'blue jeans.', 'gök jinsi', 'A1', 'wear jeans'),
    ('shirt', '/ʃɜːt/', 'N', 'köýnek', 'рубашка', 'a piece of clothing for the top of the body', 'a white shirt.', 'ak köýnek', 'A1'),
    ('skirt', '/skɜːt/', 'N', 'ýubka', 'юбка', 'a piece of clothing worn by women from the waist down', 'a long skirt.', 'uzyn ýubka', 'A1'),
    ('sweater', '/ˈswetə/', 'N', 'switer', 'свитер', 'a warm piece of clothing for the top of the body', 'a wool sweater.', 'ýüň switer', 'A1'),
    ('T-shirt', '/ˈtiːʃɜːt/', 'N', 'futbolka', 'футболка', 'a light shirt with short sleeves', 'a plain T-shirt.', 'ýönekeý futbolka', 'A1'),
    ('trousers', '/ˈtraʊzəz/', 'N', 'balak', 'брюки', 'a piece of clothing covering the legs', 'black trousers.', 'gara balak', 'A1'),
    ('shoes', '/ʃuːz/', 'N', 'aýakgap', 'туфли', 'things you wear on your feet', 'new shoes.', 'täze aýakgap', 'A1', 'wear shoes'),
    ('coat', '/kəʊt/', 'N', 'palto', 'пальто', 'a long outer piece of clothing', 'a warm coat.', 'yssy palto', 'A1'),
    ('dress', '/dres/', 'N', 'köýnek (aýal)', 'платье', 'a piece of clothing for women that covers the body and legs', 'a summer dress.', 'tomus köýnegi', 'A1'),
    ('size', '/saɪz/', 'N', 'ölçeg', 'размер', 'how big or small something is', 'What size are you?', 'Ölçegiňiz näçe?', 'A2', 'in size'),
    ('try on', '/traɪ ɒn/', 'PHR', 'synap görmek', 'примерить', 'to put on clothes to see if they fit', 'Can I try it on?', 'Synap görüp bilerinmi?', 'A2'),
]

T['story'] = [
    ('decide', '/dɪˈsaɪd/', 'V', 'karar bermek', 'решать', 'to choose after thinking', 'She decided to leave.', 'Gitmäge karar berdi.', 'A2', 'decide to'),
    ('strange', '/streɪndʒ/', 'ADJ', 'geň', 'странный', 'unusual and surprising', 'a strange noise.', 'geň bir ses eşitdim', 'A2'),
    ('surprised', '/səˈpraɪzd/', 'ADJ', 'geň galan', 'удивлённый', 'feeling that something is unexpected', 'He was surprised to see her.', 'Ony görüp geň galdy.', 'A2', 'surprised to'),
    ('valuable', '/ˈvæljuəbl/', 'ADJ', 'gymmat bahaly', 'ценный', 'worth a lot of money', 'a valuable ring.', 'gymmat bahaly ýüzük', 'B1'),
    ('desert', '/ˈdezət/', 'N', 'çöl', 'пустыня', 'a dry area of land with little water', 'They crossed the desert.', 'Çölden geçdiler.', 'A2'),
    ('mountain', '/ˈmaʊntən/', 'N', 'dag', 'гора', 'a very high hill', 'a high mountain.', 'beýik dag', 'A2'),
    ('palace', '/ˈpæləs/', 'N', 'köşk', 'дворец', 'the home of a king or queen', 'a royal palace.', 'şalyk köşgi', 'B1'),
    ('village', '/ˈvɪlɪdʒ/', 'N', 'oba', 'деревня', 'a very small town in the countryside', 'a quiet village.', 'asuda oba', 'A2'),
    ('inside', '/ˌɪnˈsaɪd/', 'PREP', 'içinde', 'внутри', 'within something', 'inside the house.', 'öýüň içinde', 'A2'),
    ('towards', '/təˈwɔːdz/', 'PREP', 'tarap', 'к, в направлении', 'in the direction of', 'She walked towards the door.', 'Gapa tarap ýöredi.', 'B1'),
    ('sell', '/sel/', 'V', 'satmak', 'продавать', 'to give something for money', 'They sell fruit here.', 'Bu ýerde miwe satýarlar.', 'A2'),
    ('comfortable', '/ˈkʌmftəbl/', 'ADJ', 'amatly', 'удобный', 'pleasant to use or wear', 'a comfortable bed.', 'amatly düşek', 'A2'),
]

T['crime'] = [
    ('inspector', '/ɪnˈspektə/', 'N', 'inspektor', 'инспектор', 'a police officer of high rank', 'Inspector Granger arrived.', 'Inspektor Greýnjer geldi.', 'B1'),
    ('murder', '/ˈmɜːdə/', 'N', 'adam öldürmek', 'убийство', 'the crime of killing someone', 'a murder mystery.', 'adam öldürme syry', 'B1'),
    ('kill', '/kɪl/', 'V', 'öldürmek', 'убивать', 'to make someone die', 'Somebody killed him.', 'Ony birisi öldürdi.', 'A2'),
    ('dead', '/ded/', 'ADJ', 'öli', 'мёртвый', 'no longer alive', 'He was dead.', 'Ol ölüdi.', 'A2'),
    ('die', '/daɪ/', 'V', 'ölmek', 'умирать', 'to stop living', 'He died in 1965.', '1965-nji ýylda aradan çykdy.', 'A2'),
    ('asleep', '/əˈsliːp/', 'ADJ', 'ukuda', 'спящий', 'sleeping', 'Was he asleep?', 'Ukudymy?', 'A2', 'fall asleep'),
    ('midnight', '/ˈmɪdnaɪt/', 'N', 'gije ýary', 'полночь', 'twelve o\'clock at night', 'He died at midnight.', 'Gije ýary aradan çykdy.', 'A2', 'at midnight'),
    ('moustache', '/məˈstɑːʃ/', 'N', 'murt', 'усы', 'hair above a man\'s mouth', 'a big moustache.', 'uly murt', 'B1'),
    ('library', '/ˈlaɪbrəri/', 'N', 'kitaphana', 'библиотека', 'a room or building with books', 'They talked in the library.', 'Kitaphanada gürleşdiler.', 'A2', 'in the library'),
    ('hear', '/hɪə/', 'V', 'eşitmek', 'слышать', 'to know a sound with your ears', 'Did you hear anything?', 'Bir zat eşitdiňmi?', 'A1'),
    ('secret', '/ˈsiːkrət/', 'N', 'sir', 'секрет', 'something you do not tell people', 'Tell me a secret.', 'Maňa bir sir aýt.', 'A2', 'tell a secret'),
]

T['containers'] = [
    ('bottle', '/ˈbɒtl/', 'N', 'çüýşe', 'бутылка', 'a container with a narrow neck for liquids', 'a bottle of water.', 'bir çüýşe suw', 'A1', 'a bottle of'),
    ('box', '/bɒks/', 'N', 'guty', 'коробка', 'a container with flat sides', 'a box of chocolates.', 'bir guty şokolad', 'A1', 'a box of'),
    ('can', '/kæn/', 'N', 'banka', 'банка', 'a metal container for food or drink', 'a can of Coke.', 'bir banka koka-kola', 'A2', 'a can of'),
    ('carton', '/ˈkɑːtn/', 'N', 'kagyz gap', 'пакет, картонная упаковка', 'a light container for drinks', 'a carton of juice.', 'bir gap şire', 'B1', 'a carton of'),
    ('jar', '/dʒɑː/', 'N', 'banka (aýna)', 'банка (стеклянная)', 'a glass container with a lid', 'a jar of jam.', 'bir banka mürebbä', 'A2', 'a jar of'),
    ('packet', '/ˈpækɪt/', 'N', 'bukja', 'пачка', 'a small paper or plastic container', 'a packet of crisps.', 'bir bukja çips', 'A2', 'a packet of'),
    ('tin', '/tɪn/', 'N', 'konserw bankasy', 'жестяная банка', 'a metal container for food', 'a tin of tomatoes.', 'bir banka pomidor', 'B1', 'a tin of'),
    ('some', '/sʌm/', 'DET', 'biraz', 'немного', 'an amount of something', 'I need some milk.', 'Biraz süýt gerek.', 'A1', 'some milk'),
    ('any', '/ˈeni/', 'DET', 'hiç, islendik', 'какой-нибудь', 'used in questions and negatives', "We don't have any bread.", 'Çöregimiz ýok.', 'A1', 'any bread'),
    ('much', '/mʌtʃ/', 'DET', 'köp', 'много', 'a large amount', 'How much sugar do you want?', 'Näçe şeker isleýärsiň?', 'A1', 'how much'),
    ('many', '/ˈmeni/', 'DET', 'köp (sanalýan)', 'много (исчисляемое)', 'a large number', 'How many eggs do we need?', 'Näçe ýumurtga gerek?', 'A1', 'how many'),
    ('a lot of', '/ə lɒt əv/', 'DET', 'köp', 'много', 'a large amount or number', 'a lot of friends.', 'köp dost', 'A1'),
    ('a few', '/ə fjuː/', 'DET', 'birnäçe', 'несколько', 'a small number', 'a few minutes.', 'birnäçe minut', 'A1'),
    ('a little', '/ə ˈlɪtl/', 'DET', 'biraz', 'немного', 'a small amount', 'a little sugar.', 'biraz şeker', 'A1'),
]

T['high_numbers'] = [
    ('population', '/ˌpɒpjuˈleɪʃn/', 'N', 'ilaty', 'население', 'all the people living in a place', 'The population is 67 million.', 'Ilaty 67 million.', 'A2'),
    ('kilometre', '/ˈkɪləmiːtə/', 'N', 'kilometr', 'километр', 'a unit of length equal to 1,000 metres', 'It is 2,500 km away.', '2500 km uzaklykda.', 'A2'),
    ('metre', '/ˈmiːtə/', 'N', 'metr', 'метр', 'a unit of length equal to 100 centimetres', 'The wall is two metres high.', 'Diwar iki metr beýiklikde.', 'A2'),
    ('percent', '/pəˈsent/', 'ADV', 'göterim', 'процент', 'one part in every hundred', 'Fifty percent agreed.', 'Elli göterimi razy boldy.', 'A2'),
    ('number', '/ˈnʌmbə/', 'N', 'san', 'число', 'a word or sign that says how many', 'a phone number.', 'telefon belgisi', 'A1', 'phone number'),
    ('half', '/hɑːf/', 'N', 'ýarym', 'половина', 'one of two equal parts', 'Half of them came.', 'Ýarymy geldi.', 'A2', 'half of'),
    ('double', '/ˈdʌbl/', 'ADJ', 'iki esse', 'двойной', 'twice as much', 'double the price.', 'iki esse baha', 'A2'),
    ('score', '/skɔː/', 'N', 'hasap, bal', 'счёт', 'the number of points in a game', 'The score was two to one.', 'Hasap iki bir boldy.', 'A2'),
    ('average', '/ˈævərɪdʒ/', 'N', 'ortaça', 'среднее', 'the usual amount', 'the average temperature.', 'ortaça temperatura', 'B1', 'on average'),
    ('total', '/ˈtəʊtl/', 'N', 'jemi', 'итого', 'the whole amount', 'The total is forty.', 'Jemi kyrk.', 'A2', 'in total'),
]

T['holidays'] = [
    ('holiday', '/ˈhɒlədeɪ/', 'N', 'dynç alyş', 'отпуск, каникулы', 'a time when you do not work or study', 'We are on holiday.', 'Dynç alyşda.', 'A1', 'on holiday'),
    ('book', '/bʊk/', 'V', 'öňünden almak', 'бронировать', 'to arrange something in advance', 'We booked a hotel.', 'Myhmanhana öňünden aldyk.', 'A2', 'book a hotel'),
    ('rent', '/rent/', 'V', 'kärendesine almak', 'арендовать', 'to pay to use something for a time', 'We rented a bike.', 'Welosiped kärendesine aldyk.', 'A2', 'rent a car'),
    ('visit', '/ˈvɪzɪt/', 'V', 'baryp görmek', 'посещать', 'to go to see a place or person', 'We visited the museum.', 'Muzeýe bardyk.', 'A1', 'visit a museum'),
    ('stay', '/steɪ/', 'V', 'galmak', 'оставаться', 'to live somewhere for a short time', 'We stayed in a small hotel.', 'Kiçi myhmanhanada galdyk.', 'A1', 'stay in a hotel'),
    ('flight', '/flaɪt/', 'N', 'uçar gatnawy', 'рейс', 'a journey by plane', 'Our flight was late.', 'Uçar gatnawymyz giç galdy.', 'A2', 'catch a flight'),
    ('accommodation', '/əˌkɒməˈdeɪʃn/', 'N', 'ýaşaýyş ýeri', 'жильё', 'a place to sleep on a trip', 'We need accommodation for two nights.', 'Iki gije üçin ýer gerek.', 'B1'),
    ('abroad', '/əˈbrɔːd/', 'ADV', 'daşary ýurtda', 'за границу', 'in another country', 'They went abroad last summer.', 'Geçen tomus daşary ýurda gitdiler.', 'A2', 'go abroad'),
    ('guide', '/ɡaɪd/', 'N', 'gid', 'гид', 'a person who shows visitors a place', 'The guide knew the city well.', 'Gid şäheri gowy bilýärdi.', 'A2', 'tour guide'),
    ('trip', '/trɪp/', 'N', 'syýahat', 'поездка', 'a journey to a place and back', 'a short trip.', 'gysga syýahat', 'A1', 'take a trip'),
    ('sight', '/saɪt/', 'N', 'görmeli ýer', 'достопримечательность', 'a place visitors go to see', 'the sights of London.', 'Londonyň görmeli ýerleri', 'A2', 'see the sights'),
]

T['life_events'] = [
    ('become', '/bɪˈkʌm/', 'V', 'bolmak', 'становиться', 'to start to be something', 'She became famous.', 'Meşhur boldy.', 'A2', 'become famous'),
    ('famous', '/ˈfeɪməs/', 'ADJ', 'meşhur', 'знаменитый', 'known by many people', 'a famous singer.', 'meşhur aýdymçy', 'A1'),
    ('get married', '/ɡet ˈmærid/', 'PHR', 'öýlenmek / durmuşa çykmak', 'жениться', 'to become husband and wife', 'They got married in May.', 'Maýda öýlendiler.', 'A2'),
    ('fall in love', '/fɔːl ɪn lʌv/', 'PHR', 'söýmek, aşyk bolmak', 'влюбиться', 'to start to love someone', 'He fell in love with her.', 'Oňa aşyk boldy.', 'A2', 'fall in love with'),
    ('move house', '/muːv haʊs/', 'PHR', 'öý göçürmek', 'переехать', 'to start living in a different home', 'We moved house last year.', 'Geçen ýyl öý göçürdik.', 'A2'),
    ('get a job', '/ɡet ə dʒɒb/', 'PHR', 'iş tapmak', 'найти работу', 'to start working somewhere', 'She got a new job.', 'Täze iş tapdy.', 'A1'),
    ('meet somebody new', '/miːt ˈsʌmbədi njuː/', 'PHR', 'täze adam bilen tanyşmak', 'познакомиться с кем-то новым', 'to be introduced to a person you do not know', 'He met somebody new at work.', 'Işde täze adam bilen tanyşdy.', 'A2'),
    ('have a surprise', '/hæv ə səˈpraɪz/', 'PHR', 'geň galmak', 'получить сюрприз', 'to be given something unexpected', 'She had a surprise for him.', 'Oňa bir geň sowgady bardy.', 'A2'),
    ('travel', '/ˈtrævl/', 'V', 'syýahat etmek', 'путешествовать', 'to go to different places', 'They travel a lot.', 'Köp syýahat edýärler.', 'A1'),
    ('lucky', '/ˈlʌki/', 'ADJ', 'şowly', 'везучий', 'having good things happen by chance', 'You were lucky.', 'Şowly bolduň.', 'A2'),
]

T['infinitive'] = [
    ('learn', '/lɜːn/', 'V', 'öwrenmek', 'учиться', 'to get knowledge or skill', 'She wants to learn English.', 'Iňlis öwrenmek isleýär.', 'A1', 'learn to'),
    ('teach', '/tiːtʃ/', 'V', 'öwretmek', 'учить, преподавать', 'to give knowledge to someone', 'He teaches music.', 'Saz öwredýär.', 'A1'),
    ('practise', '/ˈpræktɪs/', 'V', 'türgenleşmek', 'практиковаться', 'to do something again to get better', 'Practise every day.', 'Her gün türgenleş.', 'A2'),
    ('improve', '/ɪmˈpruːv/', 'V', 'gowulandyrmak', 'улучшать', 'to make something better', 'My English improved.', 'Iňlisim gowulandy.', 'A2'),
    ('enjoy', '/ɪnˈdʒɔɪ/', 'V', 'lezzet almak', 'наслаждаться', 'to like doing something', 'I enjoy travelling.', 'Syýahat etmekden lezzet alýaryn.', 'A1', 'enjoy doing'),
    ('hope', '/həʊp/', 'V', 'umyt etmek', 'надеяться', 'to want something to happen', 'I hope to see you soon.', 'Tizara görüşeris diýip umyt edýärin.', 'A2', 'hope to'),
    ('plan', '/plæn/', 'V', 'meýilleşdirmek', 'планировать', 'to decide what you will do', 'We plan to leave early.', 'Ir gitmegi meýilleşdirýäris.', 'A2', 'plan to'),
    ('offer', '/ˈɒfə/', 'V', 'hödürlemek', 'предлагать', 'to say you will do something for someone', 'He offered to help.', 'Kömek etmegi hödürledi.', 'A2', 'offer to'),
    ('promise', '/ˈprɒmɪs/', 'V', 'wada bermek', 'обещать', 'to say you will certainly do something', 'She promised to call.', 'Jaň etjegini wada berdi.', 'A2', 'promise to'),
    ('refuse', '/rɪˈfjuːz/', 'V', 'ýüz öwürmek', 'отказываться', 'to say no to something', 'He refused to answer.', 'Jogap bermekden ýüz öwürdi.', 'B1', 'refuse to'),
    ('agree', '/əˈɡriː/', 'V', 'razy bolmak', 'соглашаться', 'to have the same opinion', 'We agreed to meet at six.', 'Sagat altyda duşuşmaga razy bolduk.', 'A2', 'agree to'),
    ('decide to', '/dɪˈsaɪd tuː/', 'PHR', '-mäge karar bermek', 'решить сделать', 'to choose to do something', 'She decided to stay.', 'Galmaga karar berdi.', 'A2'),
]

T['past_participles'] = [
    ('seen', '/siːn/', 'V', 'gören', 'видевший', 'the past participle of "see"', 'I have seen this film.', 'Bu filmi gördüm.', 'A2'),
    ('been', '/biːn/', 'V', 'bolan, baran', 'бывший', 'the past participle of "be"', 'She has been to Turkey.', 'Türkiýede boldy.', 'A1'),
    ('gone', '/ɡɒn/', 'V', 'giden', 'ушедший', 'the past participle of "go"', 'He has gone home.', 'Öýe gitdi.', 'A1'),
    ('done', '/dʌn/', 'V', 'eden', 'сделавший', 'the past participle of "do"', 'I have done my homework.', 'Öý işimi etdim.', 'A1'),
    ('eaten', '/ˈiːtn/', 'V', 'iýen', 'съевший', 'the past participle of "eat"', 'We have eaten already.', 'Eýýäm iýdik.', 'A2'),
    ('taken', '/ˈteɪkən/', 'V', 'alan', 'взявший', 'the past participle of "take"', 'She has taken the bus.', 'Awtobusda gitdi.', 'A2'),
    ('given', '/ˈɡɪvn/', 'V', 'beren', 'давший', 'the past participle of "give"', 'He has given me a book.', 'Maňa kitap berdi.', 'A2'),
    ('written', '/ˈrɪtn/', 'V', 'ýazan', 'написавший', 'the past participle of "write"', 'I have written to her.', 'Oňa ýazdym.', 'A2'),
    ('spoken', '/ˈspəʊkən/', 'V', 'gürlän', 'говоривший', 'the past participle of "speak"', 'She has spoken to him.', 'Onuň bilen gürleşdi.', 'A2'),
    ('lost', '/lɒst/', 'V', 'ýitiren', 'потерявший', 'the past participle of "lose"', 'I have lost my keys.', 'Açarlarymy ýitirdim.', 'A2'),
    ('won', '/wʌn/', 'V', 'udan', 'выигравший', 'the past participle of "win"', 'They have won the game.', 'Oýny utdular.', 'A2'),
    ('met', '/met/', 'V', 'duşuşan', 'встретивший', 'the past participle of "meet"', 'We have met before.', 'Öň duşuşdyk.', 'A2'),
    ('ever', '/ˈevə/', 'ADV', 'hiç', 'когда-либо', 'used in questions about any time', 'Have you ever been to London?', 'Londonda hiç bolduňmy?', 'A1'),
    ('already', '/ɔːlˈredi/', 'ADV', 'eýýäm', 'уже', 'before now', 'I have already eaten.', 'Eýýäm iýdim.', 'A2'),
    ('yet', '/jet/', 'ADV', 'entek', 'ещё', 'used in negatives to mean not until now', "I haven't finished yet.", 'Entek gutarmadym.', 'A2'),
    ('just', '/dʒʌst/', 'ADV', 'häzir', 'только что', 'a very short time ago', 'She has just left.', 'Häzir gitdi.', 'A2'),
]

T['travel_words'] = [
    ('journey', '/ˈdʒɜːni/', 'N', 'ýol, syýahat', 'путешествие', 'a trip from one place to another', 'a long journey.', 'uzyn ýol', 'A2'),
    ('suitcase', '/ˈsuːtkeɪs/', 'N', 'çemodan', 'чемодан', 'a case for clothes when travelling', 'a heavy suitcase.', 'agyr çemodan', 'A2'),
    ('passport', '/ˈpɑːspɔːt/', 'N', 'pasport', 'паспорт', 'an official document for travelling', 'Show your passport.', 'Pasportyňyzy görkeziň.', 'A2'),
    ('airport', '/ˈeəpɔːt/', 'N', 'howa menzili', 'аэропорт', 'a place where planes take off and land', 'The airport is busy.', 'Howa menzili işlek.', 'A1'),
    ('luggage', '/ˈlʌɡɪdʒ/', 'N', 'bagaž', 'багаж', 'the bags you take when travelling', 'How many pieces of luggage?', 'Näçe bagaž?', 'B1'),
    ('timetable', '/ˈtaɪmteɪbl/', 'N', 'wagt tertibi', 'расписание', 'a list of when things happen', 'the train timetable.', 'otly wagt tertibi', 'B1'),
    ('delay', '/dɪˈleɪ/', 'N', 'giçikme', 'задержка', 'when something is late', 'There was a delay.', 'Giçikme boldy.', 'B1'),
]

# ---- Teacher's Guide round 12: words from the lesson VOCABULARY boxes and
#      exercise keys, each block headed by its TG evidence page ----
# 1A phrase key, TG p.13 ("Goodbye = Bye")
T['greetings'] = [
    ('goodbye', '/ˌɡʊdˈbaɪ/', 'INTJ', 'hoş', 'до свидания', 'what you say when you leave someone', 'Goodbye! See you tomorrow.', 'Hoş! Ertir görüşeris.', 'A1', 'bye'),
]

# 5A "Vote for me!" VERBS-column key, TG p.255 ("a 2 use 3 swim 4 send 5 find
# 6 forget 7 tell 8 meet 9 look for 10 see 11 help 12 give 13 sing 14 take
# 15 wait for 16 try 17 draw 18 run 19 hear 20 call 21 buy 22 leave 23 paint
# 24 talk"); send/hear/leave/take were already in the Bank
T['verbs5A'] = [
    ('buy', '/baɪ/', 'V', 'satyn almak', 'покупать', 'to get something by paying money', 'I buy a newspaper every morning.', 'Her irden gazet satyn alýaryn.', 'A1', 'buy a newspaper'),
    ('call', '/kɔːl/', 'V', 'jaň etmek', 'звонить', 'to phone someone', 'Call me tonight.', 'Şu gije maňa jaň et.', 'A1', 'call a friend'),
    ('draw', '/drɔː/', 'V', 'surat çekmek', 'рисовать', 'to make a picture with a pen or pencil', 'She can draw very well.', 'Ol gaty gowy surat çekýär.', 'A1'),
    ('find', '/faɪnd/', 'V', 'tapmak', 'находить', 'to see or get something you were looking for', "I can't find my keys.", 'Açarymy tapyp bilemok.', 'A1'),
    ('forget', '/fəˈɡet/', 'V', 'ýatdan çykarmak', 'забывать', 'to not remember', "Don't forget your passport.", 'Pasportyňy ýatdan çykarma.', 'A1'),
    ('give', '/ɡɪv/', 'V', 'bermek', 'давать', 'to put something in someone’s hand', 'Give me the menu, please.', 'Menýuny beriň, haýyş.', 'A1'),
    ('help', '/help/', 'V', 'kömek etmek', 'помогать', 'to do something useful for someone', 'Can you help me, please?', 'Maňa kömek edip bilersiňizmi?', 'A1'),
    ('look for', '/lʊk fɔː/', 'PHR', 'gözlemek', 'искать', 'to try to find something', "I'm looking for my phone.", 'Telefonymy gözleýärin.', 'A1'),
    ('meet', '/miːt/', 'V', 'duşuşmak', 'встречать, встречаться', 'to come together with someone', "Let's meet at the cinema.", 'Kinode duşuşalyň.', 'A1'),
    ('paint', '/peɪnt/', 'V', 'reňklemek, surat çekmek', 'красить, писать красками', 'to put colour on something', 'He likes to paint landscapes.', 'Ol peýzaž çekmegi halaýar.', 'A1'),
    ('run', '/rʌn/', 'V', 'ylgamak', 'бегать', 'to move fast on your feet', 'I run in the park every day.', 'Her gün parkda ylgaw edýärin.', 'A1'),
    ('see', '/siː/', 'V', 'görmek', 'видеть', 'to use your eyes to notice something', 'Did you see the match?', 'Duşuşygy gördüňmi?', 'A1'),
    ('sing', '/sɪŋ/', 'V', 'aýdym aýtmak', 'петь', 'to make music with your voice', 'She sings beautifully.', 'Ol owadan aýdym aýdýar.', 'A1'),
    ('swim', '/swɪm/', 'V', 'ýüzmek', 'плавать', 'to move through water', 'We swim in the sea in summer.', 'Tomusda deňizde ýüzýäris.', 'A1'),
    ('talk', '/tɔːk/', 'V', 'gürleşmek', 'разговаривать', 'to speak to someone', 'They talk on the phone every day.', 'Olar her gün telefonda gürleşýärler.', 'A1'),
    ('tell', '/tel/', 'V', 'aýtmak, gürrüň bermek', 'рассказывать, говорить', 'to give someone information', 'Tell me about your day.', 'Günüň barada gürrüň ber.', 'A1'),
    ('try', '/traɪ/', 'V', 'synanyşmak', 'пробовать, пытаться', 'to attempt to do something', 'Try the chocolate cake.', 'Şokoladly keksi synap gör.', 'A1'),
    ('use', '/juːz/', 'V', 'ulanmak', 'использовать', 'to do something with a thing', 'Can I use your phone?', 'Telefonyňy ulanyp bilerinmi?', 'A1'),
    ('wait for', '/weɪt fɔː/', 'PHR', 'garaşmak', 'ждать', 'to stay until something happens', 'We wait for the bus here.', 'Awtobusa şu ýerde garaşýarys.', 'A1'),
]

# 6C "Making music" instrument key, TG p.87 e 6.17 ("1 accordion – accordionist
# 2 bass – bass player 3 violin – violinist 4 guitar – guitarist 5 piano –
# pianist 6 drums – drummer 7 keyboard – keyboard player 8 trumpet – trumpeter
# 9 saxophone – saxophonist"; "instrument + player" taught alongside)
T['instruments'] = [
    ('accordion', '/əˈkɔːdiən/', 'N', 'akkordeon', 'аккордеон', 'a musical instrument you press with both hands', 'He plays the accordion at weddings.', 'Ol toýlarda akkordeon çalýar.', 'A2'),
    ('bass', '/beɪs/', 'N', 'bas', 'бас', 'the lowest sound in music; a bass guitar', 'The bass is very loud in this song.', 'Bu aýdymda bas gaty güýçli.', 'A2'),
    ('drums', '/drʌmz/', 'N', 'deprek', 'барабаны', 'a set of round instruments you hit with sticks', 'She plays the drums in a band.', 'Ol toparda deprek çalýar.', 'A2'),
    ('guitar', '/ɡɪˈtɑː/', 'N', 'gitara', 'гитара', 'an instrument with strings that you play with your fingers', 'He plays the guitar very well.', 'Ol gitarany gaty gowy çalýar.', 'A1'),
    ('keyboard', '/ˈkiːbɔːd/', 'N', 'klawişli saz guraly', 'клавишные', 'an electronic musical instrument like a piano', 'The keyboard player joined the band.', 'Klawişçi topara goşuldy.', 'A2'),
    ('piano', '/piˈænəʊ/', 'N', 'pianino', 'пианино, фортепиано', 'a large instrument with black and white keys', 'She plays the piano every evening.', 'Ol her agşam pianino çalýar.', 'A1'),
    ('saxophone', '/ˈsæksəfəʊn/', 'N', 'saksafon', 'саксофон', 'a curved brass instrument you blow into', 'Jazz often has a saxophone.', 'Jazda köplenç saksafon bolýar.', 'A2'),
    ('trumpet', '/ˈtrʌmpɪt/', 'N', 'truba', 'труба', 'a brass instrument you blow into', 'He plays the trumpet in the school band.', 'Ol mekdep toparynda truba çalýar.', 'A2'),
    ('violin', '/ˌvaɪəˈlɪn/', 'N', 'skripka', 'скрипка', 'a string instrument you play with a bow', 'The violin is a beautiful instrument.', 'Skripka owadan saz guraly.', 'A2'),
    ('musical instrument', '/ˌmjuːzɪkl ˈɪnstrəmənt/', 'N', 'saz guraly', 'музыкальный инструмент', 'an object you play music on', 'Can you play a musical instrument?', 'Saz guraly çalyp bilýärsiňmi?', 'A2', 'play an instrument'),
]

# 8B "A house with a history": the Central heating and air conditioning box,
# TG p.109 + the furniture key p.256 ("8 air conditioning 13 ceiling 20
# central heating"); the light/lamp Vocabulary notes p.108 ("e.g. a floor
# lamp, a table lamp")
T['house2'] = [
    ('ceiling', '/ˈsiːlɪŋ/', 'N', 'potolok', 'потолок', 'the top inside surface of a room', 'There is a lamp on the ceiling.', 'Potolokda çyra bar.', 'A2'),
    ('air conditioning', '/ˈeə kənˌdɪʃənɪŋ/', 'N', 'howa kondisioneri', 'кондиционер', 'a machine that keeps a room cool', 'The hotel has air conditioning.', 'Myhmanhanada howa kondisioneri bar.', 'A2'),
    ('central heating', '/ˌsentrəl ˈhiːtɪŋ/', 'N', 'merkezi ýylylyk ulgamy', 'центральное отопление', 'a system that heats a whole building', 'Our flat has central heating.', 'Öýümizde merkezi ýylylyk ulgamy bar.', 'A2'),
    ('floor lamp', '/ˈflɔː læmp/', 'N', 'pol çyrasy', 'торшер', 'a tall lamp that stands on the floor', 'The floor lamp is next to the sofa.', 'Pol çyrasy diwanyň ýanynda.', 'A2'),
    ('table lamp', '/ˈteɪbl læmp/', 'N', 'stol çyrasy', 'настольная лампа', 'a small lamp that stands on a table', 'There is a table lamp on the desk.', 'Stolyň üstünde stol çyrasy bar.', 'A2'),
]

# 9A "#mydinnerlastnight" teach line, TG p.120
T['takeaway9A'] = [
    ('takeaway', '/ˈteɪkəweɪ/', 'N', 'taýawan (öýe iýmit)', 'еда навынос', 'hot food you buy cooked to eat at home (British English)', 'We ordered some takeaway salads.', 'Biz biraz taýawan salat sargyt etdik.', 'A2'),
]

# 9B "White gold" quantity examples, TG p.122-123 ("How much sugar is there
# in dark chocolate?", white bread / olive oil in the same food set)
T['sugar_foods'] = [
    ('dark chocolate', '/ˌdɑːk ˈtʃɒklət/', 'N', 'gara şokolad', 'тёмный шоколад', 'chocolate with a lot of cocoa and little milk', 'Dark chocolate has less sugar.', 'Gara şokoladda şeker az.', 'A2'),
    ('white bread', '/ˌwaɪt ˈbred/', 'N', 'ak çörek', 'белый хлеб', 'bread made from white flour', 'White bread is soft.', 'Ak çörek ýumşak bolýar.', 'A1'),
    ('olive oil', '/ˌɒlɪv ˈɔɪl/', 'N', 'zeýtun ýagy', 'оливковое масло', 'oil from olives, used in cooking', 'Cook the vegetables in olive oil.', 'Gök önümleri zeýtun ýagynda bişiriň.', 'A2'),
]

# ---- Practical English: six episodes, each with its own words
T['pe_hotel'] = [
    ('reception', '/rɪˈsepʃn/', 'N', 'resepsiýa', 'стойка регистрации', 'the desk where guests arrive', 'Ask at reception.', 'Resepsiýadan soraň.', 'A2', 'at reception'),
    ('the lift', '/ðə lɪft/', 'N', 'lift', 'лифт', 'a machine that carries people up and down', 'Take the lift to the third floor.', 'Üçünji gata lift bilen çykyň.', 'A2', 'take the lift'),
    ('a double room', '/ə ˈdʌbl ruːm/', 'N', 'iki adamlyk otag', 'двухместный номер', 'a hotel room with a big bed for two', 'We booked a double room.', 'Iki adamlyk otag aldyk.', 'A2'),
    ('a single room', '/ə ˈsɪŋɡl ruːm/', 'N', 'bir adamlyk otag', 'одноместный номер', 'a hotel room for one person', 'A single room, please.', 'Bir adamlyk otag, haýyş.', 'A2'),
    ('the ground floor', '/ðə ɡraʊnd flɔː/', 'N', 'zemini gat', 'первый этаж', 'the floor at street level', 'Breakfast is on the ground floor.', 'Ertirlik zemini gatda.', 'A2'),
    ('check in', '/tʃek ɪn/', 'PHR', 'hasaba durmak', 'заселиться', 'to arrive and register at a hotel', 'We checked in at nine.', 'Sagat dokuzda hasaba durduk.', 'A2'),
    ('check out', '/tʃek aʊt/', 'PHR', 'hasapdan çykmak', 'выселиться', 'to leave a hotel and pay', 'We checked out early.', 'Ir hasapdan çykdym.', 'A2'),
    ('reservation', '/ˌrezəˈveɪʃn/', 'N', 'öňünden alyş', 'бронь', 'an arrangement to keep a room', 'I have a reservation.', 'Öňünden alyşym bar.', 'A2', 'make a reservation'),
]

T['pe_cafe'] = [
    ('espresso', '/ˈesprəʊ/', 'N', 'espresso', 'эспрессо', 'a small strong coffee', 'an espresso, please.', 'bir espresso, haýyş', 'A2'),
    ('americano', '/əˌmerɪˈkɑːnəʊ/', 'N', 'amerikano', 'американо', 'a coffee made weaker with water', 'a regular americano.', 'adaty amerikano', 'A2'),
    ('latte', '/ˈlæteɪ/', 'N', 'latte', 'латте', 'a coffee with a lot of milk', 'a large latte.', 'uly latte', 'A2'),
    ('cappuccino', '/ˌkæpuˈtʃiːnəʊ/', 'N', 'kappuçino', 'капучино', 'a coffee with hot milk and foam', 'a double cappuccino.', 'iki esse kappuçino', 'A2'),
    ('brownie', '/ˈbraʊni/', 'N', 'şokoladly köke', 'брауни', 'a small square chocolate cake', 'a chocolate brownie.', 'şokoladly köke', 'A2'),
    ('croissant', '/ˈkrwæsɒŋ/', 'N', 'kruassan', 'круассан', 'a curved bread roll made with butter', 'a fresh croissant.', 'täze kruassan', 'A2'),
    ('take away', '/teɪk əˈweɪ/', 'PHR', 'ýanyň bilen almak', 'на вынос', 'food or drink you take with you', 'A coffee to take away.', 'Ýanym bilen bir kofe.', 'A2', 'to take away'),
    ('for here', '/fə hɪə/', 'PHR', 'şu ýerde', 'здесь (в кафе)', 'eaten or drunk where you buy it', 'For here or to take away?', 'Şu ýerdemi ýa-da ýanyňyz bilen?', 'A2'),
    # ---- café dialogue drill, TG p.53 ----
    ('single', '/ˈsɪŋɡl/', 'ADJ', 'ýeke (espresso)', 'одинарный', 'only one espresso', 'A single espresso, please.', 'Bir ýeke espresso, haýyş.', 'A2'),
    ('regular', '/ˈreɡjələ/', 'ADJ', 'adaty ölçeg', 'обычный размер', 'normal size (American English)', 'A regular latte, please.', 'Adaty ölçegli latte, haýyş.', 'A2'),
    ('large', '/lɑːdʒ/', 'ADJ', 'uly', 'большой', 'big size', 'A large cappuccino, please.', 'Uly kapuçino, haýyş.', 'A1'),
    ('anything else', '/ˌeniθɪŋ ˈels/', 'PHR', 'başga zat?', 'что-нибудь ещё?', 'what a seller asks when you may want more', 'Anything else? No, thanks.', 'Başga zat? Ýok, sag boluň.', 'A2'),
]

T['pe_shop'] = [
    ('How much is it?', '/haʊ mʌtʃ ɪz ɪt/', 'PHR', 'bahasy näçe?', 'сколько это стоит?', 'used to ask the price', 'How much is it? Twenty pounds.', 'Bahasy näçe? Iýirmi funt.', 'A1'),
    ("I'm looking for...", '/aɪm ˈlʊkɪŋ fɔː/', 'PHR', '... gözleýärin', 'я ищу...', 'used to say what you want to buy', "I'm looking for a shirt.", 'Köýnek gözleýärin.', 'A2'),
    ('Do you have this in...?', '/du ju hæv ðɪs ɪn/', 'PHR', 'munuň ... bar?', 'у вас есть это в...?', 'used to ask for another size or colour', 'Do you have this in blue?', 'Munuň gögi barmy?', 'A2'),
    ("It doesn't fit", '/ɪt dʌznt fɪt/', 'PHR', 'bolanok, ölçegi gelenok', 'не подходит по размеру', 'used when clothes are the wrong size', "It doesn't fit. Have you got a larger one?", 'Ölçegi gelenok. Ulysy barmy?', 'A2'),
    ('fitting room', '/ˈfɪtɪŋ ruːm/', 'N', 'synag otagy', 'примерочная', 'a room where you try on clothes', 'The fitting room is over there.', 'Synag otagy aňyrda.', 'A2'),
    ('I\'m sorry', '/aɪm ˈsɒri/', 'PHR', 'bagyşlaň', 'извините', 'used to apologize', "I'm really sorry.", 'Hakykatdan bagyşlaň.', 'A1'),
    ("Don't worry", '/dəʊnt ˈwʌri/', 'PHR', 'alada etme', 'не беспокойтесь', 'used to tell someone not to be upset', "Don't worry. No problem.", 'Alada etme. Mesele ýok.', 'A2'),
]

T['pe_directions'] = [
    ('turn left', '/tɜːn left/', 'PHR', 'çepe öwrüliň', 'поверните налево', 'used to tell someone which way to go', 'Turn left at the corner.', 'Burçda çepe öwrüliň.', 'A1'),
    ('turn right', '/tɜːn raɪt/', 'PHR', 'saga öwrüliň', 'поверните направо', 'used to tell someone which way to go', 'Turn right here.', 'Şu ýerde saga öwrüliň.', 'A1'),
    ('go straight on', '/ɡəʊ streɪt ɒn/', 'PHR', 'göni öňe gidiň', 'идите прямо', 'used to tell someone to keep going', 'Go straight on for 100 metres.', '100 metr göni öňe gidiň.', 'A2'),
    ('on the corner', '/ɒn ðə ˈkɔːnə/', 'PHR', 'burçda', 'на углу', 'where two streets meet', 'The bank is on the corner.', 'Bank burçda.', 'A2'),
    ('at the traffic lights', '/ət ðə ˈtræfɪk laɪts/', 'PHR', 'çyra ýanýan ýerde', 'на светофоре', 'where the road signals are', 'Turn right at the traffic lights.', 'Çyra ýanýan ýerde saga öwrüliň.', 'A2'),
    ('go past', '/ɡəʊ pɑːst/', 'PHR', 'ýanyndan geçiň', 'пройти мимо', 'to go by something without stopping', 'Go past the church.', 'Buthananyň ýanyndan geçiň.', 'A2'),
    ('at the end of the street', '/ət ði end əv ðə striːt/', 'PHR', 'köçäniň ahyrynda', 'в конце улицы', 'at the furthest point of a street', 'It is at the end of the street.', 'Köçäniň ahyrynda.', 'A2'),
    ('Excuse me, where is', '/ɪkˈskjuːz miː weər ɪz/', 'PHR', 'bagyşlaň, ... nirede?', 'извините, где...?', 'used to ask a stranger where a place is', 'Excuse me, where is the station?', 'Bagyşlaň, menzil nirede?', 'A1'),
]

T['pe_restaurant'] = [
    ('starter', '/ˈstɑːtə/', 'N', 'başlangyç tagam', 'закуска', 'a small dish eaten before the main one', 'soup as a starter.', 'başlangyç hökmünde çorba', 'A2'),
    ('main course', '/meɪn kɔːs/', 'N', 'esasy tagam', 'основное блюдо', 'the largest dish of a meal', 'chicken as a main course.', 'esasy tagam hökmünde towuk', 'A2'),
    ('dessert', '/dɪˈzɜːt/', 'N', 'süýji tagam', 'десерт', 'sweet food eaten at the end of a meal', 'What is there for dessert?', 'Süýji tagam näme bar?', 'A2', 'for dessert'),
    ('menu', '/ˈmenjuː/', 'N', 'menýu', 'меню', 'a list of the food a restaurant serves', 'Can I see the menu?', 'Menýuny görüp bilerinmi?', 'A1', 'see the menu'),
    ('bill', '/bɪl/', 'N', 'hasap', 'счёт', 'the paper that says what you must pay', 'The bill, please.', 'Hasaby, haýyş.', 'A1', 'pay the bill'),
    ('tip', '/tɪp/', 'N', 'çaý pul', 'чаевые', 'extra money you leave for the waiter', 'Leave a small tip.', 'Kiçi çaý pul goýuň.', 'A2', 'leave a tip'),
    ('waiter', '/ˈweɪtə/', 'N', 'ofisiant', 'официант', 'a person who serves food in a restaurant', 'The waiter brought the bill.', 'Ofisiant hasaby getirdi.', 'A1'),
    ('order', '/ˈɔːdə/', 'V', 'sargyt etmek', 'заказывать', 'to ask for food in a restaurant', 'We ordered fish.', 'Balyk sargyt etdik.', 'A2', 'order a meal'),
    ('soup', '/suːp/', 'N', 'çorba', 'суп', 'a hot liquid meal', 'onion soup.', 'sogan çorbasy', 'A1'),
    ('grilled', '/ɡrɪld/', 'ADJ', 'grillenen', 'жареный на гриле', 'cooked over a fire or hot surface', 'grilled chicken.', 'grillenen towuk', 'A2'),
]

T['pe_airport'] = [
    ('security', '/sɪˈkjʊərəti/', 'N', 'howpsuzlyk barlagy', 'контроль безопасности', 'the place where bags are checked at an airport', 'Go through security.', 'Howpsuzlyk barlagyndan geçiň.', 'A2', 'go through security'),
    ('departure lounge', '/dɪˈpɑːtʃə laʊndʒ/', 'N', 'uçuş zaly', 'зал ожидания', 'the area where you wait for a flight', 'Wait in the departure lounge.', 'Uçuş zalynda garaşyň.', 'B1'),
    ('gate', '/ɡeɪt/', 'N', 'gapy', 'выход на посадку', 'the place where you get on a plane', 'Go to gate twelve.', 'On ikinji gapa baryň.', 'A2'),
    ('taxi rank', '/ˈtæksi ræŋk/', 'N', 'taksi duralgasy', 'стоянка такси', 'a place where taxis wait for people', 'Take a taxi from the rank.', 'Duralgadan taksi tutuň.', 'B1'),
    ('cab', '/kæb/', 'N', 'taksi', 'такси', 'another word for a taxi', 'I called a cab.', 'Taksi çagyrdym.', 'A2', 'call a cab'),
    ('coach', '/kəʊtʃ/', 'N', 'uly awtobus', 'автобус (междугородный)', 'a large bus for long journeys', 'The coach leaves at eight.', 'Uly awtobus sagat sekizde gidýär.', 'B1'),
    ('the Tube', '/ðə tjuːb/', 'N', 'London metrosy', 'лондонское метро', 'the underground railway in London', 'Take the Tube to the airport.', 'Howa menziline metro bilen gidiň.', 'B1'),
]


# lesson -> (unit, title, topic from the contents table, [topics that supply its words])
# Student's Book page of each lesson, from the book's own syllabus checklist
# (Teacher's Guide pp.4-7 — the owner-supplied PDF; parsed table saved at
# content/pdf/ele-syllabus-pages.json). Every entry keeps its Source Location.
PAGE = {
    '1A': 6, '1B': 8, '1C': 10, 'PE1': 12, '2A': 14, '2B': 16, '2C': 18,
    '3A': 22, '3B': 24, '3C': 26, 'PE2': 28, '4A': 30, '4B': 32, '4C': 34,
    '5A': 38, '5B': 40, '5C': 42, 'PE3': 44, '6A': 46, '6B': 48, '6C': 50,
    '7A': 54, '7B': 56, '7C': 58, 'PE4': 60, '8A': 62, '8B': 64, '8C': 66,
    '9A': 70, '9B': 72, '9C': 74, 'PE5': 76, '10A': 78, '10B': 80, '10C': 82,
    '11A': 86, '11B': 88, '11C': 90, 'PE6': 92, '12A': 94, '12B': 96, '12C': 98,
}

LESSONS = {
    '1A':  (1,  'Welcome to the class', 'days · numbers 0-20 · hello and goodbye', ['days_numbers', 'greetings']),
    '1B':  (1,  'One world', 'countries · nationalities · numbers 21-100', ['days_numbers', 'countries']),
    '1C':  (1,  "What's your email?", 'classroom language', ['classroom']),
    '2A':  (2,  'Are you tidy or untidy?', 'things · in, on, under', ['things']),
    '2B':  (2,  'Made in America', 'colours · adjectives · modifiers', ['adjectives']),
    '2C':  (2,  'Slow down!', 'feelings · imperatives', ['feelings']),
    '3A':  (3,  'Britain: the good and the bad', 'verb phrases', ['verbs']),
    '3B':  (3,  '9 to 5', 'jobs', ['jobs']),
    '3C':  (3,  'Love me, love my dog', 'telling the time', ['time']),
    '4A':  (4,  'Family photos', 'the family', ['family']),
    '4B':  (4,  'From morning to night', 'daily routine', ['routine']),
    '4C':  (4,  'Blue Zones', 'months · adverbs of frequency', ['time']),
    '5A':  (5,  'Vote for me!', 'verb phrases', ['verbs5A']),
    '5B':  (5,  'A quiet life?', 'noise', ['noise']),
    '5C':  (5,  'A city for all seasons', 'the weather', ['weather']),
    '6A':  (6,  'A North African story', 'words in a story', ['story']),
    '6B':  (6,  'The third Friday in June', 'past time expressions', ['past_verbs']),
    '6C':  (6,  'Making music', 'go, have, get · musical instruments', ['go_have_get', 'instruments']),
    # 7A Selfies / 7B Wrong name, wrong place / 7C Happy New Year? — the TG
    # syllabus proves these lessons exist, but no content for them was ever
    # imported, so they stay empty rather than borrowing Unit 8's words.
    '8A':  (8,  'A murder mystery', 'the story · there is / there are', ['crime']),
    '8B':  (8,  'A house with a history', 'the house', ['house', 'house2']),
    '8C':  (8,  'Room 333', 'prepositions', ['prepositions']),
    '9A':  (9,  '#mydinnerlastnight', 'food and drink', ['food', 'takeaway9A']),
    '9B':  (9,  'White gold', 'food containers · quantifiers', ['containers', 'sugar_foods']),
    '9C':  (9,  'Facts and figures', 'high numbers', ['high_numbers']),
    '10A': (10, 'The most dangerous place...', 'places and buildings', ['places', 'superlatives', 'comparatives']),
    '10B': (10, 'Five continents in a day', 'city holidays · be going to', ['holidays']),
    '10C': (10, 'The fortune teller', 'verb phrases', ['life_events']),
    '11A': (11, 'Culture shock', 'adverbs', ['adverbs']),
    '11B': (11, 'Experiences or things?', 'verbs + infinitive', ['infinitive']),
    '11C': (11, 'How smart is your phone?', 'phones and the internet', ['phones']),
    '12A': (12, "I've seen it ten times!", 'irregular past participles · present perfect', ['past_participles']),
    '12B': (12, "He's been everywhere!", 'travel · experiences', ['travel_words']),
    '12C': (12, 'The English File interview', 'getting to the airport · public transport', ['transport']),
}


# word -> lesson, for the two Vocabulary Bank sections that serve more than one
# lesson. Checked against the book's own split of those pages:
#   p.148 "Days and numbers" -> 1A gets the days and 0-20, 1B gets 21-100,
#        the continents and the nationality adjectives
#   p.157 "Time"             -> 3C gets the clock, 4C gets months and frequency
def _wl(words, lesson):
    """Add words to WORD_LESSON. Keys are lowercased because lesson_for() looks
    words up by their lowercase headword, and the list below is written with the
    capitalisation the book uses."""
    for w in words.split():
        WORD_LESSON[w.replace('_', ' ').lower()] = lesson


WORD_LESSON = {}
_wl('Monday Tuesday Wednesday Thursday Friday Saturday Sunday weekday weekend '
    'zero one two three four five six seven eight nine ten', '1A')
_wl('eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen '
    'twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million '
    'north south east west continent Africa Asia Australia Europe '
    'North_America South_America African Asian Australian European American', '1B')
_wl("o'clock past to_(time) half_past quarter date", '3C')
_wl('first second third fourth fifth twelfth twentieth twenty-first thirty-first', '4C')
_wl('hardly_ever once_a_week twice_a_week every_day', '4C')
# 6C's "go, have, get" list repeats three routine verbs; the book teaches them in 4B
_wl('go_shopping get_up get_dressed', '4B')
_wl('always usually often sometimes hardly_ever never once_a_week twice_a_week '
    'every_day month January February March April May June July August September '
    'October November December', '4C')


def lesson_for(topic, en, fallback):
    """Which lesson owns this word. The Vocabulary Bank is organised by topic, but
    a topic can serve two lessons, so the word decides."""
    key = en.strip().lower()
    return WORD_LESSON.get(key, fallback)


# Practical English is not a Vocabulary Bank topic: it is six filmed episodes,
# each with its own words, so it gets its own unit.
PE_UNIT = 13
for code, n, title, topic, key in (
    ('PE1', 13, 'Arriving in London', 'in a hotel', 'pe_hotel'),
    ('PE2', 13, 'Coffee to take away', 'buying a coffee', 'pe_cafe'),
    ('PE3', 13, 'In a clothes shop', 'buying clothes', 'pe_shop'),
    ('PE4', 13, 'Getting lost', 'asking the way · directions', 'pe_directions'),
    ('PE5', 13, 'At a restaurant', 'understanding a menu', 'pe_restaurant'),
    ('PE6', 13, 'Going home', 'getting to the airport', 'pe_airport'),
):
    LESSONS[code] = (PE_UNIT, title, topic, [key])

# The Vocabulary Bank "Clothes" page serves PE3: the TG syllabus gives PE3
# "buying clothes · V clothes" (ele-tg.txt pp.4-7), and the old data carried
# the same words under a phantom "5C". Owner round 12: PE episodes stand on
# their own, so the clothes list joins the PE3 episode.
LESSONS['PE3'] = (PE_UNIT, 'In a clothes shop', 'buying clothes · clothes',
                  ['pe_shop', 'clothes'])


def lesson_sort_key(code):
    """Order lessons the way the book does. Numeric codes sort by unit then by
    letter; the Practical English episodes (PE1-PE6) come after unit 12."""
    m = re.match(r'^(\\d+)(.*)$', code)
    if m:
        return (int(m.group(1)), m.group(2))
    return (13, code)


def main():
    words, seen, dups = [], {}, []

    for lesson in sorted(LESSONS, key=lesson_sort_key):
        unit, title, topic, topics = LESSONS[lesson]
        # The Practical English episodes are numbered 1-6 inside their own unit,
        # so PE1..PE6 do not carry the unit number in their code.
        if lesson[0].isdigit() and lesson[:-1] != str(unit):
            raise SystemExit(f'lesson {lesson} says unit {unit}')
        for t in topics:
            if t not in T:
                raise SystemExit(f'lesson {lesson} refers to unknown topic "{t}"')
            for e in T[t]:
                if lesson_for(t, e[0], lesson) != lesson:
                    continue   # this word belongs to another lesson
                en, ipa, pos, tm, ru, de, ex, exTm, cefr = e[:9]
                coll = e[9] if len(e) > 9 else ''
                key = en.strip().lower()
                if key in seen:
                    dups.append(f'{lesson}: "{en}" (already in {seen[key]})')
                    continue
                seen[key] = lesson
                words.append({
                    'en': en, 'ipa': ipa, 'pos': pos, 'tm': tm, 'ru': ru,
                    'def': de, 'ex': ex, 'exTm': exTm, 'cefr': cefr,
                    'ox': 'Oxford 3000' if cefr in ('A1', 'A2') else 'Oxford 5000',
                    'syn': '—', 'coll': coll or '—', 'stage': 'New',
                    'books': [{'book': 'ele', 'unit': unit, 'lesson': lesson,
                           'page': PAGE[lesson]}],
                    'proofread': False,
                })

    if dups:
        raise SystemExit('duplicate headwords:\n  ' + '\n  '.join(dups))

    used = set(t for ts in LESSONS.values() for t in ts[3])
    unused = sorted(set(T) - used)
    if unused:
        raise SystemExit('topics declared but never used by a lesson: ' + ', '.join(unused))

    # Lessons with no Vocabulary Bank words are dropped rather than shown empty:
    # 2C, 5A, 5C, 6A, 7A, 8C, 9B, 9C, 10B, 11A and 11B are grammar and
    # communication lessons. They are listed in the book's contents table, but
    # there is no word list behind them, so an empty row would only mislead.
    lessons = []
    for lesson in sorted(LESSONS, key=lesson_sort_key):
        unit, title, topic, topics = LESSONS[lesson]
        n = sum(1 for w in words if w['books'][0]['lesson'] == lesson)
        if not n:
            continue
        lessons.append({'lesson': lesson, 'unit': unit, 'title': title, 'topic': topic,
                        'words': n})
    dropped = [l for l in LESSONS if l not in {x['lesson'] for x in lessons}]
    if dropped:
        print(f'grammar/communication lessons with no Vocabulary Bank words, not shown: {", ".join(dropped)}')

    pack = {
        'book': 'ele',
        'title': 'English File Elementary (4th edition) — Vocabulary Bank, by lesson',
        'lessons': lessons,
        'words': words,
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(pack, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print(f'wrote {os.path.normpath(OUT)}: {len(words)} words, {len(lessons)} lessons')
    by_unit = {}
    for l in lessons:
        by_unit.setdefault(l['unit'], []).append(l)
    for unit in sorted(by_unit):
        print(f"\nunit {unit:>2} — {sum(l['words'] for l in by_unit[unit])} words")
        for l in by_unit[unit]:
            print(f"    {l['lesson']:<4} {l['words']:>3} words  {l['title']}")


if __name__ == '__main__':
    main()
