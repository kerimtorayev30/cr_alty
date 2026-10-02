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
# SB pages from the syllabus checklist (TG pp.4-6), verified against the TG.
PAGE = {
    '1A': 6, '1B': 10, '2A': 16, '2B': 20, '3A': 26, '3B': 30,
    '4A': 36, '4B': 40, '5A': 46, '5B': 50, '6A': 56, '6B': 60,
    '7A': 66, '7B': 70, '8A': 76, '8B': 80, '9A': 86, '9B': 90,
    '10A': 96, '10B': 100,
    'PE1': 14, 'PE2': 34, 'PE3': 54, 'PE4': 74, 'PE5': 94,
}

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
    ('affectionate', '/əˈfekʃənət/', 'ADJ', 'mähirli', 'ласковый', 'showing love for people', 'She is affectionate with her children.', 'Çagalary bilen mähirli.', 'B1'),
    ('assertive', '/əˈsɜːtɪv/', 'ADJ', 'özüni ynamly alyp barýan', 'напористый, уверенный', 'saying clearly what you want and believe', 'You need to be more assertive at work.', 'Işde has ynamly bolmaly.', 'B2'),
    ('creative', '/kriˈeɪtɪv/', 'ADJ', 'döredijilikli', 'творческий, креативный', 'good at thinking of new ideas', 'She has a creative job.', 'Döredijilikli işi bar.', 'B1'),
    ('envious', '/ˈenviəs/', 'ADJ', 'görip', 'завистливый', 'wanting something that someone else has', 'I am envious of your new car.', 'Täze ulagyňa görip.', 'B1'),
    ('glamorous', '/ˈɡlæmərəs/', 'ADJ', 'özüne çekiji, kaşaň', 'гламурный, блестящий', 'attractive and exciting', 'Actors have glamorous lives.', 'Aktýorlaryň durmuşy kaşaň.', 'B1'),
    ('helpful', '/ˈhelpfl/', 'ADJ', 'peýdaly, kömekçi', 'отзывчивый, полезный', 'giving help', 'The staff were very helpful.', 'Işgärler gaty kömekçidi.', 'A2'),
    ('hopeful', '/ˈhəʊpfl/', 'ADJ', 'umytly', 'исполненный надежды', 'feeling that something good will happen', 'She is hopeful about the future.', 'Geljege umytly.', 'B1'),
    ('impressive', '/ɪmˈpresɪv/', 'ADJ', 'täsirli', 'впечатляющий', 'making you admire it', 'The view from the top was impressive.', 'Depedäniň görnüşi täsirli boldy.', 'B1'),
    ('impulsive', '/ɪmˈpʌlsɪv/', 'ADJ', 'hyjuwly, oýlanyşyksyz', 'импульсивный', 'doing things suddenly without thinking', 'He is impulsive and spends too much.', 'Oýlanyşyksyz we köp sarp edýär.', 'B1'),
    ('noisy', '/ˈnɔɪzi/', 'ADJ', 'galmagally', 'шумный', 'making a lot of noise', 'The neighbours are very noisy.', 'Goňşular gaty galmagally.', 'A2'),
    ('powerful', '/ˈpaʊəfl/', 'ADJ', 'güýçli', 'могущественный, мощный', 'very strong', 'He is a powerful man.', 'Ol güýçli adam.', 'B1'),
    ('profitable', '/ˈprɒfɪtəbl/', 'ADJ', 'bähbitli, girdejili', 'прибыльный', 'making a lot of money', 'The business was very profitable.', 'Biznes gaty girdejilidi.', 'B1'),
    ('rebellious', '/rɪˈbeljəs/', 'ADJ', 'boýun egmeýän, garşylykly', 'бунтарский, непокорный', 'refusing to obey rules', 'She was rebellious as a teenager.', 'Ýetginjek wagty boýun egmeýärdi.', 'B1'),
    ('reliable', '/rɪˈlaɪəbl/', 'ADJ', 'ynançly', 'надёжный', 'someone you can trust', 'He is a reliable friend.', 'Ynançly dost.', 'B1'),
    ('restful', '/ˈrestfl/', 'ADJ', 'dynç beriji', 'успокаивающий', 'quiet and relaxing', 'The hotel was calm and restful.', 'Myhmanhana asuda we dynç berijidi.', 'B1'),
    ('risky', '/ˈrɪski/', 'ADJ', 'howply', 'рискованный', 'possibly dangerous', 'It is risky to drive so fast.', 'Beýle çalt sürmek howply.', 'B1'),
    ('sociable', '/ˈsəʊʃəbl/', 'ADJ', 'jemgyýetçil', 'общительный', 'enjoying the company of other people', 'She is friendly and sociable.', 'Ol dostlukly we jemgyýetçil.', 'B1'),
    ('spacious', '/ˈspeɪʃəs/', 'ADJ', 'giň', 'просторный', 'with a lot of space', 'The flat is bright and spacious.', 'Öý ýagty we giň.', 'B1'),
    ('suitable', '/ˈsuːtəbl/', 'ADJ', 'amatly, laýyk', 'подходящий', 'right for a particular purpose', 'This film is not suitable for children.', 'Bu film çagalar üçin laýyk däl.', 'B1'),
    ('careless', '/ˈkeələs/', 'ADJ', 'biperwaý', 'небрежный, невнимательный', 'not taking enough care', 'He made a careless mistake.', 'Biperwaý ýalňyşlyk goýberdi.', 'B1'),
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
    ('batteries', '/ˈbætriz/', 'N', 'batareýler', 'батарейки', 'small objects that give power to things', 'Take spare batteries for the camera.', 'Fotoapparat üçin ätiýaç batareý al.', 'A2'),
    ('bathrobe', '/ˈbɑːθrəʊb/', 'N', 'hamam dony', 'банный халат', 'a loose coat you wear after a bath', 'The hotel provides a bathrobe.', 'Myhmanhana hamam dony berýär.', 'B1'),
    ('beach bag', '/ˈbiːtʃ bæɡ/', 'N', 'kenar torbasy', 'пляжная сумка', 'a bag you take to the beach', 'Put the towel in the beach bag.', 'Däsmaly kenar torbasyna sal.', 'A2'),
    ('deodorant', '/diˈəʊdərənt/', 'N', 'dezodorant', 'дезодорант', 'a substance you use to stop body smell', 'Do not forget your deodorant.', 'Dezodorantyňy unutma.', 'B1'),
    ('earphones', '/ˈɪəfəʊnz/', 'N', 'gulaklyk', 'наушники (вкладыши)', 'small speakers you put in your ears', 'He listens to music with earphones.', 'Gulaklyk bilen aýdym diňleýär.', 'B1'),
    ('hairdryer', '/ˈheədraɪə/', 'N', 'saç guradyjy', 'фен', 'a machine that dries your hair', 'Is there a hairdryer in the room?', 'Otagda saç guradyjy barmy?', 'A2'),
    ('headphones', '/ˈhedfəʊnz/', 'N', 'gulaklyk (uly)', 'наушники', 'speakers you wear over your ears', 'She wears big headphones on the plane.', 'Uçarda uly gulaklyk geýýär.', 'A2'),
    ('make-up', '/ˈmeɪkʌp/', 'N', 'ýüz boýagy', 'макияж, косметика', 'coloured substances women put on their faces', 'She does not wear much make-up.', 'Köp makiýaž ulanmaýar.', 'A2'),
    ('pack of cards', '/ˌpæk əv ˈkɑːdz/', 'N', 'kagyz oýun toplumy', 'колода карт', 'a set of playing cards', 'Take a pack of cards for the journey.', 'Ýol üçin kagyz oýun toplumyny al.', 'A2'),
    ('pyjamas', '/pəˈdʒɑːməz/', 'N', 'pijama', 'пижама', 'clothes you wear in bed', 'I packed two pairs of pyjamas.', 'Iki pijama ýygnadym.', 'A2'),
    ('scissors', '/ˈsɪzəz/', 'N', 'gaýçy', 'ножницы', 'a tool for cutting paper or hair', 'Nail scissors are useful when travelling.', 'Syýahatda dyrnak gaýçysy peýdaly.', 'A2'),
    ('slippers', '/ˈslɪpəz/', 'N', 'öý köwşi', 'тапочки', 'soft light shoes you wear indoors', 'Put on your slippers.', 'Öý köwşüňi geý.', 'A2'),
    ('sponge bag', '/ˈspʌndʒ bæɡ/', 'N', 'aşgana haltajygy', 'косметичка (для туалетных принадлежностей)', 'a small bag for soap, toothbrush, etc.', 'My toothbrush is in the sponge bag.', 'Çotgam aşgana haltajygynda.', 'B1'),
    ('sun hat', '/ˈsʌn hæt/', 'N', 'gün telpegi', 'шляпа от солнца', 'a hat that protects you from the sun', 'Wear a sun hat at the beach.', 'Kenarda gün telpegini geý.', 'A2'),
    ('toothbrush', '/ˈtuːθbrʌʃ/', 'N', 'diş çotgasy', 'зубная щётка', 'a brush for cleaning your teeth', 'Buy a new toothbrush.', 'Täze diş çotgasy satyn al.', 'A2'),
    ('towel', '/ˈtaʊəl/', 'N', 'däsmal', 'полотенце', 'a piece of cloth for drying your body', 'Take a beach towel.', 'Kenar däsmalyny al.', 'A2'),
    ('underwear', '/ˈʌndəweə/', 'N', 'iç geýim', 'нижнее бельё', 'clothes you wear under other clothes', 'Pack clean underwear for a week.', 'Bir hepdelik arassa iç geýim ýygnаň.', 'A2'),
    ('guidebook', '/ˈɡaɪdbʊk/', 'N', 'syýahat gollanmasy', 'путеводитель', 'a book with information about a place', 'The guidebook lists the best hotels.', 'Gollanma iň gowy myhmanhanalary görkezýär.', 'B1'),
    ('visa', '/ˈviːzə/', 'N', 'wiza', 'виза', 'official permission to enter a country', 'You need a visa for the USA.', 'ABŞ üçin wiza gerek.', 'B1'),
    ('driving licence', '/ˈdraɪvɪŋ ˌlaɪsns/', 'N', 'sürüji şahadatnamasy', 'водительские права', 'an official document that allows you to drive', 'Show your driving licence to rent a car.', 'Ulag kärendesi üçin sürüji şahadatnamaňy görkez.', 'B1'),
    ('booking confirmation', '/ˌbʊkɪŋ ˌkɒnfəˈmeɪʃn/', 'N', 'bron tassyklanamasy', 'подтверждение бронирования', 'a document that proves you have paid for a room or flight', 'Print the booking confirmation.', 'Bron tassyklanamasyny çap et.', 'B1'),
    ('travel insurance', '/ˈtrævl ɪnˈʃʊərəns/', 'N', 'syýahat ätiýaçlandyryşy', 'туристическая страховка', 'insurance for accidents or problems on holiday', 'Take out travel insurance before you go.', 'Gitmezden öň syýahat ätiýaçlandyryşyny al.', 'B1'),
    ('fold', '/fəʊld/', 'V', 'eplemek, buklatmak', 'складывать', 'to bend clothes so they are flat and tidy', 'Fold your shirts before packing.', 'Köýnekleri ýygnamazyňdan öň eple.', 'B1'),
    ('pack', '/pæk/', 'V', 'ýygnamak', 'укладывать вещи', 'to put things in a bag before a journey', 'I packed my suitcase last night.', 'Düýn agşam çemodanymy ýygnadym.', 'A2'),
    ('roll up', '/ˌrəʊl ˈʌp/', 'PHR', 'togalaklamak, dürlemek', 'скатывать', 'to fold clothes into a roll to save space', 'Roll up your T-shirts to save space.', 'Ýer tygsytlamak üçin köýnekçeleri dürle.', 'B1'),
    ('unpack', '/ˌʌnˈpæk/', 'V', 'ýygnaýjy açmak, çykarmak', 'распаковывать', 'to take things out of a bag after a journey', 'She unpacked as soon as she arrived.', 'Gelen badyna zatlaryny çykardy.', 'B1'),
    ('wrap', '/ræp/', 'V', 'düýrmek, örtmek', 'заворачивать', 'to cover something in paper or cloth', 'Wrap the glasses in clothes.', 'Aýnalary eşige dür.', 'B1'),
]

