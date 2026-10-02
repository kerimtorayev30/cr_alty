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

# ---- Vocabulary Bank — Binomials -> 4A ----
T['binomials'] = [
    ('odds and ends', '/ɒdz ənd endz/', 'PHR', 'owny-uwak zatlar', 'мелочи, всякая всячина', 'small things of different kinds', 'The box was full of odds and ends.', 'Guty owny-uwak zatlar bilen doludy.', 'C2'),
    ('ups and downs', '/ʌps ənd daʊnz/', 'PHR', 'belent-pes günler', 'взлёты и падения', 'a mixture of good and bad experiences', 'Every marriage has its ups and downs.', 'Her bir durmuşyň belent-pes günleri bolýar.', 'C1'),
    ('bits and pieces', '/bɪts ənd ˈpiːsɪz/', 'PHR', 'owny-uwak bölekler', 'мелкие предметы', 'small separate items or tasks', 'I have a few bits and pieces to do.', 'Eden bir-iki owny işim bar.', 'C1'),
    ('pros and cons', '/prəʊz ənd kɒnz/', 'PHR', 'artykmaçlyklary we kemçilikleri', 'за и против', 'the advantages and disadvantages of something', 'We weighed up the pros and cons.', 'Biz artykmaçlyklaryny we kemçiliklerini deňeşdirdik.', 'C1'),
    ('by and large', '/baɪ ənd lɑːdʒ/', 'PHR', 'umuman alanyňda', 'в целом', 'in general, when everything is considered', 'By and large, the plan worked.', 'Umuman alanyňda, meýilnama işledi.', 'C2'),
    ('hit and miss', '/hɪt ənd mɪs/', 'PHR', 'şowsuz ýa-da üstünlikli (tötänleýin)', 'то густо, то пусто', 'sometimes good and sometimes bad, unpredictable', 'The service here is hit and miss.', 'Bu ýerdäki hyzmat tötänleýin.', 'C2'),
    ('touch and go', '/tʌtʃ ənd ɡəʊ/', 'PHR', 'howply ýagdaý (iki aralykda)', 'на волоске', 'uncertain, could succeed or fail at any moment', 'His recovery was touch and go.', 'Onuň sagalmagy howply ýagdaýdady.', 'C2'),
    ('now and then', '/naʊ ənd ðen/', 'PHR', 'ara-syrada', 'время от времени', 'sometimes, but not often', 'We meet now and then.', 'Biz ara-syrada duşuşýarys.', 'B2'),
    ('back and forth', '/bæk ənd fɔːθ/', 'PHR', 'ylla-yzlary (gidip-gelip)', 'взад и вперёд', 'moving first one way and then the other', 'They argued back and forth.', 'Olar ylla-yzlary jedelleşdiler.', 'C1'),
    ('give and take', '/ɡɪv ənd teɪk/', 'PHR', 'özara ýüzleşme (ylalaşyk)', 'взаимные уступки', 'willingness to compromise with others', 'Marriage needs give and take.', 'Durmuş özara ýüzleşmäni talap edýär.', 'C2'),
    ('wear and tear', '/weə ənd teə/', 'PHR', 'könelme (ulanyş zerarly)', 'износ', 'damage that happens through normal use', 'The warranty covers wear and tear.', 'Kepillik könelmäni öz içine alýar.', 'C2'),
    ('safe and sound', '/seɪf ənd saʊnd/', 'PHR', 'aman-esen (zyýansyz)', 'цел и невредим', 'back without any harm or injury', 'The children came home safe and sound.', 'Çagalar öýe aman-esen geldiler.', 'C1'),
]

