#!/usr/bin/env python3
"""English File Pre-intermediate — vocabulary organised by the book's own structure.

WHERE THE WORDS COME FROM. Same method as Elementary (see gen_elementary.py):
the OCR dump (uploads/pre inermediate.txt) kept the Vocabulary Bank headwords
legible (p.150-161, dump lines ~18498-19660), so the topic lists were read out
of the book itself and cleaned up by hand; in-lesson VOCABULARY boxes supplied
the lessons the bank does not cover. Exercise instructions, audio cues and
column bleed were rejected.

Two things are NOT from the book and are flagged as such:
  - tm / ru / def / ex are my own work; the book is English-only. Every entry is
    proofread:false, so no native TM/RU check has happened.
  - the IPA below is written properly rather than copied from the OCR, whose
    phonetic characters are unreliable ("fofoienely" for /ˈfrendli/).

STRUCTURE. 12 units (contents table, dump lines 40-233) plus the six Practical
English episodes, which get unit 13 exactly as in Elementary. The Vocabulary
Bank has 14 sections: Describing people (150), Things you wear (151), Holidays
(152), Prepositions (153), Housework/make or do (154), Shopping (155),
Describing a town or city (156), Opposite verbs (157), Verb forms (158), get
(159), Confusing verbs (159-160), Expressing movement (160), Phrasal verbs
(161). "Verb forms" serves BOTH 7A (infinitive side) and 7B (gerund side), so
its words are split per word via WORD_LESSON.

Unit and lesson layout, from the contents table:
  1A Are you? Can you? Do you? · 1B The perfect date? · 1C The Remake Project
  2A OMG! Where's my passport? · 2B That's me in the picture! · 2C One dark October evening
  3A TripAside · 3B Put it in your calendar! · 3C Word games
  4A Who does what? · 4B In your basket · 4C #greatweekend
  5A I want it NOW! · 5B Twelve lost wallets · 5C How much is enough?
  6A Think positive - or negative? · 6B I'll always love you · 6C The meaning of dreaming
  7A First day nerves · 7B Happiness is ... · 7C Could you pass the test?
  8A Should I stay or should I go? · 8B Murphy's Law · 8C Who is Vivienne?
  9A Beware of the dog · 9B Fearof.net · 9C Scream queens
  10A Into the net · 10B Early birds · 10C International inventions
  11A Ask the teacher · 11B Help! I can't decide! · 11C Twinstrangers.net
  12A Unbelievable! · 12B Think before you speak · 12C The English File quiz
  PE1 Hotel problems · PE2 Restaurant problems · PE3 The wrong shoes ·
  PE4 At the pharmacy · PE5 Getting around · PE6 Time to go home

Usage: python3 content/tools/gen_pre.py
"""
import json
import os
import re
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'preintermediate.json')

# topic -> [ (en, ipa, pos, tm, ru, def, ex, exTm, cefr[, coll]) ]
# SB pages from the syllabus (TG pp.4-7), verified against the uploaded PDFs.
PAGE = {
    '1A': 6, '1B': 8, '1C': 10,
    '2A': 14, '2B': 16, '2C': 18,
    '3A': 22, '3B': 24, '3C': 26,
    '4A': 30, '4B': 32, '4C': 34,
    '5A': 38, '5B': 40, '5C': 42,
    '6A': 46, '6B': 48, '6C': 50,
    '7A': 54, '7B': 56, '7C': 58,
    '8A': 62, '8B': 64, '8C': 66,
    '9A': 70, '9B': 72, '9C': 74,
    '10A': 78, '10B': 80, '10C': 82,
    '11A': 86, '11B': 88, '11C': 90,
    '12A': 94, '12B': 96, '12C': 98,
    'PE1': 12, 'PE2': 28, 'PE3': 44, 'PE4': 60, 'PE5': 76, 'PE6': 92,
}

T = {}

# ---- Vocabulary Bank p.150 — Describing people -> 1B ----
T['describing_people'] = [
    ('clever', '/ˈklevə(r)/', 'ADJ', 'akylly', 'умный', 'quick at learning and understanding things', 'She is the cleverest student in the class.', 'Ol sinipdagi iň akylly okuwçy.', 'A2'),
    ('friendly', '/ˈfrendli/', 'ADJ', 'dostlukly', 'дружелюбный', 'open and warm towards other people', 'The people here are very friendly.', 'Bu ýerdäki adamlar gaty dostlukly.', 'A1', 'a friendly smile'),
    ('funny', '/ˈfʌni/', 'ADJ', 'gülmeli', 'смешной', 'making people laugh', 'He told us a funny story.', 'Ol bize gülmeli hekaýa gürrüň berdi.', 'A1'),
    ('generous', '/ˈdʒenərəs/', 'ADJ', 'jomart', 'щедрый', 'happy to give people things', 'She is generous with her time.', 'Ol wagty bilen jomart.', 'A2'),
    ('kind', '/kaɪnd/', 'ADJ', 'mähirli', 'добрый', 'friendly and good to other people', 'It was kind of you to help.', 'Kömek etmegiňiz mähirli boldy.', 'A2', 'a kind person'),
    ('lazy', '/ˈleɪzi/', 'ADJ', 'ýalta', 'ленивый', "not wanting to work or use energy", 'My lazy brother never makes his bed.', 'Ýalta doganym hiç wagt düşegini ýygnamaýar.', 'A2'),
    ('shy', '/ʃaɪ/', 'ADJ', 'uyaljaň', 'застенчивый', "unable to talk easily to people you don't know", 'She is too shy to speak in public.', 'Ol köpçülikde gürlemäge gaty uyaljaň.', 'A2'),
    ('talkative', '/ˈtɔːkətɪv/', 'ADJ', 'gepleýji', 'разговорчивый', 'talking a lot', 'Our new neighbour is very talkative.', 'Täze goňşumyz gaty gepleýji.', 'A2'),
    ('extrovert', '/ˈekstrəvɜːt/', 'ADJ', 'ekstrawert', 'экстраверт', 'lively and confident with other people', 'He is an extrovert who loves parties.', 'Ol toýlary söýýän ekstrawert.', 'B1'),
    ('hard-working', '/ˌhɑːd ˈwɜːkɪŋ/', 'ADJ', 'zähmetsöýer', 'трудолюбивый', 'putting a lot of effort into work', 'She is a hard-working nurse.', 'Ol zähmetsöýer şepagat uýasy.', 'A2'),
    ('mean', '/miːn/', 'ADJ', 'gysganç', 'скупой', 'not wanting to spend money or give things', 'He is too mean to buy a present.', 'Ol sowgat almaga gaty gysganç.', 'A2'),
    ('quiet', '/ˈkwaɪət/', 'ADJ', 'sessiz', 'тихий', 'making little noise; not talking much', 'He is a quiet, serious boy.', 'Ol sessiz, çynlakaý oglan.', 'A1'),
    ('serious', '/ˈsɪəriəs/', 'ADJ', 'çynlakaý', 'серьёзный', 'thinking carefully; not joking', 'She gave me a serious look.', 'Ol maňa çynlakaý seretdi.', 'A2'),
    ('stupid', '/ˈstjuːpɪd/', 'ADJ', 'ahmak', 'глупый', 'not showing intelligence; a bad idea', 'That was a stupid mistake.', 'Ol ahmak ýalňyşlykdy.', 'A2'),
    ('unfriendly', '/ʌnˈfrendli/', 'ADJ', 'dostlukly däl', 'недружелюбный', 'not friendly', 'The waiter was cold and unfriendly.', 'Ofisiant sowuk we dostlukly däldi.', 'A2'),
    ('unkind', '/ˌʌnˈkaɪnd/', 'ADJ', 'mähirsiz', 'недобрый', 'not kind', 'It was unkind to laugh at him.', 'Oňa gülmek mähirsiz boldy.', 'A2'),
    ('curly', '/ˈkɜːli/', 'ADJ', 'buýra', 'кудрявый', 'having curls; not straight', 'She has curly red hair.', 'Onuň buýra gyzyl saçlary bar.', 'A2', 'curly hair'),
    ('straight', '/streɪt/', 'ADJ', 'göni', 'прямой', 'not curly or bent', 'He has long straight hair.', 'Onuň uzyn göni saçlary bar.', 'A2', 'straight hair'),
    ('beard', '/bɪəd/', 'N', 'sakgal', 'борода', 'hair on the chin and cheeks of a man', 'He has a beard and a moustache.', 'Onuň sakgaly we murtlary bar.', 'A2', 'grow a beard'),
    ('moustache', '/məˈstɑːʃ/', 'N', 'murt', 'усы', 'hair above the upper lip', 'My uncle has a big black moustache.', 'Kakamyň uly gara murtlary bar.', 'A2'),
    ('bald', '/bɔːld/', 'ADJ', 'kel', 'лысый', 'having no hair on the head', "My dad started going bald at thirty.", 'Kakam otuz ýaşynda kel bolup başlady.', 'A2', 'go bald'),
    ('tall', '/tɔːl/', 'ADJ', 'uzyn boýly', 'высокий', 'of more than average height', "He's very tall and thin.", 'Ol gaty uzyn boýly we ýuka.', 'A1'),
    ('thin', '/θɪn/', 'ADJ', 'ýuka', 'худой', 'having little fat on the body', 'She was tall and very thin.', 'Ol uzyn boýly we gaty ýukady.', 'A2'),
    ('slim', '/slɪm/', 'ADJ', 'ýiti', 'стройный', 'thin in an attractive way', 'He stayed slim by running every day.', 'Ol her gün ylgap ýiti galdy.', 'A2'),
    ('overweight', '/ˌəʊvəˈweɪt/', 'ADJ', 'agramly', 'с лишним весом', 'too fat; more polite than "fat"', 'The doctor says I am a bit overweight.', 'Lukman biraz agramlydygymy aýdýar.', 'B1'),
    ('good-looking', '/ˌɡʊd ˈlʊkɪŋ/', 'ADJ', 'ýakymly sypatly', 'красивый, привлекательный', 'pleasant to look at (men or women)', 'Her good-looking brother is an actor.', 'Onuň ýakymly sypatly dogany aktýor.', 'A2'),
    ('attractive', '/əˈtræktɪv/', 'ADJ', 'özüne çekiji', 'привлекательный', 'pleasant or beautiful to look at', 'She has an attractive smile.', 'Onuň özüne çekiji ýylgyryşy bar.', 'A2'),
    ('height', '/haɪt/', 'N', 'boý', 'рост', "how tall a person or thing is", "He's medium height and very slim.", 'Ol orta boýly we gaty ýiti.', 'A2', 'medium height'),
    ('blonde', '/blɒnd/', 'ADJ', 'sary saçly', 'блондин, светловолосый', 'with light yellow hair', 'She has long blonde hair.', 'Onuň uzyn sary saçy bar.', 'A2'),
    ('dark', '/dɑːk/', 'ADJ', 'goýy', 'тёмный', 'not light in colour', 'He has dark hair and brown eyes.', 'Onuň goýy saçy we goňur gözleri bar.', 'A2'),
    ('medium-height', '/ˌmiːdiəm ˈhaɪt/', 'ADJ', 'orta boýly', 'среднего роста', 'neither tall nor short', "He's medium-height and slim.", 'Ol orta boýly we ýuka.', 'A2'),
    ('enthusiastic', '/ɪnˌθjuːziˈæstɪk/', 'ADJ', 'joşgunly', 'увлечённый, энтузиастичный', 'very interested and excited about something', 'She is enthusiastic about her new job.', 'Ol täze işi barada joşgunly.', 'B1'),
]

# ---- Vocabulary Bank p.151 — Things you wear -> 1C (clothes; place prepositions live here too) ----
T['clothes'] = [
    ('blouse', '/blaʊz/', 'N', 'bluzka', 'блузка', "a shirt for women and girls", 'She wore a white silk blouse.', 'Ol ak ýüpek bluzka geýdi.', 'A2'),
    ('cardigan', '/ˈkɑːdɪɡən/', 'N', 'kofta', 'кофта', 'a warm sweater with buttons at the front', 'Put on a cardigan, it is cold.', 'Kofta geý, howa sowuk.', 'A2'),
    ('coat', '/kəʊt/', 'N', 'palto', 'пальто', 'a long warm outer garment', 'Hang your coat behind the door.', 'Paltoňy gapynyň arkasynda as.', 'A1'),
    ('dress', '/dres/', 'N', 'köýnek', 'платье', "a piece of clothing for women that covers the body and part of the legs", 'She bought a beautiful summer dress.', 'Ol owadan tomus köýnegi satyn aldy.', 'A1'),
    ('glove', '/ɡlʌv/', 'N', 'ellik', 'перчатка', 'a piece of clothing for the hand', 'I lost one of my gloves.', 'Elliklerimiň birini ýitirdim.', 'A2', 'a pair of gloves'),
    ('scarf', '/skɑːf/', 'N', 'şarf', 'шарф', 'a piece of cloth worn round the neck', 'He wrapped a warm scarf round his neck.', 'Ol boýnuna ýyly şarf dolady.', 'A2'),
    ('suit', '/suːt/', 'N', 'kostýum', 'костюм', 'a jacket and trousers of the same cloth', 'He wears a suit to work.', 'Ol işe kostýum geýýär.', 'A2', 'wear a suit'),
    ('sweater', '/ˈswetə(r)/', 'N', 'switer', 'свитер', 'a warm piece of clothing for the top of the body', 'This green sweater is too small.', 'Bu ýaşyl switer gaty kiçi.', 'A1'),
    ('tie', '/taɪ/', 'N', 'galstuk', 'галстук', 'a narrow piece of cloth worn round the neck with a shirt', 'My father always wears a tie.', 'Kakam hemişe galstuk dakynýar.', 'A2', 'wear a tie'),
    ('tracksuit', '/ˈtræksuːt/', 'N', 'sport kostýumy', 'спортивный костюм', 'loose clothes worn for sport or relaxing', 'He changed into a tracksuit.', 'Ol sport kostýumyny geýdi.', 'A2'),
    ('underwear', '/ˈʌndəweə(r)/', 'N', 'içki geýim', 'нижнее бельё', 'clothes worn under other clothes', 'Pack some clean underwear.', 'Arassa içki geýim ýygnap goý.', 'A2'),
    ('in front of', '/ɪn frʌnt əv/', 'PREP', 'öňünde', 'перед', 'in a position that is forward of something', 'The car is in front of the house.', 'Maşyn öýüň öňünde.', 'A2'),
    ('behind', '/bɪˈhaɪnd/', 'PREP', 'yzynda', 'позади', 'at or towards the back of something', 'The garden is behind the building.', 'Bag binanyň yzynda.', 'A2'),
    ('next to', '/nekst tuː/', 'PREP', 'ýanynda', 'рядом с', 'at the side of something; very near', 'The bank is next to the pharmacy.', 'Bank dermanhananyň ýanynda.', 'A1'),
    ('between', '/bɪˈtwiːn/', 'PREP', 'arasynda', 'между', 'in the space separating two things', 'She sat between her two friends.', 'Ol iki dostunyň arasynda oturdi.', 'A2'),
    ('opposite', '/ˈɒpəzɪt/', 'PREP', 'garşysynda', 'напротив', 'on the other side of a road or room', 'The cafe is opposite the station.', 'Kafe wokzalyň garşysynda.', 'A2'),
    ('above', '/əˈbʌv/', 'PREP', 'üstünde', 'над', 'in a higher place than something', 'There is a lamp above the table.', 'Stoluň üstünde çyra bar.', 'A2'),
    ('on the left', '/ɒn ðə left/', 'PHR', 'çepde', 'слева', 'at or towards the left side', 'The exit is on the left.', 'Çykalga çepde.', 'A2'),
    ('on the right', '/ɒn ðə raɪt/', 'PHR', 'sagda', 'справа', 'at or towards the right side', 'Take the door on the right.', 'Sagdaky gapyny saýla.', 'A2'),
    ('belt', '/belt/', 'N', 'kemer', 'ремень', 'a strip of leather you wear round your waist', 'He wears a black belt.', 'Ol gara kemer dakynýar.', 'A2'),
    ('boots', '/buːts/', 'N', 'ädik', 'ботинки, сапоги', 'strong shoes that cover your feet and ankles', 'Put on your boots, it is snowing.', 'Ädikleriňi geý, gar ýagýar.', 'A1'),
    ('bracelet', '/ˈbreɪslət/', 'N', 'bilezik', 'браслет', 'jewellery you wear round your wrist', 'She wears a gold bracelet.', 'Ol altyn bilezik dakynýar.', 'A2'),
    ('cap', '/kæp/', 'N', 'kepka', 'кепка', 'a soft hat with a peak', 'He wears a baseball cap.', 'Ol beýsbol kepka geýýär.', 'A2'),
    ('earrings', '/ˈɪərɪŋz/', 'N', 'gulakhalka', 'серьги', 'jewellery you wear on your ears', 'Her earrings are silver.', 'Onuň gulakhalkalary kümüş.', 'A2'),
    ('gloves', '/ɡlʌvz/', 'N', 'ellik', 'перчатки', 'clothes you wear on your hands', 'Wear gloves, your hands are cold.', 'Ellik geý, elleriň üşeýär.', 'A2'),
    ('hat', '/hæt/', 'N', 'şlýapa', 'шляпа', 'something you wear on your head', 'She bought a summer hat.', 'Ol tomus şlýapasy satyn aldy.', 'A1'),
    ('jeans', '/dʒiːnz/', 'N', 'jinsi', 'джинсы', 'trousers made of denim', 'He always wears jeans.', 'Ol hemişe jinsi geýýär.', 'A1'),
    ('jumper', '/ˈdʒʌmpə/', 'N', 'jemper', 'джемпер, пуловер', 'a warm piece of clothing for the top of your body (British English)', 'Put on a jumper, it is cold.', 'Jemper geý, sowuk.', 'A2'),
    ('leggings', '/ˈleɡɪŋz/', 'N', 'legins', 'легинсы', 'very tight trousers worn by women', 'She wears black leggings.', 'Ol gara legins geýýär.', 'A2'),
    ('necklace', '/ˈnekləs/', 'N', 'monjuk', 'ожерелье', 'jewellery you wear round your neck', 'What a beautiful necklace!', 'Nähili owadan monjuk!', 'A2'),
    ('sandals', '/ˈsændlz/', 'N', 'sandal', 'сандалии', 'light shoes for warm weather', 'I wear sandals in summer.', 'Tomusda sandal geýýärin.', 'A2'),
    ('shirt', '/ʃɜːt/', 'N', 'köýnek', 'рубашка', 'clothes for the top of your body with buttons', 'He wears a white shirt to work.', 'Ol işe ak köýnek geýýär.', 'A1'),
    ('shoes', '/ʃuːz/', 'N', 'aýakgap', 'туфли, ботинки', 'things you wear on your feet', 'These shoes are comfortable.', 'Bu aýakgaplar amatly.', 'A1'),
    ('skirt', '/skɜːt/', 'N', 'ýubka', 'юбка', 'clothes worn by women from the waist down', 'She wears a long skirt.', 'Ol uzyn ýubka geýýär.', 'A1'),
    ('socks', '/sɒks/', 'N', 'jorap', 'носки', 'soft clothes you wear on your feet inside shoes', 'I need clean socks.', 'Maňa arassa jorap gerek.', 'A2'),
    ('tights', '/taɪts/', 'N', 'kalgotki', 'колготки', "thin clothes that cover women's legs", 'She wears black tights in winter.', 'Gyşda gara kalgotki geýýär.', 'A2'),
    ('top', '/tɒp/', 'N', 'bluzka', 'топ, кофточка', 'light clothes for the top of your body', 'That is a nice top.', 'Bu owadan bluzka.', 'A2'),
    ('trainers', '/ˈtreɪnəz/', 'N', 'krossowka', 'кроссовки', 'comfortable shoes for sport', 'He runs in new trainers.', 'Ol täze krossowkada ylgaw edýär.', 'A2'),
    ('trousers', '/ˈtraʊzəz/', 'N', 'balak', 'брюки', 'clothes that cover you from the waist to the feet', 'His trousers are too long.', 'Onuň balagy gaty uzyn.', 'A2'),
    ('flip-flops', '/ˈflɪp flɒps/', 'N', 'şypbyk', 'шлёпанцы, вьетнамки', 'very light shoes you wear in summer', 'We wear flip-flops on the beach.', 'Kenarda şypbyk geýýäris.', 'A2'),
    ('pyjamas', '/pəˈdʒɑːməz/', 'N', 'pijama', 'пижама', 'clothes you wear in bed', 'I sleep in cotton pyjamas.', 'Pagta pijamada ýatýaryn.', 'A2'),
]

