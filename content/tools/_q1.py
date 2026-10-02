#!/usr/bin/env python3
"""English File Advanced Plus (4th edition) — vocabulary organised by the book.

Same method as gen_adv.py / gen_intp.py. The OCR dump (uploads/Avanced plus.txt,
9,957 lines) kept the contents table and the Vocabulary Bank references legible.
tm / ru / def / ex are my own work and proofread:false; the IPA is written
properly, not copied from the OCR.

STRUCTURE (contents table, dump lines 2-56). Advanced Plus 4th edition has EIGHT
units, each with TWO lessons (A and B — no C) and NO Colloquial English /
Practical English episodes (grep for "Colloquial English" returns nothing; there
are exactly eight "Revise and Check" sections). So this pack has 16 lessons and
no episode data-units. Each lesson has a vocabulary focus; twelve come from the
Vocabulary Bank (pp.140-158) and four from in-lesson VOCABULARY boxes:
  1A vague language            · 1B phrasal nouns
  2A prefixes and suffixes     · 2B ways of moving
  3A research language         · 3B idioms from Shakespeare
  4A binomials                 · 4B acronyms and initialisms
  5A more sophisticated emotions · 5B individuals and populations
  6A adverb collocations + verbs for making things · 6B numbers and measurements
  7A punishment                · 7B connotation
  8A eating and drinking       · 8B ways of seeing

Usage: python3 content/tools/gen_advp.py
"""
import json
import os
import re
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'advancedplus.json')

# topic -> [ (en, ipa, pos, tm, ru, def, ex, exTm, cefr[, coll]) ]
T = {}

# ---- Vocabulary Bank — Vague language -> 1A ----
T['vague_language'] = [
    ('and so on', '/ænd səʊ ˈɒn/', 'PHR', 'we şuňa meňzeşler', 'и тому подобное', 'used after a list to mean there are more examples', 'We bought bread, cheese, fruit and so on.', 'Biz çörek, peýnir, miwe we şuňa meňzeşleri satyn aldyk.', 'C1'),
    ('or something', '/ɔː ˈsʌmθɪŋ/', 'PHR', 'ýa-da meňzeş zat', 'или что-то вроде', 'used when you are not sure of the exact thing', 'He is a lawyer or something.', 'Ol aklawçy ýa-da meňzeş zat.', 'C1'),
    ('kind of', '/kaɪnd əv/', 'ADV', 'birhili (takmynan)', 'вроде, как бы', 'used to make a statement less exact or direct', 'It was kind of strange.', 'Ol birhili geňdi.', 'C1'),
    ('sort of', '/sɔːt əv/', 'ADV', 'birhili (takmynan)', 'вроде, типа', 'used to make a statement less exact or direct', 'I sort of agree with you.', 'Men saňa birhili goşulýaryn.', 'C1'),
    ('I suppose', '/aɪ səˈpəʊz/', 'PHR', 'meniň pikirimçe', 'я полагаю', 'used to agree in a way that is not enthusiastic', 'I suppose you are right.', 'Meniň pikirimçe, sen mamla.', 'C1'),
    ('more or less', '/mɔː ɔː les/', 'PHR', 'takmynan (üç aşak bäş ýokary)', 'более или менее', 'almost, but not exactly', 'The work is more or less finished.', 'Iş takmynan gutardy.', 'C1'),
    ('to some extent', '/tə sʌm ɪkˈstent/', 'PHR', 'belli bir derejede', 'в некоторой степени', 'partly, but not completely', 'You are right to some extent.', 'Sen belli bir derejede mamla.', 'C1'),
    ('roughly', '/ˈrʌfli/', 'ADV', 'takmynan', 'примерно', 'approximately, not exactly', 'It costs roughly ten manat.', 'Ol takmynan on manat durýar.', 'C1'),
    ('approximately', '/əˈprɒksɪmətli/', 'ADV', 'takmynan (anyk däl)', 'приблизительно', 'close to a number but not exact', 'Approximately fifty people came.', 'Takmynan elli adam geldi.', 'C1'),
    ('whatnot', '/ˈwɒtnɒt/', 'N', 'we şuňa meňzeş zatlar', 'и прочее', 'used after a list to mean other similar things', 'The box held pens, paper, whatnot.', 'Gutuda galam, kagyz we şuňa meňzeş zatlar bardy.', 'C1'),
    ('or so', '/ɔː səʊ/', 'PHR', 'töweregi (takmynan)', 'или около того', 'used after a number to mean approximately', 'There were thirty or so guests.', 'Otuza töweregi myhman bardy.', 'B2'),
    ('stuff', '/stʌf/', 'N', 'zatlar (umumy at)', 'всякие вещи', 'things in general, without naming them', 'Put your stuff on the table.', 'Zatlaryňy stoluň üstüne goý.', 'B1'),
]

