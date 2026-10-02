#!/usr/bin/env python3
"""English File Beginner — vocabulary organised by LESSON (1A, 1B, 1C, 2A, ...).

English File units are taught as three lessons each, and the Vocabulary Bank maps
onto those lessons, not onto whole units. The lesson -> vocabulary mapping below
was read out of the book's own contents table in the OCR dump
(uploads/beginner book databsae.txt, lines 20-92), which lists every lesson with
its page, title, grammar and VOCABULARY column. That table is legible even though
the word lists themselves are not, so this mapping is verified rather than
invented. Quoted from it, in order:

  p.6  1A A cappuccino, please      numbers 0-10, days of the week, saying goodbye
  p.8  1B World music               countries
  p.10 1C Practical English Ep.1    the classroom / the alphabet
  p.12 2A Are you on holiday?       nationalities
  p.14 2B That's my bus!            phone numbers, numbers 11-100
  p.18 3A Where are my keys?        small things
  p.20 3B Souvenirs                 souvenirs
  p.22 3C Practical English Ep.2    the time, saying how you feel
  p.24 4A Meet the family           people and family
  p.26 4B The perfect car           colours and common adjectives
  p.30 5A A big breakfast?          food and drink
  p.32 5B A very long flight        common verb phrases 1
  p.34 5C Practical English Ep.3    the time, saying how you feel
  p.36 6A A school reunion          jobs and places of work
  p.38 6B Good morning, goodnight   a typical day
  p.42 7A Have a nice weekend!      common verb phrases 2: free time
  p.44 7B Lights, camera, action!   kinds of films
  p.46 7C Practical English Ep.4    months, ordinal numbers
  p.48 8A Can I park here?          more verb phrases
  p.50 8B Do you like cooking?     activities
  p.54 9A Everything's fine!        common verb phrases 2: travelling
  p.56 9B Working undercover        clothes
  p.60 10A A room with a view       hotels, in / on / under
  p.62 10B Where were you?          in / on / at (was, were)
  p.66 11A A new life in the USA    regular verbs
  p.68 11B How was your day?        irregular verbs; phrases with get, go, have, do
  p.70 11C Practical English Ep.6   prepositions of place
  p.72 12A Strangers on a train     regular and irregular verbs
  p.74 12B Revise the past          revision of past verb forms

HONESTY NOTE, updated round 11: the book's word *lists* are not machine-readable
in the OCR dump (content/tools/extract_beginner.py recovered 60 of ~270 items,
most corrupted), so the original headwords are reconstructed from knowledge of
the book. Round 11 added 34 words extracted from the Teacher's Guide PDF text
layer (owner-supplied EF4_Beginner_Teacher_s_Guide.pdf) — each carries an inline
"added round 11" comment naming its TG page and evidence pattern (word bank,
answer key, teach/elicit line). See content/tools/extract_beg_tg.py. Every word
remains proofread:false — no native TM/RU check.

Usage: python3 content/tools/gen_beginner.py
"""
import json
import os
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'beginner.json')

# lesson -> (unit, lesson title from the contents table, vocabulary topic, words)
# word = (en, ipa, pos, tm, ru, def, ex, exTm, cefr[, coll])

# Practical English episodes live in unit 13 — a PE "unit" beyond the book's
# 12 real units, exactly like the other imported books (ele/pre/int/...). The
# app renders them as their own yellow cards after units 1/3/5/7/11 via the
# book's pe:{unit:lesson} map, so they never sit inside a normal unit.

# Student's Book page of each lesson, from the book's own contents/syllabus
# table (quoted in the docstring above; identical to the Teacher's Guide
# syllabus, TG pp.4-7). Lets every entry keep its Source Location (§8).
PAGE = {
    '1A': 6, '1B': 8, '1C': 10, '2A': 12, '2B': 14, '3A': 18, '3B': 20,
    '3C': 22, '4A': 24, '4B': 26, '5A': 30, '5B': 32, '5C': 34, '6A': 36,
    '6B': 38, '7A': 42, '7B': 44, '7C': 46, '8A': 48, '8B': 50, '9A': 54,
    '9B': 56, '10A': 60, '10B': 62, '11A': 66, '11B': 68, '11C': 70,
    '12A': 72, '12B': 74,
}
L = {}

L['1A'] = (1, 'A cappuccino, please', 'numbers 0–10 · days of the week · saying goodbye', [
    ('hello', '/həˈləʊ/', 'INTJ', 'salam', 'привет', 'a word you say to greet someone', 'Hello! My name is Aýna.', 'Salam! Meniň adym Aýna.', 'A1', 'say hello'),
    ('goodbye', '/ˌɡʊdˈbaɪ/', 'INTJ', 'hoş', 'до свидания', 'a word you say when you leave', 'Goodbye, see you tomorrow.', 'Hoş, ertir görüşeris.', 'A1', 'say goodbye'),
    ('thank you', '/ˈθæŋk juː/', 'PHR', 'sag boluň', 'спасибо', 'what you say to show you are grateful', 'Thank you for your help.', 'Kömegiňiz üçin sag boluň.', 'A1', 'thank you very much'),
    ('please', '/pliːz/', 'ADV', 'haýyş', 'пожалуйста', 'used to make a request polite', 'A cappuccino, please.', 'Bir kapuçino, haýyş.', 'A1'),
    ('sorry', '/ˈsɒri/', 'ADJ', 'bagyşlaň', 'извините', 'used to say you regret something or to ask someone to repeat', 'Sorry, can you say that again?', 'Bagyşlaň, ýene aýdyp bilersiňizmi?', 'A1', "I'm sorry"),
    ('good morning', '/ˌɡʊd ˈmɔːnɪŋ/', 'PHR', 'haýyrly irden', 'доброе утро', 'what you say when you meet someone in the morning', 'Good morning, teacher!', 'Haýyrly irden, mugallym!', 'A1'),
    ('good evening', '/ˌɡʊd ˈiːvnɪŋ/', 'PHR', 'haýyrly agşam', 'добрый вечер', 'what you say when you meet someone in the evening', 'Good evening, how are you?', 'Haýyrly agşam, nähili?', 'A1'),
    ('zero', '/ˈzɪərəʊ/', 'NUM', 'nol', 'ноль', 'the number 0', 'The score was one–zero.', 'Hasap bir–nol boldy.', 'A1'),
    ('one', '/wʌn/', 'NUM', 'bir', 'один', 'the number 1', 'I have one brother.', 'Meniň bir agam bar.', 'A1'),
    ('two', '/tuː/', 'NUM', 'iki', 'два', 'the number 2', 'Two coffees, please.', 'Iki sany kofe, haýyş.', 'A1'),
    ('three', '/θriː/', 'NUM', 'üç', 'три', 'the number 3', 'There are three chairs.', 'Üç sany oturgyç bar.', 'A1'),
    ('four', '/fɔː/', 'NUM', 'dört', 'четыре', 'the number 4', 'My family has four people.', 'Maşgalamyzda dört adam bar.', 'A1'),
    ('five', '/faɪv/', 'NUM', 'bäş', 'пять', 'the number 5', 'I get up at five.', 'Men sagat bäşde turýaryn.', 'A1'),
    ('six', '/sɪks/', 'NUM', 'alty', 'шесть', 'the number 6', 'Six eggs, please.', 'Alty sany ýumurtga, haýyş.', 'A1'),
    ('seven', '/ˈsevn/', 'NUM', 'ýedi', 'семь', 'the number 7', 'There are seven days in a week.', 'Hepdede ýedi gün bar.', 'A1'),
    ('eight', '/eɪt/', 'NUM', 'sekiz', 'восемь', 'the number 8', 'The lesson starts at eight.', 'Sapak sagat sekizde başlaýar.', 'A1'),
    ('nine', '/naɪn/', 'NUM', 'dokuz', 'девять', 'the number 9', 'My room is number nine.', 'Meniň otagym dokuzynjy.', 'A1'),
    ('ten', '/ten/', 'NUM', 'on', 'десять', 'the number 10', 'I have ten pencils.', 'Meniň on sany galamym bar.', 'A1'),
    ('Monday', '/ˈmʌndeɪ/', 'N', 'duşenbe', 'понедельник', 'the first day of the working week', 'I work on Monday.', 'Men duşenbe işleýärin.', 'A1', 'on Monday'),
    ('Tuesday', '/ˈtjuːzdeɪ/', 'N', 'sişenbe', 'вторник', 'the day after Monday', 'We have English on Tuesday.', 'Sişenbe biziň iňlis sapagymyz bar.', 'A1', 'on Tuesday'),
    ('Wednesday', '/ˈwenzdeɪ/', 'N', 'çarşenbe', 'среда', 'the middle day of the working week', 'She is busy on Wednesday.', 'Ol çarşenbe güni meşgul.', 'A1', 'on Wednesday'),
    ('Thursday', '/ˈθɜːzdeɪ/', 'N', 'penşenbe', 'четверг', 'the day after Wednesday', 'They arrive on Thursday.', 'Olar penşenbe gelýärler.', 'A1', 'on Thursday'),
    ('Friday', '/ˈfraɪdeɪ/', 'N', 'anna', 'пятница', 'the last day of the working week', 'See you on Friday!', 'Anna güni görüşeris!', 'A1', 'on Friday'),
    ('Saturday', '/ˈsætədeɪ/', 'N', 'şenbe', 'суббота', 'the first day of the weekend', 'I relax on Saturday.', 'Şenbe güni dynç alýaryn.', 'A1', 'on Saturday'),
    ('Sunday', '/ˈsʌndeɪ/', 'N', 'ýekşenbe', 'воскресенье', 'the last day of the week', 'Sunday is a family day.', 'Ýekşenbe maşgala güni.', 'A1', 'on Sunday'),
])

L['1B'] = (1, 'World music', 'countries', [
    ('the UK', '/ðə ˌjuː ˈkeɪ/', 'N', 'Beýik Britaniýa', 'Великобритания', 'the country made up of England, Scotland, Wales and Northern Ireland', 'She lives in the UK.', 'Ol Beýik Britaniýada ýaşaýar.', 'A1'),
    ('the USA', '/ðə ˌjuː es ˈeɪ/', 'N', 'ABŞ', 'США', 'the United States of America', 'He is from the USA.', 'Ol ABŞ-dan.', 'A1'),
    ('Turkey', '/ˈtɜːki/', 'N', 'Türkiýe', 'Турция', 'a country in Europe and Asia', 'They are from Turkey.', 'Olar Türkiýeden.', 'A1'),
    ('Russia', '/ˈrʌʃə/', 'N', 'Orsýet', 'Россия', 'the largest country in the world', 'She is from Russia.', 'Ol Orsýetden.', 'A1'),
    ('China', '/ˈtʃaɪnə/', 'N', 'Hytaý', 'Китай', 'a large country in East Asia', 'This tea is from China.', 'Bu çaý Hytaýdan.', 'A1'),
    ('Japan', '/dʒəˈpæn/', 'N', 'Ýaponiýa', 'Япония', 'an island country in East Asia', 'He works in Japan.', 'Ol Ýaponiýada işleýär.', 'A1'),
    ('Brazil', '/brəˈzɪl/', 'N', 'Braziliýa', 'Бразилия', 'the largest country in South America', 'Football is popular in Brazil.', 'Braziliýada futbol meşhur.', 'A1'),
    ('Egypt', '/ˈiːdʒɪpt/', 'N', 'Müsür', 'Египет', 'a country in North Africa', 'The pyramids are in Egypt.', 'Piramidalar Müsürde.', 'A1'),
    ('Italy', '/ˈɪtəli/', 'N', 'Italiýa', 'Италия', 'a country in southern Europe', 'Modena is in Italy.', 'Modena Italiýada.', 'A1'),
    ('Spain', '/speɪn/', 'N', 'Ispaniýa', 'Испания', 'a country in south-west Europe', 'They speak Spanish in Spain.', 'Ispaniýada ispança gepleýärler.', 'A1'),
    ('Poland', '/ˈpəʊlənd/', 'N', 'Polşa', 'Польша', 'a country in central Europe', 'Gdansk is in Poland.', 'Gdansk Polşada.', 'A1'),
    ('Turkmenistan', '/tɜːkˈmenɪstæn/', 'N', 'Türkmenistan', 'Туркменистан', 'a country in Central Asia', 'I am from Turkmenistan.', 'Men Türkmenistandan.', 'A1'),
    # ── added round 11 from the Teacher's Guide (evidence: TG photocopiable
    # 1B word bank, p.133/209 "Egypt England France Germany Italy Poland
    # Russia Spain Switzerland Turkey", + country key p.17 "Mexico") ──
    ('England', '/ˈɪŋɡlənd/', 'N', 'Angliýa', 'Англия', 'a country that is part of the UK', 'London is in England.', 'London Angliýada.', 'A1'),
    ('France', '/frɑːns/', 'N', 'Fransiýa', 'Франция', 'a country in western Europe', 'Paris is the capital of France.', 'Pariž Fransiýanyň paýtagty.', 'A1'),
    ('Germany', '/ˈdʒɜːməni/', 'N', 'Germaniýa', 'Германия', 'a country in central Europe', 'She is from Germany.', 'Ol Germaniýadan.', 'A1'),
    ('Switzerland', '/ˈswɪtsələnd/', 'N', 'Şweýsariýa', 'Швейцария', 'a country in central Europe, famous for mountains and chocolate', 'They are from Switzerland.', 'Olar Şweýsariýadan.', 'A1'),
    ('Mexico', '/ˈmeksɪkəʊ/', 'N', 'Meksika', 'Мексика', 'a country in North America', 'He is from Mexico.', 'Ol Meksikadan.', 'A1'),
])