# ---- Vocabulary Bank — Acronyms and initialisms -> 4B ----
T['acronyms'] = [
    ('CEO', '/ˌsiː iː ˈəʊ/', 'N', 'baş direktor (edara ýolbaşçysy)', 'генеральный директор', 'the person in charge of a company, chief executive officer', 'The CEO announced the deal.', 'Baş direktor şertnamany yglan etdi.', 'C1'),
    ('DIY', '/ˌdiː aɪ waɪ/', 'N', 'özüň et (öý işleri)', 'сделай сам', 'doing home repairs yourself, do it yourself', 'He is good at DIY.', 'Ol öý işlerini özi etmegi başarýar.', 'B2'),
    ('FAQ', '/ˌef eɪ ˈkjuː/', 'N', 'ýygy soralýan soraglar', 'часто задаваемые вопросы', 'a list of questions people often ask, and answers', 'Check the FAQ on our website.', 'Web sahypamyzdaky ýygy soralýan soraglara serediň.', 'B2'),
    ('ASAP', '/ˌeɪ es eɪ ˈpiː/', 'ADV', 'mümkin boldugyça tiz', 'как можно скорее', 'as soon as possible', 'Call me back ASAP.', 'Maňa mümkin boldugyça tiz jaň ediň.', 'C1'),
    ('ETA', '/ˌiː tiː ˈeɪ/', 'N', 'gelýän wagty (çaklama)', 'расчётное время прибытия', 'the time something is expected to arrive', 'The ETA is six o clock.', 'Gelýän wagty sagat alty.', 'C1'),
    ('RSVP', '/ˌɑːr es viː ˈpiː/', 'PHR', 'jogap bermegiňizi haýyş edýäris', 'просьба ответить', 'please reply, from French repondez s il vous plait', 'Please RSVP by Friday.', 'Anna gününe çenli jogap bermegiňizi haýyş edýäris.', 'C1'),
    ('VIP', '/ˌviː aɪ ˈpiː/', 'N', 'möhüm şahs', 'очень важная персона', 'a very important person', 'They got VIP treatment.', 'Olar möhüm şahs hökmünde garşylandy.', 'B2'),
    ('HQ', '/ˌeɪtʃ ˈkjuː/', 'N', 'baş edara', 'штаб-квартира', 'the main office of an organisation, headquarters', 'The HQ is in Ashgabat.', 'Baş edara Aşgabatda.', 'B2'),
    ('PR', '/ˌpiː ˈɑːr/', 'N', 'jemgyýetçilik bilen aragatnaşyk', 'связи с общественностью', 'the work of managing a public image, public relations', 'She works in PR.', 'Ol jemgyýetçilik aragatnaşygynda işleýär.', 'C1'),
    ('HR', '/ˌeɪtʃ ˈɑːr/', 'N', 'işgärler bölümi', 'отдел кадров', 'the department that manages staff, human resources', 'Contact HR about the job.', 'Iş barada işgärler bölümi bilen habarlaşyň.', 'B2'),
    ('GDP', '/ˌdʒiː diː ˈpiː/', 'N', 'jemi içerki önüm', 'валовой внутренний продукт', 'the total value of goods a country produces, gross domestic product', 'The GDP grew by three per cent.', 'Jemi içerki önüm üç göterim ösdi.', 'C1'),
    ('CV', '/ˌsiː ˈviː/', 'N', 'iş terjimehaly', 'резюме', 'a document listing your education and work, curriculum vitae', 'Send your CV by email.', 'Iş terjimehalyňyzy e-poçta bilen iberiň.', 'B2'),
]

# ---- Vocabulary Bank — More sophisticated emotions -> 5A ----
T['emotions'] = [
    ('thrilled', '/θrɪld/', 'ADJ', 'örän şat (buýsançly)', 'в восторге', 'extremely happy and excited about something', 'She was thrilled with the result.', 'Ol netijä örän şat boldy.', 'C1'),
    ('devastated', '/ˈdevəsteɪtɪd/', 'ADJ', 'örän gamgyn (ýüregi ezilen)', 'опустошённый, убитый горем', 'extremely upset and shocked', 'He was devastated by the news.', 'Ol bu habardan örän gamgyn boldy.', 'C1'),
    ('ecstatic', '/ɪkˈstætɪk/', 'ADJ', 'joşgunly begençli', 'в экстазе', 'feeling overwhelming happiness', 'The fans were ecstatic.', 'Janköýerler joşgunly begençlidiler.', 'C2'),
    ('gutted', '/ˈɡʌtɪd/', 'ADJ', 'örän lapykeç', 'глубоко разочарованный', 'extremely disappointed, informal', 'She was gutted to lose.', 'Ol utulyp örän lapykeç boldy.', 'C2'),
    ('over the moon', '/ˌəʊvə ðə muːn/', 'PHR', 'aýyň üstünde (örän şat)', 'на седьмом небе', 'extremely pleased about something', 'He was over the moon about the job.', 'Ol iş barada aýyň üstündedi.', 'C1'),
    ('apprehensive', '/ˌæprɪˈhensɪv/', 'ADJ', 'aladaly (howatyrly)', 'опасающийся', 'worried that something bad may happen', 'She felt apprehensive before the exam.', 'Ol synagdan öň howatyrlandy.', 'C2'),
    ('relieved', '/rɪˈliːvd/', 'ADJ', 'ýeňillik duýan (arkaýyn)', 'испытывающий облегчение', 'glad that something unpleasant has ended', 'I was relieved to hear the truth.', 'Men hakykaty eşidip ýeňillik duýdum.', 'B2'),
    ('resentful', '/rɪˈzentfl/', 'ADJ', 'kineli (gaharly)', 'возмущённый, обиженный', 'feeling bitter anger at unfair treatment', 'She was resentful of his success.', 'Ol onuň üstünligine kineli boldy.', 'C2'),
    ('content', '/kənˈtent/', 'ADJ', 'kanagatlanýan (hoşal)', 'довольный', 'happy and satisfied with what you have', 'He is content with his life.', 'Ol durmuşyndan kanagatlanýar.', 'C1'),
    ('elated', '/ɪˈleɪtɪd/', 'ADJ', 'örän begençli (joşan)', 'ликующий', 'extremely happy and proud', 'They were elated by the victory.', 'Olar ýeňişden örän begençlidiler.', 'C2'),
    ('despondent', '/dɪˈspɒndənt/', 'ADJ', 'umytsyz (ruhdan düşen)', 'унылый, подавленный', 'unhappy and without hope', 'She grew despondent after months.', 'Aýlardan soň ol umytsyz boldy.', 'C2'),
    ('anxious', '/ˈæŋkʃəs/', 'ADJ', 'aladaly (ynjalyksyz)', 'тревожный', 'worried and nervous about something', 'He was anxious about the interview.', 'Ol söhbetdeşlik barada aladalandy.', 'B2'),
]

