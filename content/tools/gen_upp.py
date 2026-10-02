#!/usr/bin/env python3
"""English File Upper-Intermediate — vocabulary organised by the book's own structure.

Same method as gen_int.py / gen_pre.py. The OCR dump (uploads/upper.txt,
10,404 lines) kept the contents table and the Vocabulary Bank references
legible. tm / ru / def / ex are my own work and proofread:false; the IPA is
written properly, not copied from the OCR.

STRUCTURE (contents table, dump lines 27-100). Upper-Intermediate 4th edition
has 10 units, each with TWO lessons (A and B — no C), and five Colloquial
English episodes after units 1, 3, 5, 7 and 9:
  1A Questions and answers · 1B It's a mystery · CE1 talking about getting a job
  2A Doctor, doctor! · 2B Act your age
  3A Fasten your seat belts · 3B A really good ending? · CE2 talking about books
  4A Stormy weather · 4B A risky business
  5A I'm a survivor · 5B Wish you were here · CE3 talking about waste
  6A Night night · 6B Music to my ears
  7A Let's not argue · 7B It's all an act · CE4 talking about performances
  8A Cutting crime · 8B Fake news
  9A Good business? · 9B Super cities · CE5 talking about advertising
  10A Science fact, science-fiction · 10B Free speech

Vocabulary Bank (12 sections) -> lesson: Illnesses and injuries->2A,
Clothes and fashion->2B, Air travel->3A, Adverbs and adverbial phrases->3B,
Weather->4A, Feelings->5A, Verbs often confused->7A, The body->7B,
Crime and punishment->8A, The media->8B, Business->9A, Word building->9B.
Everything else comes from in-lesson boxes.

Colloquial English episodes carry unit 11 in the data (units 1-10 are the
book's), and the app shows each episode right after the unit it follows.

Usage: python3 content/tools/gen_upp.py
"""
import json
import os
import re
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'upperintermediate.json')

# topic -> [ (en, ipa, pos, tm, ru, def, ex, exTm, cefr[, coll]) ]
# SB pages from the syllabus checklist (TG pp.4-6), verified against the TG.
PAGE = {
    '1A': 6, '1B': 10, '2A': 16, '2B': 20, '3A': 26, '3B': 30,
    '4A': 36, '4B': 40, '5A': 46, '5B': 50, '6A': 56, '6B': 60,
    '7A': 66, '7B': 70, '8A': 76, '8B': 80, '9A': 86, '9B': 90,
    '10A': 96, '10B': 100,
    'CE1': 14, 'CE2': 34, 'CE3': 54, 'CE4': 74, 'CE5': 94,
}

T = {}

# ---- in-lesson 1A — getting a job (Questions and answers) ----
T['job_hunting'] = [
    ('application', '/ˌæplɪˈkeɪʃn/', 'N', 'ýüz tutma', 'заявление', 'a formal request for a job', 'She sent her application yesterday.', 'Ýüz tutmasyny düýn iberdi.', 'B1', 'job application'),
    ('candidate', '/ˈkændɪdət/', 'N', 'dalaşgär', 'кандидат', 'a person being considered for a job', 'There were six candidates for the job.', 'Işe alty dalaşgär bardy.', 'B1', 'shortlisted candidate'),
    ('CV', '/ˌsiː ˈviː/', 'N', 'te terjimehaly', 'резюме', 'a document listing your education and work', 'Attach your CV to the email.', 'Te terjimehalyňyzy emaila goşuň.', 'B1', 'write a CV'),
    ('employer', '/ɪmˈplɔɪə(r)/', 'N', 'iş beriji', 'работодатель', 'a person or company that gives jobs', 'My employer offers health insurance.', 'Iş berijim saglyk ätiýaçlandyrmasyny hödürleýär.', 'B1'),
    ('interview', '/ˈɪntəvjuː/', 'N', 'söhbetdeşlik', 'собеседование', 'a meeting to decide if you get a job', 'The interview lasted an hour.', 'Söhbetdeşlik bir sagat dowam etdi.', 'B1', 'job interview'),
    ('qualification', '/ˌkwɒlɪfɪˈkeɪʃn/', 'N', 'hünär derejesi', 'квалификация', 'a skill or exam that you need for a job', 'What qualifications do you have?', 'Haýsy hünär derejeleriňiz bar?', 'B1', 'teaching qualification'),
    ('salary', '/ˈsæləri/', 'N', 'aýlyk hak', 'зарплата', 'money paid every month for work', 'The salary is 5,000 manat a month.', 'Aýlyk hak aýda 5,000 manat.', 'A2', 'monthly salary'),
    ('skill', '/skɪl/', 'N', 'endik', 'умение, навык', 'an ability to do something well', 'Communication is a key skill.', 'Aragatnaşyk esasy endikdir.', 'A2', 'language skills'),
    ('strength', '/streŋθ/', 'N', 'güýçli tarap', 'сильная сторона', 'something you are good at', 'Patience is my main strength.', 'Sabyrlylyk meniň esasy güýçli tarapym.', 'B1', 'main strength'),
    ('weakness', '/ˈwiːknəs/', 'N', 'gowsuz tarap', 'слабая сторона', 'something you are not good at', 'Public speaking is his weakness.', 'Köpçülik öňünde çykyş onuň gowsuz tarapy.', 'B1'),
    ('experience', '/ɪkˈspɪəriəns/', 'N', 'tecrübe', 'опыт', 'knowledge gained by doing something', 'Do you have any teaching experience?', 'Mugallymçylyk tejribäňiz barmy?', 'A2', 'work experience'),
    ('recruit', '/rɪˈkruːt/', 'V', 'işe almak', 'набирать (кадры)', 'to find new people for a job', 'The company recruited ten engineers.', 'Kompaniýa on hünärmeni işe aldy.', 'B2', 'recruit staff'),
    ('resign', '/rɪˈzaɪn/', 'V', 'işden çekilmek', 'увольняться (самому)', 'to leave a job by choice', 'She resigned to study abroad.', 'Daşary ýurtda okamak üçin işden çekildi.', 'B1', 'resign from'),
]

# ---- in-lesson 1B — compound adjectives ----
T['compound_adjs'] = [
    ('open-minded', '/ˌəʊpən ˈmaɪndɪd/', 'ADJ', 'açyk pikirli', 'непредвзятый', 'willing to consider new ideas', 'She is open-minded about new ideas.', 'Täze pikirlere açyk pikirli.', 'B2'),
    ('narrow-minded', '/ˌnærəʊ ˈmaɪndɪd/', 'ADJ', 'çäklendirilen pikirli', 'ограниченный (о взглядах)', 'not willing to accept different ideas', 'His narrow-minded views upset people.', 'Çäklendirilen pikirleri adamlary biynjalyk edýär.', 'B2'),
    ('old-fashioned', '/ˌəʊld ˈfæʃnd/', 'ADJ', 'köne düşünjeli', 'старомодный', 'not modern', 'He has some old-fashioned opinions.', 'Käbir köne düşünjeli pikiri bar.', 'A2'),
    ('good-looking', '/ˌɡʊd ˈlʊkɪŋ/', 'ADJ', 'ýaraşykly', 'красивый, привлекательный', 'attractive in appearance', 'Her good-looking brother is an actor.', 'Ýaraşykly dogany aktýor.', 'A2'),
    ('well-known', '/ˌwel ˈnəʊn/', 'ADJ', 'meşhur', 'известный', 'known by many people', 'He is a well-known TV presenter.', 'Meşhur telewizion alyp baryjy.', 'A2'),
    ('well-paid', '/ˌwel ˈpeɪd/', 'ADJ', 'gowy tölenýän', 'хорошо оплачиваемый', 'earning a lot of money', 'She has a well-paid job in finance.', 'Maliýede gowy tölenýän işi bar.', 'B1', 'a well-paid job'),
    ('part-time', '/ˌpɑːt ˈtaɪm/', 'ADJ', 'ýarym ştatly', 'неполный рабочий день', 'working less than full hours', 'He works part-time in a café.', 'Kafede ýarym ştatly işleýär.', 'A2', 'part-time job'),
    ('short-term', '/ˌʃɔːt ˈtɜːm/', 'ADJ', 'gysga möhletli', 'краткосрочный', 'lasting a short time', 'This is only a short-term solution.', 'Bu diňe gysga möhletli çözgüt.', 'B2', 'short-term plan'),
    ('long-term', '/ˌlɒŋ ˈtɜːm/', 'ADJ', 'uzak möhletli', 'долгосрочный', 'lasting a long time', 'They need a long-term strategy.', 'Uzak möhletli strategiýa gerek.', 'B2', 'long-term effect'),
    ('high-quality', '/ˌhaɪ ˈkwɒləti/', 'ADJ', 'ýokary hilli', 'высококачественный', 'very good in quality', 'They sell high-quality shoes.', 'Ýokary hilli aýakgap satýarlar.', 'B1', 'high-quality products'),
    ('good-tempered', '/ˌɡʊd ˈtempəd/', 'ADJ', 'gowy häsiýetli', 'добродушный', 'rarely angry', 'Our good-tempered dog loves children.', 'Gowy häsiýetli itimiz çagalary söýýär.', 'B2'),
    ('bad-tempered', '/ˌbæd ˈtempəd/', 'ADJ', 'erbet häsiýetli', 'раздражительный', 'often angry', 'The bad-tempered neighbour shouted again.', 'Erbet häsiýetli goňşy ýene gygyrdy.', 'B2'),
    ('world-famous', '/ˌwɜːld ˈfeɪməs/', 'ADJ', 'dünýä belli', 'всемирно известный', 'known everywhere in the world', 'They visited the world-famous museum.', 'Dünýä belli muzeýe baryp gördüler.', 'A2'),
    ('paranormal', '/ˌpærəˈnɔːml/', 'ADJ', 'fövkalade, paranormal', 'паранормальный', 'that science cannot explain', 'The programme was about paranormal events.', 'Gepleşik paranormal wakalar baradady.', 'B2'),
]

# ---- Vocabulary Bank — Illnesses and injuries -> 2A ----
T['illnesses'] = [
    ('ache', '/eɪk/', 'N', 'agyry', 'боль (ноющая)', 'a continuous pain', 'I have an ache in my back.', 'Arkamda agyry bar.', 'A2', 'back ache'),
    ('headache', '/ˈhedeɪk/', 'N', 'kelle agyry', 'головная боль', 'a pain in the head', 'I have a terrible headache.', 'Elhenç kelle agyrym bar.', 'A2', 'have a headache'),
    ('stomachache', '/ˈstʌməkeɪk/', 'N', 'garyn agyry', 'боль в животе', 'a pain in the stomach', 'The child has a stomachache.', 'Çaganyň garyny agyrýar.', 'A2'),
    ('toothache', '/ˈtuːθeɪk/', 'N', 'diş agyry', 'зубная боль', 'a pain in a tooth', 'Toothache kept him awake.', 'Diş agyry ony ukusyz goýdy.', 'A2'),
    ('bruise', '/bruːz/', 'N', 'gökerti', 'синяк', 'a dark mark on the skin after a hit', 'She has a bruise on her arm.', 'Golunda gökerti bar.', 'B1', 'a black bruise'),
    ('rash', '/ræʃ/', 'N', 'gijilewük', 'сыпь', 'red spots on the skin', 'The baby has a rash on her neck.', 'Çaganyň boýnunda gijilewük bar.', 'B1'),
    ('sprain', '/spreɪn/', 'V', 'burmak (bilegi)', 'растянуть (связки)', 'to injure a joint by twisting it', 'I sprained my ankle playing football.', 'Futbol oýnap ýanjygymy burdum.', 'B1', 'sprain your ankle'),
    ('swelling', '/ˈswelɪŋ/', 'N', 'çiş', 'отёк', 'an area that becomes bigger after injury', 'Put ice on the swelling.', 'Çişe buz goý.', 'B2'),
    ('dizzy', '/ˈdɪzi/', 'ADJ', 'başı aýlanan', 'головокружительный (о состоянии)', 'feeling that everything is turning', 'I felt dizzy after the ride.', 'Attraksiondan soň başym aýlandy.', 'A2', 'feel dizzy'),
    ('unconscious', '/ʌnˈkɒnʃəs/', 'ADJ', 'huşsuz', 'без сознания', 'not awake or aware', 'The driver was unconscious after the crash.', 'Sürüji çaknyşykdan soň huşsuz boldy.', 'B2'),
    ('recover', '/rɪˈkʌvə(r)/', 'V', 'sagalmak', 'выздоравливать', 'to get better after an illness', 'She recovered in two weeks.', 'Iki hepdede sagaldy.', 'B1', 'recover from'),
    ('symptom', '/ˈsɪmptəm/', 'N', 'alamat', 'симптом', 'a sign that shows an illness', 'Fever is a common symptom.', 'Gyzgyn adaty alamat.', 'B1', 'flu symptoms'),
    ('painkiller', '/ˈpeɪnkɪlə(r)/', 'N', 'agyry aýryjy', 'обезболивающее', 'medicine that stops pain', 'Take a painkiller after the operation.', 'Operasiýadan soň agyry aýryjy iç.', 'B1'),
    ('prescription', '/prɪˈskrɪpʃn/', 'N', 'resept', 'рецепт (врача)', "a doctor's written order for medicine", 'The doctor wrote a prescription.', 'Lukman resept ýazdy.', 'B1', 'on prescription'),
    ('surgery', '/ˈsɜːdʒəri/', 'N', ' operasiýa; lukman otagy', 'операция; приёмная врача', 'a medical operation, or the place a doctor works', 'He needs surgery on his knee.', 'Dyzine operasiýa gerek.', 'B1', 'have surgery'),
    ('allergic reaction', '/əˌledʒɪk riˈækʃn/', 'N', 'allergik reaksiýa', 'аллергическая реакция', 'a bad effect on your body from something you eat or touch', 'He had an allergic reaction to the nuts.', 'Hozlara allergik reaksiýasy boldy.', 'B1'),
    ('bleed', '/bliːd/', 'V', 'ganamak', 'кровоточить', 'to lose blood', 'Your nose is bleeding.', 'Burnuň ganaýar.', 'B1'),
    ('blood pressure', '/ˈblʌd ˌpreʃə/', 'N', 'gan basyşy', 'кровяное давление', 'the force of blood in your body', 'The doctor measured my blood pressure.', 'Lukman gan basyşymy ölçedi.', 'B1'),
    ('burn', '/bɜːn/', 'N', 'ýanyk', 'ожог', 'an injury from fire or heat', 'She had a burn on her hand.', 'Elinde ýanyk bardy.', 'B1'),
    ('choke', '/tʃəʊk/', 'V', 'bogulmak, demgysmak', 'давиться, задыхаться', 'to have trouble breathing because something is stuck in your throat', 'The child choked on a grape.', 'Çaga üzüm demgysdy.', 'B1'),
    ('flu', '/fluː/', 'N', 'dümew', 'грипп', 'an illness like a bad cold', 'I had the flu last week.', 'Geçen hepde dümew bolupdym.', 'A2'),
    ('food poisoning', '/ˈfuːd ˌpɔɪzənɪŋ/', 'N', 'iýmit zäherlenmesi', 'пищевое отравление', 'illness from eating bad food', 'He got food poisoning from the fish.', 'Balykdan iýmit zäherlenmesini aldy.', 'B1'),
    ('get over', '/ˌɡet ˈəʊvə/', 'PHR', 'soňuna çykmak, sagalmak', 'оправиться, преодолеть', 'to become well again after an illness', 'It took her weeks to get over the flu.', 'Dümewden sagalmagy hepdelere çekdi.', 'B1'),
    ('lie down', '/ˌlaɪ ˈdaʊn/', 'PHR', 'uzynlygyna ýatmak', 'ложиться, прилечь', 'to put your body in a flat position', 'You look ill — lie down.', 'Näsag görünýärsiň — uzynlygyna ýat.', 'A2'),
    ('plaster', '/ˈplɑːstə/', 'N', 'ýelmeşikli sargy', 'пластырь', 'a small sticky cover for a cut', 'Put a plaster on your finger.', 'Barmagyňa ýelmeşikli sargy goý.', 'B1'),
    ('sunburn', '/ˈsʌnbɜːn/', 'N', 'gün ýanmasy', 'солнечный ожог', 'painful red skin from too much sun', 'Use cream to avoid sunburn.', 'Gün ýanmasyndan goranmak üçin krem ulan.', 'B1'),
    ('swollen', '/ˈswəʊlən/', 'ADJ', 'çişen', 'опухший', 'bigger and rounder because of injury', 'My ankle is swollen.', 'Ýanbaşym çişdi.', 'B1'),
    ('vomit', '/ˈvɒmɪt/', 'V', 'gaýtarmak', 'рвать, тошнить', 'to bring food back up from your stomach', 'He felt sick and vomited.', 'Erbet duýup gaýtartdy.', 'B1'),
    ('throw up', '/ˌθrəʊ ˈʌp/', 'PHR', 'gaýtarmak', 'рвать, тошнить', 'to vomit', 'She threw up after the journey.', 'Ýolculukdan soň gaýtardy.', 'B1'),
    ('faint', '/feɪnt/', 'V', 'huşundan gitmek', 'терять сознание, падать в обморок', 'to fall asleep-like because of illness or shock', 'She fainted in the hot room.', 'Yssy otagda huşundan gitdi.', 'B1'),
    ('pass out', '/ˌpɑːs ˈaʊt/', 'PHR', 'huşundan gitmek', 'отключиться, потерять сознание', 'to faint', 'He passed out from the heat.', 'Yssydan huşundan gitdi.', 'B1'),
    ('come round', '/ˌkʌm ˈraʊnd/', 'PHR', 'huşuna gelmek', 'приходить в сознание', 'to become conscious again', 'She came round in the hospital.', 'Hassahanada huşuna geldi.', 'B1'),
    ('sneeze', '/sniːz/', 'V', 'asgyrmak', 'чихать', 'to make a sudden loud noise through your nose', 'Cover your mouth when you sneeze.', 'Asgyranyňda agzyňy ýap.', 'A2'),
    ('cough', '/kɒf/', 'V', 'üsgürmek', 'кашлять', 'to push air out loudly because of a tickle in your throat', 'He coughed all night.', 'Bütin gije üsgürdi.', 'A2'),
    ('diarrhoea', '/ˌdaɪəˈrɪə/', 'N', 'içgeçme', 'диарея', 'a medical condition when your body removes food too quickly', 'The illness caused diarrhoea.', 'Kesel içgeçme getirdi.', 'B1'),
    ('pulse', '/pʌls/', 'N', 'urgy, puls', 'пульс', 'the regular beat of blood in your body', 'The nurse took his pulse.', 'Şepagat uýasy pulsuny aldy.', 'B1'),
]