# ---- Vocabulary Bank — Phrasal nouns -> 1B ----
T['phrasal_nouns'] = [
    ('upbringing', '/ˈʌpbrɪŋɪŋ/', 'N', 'terbiýe (ösüş)', 'воспитание', 'the way a child is raised and taught behaviour', 'He had a strict upbringing.', 'Onuň berk terbiýesi bardy.', 'C1'),
    ('income', '/ˈɪnkʌm/', 'N', 'giriş (girdeji)', 'доход', 'money received from work or investments', 'Her income rose last year.', 'Onuň girdejisi geçen ýyl artdy.', 'B2'),
    ('outcome', '/ˈaʊtkʌm/', 'N', 'netije', 'результат, исход', 'the result of an event or process', 'Nobody knows the outcome yet.', 'Netijäni heniz hiç kim bilenok.', 'C1'),
    ('downpour', '/ˈdaʊnpɔː/', 'N', 'guýma ýagyş', 'ливень', 'a lot of rain falling in a short time', 'We got caught in a downpour.', 'Biz guýma ýagyşa düşdük.', 'C1'),
    ('aftertaste', '/ˈɑːftəteɪst/', 'N', 'tagam yzy (agyzda galan)', 'послевкусие', 'a taste that stays in your mouth afterwards', 'The medicine left a bitter aftertaste.', 'Derman ajy tagam yzyny galdyrdy.', 'C2'),
    ('outcry', '/ˈaʊtkraɪ/', 'N', 'garym-gatym protest', 'возмущение, протест', 'a strong public expression of anger', 'The tax caused a public outcry.', 'Salgyt jemgyýetçilik protestine sebäp boldy.', 'C2'),
    ('downfall', '/ˈdaʊnfɔːl/', 'N', 'ýykylyş (derejeden gaçma)', 'падение, крах', 'the loss of power or success of a person', 'Greed was his downfall.', 'Açgözlük onuň ýykylyşy boldy.', 'C2'),
    ('backlash', '/ˈbæklæʃ/', 'N', 'güýçli garşylyk', 'резкая негативная реакция', 'a strong negative reaction by many people', 'The decision provoked a backlash.', 'Bu karar güýçli garşylyk döretdi.', 'C2'),
    ('aftermath', '/ˈɑːftəmæθ/', 'N', 'soňy (waka soňy)', 'последствия', 'the period and effects following a bad event', 'They rebuilt the town in the aftermath.', 'Olar şäheri wakanyň soňunda täzeden gurdular.', 'C1'),
    ('outlay', '/ˈaʊtleɪ/', 'N', 'çykdajy (ilkinji)', 'затраты, расходы', 'an amount of money spent on something', 'The initial outlay was high.', 'Ilkinji çykdajy ýokary boldy.', 'C2'),
    ('intake', '/ˈɪnteɪk/', 'N', 'kabul (içine alyş)', 'потребление, приём', 'the amount taken in over a period', 'Cut down your daily sugar intake.', 'Gündelik şeker kabulyňyzy azaldyň.', 'C1'),
    ('outburst', '/ˈaʊtbɜːst/', 'N', 'duýgy partlamasy', 'вспышка, взрыв эмоций', 'a sudden strong expression of emotion', 'She regretted her angry outburst.', 'Ol gaharly partlamasyna ökünýärdi.', 'C2'),
]