# ---- in-lesson 5B — individuals and populations ----
T['populations'] = [
    ('immigrant', '/ˈɪmɪɡrənt/', 'N', 'gelen immigrant (gelip ýerleşen)', 'иммигрант', 'a person who comes to live in a new country', 'The city welcomed the immigrants.', 'Şäher immigrantlary garşylady.', 'B2'),
    ('emigrant', '/ˈemɪɡrənt/', 'N', 'giden immigrant (öz ýurdundan çykan)', 'эмигрант', 'a person who leaves their country to live abroad', 'Many emigrants sought work abroad.', 'Köp emigrantlar daşary ýurtda iş gözlediler.', 'C1'),
    ('migrant', '/ˈmaɪɡrənt/', 'N', 'göçüp ýören adam', 'мигрант', 'a person who moves to find work, often for a while', 'Migrant workers follow the harvest.', 'Göçüp ýören işçiler hasylyň yzyna düşýärler.', 'C1'),
    ('refugee', '/ˌrefjuˈdʒiː/', 'N', 'bosgun', 'беженец', 'a person forced to leave home by war or danger', 'The refugees crossed the border.', 'Bosgunlar serhetden geçdiler.', 'B2'),
    ('asylum seeker', '/əˈsaɪləm ˌsiːkə/', 'N', 'pena gözleýän', 'лицо, ищущее убежища', 'a person asking another country for protection', 'The asylum seeker waited for a decision.', 'Pena gözleýän karara garaşdy.', 'C1'),
    ('expatriate', '/eksˈpætriət/', 'N', 'daşary ýurtda ýaşaýan watandaş', 'экспатриант', 'a person living outside their native country', 'The expatriate works for an oil firm.', 'Ekspat nebit kompaniýasynda işleýär.', 'C2'),
    ('indigenous', '/ɪnˈdɪdʒənəs/', 'ADJ', 'ýerli (gadymy)', 'коренной', 'living in a place before others arrived', 'The indigenous people protect the forest.', 'Ýerli halk tokaýy goraýar.', 'C1'),
    ('ethnic minority', '/ˈeθnɪk maɪˈnɒrəti/', 'N', 'etniçeslik azlyk', 'этническое меньшинство', 'a group with a different culture within a country', 'The law protects every ethnic minority.', 'Kanun her etniçeslik azlygy goraýar.', 'C1'),
    ('diaspora', '/daɪˈæspərə/', 'N', 'dagynyk millet (ýaýran halk)', 'диаспора', 'people scattered away from their homeland', 'The diaspora keeps its traditions.', 'Diaspora öz däplerini saklaýar.', 'C2'),
    ('integration', '/ˌɪntɪˈɡreɪʃn/', 'N', 'jemi bolup goşulma (uýgunlaşma)', 'интеграция', 'the process of joining and fitting into a group', 'Integration takes time and effort.', 'Goşulma wagt we tagalla talap edýär.', 'C1'),
    ('nationality', '/ˌnæʃəˈnæləti/', 'N', 'milliýet (raýatlyk)', 'национальность, гражданство', 'the country a person officially belongs to', 'She has dual nationality.', 'Onuň goşa milliýeti bar.', 'B1'),
    ('population', '/ˌpɒpjuˈleɪʃn/', 'N', 'ilat', 'население', 'all the people living in a place', 'The population is growing fast.', 'Ilat çalt ösýär.', 'B1'),
]

