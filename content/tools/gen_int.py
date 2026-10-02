#!/usr/bin/env python3
"""English File Intermediate — vocabulary organised by the book's own structure.

Same method as gen_pre.py / gen_elementary.py. The OCR dump
(uploads/intermediate.txt, 17,180 lines) kept the Vocabulary Bank headwords
legible (p.152-165, dump lines ~15583-16600): 11 sections. In-lesson
VOCABULARY boxes supplied the rest. tm / ru / def / ex are my own work and
proofread:false; the IPA is written properly, not copied from the OCR.

STRUCTURE (contents table, dump lines 15-112). Intermediate 4th edition has
10 units, each with TWO lessons (A and B — no C), and five Practical English
episodes sitting after units 1, 3, 5, 7 and 9:
  1A Eating in...and out · 1B Modern families · PE1 Meeting the parents
  2A Spending money · 2B Changing lives
  3A Survive the drive · 3B Men, women, and children · PE2 A difficult celebrity
  4A Bad manners? · 4B Yes, I can!
  5A Sporting superstitions · 5B #thewaywemet · PE3 Ola friends
  6A Behind the scenes · 6B Every picture tells a story
  7A Live and learn · 7B The hotel of Mum and Dad · PE4 Boys' night out
  8A The right job for you · 8B Have a nice day!
  9A Lucky encounters · 9B Digital detox · PE5 Unexpected events
  10A Idols and icons · 10B And the murderer is...

Vocabulary Bank (11 sections) -> lesson: Food and cooking->1A, Money->2A,
Transport->3A, Dependent prepositions->3B, Sport->5A, Relationships->5B,
Cinema->6A, The body->6B, Education->7A, Houses->7B, Work->8A.
Everything else comes from in-lesson boxes.

PE episodes carry unit 11 in the data (units 1-10 are the book's), and the app
shows each episode right after the unit it follows in the book.

Usage: python3 content/tools/gen_int.py
"""
import json
import os
import re
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'intermediate.json')

# topic -> [ (en, ipa, pos, tm, ru, def, ex, exTm, cefr[, coll]) ]
# SB pages from the syllabus checklist (TG pp.4-6), verified against the TG.
PAGE = {
    '1A': 6, '1B': 10, '2A': 16, '2B': 20, '3A': 26, '3B': 30,
    '4A': 36, '4B': 40, '5A': 46, '5B': 50, '6A': 56, '6B': 60,
    '7A': 66, '7B': 70, '8A': 76, '8B': 80, '9A': 86, '9B': 90,
    '10A': 96, '10B': 100,
    'PE1': 14, 'PE2': 34, 'PE3': 54, 'PE4': 74, 'PE5': 94,
}

T = {}

# ---- Vocabulary Bank — Food and cooking -> 1A ----
T['food_cooking'] = [
    ('boil', '/bɔɪl/', 'V', 'gaýnatmak', 'кипятить; варить', 'to cook in very hot water', 'Boil the eggs for eight minutes.', 'Ýumurtgalary sekiz minut gaýnat.', 'A2'),
    ('fry', '/fraɪ/', 'V', 'gowurmak', 'жарить', 'to cook in hot oil', 'She fried the potatoes.', 'Ol ýeralmany gowurdy.', 'A2'),
    ('grill', '/ɡrɪl/', 'V', 'kabap etmek', 'жарить на гриле', 'to cook over fire or hot metal', 'We grilled the fish outside.', 'Balygy daşarda kabap etdik.', 'A2'),
    ('roast', '/rəʊst/', 'V', 'kabap bişirmek', 'запекать', 'to cook meat in the oven', 'Mum roasted a chicken.', 'Ejem towuk kabap bişirdi.', 'A2', 'roast chicken'),
    ('bake', '/beɪk/', 'V', 'tamdyrda bişirmek', 'выпекать', 'to cook bread or cakes in an oven', 'She baked a birthday cake.', 'Doglan güni üçin keks bişirdi.', 'A2', 'bake a cake'),
    ('steam', '/stiːm/', 'V', 'bugda bişirmek', 'готовить на пару', 'to cook over boiling water', 'Steamed vegetables are healthy.', 'Bugda bişen gök önümler peýdaly.', 'B1'),
    ('chop', '/tʃɒp/', 'V', 'dogramak', 'крошить, рубить', 'to cut into small pieces', 'Chop the onions finely.', 'Sogany ownuk dogra.', 'B1', 'chop the onions'),
    ('slice', '/slaɪs/', 'V', 'tilimlemek', 'нарезать ломтиками', 'to cut into thin flat pieces', 'Slice the bread, please.', 'Çöregi tilimle.', 'B1', 'slice the bread'),
    ('mix', '/mɪks/', 'V', 'garyşdyrmak', 'смешивать', 'to put things together and stir', 'Mix the flour and sugar.', 'Uny we şekeri garyşdyr.', 'A2', 'mix the ingredients'),
    ('stir', '/stɜː(r)/', 'V', 'garmak', 'мешать', 'to move a spoon round in a liquid', 'Stir the soup slowly.', 'Çorbany haýal garyşdyr.', 'B1', 'stir the sauce'),
    ('pour', '/pɔː(r)/', 'V', 'guýmak', 'наливать', 'to make a liquid flow from a container', 'Pour the tea into the cups.', 'Çaýy käselere guý.', 'A2', 'pour the water'),
    ('ingredient', '/ɪnˈɡriːdiənt/', 'N', 'goşundy', 'ингредиент', 'one of the things you use to make food', 'We need five ingredients.', 'Bize bäş goşundy gerek.', 'B1', 'fresh ingredients'),
    ('recipe', '/ˈresəpi/', 'N', 'tagam ýasalyşy', 'рецепт', 'instructions for cooking a dish', 'This recipe is very easy.', 'Bu tagam ýasalyşy gaty aňsat.', 'A2', 'follow a recipe'),
    ('bitter', '/ˈbɪtə(r)/', 'ADJ', 'ajy', 'горький', 'having a sharp unpleasant taste', 'The coffee tasted bitter.', 'Kofe ajy tagamly boldy.', 'A2'),
    ('fresh', '/freʃ/', 'ADJ', 'täze', 'свежий', 'recently made or picked; not frozen', 'Buy fresh fruit at the market.', 'Bazardan täze miwe al.', 'A2', 'fresh bread'),
    ('tasty', '/ˈteɪsti/', 'ADJ', 'tagamly', 'вкусный', 'having a good flavour', 'That was a tasty meal.', 'Ol tagamly nahardy.', 'A2'),
    ('crab', '/kræb/', 'N', 'çerçik, krab', 'краб', 'a sea animal with a shell and ten legs', 'We ate crab by the sea.', 'Deňiz kenarynda krab iýdik.', 'B1'),
    ('lobster', '/ˈlɒbstə/', 'N', 'omar', 'омар, лобстер', 'a large sea animal with claws', 'The lobster was very expensive.', 'Omar gaty gymmatdy.', 'B1'),
    ('mussels', '/ˈmʌslz/', 'N', 'midiýa', 'мидии', 'small black shellfish you can eat', 'We had mussels in a creamy sauce.', 'Midiýany kremli sousda iýdik.', 'B1'),
    ('prawns', '/prɔːnz/', 'N', 'krewetka', 'креветки', 'small sea animals you eat, like very small lobsters', 'I love prawns in garlic butter.', 'Sarymsak ýagyndaky krewetkany gowy görýärin.', 'B1'),
    ('salmon', '/ˈsæmən/', 'N', 'gyzylbalyk', 'лосось', 'a large fish with pink flesh', 'Grilled salmon is healthy.', 'Gowrulan gyzylbalyk peýdaly.', 'B1'),
    ('squid', '/skwɪd/', 'N', 'kalmar', 'кальмар', 'a sea animal with a long body, used as food', 'They served fried squid.', 'Olar gowrulan kalmar berdiler.', 'B1'),
    ('tuna', '/ˈtjuːnə/', 'N', 'tunes balygy', 'тунец', 'a large sea fish eaten as food', 'I had a tuna sandwich.', 'Tunes balykly buterbrod iýdim.', 'B1'),
    ('beef', '/biːf/', 'N', 'sygyr eti', 'говядина', 'meat from a cow', 'The beef was very tender.', 'Sygyr eti gaty ýumşakdy.', 'B1'),
    ('chicken', '/ˈtʃɪkɪn/', 'N', 'towuk eti', 'курица (мясо)', 'meat from a chicken', 'We had roast chicken for dinner.', 'Agşamlyk nahara towuk gowrulanyny iýdik.', 'A2'),
    ('duck', '/dʌk/', 'N', 'ördek eti', 'утка (мясо)', 'meat from a duck', 'Duck with orange sauce is a classic dish.', 'Apelsin sously ördek klassik tagam.', 'B1'),
    ('lamb', '/læm/', 'N', 'goýun eti, guzy eti', 'баранина', 'meat from a young sheep', 'We cooked lamb on the fire.', 'Odunda guzy eti bişirdik.', 'B1'),
    ('pork', '/pɔːk/', 'N', 'doňuz eti', 'свинина', 'meat from a pig', 'He never eats pork.', 'Ol doňuz etini hiç iýmeýär.', 'B1'),
    ('aubergine', '/ˈəʊbədʒiːn/', 'N', 'badamjan', 'баклажан', 'a long purple vegetable', 'She made a dish with aubergine.', 'Ol badamjanly tagam bişirdi.', 'B1'),
    ('avocado', '/ˌævəˈkɑːdəʊ/', 'N', 'awokado', 'авокадо', 'a green fruit with a large seed', 'Avocado on toast is popular.', 'Tostdaky awokado meşhur.', 'B1'),
    ('beetroot', '/ˈbiːtruːt/', 'N', 'gyzyl çugundyr', 'свёкла', 'a round dark red vegetable', 'Beetroot makes your hands red.', 'Gyzyl çugundyr elleriňi gyzyl edýär.', 'B1'),
    ('cabbage', '/ˈkæbɪdʒ/', 'N', 'kelem', 'капуста', 'a large round green vegetable', 'She cooked cabbage with meat.', 'Kelemi et bilen bişirdi.', 'A2'),
    ('cherries', '/ˈtʃeriz/', 'N', 'alça, ülje', 'вишни, черешни', 'small soft round red fruits', 'We picked cherries in the garden.', 'Bagda alça ýyğdyk.', 'B1'),
    ('courgette', '/kʊəˈʒet/', 'N', 'kabak', 'кабачок', 'a long green vegetable (British English)', 'Add the courgette to the pan.', 'Kabagy çemçe goş.', 'B1'),
    ('cucumber', '/ˈkjuːkʌmbə/', 'N', 'hyýar', 'огурец', 'a long green vegetable eaten raw', 'Put cucumber in the salad.', 'Hyýary salata sal.', 'A2'),
    ('grapes', '/ɡreɪps/', 'N', 'üzüm', 'виноград', 'small sweet green or purple fruits', 'She bought a kilo of grapes.', 'Bir kilo üzüm satyn aldy.', 'A2'),
    ('mango', '/ˈmæŋɡəʊ/', 'N', 'mango', 'манго', 'a sweet yellow tropical fruit', 'Mango is my favourite fruit.', 'Mango meniň iň söýýän miwäm.', 'B1'),
    ('cut down on', '/ˌkʌt daʊn ˈɒn/', 'PHR', 'azaltmak', 'сократить (потребление)', 'to eat or use less of something', "I'm trying to cut down on sugar.", 'Şekeri azaltmaga çalyşýaryn.', 'B1'),
    ('cut out', '/ˌkʌt ˈaʊt/', 'PHR', 'düýbünden aýyrmak', 'полностью исключить', 'to stop eating or using something completely', 'The doctor told me to cut out cheese.', 'Lukman peýniri düýbünden aýyrmagy tabşyrdy.', 'B1'),
    ('eat out', '/ˌiːt ˈaʊt/', 'PHR', 'daşarda naharlanmak', 'есть вне дома', 'to eat at a restaurant, not at home', 'We eat out twice a week.', 'Hepdede iki gezek daşarda naharlanýarys.', 'A2'),
]

# ---- in-lesson — family · personality adjectives -> 1B ----
T['family_personality'] = [
    ('nephew', '/ˈnefjuː/', 'N', 'ýegen (oglan)', 'племянник', "a brother's or sister's son", 'My nephew is five years old.', 'Ýegenim bäş ýaşynda.', 'A2'),
    ('niece', '/niːs/', 'N', 'ýegen (gyz)', 'племянница', "a brother's or sister's daughter", 'His niece lives with us.', 'Onuň ýegeni bizde ýaşaýar.', 'A2'),
    ('twin', '/twɪn/', 'N', 'ekiz', 'близнец', 'one of two children born at the same time', 'My cousins are twins.', 'Doganlarym ekiz.', 'A2', 'identical twins'),
    ('engaged', '/ɪnˈɡeɪdʒd/', 'ADJ', 'ady bagly', 'помолвленный', 'having promised to marry someone', 'They got engaged in spring.', 'Ýazda atlaryny bagladylar.', 'B1', 'get engaged'),
    ('divorced', '/dɪˈvɔːst/', 'ADJ', 'aýrylyşan', 'разведённый', 'no longer married', 'She is divorced with two kids.', 'Iki çagaly aýrylyşan aýal.', 'B1'),
    ('ambitious', '/æmˈbɪʃəs/', 'ADJ', 'öňe saýlanmaga çalyşýan', 'амбициозный', 'wanting very much to succeed', 'He is young and ambitious.', 'Ol ýaş we öňe saýlanmaga çalyşýan.', 'B1'),
    ('arrogant', '/ˈærəɡənt/', 'ADJ', 'tekepbir', 'высокомерный', 'thinking you are better than others', 'I find him rather arrogant.', 'Ony birneme tekepbir görýärin.', 'B1'),
    ('bossy', '/ˈbɒsi/', 'ADJ', 'buýruçyl', 'любящий командовать', 'always telling people what to do', 'My bossy sister organises everything.', 'Buýruçyl uýam hemme zady gurnaýar.', 'B1'),
    ('confident', '/ˈkɒnfɪdənt/', 'ADJ', 'ynamly', 'уверенный', 'sure of yourself and your abilities', 'She felt confident before the exam.', 'Synagdan öň ynamly boldy.', 'A2'),
    ('easy-going', '/ˌiːzi ˈɡəʊɪŋ/', 'ADJ', 'uşal', 'покладистый', 'relaxed and happy to accept things', 'He is an easy-going teacher.', 'Ol ushal mugallym.', 'B1'),
    ('honest', '/ˈɒnɪst/', 'ADJ', 'dogruçyl', 'честный', 'always telling the truth', 'Be honest with me.', 'Meniň bilen dogruçyl bol.', 'A2'),
    ('impatient', '/ɪmˈpeɪʃnt/', 'ADJ', 'sabyrsyz', 'нетерпеливый', 'not able to wait calmly', 'The impatient driver started honking.', 'Sabyrsyz sürüji signal berip başlady.', 'B1'),
    ('jealous', '/ˈdʒeləs/', 'ADJ', 'gabanjaň', 'ревнивый, завистливый', 'unhappy because someone has what you want', 'He was jealous of her success.', 'Onuň üstünligine gabanýardy.', 'B1', 'jealous of'),
    ('reliable', '/rɪˈlaɪəbl/', 'ADJ', 'ynançly', 'надёжный', 'able to be trusted', 'Ask Anna — she is very reliable.', 'Annadan sora — ol gaty ynançly.', 'B1'),
    ('selfish', '/ˈselfɪʃ/', 'ADJ', 'hodbin', 'эгоистичный', 'caring only about yourself', 'It was selfish to eat it all.', 'Hemmesini iýmek hodbin boldy.', 'A2'),
    ('sensible', '/ˈsensəbl/', 'ADJ', 'paýhasly', 'благоразумный', 'showing good judgement', 'Take a sensible decision.', 'Paýhasly karar ber.', 'B1'),
    ('sociable', '/ˈsəʊʃəbl/', 'ADJ', 'jemgyýetçil', 'общительный', 'liking to be with people', 'She is warm and sociable.', 'Ol mähirli we jemgyýetçil.', 'B1'),
    ('affectionate', '/əˈfekʃənət/', 'ADJ', 'mähirli', 'ласковый', 'showing love for people', 'She is very affectionate with her children.', 'Ol çagalary bilen gaty mähirli.', 'B1'),
    ('anxious', '/ˈæŋkʃəs/', 'ADJ', 'aladaly, biynjalyk', 'тревожный', 'worried about something', 'He felt anxious before the interview.', 'Söhbetdeşlikden öň aladalandy.', 'B1'),
    ('charming', '/ˈtʃɑːmɪŋ/', 'ADJ', 'sympatik, özüne çekiji', 'обаятельный', 'very pleasant and easy to like', 'Her husband is charming.', 'Adamsy gaty sympatik.', 'B1'),
    ('competitive', '/kəmˈpetətɪv/', 'ADJ', 'bäsleşigi söýýän', 'состязательный, конкурентный', 'wanting very much to win', 'He is very competitive at tennis.', 'Tennisde gaty bäsleşigi söýýär.', 'B1'),
    ('imaginative', '/ɪˈmædʒɪnətɪv/', 'ADJ', 'hyýally, oýlap tapyjy', 'с богатым воображением', 'good at thinking of new and interesting ideas', 'She tells imaginative stories.', 'Hyýaly hekaýalar gürrüň berýär.', 'B1'),
    ('independent', '/ˌɪndɪˈpendənt/', 'ADJ', 'özygtyýarly', 'независимый', 'doing things yourself, without help from others', 'She is very independent.', 'Ol gaty özygtyýarly.', 'B1'),
    ('insecure', '/ˌɪnsɪˈkjʊə/', 'ADJ', 'özüne ynamy pes', 'неуверенный в себе', 'not confident about yourself', 'He feels insecure about his English.', 'Iňlis diline ynamy pes.', 'B1'),
    ('mature', '/məˈtʃʊə/', 'ADJ', 'kämil, ýetişen', 'зрелый', 'behaving like an older person', 'She is very mature for her age.', 'Ýaşy üçin gaty kämil.', 'B1'),
    ('patient', '/ˈpeɪʃnt/', 'ADJ', 'sabyrly', 'терпеливый', 'able to wait without getting angry', 'A teacher must be patient.', 'Mugallym sabyrly bolmaly.', 'B1'),
    ('rebellious', '/rɪˈbeljəs/', 'ADJ', 'garşylykly, boýun egmeýän', 'бунтарский, непокорный', 'refusing to obey rules', 'He was rebellious as a teenager.', 'Ýetginjek wagty boýun egmeýärdi.', 'B1'),
    ('sensitive', '/ˈsensətɪv/', 'ADJ', 'duýgur', 'чувствительный', 'easily hurt or offended', 'She is sensitive to criticism.', 'Tankyda duýgur.', 'B1'),
    ('spoilt', '/spɔɪlt/', 'ADJ', 'erkeledilen', 'избалованный', 'behaving badly because you always get what you want', 'The spoilt child wanted another toy.', 'Erkeledilen çaga ýene oýunjak isledi.', 'B1'),
    ('stubborn', '/ˈstʌbən/', 'ADJ', 'inat', 'упрямый', 'refusing to change your opinion', 'He is too stubborn to say sorry.', 'Ötür soramak üçin gaty inat.', 'B1'),
]