L['1C'] = (13, 'Practical English 1 · checking into a hotel', 'the classroom · the alphabet', [
    ('board', '/bɔːd/', 'N', 'tagta', 'доска', 'the flat surface a teacher writes on', 'Look at the board, please.', 'Tagta serediň, haýyş.', 'A1'),
    ('door', '/dɔː/', 'N', 'gapy', 'дверь', 'the part you open to go into a room', 'Close the door, please.', 'Gapyny ýapyň, haýyş.', 'A1', 'open the door'),
    ('window', '/ˈwɪndəʊ/', 'N', 'aýna, penjire', 'окно', 'an opening in a wall with glass in it', 'Open the window, it is hot.', 'Penjiräni açyň, yssy.', 'A1', 'open the window'),
    ('chair', '/tʃeə/', 'N', 'oturgyç', 'стул', 'a seat for one person', 'Sit on the chair.', 'Oturgyça oturyň.', 'A1'),
    ('table', '/ˈteɪbl/', 'N', 'stol', 'стол', 'a piece of furniture with a flat top', 'The books are on the table.', 'Kitaplar stoluň üstünde.', 'A1', 'on the table'),
    ('laptop', '/ˈlæptɒp/', 'N', 'noutbuk', 'ноутбук', 'a small computer you can carry', 'I do my homework on my laptop.', 'Öý işimi noutbukda edýärin.', 'A1'),
    ('dictionary', '/ˈdɪkʃənri/', 'N', 'sözlük', 'словарь', 'a book that lists words and their meanings', 'Look it up in the dictionary.', 'Sözlükden tap.', 'A1', 'look it up in the dictionary'),
    ('paper', '/ˈpeɪpə/', 'N', 'kagyz', 'бумага', 'the material you write on', 'I need a piece of paper.', 'Maňa bir bölek kagyz gerek.', 'A1', 'a piece of paper'),
    ('pen', '/pen/', 'N', 'ruçka', 'ручка', 'an object you write with, using ink', 'Can I borrow your pen?', 'Ruçkaňy alyp bilerinmi?', 'A1', 'borrow a pen'),
    ('bag', '/bæɡ/', 'N', 'sumka', 'сумка', 'a soft container you carry things in', 'Your sunglasses are in your bag.', 'Äýnegiň sumkaňda.', 'A1'),
    ('pencil', '/ˈpensl/', 'N', 'galam', 'карандаш', 'an object you write with, made of wood and graphite', 'Write in pencil, please.', 'Galam bilen ýazyň, haýyş.', 'A1'),
    ('notebook', '/ˈnəʊtbʊk/', 'N', 'depder', 'тетрадь', 'a book with empty pages for writing notes', 'Write the new words in your notebook.', 'Täze sözleri depderiňe ýaz.', 'A1'),
    ('alphabet', '/ˈælfəbet/', 'N', 'elipbiý', 'алфавит', 'the set of letters used to write a language', 'The English alphabet has 26 letters.', 'Iňlis elipbiýinde 26 harp bar.', 'A1', 'the English alphabet'),
    ('letter', '/ˈletə/', 'N', 'harp', 'буква', 'one of the symbols that make up an alphabet', 'What letter is this?', 'Bu haýsy harp?', 'A1'),
    ('spell', '/spel/', 'V', 'bölekleýin aýtmak, harplap aýtmak', 'произносить по буквам', 'to say the letters of a word in order', 'Can you spell your name?', 'Adyňyzy harplap aýdyp bilersiňizmi?', 'A1', "spell your name"),
    ('excuse me', '/ɪkˈskjuːz miː/', 'PHR', 'bagyşlaň', 'извините', 'used to get someone\'s attention politely', 'Excuse me, what\'s this in English?', 'Bagyşlaň, bu iňlisçe näme?', 'A1'),
    # ── added round 11: PE1 abbreviations key, TG p.21 ("1 VIP 2 CNN 3 FBI
    # 4 BBC 5 ATM 6 USB 7 BMW 8 EU") — only the everyday abbreviations are
    # taken; brand/media names (CNN, FBI, BBC, BMW, EU) are proper names. ──
    ('ATM', '/ˌeɪ tiː ˈem/', 'N', 'bankomat', 'банкомат', 'a machine where you get money from your bank account', 'Where is the ATM? I need some money.', 'Bankomat nirede? Maňa pul gerek.', 'A1'),
    ('USB', '/ˌjuː es ˈbiː/', 'N', 'USB (ýat enjamy)', 'ю-эс-би, флешка', 'a small device that stores computer files', 'The photos are on my USB.', 'Suratlar USB-imde.', 'A1'),
    ('VIP', '/ˌviː aɪ ˈpiː/', 'N', 'VIP, örän möhüm adam', 'VIP, очень важная персона', 'a very important person', 'VIP guests stay in the best rooms.', 'VIP myhmanlar iň gowy otaglarda galýar.', 'A1'),
])

L['2A'] = (2, 'Are you on holiday?', 'nationalities', [
    ('British', '/ˈbrɪtɪʃ/', 'ADJ', 'britan', 'британский', 'from the UK', 'She is British.', 'Ol britan.', 'A1'),
    ('American', '/əˈmerɪkən/', 'ADJ', 'amerikan', 'американский', 'from the USA', 'He is American.', 'Ol amerikan.', 'A1'),
    ('Turkish', '/ˈtɜːkɪʃ/', 'ADJ', 'türk', 'турецкий', 'from Turkey', 'This is Turkish coffee.', 'Bu türk kofesi.', 'A1'),
    ('Russian', '/ˈrʌʃn/', 'ADJ', 'orus', 'русский', 'from Russia', 'They are Russian.', 'Olar orus.', 'A1'),
    ('Chinese', '/ˌtʃaɪˈniːz/', 'ADJ', 'hytaý', 'китайский', 'from China', 'I like Chinese food.', 'Hytaý naharyny halaýaryn.', 'A1'),
    ('Japanese', '/ˌdʒæpəˈniːz/', 'ADJ', 'ýapon', 'японский', 'from Japan', 'This is a Japanese car.', 'Bu ýapon maşyny.', 'A1'),
    ('Brazilian', '/brəˈzɪliən/', 'ADJ', 'braziliýaly', 'бразильский', 'from Brazil', 'He is Brazilian.', 'Ol braziliýaly.', 'A1'),
    ('Italian', '/ɪˈtæliən/', 'ADJ', 'italýan', 'итальянский', 'from Italy', 'Italian food is famous.', 'Italýan nahary meşhur.', 'A1'),
    ('Spanish', '/ˈspænɪʃ/', 'ADJ', 'ispan', 'испанский', 'from Spain', 'She speaks Spanish.', 'Ol ispança gepleýär.', 'A1', 'speak Spanish'),
    ('Polish', '/ˈpəʊlɪʃ/', 'ADJ', 'polýak', 'польский', 'from Poland', 'This is a Polish name.', 'Bu polýak ady.', 'A1'),
    ('Turkmen', '/tɜːkˈmen/', 'ADJ', 'türkmen', 'туркменский', 'from Turkmenistan', 'I am Turkmen.', 'Men türkmen.', 'A1'),
    ('nationality', '/ˌnæʃəˈnæləti/', 'N', 'millet, milliýet', 'национальность', 'the country someone is a citizen of', 'What\'s your nationality?', 'Milliýetiňiz näme?', 'A1'),
    # ── added round 11: nationalities circled in the 2A key, TG p.25
    # ("2 American 3 Chinese 4 Swiss" + "the United States (USA)"), and the
    # 2A new-word drill, TG p.28 ("drill … e.g. business /ˈbɪznəs/") ──
    ('Swiss', '/swɪs/', 'ADJ', 'şweýsariýaly', 'швейцарский, швейцарец', 'from Switzerland', 'She is Swiss. She is from Switzerland.', 'Ol şweýsariýaly. Ol Şweýsariýadan.', 'A1'),
    ('English', '/ˈɪŋɡlɪʃ/', 'ADJ', 'iňlis', 'английский, англичанин', 'from England; also the language', 'He is English. He is from England.', 'Ol iňlis. Ol Angliýadan.', 'A1'),
    ('German', '/ˈdʒɜːmən/', 'ADJ', 'nemes', 'немецкий, немец', 'from Germany; also the language', 'She is German. She is from Germany.', 'Ol nemes. Ol Germaniýadan.', 'A1'),
    ('the United States', '/ðə juːˌnaɪtɪd ˈsteɪts/', 'N', 'Amerikanyň Birleşen Ştatlary', 'Соединённые Штаты', 'the full name of the USA', 'He is from the United States (USA).', 'Ol Amerikanyň Birleşen Ştatlaryndan (ABŞ).', 'A1', 'the USA'),
    ('business', '/ˈbɪznəs/', 'N', 'iş, biznes', 'бизнес, дело', 'work that you do for a company, not for pleasure', 'Are you here on business or on holiday?', 'Siz iş bilenmi ýa-da dynç almaga geldiňizmi?', 'A1', 'on business'),
])

L['2B'] = (2, "That's my bus!", 'phone numbers · numbers 11–100', [
    ('eleven', '/ɪˈlevn/', 'NUM', 'on bir', 'одиннадцать', 'the number 11', 'There are eleven players.', 'On bir oýunçy bar.', 'A1'),
    ('twelve', '/twelv/', 'NUM', 'on iki', 'двенадцать', 'the number 12', 'The class starts at twelve.', 'Sapak on ikide başlaýar.', 'A1'),
    ('thirteen', '/ˌθɜːˈtiːn/', 'NUM', 'on üç', 'тринадцать', 'the number 13', 'She is thirteen years old.', 'Ol on üç ýaşynda.', 'A1'),
    ('fourteen', '/ˌfɔːˈtiːn/', 'NUM', 'on dört', 'четырнадцать', 'the number 14', 'There are fourteen students.', 'On dört okuwçy bar.', 'A1'),
    ('fifteen', '/ˌfɪfˈtiːn/', 'NUM', 'on bäş', 'пятнадцать', 'the number 15', 'It costs fifteen manat.', 'Bahasy on bäş manat.', 'A1'),
    ('sixteen', '/ˌsɪksˈtiːn/', 'NUM', 'on alty', 'шестнадцать', 'the number 16', 'He is sixteen.', 'Ol on alty ýaşynda.', 'A1'),
    ('seventeen', '/ˌsevnˈtiːn/', 'NUM', 'on ýedi', 'семнадцать', 'the number 17', 'My sister is seventeen.', 'Uýam on ýedi ýaşynda.', 'A1'),
    ('eighteen', '/ˌeɪˈtiːn/', 'NUM', 'on sekiz', 'восемнадцать', 'the number 18', 'You can vote at eighteen.', 'On sekiz ýaşynda saýlap bilersiň.', 'A1'),
    ('nineteen', '/ˌnaɪnˈtiːn/', 'NUM', 'on dokuz', 'девятнадцать', 'the number 19', 'The bus leaves at nineteen.', 'Awtobus on dokuzda gidýär.', 'A1'),
    ('twenty', '/ˈtwenti/', 'NUM', 'ýigrimi', 'двадцать', 'the number 20', 'I am twenty years old.', 'Men ýigrimi ýaşymda.', 'A1'),
    ('thirty', '/ˈθɜːti/', 'NUM', 'otuz', 'тридцать', 'the number 30', 'The lesson is thirty minutes.', 'Sapak otuz minut.', 'A1'),
    ('forty', '/ˈfɔːti/', 'NUM', 'kyrk', 'сорок', 'the number 40', 'He is forty.', 'Ol kyrk ýaşynda.', 'A1'),
    ('fifty', '/ˈfɪfti/', 'NUM', 'elli', 'пятьдесят', 'the number 50', 'There are fifty words.', 'Elli sany söz bar.', 'A1'),
    ('sixty', '/ˈsɪksti/', 'NUM', 'altmyş', 'шестьдесят', 'the number 60', 'My grandfather is sixty.', 'Atam altmyş ýaşynda.', 'A1'),
    ('seventy', '/ˈsevnti/', 'NUM', 'ýetmiş', 'семьдесят', 'the number 70', 'Seventy people came.', 'Ýetmiş adam geldi.', 'A1'),
    ('eighty', '/ˈeɪti/', 'NUM', 'segsen', 'восемьдесят', 'the number 80', 'It is eighty pages long.', 'Seksen sahypa.', 'A1'),
    ('ninety', '/ˈnaɪnti/', 'NUM', 'togsan', 'девяносто', 'the number 90', 'Ninety percent passed.', 'Togsan göterimi geçdi.', 'A1'),
    ('hundred', '/ˈhʌndrəd/', 'NUM', 'ýüz', 'сто', 'the number 100', 'A hundred students study here.', 'Ýüz okuwçy şu ýerde okaýar.', 'A1', 'a hundred'),
    ('number', '/ˈnʌmbə/', 'N', 'san, nomer', 'номер', 'a symbol or word that says how many, or an identifying code', 'What\'s your phone number?', 'Telefon nomeriňiz näme?', 'A1', 'phone number'),
    ('mobile', '/ˈməʊbaɪl/', 'N', 'ykjam telefon', 'мобильный телефон', 'a phone you can carry with you', 'My mobile is in my bag.', 'Ykjam telefonum sumkamda.', 'A1', 'mobile phone'),
    ('phone number', '/ˈfəʊn ˌnʌmbə/', 'N', 'telefon belgisi', 'номер телефона', 'the numbers you use to call someone', 'Write down his phone number.', 'Onuň telefon belgisini ýaz.', 'A1'),
])

