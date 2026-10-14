"""S002_captions.kr.sbv(한국어)를 13개 언어로 옮긴 .sbv 파일 생성.

타임코드·줄 구성은 원본 그대로 두고, 자막 문장만 언어별 번역으로 바꾼다.
번역은 문장 단위 표(KO 순서와 같은 순서)로 관리한다. 원본에 없는 문장이 있으면 에러.
실행: python make_captions.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "S002_captions.kr.sbv")

KO = [
    "안녕하세요, 여러분. 미노예요.", "저는 지금 우리 집 부엌에 있어요.", "배가 고파요", "그래서 밥을 먹을 거예요", "직접 요리해서 먹을 거예요",
    "요리해서 먹을 거예요", "그럼 한번 보시죠", "냉장고", "냉장고를 열어요", "계란을 하나 꺼내요",
    "파랑 양파도 필요해요", "파랑 양파를 꺼내요", "양파", "파", "냉장고를 닫아요",
    "이건 김치 냉장고예요", "김치 냉장고를 열어요", "김치를 꺼내요", "김치 냉장고를 닫아요", "김치예요",
    "김치를 꺼내서", "그릇에 담아요", "참치도 넣어 먹을 거예요", "밥솥이에요", "밥솥을 열어요",
    "밥솥 안에 밥이 있어요.", "주걱으로", "주걱으로 밥을 퍼요", "밥을 그릇에 담아요", "밥솥을 닫아요",
    "이 재료로 김치 볶음밥을 만들 거예요", "우선", "파를 썰어요", "양파도 썰어요", "가위",
    "집게", "김치는 집게로 집어요", "그리고 가위로 잘라요", "가위로 잘라요", "참치캔",
    "참치캔을 열어요", "후라이팬을 레인지 위에 올리고", "전원을 켜요", "불을 올려요", "불이 켜지면 빨간색으로 변해요",
    "파와 양파를 볶아줘요", "파와 양파를 다 볶았으면", "김치를 넣어요", "김치를 섞어요", "냄새가 좋아요",
    "참치도 넣어 줘요", "참치도 섞어 줘요", "밥을 넣어요", "그리고 밥을 섞어요", "밥을 섞어요",
    "소금", "소금을 뿌려 줘요", "후추", "후추도 넣어 줘요", "맛을 봐요",
    "조금 싱거워요", "소금을 더 뿌려요", "뜨거워요", "맛있어요.", "계란을 깨요",
    "계란을 넣어요", "계란을 뒤집개로", "뒤집어 줘요", "계란후라이를", "김치 볶음밥 위에 올려요",
    "숟가락으로 퍼서 먹어요", "퍼서 먹어요", "김치가 조금 매워요", "매워요", "물이 필요해요",
    "물을 따라요", "물을 마셔요", "깨끗하게 먹었어요", "오늘은 집에서 요리를 했어요", "여러분들은 집에서 어떤 요리를 해요?",
    "댓글에 남겨주세요", "감사합니다", "다음 영상에서 만나요",
]

T = {}

T["en"] = [
    "Hello, everyone. I'm Mino.", "I'm in the kitchen at my home right now.", "I'm hungry.", "So I'm going to eat.", "I'm going to cook it myself and eat.",
    "I'll cook and eat.", "Well then, let's take a look!", "Fridge", "I open the fridge.", "I take out one egg.",
    "I also need green onion and onion.", "I take out the green onion and onion.", "Onion", "Green onion", "I close the fridge.",
    "This is a kimchi fridge.", "I open the kimchi fridge.", "I take out the kimchi.", "I close the kimchi fridge.", "This is kimchi.",
    "I take out the kimchi and", "put it in a bowl.", "I'm going to add tuna, too.", "This is the rice cooker.", "I open the rice cooker.",
    "There's rice inside the rice cooker.", "With the rice paddle...", "I scoop the rice with the rice paddle.", "I put the rice in a bowl.", "I close the rice cooker.",
    "With these ingredients, I'll make kimchi fried rice.", "First,", "I slice the green onion.", "I slice the onion, too.", "Scissors",
    "Tongs", "I pick up the kimchi with tongs.", "And I cut it with scissors.", "I cut it with scissors.", "Can of tuna",
    "I open the can of tuna.", "I put the frying pan on the stove and", "turn on the power.", "I turn up the heat.", "When the heat comes on, it turns red.",
    "I stir-fry the green onion and onion.", "Once the green onion and onion are stir-fried,", "I add the kimchi.", "I mix in the kimchi.", "It smells good!",
    "I add the tuna, too.", "I mix in the tuna, too.", "I add the rice.", "And I mix in the rice.", "I mix in the rice.",
    "Salt", "I sprinkle some salt.", "Pepper", "I add pepper, too.", "I taste it.",
    "It's a little bland.", "I sprinkle more salt.", "Hot!", "Delicious.", "I crack the egg.",
    "I put the egg in.", "With the spatula, the egg...", "I flip it over.", "The fried egg...", "I put it on top of the kimchi fried rice.",
    "I scoop it with a spoon and eat.", "Scoop and eat.", "The kimchi is a little spicy.", "Spicy!", "I need water.",
    "I pour water.", "I drink water.", "I ate every last bite!", "Today I cooked at home.", "What do you cook at home?",
    "Leave it in the comments!", "Thank you!", "See you in the next video!",
]

T["zh-Hans"] = [
    "大家好，我是米诺。", "我现在在我家的厨房。", "我饿了。", "所以我要吃饭。", "我要自己做饭吃。",
    "做饭来吃。", "那我们来看看吧！", "冰箱", "打开冰箱。", "拿出一个鸡蛋。",
    "还需要葱和洋葱。", "拿出葱和洋葱。", "洋葱", "葱", "关上冰箱。",
    "这是泡菜冰箱。", "打开泡菜冰箱。", "拿出泡菜。", "关上泡菜冰箱。", "这是泡菜。",
    "把泡菜拿出来，", "装进碗里。", "还要加金枪鱼一起吃。", "这是电饭锅。", "打开电饭锅。",
    "电饭锅里有米饭。", "用饭勺……", "用饭勺盛饭。", "把饭装进碗里。", "关上电饭锅。",
    "用这些材料做泡菜炒饭。", "首先，", "切葱。", "洋葱也切一下。", "剪刀",
    "夹子", "泡菜用夹子夹起来，", "然后用剪刀剪。", "用剪刀剪。", "金枪鱼罐头",
    "打开金枪鱼罐头。", "把平底锅放在炉子上，", "打开电源。", "把火调大。", "火一开就会变成红色。",
    "炒葱和洋葱。", "葱和洋葱炒好以后，", "放入泡菜。", "把泡菜拌一拌。", "好香啊！",
    "金枪鱼也放进去。", "金枪鱼也拌一拌。", "放入米饭。", "然后把饭拌一拌。", "把饭拌一拌。",
    "盐", "撒点盐。", "胡椒", "胡椒也放一点。", "尝一尝味道。",
    "有点淡。", "再撒点盐。", "好烫！", "好吃。", "打鸡蛋。",
    "放入鸡蛋。", "用锅铲把鸡蛋……", "翻过来。", "把煎蛋……", "放在泡菜炒饭上面。",
    "用勺子舀着吃。", "舀着吃。", "泡菜有点辣。", "好辣！", "需要水。",
    "倒水。", "喝水。", "吃得干干净净！", "今天在家做了饭。", "大家在家都做什么菜呢？",
    "请在评论区留言！", "谢谢！", "下个视频见！",
]

T["id"] = [
    "Halo, semuanya. Aku Mino.", "Sekarang aku ada di dapur rumahku.", "Aku lapar.", "Jadi aku mau makan.", "Aku mau masak sendiri lalu makan.",
    "Masak dulu, lalu makan.", "Kalau begitu, ayo kita lihat!", "Kulkas", "Aku buka kulkas.", "Aku ambil satu telur.",
    "Aku juga butuh daun bawang dan bawang bombai.", "Aku ambil daun bawang dan bawang bombai.", "Bawang bombai", "Daun bawang", "Aku tutup kulkas.",
    "Ini kulkas kimchi.", "Aku buka kulkas kimchi.", "Aku ambil kimchi.", "Aku tutup kulkas kimchi.", "Ini kimchi.",
    "Aku ambil kimchi, lalu", "kutaruh di mangkuk.", "Aku juga mau tambah tuna.", "Ini rice cooker.", "Aku buka rice cooker.",
    "Di dalam rice cooker ada nasi.", "Pakai centong nasi...", "Aku ambil nasi pakai centong.", "Aku taruh nasi di mangkuk.", "Aku tutup rice cooker.",
    "Dengan bahan-bahan ini, aku mau bikin nasi goreng kimchi.", "Pertama,", "Aku iris daun bawang.", "Bawang bombai juga kuiris.", "Gunting",
    "Penjepit", "Kimchi kujepit pakai penjepit.", "Lalu kugunting.", "Kugunting pakai gunting.", "Tuna kaleng",
    "Aku buka tuna kaleng.", "Aku taruh wajan di atas kompor, lalu", "nyalakan kompornya.", "Aku besarkan apinya.", "Kalau sudah menyala, warnanya jadi merah.",
    "Aku tumis daun bawang dan bawang bombai.", "Kalau daun bawang dan bawang bombai sudah matang,", "aku masukkan kimchi.", "Aku aduk kimchinya.", "Baunya enak!",
    "Tuna juga dimasukkan.", "Tunanya juga diaduk.", "Aku masukkan nasi.", "Lalu nasinya diaduk.", "Nasinya diaduk.",
    "Garam", "Aku taburi garam.", "Merica", "Merica juga dimasukkan.", "Aku cicipi.",
    "Agak hambar.", "Aku tambah garam lagi.", "Panas!", "Enak.", "Aku pecahkan telur.",
    "Aku masukkan telur.", "Telurnya, pakai spatula...", "kubalik.", "Telur ceploknya...", "kutaruh di atas nasi goreng kimchi.",
    "Aku sendok lalu makan.", "Sendok, lalu makan.", "Kimchinya agak pedas.", "Pedas!", "Aku butuh air.",
    "Aku tuang air.", "Aku minum air.", "Habis sampai bersih!", "Hari ini aku masak di rumah.", "Kalian biasanya masak apa di rumah?",
    "Tulis di kolom komentar ya!", "Terima kasih!", "Sampai jumpa di video berikutnya!",
]

T["pt-BR"] = [
    "Oi, pessoal. Aqui é Mino!", "Agora estou na cozinha da minha casa.", "Estou com fome.", "Então vou comer.", "Vou cozinhar por conta própria e comer.",
    "Vou cozinhar e comer.", "Então vamos dar uma olhada!", "Geladeira", "Abro a geladeira.", "Pego um ovo.",
    "Também preciso de cebolinha e cebola.", "Pego a cebolinha e a cebola.", "Cebola", "Cebolinha", "Fecho a geladeira.",
    "Esta é a geladeira de kimchi.", "Abro a geladeira de kimchi.", "Pego o kimchi.", "Fecho a geladeira de kimchi.", "Isto é kimchi.",
    "Pego o kimchi e", "coloco numa tigela.", "Também vou colocar atum.", "Esta é a panela de arroz.", "Abro a panela de arroz.",
    "Tem arroz dentro da panela de arroz.", "Com a colher de arroz...", "Pego o arroz com a colher de arroz.", "Coloco o arroz na tigela.", "Fecho a panela de arroz.",
    "Com estes ingredientes, vou fazer arroz frito com kimchi.", "Primeiro,", "Corto a cebolinha.", "Corto a cebola também.", "Tesoura",
    "Pegador", "Pego o kimchi com o pegador.", "E corto com a tesoura.", "Corto com a tesoura.", "Lata de atum",
    "Abro a lata de atum.", "Coloco a frigideira no fogão e", "ligo o fogão.", "Aumento o fogo.", "Quando liga, ele fica vermelho.",
    "Refogo a cebolinha e a cebola.", "Quando a cebolinha e a cebola estiverem refogadas,", "coloco o kimchi.", "Misturo o kimchi.", "Que cheiro bom!",
    "Coloco o atum também.", "Misturo o atum também.", "Coloco o arroz.", "E misturo o arroz.", "Misturo o arroz.",
    "Sal", "Polvilho sal.", "Pimenta-do-reino", "Coloco pimenta-do-reino também.", "Experimento.",
    "Está um pouco sem sal.", "Coloco mais sal.", "Está quente!", "Delicioso.", "Quebro o ovo.",
    "Coloco o ovo.", "Com a espátula, o ovo...", "eu viro.", "O ovo frito...", "coloco em cima do arroz frito com kimchi.",
    "Pego com a colher e como.", "Pego e como.", "O kimchi está um pouco apimentado.", "Apimentado!", "Preciso de água.",
    "Coloco água no copo.", "Bebo água.", "Comi tudinho!", "Hoje cozinhei em casa.", "E vocês, o que cozinham em casa?",
    "Deixem nos comentários!", "Valeu, pessoal!", "Até o próximo vídeo!",
]

T["fil"] = [
    "Hello, everyone. Ako si Mino.", "Nandito ako ngayon sa kusina ng bahay namin.", "Gutom na ako.", "Kaya kakain ako.", "Magluluto ako mismo at kakain.",
    "Magluluto ako at kakain.", "O sige, tingnan natin!", "Ref", "Binubuksan ko ang ref.", "Kumukuha ako ng isang itlog.",
    "Kailangan ko rin ng dahon ng sibuyas at sibuyas.", "Kinukuha ko ang dahon ng sibuyas at sibuyas.", "Sibuyas", "Dahon ng sibuyas", "Isinasara ko ang ref.",
    "Ito ang kimchi ref.", "Binubuksan ko ang kimchi ref.", "Kinukuha ko ang kimchi.", "Isinasara ko ang kimchi ref.", "Ito ang kimchi.",
    "Kinukuha ko ang kimchi at", "inilalagay sa mangkok.", "Lalagyan ko rin ng tuna.", "Ito ang rice cooker.", "Binubuksan ko ang rice cooker.",
    "May kanin sa loob ng rice cooker.", "Gamit ang sandok ng kanin...", "Sumasandok ako ng kanin gamit ang sandok.", "Inilalagay ko ang kanin sa mangkok.", "Isinasara ko ang rice cooker.",
    "Gagawa ako ng kimchi fried rice gamit ang mga sangkap na ito.", "Una,", "Hinihiwa ko ang dahon ng sibuyas.", "Hinihiwa ko rin ang sibuyas.", "Gunting",
    "Sipit", "Sinisipit ko ang kimchi.", "At ginugupit ko ng gunting.", "Ginugupit ko ng gunting.", "De-latang tuna",
    "Binubuksan ko ang de-latang tuna.", "Ipinapatong ko ang kawali sa kalan at", "binubuksan ang kalan.", "Nilalakasan ko ang apoy.", "Kapag bukas na, nagiging pula ito.",
    "Iginigisa ko ang dahon ng sibuyas at sibuyas.", "Kapag luto na ang dahon ng sibuyas at sibuyas,", "inilalagay ko ang kimchi.", "Hinahalo ko ang kimchi.", "Ang bango!",
    "Inilalagay ko rin ang tuna.", "Hinahalo ko rin ang tuna.", "Inilalagay ko ang kanin.", "At hinahalo ko ang kanin.", "Hinahalo ko ang kanin.",
    "Asin", "Binubudburan ko ng asin.", "Paminta", "Nilalagyan ko rin ng paminta.", "Tinitikman ko.",
    "Medyo matabang.", "Dinadagdagan ko pa ng asin.", "Mainit!", "Masarap.", "Binabasag ko ang itlog.",
    "Inilalagay ko ang itlog.", "Gamit ang siyanse, ang itlog...", "binabaligtad ko.", "Ang pritong itlog...", "ipinapatong ko sa ibabaw ng kimchi fried rice.",
    "Sumasandok ako gamit ang kutsara at kumakain.", "Sandok, tapos kain.", "Medyo maanghang ang kimchi.", "Maanghang!", "Kailangan ko ng tubig.",
    "Nagsasalin ako ng tubig.", "Umiinom ako ng tubig.", "Naubos ko lahat!", "Nagluto ako sa bahay ngayon.", "Kayo, ano'ng niluluto ninyo sa bahay?",
    "Isulat ninyo sa comments!", "Salamat!", "Kita-kits sa susunod na video!",
]

T["ru"] = [
    "Всем привет! С вами Мино.", "Сейчас я на кухне у себя дома.", "Так хочется есть!", "Поэтому сейчас будем есть.", "Приготовим сами и поедим.",
    "Приготовим и поедим.", "Ну что, давайте посмотрим!", "Холодильник", "Открываю холодильник.", "Достаю одно яйцо.",
    "Ещё нужны зелёный лук и репчатый лук.", "Достаю зелёный лук и репчатый лук.", "Репчатый лук", "Зелёный лук", "Закрываю холодильник.",
    "Это холодильник для кимчи.", "Открываю холодильник для кимчи.", "Достаю кимчи.", "Закрываю холодильник для кимчи.", "Это кимчи.",
    "Достаю кимчи и", "кладу в миску.", "Ещё добавим тунец.", "Это рисоварка.", "Открываю рисоварку.",
    "В рисоварке есть рис.", "Лопаткой для риса...", "Накладываю рис лопаткой.", "Кладу рис в миску.", "Закрываю рисоварку.",
    "Из этих продуктов приготовим жареный рис с кимчи.", "Сначала", "Режу зелёный лук.", "Репчатый лук тоже режу.", "Ножницы",
    "Щипцы", "Кимчи беру щипцами.", "И режу ножницами.", "Режу ножницами.", "Банка тунца",
    "Открываю банку тунца.", "Ставлю сковороду на плиту и", "включаю плиту.", "Делаю огонь посильнее.", "Когда плита включается, она становится красной.",
    "Обжариваю зелёный и репчатый лук.", "Когда лук обжарился,", "добавляю кимчи.", "Перемешиваю кимчи.", "Как вкусно пахнет!",
    "Добавляю и тунец.", "Тунец тоже перемешиваю.", "Добавляю рис.", "И перемешиваю рис.", "Перемешиваю рис.",
    "Соль", "Посыпаю солью.", "Перец", "Добавляю и перец.", "Пробую на вкус.",
    "Немного пресно.", "Досаливаю ещё.", "Горячо!", "Вкусно.", "Разбиваю яйцо.",
    "Кладу яйцо.", "Яйцо лопаткой...", "переворачиваю.", "Яичницу...", "кладу сверху на жареный рис с кимчи.",
    "Набираю ложкой и ем.", "Набираю и ем.", "Кимчи немного острое.", "Остро!", "Нужна вода.",
    "Наливаю воду.", "Пью воду.", "Всё съедено подчистую!", "Сегодня мы готовили дома.", "А что вы готовите дома?",
    "Напишите в комментариях!", "Спасибо!", "До встречи в следующем видео!",
]

T["es"] = [
    "¡Hola a todos! Soy Mino.", "Ahora estoy en la cocina de mi casa.", "Tengo hambre.", "Así que voy a comer.", "Voy a cocinar yo y luego a comer.",
    "Voy a cocinar y a comer.", "Bueno, ¡vamos a ver!", "Refrigerador", "Abro el refrigerador.", "Saco un huevo.",
    "También necesito cebolleta y cebolla.", "Saco la cebolleta y la cebolla.", "Cebolla", "Cebolleta", "Cierro el refrigerador.",
    "Este es un refrigerador para kimchi.", "Abro el refrigerador para kimchi.", "Saco el kimchi.", "Cierro el refrigerador para kimchi.", "Esto es kimchi.",
    "Saco el kimchi y", "lo pongo en un tazón.", "También le voy a poner atún.", "Esta es la olla arrocera.", "Abro la olla arrocera.",
    "Dentro de la olla arrocera hay arroz.", "Con la pala para arroz...", "Sirvo el arroz con la pala.", "Pongo el arroz en un tazón.", "Cierro la olla arrocera.",
    "Con estos ingredientes voy a hacer arroz frito con kimchi.", "Primero,", "Corto la cebolleta.", "También corto la cebolla.", "Tijeras",
    "Pinzas", "El kimchi lo agarro con las pinzas.", "Y lo corto con las tijeras.", "Lo corto con las tijeras.", "Lata de atún",
    "Abro la lata de atún.", "Pongo la sartén sobre la estufa y", "la enciendo.", "Subo el fuego.", "Cuando se enciende, se pone roja.",
    "Sofrío la cebolleta y la cebolla.", "Cuando la cebolleta y la cebolla estén listas,", "pongo el kimchi.", "Mezclo el kimchi.", "¡Qué bien huele!",
    "Pongo también el atún.", "Mezclo también el atún.", "Pongo el arroz.", "Y mezclo el arroz.", "Mezclo el arroz.",
    "Sal", "Le echo sal.", "Pimienta", "Le pongo pimienta también.", "Lo pruebo.",
    "Está un poco soso.", "Le echo más sal.", "¡Está caliente!", "Está rico.", "Rompo el huevo.",
    "Pongo el huevo.", "Con la espátula, el huevo...", "le doy la vuelta.", "El huevo frito...", "lo pongo encima del arroz frito con kimchi.",
    "Lo tomo con la cuchara y como.", "Tomo y como.", "El kimchi está un poco picante.", "¡Pica!", "Necesito agua.",
    "Sirvo agua.", "Bebo agua.", "¡Me lo comí todo!", "Hoy cociné en casa.", "Y ustedes, ¿qué cocinan en casa?",
    "¡Déjenlo en los comentarios!", "¡Gracias!", "¡Nos vemos en el próximo video!",
]

T["fr"] = [
    "Bonjour à tous. Ici Mino !", "Je suis dans la cuisine de chez moi.", "J'ai faim.", "Alors, je vais manger.", "Je vais cuisiner moi-même et manger.",
    "Je vais cuisiner et manger.", "Allez, on regarde !", "Frigo", "J'ouvre le frigo.", "Je sors un œuf.",
    "Il me faut aussi de la ciboule et un oignon.", "Je sors la ciboule et l'oignon.", "Oignon", "Ciboule", "Je ferme le frigo.",
    "Ça, c'est un frigo à kimchi.", "J'ouvre le frigo à kimchi.", "Je sors le kimchi.", "Je ferme le frigo à kimchi.", "Voici le kimchi.",
    "Je sors le kimchi et", "je le mets dans un bol.", "Je vais aussi ajouter du thon.", "Voici le cuiseur à riz.", "J'ouvre le cuiseur à riz.",
    "Il y a du riz dans le cuiseur.", "Avec la spatule à riz...", "Je prends du riz avec la spatule.", "Je mets le riz dans un bol.", "Je ferme le cuiseur à riz.",
    "Avec ces ingrédients, je vais faire du riz sauté au kimchi.", "D'abord,", "Je coupe la ciboule.", "Je coupe aussi l'oignon.", "Ciseaux",
    "Pince", "Je prends le kimchi avec la pince.", "Et je le coupe aux ciseaux.", "Je le coupe aux ciseaux.", "Boîte de thon",
    "J'ouvre la boîte de thon.", "Je pose la poêle sur la plaque et", "j'allume la plaque.", "J'augmente le feu.", "Quand elle chauffe, elle devient rouge.",
    "Je fais revenir la ciboule et l'oignon.", "Une fois la ciboule et l'oignon bien revenus,", "j'ajoute le kimchi.", "Je mélange le kimchi.", "Ça sent bon !",
    "J'ajoute aussi le thon.", "Je mélange aussi le thon.", "J'ajoute le riz.", "Et je mélange le riz.", "Je mélange le riz.",
    "Sel", "Je saupoudre de sel.", "Poivre", "J'ajoute aussi du poivre.", "Je goûte.",
    "C'est un peu fade.", "Je rajoute du sel.", "C'est chaud !", "C'est bon.", "Je casse l'œuf.",
    "Je mets l'œuf.", "Avec la spatule, l'œuf...", "je le retourne.", "L'œuf au plat...", "je le pose sur le riz sauté au kimchi.",
    "Je prends une cuillerée et je mange.", "Une cuillerée, et je mange.", "Le kimchi est un peu épicé.", "Ça pique !", "Il me faut de l'eau.",
    "Je verse de l'eau.", "Je bois de l'eau.", "J'ai tout mangé !", "Aujourd'hui, j'ai cuisiné à la maison.", "Et vous, qu'est-ce que vous cuisinez à la maison ?",
    "Dites-le en commentaire !", "Merci !", "À la prochaine vidéo !",
]

T["de"] = [
    "Hallo zusammen! Hier ist Mino!", "Ich bin gerade in der Küche bei mir zu Hause.", "Ich habe Hunger.", "Also werde ich etwas essen.", "Ich koche selbst und esse dann.",
    "Ich koche und esse.", "Na dann, schauen wir mal!", "Kühlschrank", "Ich öffne den Kühlschrank.", "Ich nehme ein Ei heraus.",
    "Ich brauche auch Frühlingszwiebeln und eine Zwiebel.", "Ich nehme Frühlingszwiebeln und Zwiebel heraus.", "Zwiebel", "Frühlingszwiebel", "Ich schließe den Kühlschrank.",
    "Das ist ein Kimchi-Kühlschrank.", "Ich öffne den Kimchi-Kühlschrank.", "Ich nehme das Kimchi heraus.", "Ich schließe den Kimchi-Kühlschrank.", "Das ist Kimchi.",
    "Ich nehme das Kimchi heraus und", "gebe es in eine Schüssel.", "Ich gebe auch Thunfisch dazu.", "Das ist der Reiskocher.", "Ich öffne den Reiskocher.",
    "Im Reiskocher ist Reis.", "Mit dem Reislöffel...", "Ich schöpfe den Reis mit dem Reislöffel.", "Ich gebe den Reis in eine Schüssel.", "Ich schließe den Reiskocher.",
    "Mit diesen Zutaten mache ich Kimchi-Bratreis.", "Zuerst:", "Ich schneide die Frühlingszwiebeln.", "Ich schneide auch die Zwiebel.", "Schere",
    "Zange", "Das Kimchi nehme ich mit der Zange.", "Und schneide es mit der Schere.", "Ich schneide es mit der Schere.", "Thunfischdose",
    "Ich öffne die Thunfischdose.", "Ich stelle die Pfanne auf den Herd und", "schalte ihn ein.", "Ich drehe die Hitze hoch.", "Wenn er an ist, wird er rot.",
    "Ich brate Frühlingszwiebeln und Zwiebel an.", "Wenn Frühlingszwiebeln und Zwiebel angebraten sind,", "gebe ich das Kimchi dazu.", "Ich mische das Kimchi unter.", "Das riecht gut!",
    "Ich gebe auch den Thunfisch dazu.", "Ich mische auch den Thunfisch unter.", "Ich gebe den Reis dazu.", "Und mische den Reis unter.", "Ich mische den Reis unter.",
    "Salz", "Ich streue Salz darüber.", "Pfeffer", "Ich gebe auch Pfeffer dazu.", "Ich probiere.",
    "Ein bisschen fade.", "Ich streue noch mehr Salz darüber.", "Heiß!", "Lecker.", "Ich schlage das Ei auf.",
    "Ich gebe das Ei hinein.", "Mit dem Pfannenwender das Ei...", "wende ich.", "Das Spiegelei...", "lege ich auf den Kimchi-Bratreis.",
    "Ich nehme einen Löffel voll und esse.", "Löffel voll und essen.", "Das Kimchi ist ein bisschen scharf.", "Scharf!", "Ich brauche Wasser.",
    "Ich gieße Wasser ein.", "Ich trinke Wasser.", "Alles aufgegessen!", "Heute habe ich zu Hause gekocht.", "Was kocht ihr so zu Hause?",
    "Schreibt es in die Kommentare!", "Danke!", "Bis zum nächsten Video!",
]

T["ar"] = [
    "مرحبًا بالجميع، أنا مينو.", "أنا الآن في مطبخ بيتي.", "أشعر بالجوع.", "لذلك سآكل.", "سأطبخ بنفسي ثم آكل.",
    "سأطبخ وآكل.", "حسنًا، لنلقِ نظرة!", "الثلاجة", "أفتح الثلاجة.", "أُخرج بيضة واحدة.",
    "أحتاج أيضًا إلى البصل الأخضر والبصل.", "أُخرج البصل الأخضر والبصل.", "بصل", "بصل أخضر", "أغلق الثلاجة.",
    "هذه ثلاجة الكيمتشي.", "أفتح ثلاجة الكيمتشي.", "أُخرج الكيمتشي.", "أغلق ثلاجة الكيمتشي.", "هذا كيمتشي.",
    "أُخرج الكيمتشي و", "أضعه في وعاء.", "سأضيف التونة أيضًا.", "هذه طنجرة الأرز.", "أفتح طنجرة الأرز.",
    "يوجد أرز داخل طنجرة الأرز.", "بمغرفة الأرز...", "أغرف الأرز بالمغرفة.", "أضع الأرز في الوعاء.", "أغلق طنجرة الأرز.",
    "بهذه المكونات سأعدّ أرزًا مقليًا بالكيمتشي.", "أولًا،", "أقطّع البصل الأخضر.", "وأقطّع البصل أيضًا.", "مقص",
    "ملقط", "آخذ الكيمتشي بالملقط.", "ثم أقصّه بالمقص.", "أقصّه بالمقص.", "علبة تونة",
    "أفتح علبة التونة.", "أضع المقلاة على الموقد و", "أشغّل الموقد.", "أرفع الحرارة.", "عندما يشتغل يصبح أحمر.",
    "أقلّب البصل الأخضر والبصل على النار.", "عندما ينضج البصل الأخضر والبصل،", "أضيف الكيمتشي.", "أخلط الكيمتشي.", "الرائحة طيبة!",
    "أضيف التونة أيضًا.", "وأخلط التونة أيضًا.", "أضيف الأرز.", "ثم أخلط الأرز.", "أخلط الأرز.",
    "ملح", "أرشّ الملح.", "فلفل أسود", "وأضيف الفلفل الأسود أيضًا.", "أتذوّقه.",
    "ينقصه قليل من الملح.", "أرشّ مزيدًا من الملح.", "ساخن!", "لذيذ.", "أكسر البيضة.",
    "أضع البيضة.", "البيضة، بالملعقة المسطحة...", "أقلبها.", "البيضة المقلية...", "أضعها فوق الأرز المقلي بالكيمتشي.",
    "أغرف بالملعقة وآكل.", "أغرف وآكل.", "الكيمتشي حار قليلًا.", "حار!", "أحتاج إلى الماء.",
    "أصبّ الماء.", "أشرب الماء.", "أكلت كل شيء!", "اليوم طبخت في البيت.", "وأنتم، ماذا تطبخون في البيت؟",
    "اكتبوا لنا في التعليقات!", "شكرًا لكم!", "نلتقي في الفيديو القادم!",
]

T["ja"] = [
    "みなさん、こんにちは。ミノです。", "今、うちの台所にいます。", "お腹がすきました。", "だから、ご飯を食べます。", "自分で料理して食べます。",
    "料理して食べます。", "では、見てみましょう！", "冷蔵庫", "冷蔵庫を開けます。", "卵を一つ出します。",
    "ネギと玉ねぎも必要です。", "ネギと玉ねぎを出します。", "玉ねぎ", "ネギ", "冷蔵庫を閉めます。",
    "これはキムチ冷蔵庫です。", "キムチ冷蔵庫を開けます。", "キムチを出します。", "キムチ冷蔵庫を閉めます。", "キムチです。",
    "キムチを出して、", "お皿に入れます。", "ツナも入れて食べます。", "炊飯器です。", "炊飯器を開けます。",
    "炊飯器の中にご飯があります。", "しゃもじで…", "しゃもじでご飯をよそいます。", "ご飯をお皿に入れます。", "炊飯器を閉めます。",
    "この材料でキムチチャーハンを作ります。", "まず、", "ネギを切ります。", "玉ねぎも切ります。", "はさみ",
    "トング", "キムチはトングでつかみます。", "そして、はさみで切ります。", "はさみで切ります。", "ツナ缶",
    "ツナ缶を開けます。", "フライパンをコンロの上に置いて、", "電源を入れます。", "火を強くします。", "火がつくと赤くなります。",
    "ネギと玉ねぎを炒めます。", "ネギと玉ねぎが炒まったら、", "キムチを入れます。", "キムチを混ぜます。", "いい匂いです！",
    "ツナも入れます。", "ツナも混ぜます。", "ご飯を入れます。", "そして、ご飯を混ぜます。", "ご飯を混ぜます。",
    "塩", "塩をふります。", "こしょう", "こしょうも入れます。", "味見をします。",
    "ちょっと薄いです。", "塩をもう少しふります。", "熱いです！", "おいしいです。", "卵を割ります。",
    "卵を入れます。", "卵をフライ返しで…", "ひっくり返します。", "目玉焼きを…", "キムチチャーハンの上にのせます。",
    "スプーンですくって食べます。", "すくって食べます。", "キムチがちょっと辛いです。", "辛いです！", "水が必要です。",
    "水を注ぎます。", "水を飲みます。", "きれいに食べました！", "今日は家で料理をしました。", "みなさんは家でどんな料理をしますか？",
    "コメントで教えてください！", "ありがとうございました！", "次の動画で会いましょう！",
]

T["ms"] = [
    "Hai semua. Saya Mino.", "Sekarang saya di dapur rumah saya.", "Saya lapar.", "Jadi saya nak makan.", "Saya nak masak sendiri dan makan.",
    "Masak, kemudian makan.", "Jom kita tengok!", "Peti sejuk", "Saya buka peti sejuk.", "Saya keluarkan sebiji telur.",
    "Saya juga perlukan daun bawang dan bawang besar.", "Saya keluarkan daun bawang dan bawang besar.", "Bawang besar", "Daun bawang", "Saya tutup peti sejuk.",
    "Ini peti sejuk kimchi.", "Saya buka peti sejuk kimchi.", "Saya keluarkan kimchi.", "Saya tutup peti sejuk kimchi.", "Ini kimchi.",
    "Saya keluarkan kimchi dan", "masukkan ke dalam mangkuk.", "Saya nak tambah tuna juga.", "Ini periuk nasi.", "Saya buka periuk nasi.",
    "Ada nasi di dalam periuk nasi.", "Dengan senduk nasi...", "Saya cedok nasi dengan senduk nasi.", "Saya letak nasi dalam mangkuk.", "Saya tutup periuk nasi.",
    "Dengan bahan-bahan ini, saya akan buat nasi goreng kimchi.", "Mula-mula,", "Saya hiris daun bawang.", "Bawang besar pun saya hiris.", "Gunting",
    "Penyepit", "Kimchi saya sepit dengan penyepit.", "Kemudian saya gunting.", "Saya gunting dengan gunting.", "Tin tuna",
    "Saya buka tin tuna.", "Saya letak kuali di atas dapur dan", "hidupkan suisnya.", "Saya besarkan api.", "Bila dah hidup, warnanya jadi merah.",
    "Saya tumis daun bawang dan bawang besar.", "Bila daun bawang dan bawang besar dah layu,", "saya masukkan kimchi.", "Saya gaul kimchi.", "Baunya sedap!",
    "Saya masukkan tuna juga.", "Tuna pun saya gaul.", "Saya masukkan nasi.", "Kemudian saya gaul nasi.", "Saya gaul nasi.",
    "Garam", "Saya tabur garam.", "Lada hitam", "Saya masukkan lada hitam juga.", "Saya rasa.",
    "Tawar sikit.", "Saya tabur garam lagi.", "Panas!", "Sedap.", "Saya pecahkan telur.",
    "Saya masukkan telur.", "Telur, dengan sudip...", "saya terbalikkan.", "Telur mata kerbau...", "saya letak di atas nasi goreng kimchi.",
    "Saya cedok dengan sudu dan makan.", "Cedok, kemudian makan.", "Kimchi ni pedas sikit.", "Pedas!", "Saya perlukan air.",
    "Saya tuang air.", "Saya minum air.", "Licin pinggan!", "Hari ini saya masak di rumah.", "Kamu semua selalu masak apa di rumah?",
    "Tulis di ruangan komen ya!", "Terima kasih!", "Jumpa lagi dalam video seterusnya!",
]

T["vi"] = [
    "Xin chào mọi người. Mình là Mino đây!", "Bây giờ mình đang ở bếp nhà mình.", "Mình đói bụng.", "Vì vậy mình sẽ ăn cơm.", "Mình sẽ tự nấu rồi ăn.",
    "Nấu rồi ăn.", "Vậy thì mình cùng xem nhé!", "Tủ lạnh", "Mình mở tủ lạnh.", "Mình lấy ra một quả trứng.",
    "Mình cũng cần hành lá và hành tây.", "Mình lấy hành lá và hành tây ra.", "Hành tây", "Hành lá", "Mình đóng tủ lạnh.",
    "Đây là tủ lạnh kim chi.", "Mình mở tủ lạnh kim chi.", "Mình lấy kim chi ra.", "Mình đóng tủ lạnh kim chi.", "Đây là kim chi.",
    "Mình lấy kim chi ra rồi", "cho vào bát.", "Mình sẽ cho thêm cá ngừ nữa.", "Đây là nồi cơm điện.", "Mình mở nồi cơm điện.",
    "Trong nồi cơm điện có cơm.", "Bằng muôi cơm...", "Mình xới cơm bằng muôi.", "Mình cho cơm vào bát.", "Mình đóng nồi cơm điện.",
    "Với những nguyên liệu này, mình sẽ làm cơm chiên kim chi.", "Trước tiên,", "Mình thái hành lá.", "Mình thái cả hành tây nữa.", "Kéo",
    "Kẹp gắp", "Kim chi thì mình gắp bằng kẹp.", "Rồi cắt bằng kéo.", "Cắt bằng kéo.", "Cá ngừ hộp",
    "Mình mở hộp cá ngừ.", "Mình đặt chảo lên bếp rồi", "bật nguồn.", "Mình tăng lửa.", "Khi bếp bật lên, nó chuyển sang màu đỏ.",
    "Mình xào hành lá và hành tây.", "Khi hành lá và hành tây đã xào xong,", "mình cho kim chi vào.", "Mình đảo đều kim chi.", "Thơm quá!",
    "Mình cho cả cá ngừ vào.", "Đảo đều cả cá ngừ.", "Mình cho cơm vào.", "Rồi đảo đều cơm.", "Đảo đều cơm.",
    "Muối", "Mình rắc muối.", "Hạt tiêu", "Cho thêm cả hạt tiêu.", "Mình nếm thử.",
    "Hơi nhạt.", "Mình rắc thêm muối.", "Nóng quá!", "Ngon quá.", "Mình đập trứng.",
    "Mình cho trứng vào.", "Trứng, bằng xẻng lật...", "mình lật lại.", "Trứng ốp la...", "mình đặt lên trên cơm chiên kim chi.",
    "Mình xúc bằng thìa rồi ăn.", "Xúc rồi ăn.", "Kim chi hơi cay.", "Cay quá!", "Mình cần nước.",
    "Mình rót nước.", "Mình uống nước.", "Ăn sạch sành sanh rồi!", "Hôm nay mình đã nấu ăn ở nhà.", "Mọi người thường nấu món gì ở nhà?",
    "Hãy để lại bình luận nhé!", "Cảm ơn mọi người!", "Hẹn gặp lại ở video sau nhé!",
]


def main():
    assert len(KO) == len(set(KO)) == 83
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
        with open(os.path.join(HERE, f"S002_captions.{lang}.sbv"), "w", encoding="utf-8", newline="\r\n") as f:  # 원본과 같은 CRLF
            f.write(out)
        print(f"{lang}: {len(cues)}줄")


if __name__ == "__main__":
    main()