# ---- Vocabulary Bank p.152 — Holidays -> 2A ----
T['holidays'] = [
    ('accommodation', '/əˌkɒməˈdeɪʃn/', 'N', 'ýaşaýyş ýeri', 'жильё', 'a place to stay on holiday', 'The price includes flights and accommodation.', 'Bahada uçar we ýaşaýyş ýeri bar.', 'B1', 'book accommodation'),
    ('camping', '/ˈkæmpɪŋ/', 'N', 'düşelge', 'кемпинг', 'sleeping outside in a tent', 'We went camping in the mountains.', 'Biz daglarda düşelge gurduk.', 'A2', 'go camping'),
    ('coach', '/kəʊtʃ/', 'N', 'awtobus', 'автобус (междугородный)', 'a comfortable bus for long journeys', 'The coach leaves at seven.', 'Awtobus ýedide gidýär.', 'A2', 'by coach'),
    ('cruise', '/kruːz/', 'N', 'kruiz', 'круиз', 'a holiday travelling on a large ship', 'They went on a Mediterranean cruise.', 'Olar Ortaýer deňzi kruizine gitdiler.', 'B1', 'go on a cruise'),
    ('ferry', '/ˈferi/', 'N', 'parom', 'паром', 'a boat that carries people and cars across water', 'We caught the ferry to the island.', 'Ada gidýän paroma mündik.', 'B1', 'catch a ferry'),
    ('guest house', '/ˈɡest haʊs/', 'N', 'myhman öýi', 'гостевой дом', 'a small cheap place to stay, like a home', 'We stayed in a little guest house.', 'Kiçijik myhman öýünde galdyk.', 'A2'),
    ('journey', '/ˈdʒɜːni/', 'N', 'syýahat', 'путешествие', 'the act of travelling from one place to another', 'The journey took six hours.', 'Syýahat alty sagat dowam etdi.', 'A2', 'a long journey'),
    ('luggage', '/ˈlʌɡɪdʒ/', 'N', 'goş', 'багаж', 'bags and suitcases you travel with', 'We left our luggage at the hotel.', 'Goşumyzy myhmanhanada goýduk.', 'A2', 'hand luggage'),
    ('passenger', '/ˈpæsɪndʒə(r)/', 'N', 'ýolagçy', 'пассажир', 'a person travelling in a vehicle', 'All passengers must fasten their seatbelts.', 'Ähli ýolagçylar kemerlerini dakynmaly.', 'A2'),
    ('platform', '/ˈplætfɔːm/', 'N', 'platforma', 'платформа', 'the place where you wait for a train', 'The train leaves from platform four.', 'Otly dördünji platformadan gidýär.', 'A2', 'on the platform'),
    ('scenery', '/ˈsiːnəri/', 'N', 'tebigy gözellik', 'пейзаж', 'the natural features of a place', 'The mountain scenery was beautiful.', 'Dag tebigaty örän owadandy.', 'B1', 'beautiful scenery'),
    ('season', '/ˈsiːzn/', 'N', 'pasyl', 'сезон', 'one of the four parts of the year; a period for an activity', 'Autumn is my favourite season.', 'Güýz meniň iň söýýän paslym.', 'A2', 'the rainy season'),
    ('sightseeing', '/ˈsaɪtsiːɪŋ/', 'N', 'görmeli ýerlere gezelenç', 'осмотр достопримечательностей', 'visiting interesting places', 'We spent the day sightseeing.', 'Güni gözel ýerlere gezelenç edip geçirdik.', 'A2', 'go sightseeing'),
    ('souvenir', '/ˌsuːvəˈnɪə(r)/', 'N', 'ýadygärlik sowgat', 'сувенир', 'something you buy to remember a place', 'I bought a souvenir for my mother.', 'Ejem üçin ýadygärlik sowgat aldym.', 'A2'),
    ('tent', '/tent/', 'N', 'çadyr', 'палатка', 'a cloth shelter you sleep in', 'We put up the tent by the river.', 'Çadyry derýanyň ýanynda gurdyk.', 'A2', 'put up a tent'),
    ('tour', '/tʊə(r)/', 'N', 'tur', 'тур', 'a short visit to look round a place', 'We took a tour of the old city.', 'Köne şähere tur etdik.', 'A2', 'a guided tour'),
    ('voyage', '/ˈvɔɪɪdʒ/', 'N', 'deňiz syýahaty', 'морское путешествие', 'a long journey by sea or in space', 'The voyage across the ocean took a month.', 'Okean syýahaty bir aý dowam etdi.', 'B1'),
    ('delayed', '/dɪˈleɪd/', 'ADJ', 'giçikdirilen', 'задержанный', 'later than planned', 'Our flight was delayed by two hours.', 'Uçarymyz iki sagat giçikdirildi.', 'A2', 'a delayed flight'),
    ('book', '/bʊk/', 'V', 'öňünden almak, bron etmek', 'бронировать', 'to arrange to have a room, ticket, etc. in the future', 'We booked a flight online.', 'Uçar petegini onlaýn bron etdik.', 'A2', 'book a flight'),
    ('hire', '/ˈhaɪə/', 'V', 'kärendesine almak', 'брать напрокат', 'to pay to use something for a short time', 'We hired a bike for the day.', 'Günlük welosiped kärendesine aldyk.', 'A2', 'hire a car'),
    ('rent', '/rent/', 'V', 'kärendesine almak', 'арендовать', 'to pay money to use a house, car, etc.', 'They rented a flat by the sea.', 'Deňiz kenaryndaky öýi kärendesine aldylar.', 'A2'),
    ('stay', '/steɪ/', 'V', 'galmak', 'оставаться, останавливаться', 'to sleep somewhere for a night or more', 'We stayed in a small hotel.', 'Kiçi myhmanhanada galdyk.', 'A2', 'stay in a hotel'),
    ('sunbathe', '/ˈsʌnbeɪð/', 'V', 'güne düşmek', 'загорать', 'to sit or lie in the sun', 'She sunbathed on the beach all morning.', 'Ol bütin irden kenarda güne düşdi.', 'A2'),
    ('go abroad', '/ˌɡəʊ əˈbrɔːd/', 'PHR', 'daşary ýurda gitmek', 'поехать за границу', 'to travel to another country', 'They go abroad every summer.', 'Olar her tomus daşary ýurda gidýärler.', 'A2'),
]

# ---- Vocabulary Bank p.153 — Prepositions (time side) -> 2B ----
T['prepositions_time'] = [
    ('at', '/æt/', 'PREP', 'sagatda', 'в (время)', "used before a time or point", 'The film starts at eight.', 'Film sekizde başlaýar.', 'A1', 'at night'),
    ('in', '/ɪn/', 'PREP', 'içinde', 'в (период)', 'used before months, years and parts of the day', 'My birthday is in June.', 'Doglan günim iýunda.', 'A1', 'in the morning'),
    ('on', '/ɒn/', 'PREP', 'güni', 'в (день)', 'used before days and dates', 'We arrived on Tuesday.', 'Sişenbe güni geldik.', 'A1', 'on Monday'),
    ('at night', '/æt naɪt/', 'PHR', 'gijesine', 'ночью', 'during the night', 'I never drink coffee at night.', 'Gijesine hiç wagt kofe içmeýärin.', 'A1'),
    ('in the morning', '/ɪn ðə ˈmɔːnɪŋ/', 'PHR', 'irden', 'утром', 'during the morning', 'I go running in the morning.', 'Irden ylgamaga gidýärin.', 'A1'),
    ('on time', '/ɒn taɪm/', 'PHR', 'wagtynda', 'вовремя', 'at the planned time; not late', 'The train arrived on time.', 'Otly wagtynda geldi.', 'A2', 'arrive on time'),
    ('in time', '/ɪn taɪm/', 'PHR', 'wagt ýetişip', 'успеть вовремя', 'early enough for something', 'We got to the airport in time.', 'Wagtynda aeroporta ýetişdik.', 'A2', 'in time for'),
    ('during', '/ˈdjʊərɪŋ/', 'PREP', 'dowamynda', 'во время', 'from the beginning to the end of a period', 'She fell asleep during the film.', 'Filmiň dowamynda uklap galdy.', 'A2', 'during the night'),
    ('for', '/fə(r)/', 'PREP', 'dowamynda (wagt)', 'в течение', 'used to say how long something lasts', 'We waited for two hours.', 'Iki sagat garadyk.', 'A1', 'for ages'),
    ('since', '/sɪns/', 'PREP', 'şondan bäri', 'с (поры)', 'from a point in the past until now', 'She has lived here since 2019.', '2019-njy ýyldan bäri şu ýerde ýaşaýar.', 'A2', 'since then'),
    ('until', '/ənˈtɪl/', 'PREP', 'çenli', 'до (поры)', 'up to a particular time', 'The shop is open until nine.', 'Dükan doquza çenli açyk.', 'A2'),
    ('by', '/baɪ/', 'PREP', 'çenli (möhlet)', 'к (сроку)', 'not later than a time', 'Finish the report by Friday.', 'Hasabaty anna güni çenli gutar.', 'A2', 'by the time'),
    ('from ... to', '/frɒm tuː/', 'PREP', '-dan ... çenli', 'с ... до', 'showing the start and end of a period', 'I work from nine to five.', 'Dokuzdan bäşe çenli işleýärin.', 'A1'),
]

# ---- Vocabulary Bank p.154 — Housework, make or do? -> 4A ----
T['housework'] = [
    ('do the ironing', '/duː ði ˈaɪənɪŋ/', 'PHR', 'eşik ütükleme işi', 'глажка белья', 'to make clothes flat with an iron', 'He does the ironing on Sundays.', 'Ol ýekşenbe güni eşikleri ütikleýär.', 'A2', 'do the ironing'),
    ('do the washing-up', '/duː ðə ˈwɒʃɪŋ ʌp/', 'PHR', 'gap-gaç ýuwmak', 'мыть посуду', 'to wash plates and cups after a meal', 'I cooked, so you do the washing-up.', 'Men bişirdim, gap-gaçy sen ýuw.', 'A2'),
    ('do the housework', '/duː ðə ˈhaʊswɜːk/', 'PHR', 'öý işlerini etmek', 'делать работу по дому', 'to clean and tidy the house', 'We share the housework equally.', 'Öý işlerini deň paýlaşýarys.', 'A2'),
    ('make the bed', '/meɪk ðə bed/', 'PHR', 'düşek ýygnamak', 'заправлять кровать', 'to arrange the sheets and blankets neatly', 'She makes her bed every morning.', 'Ol her ertir düşegini ýygnaýar.', 'A1'),
    ('tidy', '/ˈtaɪdi/', 'V', 'ýygnamak', 'убирать', 'to make a place neat', 'Tidy your room before you go out.', 'Çykmazdan otagyňy ýygna.', 'A2', 'tidy your room'),
    ('sweep', '/swiːp/', 'V', 'süpürmek', 'мести', 'to clean the floor with a brush', 'I swept the kitchen floor.', 'Aşhana poluny süpürdim.', 'A2', 'sweep the floor'),
    ('dust', '/dʌst/', 'V', 'tozan almak', 'вытирать пыль', 'to remove dust from furniture', 'She dusted the shelves.', 'Tekjeleriň tozanyny aldy.', 'A2', 'dust the furniture'),
    ('vacuum', '/ˈvækjuːm/', 'V', 'sorujy bilen arassalamak', 'пылесосить', 'to clean with a vacuum cleaner', 'He vacuums the carpet every week.', 'Her hepde haly sorýar.', 'A2', 'vacuum the carpet'),
    ('fold', '/fəʊld/', 'V', 'eplemek', 'складывать', 'to bend clothes neatly into shape', 'I folded the clean shirts.', 'Arassa köýnekleri epledim.', 'B1', 'fold the clothes'),
    ('set the table', '/set ðə ˈteɪbl/', 'PHR', 'süfra ýazmak', 'накрывать на стол', 'to put plates and cutlery ready for a meal', 'Please set the table for four.', 'Dört adamlyk süfra ýaz.', 'A2'),
    ('take out the rubbish', '/teɪk aʊt ðə ˈrʌbɪʃ/', 'PHR', 'zibil dökmek', 'выносить мусор', 'to carry the rubbish outside', 'It is your turn to take out the rubbish.', 'Zibili dökmek nobaty sende.', 'A2'),
]

# ---- Vocabulary Bank p.155 — Shopping -> 4B ----
T['shopping'] = [
    ('bargain', '/ˈbɑːɡən/', 'N', 'arzan satyn alyş', 'выгодная покупка', 'something bought at a very good price', 'These shoes were a real bargain.', 'Bu aýakgap hakykatdan arzan düşdi.', 'A2', 'a real bargain'),
    ('cash', '/kæʃ/', 'N', 'nagt pul', 'наличные', 'money in coins and notes', 'I paid in cash.', 'Nagt pul bilen töledim.', 'A2', 'pay in cash'),
    ('changing room', '/ˈtʃeɪndʒɪŋ ruːm/', 'N', 'synag otagy', 'примерочная', 'a room where you try on clothes in a shop', 'The changing rooms are over there.', 'Synag otaglary şol ýerde.', 'A2'),
    ('cheap', '/tʃiːp/', 'ADJ', 'arzan', 'дешёвый', 'costing little money', 'This coat was very cheap.', 'Bu palto gaty arzan eken.', 'A1'),
    ('credit card', '/ˈkredɪt kɑːd/', 'N', 'kredit kartoçkasy', 'кредитная карта', 'a small plastic card used to pay later', 'Do you accept credit cards?', 'Kredit kartoçkalaryny kabul edýärsiňizmi?', 'A2', 'pay by credit card'),
    ('customer', '/ˈkʌstəmə(r)/', 'N', 'müşderi', 'покупатель', 'a person who buys from a shop', 'The customer asked for a smaller size.', 'Müşderi kiçi ölçeg sorady.', 'A2'),
    ('discount', '/ˈdɪskaʊnt/', 'N', 'arzanladyş', 'скидка', 'a reduction in the usual price', 'Students get a ten per cent discount.', 'Talyplar on göterim arzanladyş alýar.', 'A2', 'get a discount'),
    ('expensive', '/ɪkˈspensɪv/', 'ADJ', 'gymmat', 'дорогой', 'costing a lot of money', 'That restaurant is too expensive for us.', 'Ol restoran biziň üçin gaty gymmat.', 'A1'),
    ('offer', '/ˈɒfə(r)/', 'N', 'arzanladyş teklibi', 'акция, предложение', 'a special low price for a short time', 'The jeans are on offer this week.', 'Jinsiler şu hepde arzanladyşda.', 'A2', 'on offer'),
    ('receipt', '/rɪˈsiːt/', 'N', 'çek', 'чек', 'a piece of paper showing what you paid', 'Keep the receipt in case you return it.', 'Yzyna gaýtarsaň çek sakla.', 'A2', 'keep the receipt'),
    ('refund', '/ˈriːfʌnd/', 'N', 'pul yzyna gaýtarma', 'возврат денег', 'money given back when you return something', 'I got a full refund.', 'Doly pulumy yzyna aldym.', 'B1', 'get a refund'),
    ('reduce', '/rɪˈdjuːs/', 'V', 'arzanlatmak', 'снижать', 'to make the price lower', 'They reduced all winter coats.', 'Ähli gyş paltolaryny arzanlatdylar.', 'A2'),
    ('size', '/saɪz/', 'N', 'ölçeg', 'размер', 'how big or small something is; a number for clothes', 'These trousers are the wrong size.', 'Bu balak nädogry ölçeg.', 'A1', 'what size'),
    ('shop assistant', '/ˈʃɒp əˌsɪstənt/', 'N', 'satyjy', 'продавец', 'a person who works in a shop', 'The shop assistant was very helpful.', 'Satyjy gaty kömekçil boldy.', 'A2'),
    ('value for money', '/ˈvælju fə ˈmʌni/', 'PHR', 'pula degýän', 'соотношение цены и качества', 'worth the price you pay', 'The hotel is good value for money.', 'Myhmanhana puluna degýär.', 'B1'),
    ('try on', '/traɪ ɒn/', 'PHR', 'synap görmek', 'примерять', 'to put on clothes to see if they fit', 'Can I try this on?', 'Muny synap görüp bolarmy?', 'A2', 'try on clothes'),
    ('basket', '/ˈbɑːskɪt/', 'N', 'sebet', 'корзина', 'a container you carry when shopping', 'Put the bread in the basket.', 'Çöregi sebede sal.', 'A2'),
    ('checkout', '/ˈtʃekaʊt/', 'N', 'kassa', 'касса (место оплаты)', 'the place where you pay in a shop', 'Pay at the checkout, please.', 'Kassada töläň, haýyş.', 'A2'),
    ('debit card', '/ˈdebɪt kɑːd/', 'N', 'debet karty', 'дебетовая карта', 'a plastic card that takes money directly from your bank account', 'I paid by debit card.', 'Debet karty bilen töledim.', 'A2'),
    ('delivery', '/dɪˈlɪvəri/', 'N', 'eltip bermek', 'доставка', 'when goods are brought to your house', 'The delivery took two days.', 'Eltip bermek iki gün aldy.', 'A2'),
    ('item', '/ˈaɪtəm/', 'N', 'haryt', 'товар, предмет', 'a single thing in a list or a shop', 'This item was in the sale.', 'Bu haryt arzanladyşda boldy.', 'A2'),
    ('shelves', '/ˈʃelvz/', 'N', 'tekçeler', 'полки', 'flat boards where things are kept in a shop', 'The books are on the top shelves.', 'Kitaplar ýokarky tekçelerde.', 'A2'),
    ('till', '/tɪl/', 'N', 'kassa', 'касса (аппарат)', 'the machine where you pay in a shop', 'She put the money in the till.', 'Puly kassa saldy.', 'A2'),
    ('trolley', '/ˈtrɒli/', 'N', 'söwda arabasy', 'тележка', 'a large basket on wheels you push in a supermarket', 'Put the milk in the trolley.', 'Süýdi araba sal.', 'A2'),
    ('website', '/ˈwebsaɪt/', 'N', 'web sahypa', 'веб-сайт', 'a set of pages on the internet', 'Order it from the website.', 'Web sahypadan sargyt et.', 'A2'),
    ('auction', '/ˈɔːkʃn/', 'N', 'auksion', 'аукцион', 'a sale where people offer more and more money for a thing', 'The painting was sold at auction.', 'Surat auksionda satyldy.', 'B1'),
]

