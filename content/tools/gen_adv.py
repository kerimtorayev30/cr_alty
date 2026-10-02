#!/usr/bin/env python3
"""English File Advanced — vocabulary organised by the book's own structure.

Same method as gen_upp.py / gen_int.py. The OCR dump (uploads/Advanced.txt,
11,181 lines) kept the contents table and the Vocabulary Bank references
legible. tm / ru / def / ex are my own work and proofread:false; the IPA is
written properly, not copied from the OCR.

STRUCTURE (contents table, dump lines 26-105). Advanced 4th edition has 10
units, each with TWO lessons (A and B — no C), and five Colloquial English
episodes after units 1, 3, 5, 7 and 9:
  1A We are family · 1B A job for life? · CE1 talking about work and family
  2A Do you remember...? · 2B On the tip of my tongue
  3A A love-hate relationship · 3B Dramatic licence · CE2 talking about history
  4A An open book · 4B The sound of silence
  5A No time for anything · 5B Not for profit? · CE3 talking about stress
  6A Help, I need somebody! · 6B Can't give it up
  7A As a matter of fact... · 7B A masterpiece? · CE4 talking about illustration
  8A The best medicine? · 8B A 'must-see' attraction
  9A Pet hates · 9B How to cook, how to eat · CE5 talking about insects
  10A On your marks, set, go! · 10B No direction home

Vocabulary Bank (11 sections) -> lesson: Personality->1A, Work->1B,
Phrases with get->3A, Conflict and warfare->3B, Sounds and the human
voice->4B, Expressions with time->5A, Money->5B, Prefixes->7A,
Travel and tourism->8B, Animal matters->9A, Preparing food->9B.
Everything else comes from in-lesson boxes.

Colloquial English episodes carry unit 11 in the data (units 1-10 are the
book's), and the app shows each episode right after the unit it follows.

Usage: python3 content/tools/gen_adv.py
"""
import json
import os
import re
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'advanced.json')

# topic -> [ (en, ipa, pos, tm, ru, def, ex, exTm, cefr[, coll]) ]
T = {}

# ---- Vocabulary Bank — Personality -> 1A ----
T['personality'] = [
    ('charming', '/ˈtʃɑːmɪŋ/', 'ADJ', 'özüne çekiji (sympatik)', 'очаровательный', 'very pleasant and likeable', 'The charming host welcomed everyone.', 'Özüne çekiji eýe hemmäni garşylady.', 'B1'),
    ('cheerful', '/ˈtʃɪəfl/', 'ADJ', 'şähdaçyk', 'жизнерадостный', 'happy and positive', 'She gave us a cheerful smile.', 'Şähdaçyk ýylgyryş berdi.', 'A2'),
    ('cruel', '/ˈkruːəl/', 'ADJ', 'rehimsiz', 'жестокий', 'causing pain without pity', 'It was cruel to laugh at him.', 'Oňa gülmek rehimsiz boldy.', 'B1'),
    ('gentle', '/ˈdʒentl/', 'ADJ', 'mulýum', 'нежный, мягкий', 'kind and careful', 'Be gentle with the kitten.', 'Pişik çagasyna mulýum bol.', 'A2'),
    ('mean', '/miːn/', 'ADJ', 'gysganç (erbet)', 'скупой, злой', 'unkind, or unwilling to share', 'It was mean of him to say that.', 'Onuň beýle aýtmagy erbet boldy.', 'A2'),
    ('moody', '/ˈmuːdi/', 'ADJ', 'keýpi üýtgeýän', 'с переменчивым настроением', 'often changing moods', 'Teenagers can be moody.', 'Ýetginjekleriň keýpi üýtgäp durýar.', 'B1'),
    ('optimistic', '/ˌɒptɪˈmɪstɪk/', 'ADJ', 'oňyn pikirlenýän', 'оптимистичный', 'expecting good things', 'She is optimistic about the future.', 'Geljege oňyn garaýar.', 'B1', 'optimistic about'),
    ('outgoing', '/ˈaʊtɡəʊɪŋ/', 'ADJ', 'açyk (jemgyýetçil)', 'общительный, открытый', 'friendly and sociable', 'His outgoing manner wins people over.', 'Açyk häsiýeti adamlary özüne çekýär.', 'B1'),
    ('patient', '/ˈpeɪʃnt/', 'ADJ', 'sabyrly', 'терпеливый', 'able to wait without complaining', 'A good teacher is patient.', 'Gowy mugallym sabyrly bolýar.', 'A2'),
    ('pessimistic', '/ˌpesɪˈmɪstɪk/', 'ADJ', 'ýaramaz pikirlenýän', 'пессимистичный', 'expecting bad things', 'Do not be so pessimistic!', 'Beýle ýaramaz pikirlenme!', 'B1'),
    ('shy', '/ʃaɪ/', 'ADJ', 'ýaýraň', 'застенчивый', 'nervous about meeting people', 'The shy boy hid behind his mother.', 'Ýaýraň oglan ejesiniň arkasynda gizlendi.', 'A2'),
    ('stubborn', '/ˈstʌbən/', 'ADJ', 'tetik (inat)', 'упрямый', 'refusing to change your mind', 'He is too stubborn to apologise.', 'Ol ötünç soramak üçin gaty inat.', 'B1'),
    ('vain', '/veɪn/', 'ADJ', 'özüni göterýän', 'тщеславный', 'too proud of your appearance', 'The vain actor admired his photo.', 'Özüni göterýän aktýor suratyna syn etdi.', 'B2'),
    ('wise', '/waɪz/', 'ADJ', 'paýhasly (dana)', 'мудрый', 'having deep understanding', 'My grandmother gave me wise advice.', 'Mamam paýhasly maslahat berdi.', 'A2'),
]

# ---- Vocabulary Bank — Work -> 1B ----
T['work2'] = [
    ('ambition', '/æmˈbɪʃn/', 'N', 'maksat (öňe saýlanma)', 'амбиция, стремление', 'a strong wish to achieve something', 'Her ambition is to become a doctor.', 'Maksady lukman bolmak.', 'B1', 'career ambition'),
    ('career', '/kəˈrɪə(r)/', 'N', 'kär (uzak möhletli iş)', 'карьера', 'a job or profession you do for years', 'He built a career in banking.', 'Bank ulgamynda kär gurdu.', 'A2', 'career path'),
    ('intern', '/ˈɪntɜːn/', 'N', 'stajýor', 'стажёр', 'a student gaining work experience', 'The intern helped with the report.', 'Stajýor hasabata kömek etdi.', 'B1'),
    ('job satisfaction', '/dʒɒb ˌsætɪsˈfækʃn/', 'N', 'işden kanagatlanma', 'удовлетворение работой', 'the pleasure you get from your job', 'Job satisfaction matters more than pay.', 'Işden kanagatlanma aýlykdan möhüm.', 'B2'),
    ('profession', '/prəˈfeʃn/', 'N', 'hünär (kär)', 'профессия', 'a job needing special training', 'Teaching is a noble profession.', 'Mugallymçylyk asylly hünär.', 'A2'),
    ('promotion', '/prəˈməʊʃn/', 'N', 'wezipe galmak', 'повышение (в должности)', 'moving to a higher job level', 'She got a promotion last year.', 'Geçen ýyl wezipesi galdy.', 'A2', 'get a promotion'),
    ('qualified', '/ˈkwɒlɪfaɪd/', 'ADJ', 'hünärli', 'квалифицированный', 'having the right training for a job', 'We need a qualified electrician.', 'Hünärli elektrik gerek.', 'A2', 'highly qualified'),
    ('retire', '/rɪˈtaɪə(r)/', 'V', 'pensiýa çykmak', 'выходить на пенсию', 'to stop working because of age', 'He plans to retire at sixty.', 'Alty ýaşynda pensiýa çykmagy meýilleşdirýär.', 'A2', 'retire from'),
    ('unemployment', '/ˌʌnɪmˈplɔɪmənt/', 'N', 'işsizlik', 'безработица', 'the state of having no job', 'Unemployment fell this year.', 'Işsizlik şu ýyl azaldy.', 'B1', 'unemployment rate'),
    ('vacancy', '/ˈveɪkənsi/', 'N', 'boş iş orny', 'вакансия', 'an unfilled job position', 'There is a vacancy in the sales team.', 'Satuw toparynda boş iş orny bar.', 'B1', 'job vacancy'),
    ('workaholic', '/ˌwɜːkəˈhɒlɪk/', 'N', 'işbaz', 'трудоголик', 'a person who works too much', 'The workaholic never takes holidays.', 'Işbaz hiç wagt dynç almaga gitmeýär.', 'B2'),
    ('workforce', '/ˈwɜːkfɔːs/', 'N', 'işçi güýji', 'рабочая сила', 'all the workers of a company', 'The workforce grew by ten per cent.', 'Işçi güýji on göterim artdy.', 'B2'),
]