# ---- Vocabulary Bank — Money -> 2A ----
T['money'] = [
    ('charge', '/tʃɑːdʒ/', 'V', 'töletmek', 'брать плату', 'to ask an amount of money', 'They charge ten manat for entry.', 'Giriş üçin on manat töledýärler.', 'A2', 'charge for'),
    ('cost', '/kɒst/', 'V', 'durmak', 'стоить', 'to have a price', 'The coat cost me a fortune.', 'Palto maňa köp durdy.', 'A1', 'cost a fortune'),
    ('loan', '/ləʊn/', 'N', 'karz', 'заём, ссуда', 'money you borrow from a bank', 'They took out a loan for the flat.', 'Öý üçin karz aldylar.', 'B1', 'take out a loan'),
    ('owe', '/əʊ/', 'V', 'karzdar bolmak', 'быть должным', 'to need to pay money back', 'I still owe you five manat.', 'Saña entek bäş manat karzym bar.', 'B1', 'owe money'),
    ('price', '/praɪs/', 'N', 'baha', 'цена', 'the amount of money something costs', 'The price of petrol went up.', 'Benziniň bahasy galdy.', 'A2', 'high price'),
    ('rent', '/rent/', 'V', 'kärendesine almak', 'арендовать', 'to pay to use a flat or car', 'We rent a flat near the centre.', 'Merkeziň ýanyndaky öýi kärendesine alýarys.', 'A2', 'rent a flat'),
    ('save', '/seɪv/', 'V', 'tygşytlamak', 'копить', 'to keep money for later', 'She saves a little every month.', 'Her aý biraz tygşytlaýar.', 'A2', 'save money'),
    ('spend', '/spend/', 'V', 'sarp etmek', 'тратить', 'to use money to buy things', 'He spent all his salary in a week.', 'Aýlygyny bir hepdede sarp etdi.', 'A1', 'spend money on'),
    ('waste', '/weɪst/', 'V', 'isrip etmek', 'тратить впустую', 'to use money or time badly', "Don't waste money on apps you never open.", 'Hiç wagt açmaýan programmalaryňa pul isrip etme.', 'A2', 'waste money'),
    ('worth', '/wɜːθ/', 'ADJ', 'degýän', 'стоящий (чего-л.)', 'having a value; good enough for', 'The film is worth seeing.', 'Film görmäge degýär.', 'A2', 'worth doing'),
    ('affordable', '/əˈfɔːdəbl/', 'ADJ', 'elýeterli', 'доступный по цене', 'not too expensive', 'The rent is affordable for students.', 'Kärende talyplar üçin elýeterli.', 'B1'),
    ('broke', '/brəʊk/', 'ADJ', 'pulsuz', 'на мели', 'having no money (informal)', 'I was broke until payday.', 'Aýlyk gününe çenli pulsuz boldum.', 'B1', 'go broke'),
    ('borrow', '/ˈbɒrəʊ/', 'V', 'karz almak', 'брать взаймы', 'to take money from someone and pay it back later', 'I had to borrow money from my mum.', 'Enemden karz pul almaly boldum.', 'A2'),
    ("can't afford", '/ˌkɑːnt əˈfɔːd/', 'PHR', 'güýji ýetmezlik', 'не мочь себе позволить', 'to not have enough money for something', "We can't afford a new car.", 'Täze ulaga güýjümiz ýetmeýär.', 'B1'),
    ('earn', '/ɜːn/', 'V', 'gazanjyny almak, işlemek', 'зарабатывать', 'to get money for work', 'She earns a good salary.', 'Gowy aýlyk gazanýar.', 'B1'),
    ('inherit', '/ɪnˈherɪt/', 'V', 'miras almak', 'наследовать', 'to get money or property when someone dies', 'My uncle is going to leave me money; I will inherit it.', 'Daýzam maňa pul goýar; men ony miras alaryn.', 'B1'),
    ('invest', '/ɪnˈvest/', 'V', 'maýa goýmak', 'инвестировать', 'to put money into something to make a profit', 'I want to invest some money.', 'Biraz maýa goýmak isleýärin.', 'B1'),
    ('lend', '/lend/', 'V', 'karz bermek', 'давать взаймы', 'to give money to someone for a short time', 'He promised to lend me €50.', 'Maňa 50 ýewro karz bermegi wada berdi.', 'A2'),
    ('raise', '/reɪz/', 'V', 'ýygnamak, galdyrmak', 'собирать (деньги)', 'to collect money for a purpose', 'We want to raise money for the new hospital.', 'Täze hassahana üçin pul ýygnamak isleýäris.', 'B1'),
    ('bill', '/bɪl/', 'N', 'hasap, töleg kagazy', 'счёт', 'a piece of paper that shows how much you must pay', 'Can we have the bill, please?', 'Hasaby alyp bilerismi, haýyş?', 'A2'),
    ('budget', '/ˈbʌdʒɪt/', 'N', 'büjet', 'бюджет', 'money that you have and a plan for how to spend it', 'We planned our holiday budget carefully.', 'Dynç alyş býujetimizi ünsli meýilleşdirdik.', 'B1'),
    ('contactless payment', '/ˌkɒntæktləs ˈpeɪmənt/', 'N', 'temassyz töleg', 'бесконтактная оплата', 'paying by holding your card or phone near a machine', 'Contactless payment is very fast.', 'Temassyz töleg gaty çalt.', 'B1'),
    ('insurance', '/ɪnˈʃʊərəns/', 'N', 'ätiýaçlandyryş', 'страхование', 'money you pay so a company helps if something bad happens', 'Do you have travel insurance?', 'Syýahat ätiýaçlandyryşyňyz barmy?', 'B1'),
    ('mortgage', '/ˈmɔːɡɪdʒ/', 'N', 'ipoteka', 'ипотека', 'money you borrow from a bank to buy a house', 'They pay a mortgage every month.', 'Her aý ipoteka töleýärler.', 'B1'),
    ('salary', '/ˈsæləri/', 'N', 'aýlyk', 'зарплата, оклад', 'the money you get for the work you do', 'The money you get for your work is your salary.', 'Işiň üçin alýan puluň aýlykdyr.', 'B1'),
    ('tax', '/tæks/', 'N', 'salgyt', 'налог', 'money that you pay to the government', 'You pay tax on your salary.', 'Aýlygyňdan salgyt töleýärsiň.', 'B1'),
    ('account', '/əˈkaʊnt/', 'N', 'hasap', 'счёт (в банке)', 'an arrangement with a bank to keep your money', 'I opened a bank account yesterday.', 'Düýn bank hasabyny açdym.', 'A2'),
    ('cash machine', '/ˈkæʃ məʃiːn/', 'N', 'bankomat', 'банкомат', 'a machine where you get cash from your account', 'Is there a cash machine near here?', 'Bu ýerde bankomat barmy?', 'A2'),
    ('debt', '/det/', 'N', 'karz', 'долг', 'money that you owe somebody', 'He has a lot of debt.', 'Onuň köp karzy bar.', 'B1'),
    ('live off', '/ˌlɪv ˈɒf/', 'PHR', 'hasabyna ýaşamak', 'жить на (что-то)', 'to use money to pay for everything you need', 'I can live off 250 euros a week.', 'Hepdede 250 ýewro hasabyna ýaşap bilýärin.', 'B1'),
    ('pay back', '/ˌpeɪ ˈbæk/', 'PHR', 'gaýtarmak', 'возвращать (долг)', 'to give money back to someone', "I haven't paid Jim back yet.", 'Jime entek gaýtarmadym.', 'B1'),
    ('pay by', '/ˌpeɪ ˈbaɪ/', 'PHR', 'bilen tölemek', 'платить (способом)', 'to use a particular way of paying', 'You can pay by credit card.', 'Kredit kart bilen töläp bilersiňiz.', 'A2'),
]

# ---- in-lesson — strong adjectives -> 2B ----
T['strong_adjs'] = [
    ('exhausted', '/ɪɡˈzɔːstɪd/', 'ADJ', 'lapyny gutaran', 'изнурённый', 'extremely tired', 'After the match I was exhausted.', 'Oýundan soň lapym gutardy.', 'B1'),
    ('awful', '/ˈɔːfl/', 'ADJ', 'elhenç', 'ужасный', 'very bad', 'The weather was awful.', 'Howa elhenç boldy.', 'A2'),
    ('boiling', '/ˈbɔɪlɪŋ/', 'ADJ', 'gaýnap duran', 'очень жарко', 'extremely hot', "It's boiling in here — open a window.", 'Bu ýerde gaty yssy — penjire aç.', 'A2'),
    ('freezing', '/ˈfriːzɪŋ/', 'ADJ', 'doňduryjy', 'очень холодно', 'extremely cold', 'My hands are freezing.', 'Ellerim doňýar.', 'A2'),
    ('furious', '/ˈfjʊəriəs/', 'ADJ', 'gahary atan', 'в ярости', 'extremely angry', 'Dad was furious about the broken window.', 'Kakam döwük penjire üçin gahary atdy.', 'B1', 'furious with'),
    ('starving', '/ˈstɑːvɪŋ/', 'ADJ', 'garny aç', 'очень голодный', 'extremely hungry', 'When do we eat? I am starving.', 'Haçan naharlanýarys? Garnym aç.', 'A2'),
    ('tiny', '/ˈtaɪni/', 'ADJ', 'miniskär', 'крошечный', 'extremely small', 'They live in a tiny flat.', 'Miniskär öýde ýaşaýarlar.', 'A2'),
    ('huge', '/hjuːdʒ/', 'ADJ', 'ägirt', 'огромный', 'extremely big', 'A huge crowd filled the square.', 'Ägirt märele meýdançany doldurdy.', 'A2'),
    ('filthy', '/ˈfɪlθi/', 'ADJ', 'hapa', 'отвратительно грязный', 'extremely dirty', 'Take off those filthy shoes.', 'Şol hapa aýakgaplaryňy çykar.', 'B1'),
    ('fascinating', '/ˈfæsɪneɪtɪŋ/', 'ADJ', 'özüne çekiji (gyzykly)', 'увлекательнейший', 'extremely interesting', 'The museum was fascinating.', 'Muzeý özüne çekiji boldy.', 'B1'),
    ('hilarious', '/hɪˈleəriəs/', 'ADJ', 'gülkünç', 'уморительный', 'extremely funny', 'The comedy was hilarious.', 'Komediýa gülkünç boldy.', 'B1'),
]