# ---- Vocabulary Bank p.156 — Describing a town or city -> 5B ----
T['town_city'] = [
    ('ancient', '/ˈeɪnʃənt/', 'ADJ', 'gadymy', 'древний', 'very old; from long ago', 'We visited the ancient city walls.', 'Gadymy şäher diwarlaryna baryp gördük.', 'A2', 'ancient ruins'),
    ('atmosphere', '/ˈætməsfɪə(r)/', 'N', 'howa (duýgy)', 'атмосфера', 'the feeling a place gives you', 'The old town has a lovely atmosphere.', 'Köne şäheriň ajaýyp howasy bar.', 'B1', 'a relaxed atmosphere'),
    ('busy', '/ˈbɪzi/', 'ADJ', 'işjeň', 'оживлённый', 'full of people and activity', 'We live on a busy street.', 'Işjeň köçede ýaşaýarys.', 'A1', 'a busy street'),
    ('capital', '/ˈkæpɪtl/', 'N', 'paýtagt', 'столица', 'the most important city of a country', 'Ashgabat is the capital of Turkmenistan.', 'Aşgabat Türkmenistanyň paýtagty.', 'A2', 'the capital city'),
    ('city centre', '/ˈsɪti ˈsentə(r)/', 'N', 'şäher merkezi', 'центр города', 'the middle of a city where the shops are', 'We walked to the city centre.', 'Şäher merkezine pyýada gitdik.', 'A2'),
    ('crowded', '/ˈkraʊdɪd/', 'ADJ', 'märeli', 'переполненный', 'full of people', 'The market was hot and crowded.', 'Bazar yssy we märeli boldy.', 'A2'),
    ('dull', '/dʌl/', 'ADJ', 'gysgynç', 'скучный', 'not interesting; boring', 'Life in the village seemed dull to him.', 'Obadaky durmuş oňa gysgynç görünýärdi.', 'A2'),
    ('historic', '/hɪˈstɒrɪk/', 'ADJ', 'taryhy', 'исторический', 'important in history', 'Merv is a historic city.', 'Merw taryhy şäher.', 'A2', 'a historic building'),
    ('modern', '/ˈmɒdn/', 'ADJ', 'häzirki zaman', 'современный', 'of the present time; new ideas and style', 'The modern part of the city has tall towers.', 'Şäheriň häzirki zaman böleginde beýik diňler bar.', 'A1'),
    ('multicultural', '/ˌmʌltiˈkʌltʃərəl/', 'ADJ', 'köpmedeniýetli', 'многокультурный', 'with many different cultures living together', 'London is a truly multicultural city.', 'London hakykatdan köpmedeniýetli şäher.', 'B1'),
    ('noisy', '/ˈnɔɪzi/', 'ADJ', 'gohly', 'шумный', 'making a lot of noise', 'Our street is noisy at night.', 'Köçämiz gijelerine gohly.', 'A2'),
    ('polluted', '/pəˈluːtɪd/', 'ADJ', 'hapalanan', 'загрязнённый', 'made dirty by chemicals or waste', 'The air in the city is polluted.', 'Şäherdäki howa hapalanan.', 'B1'),
    ('residential', '/ˌrezɪˈdenʃl/', 'ADJ', 'ýaşaýyş', 'жилой', 'where people live; not offices or shops', 'They live in a quiet residential area.', 'Olar asuda ýaşaýyş sebitinde ýaşaýarlar.', 'B1', 'a residential area'),
    ('safe', '/seɪf/', 'ADJ', 'howpsuz', 'безопасный', 'not dangerous', 'The city feels safe at night.', 'Şäher gijelerine howpsuz duýulýar.', 'A2'),
    ('traffic', '/ˈtræfɪk/', 'N', 'ulag hereketi', 'движение транспорта', 'vehicles moving on a road', 'The traffic is terrible in the morning.', 'Irden ulag hereketi elhenç.', 'A2', 'heavy traffic'),
    ('lively', '/ˈlaɪvli/', 'ADJ', 'joşgunly', 'оживлённый, энергичный', 'full of life and energy', 'The market square is lively on Saturdays.', 'Bazar meýdançasy şenbe günleri joşgunly.', 'A2'),
    ('tourist', '/ˈtʊərɪst/', 'N', 'syýahatçy', 'турист', 'a person visiting a place for pleasure', 'The city is full of tourists in summer.', 'Tomusda şäher syýahatçylardan doly.', 'A2', 'a tourist attraction'),
    ('cathedral', '/kəˈθiːdrəl/', 'N', 'sobor', 'собор', 'a very large important church', 'The cathedral is 800 years old.', 'Sobor 800 ýaşynda.', 'A2'),
    ('castle', '/ˈkɑːsl/', 'N', 'gala', 'замок', 'a large old strong building', 'There is an old castle on the hill.', 'Depede gadymy gala bar.', 'A2'),
    ('canal', '/kəˈnæl/', 'N', 'kanal', 'канал', 'a river made by people for boats', 'We walked along the canal.', 'Kanalyň boýy ýöräp gitdik.', 'A2'),
    ('village', '/ˈvɪlɪdʒ/', 'N', 'oba', 'деревня', 'a very small town in the country', 'She lives in a quiet village.', 'Ol asuda obada ýaşaýar.', 'A2'),
    ('church', '/tʃɜːtʃ/', 'N', 'kilise', 'церковь', 'a building where Christians pray', 'The church is in the square.', 'Kilise meýdançada.', 'A2'),
    ('harbour', '/ˈhɑːbə/', 'N', 'port', 'гавань, порт', 'a place where ships are safe', 'The boats are in the harbour.', 'Gämiler portda.', 'A2'),
    ('hill', '/hɪl/', 'N', 'depe', 'холм', 'like a small mountain', 'We climbed to the top of the hill.', 'Depäniň depesine çykdym.', 'A2'),
    ('lake', '/leɪk/', 'N', 'köl', 'озеро', 'a large area of water', 'We swam in the lake.', 'Kölde ýüzdük.', 'A2'),
    ('market', '/ˈmɑːkɪt/', 'N', 'bazar', 'рынок', 'a place where people sell food and other things', 'She buys fruit at the market.', 'Miweni bazardan satyn alýar.', 'A2'),
    ('mosque', '/mɒsk/', 'N', 'metjit', 'мечеть', 'a building where Muslims pray', 'The mosque has a beautiful garden.', 'Metjidiň owadan bagy bar.', 'A2'),
    ('museum', '/mjuˈziːəm/', 'N', 'muzeý', 'музей', 'a building with interesting old things', 'The museum opens at nine.', 'Muzeý sagat dokuzda açylýar.', 'A2'),
    ('ruins', '/ˈruːɪnz/', 'N', 'harabalyk', 'руины', 'parts of very old broken buildings', 'We visited some Roman ruins.', 'Rim harabalyklaryny gördük.', 'A2'),
    ('statue', '/ˈstætʃuː/', 'N', 'heýkel', 'статуя', 'a figure of a person or animal made of stone or metal', 'There is a statue in the square.', 'Meýdançada heýkel bar.', 'A2'),
    ('temple', '/ˈtempl/', 'N', 'ybadathana', 'храм', 'a building where people pray in some religions', 'The temple is very old.', 'Ybadathana gaty gadymy.', 'A2'),
    ('town hall', '/ˌtaʊn ˈhɔːl/', 'N', 'şäher häkimligi', 'ратуша', "the office building of a town's government", 'They got married at the town hall.', 'Şäher häkimliginde öýlendiler.', 'A2'),
    ('city walls', '/ˌsɪti ˈwɔːlz/', 'N', 'şäher diwarlary', 'городские стены', 'old walls built around a city', 'You can walk on the city walls.', 'Şäher diwarlarynda ýöräp bolýar.', 'A2'),
    ('department store', '/dɪˈpɑːtmənt stɔː/', 'N', 'uniwersal magazin', 'универмаг', 'a large shop with many departments', 'We met at the department store.', 'Uniwersal magazinde duşuşdyk.', 'A2'),
    ('area', '/ˈeəriə/', 'N', 'sebit', 'район, область', 'a part of a town or country', 'It is a quiet area of the city.', 'Şäheriň asuda sebiti.', 'A2'),
    ('coast', '/kəʊst/', 'N', 'kenar', 'побережье', 'the land next to the sea', 'They live on the south coast.', 'Olar günorta kenarda ýaşaýar.', 'A2'),
    ('population', '/ˌpɒpjuˈleɪʃn/', 'N', 'ilat', 'население', 'all the people in a place', 'The city has a population of two million.', 'Şäheriň ilaty iki million.', 'A2'),
    ('medium-sized', '/ˌmiːdiəm ˈsaɪzd/', 'ADJ', 'orta ululykda', 'среднего размера', 'not big and not small', 'It is a medium-sized town.', 'Ol orta ululykda şäher.', 'A2'),
]
# ---- Vocabulary Bank p.157 — Opposite verbs -> 6A ----
T['opposite_verbs'] = [
    ('arrive', '/əˈraɪv/', 'V', 'gelmek', 'прибывать', 'to reach a place at the end of a journey', 'We arrived at the hotel late.', 'Myhmanhana giç geldik.', 'A1', 'arrive at'),
    ('leave', '/liːv/', 'V', 'gitmek', 'уезжать', 'to go away from a place', 'The train leaves in ten minutes.', 'Otly on minutda gidýär.', 'A1', 'leave home'),
    ('borrow', '/ˈbɒrəʊ/', 'V', 'karzyna almak', 'брать взаймы', 'to take something and give it back later', 'Can I borrow your pen?', 'Galamyňy karzyna alyp bolarmy?', 'A2'),
    ('lend', '/lend/', 'V', 'karzyna bermek', 'давать взаймы', 'to let someone use your things for a time', 'She lent me her umbrella.', 'Ol maňa ýaglygyny karzyna berdi.', 'A2'),
    ('sell', '/sel/', 'V', 'satmak', 'продавать', 'to give something for money', 'They sell fresh bread here.', 'Bu ýerde täze çörek satýarlar.', 'A1'),
    ('remember', '/rɪˈmembə(r)/', 'V', 'ýatda saklamak', 'помнить', 'to have an image of something in your mind', 'I remember my first day at school.', 'Mekdepdäki ilkinji günimi ýatda saklaýaryn.', 'A1'),
    ('forget', '/fəˈɡet/', 'V', 'ýatdan çykarmak', 'забывать', 'to not remember something', "Don't forget your keys.", 'Açarlaryňy ýatdan çykarma.', 'A1'),
    ('find', '/faɪnd/', 'V', 'tapmak', 'находить', 'to discover something, often by chance', 'I found ten manat in my old coat.', 'Köne paltoýumda on manat tapdym.', 'A1'),
    ('lose', '/luːz/', 'V', 'ýitirmek', 'терять', 'to not have something any more', 'He lost his wallet on the bus.', 'Awtobusda gapjygyny ýitirdi.', 'A1', 'lose your keys'),
    ('win', '/wɪn/', 'V', 'utuşmak', 'выигрывать', 'to be the best in a game or competition', 'Our team won the match.', 'Toparymyz oýunda utdy.', 'A2', 'win a prize'),
    ('fail', '/feɪl/', 'V', 'synagdan ýykylyp galmak', 'проваливать(ся)', 'to not pass a test', 'She failed her driving test twice.', 'Sürüjilik synagyndan iki gezek ýykyldy.', 'A2', 'fail an exam'),
    ('pass', '/pɑːs/', 'V', 'synagdan geçmek', 'сдавать (экзамен)', 'to succeed in a test', 'He passed all his exams.', 'Ähli synaglardan geçdi.', 'A2', 'pass an exam'),
    ('raise', '/reɪz/', 'V', 'galdyrmak', 'поднимать', 'to move something to a higher position', 'She raised her hand to ask a question.', 'Sorag bermek üçin elini galdyrdy.', 'A2', 'raise your hand'),
    ('lower', '/ˈləʊə(r)/', 'V', 'aşak düşürmek', 'опускать', 'to move something down', 'He lowered his voice.', 'Ol sesini aşak düşürdi.', 'B1'),
    ('close', '/kləʊz/', 'V', 'ýapmak', 'закрывать', 'to make something not open', 'Please close the window.', 'Öýjügi ýapmagyňyzy haýyş edýärin.', 'A1'),
    ('buy', '/baɪ/', 'V', 'satyn almak', 'покупать', 'to get something by paying money', 'We bought some bread.', 'Biraz çörek satyn aldyk.', 'A2'),
    ('mend', '/mend/', 'V', 'ýamamak, bejermek', 'чинить, штопать', 'to repair something, especially clothes', 'She mended the hole in my shirt.', 'Köýnegimdäki deşigi ýamady.', 'A2'),
    ('repair', '/rɪˈpeə/', 'V', 'bejermek', 'ремонтировать', 'to make something work again', 'He repaired the bike.', 'Welosipedi bejerdi.', 'A2'),
    ('pull', '/pʊl/', 'V', 'dartmak, çekmek', 'тянуть', 'to move something towards you', 'Pull the door to open it.', 'Gapyny açmak üçin dart.', 'A2'),
    ('push', '/pʊʃ/', 'V', 'itmek', 'толкать', 'to move something away from you', 'Push the door to close it.', 'Gapyny ýapmak üçin it.', 'A2'),
    ('receive', '/rɪˈsiːv/', 'V', 'almak', 'получать', 'to get something that is sent to you', 'I received your email.', 'Emailiňi aldym.', 'A2'),
    ('open', '/ˈəʊpən/', 'V', 'açmak', 'открывать', 'to make something not closed', 'They open the shop at nine.', 'Dükany sagat dokuzda açýarlar.', 'A2'),
]

# ---- Vocabulary Bank p.158 — Verb forms -> split between 7A (infinitive) and 7B (gerund) ----
T['verb_forms'] = [
    ('want', '/wɒnt/', 'V', 'islemek', 'хотеть', 'to wish for something (want to do)', 'I want to learn English.', 'Iňlis dilini öwrenmek isleýärin.', 'A1', 'want to do'),
    ('decide', '/dɪˈsaɪd/', 'V', 'karar bermek', 'решать', 'to make a choice (decide to do)', 'We decided to stay at home.', 'Öýde galmaga karar berdik.', 'A2', 'decide to go'),
    ('hope', '/həʊp/', 'V', 'umyt etmek', 'надеяться', 'to want something to happen (hope to do)', 'I hope to see you soon.', 'Ýakyn wagtda görüşeris diýip umyt edýärin.', 'A2', 'hope to see'),
    ('learn', '/lɜːn/', 'V', 'öwrenmek', 'учиться', 'to get knowledge or skill (learn to do)', 'She is learning to drive.', 'Ulag sürmegi öwrenýär.', 'A1', 'learn to swim'),
    ('manage', '/ˈmænɪdʒ/', 'V', 'hötdesinden gelmek', 'справляться', 'to succeed in doing something difficult', 'He managed to fix the bike.', 'Welosipedi bejermegiň hötdesinden geldi.', 'A2', 'manage to do'),
    ('offer to', '/ˈɒfə(r) tuː/', 'PHR', 'etmegi teklip etmek', 'предлагать сделать', 'to say you will do something', 'She offered to help me.', 'Maňa kömek etmegi teklip etdi.', 'A2', 'offer to help'),
    ('promise', '/ˈprɒmɪs/', 'V', 'wada bermek', 'обещать', 'to say you will certainly do something', 'He promised to call me.', 'Jaň etjegine wada berdi.', 'A2', 'promise to call'),
    ('refuse', '/rɪˈfjuːz/', 'V', 'boýun towlamak', 'отказываться', 'to say no to something (refuse to do)', 'She refused to answer.', 'Jogap bermekden boýun towlady.', 'A2', 'refuse to go'),
    ('expect', '/ɪkˈspekt/', 'V', 'garamak', 'ожидать', 'to think something will happen (expect to do)', 'We expect to arrive at six.', 'Altida ýeteris diýip garaýarys.', 'A2', 'expect to win'),
    ('afford', '/əˈfɔːd/', 'V', 'güýji ýetmek', 'позволить себе', 'to have enough money for something', "I can't afford a new phone.", 'Täze telefona güýjüm ýetmeýär.', 'A2', "can't afford"),
    ('arrange', '/əˈreɪndʒ/', 'V', 'gurnamak', 'договариваться', 'to plan something (arrange to do)', 'We arranged to meet at noon.', 'Günortan duşuşmaga gurnadyk.', 'B1', 'arrange to meet'),
    ('agree', '/əˈɡriː/', 'V', 'ylalaşmak', 'соглашаться', 'to have the same opinion (agree to do)', 'They agreed to share the cost.', 'Çykdajyny paýlaşmaga ylalaşdylar.', 'A2', 'agree to help'),
    ('enjoy', '/ɪnˈdʒɔɪ/', 'V', 'lezzet almak', 'наслаждаться', 'to like doing something (enjoy doing)', 'I enjoy reading before bed.', 'Uklamazdan öň okamakdan lezzet alýaryn.', 'A1', 'enjoy reading'),
    ('avoid', '/əˈvɔɪd/', 'V', 'gaça durmak', 'избегать', 'to keep away from something (avoid doing)', 'He avoids driving in the centre.', 'Merkezde ulag sürmekden gaça durýar.', 'A2', 'avoid talking'),
    ('finish', '/ˈfɪnɪʃ/', 'V', 'gutarmak', 'заканчивать', 'to complete something (finish doing)', 'Have you finished eating?', 'Iýip gutardyňmy?', 'A1', 'finish working'),
    ('keep', '/kiːp/', 'V', 'dowam etmek', 'продолжать', 'to continue doing something', 'She keeps forgetting my name.', 'Adymy yzygiderli ýatdan çykarýar.', 'A2', 'keep trying'),
    ('mind', '/maɪnd/', 'V', 'garşy bolmak', 'возражать', 'to be annoyed by something (mind doing)', "I don't mind waiting.", 'Garaşmaga garşy däl.', 'A2', "don't mind doing"),
    ('miss', '/mɪs/', 'V', 'küýsemek', 'скучать', 'to feel sad that something is gone (miss doing)', 'I miss living near the sea.', 'Deňziň ýanynda ýaşamagy küýseýärin.', 'A2'),
    ('practise', '/ˈpræktɪs/', 'V', 'türgenleşmek', 'тренироваться', 'to do something again to improve (practise doing)', 'Practise speaking every day.', 'Her gün gürleşmäge türgenleş.', 'A2', 'practise speaking'),
    ('suggest', '/səˈdʒest/', 'V', 'teklip etmek', 'предлагать (идею)', 'to put forward an idea (suggest doing)', 'She suggested going by train.', 'Otly bilen gitmegi teklip etdi.', 'A2', 'suggest going'),
    ('would rather', '/wʊd ˈrɑːðə(r)/', 'PHR', 'gowy görerdim', 'лучше бы', 'to prefer one thing to another', "I'd rather stay at home.", 'Öýde galmagy gowy görerdim.', 'B1'),
    ('used to', '/ˈjuːst tuː/', 'PHR', 'öň ederdi', 'раньше делал', 'something true in the past but not now', 'We used to live in a village.', 'Öň obada ýaşardy.', 'A2'),
]

# ---- Vocabulary Bank p.159 — get -> 8A ----
T['get'] = [
    ('get up', '/ɡet ʌp/', 'PHR', 'turmak', 'вставать', 'to leave your bed in the morning', 'I get up at seven.', 'Ýedide turýaryn.', 'A1'),
    ('get dressed', '/ɡet drest/', 'PHR', 'geýinmek', 'одеваться', 'to put your clothes on', 'He got dressed quickly.', 'Ol çalt geýindi.', 'A1'),
    ('get married', '/ɡet ˈmærid/', 'PHR', 'öýlenmek', 'жениться', 'to start being married', 'They got married in May.', 'Maý aýynda öýlendiler.', 'A2', 'get married to'),
    ('get lost', '/ɡet lɒst/', 'PHR', 'azmak', 'заблудиться', 'to not know where you are', 'We got lost in the old town.', 'Köne şäherde azdyk.', 'A2'),
    ('get better', '/ɡet ˈbetə(r)/', 'PHR', 'gowulaşmak', 'становиться лучше', 'to improve; to become less ill', 'Your English is getting better.', 'Iňlis diliň gowulaşýar.', 'A2'),
    ('get worse', '/ɡet ˈwɜːsə(r)/', 'PHR', 'ýaramazlaşmak', 'ухудшаться', 'to become less good', 'The weather got worse in the evening.', 'Agşam howa ýaramazlaşdy.', 'A2'),
    ('get home', '/ɡet həʊm/', 'PHR', 'öýe ýetmek', 'добираться домой', 'to arrive at your home', 'What time did you get home?', 'Näçede öýe ýetdiň?', 'A1'),
    ('get ready', '/ɡet ˈredi/', 'PHR', 'taýýarlanmak', 'собираться', 'to prepare yourself', 'Get ready, we are leaving.', 'Taýýarlan, gidýäris.', 'A2'),
    ('get on well', '/ɡet ɒn wel/', 'PHR', 'oňuşmak', 'ладить', 'to have a good relationship', 'I get on well with my colleagues.', 'Işdeşlerim bilen oňuşýaryn.', 'A2', 'get on well with'),
    ('get to', '/ɡet tuː/', 'PHR', 'barmak', 'добираться до', 'to arrive at a place', 'How do I get to the station?', 'Wokzala nädip barmaly?', 'A2', 'get to work'),
    ('get fit', '/ˌɡet ˈfɪt/', 'PHR', 'forma girmek', 'прийти в форму', 'to exercise so your body becomes strong', 'She swims to get fit.', 'Forma girmek üçin ýüzýär.', 'A2'),
    ('get divorced', '/ˌɡet dɪˈvɔːst/', 'PHR', 'aýrylyşmak', 'развестись', 'to end a marriage', 'They got divorced last year.', 'Olar geçen ýyl aýrylyşdylar.', 'A2'),
    ('get tickets', '/ˌɡet ˈtɪkɪts/', 'PHR', 'bilet almak', 'достать билеты', 'to buy tickets', 'We got tickets for the concert.', 'Konsert üçin bilet aldyk.', 'A2'),
]

# ---- Vocabulary Bank p.159-160 — Confusing verbs -> 8B ----
T['confusing_verbs'] = [
    ('bring', '/brɪŋ/', 'V', 'getirmek', 'приносить', 'to carry something towards here', 'Bring your dictionary tomorrow.', 'Ertir sözlügini getir.', 'A1', 'bring something with you'),
    ('take', '/teɪk/', 'V', 'eltmek', 'уносить, брать', 'to carry something away from here', 'Take an umbrella with you.', 'Ýanyň bilen ýaglyk al.', 'A1', 'take something home'),
    ('wait', '/weɪt/', 'V', 'garamak', 'ждать', 'to stay until something happens', 'Wait for me at the corner.', 'Burçda meni gara.', 'A1', 'wait for'),
    ('say', '/seɪ/', 'V', 'aýtmak', 'говорить (слова)', 'to speak words', 'She said she was tired.', 'Ýadandygyny aýtdy.', 'A1', 'say hello'),
    ('tell', '/tel/', 'V', 'gürrüň bermek', 'рассказывать', 'to give information to a person', 'Tell me the truth.', 'Maňa hakykaty aýt.', 'A1', 'tell the truth'),
    ('speak', '/spiːk/', 'V', 'gürlemek', 'говорить (на языке)', 'to use your voice; to know a language', 'She speaks three languages.', 'Ol üç dilde gürleýär.', 'A1', 'speak English'),
    ('talk', '/tɔːk/', 'V', 'gürleşmek', 'разговаривать', 'to have a conversation', 'They talked for hours.', 'Sagatlap gürleşdiler.', 'A1', 'talk about'),
    ('hear', '/hɪə(r)/', 'V', 'eşitmek', 'слышать', 'to receive sound with your ears', 'I heard a strange noise.', 'Geň ses eşitdim.', 'A1', 'hear a noise'),
    ('listen', '/ˈlɪsn/', 'V', 'diňlemek', 'слушать', 'to pay attention to sound', 'Listen to the teacher.', 'Mugallyma diňle.', 'A1', 'listen to music'),
    ('watch', '/wɒtʃ/', 'V', 'syn etmek', 'смотреть (на движение)', 'to look at something for a time', 'We watched the match together.', 'Oýna bile syn etdik.', 'A1', 'watch TV'),
    ('look', '/lʊk/', 'V', 'seretmek', 'смотреть (взглянуть)', 'to direct your eyes at something', 'Look at this photo.', 'Şu surata seret.', 'A1', 'look at'),
    ('see', '/siː/', 'V', 'görmek', 'видеть', 'to use your eyes', 'I can see the mountains from here.', 'Bu ýerden daglary görüp bilýärin.', 'A1'),
    ('earn', '/ɜːn/', 'V', 'gazandyrmak', 'зарабатывать', 'to get money for work', 'She earns a good salary.', 'Ol gowy aýlyk gazanýar.', 'A2', 'earn money'),
    ('remind', '/rɪˈmaɪnd/', 'V', 'ýatlatmak', 'напоминать', 'to help someone remember', 'Remind me to call my mum.', 'Ejeme jaň etmegi ýatlat.', 'A2', 'remind me'),
    ('teach', '/tiːtʃ/', 'V', 'öwretmek', 'преподавать', 'to give lessons', 'My aunt teaches maths.', 'Uly ejem matematika öwredýär.', 'A1', 'teach English'),
    ('study', '/ˈstʌdi/', 'V', 'okamak', 'изучать', 'to learn about a subject', 'He is studying medicine.', 'Lukmançylyk okaýar.', 'A1', 'study hard'),
    ('rise', '/raɪz/', 'V', 'galmak', 'подниматься', 'to go up by itself', 'The sun rises in the east.', 'Gün gündogarda galýar.', 'A2', 'prices rise'),
    ('lie', '/laɪ/', 'V', 'ýatmak', 'лежать', 'to be in a flat position', 'The cat lay on the sofa.', 'Pişik diwanyň üstünde ýatdy.', 'A2', 'lie on the bed'),
    ('carry', '/ˈkæri/', 'V', 'götermek, daşamak', 'нести', 'to hold and move something with you', 'She carried a heavy bag.', 'Agyr torba göterdi.', 'A2'),
    ('miss', '/mɪs/', 'V', 'sagynmak; sypdyrmak', 'скучать; пропустить', 'to feel sad without someone; to not catch something', 'I miss my family. We missed the bus.', 'Maşgalamy sagyndym. Awtobusy sypdyrdyk.', 'A2'),
    ('wear', '/weə/', 'V', 'geýmek', 'носить', 'to have clothes on your body', 'She wears glasses to read.', 'Okamak üçin äýnek geýýär.', 'A2'),
    ('know', '/nəʊ/', 'V', 'bilmek', 'знать', 'to have information in your mind', 'I know the answer.', 'Jogaby bilýärin.', 'A2'),
    ('meet', '/miːt/', 'V', 'duşuşmak, tanyşmak', 'встречать(ся), знакомиться', 'to come together with someone', 'Nice to meet you.', 'Tanyşanyma şat.', 'A2'),
]