# ---- Vocabulary Bank — Shops and services -> 2B ----
T['shops_services'] = [
    ('bakery', '/ˈbeɪkəri/', 'N', 'çörekhana', 'булочная', 'a shop that sells bread and cakes', 'The bakery opens at seven.', 'Çörekhana ýedide açylýar.', 'A2'),
    ('butcher', '/ˈbʊtʃə(r)/', 'N', 'et satyjy (gassap)', 'мясник', 'a person or shop that sells meat', 'The butcher cut the lamb.', 'Gassap goýun etini kesdi.', 'A2'),
    ('chemist', '/ˈkemɪst/', 'N', 'dermanhana', 'аптека', 'a shop that sells medicine', 'Buy the pills at the chemist.', 'Dermanlary dermanhanadan al.', 'A2'),
    ('florist', '/ˈflɒrɪst/', 'N', 'gül satyjy', 'цветочник', 'a shop that sells flowers', 'The florist made a lovely bouquet.', 'Gül satyjy owadan çemen ýasady.', 'A2'),
    ('greengrocer', '/ˈɡriːnɡrəʊsə(r)/', 'N', 'gök önüm satyjy', 'овощной магазин', 'a shop that sells fruit and vegetables', 'The greengrocer has fresh tomatoes.', 'Gök önüm satyjyda täze pomidor bar.', 'B1'),
    ('hairdresser', '/ˈheədresə(r)/', 'N', 'sartaraş', 'парикмахер', 'a person who cuts hair', 'The hairdresser trimmed my fringe.', 'Sartaraş kakulumy kesdi.', 'A2'),
    ('jeweller', '/ˈdʒuːələ(r)/', 'N', 'zergär', 'ювелир', 'a shop that sells jewellery', 'The jeweller repaired the ring.', 'Zergär ýüzügi bejerdi.', 'A2'),
    ('newsagent', '/ˈnjuːzeɪdʒənt/', 'N', 'gazet satyjy', 'газетный киоск', 'a shop selling papers and magazines', 'The newsagent is on the corner.', 'Gazet satyjy burçda.', 'B1'),
    ('optician', '/ɒpˈtɪʃn/', 'N', 'göz lukmany (optika)', 'оптик', 'a person who tests eyes and sells glasses', 'The optician checked my sight.', 'Göz lukmany görüşimi barlady.', 'B1'),
    ('dry cleaner', '/ˌdraɪ ˈkliːnə(r)/', 'N', 'himiki arassalaýjy', 'химчистка', 'a shop that cleans clothes without water', 'Take the suit to the dry cleaner.', 'Kostýumy himiki arassalaýja ber.', 'B1'),
    ('stationer', '/ˈsteɪʃənə(r)/', 'N', 'kagyz-kalem satyjy', 'канцелярский магазин', 'a shop selling pens and paper', 'The stationer sells notebooks.', 'Kagyz-kalem satyjy depder satýar.', 'B2'),
    ('deli', '/ˈdeli/', 'N', 'tagam dükany', 'гастроном', 'a shop selling cooked food and cheese', 'We bought cheese at the deli.', 'Tagam dükanyndan peýnir aldyk.', 'B1'),
    ("baker's", '/ˈbeɪkəz/', 'N', 'çörek dükan', 'булочная', 'a shop that sells bread and cakes', 'Buy bread at the baker’s.', 'Çöregi çörek dükandan al.', 'B1'),
    ("butcher's", '/ˈbʊtʃəz/', 'N', 'et dükan', 'мясная лавка', 'a shop that sells meat', 'The butcher’s sells fresh lamb.', 'Et dükandan täze guzy eti satylýar.', 'B1'),
    ("chemist's", '/ˈkemɪsts/', 'N', 'dermanhana', 'аптека', 'a shop that sells medicine', 'Get the tablets at the chemist’s.', 'Dermanhana derman al.', 'B1'),
    ("dry-cleaner's", '/ˌdraɪ ˈkliːnəz/', 'N', 'himiki arassalaýjy', 'химчистка', 'a shop that cleans clothes with chemicals', 'Take the suit to the dry-cleaner’s.', 'Kostýumy himiki arassalaýja ber.', 'B1'),
    ("estate agent's", '/ɪˈsteɪt ˌeɪdʒənts/', 'N', 'gozgalmaýan emläk edarasy', 'агентство недвижимости', 'a shop that sells and rents houses', 'They found the flat at the estate agent’s.', 'Öýi gozgalmaýan emläk edarasyndan tapdylar.', 'B1'),
    ("fishmonger's", '/ˈfɪʃmʌŋɡəz/', 'N', 'balyk dükan', 'рыбный магазин', 'a shop that sells fish', 'The fishmonger’s has fresh salmon.', 'Balyk dükanda täze gyzylbalyk bar.', 'B1'),
    ('garden centre', '/ˈɡɑːdn ˌsentə/', 'N', 'bag merkez', 'садовый центр', 'a place that sells plants and flowers', 'We bought roses at the garden centre.', 'Bag merkezden bägül satyn aldyk.', 'B1'),
    ('launderette', '/ˌlɔːnˈdret/', 'N', 'kir ýuwujyhana', 'прачечная самообслуживания', 'a shop with washing machines you pay to use', 'There is a launderette on our street.', 'Köçämizde kir ýuwujyhana bar.', 'B1'),
    ('market stall', '/ˈmɑːkɪt stɔːl/', 'N', 'bazar piştagtas', 'рыночный прилавок', 'a table at a market where things are sold', 'She sells fruit from a market stall.', 'Bazar piştagtasyndan miwe satýar.', 'B1'),
    ('off-licence', '/ˌɒf ˈlaɪsns/', 'N', 'içgi dükan', 'винный магазин', 'a shop that sells alcohol', 'He bought wine at the off-licence.', 'Içgi dükandan çakyr aldy.', 'B2'),
    ("stationer's", '/ˈsteɪʃənəz/', 'N', 'kanselýariýa dükan', 'магазин канцтоваров', 'a shop that sells paper, pens, etc.', 'Buy envelopes at the stationer’s.', 'Bukjalary kanselýariýa dükandan al.', 'B1'),
    ('car showroom', '/ˈkɑː ˈʃəʊruːm/', 'N', 'awtosalon', 'автосалон', 'a large shop where cars are shown and sold', 'They chose the car at the showroom.', 'Ulawy awtosalonda saýladylar.', 'B1'),
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
    ('foreground', '/ˈfɔːɡraʊnd/', 'N', 'öňki plan', 'передний план', 'the part of a picture nearest to you', 'There are flowers in the foreground.', 'Öňki planda güller bar.', 'B1'),
    ('on top of', '/ˌɒn ˈtɒp əv/', 'PHR', 'üstünde', 'наверху, поверх', 'in a position above something', 'The cat is on top of the fridge.', 'Pişik holodilnigiň üstünde.', 'A2'),
    ('next to', '/ˌnekst ˈtə/', 'PREP', 'ýanynda', 'рядом с', 'at the side of something', 'Sit next to me.', 'Ýanymda otur.', 'A2'),
    ('behind', '/bɪˈhaɪnd/', 'PREP', 'yzynda, arkasynda', 'позади', 'at the back of something', 'The sun is behind the clouds.', 'Gün bulutlaryň arkasynda.', 'A2'),
    ('across', '/əˈkrɒs/', 'PREP', 'oňyrsynda, garşy tarapda', 'через, на другой стороне', 'from one side to the other', 'The bank is across the street.', 'Bank köçäniň garşy tarapynda.', 'A2'),
    ('over', '/ˈəʊvə/', 'PREP', 'üstünden, ýokarsynda', 'над, через', 'above something or crossing it', 'The plane flew over the city.', 'Uçar şäheriň üstünden uçdy.', 'A2'),
    ('round', '/raʊnd/', 'PREP', 'daşyndan, aýlanyp', 'вокруг', 'going around something', 'We walked round the lake.', 'Köliň daşyndan ýöräp geçdik.', 'A2'),
    ('towards', '/təˈwɔːdz/', 'PREP', 'tarapa', 'к, по направлению к', 'in the direction of something', 'She walked towards the camera.', 'Fotoapparata tarap ýöräp geldi.', 'A2'),
    ('under', '/ˈʌndə/', 'PREP', 'astynda', 'под', 'below something', 'The keys are under the newspaper.', 'Açarlar gazetiň astynda.', 'A2'),
    ('between', '/bɪˈtwiːn/', 'PREP', 'arasynda', 'между', 'in the middle of two things', 'The shop is between the bank and the café.', 'Dükan bank bilen kafeniň arasynda.', 'A2'),
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
    ('lid', '/lɪd/', 'N', 'gapak', 'крышка', 'the top part that covers a container', 'Put the lid back on the jar.', 'Bankanyň gapagyny ýap.', 'B1'),
    ('can', '/kæn/', 'N', 'banka, konserwa gutusy', 'жестяная банка', 'a metal container for drinks or food', 'Recycle the drink cans.', 'Içgi bankalaryny gaýtadan işle.', 'B1'),
    ('packet', '/ˈpækɪt/', 'N', 'guty, bukja', 'пачка, пакет', 'a small paper or plastic container', 'He ate a packet of crisps.', 'Bir guty çips iýdi.', 'B1'),
    ('plastic bags', '/ˈplæstɪk bæɡz/', 'N', 'plastik torbalar', 'пластиковые пакеты', 'bags made of plastic', 'Take your own bag, not plastic bags.', 'Plastik däl, öz torbaňy al.', 'A2'),
    ('carton', '/ˈkɑːtn/', 'N', 'karton guty', 'картонная упаковка', 'a container made of cardboard for liquids', 'She bought a carton of juice.', 'Bir karton şire satyn aldy.', 'B1'),
    ('tin', '/tɪn/', 'N', 'konserwa bankasy', 'консервная банка', 'a metal container for food', 'Add a tin of tomatoes.', 'Bir banka pomidor goş.', 'B1'),
    ('sell-by date', '/ˌsel baɪ ˈdeɪt/', 'N', 'ýaramlylyk möhleti', 'срок годности', 'the date after which food should not be sold', 'Check the sell-by date on the milk.', 'Süýdüň ýaramlylyk möhletini barla.', 'B1'),
    ('bin bag', '/ˈbɪn bæɡ/', 'N', 'zibil torbasy', 'мешок для мусора', 'a large plastic bag for rubbish', 'Put the rubbish in a bin bag.', 'Zibili zibil torbasyna sal.', 'B1'),
    ('refuse collectors', '/ˈrefjuːs kəˌlektəz/', 'N', 'zibil ýygnaýjylar', 'мусорщики', 'people whose job is collecting rubbish', 'The refuse collectors come on Fridays.', 'Zibil ýygnaýjylar anna günleri gelýär.', 'B1'),
    ('waste-paper basket', '/ˈweɪstpeɪpə ˌbɑːskɪt/', 'N', 'kagyz zibil sebedi', 'корзина для бумаг', 'a small container for waste paper', 'Throw the letter in the waste-paper basket.', 'Hatyny kagyz zibil sebedine at.', 'B1'),
    ('tub', '/tʌb/', 'N', 'gap, bedreçe', 'баночка, контейнер', 'a small round container', 'I bought a tub of yoghurt.', 'Bir gap ýogurt satyn aldym.', 'B1'),
    ('wrapper', '/ˈræpə/', 'N', 'örtgi, kagyz', 'обёртка', 'paper or plastic around food', 'Do not drop sweet wrappers.', 'Konfert örtgüni taşlama.', 'B1'),
    ('give away', '/ˌɡɪv əˈweɪ/', 'PHR', 'mugt bermek, paýlamak', 'раздавать', 'to give something you no longer want', 'We gave away our old clothes.', 'Köne eşiklerimizi paýladyk.', 'B1'),
    ('pot', '/pɒt/', 'N', 'gapy, küýze', 'горшок, банка', 'a round container', 'She opened a pot of jam.', 'Mürebbäniň gabyny açdy.', 'A2'),
    ('rethink', '/ˌriːˈθɪŋk/', 'V', 'täzeden oýlanmak', 'переосмыслить', 'to think about something again in a different way', 'We need to rethink our plans.', 'Meýilnamalarymyzy täzeden oýlanmaly.', 'B1'),
    ('reuse', '/ˌriːˈjuːz/', 'V', 'gaýtadan ulanmak', 'использовать повторно', 'to use something again', 'Reuse the glass jars.', 'Aýna bankalary gaýtadan ulan.', 'B1'),
]
# ---- Vocabulary Bank — Study and work -> 4B ----
T['study_work'] = [
    ('revise', '/rɪˈvaɪz/', 'V', 'gaýtalamak (synaga)', 'повторять (к экзамену)', 'to study again before an exam', 'I need to revise tonight.', 'Şu gije gaýtalamaly.', 'A2'),
    ('dissertation', '/ˌdɪsəˈteɪʃn/', 'N', 'disseratasiýa', 'диссертация', 'a long piece of academic writing', 'She finished her dissertation.', 'Disseratasiýasyny gutardy.', 'B2'),
    ('internship', '/ˈɪntɜːnʃɪp/', 'N', 'staj (tecrübe)', 'стажировка', 'a period of work experience', 'He got an internship at a bank.', 'Bankda staj aldy.', 'B1'),
    ('lecture', '/ˈlektʃə(r)/', 'N', 'leksiýa', 'лекция', 'a formal talk to students', 'The lecture lasted two hours.', 'Leksiýa iki sagat dowam etdi.', 'A2'),
    ('tutor', '/ˈtjuːtə(r)/', 'N', 'repetitor (ýolbaşçy)', 'репетитор, куратор', 'a private teacher', 'My tutor helped with the essay.', 'Repetitor esseýde kömek etdi.', 'A2'),
    ('scholarship', '/ˈskɒləʃɪp/', 'N', 'talyp haky (stipendiýa)', 'стипендия, грант', 'money given to a student', 'She won a scholarship abroad.', 'Daşary ýurt talyp hakyny gazandy.', 'A2'),
    ('course', '/kɔːs/', 'N', 'kurs', 'курс', 'a series of lessons', 'He joined an English course.', 'Iňlis kursuna ýazyldy.', 'A1', 'training course'),
    ('term', '/tɜːm/', 'N', 'okuw möwsümi', 'учебный семестр', 'one part of the school year', 'Exams are at the end of term.', 'Synaglar okuw möwsüminiň ahyrynda.', 'A2'),
    ('semester', '/sɪˈmestə(r)/', 'N', 'ýarym ýyl (semestr)', 'семестр', 'half of the academic year', 'The first semester ends in December.', 'Birinji semestr dekabrda gutarýar.', 'A2'),
    ('coursework', '/ˈkɔːswɜːk/', 'N', 'kurs işi', 'курсовая работа', 'work done during a course', 'Coursework counts towards the grade.', 'Kurs işi baha goşulýar.', 'B1'),
    ('field trip', '/ˈfiːld trɪp/', 'N', 'okuw sapary', 'выездное занятие', 'a trip students take to learn', 'The class went on a field trip.', 'Synp okuw saparyna gitdi.', 'A2'),
    ('distance learning', '/ˌdɪstəns ˈlɜːnɪŋ/', 'N', 'aragatnaşykly okuw', 'дистанционное обучение', 'studying from home online', 'She studies by distance learning.', 'Aragatnaşykly okuw arkaly okaýar.', 'B1'),
    ('faculty', '/ˈfæklti/', 'N', 'fakultet', 'факультет', 'a department of a university', 'She studies in the History faculty.', 'Taryh fakultetinde okaýar.', 'B1'),
    ('intern', '/ˈɪntɜːn/', 'N', 'stajýor', 'стажёр', 'a student who works to get experience', 'He worked as an intern last summer.', 'Geçen tomus stajýor boldy.', 'B1'),
    ('interview', '/ˈɪntəvjuː/', 'N', 'söhbetdeşlik', 'собеседование, интервью', 'a meeting where you are asked questions', 'The job interview went well.', 'Iş söhbetdeşligi gowy geçdi.', 'B1'),
    ('job offer', '/ˈdʒɒb ˌɒfə/', 'N', 'iş teklibi', 'предложение работы', 'when a company offers you a job', 'She got two job offers.', 'Iki iş teklibini aldy.', 'B1'),
    ('postgraduate', '/ˌpəʊstˈɡrædʒuət/', 'N', 'aspirant, magistrant', 'аспирант', 'a student doing a higher degree after their first', 'He is a postgraduate in biology.', 'Biologiýa boýunça magistrant.', 'B2'),
    ('professor', '/prəˈfesə/', 'N', 'professor', 'профессор', 'a senior teacher at a university', 'The professor gave an interesting lecture.', 'Professor gyzykly leksiýa berdi.', 'B1'),
    ('qualification', '/ˌkwɒlɪfɪˈkeɪʃn/', 'N', 'hünär derejesi', 'квалификация', 'an exam or skill that shows you can do a job', 'What qualifications do you need to teach?', 'Mugallym bolmak üçin haýsy derejeler gerek?', 'B1'),
    ('reapply', '/ˌriːəˈplaɪ/', 'V', 'täzeden ýüz tutmak', 'подавать повторно', 'to apply again', 'If you fail, you can reapply next year.', 'Ýykylysaň, indiki ýyl täzeden ýüz tutup bilersiň.', 'B1'),
    ('seminar', '/ˈsemɪnɑː/', 'N', 'seminar', 'семинар', 'a small university class for discussion', 'The seminar was about modern poetry.', 'Seminar häzirki zaman poeziýasy baradady.', 'B1'),
    ('thesis', '/ˈθiːsɪs/', 'N', 'dissertasiýa, diplom işi', 'диссертация, дипломная работа', 'a long piece of writing for a university degree', 'She is writing her thesis.', 'Diplom işini ýazýar.', 'B1'),
    ('tutorial', '/tjuːˈtɔːriəl/', 'N', 'tutor sapak', 'индивидуальное занятие', 'a small class with a teacher at university', 'The tutorial has six students.', 'Tutor sapakda alty talyplar bar.', 'B1'),
    ('undergraduate', '/ˌʌndəˈɡrædʒuət/', 'N', 'talyp', 'студент (бакалавриата)', 'a student doing their first university degree', 'Undergraduates study for three years.', 'Talyplar üç ýyl okaýar.', 'B1'),
    ('vacancy', '/ˈveɪkənsi/', 'N', 'boş iş orny', 'вакансия', 'a job that is available', 'There are no vacancies at the moment.', 'Häzirki wagt boş iş orny ýok.', 'B1'),
]

