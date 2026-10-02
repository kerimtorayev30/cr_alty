#!/usr/bin/env python3
"""English File Intermediate Plus — vocabulary organised by the book's own structure.

Same method as gen_adv.py / gen_int.py. The OCR dump (uploads/inter plus.txt,
10,276 lines) kept the contents table and the Vocabulary Bank references
legible. tm / ru / def / ex are my own work and proofread:false; the IPA is
written properly, not copied from the OCR.

STRUCTURE (contents table, dump lines 26-80). Intermediate Plus 4th edition
has 10 units, each with TWO lessons (A and B — no C), and five Practical
English episodes after units 1, 3, 5, 7 and 9:
  1A Why did they call you that? · 1B Life in colour · PE1 reporting lost luggage
  2A Get ready! Get set! Go! · 2B Go to checkout
  3A Grow up! · 3B Photo albums · PE2 renting a car
  4A Don't throw it away! · 4B Put it on your CV
  5A Screen time · 5B A quiet life? · PE3 making a police report
  6A What the waiter really thinks · 6B Do it yourself
  7A Take your cash · 7B Shall we go out or stay in? · PE4 house rules
  8A Treat yourself · 8B Sites and sights
  9A Total recall · 9B Here comes the bride · PE5 directions in a building
  10A The land of the free? · 10B Please turn over your papers

Vocabulary Bank (12 sections) -> lesson: Adjective suffixes->1B, Packing->2A,
Shops and services->2B, Photography->3B, Rubbish and recycling->4A, Study and
work->4B, Television->5A, The country->5B, At a restaurant->6A, DIY and
repairs->6B, Phrasal verbs->7A, Looking after yourself->8A. Everything else
comes from in-lesson boxes.

Practical English episodes carry unit 11 in the data (units 1-10 are the
book's), and the app shows each episode right after the unit it follows.

Usage: python3 content/tools/gen_intp.py
"""
import json
import os
import re
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'intermediateplus.json')

# topic -> [ (en, ipa, pos, tm, ru, def, ex, exTm, cefr[, coll]) ]
T = {}

# ---- in-lesson 1A — names ----
T['names'] = [
    ('first name', '/ˌfɜːst ˈneɪm/', 'N', 'at (öňki at)', 'имя', 'the name given to you at birth', 'Her first name is Aýna.', 'Onuň ady Aýna.', 'A1'),
    ('surname', '/ˈsɜːneɪm/', 'N', 'familiýa', 'фамилия', 'the name shared by your family', 'What is your surname?', 'Familiýaňyz näme?', 'A2'),
    ('middle name', '/ˌmɪdl ˈneɪm/', 'N', 'orta at', 'второе имя', 'a name between first and family name', 'His middle name is Alan.', 'Orta ady Alan.', 'A2'),
    ('nickname', '/ˈnɪkneɪm/', 'N', 'lakam', 'прозвище', 'an informal name for a person', 'His nickname is Shorty.', 'Lakamy Shorty.', 'A2'),
    ('initials', '/ɪˈnɪʃlz/', 'N', 'baş harplar', 'инициалы', 'the first letters of your names', 'She signed with her initials.', 'Baş harplary bilen gol çekdi.', 'B1'),
    ('maiden name', '/ˌmeɪdn ˈneɪm/', 'N', 'gyzlyk familiýasy', 'девичья фамилия', "a woman's surname before marriage", 'Her maiden name was Smith.', 'Gyzlyk familiýasy Smith boldy.', 'B1'),
    ('pet name', '/ˈpet neɪm/', 'N', 'söýgüli at', 'ласковое имя', 'a loving name for someone', 'Grandma has a pet name for everyone.', 'Mamanyň hemmäniň söýgüli ady bar.', 'B2'),
    ('namesake', '/ˈneɪmseɪk/', 'N', 'adaş', 'тёзка', 'a person with the same name as you', 'He is my namesake — we are both Merdan.', 'Ol meniň adaşym — ikimiz hem Merdan.', 'B2'),
    ('pseudonym', '/ˈsjuːdənɪm/', 'N', 'galam ady', 'псевдоним', 'a false name used by a writer', 'She wrote under a pseudonym.', 'Galam ady bilen ýazdy.', 'B2'),
    ('anonymous', '/əˈnɒnɪməs/', 'ADJ', 'atsyz (näbelli)', 'анонимный', 'with no name shown', 'The letter was anonymous.', 'Hat atsyz boldy.', 'B1'),
]