L['3A'] = (3, 'Where are my keys?', 'small things', [
    ('phone', '/fəʊn/', 'N', 'telefon', 'телефон', 'a machine you use to talk to someone far away', 'Answer the phone, please.', 'Telefona jogap beriň, haýyş.', 'A1', 'answer the phone'),
    ('watch (n.)', '/wɒtʃ/', 'N', 'sagat', 'часы', 'a small clock you wear on your wrist', 'My watch is new.', 'Sagadym täze.', 'A1'),
    ('tablet', '/ˈtæblət/', 'N', 'planşet', 'планшет', 'a flat computer you hold in your hands', 'I read on my tablet.', 'Planşetde okaýaryn.', 'A1'),
    ('wallet', '/ˈwɒlɪt/', 'N', 'gapjyk', 'кошелёк', 'a small flat case for money and cards', 'The money is in my wallet.', 'Pul gapjygymda.', 'A1'),
    ('purse', '/pɜːs/', 'N', 'aýal gapjygy', 'кошелёк', 'a small bag for coins, used especially by women', 'She put the coins in her purse.', 'Şaýy pullary gapjygyna saldy.', 'A1'),
    ('glasses', '/ˈɡlɑːsɪz/', 'N', 'äýnek', 'очки', 'two lenses in a frame you wear to see better', 'Where are my glasses?', 'Äýnegim nirede?', 'A1', 'wear glasses'),
    ('photo', '/ˈfəʊtəʊ/', 'N', 'surat', 'фотография', 'a picture made with a camera', 'This is a photo of my family.', 'Bu maşgalamyň suraty.', 'A1', 'take a photo'),
    ('charger', '/ˈtʃɑːdʒə/', 'N', 'zarýadnik', 'зарядное устройство', 'a device you use to put power into a battery', 'I can\'t find my charger.', 'Zarýadnikmi tapyp bilemok.', 'A1'),
    ('ID card', '/ˌaɪ ˈdiː kɑːd/', 'N', 'şahsyýetnama', 'удостоверение личности', 'an official card that shows who you are', 'Show your ID card, please.', 'Şahsyýetnamaňyzy görkeziň, haýyş.', 'A1'),
    ('passport', '/ˈpɑːspɔːt/', 'N', 'pasport', 'паспорт', 'an official document you need to travel abroad', 'My passport is in my bag.', 'Pasportym sumkamda.', 'A1'),
    ('umbrella', '/ʌmˈbrelə/', 'N', 'sätr', 'зонт', 'an object you hold above you to keep dry', 'Take an umbrella, it is raining.', 'Sätr alyň, ýagyş ýagýar.', 'A1'),
    ('camera', '/ˈkæmərə/', 'N', 'fotoapparat', 'фотоаппарат', 'a machine for taking photographs', 'He bought a new camera.', 'Ol täze fotoapparat satyn aldy.', 'A1', 'take a photo with a camera'),
    ('credit card', '/ˈkredɪt kɑːd/', 'N', 'kredit kart', 'кредитная карта', 'a small plastic card you use to pay for things later', 'Can I pay by credit card?', 'Kredit kart bilen töläp bilerinmi?', 'A1', 'pay by credit card'),
    ('debit card', '/ˈdebɪt kɑːd/', 'N', 'debit kart', 'дебетовая карта', 'a card that takes money straight out of your bank account', 'She paid with a debit card.', 'Ol debit kart bilen töledi.', 'A1', 'pay with a debit card'),
    ('key', '/kiː/', 'N', 'açar', 'ключ', 'a shaped piece of metal you use to open a lock', 'Where are my keys?', 'Açarlarym nirede?', 'A1', 'room key'),
    ('newspaper', '/ˈnjuːzpeɪpə/', 'N', 'gazet', 'газета', 'a set of large printed pages with news', 'He reads the newspaper every morning.', 'Ol her irden gazet okaýar.', 'A1', 'read the newspaper'),
    ('sunglasses', '/ˈsʌnɡlɑːsɪz/', 'N', 'gün äýnegi', 'солнечные очки', 'dark glasses you wear in bright sunlight', 'Where are my sunglasses?', 'Gün äýnegim nirede?', 'A1', 'wear sunglasses'),
    # ── added round 11: 3A plural-exercise key, TG p.36 ("bank cards") ──
    ('bank card', '/ˈbæŋk kɑːd/', 'N', 'bank karty', 'банковская карта', 'a plastic card from your bank that you use to pay or get money', 'Can I pay by bank card?', 'Bank karty bilen töläp bilerinmi?', 'A1'),
])

L['3B'] = (3, 'Souvenirs', 'souvenirs', [
    ('souvenir', '/ˌsuːvəˈnɪə/', 'N', 'ýadygärlik sowgat', 'сувенир', 'something you buy or keep to remember a place', 'I bought a souvenir in Istanbul.', 'Stambulyň ýadygärlik sowgadyny satyn aldym.', 'A1', 'buy a souvenir'),
    ('mug', '/mʌɡ/', 'N', 'krujka', 'кружка', 'a large cup with a handle', 'This mug says "I love London".', 'Bu krujkada "I love London" ýazylan.', 'A1'),
    ('T-shirt', '/ˈtiː ʃɜːt/', 'N', 'futbolka', 'футболка', 'a light shirt with short sleeves', 'I bought a T-shirt with the city name.', 'Şäheriň ady ýazylan futbolka aldym.', 'A1', 'wear a T-shirt'),
    ('postcard', '/ˈpəʊstkɑːd/', 'N', 'pochta kartasy', 'открытка', 'a card with a picture you send by post', 'She sent me a postcard from Rome.', 'Rimden maňa kart ugratdy.', 'A1', 'send a postcard'),
    ('keyring', '/ˈkiːrɪŋ/', 'N', 'açar halkasy', 'брелок', 'a ring or chain that holds keys', 'This keyring is from Paris.', 'Bu açar halkasy Parižden.', 'A1'),
    ('fridge magnet', '/frɪdʒ ˈmæɡnət/', 'N', 'holodilnik magniti', 'магнит на холодильник', 'a small decoration that sticks to a fridge', 'We collect fridge magnets.', 'Hlodilnik magnitlaryny ýygnaýarys.', 'A1'),
    ('gift', '/ɡɪft/', 'N', 'sowgat', 'подарок', 'something you give someone to please them', 'This gift is for you.', 'Bu sowgat saňa.', 'A1', 'buy a gift'),
    ('shop', '/ʃɒp/', 'N', 'dükan', 'магазин', 'a place where you buy things', 'The gift shop is near the museum.', 'Sowgat dükany muzeýiň ýanynda.', 'A1', 'gift shop'),
    ('price', '/praɪs/', 'N', 'baha', 'цена', 'the amount of money something costs', 'The price is ten euros.', 'Bahasy on ýewro.', 'A1', 'the price of'),
    ('cheap', '/tʃiːp/', 'ADJ', 'arzan', 'дешёвый', 'costing little money', 'The souvenirs are cheap here.', 'Bu ýerde ýadygärlikler arzan.', 'A1'),
    ('expensive', '/ɪkˈspensɪv/', 'ADJ', 'gymmat', 'дорогой', 'costing a lot of money', 'This camera is expensive.', 'Bu fotoapparat gymmat.', 'A1'),
])

L['3C'] = (13, 'Practical English 2 · understanding prices', 'the time · saying how you feel', [
    ("o'clock", '/əˈklɒk/', 'ADV', 'sagat', 'час (ровно)', 'used after a number to say the exact hour', 'The film starts at eight o\'clock.', 'Film sagat sekizde başlaýar.', 'A1'),
    ('half past', '/ˌhɑːf ˈpɑːst/', 'PHR', 'ýarym', 'половина', 'thirty minutes after the hour', 'It is half past nine.', 'Sagat dokuzdan ýarym.', 'A1'),
    ('quarter', '/ˈkwɔːtə/', 'N', 'çärýek', 'четверть', 'fifteen minutes, a quarter of an hour', 'It is a quarter past six.', 'Sagat altydan çärýek.', 'A1', 'a quarter past'),
    ('time', '/taɪm/', 'N', 'wagt, sagat', 'время', 'what you measure in minutes and hours', 'What time is it?', 'Sagat näçe?', 'A1', 'what time'),
    ('tired', '/ˈtaɪəd/', 'ADJ', 'ýadaw', 'усталый', 'needing sleep or rest', 'I am tired after work.', 'Işden soň ýadaw.', 'A1', 'feel tired'),
    ('hungry', '/ˈhʌŋɡri/', 'ADJ', 'aç', 'голодный', 'wanting to eat', 'I am hungry after work.', 'Işden soň aç.', 'A1', 'feel hungry'),
    ('thirsty', '/ˈθɜːsti/', 'ADJ', 'suwsuz', 'испытывающий жажду', 'wanting to drink', 'She is thirsty after the game.', 'Oýundan soň suwsady.', 'A1', 'feel thirsty'),
    ('happy', '/ˈhæpi/', 'ADJ', 'şat, bagtly', 'счастливый', 'feeling pleasure', 'I am happy today.', 'Bu gün şat.', 'A1', 'feel happy'),
    ('sad', '/sæd/', 'ADJ', 'gamgyn', 'грустный', 'feeling unhappy', 'He looks sad.', 'Ol gamgyn görünýär.', 'A1', 'feel sad'),
    ('cold (feel)', '/kəʊld/', 'ADJ', 'üşeýän', 'озябший', 'feeling low temperature on your body', 'I am cold, close the window.', 'Üşeýärin, penjiräni ýap.', 'A1', 'feel cold'),
    ('hot (feel)', '/hɒt/', 'ADJ', 'yssy', 'жарко', 'feeling high temperature on your body', 'It is hot in this room.', 'Bu otagda yssy.', 'A1', 'feel hot'),
])

L['4A'] = (4, 'Meet the family', 'people and family', [
    ('husband', '/ˈhʌzbənd/', 'N', 'äri, adamsy', 'муж', 'the man a woman is married to', 'Her husband is a doctor.', 'Adamsy lukman.', 'A1'),
    ('wife', '/waɪf/', 'N', 'aýaly', 'жена', 'the woman a man is married to', 'His wife is a teacher.', 'Aýaly mugallym.', 'A1'),
    ('daughter', '/ˈdɔːtə/', 'N', 'gyz', 'дочь', 'a person\'s female child', 'They have one daughter.', 'Olaryň bir gyzy bar.', 'A1'),
    ('son', '/sʌn/', 'N', 'ogul', 'сын', 'a person\'s male child', 'Their son is at school.', 'Ogly mekdepde.', 'A1'),
    ('girlfriend', '/ˈɡɜːlfrend/', 'N', 'gyz dosty', 'девушка', 'a woman someone has a romantic relationship with', 'His girlfriend is Italian.', 'Gyz dosty italýan.', 'A1'),
    ('boyfriend', '/ˈbɔɪfrend/', 'N', 'oglan dosty', 'парень', 'a man someone has a romantic relationship with', 'Her boyfriend is from Turkey.', 'Oglan dosty Türkiýeden.', 'A1'),
    ('parents', '/ˈpeərənts/', 'N', 'ene-ata', 'родители', 'your mother and father', 'My parents live in Ashgabat.', 'Ene-atam Aşgabatda ýaşaýar.', 'A1'),
    ('grandmother', '/ˈɡrænmʌðə/', 'N', 'ene, mama', 'бабушка', 'the mother of your mother or father', 'My grandmother is eighty.', 'Enem segsen ýaşynda.', 'A1'),
    ('grandfather', '/ˈɡrænfɑːðə/', 'N', 'ata', 'дедушка', 'the father of your mother or father', 'My grandfather works in the garden.', 'Atam bagda işleýär.', 'A1'),
    ('grandparents', '/ˈɡrænpeərənts/', 'N', 'ene-ata (uly)', 'дедушка и бабушка', 'the parents of your mother or father', 'We visit our grandparents on Sunday.', 'Ýekşenbe uly ene-atamyza barýarys.', 'A1'),
    ('people', '/ˈpiːpl/', 'N', 'adamlar', 'люди', 'men, women and children in general', 'Many people come here.', 'Bu ýere köp adam gelýär.', 'A1'),
    ('children', '/ˈtʃɪldrən/', 'N', 'çagalar', 'дети', 'young boys and girls', 'The children are at school.', 'Çagalar mekdepde.', 'A1'),
    ('men', '/men/', 'N', 'erkekler', 'мужчины', 'adult male people', 'Two men are waiting outside.', 'Iki erkek daşarda garaşýar.', 'A1'),
    ('women', '/ˈwɪmɪn/', 'N', 'aýallar', 'женщины', 'adult female people', 'The women work in a hospital.', 'Aýallar hassahanada işleýär.', 'A1'),
    ('aunt', '/ɑːnt/', 'N', 'bibi, eje', 'тётя', 'the sister of your mother or father', 'My aunt lives in Turkey.', 'Bibim Türkiýede ýaşaýar.', 'A1'),
    ('uncle', '/ˈʌŋkl/', 'N', 'dayy, aga', 'дядя', 'the brother of your mother or father', 'My uncle is a taxi driver.', 'Dayym taksi sürüjisi.', 'A1'),
    ('cousin', '/ˈkʌzn/', 'N', 'dogan (bibi/daýy çagasy)', 'двоюродный брат/сестра', 'the child of your aunt or uncle', 'My cousin is the same age as me.', 'Doganym meniň ýaşymda.', 'A1'),
    ('your', '/jɔː/', 'DET', 'seniň, siziň', 'твой, ваш', 'belonging to the person you are speaking to', 'What\'s your name?', 'Adyňyz näme?', 'A1'),
    ('my', '/maɪ/', 'DET', 'meniň', 'мой', 'belonging to me', 'This is my book.', 'Bu meniň kitabym.', 'A1'),
    ('his', '/hɪz/', 'DET', 'onuň (erkek)', 'его', 'belonging to a man or boy', 'His car is red.', 'Onuň maşyny gyzyl.', 'A1'),
    ('her', '/hɜː/', 'DET', 'onuň (aýal)', 'её', 'belonging to a woman or girl', 'Her name is Aýna.', 'Onuň ady Aýna.', 'A1'),
    # ── added round 11: 4A "People and family" photocopiable word bank,
    # TG p.214 — "boy children friends girl man men woman women" and
    # "boyfriend brother daughter father girlfriend … mother parents sister
    # son wife". These core family words were missing from the OCR import. ──
    ('boy', '/bɔɪ/', 'N', 'oglan', 'мальчик', 'a male child or young man', 'The boy is ten years old.', 'Oglan on ýaşynda.', 'A1'),
    ('girl', '/ɡɜːl/', 'N', 'gyz', 'девочка', 'a female child or young woman', 'The girl is my sister.', 'Gyz meniň uýam.', 'A1'),
    ('man', '/mæn/', 'N', 'erkek adam', 'мужчина', 'an adult male person (plural: men)', 'The man is my father.', 'Erkek adam meniň kakam.', 'A1'),
    ('woman', '/ˈwʊmən/', 'N', 'aýal', 'женщина', 'an adult female person (plural: women)', 'The woman is a doctor.', 'Aýal lukman.', 'A1'),
    ('brother', '/ˈbrʌðə/', 'N', 'dogan (aka, ini)', 'брат', 'a boy or man who has the same parents as you', 'This is my brother, Ryan.', 'Bu meniň doganym Raýan.', 'A1'),
    ('sister', '/ˈsɪstə/', 'N', 'uýa, siňil', 'сестра', 'a girl or woman who has the same parents as you', "Brenda is Ryan's sister.", 'Brenda Raýanyň uýasy.', 'A1'),
    ('father', '/ˈfɑːðə/', 'N', 'kaka, ata', 'отец', 'your male parent', 'My father is a teacher.', 'Kakam mugallym.', 'A1'),
    ('mother', '/ˈmʌðə/', 'N', 'eje, ene', 'мать', 'your female parent', 'Her mother is a doctor.', 'Onuň ejesi lukman.', 'A1'),
    ('friend', '/frend/', 'N', 'dost', 'друг', 'a person you like and spend time with', 'Bob and Rita are friends.', 'Bob we Rita dostlar.', 'A1'),
])