# ---- Vocabulary Bank — Prefixes and suffixes -> 2A ----
T['affixes'] = [
    ('amoral', '/ˌeɪˈmɒrəl/', 'ADJ', 'ahlaksyz (ýörelgesiz)', 'аморальный', 'not having any sense of right and wrong', 'He took an amoral view of business.', 'Ol işewürlige ahlaksyz garaýardy.', 'C2'),
    ('antenatal', '/ˌæntiˈneɪtl/', 'ADJ', 'dogluşdan öňki', 'дородовой', 'relating to the time before a baby is born', 'She goes to antenatal classes.', 'Ol dogluşdan öňki sapaklara gatnaşýar.', 'C2'),
    ('circumnavigate', '/ˌsɜːkəmˈnævɪɡeɪt/', 'V', 'töweregini aýlanyp geçmek', 'совершить кругосветное плавание', 'to sail all the way around something', 'They circumnavigated the globe.', 'Olar Ýer şarynyň daşyny aýlanyp geçdiler.', 'C2'),
    ('counterproductive', '/ˌkaʊntəprəˈdʌktɪv/', 'ADJ', 'netijesiz (garşy täsirli)', 'контрпродуктивный', 'having the opposite of the effect you want', 'The new rule proved counterproductive.', 'Täze düzgün netijesiz boldy.', 'C2'),
    ('misjudge', '/ˌmɪsˈdʒʌdʒ/', 'V', 'ýalňyş baha bermek', 'неправильно оценить', 'to form a wrong opinion of someone or something', 'I misjudged how long it would take.', 'Men onuň näçe wagt aljakdygyny ýalňyş çakladym.', 'C2'),
    ('overestimate', '/ˌəʊvərˈestɪmeɪt/', 'V', 'artyk baha bermek', 'переоценить', 'to think something is bigger or better than it is', 'We overestimated the cost.', 'Biz bahany artyk çakladyk.', 'C1'),
    ('underestimate', '/ˌʌndərˈestɪmeɪt/', 'V', 'pes baha bermek', 'недооценить', 'to think something is smaller or worse than it is', 'Do not underestimate her ability.', 'Onuň ukybyny pes baha bermäň.', 'B2'),
    ('substandard', '/ˌsʌbˈstændəd/', 'ADJ', 'standartdan pes', 'некачественный', 'worse than the normal or accepted level', 'They used substandard materials.', 'Olar standartdan pes material ulandylar.', 'C2'),
    ('supernatural', '/ˌsuːpəˈnætʃrəl/', 'ADJ', 'tebigatyň daşyndaky', 'сверхъестественный', 'relating to forces beyond the laws of nature', 'She believes in supernatural powers.', 'Ol tebigatyň daşyndaky güýçlere ynanýar.', 'C1'),
    ('transformation', '/ˌtrænsfəˈmeɪʃn/', 'N', 'özgerdiliş', 'преобразование', 'a complete change in form or appearance', 'The city underwent a transformation.', 'Şäher özgerdilişe sezewar boldy.', 'B2'),
    ('accuracy', '/ˈækjərəsi/', 'N', 'takyklyk', 'точность', 'the quality of being correct and exact', 'Check the accuracy of the figures.', 'Sanlaryň takyklygyny barlaň.', 'B2'),
    ('resilience', '/rɪˈzɪliəns/', 'N', 'çydamlylyk (gaýtadan dikeliş)', 'устойчивость, жизнестойкость', 'the ability to recover quickly after problems', 'Her resilience impressed everyone.', 'Onuň çydamlylygy hemmäni haýran galdyrdy.', 'C1'),
]