# ---- Vocabulary Bank — Television -> 5A ----
T['television'] = [
    ('reality show', '/riˈæləti ʃəʊ/', 'N', 'realiti şou', 'реалити-шоу', 'a programme with real people', 'Reality shows are very popular.', 'Realiti şou gaty meşhur.', 'A2'),
    ('soap opera', '/ˈsəʊp ˌɒpərə/', 'N', 'serial', 'мыльная опера, сериал', 'a continuing drama on TV', 'She watches a soap opera every day.', 'Her gün serial görýär.', 'A2'),
    ('sitcom', '/ˈsɪtkɒm/', 'N', 'sitkom (gülkünç serial)', 'ситком', 'a funny series with the same characters', 'That sitcom makes me laugh.', 'Şol sitkom meni güldürýär.', 'A2'),
    ('quiz show', '/ˈkwɪz ʃəʊ/', 'N', 'wiktoryna', 'викторина', 'a programme where people answer questions', 'He won money on a quiz show.', 'Wiktorynada pul gazandy.', 'A2'),
    ('chat show', '/ˈtʃæt ʃəʊ/', 'N', 'söhbetdeşlik gepleşigi', 'ток-шоу', 'a programme of talks with guests', 'The chat show had famous guests.', 'Söhbetdeşlik gepleşiginde meşhur myhmanlar bardy.', 'B1'),
    ('presenter', '/prɪˈzentə(r)/', 'N', 'alyp baryjy', 'ведущий', 'a person who hosts a programme', 'The presenter introduced the band.', 'Alyp baryjy topary tanyşdyrdy.', 'A2'),
    ('viewer', '/ˈvjuːə(r)/', 'N', 'tomaşaçy', 'зритель', 'a person who watches TV', 'Millions of viewers watched the final.', 'Millionlarça tomaşaçy finaly gördi.', 'A2'),
    ('series', '/ˈsɪəriːz/', 'N', 'serial (yzygiderli)', 'сериал, серия', 'a set of related programmes', 'The second series starts tonight.', 'Ikinji serial şu gije başlaýar.', 'A2'),
    ('episode', '/ˈepɪsəʊd/', 'N', 'bölüm (seriýa)', 'эпизод, серия', 'one part of a series', 'Did you see the last episode?', 'Soňky bölümi gördüňmi?', 'A2'),
    ('box set', '/ˈbɒks set/', 'N', 'tutuş seriýa toplumy', 'бокс-сет (все серии)', 'a complete set of a series', 'I bought the box set of the show.', 'Gepleşigiň tutuş toplumyny satyn aldym.', 'B1'),
    ('advert', '/ˈædvɜːt/', 'N', 'mahabat', 'реклама (ролик)', 'a short film on TV that sells something', 'The adverts are very long.', 'Mahabatlar gaty uzyn.', 'B1'),
    ('animation', '/ˌænɪˈmeɪʃn/', 'N', 'animasiýa', 'анимация', 'films made with drawings or computer images', 'The children watched an animation.', 'Çagalar animasiýa gördi.', 'A2'),
    ('cartoon', '/kɑːˈtuːn/', 'N', 'multfilm', 'мультфильм', 'a short animated film, often funny', 'He likes watching cartoons.', 'Multfilm görmegi gowy görýär.', 'A2'),
    ('cookery programme', '/ˈkʊkəri ˌprəʊɡræm/', 'N', 'nahar bişiriş gepleşigi', 'кулинарная программа', 'a TV programme about cooking', 'My favourite cookery programme is on at six.', 'Söýgüli nahar gepleşigim sagat altyda.', 'B1'),
    ('current affairs programme', '/ˌkʌrənt əˈfeəz ˌprəʊɡræm/', 'N', 'habar-seljeriş gepleşigi', 'общественно-политическая программа', 'a TV programme about news and politics', 'He watches a current affairs programme every week.', 'Her hepde habar-seljeriş gepleşigini görýär.', 'B2'),
    ('documentary', '/ˌdɒkjuˈmentri/', 'N', 'dokumental film', 'документальный фильм', 'a programme about real facts', 'We saw a documentary about whales.', 'Kitler barada dokumental film gördük.', 'B1'),
    ('live sport', '/ˌlaɪv ˈspɔːt/', 'N', 'göni sport ýaýlymy', 'прямая спортивная трансляция', 'sport shown on TV as it happens', 'He never misses live sport.', 'Göni sport ýaýlymyny hiç sypdyrmaýar.', 'B1'),
    ('period drama', '/ˌpɪəriəd ˈdrɑːmə/', 'N', 'taryhy drama', 'историческая драма', 'a film or series set in the past', 'The period drama was filmed in Bath.', 'Taryhy drama Batda surata düşürildi.', 'B2'),
    ('weather forecast', '/ˈweðə fɔːkɑːst/', 'N', 'howa maglumaty', 'прогноз погоды', 'a report on TV about the weather', 'The weather forecast says rain.', 'Howa maglumaty ýagyş diýýär.', 'A2'),
    ('season', '/ˈsiːzn/', 'N', 'möwsüm (serial)', 'сезон (сериала)', 'a set of episodes of a TV series', 'I watched the whole season in one day.', 'Bütin möwsümi bir günde gördim.', 'B1'),
    ('streaming service', '/ˈstriːmɪŋ ˌsɜːvɪs/', 'N', 'striming hyzmaty', 'стриминговый сервис', 'a service that shows films and series online', 'Which streaming service do you use?', 'Haýsy striming hyzmatyny ulanýarsyň?', 'B1'),
    ('turn over', '/ˌtɜːn ˈəʊvə/', 'PHR', 'kanal çalyşmak', 'переключать (канал)', 'to change to a different channel', 'Turn over, this programme is boring.', 'Kanal çalyş, bu gepleşik göwünsüz.', 'B1'),
    ('turn down', '/ˌtɜːn daʊn/', 'PHR', 'peseltmek', 'убавить (звук)', 'to make the sound quieter', 'Turn down the TV, please.', 'Telewizory peselt, haýyş.', 'A2'),
    ('turn up', '/ˌtɜːn ʌp/', 'PHR', 'galdyrmak', 'прибавить (звук)', 'to make the sound louder', 'Turn up the music!', 'Aýdymy galdyr!', 'A2'),
    ('turn off', '/ˌtɜːn ˈɒf/', 'PHR', 'öçürmek', 'выключать', 'to stop a machine working', 'Turn off the TV and go to bed.', 'Telewizory öçür-de ýat.', 'A2'),
    ('turn on', '/ˌtɜːn ˈɒn/', 'PHR', 'ýakmak, işe salmak', 'включать', 'to make a machine start working', 'Turn on the TV at eight.', 'Sagat sekizde telewizory ýak.', 'A2'),
    ('be on', '/ˌbiː ˈɒn/', 'PHR', '(efirde) bolmak', 'идти (о передаче)', 'when a programme is being shown', 'My favourite series is on tonight.', 'Söýgüli serialym şu agşam efirde.', 'A2'),
]

# ---- Vocabulary Bank — The country -> 5B ----
T['country'] = [
    ('countryside', '/ˈkʌntrisaɪd/', 'N', 'oba ýerleri', 'сельская местность', 'land away from towns', 'They moved to the countryside.', 'Oba ýerlerine göçdüler.', 'A2'),
    ('field', '/fiːld/', 'N', 'meýdan (öri)', 'поле', 'an open area of land', 'Cows grazed in the field.', 'Meýdanda sygyrlar otlady.', 'A2'),
    ('hedge', '/hedʒ/', 'N', 'haýal çit (agaç)', 'живая изгородь', 'a row of bushes as a border', 'Birds nested in the hedge.', 'Guşlar haýal çitde höwürtge gurdu.', 'B1'),
    ('lane', '/leɪn/', 'N', 'inçe ýol', 'узкая дорога', 'a narrow country road', 'We walked down a quiet lane.', 'Asuda inçe ýoldan ýöräp gitdik.', 'A2'),
    ('path', '/pɑːθ/', 'N', 'çigir (ýodajyk)', 'тропинка', 'a track for walking', 'A path leads to the river.', 'Çigir derýa alyp barýar.', 'A2'),
    ('meadow', '/ˈmedəʊ/', 'N', 'ýaýla (otlak)', 'луг', 'a field of grass and flowers', 'Wildflowers filled the meadow.', 'Ýaýlany ýabany güller doldurdy.', 'B1'),
    ('valley', '/ˈvæli/', 'N', 'jülge', 'долина', 'low land between hills', 'The village sits in a valley.', 'Oba jülgäniň içinde ýerleşýär.', 'A2'),
    ('hill', '/hɪl/', 'N', 'depe', 'холм', 'a small mountain', 'We climbed to the top of the hill.', 'Depäniň depesine çykdyk.', 'A1'),
    ('stream', '/striːm/', 'N', 'çaýjagaz (kiçi derýa)', 'ручей', 'a small river', 'A stream runs behind the house.', 'Öýüň arkasyndan çaýjagaz akýar.', 'A2'),
    ('woods', '/wʊdz/', 'N', 'tokaýjyk', 'роща, лес', 'an area of trees', 'We walked in the woods.', 'Tokaýjykda ýöräp gezdik.', 'A2', 'in the woods'),
    ('farm', '/fɑːm/', 'N', 'ferma', 'ферма', 'land where animals and crops are kept', 'The farm has twenty sheep.', 'Fermada ýigrimi goýun bar.', 'A1'),
    ('barn', '/bɑːn/', 'N', 'ambar', 'амбар, сарай', 'a farm building for storage', 'They store hay in the barn.', 'Ambarda iým saklaýarlar.', 'B1'),
    ('branch', '/brɑːntʃ/', 'N', 'şaha', 'ветка', 'a part of a tree that grows out from it', 'The bird sat on a branch.', 'Guş şahada otyrdy.', 'B1'),
    ('bush', '/bʊʃ/', 'N', 'agymsy, kol', 'куст', 'a low plant like a small tree', 'There are roses behind the bush.', 'Koluň arkasynda bägül bar.', 'B1'),
    ('cliff', '/klɪf/', 'N', 'gaýa', 'скала, утёс', 'a high steep wall of rock by the sea', 'We stood on top of the cliff.', 'Gaýanyň depesinde durduk.', 'B1'),
    ('cow', '/kaʊ/', 'N', 'sygyr', 'корова', 'a large farm animal that gives milk', 'The cows are in the field.', 'Sygyrlar meýdanda.', 'A2'),
    ('donkey', '/ˈdɒŋki/', 'N', 'eşek', 'осёл', 'an animal like a small horse', 'The donkey carried the bags.', 'Eşek torbalary göterdi.', 'A2'),
    ('fence', '/fens/', 'N', 'haýat, germew', 'забор', 'a barrier around a field or garden', 'The horse jumped over the fence.', 'At germewden böwdi.', 'B1'),
    ('gate', '/ɡeɪt/', 'N', 'derweze', 'ворота, калитка', 'a door in a fence', 'Close the gate behind you.', 'Yzyňdan derwezäni ýap.', 'B1'),
    ('hen', '/hen/', 'N', 'towuk', 'курица', 'a female chicken', 'The hens are in the yard.', 'Towuklar howluda.', 'A2'),
    ('lake', '/leɪk/', 'N', 'köl', 'озеро', 'a large area of water', 'We swam in the lake.', 'Kölde ýüzdük.', 'A2'),
    ('leaf', '/liːf/', 'N', 'ýaprak', 'лист (растения)', 'a flat green part of a plant', 'The leaves turn red in autumn.', 'Ýapraklar güýzde gyzarýar.', 'A2'),
    ('rock', '/rɒk/', 'N', 'gaýa, daş', 'камень, скала', 'a large stone', 'Climb over the rocks carefully.', 'Gaýalardan seresaply geç.', 'A2'),
    ('stick', '/stɪk/', 'N', 'çybyk', 'палка, ветка', 'a thin piece of wood from a tree', 'The dog brought back a stick.', 'It çybygy yzyna getirdi.', 'A2'),
    ('stone', '/stəʊn/', 'N', 'daş', 'камень', 'a small piece of rock', 'He threw a stone into the water.', 'Suwa daş zyňdy.', 'A2'),
    ('tractor', '/ˈtræktə/', 'N', 'traktor', 'трактор', 'a strong vehicle used on farms', 'The farmer drove the tractor.', 'Daýhan traktor sürdi.', 'A2'),
    ('farmhouse', '/ˈfɑːmhaʊs/', 'N', 'ferma öýi', 'фермерский дом', 'the main house on a farm', 'They stayed in an old farmhouse.', 'Köne ferma öýünde galdylar.', 'B1'),
]