# ---- in-lesson 2A — abstract nouns ----
T['abstract_nouns'] = [
    ('anger', '/ˈæŋɡə(r)/', 'N', 'gahar', 'гнев', 'a strong feeling of displeasure', 'He spoke with anger in his voice.', 'Sesinde gahar bilen gürledi.', 'A2', 'feel anger'),
    ('anxiety', '/æŋˈzaɪəti/', 'N', 'alada (ynjalyksyzlyk)', 'тревога', 'a feeling of worry', 'Exams cause anxiety for students.', 'Synaglar talyplarda alada döredýär.', 'B1', 'feel anxiety'),
    ('courage', '/ˈkʌrɪdʒ/', 'N', 'edermenlik', 'мужество', 'the ability to face danger', 'The firefighter showed great courage.', 'Ýangyn söndüriji uly edermenlik görkezdi.', 'A2', 'have the courage'),
    ('curiosity', '/ˌkjʊəriˈɒsəti/', 'N', 'interik', 'любопытство', 'a wish to know things', 'Her curiosity never stops.', 'Interigi hiç wagt gutaranok.', 'A2', 'out of curiosity'),
    ('enthusiasm', '/ɪnˈθjuːziæzəm/', 'N', 'yhläs', 'энтузиазм', 'a feeling of great interest', 'She talked with real enthusiasm.', 'Hakyky yhläs bilen gürrüň berdi.', 'B1', 'show enthusiasm'),
    ('friendship', '/ˈfrendʃɪp/', 'N', 'dostluk', 'дружба', 'the relationship between friends', 'Their friendship lasted forty years.', 'Dostlugy kyrk ýyl dowam etdi.', 'A2'),
    ('happiness', '/ˈhæpinəs/', 'N', 'bagt', 'счастье', 'the feeling of being happy', 'Money does not always bring happiness.', 'Pul hemişe bagt getirmeýär.', 'A2'),
    ('honesty', '/ˈɒnəsti/', 'N', 'dogruçyllyk', 'честность', 'the quality of telling the truth', 'I appreciate your honesty.', 'Dogruçyllygyňa baha berýärin.', 'B1'),
    ('intelligence', '/ɪnˈtelɪdʒəns/', 'N', 'zeka', 'интеллект', 'the ability to learn and understand', 'The puzzle tested my intelligence.', 'Tapmaça zekamy synady.', 'A2'),
    ('kindness', '/ˈkaɪndnəs/', 'N', 'mähirlilik', 'доброта', 'the quality of being kind', 'Thank you for your kindness.', 'Mähirliligiňiz üçin sag boluň.', 'A2'),
    ('loneliness', '/ˈləʊnlinəs/', 'N', 'ýalňyzlyk', 'одиночество', 'sadness from being alone', 'Loneliness affects many old people.', 'Ýalňyzlyk köp garrylara täsir edýär.', 'B1'),
    ('patience', '/ˈpeɪʃns/', 'N', 'sabyr', 'терпение', 'the ability to wait calmly', 'Teaching requires great patience.', 'Mugallymçylyk uly sabyr talap edýär.', 'A2', 'lose patience'),
    ('pride', '/praɪd/', 'N', 'buýsanç', 'гордость', 'a feeling of pleasure in yourself', 'She spoke with pride about her son.', 'Ogly barada buýsanç bilen gürledi.', 'A2', 'take pride in'),
    ('wealth', '/welθ/', 'N', 'baýlyk', 'богатство', 'a large amount of money', 'He shared his wealth with others.', 'Baýlygyny beýlekiler bilen paýlaşdy.', 'A2'),
]

# ---- in-lesson 2B — relationships ----
T['relationships'] = [
    ('acquaintance', '/əˈkweɪntəns/', 'N', 'tanyş', 'знакомый', 'a person you know a little', 'He is an acquaintance, not a friend.', 'Ol dost däl, tanyş.', 'B1'),
    ('bond', '/bɒnd/', 'N', 'baglanyşyk (duýgy)', 'связь, узы', 'a strong feeling between people', 'The twins have a special bond.', 'Ekizleriň aýratyn baglanyşygy bar.', 'B1', 'emotional bond'),
    ('companion', '/kəmˈpæniən/', 'N', 'ýoldaş (hemra)', 'спутник, компаньон', 'a person you spend time with', 'The dog was her faithful companion.', 'It onuň wepaly ýoldaşy boldy.', 'B1'),
    ('engagement', '/ɪnˈɡeɪdʒmənt/', 'N', 'atlanysyklar', 'помолвка', 'an agreement to marry', 'They announced their engagement.', 'Atlanyşyklaryny yglan etdiler.', 'B1'),
    ('marriage', '/ˈmærɪdʒ/', 'N', 'toý (nika)', 'брак, супружество', 'the state of being married', 'Their marriage has lasted ten years.', 'Nikalary on ýyl dowam etdi.', 'A2', 'happy marriage'),
    ('mate', '/meɪt/', 'N', 'dost (ýoldaş)', 'приятель', 'a friend (informal)', 'He went fishing with his mates.', 'Dostlary bilen balyk tutmaga gitdi.', 'A2'),
    ('relatives', '/ˈrelətɪvz/', 'N', 'garyndaşlar', 'родственники', 'members of your family', 'All our relatives came to the wedding.', 'Ähli garyndaşlarymyz toýa geldi.', 'A2'),
    ('sibling', '/ˈsɪblɪŋ/', 'N', 'dogan (aga-ini/uýa)', 'брат или сестра', 'a brother or sister', 'Do you have any siblings?', 'Doganyňyz barmy?', 'B1'),
    ('spouse', '/spaʊs/', 'N', 'ýanýoldaş', 'супруг(а)', 'a husband or wife', 'You may bring your spouse to the dinner.', 'Agşamlyk nahara ýanýoldaşyňyzy alyp gelip bilersiňiz.', 'B2'),
    ('generation gap', '/ˌdʒenəˈreɪʃn ɡæp/', 'N', 'nesil tapawudy', 'разрыв поколений', 'differences between old and young', 'Music often shows the generation gap.', 'Saz köplenç nesil tapawudyny görkezýär.', 'B1'),
]

# ---- Vocabulary Bank — Phrases with get -> 3A ----
T['get_phrases'] = [
    ('get away with', '/ɡet əˈweɪ wɪð/', 'PHR', 'jezasyz gutulmak', 'сходить с рук', 'to do something wrong without punishment', 'He never gets away with lies.', 'Ýalany hiç wagt jezasyz galmaýar.', 'B1'),
    ('get by', '/ɡet baɪ/', 'PHR', 'güzeranyny dolamak', 'сводить концы с концами', 'to manage with difficulty', 'They get by on a small salary.', 'Az aýlyk bilen güzeranyny dolap gelýärler.', 'B1', 'get by on'),
    ('get down to', '/ɡet daʊn tuː/', 'PHR', 'başlamak (çynlakaý)', 'браться за', 'to start doing something seriously', 'Let us get down to work.', 'Geliň, işe girişeliň.', 'A2', 'get down to business'),
    ('get over', '/ɡet ˈəʊvə(r)/', 'PHR', 'gutulmak (keselden)', 'оправиться от', 'to recover from something bad', 'She finally got over the flu.', 'Ahyry dümewden gutuldy.', 'A2', 'get over an illness'),
    ('get together', '/ɡet təˈɡeðə(r)/', 'PHR', 'ýygnanmak', 'собираться вместе', 'to meet and spend time', 'We get together every Sunday.', 'Her ýekşenbe ýygnanýarys.', 'A2'),
    ('get used to', '/ɡet ˈjuːzd tuː/', 'PHR', 'öwrenişmek', 'привыкать', 'to become familiar with something', 'I got used to the cold weather.', 'Sowuk howa öwrenişdim.', 'A2', 'get used to doing'),
    ('get away', '/ɡet əˈweɪ/', 'PHR', 'gaçyp gutulmak', 'сбежать, вырваться', 'to escape, or go on holiday', 'The thieves got away in a car.', 'Ogrular maşyn bilen gaçyp gutuldy.', 'A2'),
    ('get round to', '/ɡet ˈraʊnd tuː/', 'PHR', 'wagt tapyp etmek', 'собираться сделать', 'to finally do something delayed', 'I never got round to calling him.', 'Oňa jaň etmäge wagt tapmadym.', 'B2'),
]

# ---- Vocabulary Bank — Conflict and warfare -> 3B ----
T['conflict'] = [
    ('battlefield', '/ˈbætlfiːld/', 'N', 'söweş meýdany', 'поле боя', 'a place where a battle happens', 'The battlefield is now a museum.', 'Söweş meýdany indi muzeý.', 'B1'),
    ('casualty', '/ˈkæʒuəlti/', 'N', 'pidalar (ýitgiler)', 'жертвы, потери', 'a person killed or injured in war', 'The battle caused many casualties.', 'Söweş köp pidalara sebäp boldy.', 'B2'),
    ('civilian', '/səˈvɪliən/', 'N', 'asuda ilat', 'мирный житель', 'a person not in the army', 'The war harmed many civilians.', 'Uruş köp asuda ilata zyýan ýetirdi.', 'B1'),
    ('defeat', '/dɪˈfiːt/', 'V', 'ýeňmek', 'побеждать (в войне)', 'to win against an enemy', 'The army defeated the invaders.', 'Goşun basyp alýjylary ýeňdi.', 'A2'),
    ('defend', '/dɪˈfend/', 'V', 'goramak', 'защищать', 'to protect from attack', 'The soldiers defended the city.', 'Esgirler şäheri gorady.', 'A2', 'defend against'),
    ('enemy', '/ˈenəmi/', 'N', 'duşman', 'враг', 'a person or country you fight', 'The enemy attacked at dawn.', 'Duşman dan atacasy hüjüm etdi.', 'A2'),
    ('invade', '/ɪnˈveɪd/', 'V', 'basyp almak', 'вторгаться', 'to enter a country by force', 'The invaders crossed the border.', 'Basyp alýjylar serhetden geçdi.', 'B1'),
    ('rescue', '/ˈreskjuː/', 'V', 'halas etmek', 'спасать', 'to save someone from danger', 'Firefighters rescued the family.', 'Ýangyn söndürijiler maşgalany halas etdi.', 'A2', 'rescue someone'),
    ('siege', '/siːdʒ/', 'N', 'gabaw', 'осада', 'surrounding a place to force surrender', 'The siege lasted three months.', 'Gabaw üç aý dowam etdi.', 'B2', 'under siege'),
    ('soldier', '/ˈsəʊldʒə(r)/', 'N', 'esger', 'солдат', 'a member of an army', 'The soldier returned home.', 'Esger öýüne gaýtdy.', 'A2'),
    ('surrender', '/səˈrendə(r)/', 'V', 'boýun egmek', 'сдаваться', 'to stop fighting and admit defeat', 'The troops were forced to surrender.', 'Goşun boýun egmäge mejbur boldy.', 'B1'),
    ('victim', '/ˈvɪktɪm/', 'N', 'pida', 'жертва', 'a person harmed by something', 'The victims received help quickly.', 'Pidalar kömegi tiz aldy.', 'A2', 'victim of'),
    ('weapon', '/ˈwepən/', 'N', 'ýarag', 'оружие', 'an object used for fighting', 'The museum displays old weapons.', 'Muzeý köne ýaraglary görkezýär.', 'A2', 'carry a weapon'),
]

