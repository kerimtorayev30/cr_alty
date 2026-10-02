#!/usr/bin/env python3
"""Fill Elementary's remaining lessons and add the Practical English unit.

The owner is right on both counts, and the book backs it up:

  * Every Elementary unit has an A, a B and a C lesson. I had left 11 lessons
    out because their words are not in the Vocabulary Bank — but each of those
    lessons has its own "VOCABULARY" box on the lesson page, and that is where
    the words come from:
      2C feelings (p.18) · 5A noise (p.38) · 5C clothes (p.42)
      6A words in a story (p.46) · 7A the murder-mystery story (p.62)
      8B food containers (p.72) · 8C high numbers (p.74)
      9B city holidays (p.80) · 9C verb phrases (p.82)
      10B verbs + infinitive (p.88) · 11A irregular past participles (p.96)
    11B keeps no list of its own; the book revises travel there.

  * Practical English is six episodes with their own words, so it becomes its
    own unit (13) with lessons PE1-PE6:
      PE1 Arriving in London / in a hotel (p.12)
      PE2 Coffee to take away / buying a coffee (p.28)
      PE3 In a clothes shop (p.44)
      PE4 Getting lost / asking the way (p.60)
      PE5 At a restaurant / understanding a menu (p.76)
      PE6 Going home / getting to the airport (p.92)

Where the book only lists headwords (a picture-match box), the Turkish, Russian,
definition and example are mine and stay proofread:false.
"""
import sys

GEN = 'content/tools/gen_elementary.py'
s = open(GEN, encoding='utf-8').read()