# ---- Vocabulary Bank — Clothes and fashion -> 2B ----
T['clothes'] = [
    ('casual', '/ˈkæʒuəl/', 'ADJ', 'ýönekeý (geýim)', 'повседневный', 'comfortable and not formal', 'The office dress code is casual.', 'Edaranyň geýim düzgüni ýönekeý.', 'A2', 'casual clothes'),
    ('checked', '/tʃekt/', 'ADJ', 'öýjükli', 'в клетку', 'with a pattern of squares', 'He wore a checked shirt.', 'Öýjükli köýnek geýdi.', 'B1', 'a checked shirt'),
    ('cotton', '/ˈkɒtn/', 'N', 'pagta (mata)', 'хлопок', 'cloth made from a soft white plant', 'This T-shirt is 100% cotton.', 'Bu futbolka 100% pagta.', 'A2', 'made of cotton'),
    ('label', '/ˈleɪbl/', 'N', 'ýarlyk', 'этикетка, ярлык', 'a piece of material with information', 'Check the label for washing advice.', 'Ýuwmak maslahaty üçin ýarlygy barla.', 'A2', 'designer label'),
    ('leather', '/ˈleðə(r)/', 'N', 'deri (material)', 'кожа (материал)', 'skin of an animal used to make clothes', 'She bought a leather jacket.', 'Deri kurtka satyn aldy.', 'A2', 'leather shoes'),
    ('plain', '/pleɪn/', 'ADJ', 'ýönekeý (nagşysyz)', 'однотонный, гладкий', 'with no pattern or decoration', 'He prefers plain white shirts.', 'Ýönekeý ak köýnekleri gowy görýär.', 'B1', 'a plain T-shirt'),
    ('silk', '/sɪlk/', 'N', 'ýüpek', 'шёлк', 'soft shiny cloth made by insects', 'Her silk dress cost a fortune.', 'Ýüpek köýnegi köp durdy.', 'A2', 'silk scarf'),
    ('size', '/saɪz/', 'N', 'ölçeg', 'размер', 'how big or small clothes are', 'Do you have this in my size?', 'Bu meniň ölçegimde barmy?', 'A1', 'in size 42'),
    ('smart', '/smɑːt/', 'ADJ', 'oňat geýnen', 'нарядный, элегантный', 'looking clean and formal', 'You look smart in that suit.', 'Şol kostýumda oňat geýnen görünýärsiň.', 'A2', 'smart clothes'),
    ('striped', '/straɪpt/', 'ADJ', 'çyzykly', 'полосатый', 'with lines of colour', 'She wore a striped jumper.', 'Çyzykly switer geýdi.', 'B1', 'a striped shirt'),
    ('suit', '/suːt/', 'N', 'kostýum', 'костюм', 'a jacket and trousers of the same cloth', 'He wore a grey suit to the meeting.', 'Duşuşyga çal kostýum geýdi.', 'A2', 'wear a suit'),
    ('suede', '/sweɪd/', 'N', 'zamşa', 'замша', 'soft leather with a furry surface', 'Her suede boots are expensive.', 'Zamşa ädikleri gymmat.', 'B2'),
    ('tracksuit', '/ˈtræksuːt/', 'N', 'sport kostýumy', 'спортивный костюм', 'loose clothes worn for sport', 'He jogs in a blue tracksuit.', 'Gök sport kostýumynda ylgaw edýär.', 'A2'),
    ('try on', '/traɪ ɒn/', 'PHR', 'geýip görmek', 'примерять', 'to put on clothes to test them', 'Can I try on this coat?', 'Bu paltony geýip görüp bilerinmi?', 'A2', 'try on a dress'),
    ('wool', '/wʊl/', 'N', 'ýüň', 'шерсть', 'cloth made from sheep hair', 'Wool socks keep your feet warm.', 'Ýüň joraplar aýaklaryňy ýyly saklaýar.', 'A2', 'wool jumper'),
    ('classic', '/ˈklæsɪk/', 'ADJ', 'klassiki', 'классический', 'simple and traditional in style', 'She wore a classic black dress.', 'Klassiki gara köýnek geýdi.', 'B1'),
    ('hooded', '/ˈhʊdɪd/', 'ADJ', 'başlykly', 'с капюшоном', 'with a part that covers your head', 'He wore a hooded jacket.', 'Başlykly kurtka geýdi.', 'B1'),
    ('lace top', '/ˈleɪs tɒp/', 'N', 'tör köýnekçe', 'кружевной топ', 'a light top made of delicate net-like material', 'She bought a white lace top.', 'Ak tör köýnekçe satyn aldy.', 'B1'),
    ('linen suit', '/ˈlɪnɪn suːt/', 'N', 'keteni kostýum', 'льняной костюм', 'a suit made of light cloth for hot weather', 'He wore a linen suit to the wedding.', 'Toýa keteni kostýum geýdi.', 'B1'),
    ('polo neck', '/ˈpəʊləʊ nek/', 'N', 'boýunly switer', 'водолазка', 'a sweater with a high part round the neck', 'She wore a black polo neck.', 'Gara boýunly switer geýdi.', 'B1'),
    ('scruffy', '/ˈskrʌfi/', 'ADJ', 'selpi, kirpi', 'неряшливый', 'old and untidy', 'He looked scruffy in his old jeans.', 'Köne jinsisinde selpi görünýärdi.', 'B1'),
    ('sleeveless', '/ˈsliːvləs/', 'ADJ', 'ýeňsiz', 'без рукавов', 'without sleeves', 'She bought a sleeveless dress.', 'Ýeňsiz köýnek satyn aldy.', 'B1'),
    ('spotted', '/ˈspɒtɪd/', 'ADJ', 'meňňili', 'в горошек, в крапинку', 'covered with small round marks', 'He wore a spotted shirt.', 'Meňňili köýnek geýdi.', 'B1'),
    ('tight', '/taɪt/', 'ADJ', 'gysyk, dar', 'тесный, обтягивающий', 'fitting very closely to the body', 'These shoes are too tight.', 'Bu aýakgaplar gaty dar.', 'B1'),
    ('loose', '/luːs/', 'ADJ', 'giň, bol', 'свободный, мешковатый', 'not fitting closely to the body', 'She prefers loose clothes in summer.', 'Tomusda giň eşikleri ileri tutýar.', 'B1'),
    ('denim', '/ˈdenɪm/', 'N', 'jinsi mata', 'джинсовая ткань', 'strong cotton cloth used for jeans', 'She wore a denim jacket.', 'Jinsi penjek geýdi.', 'B1'),
    ('dress up', '/ˌdres ˈʌp/', 'PHR', 'keýpine geýinmek', 'наряжаться', 'to put on special or formal clothes', 'We dressed up for the party.', 'Toý üçin keýpimize geýindik.', 'B1'),
    ('get changed', '/ˌɡet ˈtʃeɪndʒd/', 'PHR', 'eşik çalyşmak', 'переодеваться', 'to put on different clothes', 'Go and get changed for dinner.', 'Nahar üçin eşigiňi çalyş.', 'A2'),
    ('fit', '/fɪt/', 'V', 'ödün bolmak, gelmek', 'быть впору', 'to be the right size for you', 'The coat fits perfectly.', 'Penjek edil ödüňe gelýär.', 'B1'),
    ('go with', '/ˌɡəʊ ˈwɪð/', 'PHR', 'gelşmek, öwüşgin bermek', 'сочетаться, подходить', 'to look good together', 'That tie doesn’t go with your shirt.', 'Bu galstuk köýnegiňe gelşmeýär.', 'B1'),
]

# ---- Vocabulary Bank — Air travel -> 3A ----
T['air_travel'] = [
    ('boarding pass', '/ˈbɔːdɪŋ pɑːs/', 'N', 'uçar petegi', 'посадочный талон', 'the document that lets you enter a plane', 'Show your boarding pass at the gate.', 'Girelgä uçar petegiňizi görkeziň.', 'A2', 'print your boarding pass'),
    ('check in', '/tʃek ɪn/', 'PHR', 'registrasiýa bolmak', 'регистрироваться (на рейс)', 'to register for a flight', 'We checked in two hours early.', 'Iki sagat öň registrasiýa bolduk.', 'A2', 'check in online'),
    ('customs', '/ˈkʌstəmz/', 'N', 'gümrük', 'таможня', 'the place where bags are checked', 'It took an hour to get through customs.', 'Gümrükden geçmek bir sagat aldy.', 'A2', 'go through customs'),
    ('departure', '/dɪˈpɑːtʃə(r)/', 'N', 'ugrama', 'вылет, отправление', 'the time a plane leaves', 'The departure time is 6 a.m.', 'Ugrama wagty irden 6.', 'A2', 'departure lounge'),
    ('gate', '/ɡeɪt/', 'N', 'girelge (uçar)', 'выход на посадку', 'the door where you enter a plane', 'The flight leaves from gate 12.', 'Reýs 12-nji girelgä gidýär.', 'A2', 'at the gate'),
    ('overhead locker', '/ˈəʊvəhed ˈlɒkə(r)/', 'N', 'ýokarky ýük şkafy', 'багажная полка', 'the space above the seats for bags', 'Put your bag in the overhead locker.', 'Sumkaňyzy ýokarky ýük şkafyna goýuň.', 'B1'),
    ('passenger', '/ˈpæsɪndʒə(r)/', 'N', 'ýolagçy', 'пассажир', 'a person travelling in a vehicle', 'The plane carried 200 passengers.', 'Uçar 200 ýolagçy göterdi.', 'A2'),
    ('pilot', '/ˈpaɪlət/', 'N', 'uçarman', 'пилот', 'the person who flies a plane', 'The pilot announced our arrival.', 'Uçarman gelişimizi yglan etdi.', 'A2', 'airline pilot'),
    ('runway', '/ˈrʌnweɪ/', 'N', 'uçuş zolagy', 'взлётно-посадочная полоса', 'the strip where planes take off', 'The plane taxied to the runway.', 'Uçar uçuş zolagyna tarap hereket etdi.', 'B1'),
    ('take-off', '/ˈteɪk ɒf/', 'N', 'uçma (howa gämisi)', 'взлёт', 'the moment a plane leaves the ground', 'Take-off was delayed by fog.', 'Uçma tuman sebäpli giçikdi.', 'A2', 'during take-off'),
    ('flight', '/flaɪt/', 'N', 'uçar sapary', 'рейс, полёт', 'a journey by plane', 'The flight to Istanbul takes three hours.', 'Stambula uçar sapary üç sagat alýar.', 'A1', 'direct flight'),
    ('airline', '/ˈeəlaɪn/', 'N', 'howa ýollary', 'авиакомпания', 'a company that flies planes', 'Which airline do you fly with?', 'Haýsy howa ýollary bilen uçýarsyňyz?', 'A2', 'airline ticket'),
    ('landing', '/ˈlændɪŋ/', 'N', 'gonma', 'посадка (самолёта)', 'the moment a plane comes down', 'The landing was very smooth.', 'Gonma gaty ýumşak boldy.', 'A2', 'a smooth landing'),
    ('cabin crew', '/ˈkæbɪn kruː/', 'N', 'uçar ekipaży', 'бортпроводники', 'the people who look after passengers on a plane', 'The cabin crew showed us to our seats.', 'Uçar ekipažy bizi ýerlerimize alyp bardy.', 'B1'),
    ('jet lag', '/ˈdʒet læɡ/', 'N', 'wagt üýtgemeginiň täsiri', 'реакция на смену часовых поясов', 'tiredness after a long flight across time zones', 'It took me a week to beat jet lag.', 'Wagt täsirinden gutulmak bir hepde aldy.', 'B1'),
    ('long-haul', '/ˌlɒŋ ˈhɔːl/', 'ADJ', 'uzak aralykly', 'дальнемагистральный', 'flying a very long distance', 'We took a long-haul flight to Australia.', 'Awstraliýa uzak aralykly uçar bilen gitdik.', 'B1'),
    ('connecting flight', '/kəˈnektɪŋ flaɪt/', 'N', 'birikdiriji uçar', 'стыковочный рейс', 'a plane you take after your first plane', 'We missed our connecting flight.', 'Birikdiriji uçarymyzy sypdyrdyk.', 'B1'),
    ('check-in desk', '/ˈtʃekɪn desk/', 'N', 'registrasiýa stoly', 'стойка регистрации', 'where you give your bags and get your boarding pass', 'Go to the check-in desk with your passport.', 'Pasportyň bilen registrasiýa stoluna bar.', 'B1'),
    ('domestic', '/dəˈmestɪk/', 'ADJ', 'içerki', 'внутренний (о рейсе)', 'within one country', 'We took a domestic flight to Edinburgh.', 'Edinburga içerki uçar bilen gitdik.', 'B1'),
    ('excess baggage', '/ˌekses ˈbæɡɪdʒ/', 'N', 'artykmaç bagaj', 'излишний багаж', 'bags that weigh more than allowed', 'We paid for excess baggage.', 'Artykmaç bagaž üçin töledik.', 'B1'),
    ('hand luggage', '/ˈhænd ˌlʌɡɪdʒ/', 'N', 'el bagažy', 'ручная кладь', 'small bags you carry onto the plane', 'Hand luggage must weigh under 10 kilos.', 'El bagažy 10 kilodan az bolmaly.', 'B1'),
    ('metal detector', '/ˈmetl dɪˌtektə/', 'N', 'metal detektory', 'металлоискатель', 'a machine that finds metal objects on people', 'Walk through the metal detector.', 'Metal detektoryndan geç.', 'B1'),
    ('queue', '/kjuː/', 'N', 'nobat', 'очередь', 'a line of people waiting', 'There was a long queue at security.', 'Howpsuzlykda uzyn nobat bardy.', 'A2'),
    ('security', '/sɪˈkjʊərəti/', 'N', 'howpsuzlyk', 'служба безопасности', 'the place where you are checked before a flight', 'We waited an hour at security.', 'Howpsuzlykda bir sagat garaşdyk.', 'A2'),
    ('turbulence', '/ˈtɜːbjələns/', 'N', 'turbulentlik, yralanma', 'турбулентность', 'rough movement of a plane in the air', 'The plane shook because of turbulence.', 'Turbulentlik sebäpli uçar yralandy.', 'B1'),
    ('unpack', '/ˌʌnˈpæk/', 'V', 'zatlaryny çykarmak', 'распаковывать', 'to take things out of your bags', 'She unpacked as soon as she arrived.', 'Gelen badyna zatlaryny çykardy.', 'A2'),
    ('visa', '/ˈviːzə/', 'N', 'wiza', 'виза', 'official permission to enter a country', 'You need a visa to visit the USA.', 'ABŞ-a barmak üçin wiza gerek.', 'B1'),
]