# ---- Vocabulary Bank — At a restaurant -> 6A ----
T['restaurant'] = [
    ('menu', '/ˈmenjuː/', 'N', 'tagam sanawy', 'меню', 'a list of food you can order', 'Can I see the menu, please?', 'Tagam sanawyny görüp bilerinmi?', 'A1'),
    ('starter', '/ˈstɑːtə(r)/', 'N', 'başlangyç tagam', 'закуска (первое)', 'a small dish before the main one', 'I had soup as a starter.', 'Başlangyç tagam hökmünde çorba aldym.', 'A2'),
    ('main course', '/ˌmeɪn ˈkɔːs/', 'N', 'esasy tagam', 'основное блюдо', 'the largest part of a meal', 'The main course was chicken.', 'Esasy tagam towuk boldy.', 'A2'),
    ('dessert', '/dɪˈzɜːt/', 'N', 'süýji tagam', 'десерт', 'sweet food at the end of a meal', 'We shared a chocolate dessert.', 'Şokoladly süýji tagamy paýlaşdyk.', 'A2'),
    ('waiter', '/ˈweɪtə(r)/', 'N', 'ofisiant', 'официант', 'a person who serves food', 'The waiter brought the bill.', 'Ofisiant hasaby getirdi.', 'A2'),
    ('bill', '/bɪl/', 'N', 'hasap (töleg)', 'счёт', 'the paper showing what you owe', 'Can we have the bill, please?', 'Hasaby alyp bilerismi?', 'A2', 'pay the bill'),
    ('tip', '/tɪp/', 'N', 'çaýpulu (bahşyş)', 'чаевые', 'extra money for good service', 'We left a generous tip.', 'Jomart çaýpulu goýduk.', 'A2', 'leave a tip'),
    ('reservation', '/ˌrezəˈveɪʃn/', 'N', 'bron', 'бронь', 'a booking at a restaurant', 'I made a reservation for two.', 'Iki adam üçin bron etdim.', 'A2', 'make a reservation'),
    ('order', '/ˈɔːdə(r)/', 'V', 'sargyt etmek', 'заказывать', 'to ask for food', 'We ordered the fish.', 'Balyk sargyt etdik.', 'A1', 'order a meal'),
    ('chef', '/ʃef/', 'N', 'aşpez (baş aşpez)', 'шеф-повар', 'the cook in a restaurant', 'The chef prepared a special dish.', 'Aşpez ýörite tagam taýýarlady.', 'A2'),
    ('cuisine', '/kwɪˈziːn/', 'N', 'aşhana (tagam stili)', 'кухня (национальная)', 'a style of cooking', 'I love Italian cuisine.', 'Italiýan aşhanasyny gowy görýärin.', 'B1', 'French cuisine'),
    ('booking', '/ˈbʊkɪŋ/', 'N', 'bron (ýazgy)', 'бронирование', 'an arrangement to reserve a table', 'We have a booking at eight.', 'Sagat sekizde bronumuz bar.', 'A2', 'table booking'),
    ('bowl', '/bəʊl/', 'N', 'käse', 'миска, пиала', 'a deep round dish', 'I had a bowl of soup.', 'Bir käse çorba iýdim.', 'A2'),
    ('candle', '/ˈkændl/', 'N', 'şem', 'свеча', 'a stick of wax that gives light', 'There were candles on the table.', 'Stoluň üstünde şem bardy.', 'A2'),
    ('cup', '/kʌp/', 'N', 'piýala', 'чашка', 'a round container with a handle for drinking', 'I drank a cup of coffee.', 'Bir piýala kofe içdim.', 'A1'),
    ('fork', '/fɔːk/', 'N', 'çemçe (dirsekli)', 'вилка', 'a tool with points for eating with', 'Eat the pasta with a fork.', 'Makaronyny çemçe bilen iý.', 'A2'),
    ('glass', '/ɡlɑːs/', 'N', 'stakan', 'стакан, бокал', 'a container for drinks made of glass', 'She poured a glass of water.', 'Bir stakan suw guýdy.', 'A2'),
    ('knife', '/naɪf/', 'N', 'pyçak', 'нож', 'a tool for cutting food', 'Cut the meat with a knife.', 'Eti pyçak bilen kes.', 'A2'),
    ('mug', '/mʌɡ/', 'N', 'krujka', 'кружка', 'a large cup for hot drinks', 'He drank coffee from a big mug.', 'Uly krujkadan kofe içdi.', 'A2'),
    ('napkin', '/ˈnæpkɪn/', 'N', 'salfetka', 'салфетка', 'paper or cloth for cleaning your mouth', 'Put the napkin on your knees.', 'Salfetkany dyzyňyza goýuň.', 'B1'),
    ('serving dish', '/ˈsɜːvɪŋ dɪʃ/', 'N', 'uly tabak', 'блюдо для подачи', 'a large dish food is served from', 'The vegetables came in a serving dish.', 'Gök önümler uly tabakda geldi.', 'B1'),
    ('spoon', '/spuːn/', 'N', 'çemçe', 'ложка', 'a tool with a round end for eating', 'Eat the soup with a spoon.', 'Çorbany çemçe bilen iý.', 'A2'),
    ('wine glass', '/ˈwaɪn ɡlɑːs/', 'N', 'çakyr bokaly', 'бокал для вина', 'a glass for drinking wine', 'She raised her wine glass.', 'Çakyr bokalyny galdyrdy.', 'B1'),
    ('clear', '/klɪə/', 'V', 'ýygnamak (stol)', 'убирать (со стола)', 'to take away dishes after a meal', 'The waiter cleared the table.', 'Ofisiant stoly ýygnady.', 'B1'),
    ('lay the table', '/ˌleɪ ðə ˈteɪbl/', 'PHR', 'stol ýazmak', 'накрывать на стол', 'to put plates, glasses, etc. on the table', 'Please lay the table for four.', 'Dört adam üçin stol ýaz, haýyş.', 'B1'),
    ('send it back', '/ˌsend ɪt ˈbæk/', 'PHR', 'yzyna gaýtarmak', 'отослать обратно (блюдо)', 'to ask the kitchen to replace a dish you do not like', 'The soup was cold, so I sent it back.', 'Çorba sowukdy, şonuň üçin yzyna gaýtardym.', 'B1'),
    ('leave a tip', '/ˌliːv ə ˈtɪp/', 'PHR', 'çaýpuly goýmak', 'оставить чаевые', 'to give extra money to a waiter', 'We left a tip of ten percent.', 'On göterim çaýpuly goýduk.', 'B1'),
    ('ask for the bill', '/ˌɑːsk fə ðə ˈbɪl/', 'PHR', 'hasap soramak', 'попросить счёт', 'to ask to pay in a restaurant', 'After dessert we asked for the bill.', 'Desertden soň hasap soradyk.', 'B1'),
    ('meal', '/miːl/', 'N', 'nahar, tagam', 'еда, приём пищи', 'food eaten at one time', 'We had a lovely meal.', 'Ajap nahar iýdik.', 'A2'),
]

# ---- Vocabulary Bank — DIY and repairs -> 6B ----
T['diy'] = [
    ('hammer', '/ˈhæmə(r)/', 'N', 'çekiç', 'молоток', 'a tool for hitting nails', 'He hit the nail with a hammer.', 'Çüýi çekiç bilen kakdy.', 'A2'),
    ('screw', '/skruː/', 'N', 'nurbat (wint)', 'винт, шуруп', 'a metal pin you twist in', 'Tighten the screw.', 'Nurbaty berk berkit.', 'A2'),
    ('screwdriver', '/ˈskruːdraɪvə(r)/', 'N', 'otwýortka', 'отвёртка', 'a tool for turning screws', 'Pass me the screwdriver.', 'Otwýortkany maňa ber.', 'A2'),
    ('drill', '/drɪl/', 'N', 'burgy (elektrik)', 'дрель', 'a tool for making holes', 'He used a drill on the wall.', 'Diwarda burgy ulandy.', 'A2'),
    ('saw', '/sɔː/', 'N', 'byçgy', 'пила', 'a tool for cutting wood', 'Cut the wood with a saw.', 'Agajy byçgy bilen kes.', 'A2'),
    ('paint', '/peɪnt/', 'V', 'reňklemek', 'красить', 'to cover with colour', 'We painted the room white.', 'Otagy ak reňkledik.', 'A1'),
    ('brush', '/brʌʃ/', 'N', 'çotga (reňk)', 'кисть', 'a tool for painting', 'Clean the brush after use.', 'Ulanylandan soň çotgany arassala.', 'A2'),
    ('ladder', '/ˈlædə(r)/', 'N', 'merdiwan', 'лестница (приставная)', 'a set of steps you can move', 'He climbed the ladder.', 'Merdiwana dyrmaşdy.', 'A2'),
    ('tool', '/tuːl/', 'N', 'gural', 'инструмент', 'an object used to make or fix things', 'Keep your tools in a box.', 'Gurallaryňy gutuda sakla.', 'A2'),
    ('plumber', '/ˈplʌmə(r)/', 'N', 'santehnik', 'сантехник', 'a person who fixes water pipes', 'Call a plumber for the leak.', 'Syzynty üçin santehnik çagyr.', 'A2'),
    ('fix', '/fɪks/', 'V', 'bejermek', 'чинить', 'to repair something', 'He fixed the broken chair.', 'Döwülen stuly bejerdi.', 'A2'),
    ('mend', '/mend/', 'V', 'ýamamak (bejermek)', 'латать, чинить', 'to repair something torn or broken', 'She mended the hole in her coat.', 'Paltoşyndaky deşigi ýamady.', 'B1'),
    ('brick', '/brɪk/', 'N', 'kerpiç', 'кирпич', 'a hard block used for building walls', 'The house is made of red brick.', 'Öý gyzyl kerpiçden ýasalan.', 'B1'),
    ('bucket', '/ˈbʌkɪt/', 'N', 'bedre', 'ведро', 'a round open container with a handle', 'Fill the bucket with water.', 'Bedräni suw bilen doldur.', 'B1'),
    ('drawing pin', '/ˈdrɔːɪŋ pɪn/', 'N', 'düýbüşli iňňe', 'канцелярская кнопка', 'a short pin for fixing paper to a wall', 'He fixed the poster with drawing pins.', 'Plakaty düýbüşli iňňe bilen berkitdi.', 'B1'),
    ('glue', '/ɡluː/', 'N', 'ýelim', 'клей', 'a substance used to stick things together', 'Use glue to fix the broken cup.', 'Döwülen käsäni ýelimle.', 'B1'),
    ('handle', '/ˈhændl/', 'N', 'tutawaç, gulp', 'ручка, рукоятка', 'the part of a door or tool you hold', 'The door handle is broken.', 'Gapy gulpy döwük.', 'B1'),
    ('paintbrush', '/ˈpeɪntbrʌʃ/', 'N', 'çotga (reňk)', 'малярная кисть', 'a brush used for painting', 'Wash the paintbrush after use.', 'Ulanylandan soň çotgany ýuw.', 'B1'),
    ('penknife', '/ˈpennaɪf/', 'N', 'büklenýän pyçak', 'складной нож', 'a small knife that folds', 'He cut the string with a penknife.', 'Ýüpi büklenýän pyçak bilen kesdi.', 'B1'),
    ('spanner', '/ˈspænə/', 'N', 'açar (tehnik)', 'гаечный ключ', 'a tool for turning nuts', 'Use a spanner to tighten the bolt.', 'Bolti berkitmek üçin açar ulan.', 'B1'),
    ('string', '/strɪŋ/', 'N', 'ýüp, sapak', 'верёвка, бечёвка', 'thin strong rope', 'Tie the parcel with string.', 'Bohçany ýüp bilen daň.', 'B1'),
    ('tile', '/taɪl/', 'N', 'kafel, plitka', 'плитка (кафель)', 'a flat piece used to cover floors or walls', 'The kitchen has white tiles.', 'Aşhanada ak kafel bar.', 'B1'),
    ('light bulb', '/ˈlaɪt bʌlb/', 'N', 'lampoçka', 'лампочка', 'the glass part of a lamp that gives light', 'Change the light bulb, please.', 'Lampoçkany çalyş, haýyş.', 'A2'),
    ('put together', '/ˌpʊt təˈɡeðə/', 'PHR', 'ýygnamak, gurmak', 'собирать (мебель)', 'to make something by joining parts', 'We put together the new shelf.', 'Täze tekjäni gurdyk.', 'B1'),
]

