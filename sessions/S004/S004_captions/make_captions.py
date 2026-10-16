"""S004_captions.kr.sbv(한국어)를 13개 언어로 옮긴 .sbv 파일 생성.

타임코드·줄 구성은 원본 그대로 두고, 자막 문장만 언어별 번역으로 바꾼다.
번역은 문장 단위 표(KO 순서와 같은 순서)로 관리한다. 원본에 없는 문장이 있으면 에러.
실행: python make_captions.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "S004_captions.kr.sbv")

KO = [
    "안녕하세요 여러분! 미노예요", "오늘은 제가 아침에 어떻게 씻고 준비하는지", "말해볼게요", "그럼 한 번 보시죠", "화장실 불을 켜요",
    "화장실로 들어가요", "세면대", "세면대가 있어요", "이건 비누예요", "비누",
    "비누는 손을 닦을 때 써요", "이건 핸드워시예요", "핸드워시는 액체 비누예요", "핸드워시도 손을 닦을 때 써요", "수도꼭지를 틀어요",
    "수도꼭지를 틀면 물이 나와요", "물이 나와요", "수도꼭지를 돌려요", "수도꼭지를 왼쪽으로 돌리면", "따뜻한 물이 나와요",
    "손을 닦아요", "비누를 손으로 비벼요", "손을 비벼서 거품을 내요", "거품을 내요", "물로 손을 헹궈요",
    "손에서 물을 털어요", "손을 털어요", "세수를 해요", "뚜껑을 열어요", "클렌저를 짜요",
    "뚜껑을 닫아요", "얼굴에 거품을 묻혀요", "거품을 묻혀요", "골고루 묻혀요", "다시 물을 틀고",
    "얼굴을 씻어요", "수건", "수건으로 얼굴을 닦아요", "얼굴을 닦아요", "수건을 쓰고 나면",
    "새 걸로 바꿔요", "새 수건을 꺼내요", "수건을 꺼내요", "수건을 걸어요", "칫솔건조기예요",
    "칫솔을 걸어 두면 칫솔이 말라요", "칫솔을 꺼내요", "치약 뚜껑을 열어요", "치약을 짜요", "칫솔로 이를 닦아요",
    "이를 닦아요", "컵이에요", "컵에 물을 받아요", "물을 받아요", "입을 헹궈요",
    "입을 물로 헹궈요", "칫솔을 물로 씻어요", "물을 털어요", "샤워부스예요", "샤워기가 있어요",
    "머리를 감거나 몸을 씻어요", "바디워시", "몸을 씻어요", "샴푸", "머리를 감아요",
    "펌프를 눌러요", "발을 비벼요", "발을 비벼서 거품을 내요", "발을 헹궈요", "물로 발을 헹궈요",
    "마지막으로 발수건으로 발을 닦아요", "발수건으로 발을 닦아요", "여러분", "한국어는 단어 3000개만 알면", "듣고 말하는 데 전혀 문제 없어요",
    "그리고 단어들 따로 공부할 필요 없어요", "제 영상만 꾸준히 보시면", "자연스럽게 외워져 있을 거예요", "그냥 편하게 보세요", "굳이 스트레스 받으면서 공부할 필요 없어요",
    "천천히 해도 꾸준히 하면", "여러분은 꼭 한국어를 잘하게 될 거예요", "그럼 다음 영상에서 만나요",
]
# "손을 닦아요"·"손을 닦을 때": 장면은 손을 씻는 것이라 번역은 'wash'로 옮겼다 (얼굴·발을 수건으로 "닦아요"는 'dry').

T = {}

T["en"] = [
    "Hello, everyone! I'm Mino.", "Today, how I wash up and get ready in the morning —", "I'll tell you all about it.", "Well then, let's take a look!", "I turn on the bathroom light.",
    "I go into the bathroom.", "Sink", "There's a sink.", "This is soap.", "Soap",
    "Soap is for washing your hands.", "This is hand wash.", "Hand wash is liquid soap.", "Hand wash is also for washing your hands.", "I turn on the tap.",
    "When you turn on the tap, water comes out.", "Water comes out.", "I turn the tap.", "If you turn the tap to the left,", "warm water comes out.",
    "I wash my hands.", "I rub the soap in my hands.", "I rub my hands together to make a lather.", "I make a lather.", "I rinse my hands with water.",
    "I shake the water off my hands.", "I shake my hands.", "I wash my face.", "I open the cap.", "I squeeze out the cleanser.",
    "I close the cap.", "I put the foam on my face.", "I put the foam on.", "I spread it evenly.", "I turn on the water again, and",
    "I wash my face.", "Towel", "I dry my face with a towel.", "I dry my face.", "After I use a towel,",
    "I change it for a new one.", "I take out a new towel.", "I take out the towel.", "I hang up the towel.", "This is a toothbrush dryer.",
    "If you hang your toothbrush here, it dries.", "I take out my toothbrush.", "I open the toothpaste cap.", "I squeeze out the toothpaste.", "I brush my teeth with the toothbrush.",
    "I brush my teeth.", "This is a cup.", "I fill the cup with water.", "I fill it with water.", "I rinse my mouth.",
    "I rinse my mouth with water.", "I wash the toothbrush with water.", "I shake off the water.", "This is the shower booth.", "There's a shower head.",
    "Here you wash your hair or your body.", "Body wash", "I wash my body.", "Shampoo", "I wash my hair.",
    "I press the pump.", "I rub my feet.", "I rub my feet to make a lather.", "I rinse my feet.", "I rinse my feet with water.",
    "Lastly, I dry my feet with a foot towel.", "I dry my feet with a foot towel.", "Everyone,", "in Korean, if you know just 3,000 words,", "you'll have no problem at all listening and speaking.",
    "And you don't need to study the words separately.", "If you just keep watching my videos,", "you'll find you've learned them naturally.", "Just relax and watch.", "There's no need to stress yourself out studying.",
    "Even if you go slowly, if you keep at it,", "you'll definitely get good at Korean.", "See you in the next video!",
]

T["zh-Hans"] = [
    "大家好！我是米诺。", "今天我来说说我早上是怎么洗漱、", "做准备的。", "那我们一起来看看吧！", "打开卫生间的灯。",
    "走进卫生间。", "洗手台", "这里有洗手台。", "这是香皂。", "香皂",
    "香皂是洗手的时候用的。", "这是洗手液。", "洗手液是液体肥皂。", "洗手液也是洗手的时候用的。", "打开水龙头。",
    "打开水龙头，水就流出来了。", "水流出来了。", "转动水龙头。", "把水龙头往左转，", "就会流出温水。",
    "洗手。", "用手搓香皂。", "搓手搓出泡沫。", "搓出泡沫。", "用水冲洗双手。",
    "甩掉手上的水。", "甩甩手。", "洗脸。", "打开盖子。", "挤出洁面乳。",
    "盖上盖子。", "把泡沫抹在脸上。", "抹上泡沫。", "均匀地抹开。", "再打开水，",
    "洗脸。", "毛巾", "用毛巾擦脸。", "擦脸。", "毛巾用过以后，",
    "就换一条新的。", "拿出一条新毛巾。", "拿出毛巾。", "把毛巾挂起来。", "这是牙刷烘干器。",
    "把牙刷挂在这里，牙刷就会干。", "拿出牙刷。", "打开牙膏盖。", "挤牙膏。", "用牙刷刷牙。",
    "刷牙。", "这是杯子。", "往杯子里接水。", "接水。", "漱口。",
    "用水漱口。", "用水冲洗牙刷。", "甩掉水。", "这是淋浴间。", "这里有花洒。",
    "在这里洗头或者洗澡。", "沐浴露", "洗身体。", "洗发水", "洗头。",
    "按压泵头。", "搓脚。", "搓脚搓出泡沫。", "冲洗脚。", "用水冲洗脚。",
    "最后，用擦脚巾擦脚。", "用擦脚巾擦脚。", "大家，", "韩语只要掌握3000个单词，", "听和说就完全没有问题。",
    "而且不用单独去背单词。", "只要坚持看我的视频，", "自然而然就记住了。", "轻轻松松地看就好。", "没必要带着压力去学习。",
    "慢一点也没关系，只要坚持，", "你们一定会把韩语说得很好。", "那我们下个视频见！",
]

T["id"] = [
    "Halo, semuanya! Aku Mino.", "Hari ini aku mau cerita bagaimana aku bersih-bersih", "dan bersiap di pagi hari.", "Yuk, kita lihat!", "Aku menyalakan lampu kamar mandi.",
    "Aku masuk ke kamar mandi.", "Wastafel", "Ada wastafel.", "Ini sabun.", "Sabun",
    "Sabun dipakai untuk mencuci tangan.", "Ini hand wash.", "Hand wash adalah sabun cair.", "Hand wash juga dipakai untuk mencuci tangan.", "Aku membuka keran.",
    "Kalau keran dibuka, airnya keluar.", "Airnya keluar.", "Aku memutar keran.", "Kalau keran diputar ke kiri,", "keluar air hangat.",
    "Aku mencuci tangan.", "Aku menggosok sabun di tangan.", "Aku menggosok tangan sampai berbusa.", "Sampai berbusa.", "Aku membilas tangan dengan air.",
    "Aku mengibaskan air dari tangan.", "Aku mengibaskan tangan.", "Aku cuci muka.", "Aku membuka tutupnya.", "Aku memencet sabun cuci muka.",
    "Aku menutup tutupnya.", "Aku mengoleskan busa ke wajah.", "Aku mengoleskan busanya.", "Aku oleskan secara merata.", "Aku nyalakan air lagi, lalu",
    "aku membasuh wajah.", "Handuk", "Aku mengeringkan wajah dengan handuk.", "Aku mengeringkan wajah.", "Setelah handuk dipakai,",
    "aku ganti dengan yang baru.", "Aku mengambil handuk baru.", "Aku mengambil handuk.", "Aku menggantung handuk.", "Ini pengering sikat gigi.",
    "Kalau sikat gigi digantung di sini, sikat giginya jadi kering.", "Aku mengambil sikat gigi.", "Aku membuka tutup pasta gigi.", "Aku memencet pasta gigi.", "Aku menyikat gigi dengan sikat gigi.",
    "Aku menyikat gigi.", "Ini gelas.", "Aku mengisi gelas dengan air.", "Aku mengisi air.", "Aku berkumur.",
    "Aku berkumur dengan air.", "Aku mencuci sikat gigi dengan air.", "Aku mengibaskan airnya.", "Ini bilik shower.", "Ada shower.",
    "Di sini kita keramas atau mandi.", "Sabun mandi", "Aku membersihkan badan.", "Sampo", "Aku keramas.",
    "Aku menekan pompanya.", "Aku menggosok kaki.", "Aku menggosok kaki sampai berbusa.", "Aku membilas kaki.", "Aku membilas kaki dengan air.",
    "Terakhir, aku mengeringkan kaki dengan handuk kaki.", "Aku mengeringkan kaki dengan handuk kaki.", "Teman-teman,", "dalam bahasa Korea, kalau kalian tahu 3.000 kata saja,", "kalian sama sekali tidak akan kesulitan mendengar dan berbicara.",
    "Dan kalian tidak perlu menghafal kata-katanya secara terpisah.", "Asal rutin menonton videoku,", "kalian akan hafal dengan sendirinya.", "Santai saja menontonnya.", "Tidak perlu belajar sampai stres.",
    "Pelan-pelan pun tidak apa-apa, asal konsisten,", "kalian pasti akan jago bahasa Korea.", "Sampai jumpa di video berikutnya!",
]

T["pt-BR"] = [
    "Olá, pessoal! Eu sou Mino.", "Hoje vou contar como eu me lavo e me arrumo", "de manhã.", "Então, vamos ver!", "Acendo a luz do banheiro.",
    "Entro no banheiro.", "Pia", "Tem uma pia.", "Isto é sabonete.", "Sabonete",
    "O sabonete é usado para lavar as mãos.", "Este é o sabonete para as mãos.", "O sabonete para as mãos é líquido.", "Ele também é usado para lavar as mãos.", "Abro a torneira.",
    "Quando você abre a torneira, sai água.", "Sai água.", "Giro a torneira.", "Se girar a torneira para a esquerda,", "sai água morna.",
    "Lavo as mãos.", "Esfrego o sabonete nas mãos.", "Esfrego as mãos para fazer espuma.", "Faço espuma.", "Enxáguo as mãos com água.",
    "Sacudo a água das mãos.", "Sacudo as mãos.", "Lavo o rosto.", "Abro a tampa.", "Aperto o limpador facial.",
    "Fecho a tampa.", "Passo a espuma no rosto.", "Passo a espuma.", "Espalho por igual.", "Abro a água de novo e",
    "lavo o rosto.", "Toalha", "Seco o rosto com a toalha.", "Seco o rosto.", "Depois de usar a toalha,",
    "troco por uma nova.", "Pego uma toalha nova.", "Pego a toalha.", "Penduro a toalha.", "Este é o secador de escova de dentes.",
    "Se você pendurar a escova aqui, ela seca.", "Pego a escova de dentes.", "Abro a tampa da pasta de dente.", "Aperto a pasta de dente.", "Escovo os dentes com a escova.",
    "Escovo os dentes.", "Isto é um copo.", "Encho o copo de água.", "Encho de água.", "Enxáguo a boca.",
    "Enxáguo a boca com água.", "Lavo a escova com água.", "Sacudo a água.", "Este é o box do chuveiro.", "Tem um chuveiro.",
    "Aqui a gente lava o cabelo ou o corpo.", "Sabonete líquido corporal", "Lavo o corpo.", "Xampu", "Lavo o cabelo.",
    "Aperto o dosador.", "Esfrego os pés.", "Esfrego os pés para fazer espuma.", "Enxáguo os pés.", "Enxáguo os pés com água.",
    "Por último, seco os pés com a toalha de pés.", "Seco os pés com a toalha de pés.", "Pessoal,", "no coreano, se você souber só 3.000 palavras,", "não vai ter nenhum problema para ouvir e falar.",
    "E não precisa estudar as palavras separadamente.", "Se você assistir aos meus vídeos com frequência,", "vai perceber que aprendeu naturalmente.", "É só assistir com calma.", "Não precisa estudar se estressando.",
    "Mesmo devagar, se tiver constância,", "com certeza você vai falar coreano muito bem.", "Até o próximo vídeo!",
]

T["fil"] = [
    "Hello, everyone! Ako si Mino.", "Ngayon, ikukuwento ko kung paano ako naghihilamos at naghahanda", "sa umaga.", "Tara, panoorin natin!", "Binubuksan ko ang ilaw ng banyo.",
    "Pumapasok ako sa banyo.", "Lababo", "May lababo.", "Ito ay sabon.", "Sabon",
    "Ginagamit ang sabon sa paghuhugas ng kamay.", "Ito ay hand wash.", "Ang hand wash ay likidong sabon.", "Ginagamit din ang hand wash sa paghuhugas ng kamay.", "Binubuksan ko ang gripo.",
    "Kapag binuksan mo ang gripo, lumalabas ang tubig.", "Lumalabas ang tubig.", "Pinipihit ko ang gripo.", "Kapag pinihit mo ang gripo pakaliwa,", "lumalabas ang maligamgam na tubig.",
    "Naghuhugas ako ng kamay.", "Kinukuskos ko ang sabon sa kamay.", "Kinukuskos ko ang kamay para bumula.", "Pinabubula ko.", "Binabanlawan ko ang kamay ng tubig.",
    "Pinapagpag ko ang tubig sa kamay.", "Pinapagpag ko ang kamay.", "Naghihilamos ako.", "Binubuksan ko ang takip.", "Pinipiga ko ang cleanser.",
    "Isinasara ko ang takip.", "Ipinapahid ko ang bula sa mukha.", "Ipinapahid ko ang bula.", "Pantay kong ipinapahid.", "Binubuksan ko ulit ang tubig, at",
    "hinuhugasan ko ang mukha.", "Tuwalya", "Pinupunasan ko ang mukha gamit ang tuwalya.", "Pinupunasan ko ang mukha.", "Pagkagamit ko ng tuwalya,",
    "pinapalitan ko ito ng bago.", "Kumukuha ako ng bagong tuwalya.", "Kinukuha ko ang tuwalya.", "Isinasabit ko ang tuwalya.", "Ito ay toothbrush dryer.",
    "Kapag isinabit mo rito ang toothbrush, natutuyo ito.", "Kinukuha ko ang toothbrush.", "Binubuksan ko ang takip ng toothpaste.", "Pinipiga ko ang toothpaste.", "Nagsisipilyo ako gamit ang toothbrush.",
    "Nagsisipilyo ako.", "Ito ay baso.", "Nilalagyan ko ng tubig ang baso.", "Nilalagyan ko ng tubig.", "Nagmumumog ako.",
    "Nagmumumog ako ng tubig.", "Hinuhugasan ko ang toothbrush ng tubig.", "Pinapagpag ko ang tubig.", "Ito ang shower booth.", "May shower.",
    "Dito nagsha-shampoo o naghuhugas ng katawan.", "Body wash", "Hinuhugasan ko ang katawan.", "Shampoo", "Nagsha-shampoo ako.",
    "Pinipindot ko ang pump.", "Kinukuskos ko ang paa.", "Kinukuskos ko ang paa para bumula.", "Binabanlawan ko ang paa.", "Binabanlawan ko ang paa ng tubig.",
    "Panghuli, pinupunasan ko ang paa gamit ang foot towel.", "Pinupunasan ko ang paa gamit ang foot towel.", "Mga kaibigan,", "sa Korean, kung alam mo lang ang 3,000 na salita,", "wala ka nang problema sa pakikinig at pagsasalita.",
    "At hindi mo na kailangang pag-aralan nang hiwalay ang mga salita.", "Basta tuloy-tuloy kang manood ng mga video ko,", "kusa mo na lang silang matatandaan.", "Manood ka lang nang relax.", "Hindi mo kailangang mag-aral nang stressed.",
    "Kahit mabagal, basta tuloy-tuloy,", "siguradong gagaling ka sa Korean.", "Kita-kits sa susunod na video!",
]

T["ru"] = [
    "Всем привет! С вами Мино.", "Сегодня я расскажу, как умываюсь и собираюсь", "по утрам.", "Ну что, давайте посмотрим!", "Включаю свет в ванной.",
    "Захожу в ванную.", "Раковина", "Здесь раковина.", "Это мыло.", "Мыло",
    "Мылом моют руки.", "Это средство для мытья рук.", "Это жидкое мыло.", "Им тоже моют руки.", "Открываю кран.",
    "Если открыть кран, течёт вода.", "Течёт вода.", "Поворачиваю кран.", "Если повернуть кран влево,", "потечёт тёплая вода.",
    "Мою руки.", "Тру мыло в руках.", "Тру руки, чтобы появилась пена.", "Взбиваю пену.", "Ополаскиваю руки водой.",
    "Стряхиваю воду с рук.", "Встряхиваю руками.", "Умываюсь.", "Открываю крышку.", "Выдавливаю пенку для умывания.",
    "Закрываю крышку.", "Наношу пену на лицо.", "Наношу пену.", "Равномерно распределяю.", "Снова открываю воду",
    "и умываю лицо.", "Полотенце", "Вытираю лицо полотенцем.", "Вытираю лицо.", "Когда полотенце использовано,",
    "меняю его на новое.", "Достаю новое полотенце.", "Достаю полотенце.", "Вешаю полотенце.", "Это сушилка для зубных щёток.",
    "Если повесить щётку сюда, она высохнет.", "Достаю зубную щётку.", "Открываю крышку зубной пасты.", "Выдавливаю пасту.", "Чищу зубы щёткой.",
    "Чищу зубы.", "Это стакан.", "Набираю воду в стакан.", "Набираю воду.", "Полощу рот.",
    "Полощу рот водой.", "Мою щётку водой.", "Стряхиваю воду.", "Это душевая кабина.", "Здесь есть душ.",
    "Здесь моют голову или тело.", "Гель для душа", "Мою тело.", "Шампунь", "Мою голову.",
    "Нажимаю на дозатор.", "Тру ступни.", "Тру ступни, чтобы появилась пена.", "Ополаскиваю ступни.", "Ополаскиваю ступни водой.",
    "И напоследок вытираю ноги полотенцем для ног.", "Вытираю ноги полотенцем для ног.", "Друзья,", "в корейском, если знать всего 3000 слов,", "вы без проблем будете понимать на слух и говорить.",
    "И учить слова отдельно не нужно.", "Просто регулярно смотрите мои видео,", "и слова запомнятся сами собой.", "Смотрите спокойно, без напряжения.", "Не нужно учиться через стресс.",
    "Даже если медленно, но регулярно,", "вы обязательно будете хорошо говорить по-корейски.", "До встречи в следующем видео!",
]

T["vi"] = [
    "Xin chào các bạn! Mình là Mino đây!", "Hôm nay mình sẽ kể buổi sáng mình", "vệ sinh cá nhân và chuẩn bị thế nào.", "Nào, cùng xem nhé!", "Mình bật đèn nhà vệ sinh.",
    "Mình đi vào nhà vệ sinh.", "Bồn rửa mặt", "Có bồn rửa mặt.", "Đây là xà phòng.", "Xà phòng",
    "Xà phòng dùng để rửa tay.", "Đây là nước rửa tay.", "Nước rửa tay là xà phòng dạng lỏng.", "Nước rửa tay cũng dùng để rửa tay.", "Mình mở vòi nước.",
    "Mở vòi nước thì nước chảy ra.", "Nước chảy ra.", "Mình xoay vòi nước.", "Nếu xoay vòi sang trái", "thì nước ấm chảy ra.",
    "Mình rửa tay.", "Mình xoa xà phòng vào tay.", "Mình xoa tay để tạo bọt.", "Tạo bọt.", "Mình rửa sạch tay bằng nước.",
    "Mình vẩy nước trên tay.", "Mình vẩy tay.", "Mình rửa mặt.", "Mình mở nắp.", "Mình bóp sữa rửa mặt.",
    "Mình đóng nắp.", "Mình thoa bọt lên mặt.", "Thoa bọt.", "Thoa đều khắp mặt.", "Mình mở nước lại",
    "và rửa mặt.", "Khăn", "Mình lau mặt bằng khăn.", "Mình lau mặt.", "Dùng khăn xong",
    "thì mình đổi cái mới.", "Mình lấy khăn mới ra.", "Mình lấy khăn ra.", "Mình treo khăn lên.", "Đây là máy sấy bàn chải đánh răng.",
    "Treo bàn chải vào đây thì bàn chải sẽ khô.", "Mình lấy bàn chải ra.", "Mình mở nắp kem đánh răng.", "Mình bóp kem đánh răng.", "Mình đánh răng bằng bàn chải.",
    "Mình đánh răng.", "Đây là cái cốc.", "Mình hứng nước vào cốc.", "Hứng nước.", "Mình súc miệng.",
    "Mình súc miệng bằng nước.", "Mình rửa bàn chải bằng nước.", "Mình vẩy cho ráo nước.", "Đây là buồng tắm vòi sen.", "Có vòi sen.",
    "Ở đây mình gội đầu hoặc tắm.", "Sữa tắm", "Mình tắm rửa cơ thể.", "Dầu gội", "Mình gội đầu.",
    "Mình nhấn vòi bơm.", "Mình chà chân.", "Mình chà chân để tạo bọt.", "Mình rửa sạch chân.", "Mình rửa sạch chân bằng nước.",
    "Cuối cùng, mình lau chân bằng khăn lau chân.", "Mình lau chân bằng khăn lau chân.", "Các bạn ơi,", "tiếng Hàn chỉ cần biết 3.000 từ thôi", "là nghe và nói hoàn toàn không có vấn đề gì.",
    "Và các bạn không cần học từ vựng riêng đâu.", "Chỉ cần xem video của mình đều đặn,", "các bạn sẽ tự nhiên nhớ được.", "Cứ thoải mái mà xem nhé.", "Không cần phải học trong căng thẳng đâu.",
    "Dù chậm nhưng đều đặn,", "các bạn nhất định sẽ giỏi tiếng Hàn.", "Hẹn gặp lại các bạn ở video sau nhé!",
]

T["es"] = [
    "¡Hola a todos! Soy Mino.", "Hoy les voy a contar cómo me aseo y me preparo", "por la mañana.", "¡Bueno, vamos a verlo!", "Enciendo la luz del baño.",
    "Entro al baño.", "Lavabo", "Hay un lavabo.", "Esto es jabón.", "Jabón",
    "El jabón se usa para lavarse las manos.", "Esto es jabón de manos.", "El jabón de manos es jabón líquido.", "El jabón de manos también se usa para lavarse las manos.", "Abro el grifo.",
    "Si abres el grifo, sale agua.", "Sale agua.", "Giro el grifo.", "Si giras el grifo a la izquierda,", "sale agua tibia.",
    "Me lavo las manos.", "Froto el jabón en las manos.", "Me froto las manos para hacer espuma.", "Hago espuma.", "Me enjuago las manos con agua.",
    "Sacudo el agua de las manos.", "Sacudo las manos.", "Me lavo la cara.", "Abro la tapa.", "Aprieto el limpiador facial.",
    "Cierro la tapa.", "Me pongo la espuma en la cara.", "Me pongo la espuma.", "La reparto bien.", "Abro el agua otra vez y",
    "me lavo la cara.", "Toalla", "Me seco la cara con la toalla.", "Me seco la cara.", "Después de usar la toalla,",
    "la cambio por una nueva.", "Saco una toalla nueva.", "Saco la toalla.", "Cuelgo la toalla.", "Este es un secador de cepillos de dientes.",
    "Si cuelgas el cepillo aquí, se seca.", "Saco el cepillo de dientes.", "Abro la tapa de la pasta de dientes.", "Aprieto la pasta de dientes.", "Me cepillo los dientes con el cepillo.",
    "Me cepillo los dientes.", "Esto es un vaso.", "Lleno el vaso de agua.", "Lo lleno de agua.", "Me enjuago la boca.",
    "Me enjuago la boca con agua.", "Lavo el cepillo con agua.", "Sacudo el agua.", "Esta es la cabina de ducha.", "Aquí está la ducha.",
    "Aquí te lavas el pelo o el cuerpo.", "Gel de baño", "Me lavo el cuerpo.", "Champú", "Me lavo el pelo.",
    "Presiono el dosificador.", "Me froto los pies.", "Me froto los pies para hacer espuma.", "Me enjuago los pies.", "Me enjuago los pies con agua.",
    "Por último, me seco los pies con la toalla de pies.", "Me seco los pies con la toalla de pies.", "Les cuento algo:", "en coreano, si sabes solo 3000 palabras,", "no tendrás ningún problema para escuchar y hablar.",
    "Y no hace falta estudiar las palabras aparte.", "Si ves mis videos con constancia,", "te las sabrás de forma natural.", "Solo míralos con calma.", "No hace falta estudiar con estrés.",
    "Aunque vayas despacio, si eres constante,", "seguro que vas a hablar muy bien coreano.", "¡Nos vemos en el próximo video!",
]

T["fr"] = [
    "Bonjour à tous ! C'est Mino.", "Aujourd'hui, je vais vous montrer comment je me lave et me prépare", "le matin.", "Allez, on regarde !", "J'allume la lumière de la salle de bain.",
    "J'entre dans la salle de bain.", "Lavabo", "Il y a un lavabo.", "Ça, c'est du savon.", "Savon",
    "On utilise le savon pour se laver les mains.", "Ça, c'est du savon pour les mains.", "Le savon pour les mains, c'est du savon liquide.", "On l'utilise aussi pour se laver les mains.", "J'ouvre le robinet.",
    "Quand on ouvre le robinet, l'eau coule.", "L'eau coule.", "Je tourne le robinet.", "Si on tourne le robinet vers la gauche,", "de l'eau tiède coule.",
    "Je me lave les mains.", "Je frotte le savon dans mes mains.", "Je me frotte les mains pour faire mousser.", "Je fais mousser.", "Je me rince les mains à l'eau.",
    "Je secoue l'eau de mes mains.", "Je secoue les mains.", "Je me lave le visage.", "J'ouvre le bouchon.", "Je presse le nettoyant visage.",
    "Je ferme le bouchon.", "J'applique la mousse sur mon visage.", "J'applique la mousse.", "Je l'étale bien partout.", "Je rouvre l'eau et",
    "je me rince le visage.", "Serviette", "Je m'essuie le visage avec une serviette.", "Je m'essuie le visage.", "Après avoir utilisé une serviette,",
    "je la remplace par une neuve.", "Je sors une serviette propre.", "Je sors la serviette.", "J'accroche la serviette.", "C'est un sèche-brosse à dents.",
    "Si on y accroche sa brosse à dents, elle sèche.", "Je sors ma brosse à dents.", "J'ouvre le bouchon du dentifrice.", "Je presse le tube de dentifrice.", "Je me brosse les dents avec la brosse à dents.",
    "Je me brosse les dents.", "C'est un gobelet.", "Je remplis le gobelet d'eau.", "Je le remplis d'eau.", "Je me rince la bouche.",
    "Je me rince la bouche à l'eau.", "Je lave la brosse à dents à l'eau.", "Je secoue l'eau.", "C'est la cabine de douche.", "Il y a une douchette.",
    "Ici, on se lave les cheveux ou le corps.", "Gel douche", "Je me lave le corps.", "Shampoing", "Je me lave les cheveux.",
    "J'appuie sur la pompe.", "Je me frotte les pieds.", "Je me frotte les pieds pour faire mousser.", "Je me rince les pieds.", "Je me rince les pieds à l'eau.",
    "Pour finir, je m'essuie les pieds avec la serviette pour les pieds.", "Je m'essuie les pieds avec la serviette pour les pieds.", "Vous savez,", "en coréen, si vous connaissez seulement 3 000 mots,", "vous n'aurez aucun problème pour comprendre et parler.",
    "Et pas besoin d'étudier les mots à part.", "Si vous regardez mes vidéos régulièrement,", "vous les retiendrez naturellement.", "Regardez-les tranquillement.", "Pas besoin de vous stresser à étudier.",
    "Même si vous allez lentement, avec de la régularité,", "vous parlerez forcément bien coréen.", "À la prochaine vidéo !",
]

T["de"] = [
    "Hallo zusammen! Hier ist Mino!", "Heute erzähle ich euch, wie ich mich", "morgens wasche und fertig mache.", "Na dann, schauen wir mal!", "Ich mache das Licht im Bad an.",
    "Ich gehe ins Bad.", "Waschbecken", "Hier ist ein Waschbecken.", "Das ist Seife.", "Seife",
    "Seife benutzt man zum Händewaschen.", "Das ist Handseife.", "Handseife ist flüssige Seife.", "Handseife benutzt man auch zum Händewaschen.", "Ich drehe den Wasserhahn auf.",
    "Wenn man den Wasserhahn aufdreht, kommt Wasser.", "Wasser kommt heraus.", "Ich drehe am Wasserhahn.", "Wenn man den Wasserhahn nach links dreht,", "kommt warmes Wasser.",
    "Ich wasche mir die Hände.", "Ich reibe die Seife zwischen den Händen.", "Ich reibe die Hände, bis es schäumt.", "Ich mache Schaum.", "Ich spüle die Hände mit Wasser ab.",
    "Ich schüttle das Wasser von den Händen.", "Ich schüttle die Hände aus.", "Ich wasche mir das Gesicht.", "Ich öffne den Deckel.", "Ich drücke etwas Reinigungsschaum heraus.",
    "Ich schließe den Deckel.", "Ich verteile den Schaum auf dem Gesicht.", "Ich verteile den Schaum.", "Schön gleichmäßig.", "Ich drehe das Wasser wieder auf und",
    "wasche mir das Gesicht.", "Handtuch", "Ich trockne mir das Gesicht mit dem Handtuch ab.", "Ich trockne mir das Gesicht ab.", "Wenn ich ein Handtuch benutzt habe,",
    "tausche ich es gegen ein neues.", "Ich nehme ein neues Handtuch heraus.", "Ich nehme das Handtuch heraus.", "Ich hänge das Handtuch auf.", "Das ist ein Zahnbürstentrockner.",
    "Wenn man die Zahnbürste hier aufhängt, trocknet sie.", "Ich nehme die Zahnbürste heraus.", "Ich öffne den Deckel der Zahnpasta.", "Ich drücke Zahnpasta heraus.", "Ich putze mir mit der Zahnbürste die Zähne.",
    "Ich putze mir die Zähne.", "Das ist ein Becher.", "Ich fülle den Becher mit Wasser.", "Ich fülle Wasser ein.", "Ich spüle mir den Mund aus.",
    "Ich spüle mir den Mund mit Wasser aus.", "Ich wasche die Zahnbürste mit Wasser ab.", "Ich schüttle das Wasser ab.", "Das ist die Duschkabine.", "Hier ist der Duschkopf.",
    "Hier wäscht man sich die Haare oder den Körper.", "Duschgel", "Ich wasche meinen Körper.", "Shampoo", "Ich wasche mir die Haare.",
    "Ich drücke auf den Pumpspender.", "Ich reibe mir die Füße ein.", "Ich reibe die Füße, bis es schäumt.", "Ich spüle die Füße ab.", "Ich spüle die Füße mit Wasser ab.",
    "Zum Schluss trockne ich mir die Füße mit dem Fußhandtuch ab.", "Ich trockne mir die Füße mit dem Fußhandtuch ab.", "Leute,", "im Koreanischen reichen schon 3.000 Wörter,", "um ohne Probleme zu verstehen und zu sprechen.",
    "Und ihr müsst die Wörter nicht extra lernen.", "Wenn ihr einfach regelmäßig meine Videos schaut,", "habt ihr sie ganz natürlich im Kopf.", "Schaut einfach ganz entspannt zu.", "Ihr müsst euch beim Lernen nicht stressen.",
    "Auch wenn ihr langsam vorankommt – wenn ihr dranbleibt,", "werdet ihr ganz sicher gut Koreanisch sprechen.", "Bis zum nächsten Video!",
]

T["ar"] = [
    "مرحبًا بالجميع! أنا مينو.", "اليوم سأخبركم كيف أغتسل وأستعد", "في الصباح.", "هيا نشاهد!", "أشعل ضوء الحمام.",
    "أدخل إلى الحمام.", "المغسلة", "هناك مغسلة.", "هذا صابون.", "صابون",
    "نستخدم الصابون لغسل اليدين.", "هذا صابون اليدين.", "صابون اليدين هو صابون سائل.", "نستخدم صابون اليدين أيضًا لغسل اليدين.", "أفتح الصنبور.",
    "عندما تفتح الصنبور، يخرج الماء.", "يخرج الماء.", "أدير الصنبور.", "إذا أدرت الصنبور إلى اليسار،", "يخرج ماء دافئ.",
    "أغسل يديّ.", "أفرك الصابون بيديّ.", "أفرك يديّ لتكوين الرغوة.", "أكوّن الرغوة.", "أشطف يديّ بالماء.",
    "أنفض الماء عن يديّ.", "أنفض يديّ.", "أغسل وجهي.", "أفتح الغطاء.", "أعصر غسول الوجه.",
    "أغلق الغطاء.", "أضع الرغوة على وجهي.", "أضع الرغوة.", "أوزّعها بالتساوي.", "أفتح الماء مرة أخرى",
    "وأغسل وجهي.", "منشفة", "أجفف وجهي بالمنشفة.", "أجفف وجهي.", "بعد استخدام المنشفة،",
    "أستبدلها بواحدة جديدة.", "أُخرج منشفة جديدة.", "أُخرج المنشفة.", "أعلّق المنشفة.", "هذا مجفف فرشاة الأسنان.",
    "إذا علّقت الفرشاة هنا، تجف.", "أُخرج فرشاة الأسنان.", "أفتح غطاء معجون الأسنان.", "أعصر معجون الأسنان.", "أنظف أسناني بالفرشاة.",
    "أنظف أسناني.", "هذا كوب.", "أملأ الكوب بالماء.", "أملؤه بالماء.", "أتمضمض.",
    "أتمضمض بالماء.", "أغسل الفرشاة بالماء.", "أنفض الماء.", "هذه كابينة الاستحمام.", "هناك دُش.",
    "هنا نغسل الشعر أو الجسم.", "غسول الجسم", "أغسل جسمي.", "شامبو", "أغسل شعري.",
    "أضغط على المضخة.", "أفرك قدميّ.", "أفرك قدميّ لتكوين الرغوة.", "أشطف قدميّ.", "أشطف قدميّ بالماء.",
    "وأخيرًا، أجفف قدميّ بمنشفة القدمين.", "أجفف قدميّ بمنشفة القدمين.", "يا أصدقاء،", "في اللغة الكورية، إذا عرفتم 3000 كلمة فقط،", "فلن تواجهوا أي مشكلة في الاستماع والتحدث.",
    "ولا داعي لدراسة الكلمات بشكل منفصل.", "فقط شاهدوا فيديوهاتي باستمرار،", "وستجدون أنكم حفظتموها بشكل طبيعي.", "شاهدوا براحة فقط.", "لا داعي للدراسة تحت الضغط.",
    "حتى لو تقدّمتم ببطء، إذا واظبتم،", "فستتقنون الكورية بالتأكيد.", "أراكم في الفيديو القادم!",
]

T["ja"] = [
    "みなさん、こんにちは！ミノです。", "今日は、私が朝どうやって顔を洗って準備するのか", "お話しします。", "では、見てみましょう！", "バスルームの電気をつけます。",
    "バスルームに入ります。", "洗面台", "洗面台があります。", "これは石けんです。", "石けん",
    "石けんは手を洗うときに使います。", "これはハンドソープです。", "ハンドソープは液体の石けんです。", "ハンドソープも手を洗うときに使います。", "蛇口をひねって水を出します。",
    "蛇口をひねると、水が出ます。", "水が出ます。", "蛇口を回します。", "蛇口を左に回すと、", "温かいお湯が出ます。",
    "手を洗います。", "石けんを手でこすります。", "手をこすって泡を立てます。", "泡を立てます。", "水で手をすすぎます。",
    "手の水を払います。", "手を振って水を切ります。", "顔を洗います。", "ふたを開けます。", "洗顔料をしぼります。",
    "ふたを閉めます。", "顔に泡をつけます。", "泡をつけます。", "まんべんなくつけます。", "また水を出して、",
    "顔を洗います。", "タオル", "タオルで顔をふきます。", "顔をふきます。", "タオルを使ったら、",
    "新しいのに替えます。", "新しいタオルを出します。", "タオルを出します。", "タオルをかけます。", "歯ブラシ乾燥機です。",
    "歯ブラシをかけておくと、歯ブラシが乾きます。", "歯ブラシを取り出します。", "歯みがき粉のふたを開けます。", "歯みがき粉をしぼります。", "歯ブラシで歯をみがきます。",
    "歯をみがきます。", "コップです。", "コップに水をくみます。", "水をくみます。", "口をすすぎます。",
    "水で口をすすぎます。", "歯ブラシを水で洗います。", "水を切ります。", "シャワーブースです。", "シャワーがあります。",
    "ここで髪を洗ったり、体を洗ったりします。", "ボディソープ", "体を洗います。", "シャンプー", "髪を洗います。",
    "ポンプを押します。", "足をこすります。", "足をこすって泡を立てます。", "足をすすぎます。", "水で足をすすぎます。",
    "最後に、足ふきタオルで足をふきます。", "足ふきタオルで足をふきます。", "みなさん、", "韓国語は単語を3000個知っていれば、", "聞くのも話すのも全く問題ありません。",
    "そして、単語を別に勉強する必要はありません。", "私の動画を続けて見ていれば、", "自然と覚えているはずです。", "気楽に見てください。", "わざわざストレスを感じながら勉強する必要はありません。",
    "ゆっくりでも、続けていれば、", "みなさんはきっと韓国語が上手になります。", "では、次の動画で会いましょう！",
]

T["ms"] = [
    "Hai semua! Saya Mino.", "Hari ini saya nak tunjukkan bagaimana saya membersihkan diri dan bersiap", "pada waktu pagi.", "Jom kita tengok!", "Saya pasang lampu bilik air.",
    "Saya masuk ke bilik air.", "Sinki", "Ada sinki.", "Ini sabun.", "Sabun",
    "Sabun digunakan untuk mencuci tangan.", "Ini sabun basuh tangan.", "Sabun basuh tangan ialah sabun cecair.", "Sabun basuh tangan juga digunakan untuk mencuci tangan.", "Saya buka paip.",
    "Kalau buka paip, air keluar.", "Air keluar.", "Saya pusing paip.", "Kalau pusing paip ke kiri,", "air suam keluar.",
    "Saya cuci tangan.", "Saya gosok sabun pada tangan.", "Saya gosok tangan sampai berbuih.", "Sampai berbuih.", "Saya bilas tangan dengan air.",
    "Saya kibas air dari tangan.", "Saya kibas tangan.", "Saya cuci muka.", "Saya buka penutup.", "Saya picit pencuci muka.",
    "Saya tutup penutup.", "Saya sapukan buih pada muka.", "Saya sapukan buih.", "Sapu sekata.", "Saya buka air semula, dan",
    "saya cuci muka.", "Tuala", "Saya lap muka dengan tuala.", "Saya lap muka.", "Selepas guna tuala,",
    "saya tukar dengan yang baharu.", "Saya keluarkan tuala baharu.", "Saya keluarkan tuala.", "Saya sangkut tuala.", "Ini pengering berus gigi.",
    "Kalau sangkut berus gigi di sini, ia akan kering.", "Saya keluarkan berus gigi.", "Saya buka penutup ubat gigi.", "Saya picit ubat gigi.", "Saya gosok gigi dengan berus gigi.",
    "Saya gosok gigi.", "Ini cawan.", "Saya isi air dalam cawan.", "Saya isi air.", "Saya berkumur.",
    "Saya berkumur dengan air.", "Saya basuh berus gigi dengan air.", "Saya kibas airnya.", "Ini kubikel mandi.", "Ada pancuran air.",
    "Di sini kita syampu rambut atau mandi.", "Sabun mandi", "Saya cuci badan.", "Syampu", "Saya syampu rambut.",
    "Saya tekan pam.", "Saya gosok kaki.", "Saya gosok kaki sampai berbuih.", "Saya bilas kaki.", "Saya bilas kaki dengan air.",
    "Akhir sekali, saya lap kaki dengan tuala kaki.", "Saya lap kaki dengan tuala kaki.", "Semua,", "dalam bahasa Korea, kalau tahu 3,000 perkataan sahaja,", "anda langsung tiada masalah untuk mendengar dan bercakap.",
    "Dan tak perlu belajar perkataan secara berasingan.", "Asalkan selalu tonton video saya,", "anda akan ingat secara semula jadi.", "Tonton saja dengan santai.", "Tak perlu belajar sampai tertekan.",
    "Walaupun perlahan, asalkan konsisten,", "anda pasti akan pandai berbahasa Korea.", "Jumpa lagi dalam video seterusnya!",
]


def parse(path):
    src = open(path, encoding="utf-8").read().replace("\r\n", "\n").strip("\n")
    cues = []
    for b in src.split("\n\n"):
        time, text = b.split("\n", 1)
        assert re.match(r"^\d+:\d\d:\d\d\.\d{3},\d+:\d\d:\d\d\.\d{3}$", time), time
        cues.append((time, text.strip()))
    return cues


def main():
    assert len(KO) == len(set(KO)) == 83
    for lang, rows in T.items():
        assert len(rows) == len(KO), (lang, len(rows))
    idx = {k: i for i, k in enumerate(KO)}
    cues = parse(SRC)
    for _, key in cues:
        assert key in idx, f"번역표에 없는 문장: {key!r}"
    for lang, rows in T.items():
        out = "\n\n".join(f"{time}\n{rows[idx[key]]}" for time, key in cues) + "\n"
        path = os.path.join(HERE, f"S004_captions.{lang}.sbv")
        with open(path, "w", encoding="utf-8", newline="\r\n") as f:  # 원본과 같은 CRLF
            f.write(out)
        # 검증: 타임코드 개수·값이 원본과 같은지
        assert [t for t, _ in parse(path)] == [t for t, _ in cues], lang
        print(f"{lang}: {len(cues)}줄 OK")


if __name__ == "__main__":
    main()