L['4B'] = (4, 'The perfect car', 'colours · common adjectives', [
    ('black', '/blæk/', 'ADJ', 'gara', 'чёрный', 'the darkest colour', 'He drives a black car.', 'Ol gara maşyn sürýär.', 'A1'),
    ('blue', '/bluː/', 'ADJ', 'gök', 'синий', 'the colour of a clear sky', 'The sky is blue.', 'Asman gök.', 'A1'),
    ('brown', '/braʊn/', 'ADJ', 'goňur', 'коричневый', 'the colour of earth or wood', 'She has brown eyes.', 'Onuň gözleri goňur.', 'A1'),
    ('green', '/ɡriːn/', 'ADJ', 'ýaşyl', 'зелёный', 'the colour of grass', 'The car is green.', 'Maşyn ýaşyl.', 'A1'),
    ('orange', '/ˈɒrɪndʒ/', 'ADJ', 'mämişi', 'оранжевый', 'the colour between red and yellow', 'I like the orange one.', 'Mämişi bolanyny halaýaryn.', 'A1'),
    ('white', '/waɪt/', 'ADJ', 'ak', 'белый', 'the colour of snow', 'The walls are white.', 'Diwarlar ak.', 'A1'),
    ('yellow', '/ˈjeləʊ/', 'ADJ', 'sary', 'жёлтый', 'the colour of the sun', 'She has a yellow bag.', 'Onuň sary sumkasy bar.', 'A1'),
    ('red', '/red/', 'ADJ', 'gyzyl', 'красный', 'the colour of blood', 'Stop at the red light.', 'Gyzyl çyrada duruň.', 'A1'),
    ('beautiful', '/ˈbjuːtɪfl/', 'ADJ', 'owadan', 'красивый', 'very pleasing to look at', 'What a beautiful view!', 'Nähili owadan görnüş!', 'A1'),
    ('dirty', '/ˈdɜːti/', 'ADJ', 'hapa, kirli', 'грязный', 'not clean', 'My hands are dirty.', 'Ellerim hapa.', 'A1'),
    ('easy', '/ˈiːzi/', 'ADJ', 'aňsat', 'лёгкий', 'not difficult', 'This exercise is easy.', 'Bu maşk aňsat.', 'A1'),
    ('difficult', '/ˈdɪfɪkəlt/', 'ADJ', 'kyn', 'трудный', 'not easy', 'English spelling is difficult.', 'Iňlis ýazuwy kyn.', 'A1'),
    ('old', '/əʊld/', 'ADJ', 'köne, garry', 'старый', 'not new, or having lived a long time', 'This is an old building.', 'Bu köne bina.', 'A1'),
    ('new', '/njuː/', 'ADJ', 'täze', 'новый', 'recently made or bought', 'I have a new phone.', 'Täze telefonum bar.', 'A1'),
    ('big', '/bɪɡ/', 'ADJ', 'uly', 'большой', 'large in size', 'They live in a big flat.', 'Olar uly öýde ýaşaýar.', 'A1'),
    ('small', '/smɔːl/', 'ADJ', 'kiçi', 'маленький', 'not big in size', 'I want a small table.', 'Kiçi stol isleýärin.', 'A1'),
    ('hot', '/hɒt/', 'ADJ', 'yssy, gyzgyn', 'горячий', 'having a high temperature', 'Be careful, the soup is hot.', 'Ünsli boluň, çorba gyzgyn.', 'A1'),
    ('cold', '/kəʊld/', 'ADJ', 'sowuk', 'холодный', 'having a low temperature', 'The water is cold.', 'Suw sowuk.', 'A1'),
    ('fast', '/fɑːst/', 'ADJ', 'çalt, tiz', 'быстрый', 'moving quickly', 'That is a fast car.', 'Ol çalt maşyn.', 'A1'),
    ('slow', '/sləʊ/', 'ADJ', 'haýal', 'медленный', 'not fast', 'The bus is slow today.', 'Bu gün awtobus haýal.', 'A1'),
    ('good', '/ɡʊd/', 'ADJ', 'gowy, oňat', 'хороший', 'of a high standard', 'This is a good book.', 'Bu gowy kitap.', 'A1'),
    ('bad', '/bæd/', 'ADJ', 'erbet, ýaman', 'плохой', 'not good', 'The weather is bad.', 'Howa erbet.', 'A1'),
    ('great', '/ɡreɪt/', 'ADJ', 'ajaýyp', 'отличный', 'very good', 'We had a great time.', 'Ajaýyp wagt geçirdik.', 'A1'),
    ('terrible', '/ˈterəbl/', 'ADJ', 'elhenç', 'ужасный', 'very bad', 'The traffic is terrible.', 'Ýol hereketi elhenç.', 'A1'),
    ('ugly', '/ˈʌɡli/', 'ADJ', 'ýakymsyz', 'некрасивый', 'not attractive to look at', 'That is an ugly hat.', 'Ol ýakymsyz telpek.', 'A1'),
    # ── added round 11: TG p.50 "elicit good-looking, which Sts saw in 2B,
    # … it is used for both men and women" ──
    ('good-looking', '/ˌɡʊd ˈlʊkɪŋ/', 'ADJ', 'görmegeý, owadan', 'красивый, привлекательный', 'attractive; used for both men and women', 'The actor is very good-looking.', 'Aktor gaty görmegeý.', 'A1'),
])

L['5A'] = (5, 'A big breakfast?', 'food and drink', [
    ('cereal', '/ˈsɪəriəl/', 'N', 'düýi dänesi, gury ertirlik', 'хлопья', 'a breakfast food made from grain, eaten with milk', 'I have cereal for breakfast.', 'Ertirlikde gury ertirlik iýýärin.', 'A1', 'a bowl of cereal'),
    ('eggs', '/eɡz/', 'N', 'ýumurtga', 'яйца', 'round white or brown food laid by hens', 'Two eggs, please.', 'Iki ýumurtga, haýyş.', 'A1', 'boiled eggs'),
    ('pasta', '/ˈpæstə/', 'N', 'makaron', 'паста', 'an Italian food made from flour and water', 'We eat pasta on Friday.', 'Anna güni makaron iýýäris.', 'A1'),
    ('salad', '/ˈsæləd/', 'N', 'salat', 'салат', 'a dish of raw vegetables', 'A green salad, please.', 'Ýaşyl salat, haýyş.', 'A1'),
    ('fruit', '/fruːt/', 'N', 'miwe', 'фрукты', 'sweet food that grows on trees or plants', 'Eat more fruit.', 'Köpräk miwe iýiň.', 'A1', 'fresh fruit'),
    ('butter', '/ˈbʌtə/', 'N', 'ýag', 'сливочное масло', 'a soft yellow food made from cream', 'Bread and butter, please.', 'Çörek we ýag, haýyş.', 'A1'),
    ('cheese', '/tʃiːz/', 'N', 'peýnir', 'сыр', 'a solid food made from milk', 'I like cheese on bread.', 'Çörekde peýniri halaýaryn.', 'A1'),
    ('chicken', '/ˈtʃɪkɪn/', 'N', 'towuk', 'курица', 'meat from a bird, or the bird itself', 'We had chicken for dinner.', 'Agşamlyga towuk iýdik.', 'A1'),
    ('meat', '/miːt/', 'N', 'et', 'мясо', 'the flesh of animals eaten as food', 'He does not eat meat.', 'Ol et iýmeýär.', 'A1'),
    ('fish', '/fɪʃ/', 'N', 'balyk', 'рыба', 'an animal that lives in water, eaten as food', 'Fresh fish is good for you.', 'Täze balyk peýdaly.', 'A1'),
    ('rice', '/raɪs/', 'N', 'tüwi', 'рис', 'small white or brown grains cooked and eaten', 'Rice with meat, please.', 'Et bilen tüwi, haýyş.', 'A1', 'a plate of rice'),
    ('potatoes', '/pəˈteɪtəʊz/', 'N', 'ýeralma', 'картофель', 'round brown vegetables that grow underground', 'I like boiled potatoes.', 'Gaýnadylan ýeralmany halaýaryn.', 'A1'),
    ('sugar', '/ˈʃʊɡə/', 'N', 'şeker', 'сахар', 'a sweet white substance you put in tea', 'No sugar for me, thanks.', 'Maňa şekersiz, sag boluň.', 'A1', 'a spoon of sugar'),
    ('chocolate', '/ˈtʃɒklət/', 'N', 'şokolad', 'шоколад', 'a sweet brown food made from cocoa', 'I love chocolate.', 'Şokolady gowy görýärin.', 'A1', 'a bar of chocolate'),
    ('tea', '/tiː/', 'N', 'çaý', 'чай', 'a hot drink made with leaves and water', 'Would you like some tea?', 'Çaý isleýärsiňizmi?', 'A1', 'a cup of tea'),
    ('coffee', '/ˈkɒfi/', 'N', 'kofe', 'кофе', 'a hot dark drink made from beans', 'A cappuccino, please.', 'Bir kapuçino, haýyş.', 'A1', 'a cup of coffee'),
    ('milk', '/mɪlk/', 'N', 'süýt', 'молоко', 'a white drink that comes from cows', 'Milk in my tea, please.', 'Çaýyma süýt, haýyş.', 'A1', 'a glass of milk'),
    ('orange juice', '/ˈɒrɪndʒ dʒuːs/', 'N', 'pytykal suwy', 'апельсиновый сок', 'a drink made from oranges', 'Orange juice for breakfast.', 'Ertirlik pytykal suwy.', 'A1'),
    ('mineral water', '/ˈmɪnərəl wɔːtə/', 'N', 'mineral suw', 'минеральная вода', 'natural water from underground', 'A bottle of mineral water, please.', 'Bir çüýşe mineral suw, haýyş.', 'A1'),
    ('wine', '/waɪn/', 'N', 'çakyr', 'вино', 'an alcoholic drink made from grapes', 'They ordered red wine.', 'Gyzyl çakyr sargyt etdiler.', 'A1', 'a glass of wine'),
    ('beer', '/bɪə/', 'N', 'piwo', 'пиво', 'an alcoholic drink made from grain', 'Two beers, please.', 'Iki piwo, haýyş.', 'A1'),
    ('breakfast', '/ˈbrekfəst/', 'N', 'ertirlik', 'завтрак', 'the first meal of the day', 'Breakfast is at seven.', 'Ertirlik sagat ýedide.', 'A1', 'have breakfast'),
    ('lunch', '/lʌntʃ/', 'N', 'günortanlyk', 'обед', 'the meal you eat in the middle of the day', 'We have lunch at one.', 'Günortanlyk sagat birde.', 'A1', 'have lunch'),
    ('dinner', '/ˈdɪnə/', 'N', 'agşamlyk', 'ужин', 'the main meal of the day, eaten in the evening', 'Dinner is ready!', 'Agşamlyk taýýar!', 'A1', 'have dinner'),
    ('eat', '/iːt/', 'V', 'iýmek', 'есть', 'to put food in your mouth and swallow it', 'I eat breakfast at seven.', 'Sagat ýedide ertirlik iýýärin.', 'A1'),
    ('drink', '/drɪŋk/', 'V', 'içmek', 'пить', 'to swallow liquid', 'I drink tea every morning.', 'Her irden çaý içýärin.', 'A1', 'drink water'),
    ('have (food)', '/hæv/', 'V', 'iýmek, içmek', 'есть, пить', 'used for eating or drinking something', 'I had a coffee.', 'Bir kofe içdim.', 'A1', 'have breakfast'),
    # ── added round 11: 5A key, TG p.55 ("2 milk 3 fruit 4 yogurt …") ──
    ('yogurt', '/ˈjɒɡət/', 'N', 'gatyk', 'йогурт', 'a soft sour food made from milk (also spelled yoghurt)', 'I have yogurt and fruit for breakfast.', 'Men ertirlikde gatyk we miýe iýýärin.', 'A1'),
])