# ---- Vocabulary Bank p.160 — Expressing movement (sports) -> 10A ----
T['movement'] = [
    ('athletics', '/æθˈletɪks/', 'N', 'ýeňil atletika', 'лёгкая атлетика', 'sports like running, jumping and throwing', 'She does athletics at school.', 'Mekdepde ýeňil atletika bilen meşgullanýar.', 'A2', 'do athletics'),
    ('badminton', '/ˈbædmɪntən/', 'N', 'badminton', 'бадминтон', 'a game with rackets and a light object', 'We play badminton in the park.', 'Seýilgähde badminton oýnaýarys.', 'A2', 'play badminton'),
    ('boxing', '/ˈbɒksɪŋ/', 'N', 'boks', 'бокс', 'a sport where two people fight with gloves', 'He does boxing twice a week.', 'Hepdede iki gezek boks bilen meşgullanýar.', 'A2', 'do boxing'),
    ('karate', '/kəˈrɑːti/', 'N', 'karate', 'карате', 'a Japanese sport of fighting with hands and feet', 'My sister has done karate for years.', 'Uýam ýyllap karate bilen meşgullandy.', 'A2', 'do karate'),
    ('rugby', '/ˈrʌɡbi/', 'N', 'regbi', 'регби', 'a team game with an oval ball', 'They play rugby at university.', 'Uniwersitetde regbi oýnaýarlar.', 'A2', 'play rugby'),
    ('table tennis', '/ˈteɪbl tenɪs/', 'N', 'stol tennisi', 'настольный теннис', 'a game like tennis on a table', 'We watched a table tennis final.', 'Stol tennisi finalyna seretdik.', 'A2', 'play table tennis'),
    ('volleyball', '/ˈvɒlibɔːl/', 'N', 'wolleybol', 'волейбол', 'a team game over a high net', 'The girls play volleyball after school.', 'Gyzlar mekdepden soň wolleybol oýnaýar.', 'A2', 'play volleyball'),
    ('climb', '/klaɪm/', 'V', 'dyrmaşmak', 'взбираться', 'to go up something steep', 'We climbed the hill in the dark.', 'Tüm garaňkylykda depe dyrmaşdyk.', 'A2', 'climb a mountain'),
    ('crawl', '/krɔːl/', 'V', 'emmeklemek', 'ползти', 'to move on hands and knees', 'The baby crawled across the floor.', 'Çaga poluň üstünden emmekledi.', 'B1'),
    ('dive', '/daɪv/', 'V', 'suwa bökmek', 'нырять', 'to jump into water head first', 'He dived into the pool.', 'Howuza başy bilen bökdü.', 'B1', 'dive into'),
    ('jump', '/dʒʌmp/', 'V', 'bökmek', 'прыгать', 'to push yourself off the ground', 'The cat jumped onto the table.', 'Pişik stoluň üstüne bökdü.', 'A2', 'jump high'),
    ('slide', '/slaɪd/', 'V', 'typmak', 'скользить', 'to move smoothly over a surface', 'The car slid on the ice.', 'Maşyn buzuň üstünden typdy.', 'B1', 'slide across'),
    ('throw', '/θrəʊ/', 'V', 'zyňmak', 'бросать', 'to send something through the air', 'Throw me the ball.', 'Top maňa zyň.', 'A2', 'throw a ball'),
    ('catch', '/kætʃ/', 'V', 'tutmak', 'ловить', 'to take hold of something moving', 'She caught the ball with one hand.', 'Topy bir eli bilen tutdy.', 'A2', 'catch a ball'),
    ('along', '/əˈlɒŋ/', 'PREP', 'boýuna', 'вдоль', 'following a street or river', 'We walked along the street.', 'Köçäniň boýy ýöräp gitdik.', 'A2'),
    ('into', '/ˈɪntə/', 'PREP', 'içine', 'в (внутрь)', 'to the inside of a place', 'She went into the shop.', 'Dükana girdi.', 'A2'),
    ('over', '/ˈəʊvə/', 'PREP', 'üstünden', 'через, над', 'from one side to the other', 'They walked over the bridge.', 'Köpriniň üstünden geçdiler.', 'A2'),
    ('past', '/pɑːst/', 'PREP', 'ýanyndan', 'мимо', 'going by something', 'He ran past the church.', 'Kilisäniň ýanyndan ylgap geçdi.', 'A2'),
    ('through', '/θruː/', 'PREP', 'içinden', 'через, сквозь', 'from one end to the other inside something', 'The train went through the tunnel.', 'Otly tunelden geçdi.', 'A2'),
    ('towards', '/təˈwɔːdz/', 'PREP', 'tarapa', 'к, по направлению к', 'in the direction of something', 'She walked towards the lake.', 'Köle tarap ýöräp gitdi.', 'A2'),
    ('hit', '/hɪt/', 'V', 'urmak', 'ударять, бить', 'to touch something hard with force', 'He hit the ball hard.', 'Ol pökgä gaty urdy.', 'A2'),
    ('kick', '/kɪk/', 'V', 'depmek', 'ударять ногой', 'to hit something with your foot', 'Kick the ball to me!', 'Pökgini maňa dep!', 'A2'),
]

# ---- Vocabulary Bank p.161 — Phrasal verbs -> 10B ----
T['phrasal_verbs'] = [
    ('drop off', '/drɒp ɒf/', 'PHR', 'düşürmek', 'высаживать', 'to take someone to a place and leave them', 'I will drop you off at school.', 'Seni mekdebe düşürerin.', 'A2', 'drop off at the airport'),
    ('pick up', '/pɪk ʌp/', 'PHR', 'almak', 'поднимать; забирать', 'to lift something; to collect someone', 'Can you pick the children up at six?', 'Çagalary altyda alyp bilersiňmi?', 'A2', 'pick up from the airport'),
    ('put away', '/pʊt əˈweɪ/', 'PHR', 'ýerine goýmak', 'убирать на место', 'to put things where they belong', 'Put away your clothes.', 'Eşikleriňi ýerine goý.', 'A2', 'put away the dishes'),
    ('send back', '/send bæk/', 'PHR', 'yzyna ibermek', 'отправлять обратно', 'to return something by post', 'We sent the shoes back to the shop.', 'Aýakgaplary dükana yzyna iberdik.', 'A2', 'send back an order'),
    ('take out', '/teɪk aʊt/', 'PHR', 'çykarmak', 'выносить', 'to remove something from a place', 'He took out the bins.', 'Zibil gaplaryny çykardy.', 'A2', 'take out the rubbish'),
    ('turn off', '/tɜːn ɒf/', 'PHR', 'öçürmek', 'выключать', 'to stop a machine or light', 'Turn off the TV and go to bed.', 'Telewizory öçür-de ýat.', 'A1', 'turn off the lights'),
    ('turn on', '/tɜːn ɒn/', 'PHR', 'ýakmak', 'включать', 'to start a machine or light', 'Turn on the heating, please.', 'Ýyladyjyny ýak.', 'A1', 'turn on the TV'),
    ('write down', '/raɪt daʊn/', 'PHR', 'ýazyp almak', 'записывать', 'to record words on paper', 'Write down the new words.', 'Täze sözleri ýazyp al.', 'A2', 'write down the answer'),
    ('go on', '/ɡəʊ ɒn/', 'PHR', 'dowam etmek', 'продолжать', 'to continue doing something', 'She went on talking.', 'Gürleşmegini dowam etdi.', 'A2', 'go on doing'),
    ('look for', '/lʊk fə(r)/', 'PHR', 'gözlemek', 'искать', 'to try to find something', "I'm looking for my keys.", 'Açarlarymy gözleýärin.', 'A2', 'look for a job'),
    ('look round', '/lʊk raʊnd/', 'PHR', 'aýlanyp görmek', 'осматривать', 'to walk around a place to see it', 'We looked round the museum.', 'Muzeýi aýlanyp gördük.', 'A2', 'look round a city'),
    ('run out of', '/rʌn aʊt əv/', 'PHR', 'gutarmak', 'заканчиваться (о запасах)', 'to use all of something', 'We ran out of petrol.', 'Benzinimiz gutardy.', 'A2', 'run out of time'),
    ('find out', '/ˌfaɪnd ˈaʊt/', 'PHR', 'öwrenmek, anyklamak', 'выяснить, узнать', 'to get information about something', 'I found out the answer online.', 'Jogaby onlaýn öwrendim.', 'A2'),
    ('get out of bed', '/ˌɡet aʊt əv ˈbed/', 'PHR', 'düşekden turmak', 'вставать с постели', 'to leave your bed in the morning', 'He gets out of bed at seven.', 'Sagat ýedide düşekden turýar.', 'A2'),
    ('go off', '/ˌɡəʊ ˈɒf/', 'PHR', '(jaň) çalmak', 'звенеть, срабатывать', 'when an alarm makes a noise', 'My alarm went off at six.', 'Budilnigim sagat altyda çaldy.', 'A2'),
    ('go to bed', '/ˌɡəʊ tə ˈbed/', 'PHR', 'ýatmak', 'ложиться спать', 'to get into bed to sleep', 'I go to bed at eleven.', 'Sagat on birede ýatýaryn.', 'A1'),
    ('turn up', '/ˌtɜːn ˈʌp/', 'PHR', 'peýda bolmak', 'появляться (часто неожиданно)', 'to arrive, often late', 'He turned up an hour late.', 'Bir sagat giç geldi.', 'A2'),
]

# ---- In-lesson boxes ----
T['verb_phrases_1a'] = [
    ('do your homework', '/duː jə ˈhəʊmwɜːk/', 'PHR', 'öý işini etmek', 'делать домашнее задание', 'to complete the work a teacher gives', 'Have you done your homework?', 'Öý işiňi etdiňmi?', 'A1'),
    ('make a mistake', '/meɪk ə mɪˈsteɪk/', 'PHR', 'ýalňyşmak', 'ошибаться', 'to do something wrong', "Don't be afraid to make a mistake.", 'Ýalňyşmakdan gorkma.', 'A2', 'make a mistake'),
    ('take a photo', '/teɪk ə ˈfəʊtəʊ/', 'PHR', 'surata düşürmek', 'фотографировать', 'to use a camera', 'Can I take a photo of you?', 'Suratyňyza düşürip bolarmy?', 'A1', 'take a photo of'),
    ('have a shower', '/hæv ə ˈʃaʊə(r)/', 'PHR', 'duş kabul etmek', 'принимать душ', 'to wash under a shower', 'I have a shower every morning.', 'Her ertir duş kabul edýärin.', 'A1'),
    ('go online', '/ɡəʊ ˌɒnˈlaɪn/', 'PHR', 'onlaýn girmek', 'выходить в интернет', 'to use the internet', 'He goes online after dinner.', 'Agşam naharyndan soň onlaýn girýär.', 'A1', 'go online'),
    ('get a job', '/ɡet ə dʒɒb/', 'PHR', 'iş tapmak', 'находить работу', 'to start working somewhere', 'She got a job in a bank.', 'Bankda iş tapdy.', 'A2', 'get a job'),
    ('do exercise', '/duː ˈeksəsaɪz/', 'PHR', 'maşk etmek', 'делать упражнения', 'to train your body', 'I do exercise three times a week.', 'Hepdede üç gezek maşk edýärin.', 'A2'),
    ('have fun', '/hæv fʌn/', 'PHR', 'keýp etmek', 'веселиться', 'to enjoy yourself', 'We had fun at the party.', 'Toýda keýp etdik.', 'A1', 'have fun'),
    ('spell', '/spel/', 'V', 'harplap aýtmak', 'произносить по буквам', 'to say or write the letters of a word', 'How do you spell your name?', 'Adyňyzy nädip harplaýarsyňyz?', 'A1', 'spell a word'),
    ('capital letter', '/ˈkæpɪtl ˈletə(r)/', 'N', 'baş harp', 'заглавная буква', 'a big letter, e.g. A not a', 'Start the sentence with a capital letter.', 'Sözlemi baş harp bilen başla.', 'A2'),
    ('punctuation', '/ˌpʌŋktʃuˈeɪʃn/', 'N', 'durk bellikleri', 'пунктуация', 'marks like full stops and commas', 'Check your spelling and punctuation.', 'Ýazuwyňy we durk belliklerini barla.', 'B1'),
]

T['sequencers'] = [
    ('first', '/fɜːst/', 'ADV', 'ilki', 'сначала', 'before anything else', 'First, break the eggs.', 'Ilki ýumurtgalary döw.', 'A1'),
    ('then', '/ðen/', 'ADV', 'soňra', 'затем', 'after that; next', 'Then add the sugar.', 'Soňra şeker goş.', 'A1'),
    ('after that', '/ˈɑːftə ðæt/', 'PHR', 'şondan soň', 'после этого', 'following the thing just mentioned', 'After that, we went home.', 'Şondan soň öýe gitdik.', 'A2'),
    ('finally', '/ˈfaɪnəli/', 'ADV', 'iň soňunda', 'наконец', 'after a long time; the last thing', 'We finally arrived at midnight.', 'Iň soňunda gije ýarymda ýetdik.', 'A2'),
    ('suddenly', '/ˈsʌdənli/', 'ADV', 'birden', 'вдруг', 'quickly and without warning', 'Suddenly the lights went out.', 'Birden çyralar öçdi.', 'A2'),
    ('eventually', '/ɪˈventʃuəli/', 'ADV', 'aýagynda', 'в конце концов', 'in the end, after a long time', 'He eventually said yes.', 'Aýagynda hawa diýdi.', 'B1'),
    ('immediately', '/ɪˈmiːdiətli/', 'ADV', 'derrew', 'немедленно', 'at once; without delay', 'Come home immediately.', 'Derrew öýe gel.', 'A2'),
    ('meanwhile', '/ˈmiːnwaɪl/', 'ADV', 'şol wagtyň özünde', 'тем временем', 'during the same time', 'I cooked; meanwhile he set the table.', 'Men bişirdim; şol wagt ol süfra ýazdy.', 'B1'),
    ('while', '/waɪl/', 'CONJ', 'şol wagtda', 'в то время как', 'during the time that', 'She read while he slept.', 'Ol uklap ýatyrka ol okady.', 'A2'),
    ('as soon as', '/əz suːn əz/', 'CONJ', 'dessine', 'как только', 'immediately after something', 'I called her as soon as I heard.', 'Eşiden dessine oňa jaň etdim.', 'A2', 'as soon as possible'),
    ('at first', '/ət fɜːst/', 'PHR', 'başda', 'сначала', 'at the beginning', 'At first I was nervous.', 'Başda tolgunýardym.', 'A2'),
    ('in the end', '/ɪn ði end/', 'PHR', 'soňunda', 'в итоге', 'after everything happened', 'In the end we stayed at home.', 'Soňunda öýde galdyk.', 'A2', 'in the end'),
]

T['airports'] = [
    ('boarding pass', '/ˈbɔːdɪŋ pɑːs/', 'N', 'münüş kartasy', 'посадочный талон', 'a document that lets you get on a plane', 'Show your boarding pass at the gate.', 'Münüş kartany derwezede görkez.', 'A2', 'show your boarding pass'),
    ('check in', '/tʃek ɪn/', 'PHR', 'hasaba durmak', 'регистрироваться', 'to register at an airport or hotel', 'We checked in two hours early.', 'Iki sagat ir hasaba durduk.', 'A2', 'check in online'),
    ('customs', '/ˈkʌstəmz/', 'N', 'gümrük', 'таможня', 'the place where bags are checked at a border', 'It took an hour to get through customs.', 'Gümrükden geçmek bir sagat aldy.', 'A2', 'go through customs'),
    ('departure', '/dɪˈpɑːtʃə(r)/', 'N', 'ugrama', 'отправление', 'a plane leaving; the time it leaves', 'Check the departure time on the screen.', 'Ekrandan ugrama wagtyny barla.', 'A2', 'departure time'),
    ('gate', '/ɡeɪt/', 'N', 'derweze', 'выход на посадку', 'the door where you get on a plane', 'The flight leaves from gate 23.', 'Uçar 23-nji derwezeden gidýär.', 'A2', 'at the gate'),
    ('hand luggage', '/ˈhænd lʌɡɪdʒ/', 'N', 'el goşy', 'ручная кладь', 'a small bag you carry onto a plane', 'You can take one piece of hand luggage.', 'Bir el goşuny alyp bilersiňiz.', 'A2'),
    ('passport control', '/ˈpɑːspɔːt kənˈtrəʊl/', 'N', 'pasport gözegçiligi', 'паспортный контроль', 'where officials check passports', 'The queue at passport control was long.', 'Pasport gözegçiliginde nobat uzyn bolady.', 'A2'),
    ('security', '/sɪˈkjʊərəti/', 'N', 'howpsuzlyk barlagy', 'контроль безопасности', 'the place where you and your bags are checked', 'Take off your belt at security.', 'Howpsuzlykda kemeriňizi çykaryň.', 'A2', 'go through security'),
    ('terminal', '/ˈtɜːmɪnl/', 'N', 'terminal', 'терминал', 'a building at an airport', 'Our flight leaves from Terminal 2.', 'Uçarymyz 2-nji terminaldan gidýär.', 'A2'),
    ('take off', '/teɪk ɒf/', 'PHR', 'uçmak', 'взлетать', 'to leave the ground (plane)', 'The plane took off on time.', 'Uçar wagtynda uçdy.', 'A2', 'take off on time'),
    ('land', '/lænd/', 'V', 'gonmak', 'приземляться', 'to come down onto the ground', 'We landed in Istanbul at noon.', 'Günortan Stambulda gondyk.', 'A2', 'land safely'),
    ('arrivals', '/əˈraɪvlz/', 'N', 'geliş zaly', 'зона прибытия', 'the area where passengers arrive', 'I waited for her in arrivals.', 'Ony geliş zalynda garadym.', 'A2'),
    ('cancel', '/ˈkænsl/', 'V', 'ýatyrmak', 'отменять', 'to stop something planned', 'They cancelled the evening flight.', 'Agşamky uçary ýatyrdylar.', 'A2', 'cancel a flight'),
]