# ---- Vocabulary Bank — Phrasal verbs (money) -> 7A ----
T['money_phrasal'] = [
    ('cash machine', '/ˈkæʃ məʃiːn/', 'N', 'bankomat', 'банкомат', 'a machine that gives you money', 'There is a cash machine outside.', 'Daşarda bankomat bar.', 'A2'),
    ('withdraw', '/wɪðˈdrɔː/', 'V', 'pul çykarmak', 'снимать (деньги)', 'to take money from an account', 'I withdrew fifty manat.', 'Elli manat çykardym.', 'A2', 'withdraw cash'),
    ('deposit', '/dɪˈpɒzɪt/', 'V', 'goýmak (puly)', 'вносить (деньги)', 'to put money into an account', 'She deposited her salary.', 'Aýlygyny goýdy.', 'A2', 'deposit money'),
    ('PIN', '/pɪn/', 'N', 'pin-kod', 'пин-код', 'a secret number for a card', 'Never share your PIN.', 'Pin-koduňy hiç wagt paýlaşma.', 'A2'),
    ('balance', '/ˈbæləns/', 'N', 'galyndy (hasapdaky)', 'баланс, остаток', 'the money left in an account', 'Check your balance online.', 'Galyndyňy onlaýn barla.', 'A2', 'account balance'),
    ('banknote', '/ˈbæŋknəʊt/', 'N', 'kagyz pul', 'банкнота', 'a piece of paper money', 'He paid with a large banknote.', 'Uly kagyz pul bilen töledi.', 'B1'),
    ('account', '/əˈkaʊnt/', 'N', 'hasap', 'счёт (в банке)', 'an arrangement with a bank', 'She opened a bank account.', 'Bank hasabyny açdy.', 'A2', 'open an account'),
    ('pay in', '/peɪ ɪn/', 'PHR', 'goýmak (hasaba)', 'вносить (на счёт)', 'to put money into an account', 'I paid in the cheque.', 'Çeki hasaba goýdum.', 'B1'),
    ('take out', '/teɪk aʊt/', 'PHR', 'çykarmak (pul)', 'снимать (деньги)', 'to withdraw money', 'I took out some cash.', 'Biraz nagt pul çykardym.', 'A2', 'take out money'),
    ('pay back', '/peɪ bæk/', 'PHR', 'gaýtarmak (karz)', 'возвращать (долг)', 'to return borrowed money', 'I will pay you back tomorrow.', 'Ertir saňa gaýtararyn.', 'A2', 'pay back a loan'),
    ('put aside', '/pʊt əˈsaɪd/', 'PHR', 'ýygnaýyş etmek (aýyrmak)', 'откладывать (деньги)', 'to save money for later', 'We put aside a little each month.', 'Her aý biraz aýyrýarys.', 'A2'),
    ('set up', '/set ʌp/', 'PHR', 'gurmak (iş)', 'организовать, учредить', 'to start a business', 'They set up a small company.', 'Kiçi kompaniýa gurdular.', 'A2', 'set up a business'),
    ('pay off', '/ˌpeɪ ˈɒf/', 'PHR', 'doly tölemek', 'выплатить (долг)', 'to finish paying money you owe', 'I am paying off my student loan until I am 45.', 'Talyp karzyny 45 ýaşyma çenli töleýärin.', 'B1'),
    ('live on', '/ˌlɪv ˈɒn/', 'PHR', 'hasabyna ýaşamak', 'жить на (средства)', 'to use an amount of money to live', 'It is difficult to live on one salary.', 'Bir aýlyk hasabyna ýaşamak kyn.', 'B1'),
    ('live off', '/ˌlɪv ˈɒf/', 'PHR', 'hasabyna güzeran görmek', 'жить за счёт (кого-то)', 'to depend financially on someone', 'I lived off my parents while I was a student.', 'Talyptygymda ene-atamyň hasabyna ýaşadym.', 'B1'),
    ('get by', '/ˌɡet ˈbaɪ/', 'PHR', 'güzeranyny görmek', 'сводить концы с концами', 'to have just enough money to live', 'We get by on very little money.', 'Gaty az pul bilen güzeranymyzy görýäris.', 'B1'),
    ('run away', '/ˌrʌn əˈweɪ/', 'PHR', 'gaçmak', 'убегать', 'to leave quickly to escape', "Don't run away! I won't hurt you.", 'Gaçma! Saňa zyýan bermerin.', 'A2'),
    ('be away', '/ˌbiː əˈweɪ/', 'PHR', 'ýokda bolmak', 'отсутствовать', 'to not be in a place', 'The boss will be away until next week.', 'Boss indiki hepde çenli ýok.', 'A2'),
    ('put away', '/ˌpʊt əˈweɪ/', 'PHR', 'ýerine ýygnamak', 'убирать на место', 'to put something where it belongs', 'Put your toys away.', 'Oýunjaklaryňy ýerine ýygnaň.', 'A2'),
    ('take away', '/ˌteɪk əˈweɪ/', 'PHR', 'aýyrmak, eltip bermek', 'убирать; брать навынос', 'to remove something; to buy food to eat elsewhere', 'A paracetamol will take the pain away.', 'Parasetamol agyryny aýyrar.', 'A2'),
    ('get back', '/ˌɡet ˈbæk/', 'PHR', 'yzyna gelmek', 'возвращаться', 'to return to a place', "I'll get back in ten minutes.", 'On minutda yzyma gelýärin.', 'A2'),
    ('call back', '/ˌkɔːl ˈbæk/', 'PHR', 'yzyna jaň etmek', 'перезванивать', 'to phone someone again later', 'Could you call back in half an hour?', 'Ýarym sagatdan yzyňa jaň edip bilerşiňmi?', 'A2'),
    ('give back', '/ˌɡɪv ˈbæk/', 'PHR', 'yzyna bermek', 'возвращать', 'to return something', "That's my book! Give it back.", 'Bu meniň kitabym! Yzyna ber.', 'A2'),
    ('take after', '/ˌteɪk ˈɑːftə/', 'PHR', 'meňzemek', 'быть похожим на (родственника)', 'to be similar to an older family member', 'I take after my mother.', 'Eneme meňzeýärin.', 'B1'),
    ('take on', '/ˌteɪk ˈɒn/', 'PHR', 'işe almak', 'нанимать', 'to employ someone', 'They are taking on ten new interns.', 'On täze stajýor işe alýarlar.', 'B1'),
    ('take off', '/ˌteɪk ˈɒf/', 'PHR', 'çykarmak; uçmak', 'снимать; взлетать', 'to remove clothes; when a plane leaves the ground', 'Take your shoes off, please.', 'Aýakgabyňy çykar, haýyş.', 'A2'),
    ('take over', '/ˌteɪk ˈəʊvə/', 'PHR', 'öz üstüne almak', 'брать на себя; поглощать', 'to take control of something', 'My company was taken over by a big firm.', 'Kompaniýamy uly firma satyn aldy.', 'B1'),
    ('take apart', '/ˌteɪk əˈpɑːt/', 'PHR', 'böleklere bölmek', 'разбирать на части', 'to separate something into its parts', 'Take the keyboard apart to clean it.', 'Arassalamak üçin klawiaturany böleklere böl.', 'B1'),
    ('take up', '/ˌteɪk ˈʌp/', 'PHR', 'başlamak (hobbi)', 'начать заниматься', 'to start a new hobby or activity', "I think I'll take up running.", 'Ylgawa başlasym gelýär.', 'B1'),
    ('grow up', '/ˌɡrəʊ ˈʌp/', 'PHR', 'ulalmak, ýetişmek', 'взрослеть', 'to become an adult', 'I grew up on a farm.', 'Fermada ulaldym.', 'A2'),
    ('settle down', '/ˌsetl ˈdaʊn/', 'PHR', 'ornuşmak, maşgula gurmaka girişmek', 'остепениться, обустроиться', 'to start living a quiet life in one place', 'He moved back to the city to settle down and start a family.', 'Maşgula gurmak üçin şähere dolandy.', 'B1'),
    ('back up', '/ˌbæk ˈʌp/', 'PHR', 'ätiýaçlyk nusgasyny etmek', 'делать резервную копию', 'to copy a file so you do not lose it', 'Back up your files every week.', 'Her hepde faýllaryňyň nusgasyny et.', 'B1'),
    ('close down', '/ˌkləʊz ˈdaʊn/', 'PHR', 'ýapylmak', 'закрываться (о предприятии)', 'to stop being open permanently', 'The shop closed down last month.', 'Dükan geçen aý ýapyldy.', 'B1'),
    ('put up', '/ˌpʊt ˈʌp/', 'PHR', 'asmak, berkitmek', 'вешать, устанавливать', 'to fix something on a wall', 'We put up new shelves.', 'Täze tekçeleri asdyk.', 'B1'),
    ('send back', '/ˌsend ˈbæk/', 'PHR', 'yzyna ugratmak', 'отсылать обратно', 'to return something you bought', 'You can send back anything you bought online.', 'Onlaýn alan zadyňy yzyna ugradyp bolýar.', 'B1'),
    ('switch off', '/ˌswɪtʃ ˈɒf/', 'PHR', 'öçürmek', 'выключать', 'to stop a machine with a switch', 'Switch off the computer.', 'Kompýuteri öçür.', 'A2'),
    ('try on', '/ˌtraɪ ˈɒn/', 'PHR', 'geýip görmek', 'примерять', 'to put on clothes to see if they fit', 'Can I try on this jacket?', 'Bu penjegi geýip görüp bilerinmi?', 'A2'),
    ('keep away', '/ˌkiːp əˈweɪ/', 'PHR', 'daşda saklamak', 'отпугивать, держать подальше', 'to stop something coming near', 'The spray keeps away insects.', 'Spreý mör-möjekleri daşda saklaýar.', 'B1'),
    ('ask for', '/ˌɑːsk ˈfɔː/', 'PHR', 'soramak', 'просить', 'to say you want something', 'Ask for the bill when you are ready.', 'Taýýar bolsaň hasap sora.', 'A2'),
    ('be out of', '/ˌbiː aʊt əv/', 'PHR', 'gutarmak, ýok bolmak', 'закончиться (о товаре)', 'to have none left', 'We are out of milk.', 'Süýt gutardy.', 'A2'),
    ('look for', '/ˌlʊk ˈfɔː/', 'PHR', 'gözlemek', 'искать', 'to try to find something', 'I am looking for a cash machine.', 'Bankomat gözleýärin.', 'A2'),
    ('look round', '/ˌlʊk ˈraʊnd/', 'PHR', 'aýlanyp görmek', 'осматривать', 'to walk around a place and look at it', 'We looked round the shop.', 'Dükany aýlanyp gördük.', 'B1'),
    ('sell out', '/ˌsel ˈaʊt/', 'PHR', 'gutarmak (satuwda)', 'распродаваться', 'when all of something is sold', 'The concert tickets sold out in an hour.', 'Konsert biletleri bir sagatda gutardy.', 'B1'),
    ('zoom in', '/ˌzuːm ˈɪn/', 'PHR', 'ulaltmak (surat)', 'приближать (изображение)', 'to make something look closer or bigger', 'Zoom in on the person you want to photograph.', 'Surata düşürjek adamyňy ulalt.', 'B1'),
]

# ---- in-lesson 7B — live entertainment ----
T['live_entertainment'] = [
    ('concert', '/ˈkɒnsət/', 'N', 'konsert', 'концерт', 'a live music performance', 'We went to a rock concert.', 'Rok konsertine gitdik.', 'A2'),
    ('stage', '/steɪdʒ/', 'N', 'sahna', 'сцена', 'the platform where performers stand', 'The band walked onto the stage.', 'Topar sahna çykdy.', 'A2', 'on stage'),
    ('front row', '/ˌfrʌnt ˈrəʊ/', 'N', 'öňdäki hatar', 'первый ряд', 'the seats nearest the stage', 'We sat in the front row.', 'Öňdäki hatarda oturduk.', 'A2', 'in the front row'),
    ('encore', '/ˈɑːnkɔː(r)/', 'N', 'gaýtadan çykyş', 'выступление на бис', 'an extra song after the show', 'The crowd shouted for an encore.', 'Märele gaýtadan çykyş sorap gygyrdy.', 'B1'),
    ('sold out', '/ˌsəʊld ˈaʊt/', 'ADJ', 'biletler gutaran', 'распроданный', 'with all tickets sold', 'The show was sold out.', 'Tomaşanyň biletleri gutardy.', 'A2'),
    ('interval', '/ˈɪntəvl/', 'N', 'arakesme', 'антракт', 'a break in the middle of a show', 'We bought drinks at the interval.', 'Arakesmede içgi aldyk.', 'B1'),
    ('orchestra', '/ˈɔːkɪstrə/', 'N', 'orkestr', 'оркестр', 'a large group of musicians', 'The orchestra played beautifully.', 'Orkestr owadan çaldy.', 'A2'),
    ('applause', '/əˈplɔːz/', 'N', 'el çarpyşma', 'аплодисменты', 'clapping to show you liked it', 'The room burst into applause.', 'Otag el çarpyşma gaplandy.', 'A2', 'round of applause'),
    ('live', '/laɪv/', 'ADJ', 'göni (janly)', 'живой (в прямом эфире)', 'happening now, in person', 'I prefer live music.', 'Göni sazy gowy görýärin.', 'A2', 'live performance'),
    ('show', '/ʃəʊ/', 'N', 'tomaşa', 'шоу, представление', 'a performance for an audience', 'The show starts at eight.', 'Tomaşa sekizde başlaýar.', 'A1'),
]