# ---- Vocabulary Bank — Adjective suffixes -> 1B ----
T['adj_suffixes'] = [
    ('bright', '/braɪt/', 'ADJ', 'ýagty (açyk reňk)', 'яркий', 'full of light, or a strong colour', 'She wore a bright red dress.', 'Ýagty gyzyl köýnek geýdi.', 'A2'),
    ('dark', '/dɑːk/', 'ADJ', 'goýy (garaňky)', 'тёмный', 'with little light, or a deep colour', 'He has dark brown eyes.', 'Goýy goňur gözleri bar.', 'A1'),
    ('pale', '/peɪl/', 'ADJ', 'açyk (solgun)', 'бледный, светлый', 'light in colour', 'The walls are pale blue.', 'Diwarlar açyk gök.', 'A2'),
    ('dull', '/dʌl/', 'ADJ', 'solgun (gyzyksyz)', 'тусклый', 'not bright or interesting', 'The sky was a dull grey.', 'Asman solgun çal boldy.', 'A2'),
    ('vivid', '/ˈvɪvɪd/', 'ADJ', 'aýdyň (örän ýagty)', 'живой, яркий', 'very bright and clear', 'She has vivid memories of that day.', 'Şol gün barada aýdyň ýatlamalary bar.', 'B1', 'vivid colours'),
    ('colourful', '/ˈkʌləfl/', 'ADJ', 'reňkli', 'красочный', 'having many bright colours', 'The market sells colourful fabrics.', 'Bazar reňkli matalary satýar.', 'A2'),
    ('cheerful', '/ˈtʃɪəfl/', 'ADJ', 'şähdaçyk', 'жизнерадостный', 'happy and positive', 'She gave a cheerful wave.', 'Şähdaçyk el bulady.', 'A2'),
    ('gloomy', '/ˈɡluːmi/', 'ADJ', 'garaňky (gamgyn)', 'мрачный', 'dark and sad', 'The weather was cold and gloomy.', 'Howa sowuk we garaňky boldy.', 'B1'),
    ('glorious', '/ˈɡlɔːriəs/', 'ADJ', 'şanly (ajaýyp)', 'великолепный', 'very beautiful or impressive', 'We had glorious weather.', 'Ajaýyp howa boldy.', 'B1'),
    ('sparkling', '/ˈspɑːklɪŋ/', 'ADJ', 'ýaldyrawuk', 'сверкающий', 'shining with small flashes', 'The lake was sparkling clean.', 'Köl ýaldyrap durdy.', 'B1'),
    ('spotless', '/ˈspɒtləs/', 'ADJ', 'tämiz (lekisiz)', 'безупречно чистый', 'completely clean', 'The kitchen was spotless.', 'Aşhana tämiz boldy.', 'B1'),
    ('countless', '/ˈkaʊntləs/', 'ADJ', 'san-sajaksyz', 'бесчисленный', 'too many to count', 'There are countless stars tonight.', 'Şu gije san-sajaksyz ýyldyz bar.', 'B1'),
]

# ---- Vocabulary Bank — Packing -> 2A ----
T['packing'] = [
    ('suitcase', '/ˈsuːtkeɪs/', 'N', 'çemodan', 'чемодан', 'a bag for carrying clothes when travelling', 'She packed a large suitcase.', 'Uly çemodan ýygnady.', 'A2'),
    ('razor', '/ˈreɪzə(r)/', 'N', 'pyçak (sakal)', 'бритва', 'a tool for cutting hair off the skin', 'He bought a new razor.', 'Täze sakgal pyçagyny satyn aldy.', 'B1'),
    ('swimsuit', '/ˈswɪmsuːt/', 'N', 'ýüzmek lybasy', 'купальник', 'clothes worn for swimming', 'Do not forget your swimsuit.', 'Ýüzmek lybasyňy ýatdan çykarma.', 'A2'),
    ('sunscreen', '/ˈsʌnskriːn/', 'N', 'günden goraýjy krem', 'солнцезащитный крем', 'cream that protects skin from sun', 'Put on sunscreen at the beach.', 'Kenarda günden goraýjy krem çal.', 'A2'),
    ('toothpaste', '/ˈtuːθpeɪst/', 'N', 'diş pastasy', 'зубная паста', 'a paste for cleaning teeth', 'We need more toothpaste.', 'Köp diş pastasy gerek.', 'A2'),
    ('toiletries', '/ˈtɔɪlətriz/', 'N', 'şahsy arassalyk serişdeleri', 'туалетные принадлежности', 'things you use to wash yourself', 'Pack your toiletries in a small bag.', 'Şahsy arassalyk serişdeleriňi kiçi sumka ýygnap goý.', 'B1'),
    ('backpack', '/ˈbækpæk/', 'N', 'arkalyk sumka', 'рюкзак', 'a bag carried on the back', 'He travels with one backpack.', 'Bir arkalyk sumka bilen syýahat edýär.', 'A2'),
    ('flip-flops', '/ˈflɪp flɒps/', 'N', 'şypbyk', 'шлёпанцы', 'light open shoes for summer', 'She wore flip-flops to the beach.', 'Kenara şypbyk geýdi.', 'A2'),
    ('adapter', '/əˈdæptə(r)/', 'N', 'geçiriji (tok)', 'переходник, адаптер', 'a plug that fits foreign sockets', 'Take an adapter for the hotel.', 'Myhmanhana üçin tok geçirijisi al.', 'B1'),
    ('holdall', '/ˈhəʊldɔːl/', 'N', 'uly sumka', 'дорожная сумка', 'a large soft bag for travel', 'He carried a black holdall.', 'Gara uly sumka göterdi.', 'B2'),
    ('washbag', '/ˈwɒʃbæɡ/', 'N', 'ýuwunmak sumkasy', 'несессер', 'a small bag for washing things', 'My washbag has a toothbrush.', 'Ýuwunmak sumkamda diş çotgasy bar.', 'B2'),
    ('comb', '/kəʊm/', 'N', 'darak', 'расчёска', 'a tool for tidying hair', 'She ran a comb through her hair.', 'Saçyny darak bilen darady.', 'A2'),
]