# ---- in-lesson 4A — describing books and films ----
T['books_films'] = [
    ('bestseller', '/ˌbestˈselə(r)/', 'N', 'iň köp satylýan kitap', 'бестселлер', 'a book that sells in huge numbers', 'Her novel became a bestseller.', 'Romany iň köp satylýan kitap boldy.', 'A2'),
    ('blockbuster', '/ˈblɒkbʌstə(r)/', 'N', 'uly üstünlikli film', 'блокбастер', 'a very successful film', 'The blockbuster earned millions.', 'Uly üstünlikli film millionlar gazandy.', 'A2'),
    ('cliffhanger', '/ˈklɪfhæŋə(r)/', 'N', 'yzy gyzykly gutarýan', 'захватывающая концовка', 'an ending that leaves you wanting more', 'The series ended on a cliffhanger.', 'Serial yzy gyzykly gutardy.', 'B2'),
    ('gripping', '/ˈɡrɪpɪŋ/', 'ADJ', 'özüne bend edýän', 'захватывающий', 'so exciting you cannot stop', 'It was a gripping thriller.', 'Özüne bend edýän triller boldy.', 'B1'),
    ('masterpiece', '/ˈmɑːstəpiːs/', 'N', 'şedewr', 'шедевр', 'an excellent work of art', 'The painting is a true masterpiece.', 'Surat hakyky şedewr.', 'B1'),
    ('moving', '/ˈmuːvɪŋ/', 'ADJ', 'täsirli (duýgur)', 'трогательный', 'making you feel strong emotions', 'The ending was deeply moving.', 'Soňy örän täsirli boldy.', 'A2'),
    ('sequel', '/ˈsiːkwəl/', 'N', 'dowamy (kitap/film)', 'продолжение, сиквел', 'a story that continues an earlier one', 'The sequel comes out next year.', 'Dowamy indiki ýyl çykýar.', 'A2'),
    ('thriller', '/ˈθrɪlə(r)/', 'N', 'triller', 'триллер', 'an exciting story about crime', 'I love a good thriller.', 'Gowy trilleri gowy görýärin.', 'A2'),
    ('trailer', '/ˈtreɪlə(r)/', 'N', 'film mahabaty', 'трейлер', 'a short advertisement for a film', 'The trailer looks amazing.', 'Film mahabaty ajaýyp görünýär.', 'A2', 'watch a trailer'),
    ('twist', '/twɪst/', 'N', 'garaşylmadyk öwrüm', 'неожиданный поворот', 'a surprising change in a story', 'The final twist shocked everyone.', 'Soňky öwrüm hemmäni şok etdi.', 'B1', 'plot twist'),
]

# ---- Vocabulary Bank — Sounds and the human voice -> 4B ----
T['voice'] = [
    ('accent', '/ˈæksent/', 'N', 'talaffuz (şiwä)', 'акцент', 'a way of speaking from a region', 'She has a beautiful accent.', 'Owadan talaffuzy bar.', 'A2', 'foreign accent'),
    ('echo', '/ˈekəʊ/', 'N', 'ýaň', 'эхо', 'a sound that comes back', 'Our voices made an echo.', 'Seslerimiz ýaň etdi.', 'A2'),
    ('hoarse', '/hɔːs/', 'ADJ', 'ýogyn (sesi ýatyk)', 'охрипший', 'with a rough voice', 'He was hoarse after shouting.', 'Gygyrandan soň sesi ýatyk boldy.', 'B2'),
    ('mumble', '/ˈmʌmbl/', 'V', 'pyşyrdamak (aňsat eşitmezlik)', 'бормотать', 'to speak unclearly and quietly', 'He mumbled an apology.', 'Ötünç sorap pyşyrdady.', 'B2'),
    ('mutter', '/ˈmʌtə(r)/', 'V', 'zöldürdemek', 'ворчать себе под нос', 'to complain quietly under the breath', 'She muttered about the price.', 'Baha barada zöldürdedi.', 'B2'),
    ('scream', '/skriːm/', 'V', 'gygyrmak (gaty)', 'кричать, вопить', 'to make a loud high sound', 'The fans screamed with joy.', 'Janköýerler şatlykdan gygyrdy.', 'A2'),
    ('shout', '/ʃaʊt/', 'V', 'gygyrmak', 'кричать', 'to say something very loudly', 'Do not shout at the children.', 'Çagalara gygyrma.', 'A2', 'shout at'),
    ('sigh', '/saɪ/', 'V', 'ah çekmek', 'вздыхать', 'to breathe out slowly with feeling', 'She sighed with relief.', 'Ýeňillik bilen ah çekdi.', 'A2'),
    ('squeak', '/skwiːk/', 'V', 'çyrlamak (ýuka ses)', 'пищать', 'to make a short high sound', 'The mouse squeaked in the trap.', 'Syçan duzakda çyrlady.', 'B2'),
    ('whisper', '/ˈwɪspə(r)/', 'V', 'pyşyrdamak', 'шептать', 'to speak very quietly', 'She whispered the answer.', 'Jogaby pyşyrdady.', 'A2', 'whisper to'),
]
# ---- Vocabulary Bank — Expressions with time -> 5A ----
T['time_expr'] = [
    ('ahead of time', '/əˈhed əv taɪm/', 'PHR', 'öňünden', 'заранее', 'earlier than planned', 'We finished ahead of time.', 'Öňünden gutardy.', 'A2'),
    ('behind schedule', '/bɪˈhaɪnd ˈʃedjuːl/', 'PHR', 'meýilnamadan yza galan', 'с опозданием от графика', 'later than planned', 'The project is two weeks behind schedule.', 'Taslama iki hepde yza galdy.', 'B1'),
    ('for the time being', '/fə ðə taɪm ˈbiːɪŋ/', 'PHR', 'häzirlikçe', 'на данный момент', 'for now, but not for ever', 'Stay here for the time being.', 'Häzirlikçe şu ýerde gal.', 'B1'),
    ('in advance', '/ɪn ədˈvɑːns/', 'PHR', 'öňünden (öňünden tölemek)', 'заблаговременно', 'before something happens', 'Book the tickets in advance.', 'Biletleri öňünden bronla.', 'A2', 'pay in advance'),
    ('in no time', '/ɪn nəʊ taɪm/', 'PHR', 'göz açyp ýumasy salymda', 'в мгновение ока', 'very quickly', 'Dinner will be ready in no time.', 'Agşamlyk göz açyp ýumasy salymda taýyn bolar.', 'A2'),
    ('on time', '/ɒn taɪm/', 'PHR', 'wagtynda', 'вовремя', 'at the planned time', 'The train arrived on time.', 'Otluda wagtynda geldi.', 'A1'),
    ('in time', '/ɪn taɪm/', 'PHR', 'wagty ýetip (giç galman)', 'вовремя (успеть)', 'early enough to do something', 'We got there in time for dinner.', 'Agşamlyk nahara wagty ýetip ýetdik.', 'A2', 'in time for'),
    ('time after time', '/taɪm ˈɑːftə taɪm/', 'PHR', 'gaýta-gaýta', 'раз за разом', 'again and again', 'He has warned you time after time.', 'Saňa gaýta-gaýta duýdurdy.', 'B1'),
    ('from time to time', '/frɒm taɪm tuː taɪm/', 'PHR', 'wagtal-wagtal', 'время от времени', 'sometimes, not often', 'We visit them from time to time.', 'Wagtal-wagtal olara baryp görýäris.', 'A2'),
    ('kill time', '/kɪl taɪm/', 'PHR', 'wagt öldürmek', 'коротать время', 'to do something while waiting', 'We killed time at the airport.', 'Howa menzilinde wagt öldürdik.', 'A2'),
]

# ---- Vocabulary Bank — Money -> 5B ----
T['money2'] = [
    ('bankrupt', '/ˈbæŋkrʌpt/', 'ADJ', 'müflüs', 'банкрот', 'unable to pay your debts', 'The company went bankrupt last year.', 'Kompaniýa geçen ýyl müflüs boldy.', 'B1', 'go bankrupt'),
    ('budget', '/ˈbʌdʒɪt/', 'N', 'büjet', 'бюджет', 'a plan for spending money', 'We are on a tight budget this month.', 'Şu aý büjetimiz gysyk.', 'A2', 'on a budget'),
    ('currency', '/ˈkʌrənsi/', 'N', 'walýuta', 'валюта', 'the money used in a country', 'The local currency is the manat.', 'Ýerli walýuta manat.', 'A2', 'foreign currency'),
    ('debt', '/det/', 'N', 'karz (bergi)', 'долг', 'money that you owe', 'He paid off all his debts.', 'Ähli bergilerini töledi.', 'B1', 'pay off a debt'),
    ('deposit', '/dɪˈpɒzɪt/', 'N', 'depozit (öňünden töleg)', 'залог, депозит', 'part of the money paid first', 'We paid a deposit for the flat.', 'Öý üçin depozit töledik.', 'B1', 'pay a deposit'),
    ('fortune', '/ˈfɔːtʃuːn/', 'N', 'uly baýlyk', 'состояние, состояние денег', 'a very large amount of money', 'The car cost a fortune.', 'Maşyn uly baýlyga durdy.', 'A2', 'cost a fortune'),
    ('income', '/ˈɪnkʌm/', 'N', 'girdeji (aýlyk)', 'доход', 'money received regularly', 'Their income covers all expenses.', 'Girdejileri ähli çykdajylary örtýär.', 'A2', 'monthly income'),
    ('instalment', '/ɪnˈstɔːlmənt/', 'N', 'bölekleýin töleg', 'взнос, рассрочка', 'one part of a total payment', 'We pay the loan in monthly instalments.', 'Karzy aýlyk bölekleýin töleýäris.', 'B2', 'pay in instalments'),
    ('pension', '/ˈpenʃn/', 'N', 'pensiýa (pul)', 'пенсия', 'money paid after retirement', 'Her pension is paid monthly.', 'Pensiýasy aýlyk tölenýär.', 'A2', 'state pension'),
    ('tax', '/tæks/', 'N', 'salyk', 'налог', 'money paid to the government', 'Income tax went up this year.', 'Girdeji salygy şu ýyl galdy.', 'A2', 'pay tax'),
    ('cheque', '/tʃek/', 'N', 'çek', 'чек', 'a paper order to a bank to pay', 'He paid the rent by cheque.', 'Kärendäni çek bilen töledi.', 'A2', 'pay by cheque'),
    ('coin', '/kɔɪn/', 'N', 'teňňe', 'монета', 'a small flat piece of metal money', 'He tossed a coin to decide.', 'Karar bermek üçin teňňe zyňdy.', 'A1'),
]