# ---- Vocabulary Bank — Transport -> 3A ----
T['transport'] = [
    ('brake', '/breɪk/', 'N', 'tormoz', 'тормоз', 'the control that slows a vehicle', 'He put his foot on the brake.', 'Tormoz pedalyna aýagyny basdy.', 'B1', 'put on the brakes'),
    ('fare', '/feə(r)/', 'N', 'ýol haky', 'плата за проезд', 'the money you pay for a journey', 'The bus fare went up again.', 'Awtobus ýol haky ýene galdy.', 'B1', 'bus fare'),
    ('lorry', '/ˈlɒri/', 'N', 'ýük maşyny', 'грузовик', 'a big road vehicle for goods', 'A lorry blocked the road.', 'Ýük maşyny ýoly böwetdi.', 'A2'),
    ('motorbike', '/ˈməʊtəbaɪk/', 'N', 'motoulag', 'мотоцикл', 'a two-wheeled vehicle with an engine', 'He goes to work by motorbike.', 'Işe motoulagda gidýär.', 'A2', 'by motorbike'),
    ('queue', '/kjuː/', 'N', 'nobat', 'очередь', 'a line of people waiting', 'There was a long queue at the stop.', 'Duralgada uzyn nobat bardy.', 'A2', 'in a queue'),
    ('rail', '/reɪl/', 'N', 'demir ýol', 'железная дорога', 'the system of trains', 'They travelled by rail.', 'Demir ýol bilen syýahat etdiler.', 'A2', 'by rail'),
    ('rush hour', '/ˈrʌʃ aʊə(r)/', 'N', 'adatdan daşary wagt', 'час пик', 'the busiest time on the roads', 'Avoid driving in rush hour.', 'Adatdan daşary wagt ulag sürmekden gaça dur.', 'A2', 'in rush hour'),
    ('seat belt', '/ˈsiːt belt/', 'N', 'howpsuzlyk kemeri', 'ремень безопасности', 'the strap that keeps you safe in a car', 'Fasten your seat belt.', 'Howpsuzlyk kemeriňi dakyn.', 'A2', 'fasten your seat belt'),
    ('traffic jam', '/ˈtræfɪk dʒæm/', 'N', 'dykyn', 'пробка', 'a line of vehicles that cannot move', 'We were stuck in a traffic jam.', 'Dykyna düşdük.', 'A2', 'stuck in a traffic jam'),
    ('vehicle', '/ˈviːəkl/', 'N', 'ulag serişdesi', 'транспортное средство', 'anything used to carry people on land', 'No vehicles are allowed here.', 'Bu ýerde ulag serişdelerine rugsat berilmeýär.', 'B1'),
    ('get on', '/ɡet ɒn/', 'PHR', 'münmek', 'садиться (в транспорт)', 'to enter a bus, train or plane', 'We got on the wrong bus.', 'Nädogry awtobusa mündük.', 'A2', 'get on the bus'),
    ('get off', '/ɡet ɒf/', 'PHR', 'düşmek', 'сходить (с транспорта)', 'to leave a bus, train or plane', 'Get off at the next stop.', 'Indiki duralgada düş.', 'A2', 'get off the train'),
    ('delay', '/dɪˈleɪ/', 'N', 'giçikme', 'задержка', 'a situation when something is late', 'There was a two-hour delay.', 'Iki sagatlyk giçikme boldy.', 'A2', 'a long delay'),
    ('commute', '/kəˈmjuːt/', 'V', 'gatnamak', 'ездить на работу', 'to travel regularly between home and work', 'She commutes from Mary every day.', 'Her gün Marydan gatnaýar.', 'B1'),
    ('cycle lane', '/ˈsaɪkl leɪn/', 'N', 'welosiped ýodasy', 'велодорожка', 'a part of the road only for bicycles', 'Do not drive in the cycle lane.', 'Welosiped ýodasynda sürme.', 'B1'),
    ('platform', '/ˈplætfɔːm/', 'N', 'peron', 'платформа, перрон', 'the place where you wait for a train', 'The train leaves from platform 4.', 'Otly 4-nji perondan gidýär.', 'B1'),
    ('car crash', '/ˈkɑː kræʃ/', 'N', 'ulag heläkçiligi', 'авария, ДТП', 'an accident between cars', 'There was a car crash on the motorway.', 'Awtobanda ulag heläkçiligi boldy.', 'B1'),
    ('tram', '/træm/', 'N', 'tramwaý', 'трамвай', 'a vehicle like a bus that runs on rails in a city', 'We took the tram to the centre.', 'Merkeze tramwaýda gitdik.', 'B1'),
    ('ferry', '/ˈferi/', 'N', 'parom', 'паром', 'a boat that carries people and cars across water', 'We crossed to the island by ferry.', 'Ada paromda geçdik.', 'B1'),
    ('zebra crossing', '/ˌzebrə ˈkrɒsɪŋ/', 'N', 'pyýada geçelgesi', 'пешеходный переход', 'a place with black and white lines where you walk across a road', 'Cross the road at the zebra crossing.', 'Ýoly pyýada geçelgesinden geç.', 'B1'),
    ('taxi rank', '/ˈtæksi ræŋk/', 'N', 'taksi duralgasy', 'стоянка такси', 'a place where taxis wait for customers', 'There is a taxi rank outside the station.', 'Wokzalyň öňünde taksi duralgasy bar.', 'B1'),
    ('scooter', '/ˈskuːtə/', 'N', 'skuter', 'скутер, мотороллер', 'a small light motorbike', 'He goes to work by scooter.', 'Işe skuterde gidýär.', 'B1'),
    ('petrol station', '/ˈpetrəl steɪʃn/', 'N', 'ýangyç duralgasy', 'заправка', 'a place where you buy fuel for a car', 'Stop at the next petrol station.', 'Indiki ýangyç duralgasynda saklan.', 'B1'),
    ('coach', '/kəʊtʃ/', 'N', 'awtobus (uzak ýol)', 'автобус (междугородный)', 'a bus for long journeys', 'We went to London by coach.', 'Londona awtobusda gitdik.', 'B1'),
    ('speed camera', '/ˈspiːd ˌkæmərə/', 'N', 'tizlik kameras', 'камера контроля скорости', 'a camera that photographs cars going too fast', 'The speed camera caught him at 90 km/h.', 'Tizlik kameras ony 90 km/sag tutdy.', 'B1'),
    ('parking fine', '/ˈpɑːkɪŋ faɪn/', 'N', 'durma jerimesi', 'штраф за парковку', 'money you pay for leaving your car in the wrong place', 'She got a parking fine today.', 'Şu gün durma jerimesini aldy.', 'B1'),
    ('van', '/væn/', 'N', 'furgon', 'фургон', 'a vehicle like a small truck', 'The flowers arrived in a van.', 'Güller furgonda geldi.', 'B1'),
    ('speed limit', '/ˈspiːd ˌlɪmɪt/', 'N', 'tizlik çägi', 'ограничение скорости', 'the fastest you are allowed to drive', 'The speed limit here is 50 km/h.', 'Bu ýerde tizlik çägi 50 km/sag.', 'B1'),
    ('roadworks', '/ˈrəʊdwɜːks/', 'N', 'ýol işleri', 'дорожные работы', 'work being done to repair a road', 'There are roadworks on the bridge.', 'Köpride ýol işleri bar.', 'B1'),
    ('motorway', '/ˈməʊtəweɪ/', 'N', 'awtoban', 'автострада', 'a very wide fast road between cities', 'We drove 200 km on the motorway.', 'Awtobanda 200 km sürdük.', 'B1'),
    ('the Underground', '/ði ˈʌndəɡraʊnd/', 'N', 'metro (London)', 'метро (в Лондоне)', 'the railway system under London', 'Take the Underground to Oxford Street.', 'Oksford köçesine metroda git.', 'B1'),
]

# ---- Vocabulary Bank — Dependent prepositions -> 3B ----
T['dep_preps'] = [
    ('apologize for', '/əˈpɒlədʒaɪz fə(r)/', 'PHR', 'bagyşlama soramak', 'извиняться за', 'to say sorry for something', 'He apologized for being late.', 'Giç galany üçin bagyşlama sorady.', 'B1', 'apologize for being late'),
    ('approve of', '/əˈpruːv əv/', 'PHR', 'makullamak', 'одобрять', 'to think something is good or right', 'Her parents do not approve of the plan.', 'Ene-atasy meýilnamany makullamaýar.', 'B1', 'approve of the idea'),
    ('believe in', '/bɪˈliːv ɪn/', 'PHR', 'ynanmak', 'верить в', 'to feel sure something exists or is good', 'I believe in you.', 'Saňa ynanýaryn.', 'A2', 'believe in yourself'),
    ('insist on', '/ɪnˈsɪst ɒn/', 'PHR', 'tutdurmak', 'настаивать на', 'to demand something firmly', 'She insisted on paying.', 'Tölemäge tutdurdy.', 'B1', 'insist on doing'),
    ('rely on', '/rɪˈlaɪ ɒn/', 'PHR', 'bil baglamak', 'полагаться на', 'to trust someone to do what you need', 'You can rely on me.', 'Maňa bil baglap bilersiň.', 'A2', 'rely on someone'),
    ('succeed in', '/səkˈsiːd ɪn/', 'PHR', 'üstünlik gazanmak', 'преуспевать в', 'to achieve what you want', 'He succeeded in finding a job.', 'Iş tapmakda üstünlik gazandy.', 'B1', 'succeed in doing'),
    ('agree with', '/əˈɡriː wɪð/', 'PHR', 'ylalaşmak', 'соглашаться с', 'to have the same opinion as a person', 'I agree with you completely.', 'Seniň bilen doly ylalaşýaryn.', 'A2', 'agree with someone'),
    ('dream of', '/driːm əv/', 'PHR', 'arzuw etmek', 'мечтать о', 'to want something very much', 'She dreams of studying abroad.', 'Daşary ýurtda okamagy arzuw edýär.', 'A2', 'dream of doing'),
    ('interested in', '/ˈɪntrəstɪd ɪn/', 'PHR', 'gyzyklanýan', 'интересующийся', 'wanting to know about something', 'He is interested in photography.', 'Surata düşürmek bilen gyzyklanýar.', 'A2', 'interested in music'),
]

# ---- in-lesson — phone language -> 4A ----
T['phone_language'] = [
    ('get through', '/ɡet θruː/', 'PHR', 'telefon arkaly ýetmek', 'дозвониться', 'to succeed in speaking on the phone', 'I could not get through all morning.', 'Irdenläp telefon arkaly ýetip bilmedim.', 'A2', 'get through to'),
    ('hold on', '/həʊld ɒn/', 'PHR', 'garaşmak', 'подождать (на линии)', 'to wait on the phone', 'Hold on a moment, please.', 'Bir pursat garaşyň.', 'A2', 'hold on a second'),
    ('put through', '/pʊt θruː/', 'PHR', 'birikdirmek', 'соединять (по телефону)', 'to connect a phone call', 'Could you put me through to sales?', 'Satuw bölümi bilen birikdirip bilersiňizmi?', 'B1', 'put through to'),
    ('take a message', '/teɪk ə ˈmesɪdʒ/', 'PHR', 'habar ýazmak', 'записать сообщение', 'to write down what a caller says', 'Can I take a message?', 'Habar ýazyp bilerinmi?', 'A2'),
    ('leave a message', '/liːv ə ˈmesɪdʒ/', 'PHR', 'habar goýmak', 'оставить сообщение', 'to tell someone something by phone', 'Please leave a message after the tone.', 'Signal eşidilenden soň habar goýuň.', 'A2'),
    ('cut off', '/kʌt ɒf/', 'PHR', 'aragatnaşyk kesilmek', 'обрывать связь', 'to lose the phone connection suddenly', 'We were cut off mid-sentence.', 'Sözlemiň ortasynda aragatnaşyk kesildi.', 'B1', 'get cut off'),
    ('dial', '/ˈdaɪəl/', 'V', 'nomar ýygnamak', 'набирать номер', 'to enter a phone number', 'Dial the number again, slowly.', 'Nomary ýene, haýal ýygnap gör.', 'B1', 'dial a number'),
    ('on the phone', '/ɒn ðə fəʊn/', 'PHR', 'telefon arkaly', 'по телефону', 'talking by telephone', 'She has been on the phone for an hour.', 'Bir sagat bäri telefon arkaly gürleşýär.', 'A1', 'talk on the phone'),
]

# ---- in-lesson — -ed / -ing adjectives -> 4B ----
T['ed_ing2'] = [
    ('alarmed', '/əˈlɑːmd/', 'ADJ', 'aladalan', 'встревоженный', 'worried about possible danger', 'She was alarmed by the news.', 'Habar ony aladalandyrdy.', 'B1', 'alarmed by'),
    ('amusing', '/əˈmjuːzɪŋ/', 'ADJ', 'güldüriji', 'забавный', 'making you smile or laugh', 'He told an amusing story.', 'Güldüriji hekaýa gürrüň berdi.', 'B1'),
    ('annoyed', '/əˈnɔɪd/', 'ADJ', 'gaharly (birneme)', 'раздражённый', 'a little angry', 'She was annoyed at the delay.', 'Giçikmä gahary geldi.', 'A2', 'annoyed with'),
    ('astonished', '/əˈstɒnɪʃt/', 'ADJ', 'haýran galan (güýçli)', 'изумлённый', 'very surprised', 'We were astonished by the price.', 'Bahadan haýran galdyk.', 'B1', 'astonished at'),
    ('depressed', '/dɪˈprest/', 'ADJ', 'ruhdan düşen', 'подавленный', 'very unhappy for a long time', 'The long winter made him depressed.', 'Uzyn gyş ony ruhdan düşürdi.', 'B1'),
    ('disgusting', '/dɪsˈɡʌstɪŋ/', 'ADJ', 'ygrenç', 'отвратительный', 'extremely unpleasant', 'The soup smelled disgusting.', 'Çorbanyň ysy ygrenç boldy.', 'B1'),
    ('stressed', '/strest/', 'ADJ', 'dartgynly', 'в стрессе', 'worried and unable to relax', 'Students feel stressed before exams.', 'Talyplar synagdan öň dartgynly bolýar.', 'A2', 'stressed out'),
    ('irritated', '/ˈɪrɪteɪtɪd/', 'ADJ', 'jynjygalan', 'раздражённый (слегка)', 'slightly annoyed', 'He got irritated by the questions.', 'Soraglardan jynjygalandy.', 'B1', 'irritated by'),
    ('thrilled', '/θrɪld/', 'ADJ', 'şaý-sevinçli', 'в восторге', 'extremely happy and excited', 'She was thrilled with the result.', 'Netijeden şaý-sevinçli boldy.', 'B1', 'thrilled with'),
    ('puzzled', '/ˈpʌzld/', 'ADJ', 'bulaşan (oýlanan)', 'озадаченный', 'unable to understand something', 'He looked puzzled by the question.', 'Soragdan bulaşan ýaly boldy.', 'B1', 'puzzled by'),
]