# ---- Vocabulary Bank — Adverbs and adverbial phrases -> 3B ----
T['adverbs'] = [
    ('absolutely', '/ˈæbsəluːtli/', 'ADV', 'düýbünden', 'абсолютно', 'completely', 'The view was absolutely amazing.', 'Görnüş düýbünden haýran galdyryjy boldy.', 'A2'),
    ('almost', '/ˈɔːlməʊst/', 'ADV', 'diýen ýaly', 'почти', 'very nearly', 'Almost everyone passed the exam.', 'Diýen ýaly hemme synagdan geçdi.', 'A2'),
    ('by far', '/baɪ fɑː(r)/', 'PHR', 'has aýdyň', 'намного, безусловно', 'used to say something is much the best', 'She is by far the best player.', 'Ol has aýdyň iň gowy oýunçy.', 'B1'),
    ('definitely', '/ˈdefɪnətli/', 'ADV', 'elbetde', 'определённо', 'without any doubt', 'This is definitely the best film this year.', 'Bu elbetde şu ýylyň iň gowy filmi.', 'A2'),
    ('especially', '/ɪˈspeʃəli/', 'ADV', 'aýratyn', 'особенно', 'more than usual', 'I love fruit, especially melons.', 'Miwe gowy görýärin, aýratyn gawunlary.', 'A2'),
    ('hardly', '/ˈhɑːdli/', 'ADV', 'diýen ýaly däl', 'едва, почти не', 'almost not', 'I could hardly hear the music.', 'Sazy diýen ýaly eşidilmeýärdi.', 'A2', 'hardly ever'),
    ('nearly', '/ˈnɪəli/', 'ADV', 'diýen ýaly (ýakyn)', 'почти', 'almost; very nearly', 'It is nearly midnight.', 'Diýen ýaly gije ýary.', 'A2'),
    ('particularly', '/pəˈtɪkjələli/', 'ADV', 'aýratynlykda', 'в частности', 'more than in other cases', 'The second half was particularly exciting.', 'Ikinji ýarym aýratynlykda täsirli boldy.', 'B1'),
    ('slightly', '/ˈslaɪtli/', 'ADV', 'birneme', 'слегка', 'a little', 'The jacket is slightly too big.', 'Kurtka birneme uly.', 'A2'),
    ('totally', '/ˈtəʊtəli/', 'ADV', 'düýbünden (doly)', 'полностью', 'completely', 'I totally agree with you.', 'Düýbünden seniň bilen ylalaşýaryn.', 'A2'),
    ('apparently', '/əˈpærəntli/', 'ADV', 'meňzeýän, görünmegine görä', 'по-видимому', 'used to say what people told you but you are not sure', 'Apparently, he is leaving.', 'Görnüşine görä, ol gidýär.', 'B1'),
    ('at the end', '/ət ði ˈend/', 'PHR', 'soňunda (ýeriň/wagtyň)', 'в конце', 'at the final part of something', 'There is a shop at the end of the street.', 'Köçäniň ahyrynda dükan bar.', 'A2'),
    ('at the moment', '/ət ðə ˈməʊmənt/', 'PHR', 'häzirki wagtda', 'в данный момент', 'at this time; right now', 'She is busy at the moment.', 'Häzirki wagtda meşgul.', 'A2'),
    ('basically', '/ˈbeɪsɪkli/', 'ADV', 'esasan', 'в основном', 'used to give the main facts', 'Basically, we have two options.', 'Esasan, iki wariantymyz bar.', 'B1'),
    ('certainly', '/ˈsɜːtnli/', 'ADV', 'elbetde', 'конечно', 'used to say yes strongly', 'Will you help? Certainly!', 'Kömek edersiňmi? Elbetde!', 'B1'),
    ('eventually', '/ɪˈventʃuəli/', 'ADV', 'aňrysoňunda', 'в конце концов', 'finally, after a long time', 'The bus eventually arrived.', 'Awtobus aňrysoňunda geldi.', 'B1'),
    ('gradually', '/ˈɡrædʒuəli/', 'ADV', 'drgyn-dyrgyn, kem-kemden', 'постепенно', 'slowly, in small stages', 'He gradually got better.', 'Kem-kemden gowulaşdy.', 'B1'),
    ('in fact', '/ɪn ˈfækt/', 'PHR', 'aslynda', 'на самом деле', 'used to add a surprising truth', 'He looks young. In fact, he is 50.', 'Ýaş görünýär. Aslynda 50 ýaşynda.', 'B1'),
    ('in the end', '/ɪn ði ˈend/', 'PHR', 'soňy bilen', 'в конце концов, в итоге', 'finally, after many problems', 'In the end, we stayed at home.', 'Soňy bilen öýde galdyk.', 'B1'),
    ('lately', '/ˈleɪtli/', 'ADV', 'soňky wagtlarda', 'в последнее время', 'recently', 'Have you seen her lately?', 'Soňky wagtlarda ony gördüňmi?', 'B1'),
    ('obviously', '/ˈɒbviəsli/', 'ADV', 'äşgär, aýdyň', 'очевидно', 'used to say something is easy to see', 'Obviously, she was angry.', 'Äşgär, ol gaharlydy.', 'B1'),
    ('yet', '/jet/', 'ADV', 'entek', 'ещё (в вопросах и отрицаниях)', 'until now', 'She hasn’t arrived yet.', 'Entek gelmedi.', 'A2'),
]
# ---- Vocabulary Bank — Weather + the environment -> 4A ----
T['weather'] = [
    ('climate', '/ˈklaɪmət/', 'N', 'howa şertleri', 'климат', 'the general weather of a place', 'Turkmenistan has a dry climate.', 'Türkmenistanyň howa şertleri gurak.', 'A2', 'dry climate'),
    ('drought', '/draʊt/', 'N', 'gurakçylyk', 'засуха', 'a long time without rain', 'The drought ruined the harvest.', 'Gurakçylyk hasyly ýok etdi.', 'B1'),
    ('flood', '/flʌd/', 'N', 'suw joşmasy', 'наводнение', 'water covering dry land', 'The flood closed the road.', 'Suw joşmasy ýoly ýapdy.', 'A2'),
    ('hurricane', '/ˈhʌrɪkən/', 'N', 'harasat', 'ураган', 'a violent tropical storm', 'The hurricane destroyed the village.', 'Harasat obany weýran etdi.', 'A2'),
    ('thunderstorm', '/ˈθʌndəstɔːm/', 'N', 'gök gürrüldili ýagyş', 'гроза', 'a storm with thunder and lightning', 'The thunderstorm lasted an hour.', 'Gök gürrüldili ýagyş bir sagat dowam etdi.', 'A2'),
    ('forecast', '/ˈfɔːkɑːst/', 'N', 'howa maglumaty', 'прогноз погоды', 'a report about coming weather', 'The forecast says snow tomorrow.', 'Howa maglumaty ertir gar diýýär.', 'A2', 'weather forecast'),
    ('humid', '/ˈhjuːmɪd/', 'ADJ', 'ygally (howa)', 'влажный', 'with a lot of water in the air', 'Summers here are hot and humid.', 'Bu ýerde tomus yssy we ygally.', 'B1'),
    ('global warming', '/ˌɡləʊbl ˈwɔːmɪŋ/', 'N', 'global ýylylyk', 'глобальное потепление', 'the rise in the Earth\'s temperature', 'Global warming is melting the ice.', 'Global ýylylyk buzlary eredýär.', 'B1'),
    ('climate change', '/ˈklaɪmət tʃeɪndʒ/', 'N', 'howanyň üýtgemegi', 'изменение климата', 'long-term changes in the weather', 'We must fight climate change.', 'Howanyň üýtgemegine garşy göreşmeli.', 'B1'),
    ('endangered species', '/ɪnˈdeɪndʒəd ˈspiːʃiːz/', 'N', 'howp astyndaky görnüşler', 'вымирающие виды', 'animals or plants that may die out', 'The snow leopard is an endangered species.', 'Garyň barsy howp astyndaky görnüş.', 'B2'),
    ('emissions', '/ɪˈmɪʃnz/', 'N', 'zyňyndylar', 'выбросы', 'gases sent into the air', 'Cars produce harmful emissions.', 'Maşynlar zyýanly zyňyndylar çykarýar.', 'B2', 'carbon emissions'),
    ('deforestation', '/ˌdiːˌfɒrɪˈsteɪʃn/', 'N', 'tokaýlaryň gyrylmagy', 'вырубка лесов', 'cutting down all the trees in an area', 'Deforestation threatens many animals.', 'Tokaýlaryň gyrylmagy köp haýwanlara howp salýar.', 'B2'),
    ('below zero', '/bɪˈləʊ ˈzɪərəʊ/', 'PHR', 'noldan aşak', 'ниже нуля', 'colder than 0°C', 'It was ten degrees below zero.', 'On gradus noldan aşakdy.', 'B1'),
    ('blizzard', '/ˈblɪzəd/', 'N', 'boran, çovgun', 'буран, метель', 'a severe snowstorm with strong wind', 'The blizzard closed the roads.', 'Boran ýollary ýapdy.', 'B1'),
    ('breeze', '/briːz/', 'N', 'şemal, ýel', 'лёгкий ветер, бриз', 'a gentle wind', 'A cool breeze came from the sea.', 'Deňizden salkyn şemal geldi.', 'B1'),
    ('changeable', '/ˈtʃeɪndʒəbl/', 'ADJ', 'üýtgäp duran', 'изменчивый', 'often changing', 'The weather here is very changeable.', 'Bu ýerde howa gaty üýtgäp durýar.', 'B1'),
    ('chilly', '/ˈtʃɪli/', 'ADJ', 'sowugrak', 'прохладный', 'uncomfortably cold', 'It is chilly this morning.', 'Şu irden sowugrak.', 'B1'),
    ('damp', '/dæmp/', 'ADJ', 'çygly', 'сырой, влажный', 'slightly wet', 'The walls are cold and damp.', 'Diwarlar sowuk we çygly.', 'B1'),
    ('hail', '/heɪl/', 'N', 'dolu', 'град', 'balls of ice falling from the sky', 'The hail damaged the cars.', 'Dolu ulaglara zyýan berdi.', 'B1'),
    ('heatwave', '/ˈhiːtweɪv/', 'N', 'yssy howa döwri', 'волна жары', 'a period of unusually hot weather', 'The heatwave lasted two weeks.', 'Yssy döwri iki hepde dowam etdi.', 'B1'),
    ('lightning', '/ˈlaɪtnɪŋ/', 'N', 'yldyrym', 'молния', 'a flash of light in the sky in a storm', 'Lightning lit up the sky.', 'Yldyrym asmany ýagtyltdy.', 'B1'),
    ('monsoon', '/ˌmɒnˈsuːn/', 'N', 'musson', 'муссон', 'the season of heavy rain in Asia', 'The monsoon starts in June.', 'Musson iýunda başlaýar.', 'B1'),
    ('pouring', '/ˈpɔːrɪŋ/', 'ADJ', 'guýup ýagan', 'проливной', 'raining very heavily', 'It is pouring outside.', 'Daşarda guýup ýagýar.', 'B1'),
    ('settled', '/ˈsetld/', 'ADJ', 'durnukly', 'устойчивый (о погоде)', 'not changing; calm', 'We had a week of settled weather.', 'Bir hepde durnukly howa boldy.', 'B1'),
]

# ---- in-lesson 4B — expressions with take ----
T['take'] = [
    ('take advantage of', '/teɪk ədˈvɑːntɪdʒ əv/', 'PHR', 'peýdalanmak', 'воспользоваться; обмануть', 'to use an opportunity, or to treat someone unfairly', 'Take advantage of the free trial.', 'Mugt synagdan peýdalanyň.', 'B1'),
    ('take after', '/teɪk ɑːftə(r)/', 'PHR', 'meňzemek', 'пойти в (кого-л.)', 'to be similar to an older relative', 'She takes after her mother.', 'Ol ejesine meňzeýär.', 'B1'),
    ('take part in', '/teɪk pɑːt ɪn/', 'PHR', 'gatnaşmak', 'участвовать в', 'to join an activity', 'Did you take part in the competition?', 'Bäsleşige gatnaşdyňmy?', 'A2'),
    ('take place', '/teɪk pleɪs/', 'PHR', 'bolup geçmek', 'происходить', 'to happen', 'The concert takes place on Friday.', 'Konsert anna güni bolup geçýär.', 'A2'),
    ('take turns', '/teɪk tɜːnz/', 'PHR', 'nobatma-nobat', 'по очереди', 'to do something one after another', 'We take turns to drive.', 'Nobatma-nobat ulag sürýäris.', 'A2', 'take turns to do'),
    ('take care of', '/teɪk keər əv/', 'PHR', 'ideg etmek', 'заботиться о', 'to look after someone or something', 'She takes care of her little brother.', 'Kiçi doganyna ideg edýär.', 'A2'),
    ('take over', '/teɪk ˈəʊvə(r)/', 'PHR', 'öz üstüne almak', 'брать на себя (контроль)', 'to gain control of something', 'The new manager took over in June.', 'Täze müdir iýunda öz üstüne aldy.', 'B1'),
    ('take up', '/teɪk ʌp/', 'PHR', 'başlamak', 'начать заниматься', 'to start a hobby or activity', 'He took up painting last year.', 'Geçen ýyl surata düşürmäge başlady.', 'A2', 'take up a hobby'),
    ('take your time', '/teɪk jɔː(r) taɪm/', 'PHR', 'howlukma', 'не торопись', 'to do something without hurrying', 'Take your time — there is no rush.', 'Howlukma — howlukmaçlyk ýok.', 'A2'),
    ('take it easy', '/teɪk ɪt ˈiːzi/', 'PHR', 'dynç al', 'не волнуйся, спокойнее', 'to relax and not worry', 'Take it easy — everything will be fine.', 'Dynç al — hemme zat gowy bolar.', 'A2'),
    ('take a break', '/teɪk ə breɪk/', 'PHR', 'arakesme etmek', 'сделать перерыв', 'to rest for a while', 'Let us take a break for ten minutes.', 'Geliň, on minut arakesme edeliň.', 'A2'),
    ('take something seriously', '/teɪk ˈsʌmθɪŋ ˈsɪəriəsli/', 'PHR', 'çynlakaý kabul etmek', 'принимать всерьёз', 'to treat something as important', 'You should take his warning seriously.', 'Onuň duýduryşyny çynlakaý kabul etmeli.', 'B1'),
]