# ---- in-lesson 6A — compound adjectives ----
T['compound_adjs2'] = [
    ('absent-minded', '/ˌæbsnt ˈmaɪndɪd/', 'ADJ', 'ünsüz (huşsuz)', 'рассеянный', 'often forgetting things', 'The absent-minded professor lost his keys.', 'Ünsüz professor açarlaryny ýitirdi.', 'B1'),
    ('broad-minded', '/ˌbrɔːd ˈmaɪndɪd/', 'ADJ', 'giň pikirli', 'широко мыслящий', 'accepting different opinions', 'Her broad-minded parents welcomed everyone.', 'Giň pikirli ene-atasy hemmäni garşylady.', 'B2'),
    ('deep-fried', '/ˌdiːp ˈfraɪd/', 'ADJ', 'ýagda gowrulan', 'жаренный во фритюре', 'cooked in deep hot oil', 'Deep-fried food is not healthy.', 'Ýagda gowrulan nahar peýdaly däl.', 'B1'),
    ('first-class', '/ˌfɜːst ˈklɑːs/', 'ADJ', 'birinji derejeli', 'первоклассный', 'of the best quality', 'We travelled first-class to London.', 'Londona birinji derejeli gatnadyk.', 'A2'),
    ('hard-working', '/ˌhɑːd ˈwɜːkɪŋ/', 'ADJ', 'zähmetsöýer', 'трудолюбивый', 'putting a lot of effort into work', 'She is an honest, hard-working student.', 'Dogruçyl, zähmetsöýer talyp.', 'A2'),
    ('ill-mannered', '/ˌɪl ˈmænəd/', 'ADJ', 'edebsiz', 'невоспитанный', 'having bad manners', 'The ill-mannered guest interrupted everyone.', 'Edebsiz myhman hemmäniň sözünü kesdi.', 'B2'),
    ('short-sighted', '/ˌʃɔːt ˈsaɪtɪd/', 'ADJ', 'uzagy görmeyän', 'близорукий; недальновидный', 'unable to see far, or not planning ahead', 'It was a short-sighted decision.', 'Uzagy görmeyän karar boldy.', 'B2'),
    ('well-behaved', '/ˌwel bɪˈheɪvd/', 'ADJ', 'edeply', 'воспитанный (о поведении)', 'behaving politely', 'The well-behaved children sat quietly.', 'Edepli çagalar sessiz otyrdy.', 'B1'),
    ('well-dressed', '/ˌwel ˈdrest/', 'ADJ', 'oňat geýnen', 'хорошо одетый', 'wearing nice clothes', 'The well-dressed guests arrived at eight.', 'Oňat geýnen myhmanlar sekizde geldi.', 'A2'),
    ('well-off', '/ˌwel ˈɒf/', 'ADJ', 'halatly (baý)', 'состоятельный', 'having plenty of money', 'Her well-off family helped with the fees.', 'Halatly maşgalasy töleglere kömek etdi.', 'B1'),
    ('time-consuming', '/ˌtaɪm kənˈsjuːmɪŋ/', 'ADJ', 'wagt talap edýän', 'трудоёмкий', 'taking a lot of time', 'Sorting photos is time-consuming.', 'Suratlary tertiplemek wagt talap edýän iş.', 'B2'),
    ('mouth-watering', '/ˌmaʊθ ˈwɔːtərɪŋ/', 'ADJ', 'agyz suwardyjy', 'аппетитный', 'looking or smelling delicious', 'The cake looked mouth-watering.', 'Tort agyz suwardyjy görünýärdi.', 'B2'),
]

# ---- in-lesson 6B — phones and technology ----
T['phones_tech'] = [
    ('backup', '/ˈbækʌp/', 'N', 'ätiýaç nusga', 'резервная копия', 'a copy of data kept safe', 'Always make a backup of your files.', 'Faýllaryňyzyň ätiýaç nusgasyny hemişe ediň.', 'A2', 'make a backup'),
    ('browser', '/ˈbraʊzə(r)/', 'N', 'brauzer', 'браузер', 'a program for using the internet', 'Open the browser and type the address.', 'Brauzeri açyň we salgyny ýazyň.', 'A2', 'web browser'),
    ('crash', '/kræʃ/', 'V', 'işlemez bolmak', 'зависать, падать (о программе)', 'to stop working suddenly', 'My computer crashed twice today.', 'Kompýuterim şu gün iki gezek işlemez boldy.', 'A2'),
    ('gadget', '/ˈɡædʒɪt/', 'N', 'enjamjagaz (gajet)', 'гаджет', 'a small clever device', 'He loves the latest gadgets.', 'Iň täze gajetleri gowy görýär.', 'B1', 'electronic gadget'),
    ('glitch', '/ɡlɪtʃ/', 'N', 'kiçi näsazlyk', 'мелкий сбой', 'a small technical problem', 'A glitch delayed the update.', 'Kiçi näsazlyk täzelenmäni giçikdirdi.', 'B2'),
    ('network', '/ˈnetwɜːk/', 'N', 'tor', 'сеть', 'a system of connected computers', 'The network is down again.', 'Tor ýene işlemeýär.', 'A2', 'mobile network'),
    ('notification', '/ˌnəʊtɪfɪˈkeɪʃn/', 'N', 'habarnama', 'уведомление', 'a message telling you something', 'Turn off the notifications.', 'Habarnamalary öçür.', 'A2', 'push notification'),
    ('password', '/ˈpɑːswɜːd/', 'N', 'açarsöz', 'пароль', 'a secret word to enter a system', 'Never share your password.', 'Açarsözüňizi hiç wagt paýlaşmaň.', 'A1', 'change your password'),
    ('software', '/ˈsɒftweə(r)/', 'N', 'programma üpjünçiligi', 'программное обеспечение', 'programs that run on computers', 'The software needs an update.', 'Programma üpjünçiligi täzelenmeli.', 'A2', 'install software'),
    ('spam', '/spæm/', 'N', 'islenmeýän hatlar', 'спам', 'unwanted email messages', 'My inbox is full of spam.', 'Poçta gutym islenmeýän hatlardan doly.', 'A2', 'spam email'),
    ('update', '/ˈʌpdeɪt/', 'V', 'täzelemek', 'обновлять', 'to make software newer', 'Update the app before the trip.', 'Syýahatdan öň programmany täzeläň.', 'A2', 'software update'),
    ('virus', '/ˈvaɪrəs/', 'N', 'wirus', 'вирус (компьютерный)', 'a program that damages computers', 'A virus deleted all my files.', 'Wirus ähli faýllarymy pozdy.', 'A2', 'computer virus'),
]

# ---- Vocabulary Bank — Prefixes -> 7A ----
T['prefixes'] = [
    ('antisocial', '/ˌæntiˈsəʊʃl/', 'ADJ', 'jemgyýete garşy', 'антисоциальный', 'avoiding other people', 'Staying home every night seems antisocial.', 'Her agşam öýde galmak jemgyýete garşy görünýär.', 'B1'),
    ('co-founder', '/ˌkəʊ ˈfaʊndə(r)/', 'N', 'bilelikde esaslandyryjy', 'сооснователь', 'a person who starts a company with others', 'She is the co-founder of the app.', 'Programmanyň bilelikde esaslandyryjysy.', 'B2'),
    ('counter-attack', '/ˌkaʊntər əˈtæk/', 'N', 'jogap hüjümi', 'контратака', 'an attack in reply to another', 'The team scored on a counter-attack.', 'Topar jogap hüjüminde utuk gazandy.', 'B2'),
    ('devalue', '/ˌdiːˈvæljuː/', 'V', 'bahasyny gaçyrmak', 'обесценивать', 'to reduce the value of something', 'The currency was devalued.', 'Walýutanyň bahasy gaçyryldy.', 'B2'),
    ('extraordinary', '/ɪkˈstrɔːdnri/', 'ADJ', 'adatdan daşary', 'необычайный', 'very unusual and impressive', 'She has an extraordinary memory.', 'Adatdan daşary ýady bar.', 'A2'),
    ('forearm', '/ˈfɔːrɑːm/', 'N', 'baldyr (el)', 'предплечье', 'the part of the arm below the elbow', 'He tattooed his forearm.', 'Eliniň baldyryna nakgaş etdirdi.', 'B1'),
    ('international', '/ˌɪntəˈnæʃnəl/', 'ADJ', 'halkara', 'международный', 'involving several countries', 'The airport handles international flights.', 'Howa menzili halkara uçuşlary kabul edýär.', 'A2'),
    ('multimedia', '/ˌmʌltiˈmiːdiə/', 'N', 'multimedia', 'мультимедиа', 'using sound, video and text together', 'The lesson used multimedia tools.', 'Sapak multimedia gurallaryny ulandy.', 'B1'),
    ('nonstop', '/ˌnɒnˈstɒp/', 'ADV', 'tohtamanzyn (fasylasysyz)', 'безостановочно', 'without stopping', 'We flew nonstop to Ashgabat.', 'Aşgabada tohtamanzyn uçduk.', 'A2'),
    ('postgraduate', '/ˌpəʊstˈɡrædʒuət/', 'N', 'aspirant', 'аспирант', 'a student studying after a degree', 'She is a postgraduate in physics.', 'Fizika boýunça aspirant.', 'B2'),
    ('preview', '/ˈpriːvjuː/', 'N', 'öňünden görkezme', 'предварительный просмотр', 'an early look at something', 'We saw a preview of the film.', 'Filmiň öňünden görkezmesini gördük.', 'A2', 'sneak preview'),
    ('semicircle', '/ˈsemisɜːkl/', 'N', 'ýarym tegelek', 'полукруг', 'half of a circle', 'The chairs stood in a semicircle.', 'Stullar ýarym tegelek bolup durdy.', 'B1'),
    ('transfer', '/trænsˈfɜː(r)/', 'V', 'geçirmek', 'переводить, перемещать', 'to move from one place to another', 'He transferred to another department.', 'Başga bölüme geçdi.', 'A2', 'transfer money'),
    ('underwear', '/ˈʌndəweə(r)/', 'N', 'içki geýim', 'нижнее бельё', 'clothes worn under other clothes', 'Pack some clean underwear.', 'Arassa içki geýim ýygnap goý.', 'A2'),
    ('upgrade', '/ˈʌpɡreɪd/', 'V', 'gowulandyrmak (täzelemek)', 'модернизировать', 'to improve to a better version', 'They upgraded our hotel room.', 'Myhmanhana otagymyzy gowulandyrdylar.', 'A2', 'upgrade to'),
]

