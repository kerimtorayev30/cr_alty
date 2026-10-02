#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the general EN<->TM<->RU search dictionary seed for Yatla.

This is a SEARCH-ONLY dictionary: it broadens what the Search tab can find
beyond the 2,461 curated book words, without polluting the learning/review
pipeline (those keep using the book pack only). Each entry is compact:
  (english, turkmen, russian, part_of_speech)

Turkmen notes (validated after generation):
  - dotless 'i' (U+0131, Turkish) is WRONG in Turkmen -> use 'y'  ("acyk" -> "acık" is Turkish)
  - allowed special letters: ä  ö  ü  ý  ň  ş  ç  ž
  - no Cyrillic may leak into the Turkmen field
Russian is plain Cyrillic.

Machine-authored. 0 entries native-proofread. Owner to proofread before ship.
"""
import json, re, sys, unicodedata

# --- Turkmen sanity checks -------------------------------------------------
TM_ALLOWED = set("abcdefghijklmnopqrstuvwxyzäöüýňşçžABCDEFGHIJKLMNOPQRSTUVWXYZ' -")
BAD_TM = {"\u0131": "Turkish dotless i (use y)"}

def check_tm(w, tm):
    for ch in tm:
        if ch in BAD_TM:
            return "TM %r in %r has %s" % (ch, tm, BAD_TM[ch])
        if ch not in TM_ALLOWED:
            return "TM %r in %r not allowed" % (ch, tm)
    return None

def check_ru(w, ru):
    for ch in ru:
        o = ord(ch)
        if o < 128:
            continue
        # allow Cyrillic block + common punctuation
        if 0x0400 <= o <= 0x04FF:
            continue
        if ch in "ёЁ-’' ":
            continue
        return "RU %r in %r unexpected" % (ch, ru)
    return None

# --- data: (en, tm, ru, pos) ----------------------------------------------
# pos: N noun, V verb, ADJ adjective, ADV adverb, PREP, CONJ, PRON, NUM, INTJ
DATA = []
def add(*rows):
    for r in rows:
        DATA.append(r)

# numbers / quantities
add(
 ("one","bir","один","NUM"),("two","iki","два","NUM"),("three","üç","три","NUM"),
 ("four","dört","четыре","NUM"),("five","bäş","пять","NUM"),("six","alty","шесть","NUM"),
 ("seven","ýedi","семь","NUM"),("eight","sekiz","восемь","NUM"),("nine","dokuz","девять","NUM"),
 ("ten","on","десять","NUM"),("eleven","on bir","одиннадцать","NUM"),("twelve","on iki","двенадцать","NUM"),
 ("twenty","ýigrimi","двадцать","NUM"),("thirty","otuz","тридцать","NUM"),("forty","kyrk","сорок","NUM"),
 ("fifty","elli","пятьдесят","NUM"),("hundred","ýüz","сто","NUM"),("thousand","müň","тысяча","NUM"),
 ("million","million","миллион","NUM"),("zero","nol","ноль","NUM"),
 ("first","birinji","первый","ADJ"),("second","ikinji","второй","ADJ"),("third","üçünji","третий","ADJ"),
 ("half","ýarym","половина","N"),("quarter","çärýek","четверть","N"),("double","iki esse","двойной","ADJ"),
 ("many","köp","много","ADJ"),("few","az","мало","ADJ"),("much","köp","много","ADV"),
 ("some","birnäçe","несколько","ADJ"),("all","ähli","все","ADJ"),("none","hiç","ни один","PRON"),
 ("each","her","каждый","ADJ"),("every","her","каждый","ADJ"),("other","başga","другой","ADJ"),
 ("same","meňzeş","одинаковый","ADJ"),("enough","ýeterlik","достаточно","ADV"),
)

# time / calendar
add(
 ("day","gün","день","N"),("night","gije","ночь","N"),("morning","irden","утро","N"),
 ("evening","agşam","вечер","N"),("afternoon","günortan","день","N"),("today","şu gün","сегодня","ADV"),
 ("tomorrow","ertir","завтра","ADV"),("yesterday","düýn","вчера","ADV"),("now","häzir","сейчас","ADV"),
 ("week","hepde","неделя","N"),("month","aý","месяц","N"),("year","ýyl","год","N"),
 ("hour","sagat","час","N"),("minute","minut","минута","N"),("time","wagt","время","N"),
 ("always","elmydama","всегда","ADV"),("never","hiç haçan","никогда","ADV"),("often","köplenç","часто","ADV"),
 ("sometimes","käwagt","иногда","ADV"),("usually","adatça","обычно","ADV"),("again","ýene","снова","ADV"),
 ("early","ir","рано","ADV"),("late","giç","поздно","ADV"),("soon","tiz","скоро","ADV"),
 ("monday","duşenbe","понедельник","N"),("tuesday","sişenbe","вторник","N"),("wednesday","çarşenbe","среда","N"),
 ("thursday","penşenbe","четверг","N"),("friday","anna","пятница","N"),("saturday","şenbe","суббота","N"),
 ("sunday","ýekşenbe","воскресенье","N"),("weekend","hepde ahyry","выходные","N"),
 ("january","ýanwar","январь","N"),("february","fewral","февраль","N"),("march","mart","март","N"),
 ("april","aprel","апрель","N"),("may","maý","май","N"),("june","iýun","июнь","N"),
 ("july","iýul","июль","N"),("august","awgust","август","N"),("september","sentýabr","сентябрь","N"),
 ("october","oktýabr","октябрь","N"),("november","noýabr","ноябрь","N"),("december","dekabr","декабрь","N"),
 ("spring","ýaz","весна","N"),("summer","tomus","лето","N"),("autumn","güýz","осень","N"),("winter","gyş","зима","N"),
 ("birthday","doglan gün","день рождения","N"),("holiday","dynç alyş","праздник","N"),
)

# colors / appearance
add(
 ("color","reňk","цвет","N"),("red","gyzyl","красный","ADJ"),("blue","gök","синий","ADJ"),
 ("green","ýaşyl","зелёный","ADJ"),("yellow","sary","жёлтый","ADJ"),("black","gara","чёрный","ADJ"),
 ("white","ak","белый","ADJ"),("grey","çal","серый","ADJ"),("brown","goňur","коричневый","ADJ"),
 ("orange","mämişi","оранжевый","ADJ"),("pink","gül reňki","розовый","ADJ"),("purple","benewşe","фиолетовый","ADJ"),
 ("dark","garaňky","тёмный","ADJ"),("light","ýagty","светлый","ADJ"),("bright","ýagty","яркий","ADJ"),
 ("big","uly","большой","ADJ"),("small","kiçi","маленький","ADJ"),("large","uly","крупный","ADJ"),
 ("long","uzyn","длинный","ADJ"),("short","gysga","короткий","ADJ"),("tall","uzyn","высокий","ADJ"),
 ("wide","ini","широкий","ADJ"),("narrow","dar","узкий","ADJ"),("thick","ýogyn","толстый","ADJ"),
 ("thin","ýuka","тонкий","ADJ"),("heavy","agyr","тяжёлый","ADJ"),("deep","çuň","глубокий","ADJ"),
 ("shallow","taýaz","мелкий","ADJ"),("high","beýik","высокий","ADJ"),("low","pes","низкий","ADJ"),
 ("new","täze","новый","ADJ"),("old","köne","старый","ADJ"),("young","ýaş","молодой","ADJ"),
 ("clean","arassa","чистый","ADJ"),("dirty","hapalanan","грязный","ADJ"),("wet","ýaş","мокрый","ADJ"),
 ("dry","gury","сухой","ADJ"),("full","doly","полный","ADJ"),("empty","boş","пустой","ADJ"),
 ("closed","ýapyk","закрытый","ADJ"),("strong","güýçli","сильный","ADJ"),
 ("weak","gowşak","слабый","ADJ"),("fast","çalt","быстрый","ADJ"),("slow","haýal","медленный","ADJ"),
 ("easy","aňsat","лёгкий","ADJ"),("difficult","kyn","трудный","ADJ"),("cheap","arzan","дешёвый","ADJ"),
 ("expensive","gymmat","дорогой","ADJ"),("beautiful","owadan","красивый","ADJ"),("ugly","ýakymsyz","некрасивый","ADJ"),
 ("good","gowy","хороший","ADJ"),("bad","erbet","плохой","ADJ"),("happy","bagtly","счастливый","ADJ"),
 ("sad","gamgyn","грустный","ADJ"),("angry","gaharly","злой","ADJ"),("tired","ýadaw","усталый","ADJ"),
 ("hungry","aç","голодный","ADJ"),("thirsty","susuz","испытывающий жажду","ADJ"),("sick","kesel","больной","ADJ"),
 ("healthy","sagdyn","здоровый","ADJ"),("rich","baý","богатый","ADJ"),("poor","garyp","бедный","ADJ"),
 ("right","dogry","правильный","ADJ"),("wrong","ýalňyş","неправильный","ADJ"),("true","çyn","истинный","ADJ"),
 ("false","ýalňyş","ложный","ADJ"),("important","möhüm","важный","ADJ"),("interesting","gyzykly","интересный","ADJ"),
 ("boring","ýadawsyz","скучный","ADJ"),("funny","gülmeli","смешной","ADJ"),("kind","mähirli","добрый","ADJ"),
 ("kind person","mähirli adam","добрый человек","N"),("polite","edepli","вежливый","ADJ"),("busy","meşgul","занятой","ADJ"),
 ("free","boş","свободный","ADJ"),("ready","taýýar","готовый","ADJ"),("sure","ynamly","уверенный","ADJ"),
 ("possible","mümkin","возможный","ADJ"),("necessary","zerur","необходимый","ADJ"),("different","dürli","разный","ADJ"),
 ("special","aýratyn","особенный","ADJ"),("famous","meşhur","известный","ADJ"),("quiet","sessiz","тихий","ADJ"),
 ("loud","sesli","громкий","ADJ"),("warm","ýyly","тёплый","ADJ"),("cool","salkyn","прохладный","ADJ"),
 ("cold","sowuk","холодный","ADJ"),("hot","yssy","горячий","ADJ"),("sweet","süýji","сладкий","ADJ"),
 ("sour","turşy","кислый","ADJ"),("salty","duzly","солёный","ADJ"),("bitter","ajy","горький","ADJ"),
 ("fresh","täze","свежий","ADJ"),("delicious","tagamly","вкусный","ADJ"),("safe","howpsuz","безопасный","ADJ"),
 ("dangerous","howply","опасный","ADJ"),("cheap price","arzan baha","дешёвая цена","N"),
)

# family / people
add(
 ("person","adam","человек","N"),("people","adamlar","люди","N"),("man","adam","мужчина","N"),
 ("woman","aýal","женщина","N"),("boy","oglan","мальчик","N"),("girl","gyz","девочка","N"),
 ("child","çaga","ребёнок","N"),("children","çagalar","дети","N"),("baby","çaga","младенец","N"),
 ("family","maşgala","семья","N"),("father","kaka","отец","N"),("mother","eje","мать","N"),
 ("parents","ene-ata","родители","N"),("son","ogul","сын","N"),("daughter","gyz","дочь","N"),
 ("brother","dogan","брат","N"),("sister","uýa","сестра","N"),("grandfather","baba","дедушка","N"),
 ("grandmother","mama","бабушка","N"),("uncle","dayy","дядя","N"),("aunt","bibi","тётя","N"),
 ("cousin","ýegen","двоюродный брат","N"),("husband","äri","муж","N"),("wife","aýaly","жена","N"),
 ("friend","dost","друг","N"),("neighbor","goňşy","сосед","N"),("guest","myhman","гость","N"),
 ("teacher","mugallym","учитель","N"),("student","okuwçy","ученик","N"),("pupil","okuwçy","ученик","N"),
 ("doctor","lukman","врач","N"),("nurse","şepagat uýasy","медсестра","N"),("engineer","inžener","инженер","N"),
 ("driver","sürüji","водитель","N"),("worker","işçi","рабочий","N"),("farmer","daýhan","фермер","N"),
 ("chef","aşpez","повар","N"),("seller","satyjy","продавец","N"),("buyer","alyjy","покупатель","N"),
 ("police","polisiýa","полиция","N"),("soldier","esger","солдат","N"),("artist","suratkeş","художник","N"),
 ("singer","aýdymçy","певец","N"),("player","oýunçy","игрок","N"),("name","at","имя","N"),
 ("surname","familiýa","фамилия","N"),("age","ýaş","возраст","N"),("man friend","dost","приятель","N"),
 ("king","patyşa","король","N"),("queen","şaly aýal","королева","N"),("hero","gahryman","герой","N"),
 ("boss","başlyk","начальник","N"),("colleague","işdeş","коллега","N"),("stranger","tanymal däl","незнакомый человек","N"),
 ("twin","ekiz","близнец","N"),("husband and wife","är-aýal","супруги","N"),("grown-up","uly adam","взрослый","N"),
)

# body / health
add(
 ("body","beden","тело","N"),("head","kelle","голова","N"),("face","ýüz","лицо","N"),
 ("eye","göz","глаз","N"),("ear","gulak","ухо","N"),("nose","burun","нос","N"),
 ("mouth","agyz","рот","N"),("tooth","diş","зуб","N"),("teeth","dişler","зубы","N"),
 ("tongue","dil","язык","N"),("lip","dodak","губа","N"),("hair","saç","волосы","N"),
 ("neck","boýun","шея","N"),("shoulder","egyn","плечо","N"),("arm","gol","рука","N"),
 ("hand","el","кисть","N"),("finger","barmak","палец","N"),("leg","aýak","нога","N"),
 ("foot","aýak","ступня","N"),("feet","aýaklar","ступни","N"),("knee","diz","колено","N"),
 ("back","arka","спина","N"),("chest","döş","грудь","N"),("stomach","aşgazan","живот","N"),
 ("heart","ýürek","сердце","N"),("blood","gan","кровь","N"),("bone","süňk","кость","N"),
 ("skin","deri","кожа","N"),("brain","beýni","мозг","N"),("voice","ses","голос","N"),
 ("health","saglyk","здоровье","N"),("illness","kesel","болезнь","N"),("pain","agyry","боль","N"),
 ("headache","kelleagyry","головная боль","N"),("medicine","derman","лекарство","N"),("hospital","hassahana","больница","N"),
 ("fever","gyzzyrma","температура","N"),("cough","üsgülewük","кашель","N"),("wound","ýara","рана","N"),
 ("sleep","uky","сон","N"),("dream","düýş","мечта","N"),("rest","dynç","отдых","N"),
 ("strength","güýç","сила","N"),("breath","dem","дыхание","N"),("smile","ýylgyryş","улыбка","N"),
)

# food / drink
add(
 ("food","iýmit","еда","N"),("bread","çörek","хлеб","N"),("water","suw","вода","N"),
 ("milk","süýt","молоко","N"),("tea","çaý","чай","N"),("coffee","kofe","кофе","N"),
 ("meat","et","мясо","N"),("chicken","towuk","курица","N"),("fish","balyk","рыба","N"),
 ("egg","ýumurtga","яйцо","N"),("rice","tüwi","рис","N"),("soup","çorba","суп","N"),
 ("salad","salat","салат","N"),("cheese","peýnir","сыр","N"),("butter","ýag","масло","N"),
 ("oil","ýag","масло","N"),("sugar","şeker","сахар","N"),("salt","duz","соль","N"),
 ("pepper","burç","перец","N"),("fruit","miwe","фрукт","N"),("vegetable","gök önüm","овощ","N"),
 ("apple","alma","яблоко","N"),("banana","banan","банан","N"),("grape","üzüm","виноград","N"),
 ("melon","gawun","дыня","N"),("watermelon","garpyz","арбуз","N"),("pomegranate","nar","гранат","N"),
 ("tomato","pomidor","помидор","N"),("potato","ýeralma","картофель","N"),("onion","sogan","лук","N"),
 ("carrot","käşir","морковь","N"),("cucumber","hyýar","огурец","N"),("garlic","sarymsak","чеснок","N"),
 ("juice","şire","сок","N"),("ice cream","dondurma","мороженое","N"),("cake","tort","торт","N"),
 ("candy","konfet","конфета","N"),("honey","bal","мёд","N"),("breakfast","ertirlik","завтрак","N"),
 ("lunch","günortanlyk","обед","N"),("dinner","agşamlyk","ужин","N"),("meal","nahar","еда","N"),
 ("plate","tarelka","тарелка","N"),("cup","käse","чашка","N"),("glass","stakan","стакан","N"),
 ("bottle","çüýşe","бутылка","N"),("fork","çarşak","вилка","N"),("spoon","çemçe","ложка","N"),
 ("knife","pyçak","нож","N"),("table","stol","стол","N"),("breakfast food","ertirlik","завтрак","N"),
 ("meal time","nahar wagty","время еды","N"),("tasty food","tagamly nahar","вкусная еда","N"),
)

# animals / nature
add(
 ("animal","haýwan","животное","N"),("dog","it","собака","N"),("cat","pişik","кошка","N"),
 ("horse","at","лошадь","N"),("cow","sygyr","корова","N"),("sheep","goýun","овца","N"),
 ("goat","geçi","коза","N"),("camel","düýe","верблюд","N"),("bird","guş","птица","N"),
 ("chicken bird","towuk","курица","N"),("duck","ördek","утка","N"),("wolf","möjek","волк","N"),
 ("fox","tilki","лиса","N"),("bear","aýy","медведь","N"),("lion","ýolbars","лев","N"),
 ("elephant","pil","слон","N"),("mouse","syçan","мышь","N"),("rabbit","towşan","кролик","N"),
 ("snake","ýylan","змея","N"),("insect","mör-möjek","насекомое","N"),("bee","ary","пчела","N"),
 ("housefly","siňek","муха","N"),("fish animal","balyk","рыба","N"),("nature","tebigat","природа","N"),
 ("tree","agaç","дерево","N"),("flower","gül","цветок","N"),("grass","ot","трава","N"),
 ("leaf","ýaprak","лист","N"),("root","kök","корень","N"),("branch","şaha","ветка","N"),
 ("forest","toqaý","лес","N"),("garden","bag","сад","N"),("field","meýdan","поле","N"),
 ("mountain","dag","гора","N"),("hill","depe","холм","N"),("river","derýa","река","N"),
 ("lake","köl","озеро","N"),("sea","deňiz","море","N"),("sky","asman","небо","N"),
 ("sun","gün","солнце","N"),("moon","aý","луна","N"),("star","ýyldyz","звезда","N"),
 ("cloud","bulut","облако","N"),("rain","ýagyş","дождь","N"),("snow","gar","снег","N"),
 ("wind","ýel","ветер","N"),("storm","tupan","шторм","N"),("weather","howa","погода","N"),
 ("air","howa","воздух","N"),("fire","ot","огонь","N"),("stone","daş","камень","N"),
 ("sand","çäge","песок","N"),("earth","ýer","земля","N"),("world","dünýä","мир","N"),
 ("desert","çöl","пустыня","N"),("island","ada","остров","N"),("valley","jülge","долина","N"),
 ("flower garden","gül bagy","цветник","N"),("green field","ýaşyl meýdan","зелёное поле","N"),
)

# home / objects / clothing
add(
 ("house","öý","дом","N"),("home","öý","дом","N"),("room","otag","комната","N"),
 ("door","gapy","дверь","N"),("window","aýna","окно","N"),("wall","diwar","стена","N"),
 ("floor","pol","пол","N"),("roof","üçek","крыша","N"),("kitchen","aşhana","кухня","N"),
 ("bedroom","ýatylýan otag","спальня","N"),("bathroom","ýuwunýan otag","ванная","N"),("bed","düşek","кровать","N"),
 ("chair","oturgyç","стул","N"),("sofa","diwan","диван","N"),("carpet","haly","ковёр","N"),
 ("mirror","aýna","зеркало","N"),("lamp","çyra","лампа","N"),("key","açar","ключ","N"),
 ("clock","sagat","часы","N"),("book","kitap","книга","N"),("pen","galam","ручка","N"),
 ("pencil","galam","карандаш","N"),("paper","kagyz","бумага","N"),("bag","torba","сумка","N"),
 ("phone","telefon","телефон","N"),("computer","kompýuter","компьютер","N"),("television","telewizor","телевизор","N"),
 ("car","maşyn","машина","N"),("bicycle","welosiped","велосипед","N"),("clothes","eşik","одежда","N"),
 ("shirt","köýnek","рубашка","N"),("dress","don","платье","N"),("trousers","balak","брюки","N"),
 ("shoes","köwüş","ботинки","N"),("hat","telpek","шапка","N"),("coat","palto","пальто","N"),
 ("sock","jorap","носок","N"),("glasses","äýnek","очки","N"),("watch","sagat","наручные часы","N"),
 ("ring","ýüzük","кольцо","N"),("money","pul","деньги","N"),("box","guty","коробка","N"),
 ("basket","sebet","корзина","N"),("rope","ýüp","верёвка","N"),("thread","sapak","нитка","N"),
 ("needle","iňňe","игла","N"),("scissors","gaýçy","ножницы","N"),("umbrella","saýawan","зонт","N"),
 ("toy","oýunjak","игрушка","N"),("ball","pökgi","мяч","N"),("picture","surat","картина","N"),
 ("photo","surat","фотография","N"),("letter","hat","письмо","N"),("newspaper","gazet","газета","N"),
 ("magazine","žurnal","журнал","N"),("song","aýdym","песня","N"),("music","saz","музыка","N"),
 ("game","oýun","игра","N"),("gift","sowgat","подарок","N"),("flower bouquet","gül desse","букет","N"),
)

# city / places / transport
add(
 ("city","şäher","город","N"),("town","şäherçe","городок","N"),("village","oba","деревня","N"),
 ("street","köçe","улица","N"),("road","ýol","дорога","N"),("bridge","köpri","мост","N"),
 ("square","meýdança","площадь","N"),("park","park","парк","N"),("shop","dükan","магазин","N"),
 ("market","bazar","рынок","N"),("school","mekdep","школа","N"),("university","uniwersitet","университет","N"),
 ("library","kitaphana","библиотека","N"),("museum","muzeý","музей","N"),("theatre","teatr","театр","N"),
 ("cinema","kinoteatr","кинотеатр","N"),("bank","bank","банк","N"),("post office","poçta","почта","N"),
 ("restaurant","restoran","ресторан","N"),("cafe","kafe","кафе","N"),("hotel","myhmanhana","отель","N"),
 ("station","beket","станция","N"),("airport","howa menzili","аэропорт","N"),("bus","awtobus","автобус","N"),
 ("train","otly","поезд","N"),("plane","uçar","самолёт","N"),("taxi","taksi","такси","N"),
 ("ship","gämi","корабль","N"),("boat","gaýyk","лодка","N"),("ticket","bilet","билет","N"),
 ("map","karta","карта","N"),("address","salgy","адрес","N"),("country","ýurt","страна","N"),
 ("capital","paýtagt","столица","N"),("border","serhet","граница","N"),("factory","zawod","завод","N"),
 ("office","edara","офис","N"),("company","kompaniýa","компания","N"),("government","hökümet","правительство","N"),
 ("mosque","metjit","мечеть","N"),("church","kilise","церковь","N"),("stadium","stadion","стадион","N"),
 ("pool","howuz","бассейн","N"),("pharmacy","dermanhana","аптека","N"),("bus stop","awtobus duralgasy","автобусная остановка","N"),
 ("train station","otly bekedi","вокзал","N"),("city centre","şäher merkezi","центр города","N"),
)

# work / school / abstract
add(
 ("work","iş","работа","N"),("job","iş","работа","N"),("business","iş","дело","N"),
 ("meeting","duşuşyk","встреча","N"),("project","taslama","проект","N"),("plan","meýilnama","план","N"),
 ("idea","pikir","идея","N"),("question","soruag","вопрос","N"),("answer","jogap","ответ","N"),
 ("problem","mesele","проблема","N"),("solution","çözgüt","решение","N"),("reason","sebäp","причина","N"),
 ("result","netije","результат","N"),("example","mysal","пример","N"),("rule","kada","правило","N"),
 ("law","kanun","закон","N"),("rights","hukuklar","права","N"),("duty","borç","обязанность","N"),
 ("help","kömek","помощь","N"),("advice","maslahat","совет","N"),("news","habar","новость","N"),
 ("story","hekaýa","история","N"),("history","taryh","история","N"),("science","ylym","наука","N"),
 ("math","matematika","математика","N"),("language","dil","язык","N"),("word","söz","слово","N"),
 ("sentence","sözlem","предложение","N"),("text","tekst","текст","N"),("page","sahypa","страница","N"),
 ("lesson","sapak","урок","N"),("class","synp","класс","N"),("exam","synag","экзамен","N"),
 ("homework","öý işi","домашнее задание","N"),("mistake","ýalňyşlyk","ошибка","N"),("truth","hakykat","правда","N"),
 ("lie","ýalan","ложь","N"),("hope","umyt","надежда","N"),("dream goal","arzuw","мечта","N"),
 ("fear","gorky","страх","N"),("love","söýgi","любовь","N"),("hate","ýigrenç","ненависть","N"),
 ("joy","şatlyk","радость","N"),("peace","parahatçylyk","мир","N"),("war","uruş","война","N"),
 ("life","durmuş","жизнь","N"),("death","ölüm","смерть","N"),("luck","bagt","удача","N"),
 ("chance","mümkinçilik","шанс","N"),("power","güýç","власть","N"),("freedom","azatlyk","свобода","N"),
 ("culture","medeniýet","культура","N"),("tradition","däp","традиция","N"),("custom","adat","обычай","N"),
 ("art","sungat","искусство","N"),("sport","sport","спорт","N"),("football","futbol","футбол","N"),
 ("team","topar","команда","N"),("victory","ýeňiş","победа","N"),("prize","baýrak","приз","N"),
 ("beginning","başlangyç","начало","N"),("end","soň","конец","N"),("part","bölek","часть","N"),
 ("whole","bitewi","целое","N"),("group","topar","группа","N"),("number","san","число","N"),
 ("price","baha","цена","N"),("cost","bahasy","стоимость","N"),("quality","hil","качество","N"),
 ("quantity","mukdar","количество","N"),("way","ýol","путь","N"),("place","ýer","место","N"),
 ("thing","zat","вещь","N"),("sort","görnüş","сорт","N"),("type","görnüş","тип","N"),
 ("form","forma","форма","N"),("size","ölçeg","размер","N"),("space","giňişlik","пространство","N"),
 ("distance","aralyk","расстояние","N"),("speed","tizlik","скорость","N"),("temperature","temperatura","температура","N"),
)

# verbs
add(
 ("be","bolmak","быть","V"),("have","bolmak","иметь","V"),("do","etmek","делать","V"),
 ("make","ýasamak","делать","V"),("go","gitmek","идти","V"),("come","gelmek","приходить","V"),
 ("see","görmek","видеть","V"),("look","seretmek","смотреть","V"),("hear","eşitmek","слышать","V"),
 ("listen","diňlemek","слушать","V"),("speak","gürlemek","говорить","V"),("say","aýtmak","сказать","V"),
 ("tell","gürrüň bermek","рассказывать","V"),("ask","soramak","спрашивать","V"),("answer verb","jogap bermek","отвечать","V"),
 ("read","okamak","читать","V"),("write","ýazmak","писать","V"),("learn","öwrenmek","учиться","V"),
 ("teach","öwretmek","учить","V"),("study","okamak","изучать","V"),("know","bilmek","знать","V"),
 ("think","pikir etmek","думать","V"),("understand","düşünmek","понимать","V"),("remember","ýatda saklamak","помнить","V"),
 ("forget","ýatdan çykarmak","забывать","V"),("believe","ynanmak","верить","V"),("want","islemek","хотеть","V"),
 ("need","zerur bolmak","нуждаться","V"),("like","halamak","нравиться","V"),("love verb","söýmek","любить","V"),
 ("hate verb","ýigrenmek","ненавидеть","V"),("eat","iýmek","есть","V"),("drink","içmek","пить","V"),
 ("cook","bişirmek","готовить","V"),("buy","satyn almak","покупать","V"),("sell","satmak","продавать","V"),
 ("pay","tölemek","платить","V"),("give","bermek","давать","V"),("take","almak","брать","V"),
 ("get","almak","получать","V"),("put","goýmak","класть","V"),("hold","saklamak","держать","V"),
 ("carry","götermek","нести","V"),("bring","getirmek","приносить","V"),("send","ibermek","отправлять","V"),
 ("receive","almak","получать","V"),("open","açmak","открывать","V"),("close","ýapmak","закрывать","V"),
 ("start","başlamak","начинать","V"),("stop","durmak","останавливаться","V"),("finish","gutarmak","заканчивать","V"),
 ("continue","dowam etmek","продолжать","V"),("wait","garaşmak","ждать","V"),("help verb","kömek etmek","помогать","V"),
 ("use","ulanmak","использовать","V"),("try","synanyşmak","пытаться","V"),("work verb","işlemek","работать","V"),
 ("play","oýnamak","играть","V"),("sing","aýtmak","петь","V"),("dance","tans etmek","танцевать","V"),
 ("run","ylgamak","бежать","V"),("walk","ýöremek","гулять","V"),("sit","oturmak","сидеть","V"),
 ("stand","durmak","стоять","V"),("sleep verb","ýatmak","спать","V"),("wake","turmak","просыпаться","V"),
 ("live","ýaşamak","жить","V"),("die","ölmek","умирать","V"),("born","dogulmak","рождаться","V"),
 ("grow","ösmek","расти","V"),("build","gurmak","строить","V"),("break","döwmek","ломать","V"),
 ("fix","bejermek","чинить","V"),("clean verb","arassalamak","чистить","V"),("wash","ýuwmak","мыть","V"),
 ("wear","geýmek","носить","V"),("drive","sürmek","водить","V"),("ride","atlanmak","ехать верхом","V"),
 ("fly","uçmak","летать","V"),("swim","ýüzmek","плавать","V"),("win","ýeňmek","победить","V"),
 ("lose","ýitirmek","терять","V"),("find","tapmak","находить","V"),("choose","saýlamak","выбирать","V"),
 ("change","üýtgetmek","менять","V"),("turn","öwürmek","поворачивать","V"),("move","hereket etmek","двигаться","V"),
 ("stay","galmak","оставаться","V"),("leave","gitmek","уходить","V"),("return","gaýtmak","возвращаться","V"),
 ("meet","duşuşmak","встречать","V"),("visit","baryp görmek","посещать","V"),("travel","syýahat etmek","путешествовать","V"),
 ("call","jaň etmek","звонить","V"),("show","görkezmek","показывать","V"),("explain","düşündirmek","объяснять","V"),
 ("agree","razylaşmak","соглашаться","V"),("refuse","ýüz öwürmek","отказываться","V"),("decide","karar bermek","решать","V"),
 ("hope verb","umyt etmek","надеяться","V"),("feel","duýmak","чувствовать","V"),("seem","meňzemek","казаться","V"),
 ("become","bolmak","становиться","V"),("happen","bolup geçmek","случаться","V"),("seem appear","görünmek","появляться","V"),
 ("count","sanamak","считать","V"),("measure","ölçemek","измерять","V"),("add","goşmak","добавлять","V"),
 ("divide","bölmek","делить","V"),("share","paýlaşmak","делиться","V"),("save","tygşytlamak","экономить","V"),
 ("spend","sarp etmek","тратить","V"),("cost verb","durmak","стоить","V"),("borrow","karz almak","занимать","V"),
 ("lend","karz bermek","давать взаймы","V"),("laugh","gülmek","смеяться","V"),("cry","aglamak","плакать","V"),
 ("smile verb","ýylgyrmak","улыбаться","V"),("shout","gygyrmak","кричать","V"),("rest verb","dynç almak","отдыхать","V"),
)

# prepositions / conjunctions / pronouns / misc
add(
 ("in","içinde","в","PREP"),("on","üstünde","на","PREP"),("under","astynda","под","PREP"),
 ("next to","ýanynda","рядом с","PREP"),("between","arasynda","между","PREP"),("before","öň","перед","PREP"),
 ("after","soň","после","PREP"),("with","bilen","с","PREP"),("without","bolmazdan","без","PREP"),
 ("for","üçin","для","PREP"),("about","barada","о","PREP"),("from","-dan","из","PREP"),
 ("to","-a","к","PREP"),("at","-de","у","PREP"),("and","we","и","CONJ"),
 ("but","ýöne","но","CONJ"),("or","ýa-da","или","CONJ"),("because","sebäbi","потому что","CONJ"),
 ("if","eger","если","CONJ"),("when","haçan","когда","CONJ"),("while","wagty","в то время как","CONJ"),
 ("so","şonuň üçin","поэтому","CONJ"),("also","hem","также","ADV"),("very","örän","очень","ADV"),
 ("too","hem","тоже","ADV"),("only","diňe","только","ADV"),("just","diňe","просто","ADV"),
 ("really","hakykatdan","действительно","ADV"),("maybe","belki","может быть","ADV"),("yes","hawa","да","ADV"),
 ("no","ýok","нет","ADV"),("not","däl","не","ADV"),("here","şu ýerde","здесь","ADV"),
 ("there","şol ýerde","там","ADV"),("where","nirede","где","ADV"),("why","näme üçin","почему","ADV"),
 ("how","nädip","как","ADV"),("what","näme","что","PRON"),("who","kim","кто","PRON"),
 ("which","haýsy","который","PRON"),("this","şu","этот","PRON"),("that","şol","тот","PRON"),
 ("these","şular","эти","PRON"),("those","şolar","те","PRON"),("I","men","я","PRON"),
 ("you","sen","ты","PRON"),("he","ol","он","PRON"),("she","ol","она","PRON"),
 ("it","ol","оно","PRON"),("we","biz","мы","PRON"),("they","olar","они","PRON"),
 ("my","meniň","мой","PRON"),("your","seniň","твой","PRON"),("his","onuň","его","PRON"),
 ("our","biziň","наш","PRON"),("their","olaryň","их","PRON"),("myself","özüm","себя","PRON"),
 ("please","haýyş","пожалуйста","INTJ"),("thanks","sag bol","спасибо","INTJ"),("sorry","bagyşlaň","извините","INTJ"),
 ("hello word","salam","привет","INTJ"),("goodbye","hoş","до свидания","INTJ"),("welcome","hoş geldiňiz","добро пожаловать","INTJ"),
 ("congratulations","gutlaýarys","поздравляем","INTJ"),("well done","berekella","молодец","INTJ"),
)

# ---- batch 2: next tier of high-frequency vocabulary -----------------------
add(
 # verbs
 ("arrive","gelip ýetmek","приезжать","V"),("appear","peýda bolmak","появляться","V"),
 ("begin","başlamak","начинать","V"),("belong","degişli bolmak","принадлежать","V"),
 ("catch","tutmak","ловить","V"),("cause","sebäp bolmak","причинять","V"),
 ("celebrate","baýram etmek","праздновать","V"),("collect","ýygnamak","собирать","V"),
 ("compare","deňeşdirmek","сравнивать","V"),("complete","tamamlamak","завершать","V"),
 ("contain","öz içine almak","содержать","V"),("control","gözegçilik etmek","контролировать","V"),
 ("copy","göçürmek","копировать","V"),("cover","örtmek","накрывать","V"),
 ("create","döretmek","создавать","V"),("cross","garşy geçmek","пересекать","V"),
 ("cut","kesmek","резать","V"),("damage","zyýan ýetirmek","повреждать","V"),
 ("deliver","eltip bermek","доставлять","V"),("describe","suratlandyrmak","описывать","V"),
 ("design","taslamak","проектировать","V"),("destroy","ýok etmek","разрушать","V"),
 ("develop","ösdürmek","развивать","V"),("disappear","ýitip gitmek","исчезать","V"),
 ("discuss","ara alyp maslahatlaşmak","обсуждать","V"),("doubt","şübhe etmek","сомневаться","V"),
 ("draw","surat çekmek","рисовать","V"),
 ("drop","gaçyrmak","ронять","V"),("earn","gazanmak","зарабатывать","V"),
 ("enter","girmek","входить","V"),("escape","gaçmak","убегать","V"),
 ("exist","bolmak","существовать","V"),("expect","garaşmak","ожидать","V"),
 ("fall","gaçmak","падать","V"),("feed","iýmitlendirmek","кормить","V"),
 ("fill","doldurmak","наполнять","V"),("fit","ýaraşmak","подходить","V"),
 ("follow","yzyna eýermek","следовать","V"),("gather","ýygnanmak","собираться","V"),
 ("guess","çaklamak","угадывать","V"),("hide","gizlemek","прятать","V"),
 ("hit","urmak","бить","V"),("hunt","awlamak","охотиться","V"),
 ("hurry","howlukmak","торопиться","V"),("imagine","göz öňüne getirmek","представлять","V"),
 ("improve","gowulandyrmak","улучшать","V"),("include","öz içine almak","включать","V"),
 ("increase","köpeltmek","увеличивать","V"),("inform","habar bermek","сообщать","V"),
 ("invite","çagyrmak","приглашать","V"),("join","goşulmak","присоединяться","V"),
 ("jump","bökmek","прыгать","V"),("kick","tepmek","пинать","V"),
 ("kill","öldürmek","убивать","V"),("kiss","ogşamak","целовать","V"),
 ("knock","kakmak","стучать","V"),("lead","ýolbaşçylyk etmek","вести","V"),
 ("let","goýbermek","позволять","V"),("lift","galdyrmak","поднимать","V"),
 ("manage","dolandyrmak","управлять","V"),("marry","öýlenmek","жениться","V"),
 ("match","deň gelmek","соответствовать","V"),("mean","aňlatmak","означать","V"),
 ("mention","bellik etmek","упоминать","V"),("miss","sagynmak","скучать","V"),
 ("mix","garyşdyrmak","смешивать","V"),("notice","üns bermek","замечать","V"),
 ("obey","boýun bolmak","подчиняться","V"),("offer","hödürlemek","предлагать","V"),
 ("organize","guramak","организовывать","V"),("own","eýe bolmak","владеть","V"),
 ("paint","boýamak","красить","V"),
 ("pass","geçmek","проходить","V"),("pick","saýlap almak","выбирать","V"),
 ("point","barmak bilen görkezmek","указывать","V"),
 ("pour","guýmak","лить","V"),("practice","türgenleşmek","практиковаться","V"),
 ("praise","makullamak","хвалить","V"),("pray","doga etmek","молиться","V"),
 ("prefer","ileri tutmak","предпочитать","V"),("prepare","taýýarlamak","готовить","V"),
 ("press","basmak","нажимать","V"),("prevent","öňüni almak","предотвращать","V"),
 ("print","çap etmek","печатать","V"),("produce","öndürmek","производить","V"),
 ("promise","wada bermek","обещать","V"),("protect","goramak","защищать","V"),
 ("prove","subut etmek","доказывать","V"),("provide","üpjün etmek","предоставлять","V"),
 ("pull","çekmek","тянуть","V"),("punish","jazalandyrmak","наказывать","V"),
 ("push","itmek","толкать","V"),("reach","ýetmek","достигать","V"),
 ("recognize","tanamak","узнавать","V"),("recommend","maslahat bermek","рекомендовать","V"),
 ("record","ýazga geçirmek","записывать","V"),("reduce","azaltmak","уменьшать","V"),
 ("regret","ökünmek","сожалеть","V"),("relax","dynç almak","расслабляться","V"),
 ("remind","ýada salmak","напоминать","V"),("repeat","gaýtalamak","повторять","V"),
 ("replace","çalşyrmak","заменять","V"),("reply","jogap bermek","отвечать","V"),
 ("request","haýyş etmek","просить","V"),("respect","hormatlamak","уважать","V"),
 ("reveal","ýüze çykarmak","раскрывать","V"),("rise","galmak","подниматься","V"),
 ("rob","talamak","грабить","V"),("roll","togalamak","катить","V"),
 ("rub","sürtmek","тереть","V"),("rush","howlukmak","торопиться","V"),
 ("scare","gorkuzmak","пугать","V"),("search","gözlemek","искать","V"),
 ("serve","hyzmat etmek","служить","V"),("shine","ýaldyramak","сиять","V"),
 ("shoot","atmak","стрелять","V"),
 ("smell","yys almak","нюхать","V"),("solve","çözmek","решать","V"),
 ("sound","ýaňlanmak","звучать","V"),("steal","ogurlamak","красть","V"),
 ("succeed","üstünlik gazanmak","преуспевать","V"),("support","goldamak","поддерживать","V"),
 ("surprise","haýran galdyrmak","удивлять","V"),("survive","diri galmak","выживать","V"),
 ("talk","gürleşmek","разговаривать","V"),("taste","tagamyna bakmak","пробовать","V"),
 ("test","barlamak","проверять","V"),("thank","sag bolsun aýtmak","благодарить","V"),
 ("throw","zyňmak","бросать","V"),("tie","baglamak","завязывать","V"),
 ("touch","ellemek","трогать","V"),
 ("translate","terjime etmek","переводить","V"),("treat","bejermek","лечить","V"),
 ("trust","ynanmak","доверять","V"),("warn","duýduryş bermek","предупреждать","V"),
 ("waste","isrip etmek","тратить впустую","V"),
 ("weigh","tartmak","взвешивать","V"),("wish","arzuw etmek","желать","V"),
 ("wonder","haýran galmak","удивляться","V"),("worry","alada etmek","беспокоиться","V"),
 ("wrap","ýapmak","оборачивать","V"),
 # adjectives
 ("able","başarýan","способный","ADJ"),("afraid","gorkan","испуганный","ADJ"),
 ("alone","ýalňyz","одинокий","ADJ"),("amazing","haýran galdyryjy","удивительный","ADJ"),
 ("angry person","gaharly","сердитый","ADJ"),("available","elýeterli","доступный","ADJ"),
 ("awful","elhenç","ужасный","ADJ"),("basic","esasy","основной","ADJ"),
 ("better","gowy","лучший","ADJ"),("bitter taste","ajy","горький","ADJ"),
 ("blank","boş","пустой","ADJ"),("brave","gaýratly","храбрый","ADJ"),
 ("busy person","meşgul","занятой","ADJ"),("calm","asuda","спокойный","ADJ"),
 ("careful","ünsli","осторожный","ADJ"),("certain","ynamly","уверенный","ADJ"),
 ("clear","aýdyň","ясный","ADJ"),("clever","akylly","умный","ADJ"),
 ("common","adaty","обычный","ADJ"),("complex","çylşyrymly","сложный","ADJ"),
 ("confident","ynamly","уверенный в себе","ADJ"),("cool weather","salkyn","прохладный","ADJ"),
 ("correct","dogry","верный","ADJ"),("crazy","däli","сумасшедший","ADJ"),
 ("cute","süýji","милый","ADJ"),("dear","gymmat","дорогой","ADJ"),
 ("delighted","şat","восхищённый","ADJ"),("direct","göni","прямой","ADJ"),
 ("dry weather","gury","сухой","ADJ"),("eager","höwesli","желающий","ADJ"),
 ("empty space","boş","пустой","ADJ"),("equal","deň","равный","ADJ"),
 ("exact","takyk","точный","ADJ"),("excellent","ajaýyp","отличный","ADJ"),
 ("excited","tolgunan","взволнованный","ADJ"),("extra","goşmaça","дополнительный","ADJ"),
 ("fair","adyl","справедливый","ADJ"),("far","daş","далёкий","ADJ"),
 ("favourite","söýgüli","любимый","ADJ"),("final","soňky","окончательный","ADJ"),
 ("fine","gowy","хороший","ADJ"),("firm","berk","твёрдый","ADJ"),
 ("flat","tekiz","плоский","ADJ"),("foreign","daşary ýurt","иностранный","ADJ"),
 ("formal","resmi","официальный","ADJ"),("forward","öňe","вперёд","ADJ"),
 ("friendly","dostlukly","дружелюбный","ADJ"),("frightened","gorkan","испуганный","ADJ"),
 ("general","umumy","общий","ADJ"),("gentle","ýumşak","нежный","ADJ"),
 ("glad","şat","рад","ADJ"),("golden","altyndan","золотой","ADJ"),
 ("grateful","minnetdar","благодарный","ADJ"),("guilty","günäkär","виноватый","ADJ"),
 ("handsome","ýakymly","красивый","ADJ"),("hard","gaty","твёрдый","ADJ"),
 ("helpful","peýdaly","полезный","ADJ"),("honest","dogruçyl","честный","ADJ"),
 ("horrible","elhenç","ужасный","ADJ"),("huge","ägirt","огромный","ADJ"),
 ("ill","kesel","больной","ADJ"),("innocent","günäsiz","невинный","ADJ"),
 ("keen","höwesli","увлечённый","ADJ"),("lazy","ýalta","ленивый","ADJ"),
 ("left","çep","левый","ADJ"),("legal","kanuny","законный","ADJ"),
 ("likely","ähtimal","вероятный","ADJ"),("little","kiçi","маленький","ADJ"),
 ("lively","janly","оживлённый","ADJ"),("lonely","ýalňyz","одинокий","ADJ"),
 ("lovely","owadan","прекрасный","ADJ"),("lucky","bagtly","везучий","ADJ"),
 ("main","esasy","главный","ADJ"),("major","esasy","основной","ADJ"),
 ("mean person","gysganç","скупой","ADJ"),("medical","lukmançylyk","медицинский","ADJ"),
 ("merry","şadyýan","весёлый","ADJ"),("modern","häzirki zaman","современный","ADJ"),
 ("moist","çygly","влажный","ADJ"),("narrow road","dar","узкий","ADJ"),
 ("national","milli","национальный","ADJ"),("natural","tebigy","естественный","ADJ"),
 ("naughty","ýaramaz","озорной","ADJ"),("near","ýakyn","близкий","ADJ"),
 ("neat","sypyrylan","опрятный","ADJ"),("negative","negatiw","отрицательный","ADJ"),
 ("nervous","aladaly","нервный","ADJ"),("nice","gowy","приятный","ADJ"),
 ("normal","kadaly","нормальный","ADJ"),("odd","geň","странный","ADJ"),
 ("official","resmi","служебный","ADJ"),("opposite","garşylykly","противоположный","ADJ"),
 ("ordinary","adaty","обыкновенный","ADJ"),("original","asl","первоначальный","ADJ"),
 ("outer","daşky","внешний","ADJ"),("own person","öz","собственный","ADJ"),
 ("particular","aýratyn","особый","ADJ"),("patient","sabyrly","терпеливый","ADJ"),
 ("perfect","kämil","идеальный","ADJ"),("personal","şahsy","личный","ADJ"),
 ("physical","fiziki","физический","ADJ"),("pleasant","ýakymly","приятный","ADJ"),
 ("pleased","şat","довольный","ADJ"),("plenty","köp","множество","ADJ"),
 ("polite person","edepli","вежливый","ADJ"),("popular","meşhur","популярный","ADJ"),
 ("positive","pozitiw","положительный","ADJ"),("possible thing","mümkin","возможный","ADJ"),
 ("powerful","güýçli","мощный","ADJ"),("practical","amaly","практический","ADJ"),
 ("pregnant","göwreli","беременная","ADJ"),("present","häzirki","настоящий","ADJ"),
 ("pretty","owadan","хорошенький","ADJ"),("private","şahsy","частный","ADJ"),
 ("probable","ähtimal","вероятный","ADJ"),("proper","dogry","подходящий","ADJ"),
 ("proud","buýsançly","гордый","ADJ"),("public","jemi","общественный","ADJ"),
 ("pure","arassa","чистый","ADJ"),("quick","çalt","быстрый","ADJ"),
 ("raw","çig","сырой","ADJ"),("real","hakyky","настоящий","ADJ"),
 ("recent","soňky","недавний","ADJ"),("regular","kadaly","регулярный","ADJ"),
 ("related","baglanyşykly","связанный","ADJ"),("responsible","jogapkär","ответственный","ADJ"),
 ("round","tegelek","круглый","ADJ"),("rude","gaba","грубый","ADJ"),
 ("sad person","gamgyn","печальный","ADJ"),("scared","gorkan","напуганный","ADJ"),
 ("secret","gizlin","тайный","ADJ"),("secure","howpsuz","надёжный","ADJ"),
 ("serious","çynlakaý","серьёзный","ADJ"),("several","birnäçe","несколько","ADJ"),
 ("sharp","iti","острый","ADJ"),("shy","utanaçak","застенчивый","ADJ"),
 ("silly","akylsyz","глупый","ADJ"),("simple","ýönekeý","простой","ADJ"),
 ("sincere","çyn ýürekden","искренний","ADJ"),("single","ýeke","одиночный","ADJ"),
 ("slight","ýeňil","небольшой","ADJ"),("smart","akylly","сообразительный","ADJ"),
 ("smooth","tekiz","гладкий","ADJ"),("soft","ýumşak","мягкий","ADJ"),
 ("solid","gaty","твёрдый","ADJ"),
 ("spare","ätiýaçlyk","запасной","ADJ"),
 ("straight","göni","прямой","ADJ"),("strange","geň","странный","ADJ"),
 ("strict","gaty","строгий","ADJ"),("stupid","akylsyz","глупый","ADJ"),
 ("successful","üstünlikli","успешный","ADJ"),("sudden","duýdansyz","внезапный","ADJ"),
 ("suitable","laýyk","подходящий","ADJ"),("surprised","haýran","удивлённый","ADJ"),
 ("talented","zehinli","талантливый","ADJ"),("terrible","elhenç","ужасный","ADJ"),
 ("thirsty person","susuz","испытывающий жажду","ADJ"),("tight","gysyk","тугой","ADJ"),
 ("tiny","örän kiçi","крошечный","ADJ"),("tired person","ýadaw","уставший","ADJ"),
 ("total","jemi","общий","ADJ"),("tough","berk","жёсткий","ADJ"),
 ("typical","adaty","типичный","ADJ"),("unusual","adaty däl","необычный","ADJ"),
 ("useful","peýdaly","полезный","ADJ"),("usual","adaty","обычный","ADJ"),
 ("various","dürli","различный","ADJ"),("vast","giň","обширный","ADJ"),
 ("weak person","gowşak","слабый","ADJ"),("wealthy","baý","состоятельный","ADJ"),
 ("weird","geň","причудливый","ADJ"),("welcome word","hoş","желанный","ADJ"),
 ("western","günbatar","западный","ADJ"),("whole thing","bitin","целый","ADJ"),
 ("willing","meýletin","желающий","ADJ"),("wise","paýhasly","мудрый","ADJ"),
 ("wonderful","ajaýyp","замечательный","ADJ"),("wooden","agachdan","деревянный","ADJ"),
 ("worth","mynasyp","стоящий","ADJ"),("wrong thing","ýalňyş","ошибочный","ADJ"),
 ("young person","ýaş","молодой","ADJ"),
 # nouns: household, tech, travel, emotion, materials, more
 ("apartment","öý","квартира","N"),("attic","üçek","чердак","N"),
 ("balcony","balkon","балкон","N"),("basement","zirzemin","подвал","N"),
 ("bath","ýuwunma","ванна","N"),("blanket","ýorgan","одеяло","N"),
 ("ceiling","potolok","потолок","N"),("curtain","perde","занавеска","N"),
 ("cushion","ýassyk","подушка","N"),("drawer","ýaşyk","ящик","N"),
 ("furniture","mebel","мебель","N"),("garage","garazh","гараж","N"),
 ("gate","derweze","ворота","N"),("hall","zal","зал","N"),
 ("iron","ütük","утюг","N"),("kettle","çäýnek","чайник","N"),
 ("ladder","merdiwan","лестница","N"),("pillow","ýassyk","подушка","N"),
 ("refrigerator","sowadyjy","холодильник","N"),("shelf","tekje","полка","N"),
 ("soap","sabyn","мыло","N"),("stove","peç","плита","N"),
 ("suitcase","çemodan","чемодан","N"),("telephone","telefon","телефон","N"),
 ("towel","dezmalyk","полотенце","N"),("vacuum","tozsoran","пылесос","N"),
 ("wallet","gapjyk","кошелёк","N"),("washing machine","ýuwujy maşyn","стиральная машина","N"),
 ("internet","internet","интернет","N"),("website","web sahypa","веб-сайт","N"),
 ("email","e-poçta","электронная почта","N"),("message","habar","сообщение","N"),
 ("screen","ekran","экран","N"),("keyboard","klawiatura","клавиатура","N"),
 ("computer mouse","syçanjyk","компьютерная мышь","N"),("battery","batareýa","батарея","N"),
 ("charger","zarýadnik","зарядное устройство","N"),("camera","kamera","камера","N"),
 ("video","wideo","видео","N"),("program","programma","программа","N"),
 ("data","maglumat","данные","N"),("file","faýl","файл","N"),
 ("password","parol","пароль","N"),("button","düwme","кнопка","N"),
 ("adventure","başdan geçirme","приключение","N"),("journey","syýahat","путешествие","N"),
 ("passenger","ýolagçy","пассажир","N"),("luggage","goş","багаж","N"),
 ("passport","pasport","паспорт","N"),("customs","gümrük","таможня","N"),
 ("traffic","ýol hereketi","движение","N"),("accident","betbagtçylyk","авария","N"),
 ("fuel","ýangyç","топливо","N"),("engine","hereketlendiriji","двигатель","N"),
 ("wheel","tigir","колесо","N"),("speed limit","tizlik çägi","ограничение скорости","N"),
 ("anger","gahar","гнев","N"),("happiness","bagt","счастье","N"),
 ("sadness","gam","печаль","N"),
 ("confidence","ynam","уверенность","N"),
 ("patience","sabyr","терпение","N"),("courage","gaýrat","смелость","N"),
 ("memory","ýat","память","N"),("thought","pikir","мысль","N"),
 ("attention","üns","внимание","N"),("interest","gyzyklanma","интерес","N"),
 ("wish noun","arzuw","желание","N"),("effort","tagalla","усилие","N"),
 ("success","üstünlik","успех","N"),("failure","şowsuzlyk","неудача","N"),
 ("goal","maksat","цель","N"),("purpose","maksat","цель","N"),
 ("wood","agaç","дерево","N"),("metal","metal","металл","N"),
 ("plastic","plastik","пластик","N"),("glass material","aýna","стекло","N"),
 ("leather","deri","кожа","N"),("cotton","pagta","хлопок","N"),
 ("silk","ipak","шёлк","N"),("wool","ýüň","шерсть","N"),
 ("gold","altyn","золото","N"),("silver","kümüş","серебро","N"),
 ("iron metal","demir","железо","N"),("copper","mis","медь","N"),
 ("coal","kömür","уголь","N"),("gas","gaz","газ","N"),
 ("electricity","elektrik","электричество","N"),("energy","energiýa","энергия","N"),
 ("engineer person","inžener","инженер","N"),("lawyer","ýurist","юрист","N"),
 ("nurse person","şepagat uýasy","медсестра","N"),("pilot","uçarman","пилот","N"),
 ("scientist","alym","учёный","N"),("writer","ýazyjy","писатель","N"),
 ("journalist","žurnalist","журналист","N"),("photographer","suratkeş","фотограф","N"),
 ("dentist","diş lukmany","дантист","N"),("vet","weterinar","ветеринар","N"),
 ("manager","dolandyryjy","менеджер","N"),("secretary","kätip","секретарь","N"),
 ("accountant","hasapçy","бухгалтер","N"),("tailor","tikaçy","портной","N"),
 ("barber","sartaraş","парикмахер","N"),("waiter","ofisiant","официант","N"),
 ("guard","goragçy","охранник","N"),("cleaner","arassalaýjy","уборщик","N"),
 ("brick","kerpiç","кирпич","N"),("cement","sement","цемент","N"),
 ("nail","çüý","гвоздь","N"),("hammer","bolotok","молоток","N"),
 ("saw","byçgy","пила","N"),("tool","gural","инструмент","N"),
 ("machine","maşyn","машина","N"),("device","enjam","устройство","N"),
 ("weather rain","ýagyş","дождь","N"),("fog","duman","туман","N"),
 ("ice","buz","лёд","N"),("flood","suw joşmasy","наводнение","N"),
 ("earthquake","ýer titremesi","землетрясение","N"),("climate","howa","климат","N"),
 ("season","pasyl","сезон","N"),("temperature weather","temperatura","температура","N"),
 ("north","demirgazyk","север","N"),("south","günorta","юг","N"),
 ("east","gündogar","восток","N"),("west","günbatar","запад","N"),
 ("direction","ugur","направление","N"),("distance way","aralyk","расстояние","N"),
 ("corner","burç","угол","N"),("edge","gyra","край","N"),
 ("middle","orta","середина","N"),("side","tarap","сторона","N"),
 ("top","depesi","верх","N"),("bottom","asty","низ","N"),
 ("front","öň","перед","N"),("behind","yzy","позади","N"),
 ("inside","içi","внутри","N"),("outside","daşy","снаружи","N"),
 ("entrance","giriş","вход","N"),("exit","çykyş","выход","N"),
 ("step","ädim","шаг","N"),("path","ýoda","тропинка","N"),
 ("trip","syýahat","поездка","N"),("tour","tur","тур","N"),
 ("guest person","myhman","гость","N"),("host","hojaýyn","хозяин","N"),
 ("party","agşamlama","вечеринка","N"),("wedding","toý","свадьба","N"),
 ("funeral","jynaza","похороны","N"),("celebration","baýram","празднование","N"),
 ("letter mail","hat","письмо","N"),
 ("stamp","marka","марка","N"),("envelope","konwert","конверт","N"),
 ("parcel","posylka","посылка","N"),("message note","bellik","заметка","N"),
 ("diary","gündelik","дневник","N"),("dictionary","sözlük","словарь","N"),
 ("sentence grammar","sözlem","предложение","N"),("grammar","grammatika","грамматика","N"),
 ("pronunciation","aýdylyş","произношение","N"),("meaning","many","значение","N"),
 ("translation","terjime","перевод","N"),("exercise","maşk","упражнение","N"),
 ("test exam","synag","тест","N"),("mark","baha","оценка","N"),
 ("certificate","şahadatnama","свидетельство","N"),("degree","dereje","степень","N"),
 ("knowledge","bilim","знание","N"),("skill","endik","навык","N"),
 ("experience","tejribe","опыт","N"),("training","türgenleşik","обучение","N"),
 ("practice noun","tejribe","практика","N"),("lesson class","sapak","занятие","N"),
)

# --- validate -------------------------------------------------------------
# Drop awkward filler headwords that were only added to dodge an en collision;
# the clean base word already exists, so these add nothing but noise to Search.
REMOVE={"chicken bird","fish animal","kind person","breakfast food","meal time",
        "tasty food","flower garden","green field","man friend","cheap price",
        "seem appear"}
DATA=[r for r in DATA if r[0] not in REMOVE]

# The general dictionary must only ADD words the Oxford English File books do not
# already teach. If a headword is already a book word, the book's richer entry
# (definition, example, IPA, lesson) wins and the dictionary duplicate is dropped,
# so Search never shows the same word twice.
try:
    import os
    _merged=os.path.join(os.path.dirname(__file__),"..","merged","yatla-all.json")
    _pack=json.load(open(_merged,encoding="utf-8"))
    _pw=_pack["words"] if isinstance(_pack,dict) and "words" in _pack else _pack
    BOOK_EN=set(w["en"].strip().lower() for w in _pw)
    _before=len(DATA)
    DATA=[r for r in DATA if r[0].strip().lower() not in BOOK_EN]
    print("dedup vs books: dropped %d headwords already taught by the books" % (_before-len(DATA)))
except Exception as e:
    print("WARNING: could not dedup against book pack (%s)" % e)

errors=[]
seen={}
for en,tm,ru,pos in DATA:
    if en in seen:
        errors.append("DUP en %r" % en)
    seen[en]=1
    m=check_tm(en,tm)
    if m: errors.append(m)
    m=check_ru(en,ru)
    if m: errors.append(m)
    if pos not in {"N","V","ADJ","ADV","PREP","CONJ","PRON","NUM","INTJ"}:
        errors.append("BAD pos %r for %r" % (pos,en))

if errors:
    print("VALIDATION ERRORS (%d):" % len(errors))
    for e in errors[:60]:
        print("  ", e)
    sys.exit(1)

rows=[[en,tm,ru,pos] for (en,tm,ru,pos) in DATA]
out={"version":1,"format":"dict","fields":["en","tm","ru","pos"],"rows":rows}
with open("content/dict-general.json","w",encoding="utf-8") as f:
    json.dump(out,f,ensure_ascii=False,separators=(",",":"))
print("OK: %d general dictionary words written to content/dict-general.json" % len(rows))
# distribution
from collections import Counter
c=Counter(r[3] for r in rows)
print("by pos:", dict(c))