# ---- Vocabulary Bank + in-lesson 6A — adverb collocations, verbs for making ----
T['adverbs_making'] = [
    ('deeply', '/ˈdiːpli/', 'ADV', 'çuňňur (güýçli)', 'глубоко', 'used to add strong feeling to a verb', 'I deeply regret the mistake.', 'Men ýalňyşlyga çuňňur ökünýärin.', 'B2'),
    ('highly', '/ˈhaɪli/', 'ADV', 'örän (ýokary derejede)', 'весьма, крайне', 'used to mean very, especially with praise', 'I highly recommend this book.', 'Men bu kitaby örän maslahat berýärin.', 'B2'),
    ('utterly', '/ˈʌtəli/', 'ADV', 'düýbünden (doly)', 'совершенно', 'completely, often with a negative idea', 'The idea was utterly ridiculous.', 'Bu pikiriň düýbünden many ýokdy.', 'C1'),
    ('virtually', '/ˈvɜːtʃuəli/', 'ADV', 'diýen ýaly (tas)', 'практически', 'almost completely, nearly', 'It is virtually impossible.', 'Bu diýen ýaly mümkin däl.', 'C1'),
    ('bitterly', '/ˈbɪtəli/', 'ADV', 'ajy (örän, gynançly)', 'горько', 'used to show strong sadness or anger', 'She was bitterly disappointed.', 'Ol ajy lapykeç boldy.', 'C1'),
    ('manufacture', '/ˌmænjuˈfæktʃə/', 'V', 'önümçilikde ýasamak', 'производить', 'to make goods in large numbers with machines', 'The factory manufactures parts.', 'Zawod bölekleri öndürýär.', 'B2'),
    ('assemble', '/əˈsembl/', 'V', 'ýygnamak (böleklerden)', 'собирать, монтировать', 'to fit parts together to make something', 'He assembled the shelf himself.', 'Ol tekjäni özi ýygnady.', 'C1'),
    ('forge', '/fɔːdʒ/', 'V', 'demir urup ýasamak', 'ковать', 'to shape metal by heating and hammering', 'They forged the iron gates.', 'Olar demir derwezeleri urup ýasadylar.', 'C2'),
    ('craft', '/krɑːft/', 'V', 'ussatlyk bilen ýasamak', 'изготавливать вручную', 'to make something carefully with skill', 'She crafted a wooden bowl.', 'Ol ussatlyk bilen agaç käse ýasady.', 'C1'),
    ('mould', '/məʊld/', 'V', 'galyba salyp şekil bermek', 'формовать, лепить', 'to shape soft material into a form', 'The potter moulded the clay.', 'Küýzegär palçyga şekil berdi.', 'C2'),
    ('construct', '/kənˈstrʌkt/', 'V', 'gurmak (binany)', 'строить, сооружать', 'to build something large such as a bridge', 'They constructed a new bridge.', 'Olar täze köpri gurdular.', 'B2'),
    ('innovative', '/ˈɪnəveɪtɪv/', 'ADJ', 'täzeçil (özgerdiji)', 'инновационный', 'using new ideas or methods', 'It is an innovative design.', 'Bu täzeçil dizaýn.', 'B2'),
]