T['verbs_preps'] = [
    ('arrive in', '/əˈraɪv ɪn/', 'PHR', 'gelmek', 'прибывать в (город)', 'to reach a city or country', 'We arrived in London on Friday.', 'Anna güni Londona geldik.', 'A2', 'arrive in a city'),
    ('depend on', '/dɪˈpend ɒn/', 'PHR', 'bagly bolmak', 'зависеть от', 'to be decided by something else', 'It depends on the weather.', 'Howa bagly.', 'A2', 'depend on you'),
    ('laugh at', '/lɑːf æt/', 'PHR', 'gülmek', 'смеяться над', 'to smile or make sounds because something is funny', "Don't laugh at my mistakes.", 'Ýalňyşlaryma gülme.', 'A2', 'laugh at a joke'),
    ('think about', '/θɪŋk əˈbaʊt/', 'PHR', 'pikirlenmek', 'думать о', 'to have something in your mind', "I'm thinking about my holiday.", 'Dynç alyşym barada pikir edýärin.', 'A2', 'think about it'),
    ('belong to', '/bɪˈlɒŋ tuː/', 'PHR', 'degli bolmak', 'принадлежать', 'to be the property of someone', 'This bag belongs to me.', 'Bu sumka maňa degişli.', 'A2', 'belong to me'),
    ('consist of', '/kənˈsɪst əv/', 'PHR', 'ybarat bolmak', 'состоять из', 'to be made of parts', 'The test consists of three parts.', 'Synag üç bölümden ybarat.', 'B1', 'consist of parts'),
    ('look after', '/lʊk ˈɑːftə(r)/', 'PHR', 'göz-gulak bolmak', 'заботиться о', 'to take care of someone or something', 'She looks after her little brother.', 'Kiçi doganyna göz-gulak bolýar.', 'A2', 'look after children'),
    ('look forward to', '/lʊk ˈfɔːwəd tuː/', 'PHR', 'sabyrsyzlyk bilen garaşmak', 'с нетерпением ждать', 'to be excited about something coming', 'I look forward to seeing you.', 'Görüşmäge sabyrsyzlyk bilen garaşýaryn.', 'A2', 'look forward to meeting'),
    ('stay at', '/steɪ æt/', 'PHR', 'galmak', 'оставаться в', 'to live somewhere for a time', 'We stayed at a small hotel.', 'Kiçi myhmanhanada galdyk.', 'A2', 'stay at home'),
    ('listen to', '/ˈlɪsn tuː/', 'PHR', 'diňlemek', 'слушать (что-то)', 'to pay attention to sound or a person', 'I listen to music on the bus.', 'Awtobusda aýdym diňleýärin.', 'A1', 'listen to the radio'),
    ('wait for', '/weɪt fə(r)/', 'PHR', 'garamak', 'ждать (кого/что)', 'to stay until someone arrives', 'I am waiting for the bus.', 'Awtobusa garaýaryn.', 'A1', 'wait for the train'),
    ('talk about', '/tɔːk əˈbaʊt/', 'PHR', 'gürleşmek', 'говорить о', 'to discuss something', 'We talked about our plans.', 'Meýilnamalarymyz barada gürleşdik.', 'A2', 'talk about work'),
]

T['paraphrasing'] = [
    ('thing', '/θɪŋ/', 'N', 'zat', 'вещь', 'an object you cannot name', 'What is that thing on the table?', 'Stoluň üstündäki ol zat näme?', 'A1'),
    ('stuff', '/stʌf/', 'N', 'zatlar', 'вещи, всякое', 'things, especially when you do not name them', 'I left my stuff in the car.', 'Zatlarymy maşynda goýdum.', 'A2', 'all my stuff'),
    ('somebody', '/ˈsʌmbədi/', 'PRON', 'biri', 'кто-то', 'a person you do not name', 'Somebody called for you.', 'Biri seni sorady.', 'A2'),
    ('somewhere', '/ˈsʌmweə(r)/', 'ADV', 'bir ýerde', 'где-то', 'a place you do not name', 'I put it somewhere in this room.', 'Ony şu otagyň bir ýerine goýdum.', 'A2'),
    ('kind of', '/kaɪnd əv/', 'PHR', 'bir görnüş', 'вроде, типа', 'a type of something', 'It is a kind of bread.', 'Ol bir görnüş çörek.', 'A2', 'a kind of'),
    ('sort of', '/sɔːt əv/', 'PHR', 'bir görnüşli', 'что-то вроде', 'a type of something', 'We watched a sort of comedy.', 'Bir görnüş komediýa seretdik.', 'A2', 'a sort of'),
    ('actually', '/ˈæktʃuəli/', 'ADV', 'aslynda', 'на самом деле', 'in fact; really', 'Actually, I have never been there.', 'Aslynda, ol ýerde hiç wagt bolmadym.', 'A2'),
    ('basically', '/ˈbeɪsɪkli/', 'ADV', 'esasan', 'в основном', 'in the most important way', 'Basically, we just need more time.', 'Esasan, bize diňe köpräk wagt gerek.', 'B1'),
    ('etc.', '/et ˈsetərə/', 'ADV', 'we ş.m.', 'и т.д.', 'and other similar things', 'Buy fruit: apples, pears, etc.', 'Miwe al: alma, armut we ş.m.', 'A2'),
]

T['ed_ing_adjs'] = [
    ('bored', '/bɔːd/', 'ADJ', 'göwnüçökgün', 'скучающий', "feeling unhappy because something is not interesting", 'The children got bored at the museum.', 'Çagalar muzeýde göwnüçökgün boldy.', 'A2'),
    ('boring', '/ˈbɔːrɪŋ/', 'ADJ', 'gysgynç', 'скучный', 'not interesting', 'The film was really boring.', 'Film hakykatdan gysgynç boldy.', 'A2'),
    ('excited', '/ɪkˈsaɪtɪd/', 'ADJ', 'tolgunan', 'взволнованный', 'feeling happy about something coming', 'She was excited about the trip.', 'Syýahat barada tolgundy.', 'A2', 'excited about'),
    ('exciting', '/ɪkˈsaɪtɪŋ/', 'ADJ', 'tolgunçylykly', 'увлекательный', 'making you feel excited', 'It was an exciting match.', 'Tolgunçylykly oýun boldy.', 'A2'),
    ('interested', '/ˈɪntrəstɪd/', 'ADJ', 'gyzyklanýan', 'заинтересованный', 'wanting to know more about something', 'He is interested in history.', 'Taryha gyzyklanýar.', 'A1', 'interested in'),
    ('interesting', '/ˈɪntrəstɪŋ/', 'ADJ', 'gyzykly', 'интересный', 'making you want to know more', 'She told us an interesting story.', 'Gyzykly hekaýa gürrüň berdi.', 'A1'),
    ('surprised', '/səˈpraɪzd/', 'ADJ', 'geň galan', 'удивлённый', 'feeling surprise', 'I was surprised to see him.', 'Ony görüp geň galdym.', 'A2', 'surprised to see'),
    ('surprising', '/səˈpraɪzɪŋ/', 'ADJ', 'geň', 'удивительный', 'making you feel surprise', 'The news was surprising.', 'Habar geň boldy.', 'A2'),
    ('tired', '/ˈtaɪəd/', 'ADJ', 'ýadaw', 'уставший', 'needing sleep or rest', 'You look tired. Go to bed.', 'Ýadaw görünýärsiň. Ýat.', 'A1'),
    ('tiring', '/ˈtaɪərɪŋ/', 'ADJ', 'ýadadýan', 'утомительный', 'making you feel tired', 'It was a long tiring day.', 'Uzyn ýadadýan gün boldy.', 'A2'),
    ('amazed', '/əˈmeɪzd/', 'ADJ', 'haýran galan', 'изумлённый', 'feeling great surprise', 'We were amazed by the view.', 'Görnüşe haýran galdyk.', 'A2', 'amazed by'),
    ('amazing', '/əˈmeɪzɪŋ/', 'ADJ', 'haýran galdyryjy', 'изумительный', 'very good; causing surprise', 'The food was amazing.', 'Nahar ajaýyp bolady.', 'A2'),
    ('confused', '/kənˈfjuːzd/', 'ADJ', 'bulaşan', 'запутавшийся', 'unable to understand clearly', 'I got confused by the instructions.', 'Görkezmelerden bulaşdym.', 'A2', 'confused by'),
    ('confusing', '/kənˈfjuːzɪŋ/', 'ADJ', 'bulaşdyryjy', 'запутанный', 'difficult to understand', 'The rules are confusing.', 'Düzgünler bulaşdyryjy.', 'A2'),
    ('disappointed', '/ˌdɪsəˈpɔɪntɪd/', 'ADJ', 'lapykeç', 'разочарованный', 'unhappy because something was not as good as you hoped', 'She was disappointed with the result.', 'Netijeden lapykeç boldy.', 'A2', 'disappointed with'),
    ('disappointing', '/ˌdɪsəˈpɔɪntɪŋ/', 'ADJ', 'lapykeç ediji', 'разочаровывающий', 'not as good as you hoped', 'The concert was disappointing.', 'Konsert lapykeç ediji boldy.', 'A2'),
    ('embarrassed', '/ɪmˈbærəst/', 'ADJ', 'utançly', 'смущённый', 'feeling shy or ashamed', 'He felt embarrassed about his mistake.', 'Ýalňyşy üçin utançly boldy.', 'A2', 'embarrassed about'),
    ('embarrassing', '/ɪmˈbærəsɪŋ/', 'ADJ', 'utançly ýagdaý', 'неловкий', 'making you feel embarrassed', 'It was an embarrassing moment.', 'Utançly pursat boldy.', 'A2'),
    ('shocked', '/ʃɒkt/', 'ADJ', 'şok bolan', 'потрясённый', 'feeling sudden strong surprise', 'We were shocked by the news.', 'Habar bizi şok etdi.', 'A2', 'shocked by'),
    ('shocking', '/ˈʃɒkɪŋ/', 'ADJ', 'şok ediji', 'потрясающий (негативно)', 'very bad and surprising', 'The weather was shocking.', 'Howa şok ediji boldy.', 'A2'),
    ('frightened', '/ˈfraɪtnd/', 'ADJ', 'gorkan', 'испуганный', 'afraid; feeling fear', 'She was frightened of the dark.', 'Garanlykdan gorkýardy.', 'A2', 'frightened of'),
    ('frightening', '/ˈfraɪtnɪŋ/', 'ADJ', 'gorkuzýan', 'пугающий', 'making you feel fear', 'It was a frightening experience.', 'Gorkuzýan tejribe boldy.', 'A2'),
]

T['numbers_types'] = [
    ('half', '/hɑːf/', 'N', 'ýarym', 'половина', 'one of two equal parts', 'Cut the apple in half.', 'Almany ýarym kes.', 'A2', 'half an hour'),
    ('third', '/θɜːd/', 'ORD', 'üçden bir', 'треть', 'one of three equal parts', 'A third of the class was absent.', 'Sinpiň üçden biri ýokdy.', 'A2'),
    ('quarter', '/ˈkwɔːtə(r)/', 'N', 'dörtden bir', 'четверть', 'one of four equal parts', 'It takes a quarter of an hour.', 'On bäş minut alýar.', 'A2', 'a quarter past'),
    ('double', '/ˈdʌbl/', 'V', 'iki esse artdyrmak', 'удваивать', 'to become or make twice as much', 'The price doubled in two years.', 'Baha iki ýylda iki esse artdy.', 'A2', 'double in size'),
    ('twice', '/twaɪs/', 'ADV', 'iki gezek', 'дважды', 'two times', 'I have been there twice.', 'Ol ýerde iki gezek boldum.', 'A2', 'twice a week'),
    ('dozen', '/ˈdʌzn/', 'N', 'on ikilik', 'дюжина', 'the number twelve; a set of twelve', 'She bought two dozen eggs.', 'Iki on iki ýumurtga aldy.', 'B1', 'a dozen eggs'),
    ('a couple of', '/ə ˈkʌpl əv/', 'PHR', 'birnäçe', 'пара, несколько', 'two or a few', 'I need a couple of minutes.', 'Birnäçe minut gerek.', 'A2', 'a couple of days'),
    ('approximately', '/əˈprɒksɪmətli/', 'ADV', 'takmynan', 'приблизительно', 'about; not exactly', 'The trip costs approximately 500 manat.', 'Syýahat takmynan 500 manat durýar.', 'B1'),
    ('exactly', '/ɪɡˈzæktli/', 'ADV', 'takyk', 'точно', 'in a precise way; completely', 'The train leaves at exactly six.', 'Otly takyk altyda gidýär.', 'A2', 'exactly right'),
    ('per cent', '/pə ˈsent/', 'N', 'göterim', 'процент', 'one part in every hundred', 'Sixty per cent said yes.', 'Altmış göterim hawa diýdi.', 'A2', 'fifty per cent'),
    ('increase', '/ɪnˈkriːs/', 'V', 'köpeltmek', 'увеличивать(ся)', 'to become or make bigger', 'Sales increased by ten per cent.', 'Satuwlar on göterim artdy.', 'A2', 'increase by'),
    ('decrease', '/dɪˈkriːs/', 'V', 'azaltmak', 'уменьшать(ся)', 'to become or make smaller', 'The temperature decreased at night.', 'Gije temperatura azaldy.', 'A2', 'decrease by'),
]

T['health'] = [
    ('headache', '/ˈhedeɪk/', 'N', 'baş agyry', 'головная боль', 'pain in the head', 'I have a terrible headache.', 'Elhenç baş agyrym bar.', 'A2', 'have a headache'),
    ('stomach ache', '/ˈstʌmək eɪk/', 'N', 'garyn agyry', 'боль в животе', 'pain in the stomach', 'He has a stomach ache.', 'Onuň garyn agyrysy bar.', 'A2', 'have a stomach ache'),
    ('sore throat', '/sɔː θrəʊt/', 'N', 'bogaz agyry', 'больное горло', 'pain in the throat', 'I have a sore throat and a cough.', 'Bogaz agyrym we üsgülewügim bar.', 'A2', 'have a sore throat'),
    ('cough', '/kɒf/', 'N', 'üsgülewük', 'кашель', 'the act of forcing air out noisily', 'Her cough got worse at night.', 'Üsgülewügi gije ýaramazlaşdy.', 'A2', 'have a cough'),
    ('cold', '/kəʊld/', 'N', 'sowuklama', 'простуда', 'a common illness with a runny nose', 'I caught a cold last week.', 'Geçen hepde sowukladym.', 'A1', 'catch a cold'),
    ('flu', '/fluː/', 'N', 'dümew', 'грипп', 'an illness like a bad cold', 'She stayed home with the flu.', 'Dümew bilen öýde galdy.', 'A2', 'have the flu'),
    ('temperature', '/ˈtemprətʃə(r)/', 'N', 'gyzzyrma', 'температура', 'a body heat higher than normal', 'The baby has a high temperature.', 'Çaganyň gyzzyrmasy bar.', 'A2', 'have a temperature'),
    ('pain', '/peɪn/', 'N', 'agyry', 'боль', 'the feeling of hurting', 'He felt a sharp pain in his leg.', 'Aýagynda ýiti agyry duýdy.', 'A2', 'feel pain'),
    ('pill', '/pɪl/', 'N', 'derman kökesi', 'таблетка', 'a small round piece of medicine', 'Take two pills after food.', 'Nahardan soň iki köke iç.', 'A2', 'take a pill'),
    ('patient', '/ˈpeɪʃnt/', 'N', 'näsag', 'пациент', 'a person being treated by a doctor', 'The doctor saw twenty patients today.', 'Lukman şu gün ýigrimi näsaga seretdi.', 'A2'),
    ('dizzy', '/ˈdɪzi/', 'ADJ', 'başy aýlanan', 'испытывающий головокружение', 'feeling that everything is moving', 'I felt dizzy after the ride.', 'Atlanyşykdan soň başym aýlandy.', 'B1', 'feel dizzy'),
    ('hurt', '/hɜːt/', 'V', 'agyrtmak', 'болеть, причинять боль', 'to feel or cause pain', 'My back hurts when I sit.', 'Otyran wagtym arkam agyrýar.', 'A2'),
    ('ill', '/ɪl/', 'ADJ', 'näsag', 'больной', 'not well; sick', 'He has been ill for a week.', 'Bir hepdedir näsag.', 'A2', 'feel ill'),
    ('injured', '/ˈɪndʒəd/', 'ADJ', 'şikes alan', 'травмированный', 'hurt in an accident', 'Two players were injured.', 'Iki oýunçy şikes aldy.', 'A2'),
    ('recover', '/rɪˈkʌvə(r)/', 'V', 'sagalmak', 'выздоравливать', 'to become well again', 'She recovered quickly.', 'Ol çalt sagaldy.', 'B1', 'recover from'),
    ('blood', '/blʌd/', 'N', 'gan', 'кровь', 'the red liquid in your body', 'The doctor took some blood.', 'Lukman biraz gan aldy.', 'A2'),
    ('bones', '/bəʊnz/', 'N', 'süňkler', 'кости', 'the hard parts inside your body', 'Exercise is good for your bones.', 'Maşk süňkler üçin peýdaly.', 'A2'),
    ('heart', '/hɑːt/', 'N', 'ýürek', 'сердце', 'the part of your body that moves blood', 'Running is good for your heart.', 'Ylgaw ýürek üçin peýdaly.', 'A2'),
    ('liver', '/ˈlɪvə/', 'N', 'bagyr', 'печень', 'the part of your body that cleans your blood', 'Alcohol is bad for your liver.', 'Alkogol bagyr üçin zyýanly.', 'A2'),
    ('muscles', '/ˈmʌslz/', 'N', 'myşsalar', 'мышцы', 'the parts of your body that make you move', 'Swimming builds your muscles.', 'Ýüzmek myşsalary berkidýär.', 'A2'),
    ('teeth', '/tiːθ/', 'N', 'dişler', 'зубы', 'the hard white parts in your mouth', 'Clean your teeth twice a day.', 'Günde iki gezek dişleriňi arassala.', 'A2'),
    ('alcohol', '/ˈælkəhɒl/', 'N', 'alkogol', 'алкоголь', 'drinks like beer and wine', 'He never drinks alcohol.', 'Ol hiç wagt alkogol içmeýär.', 'A2'),
    ('worry', '/ˈwʌri/', 'V', 'alada etmek', 'беспокоиться', 'to feel unhappy about problems', "Don't worry about the exam.", 'Synag barada alada etme.', 'A2'),
]

T['verb_back'] = [
    ('call back', '/kɔːl bæk/', 'PHR', 'yzyna jaň etmek', 'перезванивать', 'to phone someone again', "I'll call you back later.", 'Soňra yzyna jaň ederin.', 'A2'),
    ('come back', '/kʌm bæk/', 'PHR', 'yzyna gelmek', 'возвращаться', 'to return to a place', 'When will you come back?', 'Haçan yzyňa gelýärsiň?', 'A1'),
    ('get back', '/ɡet bæk/', 'PHR', 'yzyna ýetmek', 'возвращаться (прибывать)', 'to arrive back', 'We got back at midnight.', 'Gije ýarymda yzymyza ýetdik.', 'A2', 'get back home'),
    ('give back', '/ɡɪv bæk/', 'PHR', 'yzyna bermek', 'возвращать', 'to return something you borrowed', 'Give back my book, please.', 'Kitabymy yzyna ber.', 'A2', 'give back the money'),
    ('go back', '/ɡəʊ bæk/', 'PHR', 'yzyna gitmek', 'возвращаться (уходить)', 'to return to a place', 'I want to go back to Spain.', 'Ispaniýa yzyna gitmek isleýärin.', 'A1', 'go back home'),
    ('pay back', '/peɪ bæk/', 'PHR', 'karzyňy gaýtarmak', 'возвращать (деньги)', 'to return money you borrowed', 'I will pay you back tomorrow.', 'Ertin puluňy yzyna bererin.', 'A2', 'pay back a loan'),
    ('put back', '/pʊt bæk/', 'PHR', 'yzyna goýmak', 'класть обратно', 'to put something where it was', 'Put the milk back in the fridge.', 'Süýdi sowadyja yzyna goý.', 'A2'),
    ('take back', '/teɪk bæk/', 'PHR', 'yzyna gaýtarmak', 'возвращать (в магазин)', 'to return something to a shop', 'I took the jacket back.', 'Kurtkany yzyna gaýtardym.', 'A2', 'take back to the shop'),
    ('talk back', '/tɔːk bæk/', 'PHR', 'jogap gaýtarmak', 'огрызаться', 'to answer someone rudely', 'Never talk back to your teacher.', 'Mugallyma hiç wagt jogap gaýtarma.', 'B1'),
    ('write back', '/raɪt bæk/', 'PHR', 'yzyna ýazmak', 'отвечать (письмом)', 'to reply to a message', 'She wrote back the same day.', 'Şol gün yzyna ýazdy.', 'A2', 'write back soon'),
]

T['modifiers'] = [
    ('quite', '/kwaɪt/', 'ADV', 'birneme', 'довольно', 'a little more than expected', 'The film was quite good.', 'Film birneme gowy bolady.', 'A2'),
    ('rather', '/ˈrɑːðə(r)/', 'ADV', 'biraz (güýçli)', 'довольно (сильно)', 'quite; more than expected', 'It was rather cold yesterday.', 'Düýn howa biraz sowuk bolady.', 'A2'),
    ('pretty', '/ˈprɪti/', 'ADV', 'gaty (gürlüşde)', 'довольно (разг.)', 'quite; fairly (informal)', 'The test was pretty easy.', 'Synag gaty aňsat bolady.', 'A2'),
    ('fairly', '/ˈfeəli/', 'ADV', 'birneme', 'весьма', 'quite; but not very', 'The hotel was fairly cheap.', 'Myhmanhana birneme arzan boldy.', 'B1'),
    ('really', '/ˈrɪəli/', 'ADV', 'hakykatdan', 'действительно', 'very; in a real way', 'I am really tired.', 'Hakykatdan ýadadym.', 'A1'),
    ('a bit', '/ə bɪt/', 'PHR', 'birjyk', 'немного', 'a small amount', 'The soup is a bit cold.', 'Çorba birjyk sowuk.', 'A2', 'a bit tired'),
    ('a little', '/ə ˈlɪtl/', 'PHR', 'biraz', 'немного (чуть)', 'a small amount', 'Speak a little more slowly.', 'Biraz haýal gürle.', 'A2'),
    ('slightly', '/ˈslaɪtli/', 'ADV', 'birjyk (az)', 'слегка', 'a little; not much', 'The price is slightly higher now.', 'Baha indi birjyk ýokary.', 'B1'),
    ('particularly', '/pəˈtɪkjələli/', 'ADV', 'aýratyn', 'особенно', 'especially; more than usual', "I wasn't particularly hungry.", 'Aýratyn aç däldim.', 'B1', 'not particularly'),
    ('absolutely', '/ˈæbsəluːtli/', 'ADV', 'düýbünden', 'абсолютно', 'completely', 'You are absolutely right.', 'Düýbünden dogry aýdýarsyň.', 'A2'),
    ('completely', '/kəmˈpliːtli/', 'ADV', 'doly', 'полностью', 'in every way; totally', 'I completely forgot your birthday.', 'Doglan günüňi doly ýatdan çykarypdym.', 'A2'),
    ('totally', '/ˈtəʊtəli/', 'ADV', 'düýbünden doly', 'совершенно', 'completely', 'The two brothers are totally different.', 'Iki dogan düýbünden başga.', 'A2'),
]