# ---- in-lesson 7B — art · colour idioms ----
T['art_colour'] = [
    ('artwork', '/ˈɑːtwɜːk/', 'N', 'sungat eseri', 'произведение искусства', 'a painting or drawing', 'The gallery displays modern artwork.', 'Galereýa häzirki zaman sungat eserlerini görkezýär.', 'A2'),
    ('canvas', '/ˈkænvəs/', 'N', 'kanwas', 'холст', 'cloth that paintings are done on', 'The artist painted on a huge canvas.', 'Suratkeş ägirt kanwasda surat çekdi.', 'B1'),
    ('contemporary', '/kənˈtemprəri/', 'ADJ', 'häzirki zaman', 'современный', 'belonging to the present time', 'She collects contemporary art.', 'Häzirki zaman sungatyny ýygnaýar.', 'B1', 'contemporary art'),
    ('exhibition', '/ˌeksɪˈbɪʃn/', 'N', 'sergi', 'выставка', 'a public show of art', 'The exhibition opens on Friday.', 'Sergi anna güni açylýar.', 'A2', 'visit an exhibition'),
    ('landscape', '/ˈlændskeɪp/', 'N', 'tebigat görnüşi', 'пейзаж', 'a picture of countryside', 'He painted a mountain landscape.', 'Dag görnüşini surat çekdi.', 'A2'),
    ('portrait', '/ˈpɔːtrət/', 'N', 'portret', 'портрет', 'a picture of a person', 'The portrait hangs in the hall.', 'Portret zalyň diwarynda asylgy.', 'A2', 'paint a portrait'),
    ('sculpture', '/ˈskʌlptʃə(r)/', 'N', 'heýkel', 'скульптура', 'a statue or carved art', 'The sculpture stands in the park.', 'Heýkel parkyň içinde dur.', 'A2'),
    ('sketch', '/sketʃ/', 'N', 'çyzgy (garalama)', 'набросок, эскиз', 'a quick simple drawing', 'She made a sketch of the old man.', 'Garry adamyň çyzgysyny etdi.', 'A2', 'make a sketch'),
    ('still life', '/ˌstɪl ˈlaɪf/', 'N', 'natýurmort', 'натюрморт', 'a painting of objects like fruit', 'The still life shows apples and grapes.', 'Natýurmortda alma we üzüm görkezilýär.', 'B1'),
    ('out of the blue', '/aʊt əv ðə bluː/', 'PHR', 'duýdansyz', 'как гром среди ясного неба', 'suddenly and unexpectedly', 'She called me out of the blue.', 'Duýdansyz maňa jaň etdi.', 'B1'),
    ('red tape', '/ˌred ˈteɪp/', 'N', 'kagyzbazlyk', 'бюрократия, волокита', 'too many official rules', 'Red tape delayed the project.', 'Kagyzbazlyk taslamany giçikdirdi.', 'B2'),
    ('white lie', '/ˌwaɪt ˈlaɪ/', 'N', 'ýumşak ýalan', 'невинная ложь', 'a small lie that does not hurt', 'It was just a white lie.', 'Diňe ýumşak ýalan boldy.', 'B1', 'tell a white lie'),
]

# ---- in-lesson 8A — health and medicine ----
T['health'] = [
    ('antibiotic', '/ˌæntibaɪˈɒtɪk/', 'N', 'antibiotik', 'антибиотик', 'medicine that kills bacteria', 'The doctor prescribed an antibiotic.', 'Lukman antibiotik ýazdy.', 'A2', 'take antibiotics'),
    ('check-up', '/ˈtʃek ʌp/', 'N', 'lukmançylyk barlagy', 'медосмотр', 'a general medical examination', 'I have a check-up next week.', 'Indiki hepde lukmançylyk barlagym bar.', 'A2', 'medical check-up'),
    ('cure', '/kjʊə(r)/', 'N', 'bejergi (emel)', 'лекарство, средство', 'a treatment that ends an illness', 'There is no cure yet.', 'Entek emel ýok.', 'A2', 'find a cure'),
    ('diagnosis', '/ˌdaɪəɡˈnəʊsɪs/', 'N', 'kesel anyklama', 'диагноз', "a doctor's judgement of an illness", 'The diagnosis was made quickly.', 'Diaгноз tiz goýuldy.', 'B1', 'make a diagnosis'),
    ('dose', '/dəʊs/', 'N', 'doza', 'доза', 'an amount of medicine', 'Take one dose every morning.', 'Her irden bir doza içiň.', 'A2', 'a dose of'),
    ('GP', '/ˌdʒiː ˈpiː/', 'N', 'maşgala lukmany', 'врач общей практики', 'a general practice doctor', 'Make an appointment with the GP.', 'Maşgala lukmanyna ýazylyň.', 'A2', 'go to the GP'),
    ('injection', '/ɪnˈdʒekʃn/', 'N', 'ukol (sanjym)', 'укол, инъекция', 'medicine given with a needle', 'The injection did not hurt.', 'Ukol agyrmady.', 'A2', 'give an injection'),
    ('operation', '/ˌɒpəˈreɪʃn/', 'N', 'operasiýa', 'операция', 'a medical procedure inside the body', 'She had an operation on her heart.', 'Ýüregine operasiýa etdirdi.', 'A2', 'have an operation'),
    ('remedy', '/ˈremədi/', 'N', 'emel (halk bejergisi)', 'средство (от болезни)', 'something that cures a problem', 'Honey is a good remedy for coughs.', 'Bal üsgülewüğe gowy emel.', 'B1', 'home remedy'),
    ('side effect', '/ˌsaɪd ɪˈfekt/', 'N', 'gapdal täsiri', 'побочный эффект', 'an unwanted effect of medicine', 'The pill has no side effects.', 'Dermanyň gapdal täsiri ýok.', 'A2'),
    ('surgeon', '/ˈsɜːdʒən/', 'N', 'hirurg', 'хирург', 'a doctor who does operations', 'The surgeon explained the risks.', 'Hirurg howplary düşündirdi.', 'A2'),
    ('treatment', '/ˈtriːtmənt/', 'N', 'bejergi', 'лечение', 'care given for an illness', 'The treatment worked well.', 'Bejergi gowy netije berdi.', 'A2', 'medical treatment'),
    ('vaccination', '/ˌvæksɪˈneɪʃn/', 'N', 'waksina (sanjym)', 'вакцинация', 'an injection that prevents disease', 'The vaccination protects children.', 'Waksina çagalary goraýar.', 'A2', 'get a vaccination'),
]