# ---- Vocabulary Bank — Numbers and measurements -> 6B ----
T['numbers'] = [
    ('dozen', '/ˈdʌzn/', 'NUM', 'on iki (bir topar)', 'дюжина', 'a group of twelve things', 'She bought a dozen eggs.', 'Ol bir topar ýumurtga satyn aldy.', 'B2'),
    ('gross', '/ɡrəʊs/', 'NUM', 'ýüz kyrk dört', 'гросс (144 штуки)', 'a group of one hundred and forty-four', 'They ordered a gross of pens.', 'Olar ýüz kyrk dört sany galam sargyt etdiler.', 'C2'),
    ('per cent', '/pə ˈsent/', 'NUM', 'göterim', 'процент', 'one part in every hundred', 'Sales rose by ten per cent.', 'Satuw on göterim artdy.', 'B1'),
    ('ratio', '/ˈreɪʃiəʊ/', 'N', 'gatnaşyk (san deňeşdirme)', 'соотношение', 'the relationship between two amounts as numbers', 'The teacher-pupil ratio is low.', 'Mugallym-okuwçy gatnaşygy pes.', 'C1'),
    ('fraction', '/ˈfrækʃn/', 'N', 'bölek (kesir)', 'дробь', 'a part of a whole, shown as one number over another', 'Three quarters is a fraction.', 'Dörtden üç bölekdir.', 'C1'),
    ('decimal', '/ˈdesɪml/', 'N', 'onluk san (oturlyk)', 'десятичная дробь', 'a number written with a point, not a fraction', 'Write it as a decimal.', 'Ony onluk san görnüşinde ýazyň.', 'C1'),
    ('square metre', '/skweə ˈmiːtə/', 'N', 'kwadrat metr', 'квадратный метр', 'a unit for measuring area', 'The flat is fifty square metres.', 'Öý elli kwadrat metr.', 'B2'),
    ('hectare', '/ˈhekter/', 'N', 'gektar', 'гектар', 'a unit of area equal to ten thousand square metres', 'The farm covers ten hectares.', 'Ferma on gektary eýeleýär.', 'C1'),
    ('tonne', '/tʌn/', 'N', 'tonna (metric)', 'тонна', 'a unit of weight equal to one thousand kilograms', 'The load weighed a tonne.', 'Ýük bir tonna çekýärdi.', 'B2'),
    ('dimensions', '/daɪˈmenʃnz/', 'N', 'ölçegler (ululyk)', 'размеры', 'the measurements of size or shape', 'Check the dimensions before you build.', 'Gurmazdan öň ölçegleri barlaň.', 'B2'),
    ('area', '/ˈeəriə/', 'N', 'meýdan (ýer ululygy)', 'площадь', 'the amount of space inside a flat surface', 'The area of the field is large.', 'Meýdanyň ululygy uly.', 'B1'),
    ('volume', '/ˈvɒljuːm/', 'N', 'göwrüm (sygym)', 'объём', 'the amount of space inside a solid object', 'Find the volume of the box.', 'Gutynyň göwrümini tapyň.', 'B2'),
]

# ---- Vocabulary Bank — Punishment -> 7A ----
T['punishment'] = [
    ('fine', '/faɪn/', 'N', 'jerime', 'штраф', 'money you must pay as a punishment', 'He had to pay a fine.', 'Ol jerime tölemeli boldy.', 'B2'),
    ('sentence', '/ˈsentəns/', 'N', 'höküm (jeza möhleti)', 'приговор', 'the punishment a court gives a criminal', 'The judge gave a long sentence.', 'Kazy uzak höküm çykardy.', 'C1'),
    ('probation', '/prəˈbeɪʃn/', 'N', 'şertli synag möhleti', 'испытательный срок', 'a period of good behaviour instead of prison', 'He was released on probation.', 'Ol şertli synag möhleti bilen boşadyldy.', 'C2'),
    ('community service', '/kəˈmjuːnəti ˈsɜːvɪs/', 'N', 'jemgyýetçilik hyzmaty', 'общественные работы', 'unpaid work for the community as a punishment', 'She did community service.', 'Ol jemgyýetçilik hyzmatyny etdi.', 'C1'),
    ('suspended sentence', '/səˈspendɪd ˈsentəns/', 'N', 'şertli höküm (tussaglyksyz)', 'условный срок', 'a prison sentence not served unless you offend again', 'He got a suspended sentence.', 'Ol şertli höküm aldy.', 'C2'),
    ('parole', '/pəˈrəʊl/', 'N', 'möhletinden öň boşatma', 'досрочное освобождение', 'permission to leave prison before the end of a sentence', 'She was released on parole.', 'Ol möhletinden öň boşadyldy.', 'C2'),
    ('capital punishment', '/ˈkæpɪtl ˌpʌnɪʃmənt/', 'N', 'ölüm jezasyny', 'смертная казнь', 'the punishment of death for a crime', 'Capital punishment is banned here.', 'Bu ýerde ölüm jezasy gadagan.', 'C2'),
    ('life sentence', '/laɪf ˈsentəns/', 'N', 'ömürlik höküm', 'пожизненное заключение', 'a punishment of staying in prison for life', 'He received a life sentence.', 'Ol ömürlik höküm aldy.', 'C1'),
    ('acquit', '/əˈkwɪt/', 'V', 'aklamak (günäsiz tapmak)', 'оправдать', 'to officially say someone is not guilty', 'The jury acquitted her.', 'Kazyýet ony akady.', 'C2'),
    ('convict', '/kənˈvɪkt/', 'V', 'günäli tapmak (höküm etmek)', 'признать виновным', 'to officially say someone is guilty of a crime', 'He was convicted of theft.', 'Ol ogurlykda günäli tapyldy.', 'C1'),
    ('verdict', '/ˈvɜːdɪkt/', 'N', 'kazyýet karary', 'вердикт', 'the decision of guilty or not guilty in court', 'The verdict was not guilty.', 'Kazyýet karary günäsiz boldy.', 'C1'),
    ('custody', '/ˈkʌstədi/', 'N', 'tussaglyk (saklamak)', 'под стражей, опека', 'the state of being kept in prison or under guard', 'The suspect is in custody.', 'Güman edilýän tussaglykda.', 'C1'),
]