T['adj_preps'] = [
    ('afraid of', '/əˈfreɪd əv/', 'PHR', 'gorkýan', 'боящийся', 'feeling fear about something', 'She is afraid of flying.', 'Uçmakdan gorkýar.', 'A2', 'afraid of spiders'),
    ('angry with', '/ˈæŋɡri wɪð/', 'PHR', 'gaharly', 'злой на', 'feeling anger towards a person', 'My mum was angry with me.', 'Ejem menden gaharly boldy.', 'A2', 'angry with someone'),
    ('bad at', '/bæd æt/', 'PHR', 'erbet', 'плохой в', 'not good at something', 'I am bad at remembering names.', 'Atlary ýatda saklamakda erbet.', 'A2', 'bad at maths'),
    ('famous for', '/ˈfeɪməs fə(r)/', 'PHR', 'meşhur', 'известный чем-то', 'well known because of something', 'The city is famous for its carpets.', 'Şäher halyçylygy bilen meşhur.', 'A2', 'famous for food'),
    ('full of', '/fʊl əv/', 'PHR', 'doly', 'полный', 'containing a lot of something', 'The square was full of people.', 'Meýdança adamdan doludy.', 'A2', 'full of people'),
    ('good at', '/ɡʊd æt/', 'PHR', 'ussat', 'хороший в', 'able to do something well', 'He is good at football.', 'Futbolda ussat.', 'A2', 'good at languages'),
    ('keen on', '/kiːn ɒn/', 'PHR', 'höwesli', 'увлекающийся', 'very interested in something', 'She is keen on photography.', 'Surata düşürmäge höwesli.', 'B1', 'keen on music'),
    ('married to', '/ˈmærid tuː/', 'PHR', 'durmuşda', 'женатый на', 'having a husband or wife', 'She is married to a doctor.', 'Lukman bilen durmuşda.', 'A2', 'married to him'),
    ('proud of', '/praʊd əv/', 'PHR', 'buýsanýan', 'гордящийся', 'pleased about something you did', 'We are proud of our son.', 'Oglumyz bilen buýsanýarys.', 'A2', 'proud of you'),
    ('tired of', '/ˈtaɪəd əv/', 'PHR', 'ýadan', 'уставший от', 'bored with something repeated', 'I am tired of waiting.', 'Garaşmakdan ýadadym.', 'A2', 'tired of waiting'),
    ('worried about', '/ˈwʌrid əˈbaʊt/', 'PHR', 'alada', 'беспокоящийся о', 'feeling unhappy about possible problems', 'She is worried about the exam.', 'Synag barada alada edýär.', 'A2', 'worried about money'),
    ('similar to', '/ˈsɪmələ tuː/', 'PHR', 'meňzeş', 'похожий на', 'almost the same as something', 'Your coat is similar to mine.', 'Paltoň menkiňe meňzeş.', 'A2', 'similar to mine'),
]

T['adverbs_manner'] = [
    ('angrily', '/ˈæŋɡrɪli/', 'ADV', 'gaharly', 'сердито', 'in an angry way', 'She closed the door angrily.', 'Gapyny gaharly ýapdy.', 'A2'),
    ('badly', '/ˈbædli/', 'ADV', 'erbet', 'плохо', 'not well', 'He played badly in the first half.', 'Birinji ýarymda erbet oýnady.', 'A2'),
    ('carefully', '/ˈkeəfəli/', 'ADV', 'ünsli', 'осторожно, внимательно', 'in a careful way', 'Read the instructions carefully.', 'Görkezmeleri ünsli oka.', 'A2'),
    ('easily', '/ˈiːzɪli/', 'ADV', 'aňsatlyk bilen', 'легко', 'without difficulty', 'She easily won the race.', 'Ýaryşy aňsatlyk bilen utdy.', 'A2'),
    ('fast', '/fɑːst/', 'ADV', 'çalt', 'быстро', 'quickly', 'He drives too fast.', 'Gaty çalt sürýär.', 'A1'),
    ('hard', '/hɑːd/', 'ADV', 'yhlasy bilen', 'усердно', 'with a lot of effort', 'She works hard every day.', 'Her gün yhlasly işleýär.', 'A2', 'work hard'),
    ('hardly', '/ˈhɑːdli/', 'ADV', 'diýen ýaly hiç', 'едва, почти не', 'almost not at all', 'I hardly know him.', 'Ony diýen ýaly tanamaýaryn.', 'A2', 'hardly ever'),
    ('late', '/leɪt/', 'ADV', 'giç', 'поздно', 'after the expected time', 'The bus arrived late.', 'Awtobus giç geldi.', 'A1', 'arrive late'),
    ('luckily', '/ˈlʌkɪli/', 'ADV', 'bagtymyza', 'к счастью', 'fortunately', 'Luckily nobody was hurt.', 'Bagtymyza hiç kim şikes almady.', 'A2'),
    ('quickly', '/ˈkwɪkli/', 'ADV', 'çalt', 'быстро (скоро)', 'in a short time; with speed', 'Come quickly!', 'Çalt gel!', 'A1'),
    ('quietly', '/ˈkwaɪətli/', 'ADV', 'sessiz', 'тихо', 'without noise', 'She spoke quietly in his ear.', 'Gulagyna sessiz gepldi.', 'A2'),
    ('slowly', '/ˈsləʊli/', 'ADV', 'haýal', 'медленно', 'not quickly', 'Please speak slowly.', 'Haýal gürlemegiňizi haýyş edýärin.', 'A1'),
    ('well', '/wel/', 'ADV', 'gowy', 'хорошо', 'in a good way', 'He sings well.', 'Ol gowy aýdym aýdýar.', 'A1'),
]
T['animals'] = [
    ('ant', '/ænt/', 'N', 'garynja', 'муравей', 'a very small insect living in large groups', 'Ants carried a leaf across the path.', 'Garynjalar ýapragy ýoldan geçirdi.', 'A2'),
    ('bee', '/biː/', 'N', 'ary', 'пчела', 'a flying insect that makes honey', 'A bee landed on the flower.', 'Ary güle gondy.', 'A2'),
    ('beetle', '/ˈbiːtl/', 'N', 'möjek', 'жук', 'an insect with a hard shell', 'A large black beetle crawled past.', 'Uly gara möjek emekläp geçdi.', 'B1'),
    ('butterfly', '/ˈbʌtəflaɪ/', 'N', 'kebelek', 'бабочка', 'an insect with large colourful wings', 'Butterflies flew over the meadow.', 'Kebeleklar çemeniň üstünde uçdy.', 'A2'),
    ('crab', '/kræb/', 'N', 'ýengç', 'краб', 'a sea animal with a shell and ten legs', 'We found a crab under the rock.', 'Daşyň astyndan ýengç tapdyk.', 'B1'),
    ('fly', '/flaɪ/', 'N', 'siňek', 'муха', 'a common flying insect', 'There is a fly in my soup.', 'Çorbamda siňek bar.', 'A2'),
    ('frog', '/frɒɡ/', 'N', 'gurbaga', 'лягушка', 'a small animal that jumps and lives near water', 'Frogs were singing by the pond.', 'Gurbagalar howdanyň ýanynda aýdym aýdýardy.', 'A2'),
    ('mosquito', '/məˈskiːtəʊ/', 'N', 'çybyn', 'комар', 'a small insect that bites', 'Mosquitoes kept me awake all night.', 'Çybynlar bütin gije uky bermedi.', 'A2'),
    ('snake', '/sneɪk/', 'N', 'ýylan', 'змея', 'a long animal with no legs', 'A snake was crossing the road.', 'Ýylan ýoldan geçýärdi.', 'A2'),
    ('spider', '/ˈspaɪdə(r)/', 'N', 'möý', 'паук', 'an insect-like animal with eight legs', 'A big spider sat in the corner.', 'Uly möý burçda oturýardy.', 'A2'),
    ('whale', '/weɪl/', 'N', 'kit', 'кит', 'the largest animal in the sea', 'We saw a whale from the boat.', 'Gaýykdan kit gördük.', 'A2'),
    ('bat', '/bæt/', 'N', 'ýarganat', 'летучая мышь', 'a small animal that flies at night', 'Bats sleep in old buildings.', 'Ýarganatlar köne binalarda uklaýar.', 'B1'),
    ('dolphin', '/ˈdɒlfɪn/', 'N', 'delfin', 'дельфин', 'a clever sea animal', 'Dolphins followed our boat.', 'Delfinler gaýygymyzyň yzyndan ýüzdü.', 'A2'),
    ('eagle', '/ˈiːɡl/', 'N', 'bürgüt', 'орёл', 'a large strong bird', 'An eagle circled above the mountains.', 'Bürgüt daglaryň üstünde aýlandy.', 'B1'),
    ('owl', '/aʊl/', 'N', 'baýguş', 'сова', 'a bird that is active at night', 'An owl called in the dark forest.', 'Garaňky tokaýda baýguş gygyrdy.', 'B1'),
    ('shark', '/ʃɑːk/', 'N', 'akula', 'акула', 'a large dangerous fish', 'We did not swim because of the sharks.', 'Akulalar sebäpli ýüzmedik.', 'A2'),
    ('bear', '/beə/', 'N', 'aýy', 'медведь', 'a large heavy wild animal', 'We saw a bear in the forest.', 'Tokaýda aýy gördük.', 'A2'),
    ('bird', '/bɜːd/', 'N', 'guş', 'птица', 'an animal with wings and feathers', 'The birds are singing.', 'Guşlar aýdym aýdýar.', 'A1'),
    ('bull', '/bʊl/', 'N', 'öküz', 'бык', 'a male cow', 'The bull is dangerous.', 'Öküz howply.', 'A2'),
    ('camel', '/ˈkæml/', 'N', 'düýe', 'верблюд', 'a desert animal with humps', 'We rode a camel.', 'Düýä mündik.', 'A2'),
    ('chicken', '/ˈtʃɪkɪn/', 'N', 'towuk', 'курица', 'a farm bird', 'The chickens are in the garden.', 'Towuklar bagda.', 'A1'),
    ('cow', '/kaʊ/', 'N', 'sygyr', 'корова', 'a large farm animal that gives milk', 'The cow gives us milk.', 'Sygyr bize süýt berýär.', 'A2'),
    ('crocodile', '/ˈkrɒkədaɪl/', 'N', 'timsah', 'крокодил', 'a large reptile with big teeth', 'The crocodile waited in the river.', 'Timsah derýada garaşdy.', 'A2'),
    ('deer', '/dɪə/', 'N', 'maral', 'олень', 'a wild animal like a small horse with horns', 'A deer ran across the road.', 'Maral ýoldan ylgap geçdi.', 'A2'),
    ('elephant', '/ˈelɪfənt/', 'N', 'pil', 'слон', 'the largest land animal', 'The elephant has big ears.', 'Piliň uly gulaklary bar.', 'A2'),
    ('giraffe', '/dʒəˈrɑːf/', 'N', 'zürafa', 'жираф', 'a tall African animal with a long neck', 'The giraffe eats leaves from trees.', 'Zürafa agaçlaryň ýapraklaryny iýýär.', 'A2'),
    ('goat', '/ɡəʊt/', 'N', 'geçi', 'коза', 'a farm animal with horns', 'The goat climbed the hill.', 'Geçi depä dyrmaşdy.', 'A2'),
    ('horse', '/hɔːs/', 'N', 'at', 'лошадь', 'a large animal you can ride', 'She rides her horse every day.', 'Her gün atyna münýär.', 'A1'),
    ('kangaroo', '/ˌkæŋɡəˈruː/', 'N', 'kenguru', 'кенгуру', 'an Australian animal that jumps', 'The kangaroo carried its baby.', 'Kenguru çagasyny göterdi.', 'A2'),
    ('lion', '/ˈlaɪən/', 'N', 'arslan', 'лев', 'a large wild cat', 'The lion is the king of animals.', 'Arslan haýwanlaryň şasy.', 'A2'),
    ('mouse', '/maʊs/', 'N', 'syçan', 'мышь', 'a small furry animal', 'A mouse ran under the table.', 'Syçan stoluň aşagyndan ylgady.', 'A2'),
    ('pig', '/pɪɡ/', 'N', 'doňuz', 'свинья', 'a farm animal', 'The pigs are eating.', 'Doňuzlar iýýär.', 'A2'),
    ('rabbit', '/ˈræbɪt/', 'N', 'towşan', 'кролик', 'a small animal with long ears', 'The rabbit eats carrots.', 'Towşan käşir iýýär.', 'A2'),
    ('rat', '/ræt/', 'N', 'krysa', 'крыса', 'like a big mouse', 'A rat ran along the wall.', 'Krysa diwaryň boýun ylgady.', 'A2'),
    ('sheep', '/ʃiːp/', 'N', 'goýun', 'овца', 'a farm animal with wool', 'The sheep are in the field.', 'Goýunlar meýdanda.', 'A2'),
    ('tiger', '/ˈtaɪɡə/', 'N', 'ýolbars', 'тигр', 'a large wild cat with lines on its body', 'The tiger hunts at night.', 'Ýolbars gije awlaýar.', 'A2'),
    ('wasp', '/wɒsp/', 'N', 'eşek arysy', 'оса', 'a flying insect that can sting', 'A wasp is in the kitchen.', 'Aşhanada eşek arysy bar.', 'A2'),
    ('jellyfish', '/ˈdʒelifɪʃ/', 'N', 'meduza', 'медуза', 'a soft sea animal', 'Do not touch the jellyfish.', 'Meduza el degirme.', 'A2'),
]

T['fear'] = [
    ('scared', '/skeəd/', 'ADJ', 'gorkan', 'испуганный', 'afraid; feeling fear', 'The little boy was scared of dogs.', 'Kiçi oglan itlerden gorkýardy.', 'A2', 'scared of'),
    ('terrified', '/ˈterɪfaɪd/', 'ADJ', 'elhenç gorkan', 'в ужасе', 'very scared', 'She is terrified of heights.', 'Beýiklikden elhenç gorkýar.', 'B1', 'terrified of heights'),
    ('horror', '/ˈhɒrə(r)/', 'N', 'elhençlik', 'ужас', 'great fear; a film type about fear', 'He watched a horror film alone.', 'Elhençlik filmini ýeke gördi.', 'A2', 'a horror film'),
    ('nightmare', '/ˈnaɪtmeə(r)/', 'N', 'gabus', 'кошмар', 'a frightening dream', 'I had a nightmare last night.', 'Düýn gije gabus gördüm.', 'A2', 'have a nightmare'),
    ('scream', '/skriːm/', 'V', 'gygyrmak', 'кричать (от страха)', 'to make a loud high sound from fear', 'She screamed when she saw the spider.', 'Möýi görüp gygyrdy.', 'A2', 'scream in fear'),
    ('shout', '/ʃaʊt/', 'V', 'sesli gygyrmak', 'кричать (громко)', 'to say something very loudly', 'He shouted for help.', 'Kömek sorap gygyrdy.', 'A2', 'shout for help'),
    ('panic', '/ˈpænɪk/', 'N', 'howp', 'паника', 'sudden uncontrollable fear', "Don't panic — we will find a way.", 'Howp etme — ýol taparys.', 'B1', "don't panic"),
    ('shake', '/ʃeɪk/', 'V', 'titremek', 'дрожать', 'to move quickly from fear or cold', 'His hands were shaking.', 'Elleri titräp durdy.', 'A2', 'shake with fear'),
    ('tremble', '/ˈtrembl/', 'V', 'gorkudan titremek', 'трястись', 'to shake because of fear', 'Her voice trembled as she spoke.', 'Gürände sesi titredi.', 'B1'),
    ('nervous', '/ˈnɜːvəs/', 'ADJ', 'tolgunan', 'нервничающий', 'worried and not relaxed', 'I felt nervous before the exam.', 'Synagdan öň tolgundym.', 'A2', 'feel nervous'),
]

T['biographies'] = [
    ('born', '/bɔːn/', 'ADJ', 'doğan', 'родившийся', 'used to say where or when someone started life', 'She was born in 1990.', '1990-njy ýylda dogdy.', 'A2', 'born in'),
    ('die', '/daɪ/', 'V', 'aradan çykmak', 'умирать', 'to stop living', 'The famous poet died young.', 'Meşhur şahy ýaşlygyna aradan çykdy.', 'A2', 'die young'),
    ('dead', '/ded/', 'ADJ', 'öli', 'мёртвый', 'not alive', 'The tree has been dead for years.', 'Agaç ýyllar öň gurapdyr.', 'A2'),
    ('grow up', '/ɡrəʊ ʌp/', 'PHR', 'ulalmak', 'взрослеть', 'to become an adult', 'He grew up in a small village.', 'Kiçi obada ulaldy.', 'A2', 'grow up in'),
    ('marry', '/ˈmæri/', 'V', 'öýlenmek', 'жениться', 'to become husband and wife', 'They married in the spring.', 'Ýaz aýynda öýlendiler.', 'A2', 'marry young'),
    ('retire', '/rɪˈtaɪə(r)/', 'V', 'pensiýa çykmak', 'уходить на пенсию', 'to stop working because of age', 'My father retired last year.', 'Kakam geçen ýyl pensiýa çykdy.', 'A2', 'retire from work'),
    ('career', '/kəˈrɪə(r)/', 'N', 'kär durmuşy', 'карьера', 'a job or profession over many years', 'She had a long career in medicine.', 'Lukmançylykda uzak kär durmuşy boldy.', 'A2', 'a successful career'),
    ('achievement', '/əˈtʃiːvmənt/', 'N', 'üstünlik', 'достижение', 'something important you succeed in doing', 'Winning the prize was a great achievement.', 'Baýragy almak uly üstünlik boldy.', 'B1', 'a great achievement'),
    ('invent', '/ɪnˈvent/', 'V', 'oýlap tapmak', 'изобретать', 'to create something for the first time', 'He invented a new kind of engine.', 'Täze görnüşli hereketlendiriji oýlap tapdy.', 'A2', 'invent a machine'),
    ('discover', '/dɪˈskʌvə(r)/', 'V', 'üstüni açmak', 'открывать (находить)', 'to find something for the first time', 'Scientists discovered a new planet.', 'Alymlar täze planetanyň üstüni açdy.', 'A2', 'discover a place'),
    ('writer', '/ˈraɪtə(r)/', 'N', 'ýazyjy', 'писатель', 'a person who writes books', 'The writer won two prizes.', 'Ýazyjy iki baýrak aldy.', 'A1', 'a famous writer'),
    ('poet', '/ˈpəʊɪt/', 'N', 'şahyr', 'поэт', 'a person who writes poems', 'Magtymguly is a great Turkmen poet.', 'Magtymguly beýik türkmen şahyry.', 'A2'),
    ('novelist', '/ˈnɒvəlɪst/', 'N', 'romançy', 'романист', 'a person who writes long stories', 'The novelist lives in London.', 'Romançy Londonda ýaşaýar.', 'B1'),
    ('painter', '/ˈpeɪntə(r)/', 'N', 'suratkeş', 'художник', 'a person who paints pictures', 'The painter showed us her work.', 'Suratkeş bize işlerini görkezdi.', 'A2'),
]