# ---- Vocabulary Bank — Looking after yourself -> 8A ----
T['looking_after'] = [
    ('treat', '/triːt/', 'V', 'hezzetlemek (höwes)', 'баловать, побаловать', 'to do something nice for yourself', 'Treat yourself to a massage.', 'Özüňi massaj bilen hezzetle.', 'A2', 'treat yourself'),
    ('spa', '/spɑː/', 'N', 'spa (suw bejergisi)', 'спа', 'a place for relaxing treatments', 'They spent the day at a spa.', 'Güni spa-da geçirdiler.', 'A2'),
    ('massage', '/ˈmæsɑːʒ/', 'N', 'massaj', 'массаж', 'rubbing the body to relax it', 'A back massage helped her relax.', 'Arka massajy köşeşmäge kömek etdi.', 'A2', 'have a massage'),
    ('pamper', '/ˈpæmpə(r)/', 'V', 'erjelletmek (hezzet)', 'баловать, нежить', 'to look after someone with treats', 'She pampered herself all weekend.', 'Hepde ahyry özini erjelletdi.', 'B1'),
    ('relax', '/rɪˈlæks/', 'V', 'köşeşmek', 'расслабляться', 'to rest and feel calm', 'Music helps me relax.', 'Saz maňa köşeşmäge kömek edýär.', 'A2'),
    ('unwind', '/ˌʌnˈwaɪnd/', 'V', 'dynç almak (köşeşmek)', 'расслабляться, развеяться', 'to relax after stress', 'I unwind with a long bath.', 'Uzyn wanna bilen dynç alýaryn.', 'B1'),
    ('sauna', '/ˈsaʊnə/', 'N', 'sauna', 'сауна', 'a hot room for sweating and relaxing', 'They cooled off after the sauna.', 'Saunadan soň sowyndylar.', 'A2'),
    ('manicure', '/ˈmænɪkjʊə(r)/', 'N', 'manikýur', 'маникюр', 'care for the hands and nails', 'She had a manicure yesterday.', 'Düýn manikýur etdirdi.', 'B1'),
    ('wellbeing', '/ˌwelˈbiːɪŋ/', 'N', 'sagdynlyk (abadaňlyk)', 'благополучие', 'the state of being healthy and happy', 'Exercise improves your wellbeing.', 'Maşk sagdynlygyňy gowulandyrýar.', 'B2'),
    ('beauty salon', '/ˈbjuːti ˈsælɒn/', 'N', 'gözellik salony', 'салон красоты', 'a place for beauty treatments', 'The beauty salon is on Main Street.', 'Gözellik salony Baş köçede.', 'A2'),
    ('facial', '/ˈfeɪʃl/', 'N', 'ýüz bejergisi', 'процедура для лица', 'a beauty treatment for the face', 'She had a facial at the spa.', 'Spada ýüz bejergisini aldy.', 'B1'),
    ('yoga', '/ˈjəʊɡə/', 'N', 'ýoga', 'йога', 'exercises for the body and breathing', 'She does yoga every morning.', 'Her irden ýoga edýär.', 'A2'),
    ('pilates', '/pɪˈlɑːtiːz/', 'N', 'pilates', 'пилатес', 'exercises that develop the body muscles', 'Pilates is good for your back.', 'Pilates arkaň üçin peýdaly.', 'B1'),
    ('pedicure', '/ˈpedɪkjʊə/', 'N', 'pedikýur', 'педикюр', 'a beauty treatment for your feet', 'I had a manicure and a pedicure.', 'Manikýur we pedikýur etdirdim.', 'B1'),
    ('fringe', '/frɪndʒ/', 'N', 'maňlaý saç', 'чёлка', 'short hair that hangs over your forehead', 'She cut her fringe herself.', 'Maňlaý saçyny özi kesdi.', 'B1'),
    ('parting', '/ˈpɑːtɪŋ/', 'N', 'saç aýryşy', 'пробор', 'the line where hair is divided', 'He has a parting on the left.', 'Çep tarapda saç aýryşy bar.', 'B1'),
    ('highlights', '/ˈhaɪlaɪts/', 'N', 'açyk reňkli saç tutamlary', 'мелирование', 'parts of hair made lighter than the rest', 'She had blonde highlights.', 'Saryşyn tutamlar etdirdi.', 'B1'),
    ('buzz cut', '/ˈbʌz kʌt/', 'N', 'gaty gysga saç kesimi', 'очень короткая стрижка', 'a very short haircut', 'He had a buzz cut in the army.', 'Goşunda gaty gysga saç kesdirdi.', 'B1'),
    ('ponytail', '/ˈpəʊniteɪl/', 'N', 'guýruk saç', 'хвост (причёска)', 'hair tied at the back of the head', 'She wore her hair in a ponytail.', 'Saçyny guýruk edip daňdy.', 'B1'),
    ('plaits', '/plæts/', 'N', 'örgüli saç', 'косы', 'hair made by twisting three parts together', 'The girl had two plaits.', 'Gyzjagazyň iki örgüli saçy bardy.', 'B1'),
    ('cross-trainer', '/ˈkrɒs treɪnə/', 'N', 'kross türgenleşik enjamy', 'кросс-тренажёр', 'an exercise machine for arms and legs', 'He uses the cross-trainer for twenty minutes.', 'Ýigrimi minut kross-trenažýory ulanýar.', 'B1'),
    ('rowing machine', '/ˈrəʊɪŋ məʃiːn/', 'N', 'greb türgenleşik enjamy', 'гребной тренажёр', 'an exercise machine you pull like rowing', 'The rowing machine is very hard work.', 'Grebleý trenažýory gaty kyn iş.', 'B1'),
    ('running machine', '/ˈrʌnɪŋ məʃiːn/', 'N', 'ylgaw türgenleşik enjamy', 'беговая дорожка', 'a machine with a moving surface you run on', 'She runs on the running machine.', 'Ylgaw trenažýorynda ylgaw edýär.', 'B1'),
    ('exercise bike', '/ˈeksəsaɪz baɪk/', 'N', 'türgenleşik welosipedi', 'велотренажёр', 'a bicycle that stays in one place for exercise', 'I ride the exercise bike while watching TV.', 'Telewizor görüp türgenleşik welosipedini münýärin.', 'B1'),
    ('sit-ups', '/ˈsɪtʌps/', 'N', 'oturyp-turmak maşky', 'упражнение на пресс', 'an exercise where you sit up from lying down', 'He does fifty sit-ups every day.', 'Her gün elli oturyp-turmak maşky edýär.', 'B1'),
    ('press-ups', '/ˈpresʌps/', 'N', 'otjimaniýe', 'отжимания', 'an exercise lifting your body on your hands', 'Can you do twenty press-ups?', 'Ýigrimi otžimaniýe edip bilýäňmi?', 'B1'),
    ('aerobics', '/eəˈrəʊbɪks/', 'N', 'aerobika', 'аэробика', 'active exercises done to music', 'She goes to aerobics on Tuesdays.', 'Sişenbe günleri aerobika gatnaşýar.', 'B1'),
    ('spinning', '/ˈspɪnɪŋ/', 'N', 'spinning', 'спиннинг (велотренировка)', 'aerobic exercises on an exercise bike with music', 'Spinning classes are very popular.', 'Spinning sapaklary gaty meşhur.', 'B1'),
    ('trim', '/trɪm/', 'N', 'saç ujyny almak', 'подравнивание (кончиков)', 'a small haircut to make hair tidy', 'Just a trim, please.', 'Diňe ujyny alyň, haýyş.', 'B1'),
    ('blow dry', '/ˈbləʊ draɪ/', 'N', 'fen bilen guramak', 'укладка феном', 'drying hair with warm air', 'She had a wash and blow dry.', 'Saçyny ýuwdurdy we fen etdirdi.', 'B1'),
]

# ---- in-lesson 8B — wars and battles, historic buildings ----
T['historic'] = [
    ('castle', '/ˈkɑːsl/', 'N', 'gala', 'замок', 'a large strong building from the past', 'The castle overlooks the town.', 'Gala şähere syn edýär.', 'A2'),
    ('fortress', '/ˈfɔːtrəs/', 'N', 'gala (berkitme)', 'крепость', 'a strong place built for defence', 'The fortress was never captured.', 'Gala hiç wagt alynmady.', 'B1'),
    ('monument', '/ˈmɒnjumənt/', 'N', 'ýadygärlik', 'памятник, монумент', 'a statue built to remember', 'They laid flowers at the monument.', 'Ýadygärlige gül goýdular.', 'A2'),
    ('memorial', '/məˈmɔːriəl/', 'N', 'hatyra ýadygärligi', 'мемориал', 'something built to remember people', 'The memorial honours the fallen.', 'Hatyra ýadygärligi pidalary hatyralaýar.', 'B1'),
    ('statue', '/ˈstætʃuː/', 'N', 'heýkel', 'статуя', 'a figure of a person or animal', 'A statue stands in the square.', 'Meýdançada heýkel dur.', 'A2'),
    ('cathedral', '/kəˈθiːdrəl/', 'N', 'uly ybadathana', 'собор', 'a very large church', 'The cathedral took 200 years to build.', 'Uly ybadathana 200 ýylda gurlupdyr.', 'A2'),
    ('tower', '/ˈtaʊə(r)/', 'N', 'minara (diň)', 'башня', 'a tall narrow building', 'We climbed the old tower.', 'Köne minara dyrmaşdyk.', 'A2'),
    ('ruins', '/ˈruːɪnz/', 'N', 'harabalar', 'руины', 'the remains of an old building', 'We explored the ancient ruins.', 'Gadymy harabalary öwrendik.', 'A2'),
    ('ancient', '/ˈeɪnʃənt/', 'ADJ', 'gadymy', 'древний', 'very old, from long ago', 'The museum has ancient coins.', 'Muzeýde gadymy teňňeler bar.', 'A2'),
    ('tomb', '/tuːm/', 'N', 'mazar (gübbez)', 'гробница', 'a place where a dead person lies', 'The king was buried in a tomb.', 'Patyşa mazarda jaýlanypdyr.', 'B1'),
    ('palace', '/ˈpæləs/', 'N', 'köşk', 'дворец', 'the home of a king or queen', 'The palace has 300 rooms.', 'Köşküň 300 otagy bar.', 'A2'),
    ('temple', '/ˈtempl/', 'N', 'ybadathana', 'храм', 'a building for worship', 'The temple is on the hill.', 'Ybadathana depede.', 'A2'),
    ('archer', '/ˈɑːtʃə/', 'N', 'ýaý atyjy', 'лучник', 'a person who shoots with a bow and arrow', 'The archers stood on the wall.', 'Ýaý atyjylar diwaryň üstünde durdy.', 'B1'),
    ('arrow', '/ˈærəʊ/', 'N', 'ok', 'стрела', 'a thin stick shot from a bow', 'The arrow hit the target.', 'Ok nyşana degdi.', 'B1'),
    ('bow', '/bəʊ/', 'N', 'ýaý', 'лук (оружие)', 'a weapon for shooting arrows', 'He shot the bow with skill.', 'Ýaýy ussatlyk bilen atdy.', 'B1'),
    ('helmet', '/ˈhelmɪt/', 'N', 'duýga, kaska', 'шлем', 'a hard hat that protects your head', 'The soldiers wore metal helmets.', 'Esgeler demir duýga geýdi.', 'B1'),
    ('shield', '/ʃiːld/', 'N', 'galkan', 'щит', 'a cover you hold to protect yourself in a fight', 'He carried a wooden shield.', 'Agaç galkan göterdi.', 'B1'),
    ('battle', '/ˈbætl/', 'N', 'söweş', 'битва, сражение', 'a fight between armies', 'The Battle of Hastings was in 1066.', 'Gastings söweşi 1066-njy ýylda boldy.', 'B1'),
]

# ---- in-lesson 9A — word building ----
T['word_building3'] = [
    ('unbelievable', '/ˌʌnbɪˈliːvəbl/', 'ADJ', 'ynanyp bolmajak', 'невероятный', 'impossible to believe', 'The news was unbelievable.', 'Habar ynanyp bolmajak boldy.', 'A2'),
    ('unbreakable', '/ˌʌnˈbreɪkəbl/', 'ADJ', 'döwülmeýän', 'небьющийся', 'impossible to break', 'The phone has an unbreakable screen.', 'Telefonyň döwülmeýän ekrany bar.', 'B1'),
    ('unforgettable', '/ˌʌnfəˈɡetəbl/', 'ADJ', 'ýatdan çykmaz', 'незабываемый', 'impossible to forget', 'We had an unforgettable trip.', 'Ýatdan çykmaz sapar etdik.', 'A2'),
    ('misunderstanding', '/ˌmɪsʌndəˈstændɪŋ/', 'N', 'nädogry düşünme', 'недоразумение', 'a failure to understand correctly', 'It was just a misunderstanding.', 'Diňe nädogry düşünme boldy.', 'A2'),
    ('rewrite', '/ˌriːˈraɪt/', 'V', 'täzeden ýazmak', 'переписывать', 'to write something again', 'I had to rewrite the essay.', 'Esseýi täzeden ýazmaly boldum.', 'A2'),
    ('retell', '/ˌriːˈtel/', 'V', 'gaýtadan gürrüň bermek', 'пересказывать', 'to tell a story again', 'Retell the story in your own words.', 'Hekaýany öz sözüň bilen gaýtadan gürrüň ber.', 'B1'),
    ('rediscover', '/ˌriːdɪˈskʌvə(r)/', 'V', 'täzeden açmak', 'заново открыть', 'to find something again', 'She rediscovered her love of painting.', 'Suratkeşlige bolan söýgüsini täzeden açdy.', 'B1'),
    ('reconnect', '/ˌriːkəˈnekt/', 'V', 'täzeden birikmek', 'воссоединиться', 'to join or meet again', 'He reconnected with old friends.', 'Köne dostlary bilen täzeden birikdi.', 'B1'),
    ('reappear', '/ˌriːəˈpɪə(r)/', 'V', 'täzeden peýda bolmak', 'снова появиться', 'to appear again', 'The sun reappeared after the rain.', 'Ýagyşdan soň Gün täzeden peýda boldy.', 'B1'),
    ('unstoppable', '/ʌnˈstɒpəbl/', 'ADJ', 'saklanyp bolmajak', 'неудержимый', 'impossible to stop', 'The team was unstoppable.', 'Topar saklanyp bolmajak boldy.', 'B1'),
    ('fearless', '/ˈfɪələs/', 'ADJ', 'gorkusyz', 'бесстрашный', 'not afraid of anything', 'The fearless climber reached the top.', 'Gorkusyz alpinist depä ýetdi.', 'B1'),
    ('hopeless', '/ˈhəʊpləs/', 'ADJ', 'umytsyz (başarnyksyz)', 'безнадёжный', 'with no hope, or very bad at something', 'He is hopeless at maths.', 'Matematikada başarnyksyz.', 'A2'),
    ('ability', '/əˈbɪləti/', 'N', 'ukyptylyk', 'способность', 'the skill to do something', 'She has the ability to learn languages.', 'Dil öwrenmek ukyby bar.', 'B1'),
    ('accurate', '/ˈækjərət/', 'ADJ', 'takyk', 'точный', 'correct and without mistakes', 'The weather report was not accurate.', 'Howa maglumaty takyk däldi.', 'B1'),
    ('atomic', '/əˈtɒmɪk/', 'ADJ', 'atom', 'атомный', 'using the energy of atoms', 'Atomic energy is controversial.', 'Atom energiýasy jedelli mesele.', 'B2'),
    ('autobiographical', '/ˌɔːtəbaɪəˈɡræfɪkl/', 'ADJ', 'awtobiografik', 'автобиографический', 'about the writer’s own life', 'The novel has autobiographical elements.', 'Romanda awtobiografik elementler bar.', 'B2'),
    ('connection', '/kəˈnekʃn/', 'N', 'aragatnaşyk, baglanyşyk', 'связь', 'a link between things', 'There is a connection between the two events.', 'Iki wakanyň arasynda baglanyşyk bar.', 'B1'),
    ('easily', '/ˈiːzɪli/', 'ADV', 'aňsatlyk bilen', 'легко', 'without difficulty', 'She won easily.', 'Aňsatlyk bilen ýeňdi.', 'A2'),
    ('emotional', '/ɪˈməʊʃənl/', 'ADJ', 'duýguly', 'эмоциональный', 'about feelings', 'It was an emotional moment.', 'Duýguly pursatdy.', 'B1'),
    ('memorable', '/ˈmemərəbl/', 'ADJ', 'ýatdan çykmajak', 'незабываемый', 'easy to remember because it is special', 'We had a memorable holiday.', 'Ýatdan çykmajak dynç alyş geçirdik.', 'B1'),
    ('memorize', '/ˈmeməraɪz/', 'V', 'ýatda saklamak', 'запоминать', 'to learn something so you remember it', 'We memorized the poem.', 'Goşgyny ýatda sakladyk.', 'B1'),
    ('recall', '/rɪˈkɔːl/', 'V', 'ýada salmak', 'вспоминать', 'to remember something', 'I cannot recall his name.', 'Adyny ýada salyp bilemok.', 'B1'),
    ('remind', '/rɪˈmaɪnd/', 'V', 'ýatlatmak', 'напоминать', 'to help someone remember', 'Remind me to call her.', 'Oňa jaň etmegimi ýatlat.', 'B1'),
    ('unlikely', '/ʌnˈlaɪkli/', 'ADJ', 'ähtimal däl', 'маловероятный', 'not likely to happen', 'It is unlikely to rain today.', 'Bu gün ýagyş ähtimal däl.', 'B1'),
    ('unpleasant', '/ʌnˈpleznt/', 'ADJ', 'ýakymsyz', 'неприятный', 'not nice', 'There was an unpleasant smell.', 'Ýakymsyz ys bardy.', 'B1'),
]