# ---- Vocabulary Bank — Travel and tourism -> 8B ----
T['travel_tourism'] = [
    ('accommodation', '/əˌkɒməˈdeɪʃn/', 'N', 'ýaşaýyş ýeri', 'жильё, размещение', 'a place to stay', 'The price includes accommodation.', 'Baha ýaşaýyş ýerini hem öz içine alýar.', 'A2', 'book accommodation'),
    ('attraction', '/əˈtrækʃn/', 'N', 'görmeli ýer', 'достопримечательность', 'a place tourists visit', 'The old city is the main attraction.', 'Köne şäher esasy görmeli ýer.', 'A2', 'tourist attraction'),
    ('backpacker', '/ˈbækpækə(r)/', 'N', 'ýeňil sumkaly syýahatçy', 'бэкпекер', 'a traveller with a big bag', 'Backpackers prefer cheap hostels.', 'Ýeňil sumkaly syýahatçylar arzan ýatakhanalary gowy görýär.', 'B1'),
    ('brochure', '/ˈbrəʊʃə(r)/', 'N', 'buklet', 'брошюра', 'a small book of travel information', 'The brochure lists all the hotels.', 'Buklet ähli myhmanhanalary sanlaýar.', 'A2', 'travel brochure'),
    ('destination', '/ˌdestɪˈneɪʃn/', 'N', 'barmaly ýer', 'пункт назначения', 'the place you travel to', 'Paris is a popular destination.', 'Parij meşhur barmaly ýer.', 'A2', 'tourist destination'),
    ('excursion', '/ɪkˈskɜːʃn/', 'N', 'ekskursiýa', 'экскурсия', 'a short organised trip', 'We went on a boat excursion.', 'Gaýyk ekskursiýasyna gitdik.', 'A2', 'go on an excursion'),
    ('itinerary', '/aɪˈtɪnərəri/', 'N', 'syýahat meýilnamasy', 'маршрут', 'a plan of a journey', 'The itinerary includes three cities.', 'Syýahat meýilnamasy üç şäheri öz içine alýar.', 'B1', 'plan an itinerary'),
    ('sightseeing', '/ˈsaɪtsiːɪŋ/', 'N', 'görmeli ýerleri görmek', 'осмотр достопримечательностей', 'visiting famous places', 'We spent the morning sightseeing.', 'Irdeniň dowamynda görmeli ýerleri gördük.', 'A2', 'go sightseeing'),
    ('tourist', '/ˈtʊərɪst/', 'N', 'turist', 'турист', 'a person visiting a place for pleasure', 'The old town is full of tourists.', 'Köne şäher turistlerden doly.', 'A1'),
    ('resort', '/rɪˈzɔːt/', 'N', 'dynç alyş ýeri', 'курорт', 'a place for holidays', 'Awaza is a seaside resort.', 'Awaza deňiz kenaryndaky dynç alyş ýeri.', 'A2', 'beach resort'),
    ('travel agent', '/ˈtrævl eɪdʒənt/', 'N', 'syýahat agenti', 'турагент', 'a person who arranges trips', 'The travel agent found us a deal.', 'Syýahat agenti bize arzan tapdy.', 'A2'),
    ('holidaymaker', '/ˈhɒlədeɪmeɪkə(r)/', 'N', 'dynç alyşçy', 'отпускник', 'a person on holiday', 'The beach was crowded with holidaymakers.', 'Kenar dynç alyşçylardan doly boldy.', 'B1'),
]

# ---- Vocabulary Bank — Animal matters -> 9A ----
T['animal_matters'] = [
    ('animal rights', '/ˌænɪml ˈraɪts/', 'N', 'haýwan hukuklary', 'права животных', 'the idea that animals deserve care', 'She campaigns for animal rights.', 'Haýwan hukuklary üçin kampaniýa alyp barýar.', 'B1'),
    ('cage', '/keɪdʒ/', 'N', 'gapas', 'клетка', 'a box with bars for animals', 'The parrot escaped from its cage.', 'Tötüji gapasdan gaçdy.', 'A2', 'in a cage'),
    ('cruelty', '/ˈkruːəlti/', 'N', 'rehimsizlik', 'жестокость', 'behaviour that causes suffering', 'Cruelty to animals is a crime.', 'Haýwanlara rehimsizlik jenaýat.', 'B1', 'animal cruelty'),
    ('extinction', '/ɪkˈstɪŋkʃn/', 'N', 'ýok bolmak (görnüşiň)', 'вымирание', 'when a species dies out', 'The tiger faces extinction.', 'Ýolbars ýok bolmak howpy astynda.', 'B1', 'face extinction'),
    ('fur', '/fɜː(r)/', 'N', 'ýüň (haýwanyň)', 'мех', 'the soft hair on animals', 'The cat has soft white fur.', 'Pişigiň ýumşak ak ýüňi bar.', 'A2'),
    ('habitat', '/ˈhæbɪtæt/', 'N', 'ýaşaýyş gurşawy', 'среда обитания', 'the natural home of an animal', 'Cutting trees destroys habitats.', 'Agaçlary çapmak ýaşaýyş gurşawyny weýran edýär.', 'B1', 'natural habitat'),
    ('hunt', '/hʌnt/', 'V', 'awlamak', 'охотиться', 'to chase animals to catch them', 'Lions hunt at night.', 'Ýolbarslar gije awlaýar.', 'A2'),
    ('poacher', '/ˈpəʊtʃə(r)/', 'N', 'bikanun awçy', 'браконьер', 'a person who hunts illegally', 'Poachers killed the rhino.', 'Bikanun awçylar karkidany öldürdi.', 'B1'),
    ('stray', '/streɪ/', 'ADJ', 'eýesiz (haýwan)', 'бездомный (о животном)', 'lost, with no home', 'A stray dog followed us home.', 'Eýesiz it yzymyzdan öýe geldi.', 'A2', 'stray cat'),
    ('wildlife', '/ˈwaɪldlaɪf/', 'N', 'ýabany tebigat', 'дикая природа', 'animals and plants in nature', 'The reserve protects wildlife.', 'Goraghana ýabany tebigaty goraýar.', 'A2', 'wildlife reserve'),
]

# ---- Vocabulary Bank — Preparing food -> 9B ----
T['preparing_food'] = [
    ('beat', '/biːt/', 'V', 'çalmak (ýumurtga)', 'взбивать', 'to mix quickly, like eggs', 'Beat the eggs with sugar.', 'Ýumurtgalary şeker bilen çal.', 'A2', 'beat the eggs'),
    ('dice', '/daɪs/', 'V', 'kubik dogramak', 'нарезать кубиками', 'to cut into small cubes', 'Dice the onions and carrots.', 'Sogany we käşiri kubik dogra.', 'B1'),
    ('grate', '/ɡreɪt/', 'V', 'gyrkmak (rende)', 'тереть на тёрке', 'to rub food into small pieces', 'Grate the cheese over the pasta.', 'Peýniri makaronyň üstüne gyrk.', 'B1', 'grate the cheese'),
    ('knead', '/niːd/', 'V', 'ýugurmak (hamyr)', 'месить (тесто)', 'to press dough with the hands', 'Knead the dough for ten minutes.', 'Hamry on minut ýugur.', 'B1'),
    ('melt', '/melt/', 'V', 'eremek', 'таять, топить', 'to become liquid with heat', 'Melt the butter in a pan.', 'Ýagy gazanda eredýiň.', 'A2', 'melt the butter'),
    ('peel', '/piːl/', 'V', 'gabygyny soýmak', 'чистить (кожуру)', 'to take the skin off fruit', 'Peel the potatoes first.', 'Ilki ýeralmanyň gabygyny sow.', 'A2', 'peel the potatoes'),
    ('saucepan', '/ˈsɔːspən/', 'N', 'gazanjagaz', 'кастрюля', 'a deep pan for cooking', 'Put the milk in a saucepan.', 'Süýdi gazanjagaza guý.', 'A2'),
    ('seasoning', '/ˈsiːznɪŋ/', 'N', 'tagam beriji', 'приправа', 'salt, pepper and herbs', 'Add seasoning to taste.', 'Tagamyna görä tagam beriji goşuň.', 'B1', 'add seasoning'),
    ('sieve', '/sɪv/', 'N', 'ele', 'сито', 'a tool with holes for separating', 'Sift the flour through a sieve.', 'Uny elekden geçir.', 'B2', 'through a sieve'),
    ('simmer', '/ˈsɪmə(r)/', 'V', 'haýal gaýnatmak', 'томить на медленном огне', 'to cook just below boiling', 'Simmer the soup for twenty minutes.', 'Çorbany ýigrimi minut haýal gaýnat.', 'B1'),
    ('whisk', '/wɪsk/', 'V', 'galtaşdyryp çalmak', 'взбивать венчиком', 'to beat with a special tool', 'Whisk the cream until thick.', 'Gaýmagy goýalýança galtaşdyryp çal.', 'B1'),
    ('marinade', '/ˈmærɪneɪd/', 'V', 'duzlama ýatyrmak', 'мариновать', 'to leave food in a flavoured liquid', 'Marinade the chicken for an hour.', 'Towugy bir sagat duzlamada ýatyryň.', 'B1'),
]

# ---- in-lesson 10A — word building ----
T['word_building2'] = [
    ('achievement', '/əˈtʃiːvmənt/', 'N', 'üstünlik (gazanylan)', 'достижение', 'something important you succeed in', 'Graduating was a great achievement.', 'Uniwersiteti gutarmak uly üstünlik boldy.', 'A2', 'great achievement'),
    ('agreement', '/əˈɡriːmənt/', 'N', 'ylalaşyk', 'соглашение', 'a decision people accept together', 'Both sides signed the agreement.', 'Iki tarap hem ylalaşyga gol çekdi.', 'A2', 'sign an agreement'),
    ('appointment', '/əˈpɔɪntmənt/', 'N', 'bellenen wagt (duşuşyk)', 'встреча, запись (на приём)', 'an arranged meeting', 'I have a dentist appointment at four.', 'Sagat dörtde diş lukmanyna ýazyldym.', 'A2', 'make an appointment'),
    ('arrangement', '/əˈreɪndʒmənt/', 'N', 'gurnama (meýilleşdirme)', 'договорённость', 'a plan made for something', 'We made arrangements for the trip.', 'Syýahat üçin gurnama etdik.', 'A2', 'make arrangements'),
    ('assessment', '/əˈsesmənt/', 'N', 'bahalandyryş', 'оценка, аттестация', 'a judgement of quality', 'The assessment takes one hour.', 'Bahalandyryş bir sagat alýar.', 'B1', 'assessment test'),
    ('commitment', '/kəˈmɪtmənt/', 'N', 'ygrarlylyk', 'преданность, обязательство', 'a promise to work hard at something', 'The job needs real commitment.', 'Iş hakyky ygrarlylyk talap edýär.', 'B1', 'make a commitment'),
    ('development', '/dɪˈveləpmənt/', 'N', 'ösüş', 'развитие', 'the process of growing', 'The city saw rapid development.', 'Şäher çalt ösüş gördi.', 'A2', 'economic development'),
    ('employment', '/ɪmˈplɔɪmənt/', 'N', 'iş bilen üpjünçilik', 'занятость', 'having a paid job', 'Employment rose in the spring.', 'Ýazda iş bilen üpjünçilik artdy.', 'B1', 'full employment'),
    ('entertainment', '/ˌentəˈteɪnmənt/', 'N', 'güýme', 'развлечение', 'things that amuse people', 'The city offers great entertainment.', 'Şäher ajaýyp güýme hödürleýär.', 'A2', 'live entertainment'),
    ('equipment', '/ɪˈkwɪpmənt/', 'N', 'enjam', 'оборудование', 'the things needed for an activity', 'The camping equipment is new.', 'Kemping enjamy täze.', 'A2', 'sports equipment'),
    ('failure', '/ˈfeɪljə(r)/', 'N', 'şowsuzlyk', 'неудача, провал', 'not succeeding', 'Failure taught him a lot.', 'Şowsuzlyk oňa köp zat övretdi.', 'A2', 'fear of failure'),
    ('payment', '/ˈpeɪmənt/', 'N', 'töleg', 'платёж', 'the act of paying', 'Payment is due at the end of the month.', 'Töleg aýyň ahyrynda edilmeli.', 'A2', 'make a payment'),
    ('performance', '/pəˈfɔːməns/', 'N', 'çykyş (tomaşa)', 'выступление, представление', 'a show or act', 'Her performance was brilliant.', 'Çykyşy ajaýyp boldy.', 'A2', 'live performance'),
    ('replacement', '/rɪˈpleɪsmənt/', 'N', 'çalşylma (çalyşma)', 'замена', 'a person or thing that replaces another', 'We need a replacement for the old printer.', 'Köne printere çalşylma gerek.', 'B1', 'replacement parts'),
]