# ---- in-lesson 7B — connotation ----
T['connotation'] = [
    ('thrifty', '/ˈθrɪfti/', 'ADJ', 'tygşytly (ojakly)', 'бережливый', 'careful with money, in a good way', 'She is thrifty and saves well.', 'Ol tygşytly we gowy tygşytlaýar.', 'C2'),
    ('stingy', '/ˈstɪndʒi/', 'ADJ', 'gysganç (pula gysganç)', 'скупой', 'unwilling to spend money, in a bad way', 'He is too stingy to tip.', 'Ol çaý pul bermäge gaty gysganç.', 'C2'),
    ('confident', '/ˈkɒnfɪdənt/', 'ADJ', 'ynamly (özüne ynanýan)', 'уверенный', 'sure of yourself, in a good way', 'She gave a confident answer.', 'Ol ynamly jogap berdi.', 'B2'),
    ('arrogant', '/ˈærəɡənt/', 'ADJ', 'tekepbir (özünden razy)', 'высокомерный', 'thinking you are better than others, in a bad way', 'His arrogant tone annoyed everyone.', 'Onuň tekepbir äheňi hemmäni gaharlandyrdy.', 'C1'),
    ('curious', '/ˈkjʊəriəs/', 'ADJ', 'merakly (bilmek isleýän)', 'любопытный', 'eager to know things, in a good way', 'Children are naturally curious.', 'Çagalar tebigy merakly.', 'B2'),
    ('nosy', '/ˈnəʊzi/', 'ADJ', 'burnuny sokýan', 'любопытный (навязчивый)', 'too interested in other people s business, bad way', 'Do not be so nosy.', 'Beýle burnuňy sokma.', 'C1'),
    ('determined', '/dɪˈtɜːmɪnd/', 'ADJ', 'kürt (berk kararly)', 'решительный', 'having a strong will to succeed, good way', 'She is determined to win.', 'Ol ýeňmäge berk kararly.', 'B2'),
    ('stubborn', '/ˈstʌbən/', 'ADJ', 'tetik (pikirini üýtgetmeýän)', 'упрямый', 'refusing to change your mind, bad way', 'He is too stubborn to listen.', 'Ol diňlemäge gaty tetik.', 'C1'),
    ('ambitious', '/æmˈbɪʃəs/', 'ADJ', 'ysmanakly (uly maksatly)', 'амбициозный', 'having a strong desire to succeed, good way', 'She is an ambitious young lawyer.', 'Ol ysmanakly ýaş aklawçy.', 'B2'),
    ('ruthless', '/ˈruːθləs/', 'ADJ', 'rehimsiz (aýamasyz)', 'безжалостный', 'doing anything to succeed, with no pity, bad way', 'He is a ruthless businessman.', 'Ol rehimsiz işewür.', 'C2'),
    ('generous', '/ˈdʒenərəs/', 'ADJ', 'joomart (eli açyk)', 'щедрый', 'happy to give more than usual, good way', 'She is generous with her time.', 'Ol wagty babatda jomart.', 'B1'),
    ('extravagant', '/ɪkˈstrævəɡənt/', 'ADJ', 'ysraçy (çendenaşa)', 'расточительный', 'spending far too much money, bad way', 'The party was extravagant.', 'Toý ysraçy boldy.', 'C2'),
]