# ---- Vocabulary Bank — Ways of moving -> 2B ----
T['moving'] = [
    ('stride', '/straɪd/', 'V', 'ädim ätmek (ynamly)', 'шагать', 'to walk with long confident steps', 'She strode into the room.', 'Ol otaga ynamly ädim ädip girdi.', 'C1'),
    ('stroll', '/strəʊl/', 'V', 'haýal gezelenç etmek', 'прогуливаться', 'to walk slowly in a relaxed way', 'They strolled along the beach.', 'Olar kenarda haýal gezelenç etdiler.', 'C1'),
    ('trudge', '/trʌdʒ/', 'V', 'agyr ädimlemek (ýadaw)', 'плестись', 'to walk slowly with heavy steps, tiredly', 'We trudged home in the snow.', 'Biz garda ýadaw ädimläp öýe gaýtdyk.', 'C2'),
    ('wander', '/ˈwɒndə/', 'V', 'aýlanyp ýörmek (maksatsyz)', 'бродить', 'to walk around slowly with no clear direction', 'We wandered through the old town.', 'Biz köne şäherde aýlanyp ýördük.', 'B2'),
    ('march', '/mɑːtʃ/', 'V', 'ädim urup ýörmek', 'маршировать', 'to walk with firm regular steps like soldiers', 'The crowd marched to the square.', 'Mähelle meýdana ädim urup ýöräp gitdi.', 'B2'),
    ('crawl', '/krɔːl/', 'V', 'ýmbyr-ýumbyr süýşmek', 'ползти', 'to move along on your hands and knees', 'The baby crawled across the floor.', 'Bäbek poluň üstünden süýşdi.', 'B2'),
    ('stagger', '/ˈstæɡə/', 'V', 'titräp ýörmek (ykjyramak)', 'шататься', 'to walk unsteadily, almost falling', 'He staggered out of the bar.', 'Ol bardan titräp çykdy.', 'C2'),
    ('stumble', '/ˈstʌmbl/', 'V', 'büzülip gitmek (aýagy büdräp)', 'спотыкаться', 'to hit your foot and almost fall while walking', 'She stumbled over a stone.', 'Ol daşa büzlip gitdi.', 'C1'),
    ('tiptoe', '/ˈtɪptəʊ/', 'V', 'barmak ujunda ýörmek', 'красться на цыпочках', 'to walk quietly on the tips of your toes', 'He tiptoed past the bedroom.', 'Ol ýatylýan otagyň deňinden barmak ujunda geçdi.', 'C2'),
    ('sprint', '/sprɪnt/', 'V', 'tiz ylgamak (gysga aralyk)', 'мчаться, бежать спринт', 'to run at full speed for a short distance', 'She sprinted to catch the bus.', 'Ol awtobusa ýetişmek üçin tiz ylgady.', 'C1'),
    ('shuffle', '/ˈʃʌfl/', 'V', 'aýak süýşürip ýörmek', 'шаркать', 'to walk without lifting your feet properly', 'The old man shuffled to the door.', 'Garry adam aýak süýşürip gapa bardy.', 'C2'),
    ('trek', '/trek/', 'V', 'uzyn we kyn ýol ýöremek', 'совершать долгий переход', 'to make a long hard journey on foot', 'We trekked through the mountains.', 'Biz daglaryň içinden uzyn ýol ýördük.', 'C1'),
]

# ---- in-lesson 3A — research language ----
T['research'] = [
    ('questionnaire', '/ˌkwestʃəˈneə/', 'N', 'soragnama', 'анкета', 'a set of written questions to collect information', 'We sent out a questionnaire.', 'Biz soragnama iberdik.', 'C1'),
    ('survey', '/ˈsɜːveɪ/', 'N', 'sorag-jogap barlagy', 'опрос', 'a study that asks people questions to find opinions', 'A recent survey shows the trend.', 'Soňky sorag-jogap bu tendensiýany görkezýär.', 'B2'),
    ('sample', '/ˈsɑːmpl/', 'N', 'nusga (barlag topary)', 'выборка', 'a small group used to represent a larger one', 'The sample included two hundred students.', 'Nusga iki ýüz studenti öz içine aldy.', 'B2'),
    ('respondent', '/rɪˈspɒndənt/', 'N', 'jogap beriji', 'респондент', 'a person who answers questions in a survey', 'Half the respondents agreed.', 'Jogap berijileriň ýarysy razy boldy.', 'C1'),
    ('data', '/ˈdeɪtə/', 'N', 'maglumatlar (sanlar)', 'данные', 'facts or numbers collected for study', 'The data supports our theory.', 'Maglumatlar biziň nazaryýetimizi tassyklaýar.', 'B2'),
    ('findings', '/ˈfaɪndɪŋz/', 'N', 'tapyndylar (barlag netijeleri)', 'результаты исследования', 'the results of a study or investigation', 'The findings were published last week.', 'Tapyndylar geçen hepde çap edildi.', 'C1'),
    ('statistics', '/stəˈtɪstɪks/', 'N', 'statistika', 'статистика', 'numbers that summarise a large set of facts', 'The statistics show a rise.', 'Statistika ösüşi görkezýär.', 'B2'),
    ('hypothesis', '/haɪˈpɒθəsɪs/', 'N', 'çaklama (ylymy)', 'гипотеза', 'an idea that is tested by research', 'Our hypothesis was confirmed.', 'Biziň çaklamamyz tassyklandy.', 'C1'),
    ('variable', '/ˈveəriəbl/', 'N', 'üýtgeýän ululyk', 'переменная', 'a factor that can change and affect a result', 'Age is an important variable.', 'Ýaş möhüm üýtgeýän ululykdyr.', 'C1'),
    ('correlation', '/ˌkɒrəˈleɪʃn/', 'N', 'özara baglanyşyk', 'корреляция', 'a connection between two things that change together', 'There is a strong correlation here.', 'Bu ýerde güýçli özara baglanyşyk bar.', 'C2'),
    ('methodology', '/ˌmeθəˈdɒlədʒi/', 'N', 'metodologiýa (usul ulgamy)', 'методология', 'the set of methods used in a study', 'The methodology is explained below.', 'Metodologiýa aşakda düşündirilýär.', 'C1'),
    ('analysis', '/əˈnæləsɪs/', 'N', 'seljerme', 'анализ', 'a detailed examination of something', 'The analysis took three months.', 'Seljerme üç aý aldy.', 'B2'),
]