# ---- Vocabulary Bank — Shops and services -> 2B ----
T['shops_services'] = [
    ('bakery', '/ˈbeɪkəri/', 'N', 'çörekhanа', 'булочная', 'a shop that sells bread and cakes', 'The bakery opens at seven.', 'Çörekhanа ýedide açylýar.', 'A2'),
    ('butcher', '/ˈbʊtʃə(r)/', 'N', 'et satyjy (gassap)', 'мясник', 'a person or shop that sells meat', 'The butcher cut the lamb.', 'Gassap goýun etini kesdi.', 'A2'),
    ('chemist', '/ˈkemɪst/', 'N', 'dermanhana', 'аптека', 'a shop that sells medicine', 'Buy the pills at the chemist.', 'Dermanlary dermanhanadan al.', 'A2'),
    ('florist', '/ˈflɒrɪst/', 'N', 'gül satyjy', 'цветочник', 'a shop that sells flowers', 'The florist made a lovely bouquet.', 'Gül satyjy owadan çemen ýasady.', 'A2'),
    ('greengrocer', '/ˈɡriːnɡrəʊsə(r)/', 'N', 'gök önüm satyjy', 'овощной магазин', 'a shop that sells fruit and vegetables', 'The greengrocer has fresh tomatoes.', 'Gök önüm satyjyda täze pomidor bar.', 'B1'),
    ('hairdresser', '/ˈheədresə(r)/', 'N', 'sartaraş', 'парикмахер', 'a person who cuts hair', 'The hairdresser trimmed my fringe.', 'Sartaraş kakulumy kesdi.', 'A2'),
    ('jeweller', '/ˈdʒuːələ(r)/', 'N', 'zergär', 'ювелир', 'a shop that sells jewellery', 'The jeweller repaired the ring.', 'Zergär ýüzügi bejерdi.', 'A2'),
    ('newsagent', '/ˈnjuːzeɪdʒənt/', 'N', 'gazet satyjy', 'газетный киоск', 'a shop selling papers and magazines', 'The newsagent is on the corner.', 'Gazet satyjy burçda.', 'B1'),
    ('optician', '/ɒpˈtɪʃn/', 'N', 'göz lukmany (optika)', 'оптик', 'a person who tests eyes and sells glasses', 'The optician checked my sight.', 'Göz lukmany görüşimi barlady.', 'B1'),
    ('dry cleaner', '/ˌdraɪ ˈkliːnə(r)/', 'N', 'himiki arassalaýjy', 'химчистка', 'a shop that cleans clothes without water', 'Take the suit to the dry cleaner.', 'Kostýumy himiki arassalaýja ber.', 'B1'),
    ('stationer', '/ˈsteɪʃənə(r)/', 'N', 'kagyz-kalem satyjy', 'канцелярский магазин', 'a shop selling pens and paper', 'The stationer sells notebooks.', 'Kagyz-kalem satyjy depder satýar.', 'B2'),
    ('deli', '/ˈdeli/', 'N', 'tagam dükany', 'гастроном', 'a shop selling cooked food and cheese', 'We bought cheese at the deli.', 'Tagam dükanyndan peýniр aldyk.', 'B1'),
]