# ---- Vocabulary Bank — Feelings -> 5A ----
T['feelings_adj'] = [
    ('anxious', '/ˈæŋkʃəs/', 'ADJ', 'aladaly', 'тревожный', 'worried about something', 'She felt anxious before the flight.', 'Uçuşdan öň aladaly boldy.', 'B1', 'feel anxious'),
    ('ashamed', '/əˈʃeɪmd/', 'ADJ', 'utanýan', 'пристыженный', 'feeling bad about something you did', 'He was ashamed of his mistake.', 'Ýalňyşy üçin utanýardy.', 'B1', 'ashamed of'),
    ('delighted', '/dɪˈlaɪtɪd/', 'ADJ', 'şaý-sevinçli (şat)', 'в восторге', 'very pleased', 'We were delighted with the news.', 'Habara şaý-sevinçli bolduk.', 'B1', 'delighted with'),
    ('grateful', '/ˈɡreɪtfl/', 'ADJ', 'minnetdar', 'благодарный', 'feeling thankful', 'I am grateful for your help.', 'Kömegiňiz üçin minnetdar.', 'B1', 'grateful for'),
    ('homesick', '/ˈhəʊmsɪk/', 'ADJ', 'watana küýseli', 'тоскующий по дому', 'missing your home', 'He got homesick in his first month.', 'Birinji aýynda watana küýsedi.', 'B1'),
    ('miserable', '/ˈmɪzrəbl/', 'ADJ', 'bagtyýar däl (örän betbagt)', 'несчастный', 'very unhappy', 'The cold rain made us miserable.', 'Sowuk ýagyş bizi betbagt etdi.', 'B1'),
    ('proud', '/praʊd/', 'ADJ', 'buýsançly', 'гордый', 'pleased about something you did', 'Her parents are proud of her.', 'Ene-atasy oňa buýsanýar.', 'A2', 'proud of'),
    ('relieved', '/rɪˈliːvd/', 'ADJ', 'ýeňillik duýýan', 'чувствующий облегчение', 'happy that a problem ended', 'I was relieved when he called.', 'Ol jaň edende ýeňillik duýdum.', 'B1', 'relieved to hear'),
    ('upset', '/ʌpˈset/', 'ADJ', 'ynjylan', 'расстроенный', 'unhappy because of something bad', 'She was upset by the news.', 'Habardan ynjyldy.', 'A2', 'feel upset'),
    ('envious', '/ˈenviəs/', 'ADJ', 'imrenýän', 'завистливый (по-доброму)', 'wanting what someone else has', 'I was envious of her success.', 'Onuň üstünligine imrenýärdim.', 'B2', 'envious of'),
    ('embarrassed', '/ɪmˈbærəst/', 'ADJ', 'utanjaň (ýagdaýda)', 'смущённый', 'feeling awkward in front of others', 'He felt embarrassed by the applause.', 'El çarpyşmalardan utanjaň boldy.', 'A2', 'feel embarrassed'),
    ('frustrated', '/frʌˈstreɪtɪd/', 'ADJ', 'lapykeç (gaharly)', 'разочарованный (раздражённый)', 'angry because you cannot do something', 'She got frustrated with the slow internet.', 'Haýal internetden lapykeç boldy.', 'B1', 'frustrated with'),
    ('astonished', '/əˈstɒnɪʃt/', 'ADJ', 'haýran galan', 'изумлённый', 'very surprised', 'She was astonished by the news.', 'Habra haýran galdy.', 'B1'),
    ('bewildered', '/bɪˈwɪldəd/', 'ADJ', 'çaşan', 'сбитый с толку', 'completely confused', 'He looked bewildered by the question.', 'Soragdan çaşan ýaly görünýärdi.', 'B2'),
    ('devastated', '/ˈdevəsteɪtɪd/', 'ADJ', 'çym-pytrak bolan (duýgy)', 'подавленный, убитый горем', 'extremely shocked and upset', 'She was devastated when he died.', 'Ol ölende çym-pytrak boldy.', 'B2'),
    ('stunned', '/stʌnd/', 'ADJ', 'haýran, lal bolan', 'ошеломлённый', 'so surprised you cannot speak', 'He was stunned by the result.', 'Netijeden lal boldy.', 'B2'),
    ('fed up', '/ˌfed ˈʌp/', 'ADJ', 'jany ýadan', 'сытый по горло', 'annoyed because something has continued too long', 'I am fed up with the rain.', 'Ýagyşdan janym ýady.', 'B1'),
    ('gutted', '/ˈɡʌtɪd/', 'ADJ', 'lapykeç (güýçli)', 'крайне разочарованный (разг.)', 'extremely disappointed (informal)', 'He was gutted when his team lost.', 'Topary ýykylanda lapykeç boldy.', 'B2'),
    ('desperate', '/ˈdespərət/', 'ADJ', 'umytsyz, çäresiz', 'отчаянный', 'feeling you have little hope', 'She was desperate for a job.', 'Işe çäresiz mätäçdi.', 'B1'),
    ('offended', '/əˈfendɪd/', 'ADJ', 'ynjylyk', 'обиженный', 'hurt or upset by what someone said', 'She was offended by his joke.', 'Degişmesinden ynjyldy.', 'B1'),
    ('thrilled', '/θrɪld/', 'ADJ', 'şatlykdan uçan', 'в восторге', 'extremely happy and excited', 'They were thrilled with the news.', 'Habra şatlykdan uçdular.', 'B1'),
    ('down', '/daʊn/', 'ADJ', 'ruhdan düşen', 'подавленный (разг.)', 'sad (informal)', 'He has been feeling down lately.', 'Soňky wagtlarda ruhdan düşüp ýör.', 'B1'),
    ('shattered', '/ˈʃætəd/', 'ADJ', 'ýadan, ysgynsyz', 'измотанный (разг.)', 'extremely tired (informal)', 'I was shattered after the match.', 'Oýundan soň ysgynsyzdym.', 'B2'),
    ('lonely', '/ˈləʊnli/', 'ADJ', 'ýalňyz, köňülsüz', 'одинокий', 'sad because you are alone', 'She felt lonely in the new city.', 'Täze şäherde ýalňyz duýdy.', 'B1'),
    ('scared stiff', '/ˌskeəd ˈstɪf/', 'ADJ', 'gorkudan doňan', 'парализованный страхом', 'extremely frightened', 'I was scared stiff of spiders.', 'Mör-möjeklerden gorkudan doňýardym.', 'B1'),
    ('overwhelmed', '/ˌəʊvəˈwelmd/', 'ADJ', 'duýga gark bolan', 'подавленный (чувствами)', 'affected very strongly by feelings', 'She was overwhelmed with joy.', 'Şatlyga gark boldy.', 'B2'),
    ('terrified', '/ˈterɪfaɪd/', 'ADJ', 'gorkan, howp alan', 'испуганный до ужаса', 'very frightened', 'He is terrified of flying.', 'Uçardan gaty gorkýar.', 'B1'),
]

# ---- in-lesson 5B — expressing feelings: verbs ----
T['feelings_verbs'] = [
    ('amuse', '/əˈmjuːz/', 'V', 'güldürmek', 'забавлять', 'to make someone smile or laugh', 'His jokes amused the children.', 'Degişmeleri çagalary güldürdi.', 'B1'),
    ('annoy', '/əˈnɔɪ/', 'V', 'gaharyňy getirmek', 'раздражать', 'to make someone a little angry', 'The noise annoyed the neighbours.', 'Goh goňşularyň gaharyny getirdi.', 'A2'),
    ('bore', '/bɔː(r)/', 'V', 'bikar etmek', 'наскучивать', 'to make someone lose interest', 'The long speech bored everyone.', 'Uzyn çykyş hemmäni bikar etdi.', 'A2'),
    ('confuse', '/kənˈfjuːz/', 'V', 'bulaşdyrmak', 'смущать, путать', 'to make something hard to understand', 'The instructions confused me.', 'Görkezmeler meni bulaşdyrdy.', 'A2'),
    ('depress', '/dɪˈpres/', 'V', 'ruhdan düşürmek', 'удручать', 'to make someone very unhappy', 'The grey weather depressed him.', 'Çal howa ony ruhdan düşürdi.', 'B1'),
    ('embarrass', '/ɪmˈbærəs/', 'V', 'utandyrmak', 'смущать', 'to make someone feel awkward', 'His questions embarrassed the speaker.', 'Soraglary çykyş edijini utandyrdy.', 'A2'),
    ('excite', '/ɪkˈsaɪt/', 'V', 'täsirlendirmek (joşdurmaga)', 'волновать', 'to make someone feel eager', 'The trip excited the students.', 'Syýahat talyplary joşdurdy.', 'A2'),
    ('frighten', '/ˈfraɪtn/', 'V', 'gorkuzmak', 'пугать', 'to make someone afraid', 'The thunder frightened the baby.', 'Gök gürrüldisi çagany gorkuzdy.', 'A2', 'frighten someone'),
    ('irritate', '/ˈɪrɪteɪt/', 'V', 'jynjygaltmak', 'раздражать (слегка)', 'to annoy someone slightly', 'His habit of humming irritated me.', 'Onuň hümmürdeme endigi meni jynjygaltdy.', 'B1'),
    ('shock', '/ʃɒk/', 'V', 'şok etmek', 'шокировать', 'to surprise someone very much', 'The result shocked everyone.', 'Netije hemmäni şok etdi.', 'A2'),
    ('inspired', '/ɪnˈspaɪəd/', 'ADJ', 'ruhlanan', 'вдохновлённый', 'made to feel excited to do something', 'The film inspired her to travel.', 'Film ony syýahata ruhlandyrdy.', 'B1'),
    ('terrifying', '/ˈterɪfaɪɪŋ/', 'ADJ', 'elhenç', 'ужасающий', 'making you feel very frightened', 'It was a terrifying experience.', 'Elhenç tejribedi.', 'B1'),
]

# ---- in-lesson 6A — sleep ----
T['sleep'] = [
    ('fall asleep', '/fɔːl əˈsliːp/', 'PHR', 'uklamak (ukusyna gitmek)', 'засыпать', 'to start sleeping', 'I fell asleep during the film.', 'Filmiň dowamynda ukusyna gitdim.', 'A2'),
    ('doze off', '/dəʊz ɒf/', 'PHR', 'mürgülemek', 'задремать', 'to fall asleep lightly', 'He dozed off on the bus.', 'Awtobusda mürgüledi.', 'B1'),
    ('oversleep', '/ˌəʊvəˈsliːp/', 'V', 'ukuda galmak', 'проспать', 'to wake up later than planned', 'I overslept and missed the train.', 'Ukuda galyp, otludyr sypdyrdym.', 'B1'),
    ('nap', '/næp/', 'N', 'gündizki uky', 'дневной сон', 'a short sleep in the day', 'A 20-minute nap helps you focus.', '20 minutlyk gündizki uky ünsüňi jemlemäge kömek edýär.', 'A2', 'take a nap'),
    ('insomnia', '/ɪnˈsɒmniə/', 'N', 'ukusyzlyk', 'бессонница', 'when you cannot sleep', 'Stress can cause insomnia.', 'Dartgynlylyk ukusyzlyga sebäp bolup biler.', 'B2'),
    ('yawn', '/jɔːn/', 'V', 'äsnemek', 'зевать', 'to open the mouth wide when tired', 'She yawned at the meeting.', 'Duşuşykda äsnedi.', 'A2'),
    ('bedtime', '/ˈbedtaɪm/', 'N', 'ýatyş wagty', 'время сна', 'the time you usually go to bed', 'Bedtime for the children is nine.', 'Çagalaryň ýatyş wagty dokuz.', 'A2'),
    ('light sleeper', '/laɪt ˈsliːpə(r)/', 'N', 'ýeňil ukyly', 'чутко спящий', 'a person who wakes easily', 'I am a light sleeper — any noise wakes me.', 'Ýeňil ukyly — islendik ses meni oýarýar.', 'B1'),
    ('sleeping pill', '/ˈsliːpɪŋ pɪl/', 'N', 'uky dermany', 'снотворное', 'medicine that helps you sleep', 'The doctor gave him a sleeping pill.', 'Lukman oňa uky dermanyny berdi.', 'B1', 'take a sleeping pill'),
    ('wide awake', '/ˌwaɪd əˈweɪk/', 'PHR', 'düýbünden oýak', 'бодрствующий', 'completely awake', 'The noise left me wide awake at 3 a.m.', 'Goh gije 3-de meni düýbünden oýak goýdy.', 'A2'),
]

# ---- in-lesson 6B — music ----
T['music'] = [
    ('album', '/ˈælbəm/', 'N', 'albom (saz)', 'альбом', 'a collection of songs', 'Their new album came out in May.', 'Täze albomlary maýda çykdy.', 'A2', 'debut album'),
    ('band', '/bænd/', 'N', 'saz topary', 'группа (музыкальная)', 'a group of musicians', 'The band plays every Saturday.', 'Saz topary her şenbe oýnaýar.', 'A1', 'rock band'),
    ('chorus', '/ˈkɔːrəs/', 'N', 'gaýtalama bent', 'припев', 'the part of a song that repeats', 'Everyone sings the chorus.', 'Hemme kişi gaýtalama bendi aýdýar.', 'B1', 'sing the chorus'),
    ('composer', '/kəmˈpəʊzə(r)/', 'N', 'kompozitor', 'композитор', 'a person who writes music', 'The composer wrote the music at twenty.', 'Kompozitor sazy ýigrimi ýaşynda ýazdy.', 'B1'),
    ('conductor', '/kənˈdʌktə(r)/', 'N', 'dirijor', 'дирижёр', 'the person who leads an orchestra', 'The conductor raised his baton.', 'Dirijor taýajygyny galdyrdy.', 'B1'),
    ('gig', '/ɡɪɡ/', 'N', 'konsert (kiçi)', 'концерт (группы)', 'a live music performance', 'We went to a gig last night.', 'Düýn agşam konserte gitdik.', 'B1', 'play a gig'),
    ('lyrics', '/ˈlɪrɪks/', 'N', 'sözler (aýdymyň)', 'слова песни', 'the words of a song', 'I love the lyrics of this song.', 'Bu aýdymyň sözlerini gowy görýärin.', 'A2', 'song lyrics'),
    ('venue', '/ˈvenjuː/', 'N', 'konsert meýdançasy', 'место проведения', 'the place where an event happens', 'The venue holds 2,000 people.', 'Meýdança 2,000 adam sygdyrýar.', 'B1', 'concert venue'),
    ('volume', '/ˈvɒljuːm/', 'N', 'ses derejesi', 'громкость', 'how loud the sound is', 'Turn the volume down, please.', 'Ses derejesini peselt.', 'A2', 'turn up the volume'),
    ('catchy', '/ˈkætʃi/', 'ADJ', 'ýatda galýan', 'запоминающийся (о мелодии)', 'easy to remember and sing', 'The song has a catchy tune.', 'Aýdymyň ýatda galýan ahengi bar.', 'B1', 'catchy tune'),
    ('tune', '/tjuːn/', 'N', 'ahenk', 'мелодия', 'a series of musical notes', 'She hummed a familiar tune.', 'Tanyş ahengi hümmürdedi.', 'A2', 'hum a tune'),
    ('hit', '/hɪt/', 'N', 'hit (meşhur aýdym)', 'хит', 'a very successful song or film', 'The single became a huge hit.', 'Singl uly hite öwrüldi.', 'A2', 'number-one hit'),
    ('single', '/ˈsɪŋɡl/', 'N', 'singl', 'сингл', 'one song released on its own', 'They released a new single.', 'Täze singl çykardylar.', 'A2'),
]