L['5B'] = (5, 'A very long flight', 'common verb phrases 1', [
    ('live', '/lɪv/', 'V', 'ýaşamak', 'жить', 'to have your home in a place', 'I live in Ashgabat.', 'Aşgabatda ýaşaýaryn.', 'A1', 'live in'),
    ('flat', '/flæt/', 'N', 'öý, kwartira', 'квартира', 'a set of rooms to live in inside a building', 'They live in a small flat.', 'Olar kiçi kwartirada ýaşaýar.', 'A1', 'live in a flat'),
    ('cook', '/kʊk/', 'V', 'nahar bişirmek', 'готовить', 'to make food with heat', 'My father cooks dinner.', 'Kakam agşamlyk bişirýär.', 'A1', 'cook dinner'),
    ('study', '/ˈstʌdi/', 'V', 'okamak, öwrenmek', 'учиться', 'to spend time learning about a subject', 'I study English every day.', 'Her gün iňlis öwrenýärin.', 'A1', 'study English'),
    ('work (v.)', '/wɜːk/', 'V', 'işlemek', 'работать', 'to do a job', 'She works in a hotel.', 'Ol myhmanhanada işleýär.', 'A1', 'work in'),
    ('need', '/niːd/', 'V', 'zerur bolmak', 'нуждаться', 'to require something', 'I need a new phone.', 'Maňa täze telefon gerek.', 'A1', 'need to'),
    ('go to bed', '/ɡəʊ tə bed/', 'PHR', 'ýatmak', 'ложиться спать', 'to get into bed to sleep', 'I go to bed at eleven.', 'Sagat on birde ýatýaryn.', 'A1'),
    ('go to school', '/ɡəʊ tə skuːl/', 'PHR', 'mektbe gitmek', 'ходить в школу', 'to travel to school to learn', 'Children go to school at eight.', 'Çagalar sagat sekizde mektbe gidýär.', 'A1'),
    ('go to university', '/ɡəʊ tə ˌjuːnɪˈvɜːsəti/', 'PHR', 'uniwersitete gitmek', 'поступить в университет', 'to study at a university', 'She goes to university in Ashgabat.', 'Aşgabatda uniwersitete gidýär.', 'A1'),
    ('get up', '/ɡet ʌp/', 'PHR', 'turmak', 'вставать', 'to get out of bed', 'I get up at six.', 'Sagat altyda turýaryn.', 'A1'),
    ('play', '/pleɪ/', 'V', 'oýnamak', 'играть', 'to do a game or sport for fun', 'They play football on Sunday.', 'Ýekşenbe futbol oýnaýarlar.', 'A1', 'play football'),
    ('watch', '/wɒtʃ/', 'V', 'seretmek, tomaşa etmek', 'смотреть', 'to look at something for a time', 'We watch TV in the evening.', 'Agşam telewizora seredýäris.', 'A1', 'watch TV'),
    ('listen to', '/ˈlɪsn tuː/', 'PHR', 'diňlemek', 'слушать', 'to pay attention to a sound', 'I listen to music at work.', 'Işde saz diňleýärin.', 'A1', 'listen to music'),
    ('read', '/riːd/', 'V', 'okamak', 'читать', 'to look at words and understand them', 'She reads the newspaper.', 'Ol gazet okaýar.', 'A1', 'read a book'),
])

L['5C'] = (13, 'Practical English 3 · telling the time', 'the time · saying how you feel', [
    ('early', '/ˈɜːli/', 'ADV', 'irden, ir', 'рано', 'before the usual or expected time', 'I get up early.', 'Ir turýaryn.', 'A1', 'get up early'),
    ('late', '/leɪt/', 'ADV', 'giç', 'поздно', 'after the usual or expected time', 'He comes home late.', 'Öýe giç gelýär.', 'A1', 'come home late'),
    ('busy', '/ˈbɪzi/', 'ADJ', 'meşgul', 'занятой', 'having a lot to do', 'I am busy on Monday.', 'Duşenbe meşgul.', 'A1', 'be busy'),
    ('free', '/friː/', 'ADJ', 'boş', 'свободный', 'not busy', 'Are you free this evening?', 'Bu agşam boşmy?', 'A1', 'be free'),
    ('bored', '/bɔːd/', 'ADJ', 'güýmenjesiz, darýan', 'скучающий', 'unhappy because nothing is interesting', 'I am bored at home.', 'Öýde darýar.', 'A1', 'feel bored'),
    ('ill', '/ɪl/', 'ADJ', 'näsag', 'больной', 'not well, sick', 'He is ill today.', 'Ol bu gün näsag.', 'A1', 'feel ill'),
])

L['6A'] = (6, 'A school reunion', 'jobs and places of work', [
    ('doctor', '/ˈdɒktə/', 'N', 'lukman', 'врач', 'a person whose job is to treat sick people', 'My mother is a doctor.', 'Enem lukman.', 'A1'),
    ('nurse', '/nɜːs/', 'N', 'şepagat uýasy', 'медсестра', 'a person who looks after sick people', 'The nurse helps the doctor.', 'Şepagat uýasy lukmana kömek edýär.', 'A1'),
    ('waiter', '/ˈweɪtə/', 'N', 'ofisiant', 'официант', 'a man who brings food in a restaurant', 'The waiter brings the menu.', 'Ofisiant menýuny getirýär.', 'A1'),
    ('waitress', '/ˈweɪtrəs/', 'N', 'ofisiantka', 'официантка', 'a woman who brings food in a restaurant', 'The waitress is very friendly.', 'Ofisiantka gaty mähirli.', 'A1'),
    ('policeman', '/pəˈliːsmən/', 'N', 'polisiýa işgäri', 'полицейский', 'a man whose job is to stop crime', 'The policeman stops the car.', 'Polisiýa işgäri maşyny saklaýar.', 'A1'),
    ('policewoman', '/pəˈliːswʊmən/', 'N', 'polisiýa işgäri (aýal)', 'полицейская', 'a woman whose job is to stop crime', 'She wants to be a policewoman.', 'Ol polisiýa işgäri bolmak isleýär.', 'A1'),
    ('shop assistant', '/ʃɒp əˈsɪstənt/', 'N', 'dükan satyjysy', 'продавец', 'a person who serves customers in a shop', 'The shop assistant helps me.', 'Satyjy maňa kömek edýär.', 'A1'),
    ('receptionist', '/rɪˈsepʃənɪst/', 'N', 'resepsiýa işgäri', 'администратор', 'a person who welcomes guests in a hotel or office', 'The receptionist gives you the key.', 'Resepsiýa işgäri açary berýär.', 'A1'),
    ('factory worker', '/ˈfæktri ˈwɜːkə/', 'N', 'zawod işçisi', 'рабочий завода', 'a person who works in a factory', 'He is a factory worker.', 'Ol zawod işçisi.', 'A1'),
    ('taxi driver', '/ˈtæksi ˈdraɪvə/', 'N', 'taksi sürüjisi', 'таксист', 'a person who drives a taxi', 'The taxi driver knows the city.', 'Taksi sürüjisi şäheri bilýär.', 'A1'),
    ('hospital', '/ˈhɒspɪtl/', 'N', 'hassahana', 'больница', 'a building where sick people are treated', 'She works in a hospital.', 'Ol hassahanada işleýär.', 'A1', 'in hospital'),
    ('restaurant', '/ˈrestrɒnt/', 'N', 'restoran', 'ресторан', 'a place where you buy and eat meals', 'We eat at a restaurant on Sunday.', 'Ýekşenbe restoranda iýýäris.', 'A1', 'at a restaurant'),
    ('office', '/ˈɒfɪs/', 'N', 'edara', 'офис', 'a room or building where people work at desks', 'He works in an office.', 'Ol edarada işleýär.', 'A1', 'in an office'),
    ('hotel', '/həʊˈtel/', 'N', 'myhmanhana', 'гостиница', 'a building where you pay to sleep', 'The hotel is near the beach.', 'Myhmanhana deňziň ýanynda.', 'A1', 'stay at a hotel'),
    ('unemployed', '/ˌʌnɪmˈplɔɪd/', 'ADJ', 'işsiz', 'безработный', 'not having a job', 'He is unemployed at the moment.', 'Ol häzir işsiz.', 'A1'),
    ('retired', '/rɪˈtaɪəd/', 'ADJ', 'pensiýada', 'на пенсии', 'having stopped working because of age', 'My grandfather is retired.', 'Atam pensiýada.', 'A1'),
    ('university', '/ˌjuːnɪˈvɜːsəti/', 'N', 'uniwersitet', 'университет', 'a place where students study after school', 'She studies at university.', 'Ol uniwersitetde okaýar.', 'A1', 'at university'),
    ('teacher', '/ˈtiːtʃə/', 'N', 'mugallym', 'учитель', 'a person whose job is to teach', 'Our teacher is very kind.', 'Mugallymymyz gaty mähirli.', 'A1'),
    ('student', '/ˈstjuːdnt/', 'N', 'okuwçy, talyp', 'студент', 'a person who studies at a school or university', 'I am a student.', 'Men okuwçy.', 'A1'),
])

L['6B'] = (6, 'Good morning, goodnight', 'a typical day', [
    ('have a shower', '/hæv ə ˈʃaʊə/', 'PHR', 'duş almak', 'принимать душ', 'to wash your whole body under a shower', 'I have a shower every morning.', 'Her irden duş alýaryn.', 'A1'),
    ('have a coffee', '/hæv ə ˈkɒfi/', 'PHR', 'kofe içmek', 'выпить кофе', 'to drink a cup of coffee', 'Let\'s have a coffee.', 'Geliň kofe içeliň.', 'A1'),
    ('go to work', '/ɡəʊ tə wɜːk/', 'PHR', 'işe gitmek', 'идти на работу', 'to travel to the place where you work', 'She goes to work by bus.', 'Işe awtobusda gidýär.', 'A1'),
    ('finish work', '/ˈfɪnɪʃ wɜːk/', 'PHR', 'işi gutarmak', 'закончить работу', 'to stop working at the end of the day', 'I finish work at six.', 'Sagat altyda işi gutarýaryn.', 'A1'),
    ('go home', '/ɡəʊ həʊm/', 'PHR', 'öýe gitmek', 'идти домой', 'to travel to the place where you live', 'We go home together.', 'Öýe bile gidýäris.', 'A1'),
    ('go shopping', '/ɡəʊ ˈʃɒpɪŋ/', 'PHR', 'bazara gitmek', 'ходить за покупками', 'to go out to buy things', 'They go shopping on Saturday.', 'Şenbe bazara gidýärler.', 'A1'),
    ('go to the gym', '/ɡəʊ tə ðə dʒɪm/', 'PHR', 'sport zalyna gitmek', 'ходить в спортзал', 'to go to a place to exercise', 'He goes to the gym twice a week.', 'Hepdede iki gezek sport zalyna gidýär.', 'A1'),
    ('make dinner', '/meɪk ˈdɪnə/', 'PHR', 'agşamlyk taýýarlamak', 'готовить ужин', 'to prepare the evening meal', 'My mother makes dinner.', 'Enem agşamlyk taýýarlaýar.', 'A1'),
    ('do housework', '/duː ˈhaʊswɜːk/', 'PHR', 'öý işlerini etmek', 'заниматься домашней работой', 'to clean and tidy your home', 'I do housework on Sunday.', 'Ýekşenbe öý işlerini edýärin.', 'A1'),
    ('have a bath', '/hæv ə bɑːθ/', 'PHR', 'wanna almak', 'принимать ванну', 'to wash your body in a bath', 'She has a bath at night.', 'Gije wanna alýar.', 'A1'),
    ('always', '/ˈɔːlweɪz/', 'ADV', 'elmydama', 'всегда', 'every time, without exception', 'I always drink tea.', 'Elmydama çaý içýärin.', 'A1'),
    ('usually', '/ˈjuːʒuəli/', 'ADV', 'adatça', 'обычно', 'in most cases', 'I usually get up at seven.', 'Adatça sagat ýedide turýaryn.', 'A1'),
    ('sometimes', '/ˈsʌmtaɪmz/', 'ADV', 'käwagt', 'иногда', 'on some occasions', 'Sometimes I walk to work.', 'Käwagt işe ýöräp barýaryn.', 'A1'),
    ('never', '/ˈnevə/', 'ADV', 'hiç haçan', 'никогда', 'not at any time', 'I never drink coffee at night.', 'Gije hiç haçan kofe içmeýärin.', 'A1'),
])