# ---- Vocabulary Bank — Sport -> 5A ----
T['sport'] = [
    ('beat', '/biːt/', 'V', 'utmak', 'побеждать (соперника)', 'to win against a person or team', 'We beat the champions 2-1.', 'Çempionlary 2-1 utduk.', 'A2', 'beat a team'),
    ('draw', '/drɔː/', 'N', 'deňmeň', 'ничья', 'a game where both sides score the same', 'The match ended in a draw.', 'Oýun deňmeň gutardy.', 'A2', 'end in a draw'),
    ('league', '/liːɡ/', 'N', 'liga', 'лига', 'a group of teams that play each other', 'Our team is top of the league.', 'Toparymyz liganyň başynda.', 'A2', 'the league table'),
    ('referee', '/ˌrefəˈriː/', 'N', 'emin', 'судья (в спорте)', 'the person who controls a game', 'The referee showed him a red card.', 'Emin oňa gyzyl kart görkezdi.', 'A2'),
    ('score', '/skɔː(r)/', 'V', 'utuk gazanmak', 'забивать', 'to get a point or goal', 'She scored twice in the final.', 'Finalda iki gezek utuk gazandy.', 'A2', 'score a goal'),
    ('spectator', '/spekˈteɪtə(r)/', 'N', 'tomaşaçy', 'зритель', 'a person who watches a game', 'The stadium holds 40,000 spectators.', 'Stadion 40,000 tomaşaçy sygdyrýar.', 'B1'),
    ('take up', '/teɪk ʌp/', 'PHR', 'başlamak (sport)', 'начинать заниматься', 'to start a new sport or hobby', 'He took up swimming last year.', 'Geçen ýyl ýüzmä başlady.', 'A2', 'take up a sport'),
    ('train', '/treɪn/', 'V', 'türgenleşmek', 'тренироваться', 'to practise for a sport', 'They train four times a week.', 'Hepdede dört gezek türgenleşýärler.', 'A2', 'train hard'),
    ('tennis court', '/ˈtenɪs kɔːt/', 'N', 'tennis meýdançasy', 'теннисный корт', 'the area where you play tennis', 'The tennis court is free at six.', 'Tennis meýdançasy altyda boş.', 'A2', 'on court'),
    ('pitch', '/pɪtʃ/', 'N', 'oýun meýdany', 'футбольное поле', 'the field where football is played', 'The pitch was wet after the rain.', 'Ýagyşdan soň oýun meýdany öllüdi.', 'B1', 'football pitch'),
    ('track', '/træk/', 'N', 'ylgaýyş ýodasy', 'беговая дорожка', 'a path for running or racing', 'She ran two laps of the track.', 'Ýodanyň iki aýlawyny ylgady.', 'A2', 'running track'),
    ('fan', '/fæn/', 'N', 'janköýer', 'болельщик', 'a person who loves a team or star', 'He is a big fan of Arsenal.', 'Arsenalyň uly janköýeri.', 'A1', 'a big fan'),
    ('circuit', '/ˈsɜːkɪt/', 'N', 'trek, aýlawly ýol', 'трасса (авто/мото)', 'a track for motor races', 'The cars went round the circuit.', 'Ulaglar trek boýunça aýlandy.', 'B1'),
    ('hockey', '/ˈhɒki/', 'N', 'hokkeý', 'хоккей', 'a team sport played with sticks and a ball or puck', 'He plays hockey at school.', 'Mekdepde hokkeý oýnaýar.', 'A2'),
    ('warm up', '/ˌwɔːm ˈʌp/', 'PHR', 'maşk etmek, gyzgynlyk', 'разминаться', 'to do gentle exercise before sport', 'Always warm up before a run.', 'Ylgamazdan öň hemişe maşk et.', 'B1'),
    ('get injured', '/ˌɡet ˈɪndʒəd/', 'PHR', 'şikes almak', 'получить травму', 'to hurt yourself doing sport', 'She got injured playing football.', 'Futbol oýnap şikes aldy.', 'B1'),
    ('stadium', '/ˈsteɪdiəm/', 'N', 'stadion', 'стадион', 'a large place for sports with seats around it', 'The stadium holds 50,000 people.', 'Stadion 50,000 adam sygdyrýar.', 'B1'),
    ('diving', '/ˈdaɪvɪŋ/', 'N', 'suwa bökmek; daýwing', 'прыжки в воду; дайвинг', 'the sport of jumping into water, or swimming under water', 'She won a medal in diving.', 'Suwa bökmekde medal aldy.', 'B1'),
    ('golf', '/ɡɒlf/', 'N', 'golf', 'гольф', 'a sport where you hit a small ball into holes', 'He plays golf every Sunday.', 'Her ýekşenbe golf oýnaýar.', 'A2'),
    ('work out', '/ˌwɜːk ˈaʊt/', 'PHR', 'türgenleşmek', 'тренироваться', 'to do exercise to become strong and fit', 'I work out at the gym twice a week.', 'Hepdede iki gezek zalda türgenleşýärin.', 'A2'),
    ('player', '/ˈpleɪə/', 'N', 'oýunçy', 'игрок', 'a person who plays a sport or game', 'He is the best player in the team.', 'Toparda iň gowy oýunçy.', 'A2'),
    ('sports hall', '/ˈspɔːts hɔːl/', 'N', 'sport zaly', 'спортивный зал', 'a large indoor room for sport', 'We play basketball in the sports hall.', 'Sport zalynda basketbol oýnaýarys.', 'B1'),
    ('slope', '/sləʊp/', 'N', 'eňňit, gaýt', 'склон', 'a surface with one end higher than the other', 'He went down the ski slope.', 'Ol tizlenme gaýdyndan aşak düşdi.', 'B1'),
    ('umpire', '/ˈʌmpaɪə/', 'N', 'emin (tennis)', 'судья (в теннисе)', 'the person who makes sure players obey the rules in tennis', 'The umpire called the ball out.', 'Emin pökgini aut diýip yglan etdi.', 'B1'),
    ('crowd', '/kraʊd/', 'N', 'mähelle', 'толпа', 'a large group of people watching something', 'The crowd cheered loudly.', 'Mähelle gaty gygyrdy.', 'B1'),
    ('team', '/tiːm/', 'N', 'topar', 'команда', 'a group of players in a sport', 'Which team do you support?', 'Haýsy topar goldaýarsyň?', 'A2'),
    ('captain', '/ˈkæptɪn/', 'N', 'kapitan', 'капитан', 'the leader of a sports team', 'She is the captain of the volleyball team.', 'Woleýbol toparynyň kapitany.', 'B1'),
]
# ---- Vocabulary Bank — Relationships -> 5B ----
T['relationships'] = [
    ('break up', '/breɪk ʌp/', 'PHR', 'aýrylyşmak', 'расставаться', 'to end a relationship', 'They broke up after two years.', 'Iki ýyldan soň aýrylyşdylar.', 'A2', 'break up with'),
    ('couple', '/ˈkʌpl/', 'N', 'jübüt', 'пара', 'two people in a romantic relationship', 'The couple next door just married.', 'Gapydaky jübüt ýaňy öýlendi.', 'A2', 'a married couple'),
    ('fall in love', '/fɔːl ɪn lʌv/', 'PHR', 'aşyk bolmak', 'влюбляться', 'to start loving someone', 'They fell in love at university.', 'Uniwersitetde aşyk boldular.', 'A2', 'fall in love with'),
    ('fall out', '/fɔːl aʊt/', 'PHR', 'ara bozmak', 'ссориться', 'to stop being friendly after an argument', 'The sisters fell out over money.', 'Uýalar pul üstünde ara bozdy.', 'B1', 'fall out with'),
    ('get divorced', '/ɡet dɪˈvɔːst/', 'PHR', 'aýrylyşmak (nikahdan)', 'разводиться', 'to legally end a marriage', 'They got divorced last spring.', 'Geçen ýaz aýrylyşdylar.', 'A2'),
    ('go out with', '/ɡəʊ aʊt wɪð/', 'PHR', 'duşuşmak', 'встречаться с', 'to spend time romantically with someone', 'She goes out with a musician.', 'Sazanda bilen duşuşýar.', 'A2', 'go out with someone'),
    ('make up', '/meɪk ʌp/', 'PHR', 'ara düzetmek', 'мириться', 'to become friendly again after a fight', 'They argued but soon made up.', 'Jedelleşdiler ýöne tiz ara düzetdiler.', 'A2', 'make up with'),
    ('partner', '/ˈpɑːtnə(r)/', 'N', 'ýoldaş', 'партнёр', 'the person you live or work with', 'Her partner cooks well.', 'Ýoldaşy gowy bişirýär.', 'A2', 'life partner'),
    ('relationship', '/rɪˈleɪʃnʃɪp/', 'N', 'gatnaşyk', 'отношения', 'the way two people feel about each other', 'They have a strong relationship.', 'Berk gatnaşyklary bar.', 'A2', 'close relationship'),
    ('split up', '/splɪt ʌp/', 'PHR', 'aýrylyşmak (jübüt)', 'расходиться', 'to end a relationship', 'The band split up in 2020.', 'Topar 2020-nji ýylda dargady.', 'A2', 'split up with'),
    ('single', '/ˈsɪŋɡl/', 'ADJ', 'ýeke', 'не женат/не замужем', 'not married or in a relationship', 'He has been single for a year.', 'Bir ýyl bäri ýeke.', 'A1'),
    ('trust', '/trʌst/', 'V', 'ynam etmek', 'доверять', 'to believe someone is honest', 'I trust her completely.', 'Oňa doly ynam edýärin.', 'A2', 'trust someone'),
    ('lose touch', '/ˌluːz ˈtʌtʃ/', 'PHR', 'aragatnaşygy ýitirmek', 'терять связь', 'to stop communicating with someone over time', 'We lost touch after school.', 'Mekdepden soň aragatnaşygy ýitirdik.', 'B1'),
    ('get in touch', '/ˌɡet ɪn ˈtʌtʃ/', 'PHR', 'habarlaşmak', 'связаться', 'to contact someone', 'She got in touch with me last year.', 'Geçen ýyl men bilen habarlaşdy.', 'B1'),
    ('get to know', '/ˌɡet tə ˈnəʊ/', 'PHR', 'ýakyndan tanamak', 'узнавать (человека)', 'to spend time with someone and learn about them', 'We got to know each other at university.', 'Uniwersitetde birek-biregi ýakyndan tanadyk.', 'B1'),
    ('propose', '/prəˈpəʊz/', 'V', 'öýlenme teklibini etmek', 'делать предложение', 'to ask someone to marry you', 'He proposed on the beach.', 'Kenarda öýlenme teklip etdi.', 'B1'),
    ('fancy', '/ˈfænsi/', 'V', 'halamak, göwnünden turmak', 'нравиться (о человеке)', 'to be attracted to someone', 'I think she fancies him.', 'Onuň oňa göwni ýetýän bolsa gerek.', 'B1'),
    ('ask out', '/ˌɑːsk ˈaʊt/', 'PHR', 'duşuşyga çagyrmak', 'пригласить на свидание', 'to invite someone on a date', 'He finally asked her out.', 'Ahyry ony duşuşyga çagyrdy.', 'B1'),
    ('close friend', '/ˌkləʊs ˈfrend/', 'N', 'ýakyn dost', 'близкий друг', 'a friend you know very well', 'She is one of my close friends.', 'Ýakyn dostlarymyň biri.', 'A2'),
    ('flatmate', '/ˈflætmeɪt/', 'N', 'öý ýoldaşy', 'сосед по квартире', 'a person you share a flat with', 'My flatmate cooks every evening.', 'Öý ýoldaşym her agşam nahar bişirýär.', 'B1'),
]

# ---- Vocabulary Bank — Cinema -> 6A ----
T['cinema'] = [
    ('audience', '/ˈɔːdiəns/', 'N', 'tomaşaçylar', 'аудитория', 'the people watching a film or show', 'The audience clapped loudly.', 'Tomaşaçylar gaty el çarpdy.', 'A2', 'the whole audience'),
    ('cast', '/kɑːst/', 'N', 'aktýorlar düzümi', 'актёрский состав', 'all the actors in a film', 'The film has a brilliant cast.', 'Filmiň ajaýyp aktýorlar düzümi bar.', 'B1', 'the cast of'),
    ('character', '/ˈkærəktə(r)/', 'N', 'gahryman', 'персонаж', 'a person in a film or book', 'My favourite character is the doctor.', 'Iň söýýän gahrymanym lukman.', 'A2', 'the main character'),
    ('ending', '/ˈendɪŋ/', 'N', 'soňy', 'концовка', 'the last part of a story', 'The ending surprised everyone.', 'Soňy hemmäni geň galdyrdy.', 'A2', 'a happy ending'),
    ('plot', '/plɒt/', 'N', 'waka düzümi', 'сюжет', 'the story of a film or book', 'The plot was hard to follow.', 'Waka düzümini yzarlamak kyndy.', 'B1', 'a complicated plot'),
    ('scene', '/siːn/', 'N', 'sahna (filmiň)', 'сцена', 'one part of a film', 'The final scene is unforgettable.', 'Soňky sahna ýatdan çykmaz.', 'A2', 'the opening scene'),
    ('soundtrack', '/ˈsaʊndtræk/', 'N', 'film saz toplumy', 'саундтрек', 'the music in a film', 'The soundtrack won an award.', 'Film saz toplumy baýrak aldy.', 'B1', 'film soundtrack'),
    ('special effects', '/ˈspeʃl ɪˌfekts/', 'N', 'ýörite effektler', 'спецэффекты', 'images made by computers in films', 'The special effects look real.', 'Ýörite effektler hakyky görünýär.', 'A2', 'amazing special effects'),
    ('star', '/stɑː(r)/', 'N', 'ýyldyz (aktýor)', 'звезда', 'a famous actor', 'The star of the film is Turkish.', 'Filmiň ýyldyzy türk.', 'A2', 'film star'),
    ('subtitle', '/ˈsʌbtaɪtl/', 'N', 'titr', 'субтитры', 'words at the bottom of a film', 'I watched it with subtitles.', 'Titir bilen gördüm.', 'B1', 'with subtitles'),
    ('villain', '/ˈvɪlən/', 'N', 'ýaman gahryman', 'злодей', 'the bad person in a story', 'The villain steals the diamond.', 'Ýaman gahryman almazy ogarlaýar.', 'B1', 'the villain of'),
    ('setting', '/ˈsetɪŋ/', 'N', 'waka ýeri', 'место действия', 'where and when a story happens', 'The setting is 1920s Paris.', 'Waka ýeri 1920-nji ýyllaryň Pariži.', 'B1', 'the setting of'),
    ('review', '/rɪˈvjuː/', 'N', 'syn', 'рецензия', 'an article saying what a critic thinks', 'The film got good reviews.', 'Film gowy syn aldy.', 'B1', 'write a review'),
    ('based on', '/beɪst ɒn/', 'PHR', 'esaslanýan', 'основанный на', 'using an earlier story or facts', 'The film is based on a true story.', 'Film hakyky wakadan esaslanýar.', 'A2', 'based on a novel'),
    ('action film', '/ˈækʃn fɪlm/', 'N', 'boýewik', 'боевик', 'a film with fighting, cars and exciting events', 'He only watches action films.', 'Diňe боевик filmlerine tomaşa edýär.', 'A2'),
    ('animation', '/ˌænɪˈmeɪʃn/', 'N', 'animasiýa, multfilm', 'анимация', 'a film made with drawings or computer images', 'The children love this animation.', 'Çagalar bu multfilmi söýýär.', 'A2'),
    ('comedy', '/ˈkɒmədi/', 'N', 'komediýa', 'комедия', 'a film that makes you laugh', 'We saw a great comedy last night.', 'Düýn ajaýyp komediýa gördük.', 'A2'),
    ('drama', '/ˈdrɑːmə/', 'N', 'drama', 'драма', 'a serious film about people and their problems', 'The drama won three prizes.', 'Drama üç baýrak aldy.', 'B1'),
    ('historical film', '/hɪˈstɒrɪkl fɪlm/', 'N', 'taryhy film', 'исторический фильм', 'a film set in the past', 'It is a historical film about the war.', 'Urug barada taryhy film.', 'B1'),
    ('musical', '/ˈmjuːzɪkl/', 'N', 'müzikl', 'мюзикл', 'a film where the actors sing and dance', 'We watched an old musical.', 'Köne müzikl gördük.', 'B1'),
    ('thriller', '/ˈθrɪlə/', 'N', 'triller', 'триллер', 'an exciting film, often about crime', 'The thriller kept us awake.', 'Triller bizi ukusyz saklady.', 'B1'),
    ('western', '/ˈwestən/', 'N', 'western', 'вестерн', 'a film about the old American West', 'My grandfather loves westerns.', 'Atam westernleri söýýär.', 'B1'),
    ('critic', '/ˈkrɪtɪk/', 'N', 'tankytçy', 'критик', 'a person who writes opinions about films, books, etc.', 'The critics loved the film.', 'Tankytçylar filmi gowy gördi.', 'B1'),
    ('extra', '/ˈekstrə/', 'N', 'kömekçi aktýor', 'массовка, статист', 'a person employed to play a very small part in a film', 'He worked as an extra in a crowd scene.', 'Mähelle sahnaýynda kömekçi aktýor boldy.', 'B1'),
    ('script', '/skrɪpt/', 'N', 'ssenariý', 'сценарий', 'the words of a film', 'The script was brilliant.', 'Ssenariý ajaýypdy.', 'B1'),
    ('sequel', '/ˈsiːkwəl/', 'N', 'dowamy', 'продолжение, сиквел', 'a film that continues the story of an earlier film', 'The sequel was better than the first film.', 'Dowamy birinji filmden gowy boldy.', 'B1'),
    ('set', '/set/', 'N', 'surat düşürilýän meýdança', 'съемочная площадка', 'the place where a film is made', 'Visitors are not allowed on the set.', 'Myhmanlara meýdança rugsat berilmeýär.', 'B1'),
    ('trailer', '/ˈtreɪlə/', 'N', 'treýler', 'трейлер', 'short scenes from a film, shown to advertise it', 'I saw the trailer for the new Bond film.', 'Täze Bond filminiň treýlerini gördim.', 'B1'),
    ('dubbed', '/dʌbd/', 'ADJ', 'dublyorlanan', 'дублированный', 'with the voices changed into another language', 'The film was dubbed into Russian.', 'Film rus diline dublyorlandy.', 'B1'),
]