# ---- Vocabulary Bank — Verbs often confused -> 7A ----
T['confused_verbs'] = [
    ('borrow', '/ˈbɒrəʊ/', 'V', 'karz almak', 'брать взаймы', 'to take and return something', 'Can I borrow your pen?', 'Galamyňy karz alyp bilerinmi?', 'A2', 'borrow from'),
    ('lend', '/lend/', 'V', 'karz bermek', 'давать взаймы', 'to give something to return later', 'She lent me her umbrella.', 'Saýawanyny maňa karz berdi.', 'A2', 'lend someone money'),
    ('remember', '/rɪˈmembə(r)/', 'V', 'ýatda saklamak', 'помнить', 'to keep something in your mind', 'Do you remember his name?', 'Adyny ýadyňdamy?', 'A1', 'remember to do'),
    ('remind', '/rɪˈmaɪnd/', 'V', 'ýatlatmak', 'напоминать', 'to help someone remember', 'Remind me to call my mum.', 'Ejeme jaň etmegi ýatlat.', 'A2', 'remind someone to do'),
    ('raise', '/reɪz/', 'V', 'galdyrmak', 'поднимать (что-л.)', 'to lift something, or increase it', 'He raised his hand to ask.', 'Soramak üçin elini galdyrdy.', 'A2', 'raise money'),
    ('rise', '/raɪz/', 'V', 'galmak', 'подниматься (самому)', 'to go up by itself', 'Prices rose again this month.', 'Bahalar şu aý ýene galdy.', 'A2', 'the sun rises'),
    ('rob', '/rɒb/', 'V', 'talamak', 'грабить', 'to steal from a place or person', 'Thieves robbed the bank.', 'Ogrular banky talady.', 'A2', 'rob a bank'),
    ('steal', '/stiːl/', 'V', 'ogurlamak', 'украсть', 'to take something that is not yours', 'Someone stole her bag.', 'Biri sumkasyny ogurlady.', 'A2', 'steal money'),
    ('lie', '/laɪ/', 'V', 'ýalan aýtmak', 'лгать', 'to say something that is not true', 'He never lies to his family.', 'Maşgalasyna hiç wagt ýalan aýtmaýar.', 'A2', 'tell a lie'),
    ('say', '/seɪ/', 'V', 'aýtmak', 'сказать', 'to speak words', 'What did she say?', 'Ol näme aýtdy?', 'A1', 'say something'),
    ('tell', '/tel/', 'V', 'gürrüň bermek', 'рассказать', 'to give information to someone', 'Tell me the truth.', 'Maňa hakykaty aýt.', 'A1', 'tell someone'),
    ('speak', '/spiːk/', 'V', 'gürlemek', 'говорить (на языке)', 'to talk, or use a language', 'She speaks three languages.', 'Üç dilde gürleýär.', 'A1', 'speak English'),
    ('talk', '/tɔːk/', 'V', 'gepleşmek', 'разговаривать', 'to have a conversation', 'They talked for hours.', 'Sagatlap gepleşdiler.', 'A1', 'talk about'),
    ('advise', '/ədˈvaɪz/', 'V', 'maslahat bermek', 'советовать', 'to tell someone what they should do', 'I advise you to see a doctor.', 'Lukmana görünmegi maslahat berýärin.', 'B1'),
    ('avoid', '/əˈvɔɪd/', 'V', 'gaça durmak', 'избегать', 'to stay away from something', 'Avoid eating late at night.', 'Gije gijä iýmekden gaça dur.', 'B1'),
    ('beat', '/biːt/', 'V', 'urmak; ýeňmek', 'бить; побеждать', 'to hit repeatedly; to win against someone', 'They beat us 3-1.', 'Bizi 3-1 ýeňdiler.', 'B1'),
    ('deny', '/dɪˈnaɪ/', 'V', 'inkär etmek', 'отрицать', 'to say something is not true', 'He denied stealing the money.', 'Puly ogurlanyny inkär etdi.', 'B1'),
    ('discuss', '/dɪˈskʌs/', 'V', 'ara alyp maslahatlaşmak', 'обсуждать', 'to talk about something with others', 'We discussed the problem.', 'Mesele ara alnyp maslahatlaşyldy.', 'B1'),
    ('expect', '/ɪkˈspekt/', 'V', 'garaşmak, çaklamak', 'ожидать', 'to think something will happen', 'I expect she will come late.', 'Onuň giç geljegine garaşýaryn.', 'B1'),
    ('hope', '/həʊp/', 'V', 'umyt etmek', 'надеяться', 'to want something to happen', 'I hope you feel better soon.', 'Tizräk gowulaşmagyňy umyt edýärin.', 'A2'),
    ('lay', '/leɪ/', 'V', 'goýmak, düşemek', 'класть, стелить', 'to put something down carefully', 'Lay the book on the table.', 'Kitaby stoluň üstüne goý.', 'B1'),
    ('matter', '/ˈmætə/', 'V', 'ähmiýeti bolmak', 'иметь значение', 'to be important', 'It doesn’t matter who wins.', 'Kimiň ýeňýäniniň ähmiýeti ýok.', 'B1'),
    ('mind', '/maɪnd/', 'V', 'garşy bolmak', 'возражать', 'to be annoyed by something', 'Do you mind the noise?', 'Galmagaldan göwnüňe degýärmi?', 'B1'),
    ('notice', '/ˈnəʊtɪs/', 'V', 'üns bermek, görmek', 'замечать', 'to become aware of something', 'Did you notice her new glasses?', 'Onuň täze äýnegini üns berdiňmi?', 'B1'),
    ('prevent', '/prɪˈvent/', 'V', 'öňüni almak', 'предотвращать', 'to stop something happening', 'The rain prevented us from going out.', 'Ýagyş çykmagymyzyň öňüni aldy.', 'B1'),
    ('realize', '/ˈriːəlaɪz/', 'V', 'düşünmek, göz ýetirmek', 'осознавать', 'to understand something clearly', 'He didn’t realize she was angry.', 'Onuň gaharlydygyna düşünmedi.', 'B1'),
    ('refuse', '/rɪˈfjuːz/', 'V', 'ýüz döndermek', 'отказываться', 'to say no to something', 'My neighbour refused to turn down the music.', 'Goňşum aýdymy peseltmekden ýüz dönderdi.', 'B1'),
    ('wait', '/weɪt/', 'V', 'garaşmak', 'ждать', 'to stay until something happens', 'We waited an hour for the bus.', 'Awtobusa bir sagat garaşdyk.', 'A2'),
    ('warn', '/wɔːn/', 'V', 'duýdurmak', 'предупреждать', 'to tell someone about danger', 'The teacher warned us about the exam.', 'Mugallym synag barada duýdurdy.', 'B1'),
    ('win', '/wɪn/', 'V', 'ýeňmek, utmak', 'побеждать, выигрывать', 'to be first in a competition', 'She won the race.', 'Ýaryşy utdy.', 'A2'),
    ('argue', '/ˈɑːɡjuː/', 'V', 'dawa etmek, jedelleşmek', 'спорить', 'to speak angrily because you disagree', 'They argued about money.', 'Pul barada jedelleşdiler.', 'B1'),
]

# ---- Vocabulary Bank — The body -> 7B ----
T['body'] = [
    ('brain', '/breɪn/', 'N', 'beýni', 'мозг', 'the organ inside the head that thinks', 'The brain controls everything.', 'Beýni hemme zady dolandyrýar.', 'A2', 'use your brain'),
    ('chin', '/tʃɪn/', 'N', 'eňek', 'подбородок', 'the bottom part of the face', 'He has a beard on his chin.', 'Eňeginde sakgal bar.', 'A2'),
    ('eyebrow', '/ˈaɪbraʊ/', 'N', 'gaş', 'бровь', 'the line of hair above the eye', 'She raised one eyebrow.', 'Bir gaşyny galdyrdy.', 'A2', 'raise an eyebrow'),
    ('jaw', '/dʒɔː/', 'N', 'äň', 'челюсть', 'the bone that holds the teeth', 'He broke his jaw in the match.', 'Oýunda äňini döwdi.', 'B1'),
    ('liver', '/ˈlɪvə(r)/', 'N', 'bagyr', 'печень', 'the organ that cleans the blood', 'The liver filters toxins.', 'Bagyr zäherleri süzýär.', 'B1'),
    ('lung', '/lʌŋ/', 'N', 'öýken', 'лёгкое', 'the organ used for breathing', 'Smoking damages the lungs.', 'Çilim öýkenlere zyýan ýetirýär.', 'A2', 'lung disease'),
    ('nail', '/neɪl/', 'N', 'dyrnak', 'ноготь', 'the hard part on a finger', 'She cut her nails.', 'Dyrnaklaryny kesdi.', 'A2', 'bite your nails'),
    ('rib', '/rɪb/', 'N', 'gapyrga', 'ребро', 'a bone around the chest', 'He broke two ribs.', 'Iki gapyrgasyny döwdi.', 'B1'),
    ('skull', '/skʌl/', 'N', 'kelle çanagy', 'череп', 'the bone structure of the head', 'The skull protects the brain.', 'Kelle çanagy beýnini goraýar.', 'B1'),
    ('spine', '/spaɪn/', 'N', 'oňurga', 'позвоночник', 'the row of bones down the back', 'Good posture protects your spine.', 'Gowy duruş oňurgaňy goraýar.', 'B1'),
    ('tongue', '/tʌŋ/', 'N', 'dil (agyzdaky)', 'язык (орган)', 'the soft part inside the mouth', 'The tongue helps you taste.', 'Dil tagam duýmaga kömek edýär.', 'A2'),
    ('ankle', '/ˈæŋkl/', 'N', 'ýanjyky süňk', 'щиколотка, лодыжка', 'the joint between your foot and leg', 'I twisted my ankle.', 'Ýanjyky süňkümi sowdum.', 'B1'),
    ('bottom', '/ˈbɒtəm/', 'N', 'oturymlyk', 'низ, задняя часть', 'the lowest part of something; your seat', 'Sign your name at the bottom of the page.', 'Adyňy sahypanyň aşagynda ýaz.', 'B1'),
    ('calf', '/kɑːf/', 'N', 'baldyr', 'икра (ноги)', 'the back part of your leg below the knee', 'He has a cramp in his calf.', 'Baldyrynda sudorga boldy.', 'B1'),
    ('fist', '/fɪst/', 'N', 'ýumruk', 'кулак', 'a hand with the fingers bent in', 'He banged on the door with his fist.', 'Gapyny ýumrugy bilen kakdy.', 'B1'),
    ('heel', '/hiːl/', 'N', 'ökje', 'пятка', 'the back part of your foot', 'My new shoes rub my heels.', 'Täze aýakgaplarym ökjemi sürtýär.', 'B1'),
    ('knee', '/niː/', 'N', 'dyz', 'колено', 'the joint in the middle of your leg', 'She fell on her knees.', 'Dyzynyň üstüne ýykyldy.', 'A2'),
    ('palm', '/pɑːm/', 'N', 'aýa', 'ладонь', 'the inside part of your hand', 'He held the bird in his palm.', 'Guşy aýasynda saklady.', 'B1'),
    ('thigh', '/θaɪ/', 'N', 'budun', 'бедро', 'the top part of your leg', 'He broke his thigh in the accident.', 'Heläkçilikde buduny döwdi.', 'B1'),
    ('waist', '/weɪst/', 'N', 'bil', 'талия', 'the middle part of your body', 'The water came up to his waist.', 'Suw biline çenli geldi.', 'B1'),
    ('wrist', '/rɪst/', 'N', 'bilek', 'запястье', 'the joint between your hand and arm', 'She wore a watch on her wrist.', 'Bileginde sagat dakynypdy.', 'B1'),
    ('frown', '/fraʊn/', 'V', 'ýüzüni salmak', 'хмуриться', 'to make an angry face with your eyebrows', 'The teacher frowned at the noise.', 'Mugallym galmagala ýüzüni saldy.', 'B1'),
    ('hug', '/hʌɡ/', 'V', 'gujaklamak', 'обнимать', 'to put your arms round someone', 'They hugged at the airport.', 'Aeroportda gujaklaşdylar.', 'A2'),
    ('kneel', '/niːl/', 'V', 'dize çökmek', 'становиться на колени', 'to go down onto your knees', 'He knelt down to tie his shoe.', 'Aýakgabyny daňmak üçin dize çökdi.', 'B1'),
    ('stare', '/steə/', 'V', 'tik seretmek', 'пристально смотреть', 'to look at someone for a long time', 'Don’t stare at people.', 'Adamlara tik seretme.', 'B1'),
    ('wave', '/weɪv/', 'V', 'el bulamak', 'махать рукой', 'to move your hand to say hello or goodbye', 'She waved goodbye from the window.', 'Aýnadan el bulap hoşlaşdy.', 'A2'),
    ('wink', '/wɪŋk/', 'V', 'göz gyrpmak', 'подмигивать', 'to close and open one eye quickly', 'He winked at me.', 'Maňa göz gyrpdy.', 'B1'),
    ('stretch', '/stretʃ/', 'V', 'süýndirmek, germek', 'тянуться, растягиваться', 'to make your body or arms long', 'Stretch your arms above your head.', 'Elleriňi kelläňden ýokary ger.', 'B1'),
    ('blow your nose', '/ˌbləʊ jə ˈnəʊz/', 'PHR', 'burnuňy sykmak', 'сморкаться', 'to clear your nose into a tissue', 'Blow your nose gently.', 'Burnuňy ýuwaşlyk bilen sykyň.', 'B1'),
    ('brush your teeth', '/ˌbrʌʃ jə ˈtiːθ/', 'PHR', 'dişleriňi arassalamak', 'чистить зубы', 'to clean your teeth with a brush', 'Brush your teeth twice a day.', 'Günde iki gezek dişleriňi arassala.', 'A2'),
    ('nod your head', '/ˌnɒd jə ˈhed/', 'PHR', 'kelle atmak', 'кивать головой', 'to move your head down to say yes', 'He nodded his head in agreement.', 'Ylalaşyp kellesini atdy.', 'B1'),
    ('raise your eyebrows', '/ˌreɪz jə ˈaɪbraʊz/', 'PHR', 'gaşyňy galdyrmak', 'поднимать брови', 'to lift your eyebrows to show surprise', 'She raised her eyebrows at the price.', 'Baha gaşyny galdyrdy.', 'B1'),
    ('shake hands', '/ˌʃeɪk ˈhændz/', 'PHR', 'el gysyşmak', 'пожимать руки', 'to greet someone by holding their hand', 'The men shook hands.', 'Adamlar el gysyşdy.', 'B1'),
    ('touch your toes', '/ˌtʌtʃ jə ˈtəʊz/', 'PHR', 'barmaklaryňa degmek', 'дотягиваться до носков', 'to bend down and reach your feet', 'Can you touch your toes?', 'Barmaklaryňa degip bilýärsiňmi?', 'B1'),
]