L['7A'] = (7, 'Have a nice weekend!', 'common verb phrases 2 · free time', [
    ('go out', '/ɡəʊ aʊt/', 'PHR', 'çykmak, gezme gitmek', 'выходить', 'to leave your home to do something pleasant', 'We go out on Friday.', 'Anna güni gezme gidýäris.', 'A1'),
    ('go to the cinema', '/ɡəʊ tə ðə ˈsɪnəmə/', 'PHR', 'kino gitmek', 'ходить в кино', 'to go and watch a film at a cinema', 'They go to the cinema every month.', 'Her aý kino gidýärler.', 'A1'),
    ('go to the beach', '/ɡəʊ tə ðə biːtʃ/', 'PHR', 'deňiz kenaryna gitmek', 'ходить на пляж', 'to go to the sand by the sea', 'We go to the beach in summer.', 'Tomusda deňiz kenaryna gidýäris.', 'A1'),
    ('play tennis', '/pleɪ ˈtenɪs/', 'PHR', 'tennis oýnamak', 'играть в теннис', 'to play the sport of tennis', 'She plays tennis on Saturday.', 'Şenbe tennis oýnaýar.', 'A1'),
    ('play computer games', '/pleɪ kəmˈpjuːtə ɡeɪmz/', 'PHR', 'kompýuter oýny oýnamak', 'играть в компьютерные игры', 'to play games on a computer', 'My brother plays computer games.', 'Doganym kompýuter oýnuny oýnaýar.', 'A1'),
    ('stay at home', '/steɪ ət həʊm/', 'PHR', 'öýde galmak', 'оставаться дома', 'to not go out', 'I stay at home on Sunday.', 'Ýekşenbe öýde galýaryn.', 'A1'),
    ('meet friends', '/miːt frendz/', 'PHR', 'dostlar bilen duşuşmak', 'встречаться с друзьями', 'to see your friends', 'We meet friends at the weekend.', 'Hepde ahyrynda dostlar bilen duşuşýarys.', 'A1'),
    ('free time', '/friː taɪm/', 'N', 'boş wagt', 'свободное время', 'time when you are not working', 'What do you do in your free time?', 'Boş wagtyňyzda näme edýärsiňiz?', 'A1', 'in your free time'),
    ('weekend', '/ˌwiːkˈend/', 'N', 'hepde ahyry', 'выходные', 'Saturday and Sunday', 'Have a nice weekend!', 'Gowy hepde ahyry!', 'A1', 'at the weekend'),
    # ── added round 11: 7A worksheet word bank, TG p.220 ("relax"), and the
    # 7A vocabulary note, TG p.76 ("play + ball/racket sports, e.g. golf,
    # football, tennis") ──
    ('relax', '/rɪˈlæks/', 'V', 'dynç almak', 'отдыхать, расслабляться', 'to rest and do nothing difficult', 'At the weekend I relax at home.', 'Hepde ahyrynda öýde dynç alýaryn.', 'A1'),
    ('golf', '/ɡɒlf/', 'N', 'golf', 'гольф', 'a game where you hit a small ball into holes with clubs', 'He plays golf every Saturday.', 'Ol her şenbe güni golf oýnaýar.', 'A1', 'play golf'),
    ('football', '/ˈfʊtbɔːl/', 'N', 'futbol', 'футбол', 'a game where two teams kick a ball to score goals', 'We play football in the park.', 'Biz parkda futbol oýnaýarys.', 'A1', 'play football'),
])

L['7B'] = (7, 'Lights, camera, action!', 'kinds of films', [
    ('comedy', '/ˈkɒmədi/', 'N', 'komediýa', 'комедия', 'a film that makes you laugh', 'We watched a comedy.', 'Komediýa gördük.', 'A1', 'watch a comedy'),
    ('horror film', '/ˈhɒrə fɪlm/', 'N', 'gorror filmi', 'фильм ужасов', 'a film that frightens you', 'I do not like horror films.', 'Gorror filmlerini halamaýaryn.', 'A1'),
    ('action film', '/ˈækʃn fɪlm/', 'N', 'döwüş filmi', 'боевик', 'a film with a lot of exciting things happening', 'He likes action films.', 'Ol döwüş filmlerini halaýar.', 'A1'),
    ('film', '/fɪlm/', 'N', 'film', 'фильм', 'a story you watch on a screen', 'The film starts at eight.', 'Film sagat sekizde başlaýar.', 'A1', 'watch a film'),
    ('cinema', '/ˈsɪnəmə/', 'N', 'kino', 'кинотеатр', 'a building where you watch films', 'Let\'s go to the cinema.', 'Geliň kino gideliň.', 'A1', 'go to the cinema'),
    ('actor', '/ˈæktə/', 'N', 'aktýor', 'актёр', 'a person who acts in films or plays', 'She is a famous actor.', 'Ol meşhur aktýor.', 'A1'),
])

L['7C'] = (13, 'Practical English 4 · saying the date', 'months · ordinal numbers', [
    ('January', '/ˈdʒænjuəri/', 'N', 'ýanwar', 'январь', 'the first month of the year', 'My birthday is in January.', 'Doglan günim ýanwarda.', 'A1', 'in January'),
    ('February', '/ˈfebruəri/', 'N', 'fewral', 'февраль', 'the second month of the year', 'It is cold in February.', 'Fewralda sowuk bolýar.', 'A1', 'in February'),
    ('March', '/mɑːtʃ/', 'N', 'mart', 'март', 'the third month of the year', 'Spring starts in March.', 'Ýaz martda başlaýar.', 'A1', 'in March'),
    ('April', '/ˈeɪprəl/', 'N', 'aprel', 'апрель', 'the fourth month of the year', 'It rains a lot in April.', 'Aprelde köp ýagyş ýagýar.', 'A1', 'in April'),
    ('May', '/meɪ/', 'N', 'maý', 'май', 'the fifth month of the year', 'We travel in May.', 'Maýda syýahat edýäris.', 'A1', 'in May'),
    ('June', '/dʒuːn/', 'N', 'iýun', 'июнь', 'the sixth month of the year', 'School finishes in June.', 'Mekdep iýunda gutarýar.', 'A1', 'in June'),
    ('July', '/dʒuˈlaɪ/', 'N', 'iýul', 'июль', 'the seventh month of the year', 'July is very hot.', 'Iýul gaty yssy.', 'A1', 'in July'),
    ('August', '/ˈɔːɡəst/', 'N', 'awgust', 'август', 'the eighth month of the year', 'We go to the sea in August.', 'Awgustda deňze gidýäris.', 'A1', 'in August'),
    ('September', '/sepˈtembə/', 'N', 'sentýabr', 'сентябрь', 'the ninth month of the year', 'School starts in September.', 'Mekdep sentýabrda başlaýar.', 'A1', 'in September'),
    ('October', '/ɒkˈtəʊbə/', 'N', 'oktýabr', 'октябрь', 'the tenth month of the year', 'The leaves fall in October.', 'Oktýabrda ýapraklar gaçýar.', 'A1', 'in October'),
    ('November', '/nəʊˈvembə/', 'N', 'noýabr', 'ноябрь', 'the eleventh month of the year', 'It gets dark early in November.', 'Noýabrda ir garalýar.', 'A1', 'in November'),
    ('December', '/dɪˈsembə/', 'N', 'dekabr', 'декабрь', 'the twelfth month of the year', 'December is a winter month.', 'Dekabr gyş aýy.', 'A1', 'in December'),
    ('month', '/mʌnθ/', 'N', 'aý', 'месяц', 'one of the twelve parts of a year', 'This month is busy.', 'Bu aý meşgul.', 'A1', 'this month'),
    ('first', '/fɜːst/', 'ORD', 'birinji', 'первый', 'coming before all others', 'My birthday is on the first of May.', 'Doglan günim bäşiň birinji.', 'A1'),
    ('second', '/ˈsekənd/', 'ORD', 'ikinji', 'второй', 'coming after the first', 'My flat is on the second floor.', 'Kwartiram ikinji gatda.', 'A1', 'the second floor'),
    ('third', '/θɜːd/', 'ORD', 'üçünji', 'третий', 'coming after the second', 'He is third in the class.', 'Ol synpda üçünji.', 'A1'),
    ('date', '/deɪt/', 'N', 'sene', 'дата', 'the day, month and year of an event', 'What\'s the date today?', 'Bu gün nähili sene?', 'A1', "what's the date"),
])

L['8A'] = (8, 'Can I park here?', 'more verb phrases', [
    ('can', '/kæn/', 'V', 'bilemek, mümkin', 'мочь', 'used to say something is possible or allowed', 'Can I park here?', 'Bu ýerde durup bilerinmi?', 'A1', "can I"),
    ('park', '/pɑːk/', 'V', 'durmak, park etmek', 'парковать', 'to leave a car in a place for a time', 'You can\'t park here.', 'Bu ýerde durup bolmaýar.', 'A1', 'park the car'),
    ('take a photo', '/teɪk ə ˈfəʊtəʊ/', 'PHR', 'surat düşürmek', 'фотографировать', 'to make a picture with a camera', 'Can I take a photo?', 'Surat düşürip bilerinmi?', 'A1'),
    ('turn left', '/tɜːn left/', 'PHR', 'çepe öwrülmek', 'повернуть налево', 'to change direction to the left', 'Turn left at the corner.', 'Burçda çepe öwrüliň.', 'A1'),
    ('turn right', '/tɜːn raɪt/', 'PHR', 'saga öwrülmek', 'повернуть направо', 'to change direction to the right', 'Turn right after the hotel.', 'Myhmanhanadan soň saga öwrüliň.', 'A1'),
    ('go straight on', '/ɡəʊ streɪt ɒn/', 'PHR', 'göni gitmek', 'идти прямо', 'to continue in the same direction', 'Go straight on for two hundred metres.', 'Iki ýüz metr göni gidiň.', 'A1'),
    ('cross the road', '/krɒs ðə rəʊd/', 'PHR', 'ýoldan geçmek', 'перейти дорогу', 'to go from one side of a road to the other', 'Cross the road at the lights.', 'Ýoldan çyralarda geçiň.', 'A1'),
    ('ask for help', '/ɑːsk fɔː help/', 'PHR', 'kömek soramak', 'попросить помощи', 'to say you need help', 'Ask for help if you need it.', 'Gerek bolsa kömek soraň.', 'A1'),
    ('wait for', '/weɪt fɔː/', 'PHR', 'garamak', 'ждать', 'to stay until something happens', 'I wait for the bus.', 'Awtobusa garaşýaryn.', 'A1', 'wait for a bus'),
    ('get a taxi', '/ɡet ə ˈtæksi/', 'PHR', 'taksi tutmak', 'взять такси', 'to call a taxi and travel in it', 'We got a taxi to the hotel.', 'Myhmanhana taksi tutduk.', 'A1'),
    # ── added round 11: TG p.87 "Then teach driving licence and driving
    # test, and explain that you can pass or fail a test." ──
    ('driving licence', '/ˈdraɪvɪŋ ˌlaɪsns/', 'N', 'sürüjilik şahadatnamasy', 'водительские права', 'an official card that allows you to drive', 'He has a driving licence. He can drive a car.', 'Onuň sürüjilik şahadatnamasy bar. Ol maşyn sürüp bilýär.', 'A1'),
    ('driving test', '/ˈdraɪvɪŋ test/', 'N', 'sürüjilik synagy', 'экзамен по вождению', 'a test where you show you can drive a car', 'She passed her driving test.', 'Ol sürüjilik synagyndan geçdi.', 'A1', 'pass / fail a test'),
])

L['8B'] = (8, 'Do you like cooking?', 'activities', [
    ('go cycling', '/ɡəʊ ˈsaɪklɪŋ/', 'PHR', 'welosiped sürmek', 'кататься на велосипеде', 'to ride a bicycle for fun', 'We go cycling on Sunday.', 'Ýekşenbe welosiped sürýäris.', 'A1'),
    ('go running', '/ɡəʊ ˈrʌnɪŋ/', 'PHR', 'ylgamak', 'бегать', 'to run for exercise', 'He goes running every morning.', 'Her irden ylgamaga gidýär.', 'A1'),
    ('go swimming', '/ɡəʊ ˈswɪmɪŋ/', 'PHR', 'ýüzmek', 'плавать', 'to swim for fun or exercise', 'They go swimming in summer.', 'Tomusda ýüzmäge gidýärler.', 'A1'),
    ('go jogging', '/ɡəʊ ˈdʒɒɡɪŋ/', 'PHR', 'haýal ylgamak', 'бегать трусцой', 'to run slowly for exercise', 'She goes jogging in the park.', 'Parkda haýal ylgamaga gidýär.', 'A1'),
    ('go dancing', '/ɡəʊ ˈdɑːnsɪŋ/', 'PHR', 'tans etmäge gitmek', 'ходить танцевать', 'to go somewhere to dance', 'We go dancing on Friday.', 'Anna güni tans etmäge gidýäris.', 'A1'),
    ('go fishing', '/ɡəʊ ˈfɪʃɪŋ/', 'PHR', 'balyk tutmaga gitmek', 'ходить на рыбалку', 'to try to catch fish', 'My father goes fishing.', 'Kakam balyk tutmaga gidýär.', 'A1'),
    ('go for a walk', '/ɡəʊ fɔːr ə wɔːk/', 'PHR', 'aýlanmaga gitmek', 'идти на прогулку', 'to walk somewhere for pleasure', 'Let\'s go for a walk.', 'Geliň aýlanmaga gideliň.', 'A1'),
    ('go on a trip', '/ɡəʊ ɒn ə trɪp/', 'PHR', 'syýahata gitmek', 'поехать в поездку', 'to travel somewhere for pleasure', 'We went on a trip to the mountains.', 'Daglaryň ýanyna syýahata gitdik.', 'A1'),
    ('go to a party', '/ɡəʊ tə ə ˈpɑːti/', 'PHR', 'toýa/agşamlyk dabara gitmek', 'идти на вечеринку', 'to go to a social event', 'She goes to a party tonight.', 'Bu agşam toýa gidýär.', 'A1'),
    ('go to a concert', '/ɡəʊ tə ə ˈkɒnsət/', 'PHR', 'konserte gitmek', 'идти на концерт', 'to go to hear music played live', 'We went to a concert.', 'Konserte gitdik.', 'A1'),
    ('like', '/laɪk/', 'V', 'halamak', 'нравиться', 'to enjoy or approve of something', 'I like cooking.', 'Nahar bişirmegi halaýaryn.', 'A1', 'like doing'),
    ('love', '/lʌv/', 'V', 'gowy görmek, söýmek', 'любить', 'to like something very much', 'She loves music.', 'Ol sazy gowy görýär.', 'A1', 'love doing'),
    ('hate', '/heɪt/', 'V', 'ýigrenmek', 'ненавидеть', 'to dislike something very much', 'He hates getting up early.', 'Ir turmagy ýigrenýär.', 'A1', 'hate doing'),
])