TOPICS = '''
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
    ('noisy', '/ˈnɔɪzi/', 'ADJ', 'galmagally', 'шумный', 'making a lot of noise', 'a noisy street', 'galmagally köçe', 'A2'),
    ('quiet', '/ˈkwaɪət/', 'ADJ', 'asuda, sessiz', 'тихий', 'making little or no noise', 'a quiet village', 'asuda oba', 'A2'),
    ('upstairs', '/ˌʌpˈsteəz/', 'ADV', 'ýokarky gatda', 'наверху', 'on a higher floor', 'The neighbours upstairs are noisy.', 'Ýokarky goňşular galmagally.', 'A2'),
    ('downstairs', '/ˌdaʊnˈsteəz/', 'ADV', 'aşaky gatda', 'внизу', 'on a lower floor', 'She went downstairs.', 'Aşaky gata düşdi.', 'A2'),
    ('next door', '/ˌnekst ˈdɔː/', 'ADV', 'gapdaldaky öýde', 'по соседству', 'in the building beside yours', 'The people next door have a dog.', 'Gapdaldaky goňşynyň iti bar.', 'A2'),
    ('neighbour', '/ˈneɪbə/', 'N', 'goňşy', 'сосед', 'a person who lives near you', 'Our neighbour is friendly.', 'Goňşumyz mähirli.', 'A2'),
    ('shout', '/ʃaʊt/', 'V', 'gygyrmak', 'кричать', 'to speak very loudly', "Don't shout at me.", 'Maňa gygyrma.', 'A2', 'shout at'),
    ('fight', '/faɪt/', 'V', 'dawa etmek', 'ссориться', 'to argue angrily', 'They fight every day.', 'Her gün dawa edýärler.', 'A2'),
    ('play music', '/pleɪ ˈmjuːzɪk/', 'PHR', 'saz çalmak', 'играть музыку', 'to make music', 'They play music late at night.', 'Gije saz çalýarlar.', 'A1'),
]

T['clothes'] = [
    ('jacket', '/ˈdʒækɪt/', 'N', 'kurtka', 'куртка', 'a short coat', 'a leather jacket', 'deri kurtka', 'A1', 'wear a jacket'),
    ('jeans', '/dʒiːnz/', 'N', 'jinsi', 'джинсы', 'trousers made of denim', 'blue jeans', 'gök jinsi', 'A1', 'wear jeans'),
    ('shirt', '/ʃɜːt/', 'N', 'köýnek', 'рубашка', 'a piece of clothing for the top of the body', 'a white shirt', 'ak köýnek', 'A1'),
    ('skirt', '/skɜːt/', 'N', 'ýubka', 'юбка', 'a piece of clothing worn by women from the waist down', 'a long skirt', 'uzyn ýubka', 'A1'),
    ('sweater', '/ˈswetə/', 'N', 'switer', 'свитер', 'a warm piece of clothing for the top of the body', 'a wool sweater', 'ýüň switer', 'A1'),
    ('T-shirt', '/ˈtiːʃɜːt/', 'N', 'futbolka', 'футболка', 'a light shirt with short sleeves', 'a plain T-shirt', 'ýönekeý futbolka', 'A1'),
    ('trousers', '/ˈtraʊzəz/', 'N', 'balak', 'брюки', 'a piece of clothing covering the legs', 'black trousers', 'gara balak', 'A1'),
    ('shoes', '/ʃuːz/', 'N', 'aýakgap', 'туфли', 'things you wear on your feet', 'new shoes', 'täze aýakgap', 'A1', 'wear shoes'),
    ('coat', '/kəʊt/', 'N', 'palto', 'пальто', 'a long outer piece of clothing', 'a warm coat', 'yssy palto', 'A1'),
    ('dress', '/dres/', 'N', 'köýnek (aýal)', 'платье', 'a piece of clothing for women that covers the body and legs', 'a summer dress', 'tomus köýnegi', 'A1'),
    ('size', '/saɪz/', 'N', 'ölçeg', 'размер', 'how big or small something is', 'What size are you?', 'Ölçegiňiz näçe?', 'A2', 'in size'),
    ('try on', '/traɪ ɒn/', 'PHR', 'synap görmek', 'примерить', 'to put on clothes to see if they fit', 'Can I try it on?', 'Synap görüp bilerinmi?', 'A2'),
]

T['story'] = [
    ('decide', '/dɪˈsaɪd/', 'V', 'karar bermek', 'решать', 'to choose after thinking', 'She decided to leave.', 'Gitmäge karar berdi.', 'A2', 'decide to'),
    ('strange', '/streɪndʒ/', 'ADJ', 'geň', 'странный', 'unusual and surprising', 'a strange noise', 'geň ses', 'A2'),
    ('surprised', '/səˈpraɪzd/', 'ADJ', 'geň galan', 'удивлённый', 'feeling that something is unexpected', 'He was surprised to see her.', 'Ony görüp geň galdy.', 'A2', 'surprised to'),
    ('valuable', '/ˈvæljuəbl/', 'ADJ', 'gymmat bahaly', 'ценный', 'worth a lot of money', 'a valuable ring', 'gymmat bahaly ýüzük', 'B1'),
    ('desert', '/ˈdezət/', 'N', 'çöl', 'пустыня', 'a dry area of land with little water', 'They crossed the desert.', 'Çölden geçdiler.', 'A2'),
    ('mountain', '/ˈmaʊntən/', 'N', 'dag', 'гора', 'a very high hill', 'a high mountain', 'beýik dag', 'A2'),
    ('palace', '/ˈpæləs/', 'N', 'köşk', 'дворец', 'the home of a king or queen', 'a royal palace', 'şalyk köşgi', 'B1'),
    ('village', '/ˈvɪlɪdʒ/', 'N', 'oba', 'деревня', 'a very small town in the countryside', 'a quiet village', 'asuda oba', 'A2'),
    ('inside', '/ˌɪnˈsaɪd/', 'PREP', 'içinde', 'внутри', 'within something', 'inside the house', 'öýüň içinde', 'A2'),
    ('towards', '/təˈwɔːdz/', 'PREP', 'tarap', 'к, в направлении', 'in the direction of', 'She walked towards the door.', 'Gapa tarap ýöredi.', 'B1'),
    ('sell', '/sel/', 'V', 'satmak', 'продавать', 'to give something for money', 'They sell fruit here.', 'Bu ýerde miwe satýarlar.', 'A2'),
    ('comfortable', '/ˈkʌmftəbl/', 'ADJ', 'amatly', 'удобный', 'pleasant to use or wear', 'a comfortable bed', 'amatly düşek', 'A2'),
]

T['crime'] = [
    ('inspector', '/ɪnˈspektə/', 'N', 'inspektor', 'инспектор', 'a police officer of high rank', 'Inspector Granger arrived.', 'Inspektor Greýnjer geldi.', 'B1'),
    ('murder', '/ˈmɜːdə/', 'N', 'adam öldürmek', 'убийство', 'the crime of killing someone', 'a murder mystery', 'adam öldürme syry', 'B1'),
    ('kill', '/kɪl/', 'V', 'öldürmek', 'убивать', 'to make someone die', 'Somebody killed him.', 'Ony birisi öldürdi.', 'A2'),
    ('dead', '/ded/', 'ADJ', 'öli', 'мёртвый', 'no longer alive', 'He was dead.', 'Ol ölüdi.', 'A2'),
    ('die', '/daɪ/', 'V', 'ölmek', 'умирать', 'to stop living', 'He died in 1965.', '1965-nji ýylda aradan çykdy.', 'A2'),
    ('asleep', '/əˈsliːp/', 'ADJ', 'ukuda', 'спящий', 'sleeping', 'Was he asleep?', 'Ukudymy?', 'A2', 'fall asleep'),
    ('midnight', '/ˈmɪdnaɪt/', 'N', 'gije ýary', 'полночь', 'twelve o\\'clock at night', 'He died at midnight.', 'Gije ýary aradan çykdy.', 'A2', 'at midnight'),
    ('moustache', '/məˈstɑːʃ/', 'N', 'murt', 'усы', 'hair above a man\\'s mouth', 'a big moustache', 'uly murt', 'B1'),
    ('library', '/ˈlaɪbrəri/', 'N', 'kitaphana', 'библиотека', 'a room or building with books', 'They talked in the library.', 'Kitaphanada gürleşdiler.', 'A2', 'in the library'),
    ('hear', '/hɪə/', 'V', 'eşitmek', 'слышать', 'to know a sound with your ears', 'Did you hear anything?', 'Bir zat eşitdiňmi?', 'A1'),
    ('suddenly', '/ˈsʌdənli/', 'ADV', 'birden', 'вдруг', 'quickly and without warning', 'Suddenly the door opened.', 'Birden gapy açyldy.', 'A2'),
    ('secret', '/ˈsiːkrət/', 'N', 'sir', 'секрет', 'something you do not tell people', 'Tell me a secret.', 'Maňa bir sir aýt.', 'A2', 'tell a secret'),
]

T['containers'] = [
    ('bottle', '/ˈbɒtl/', 'N', 'çüýşe', 'бутылка', 'a container with a narrow neck for liquids', 'a bottle of water', 'bir çüýşe suw', 'A1', 'a bottle of'),
    ('box', '/bɒks/', 'N', 'guty', 'коробка', 'a container with flat sides', 'a box of chocolates', 'bir guty şokolad', 'A1', 'a box of'),
    ('can', '/kæn/', 'N', 'banka', 'банка', 'a metal container for food or drink', 'a can of Coke', 'bir banka koka-kola', 'A2', 'a can of'),
    ('carton', '/ˈkɑːtn/', 'N', 'kagyz gap', 'пакет, картонная упаковка', 'a light container for drinks', 'a carton of juice', 'bir gap şire', 'B1', 'a carton of'),
    ('jar', '/dʒɑː/', 'N', 'banka (aýna)', 'банка (стеклянная)', 'a glass container with a lid', 'a jar of jam', 'bir banka mürebbä', 'A2', 'a jar of'),
    ('packet', '/ˈpækɪt/', 'N', 'bukja', 'пачка', 'a small paper or plastic container', 'a packet of crisps', 'bir bukja çips', 'A2', 'a packet of'),
    ('tin', '/tɪn/', 'N', 'konserw bankasy', 'жестяная банка', 'a metal container for food', 'a tin of tomatoes', 'bir banka pomidor', 'B1', 'a tin of'),
    ('some', '/sʌm/', 'DET', 'biraz', 'немного', 'an amount of something', 'I need some milk.', 'Biraz süýt gerek.', 'A1', 'some milk'),
    ('any', '/ˈeni/', 'DET', 'hiç, islendik', 'какой-нибудь', 'used in questions and negatives', "We don't have any bread.", 'Çöregimiz ýok.', 'A1', 'any bread'),
    ('much', '/mʌtʃ/', 'DET', 'köp', 'много', 'a large amount', 'How much sugar do you want?', 'Näçe şeker isleýärsiň?', 'A1', 'how much'),
    ('many', '/ˈmeni/', 'DET', 'köp (sanalýan)', 'много (исчисляемое)', 'a large number', 'How many eggs do we need?', 'Näçe ýumurtga gerek?', 'A1', 'how many'),
    ('a lot of', '/ə lɒt əv/', 'DET', 'köp', 'много', 'a large amount or number', 'a lot of friends', 'köp dost', 'A1'),
    ('a few', '/ə fjuː/', 'DET', 'birnäçe', 'несколько', 'a small number', 'a few minutes', 'birnäçe minut', 'A1'),
    ('a little', '/ə ˈlɪtl/', 'DET', 'biraz', 'немного', 'a small amount', 'a little sugar', 'biraz şeker', 'A1'),
]

T['high_numbers'] = [
    ('population', '/ˌpɒpjuˈleɪʃn/', 'N', 'ilaty', 'население', 'all the people living in a place', 'The population is 67 million.', 'Ilaty 67 million.', 'A2'),
    ('kilometre', '/ˈkɪləmiːtə/', 'N', 'kilometr', 'километр', 'a unit of length equal to 1,000 metres', 'It is 2,500 km away.', '2500 km uzaklykda.', 'A2'),
    ('metre', '/ˈmiːtə/', 'N', 'metr', 'метр', 'a unit of length equal to 100 centimetres', 'The wall is two metres high.', 'Diwar iki metr beýiklikde.', 'A2'),
    ('percent', '/pəˈsent/', 'ADV', 'göterim', 'процент', 'one part in every hundred', 'Fifty percent agreed.', 'Elli göterimi razy boldy.', 'A2'),
    ('number', '/ˈnʌmbə/', 'N', 'san', 'число', 'a word or sign that says how many', 'a phone number', 'telefon belgisi', 'A1', 'phone number'),
    ('half', '/hɑːf/', 'N', 'ýarym', 'половина', 'one of two equal parts', 'Half of them came.', 'Ýarymy geldi.', 'A2', 'half of'),
    ('double', '/ˈdʌbl/', 'ADJ', 'iki esse', 'двойной', 'twice as much', 'double the price', 'iki esse baha', 'A2'),
    ('score', '/skɔː/', 'N', 'hasap, bal', 'счёт', 'the number of points in a game', 'The score was two to one.', 'Hasap iki bir boldy.', 'A2'),
    ('average', '/ˈævərɪdʒ/', 'N', 'ortaça', 'среднее', 'the usual amount', 'the average temperature', 'ortaça temperatura', 'B1', 'on average'),
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
    ('trip', '/trɪp/', 'N', 'syýahat', 'поездка', 'a journey to a place and back', 'a short trip', 'gysga syýahat', 'A1', 'take a trip'),
    ('sight', '/saɪt/', 'N', 'görmeli ýer', 'достопримечательность', 'a place visitors go to see', 'the sights of London', 'Londonyň görmeli ýerleri', 'A2', 'see the sights'),
]

T['life_events'] = [
    ('become', '/bɪˈkʌm/', 'V', 'bolmak', 'становиться', 'to start to be something', 'She became famous.', 'Meşhur boldy.', 'A2', 'become famous'),
    ('famous', '/ˈfeɪməs/', 'ADJ', 'meşhur', 'знаменитый', 'known by many people', 'a famous singer', 'meşhur aýdymçy', 'A1'),
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
    ('journey', '/ˈdʒɜːni/', 'N', 'ýol, syýahat', 'путешествие', 'a trip from one place to another', 'a long journey', 'uzyn ýol', 'A2'),
    ('abroad', '/əˈbrɔːd/', 'ADV', 'daşary ýurtda', 'за границей', 'in another country', 'He works abroad.', 'Daşary ýurtda işleýär.', 'A2'),
    ('suitcase', '/ˈsuːtkeɪs/', 'N', 'çemodan', 'чемодан', 'a case for clothes when travelling', 'a heavy suitcase', 'agyr çemodan', 'A2'),
    ('passport', '/ˈpɑːspɔːt/', 'N', 'pasport', 'паспорт', 'an official document for travelling', 'Show your passport.', 'Pasportyňyzy görkeziň.', 'A2'),
    ('airport', '/ˈeəpɔːt/', 'N', 'howa menzili', 'аэропорт', 'a place where planes take off and land', 'The airport is busy.', 'Howa menzili işlek.', 'A1'),
    ('luggage', '/ˈlʌɡɪdʒ/', 'N', 'bagaž', 'багаж', 'the bags you take when travelling', 'How many pieces of luggage?', 'Näçe bagaž?', 'B1'),
    ('timetable', '/ˈtaɪmteɪbl/', 'N', 'wagt tertibi', 'расписание', 'a list of when things happen', 'the train timetable', 'otly wagt tertibi', 'B1'),
    ('delay', '/dɪˈleɪ/', 'N', 'giçikme', 'задержка', 'when something is late', 'There was a delay.', 'Giçikme boldy.', 'B1'),
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
    ('espresso', '/ˈesprəʊ/', 'N', 'espresso', 'эспрессо', 'a small strong coffee', 'an espresso, please', 'bir espresso, haýyş', 'A2'),
    ('americano', '/əˌmerɪˈkɑːnəʊ/', 'N', 'amerikano', 'американо', 'a coffee made weaker with water', 'a regular americano', 'adaty amerikano', 'A2'),
    ('latte', '/ˈlæteɪ/', 'N', 'latte', 'латте', 'a coffee with a lot of milk', 'a large latte', 'uly latte', 'A2'),
    ('cappuccino', '/ˌkæpuˈtʃiːnəʊ/', 'N', 'kappuçino', 'капучино', 'a coffee with hot milk and foam', 'a double cappuccino', 'iki esse kappuçino', 'A2'),
    ('brownie', '/ˈbraʊni/', 'N', 'şokoladly köke', 'брауни', 'a small square chocolate cake', 'a chocolate brownie', 'şokoladly köke', 'A2'),
    ('croissant', '/ˈkrwæsɒŋ/', 'N', 'kruassan', 'круассан', 'a curved bread roll made with butter', 'a fresh croissant', 'täze kruassan', 'A2'),
    ('take away', '/teɪk əˈweɪ/', 'PHR', 'ýanyň bilen almak', 'на вынос', 'food or drink you take with you', 'A coffee to take away.', 'Ýanym bilen bir kofe.', 'A2', 'to take away'),
    ('for here', '/fə hɪə/', 'PHR', 'şu ýerde', 'здесь (в кафе)', 'eaten or drunk where you buy it', 'For here or to take away?', 'Şu ýerdemi ýa-da ýanyňyz bilen?', 'A2'),
]

T['pe_shop'] = [
    ('How much is it?', '/haʊ mʌtʃ ɪz ɪt/', 'PHR', 'bahasy näçe?', 'сколько это стоит?', 'used to ask the price', 'How much is it? Twenty pounds.', 'Bahasy näçe? Iýirmi funt.', 'A1'),
    ("I'm looking for...", '/aɪm ˈlʊkɪŋ fɔː/', 'PHR', '... gözleýärin', 'я ищу...', 'used to say what you want to buy', "I'm looking for a shirt.", 'Köýnek gözleýärin.', 'A2'),
    ('Do you have this in...?', '/du ju hæv ðɪs ɪn/', 'PHR', 'munuň ... bar?', 'у вас есть это в...?', 'used to ask for another size or colour', 'Do you have this in blue?', 'Munuň gögi barmy?', 'A2'),
    ("It doesn't fit", '/ɪt dʌznt fɪt/', 'PHR', 'bolanok, ölçegi gelenok', 'не подходит по размеру', 'used when clothes are the wrong size', "It doesn't fit. Have you got a larger one?", 'Ölçegi gelenok. Ulysy barmy?', 'A2'),
    ('fitting room', '/ˈfɪtɪŋ ruːm/', 'N', 'synag otagy', 'примерочная', 'a room where you try on clothes', 'The fitting room is over there.', 'Synag otagy aňyrda.', 'A2'),
    ('I\\'m sorry', '/aɪm ˈsɒri/', 'PHR', 'bagyşlaň', 'извините', 'used to apologize', "I'm really sorry.", 'Hakykatdan bagyşlaň.', 'A1'),
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
    ('Excuse me, where is...?', '/ɪkˈskjuːz miː weər ɪz/', 'PHR', 'bagyşlaň, ... nirede?', 'извините, где...?', 'used to ask a stranger for a place', 'Excuse me, where is the station?', 'Bagyşlaň, menzil nirede?', 'A1'),
]

T['pe_restaurant'] = [
    ('starter', '/ˈstɑːtə/', 'N', 'başlangyç tagam', 'закуска', 'a small dish eaten before the main one', 'soup as a starter', 'başlangyç hökmünde çorba', 'A2'),
    ('main course', '/meɪn kɔːs/', 'N', 'esasy tagam', 'основное блюдо', 'the largest dish of a meal', 'chicken as a main course', 'esasy tagam hökmünde towuk', 'A2'),
    ('dessert', '/dɪˈzɜːt/', 'N', 'süýji tagam', 'десерт', 'sweet food eaten at the end of a meal', 'What is there for dessert?', 'Süýji tagam näme bar?', 'A2', 'for dessert'),
    ('menu', '/ˈmenjuː/', 'N', 'menýu', 'меню', 'a list of the food a restaurant serves', 'Can I see the menu?', 'Menýuny görüp bilerinmi?', 'A1', 'see the menu'),
    ('bill', '/bɪl/', 'N', 'hasap', 'счёт', 'the paper that says what you must pay', 'The bill, please.', 'Hasaby, haýyş.', 'A1', 'pay the bill'),
    ('tip', '/tɪp/', 'N', 'çaý pul', 'чаевые', 'extra money you leave for the waiter', 'Leave a small tip.', 'Kiçi çaý pul goýuň.', 'A2', 'leave a tip'),
    ('waiter', '/ˈweɪtə/', 'N', 'ofisiant', 'официант', 'a person who serves food in a restaurant', 'The waiter brought the bill.', 'Ofisiant hasaby getirdi.', 'A1'),
    ('order', '/ˈɔːdə/', 'V', 'sargyt etmek', 'заказывать', 'to ask for food in a restaurant', 'We ordered fish.', 'Balyk sargyt etdik.', 'A2', 'order a meal'),
    ('soup', '/suːp/', 'N', 'çorba', 'суп', 'a hot liquid meal', 'onion soup', 'sogan çorbasy', 'A1'),
    ('grilled', '/ɡrɪld/', 'ADJ', 'grillenen', 'жареный на гриле', 'cooked over a fire or hot surface', 'grilled chicken', 'grillenen towuk', 'A2'),
]

T['pe_airport'] = [
    ('check in', '/tʃek ɪn/', 'PHR', 'hasaba durmak', 'зарегистрироваться', 'to give your bags and get a seat at an airport', 'Check in two hours before the flight.', 'Uçardan iki sagat öň hasaba duruň.', 'A2'),
    ('security', '/sɪˈkjʊərəti/', 'N', 'howpsuzlyk barlagy', 'контроль безопасности', 'the place where bags are checked at an airport', 'Go through security.', 'Howpsuzlyk barlagyndan geçiň.', 'A2', 'go through security'),
    ('departure lounge', '/dɪˈpɑːtʃə laʊndʒ/', 'N', 'uçuş zaly', 'зал ожидания', 'the area where you wait for a flight', 'Wait in the departure lounge.', 'Uçuş zalynda garaşyň.', 'B1'),
    ('gate', '/ɡeɪt/', 'N', 'gapy', 'выход на посадку', 'the place where you get on a plane', 'Go to gate twelve.', 'On ikinji gapa baryň.', 'A2'),
    ('taxi rank', '/ˈtæksi ræŋk/', 'N', 'taksi duralgasy', 'стоянка такси', 'a place where taxis wait for people', 'Take a taxi from the rank.', 'Duralgadan taksi tutuň.', 'B1'),
    ('cab', '/kæb/', 'N', 'taksi', 'такси', 'a taxi', 'I called a cab.', 'Taksi çagyrdym.', 'A2', 'call a cab'),
    ('coach', '/kəʊtʃ/', 'N', 'uly awtobus', 'автобус (междугородный)', 'a large bus for long journeys', 'The coach leaves at eight.', 'Uly awtobus sagat sekizde gidýär.', 'B1'),
    ('the Tube', '/ðə tjuːb/', 'N', 'London metrosy', 'лондонское метро', 'the underground railway in London', 'Take the Tube to the airport.', 'Howa menziline metro bilen gidiň.', 'B1'),
]
'''