# ---- Vocabulary Bank — Crime and punishment -> 8A ----
T['crime'] = [
    ('break in', '/breɪk ɪn/', 'PHR', 'ogrulyk bilen girmek', 'врываться (для кражи)', 'to enter a building by force to steal', 'Thieves broke in through the window.', 'Ogrular penjireden ogrulyk bilen girdi.', 'B1'),
    ('convict', '/kənˈvɪkt/', 'V', 'günäli tapmak', 'осудить', 'to decide in court that someone is guilty', 'The court convicted him of fraud.', 'Kazyýet ony aldawda günäli tapdy.', 'B2', 'convict someone of'),
    ('fine', '/faɪn/', 'N', 'jerime', 'штраф', 'money paid as a punishment', 'He paid a 200 manat fine.', '200 manat jerime töledi.', 'A2', 'pay a fine'),
    ('pickpocket', '/ˈpɪkpɒkɪt/', 'N', 'jübi ogrysy', 'карманник', 'a thief who steals from pockets', 'Pickpockets work in busy markets.', 'Jübi ogrulary köpçülikli bazarlarda işleýär.', 'B1'),
    ('robbery', '/ˈrɒbəri/', 'N', 'talaň', 'ограбление', 'the crime of stealing from a place', 'The robbery happened at midnight.', 'Talaň gije ýarymda boldy.', 'A2', 'armed robbery'),
    ('shoplifter', '/ˈʃɒplɪftə(r)/', 'N', 'dükan ogrysy', 'магазинный вор', 'a person who steals from shops', 'The shoplifter hid the goods in her coat.', 'Dükan ogrysy harytlary paltoşynda gizledi.', 'B1'),
    ('thief', '/θiːf/', 'N', 'ogry', 'вор', 'a person who steals', 'The thief ran away with the phone.', 'Ogry telefon bilen gaçdy.', 'A2'),
    ('vandal', '/ˈvændl/', 'N', 'wandal', 'вандал', 'a person who damages things on purpose', 'Vandals broke the bus stop glass.', 'Wandallar duralganyň aýnasyny döwdi.', 'B1'),
    ('fraud', '/frɔːd/', 'N', 'aldaw (jenaýat)', 'мошенничество', 'the crime of cheating for money', 'He was jailed for fraud.', 'Aldaw üçin türmä basyldy.', 'B2'),
    ('blackmail', '/ˈblækmeɪl/', 'N', 'gorkuzyp pul almak', 'шантаж', 'demanding money by threatening someone', 'The police stopped the blackmail.', 'Polisiýa gorkuzyp pul almanyň öňüni aldy.', 'B2'),
    ('burglar', '/ˈbɜːɡlə/', 'N', 'ogry (öýe girýän)', 'взломщик', 'a person who steals from houses', 'A burglar broke into the flat.', 'Öýe ogry girdi.', 'B1'),
    ('commit', '/kəˈmɪt/', 'V', 'etmek (jenaýat)', 'совершать (преступление)', 'to do something illegal or wrong', 'He committed the crime last year.', 'Jenaýaty geçen ýyl etdi.', 'B1'),
    ('dealer', '/ˈdiːlə/', 'N', 'satuwjy (gadagan)', 'делец, торговец', 'a person who sells drugs or stolen goods', 'The police arrested the drug dealer.', 'Polisiýa neşe satuwyjysyny tussag etdi.', 'B1'),
    ('evidence', '/ˈevɪdəns/', 'N', 'subutnama', 'улика, доказательство', 'facts that show something is true', 'The police found no evidence.', 'Polisiýa subutnama tapmady.', 'B1'),
    ('guilty', '/ˈɡɪlti/', 'ADJ', 'günäkär', 'виновный', 'having done something wrong', 'The jury found him guilty.', 'Kazyýet ony günäkär tapdy.', 'B1'),
    ('hacker', '/ˈhækə/', 'N', 'haker', 'хакер', 'a person who enters computer systems illegally', 'Hackers stole the data.', 'Hakerler maglumatlary ogurlady.', 'B1'),
    ('innocent', '/ˈɪnəsnt/', 'ADJ', 'günäsiz', 'невиновный', 'not guilty of a crime', 'He says he is innocent.', 'Günäsizdigini aýdýar.', 'B1'),
    ('judge', '/dʒʌdʒ/', 'N', 'kazy', 'судья', 'the person who decides cases in a court', 'The judge gave the verdict.', 'Kazy hökümi çykardy.', 'B1'),
    ('kidnap', '/ˈkɪdnæp/', 'V', 'adam ogurlamak', 'похищать (человека)', 'to take someone away illegally', 'The businessman was kidnapped.', 'Biznesmen ogurlandy.', 'B1'),
    ('mugger', '/ˈmʌɡə/', 'N', 'köçe ogrusy', 'грабитель', 'a person who attacks and robs people in the street', 'A mugger took her bag.', 'Köçe ogrusy torbasyny aldy.', 'B1'),
    ('proof', '/pruːf/', 'N', 'subut', 'доказательство', 'information that shows something is true', 'Do you have any proof?', 'Subutyň barmy?', 'B1'),
    ('stalker', '/ˈstɔːkə/', 'N', 'yzyndan düşýän', 'преследователь', 'a person who follows someone in a frightening way', 'She reported the stalker to the police.', 'Yzyndan düşýäni polisiýa habar berdi.', 'B2'),
    ('theft', '/θeft/', 'N', 'ogrulyk', 'кража', 'the crime of stealing', 'He was arrested for theft.', 'Ogrulyk üçin tussag edildi.', 'B1'),
    ('verdict', '/ˈvɜːdɪkt/', 'N', 'höküm', 'вердикт, приговор', 'the decision of a court', 'The verdict was not guilty.', 'Höküm günäsiz boldy.', 'B1'),
    ('witness', '/ˈwɪtnəs/', 'N', 'şaýat', 'свидетель', 'a person who sees a crime happen', 'The witness described the man.', 'Şaýat şol adamy suratlandyrdy.', 'B1'),
]

# ---- Vocabulary Bank — The media -> 8B ----
T['media'] = [
    ('article', '/ˈɑːtɪkl/', 'N', 'makala', 'статья', 'a piece of writing in a newspaper', 'I read an interesting article.', 'Gyzykly makala okadym.', 'A2', 'front-page article'),
    ('broadcast', '/ˈbrɔːdkɑːst/', 'V', 'ýaýlyma bermek', 'транслировать', 'to send a programme on TV or radio', 'The match was broadcast live.', 'Oýun göni ýaýlyma berildi.', 'B1', 'broadcast live'),
    ('channel', '/ˈtʃænl/', 'N', 'teleýaýlym', 'телеканал', 'a TV station', 'Which channel is the news on?', 'Habar haýsy teleýaýlymda?', 'A2', 'TV channel'),
    ('coverage', '/ˈkʌvərɪdʒ/', 'N', 'beýan (habarlarda)', 'освещение (в СМИ)', 'the reporting of an event', 'The election got wide coverage.', 'Saýlaw giň beýan aldy.', 'B2', 'media coverage'),
    ('current affairs', '/ˌkʌrənt əˈfeəz/', 'N', 'häzirki wakalar', 'текущие события', 'programmes about news and politics', 'He watches current affairs every night.', 'Her agşam häzirki wakalar gepleşiklerini görýär.', 'B2'),
    ('documentary', '/ˌdɒkjuˈmentri/', 'N', 'resminamaly film', 'документальный фильм', 'a factual film about real events', 'We watched a documentary about the sea.', 'Deňiz barada resminamaly film gördük.', 'A2'),
    ('editor', '/ˈedɪtə(r)/', 'N', 'redaktor', 'редактор', 'the person who prepares texts for printing', 'The editor cut the last paragraph.', 'Redaktor soňky abzasy aýyrdy.', 'A2'),
    ('headline', '/ˈhedlaɪn/', 'N', 'sözbaşy', 'заголовок', 'the title of a newspaper story', 'The headline shocked the readers.', 'Sözbaşy okyjylary şok etdi.', 'B1', 'front-page headline'),
    ('journalist', '/ˈdʒɜːnəlɪst/', 'N', 'jurnalist', 'журналист', 'a person who writes news stories', 'The journalist interviewed the mayor.', 'Jurnalist häkim bilen söhbetdeşlik geçirdi.', 'A2'),
    ('press', '/pres/', 'N', 'metbugat', 'пресса', 'newspapers and magazines', 'The story appeared in the press.', 'Waka metbugatda çykdy.', 'B1', 'the local press'),
    ('prime time', '/ˌpraɪm ˈtaɪm/', 'N', 'iň köp tomaşa edilýän wagt', 'прайм-тайм', 'the evening hours with most viewers', 'The show airs at prime time.', 'Gepleşik iň köp tomaşa edilýän wagtda çykýar.', 'B2', 'in prime time'),
    ('tabloid', '/ˈtæblɔɪd/', 'N', 'tabloid gazet', 'газета-таблоид', 'a newspaper with short sensational stories', 'The tabloid printed the rumour.', 'Tabloid gazet gürrüňi çap etdi.', 'B2'),
    ('newsreader', '/ˈnjuːzriːdə(r)/', 'N', 'habar alyp baryjy', 'диктор новостей', 'the person who reads the news on TV', 'The newsreader announced the results.', 'Habar alyp baryjy netijeleri yglan etdi.', 'B1'),
    ('agony aunt', '/ˈæɡəni ɑːnt/', 'N', 'maslahat beriji sütun ýazyjysy', 'автор колонки советов', 'a person who answers personal problems in a magazine', 'She wrote to an agony aunt.', 'Maslahat berijä hat ýazdy.', 'B2'),
    ('commentator', '/ˈkɒmənteɪtə/', 'N', 'şerhçi', 'комментатор', 'a person who describes events as they happen', 'The commentator described every goal.', 'Şerhçi her goly suratlandyrdy.', 'B1'),
    ('critic', '/ˈkrɪtɪk/', 'N', 'tankytçy', 'критик', 'a person who writes opinions about films or books', 'The critics praised the film.', 'Tankytçylar filmi öwdi.', 'B1'),
    ('freelance', '/ˈfriːlɑːns/', 'ADJ', 'erkin işleýän', 'внештатный, фриланс', 'working for different companies, not one employer', 'a freelance journalist', 'Erkin işleýän žurnalist', 'B1'),
    ('paparazzi', '/ˌpæpəˈrætsi/', 'N', 'paparassi', 'папарацци', 'photographers who follow famous people', 'The paparazzi followed the star.', 'Paparassi ýyldyzyň yzyndan düşdi.', 'B1'),
    ('presenter', '/prɪˈzentə/', 'N', 'alyp baryjy', 'ведущий', 'a person who introduces a TV or radio show', 'She is a famous TV presenter.', 'Meşhur telewideniýe alyp baryjysy.', 'B1'),
    ('censored', '/ˈsensəd/', 'ADJ', 'senzura edilen', 'цензурированный', 'with parts removed because they are not approved', 'The film was censored in some countries.', 'Film käbir ýurtlarda senzura edildi.', 'B1'),
    ('objective', '/əbˈdʒektɪv/', 'ADJ', 'bitarap', 'объективный', 'not influenced by personal feelings', 'Try to be objective in your report.', 'Hasabatyňda bitarap bolmaga çalyş.', 'B1'),
    ('sensational', '/senˈseɪʃənl/', 'ADJ', 'sensasion, gyzykly görkezilen', 'сенсационный', 'made to seem more shocking than it is', 'The paper gave it a sensational headline.', 'Gazet oňa sensasion sözbaşy berdi.', 'B1'),
    ('accurate', '/ˈækjərət/', 'ADJ', 'takyk', 'точный', 'correct and without mistakes', 'The report was not accurate.', 'Hasabat takyk däldi.', 'B1'),
    ('row', '/raʊ/', 'N', 'dawa, jedel', 'скандал, ссора', 'an angry argument', 'There was a row about the decision.', 'Karar barada dawa boldy.', 'B1'),
    ('clash', '/klæʃ/', 'N', 'çaknyşyk, garşylyk', 'столкновение', 'a fight or strong disagreement', 'The clash lasted two hours.', 'Çaknyşyk iki sagat dowam etdi.', 'B1'),
    ('celebrity gossip', '/səˈlebrəti ˈɡɒsɪp/', 'N', 'ýyldyz gürrüňleri', 'сплетни о знаменитостях', 'stories about the private lives of famous people', 'The magazine is full of celebrity gossip.', 'Žurnal ýyldyz gürrüňlerine doly.', 'B1'),
    ('cable TV', '/ˈkeɪbl tiːˈviː/', 'N', 'kabelli telewideniýe', 'кабельное телевидение', 'TV sent to homes by cables', 'We have cable TV at home.', 'Öýümizde kabelli telewideniýe bar.', 'B1'),
]

# ---- Vocabulary Bank — Business + advertising -> 9A ----
T['business'] = [
    ('advertisement', '/ədˈvɜːtɪsmənt/', 'N', 'mahabat', 'рекламное объявление', 'a notice that sells a product', 'I saw the advertisement online.', 'Mahabady onlaýn gördüm.', 'A2', 'online advertisement'),
    ('brand', '/brænd/', 'N', 'marka', 'бренд, марка', 'a type of product with a name', 'Which brand of phone do you have?', 'Haýsy marka telefonyňyz bar?', 'A2', 'famous brand'),
    ('campaign', '/kæmˈpeɪn/', 'N', 'kampaniýa', 'кампания', 'an organised effort to achieve something', 'The ad campaign lasted three months.', 'Mahabat kampaniýasy üç aý dowam etdi.', 'B1', 'advertising campaign'),
    ('commercial', '/kəˈmɜːʃl/', 'N', 'mahabat roligi', 'рекламный ролик', 'an advertisement on TV or radio', 'The commercial was very funny.', 'Mahabat roligi gaty güldüriji boldy.', 'A2', 'TV commercial'),
    ('competitor', '/kəmˈpetɪtə(r)/', 'N', 'bäsdeş', 'конкурент', 'a company selling similar things', 'Our biggest competitor lowered prices.', 'Iň uly bäsdeşimiz bahalary peseltdi.', 'B1'),
    ('consumer', '/kənˈsjuːmə(r)/', 'N', 'sarp ediji', 'потребитель', 'a person who buys things', 'Consumers want lower prices.', 'Sarp edijiler arzan bahalary isleýär.', 'B1', 'consumer rights'),
    ('logo', '/ˈləʊɡəʊ/', 'N', 'logotip', 'логотип', 'a symbol that shows a company', 'The logo is a green leaf.', 'Logotip ýaşyl ýaprak.', 'A2'),
    ('slogan', '/ˈsləʊɡən/', 'N', 'şygar', 'слоган', 'a short phrase used in advertising', 'Their slogan is catchy.', 'Şygarlary ýatda galýan.', 'B1', 'company slogan'),
    ('target audience', '/ˈtɑːɡɪt ˈɔːdiəns/', 'N', 'nyşana tomaşaçylar', 'целевая аудитория', 'the people a product is for', 'The target audience is teenagers.', 'Nyşana tomaşaçylar ýetginjekler.', 'B2'),
    ('deal', '/diːl/', 'N', 'ylalaşyk (söwda)', 'сделка', 'a business agreement', 'They signed a big deal.', 'Uly ylalaşyga gol çekdiler.', 'A2', 'make a deal'),
    ('expenses', '/ɪkˈspensɪz/', 'N', 'çykdajylar', 'расходы', 'money spent on business costs', 'The company pays travel expenses.', 'Kompaniýa ýol çykdajylaryny töleýär.', 'B1', 'business expenses'),
    ('fee', '/fiː/', 'N', 'töleg (hyzmat)', 'плата за услугу', 'money paid for a service', 'There is a small fee for delivery.', 'Eltip bermek üçin kiçi töleg bar.', 'B1', 'pay a fee'),
    ('invoice', '/ˈɪnvɔɪs/', 'N', 'hasap-faktura', 'счёт-фактура', 'a bill for goods or work', 'Please pay the invoice this week.', 'Hasap-fakturany şu hepdede töläň.', 'B1', 'send an invoice'),
    ('profit', '/ˈprɒfɪt/', 'N', 'girdeji', 'прибыль', 'money left after costs', 'The shop made a small profit.', 'Dükan az girdeji gazandy.', 'A2', 'make a profit'),
    ('supplier', '/səˈplaɪə(r)/', 'N', 'üpjün ediji', 'поставщик', 'a company that provides goods', 'We changed our supplier in March.', 'Martda üpjün edijimizi çalyşdyk.', 'B1'),
    ('close down', '/ˌkləʊz ˈdaʊn/', 'PHR', 'ýapylmak', 'закрываться (о бизнесе)', 'to stop operating permanently', 'The factory closed down last year.', 'Zawod geçen ýyl ýapyldy.', 'B1'),
    ('expand', '/ɪkˈspænd/', 'V', 'giňeltmek', 'расширять', 'to make a business bigger', 'The company expanded into Asia.', 'Kompaniýa Aziýa giňeldi.', 'B1'),
    ('export', '/ɪkˈspɔːt/', 'V', 'eksport etmek', 'экспортировать', 'to sell goods to other countries', 'Turkey exports fruit to Europe.', 'Türkiýe Ýewropa miwe eksport edýär.', 'B1'),
    ('import', '/ɪmˈpɔːt/', 'V', 'import etmek', 'импортировать', 'to bring goods from other countries', 'We import coffee from Brazil.', 'Braziliýadan kofe import edýäris.', 'B1'),
    ('in order to', '/ɪn ˈɔːdə tə/', 'PHR', 'üçin, maksady bilen', 'для того чтобы', 'used to explain why you do something', 'She works hard in order to earn more.', 'Köp gazanmak üçin gaty işleýär.', 'B1'),
    ('so as to', '/ˌsəʊ əz ˈtə/', 'PHR', 'üçin', 'чтобы', 'used to explain the purpose of an action', 'He left early so as to avoid traffic.', 'Ulag köpçüliginden gaça durmak üçin ir çykdy.', 'B1'),
    ('so that', '/ˌsəʊ ˈðæt/', 'PHR', 'üçin, şonuň üçin', 'чтобы, так что', 'used to show the result or purpose', 'Speak clearly so that everyone understands.', 'Hemmeler düşener ýaly aýdyň gepläň.', 'B1'),
]