# ---- Vocabulary Bank — The body -> 6B ----
T['body'] = [
    ('ankle', '/ˈæŋkl/', 'N', 'ýanjyk', 'лодыжка', 'the joint between foot and leg', 'She twisted her ankle.', 'Ýanjygyny burady.', 'A2', 'twist your ankle'),
    ('chest', '/tʃest/', 'N', 'döş', 'грудь', 'the front part of the body above the stomach', 'He felt a pain in his chest.', 'Döşünde agyry duýdy.', 'A2', 'chest pain'),
    ('elbow', '/ˈelbəʊ/', 'N', 'tirsek', 'локоть', 'the middle joint of the arm', 'He rested his elbows on the table.', 'Tirselerini stola direledi.', 'A2'),
    ('knee', '/niː/', 'N', 'dyz', 'колено', 'the middle joint of the leg', 'The baby crawled on her knees.', 'Çaga dyzynyň üstünde emmekledi.', 'A2', 'on your knees'),
    ('shoulder', '/ˈʃəʊldə(r)/', 'N', 'egin', 'плечо', 'the part where the arm joins the body', 'She carried the bag on one shoulder.', 'Sumkany bir egninde göterdi.', 'A2'),
    ('stomach', '/ˈstʌmək/', 'N', 'garyn', 'живот', 'the part of the body where food goes', 'My stomach hurts.', 'Garynym agyrýar.', 'A1', 'stomach pain'),
    ('thumb', '/θʌm/', 'N', 'başam barmak', 'большой палец', 'the short thick finger on the hand', 'He cut his thumb.', 'Başam barmagyny kesdi.', 'A2'),
    ('toe', '/təʊ/', 'N', 'aya barmagy', 'палец ноги', 'one of the five parts at the end of the foot', 'I stubbed my toe on the bed.', 'Aýak barmagymy düşege kakdyrdym.', 'A2', 'stub your toe'),
    ('waist', '/weɪst/', 'N', 'bil', 'талия', 'the middle part of the body', 'The skirt was tight at the waist.', 'Ýubka bilinden gysyk bolady.', 'B1'),
    ('wrist', '/rɪst/', 'N', 'bil (el)', 'запястье', 'the joint between hand and arm', 'She wore a watch on her wrist.', 'Bilinde sagat bardy.', 'A2', 'break your wrist'),
    ('muscle', '/ˈmʌsl/', 'N', 'myşsa', 'мышца', 'tissue in the body that moves it', 'Exercise strengthens your muscles.', 'Maşk myşsalaryňy berkidýär.', 'A2', 'build muscle'),
    ('skin', '/skɪn/', 'N', 'deri', 'кожа', 'the covering of the body', 'Protect your skin from the sun.', 'Deriňi gün şöhlesinden gora.', 'A2', 'dry skin'),
    ('calf', '/kɑːf/', 'N', 'baldyr', 'икра', 'the back part of the lower leg', 'His calf ached after the run.', 'Ylgandan soň baldyry agyrdy.', 'B1'),
    ('forehead', '/ˈfɔːhed/', 'N', 'maňlaý', 'лоб', 'the part of the face above the eyes', 'She wiped her forehead.', 'Maňlaýyny syldy.', 'A2'),
    ('back', '/bæk/', 'N', 'arka, bel', 'спина', 'the part of your body that you sit on', 'My back hurts after the journey.', 'Ýoldan soň arkam agyrýar.', 'A2'),
    ('chin', '/tʃɪn/', 'N', 'äň', 'подбородок', 'the part of your face under your mouth', 'He has a beard on his chin.', 'Äňinde sakgaly bar.', 'B1'),
    ('ears', '/ɪəz/', 'N', 'gulaklar', 'уши', 'the parts of your body you hear with', 'Rabbits have long ears.', 'Towşanlaryň gulaklary uzyn.', 'A2'),
    ('eyes', '/aɪz/', 'N', 'gözler', 'глаза', 'the parts of your body you see with', 'She has beautiful green eyes.', 'Owadan ýaşyl gözleri bar.', 'A2'),
    ('face', '/feɪs/', 'N', 'ýüz', 'лицо', 'the front part of your head', 'Wash your face every morning.', 'Her irden ýüzüňi ýuw.', 'A2'),
    ('feet', '/fiːt/', 'N', 'aýaklar', 'ступни', 'the parts of your body you stand on', 'My feet are tired.', 'Aýaklarym ýadaw.', 'A2'),
    ('fingers', '/ˈfɪŋɡəz/', 'N', 'barmaklar', 'пальцы (рук)', 'the five long parts of your hand', 'We have ten fingers.', 'On barmagymyz bar.', 'A2'),
    ('hands', '/hændz/', 'N', 'eller', 'кисти рук', 'the parts at the end of your arms', 'Clap your hands!', 'Elleriňi çarp!', 'A2'),
    ('head', '/hed/', 'N', 'kelle', 'голова', 'the top part of your body with your brain', 'She nodded her head.', 'Kellesini atdy.', 'A2'),
    ('legs', '/leɡz/', 'N', 'aýaklar', 'ноги', 'the long parts of your body you walk with', 'Football players have strong legs.', 'Futbolçylaryň aýaklary güýçli.', 'A2'),
    ('lips', '/lɪps/', 'N', 'dodaklar', 'губы', 'the two soft parts of your mouth', 'Her lips were cold.', 'Dodaklary sowukdy.', 'B1'),
    ('mouth', '/maʊθ/', 'N', 'agyz', 'рот', 'the part of your face you eat and speak with', 'Open your mouth and say "ah".', 'Agyzyňy aç we "a" diý.', 'A2'),
    ('neck', '/nek/', 'N', 'boýun', 'шея', 'the part between your head and your body', 'The giraffe has a long neck.', 'Zürafyň boýny uzyn.', 'A2'),
    ('nose', '/nəʊz/', 'N', 'burun', 'нос', 'the part of your face you smell with', 'He broke his nose playing rugby.', 'Regbi oýnap burnuny döwdi.', 'A2'),
    ('teeth', '/tiːθ/', 'N', 'dişler', 'зубы', 'the hard white parts in your mouth', 'The dentist cleaned my teeth.', 'Diş lukmany dişlerimi arassalady.', 'A2'),
    ('tongue', '/tʌŋ/', 'N', 'dil', 'язык', 'the part inside your mouth you taste with', 'You taste with your tongue.', 'Diliň bilen dadýarsyň.', 'B1'),
    ('bite', '/baɪt/', 'V', 'dişlemek', 'кусать', 'to use your teeth to cut something', 'The dog bit my hand.', 'It elimi dişledi.', 'A2'),
    ('clap', '/klæp/', 'V', 'el çarpmak', 'хлопать в ладоши', 'to hit your hands together to show you like something', 'The audience clapped loudly.', 'Tomaşaçylar gaty el çarpdy.', 'B1'),
    ('kick', '/kɪk/', 'V', 'depmek', 'ударять ногой', 'to hit something with your foot', 'He kicked the ball into the goal.', 'Pökgini derwezä depdi.', 'A2'),
    ('nod', '/nɒd/', 'V', 'kelle atmak', 'кивать', 'to move your head down to say yes', 'She nodded and smiled.', 'Kelle atyp ýylgyrdy.', 'B1'),
    ('point', '/pɔɪnt/', 'V', 'barmak bilen görkezmek', 'указывать', 'to show something with your finger', "Don't point at people.", 'Adamlara barmak basma.', 'B1'),
    ('smell', '/smel/', 'V', 'ys almak', 'нюхать, пахнуть', 'to use your nose to find out about something', 'Smell the flowers!', 'Gülleri ysga!', 'A2'),
    ('smile', '/smaɪl/', 'V', 'ýylgyrmak', 'улыбаться', 'to turn up the corners of your mouth', 'She smiled at the baby.', 'Çaga ýylgyrdy.', 'A2'),
    ('stare', '/steə/', 'V', 'tik seretmek', 'пристально смотреть', 'to look at someone for a long time', "Don't stare at people.", 'Adamlara tik seretme.', 'B1'),
    ('taste', '/teɪst/', 'V', 'dat görmek', 'пробовать на вкус', 'to put food in your mouth to find out what it is like', 'Taste the soup and tell me if it needs salt.', 'Çorbany dat gör, duz gerekmi aýt.', 'A2'),
    ('touch', '/tʌtʃ/', 'V', 'ellemek', 'трогать', 'to put your hand on something', 'Do not touch the painting.', 'Suraty elleme.', 'A2'),
    ('throw', '/θrəʊ/', 'V', 'zyňmak', 'бросать', 'to send something through the air with your arm', 'Throw me the ball!', 'Pökgini maňa zyň!', 'A2'),
    ('whistle', '/ˈwɪsl/', 'V', 'şaşgy çalmak, huşlamak', 'свистеть', 'to make a high sound with your lips', 'The referee whistled.', 'Emin şaşgy çaldy.', 'B1'),
]

# ---- Vocabulary Bank — Education -> 7A ----
T['education'] = [
    ('attend', '/əˈtend/', 'V', 'gatnaşmak', 'посещать', 'to go to a school or event', 'She attended every lesson.', 'Her sapaga gatnaşdy.', 'A2', 'attend school'),
    ('degree', '/dɪˈɡriː/', 'N', 'diplom (ylmy dereje)', 'диплом, степень', 'a qualification from a university', 'He has a degree in physics.', 'Fizika boýunça diplomy bar.', 'A2', 'a degree in'),
    ('graduate', '/ˈɡrædʒueɪt/', 'V', 'gutarmak (uniwersitet)', 'оканчивать (вуз)', 'to finish university with a degree', 'She graduated last summer.', 'Geçen tomus uniwersiteti gutardy.', 'A2', 'graduate from'),
    ('revise', '/rɪˈvaɪz/', 'V', 'gaýtalamak (synag üçin)', 'повторять (к экзамену)', 'to study again before an exam', 'I need to revise for the test.', 'Synag üçin gaýtalamaly.', 'A2', 'revise for'),
    ('retake', '/ˌriːˈteɪk/', 'V', 'täzeden tabşyrmak', 'пересдавать', 'to take an exam again', 'He had to retake the exam.', 'Synagy täzeden tabşyrmaly boldy.', 'B1', 'retake an exam'),
    ('skip', '/skɪp/', 'V', 'geçirmek (sapagy)', 'пропускать', 'to not go to a lesson', "Don't skip the first lesson.", 'Birinji sapagy geçirme.', 'A2', 'skip class'),
    ('take an exam', '/teɪk ən ɪɡˈzæm/', 'PHR', 'synag tabşyrmak', 'сдавать экзамен', 'to do an exam', 'They take an exam in June.', 'Iýunda synag tabşyrýarlar.', 'A2'),
    ('lecturer', '/ˈlektʃərə(r)/', 'N', 'mugallym (uniwersitet)', 'преподаватель', 'a teacher at a university', 'The lecturer explained it clearly.', 'Mugallym düşnükli düşündirdi.', 'B1'),
    ('head teacher', '/ˌhed ˈtiːtʃə(r)/', 'N', 'mekdep müdiri', 'директор школы', 'the leader of a school', 'The head teacher gave a speech.', 'Mekdep müdiri çykyş etdi.', 'A2'),
    ('cheat', '/tʃiːt/', 'V', 'aldamak (synagda)', 'списывать, жульничать', 'to break rules to gain an advantage', 'He was caught cheating in the test.', 'Synagda aldaýarka tutuldy.', 'A2', 'cheat in an exam'),
    ('assignment', '/əˈsaɪnmənt/', 'N', 'tabşyryk', 'задание', 'a piece of work for a course', 'The assignment is due Friday.', 'Tabşyryk anna güni tabşyrylmaly.', 'B1', 'finish an assignment'),
    ('deadline', '/ˈdedlaɪn/', 'N', 'möhlet', 'крайний срок', 'the last time you can finish something', 'The deadline is tomorrow.', 'Möhlet ertir.', 'B1', 'meet a deadline'),
    ('campus', '/ˈkæmpəs/', 'N', 'kampus', 'кампус', 'the grounds of a university', 'The campus has three libraries.', 'Kampusda üç kitaphana bar.', 'A2', 'on campus'),
    ('misbehave', '/ˌmɪsbɪˈheɪv/', 'V', 'özüňi erbet alyp barmak', 'плохо себя вести', 'to behave badly', 'If you misbehave, you will be punished.', 'Özüňi erbet alyp barsaň, jezalandyrylarsyň.', 'B1'),
    ('state school', '/ˌsteɪt ˈskuːl/', 'N', 'döwlet mekdebi', 'государственная школа', 'a school run by the government, usually free', 'Most children go to a state school.', 'Köp çaga döwlet mekdebe gatnaýar.', 'B1'),
    ('private school', '/ˌpraɪvət ˈskuːl/', 'N', 'hususy mekdep', 'частная школа', 'a school you have to pay to go to', 'Private schools can be very expensive.', 'Hususy mektepler gaty gymmat bolup biler.', 'B1'),
    ('nursery school', '/ˈnɜːsəri skuːl/', 'N', 'çagalar bagy', 'детский сад, ясли', 'a school for children between two and four', 'My daughter starts nursery school next month.', 'Gyzym indiki aý çagalar bagyna başlaýar.', 'B1'),
    ('primary school', '/ˈpraɪməri skuːl/', 'N', 'başlangyç mekdep', 'начальная школа', 'a school for children between five and eleven', 'He teaches at a primary school.', 'Başlangyç mekdepde sapak berýär.', 'B1'),
    ('expelled', '/ɪkˈspeld/', 'ADJ', 'mekdepden kowulan', 'исключённый (из школы)', 'made to leave school as a punishment', 'He was expelled for cheating.', 'Aldaw üçin mekdepden kowuldy.', 'B1'),
    ('punished', '/ˈpʌnɪʃt/', 'ADJ', 'jezalandyrylan', 'наказанный', 'given a punishment for doing something wrong', 'She was punished for being late.', 'Giç galany üçin jezalandyryldy.', 'B1'),
]