anchor = "# lesson -> (unit, title, topic from the contents table, [topics that supply its words])"
if s.count(anchor) != 1:
    sys.exit(f'ABORT: lessons anchor matched {s.count(anchor)}')
s = s.replace(anchor, TOPICS.strip() + "\n\n\n" + anchor)

# every Elementary unit has A, B and C — the missing eleven now have their words
LESSON_EDITS = [
    ("'2C':  (2,  'Slow down!', 'imperatives', []),",
     "'2C':  (2,  'Slow down!', 'feelings · imperatives', ['feelings']),"),
    ("'5A':  (5,  'Vote for me!', 'present continuous', []),",
     "'5A':  (5,  'Vote for me!', 'noise · present continuous', ['noise']),"),
    ("'5C':  (5,  'A city for all seasons', 'buying clothes', []),",
     "'5C':  (5,  'A city for all seasons', 'clothes', ['clothes']),"),
    ("'6A':  (6,  'Selfies', 'word formation', []),",
     "'6A':  (6,  'Selfies', 'words in a story', ['story']),"),
    ("'7A':  (7,  'A murder mystery', 'there is / there are', []),",
     "'7A':  (7,  'A murder mystery', 'the story · there is / there are', ['crime']),"),
    ("'8B':  (8,  'White gold', 'quantifiers · containers', ['comparatives']),",
     "'8B':  (8,  'White gold', 'food containers · quantifiers', ['containers']),"),
    ("'8C':  (8,  'Facts and figures', 'high numbers', []),",
     "'8C':  (8,  'Facts and figures', 'high numbers', ['high_numbers']),"),
    ("'9B':  (9,  'Five continents in a day', 'be going to', []),",
     "'9B':  (9,  'Five continents in a day', 'city holidays · be going to', ['holidays']),"),
    ("'9C':  (9,  'The fortune teller', 'city holidays', []),",
     "'9C':  (9,  'The fortune teller', 'verb phrases', ['life_events']),"),
    ("'10B': (10, 'Experiences or things?', 'verbs + infinitive', []),",
     "'10B': (10, 'Experiences or things?', 'verbs + infinitive', ['infinitive']),"),
    ("'11A': (11, \"I've seen it ten times!\", 'present perfect', []),",
     "'11A': (11, \"I've seen it ten times!\", 'irregular past participles · present perfect', ['past_participles']),"),
    ("'11B': (11, \"He's been everywhere!\", 'irregular past participles', []),",
     "'11B': (11, \"He's been everywhere!\", 'travel · experiences', ['travel_words']),"),
    # 8B no longer borrows the comparatives; they belong with the superlatives in 9A
    ("'9A':  (9,  'The most dangerous place...', 'places and buildings', ['places', 'superlatives']),",
     "'9A':  (9,  'The most dangerous place...', 'places and buildings', ['places', 'superlatives', 'comparatives']),"),
]
for old, new in LESSON_EDITS:
    if s.count(old) != 1:
        sys.exit(f'ABORT: lesson edit matched {s.count(old)} times: {old[:60]}')
    s = s.replace(old, new)