# ---- in-lesson 9B — word building ----
T['wordbuilding'] = [
    ('bilingual', '/ˌbaɪˈlɪŋɡwəl/', 'ADJ', 'iki dilli', 'двуязычный', 'able to speak two languages', 'She grew up bilingual.', 'Iki dilli bolup ulaldy.', 'B1'),
    ('decode', '/ˌdiːˈkəʊd/', 'V', 'koduny açmak', 'дешифровать', 'to change a code back to normal text', 'The team decoded the message.', 'Topar hatyň koduny açdy.', 'B2'),
    ('dishonest', '/dɪsˈɒnɪst/', 'ADJ', 'namart (dogruçyl däl)', 'нечестный', 'not telling the truth', 'He was dishonest about his age.', 'Ýaşy barada dogruçyl bolmady.', 'A2'),
    ('illogical', '/ɪˈlɒdʒɪkl/', 'ADJ', 'logikasyz', 'нелогичный', 'not sensible', 'His illogical answer confused us.', 'Logikasyz jogaby bizi bulaşdyrdy.', 'B1'),
    ('impossible', '/ɪmˈpɒsəbl/', 'ADJ', 'mümkin däl', 'невозможный', 'cannot be done', 'The task seemed impossible.', 'Tabşyryk mümkin däl ýaly boldy.', 'A2'),
    ('irregular', '/ɪˈreɡjələ(r)/', 'ADJ', 'kadasyz', 'неправильный, нерегулярный', 'not following the normal pattern', 'The verb has an irregular past form.', 'Işligiň kadasyz öten zaman görnüşi bar.', 'B1', 'irregular verbs'),
    ('misunderstand', '/ˌmɪsʌndəˈstænd/', 'V', 'nädogry düşünmek', 'неправильно понять', 'to understand something wrongly', 'I misunderstood the instructions.', 'Görkezmeleri nädogry düşündim.', 'B1', 'misunderstand someone'),
    ('nonsense', '/ˈnɒnsns/', 'N', 'manyşyz söz', 'чепуха', 'words that make no sense', 'That story is complete nonsense.', 'Ol hekaýa düýbünden manyşyz.', 'B1', 'talk nonsense'),
    ('overweight', '/ˌəʊvəˈweɪt/', 'ADJ', 'agramly (artykmaç)', 'с избыточным весом', 'weighing more than is healthy', 'The doctor said he was overweight.', 'Lukman agramynyň artykdygyny aýtdy.', 'A2'),
    ('rebuild', '/ˌriːˈbɪld/', 'V', 'täzeden gurmak', 'восстанавливать', 'to build again', 'They rebuilt the bridge after the flood.', 'Suw joşmasyndan soň köprini täzeden gurdular.', 'B1', 'rebuild a house'),
    ('submarine', '/ˌsʌbməˈriːn/', 'N', 'suwasty gämi', 'подводная лодка', 'a ship that travels under water', 'The submarine dived deep.', 'Suwasty gämi çuňňur çümdi.', 'A2'),
    ('supernatural', '/ˌsuːpəˈnætʃrəl/', 'ADJ', 'tebigatdan daşary', 'сверхъестественный', 'not explainable by nature', 'They told supernatural stories.', 'Tebigatdan daşary hekaýalar gürrüň berdiler.', 'B1'),
    ('unfair', '/ˌʌnˈfeə(r)/', 'ADJ', 'adalatsyz', 'несправедливый', 'not right or fair', 'The rules were unfair to beginners.', 'Düzgünler başlangyçlar üçin adalatsyz boldy.', 'A2'),
    ('unfortunately', '/ʌnˈfɔːtʃənətli/', 'ADV', 'gynansak-da', 'к сожалению', 'used for bad news', 'Unfortunately, the shop was closed.', 'Gynansak-da, dükan ýapykdy.', 'A2'),
    ('unlock', '/ˌʌnˈlɒk/', 'V', 'gulpy açmak', 'отпирать', 'to open a lock', 'She unlocked the front door.', 'Öý gapysynyň gulpuny açdy.', 'A2', 'unlock the door'),
    ('underestimate', '/ˌʌndərˈestɪmeɪt/', 'V', 'pes görmek', 'недооценивать', 'to think something is less than it is', 'Never underestimate your opponent.', 'Bäsdeşiňizi hiç wagt pes görmäň.', 'B1', 'underestimate someone'),
    ('antivirus', '/ˌæntiˈvaɪrəs/', 'ADJ', 'antivirus', 'антивирусный', 'against computer viruses', 'Install antivirus software.', 'Antivirus programmasyny gurna.', 'B1'),
    ('improvement', '/ɪmˈpruːvmənt/', 'N', 'gowulandyrma, gowulaşma', 'улучшение', 'when something gets better', 'There has been a big improvement in his English.', 'Iňlis dilinde uly gowulaşma bar.', 'B1'),
    ('inflation', '/ɪnˈfleɪʃn/', 'N', 'inflýasiýa', 'инфляция', 'when prices rise over time', 'Inflation reached five percent.', 'Inflýasiýa bäş göterime ýetdi.', 'B1'),
    ('loss', '/lɒs/', 'N', 'ýitgi', 'потеря, убыток', 'when you lose something or money', 'The company reported a loss.', 'Kompaniýa ýitgi barada hasabat berdi.', 'B1'),
    ('megabyte', '/ˈmeɡəbaɪt/', 'N', 'megabaýt', 'мегабайт', 'a unit of computer memory', 'The file is 500 megabytes.', 'Faýl 500 megabaýt.', 'B1'),
    ('monolingual', '/ˌmɒnəˈlɪŋɡwəl/', 'ADJ', 'bir dilli', 'одноязычный', 'using or speaking only one language', 'He grew up in a monolingual family.', 'Bir dilli maşgalada ulaldy.', 'B2'),
    ('multimillionaire', '/ˌmʌltimɪljəˈneə/', 'N', 'multimillioner', 'мультимиллионер', 'a person who is extremely rich', 'He became a multimillionaire at thirty.', 'Otuz ýaşynda multimillioner boldy.', 'B1'),
    ('recognizable', '/ˈrekəɡnaɪzəbl/', 'ADJ', 'tanaýjy, tanar ýaly', 'узнаваемый', 'able to be recognized', 'She is recognizable by her red hair.', 'Gyzyl saçyndan tanaýar ýaly.', 'B1'),
    ('sleepless', '/ˈsliːpləs/', 'ADJ', 'ukusyz', 'бессонный', 'without sleep', 'After a sleepless night he felt awful.', 'Ukusyz gijeden soň erbet duýdy.', 'B1'),
    ('success', '/səkˈses/', 'N', 'üstünlik', 'успех', 'when something works well', 'The business was a great success.', 'Biznes uly üstünlik boldy.', 'B1'),
    ('belief', '/bɪˈliːf/', 'N', 'ynanç', 'вера, убеждение', 'a feeling that something is true', 'Her belief in him never changed.', 'Oňa bolan ynamy hiç üýtgemedi.', 'B1'),
    ('death', '/deθ/', 'N', 'ölüm', 'смерть', 'when someone dies', 'His death shocked everyone.', 'Onuň ölümü hemmäni haýran galdyrdy.', 'B1'),
    ('height', '/haɪt/', 'N', 'boý, beýiklik', 'рост, высота', 'how tall someone or something is', 'What is your height?', 'Boýuň näçe?', 'A2'),
    ('hunger', '/ˈhʌŋɡə/', 'N', 'açlyk', 'голод', 'the feeling of needing food', 'Hunger made him angry.', 'Açlyk ony gaharly etdi.', 'B1'),
    ('thought', '/θɔːt/', 'N', 'pikir', 'мысль', 'an idea in your mind', 'He was lost in thought.', 'Pikire gark bolupdy.', 'B1'),
    ('width', '/wɪdθ/', 'N', 'ini, giňlik', 'ширина', 'how wide something is', 'Measure the width of the door.', 'Gapynyň inini ölçäň.', 'B1'),
]

# ---- in-lesson 10A — science ----
T['science'] = [
    ('astronomer', '/əˈstrɒnəmə(r)/', 'N', 'astronom', 'астроном', 'a scientist who studies stars', 'The astronomer found a new planet.', 'Astronom täze planetany tapdy.', 'B1'),
    ('biology', '/baɪˈɒlədʒi/', 'N', 'biologiýa', 'биология', 'the science of living things', 'She studies biology at university.', 'Uniwersitetde biologiýa okaýar.', 'A2', 'study biology'),
    ('chemistry', '/ˈkemɪstri/', 'N', 'himiýa', 'химия', 'the science of substances', 'Chemistry was his favourite subject.', 'Himiýa onuň iň söýýän dersidi.', 'A2', 'chemistry lesson'),
    ('experiment', '/ɪkˈsperɪmənt/', 'N', 'eksperiment', 'эксперимент', 'a test to learn something', 'The experiment proved the theory.', 'Eksperiment teoriýany subut etdi.', 'A2', 'do an experiment'),
    ('hypothesis', '/haɪˈpɒθəsɪs/', 'N', 'çaklama', 'гипотеза', 'an idea that you test', 'The data supported the hypothesis.', 'Maglumatlar çaklamany goldady.', 'B2', 'test a hypothesis'),
    ('laboratory', '/ləˈbɒrətri/', 'N', 'laboratoriýa', 'лаборатория', 'a room for scientific work', 'The laboratory is on the second floor.', 'Laboratoriýa ikinji gatda.', 'A2', 'research laboratory'),
    ('physics', '/ˈfɪzɪks/', 'N', 'fizika', 'физика', 'the science of matter and energy', 'Physics explains how light travels.', 'Fizika ýagtylygyň nähili hereket edýändigini düşündirýär.', 'A2'),
    ('researcher', '/rɪˈsɜːtʃə(r)/', 'N', 'barlagçy', 'исследователь', 'a person who does scientific study', 'The researchers published their findings.', 'Barlagçylar netijelerini çap etdi.', 'A2'),
    ('scientist', '/ˈsaɪəntɪst/', 'N', 'alym', 'учёный', 'a person who does science', 'The scientist won a prize.', 'Alym baýrak aldy.', 'A2'),
    ('species', '/ˈspiːʃiːz/', 'N', 'görnüş (janly)', 'вид (биологический)', 'a type of animal or plant', 'This species lives only in deserts.', 'Bu görnüş diňe çöllerde ýaşaýar.', 'A2'),
    ('telescope', '/ˈtelɪskəʊp/', 'N', 'teleskop', 'телескоп', 'an instrument for seeing far objects', 'We watched the moon through a telescope.', 'Aýa teleskop arkaly seretdik.', 'A2'),
    ('theory', '/ˈθɪəri/', 'N', 'teoriýa', 'теория', 'an idea that explains something', 'His theory explains the results.', 'Teoriýasy netijeleri düşündirýär.', 'A2', 'scientific theory'),
    ('cell', '/sel/', 'N', 'öýjük', 'клетка', 'the smallest unit of a living thing', 'Every cell contains DNA.', 'Her öýjükde DNK bar.', 'A2', 'brain cell'),
    ('data', '/ˈdeɪtə/', 'N', 'maglumatlar', 'данные', 'facts and numbers collected', 'The data shows a clear trend.', 'Maglumatlar aýdyň tendensiýany görkezýär.', 'A2', 'collect data'),
    ('gravity', '/ˈɡrævəti/', 'N', 'dartyş güýji', 'гравитация', 'the force that pulls things down', 'Gravity makes apples fall.', 'Dartyş güýji almalary gaçyrýar.', 'A2'),
    ('invention', '/ɪnˈvenʃn/', 'N', 'oýlap tapyş', 'изобретение', 'something new that is created', 'The internet was a huge invention.', 'Internet uly oýlap tapyş boldy.', 'A2', 'great invention'),
    ('solar', '/ˈsəʊlə(r)/', 'ADJ', 'gün (energiýasy)', 'солнечный', 'using energy from the sun', 'They installed solar panels.', 'Gün panellerini oturdylar.', 'A2', 'solar energy'),
    ('substance', '/ˈsʌbstəns/', 'N', 'madda', 'вещество', 'a type of material', 'The substance was completely safe.', 'Madda düýbünden howpsuz boldy.', 'B1', 'toxic substance'),
]

# ---- in-lesson 10B — collocation: word pairs ----
T['word_pairs'] = [
    ('make a decision', '/meɪk ə dɪˈsɪʒn/', 'PHR', 'karar bermek', 'принять решение', 'to decide something', 'We made a decision together.', 'Karary bile berdik.', 'A2'),
    ('do research', '/duː rɪˈsɜːtʃ/', 'PHR', 'barlag geçirmek', 'проводить исследование', 'to study a subject carefully', 'She did research on sleep.', 'Uky barada barlag geçirdi.', 'A2'),
    ('take a photo', '/teɪk ə ˈfəʊtəʊ/', 'PHR', 'surata düşürmek', 'сфотографировать', 'to use a camera', 'Let me take a photo of you.', 'Siziň suratyňyzy düşüreýin.', 'A1'),
    ('have a rest', '/hæv ə rest/', 'PHR', 'dynç almak', 'отдохнуть', 'to relax for a while', 'Have a rest before the match.', 'Oýundan öň dynç al.', 'A2'),
    ('pay attention', '/peɪ əˈtenʃn/', 'PHR', 'üns bermek', 'обращать внимание', 'to listen or watch carefully', 'Pay attention to the safety rules.', 'Howpsuzlyk düzgünlerine üns beriň.', 'A2', 'pay attention to'),
    ('keep a secret', '/kiːp ə ˈsiːkrət/', 'PHR', 'sir saklamak', 'хранить секрет', 'to not tell a secret', 'She can never keep a secret.', 'Ol hiç wagt sir saklap bilmeýär.', 'A2'),
    ('catch a cold', '/kætʃ ə kəʊld/', 'PHR', 'sowuklamak', 'простудиться', 'to become ill with a cold', 'I caught a cold in winter.', 'Gyşda sowukladym.', 'A2'),
    ('break a record', '/breɪk ə ˈrekɔːd/', 'PHR', 'rekord goýmak', 'побить рекорд', 'to do better than before', 'He broke a record in the 100 metres.', '100 metrde rekord goýdy.', 'A2'),
    ('give advice', '/ɡɪv ədˈvaɪs/', 'PHR', 'maslahat bermek', 'дать совет', 'to tell someone what to do', 'My teacher gave me good advice.', 'Mugallymym maňa gowy maslahat berdi.', 'A2'),
    ('spend time', '/spend taɪm/', 'PHR', 'wagt geçirmek', 'проводить время', 'to use time doing something', 'I spend time with my family at weekends.', 'Hepde ahyrynda maşgalam bilen wagt geçirýärin.', 'A1'),
    ('tell the truth', '/tel ðə truːθ/', 'PHR', 'hakykaty aýtmak', 'говорить правду', 'to say what is true', 'He always tells the truth.', 'Ol hemişe hakykaty aýdýar.', 'A2'),
    ('do your best', '/duː jɔː(r) best/', 'PHR', 'elinizden geleni etmek', 'сделать всё возможное', 'to try as hard as you can', 'Just do your best in the exam.', 'Synagda elinizden geleni ediň.', 'A2'),
]