L['9A'] = (9, "Everything's fine!", 'common verb phrases 2 · travelling', [
    ('take a train', '/teɪk ə treɪn/', 'PHR', 'otly bilen gitmek', 'ехать на поезде', 'to travel by train', 'We took a train to Istanbul.', 'Stambula otly bilen gitdik.', 'A1'),
    ('wait for a flight', '/weɪt fɔːr ə flaɪt/', 'PHR', 'uçuşa garamak', 'ждать рейс', 'to wait at an airport for your plane', 'We waited for the flight for two hours.', 'Uçuşa iki sagat garadyk.', 'A1'),
    ('rent a car', '/rent ə kɑː/', 'PHR', 'maşyn kärendesine almak', 'взять машину напрокат', 'to pay to use a car for a time', 'We rented a car in Italy.', 'Italiýada maşyn kärendesine aldyk.', 'A1'),
    ('arrive', '/əˈraɪv/', 'V', 'baryp ýetmek', 'прибывать', 'to reach a place', 'The train arrives at six.', 'Otly sagat altyda gelýär.', 'A1', 'arrive at'),
    ('buy presents', '/baɪ ˈpreznts/', 'PHR', 'sowgat satyn almak', 'покупать подарки', 'to get things to give to people', 'I need to buy presents.', 'Sowgat satyn almaly.', 'A1'),
    ('journey', '/ˈdʒɜːni/', 'N', 'ýolagçylyk, syýahat', 'путешествие', 'an act of travelling from one place to another', 'The journey takes three hours.', 'Ýol üç sagat dowam edýär.', 'A1', 'a long journey'),
    ('airport', '/ˈeəpɔːt/', 'N', 'howa menzili', 'аэропорт', 'a place where planes take off and land', 'The airport is far from the city.', 'Howa menzili şäherden uzak.', 'A1', 'at the airport'),
    ('station', '/ˈsteɪʃn/', 'N', 'beket, stansiýa', 'вокзал', 'a place where trains or buses stop', 'The train leaves from the station.', 'Otly stansiýadan gidýär.', 'A1', 'railway station'),
    ('ticket', '/ˈtɪkɪt/', 'N', 'bilet', 'билет', 'a piece of paper that allows you to travel or enter', 'I bought two tickets.', 'Iki bilet satyn aldym.', 'A1', 'buy a ticket'),
    ('luggage', '/ˈlʌɡɪdʒ/', 'N', 'ýük, bagaj', 'багаж', 'the bags you take when you travel', 'We have two pieces of luggage.', 'Iki sany bagažymyz bar.', 'A1', 'a piece of luggage'),
    ('holiday', '/ˈhɒlədeɪ/', 'N', 'dynç alyş', 'отпуск, каникулы', 'a time when you do not work or study', 'We are on holiday.', 'Dynç alyşda.', 'A1', 'on holiday'),
    # ── added round 11: 9A phrase-completion key, TG p.97 ("1 stay in a
    # hotel 2 do your homework 3 read a book …") ──
    ('homework', '/ˈhəʊmwɜːk/', 'N', 'öý işi', 'домашнее задание', 'work a teacher gives you to do at home', 'I do my homework after school.', 'Öý işimi mekdepden soň edýärin.', 'A1', 'do your homework'),
    ('stay in a hotel', '/steɪ ɪn ə həʊˈtel/', 'PHR', 'myhmanhanada galmak', 'остановиться в гостинице', 'to sleep in a hotel when you are away from home', 'We stay in a hotel on holiday.', 'Dynç alyşda myhmanhanada galýarys.', 'A1'),
])

L['9B'] = (9, 'Working undercover', 'clothes', [
    ('cap', '/kæp/', 'N', 'kepka', 'кепка', 'a soft hat with a part that sticks out in front', 'He wears a blue cap.', 'Gök kepka geýýär.', 'A1', 'wear a cap'),
    ('hat', '/hæt/', 'N', 'telpek, şlýapa', 'шляпа', 'something you wear on your head', 'Take off your hat.', 'Telpegiňi aýyr.', 'A1', 'wear a hat'),
    ('coat', '/kəʊt/', 'N', 'palto', 'пальто', 'a warm piece of clothing you wear outside', 'Put on your coat.', 'Paltoňy geý.', 'A1', 'wear a coat'),
    ('dress', '/dres/', 'N', 'köýnek', 'платье', 'a piece of clothing worn by women that covers the body and legs', 'She wears a red dress.', 'Gyzyl köýnek geýýär.', 'A1', 'wear a dress'),
    ('jacket', '/ˈdʒækɪt/', 'N', 'kurtka, penjek', 'куртка', 'a short coat', 'My jacket is black.', 'Kurtkam gara.', 'A1', 'wear a jacket'),
    ('jeans', '/dʒiːnz/', 'N', 'jinsi', 'джинсы', 'trousers made of strong blue cotton', 'He always wears jeans.', 'Elmydama jinsi geýýär.', 'A1', 'wear jeans'),
    ('shirt', '/ʃɜːt/', 'N', 'köýnekçek', 'рубашка', 'a piece of clothing for the top of your body with a collar', 'A white shirt, please.', 'Ak köýnekçek, haýyş.', 'A1', 'wear a shirt'),
    ('skirt', '/skɜːt/', 'N', 'ýubka', 'юбка', 'a piece of clothing worn by women from the waist down', 'She bought a long skirt.', 'Uzyn ýubka satyn aldy.', 'A1', 'wear a skirt'),
    ('socks', '/sɒks/', 'N', 'jorap', 'носки', 'soft clothing you wear on your feet inside shoes', 'I need new socks.', 'Täze jorap gerek.', 'A1', 'wear socks'),
    ('sweater', '/ˈswetə/', 'N', 'switer', 'свитер', 'a warm piece of clothing for the top of your body', 'Wear a sweater, it is cold.', 'Switer geý, sowuk.', 'A1', 'wear a sweater'),
    ('trainers', '/ˈtreɪnəz/', 'N', 'krosowka', 'кроссовки', 'soft shoes you wear for sport', 'My trainers are new.', 'Krosowkalarym täze.', 'A1', 'wear trainers'),
    ('shoes', '/ʃuːz/', 'N', 'aýakgap', 'туфли', 'things you wear on your feet', 'Take off your shoes.', 'Aýakgabyňyzy çykaryň.', 'A1', 'wear shoes'),
    ('trousers', '/ˈtraʊzəz/', 'N', 'balak', 'брюки', 'a piece of clothing that covers your legs', 'He wears black trousers.', 'Gara balak geýýär.', 'A1', 'wear trousers'),
    ('shorts', '/ʃɔːts/', 'N', 'şorty', 'шорты', 'short trousers that end above the knee', 'I wear shorts in summer.', 'Tomusda şorty geýýärin.', 'A1', 'wear shorts'),
    ('wear', '/weə/', 'V', 'geýmek', 'носить', 'to have clothing on your body', 'She wears a blue coat.', 'Gök palto geýýär.', 'A1', 'wear a coat'),
    # ── added round 11: 9B clothes key, TG p.102 ("1 a T-shirt 2 jeans 3 a
    # suit 4 a hat 5 a jacket"), and TG p.101 "elicit the manager … Model
    # and drill pronunciation of all the jobs" ──
    ('suit', '/suːt/', 'N', 'kostýum', 'костюм', 'a jacket and trousers made of the same material', 'He wears a suit to work.', 'Ol işe kostýum geýýär.', 'A1'),
    ('manager', '/ˈmænɪdʒə/', 'N', 'müdir', 'менеджер, управляющий', 'the person in charge of a hotel, shop or office', 'The manager of the hotel is very friendly.', 'Myhmanhananyň müdiri gaty mähirli.', 'A1'),
])

L['10A'] = (10, 'A room with a view', 'hotels · rooms · in / on / under', [
    ('bed', '/bed/', 'N', 'düşek, krowat', 'кровать', 'a piece of furniture you sleep on', 'The bed is very comfortable.', 'Düşek gaty amatly.', 'A1', 'go to bed'),
    ('double bed', '/ˈdʌbl bed/', 'N', 'goşa krowat', 'двуспальная кровать', 'a bed for two people', 'We want a double bed.', 'Goşa krowat isleýäris.', 'A1', 'a double bed'),
    ('pillow', '/ˈpɪləʊ/', 'N', 'ýassyk', 'подушка', 'a soft object you rest your head on in bed', 'I need another pillow.', 'Ýene bir ýassyk gerek.', 'A1'),
    ('blanket', '/ˈblæŋkɪt/', 'N', 'ýorgan', 'одеяло', 'a warm cover you use on a bed', 'The blanket is warm.', 'Ýorgan yssy.', 'A1'),
    ('lamp', '/læmp/', 'N', 'çyra', 'лампа', 'an object that gives light', 'There is a lamp on the table.', 'Stoluň üstünde çyra bar.', 'A1'),
    ('mirror', '/ˈmɪrə/', 'N', 'aýna', 'зеркало', 'glass that shows your face when you look at it', 'The mirror is on the wall.', 'Aýna diwarda.', 'A1'),
    ('cupboard', '/ˈkʌbəd/', 'N', 'şkaf', 'шкаф', 'a piece of furniture with doors, for keeping things in', 'Your clothes are in the cupboard.', 'Eşikleriň şkafda.', 'A1', 'in the cupboard'),
    ('towel', '/ˈtaʊəl/', 'N', 'polotensa, ulag', 'полотенце', 'a piece of cloth you use to dry yourself', 'Is there a towel in the room?', 'Otagda polotensa barmy?', 'A1'),
    ('shower', '/ˈʃaʊə/', 'N', 'duş', 'душ', 'a place where you wash under falling water', 'The room has a shower.', 'Otagda duş bar.', 'A1', 'have a shower'),
    ('bathroom', '/ˈbɑːθruːm/', 'N', 'hamam, ýuwunma otagy', 'ванная', 'a room with a bath, shower and toilet', 'The bathroom is small.', 'Ýuwunma otagy kiçi.', 'A1', 'in the bathroom'),
    ('reception', '/rɪˈsepʃn/', 'N', 'resepsiýa', 'стойка регистрации', 'the desk in a hotel where you check in', 'Leave the key at reception.', 'Açary resepsiýada goýuň.', 'A1', 'at reception'),
    ('lift', '/lɪft/', 'N', 'lift', 'лифт', 'a machine that carries people up and down', 'Take the lift to the third floor.', 'Üçünji gata lift bilen çykyň.', 'A1', 'take the lift'),
    ('view', '/vjuː/', 'N', 'görnüş', 'вид', 'what you can see from a place', 'The room has a lovely view.', 'Otagyň owadan görnüşi bar.', 'A1', 'a view of'),
    ('guest', '/ɡest/', 'N', 'myhman', 'гость', 'a person who stays in a hotel', 'The guests arrive at three.', 'Myhmanlar sagat üçde gelýär.', 'A1'),
    ('room', '/ruːm/', 'N', 'otag', 'комната', 'a part of a building with walls around it', 'My room is number twelve.', 'Otagym on iki.', 'A1', 'a double room'),
    ('in', '/ɪn/', 'PREP', 'içinde', 'в', 'inside something', 'The keys are in my bag.', 'Açarlar sumkamda.', 'A1'),
    ('on', '/ɒn/', 'PREP', 'üstünde', 'на', 'touching the top of something', 'The book is on the table.', 'Kitap stoluň üstünde.', 'A1'),
    ('under', '/ˈʌndə/', 'PREP', 'astynda', 'под', 'directly below something', 'The cat is under the bed.', 'Pişik düşegiň astynda.', 'A1'),
])

L['10B'] = (10, 'Where were you?', 'in / on / at (was · were)', [
    ('at', '/æt/', 'PREP', '-de, -da', 'в, у', 'used to say where someone or something is', 'She is at work.', 'Ol işde.', 'A1', 'at work'),
    ('was', '/wɒz/', 'V', 'boldy (bir adam)', 'был, была', 'the past form of "be" for I, he, she, it', 'I was at home yesterday.', 'Düýn öýde boldum.', 'A1'),
    ('were', '/wɜː/', 'V', 'boldy (köp)', 'были', 'the past form of "be" for you, we, they', 'They were at the cinema.', 'Olar kinoda boldular.', 'A1'),
    ('yesterday', '/ˈjestədeɪ/', 'ADV', 'düýn', 'вчера', 'on the day before today', 'I was tired yesterday.', 'Düýn ýadawdym.', 'A1'),
    ('last night', '/lɑːst naɪt/', 'PHR', 'düýn agşam', 'вчера вечером', 'during the night before today', 'We were at home last night.', 'Düýn agşam öýde bolduk.', 'A1'),
])