T['nationalities'] = [
    ('Brazilian', '/brəˈzɪliən/', 'ADJ', 'braziliýaly', 'бразильский', 'from Brazil', 'She has a Brazilian friend.', 'Braziliýaly dosty bar.', 'A2'),
    ('Chinese', '/ˌtʃaɪˈniːz/', 'ADJ', 'hytaýly', 'китайский', 'from China', 'We ate at a Chinese restaurant.', 'Hytaý restoranynda naharlandyk.', 'A1'),
    ('Dutch', '/dʌtʃ/', 'ADJ', 'gollandiýaly', 'голландский', 'from the Netherlands', 'The Dutch engineer works here.', 'Gollandiýaly inžener şu ýerde işleýär.', 'A2'),
    ('Greek', '/ɡriːk/', 'ADJ', 'grek', 'греческий', 'from Greece', 'I love Greek food.', 'Grek naharyny söýýärin.', 'A2'),
    ('Japanese', '/ˌdʒæpəˈniːz/', 'ADJ', 'ýaponiýaly', 'японский', 'from Japan', 'He drives a Japanese car.', 'Ýapon maşynyny sürýär.', 'A1'),
    ('Polish', '/ˈpɒlɪʃ/', 'ADJ', 'polýak', 'польский', 'from Poland', 'My neighbour is Polish.', 'Goňşum polýak.', 'A2'),
    ('Portuguese', '/ˌpɔːtʃəˈɡiːz/', 'ADJ', 'portugaliýaly', 'португальский', 'from Portugal', 'She speaks Portuguese.', 'Portugalça gürleýär.', 'A2'),
    ('Swedish', '/ˈswiːdɪʃ/', 'ADJ', 'şwesiýaly', 'шведский', 'from Sweden', 'The Swedish team won.', 'Şwesiýa topary utdy.', 'A2'),
    ('Swiss', '/swɪs/', 'ADJ', 'şweýsariýaly', 'швейцарский', 'from Switzerland', 'He bought a Swiss watch.', 'Şweýsariýa sagadyny satyn aldy.', 'A2'),
    ('Thai', '/taɪ/', 'ADJ', 'taýlandly', 'тайский', 'from Thailand', 'Thai food is often spicy.', 'Taýland nahary köplenç ajy.', 'A2'),
    ('Turkish', '/ˈtɜːkɪʃ/', 'ADJ', 'türk', 'турецкий', 'from Turkey', 'We visited the Turkish market.', 'Türk bazaryna baryp gördük.', 'A2'),
    ('Ukrainian', '/juːˈkreɪniən/', 'ADJ', 'ukrainaly', 'украинский', 'from Ukraine', 'Our Ukrainian colleague joined us.', 'Ukrainaly işdeşimiz bize goşuldy.', 'A2'),
    ('Vietnamese', '/ˌvjetnəˈmiːz/', 'ADJ', 'wýetnamly', 'вьетнамский', 'from Vietnam', 'Vietnamese coffee is very strong.', 'Wýetnam kofesi gaty güýçli.', 'B1'),
    ('Indian', '/ˈɪndiən/', 'ADJ', 'hindi', 'индийский', 'from India', 'The Indian restaurant is new.', 'Hindi restorany täze.', 'A1'),
]

T['school_subjects'] = [
    ('biology', '/baɪˈɒlədʒi/', 'N', 'biologiýa', 'биология', 'the study of living things', 'Biology is my favourite subject.', 'Biologiýa meniň iň söýýän predmetim.', 'A2'),
    ('chemistry', '/ˈkemɪstri/', 'N', 'himiýa', 'химия', 'the study of substances', 'We did an experiment in chemistry.', 'Himiýada tejribe etdik.', 'A2'),
    ('physics', '/ˈfɪzɪks/', 'N', 'fizika', 'физика', 'the study of energy and matter', 'Physics was difficult for me.', 'Fizika maňa kyn boldy.', 'A2'),
    ('geography', '/dʒiˈɒɡrəfi/', 'N', 'geografiýa', 'география', 'the study of the earth and countries', 'We studied maps in geography.', 'Geografiýada kartalary öwrendik.', 'A2'),
    ('history', '/ˈhɪstri/', 'N', 'taryh', 'история', 'the study of the past', 'The history lesson was fascinating.', 'Taryh sapagy örän gyzykly boldy.', 'A1'),
    ('literature', '/ˈlɪtrətʃə(r)/', 'N', 'edebiýat', 'литература', 'the study of books and poems', 'We read poems in literature.', 'Edebiýatda goşgulary okadyk.', 'A2'),
    ('maths', '/mæθs/', 'N', 'matematika', 'математика', 'the study of numbers', 'Maths starts at nine.', 'Matematika dokuzda başlaýar.', 'A1'),
    ('science', '/ˈsaɪəns/', 'N', 'ylym', 'наука', 'the study of the natural world', 'Children love science experiments.', 'Çagalar ylym tejribelerini söýýär.', 'A2'),
    ('art', '/ɑːt/', 'N', 'surat sapagy', 'искусство (предмет)', 'drawing and painting as a subject', 'We painted landscapes in art.', 'Surat sapagynda peýzažlary suratlandyrdyk.', 'A1'),
    ('drama', '/ˈdrɑːmə/', 'N', 'teatr sapagy', 'драма', 'acting as a school subject', 'She joined the drama club.', 'Teatr toparyna goşuldy.', 'A2', 'drama club'),
    ('timetable', '/ˈtaɪmteɪbl/', 'N', 'sapak tertibi', 'расписание', 'a plan of when lessons happen', 'Check the timetable for Monday.', 'Duşenbe üçin sapak tertibini barla.', 'A2', 'school timetable'),
    ('term', '/tɜːm/', 'N', 'okuw çärýegi', 'четверть, семестр', 'one of the parts of the school year', 'The exams are at the end of term.', 'Synaglar çärýegiň ahyrynda.', 'A2', 'this term'),
]

T['noun_formation'] = [
    ('actor', '/ˈæktə(r)/', 'N', 'aktýor', 'актёр', 'a person who acts in films or plays', 'The actor learned his lines quickly.', 'Aktýor öz sözlerini çalt ýat aldy.', 'A2'),
    ('artist', '/ˈɑːtɪst/', 'N', 'suratkeş (sungat)', 'художник, артист', 'a person who makes art', 'The artist painted the wall.', 'Suratkeş diwary suratlandyrdy.', 'A2'),
    ('designer', '/dɪˈzaɪnə(r)/', 'N', 'dizaýner', 'дизайнер', 'a person who plans how things look', 'She works as a fashion designer.', 'Moda dizaýneri bolup işleýär.', 'A2', 'fashion designer'),
    ('engineer', '/ˌendʒɪˈnɪə(r)/', 'N', 'inžener', 'инженер', 'a person who builds machines or roads', 'My brother is a software engineer.', 'Doganym programma inženeri.', 'A2', 'software engineer'),
    ('journalist', '/ˈdʒɜːnəlɪst/', 'N', 'žurnalist', 'журналист', 'a person who writes news', 'The journalist asked difficult questions.', 'Žurnalist kyn soraglar berdi.', 'A2'),
    ('musician', '/mjuˈzɪʃn/', 'N', 'sazanda', 'музыкант', 'a person who plays or writes music', 'The musician played for two hours.', 'Sazanda iki sagat çaldy.', 'A2'),
    ('scientist', '/ˈsaɪəntɪst/', 'N', 'alym', 'учёный', 'a person who does science', 'The scientist published her results.', 'Alym netijelerini çap etdi.', 'A2'),
    ('politician', '/ˌpɒləˈtɪʃn/', 'N', 'syýasatçy', 'политик', 'a person working in government', 'The politician answered questions.', 'Syýasatçy soraglara jogap berdi.', 'A2'),
    ('decision', '/dɪˈsɪʒn/', 'N', 'karar', 'решение', 'a choice you make', 'It was a difficult decision.', 'Kyn karar boldy.', 'A2', 'make a decision'),
    ('development', '/dɪˈveləpmənt/', 'N', 'ösüş', 'развитие', 'the process of growing or changing', 'The city has seen rapid development.', 'Şäher çalt ösüş gördi.', 'B1', 'economic development'),
    ('difference', '/ˈdɪfrəns/', 'N', 'tapawut', 'разница', 'the way things are not the same', 'There is a big difference between them.', 'Olaryň arasynda uly tapawut bar.', 'A2', 'tell the difference'),
    ('importance', '/ɪmˈpɔːtns/', 'N', 'ähmiýet', 'важность', 'why something matters', 'She explained the importance of sleep.', 'Ukynyň ähmiýetini düşündirdi.', 'B1', 'of great importance'),
    ('movement', '/ˈmuːvmənt/', 'N', 'hereket', 'движение', 'the act of changing position', 'The dancer made slow movements.', 'Tansçy haýal hereketler etdi.', 'A2', 'a sudden movement'),
    ('pollution', '/pəˈluːʃn/', 'N', 'hapalanma', 'загрязнение', 'damage to air, water or land', 'Pollution is a serious problem.', 'Hapalanma çynlakaý mesele.', 'A2', 'air pollution'),
    ('solution', '/səˈluːʃn/', 'N', 'çözgüt', 'решение (проблемы)', 'the answer to a problem', 'We found a simple solution.', 'Ýönekeý çözgüt tapdyk.', 'A2', 'find a solution'),
    ('success', '/səkˈses/', 'N', 'üstünlik (netije)', 'успех', 'when you achieve what you want', 'The shop was a great success.', 'Dükan uly üstünlik gazandy.', 'A2', 'a big success'),
    ('advice', '/ədˈvaɪs/', 'N', 'maslahat', 'совет', 'helpful words about what to do', 'She gave me good advice.', 'Maňa gowy maslahat berdi.', 'A2'),
    ('competition', '/ˌkɒmpəˈtɪʃn/', 'N', 'bäsleşik', 'соревнование', 'an event where people try to win', 'He won a photo competition.', 'Foto bäsleşiginde ýeňdi.', 'A2'),
    ('invention', '/ɪnˈvenʃn/', 'N', 'oýlap tapyş', 'изобретение', 'a new thing that someone makes for the first time', 'The internet is a great invention.', 'Internet beýik oýlap tapyş.', 'A2'),
    ('invitation', '/ˌɪnvɪˈteɪʃn/', 'N', 'çakylyk', 'приглашение', 'a message asking you to come', 'Thank you for the invitation.', 'Çakylyk üçin sag boluň.', 'A2'),
    ('advise', '/ədˈvaɪz/', 'V', 'maslahat bermek', 'советовать', 'to tell someone what they should do', 'I advise you to wait.', 'Saňa garaşmagy maslahat berýärin.', 'A2'),
    ('compete', '/kəmˈpiːt/', 'V', 'bäsleşmek', 'соревноваться', 'to try to win against others', 'They compete in swimming.', 'Ýüzmekde bäsleşýärler.', 'A2'),
    ('confuse', '/kənˈfjuːz/', 'V', 'çaşdyrmak', 'смущать, путать', 'to make something difficult to understand', 'The rules confused me.', 'Kadalar meni çaşdyrdy.', 'A2'),
    ('educate', '/ˈedʒukeɪt/', 'V', 'bilim bermek', 'обучать', 'to teach someone at school or university', 'She was educated in England.', 'Ol Angliýada bilim aldy.', 'A2'),
    ('invite', '/ɪnˈvaɪt/', 'V', 'çagyrmak', 'приглашать', 'to ask someone to come somewhere', 'They invited us to dinner.', 'Bizi agşamlyk nahara çagyrdylar.', 'A2'),
    ('pronounce', '/prəˈnaʊns/', 'V', 'telaffuz etmek', 'произносить', 'to say a word', 'How do you pronounce your name?', 'Adyňy nähili telaffuz etmeli?', 'A2'),
    ('revise', '/rɪˈvaɪz/', 'V', 'gaýtalamak', 'повторять (материал перед экзаменом)', 'to study again before an exam', 'I revised all weekend.', 'Bütin hepde ahyry gaýtaladym.', 'A2'),
    ('succeed', '/səkˈsiːd/', 'V', 'üstünlik gazanmak', 'преуспевать', 'to do what you wanted to do', 'She succeeded in the end.', 'Ahyrynda üstünlik gazandy.', 'A2'),
    ('hairdryer', '/ˈheədraɪə/', 'N', 'saç guradyjy', 'фен', 'a machine that dries your hair', 'I use a hairdryer every morning.', 'Her irden saç guradyjy ulanýaryn.', 'A2'),
    ('raincoat', '/ˈreɪnkəʊt/', 'N', 'ýagyş plashy', 'дождевик', 'a coat you wear in the rain', 'Take your raincoat, it is raining.', 'Ýagyş plashyňy al, ýagyş ýagýar.', 'A2'),
]

T['similarities'] = [
    ('both', '/bəʊθ/', 'DET', 'ikisi hem', 'оба', 'the two together', 'Both sisters live abroad.', 'Iki uýa hem daşary ýurtda ýaşaýar.', 'A1', 'both of them'),
    ('neither', '/ˈnaɪðə(r)/', 'DET', 'hiç haýsysy', 'ни тот ни другой', 'not one and not the other', 'Neither answer was correct.', 'Hiç haýsy jogap dogry däldi.', 'A2', 'neither of us'),
    ('either', '/ˈaɪðə(r)/', 'DET', 'islendigi', 'любой из двух', 'one or the other', 'You can take either bus.', 'Islendik awtobusa münüp bilersiň.', 'A2', 'either side'),
    ('the same as', '/ðə seɪm əz/', 'PHR', 'birmeňzeş', 'такой же, как', 'exactly like something else', 'My bag is the same as yours.', 'Sumkam senkiň bilen birmeňzeş.', 'A2', 'the same as mine'),
    ('different from', '/ˈdɪfrənt frɒm/', 'PHR', 'tapawutly', 'отличающийся от', 'not the same as', 'Life here is different from the city.', 'Bu ýerdäki durmuş şäherden tapawutly.', 'A2', 'different from mine'),
    ('in common', '/ɪn ˈkɒmən/', 'PHR', 'meňzeşlik', 'общее', 'shared interests or features', 'The twins have a lot in common.', 'Ekizleriň köp meňzeşligi bar.', 'A2', 'have things in common'),
    ('alike', '/əˈlaɪk/', 'ADV', 'meňzeş', 'похоже', 'in the same way', 'The brothers look alike.', 'Doganlar meňzeş görünýär.', 'A2', 'look alike'),
    ('unlike', '/ˌʌnˈlaɪk/', 'PREP', 'tapawutlylykda', 'в отличие от', 'different from', 'Unlike his brother, he is quiet.', 'Doganyndan tapawutlylykda, ol sessiz.', 'A2', 'unlike me'),
    ('although', '/ɔːlˈðəʊ/', 'CONJ', 'bolsa-da', 'хотя', 'even though', 'Although it rained, we went out.', 'Ýagyş ýagsa-da, çykdys.', 'A2'),
    ('however', '/haʊˈevə(r)/', 'ADV', 'şonda-da', 'однако', 'but; on the other hand', 'It was cheap. However, it broke quickly.', 'Arzandy. Şonda-da, çalt döwüldi.', 'A2'),
]

T['time_expressions'] = [
    ('already', '/ɔːlˈredi/', 'ADV', 'eýýäm', 'уже', 'before now or before expected', 'We have already eaten.', 'Eýýäm naharlandyk.', 'A2'),
    ('yet', '/jet/', 'ADV', 'entek', 'ещё (в вопросах)', 'until now (in questions and negatives)', 'Have you finished yet?', 'Entek gutardyňmy?', 'A2', 'not yet'),
    ('just', '/dʒʌst/', 'ADV', 'ýaňyja', 'только что', 'a very short time ago', 'She has just left.', 'Ol ýaňyja gitdi.', 'A2', 'just arrived'),
    ('still', '/stɪl/', 'ADV', 'heniz hem', 'всё ещё', 'up to now; continuing', 'He is still at work.', 'Ol heniz hem işde.', 'A2', 'still waiting'),
    ('recently', '/ˈriːsntli/', 'ADV', 'ýaňy-ýakynda', 'недавно', 'not long ago', 'I have recently changed jobs.', 'Ýaňy-ýakynda işimi üýtgetdim.', 'A2'),
    ('ever', '/ˈevə(r)/', 'ADV', 'hiç', 'когда-либо', 'at any time', 'Have you ever been to Italy?', 'Italiýada hiç bolduňmy?', 'A2', 'have you ever'),
    ('never', '/ˈnevə(r)/', 'ADV', 'hiç haçan', 'никогда', 'not at any time', 'I have never flown before.', 'Öň hiç wagt uçmadym.', 'A1'),
    ('forever', '/fərˈevə(r)/', 'ADV', 'hemişelik', 'навсегда', 'for all time', 'We will remember this day forever.', 'Bu güni hemişelik ýatda saklarys.', 'A2'),
    ('nowadays', '/ˈnaʊədeɪz/', 'ADV', 'häzirki wagtda', 'в наше время', 'now, compared with the past', 'Nowadays everyone has a phone.', 'Häzirki wagtda hemmeleriň telefony bar.', 'B1'),
    ('in the past', '/ɪn ðə pɑːst/', 'PHR', 'geçmişde', 'в прошлом', 'at an earlier time', 'People travelled less in the past.', 'Geçmişde adamlar az syýahat edýärdi.', 'A2', 'in the past'),
    ('ago', '/əˈɡəʊ/', 'ADV', 'öň', 'назад (о времени)', 'before now', 'She moved here two years ago.', 'Iki ýyl öň bu ýere göçdi.', 'A1', 'two days ago'),
    ('soon', '/suːn/', 'ADV', 'tiz', 'скоро', 'after a short time', 'See you soon!', 'Tiz görüşeris!', 'A1', 'as soon as possible'),
]

T['say_tell'] = [
    ('mention', '/ˈmenʃn/', 'V', 'agzamak', 'упоминать', 'to speak about something briefly', 'He mentioned the party but not the time.', 'Toýy agzady, ýöne wagtyny aýtmady.', 'A2', 'mention that'),
    ('explain', '/ɪkˈspleɪn/', 'V', 'düşündirmek', 'объяснять', 'to make something clear', 'Can you explain this word?', 'Şu sözi düşündirip bilersiňmi?', 'A2', 'explain how'),
    ('ask', '/ɑːsk/', 'V', 'soramak', 'спрашивать', 'to put a question', 'She asked me my name.', 'Adymy sorady.', 'A1', 'ask a question'),
    ('answer', '/ˈɑːnsə(r)/', 'V', 'jogap bermek', 'отвечать', 'to reply to a question', 'He answered every question.', 'Her soraga jogap berdi.', 'A1', 'answer the phone'),
    ('reply', '/rɪˈplaɪ/', 'V', 'jogap ýazmak', 'отвечать (письменно)', 'to answer in writing or speech', 'She replied to my email quickly.', 'Emailyma çalt jogap berdi.', 'A2', 'reply to'),
    ('describe', '/dɪˈskraɪb/', 'V', 'wasyp bermek', 'описывать', 'to say what something is like', 'Describe the man you saw.', 'Gören adamyny wasyp et.', 'A2', 'describe in detail'),
    ('discuss', '/dɪˈskʌs/', 'V', 'ara alyp maslahatlaşmak', 'обсуждать', 'to talk about something together', 'We discussed the plan for an hour.', 'Meýilnamany bir sagat ara alyp maslahatlaşdyk.', 'A2', 'discuss a problem'),
    ('argue', '/ˈɑːɡjuː/', 'V', 'jedelleşmek', 'спорить', 'to speak angrily because you disagree', 'They argued about money.', 'Pul barada jedelleşdiler.', 'A2', 'argue with'),
    ('complain', '/kəmˈpleɪn/', 'V', 'zeýrenmek', 'жаловаться', 'to say you are not happy about something', 'He complained about the noise.', 'Goh barada zeýrendi.', 'A2', 'complain about'),
    ('inform', '/ɪnˈfɔːm/', 'V', 'habar bermek', 'информировать', 'to tell someone facts officially', 'Please inform us of any changes.', 'Üýtgeşmeler barada habar bermegiňizi haýyş edýäris.', 'B1', 'inform us'),
    ('admit', '/ədˈmɪt/', 'V', 'boýun almak', 'признавать', 'to agree something is true', 'She admitted her mistake.', 'Ýalňyşyny boýun aldy.', 'A2', 'admit that'),
    ('deny', '/dɪˈnaɪ/', 'V', 'inkär etmek', 'отрицать', 'to say something is not true', 'He denied taking the money.', 'Puly alandygyny inkär etdi.', 'B1', 'deny doing'),
    ('warn', '/wɔːn/', 'V', 'duýdurmak', 'предупреждать', 'to tell someone about a danger', 'They warned us about the storm.', 'Tupan barada duýdurdy.', 'A2', 'warn about'),
    ('announce', '/əˈnaʊns/', 'V', 'yglan etmek', 'объявлять', 'to tell people officially', 'They announced the winner on stage.', 'Ýeňijini sahnada yglan etdiler.', 'B1', 'announce the results'),
]

T['question_words'] = [
    ('how often', '/haʊ ˈɒfn/', 'PHR', 'näçe ýygy-ýygydan', 'как часто', 'asking about frequency', 'How often do you study English?', 'Iňlis dilini näçe ýygy-ýygydan okaýarsyň?', 'A1', 'how often'),
    ('how long', '/haʊ lɒŋ/', 'PHR', 'näçe wagt', 'как долго', 'asking about time length', 'How long is the film?', 'Film näçe wagt?', 'A1', 'how long'),
    ('how far', '/haʊ fɑː(r)/', 'PHR', 'näçe uzak', 'как далеко', 'asking about distance', 'How far is the airport?', 'Aeroport näçe uzakda?', 'A2', 'how far'),
    ('how much', '/haʊ mʌtʃ/', 'PHR', 'näçe (hasap)', 'сколько (неисчисл.)', 'asking about amount or price', 'How much is this jacket?', 'Bu kurtka näçe?', 'A1', 'how much'),
    ('how many', '/haʊ ˈmeni/', 'PHR', 'näçe (san)', 'сколько (исчисл.)', 'asking about number', 'How many people came?', 'Näçe adam geldi?', 'A1', 'how many'),
    ('whose', '/huːz/', 'PRON', 'kiminiňki', 'чей', 'asking who something belongs to', 'Whose phone is this?', 'Bu kiminiň telefony?', 'A2', 'whose bag'),
    ('which', '/wɪtʃ/', 'DET', 'haýsy', 'который', 'asking what thing from a group', 'Which colour do you prefer?', 'Haýsy reňki gowy görýärsiň?', 'A1', 'which one'),
    ('what ... like', '/wɒt laɪk/', 'PHR', 'nähili', 'какой', 'asking about qualities', "What's the weather like?", 'Howa nähili?', 'A2', "what's it like"),
    ('what ... for', '/wɒt fə(r)/', 'PHR', 'näme üçin', 'для чего, зачем', 'asking the reason', 'What did you do that for?', 'Muny näme üçin etdiň?', 'A2', 'what for'),
    ('what about', '/wɒt əˈbaʊt/', 'PHR', 'barada näme', 'как насчёт', 'suggesting or asking about something', 'What about going for a walk?', 'Aýlanmaga çykmak barada näme?', 'A2', 'what about you'),
    ('how about', '/haʊ əˈbaʊt/', 'PHR', 'nähili (teklip)', 'как насчёт (предложение)', 'making a suggestion', 'How about a cup of tea?', 'Bir käse çaý nähili?', 'A2', 'how about dinner'),
]

