"""captions.sbv(한국어)를 11개 언어로 옮긴 .sbv 파일 생성.

타임코드·줄 구성은 원본 그대로 두고, 자막 문장만 언어별 번역으로 바꾼다.
번역은 문장 단위 표(KO 순서와 같은 순서)로 관리한다. 원본에 없는 문장이 있으면 에러.
실행: python make_captions.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "captions.sbv")

KO = [
    "안녕하세요~여러분", "미노 쌤이에요", "저는 오늘 마트에 가요", "마트에 가요", "걸어서 갈 거예요",
    "같이 가볼까요?", "마트에 도착했어요", "카트를 꺼내요", "마트에 들어가요", "2층으로 올라가요",
    "음료", "음료가 있어요", "음료가 많아요", "많아요", "맥주도 많아요",
    "우유도 있어요", "유통기한을 확인해요", "확인해요", "과자", "과자가 있어요",
    "감자칩이 있어요", "이 과자를 좋아해요", "좋아해요", "이 과자를 골라요", "과자를 골라요",
    "라면도 있어요", "라면도 많아요", "이 라면은 매워요", "매워요", "이 라면을 좋아해요",
    "라면을 담아요", "카트에 담아요", "김치도 있어요", "같이 먹으면", "맛있어요",
    "두부", "두부는 세일해요", "세일해요", "피자 있어요", "만두도 있어요",
    "아이스크림 있어요", "추워요", "그래서 안 먹어요", "내려가요", "과일이 있어요",
    "과일", "배는 3개 있어요", "3개 있어요", "사과는 5개 있어요", "5개 있어요",
    "감자", "고구마", "당근", "돼지고기", "돼지고기는 싸요",
    "싸요", "소고기", "소고기도 있어요", "소고기는 비싸요", "비싸요",
    "소고기는", "소고기는 돼지고기보다", "소고기는 돼지고기보다 비싸요", "이제 계산해요", "계산해요",
    "바코드를 찍어요", "바코드", "카드로 계산해요", "영수증", "영수증을 받아요",
    "봉투에 담았어요", "담았어요", "조금 무거워요", "오늘은 마트에 다녀왔어요", "마트에서",
    "과자 샀어요", "라면도 샀어요", "여러분들은 마트에서 뭘 사요?", "댓글에 남겨주세요", "그럼 다음 영상에서 만나요",
]

T = {}

T["en"] = [
    "Hello, everyone~", "I'm Teacher Mino.", "Today I'm going to the supermarket.", "I'm going to the supermarket.", "I'm going to walk there.",
    "Shall we go together?", "We've arrived at the supermarket.", "I take out a cart.", "I go into the supermarket.", "I'm going up to the 2nd floor.",
    "Drinks", "There are drinks.", "There are lots of drinks.", "Lots!", "There's lots of beer, too.",
    "There's milk, too.", "I check the expiration date.", "Check.", "Snacks", "There are snacks.",
    "There are potato chips.", "I like this snack.", "I like it.", "I'll pick this snack.", "I pick a snack.",
    "There's ramyeon, too.", "There's lots of ramyeon, too.", "This ramyeon is spicy.", "Spicy!", "I like this ramyeon.",
    "I put the ramyeon in.", "I put it in the cart.", "There's kimchi, too.", "If you eat them together,", "it's delicious.",
    "Tofu", "Tofu is on sale.", "On sale!", "There's pizza.", "There are dumplings, too.",
    "There's ice cream.", "It's cold.", "So I'm not eating it.", "Going down.", "There's fruit.",
    "Fruit", "There are 3 pears.", "There are 3.", "There are 5 apples.", "There are 5.",
    "Potatoes", "Sweet potatoes", "Carrots", "Pork", "Pork is cheap.",
    "Cheap.", "Beef", "There's beef, too.", "Beef is expensive.", "Expensive.",
    "Beef...", "Beef... than pork...", "Beef is more expensive than pork.", "Now let's pay.", "Pay.",
    "I scan the barcode.", "Barcode", "I pay by card.", "Receipt", "I get the receipt.",
    "I put everything in the bag.", "All packed!", "It's a little heavy.", "Today I went to the supermarket.", "At the supermarket,",
    "I bought snacks.", "I bought ramyeon, too.", "What do you buy at the supermarket?", "Leave it in the comments!", "See you in the next video!",
]

T["zh-Hans"] = [
    "大家好~", "我是米诺老师。", "我今天去超市。", "去超市。", "我要走路去。",
    "一起去看看吧？", "到超市了。", "拿出购物车。", "走进超市。", "上二楼。",
    "饮料", "有饮料。", "饮料很多。", "很多。", "啤酒也很多。",
    "也有牛奶。", "确认保质期。", "确认一下。", "零食", "有零食。",
    "有薯片。", "我喜欢这个零食。", "喜欢。", "选这个零食。", "选零食。",
    "也有拉面。", "拉面也很多。", "这个拉面很辣。", "很辣。", "我喜欢这个拉面。",
    "把拉面放进去。", "放进购物车。", "也有泡菜。", "一起吃的话", "很好吃。",
    "豆腐", "豆腐在打折。", "打折。", "有披萨。", "也有饺子。",
    "有冰淇淋。", "好冷。", "所以不吃。", "下楼。", "有水果。",
    "水果", "梨有3个。", "有3个。", "苹果有5个。", "有5个。",
    "土豆", "红薯", "胡萝卜", "猪肉", "猪肉很便宜。",
    "便宜。", "牛肉", "也有牛肉。", "牛肉很贵。", "贵。",
    "牛肉……", "牛肉比猪肉……", "牛肉比猪肉贵。", "现在结账。", "结账。",
    "扫条形码。", "条形码", "用卡结账。", "收据", "拿收据。",
    "装进袋子里了。", "装好了。", "有点重。", "今天去了一趟超市。", "在超市",
    "买了零食。", "还买了拉面。", "大家在超市买什么？", "请在评论区留言。", "那我们下个视频见！",
]

T["id"] = [
    "Halo, semuanya~", "Saya Guru Mino.", "Hari ini saya pergi ke supermarket.", "Pergi ke supermarket.", "Saya akan jalan kaki.",
    "Mau pergi bersama?", "Kita sudah sampai di supermarket.", "Saya ambil troli.", "Masuk ke supermarket.", "Naik ke lantai 2.",
    "Minuman", "Ada minuman.", "Minumannya banyak.", "Banyak.", "Birnya juga banyak.",
    "Ada susu juga.", "Saya cek tanggal kedaluwarsa.", "Cek.", "Camilan", "Ada camilan.",
    "Ada keripik kentang.", "Saya suka camilan ini.", "Saya suka.", "Saya pilih camilan ini.", "Pilih camilan.",
    "Ada ramyeon juga.", "Ramyeonnya juga banyak.", "Ramyeon ini pedas.", "Pedas.", "Saya suka ramyeon ini.",
    "Masukkan ramyeon.", "Masukkan ke troli.", "Ada kimchi juga.", "Kalau dimakan bersama,", "enak sekali.",
    "Tahu", "Tahu sedang diskon.", "Diskon.", "Ada pizza.", "Ada mandu (pangsit) juga.",
    "Ada es krim.", "Dingin.", "Jadi saya tidak makan.", "Turun.", "Ada buah.",
    "Buah", "Ada 3 buah pir.", "Ada 3.", "Ada 5 buah apel.", "Ada 5.",
    "Kentang", "Ubi", "Wortel", "Daging babi", "Daging babi murah.",
    "Murah.", "Daging sapi", "Ada daging sapi juga.", "Daging sapi mahal.", "Mahal.",
    "Daging sapi...", "Daging sapi... daripada daging babi...", "Daging sapi lebih mahal daripada daging babi.", "Sekarang bayar.", "Bayar.",
    "Pindai barkodenya.", "Barkode", "Bayar pakai kartu.", "Struk", "Terima struknya.",
    "Sudah dimasukkan ke kantong.", "Sudah masuk.", "Agak berat.", "Hari ini saya pergi ke supermarket.", "Di supermarket,",
    "saya beli camilan.", "saya juga beli ramyeon.", "Kalian beli apa di supermarket?", "Tulis di kolom komentar, ya.", "Sampai jumpa di video berikutnya!",
]

T["pt-BR"] = [
    "Olá, pessoal~", "Mino aqui!", "Hoje eu vou ao supermercado.", "Vou ao supermercado.", "Vou a pé.",
    "Vamos juntos?", "Chegamos ao supermercado.", "Pego um carrinho.", "Entro no supermercado.", "Subo para o primeiro andar.",
    "Bebidas", "Tem bebidas.", "Tem muitas bebidas.", "Muitas!", "Tem muita cerveja também.",
    "Tem leite também.", "Confiro a data de validade.", "Confiro.", "Salgadinhos", "Tem salgadinhos.",
    "Tem batata chips.", "Eu gosto deste salgadinho.", "Eu gosto.", "Escolho este salgadinho.", "Escolho um salgadinho.",
    "Tem lámen também.", "Tem muito lámen também.", "Este lámen é apimentado.", "Apimentado!", "Eu gosto deste lámen.",
    "Coloco o lámen.", "Coloco no carrinho.", "Tem kimchi também.", "Se comer junto,", "fica delicioso.",
    "Tofu", "O tofu está em promoção.", "Em promoção!", "Tem pizza.", "Tem mandu (bolinho) também.",
    "Tem sorvete.", "Está frio.", "Então não vou comer.", "Desço.", "Tem frutas.",
    "Frutas", "Tem 3 peras.", "Tem 3.", "Tem 5 maçãs.", "Tem 5.",
    "Batata", "Batata-doce", "Cenoura", "Carne de porco", "A carne de porco é barata.",
    "Barata.", "Carne bovina", "Tem carne bovina também.", "A carne bovina é cara.", "Cara.",
    "A carne bovina...", "A carne bovina... do que a de porco...", "A carne bovina é mais cara do que a de porco.", "Agora vou pagar.", "Pagar.",
    "Passo o código de barras.", "Código de barras", "Pago com cartão.", "Recibo", "Pego o recibo.",
    "Coloquei tudo na sacola.", "Pronto!", "Está um pouco pesado.", "Hoje eu fui ao supermercado.", "No supermercado,",
    "comprei salgadinhos.", "comprei lámen também.", "E vocês, o que compram no supermercado?", "Deixem nos comentários!", "Então, até o próximo vídeo!",
]

T["fil"] = [
    "Kumusta kayong lahat~", "Ako si Teacher Mino.", "Pupunta ako sa supermarket ngayon.", "Pupunta sa supermarket.", "Maglalakad ako papunta roon.",
    "Sabay tayong pumunta?", "Nakarating na tayo sa supermarket.", "Kukuha ako ng cart.", "Papasok sa supermarket.", "Aakyat sa 2nd floor.",
    "Inumin", "May mga inumin.", "Ang daming inumin.", "Ang dami.", "Marami ring beer.",
    "May gatas din.", "Titingnan ko ang expiration date.", "Titingnan.", "Snacks", "May snacks.",
    "May potato chips.", "Gusto ko ang snack na ito.", "Gusto ko.", "Pipiliin ko ang snack na ito.", "Pumipili ng snack.",
    "May ramyeon din.", "Marami ring ramyeon.", "Maanghang ang ramyeon na ito.", "Maanghang.", "Gusto ko ang ramyeon na ito.",
    "Ilalagay ko ang ramyeon.", "Ilalagay sa cart.", "May kimchi din.", "Kapag kinain nang sabay,", "masarap.",
    "Tofu", "Naka-sale ang tofu.", "Naka-sale.", "May pizza.", "May mandu (dumplings) din.",
    "May ice cream.", "Malamig.", "Kaya hindi ako kakain.", "Bababa.", "May prutas.",
    "Prutas", "May 3 peras.", "May 3.", "May 5 mansanas.", "May 5.",
    "Patatas", "Kamote", "Karot", "Baboy", "Mura ang baboy.",
    "Mura.", "Baka", "May baka rin.", "Mahal ang baka.", "Mahal.",
    "Ang baka...", "Ang baka... kaysa sa baboy...", "Mas mahal ang baka kaysa sa baboy.", "Magbabayad na tayo.", "Bayad.",
    "I-scan ang barcode.", "Barcode", "Magbabayad gamit ang card.", "Resibo", "Kukunin ang resibo.",
    "Inilagay ko na sa bag.", "Nailagay na.", "Medyo mabigat.", "Pumunta ako sa supermarket ngayon.", "Sa supermarket,",
    "bumili ako ng snacks.", "bumili rin ako ng ramyeon.", "Kayo, ano ang binibili ninyo sa supermarket?", "Isulat sa comments!", "Kita-kits sa susunod na video!",
]

T["ru"] = [
    "Всем привет~", "С вами Мино!", "Сегодня я иду в супермаркет.", "Иду в супермаркет.", "Пойду пешком.",
    "Пойдём вместе?", "Мы пришли в супермаркет.", "Беру тележку.", "Заходим в супермаркет.", "Поднимаемся на 2-й этаж.",
    "Напитки", "Здесь есть напитки.", "Напитков много.", "Много.", "Пива тоже много.",
    "Есть и молоко.", "Проверяю срок годности.", "Проверяю.", "Снеки", "Есть снеки.",
    "Есть картофельные чипсы.", "Мне нравится этот снек.", "Нравится.", "Выбираю этот снек.", "Выбираю снек.",
    "Есть и рамён.", "Рамёна тоже много.", "Этот рамён острый.", "Острый.", "Мне нравится этот рамён.",
    "Кладу рамён.", "Кладу в тележку.", "Есть и кимчи.", "Если есть вместе,", "очень вкусно.",
    "Тофу", "На тофу скидка.", "Скидка.", "Есть пицца.", "Есть и манду (пельмени).",
    "Есть мороженое.", "Холодно.", "Поэтому не буду есть.", "Спускаемся.", "Есть фрукты.",
    "Фрукты", "Груш — 3 штуки.", "3 штуки.", "Яблок — 5 штук.", "5 штук.",
    "Картофель", "Батат", "Морковь", "Свинина", "Свинина дешёвая.",
    "Дешёвая.", "Говядина", "Есть и говядина.", "Говядина дорогая.", "Дорогая.",
    "Говядина...", "Говядина... чем свинина...", "Говядина дороже, чем свинина.", "Теперь оплачиваем.", "Оплачиваем.",
    "Сканируем штрихкод.", "Штрихкод", "Оплачиваю картой.", "Чек", "Беру чек.",
    "Всё сложено в пакет.", "Готово.", "Немного тяжело.", "Сегодня у нас был поход в супермаркет.", "В супермаркете",
    "мы купили снеки.", "и ещё рамён.", "А что вы покупаете в супермаркете?", "Напишите в комментариях!", "Увидимся в следующем видео!",
]

T["es"] = [
    "¡Hola a todos~!", "¡Soy Mino, tu profe!", "Hoy voy al supermercado.", "Voy al supermercado.", "Voy a ir caminando.",
    "¿Vamos juntos?", "Llegamos al supermercado.", "Saco un carrito.", "Entro al supermercado.", "Subo al segundo piso.",
    "Bebidas", "Hay bebidas.", "Hay muchas bebidas.", "¡Muchas!", "También hay mucha cerveza.",
    "También hay leche.", "Reviso la fecha de caducidad.", "Reviso.", "Snacks", "Hay snacks.",
    "Hay papas fritas de bolsa.", "Me gusta este snack.", "Me gusta.", "Elijo este snack.", "Elijo un snack.",
    "También hay ramyeon.", "También hay mucho ramyeon.", "Este ramyeon es picante.", "¡Picante!", "Me gusta este ramyeon.",
    "Pongo el ramyeon.", "Lo pongo en el carrito.", "También hay kimchi.", "Si los comes juntos,", "¡está delicioso!",
    "Tofu", "El tofu está en oferta.", "¡En oferta!", "Hay pizza.", "También hay mandu (empanadillas).",
    "Hay helado.", "Hace frío.", "Así que no lo voy a comer.", "Bajo.", "Hay fruta.",
    "Fruta", "Hay 3 peras.", "Hay 3.", "Hay 5 manzanas.", "Hay 5.",
    "Papas", "Batatas", "Zanahorias", "Carne de cerdo", "El cerdo es barato.",
    "Barato.", "Carne de res", "También hay carne de res.", "La carne de res es cara.", "Cara.",
    "La carne de res...", "La carne de res... que el cerdo...", "La carne de res es más cara que el cerdo.", "Ahora vamos a pagar.", "Pagar.",
    "Escaneo el código de barras.", "Código de barras", "Pago con tarjeta.", "Recibo", "Tomo el recibo.",
    "Lo metí todo en la bolsa.", "¡Listo!", "Pesa un poco.", "Hoy fui al supermercado.", "En el supermercado",
    "compré snacks.", "y también compré ramyeon.", "¿Y ustedes qué compran en el supermercado?", "¡Déjenlo en los comentarios!", "¡Nos vemos en el próximo video!",
]

T["fr"] = [
    "Bonjour à tous~", "C'est Mino, votre prof !", "Aujourd'hui, je vais au supermarché.", "Je vais au supermarché.", "J'y vais à pied.",
    "On y va ensemble ?", "Voilà le supermarché !", "Je prends un chariot.", "J'entre dans le supermarché.", "Je monte au premier étage.",
    "Boissons", "Il y a des boissons.", "Il y a beaucoup de boissons.", "Beaucoup !", "Il y a aussi beaucoup de bière.",
    "Il y a aussi du lait.", "Je vérifie la date de péremption.", "Je vérifie.", "Snacks", "Il y a des snacks.",
    "Il y a des chips.", "J'aime ce snack.", "J'aime bien.", "Je choisis ce snack.", "Je choisis un snack.",
    "Il y a aussi des ramyeon.", "Il y a aussi beaucoup de ramyeon.", "Ce ramyeon est épicé.", "Épicé !", "J'aime ce ramyeon.",
    "Je mets le ramyeon.", "Je le mets dans le chariot.", "Il y a aussi du kimchi.", "Si on les mange ensemble,", "c'est délicieux.",
    "Tofu", "Le tofu est en promo.", "En promo !", "Il y a de la pizza.", "Il y a aussi des mandu (raviolis).",
    "Il y a de la glace.", "Il fait froid.", "Donc je n'en mange pas.", "Je descends.", "Il y a des fruits.",
    "Fruits", "Il y a 3 poires.", "Il y en a 3.", "Il y a 5 pommes.", "Il y en a 5.",
    "Pommes de terre", "Patates douces", "Carottes", "Porc", "Le porc n'est pas cher.",
    "Pas cher.", "Bœuf", "Il y a aussi du bœuf.", "Le bœuf est cher.", "Cher.",
    "Le bœuf...", "Le bœuf... que le porc...", "Le bœuf est plus cher que le porc.", "Maintenant, je paie.", "Je paie.",
    "Je scanne le code-barres.", "Code-barres", "Je paie par carte.", "Ticket de caisse", "Je prends le ticket.",
    "J'ai tout mis dans le sac.", "C'est fait !", "C'est un peu lourd.", "Aujourd'hui, j'ai fait les courses au supermarché.", "Au supermarché,",
    "j'ai acheté des snacks.", "j'ai aussi acheté des ramyeon.", "Et vous, qu'est-ce que vous achetez au supermarché ?", "Dites-le-moi en commentaire !", "À la prochaine vidéo !",
]

T["de"] = [
    "Hallo zusammen~", "Hier ist Mino!", "Heute gehe ich in den Supermarkt.", "Ich gehe in den Supermarkt.", "Ich gehe zu Fuß.",
    "Kommt ihr mit?", "Wir sind am Supermarkt.", "Ich nehme einen Einkaufswagen.", "Ich gehe in den Supermarkt.", "Ich gehe hoch in den ersten Stock.",
    "Getränke", "Es gibt Getränke.", "Es gibt viele Getränke.", "Viele!", "Es gibt auch viel Bier.",
    "Es gibt auch Milch.", "Ich prüfe das Mindesthaltbarkeitsdatum.", "Ich prüfe.", "Snacks", "Es gibt Snacks.",
    "Es gibt Kartoffelchips.", "Ich mag diesen Snack.", "Mag ich.", "Ich nehme diesen Snack.", "Ich wähle einen Snack.",
    "Es gibt auch Ramyeon.", "Es gibt auch viel Ramyeon.", "Dieses Ramyeon ist scharf.", "Scharf!", "Ich mag dieses Ramyeon.",
    "Ich lege das Ramyeon rein.", "Ich lege es in den Wagen.", "Es gibt auch Kimchi.", "Wenn man es zusammen isst,", "ist es lecker.",
    "Tofu", "Tofu ist im Angebot.", "Im Angebot!", "Es gibt Pizza.", "Es gibt auch Mandu (Teigtaschen).",
    "Es gibt Eis.", "Es ist kalt.", "Deshalb esse ich keins.", "Ich gehe runter.", "Es gibt Obst.",
    "Obst", "Es gibt 3 Birnen.", "Es gibt 3.", "Es gibt 5 Äpfel.", "Es gibt 5.",
    "Kartoffeln", "Süßkartoffeln", "Karotten", "Schweinefleisch", "Schweinefleisch ist billig.",
    "Billig.", "Rindfleisch", "Es gibt auch Rindfleisch.", "Rindfleisch ist teuer.", "Teuer.",
    "Rindfleisch...", "Rindfleisch... als Schweinefleisch...", "Rindfleisch ist teurer als Schweinefleisch.", "Jetzt bezahle ich.", "Bezahlen.",
    "Ich scanne den Barcode.", "Barcode", "Ich zahle mit Karte.", "Kassenbon", "Ich nehme den Kassenbon.",
    "Ich habe alles in die Tüte gepackt.", "Fertig!", "Es ist ein bisschen schwer.", "Heute war ich im Supermarkt.", "Im Supermarkt",
    "habe ich Snacks gekauft.", "habe ich auch Ramyeon gekauft.", "Und was kauft ihr im Supermarkt?", "Schreibt es in die Kommentare!", "Bis zum nächsten Video!",
]

T["ar"] = [
    "مرحبًا بالجميع~", "معكم مينو!", "اليوم سأذهب إلى السوبرماركت.", "أذهب إلى السوبرماركت.", "سأذهب مشيًا.",
    "هل نذهب معًا؟", "وصلنا إلى السوبرماركت.", "آخذ عربة التسوق.", "أدخل السوبرماركت.", "أصعد إلى الطابق الثاني.",
    "المشروبات", "توجد مشروبات.", "المشروبات كثيرة.", "كثيرة!", "والبيرة كثيرة أيضًا.",
    "يوجد حليب أيضًا.", "أتحقق من تاريخ انتهاء الصلاحية.", "أتحقق.", "الوجبات الخفيفة", "توجد وجبات خفيفة.",
    "توجد رقائق البطاطس.", "أحب هذه الوجبة الخفيفة.", "أحبها.", "أختار هذه الوجبة الخفيفة.", "أختار وجبة خفيفة.",
    "يوجد راميون أيضًا.", "والراميون كثير أيضًا.", "هذا الراميون حار.", "حار!", "أحب هذا الراميون.",
    "أضع الراميون.", "أضعه في العربة.", "يوجد كيمتشي أيضًا.", "إذا أكلتهما معًا،", "يكون لذيذًا.",
    "توفو", "التوفو عليه تخفيض.", "تخفيض!", "توجد بيتزا.", "يوجد ماندو (فطائر محشوة) أيضًا.",
    "يوجد آيس كريم.", "الجو بارد.", "لذلك لن آكله.", "أنزل.", "توجد فواكه.",
    "فواكه", "توجد 3 حبات كمثرى.", "توجد 3.", "توجد 5 تفاحات.", "توجد 5.",
    "بطاطس", "بطاطا حلوة", "جزر", "لحم الخنزير", "لحم الخنزير رخيص.",
    "رخيص.", "لحم البقر", "يوجد لحم بقر أيضًا.", "لحم البقر غالٍ.", "غالٍ.",
    "لحم البقر...", "لحم البقر... من لحم الخنزير...", "لحم البقر أغلى من لحم الخنزير.", "الآن أدفع.", "أدفع.",
    "أمسح الباركود.", "الباركود", "أدفع بالبطاقة.", "الإيصال", "آخذ الإيصال.",
    "وضعت كل شيء في الكيس.", "تم!", "ثقيل قليلًا.", "اليوم ذهبت إلى السوبرماركت.", "في السوبرماركت",
    "اشتريت وجبات خفيفة.", "واشتريت راميون أيضًا.", "وأنتم، ماذا تشترون من السوبرماركت؟", "اكتبوا لي في التعليقات!", "أراكم في الفيديو القادم!",
]

T["ja"] = [
    "みなさん、こんにちは～", "ミノ先生です。", "今日はスーパーに行きます。", "スーパーに行きます。", "歩いて行きます。",
    "一緒に行ってみましょうか？", "スーパーに着きました。", "カートを出します。", "スーパーに入ります。", "2階に上がります。",
    "飲み物", "飲み物があります。", "飲み物がたくさんあります。", "たくさん！", "ビールもたくさんあります。",
    "牛乳もあります。", "賞味期限を確認します。", "確認します。", "お菓子", "お菓子があります。",
    "ポテトチップスがあります。", "このお菓子が好きです。", "好きです。", "このお菓子を選びます。", "お菓子を選びます。",
    "ラーメンもあります。", "ラーメンもたくさんあります。", "このラーメンは辛いです。", "辛い！", "このラーメンが好きです。",
    "ラーメンを入れます。", "カートに入れます。", "キムチもあります。", "一緒に食べると", "おいしいです。",
    "豆腐", "豆腐はセール中です。", "セール中！", "ピザがあります。", "餃子もあります。",
    "アイスクリームがあります。", "寒いです。", "だから食べません。", "下ります。", "果物があります。",
    "果物", "梨は3個あります。", "3個あります。", "りんごは5個あります。", "5個あります。",
    "じゃがいも", "さつまいも", "にんじん", "豚肉", "豚肉は安いです。",
    "安いです。", "牛肉", "牛肉もあります。", "牛肉は高いです。", "高いです。",
    "牛肉は…", "牛肉は豚肉より…", "牛肉は豚肉より高いです。", "では、会計します。", "会計します。",
    "バーコードを読み取ります。", "バーコード", "カードで払います。", "レシート", "レシートをもらいます。",
    "袋に入れました。", "入れました。", "ちょっと重いです。", "今日はスーパーに行ってきました。", "スーパーで",
    "お菓子を買いました。", "ラーメンも買いました。", "みなさんはスーパーで何を買いますか？", "コメントで教えてください。", "では、次の動画で会いましょう！",
]

T["ms"] = [
    "Hai semua~", "Saya Cikgu Mino.", "Hari ini saya pergi ke pasar raya.", "Pergi ke pasar raya.", "Saya akan berjalan kaki.",
    "Jom pergi bersama?", "Kita dah sampai di pasar raya.", "Saya ambil troli.", "Masuk ke pasar raya.", "Naik ke tingkat 1.",
    "Minuman", "Ada minuman.", "Banyak minuman.", "Banyak!", "Bir pun banyak.",
    "Susu pun ada.", "Saya periksa tarikh luput.", "Periksa.", "Snek", "Ada snek.",
    "Ada kerepek kentang.", "Saya suka snek ini.", "Saya suka.", "Saya pilih snek ini.", "Pilih snek.",
    "Ramyeon pun ada.", "Ramyeon pun banyak.", "Ramyeon ini pedas.", "Pedas!", "Saya suka ramyeon ini.",
    "Masukkan ramyeon.", "Masukkan ke dalam troli.", "Kimchi pun ada.", "Kalau makan bersama,", "sedap.",
    "Tauhu", "Tauhu sedang jualan murah.", "Jualan murah!", "Ada piza.", "Mandu (ladu) pun ada.",
    "Ada aiskrim.", "Sejuk.", "Jadi saya tak makan.", "Turun.", "Ada buah.",
    "Buah", "Ada 3 biji pear.", "Ada 3.", "Ada 5 biji epal.", "Ada 5.",
    "Kentang", "Ubi keledek", "Lobak merah", "Daging babi", "Daging babi murah.",
    "Murah.", "Daging lembu", "Daging lembu pun ada.", "Daging lembu mahal.", "Mahal.",
    "Daging lembu...", "Daging lembu... daripada daging babi...", "Daging lembu lebih mahal daripada daging babi.", "Sekarang bayar.", "Bayar.",
    "Imbas kod bar.", "Kod bar", "Bayar dengan kad.", "Resit", "Ambil resit.",
    "Dah masukkan ke dalam beg.", "Siap!", "Agak berat.", "Hari ini saya pergi ke pasar raya.", "Di pasar raya,",
    "saya beli snek.", "saya beli ramyeon juga.", "Anda semua beli apa di pasar raya?", "Tulis di ruangan komen!", "Jumpa lagi dalam video seterusnya!",
]

T["vi"] = [
    "Xin chào các bạn~", "Mình là Mino đây!", "Hôm nay mình đi siêu thị.", "Đi siêu thị.", "Mình sẽ đi bộ.",
    "Mình cùng đi nhé?", "Đến siêu thị rồi.", "Lấy xe đẩy.", "Vào siêu thị.", "Lên tầng 2.",
    "Đồ uống", "Có đồ uống.", "Đồ uống nhiều lắm.", "Nhiều lắm!", "Bia cũng nhiều lắm.",
    "Cũng có sữa.", "Kiểm tra hạn sử dụng.", "Kiểm tra.", "Đồ ăn vặt", "Có đồ ăn vặt.",
    "Có snack khoai tây.", "Mình thích gói snack này.", "Thích lắm.", "Chọn gói snack này.", "Chọn snack.",
    "Cũng có mì ramyeon.", "Mì ramyeon cũng nhiều lắm.", "Mì này cay.", "Cay!", "Mình thích mì này.",
    "Bỏ mì vào.", "Bỏ vào xe đẩy.", "Cũng có kimchi.", "Nếu ăn cùng nhau thì", "ngon lắm.",
    "Đậu phụ", "Đậu phụ đang giảm giá.", "Giảm giá!", "Có pizza.", "Cũng có mandu (bánh xếp).",
    "Có kem.", "Lạnh quá.", "Nên mình không ăn.", "Đi xuống.", "Có trái cây.",
    "Trái cây", "Lê có 3 quả.", "Có 3 quả.", "Táo có 5 quả.", "Có 5 quả.",
    "Khoai tây", "Khoai lang", "Cà rốt", "Thịt heo", "Thịt heo rẻ.",
    "Rẻ.", "Thịt bò", "Cũng có thịt bò.", "Thịt bò đắt.", "Đắt.",
    "Thịt bò...", "Thịt bò... so với thịt heo...", "Thịt bò đắt hơn thịt heo.", "Giờ thanh toán thôi.", "Thanh toán.",
    "Quét mã vạch.", "Mã vạch", "Thanh toán bằng thẻ.", "Hóa đơn", "Nhận hóa đơn.",
    "Đã bỏ vào túi rồi.", "Xong rồi!", "Hơi nặng.", "Hôm nay mình đã đi siêu thị.", "Ở siêu thị,",
    "mình đã mua snack.", "mình cũng mua mì ramyeon.", "Các bạn thường mua gì ở siêu thị?", "Hãy để lại bình luận nhé!", "Hẹn gặp lại ở video sau nhé!",
]


def main():
    assert len(KO) == len(set(KO)) == 80
    for lang, rows in T.items():
        assert len(rows) == len(KO), (lang, len(rows))
    src = open(SRC, encoding="utf-8").read().replace("\r\n", "\n").strip("\n")
    blocks = src.split("\n\n")
    idx = {k: i for i, k in enumerate(KO)}
    cues = []
    for b in blocks:
        time, text = b.split("\n", 1)
        assert re.match(r"^\d+:\d\d:\d\d\.\d{3},\d+:\d\d:\d\d\.\d{3}$", time), time
        key = text.strip()
        assert key in idx, f"번역표에 없는 문장: {key!r}"
        cues.append((time, idx[key]))
    for lang, rows in T.items():
        out = "\n\n".join(f"{time}\n{rows[i]}" for time, i in cues) + "\n"
        with open(os.path.join(HERE, f"captions.{lang}.sbv"), "w", encoding="utf-8", newline="\r\n") as f:  # 원본과 같은 CRLF
            f.write(out)
        print(f"{lang}: {len(cues)}줄")


if __name__ == "__main__":
    main()