# ---- Vocabulary Bank — Eating and drinking -> 8A ----
T['eating'] = [
    ('nibble', '/ˈnɪbl/', 'V', 'ujy bilen dişlemek', 'покусывать, грызть', 'to eat small bites of something', 'She nibbled a biscuit.', 'Ol kökäni ujy bilen dişledi.', 'C2'),
    ('gulp', '/ɡʌlp/', 'V', 'yldyrym ýaly ýuwdamak', 'глотать', 'to swallow food or drink very quickly', 'He gulped down his coffee.', 'Ol kofesini yldyrym ýaly ýuwtdy.', 'C1'),
    ('devour', '/dɪˈvaʊə/', 'V', 'horluk bilen iýmek', 'пожирать', 'to eat something quickly and eagerly', 'The boys devoured the pizza.', 'Oglanlar pizzany horluk bilen iýdiler.', 'C2'),
    ('sip', '/sɪp/', 'V', 'ujy bilen içmek (az-azdan)', 'потягивать, отпивать', 'to drink a small amount at a time', 'She sipped her tea slowly.', 'Ol çaýyny haýal ujy bilen içdi.', 'C1'),
    ('savour', '/ˈseɪvə/', 'V', 'tagamyny çykaryp iýmek', 'наслаждаться вкусом', 'to enjoy food or an experience slowly', 'Savour every moment.', 'Her bir pursadyň tagamyny çykar.', 'C2'),
    ('munch', '/mʌntʃ/', 'V', 'gatyrdadyp iýmek', 'хрустеть, чавкать', 'to eat something noisily', 'He munched on an apple.', 'Ol almany gatyrdadyp iýdi.', 'C1'),
    ('gobble up', '/ˈɡɒbl ʌp/', 'PHR', 'horluk bilen ýuwdup iýmek', 'съедать жадно', 'to eat something very quickly and greedily', 'The children gobbled up the cake.', 'Çagalar torty horluk bilen ýuwdup iýdiler.', 'C2'),
    ('bolt down', '/bəʊlt daʊn/', 'PHR', 'gaýnadyp ýuwdamak (howlukmaç)', 'съедать наспех', 'to swallow food quickly without chewing', 'Do not bolt down your dinner.', 'Naharyňy howlukmaç iýmäň.', 'C2'),
    ('tuck into', '/tʌk ˈɪntə/', 'PHR', 'işdämen iýip başlamak', 'налегать на еду', 'to start eating eagerly', 'They tucked into the roast.', 'Olar gowrulan eti işdämen iýdiler.', 'C2'),
    ('wolf down', '/wʊlf daʊn/', 'PHR', 'möjek ýaly horluk bilen iýmek', 'проглатывать как волк', 'to eat very fast and greedily', 'He wolfed down his lunch.', 'Ol günortanlygyny horluk bilen iýdi.', 'C2'),
    ('peck at', '/pek æt/', 'PHR', 'iýmek islemän ujy bilen iýmek', 'ковыряться в еде', 'to eat only small amounts without interest', 'She just pecked at her food.', 'Ol naharyny diňe ujy bilen iýdi.', 'C2'),
    ('swallow', '/ˈswɒləʊ/', 'V', 'ýuwdamak', 'глотать, проглатывать', 'to make food or drink go down your throat', 'Swallow the pill with water.', 'Derminy suw bilen ýuwduň.', 'B2'),
]

# ---- Vocabulary Bank — Ways of seeing -> 8B ----
T['seeing'] = [
    ('glimpse', '/ɡlɪmps/', 'N', 'gysga nazar (bir pursat görmek)', 'мимолётный взгляд', 'a quick or incomplete look at something', 'I caught a glimpse of the sea.', 'Men deňze bir pursat nazar saldym.', 'C1'),
    ('glare', '/ɡleə/', 'V', 'gaharly seretmek', 'свирепо смотреть', 'to look at someone angrily', 'She glared at him.', 'Ol oňa gaharly seretdi.', 'C2'),
    ('stare', '/steə/', 'V', 'tik seretmek (uzak)', 'пристально смотреть', 'to look at something for a long time', 'Do not stare at people.', 'Adamlara tik seretme.', 'B2'),
    ('peer', '/pɪə/', 'V', 'ünsli seretmek (kyn görüp)', 'вглядываться', 'to look closely or with difficulty', 'He peered into the dark room.', 'Ol garaňky otaga ünsli seretdi.', 'C1'),
    ('squint', '/skwɪnt/', 'V', 'göz gyýap seretmek', 'щуриться', 'to look with your eyes partly closed', 'She squinted at the bright sun.', 'Ol ýagty güne göz gyýap seretdi.', 'C2'),
    ('glance', '/ɡlɑːns/', 'V', 'göz aýlamak (tiz seretmek)', 'взглянуть мельком', 'to take a quick short look', 'He glanced at his watch.', 'Ol sagadyna göz aýlady.', 'B2'),
    ('gaze', '/ɡeɪz/', 'V', 'oýlanyp uzak seretmek', 'пристально глядеть', 'to look at something steadily for a long time', 'They gazed at the stars.', 'Olar ýyldyzlara oýlanyp seretdiler.', 'C1'),
    ('peep', '/piːp/', 'V', 'ýaşyryn seretmek (deşikden)', 'подглядывать', 'to look quickly and secretly through a gap', 'She peeped through the curtains.', 'Ol perdeleriň arasyndan ýaşyryn seretdi.', 'C2'),
    ('wink', '/wɪŋk/', 'V', 'göz gypmak', 'подмигивать', 'to close and open one eye quickly as a signal', 'He winked at his friend.', 'Ol dostuna göz gypdy.', 'C1'),
    ('blink', '/blɪŋk/', 'V', 'göz gyrpym etmek', 'моргать', 'to shut and open your eyes quickly', 'She blinked in surprise.', 'Ol haýran galyp göz gyrpym etdi.', 'B2'),
    ('ogle', '/ˈəʊɡl/', 'V', 'arzuwly seretmek (namysyz)', 'заигрывать взглядом', 'to look at someone in a way that shows desire', 'He ogled her rudely.', 'Ol oňa namysyz seretdi.', 'C2'),
    ('scrutinise', '/ˈskruːtənaɪz/', 'V', 'üns bilen barlap seretmek', 'внимательно изучать', 'to look at something very carefully', 'She scrutinised the contract.', 'Ol şertnamany üns bilen barlady.', 'C2'),
]