# ---- Colloquial English episodes ----
T['ce_job'] = [
    ('What do you do?', '/wɒt du ju duː/', 'PHR', 'Näme işleýärsiň?', 'Кем вы работаете?', 'used to ask about someone\'s job', 'What do you do? — I am a nurse.', 'Näme işleýärsiň? — Şepagat uýasy.', 'A1'),
    ('I\'m looking for...', '/aɪm ˈlʊkɪŋ fə(r)/', 'PHR', 'Gözleýärin...', 'Я ищу...', 'used to say what you want', 'I am looking for a part-time job.', 'Ýarym ştatly iş gözleýärin.', 'A2'),
    ('Do you have any experience?', '/du ju hæv ˈeni ɪkˈspɪəriəns/', 'PHR', 'Tejribäňiz barmy?', 'У вас есть опыт?', 'used to ask about past work', 'Do you have any experience in sales?', 'Satuwda tejribäňiz barmy?', 'A2'),
    ('When can you start?', '/wen kæn ju stɑːt/', 'PHR', 'Haçan başlap bilersiňiz?', 'Когда вы можете начать?', 'used to ask about availability', 'When can you start? — On Monday.', 'Haçan başlap bilersiňiz? — Duşenbe.', 'A2'),
    ('What are your strengths?', '/wɔːr ər jɔː(r) streŋθs/', 'PHR', 'Güýçli taraplaryňyz näme?', 'Каковы ваши сильные стороны?', 'used to ask about good points', 'What are your strengths? — Teamwork.', 'Güýçli taraplaryňyz näme? — Toparlaşyp işlemek.', 'B1'),
    ('I\'m a hard worker.', '/aɪm ə hɑːd ˈwɜːkə(r)/', 'PHR', 'Zähmetsöýer adam.', 'Я трудолюбивый человек.', 'used to praise your own effort', 'I am a hard worker and a quick learner.', 'Zähmetsöýer we çalt öwrenýän adam.', 'A2'),
    ('Can you send me your CV?', '/kæn ju send miː jɔː(r) ˌsiː ˈviː/', 'PHR', 'Te terjimehalyňyzy iberip bilersiňizmi?', 'Можете прислать резюме?', 'used to ask for a CV', 'Can you send me your CV by email?', 'Te terjimehalyňyzy email bilen iberip bilersiňizmi?', 'B1'),
    ('We\'ll be in touch.', '/wil bi ɪn tʌtʃ/', 'PHR', 'Habarlaşarys.', 'Мы с вами свяжемся.', 'used to promise contact later', 'Thank you — we will be in touch.', 'Sag boluň — habarlaşarys.', 'A2'),
]

T['ce_books'] = [
    ('What\'s it about?', '/wɒts ɪt əˈbaʊt/', 'PHR', 'Näme barada?', 'О чём она?', 'used to ask about a story', 'What is it about? — A family in wartime.', 'Näme barada? — Uruş wagtyndaky maşgala.', 'A1'),
    ('I couldn\'t put it down.', '/aɪ ˈkʊdnt pʊt ɪt daʊn/', 'PHR', 'Elimden goýup bilmedim.', 'Я не мог оторваться.', 'used to say a book is exciting', 'It was so good I could not put it down.', 'Şeýle gowudy, elimden goýup bilmedim.', 'A2'),
    ('It\'s a real page-turner.', '/ɪts ə rɪəl peɪdʒ ˈtɜːnə(r)/', 'PHR', 'Hakyky gyzykly kitap.', 'Это настоящий увлекательный роман.', 'used to praise a book', 'The thriller is a real page-turner.', 'Triller hakyky gyzykly kitap.', 'B1'),
    ('Who\'s the author?', '/huːz ði ˈɔːθə(r)/', 'PHR', 'Awtory kim?', 'Кто автор?', 'used to ask who wrote a book', 'Who is the author of this novel?', 'Bu romanyň awtory kim?', 'A2'),
    ('I\'m halfway through.', '/aɪm ˌhɑːfˈweɪ θruː/', 'PHR', 'Ýarysyna ýetdim.', 'Я на середине.', 'used to say how far you have read', 'I am halfway through the second book.', 'Ikinji kitabyň ýarysyna ýetdim.', 'A2'),
    ('It\'s set in...', '/ɪts set ɪn/', 'PHR', 'Wakasy ... geçýär', 'Действие происходит в...', 'used to say where a story happens', 'It is set in 1930s Istanbul.', 'Wakasy 1930-njy ýyllaryň Stambulynda geçýär.', 'A2'),
    ('I\'d recommend it.', '/aɪd ˌrekəˈmend ɪt/', 'PHR', 'Maslahat bererdim.', 'Я бы рекомендовал.', 'used to suggest a book', 'I would recommend it to anyone.', 'Hemmä maslahat bererdim.', 'A2'),
    ('It didn\'t live up to the hype.', '/ɪt ˈdɪdnt lɪv ʌp tuː ðə haɪp/', 'PHR', 'Mahabatyna ýetmedi.', 'Не оправдал ожиданий.', 'used to say a book disappointed', 'Honestly, it did not live up to the hype.', 'Dogrusy, mahabatyna ýetmedi.', 'B2'),
]

T['ce_waste'] = [
    ('That\'s a waste of time.', '/ðæts ə weɪst əv taɪm/', 'PHR', 'Wagtyň isribi.', 'Это пустая трата времени.', 'used to say something is useless', 'Waiting in that queue is a waste of time.', 'Şol nobatda durmak wagtyň isribi.', 'A2'),
    ('Don\'t throw it away.', '/dəʊnt θrəʊ ɪt əˈweɪ/', 'PHR', 'Ony zyňma.', 'Не выбрасывай это.', 'used to tell someone to keep something', 'Do not throw it away — fix it.', 'Ony zyňma — bejer.', 'A2'),
    ('You could recycle it.', '/ju kʊd ˌriːˈsaɪkl ɪt/', 'PHR', 'Gaýtadan işledip bilersiň.', 'Можно сдать в переработку.', 'used to suggest reusing waste', 'You could recycle it instead.', 'Munuň ýerine gaýtadan işledip bilersiň.', 'A2'),
    ('It\'s still in good condition.', '/ɪts stɪl ɪn ɡʊd kənˈdɪʃn/', 'PHR', 'Entek gowy ýagdaýda.', 'Он ещё в хорошем состоянии.', 'used to say something still works', 'The bike is still in good condition.', 'Welosiped entek gowy ýagdaýda.', 'A2'),
    ('Why don\'t you sell it?', '/waɪ dəʊnt ju sel ɪt/', 'PHR', 'Ony satmasaň?', 'Почему бы не продать?', 'used to suggest selling', "Why don't you sell it online?", 'Ony onlaýn satmasaň?', 'A2'),
    ('I never use it.', '/aɪ ˈnevə juːz ɪt/', 'PHR', 'Ony hiç ulananok.', 'Я им никогда не пользуюсь.', 'used to explain why you keep something', 'I never use it, but I cannot throw it away.', 'Hiç ulananok, ýöne zyňyp bilemok.', 'A2'),
    ('It\'s gone to waste.', '/ɪts ɡɒn tu weɪst/', 'PHR', 'Isrip boldy.', 'Это пропало зря.', 'used to say something was not used', 'All that food has gone to waste.', 'Şol naharyň hemmesi isrip boldy.', 'A2'),
    ('Let\'s clear out the attic.', '/lets klɪər aʊt ði ˈætɪk/', 'PHR', 'Geliň, ýerligi arassalalyň.', 'Давай разберём чердак.', 'used to suggest tidying a space', 'Let us clear out the attic this weekend.', 'Geliň, şu hepde ahyry ýerligi arassalalyň.', 'B1'),
]

T['ce_performances'] = [
    ('How was the show?', '/haʊ wɒz ðə ʃəʊ/', 'PHR', 'Tomaşa nädip boldy?', 'Как прошло шоу?', 'used to ask about a performance', 'How was the show? — Brilliant!', 'Tomaşa nädip boldy? — Ajaýyp!', 'A1'),
    ('The acting was brilliant.', '/ði ˈæktɪŋ wɒz ˈbrɪliənt/', 'PHR', 'Aktýorlyk ajaýyp boldy.', 'Игра актёров была великолепна.', 'used to praise the actors', 'The acting was brilliant from start to finish.', 'Aktýorlyk başdan ahyryna ajaýyp boldy.', 'A2'),
    ('I was on the edge of my seat.', '/aɪ wɒz ɒn ði edʒ əv maɪ siːt/', 'PHR', 'Ynjalyksyzlyk bilen tomaşa etdim.', 'Я был на краю кресла (в напряжении).', 'used to say a show was exciting', 'The final act — I was on the edge of my seat.', 'Soňky perde — ynjalyksyzlyk bilen tomaşa etdim.', 'B1'),
    ('It was a sell-out.', '/ɪt wɒz ə sel aʊt/', 'PHR', 'Biletler gutardy.', 'Билеты были полностью распроданы.', 'used to say every seat was sold', 'The first night was a sell-out.', 'Ilkinji agşam biletler gutardy.', 'B1'),
    ('The plot was hard to follow.', '/ðə plɒt wɒz hɑːd tuː ˈfɒləʊ/', 'PHR', 'Wakasy kyn düşündi.', 'Сюжет было трудно понять.', 'used to criticise a story', 'The plot was hard to follow at first.', 'Wakasy başda kyn düşündi.', 'A2'),
    ('It\'s on again tonight.', '/ɪts ɒn əˈɡen təˈnaɪt/', 'PHR', 'Şu agşam ýene bar.', 'Сегодня снова идёт.', 'used to say a show repeats', 'The play is on again tonight at eight.', 'Oýun şu agşam sekizde ýene bar.', 'A2'),
    ('They got a standing ovation.', '/ðeɪ ɡɒt ə ˈstændɪŋ əʊˈveɪʃn/', 'PHR', 'Aýaga galyp el çarpyldy.', 'Им устроили овацию стоя.', 'used to describe strong applause', 'The dancers got a standing ovation.', 'Tansçylara aýaga galyp el çarpyldy.', 'B2'),
    ('I couldn\'t hear a word.', '/aɪ ˈkʊdnt hɪər ə wɜːd/', 'PHR', 'Hiç zat eşitmedim.', 'Я не слышал ни слова.', 'used to complain about sound', 'The music was so loud I could not hear a word.', 'Saz şeýle güýçlidi, hiç zat eşitmedim.', 'A2'),
]

T['ce_advertising'] = [
    ('I saw this ad everywhere.', '/aɪ sɔː ðɪs æd ˈevriweə(r)/', 'PHR', 'Bu mahabady her ýerde gördüm.', 'Я видел эту рекламу везде.', 'used to talk about an advertisement', 'I saw this ad everywhere last month.', 'Geçen aý bu mahabady her ýerde gördüm.', 'A2'),
    ('It\'s a catchy slogan.', '/ɪts ə ˈkætʃi ˈsləʊɡən/', 'PHR', 'Ýatda galýan şygar.', 'Это запоминающийся слоган.', 'used to praise an ad line', 'Their new slogan is really catchy.', 'Täze şygarlary hakykatdan ýatda galýan.', 'A2'),
    ('Does it live up to its promises?', '/dʌz ɪt lɪv ʌp tuː ɪts ˈprɒmɪsɪz/', 'PHR', 'Wadalaryna ýetýärmi?', 'Оно оправдывает обещания?', 'used to question a claim', 'The product looks good, but does it live up to its promises?', 'Haryt gowy görünýär, ýöne wadalaryna ýetýärmi?', 'B2'),
    ('I\'m not convinced.', '/aɪm nɒt kənˈvɪnst/', 'PHR', 'Ynanamok.', 'Я не убеждён.', 'used to express doubt', 'Interesting claims, but I am not convinced.', 'Gyzykly tassyklamalar, ýöne ynanamok.', 'A2'),
    ('It\'s just a gimmick.', '/ɪts dʒʌst ə ˈɡɪmɪk/', 'PHR', 'Bu diňe hiyle.', 'Это просто уловка.', 'used to call something a trick', 'The free gift is just a gimmick.', 'Mugt sowgat diňe hiyle.', 'B2'),
    ('word of mouth', '/wɜːd əv maʊθ/', 'PHR', 'agyzdan-agza', 'из уст в уста', 'people telling other people', 'The shop grew through word of mouth.', 'Dükan agyzdan-agza ulaldy.', 'B1', 'spread by word of mouth'),
    ('It went viral.', '/ɪt went ˈvaɪrəl/', 'PHR', 'Internetde ýaýrady.', 'Это стало вирусным.', 'used when something spreads online fast', 'The video went viral overnight.', 'Wideo bir gijede internetde ýaýrady.', 'A2'),
    ('buy one get one free', '/baɪ wʌn ɡet wʌn friː/', 'PHR', 'birini al, birini mugt al', 'купи один — второй бесплатно', 'a common sales offer', 'The biscuits are buy one get one free.', 'Kökeler birini al, birini mugt al.', 'A2'),
]
LESSONS = {
    '1A': (1,  'Questions and answers', 'getting a job', ['job_hunting']),
    '1B': (1,  "It's a mystery", 'compound adjectives', ['compound_adjs']),
    '2A': (2,  'Doctor, doctor!', 'illnesses and injuries', ['illnesses']),
    '2B': (2,  'Act your age', 'clothes and fashion', ['clothes']),
    '3A': (3,  'Fasten your seat belts', 'air travel', ['air_travel']),
    '3B': (3,  'A really good ending?', 'adverbs and adverbial phrases', ['adverbs']),
    '4A': (4,  'Stormy weather', 'weather · the environment', ['weather']),
    '4B': (4,  'A risky business', 'expressions with take', ['take']),
    '5A': (5,  "I'm a survivor", 'feelings', ['feelings_adj']),
    '5B': (5,  'Wish you were here', 'expressing feelings', ['feelings_verbs']),
    '6A': (6,  'Night night', 'sleep', ['sleep']),
    '6B': (6,  'Music to my ears', 'music', ['music']),
    '7A': (7,  "Let's not argue", 'verbs often confused', ['confused_verbs']),
    '7B': (7,  "It's all an act", 'the body', ['body']),
    '8A': (8,  'Cutting crime', 'crime and punishment', ['crime']),
    '8B': (8,  'Fake news', 'the media', ['media']),
    '9A': (9,  'Good business?', 'advertising · business', ['business']),
    '9B': (9,  'Super cities', 'word building: prefixes and suffixes', ['wordbuilding']),
    '10A': (10, 'Science fact, science-fiction', 'science', ['science']),
    '10B': (10, 'Free speech', 'collocation: word pairs', ['word_pairs']),
}

WORD_LESSON = {}


def lesson_for(topic, en, fallback):
    key = en.strip().lower()
    return WORD_LESSON.get(key, fallback)


# Upper-Intermediate has ten units; the five Colloquial English episodes sit
# after units 1, 3, 5, 7 and 9 in the book. In the data they carry unit 11 so
# they do not collide with the real units, and the app shows each episode
# right after the unit it follows.
PE_UNIT = 11
for code, n, title, topic, key in (
    ('CE1', 11, 'Talking about getting a job', 'colloquial English 1', 'ce_job'),
    ('CE2', 11, 'Talking about books', 'colloquial English 2 and 3', 'ce_books'),
    ('CE3', 11, 'Talking about waste', 'colloquial English 4 and 5', 'ce_waste'),
    ('CE4', 11, 'Talking about performances', 'colloquial English 6 and 7', 'ce_performances'),
    ('CE5', 11, 'Talking about advertising', 'colloquial English 8 and 9', 'ce_advertising'),
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
                    'books': [{'book': 'upp', 'unit': unit, 'lesson': lesson, 'page': PAGE.get(lesson)}],
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
        'book': 'upp',
        'title': 'English File Upper-Intermediate (4th edition) — vocabulary, by lesson',
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