# ---- in-lesson 9B — weddings ----
T['weddings'] = [
    ('bride', '/braɪd/', 'N', 'gälin', 'невеста', 'a woman on her wedding day', 'The bride wore a white dress.', 'Gälin ak köýnek geýdi.', 'A2'),
    ('groom', '/ɡruːm/', 'N', 'ýigit (täze öýlenen)', 'жених', 'a man on his wedding day', 'The groom looked nervous.', 'Ýigit tolgunýan ýaly boldy.', 'A2'),
    ('wedding', '/ˈwedɪŋ/', 'N', 'toý', 'свадьба', 'the ceremony when people marry', 'The wedding was in June.', 'Toý iýunda boldy.', 'A2'),
    ('honeymoon', '/ˈhʌnimuːn/', 'N', 'aý bal', 'медовый месяц', 'a holiday after getting married', 'They spent their honeymoon in Bali.', 'Aý balyny Balide geçirdiler.', 'A2'),
    ('ceremony', '/ˈserəməni/', 'N', 'däp-dessur (ýörite)', 'церемония', 'a formal event', 'The ceremony was short and sweet.', 'Däp-dessur gysga we owadan boldy.', 'A2'),
    ('vows', '/vaʊz/', 'N', 'ant (wada)', 'обеты, клятвы', 'promises made at a wedding', 'They exchanged their vows.', 'Antlaryny çalyşdylar.', 'B1', 'wedding vows'),
    ('ring', '/rɪŋ/', 'N', 'ýüzük', 'кольцо', 'a circle worn on the finger', 'He gave her a gold ring.', 'Altyn ýüzük berdi.', 'A1', 'wedding ring'),
    ('best man', '/ˌbest ˈmæn/', 'N', 'ýigidiň ýoldaşy', 'свидетель (шафер)', 'the man who helps the groom', 'His brother was the best man.', 'Dogany ýigidiň ýoldaşy boldy.', 'B1'),
    ('bridesmaid', '/ˈbraɪdzmeɪd/', 'N', 'gäliniň ýoldaşy', 'подружка невесты', 'a woman who helps the bride', 'Her sister was a bridesmaid.', 'Uýasy gäliniň ýoldaşy boldy.', 'B1'),
    ('reception', '/rɪˈsepʃn/', 'N', 'toý çäresi', 'свадебный приём', 'the party after a wedding', 'The reception lasted all night.', 'Toý çäresi bütin gije dowam etdi.', 'B1', 'wedding reception'),
    ('propose', '/prəˈpəʊz/', 'V', 'hödürlemek (öýlenmek)', 'делать предложение', 'to ask someone to marry you', 'He proposed on the beach.', 'Kenarda öýlenmek hödürledi.', 'A2', 'propose marriage'),
    ('marriage', '/ˈmærɪdʒ/', 'N', 'nika', 'брак, супружество', 'the state of being married', 'Their marriage is very happy.', 'Nikalary gaty bagtly.', 'A2'),
    ('couple', '/ˈkʌpl/', 'N', 'jübüt', 'пара', 'two people in a romantic relationship', 'The couple got married in June.', 'Jübüt iýunda öýlendi.', 'B1'),
    ('guest', '/ɡest/', 'N', 'myhman', 'гость', 'a person invited to an event', 'There were eighty guests at the wedding.', 'Toýda segsen myhman bardy.', 'A2'),
    ('invitation', '/ˌɪnvɪˈteɪʃn/', 'N', 'çakylyk', 'приглашение', 'a message asking you to come', 'We sent out the wedding invitations.', 'Toý çakylyklaryny ugratdyk.', 'B1'),
    ('engaged', '/ɪnˈɡeɪdʒd/', 'ADJ', 'ygtyýarly (nika)', 'помолвленный', 'having promised to marry someone', 'They got engaged on holiday.', 'Dynç alyşda nika ygtyýar boldylar.', 'B1'),
]

# ---- in-lesson 10A — British and American English ----
T['brit_amer'] = [
    ('lift', '/lɪft/', 'N', 'lift (amer. elevator)', 'лифт', 'a machine that moves people up (British English)', 'Take the lift to the fifth floor.', 'Bäşinji gata liftde çyk.', 'A1'),
    ('flat', '/flæt/', 'N', 'öý (amer. apartment)', 'квартира', 'a set of rooms to live in (British English)', 'She lives in a small flat.', 'Kiçi öýde ýaşaýar.', 'A1'),
    ('boot', '/buːt/', 'N', 'bagajnik (amer. trunk)', 'багажник', 'the space for bags in a car (British English)', 'Put the cases in the boot.', 'Çemodanlary bagaja goý.', 'A2'),
    ('petrol', '/ˈpetrəl/', 'N', 'benzin (amer. gas)', 'бензин', 'fuel for cars (British English)', 'We need to buy petrol.', 'Benzin almaly.', 'A2'),
    ('biscuit', '/ˈbɪskɪt/', 'N', 'köke (amer. cookie)', 'печенье', 'a small sweet baked food (British English)', 'Have a biscuit with your tea.', 'Çaýyň bilen köke iý.', 'A2'),
    ('lorry', '/ˈlɒri/', 'N', 'ýük maşyny (amer. truck)', 'грузовик', 'a big road vehicle (British English)', 'A lorry blocked the road.', 'Ýük maşyny ýoly böwetdi.', 'A2'),
    ('pavement', '/ˈpeɪvmənt/', 'N', 'ýodajyk (amer. sidewalk)', 'тротуар', 'the path beside a road (British English)', 'Walk on the pavement.', 'Ýodajykdan ýöre.', 'A2'),
    ('queue', '/kjuː/', 'N', 'nobat (amer. line)', 'очередь', 'a line of waiting people (British English)', 'There was a long queue.', 'Uzyn nobat bardy.', 'A2'),
    ('torch', '/tɔːtʃ/', 'N', 'el çyrasy (amer. flashlight)', 'фонарик', 'a small light you carry (British English)', 'Shine the torch here.', 'El çyrasyny şu ýere tut.', 'A2'),
    ('jumper', '/ˈdʒʌmpə(r)/', 'N', 'switer (amer. sweater)', 'свитер, джемпер', 'a warm top (British English)', 'Wear a jumper, it is cold.', 'Switer geý, sowuk.', 'A2'),
    ('tap', '/tæp/', 'N', 'kran (amer. faucet)', 'кран', 'where water comes out (British English)', 'Turn off the tap.', 'Krany ýap.', 'A2'),
    ('mobile phone', '/ˌməʊbaɪl ˈfəʊn/', 'N', 'jübi telefony (amer. cell phone)', 'мобильный телефон', 'a phone you carry (British English)', 'She left her mobile phone at home.', 'Jübi telefonuny öýde goýdy.', 'A1'),
    ('cinema', '/ˈsɪnəmə/', 'N', 'kinoteatr (BrE)', 'кинотеатр (брит.)', 'a place where you watch films (British English)', 'We went to the cinema on Saturday.', 'Şenbe güni kinoteatra gitdik.', 'A2'),
    ('postcode', '/ˈpəʊstkəʊd/', 'N', 'poçta kody (BrE)', 'почтовый индекс (брит.)', 'letters and numbers in a British address', 'What is your postcode?', 'Poçta kodyň näme?', 'B1'),
    ('secondary school', '/ˈsekəndri skuːl/', 'N', 'orta mekdep (BrE)', 'средняя школа (брит.)', 'a school for children aged 11 to 16 in Britain', 'She starts secondary school in September.', 'Sentýabrda orta mekdebe başlaýar.', 'B1'),
    ('toilet', '/ˈtɔɪlət/', 'N', 'hajathana (BrE)', 'туалет (брит.)', 'a room with a seat for getting rid of waste (British English)', 'Where is the toilet, please?', 'Hajathana nirede, haýyş?', 'A2'),
    ('trainers', '/ˈtreɪnəz/', 'N', 'krossowka (BrE)', 'кроссовки (брит.)', 'comfortable shoes for sport (British English)', 'He bought new trainers for running.', 'Ylgaw üçin täze krossowka aldy.', 'A2'),
]

# ---- in-lesson 10B — exams ----
T['exams'] = [
    ('exam', '/ɪɡˈzæm/', 'N', 'synag', 'экзамен', 'a formal test', 'The exam is on Friday.', 'Synag anna güni.', 'A1', 'take an exam'),
    ('pass', '/pɑːs/', 'V', 'geçmek (synagdan)', 'сдать (экзамен)', 'to succeed in an exam', 'She passed all her exams.', 'Ähli synaglardan geçdi.', 'A2', 'pass an exam'),
    ('grade', '/ɡreɪd/', 'N', 'baha (dereje)', 'оценка, отметка', 'a mark showing your level', 'He got the top grade.', 'Iň ýokary bahany aldy.', 'A2'),
    ('mark', '/mɑːk/', 'N', 'bal (baha)', 'балл, отметка', 'a score for a piece of work', 'You lost marks for spelling.', 'Ýazuw üçin bal ýitirdiň.', 'A2', 'full marks'),
    ('result', '/rɪˈzʌlt/', 'N', 'netije', 'результат', 'the outcome of a test', 'The results come out tomorrow.', 'Netijeler ertir çykýar.', 'A2', 'exam result'),
    ('paper', '/ˈpeɪpə(r)/', 'N', 'synag kagyzy', 'экзаменационная работа', 'a set of exam questions', 'Turn over your paper.', 'Synag kagyzyňy öwür.', 'A2', 'exam paper'),
    ('question', '/ˈkwestʃən/', 'N', 'soral', 'вопрос', 'something you must answer', 'Answer every question.', 'Her soraga jogap ber.', 'A1'),
    ('answer', '/ˈɑːnsə(r)/', 'N', 'jogap', 'ответ', 'what you write or say back', 'Write your answer clearly.', 'Jogabyňy aýdyň ýaz.', 'A1', 'the right answer'),
    ('score', '/skɔː(r)/', 'N', 'bal (utuk)', 'счёт, балл', 'the number of points you get', 'Her score was 95 out of 100.', 'Baly 100-den 95 boldy.', 'A2', 'high score'),
    ('pass mark', '/ˈpɑːs mɑːk/', 'N', 'geçiş baly', 'проходной балл', 'the score needed to pass', 'The pass mark is 60 per cent.', 'Geçiş baly 60 göterim.', 'B1'),
    ('fail', '/feɪl/', 'V', 'ýykylyp galmak (geçip bilmezlik)', 'провалить (экзамен)', 'to not pass an exam', 'He failed the driving test.', 'Sürüjilik synagyndan geçip bilmedi.', 'A2', 'fail an exam'),
    ('oral', '/ˈɔːrəl/', 'ADJ', 'dildeki (sözleýin)', 'устный', 'spoken, not written', 'The oral exam was easier.', 'Sözleýin synag aňsat boldy.', 'B1', 'oral exam'),
]