# ---- Vocabulary Bank — Houses -> 7B ----
T['houses'] = [
    ('attic', '/ˈætɪk/', 'N', 'ýerlik', 'чердак', 'the room under the roof', 'Old boxes are in the attic.', 'Köne gutular ýerlikde.', 'B1', 'in the attic'),
    ('basement', '/ˈbeɪsmənt/', 'N', 'zemin', 'подвал', 'the room below ground level', 'We store bikes in the basement.', 'Welosipedleri zeminde saklaýarys.', 'B1', 'in the basement'),
    ('ceiling', '/ˈsiːlɪŋ/', 'N', 'potolok', 'потолок', 'the top inside surface of a room', 'The ceiling needs painting.', 'Potology reňklemeli.', 'A2', 'high ceiling'),
    ('cottage', '/ˈkɒtɪdʒ/', 'N', 'obadaky kiçi öý', 'коттедж, деревенский дом', 'a small house in the countryside', 'They rent a cottage by the lake.', 'Köliň ýanyndaky öýi kärendesine alýarlar.', 'A2'),
    ('fence', '/fens/', 'N', 'haýat', 'забор', 'a barrier round a garden', 'The cat jumped over the fence.', 'Pişik haýatdan bökdi.', 'A2', 'over the fence'),
    ('fireplace', '/ˈfaɪəpleɪs/', 'N', 'ojag', 'камин', 'the place where a fire burns indoors', 'We sat by the fireplace.', 'Ojagyň ýanynda oturduk.', 'B1', 'by the fireplace'),
    ('ground floor', '/ˈɡraʊnd flɔː(r)/', 'N', 'birinji gat', 'первый этаж (нижний)', 'the floor at street level', 'The shop is on the ground floor.', 'Dükan birinji gatda.', 'A2', 'on the ground floor'),
    ('first floor', '/ˌfɜːst ˈflɔː(r)/', 'N', 'ikinji gat', 'второй этаж (брит.)', 'the floor above the ground floor', 'Their flat is on the first floor.', 'Öýleri ikinji gatda.', 'A2', 'on the first floor'),
    ('lift', '/lɪft/', 'N', 'lift', 'лифт', 'a machine that moves people up in a building', 'Take the lift to the fifth floor.', 'Bäşinji gata liftde çyk.', 'A1', 'take the lift'),
    ('stairs', '/steəz/', 'N', 'basgançak', 'лестница', 'steps from one floor to another', 'She ran up the stairs.', 'Basgançakdan ylgap çykdy.', 'A1', 'climb the stairs'),
    ('upstairs', '/ˌʌpˈsteəz/', 'ADV', 'ýokarky gatda', 'наверху', 'on a higher floor', 'The bedrooms are upstairs.', 'Ýatak otaglary ýokarky gatda.', 'A2', 'go upstairs'),
    ('downstairs', '/ˌdaʊnˈsteəz/', 'ADV', 'aşaky gatda', 'внизу', 'on a lower floor', 'The kitchen is downstairs.', 'Aşhana aşaky gatda.', 'A2', 'go downstairs'),
    ('move in', '/muːv ɪn/', 'PHR', 'göçüp gelmek', 'заселяться', 'to start living in a new home', 'They moved in last month.', 'Geçen aý göçüp geldiler.', 'A2', 'move in together'),
    ('move out', '/muːv aʊt/', 'PHR', 'göçüp gitmek', 'выселяться', 'to stop living in a home', 'He moved out at eighteen.', 'On sekiz ýaşynda göçüp gitdi.', 'A2', 'move out of'),
    ('second floor', '/ˌsekənd ˈflɔː/', 'N', 'ikinji gat', 'второй этаж', 'the floor above the first floor', 'They live on the second floor.', 'Ikinji gatda ýaşaýarlar.', 'A2'),
    ('balcony', '/ˈbælkəni/', 'N', 'balkon', 'балкон', 'a platform outside an upper window or door', 'We had breakfast on the balcony.', 'Balkonda ertirlik etdik.', 'B1'),
    ('entrance', '/ˈentrəns/', 'N', 'girelge', 'вход', 'the door or place where you go into a building', 'Wait for me at the main entrance.', 'Esasy girelgede garaş.', 'B1'),
    ('wall', '/wɔːl/', 'N', 'diwar', 'стена', 'the side part of a room or building', 'There is a picture on the wall.', 'Diwarda surat bar.', 'A2'),
    ('gate', '/ɡeɪt/', 'N', 'derweze', 'ворота, калитка', 'a door in a fence or wall outside a building', 'Close the gate behind you.', 'Yzyňdan derwezäni ýap.', 'B1'),
    ('roof', '/ruːf/', 'N', 'üçek', 'крыша', 'the top part of a building', 'The cat sat on the roof.', 'Pişik üçekde otyrdy.', 'A2'),
    ('chimney', '/ˈtʃɪmni/', 'N', 'tüsseçe', 'дымоход, труба', 'a pipe on a roof that carries smoke away', 'Smoke came out of the chimney.', 'Tüsseçeden tüssa çykdy.', 'B1'),
    ('outskirts', '/ˈaʊtskɜːts/', 'N', 'şäher etegi', 'окраина', 'the areas around the edge of a city', 'They live on the outskirts of town.', 'Şäher eteginde ýaşaýarlar.', 'B1'),
    ('path', '/pɑːθ/', 'N', 'ýodajyk', 'тропинка', 'a narrow way for walking', 'A stone path leads to the door.', 'Daş ýodajyk gapa alyp barýar.', 'B1'),
    ('terrace', '/ˈterəs/', 'N', 'terrassa; bitişik öýler hatary', 'терраса; ряд домов', 'an outdoor area next to a house, or a row of similar houses', 'We sat on the terrace in the sun.', 'Günde terrasa otyrдыk.', 'B1'),
    ('top floor', '/ˌtɒp ˈflɔː/', 'N', 'iň ýokarky gat', 'верхний этаж', 'the highest floor of a building', 'The flat is on the top floor.', 'Öý iň ýokarky gatda.', 'A2'),
]

# ---- Vocabulary Bank — Work -> 8A ----
T['work'] = [
    ('apply for', '/əˈplaɪ fə(r)/', 'PHR', 'ýüz tutmak', 'подавать заявку', 'to formally ask for a job', 'She applied for three jobs.', 'Üç işe ýüz tutdy.', 'A2', 'apply for a job'),
    ('colleague', '/ˈkɒliːɡ/', 'N', 'işdeş', 'коллега', 'a person you work with', 'A colleague helped me with the report.', 'Işdeşim hasabatda kömek etdi.', 'A2'),
    ('employee', '/ɪmˈplɔɪiː/', 'N', 'işgär', 'работник', 'a person who works for a company', 'The company has 300 employees.', 'Kompaniýada 300 işgär bar.', 'A2'),
    ('employer', '/ɪmˈplɔɪə(r)/', 'N', 'iş beriji', 'работодатель', 'a person or company that gives jobs', 'Her employer pays for training.', 'Iş berijisi okuw üçin töleýär.', 'A2'),
    ('full-time', '/ˌfʊl ˈtaɪm/', 'ADJ', 'doly ştatly', 'полный рабочий день', 'working all the usual hours', 'He found a full-time job.', 'Doly ştatly iş tapdy.', 'A2', 'full-time job'),
    ('overtime', '/ˈəʊvətaɪm/', 'N', 'goşmaça iş sagady', 'сверхурочные', 'extra hours worked', 'She did ten hours of overtime.', 'On sagat goşmaça işledi.', 'B1', 'do overtime'),
    ('get a promotion', '/ɡet ə prəˈməʊʃn/', 'PHR', 'wezipesi galmak', 'получить повышение', 'to move to a better job level', 'He got a promotion in March.', 'Mart aýynda wezipesi galdy.', 'A2'),
    ('get the sack', '/ɡet ðə sæk/', 'PHR', 'işden kowulmak', 'быть уволенным', 'to be dismissed from a job (informal)', 'He got the sack for being late.', 'Giç galany üçin işden kowuldy.', 'B1'),
    ('resign', '/rɪˈzaɪn/', 'V', 'işden çekilmek', 'увольняться (самому)', 'to leave a job by choice', 'She resigned after five years.', 'Bäş ýyldan soň işden çekildi.', 'B1', 'resign from'),
    ('temporary', '/ˈtemprəri/', 'ADJ', 'wagtlaýyn', 'временный', 'lasting for a limited time', 'It is only a temporary job.', 'Diňe wagtlaýyn iş.', 'A2', 'temporary work'),
    ('permanent', '/ˈpɜːmənənt/', 'ADJ', 'hemişelik', 'постоянный', 'lasting for ever; not temporary', 'She wants a permanent position.', 'Hemişelik wezipe isleýär.', 'A2', 'permanent job'),
    ('workload', '/ˈwɜːkləʊd/', 'N', 'iş ýüki', 'рабочая нагрузка', 'the amount of work you have', 'His workload doubled this month.', 'Iş ýüki şu aý iki esse artdy.', 'B1', 'heavy workload'),
    ('shift', '/ʃɪft/', 'N', 'çalyşma', 'смена', 'a period of time worked', 'She works the night shift.', 'Gije çalyşmasynda işleýär.', 'A2', 'night shift'),
    ('interview', '/ˈɪntəvjuː/', 'N', 'söhbetdeşlik', 'собеседование', 'a meeting to decide if you get a job', 'The interview went well.', 'Söhbetdeşlik gowy geçdi.', 'A2', 'job interview'),
    ('retire', '/rɪˈtaɪə/', 'V', 'pensija çykmak', 'уходить на пенсию', 'to stop working because of your age', 'She is going to retire next month.', 'Indiki aý pensija çykýar.', 'B1'),
    ('set up', '/ˌset ˈʌp/', 'PHR', 'esaslandyrmak, gurmak', 'основывать (бизнес)', 'to start a business', 'She set up a business selling clothes online.', 'Onlaýn eşik satýan biznes esaslandyrdy.', 'B1'),
    ('be made redundant', '/ˌmeɪd rɪˈdʌndənt/', 'PHR', 'işden boşadylmak', 'быть сокращённым', 'to lose your job because the company no longer needs you', 'He was made redundant last week.', 'Geçen hepde işden boşadyldy.', 'B1'),
    ('freelance', '/ˈfriːlɑːns/', 'ADJ', 'frilans, erkin işleýän', 'фриланс, внештатный', 'working for different companies, not one employer', 'She is a freelance journalist.', 'Frilans žurnalist.', 'B1'),
    ('part-time', '/ˌpɑːt ˈtaɪm/', 'ADJ', 'ýarym ştatly', 'работающий неполный день', 'working only some hours of the week', 'He has a part-time job in a café.', 'Kafede ýarym ştatly işi bar.', 'A2'),
    ('self-employed', '/ˌself ɪmˈplɔɪd/', 'ADJ', 'özi üçin işleýän', 'самозанятый', 'working for yourself, not for a company', "He's self-employed now.", 'Häzir özi üçin işleýär.', 'B1'),
    ('unemployed', '/ˌʌnɪmˈplɔɪd/', 'ADJ', 'işsiz', 'безработный', 'without a job', "I'm unemployed at the moment.", 'Häzirki wagt işsiz.', 'B1'),
    ('boss', '/bɒs/', 'N', 'başlyk, boss', 'начальник, босс', 'the person who tells you what to do at work', 'Ask your boss for a holiday.', 'Bossuňdan dynç alyş sora.', 'A2'),
    ('gardener', '/ˈɡɑːdnə/', 'N', 'bagban', 'садовник', 'a person whose job is taking care of a garden', 'The gardener cut the grass.', 'Bagban ot ýazdy.', 'B1'),
    ('hairdresser', '/ˈheədresə/', 'N', 'sartaraş', 'парикмахер', 'a person whose job is cutting hair', 'I go to the same hairdresser.', 'Bir sartaraşa gatnaýaryn.', 'A2'),
    ('look for a job', '/ˌlʊk fər ə ˈdʒɒb/', 'PHR', 'iş gözlemek', 'искать работу', 'to try to find work', 'She looked for a job online.', 'Onlaýn iş gözledi.', 'A2'),
    ('quit', '/kwɪt/', 'V', 'işi taşlamak', 'увольняться, бросать', 'to leave your job (American English)', 'He quit his job in June.', 'Iýunda işini taşlady.', 'B1'),
    ('vet', '/vet/', 'N', 'weterinar', 'ветеринар', 'a doctor for animals', 'We took the cat to the vet.', 'Pişigi weterinara äkitdik.', 'B1'),
]

# ---- in-lesson — shopping · nouns from verbs -> 8B ----
T['shopping2'] = [
    ('browse', '/braʊz/', 'V', 'göz aýlamak', 'просматривать (магазины)', 'to look at things without planning to buy', 'I was just browsing, thanks.', 'Diňe göz aýlaýardym, sag boluň.', 'B1', 'browse the shelves'),
    ('chain', '/tʃeɪn/', 'N', 'dükanlar zynjyry', 'сеть магазинов', 'a group of shops with the same name', 'It is a big supermarket chain.', 'Uly marketler zynjyry.', 'A2', 'a chain store'),
    ('delivery', '/dɪˈlɪvəri/', 'N', 'eltip bermek', 'доставка', 'bringing goods to your home', 'Delivery is free over 100 manat.', '100 manatdan ýokary eltip bermek mugt.', 'A2', 'free delivery'),
    ('department store', '/dɪˈpɑːtmənt stɔː(r)/', 'N', 'universam', 'универмаг', 'a large shop with many sections', 'The department store has six floors.', 'Universamyň alty gaty bar.', 'A2'),
    ('goods', '/ɡʊdz/', 'N', 'harytlar', 'товары', 'things that are sold', 'The goods arrived damaged.', 'Harytlar zeper ýetip geldi.', 'A2', 'electrical goods'),
    ('in stock', '/ɪn stɒk/', 'PHR', 'bar', 'в наличии', 'available to buy now', 'The blue one is in stock.', 'Gök reňklisi bar.', 'A2', 'have in stock'),
    ('out of stock', '/aʊt əv stɒk/', 'PHR', 'ýok', 'нет в наличии', 'not available to buy now', 'The phone is out of stock.', 'Telefon ýok.', 'A2', 'be out of stock'),
    ('online', '/ˌɒnˈlaɪn/', 'ADV', 'onlaýn', 'онлайн', 'on the internet', 'I bought the tickets online.', 'Biletleri onlaýn aldym.', 'A1', 'shop online'),
    ('window shopping', '/ˈwɪndəʊ ˌʃɒpɪŋ/', 'N', 'diňe seredip gezme', 'рассматривание витрин', 'looking at shops without buying', 'We did some window shopping.', 'Biraz diňe seredip gezdik.', 'A2'),
    ('agreement', '/əˈɡriːmənt/', 'N', 'ylalaşyk', 'соглашение', 'a decision people make together', 'We reached an agreement.', 'Ylalaşyga geldik.', 'A2', 'reach an agreement'),
    ('approval', '/əˈpruːvl/', 'N', 'makullama', 'одобрение', 'the feeling that something is good', 'She nodded her approval.', 'Makullap baş atdy.', 'B1', 'give approval'),
    ('arrival', '/əˈraɪvl/', 'N', 'gelmek', 'прибытие', 'the act of arriving', 'On arrival, go to reception.', 'Gelende resepsiýa baryň.', 'B1', 'on arrival'),
    ('invitation', '/ˌɪnvɪˈteɪʃn/', 'N', 'çakylyk', 'приглашение', 'a request to come to an event', 'We got an invitation to the wedding.', 'Toýa çakylyk aldyk.', 'A2', 'accept an invitation'),
    ('discovery', '/dɪˈskʌvəri/', 'N', 'üsti açma', 'открытие (находка)', 'finding something new', 'It was an important discovery.', 'Möhüm üsti açma boldy.', 'A2', 'make a discovery'),
]