# ---- in-lesson 3A — stages of life ----
T['stages_life'] = [
    ('baby', '/ˈbeɪbi/', 'N', 'çaga (täze doglan)', 'младенец', 'a very young child', 'The baby is sleeping.', 'Çaga uklaýar.', 'A1'),
    ('toddler', '/ˈtɒdlə(r)/', 'N', 'ýöräp başlan çaga', 'малыш (начинающий ходить)', 'a child just learning to walk', 'The toddler held her hand.', 'Ýöräp başlan çaga elini saklady.', 'B1'),
    ('infant', '/ˈɪnfənt/', 'N', 'bäbek', 'грудной ребёнок', 'a very young child or baby', 'The class is for infants.', 'Synp bäbekler üçin.', 'B2'),
    ('child', '/tʃaɪld/', 'N', 'çaga', 'ребёнок', 'a young person', 'The child played in the park.', 'Çaga parkda oýnady.', 'A1'),
    ('teenager', '/ˈtiːneɪdʒə(r)/', 'N', 'ýetginjek', 'подросток', 'a person aged 13 to 19', 'Teenagers love their phones.', 'Ýetginjekler telefonlaryny gowy görýär.', 'A2'),
    ('adolescent', '/ˌædəˈlesnt/', 'N', 'ýetginjek (ösmür)', 'подросток, юноша', 'a young person becoming an adult', 'Adolescents need good sleep.', 'Ösmürler gowy uky mätäç.', 'B2'),
    ('adult', '/ˈædʌlt/', 'N', 'uly adam', 'взрослый', 'a fully grown person', 'Adults pay the full price.', 'Uly adamlar doly baha töleýär.', 'A2'),
    ('youngster', '/ˈjʌŋstə(r)/', 'N', 'ýaş oglan-gyz', 'юнец, youngster', 'a young person', 'The youngsters played football.', 'Ýaşlar futbol oýnady.', 'B1'),
    ('middle-aged', '/ˌmɪdl ˈeɪdʒd/', 'ADJ', 'orta ýaşly', 'средних лет', 'neither young nor old', 'A middle-aged man answered the door.', 'Orta ýaşly adam gapyny açdy.', 'B1'),
    ('pensioner', '/ˈpenʃənə(r)/', 'N', 'pensiýaçy', 'пенсионер', 'a person too old to work', 'Pensioners travel free.', 'Pensiýaçylar mugt gatnaýar.', 'B1'),
    ('elderly', '/ˈeldəli/', 'ADJ', 'garry', 'пожилой', 'old (polite)', 'She helps elderly neighbours.', 'Garry goňşularyna kömek edýär.', 'A2'),
    ('newborn', '/ˈnjuːbɔːn/', 'N', 'täze doglan çaga', 'новорождённый', 'a baby just born', 'The newborn weighed three kilos.', 'Täze doglan çaga üç kilo boldy.', 'B1'),
]