# ---- Practical English episodes ----
T['pe_luggage'] = [
    ('report lost luggage', '/rɪˈpɔːt lɒst ˈlʌɡɪdʒ/', 'PHR', 'ýitirilen ýük barada habar bermek', 'сообщить о потере багажа', 'to tell the airport your bag is missing', 'I need to report lost luggage.', 'Ýitirilen ýük barada habar bermeli.', 'A2'),
    ('lost property', '/lɒst ˈprɒpəti/', 'N', 'ýitirilen zatlar bölümi', 'бюро находок', 'the office for lost things', 'Ask at the lost property office.', 'Ýitirilen zatlar bölüminde sora.', 'A2'),
    ('baggage claim', '/ˈbæɡɪdʒ kleɪm/', 'N', 'ýük alýan ýer', 'зона выдачи багажа', 'where you collect your bags', 'Your case is at baggage claim.', 'Çemodanyň ýük alýan ýerde.', 'A2'),
    ('It did not arrive.', '/ɪt ˈdɪd nɒt əˈraɪv/', 'PHR', 'Gelmedi.', 'Он не прибыл.', 'used to say your bag is missing', 'My suitcase did not arrive.', 'Çemodanym gelmedi.', 'A2'),
    ('fill in this form', '/fɪl ɪn ðɪs fɔːm/', 'PHR', 'Şu formany dolduryň.', 'Заполните эту форму.', 'used to ask for written details', 'Please fill in this form.', 'Şu formany dolduryň.', 'A2'),
    ('reference number', '/ˈrefrəns ˈnʌmbə(r)/', 'N', 'salgylanma belgisi', 'номер дела', 'a code for your case', 'Write down the reference number.', 'Salgylanma belgisini ýazyp al.', 'A2'),
    ('It is a black suitcase.', '/ɪt ɪz ə blæk ˈsuːtkeɪs/', 'PHR', 'Gara çemodan.', 'Это чёрный чемодан.', 'used to describe your bag', 'It is a black suitcase with wheels.', 'Tekerli gara çemodan.', 'A2'),
    ('contact details', '/ˈkɒntækt ˈdiːteɪlz/', 'N', 'aragatnaşyk maglumatlary', 'контактные данные', 'your phone and address', 'Leave your contact details.', 'Aragatnaşyk maglumatlaryňyzy goýuň.', 'A2'),
    ('address', '/əˈdres/', 'N', 'salgy', 'адрес', 'where someone lives or a building is', 'Please write your address on the form.', 'Salgyňyzy formanyň üstüne ýazyň.', 'A2'),
    ('describe', '/dɪˈskraɪb/', 'V', 'wasyp bermek', 'описывать', 'to say what something is like', 'Describe your bag, please.', 'Torbaňyzy wasyp beriň, haýyş.', 'A2'),
    ('details', '/ˈdiːteɪlz/', 'N', 'maglumatlar', 'данные, детали', 'small facts about something', 'Fill in your contact details.', 'Aragatnaşyk maglumatlaryňyzy dolduryň.', 'A2'),
    ('sign', '/saɪn/', 'V', 'gol çekmek', 'подписывать', 'to write your name on something', 'Sign the form here.', 'Forma şu ýerde gol çekiň.', 'A2'),
    ('size', '/saɪz/', 'N', 'ölçeg', 'размер', 'how big something is', 'What size is the suitcase?', 'Çemodanyň ölçegi nähili?', 'A2'),
    ('visitor', '/ˈvɪzɪtə/', 'N', 'myhman, gelim-gidimli', 'посетитель', 'a person who visits a place', 'The museum has thousands of visitors.', 'Muzeýde müňlerçe myhman bar.', 'A2'),
]

T['pe_rentcar'] = [
    ('rent a car', '/rent ə kɑː(r)/', 'PHR', 'maşyn kärendesine almak', 'взять машину напрокат', 'to pay to use a car', 'I would like to rent a car.', 'Maşyn kärendesine almak isleýärin.', 'A2'),
    ('full insurance', '/fʊl ɪnˈʃʊərəns/', 'N', 'doly ätiýaçlandyrma', 'полная страховка', 'cover for all damage', 'Does the price include full insurance?', 'Baha doly ätiýaçlandyrmany öz içine alýarmy?', 'B1'),
    ('unlimited mileage', '/ʌnˈlɪmɪtɪd ˈmaɪlɪdʒ/', 'N', 'çäksiz ýol', 'неограниченный пробег', 'no limit on how far you drive', 'Is there unlimited mileage?', 'Çäksiz ýol barmy?', 'B1'),
    ('automatic or manual', '/ˌɔːtəˈmætɪk ɔː ˈmænjuəl/', 'PHR', 'awtomat ýa-da mehaniki', 'автомат или механика', 'used to ask the gear type', 'Is it automatic or manual?', 'Awtomat ýa-da mehaniki?', 'A2'),
    ('Is petrol included?', '/ɪz ˈpetrəl ɪnˈkluːdɪd/', 'PHR', 'Benzin goşuldymy?', 'Бензин включён?', 'used to ask about fuel', 'Is petrol included in the price?', 'Baha benzin goşuldymy?', 'A2'),
    ('security deposit', '/sɪˈkjʊərɪti dɪˈpɒzɪt/', 'N', 'depozit (öňünden)', 'залог', 'money paid first as security', 'There is a 500 manat deposit.', '500 manat depozit bar.', 'A2'),
    ('How long for?', '/haʊ lɒŋ fə(r)/', 'PHR', 'Näçe wagtlyk?', 'На какой срок?', 'used to ask the rental period', 'How long for? — Three days.', 'Näçe wagtlyk? — Üç gün.', 'A2'),
    ('Can I see your licence?', '/kæn aɪ siː jɔː(r) ˈlaɪsns/', 'PHR', 'Prawaňyzy görüp bilerinmi?', 'Можно ваши права?', 'used to check driving papers', 'Can I see your licence, please?', 'Prawaňyzy görüp bilerinmi?', 'A2'),
]

T['pe_police'] = [
    ('report a crime', '/rɪˈpɔːt ə kraɪm/', 'PHR', 'jenaýat barada habar bermek', 'сообщить о преступлении', 'to tell the police about a crime', 'I want to report a crime.', 'Jenaýat barada habar bermek isleýärin.', 'A2'),
    ('break into', '/breɪk ˈɪntə/', 'PHR', 'ogrulyk bilen girmek', 'вломиться', 'to enter a place by force', 'Someone broke into my flat.', 'Biri öýüme ogrulyk bilen giripdir.', 'A2'),
    ('What was stolen?', '/wɒt wɒz ˈstəʊlən/', 'PHR', 'Näme ogurlandy?', 'Что было украдено?', 'used to ask what was taken', 'What was stolen from the house?', 'Öýden näme ogurlandy?', 'A2'),
    ('Did you see anyone?', '/dɪd ju siː ˈeniwʌn/', 'PHR', 'Birini gördüňizmi?', 'Вы кого-нибудь видели?', 'used to ask about witnesses', 'Did you see anyone near the door?', 'Gapynyň ýanynda birini gördüňizmi?', 'A2'),
    ('file a report', '/faɪl ə rɪˈpɔːt/', 'PHR', 'arz ýazmak', 'подать заявление', 'to make an official statement', 'You need to file a report.', 'Arz ýazmaly.', 'A2'),
    ('It happened last night.', '/ɪt ˈhæpnd lɑːst naɪt/', 'PHR', 'Düýn gije boldy.', 'Это случилось прошлой ночью.', 'used to say when it happened', 'It happened last night at ten.', 'Düýn gije sagat onda boldy.', 'A2'),
    ('case number', '/keɪs ˈnʌmbə(r)/', 'N', 'iş belgisi', 'номер дела', 'the code for your case', 'Note down the case number.', 'Iş belgisini ýazyp al.', 'A2'),
    ('contact the police', '/ˈkɒntækt ðə pəˈliːs/', 'PHR', 'polisiýa bilen habarlaşmak', 'связаться с полицией', 'to get in touch with police', 'Contact the police if you see him.', 'Ony görseň polisiýa bilen habarlaş.', 'A2'),
]

T['pe_house_rules'] = [
    ('house rules', '/ˈhaʊs ruːlz/', 'N', 'öý düzgünleri', 'правила дома', 'the rules in a home', 'Please follow the house rules.', 'Öý düzgünlerine eýeriň.', 'A2'),
    ('You have to...', '/ju hæv tuː/', 'PHR', 'Sen ... etmeli.', 'Ты должен...', 'used to say something is necessary', 'You have to take your shoes off.', 'Aýakgabyňy çykarmaly.', 'A1'),
    ('You are not allowed to...', '/ju ər nɒt əˈlaʊd tuː/', 'PHR', 'Saňa ... rugsat berilmeýär.', 'Тебе не разрешается...', 'used to say something is forbidden', 'You are not allowed to smoke here.', 'Bu ýerde çilim çekmäge rugsat berilmeýär.', 'A2'),
    ('take your shoes off', '/teɪk jɔː(r) ʃuːz ɒf/', 'PHR', 'aýakgabyňy çykar', 'сними обувь', 'used to ask someone to remove shoes', 'Please take your shoes off inside.', 'Içeride aýakgabyňy çykar.', 'A2'),
    ('keep it down', '/kiːp ɪt daʊn/', 'PHR', 'sesiňi peselt', 'потише, не шуми', 'used to ask for quiet', 'Keep it down, people are sleeping.', 'Sesiňi peselt, adamlar uklaýar.', 'A2'),
    ('no smoking', '/nəʊ ˈsməʊkɪŋ/', 'PHR', 'çilim çekmek gadagan', 'курение запрещено', 'used to forbid smoking', 'There is no smoking indoors.', 'Içeride çilim çekmek gadagan.', 'A2'),
    ('clean up after yourself', '/kliːn ʌp ˈɑːftə(r) jɔːˈself/', 'PHR', 'yzyňy ýygna', 'убери за собой', 'used to ask someone to tidy', 'Clean up after yourself in the kitchen.', 'Aşhanada yzyňy ýygna.', 'A2'),
    ('help yourself', '/help jɔːˈself/', 'PHR', 'özüň al (hoş geldiň)', 'угощайтесь', 'used to invite someone to take things', 'Help yourself to any food.', 'Islän naharyňy özüň al.', 'A2'),
]

T['pe_directions'] = [
    ('It is on the first floor.', '/ɪt ɪz ɒn ðə ˌfɜːst ˈflɔː(r)/', 'PHR', 'Birinji gatda.', 'Это на первом этаже.', 'used to say where something is', 'The office is on the first floor.', 'Edara birinji gatda.', 'A2'),
    ('take the lift', '/teɪk ðə lɪft/', 'PHR', 'liftde çyk', 'воспользуйтесь лифтом', 'used to tell someone to use the lift', 'Take the lift to the top floor.', 'Iň ýokarky gata liftde çyk.', 'A2'),
    ('turn left at the...', '/tɜːn left ət ðə/', 'PHR', '...-da çepe öwrül', 'поверните налево у...', 'used to give a direction', 'Turn left at the corner.', 'Burçda çepe öwrül.', 'A2'),
    ('go straight ahead', '/ɡəʊ streɪt əˈhed/', 'PHR', 'göni öňe git', 'идите прямо', 'used to say continue forward', 'Go straight ahead to the door.', 'Gapa çenli göni öňe git.', 'A2'),
    ('It is opposite the...', '/ɪt ɪz ˈɒpəzɪt ðə/', 'PHR', '...-yň garşysynda.', 'Это напротив...', 'used to say across from something', 'It is opposite the café.', 'Kafeniň garşysynda.', 'A2'),
    ('next to the...', '/nekst tuː ðə/', 'PHR', '...-yň ýanynda.', 'Рядом с...', 'used to say beside something', 'The bank is next to the shop.', 'Bank dükanyň ýanynda.', 'A1'),
    ('at the end of the corridor', '/ət ði end əv ðə ˈkɒrɪdɔː(r)/', 'PHR', 'koridoryň ahyrynda.', 'В конце коридора.', 'used to give a location', 'The toilets are at the end of the corridor.', 'Hajathanalar koridoryň ahyrynda.', 'A2'),
    ('you cannot miss it', '/ju ˈkænɒt mɪs ɪt/', 'PHR', 'sypdyrmarsyň.', 'вы не пропустите.', 'used to say it is easy to find', 'It has a big sign — you cannot miss it.', 'Uly belgisi bar — sypdyrmarsyň.', 'A2'),
]
LESSONS = {
    '1A': (1,  'Why did they call you that?', 'names', ['names']),
    '1B': (1,  'Life in colour', 'adjectives · adjective suffixes', ['adj_suffixes']),
    '2A': (2,  'Get ready! Get set! Go!', 'packing', ['packing']),
    '2B': (2,  'Go to checkout', 'shops and services', ['shops_services']),
    '3A': (3,  'Grow up!', 'stages of life', ['stages_life']),
    '3B': (3,  'Photo albums', 'photography', ['photography']),
    '4A': (4,  "Don't throw it away!", 'rubbish and recycling', ['recycling']),
    '4B': (4,  'Put it on your CV', 'study and work', ['study_work']),
    '5A': (5,  'Screen time', 'television', ['television']),
    '5B': (5,  'A quiet life?', 'the country', ['country']),
    '6A': (6,  'What the waiter really thinks', 'at a restaurant', ['restaurant']),
    '6B': (6,  'Do it yourself', 'DIY and repairs', ['diy']),
    '7A': (7,  'Take your cash', 'cash machines · phrasal verbs', ['money_phrasal']),
    '7B': (7,  'Shall we go out or stay in?', 'live entertainment', ['live_entertainment']),
    '8A': (8,  'Treat yourself', 'looking after yourself', ['looking_after']),
    '8B': (8,  'Sites and sights', 'wars and battles · historic buildings', ['historic']),
    '9A': (9,  'Total recall', 'word building', ['word_building3']),
    '9B': (9,  'Here comes the bride', 'weddings', ['weddings']),
    '10A': (10, 'The land of the free?', 'British and American English', ['brit_amer']),
    '10B': (10, 'Please turn over your papers', 'exams', ['exams']),
}

WORD_LESSON = {}


def lesson_for(topic, en, fallback):
    key = en.strip().lower()
    return WORD_LESSON.get(key, fallback)


# Intermediate Plus has ten units; the five Practical English episodes sit
# after units 1, 3, 5, 7 and 9 in the book. In the data they carry unit 11 so
# they do not collide with the real units, and the app shows each episode
# right after the unit it follows.
PE_UNIT = 11
for code, n, title, topic, key in (
    ('PE1', 11, 'Reporting lost luggage', 'practical English episode 1', 'pe_luggage'),
    ('PE2', 11, 'Renting a car', 'practical English episode 2', 'pe_rentcar'),
    ('PE3', 11, 'Making a police report', 'practical English episode 3', 'pe_police'),
    ('PE4', 11, 'Talking about house rules', 'practical English episode 4', 'pe_house_rules'),
    ('PE5', 11, 'Giving directions in a building', 'practical English episode 5', 'pe_directions'),
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
                    'books': [{'book': 'intp', 'unit': unit, 'lesson': lesson, 'page': PAGE.get(lesson)}],
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
        'book': 'intp',
        'title': 'English File Intermediate Plus (4th edition) — vocabulary, by lesson',
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