# Advanced Plus has eight units, each split into lessons A and B, and NO
# Colloquial English / Practical English episodes, so there is no episode
# data-unit and no pe/ce interleaving — the unit list is just 1-8.
LESSONS = {
    '1A': (1, 'Motivation and inspiration', 'vague language', ['vague_language']),
    '1B': (1, 'The parent trap', 'phrasal nouns', ['phrasal_nouns']),
    '2A': (2, 'Overcoming adversity', 'prefixes and suffixes', ['affixes']),
    '2B': (2, 'A big adventure', 'ways of moving', ['moving']),
    '3A': (3, 'Live your age', 'research language', ['research']),
    '3B': (3, 'In love with Shakespeare', 'idioms from Shakespeare', ['shakespeare']),
    '4A': (4, 'No more boys and girls', 'binomials', ['binomials']),
    '4B': (4, 'Live to work?', 'acronyms and initialisms', ['acronyms']),
    '5A': (5, 'An emotional roller coaster', 'more sophisticated emotions', ['emotions']),
    '5B': (5, 'Crossing cultures', 'individuals and populations', ['populations']),
    '6A': (6, 'Hi-tech, lo-tech', 'adverb collocations · verbs for making things', ['adverbs_making']),
    '6B': (6, 'It all adds up', 'numbers and measurements', ['numbers']),
    '7A': (7, 'Whodunnit?', 'punishment', ['punishment']),
    '7B': (7, 'Alone or with friends?', 'connotation', ['connotation']),
    '8A': (8, 'Food of love', 'eating and drinking', ['eating']),
    '8B': (8, 'Seeing things differently', 'ways of seeing', ['seeing']),
}

# 3A "research language" is the one clearly academic topic; its words carry the
# Academic word-list badge. Everything else in this C1+ book is Oxford 5000.
ACADEMIC = {'3A'}


def lesson_sort_key(code):
    m = re.match(r'^(\d+)(.*)$', code)
    if m:
        return (int(m.group(1)), m.group(2))
    return (99, code)


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
                en, ipa, pos, tm, ru, de, ex, exTm, cefr = e[:9]
                coll = e[9] if len(e) > 9 else ''
                key = en.strip().lower()
                if key in seen:
                    dups.append(f'{lesson}: "{en}" (already in {seen[key]})')
                    continue
                seen[key] = lesson
                ox = 'Academic' if lesson in ACADEMIC else ('Oxford 3000' if cefr in ('A1', 'A2') else 'Oxford 5000')
                words.append({
                    'en': en, 'ipa': ipa, 'pos': pos, 'tm': tm, 'ru': ru,
                    'def': de, 'ex': ex, 'exTm': exTm, 'cefr': cefr, 'ox': ox,
                    'syn': '—', 'coll': coll or '—', 'stage': 'New',
                    'books': [{'book': 'advp', 'unit': unit, 'lesson': lesson}],
                    'proofread': False,
                })

    if dups:
        raise SystemExit('duplicate headwords:\n  ' + '\n  '.join(dups))

    used = set(t for ts in LESSONS.values() for t in ts[3])
    unused = sorted(set(T) - used)
    if unused:
        raise SystemExit('topics declared but never used: ' + ', '.join(unused))

    lessons, empty = [], []
    for lesson in sorted(LESSONS, key=lesson_sort_key):
        unit, title, topic, topics = LESSONS[lesson]
        n = sum(1 for w in words if w['books'][0]['lesson'] == lesson)
        if not n:
            empty.append(lesson)
            continue
        lessons.append({'lesson': lesson, 'unit': unit, 'title': title, 'topic': topic, 'words': n})
    if empty:
        raise SystemExit('lessons with no words — fill them: ' + ', '.join(empty))

    pack = {
        'book': 'advp',
        'title': 'English File Advanced Plus (4th edition) — vocabulary, by lesson',
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