# ---- in-lesson — making adjectives and adverbs -> 9A ----
T['adj_adv_formation'] = [
    ('careless', '/ˈkeələs/', 'ADJ', 'ünsüz', 'невнимательный', 'not taking care', 'A careless mistake cost us the game.', 'Ünsüz ýalňyşlyk oýny elimizden aldy.', 'A2'),
    ('creative', '/kriˈeɪtɪv/', 'ADJ', 'döredijilikli', 'творческий', 'good at thinking of new ideas', 'She found a creative solution.', 'Döredijilikli çözgüt tapdy.', 'A2', 'creative ideas'),
    ('dangerous', '/ˈdeɪndʒərəs/', 'ADJ', 'howply', 'опасный', 'able to hurt you', 'Swimming here is dangerous.', 'Bu ýerde ýüzmek howply.', 'A1'),
    ('deaf', '/def/', 'ADJ', 'kereň', 'глухой', 'unable to hear', 'The deaf man read her lips.', 'Kereň adam onuň dodaklaryny okady.', 'A2'),
    ('economical', '/ˌiːkəˈnɒmɪkl/', 'ADJ', 'tygşytly', 'экономичный', 'using little money or fuel', 'This car is very economical.', 'Bu maşyn gaty tygşytly.', 'B1'),
    ('effective', '/ɪˈfektɪv/', 'ADJ', 'netijeli', 'эффективный', 'working well', 'The new system is more effective.', 'Täze ulgam has netijeli.', 'A2', 'an effective method'),
    ('endless', '/ˈendləs/', 'ADJ', 'tükeniksiz', 'бесконечный', 'seeming to have no end', 'The journey felt endless.', 'Syýahat tükeniksiz ýaly boldy.', 'B1'),
    ('harmful', '/ˈhɑːmfl/', 'ADJ', 'zyýanly', 'вредный', 'causing damage', 'Sugar is harmful to teeth.', 'Şeker dişlere zyýanly.', 'A2', 'harmful to'),
    ('homeless', '/ˈhəʊmləs/', 'ADJ', 'öýsüz', 'бездомный', 'having no home', 'They helped homeless people.', 'Öýsüz adamlara kömek etdiler.', 'A2'),
    ('hopeful', '/ˈhəʊpfl/', 'ADJ', 'umytly', 'полный надежды', 'feeling that good things will happen', 'She felt hopeful about the result.', 'Netijeden umytly boldy.', 'B1'),
    ('ideal', '/aɪˈdiːəl/', 'ADJ', 'ajaýyp (laýyk)', 'идеальный', 'perfect for a purpose', 'The weather was ideal for a picnic.', 'Howa piknik üçin ajaýyp boldy.', 'A2', 'ideal for'),
    ('practical', '/ˈpræktɪkl/', 'ADJ', 'amaly', 'практичный', 'useful and sensible', 'Wear practical shoes for the walk.', 'Ýöriş üçin amaly aýakgap geý.', 'A2', 'practical advice'),
    ('predictable', '/prɪˈdɪktəbl/', 'ADJ', 'öňünden aýdyp bolýan', 'предсказуемый', 'happening as you expect', 'The ending was completely predictable.', 'Soňy düýbünden öňünden aýdyp bolýan boldy.', 'B1'),
    ('reasonable', '/ˈriːznəbl/', 'ADJ', 'makul', 'разумный', 'fair and sensible', 'The price was reasonable.', 'Baha makul boldy.', 'A2', 'a reasonable price'),
    ('suitable', '/ˈsuːtəbl/', 'ADJ', 'laýyk', 'подходящий', 'right for a purpose', 'The film is not suitable for children.', 'Film çagalar üçin laýyk däl.', 'A2', 'suitable for'),
    ('typical', '/ˈtɪpɪkl/', 'ADJ', 'adaty', 'типичный', 'normal for its kind', 'A typical day starts at seven.', 'Adaty gün ýedide başlaýar.', 'A2', 'a typical example'),
    ('unforgettable', '/ˌʌnfəˈɡetəbl/', 'ADJ', 'ýatdan çykmaz', 'незабываемый', 'impossible to forget', 'We had an unforgettable holiday.', 'Ýatdan çykmaz dynç alyş geçirdik.', 'A2'),
    ('unnecessary', '/ʌnˈnesəsəri/', 'ADJ', 'gereksiz', 'ненужный', 'not needed', 'The meeting was unnecessary.', 'Duşuşyk gereksiz boldy.', 'A2'),
    ('unusual', '/ʌnˈjuːʒuəl/', 'ADJ', 'adaty däl', 'необычный', 'not normal or common', 'We heard an unusual noise.', 'Adaty däl ses eşitdik.', 'A2'),
    ('compensation', '/ˌkɒmpenˈseɪʃn/', 'N', 'öwez pulu', 'компенсация', 'money you get because something bad happened', 'The airline paid compensation for the delay.', 'Awiaşirket giýikme üçin öwez puluny töledi.', 'B1'),
    ('argument', '/ˈɑːɡjumənt/', 'N', 'jedel, dawa', 'спор, аргумент', 'an angry disagreement', 'They had an argument about money.', 'Pul barada dawa etdiler.', 'B1'),
    ('success', '/səkˈses/', 'N', 'üstünlik', 'успех', 'when something works well or wins', 'The party was a great success.', 'Toý uly üstünlik boldy.', 'B1'),
    ('achievement', '/əˈtʃiːvmənt/', 'N', 'üstünlik, gazanan zady', 'достижение', 'something difficult that you do well', 'Passing the exam was a big achievement.', 'Synagdan geçmek uly üstünlikdi.', 'B1'),
    ('explanation', '/ˌekspləˈneɪʃn/', 'N', 'düşündiriş', 'объяснение', 'words that make something clear', 'He gave no explanation for being late.', 'Giç galmagyna düşündiriş bermedi.', 'B1'),
    ('attachment', '/əˈtætʃmənt/', 'N', 'goşundy', 'вложение (в письме)', 'a file you send with an email', 'Did you get the attachment?', 'Goşundyny aldyňmy?', 'B1'),
    ('demonstration', '/ˌdemənˈstreɪʃn/', 'N', 'demonstrasiýa, görkezme', 'демонстрация', 'an act of showing how something works, or a public protest', 'They watched a cooking demonstration.', 'Nahar bişirmek görkezmesine tomaşa etdiler.', 'B1'),
    ('payment', '/ˈpeɪmənt/', 'N', 'töleg', 'платёж', 'the act of paying, or the money you pay', 'The payment arrived late.', 'Töleg giç geldi.', 'B1'),
    ('loss', '/lɒs/', 'N', 'ýitgi', 'потеря, убыток', 'when you lose something', 'The company made a big loss.', 'Kompaniýa uly ýitgi çekdi.', 'B1'),
    ('sale', '/seɪl/', 'N', 'satuw', 'продажа', 'the act of selling something', 'The sale of the house took a month.', 'Öýüň satuwly bir aý aldy.', 'B1'),
]

# ---- in-lesson — electronic devices -> 9B ----
T['devices'] = [
    ('app', '/æp/', 'N', 'programma', 'приложение', 'a program on a phone', 'I downloaded a language app.', 'Dil programmasyny ýükledim.', 'A1', 'download an app'),
    ('attach', '/əˈtætʃ/', 'V', 'goşmak (faýl)', 'прикреплять', 'to add a file to a message', 'Attach the photo to the email.', 'Suraty emaila goş.', 'B1', 'attach a file'),
    ('cable', '/ˈkeɪbl/', 'N', 'kabel', 'кабель', 'a thick wire', 'Connect the cable to the TV.', 'Kabeli telewizora birikdir.', 'A2', 'USB cable'),
    ('charger', '/ˈtʃɑːdʒə(r)/', 'N', 'zarýadnik', 'зарядное устройство', 'a device that fills a battery', 'I forgot my charger at home.', 'Zarýadnik öýde galdy.', 'A2', 'phone charger'),
    ('connect', '/kəˈnekt/', 'V', 'birikdirmek', 'подключать', 'to join devices together', 'Connect the printer to the network.', 'Printeri tora birikdir.', 'A2', 'connect to'),
    ('delete', '/dɪˈliːt/', 'V', 'pozmak', 'удалять', 'to remove a file or message', 'I deleted the old photos.', 'Köne suratlary pozdum.', 'A2', 'delete a message'),
    ('download', '/ˌdaʊnˈləʊd/', 'V', 'ýüklemek', 'скачивать', 'to copy files from the internet', 'Download the map before the trip.', 'Syýahatdan öň kartany ýükle.', 'A2', 'download a file'),
    ('headphones', '/ˈhedfəʊnz/', 'N', 'gulaklyk', 'наушники', 'speakers you wear on your ears', 'He listens with headphones.', 'Gulaklyk bilen diňleýär.', 'A1', 'wear headphones'),
    ('keyboard', '/ˈkiːbɔːd/', 'N', 'klawiatura', 'клавиатура', 'the keys you type on', 'The keyboard needs cleaning.', 'Klawiaturany arassalamaly.', 'A2', 'on the keyboard'),
    ('laptop', '/ˈlæptɒp/', 'N', 'noutbuk', 'ноутбук', 'a small portable computer', 'She works on her laptop.', 'Noutbukda işleýär.', 'A1', 'open your laptop'),
    ('plug in', '/plʌɡ ɪn/', 'PHR', 'tok çeşmesine birikdirmek', 'включать в розетку', 'to connect to electricity', 'Plug in the lamp, please.', 'Çyrany tok çeşmesine birikdir.', 'A2', 'plug in the charger'),
    ('remote control', '/rɪˌməʊt kənˈtrəʊl/', 'N', 'pult', 'пульт', 'a device to control a TV', 'Where is the remote control?', 'Pult nirede?', 'A2', 'TV remote control'),
    ('screen', '/skriːn/', 'N', 'ekran', 'экран', 'the flat part that shows pictures', 'The screen cracked when it fell.', 'Gaçanda ekrany döwüldi.', 'A1', 'touch screen'),
    ('scroll', '/skrəʊl/', 'V', 'aşak süýşürmek', 'прокручивать', 'to move text up or down', 'Scroll down to read more.', 'Köpräk okamak üçin aşak süýşür.', 'A2', 'scroll down'),
    ('upload', '/ˌʌpˈləʊd/', 'V', 'ýüklemek (ýokary)', 'загружать (в интернет)', 'to send files to the internet', 'She uploaded the video.', 'Wideo ýükledi.', 'A2', 'upload a photo'),
    ('wireless', '/ˈwaɪələs/', 'ADJ', 'simsiz', 'беспроводной', 'working without wires', 'The hotel has wireless internet.', 'Myhmanhanada simsiz internet bar.', 'A2', 'wireless internet'),
]

# ---- in-lesson — compound nouns -> 10A ----
T['compound_nouns'] = [
    ('fast food', '/ˌfɑːst ˈfuːd/', 'N', 'çalt nahar', 'фастфуд', 'food that is cooked and served quickly', 'We ate fast food on the way.', 'Ýolda çalt nahar iýdik.', 'A2', 'fast food restaurant'),
    ('free time', '/ˌfriː ˈtaɪm/', 'N', 'boş wagt', 'свободное время', 'time when you are not working', 'What do you do in your free time?', 'Boş wagtyňda näme edýärsiň?', 'A1', 'in your free time'),
    ('hairdryer', '/ˈheədraɪə(r)/', 'N', 'saç guradyjy', 'фен', 'a machine that dries hair', 'The hairdryer is in the bathroom.', 'Saç guradyjy hammamda.', 'A2'),
    ('mobile phone', '/ˌməʊbaɪl ˈfəʊn/', 'N', 'jübi telefony', 'мобильный телефон', 'a phone you carry with you', 'She left her mobile phone at home.', 'Jübi telefonuny öýde goýdy.', 'A1'),
    ('mother tongue', '/ˌmʌðə ˈtʌŋ/', 'N', 'ene dili', 'родной язык', 'the first language you learn', 'Turkmen is my mother tongue.', 'Türkmen dili meniň ene dilim.', 'A2'),
    ('public transport', '/ˌpʌblɪk ˈtrænspɔːt/', 'N', 'jemgyýetçilik ulagy', 'общественный транспорт', 'buses, trains and trams', 'Public transport is cheap here.', 'Jemgyýetçilik ulagy bu ýerde arzan.', 'A2', 'by public transport'),
    ('second language', '/ˌsekənd ˈlæŋɡwɪdʒ/', 'N', 'ikinji dil', 'второй язык', 'a language learned after your first', 'English is her second language.', 'Iňlis dili onuň ikinji dili.', 'A1'),
    ('social media', '/ˌsəʊʃl ˈmiːdiə/', 'N', 'sosial media', 'социальные сети', 'websites where people share things', 'She spends hours on social media.', 'Sosial mediada sagatlap oturýar.', 'A2', 'on social media'),
    ('waiting list', '/ˈweɪtɪŋ lɪst/', 'N', 'nobat sanawy', 'лист ожидания', 'a list of people waiting for something', 'There is a long waiting list.', 'Uzyn nobat sanawy bar.', 'B1', 'on a waiting list'),
    ('washing machine', '/ˈwɒʃɪŋ məʃiːn/', 'N', 'kir ýuwujy maşyn', 'стиральная машина', 'a machine that washes clothes', 'Put the shirts in the washing machine.', 'Köýnekleri kir ýuwujy maşyna sal.', 'A1'),
    ('weekend break', '/ˌwiːkˈend breɪk/', 'N', 'hepde ahyry dynç alşy', 'поездка на выходные', 'a short holiday at the weekend', 'We had a weekend break in Awaza.', 'Awazada hepde ahyry dynç alşy geçirdik.', 'B1', 'a weekend break'),
    ('swimming pool', '/ˈswɪmɪŋ puːl/', 'N', 'ýüzülýän howuz', 'бассейн', 'a place filled with water for swimming', 'The hotel has a swimming pool.', 'Myhmanhanada ýüzülýän howuz bar.', 'A1'),
    ('dining room', '/ˈdaɪnɪŋ ruːm/', 'N', 'nahar otagy', 'столовая', 'a room where meals are eaten', 'The dining room seats eight.', 'Nahar otagy sekiz adamlyk.', 'A2'),
    ('post office', '/ˈpəʊst ɒfɪs/', 'N', 'poçta', 'почта (учреждение)', 'a place where you send letters', 'The post office closes at six.', 'Poçta altyda ýapylýar.', 'A1'),
]

# ---- in-lesson — crime -> 10B ----
T['crime'] = [
    ('arrest', '/əˈrest/', 'V', 'tussag etmek', 'арестовывать', 'to take someone to the police', 'The police arrested the thief.', 'Polisiýa ogruny tussag etdi.', 'A2', 'arrest a suspect'),
    ('burglar', '/ˈbɜːɡlə(r)/', 'N', 'öý ogrysy', 'вор-взломщик', 'a person who steals from houses', 'A burglar took the TV.', 'Öý ogrysy telewizory aldy.', 'B1'),
    ('commit a crime', '/kəˈmɪt ə kraɪm/', 'PHR', 'jenaýat etmek', 'совершить преступление', 'to do something illegal', 'He committed a crime at twenty.', 'Ýigrimi ýaşynda jenaýat etdi.', 'A2'),
    ('court', '/kɔːt/', 'N', 'kazyýet', 'суд', 'the place where trials happen', 'The case went to court.', 'Iş kazyýete gitdi.', 'A2', 'in court'),
    ('criminal', '/ˈkrɪmɪnl/', 'N', 'jenaýatçy', 'преступник', 'a person who breaks the law', 'The criminal was sent to prison.', 'Jenaýatçy türmä iberildi.', 'A2'),
    ('detective', '/dɪˈtektɪv/', 'N', 'derňewçi', 'детектив', 'a police officer who solves crimes', 'The detective found the clue.', 'Derňewçi yzy tapdy.', 'A2'),
    ('evidence', '/ˈevɪdəns/', 'N', 'subutnama', 'улика, доказательство', 'facts that show something is true', 'There was no evidence.', 'Subutnama ýokdy.', 'B1', 'find evidence'),
    ('guilty', '/ˈɡɪlti/', 'ADJ', 'günäkär', 'виновный', 'responsible for a crime', 'The jury found him guilty.', 'Kazyýet ony günäkär tapdy.', 'A2', 'feel guilty'),
    ('innocent', '/ˈɪnəsnt/', 'ADJ', 'günäsiz', 'невинный', 'not responsible for a crime', 'She was proved innocent.', 'Günäsizdigi subut edildi.', 'A2'),
    ('judge', '/dʒʌdʒ/', 'N', 'kazy', 'судья', 'the person who decides in court', 'The judge asked for silence.', 'Kazy sessizlik sorady.', 'A2'),
    ('jury', '/ˈdʒʊəri/', 'N', 'halk kazylary', 'присяжные', 'the people who decide guilt in court', 'The jury reached a decision.', 'Halk kazylary karara geldi.', 'B1'),
    ('murder', '/ˈmɜːdə(r)/', 'N', 'adam öldürme', 'убийство', 'the crime of killing someone', 'The murder shocked the town.', 'Adam öldürme şäheri şok etdi.', 'A2', 'commit murder'),
    ('prison', '/ˈprɪzn/', 'N', 'türme', 'тюрьма', 'where criminals are kept', 'He spent ten years in prison.', 'Türmede on ýyl geçirdi.', 'A2', 'in prison'),
    ('sentence', '/ˈsentəns/', 'N', 'höküm', 'приговор', "a judge's punishment decision", 'He got a five-year sentence.', 'Bäş ýyllyk höküm aldy.', 'B1', 'a prison sentence'),
    ('steal', '/stiːl/', 'V', 'ogurlamak', 'красть', 'to take what is not yours', 'Someone stole my bike.', 'Biri welosipedimi ogurlady.', 'A1'),
    ('suspect', '/ˈsʌspekt/', 'N', 'gümän edilýän', 'подозреваемый', 'a person thought to have done a crime', 'The police questioned two suspects.', 'Polisiýa iki gümän edilýäni sorag etdi.', 'B1', 'the main suspect'),
    ('theft', '/θeft/', 'N', 'ogurlyk', 'кража', 'the crime of stealing', 'The theft happened at night.', 'Ogurlyk gije boldy.', 'A2'),
    ('trial', '/ˈtraɪəl/', 'N', 'kazyýet işi', 'судебный процесс', 'the court case against someone', 'The trial lasted three weeks.', 'Kazyýet işi üç hepde dowam etdi.', 'B1', 'on trial'),
    ('witness', '/ˈwɪtnəs/', 'N', 'şaýat', 'свидетель', 'a person who saw a crime', 'The witness described the man.', 'Şaýat adamy wasyp etdi.', 'A2', 'eye witness'),
]