# ---- Vocabulary Bank — Idioms from Shakespeare -> 3B ----
T['shakespeare'] = [
    ('a wild-goose chase', '/ə waɪld ɡuːs tʃeɪs/', 'PHR', 'biyparajy gözleg (boş iş)', 'бесполезная погоня', 'a hopeless search for something you cannot find', 'Looking for him was a wild-goose chase.', 'Ony gözlemek boşa iş boldy.', 'C2'),
    ('break the ice', '/breɪk ði aɪs/', 'PHR', 'buzuny döwmek (gepleşigi başlamak)', 'разрядить обстановку', 'to make people relax at the start of a meeting', 'A joke helped break the ice.', 'Degişme buzuny döwmäge kömek etdi.', 'C1'),
    ('in a pickle', '/ɪn ə ˈpɪkl/', 'PHR', 'kyn ýagdaýda', 'в затруднительном положении', 'in a difficult or troubling situation', 'I am in a bit of a pickle.', 'Men birhili kyn ýagdaýda.', 'C2'),
    ('a heart of gold', '/ə hɑːt əv ɡəʊld/', 'PHR', 'altyn ýürekli', 'золотое сердце', 'very kind and generous', 'She has a heart of gold.', 'Onuň altyn ýüregi bar.', 'C1'),
    ('seen better days', '/siːn ˈbetə deɪz/', 'PHR', 'öňki günleri gowy bolan (könelen)', 'видал лучшие времена', 'old and in worse condition than before', 'This coat has seen better days.', 'Bu palto öňki günlerini gördi.', 'C2'),
    ('fair play', '/feə pleɪ/', 'PHR', 'adalatly oýun', 'честная игра', 'honest and equal behaviour in a competition', 'We believe in fair play.', 'Biz adalatly oýna ynanýarys.', 'C1'),
    ('love is blind', '/lʌv ɪz blaɪnd/', 'PHR', 'söýgi kordur', 'любовь слепа', 'you cannot see the faults of someone you love', 'They say love is blind.', 'Söýgi kordur diýýärler.', 'C1'),
    ('too much of a good thing', '/tuː mʌtʃ əv ə ɡʊd θɪŋ/', 'PHR', 'gowy zadyň hem köpi artyk', 'всё хорошо в меру', 'even something good is bad in large amounts', 'Three cakes is too much of a good thing.', 'Üç tort gowy zadyň hem köpi artyk.', 'C2'),
    ('a brave new world', '/ə breɪv njuː wɜːld/', 'PHR', 'täze dünýä (üýtgeşik döwür)', 'дивный новый мир', 'a new situation that seems exciting but strange', 'Technology created a brave new world.', 'Tehnologiýa täze dünýäni döretdi.', 'C2'),
    ('wear your heart on your sleeve', '/weə jɔː hɑːt ɒn jɔː sliːv/', 'PHR', 'duýgularyňy gizlemän görkezmek', 'носить сердце нараспашку', 'to show your feelings openly', 'He always wears his heart on his sleeve.', 'Ol hemişe duýgularyny açyk görkezýär.', 'C2'),
    ('the green-eyed monster', '/ðə ɡriːn aɪd ˈmɒnstə/', 'PHR', 'göripçilik (ysmanak)', 'зеленоглазое чудовище (ревность)', 'a way of describing jealousy', 'Jealousy is the green-eyed monster.', 'Göripçilik ysmanakdyr.', 'C2'),
    ('in stitches', '/ɪn ˈstɪtʃɪz/', 'PHR', 'gaty gülýän (garym-gatym)', 'умирать со смеху', 'laughing very hard', 'His jokes had us in stitches.', 'Onuň degişmeleri bizi gaty güldürdi.', 'C2'),
]