# ---- in-lesson 10B — words often confused ----
T['confused_words'] = [
    ('advice', '/ədˈvaɪs/', 'N', 'maslahat', 'совет (существительное)', 'an opinion about what to do', 'She gave me good advice.', 'Gowy maslahat berdi.', 'A2', 'a piece of advice'),
    ('advise', '/ədˈvaɪz/', 'V', 'maslahat bermek', 'советовать', 'to give an opinion about what to do', 'I advise you to see a doctor.', 'Lukmana görünmegi maslahat berýärin.', 'A2', 'advise someone to do'),
    ('beside', '/bɪˈsaɪd/', 'PREP', 'ýanynda', 'рядом с', 'next to something', 'The bag is beside the door.', 'Sumka gapynyň ýanynda.', 'A2'),
    ('besides', '/bɪˈsaɪdz/', 'ADV', 'mundan başga-da', 'кроме того', 'in addition', 'Besides, it was too late.', 'Mundan başga-da, gaty giçdi.', 'A2'),
    ('compliment', '/ˈkɒmplɪmənt/', 'N', 'taryp', 'комплимент', 'words that praise someone', 'He paid her a nice compliment.', 'Oňa owadan taryp aýtdy.', 'A2', 'pay a compliment'),
    ('complement', '/ˈkɒmplɪment/', 'V', 'üstüni ýetirmek', 'дополнять', 'to go well with something', 'The sauce complements the fish.', 'Sous balygyň üstüni ýetirýär.', 'B2'),
    ('economic', '/ˌiːkəˈnɒmɪk/', 'ADJ', 'ykdysady', 'экономический', 'about the economy', 'The country faces economic problems.', 'Ýurt ykdysady kynçylyklar bilen ýüzbe-ýüz.', 'A2', 'economic growth'),
    ('historic', '/hɪˈstɒrɪk/', 'ADJ', 'taryhy (möhüm)', 'исторический (знаменательный)', 'famous in history', 'It was a historic victory.', 'Taryhy ýeňiş boldy.', 'B1', 'historic event'),
    ('historical', '/hɪˈstɒrɪkl/', 'ADJ', 'taryhy (taryha degişli)', 'исторический (связанный с историей)', 'about the past', 'She loves historical novels.', 'Taryhy romanlary gowy görýär.', 'B1', 'historical novel'),
    ('job', '/dʒɒb/', 'N', 'iş (bir wezipe)', 'работа (конкретная)', 'a particular piece of work', 'He found a new job in May.', 'Maý aýynda täze iş tapdy.', 'A1'),
    ('shade', '/ʃeɪd/', 'N', 'kölege (ýagtylykdan)', 'тень (от солнца)', 'a place protected from sun', 'We sat in the shade of the tree.', 'Agaçyň kölegesinde oturduk.', 'A2', 'in the shade'),
    ('shadow', '/ˈʃædəʊ/', 'N', 'saýa', 'тень (силуэт)', 'a dark shape made by light', 'His shadow stretched across the wall.', 'Saýasy diwara düşdi.', 'A2', 'cast a shadow'),
    ('travel', '/ˈtrævl/', 'N', 'syýahat', 'путешествие (вообще)', 'the activity of travelling', 'Air travel is cheaper now.', 'Howa syýahaty indi arzan.', 'A1', 'air travel'),
    ('trip', '/trɪp/', 'N', 'sapar (gysga)', 'поездка (конкретная)', 'a short journey somewhere', 'We had a lovely trip to the mountains.', 'Daglara ajaýyp sapar etdik.', 'A1', 'day trip'),
    ('price', '/praɪs/', 'N', 'baha (satuwda)', 'цена', 'the amount something costs', 'The price includes breakfast.', 'Baha ertirligi hem öz içine alýar.', 'A1', 'ticket price'),
    ('prize', '/praɪz/', 'N', 'baýrak', 'приз, премия', 'something won in a competition', 'She won first prize.', 'Birinji baýragy gazandy.', 'A2', 'win a prize'),
]

# ---- Colloquial English episodes ----
T['ce_work_family'] = [
    ('How do you manage?', '/haʊ du ju ˈmænɪdʒ/', 'PHR', 'Nädip hötdeleýärsiň?', 'Как вы справляетесь?', 'used to ask how someone copes', 'How do you manage with two jobs?', 'Iki işi nädip hötdeleýärsiň?', 'A2'),
    ('work-life balance', '/ˌwɜːk laɪf ˈbæləns/', 'N', 'iş-öý deňagramlylygy', 'баланс работы и жизни', 'an equal mix of work and home life', 'Good work-life balance keeps you healthy.', 'Gowy iş-öý deňagramlylygy sagdyn saklaýar.', 'B1'),
    ('I work from home.', '/aɪ wɜːk frɒm həʊm/', 'PHR', 'Öýden işleýärin.', 'Я работаю из дома.', 'used to say where you work', 'I work from home twice a week.', 'Hepdede iki gezek öýden işleýärin.', 'A2'),
    ('It runs in the family.', '/ɪt rʌnz ɪn ðə ˈfæməli/', 'PHR', 'Maşgalada bar.', 'Это семейное (передаётся по наследству).', 'used when a trait is inherited', 'Musical talent — it runs in the family.', 'Saz zehini — maşgalada bar.', 'B1'),
    ('family business', '/ˈfæməli ˈbɪznəs/', 'N', 'maşgala kärhanasy', 'семейный бизнес', 'a company owned by a family', 'They run a small family business.', 'Kiçi maşgala kärhanasyny dolandyrýarlar.', 'A2'),
    ('the breadwinner', '/ðə ˈbredwɪnə(r)/', 'N', 'maşgala ekleýji', 'кормилец', 'the person who earns for a family', 'She is the main breadwinner.', 'Maşgalanyň esasy ekleýjisi ol.', 'B2'),
    ('work long hours', '/wɜːk lɒŋ ˈaʊəz/', 'PHR', 'uzak sagat işlemek', 'работать подолгу', 'to work a lot', 'Doctors often work long hours.', 'Lukmanlar köplenç uzak sagat işleýär.', 'A2'),
    ('quality time', '/ˈkwɒləti taɪm/', 'N', 'hil wagty (maşgala bilen)', 'качественное время (с близкими)', 'time spent giving full attention', 'Spend quality time with your children.', 'Çagalaryňyz bilen hil wagtyny geçiriň.', 'A2'),
]

T['ce_history'] = [
    ('date back to', '/deɪt bæk tuː/', 'PHR', 'şol döwürden galan', 'относиться к (о времени)', 'used to say how old something is', 'The castle dates back to the twelfth century.', 'Gala on ikinji asyrdan galan.', 'A2'),
    ('steeped in history', '/stiːpt ɪn ˈhɪstri/', 'PHR', 'taryha baý', 'насыщенный историей', 'used for very historic places', 'The old city is steeped in history.', 'Köne şäher taryha baý.', 'B2'),
    ('ancient ruins', '/ˈeɪnʃnt ˈruːɪnz/', 'N', 'gadymy harabalar', 'древние руины', 'old buildings that have fallen', 'We explored the ancient ruins.', 'Gadymy harabalary öwrendik.', 'A2'),
    ('a turning point', '/ə ˈtɜːnɪŋ pɔɪnt/', 'N', 'öwrülişik nokady', 'поворотный момент', 'a moment that changes everything', 'The battle was a turning point.', 'Söweş öwrülişik nokady boldy.', 'B1'),
    ('go down in history', '/ɡəʊ daʊn ɪn ˈhɪstri/', 'PHR', 'taryha girmek', 'войти в историю', 'to be remembered for ever', 'She went down in history as a pioneer.', 'Öňdebaryjy hökmünde taryha girdi.', 'A2'),
    ('back in the day', '/bæk ɪn ðə deɪ/', 'PHR', 'köne döwürlerde', 'в былые времена', 'used about the past', 'Back in the day, there was no internet.', 'Köne döwürlerde internet ýokdy.', 'A2'),
    ('living history', '/ˈlɪvɪŋ ˈhɪstri/', 'N', 'ýaşaýan taryh', 'живая история', 'old traditions still alive today', 'The market is living history.', 'Bazar ýaşaýan taryh.', 'B1'),
    ('pass into legend', '/pɑːs ˈɪntə ˈledʒənd/', 'PHR', 'rowaýata öwrülmek', 'войти в легенды', 'to become famous in stories', 'The hero passed into legend.', 'Gahryman rowaýata öwrüldi.', 'B2'),
]