# ---- Practical English episodes ----
T['pe_react'] = [
    ('Really?', '/ˈrɪəli/', 'INTJ', 'Hakykatdanam?', 'Правда?', 'used to show interest or surprise', 'Really? That is great news!', 'Hakykatdanam? Bu ajaýyp habar!', 'A1'),
    ('What a pity', '/wɒt ə ˈpɪti/', 'PHR', 'Ýazyk!', 'Как жаль!', 'used to show you are sorry about something', 'What a pity you missed it!', 'Görmedigiň ýazyk!', 'A2'),
    ('Congratulations', '/kənˌɡrætʃuˈleɪʃnz/', 'INTJ', 'Gutlaýaryn!', 'Поздравляю!', 'used to praise good news', 'Congratulations on your new job!', 'Täze işiň bilen gutlaýaryn!', 'A2'),
    ('Good for you', '/ɡʊd fə juː/', 'PHR', 'Sag bol, afaryn!', 'Молодец!', 'used to show you are pleased for someone', 'You passed? Good for you!', 'Geçdiňmi? Afaryn!', 'A2'),
    ('Sounds great', '/saʊndz ɡreɪt/', 'PHR', 'Ajap eşidilýär!', 'Звучит здорово!', 'used to show you like an idea', 'Sounds great — let us do it!', 'Ajap eşidilýär — edeli!', 'A2'),
    ('Never mind.', '/ˈnevə maɪnd/', 'PHR', 'Zyýany ýok.', 'Неважно.', 'used to say something is not important', 'Never mind, it was only a cup.', 'Zyýany ýok, diňe käse boldy.', 'A2'),
    ('Oh no', '/əʊ nəʊ/', 'INTJ', 'Eýwaý!', 'О нет!', 'used to show you are unhappy about news', 'Oh no! I forgot the tickets!', 'Eýwaý! Bileti ýatdan çykarypdym!', 'A1'),
    ('That\'s interesting.', '/ðæts ˈɪntrəstɪŋ/', 'PHR', 'Gyzykly.', 'Интересно.', 'used to show you want to hear more', "That's interesting — tell me more.", 'Gyzykly — köpräk gürrüň ber.', 'A1'),
]

T['pe_opinions'] = [
    ('in my opinion', '/ɪn maɪ əˈpɪnjən/', 'PHR', 'meniň pikirimçe', 'по-моему', 'used to say what you think', 'In my opinion, the film was slow.', 'Meniň pikirimçe, film haýal boldy.', 'A2', 'in my opinion'),
    ('to be honest', '/tuː bi ˈɒnɪst/', 'PHR', 'dogrusy', 'честно говоря', 'used before a true but awkward opinion', 'To be honest, I did not like it.', 'Dogrusy, halamadym.', 'A2', 'to be honest'),
    ('personally', '/ˈpɜːsənəli/', 'ADV', 'şahsan', 'лично', 'used to give your own view', 'Personally, I prefer the first one.', 'Şahsan, birinjini gowy görýärin.', 'A2'),
    ('I suppose', '/aɪ səˈpəʊz/', 'PHR', 'çak edýärin', 'полагаю', 'used to agree hesitantly', 'I suppose you are right.', 'Dogrydyr diýip çak edýärin.', 'A2'),
    ('as far as I\'m concerned', '/əz fɑːr əz aɪm kənˈsɜːnd/', 'PHR', 'meniň üçin', 'что касается меня', 'used to stress your own view', "As far as I'm concerned, it works fine.", 'Meniň üçin gowy işleýär.', 'B1'),
    ('the thing is', '/ðə θɪŋ ɪz/', 'PHR', 'mesele şonda', 'дело в том', 'used to introduce the real problem', 'The thing is, we have no time.', 'Mesele şonda, wagtymyz ýok.', 'A2'),
    ('it depends', '/ɪt dɪˈpendz/', 'PHR', 'bagly', 'зависит', 'used when the answer can change', 'It depends on the weather.', 'Howa bagly.', 'A2', 'it depends on'),
    ('if you ask me', '/ɪf ju ɑːsk miː/', 'PHR', 'sorasaň', 'если честно (по-моему)', 'used before a strong opinion', 'If you ask me, he was wrong.', 'Sorasaň, ol nädogry boldy.', 'A2'),
]

T['pe_permission'] = [
    ('Can I ...?', '/kæn aɪ/', 'PHR', 'Bolýarmy ...?', 'Можно ...?', 'used to ask permission', 'Can I use your phone?', 'Telefonyňy ulanyp bolýarmy?', 'A1'),
    ('Could you ...?', '/kʊd juː/', 'PHR', '... edip bilersiňizmi?', 'Не могли бы вы ...?', 'used to ask someone politely to do something', 'Could you open the window?', 'Penjiräni açyp bilersiňizmi?', 'A1'),
    ('Do you mind ...?', '/du ju maɪnd/', 'PHR', 'Garşy dälmi ...?', 'Вы не против ...?', 'used to ask politely', 'Do you mind if I sit here?', 'Şu ýerde otursam garşy dälmi?', 'A2', 'do you mind if'),
    ('Is it OK if ...?', '/ɪz ɪt ˌəʊ ˈkeɪ ɪf/', 'PHR', '... bolýarmy?', 'Можно ли ...?', 'used to check permission', 'Is it OK if I leave early?', 'Ir gitsem bolýarmy?', 'A2'),
    ('Would you mind ...?', '/wʊd ju maɪnd/', 'PHR', 'Siz garşy bolmazmyňyz ...?', 'Вы бы не возражали ...?', 'a very polite request', 'Would you mind helping me?', 'Kömek etmäge garşy bolmazmyňyz?', 'A2', 'would you mind doing'),
    ('Would it be possible ...?', '/wʊd ɪt bi ˈpɒsəbl/', 'PHR', 'Mümkinmi ...?', 'Возможно ли ...?', 'a formal way to ask', 'Would it be possible to change seats?', 'Oturgyçlary çalyşmak mümkinmi?', 'B1'),
    ('Of course.', '/əv kɔːs/', 'PHR', 'Elbetde.', 'Конечно.', 'used to agree happily', 'Of course you can borrow it.', 'Elbetde, karzyna alyp bilersiň.', 'A2'),
    ('I\'m afraid not.', '/aɪm əˈfreɪd nɒt/', 'PHR', 'Gynansak-da, ýok.', 'Боюсь, что нет.', 'a polite way to say no', "I'm afraid not, it is taken.", 'Gynansak-da ýok, eýelendi.', 'A2'),
]

T['pe_suggestions'] = [
    ('Why don\'t we ...?', '/waɪ dəʊnt wiː/', 'PHR', '... etsek nähili?', 'Почему бы нам не ...?', 'used to suggest something', "Why don't we take a taxi?", 'Taksi münsek nähili?', 'A2'),
    ('How about ...?', '/haʊ əˈbaʊt/', 'PHR', '... nähili?', 'Как насчёт ...?', 'used to suggest something', 'How about a film tonight?', 'Şu gije film nähili?', 'A2', 'how about going'),
    ('Let\'s ...', '/lets/', 'PHR', 'Geliň ...', 'Давай(те) ...', 'used to suggest doing something together', "Let's start with the easy questions.", 'Geliň, aňsat soraglardan başlalyň.', 'A1'),
    ('Shall we ...?', '/ʃæl wiː/', 'PHR', '... etmelimi?', 'Не ... ли нам?', 'used to suggest politely', 'Shall we book a table?', 'Stol bron etmelimi?', 'A2'),
    ('We could always ...', '/wi kʊd ˈɔːlweɪz/', 'PHR', 'Hemişe ... edip bilerdik', 'Мы всегда можем ...', 'used to offer another option', 'We could always order in.', 'Hemişe sargyt edip bilerdik.', 'A2'),
    ('That\'s a good idea.', '/ðæts ə ɡʊd aɪˈdɪə/', 'PHR', 'Gowy pikir.', 'Хорошая идея.', 'used to accept a suggestion', "That's a good idea — let us try.", 'Gowy pikir — synanyşyp göreliň.', 'A1'),
    ('I\'m not sure.', '/aɪm nɒt ʃʊə(r)/', 'PHR', 'Ynanamok.', 'Не уверен.', 'used to refuse softly', "I'm not sure about tonight.", 'Şu gije barada ynanamok.', 'A1'),
    ('Sounds like a plan', '/saʊndz laɪk ə plæn/', 'PHR', 'Meýilnama ýaly eşidilýär.', 'Звучит как план.', 'used to accept a plan happily', 'Sounds like a plan — see you at six.', 'Meýilnama ýaly — altyda görüşeris.', 'A2'),
]

T['pe_indirect'] = [
    ('Could you tell me ...?', '/kʊd ju tel miː/', 'PHR', 'Aýdyp bilersiňizmi ...?', 'Не могли бы вы сказать ...?', 'a polite way to ask for information', 'Could you tell me the time?', 'Wagty aýdyp bilersiňizmi?', 'A2'),
    ('Do you know if ...?', '/du ju nəʊ ɪf/', 'PHR', '... bilýärsiňizmi?', 'Вы не знаете, ... ли?', 'used to ask indirectly', 'Do you know if the bank is open?', 'Bankyň açykdygyny bilýärsiňizmi?', 'A2'),
    ('I was wondering ...', '/aɪ wɒz ˈwʌndərɪŋ/', 'PHR', 'Pikirlenýärdim ...', 'Я wondered ...', 'a very polite question start', 'I was wondering if you could help.', 'Kömek edip bilersiňizmi diýip pikirlenýärdim.', 'B1'),
    ('Do you have any idea ...?', '/du ju hæv ˈeni aɪˈdɪə/', 'PHR', 'Hiç pikiriňiz barmy ...?', 'Вы не имеете понятия ...?', 'used to ask for information', 'Do you have any idea where it is?', 'Nirededigini hiç bilýärsiňizmi?', 'A2'),
    ('Can you remember ...?', '/kæn ju rɪˈmembə(r)/', 'PHR', 'Ýadyňyzdami ...?', 'Вы помните ...?', 'used to ask about the past', 'Can you remember his name?', 'Adyny ýadyňyzdamy?', 'A1'),
    ('I\'m not sure whether ...', '/aɪm nɒt ʃʊə(r) ˈweðə(r)/', 'PHR', 'Ynanamok ...', 'Не уверен, ... ли', 'used to express doubt', "I'm not sure whether he is coming.", 'Gelýändigine ynanamok.', 'A2'),
    ('Would you know ...?', '/wʊd ju nəʊ/', 'PHR', 'Bilýän bolsaňyz ...', 'Не подскажете ...?', 'used to ask a stranger politely', 'Would you know the way to the station?', 'Wokzala ýoly bilýän bolsaňyz?', 'A2'),
    ('Could you explain ...?', '/kʊd ju ɪkˈspleɪn/', 'PHR', 'Düşündirip bilersiňizmi ...?', 'Не объясните ли ...?', 'used to ask for a clear answer', 'Could you explain the rule again?', 'Düzgüni ýene düşündirip bilersiňizmi?', 'A2'),
]
LESSONS = {
    '1A': (1,  'Eating in...and out', 'food and cooking', ['food_cooking']),
    '1B': (1,  'Modern families', 'family · personality adjectives', ['family_personality']),
    '2A': (2,  'Spending money', 'money', ['money']),
    '2B': (2,  'Changing lives', 'strong adjectives', ['strong_adjs']),
    '3A': (3,  'Survive the drive', 'transport', ['transport']),
    '3B': (3,  'Men, women, and children', 'collocation: verbs + adjectives + prepositions', ['dep_preps']),
    '4A': (4,  'Bad manners?', 'phone language', ['phone_language']),
    '4B': (4,  'Yes, I can!', '-ed / -ing adjectives', ['ed_ing2']),
    '5A': (5,  'Sporting superstitions', 'sport', ['sport']),
    '5B': (5,  '#thewaywemet', 'relationships', ['relationships']),
    '6A': (6,  'Behind the scenes', 'cinema', ['cinema']),
    '6B': (6,  'Every picture tells a story', 'the body', ['body']),
    '7A': (7,  'Live and learn', 'education', ['education']),
    '7B': (7,  'The hotel of Mum and Dad', 'houses', ['houses']),
    '8A': (8,  'The right job for you', 'work', ['work']),
    '8B': (8,  'Have a nice day!', 'shopping · nouns from verbs', ['shopping2']),
    '9A': (9,  'Lucky encounters', 'making adjectives and adverbs', ['adj_adv_formation']),
    '9B': (9,  'Digital detox', 'electronic devices', ['devices']),
    '10A': (10, 'Idols and icons', 'compound nouns', ['compound_nouns']),
    '10B': (10, 'And the murderer is...', 'crime', ['crime']),
}

WORD_LESSON = {}


def lesson_for(topic, en, fallback):
    key = en.strip().lower()
    return WORD_LESSON.get(key, fallback)


# Intermediate has ten units; the five Practical English episodes sit after
# units 1, 3, 5, 7 and 9 in the book. In the data they carry unit 11 so they
# do not collide with the real units, and the app shows each episode right
# after the unit it follows.
PE_UNIT = 11
for code, n, title, topic, key in (
    ('PE1', 11, 'Meeting the parents', 'reacting to what people say', 'pe_react'),
    ('PE2', 11, 'A difficult celebrity', 'giving opinions', 'pe_opinions'),
    ('PE3', 11, 'Ola friends', 'permission and requests', 'pe_permission'),
    ('PE4', 11, "Boys' night out", 'making suggestions', 'pe_suggestions'),
    ('PE5', 11, 'Unexpected events', 'indirect questions', 'pe_indirect'),
):
    LESSONS[code] = (PE_UNIT, title, topic, [key])


def lesson_sort_key(code):
    m = re.match(r'^(\d+)(.*)$', code)
    if m:
        return (int(m.group(1)), m.group(2))
    return (11, code)


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
                    'books': [{'book': 'int', 'unit': unit, 'lesson': lesson, 'page': PAGE.get(lesson)}],
                    'proofread': False,
                })

    if dups:
        raise SystemExit('duplicate headwords:\n  ' + '\n  '.join(dups))

    used = set(t for ts in LESSONS.values() for t in ts[3])
    unused = sorted(set(T) - used)
    if unused:
        raise SystemExit('topics declared but never used by a lesson: ' + ', '.join(unused))

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
        'book': 'int',
        'title': 'English File Intermediate (4th edition) — vocabulary, by lesson',
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