print('  - ' + str(len(LESSON_EDITS)) + ' lessons filled from the book')

PE = """
# Practical English is not a Vocabulary Bank topic: it is six filmed episodes,
# each with its own words, so it gets its own unit.
for code, n, title, topic, key in (
    ('PE1', 1, 'Arriving in London', 'in a hotel', 'pe_hotel'),
    ('PE2', 2, 'Coffee to take away', 'buying a coffee', 'pe_cafe'),
    ('PE3', 3, 'In a clothes shop', 'buying clothes', 'pe_shop'),
    ('PE4', 4, 'Getting lost', 'asking the way · directions', 'pe_directions'),
    ('PE5', 5, 'At a restaurant', 'understanding a menu', 'pe_restaurant'),
    ('PE6', 6, 'Going home', 'getting to the airport', 'pe_airport'),
):
    LESSONS[code] = (n, title, topic, [key])
"""

anchor2 = """def main():"""
if s.count(anchor2) != 1:
    sys.exit('ABORT: main() anchor')
s = s.replace(anchor2, PE.strip() + "\n\n\n" + anchor2)
print('  - Practical English unit 13 (PE1-PE6) added')

# the sort key assumes a numeric lesson code; PE1 has none
old_sort = "    for lesson in sorted(LESSONS, key=lambda k: (int(k[:-1]), k[-1])):"
new_sort = """    for lesson in sorted(LESSONS, key=lesson_sort_key):"""
c = s.count(old_sort)
if c != 2:
    sys.exit(f'ABORT: sort key matched {c} times, expected 2')
s = s.replace(old_sort, new_sort)
s = s.replace("""def main():""", """def lesson_sort_key(code):
    \"\"\"Order lessons the way the book does. Numeric codes sort by unit then by
    letter; the Practical English episodes (PE1-PE6) come after unit 12.\"\"\"
    m = re.match(r'^(\\\\d+)(.*)$', code)
    if m:
        return (int(m.group(1)), m.group(2))
    return (13, code)


def main():""", 1)
s = s.replace("import json\nimport os\nimport sys", "import json\nimport os\nimport re\nimport sys")
print('  - lesson sort handles non-numeric codes')

# unit 13 must exist in the app's book list, or its lessons have nowhere to show
open(GEN, 'w', encoding='utf-8').write(s)
print('wrote ' + GEN)