# ---- Practical English episodes ----
T['pe_hotel'] = [
    ('reception', '/rɪˈsepʃn/', 'N', 'resepsiýa', 'стойка приёма', 'the desk where guests arrive', 'Leave the key at reception.', 'Açary resepsiýada goý.', 'A2', 'at reception'),
    ('reservation', '/ˌrezəˈveɪʃn/', 'N', 'bron', 'бронь', 'a room booked in advance', 'I have a reservation under Aliyev.', 'Aliýew adyna bronum bar.', 'A2', 'make a reservation'),
    ('double room', '/ˈdʌbl ruːm/', 'N', 'goşa otag', 'двухместный номер', 'a room with a big bed for two', 'We booked a double room.', 'Goşa otag bron etdik.', 'A2', 'book a double room'),
    ('single room', '/ˈsɪŋɡl ruːm/', 'N', 'bir kişilik otag', 'одноместный номер', 'a room for one person', 'A single room costs less.', 'Bir kişilik otag arzan.', 'A2'),
    ('towel', '/ˈtaʊəl/', 'N', 'dasmal', 'полотенце', 'cloth for drying yourself', 'There were no clean towels.', 'Arassa dasmal ýokdy.', 'A2', 'a clean towel'),
    ('sheet', '/ʃiːt/', 'N', 'ýorgan daşy', 'простыня', 'cloth on a bed', 'The sheets were changed daily.', 'Ýorgan daşlary her gün çalşyrylýardy.', 'A2', 'clean sheets'),
    ('air conditioning', '/ˈeə kənˌdɪʃənɪŋ/', 'N', 'kondisioner', 'кондиционер', 'a machine that cools a room', 'The air conditioning is broken.', 'Kondisioner işlänok.', 'A2', 'turn on the air conditioning'),
    ('heating', '/ˈhiːtɪŋ/', 'N', 'ýyladyş', 'отопление', 'the system that warms a room', 'The heating does not work.', 'Ýyladyş işlänok.', 'A2', 'central heating'),
    ('spare', '/speə(r)/', 'ADJ', 'ätiýaçlyk', 'запасной', 'extra; not being used', 'Could I have a spare pillow?', 'Ätiýaçlyk ýassyk alyp bolarmy?', 'A2', 'a spare blanket'),
    ('broken', '/ˈbrəʊkən/', 'ADJ', 'döwük', 'сломанный', 'damaged; not working', 'The TV in our room is broken.', 'Otagymyzdaky telewizor döwük.', 'A1', "it's broken"),
]

T['pe_restaurant'] = [
    ('waiter', '/ˈweɪtə(r)/', 'N', 'ofisiant', 'официант', 'a man who serves food', 'The waiter brought the menu.', 'Ofisiant menýuny getirdi.', 'A1'),
    ('order', '/ˈɔːdə(r)/', 'V', 'sargyt etmek', 'заказывать', 'to ask for food in a restaurant', 'We ordered fish and salad.', 'Balyk we salat sargyt etdik.', 'A2', 'order a meal'),
    ('starter', '/ˈstɑːtə(r)/', 'N', 'başlangyç nahar', 'закуска', 'a small dish before the main meal', 'I had soup as a starter.', 'Başlangyç nahar hökmünde çorba aldym.', 'A2'),
    ('main course', '/ˌmeɪn ˈkɔːs/', 'N', 'esasy nahar', 'основное блюдо', 'the biggest part of a meal', 'For the main course she chose chicken.', 'Esasy nahar üçin towuk saýlady.', 'A2'),
    ('dessert', '/dɪˈzɜːt/', 'N', 'süýji nahar', 'десерт', 'sweet food at the end of a meal', 'We shared a chocolate dessert.', 'Şokoladly süýji nahary paýlaşdyk.', 'A2', 'order dessert'),
    ('bill', '/bɪl/', 'N', 'hasap', 'счёт', 'the paper showing what you must pay', 'Can we have the bill, please?', 'Hasaby alyp bolarmy?', 'A2', 'ask for the bill'),
    ('tip', '/tɪp/', 'N', 'çaýpul', 'чаевые', 'extra money for the waiter', 'We left a ten per cent tip.', 'On göterim çaýpul goýduk.', 'A2', 'leave a tip'),
    ('rare', '/reə(r)/', 'ADJ', 'çigrek', 'с кровью (про мясо)', 'meat cooked only a little', 'He likes his steak rare.', 'Ol bifşteksini çigrek söýýär.', 'B1', 'a rare steak'),
    ('well done', '/ˌwel ˈdʌn/', 'ADJ', 'gowy bişen', 'хорошо прожаренный', 'meat cooked completely', 'I prefer my meat well done.', 'Etimi gowy bişen görýärin.', 'B1'),
    ('undercooked', '/ˌʌndəˈkʊkt/', 'ADJ', 'az bişen', 'недожаренный', 'not cooked enough', 'The chicken was undercooked.', 'Towuk az bişipdi.', 'B1'),
]

T['pe_return'] = [
    ('exchange', '/ɪksˈtʃeɪndʒ/', 'V', 'çalşyrmak', 'обменивать', 'to change something for another', 'Can I exchange it for a bigger size?', 'Uly ölçege çalşyp bolarmy?', 'A2', 'exchange it for'),
    ('faulty', '/ˈfɔːlti/', 'ADJ', 'näsaz', 'неисправный', 'not working properly', 'The phone was faulty.', 'Telefon näsazdy.', 'B1', 'a faulty product'),
    ('damaged', '/ˈdæmɪdʒd/', 'ADJ', 'zeper ýeten', 'повреждённый', 'harmed; broken partly', 'The box arrived damaged.', 'Guty zeper ýetip gelipdi.', 'A2'),
    ('worn out', '/wɔːn aʊt/', 'ADJ', 'könelen', 'изношенный', 'old and unusable from use', 'These shoes are worn out.', 'Bu aýakgaplar könelipdir.', 'A2'),
    ('credit note', '/ˈkredɪt nəʊt/', 'N', 'kredit kagyzy', 'кредитный талон', 'a paper worth money in a shop', 'The shop gave me a credit note.', 'Dükan maňa kredit kagyzy berdi.', 'B1', 'get a credit note'),
    ('tight', '/taɪt/', 'ADJ', 'gysyk', 'тесный', 'too small; fitting closely', 'These jeans are too tight.', 'Bu jinsi gaty gysyk.', 'A2', 'too tight'),
    ('loose', '/luːs/', 'ADJ', 'giň', 'свободный, просторный', 'not tight; bigger than needed', 'The coat is a bit loose.', 'Palto birjyk giň.', 'A2', 'too loose'),
    ('customer service', '/ˈkʌstəmə ˈsɜːvɪs/', 'N', 'müşderi hyzmaty', 'обслуживание клиентов', 'the department that helps buyers', 'Take it to customer service.', 'Müşderi hyzmatyna alyp bar.', 'A2', 'contact customer service'),
]

T['pe_pharmacy'] = [
    ('painkiller', '/ˈpeɪnkɪlə(r)/', 'N', 'agyry aýryjy', 'обезболивающее', 'medicine that stops pain', 'Take a painkiller with food.', 'Nahar bilen agyry aýryjy iç.', 'A2', 'take a painkiller'),
    ('medicine', '/ˈmedsn/', 'N', 'derman', 'лекарство', 'something you take when ill', 'The medicine tastes bitter.', 'Derman ajy tagamly.', 'A2', 'take medicine'),
    ('dose', '/dəʊs/', 'N', 'doza', 'доза', 'the amount of medicine to take', 'Take one dose twice a day.', 'Günde iki gezek bir doza iç.', 'B1', 'a double dose'),
    ('tablet', '/ˈtæblət/', 'N', 'tabletka', 'таблетка', 'a hard round piece of medicine', 'Swallow the tablet with water.', 'Tabletkany suw bilen uwut.', 'A2', 'take a tablet'),
    ('prescription', '/prɪˈskrɪpʃn/', 'N', 'resept', 'рецепт', "a doctor's paper for medicine", 'You need a prescription for these.', 'Bular üçin resept gerek.', 'B1', "a doctor's prescription"),
    ('ointment', '/ˈɔɪntmənt/', 'N', 'maz', 'мазь', 'a cream for the skin', 'Put this ointment on the burn.', 'Şu mazy ýanan ýere çal.', 'B1'),
    ('bandage', '/ˈbændɪdʒ/', 'N', 'sargy', 'бинт', 'cloth wrapped round an injury', 'He put a bandage on my hand.', 'Elime sargy sardy.', 'A2', 'put on a bandage'),
    ('plaster', '/ˈplɑːstə(r)/', 'N', 'ýelmeýji', 'пластырь', 'a small cover for a cut', 'I need a plaster for my finger.', 'Barmagym üçin ýelmeýji gerek.', 'A2'),
    ('allergy', '/ˈælədʒi/', 'N', 'allergiýa', 'аллергия', 'a bad reaction to food or plants', 'She has an allergy to nuts.', 'Hoza allergiýasy bar.', 'B1', 'an allergy to'),
    ('symptom', '/ˈsɪmptəm/', 'N', 'alamat', 'симптом', 'a sign of an illness', 'What are your symptoms?', 'Alamatlaryňyz nähili?', 'B1', 'flu symptoms'),
    ('pharmacist', '/ˈfɑːməsɪst/', 'N', 'dermançy', 'фармацевт', 'a person who prepares medicine', 'Ask the pharmacist for advice.', 'Dermançydan maslahat sora.', 'B1'),
]

T['pe_directions'] = [
    ('turn left', '/tɜːn left/', 'PHR', 'çepe öwrülmek', 'повернуть налево', 'to change direction to the left', 'Turn left at the traffic lights.', 'Çyralarda çepe öwrül.', 'A1'),
    ('turn right', '/tɜːn raɪt/', 'PHR', 'saga öwrülmek', 'повернуть направо', 'to change direction to the right', 'Turn right after the bank.', 'Bankdan soň saga öwrül.', 'A1'),
    ('go straight on', '/ɡəʊ streɪt ɒn/', 'PHR', 'göni gitmek', 'идти прямо', 'to continue without turning', 'Go straight on for two streets.', 'Iki köçe göni git.', 'A2', 'go straight on'),
    ('crossroads', '/ˈkrɒsrəʊdz/', 'N', 'çatryk', 'перекрёсток', 'a place where roads meet', 'Stop at the crossroads.', 'Çatrykda saklan.', 'A2', 'at the crossroads'),
    ('roundabout', '/ˈraʊndəbaʊt/', 'N', 'tegelek ýol', 'кольцевая развязка', 'a circle where several roads meet', 'Take the second exit at the roundabout.', 'Tegelek ýolda ikinji çykalgadan çyk.', 'A2', 'at the roundabout'),
    ('traffic lights', '/ˈtræfɪk laɪts/', 'N', 'ýol çyralary', 'светофор', 'lights that control traffic', 'Wait at the traffic lights.', 'Ýol çyralarynda gara.', 'A2', 'at the traffic lights'),
    ('pavement', '/ˈpeɪvmənt/', 'N', 'ýanýoda', 'тротуар', 'the path beside a road', 'Walk on the pavement.', 'Ýanýodada ýöre.', 'A2', 'on the pavement'),
    ('corner', '/ˈkɔːnə(r)/', 'N', 'burç', 'угол', 'where two streets meet', 'The shop is on the corner.', 'Dükan burçda.', 'A2', 'on the corner'),
    ('bridge', '/brɪdʒ/', 'N', 'köpri', 'мост', 'a road over water or a road', 'Cross the bridge and turn left.', 'Köprini geç-de çepe öwrül.', 'A2', 'cross the bridge'),
    ('underground', '/ˈʌndəɡraʊnd/', 'N', 'metro', 'метро', 'a train under the city', 'Take the underground to the centre.', 'Merkeze metro bilen git.', 'A2', 'by underground'),
]

T['pe_phone'] = [
    ('hang up', '/hæŋ ʌp/', 'PHR', 'turbany goýmak', 'класть трубку', 'to end a phone call', "Don't hang up yet.", 'Entek turbany goýma.', 'A2', 'hang up the phone'),
    ('ring', '/rɪŋ/', 'V', 'jaň etmek', 'звонить', 'to telephone someone', 'I will ring you tonight.', 'Şu gije saňa jaň ederin.', 'A1', 'ring a friend'),
    ('answer the phone', '/ˈɑːnsə ðə fəʊn/', 'PHR', 'telefona jogap bermek', 'отвечать на звонок', 'to speak when the phone rings', 'She answered the phone on the second ring.', 'Ikinji jaňda telefona jogap berdi.', 'A1'),
    ('voicemail', '/ˈvɔɪsmeɪl/', 'N', 'sesli hat', 'голосовая почта', 'a recorded phone message', 'I left a message on her voicemail.', 'Sesli poçtasyna habar goýdum.', 'A2', 'leave a voicemail'),
    ('signal', '/ˈsɪɡnəl/', 'N', 'signal', 'сигнал (связи)', 'the connection for a phone', 'There is no signal here.', 'Bu ýerde signal ýok.', 'A2', 'a weak signal'),
    ('battery', '/ˈbætri/', 'N', 'batareý', 'батарея', 'the power source in a phone', 'My battery is almost dead.', 'Batareýam diýen ýaly gutardy.', 'A2', 'a flat battery'),
    ('charge', '/tʃɑːdʒ/', 'V', 'zarýadlamak', 'заряжать', 'to put power into a battery', 'I need to charge my phone.', 'Telefonymy zarýadlamaly.', 'A2', 'charge a phone'),
    ('text', '/tekst/', 'N', 'sms', 'текстовое сообщение', 'a written phone message', 'I sent you a text.', 'Saňa sms iberdim.', 'A1', 'send a text'),
    ('message', '/ˈmesɪdʒ/', 'N', 'habar', 'сообщение', 'information sent to someone', 'He left a message for you.', 'Saña habar goýdy.', 'A1', 'leave a message'),
    ('speak up', '/spiːk ʌp/', 'PHR', 'sesiňi galdyrmak', 'говорить громче', 'to speak louder', "Sorry, can you speak up?", 'Bagyşlaň, sesiňizi galdyryp bilersiňizmi?', 'A2'),
]
LESSONS = {
    '1A':  (1,  'Are you? Can you? Do you?', 'common verb phrases · the alphabet', ['verb_phrases_1a']),
    '1B':  (1,  'The perfect date?', 'describing people: appearance · personality', ['describing_people']),
    '1C':  (1,  'The Remake Project', 'clothes · prepositions of place', ['clothes']),
    '2A':  (2,  "OMG! Where's my passport?", 'holidays', ['holidays']),
    '2B':  (2,  "That's me in the picture!", 'prepositions: at, in, on', ['prepositions_time']),
    '2C':  (2,  'One dark October evening', 'time sequencers and connectors', ['sequencers']),
    '3A':  (3,  'TripAside', 'airports', ['airports']),
    '3B':  (3,  'Put it in your calendar!', 'verbs + prepositions, e.g. arrive in', ['verbs_preps']),
    '3C':  (3,  'Word games', 'paraphrasing', ['paraphrasing']),
    '4A':  (4,  'Who does what?', 'housework · make or do?', ['housework']),
    '4B':  (4,  'In your basket', 'shopping', ['shopping']),
    '4C':  (4,  '#greatweekend', 'adjectives ending -ed and -ing', ['ed_ing_adjs']),
    '5A':  (5,  'I want it NOW!', 'types of numbers', ['numbers_types']),
    '5B':  (5,  'Twelve lost wallets', 'describing a town or city', ['town_city']),
    '5C':  (5,  'How much is enough?', 'health and the body', ['health']),
    '6A':  (6,  'Think positive - or negative?', 'opposite verbs', ['opposite_verbs']),
    '6B':  (6,  "I'll always love you", 'verb + back', ['verb_back']),
    '6C':  (6,  'The meaning of dreaming', 'modifiers', ['modifiers']),
    '7A':  (7,  'First day nerves', 'verbs + infinitive: try to, forget to, etc.', ['verb_forms']),
    '7B':  (7,  'Happiness is ...', 'verbs + gerund', ['verb_forms']),
    '7C':  (7,  'Could you pass the test?', 'adjectives + prepositions: afraid of, etc.', ['adj_preps']),
    '8A':  (8,  'Should I stay or should I go?', 'get', ['get']),
    '8B':  (8,  "Murphy's Law", 'confusing verbs', ['confusing_verbs']),
    '8C':  (8,  'Who is Vivienne?', 'adverbs of manner', ['adverbs_manner']),
    '9A':  (9,  'Beware of the dog', 'animals and insects', ['animals']),
    '9B':  (9,  'Fearof.net', 'words related to fear', ['fear']),
    '9C':  (9,  'Scream queens', 'biographies', ['biographies']),
    '10A': (10, 'Into the net', 'sports · expressing movement', ['movement']),
    '10B': (10, 'Early birds', 'phrasal verbs', ['phrasal_verbs']),
    '10C': (10, 'International inventions', 'people from different countries', ['nationalities']),
    '11A': (11, 'Ask the teacher', 'school subjects', ['school_subjects']),
    '11B': (11, "Help! I can't decide!", 'word building: noun formation', ['noun_formation']),
    '11C': (11, 'Twinstrangers.net', 'similarities and differences', ['similarities']),
    '12A': (12, 'Unbelievable!', 'time expressions', ['time_expressions']),
    '12B': (12, 'Think before you speak', 'say or tell?', ['say_tell']),
    '12C': (12, 'The English File quiz', 'question words', ['question_words']),
}


# word -> lesson, for the Vocabulary Bank section that serves two lessons.
# "Verb forms" (p.158) covers both patterns: 7A teaches verb + to infinitive,
# 7B teaches verb + gerund, so each word goes to the lesson that owns its pattern.
def _wl(words, lesson):
    for w in words.split():
        WORD_LESSON[w.replace('_', ' ').lower()] = lesson


WORD_LESSON = {}
_wl('want decide hope learn manage offer_to promise refuse expect afford arrange agree', '7A')
_wl('enjoy avoid finish keep mind miss practise suggest would_rather used_to', '7B')


def lesson_for(topic, en, fallback):
    key = en.strip().lower()
    return WORD_LESSON.get(key, fallback)


# Practical English is not a Vocabulary Bank topic: it is six filmed episodes,
# each with its own words, so it gets its own unit — unit 13, exactly as in
# Elementary, so the app shows one extra unit for it.
PE_UNIT = 13
for code, n, title, topic, key in (
    ('PE1', 13, 'Hotel problems', 'calling reception', 'pe_hotel'),
    ('PE2', 13, 'Restaurant problems', 'at the restaurant', 'pe_restaurant'),
    ('PE3', 13, 'The wrong shoes', 'taking something back to a shop', 'pe_return'),
    ('PE4', 13, 'At the pharmacy', 'feeling ill', 'pe_pharmacy'),
    ('PE5', 13, 'Getting around', 'asking how to get there', 'pe_directions'),
    ('PE6', 13, 'Time to go home', 'on the phone', 'pe_phone'),
):
    LESSONS[code] = (PE_UNIT, title, topic, [key])


def lesson_sort_key(code):
    m = re.match(r'^(\d+)(.*)$', code)
    if m:
        return (int(m.group(1)), m.group(2))
    return (13, code)


def main():
    words, seen, dups = [], {}, []

    for lesson in sorted(LESSONS, key=lesson_sort_key):
        unit, title, topic, topics = LESSONS[lesson]
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
                    'books': [{'book': 'pre', 'unit': unit, 'lesson': lesson, 'page': PAGE.get(lesson)}],
                    'proofread': False,
                })

    if dups:
        raise SystemExit('duplicate headwords:\n  ' + '\n  '.join(dups))

    used = set(t for ts in LESSONS.values() for t in ts[3])
    unused = sorted(set(T) - used)
    if unused:
        raise SystemExit('topics declared but never used by a lesson: ' + ', '.join(unused))

    # Every Pre-intermediate lesson has a word list, so nothing should drop;
    # the gate stays so an empty lesson fails loudly instead of shipping.
    lessons = []
    empty = []
    for lesson in sorted(LESSONS, key=lesson_sort_key):
        unit, title, topic, topics = LESSONS[lesson]
        n = sum(1 for w in words if w['books'][0]['lesson'] == lesson)
        if not n:
            empty.append(lesson)
            continue
        lessons.append({'lesson': lesson, 'unit': unit, 'title': title, 'topic': topic,
                        'words': n})
    if empty:
        raise SystemExit('lessons with no words — fill them: ' + ', '.join(empty))

    pack = {
        'book': 'pre',
        'title': 'English File Pre-intermediate (4th edition) — vocabulary, by lesson',
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