L['11A'] = (11, 'A new life in the USA', 'regular verbs', [
    ('start', '/stɑːt/', 'V', 'başlamak', 'начинать', 'to begin something', 'The lesson starts at nine.', 'Sapak sagat dokuzda başlaýar.', 'A1', 'start work'),
    ('stop', '/stɒp/', 'V', 'durmak, bes etmek', 'останавливать', 'to finish or not continue', 'The bus stops here.', 'Awtobus şu ýerde durýar.', 'A1', 'stop working'),
    ('walk', '/wɔːk/', 'V', 'ýöremek', 'идти пешком', 'to move on your feet', 'I walk to school.', 'Mektbe ýöräp barýaryn.', 'A1', 'walk home'),
    ('talk', '/tɔːk/', 'V', 'gürleşmek', 'разговаривать', 'to say words to someone', 'We talk on the phone.', 'Telefonda gürleşýäris.', 'A1', 'talk to'),
    ('help', '/help/', 'V', 'kömek etmek', 'помогать', 'to do something that makes it easier for someone', 'She helps me with English.', 'Iňlisde maňa kömek edýär.', 'A1', 'help someone with'),
    ('move', '/muːv/', 'V', 'göçmek, süýşürmek', 'переезжать', 'to go to live in a different place', 'They moved to the USA.', 'Olar ABŞ-a göçdüler.', 'A1', 'move to'),
    ('visit', '/ˈvɪzɪt/', 'V', 'baryp görmek', 'посещать', 'to go and see someone or a place', 'We visited our grandparents.', 'Uly ene-atamyzy baryp gördük.', 'A1', 'visit a friend'),
    ('call', '/kɔːl/', 'V', 'jaň etmek', 'звонить', 'to telephone someone', 'I called you yesterday.', 'Düýn saňa jaň etdim.', 'A1', 'call someone'),
    ('ask', '/ɑːsk/', 'V', 'soramak', 'спрашивать', 'to say a question to get an answer', 'He asked for the bill.', 'Hasaby sorady.', 'A1', 'ask for'),
    ('want', '/wɒnt/', 'V', 'islemek', 'хотеть', 'to wish for something', 'I want a coffee.', 'Kofe isleýärin.', 'A1', 'want to'),
])

L['11B'] = (11, 'How was your day?', 'irregular verbs · phrases with get, go, have, do', [
    ('went', '/went/', 'V', 'gitdi', 'пошёл, поехал', 'the past form of "go"', 'We went to the beach.', 'Deňiz kenaryna gitdik.', 'A1', 'went home'),
    ('had', '/hæd/', 'V', 'bardy, iýdi', 'было, был', 'the past form of "have"', 'I had a great day.', 'Ajaýyp gün geçirdim.', 'A1', 'had breakfast'),
    ('did', '/dɪd/', 'V', 'etdi', 'сделал', 'the past form of "do"', 'She did her homework.', 'Öý işini etdi.', 'A1', 'did the shopping'),
    ('got', '/ɡɒt/', 'V', 'aldy, tapyndy', 'получил', 'the past form of "get"', 'He got a new job.', 'Täze iş tapdy.', 'A1', 'got a taxi'),
    ('saw', '/sɔː/', 'V', 'gördi', 'видел', 'the past form of "see"', 'We saw a good film.', 'Gowy film gördük.', 'A1', 'saw a film'),
    ('ate', '/eɪt/', 'V', 'iýdi', 'ел', 'the past form of "eat"', 'I ate pasta.', 'Makaron iýdim.', 'A1'),
    ('drank', '/dræŋk/', 'V', 'içdi', 'пил', 'the past form of "drink"', 'She drank two teas.', 'Iki çaý içdi.', 'A1'),
    ('came', '/keɪm/', 'V', 'geldi', 'пришёл', 'the past form of "come"', 'He came home late.', 'Öýe giç geldi.', 'A1', 'came home'),
    ('took', '/tʊk/', 'V', 'aldy, müňdi', 'взял, сел на', 'the past form of "take"', 'We took the bus.', 'Awtobusa müňdük.', 'A1', 'took a taxi'),
    ('made', '/meɪd/', 'V', 'taýýarlady, etdi', 'сделал', 'the past form of "make"', 'She made dinner.', 'Agşamlyk taýýarlady.', 'A1', 'made dinner'),
])

L['11C'] = (13, 'Practical English 6 · asking for directions', 'prepositions of place', [
    ('above', '/əˈbʌv/', 'PREP', 'ýokarsynda', 'над', 'higher than something', 'The picture is above the bed.', 'Surat düşegiň ýokarsynda.', 'A1'),
    ('below', '/bɪˈləʊ/', 'PREP', 'aşagynda', 'под, ниже', 'lower than something', 'The car park is below the hotel.', 'Awtobus duralgasy myhmanhananyň aşagynda.', 'A1'),
    ('behind', '/bɪˈhaɪnd/', 'PREP', 'yzynda', 'за', 'at the back of something', 'The garden is behind the house.', 'Bag öýüň yzynda.', 'A1'),
    ('in front of', '/ɪn frʌnt əv/', 'PREP', 'öňünde', 'перед', 'directly ahead of something', 'There is a bus stop in front of the hotel.', 'Myhmanhananyň öňünde awtobus duralgasy bar.', 'A1'),
    ('next to', '/nekst tuː/', 'PREP', 'ýanynda', 'рядом с', 'at the side of something, very close', 'The bank is next to the shop.', 'Bank dükanyň ýanynda.', 'A1'),
    ('opposite', '/ˈɒpəzɪt/', 'PREP', 'garşysynda', 'напротив', 'on the other side of a road or space', 'The cinema is opposite the park.', 'Kino parkyň garşysynda.', 'A1'),
    ('between', '/bɪˈtwiːn/', 'PREP', 'arasynda', 'между', 'in the space separating two things', 'The shop is between the bank and the hotel.', 'Dükan bank bilen myhmanhananyň arasynda.', 'A1', 'between A and B'),
    ('near', '/nɪə/', 'PREP', 'ýakynynda', 'около, близко', 'not far from', 'The hotel is near the beach.', 'Myhmanhana deňziň ýanynda.', 'A1', 'near the station'),
])

L['12A'] = (12, 'Strangers on a train', 'regular and irregular verbs', [
    ('meet', '/miːt/', 'V', 'duşuşmak', 'встречать', 'to come together with someone', 'I met an interesting person on the train.', 'Otluda gyzykly adam bilen duşuşdym.', 'A1', 'meet a friend'),
    ('travel', '/ˈtrævl/', 'V', 'syýahat etmek', 'путешествовать', 'to go from one place to another, usually far', 'They travelled to Italy.', 'Italiýa syýahat etdiler.', 'A1', 'travel by train'),
    ('speak', '/spiːk/', 'V', 'gürlemek', 'говорить', 'to use words in a language', 'She speaks three languages.', 'Ol üç dilde gürleýär.', 'A1', 'speak English'),
    ('give', '/ɡɪv/', 'V', 'bermek', 'давать', 'to put something into someone\'s hand', 'He gave me his card.', 'Maňa wizitkasyny berdi.', 'A1', 'give someone something'),
    ('find', '/faɪnd/', 'V', 'tapmak', 'находить', 'to see something where it is', 'I found my keys.', 'Açarlarymy tapdym.', 'A1', 'find a seat'),
    ('write', '/raɪt/', 'V', 'ýazmak', 'писать', 'to make letters or words on paper', 'She wrote her email address.', 'E-poçta salgysyny ýazdy.', 'A1', 'write an email'),
    ('say', '/seɪ/', 'V', 'aýtmak', 'сказать', 'to speak words', 'He said goodbye.', 'Hoşlaşdy.', 'A1', 'say hello'),
    ('tell', '/tel/', 'V', 'gürrüň bermek', 'рассказывать', 'to give someone information', 'Tell me about your trip.', 'Syýahatyň barada gürrüň ber.', 'A1', 'tell someone'),
])

L['12B'] = (12, 'Revise the past', 'revision of past verb forms', [
    ('ago', '/əˈɡəʊ/', 'ADV', 'öň, mundan öň', 'назад', 'used to say how far back in the past something happened', 'I arrived two days ago.', 'Iki gün öň geldim.', 'A1', 'two days ago'),
    ('last week', '/lɑːst wiːk/', 'PHR', 'geçen hepde', 'на прошлой неделе', 'during the week before this one', 'We met last week.', 'Geçen hepde duşuşdyk.', 'A1'),
    ('when', '/wen/', 'ADV', 'haçan', 'когда', 'used in questions about time', 'When did you arrive?', 'Haçan geldiňiz?', 'A1'),
    ('where', '/weə/', 'ADV', 'nirede', 'где', 'used in questions about place', 'Where were you yesterday?', 'Düýn niredediňiz?', 'A1'),
    ('why', '/waɪ/', 'ADV', 'näme üçin', 'почему', 'used in questions about reasons', 'Why were you late?', 'Näme üçin giç galdiňiz?', 'A1'),
    ('how', '/haʊ/', 'ADV', 'nähili', 'как', 'used in questions about the way something happens', 'How was your day?', 'Günüň nähili geçdi?', 'A1', 'how was'),
    ('what', '/wɒt/', 'PRON', 'näme', 'что', 'used in questions about things', 'What did you do?', 'Näme etdiň?', 'A1'),
])

# Practical English lessons teach set phrases that appear in every unit's
# "Practical English" episode; they are kept with the lesson that introduces them.
L['3C'][3].append(('bill', '/bɪl/', 'N', 'hasap', 'счёт', 'a piece of paper that says how much you must pay', 'The bill, please.', 'Hasaby, haýyş.', 'A1', 'ask for the bill'))
L['7C'][3].append(('birthday', '/ˈbɜːθdeɪ/', 'N', 'doglan gün', 'день рождения', 'the day each year when you celebrate being born', 'Happy birthday!', 'Doglan günüň gutly bolsun!', 'A1', 'happy birthday'))


def main():
    words = []
    seen = {}
    dups = []

    for lesson in sorted(L, key=lambda k: (int(k[:-1]), k[-1])):
        unit, title, topic, entries = L[lesson]
        if not lesson[:-1].isdigit() or lesson[-1] not in 'ABC':
            raise SystemExit(f'bad lesson key: {lesson}')
        if not entries:
            raise SystemExit(f'lesson {lesson} ({title}) has no words')
        # The C-lesson of each file is its Practical English episode, which
        # lives in the shared PE unit 13 (owner request round 12: PE cards of
        # their own, like every other imported book), so 1C/3C/... may legally
        # disagree with their numeric prefix.
        if lesson[:-1] != str(unit) and not (lesson.endswith('C') and unit == 13):
            raise SystemExit(f'lesson {lesson} says unit {unit} but the key says {lesson[:-1]}')
        for e in entries:
            en, ipa, pos, tm, ru, de, ex, exTm, cefr = e[:9]
            coll = e[9] if len(e) > 9 else ''
            key = en.strip().lower()
            if key in seen:
                dups.append(f'{lesson}: "{en}" (already in {seen[key]})')
                continue
            seen[key] = lesson
            words.append({
                'en': en,
                'ipa': ipa,
                'pos': pos,
                'tm': tm,
                'ru': ru,
                'def': de,
                'ex': ex,
                'exTm': exTm,
                'cefr': cefr,
                'ox': 'Oxford 3000' if cefr == 'A1' else 'Oxford 5000',
                'syn': '—',
                'coll': coll or '—',
                'stage': 'New',
                'books': [{'book': 'beg', 'unit': unit, 'lesson': lesson,
                           'page': PAGE[lesson]}],
                'proofread': False,
            })

    if dups:
        raise SystemExit('duplicate headwords inside the book data:\n  ' + '\n  '.join(dups))

    # Lesson metadata, so the app can label a card "1A · A cappuccino, please"
    # without a second lookup table. Keyed "unit-lesson" to stay valid JSON.
    lessons = []
    for lesson in sorted(L, key=lambda k: (int(k[:-1]), k[-1])):
        unit, title, topic, entries = L[lesson]
        lessons.append({
            'lesson': lesson,
            'unit': unit,
            'title': title,
            'topic': topic,
            'words': sum(1 for w in words if w['books'][0]['lesson'] == lesson),
        })

    pack = {
        'book': 'beg',
        'title': 'English File Beginner (4th edition) — Vocabulary Bank, by lesson',
        'lessons': lessons,
        'words': words,
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(pack, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print(f'wrote {os.path.normpath(OUT)}: {len(words)} words, {len(lessons)} lessons')
    by_unit = {}
    for lesson in sorted(L, key=lambda k: (int(k[:-1]), k[-1])):
        unit, title, topic, entries = L[lesson]
        n = sum(1 for w in words if w['books'][0]['lesson'] == lesson)
        by_unit.setdefault(unit, []).append((lesson, title, topic, n))
    for unit in sorted(by_unit):
        total = sum(x[3] for x in by_unit[unit])
        print(f'\nunit {unit:>2} — {total} words')
        for lesson, title, topic, n in by_unit[unit]:
            print(f'    {lesson:<4} {n:>2} words  {title} — {topic}')


if __name__ == '__main__':
    main()