# ---- Vocabulary Bank — Photography -> 3B ----
T['photography'] = [
    ('camera', '/ˈkæmrə/', 'N', 'fotoapparat', 'фотоаппарат', 'a machine for taking photos', 'He bought a new camera.', 'Täze fotoapparat satyn aldy.', 'A1'),
    ('lens', '/lenz/', 'N', 'linza (obýektiw)', 'объектив', 'the glass part of a camera', 'Clean the lens before shooting.', 'Surata düşürmezden öň linzany arassala.', 'A2'),
    ('snapshot', '/ˈsnæpʃɒt/', 'N', 'tiz surat', 'снимок', 'a quick informal photo', 'She took a snapshot of the view.', 'Görnüşiň tiz surata düşürdi.', 'A2'),
    ('close-up', '/ˌkləʊs ˈʌp/', 'N', 'ýakyn plan', 'крупный план', 'a photo showing small detail', 'Take a close-up of her face.', 'Ýüzüniň ýakyn planyny düşür.', 'A2'),
    ('background', '/ˈbækɡraʊnd/', 'N', 'arka fon', 'задний план', 'the part behind the main subject', 'The mountains form the background.', 'Daglar arka fon döredýär.', 'A2', 'in the background'),
    ('focus', '/ˈfəʊkəs/', 'V', 'fokuslamak', 'фокусировать', 'to make a picture sharp', 'Focus on the front row.', 'Öňdäki hatara fokusla.', 'A2'),
    ('exposure', '/ɪkˈspəʊʒə(r)/', 'N', 'ekspozisiýa', 'экспозиция', 'the amount of light in a photo', 'Adjust the exposure for night shots.', 'Gije suratlary üçin ekspozisiýany sazla.', 'B2'),
    ('develop', '/dɪˈveləp/', 'V', 'ýüze çykarmak (surat)', 'проявлять (плёнку)', 'to make photos from film', 'They developed the film at home.', 'Plýonkany öýde ýüze çykardylar.', 'A2'),
    ('selfie', '/ˈselfi/', 'N', 'selfi', 'селфи', 'a photo you take of yourself', 'She posted a selfie online.', 'Selfini onlaýn ýerleşdirdi.', 'A2'),
    ('zoom', '/zuːm/', 'V', 'ulaltmak (ýakynlaşdyrmak)', 'приближать (зум)', 'to make the subject look nearer', 'Zoom in on the bird.', 'Guşa ýakynlaşdyr.', 'A2', 'zoom in'),
    ('shutter', '/ˈʃʌtə(r)/', 'N', 'zatwor', 'затвор', 'the part that opens to take a photo', 'Press the shutter gently.', 'Zatwory ýuwaş bas.', 'B2'),
    ('photographer', '/fəˈtɒɡrəfə(r)/', 'N', 'suratkeş (fotograf)', 'фотограф', 'a person who takes photos', 'The photographer posed us outside.', 'Fotograf bizi daşarda duruzdy.', 'A2'),
]

# ---- Vocabulary Bank — Rubbish and recycling -> 4A ----
T['recycling'] = [
    ('recycle', '/ˌriːˈsaɪkl/', 'V', 'gaýtadan işlemek', 'перерабатывать', 'to make waste into new things', 'We recycle paper and glass.', 'Kagyz we aýnany gaýtadan işleýäris.', 'A2'),
    ('rubbish', '/ˈrʌbɪʃ/', 'N', 'zibil', 'мусор', 'waste that you throw away', 'Take the rubbish outside.', 'Zibili daşaryk çykar.', 'A2'),
    ('litter', '/ˈlɪtə(r)/', 'N', 'taşlanan zibil', 'мусор (на улице)', 'rubbish left in public places', 'Do not drop litter in the park.', 'Parkda zibil taşlama.', 'A2', 'drop litter'),
    ('waste', '/weɪst/', 'N', 'isrip (galyndy)', 'отходы', 'material that is thrown away', 'The factory produces chemical waste.', 'Zawod himiki galyndy öndürýär.', 'A2', 'waste water'),
    ('bin', '/bɪn/', 'N', 'zibil bedresi', 'мусорный бак', 'a container for rubbish', 'Put it in the bin.', 'Ony zibil bedresine at.', 'A2', 'rubbish bin'),
    ('landfill', '/ˈlændfɪl/', 'N', 'zibil gömülýän ýer', 'свалка', 'a place where rubbish is buried', 'Too much waste goes to landfill.', 'Köp galyndy zibil gömülýän ýere gidýär.', 'B1'),
    ('compost', '/ˈkɒmpɒst/', 'N', 'kompost', 'компост', 'decayed plants used to feed soil', 'We make compost from food scraps.', 'Iýmit galyndylaryndan kompost ýasaýarys.', 'B1'),
    ('throw away', '/θrəʊ əˈweɪ/', 'PHR', 'zyňmak', 'выбрасывать', 'to get rid of something', 'Do not throw away that box.', 'Şol gutyny zyňma.', 'A2'),
    ('dump', '/dʌmp/', 'V', 'taşlamak (zibil)', 'сваливать, выбрасывать', 'to leave waste somewhere', 'They dumped the rubbish illegally.', 'Zibili bikanun taşladylar.', 'A2'),
    ('disposable', '/dɪˈspəʊzəbl/', 'ADJ', 'bir gezeklik', 'одноразовый', 'used once then thrown away', 'Avoid disposable cups.', 'Bir gezeklik käselerden gaça dur.', 'B1'),
    ('packaging', '/ˈpækɪdʒɪŋ/', 'N', 'gaplama', 'упаковка', 'material used to wrap goods', 'Too much packaging is wasted.', 'Köp gaplama isrip edilýär.', 'A2'),
    ('reusable', '/ˌriːˈjuːzəbl/', 'ADJ', 'gaýtadan ulanylýan', 'многоразовый', 'able to be used again', 'Bring a reusable bag.', 'Gaýtadan ulanylýan sumka getir.', 'A2'),
]