T['ce_stress'] = [
    ('I\'m stressed out.', '/aɪm ˌstrest ˈaʊt/', 'PHR', 'Dartgynly ýagdaýda.', 'Я в стрессе.', 'used to say you feel too much pressure', 'I am stressed out before exams.', 'Synagdan öň dartgynly ýagdaýda bolýaryn.', 'A2'),
    ('wind down', '/waɪnd daʊn/', 'PHR', 'köşeşmek (dynç almak)', 'расслабляться (постепенно)', 'to relax after activity', 'I wind down with a book.', 'Kitap bilen köşeşýärin.', 'B1'),
    ('recharge my batteries', '/ˌriːˈtʃɑːdʒ maɪ ˈbætriz/', 'PHR', 'güýjümi dikeltmek', 'подзарядиться', 'to get energy back', 'A weekend at the lake recharges my batteries.', 'Köl kenaryndaky hepde ahyry güýjümi dikeldýär.', 'A2'),
    ('helps me unwind', '/helps miː ˌʌnˈwaɪnd/', 'PHR', 'maňa köşeşmäge kömek edýär', 'помогает мне расслабиться', 'used to say what relaxes you', 'Walking helps me unwind.', 'Ýöremek maňa köşeşmäge kömek edýär.', 'A2'),
    ('burnout', '/ˈbɜːnaʊt/', 'N', 'ýadawlyk (işden)', 'выгорание', 'exhaustion from working too hard', 'He had to stop working to avoid burnout.', 'Ýadawlykdan gaça durmak üçin işi bes etmeli boldy.', 'B2'),
    ('chill out', '/tʃɪl aʊt/', 'PHR', 'dynç almak (gowşurmak)', 'расслабиться, отдохнуть', 'to relax completely', 'Let us chill out by the pool.', 'Geliň, howzuň ýanynda dynç alalyň.', 'A2'),
    ('at breaking point', '/ət ˈbreɪkɪŋ pɔɪnt/', 'PHR', 'çydap bilmeýän ýagdaýda', 'на грани срыва', 'almost unable to cope', 'She was at breaking point after the exams.', 'Synaglardan soň çydap bilmeýän ýagdaýda boldy.', 'B2'),
    ('let off steam', '/let ɒf stiːm/', 'PHR', 'gaharyny çykarmak', 'выпустить пар', 'to get rid of strong feelings', 'He runs to let off steam.', 'Gaharyny çykarmak üçin ylgaw edýär.', 'B1'),
]

T['ce_illustration'] = [
    ('beautifully illustrated', '/ˈbjuːtɪfli ˈɪləstreɪtɪd/', 'ADJ', 'owadan suratlandyrylan', 'красочно иллюстрированный', 'with lovely pictures', 'It is a beautifully illustrated book.', 'Owadan suratlandyrylan kitap.', 'A2'),
    ('bring it to life', '/brɪŋ ɪt tuː laɪf/', 'PHR', 'jana getirýär', 'оживляет', 'used when pictures make a story vivid', 'The drawings bring the story to life.', 'Çyzgylar hekaýany jana getirýär.', 'A2'),
    ('graphic novel', '/ˈɡræfɪk ˈnɒvl/', 'N', 'komiks roman', 'графический роман', 'a novel told in pictures', 'He reads graphic novels.', 'Komiks romanlary okaýar.', 'B1'),
    ('eye-catching', '/ˈaɪ kætʃɪŋ/', 'ADJ', 'göze ilýän', 'бросающийся в глаза', 'immediately noticed', 'The poster is very eye-catching.', 'Plakat gaty göze ilýän.', 'B1'),
    ('the visuals', '/ðə ˈvɪʒuəlz/', 'N', 'wizual taraplary', 'визуальный ряд', 'the images in a film or book', 'The visuals are stunning.', 'Wizual taraplary haýran galdyryjy.', 'B2'),
    ('The cover draws you in.', '/ðə ˈkʌvə(r) drɔːz juː ɪn/', 'PHR', 'Muqawasy özüne çekýär.', 'Обложка притягивает.', 'used to praise a book cover', 'The cover draws you in immediately.', 'Muqawasy dessine özüne çekýär.', 'A2'),
    ('caption', '/ˈkæpʃn/', 'N', 'surat ýazgysy', 'подпись (к рисунку)', 'words under a picture', 'Read the caption below the photo.', 'Suratyň aşagyndaky ýazgyny oka.', 'B1', 'photo caption'),
    ('full-page spread', '/ˌfʊl peɪdʒ ˈspred/', 'N', 'tutuş sahypa ýaýran', 'разворот на всю страницу', 'a picture across a whole page', 'The map is a full-page spread.', 'Karta tutuş sahypa ýaýran.', 'B2'),
]

T['ce_insects'] = [
    ('give me the creeps', '/ɡɪv miː ðə kriːps/', 'PHR', 'tenim ürkýär', 'меня пробирает дрожь', 'used to say something scares you', 'Spiders give me the creeps.', 'Mör-möjekler tenimi ürküzýär.', 'A2'),
    ('bee sting', '/ˈbiː stɪŋ/', 'N', 'ary çakmasy', 'укус пчелы', 'a wound from a bee', 'A bee sting can hurt a lot.', 'Ary çakmasy gaty agyryp biler.', 'A2'),
    ('insect bite', '/ˈɪnsekt baɪt/', 'N', 'möjek çakmasy', 'укус насекомого', 'a mark from an insect', 'Put cream on the insect bite.', 'Möjek çakmasyna krem çal.', 'A2'),
    ('creepy-crawly', '/ˈkriːpi krɔːli/', 'N', 'ýyldyryjy mör-möjek', 'букашка (разг.)', 'an insect or spider (informal)', 'There is a creepy-crawly on the wall!', 'Diwarda ýyldyryjy mör-möjek bar!', 'A2'),
    ('harmless', '/ˈhɑːmləs/', 'ADJ', 'zyýansyz', 'безвредный', 'causing no harm', 'The spider is completely harmless.', 'Mör-möjek düýbünden zyýansyz.', 'A2'),
    ('leave it alone', '/liːv ɪt əˈləʊn/', 'PHR', 'Ona degme.', 'Не трогай его.', 'used to say do not disturb', 'That beetle is harmless — leave it alone.', 'Şol tomzak zyýansyz — ona degme.', 'A2'),
    ('spider web', '/ˈspaɪdə(r) web/', 'N', 'möjek tory', 'паутина', 'the net a spider spins', 'A spider web covered the corner.', 'Möjek tory burçy örtüpdi.', 'A2'),
    ('swarm', '/swɔːm/', 'N', 'topar (mör-möjek)', 'рой', 'a large moving group of insects', 'A swarm of bees flew past.', 'Ary topary uçup geçdi.', 'B1', 'a swarm of bees'),
]
LESSONS = {
    '1A': (1,  'We are family', 'personality', ['personality']),
    '1B': (1,  'A job for life?', 'work', ['work2']),
    '2A': (2,  'Do you remember...?', 'word building: abstract nouns', ['abstract_nouns']),
    '2B': (2,  'On the tip of my tongue', 'lexical areas: relationships', ['relationships']),
    '3A': (3,  'A love-hate relationship', 'phrases with get', ['get_phrases']),
    '3B': (3,  'Dramatic licence', 'conflict and warfare', ['conflict']),
    '4A': (4,  'An open book', 'describing books and films', ['books_films']),
    '4B': (4,  'The sound of silence', 'sounds and the human voice', ['voice']),
    '5A': (5,  'No time for anything', 'expressions with time', ['time_expr']),
    '5B': (5,  'Not for profit?', 'money', ['money2']),
    '6A': (6,  'Help, I need somebody!', 'compound adjectives', ['compound_adjs2']),
    '6B': (6,  "Can't give it up", 'phones and technology', ['phones_tech']),
    '7A': (7,  'As a matter of fact...', 'word formation: prefixes', ['prefixes']),
    '7B': (7,  'A masterpiece?', 'art · colour idioms', ['art_colour']),
    '8A': (8,  'The best medicine?', 'health and medicine', ['health']),
    '8B': (8,  "A 'must-see' attraction", 'travel and tourism', ['travel_tourism']),
    '9A': (9,  'Pet hates', 'animal matters', ['animal_matters']),
    '9B': (9,  'How to cook, how to eat', 'preparing food', ['preparing_food']),
    '10A': (10, 'On your marks, set, go!', 'word building: adjectives, nouns, and verbs', ['word_building2']),
    '10B': (10, 'No direction home', 'words that are often confused', ['confused_words']),
}

WORD_LESSON = {}


def lesson_for(topic, en, fallback):
    key = en.strip().lower()
    return WORD_LESSON.get(key, fallback)


# Advanced has ten units; the five Colloquial English episodes sit after
# units 1, 3, 5, 7 and 9 in the book. In the data they carry unit 11 so they
# do not collide with the real units, and the app shows each episode right
# after the unit it follows.
PE_UNIT = 11
for code, n, title, topic, key in (
    ('CE1', 11, 'Talking about work and family', 'colloquial English 1', 'ce_work_family'),
    ('CE2', 11, 'Talking about history', 'colloquial English 2 and 3', 'ce_history'),
    ('CE3', 11, 'Talking about stress and relaxation', 'colloquial English 4 and 5', 'ce_stress'),
    ('CE4', 11, 'Talking about illustration', 'colloquial English 6 and 7', 'ce_illustration'),
    ('CE5', 11, 'Talking about insects and animals', 'colloquial English 8 and 9', 'ce_insects'),
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
                    'books': [{'book': 'adv', 'unit': unit, 'lesson': lesson}],
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
        'book': 'adv',
        'title': 'English File Advanced (4th edition) — vocabulary, by lesson',
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
