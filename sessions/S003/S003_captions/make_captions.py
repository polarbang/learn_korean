"""S003_captions.kr.sbv(한국어)를 13개 언어로 옮긴 .sbv 파일 생성.

타임코드·줄 구성은 원본 그대로 두고, 자막 문장만 언어별 번역으로 바꾼다.
번역은 문장 단위 표(KO 순서와 같은 순서)로 관리한다. 원본에 없는 문장이 있으면 에러.
실행: python make_captions.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "S003_captions.kr.sbv")

KO = [
    "안녕하세요 여러분. 미노예요.", "오늘은 날씨가 좋아서", "산에 왔어요.", "날씨도 시원하고", "바람이 적당히 불어서",
    "운동하기 딱 좋아요", "표지판이에요", "표지판이 가르키는 방향으로 가요.", "반대편에 아주머니 두 명이 걸어와요.", "걷다 보니 계단이 있어요.",
    "계단이 있어요.", "계단을 올라가요.", "걷다 보니까 목이 말라요.", "집에서 커피 가져와서", "커피 마실 거예요.",
    "가방에서 텀블러를 꺼내요.", "텀블러를 꺼내요.", "커피가 텀블러 안에 있어요.", "뚜껑을 돌려서 열어요.", "커피를 마셔요. 커피를 마셔요.",
    "뚜껑을 닫아요.", "가방에 넣어요.", "오르막길이 나왔어요.", "오르막길.", "길옆에 난간이 있어요.",
    "난간이 있어요.", "난간을 손으로 잡아요.", "난간을 잡아요.", "계속 오르막길이에요.", "경사가 가파라요.",
    "조금 힘들어요.", "저쪽으로는 못 가요.", "못 가요.", "울타리로 막혀 있어요.", "울타리",
    "지도가 있어요.", "지금 내 위치를 확인해요.", "위치를 확인해요.", "돌이 쌓여 있어요.", "한국 사람들은 돌을 높게 쌓으면",
    "소원을 들어 준다고 믿어요.", "돌을 하나 주워요.", "저도 돌을 하나 쌓아요.", "한국 산에는 운동 기구가 있어요.", "운동 기구가 있어요.",
    "허리를 좌우로 돌려요.", "좌우로 돌려요.", "이제 산을 내려가요.", "아저씨가 맨발로 걸어요.", "맨발로 걸어요.",
    "계속 내려가요.", "아주머니 세 명이", "수다를 떨고 있어요.", "아주머니 세 명이 수다를 떨고 있어요.", "꽃이 폈어요.",
    "벌이 꽃에 앉았어요.", "가까이 가니까 날아갔어요.", "집에 오는 길에 고양이가 있었어요.", "고양이.", "눈을 감아요.",
    "졸린가 봐요.", "엄청 귀여워요.", "여러분, 오늘은 여러분들한테", "팁 하나 드리려고 해요.", "한국어는 단어 3천개",
    "3천개만 알면", "듣고 말하는데 전혀 문제 없어요.", "그리고 이 단어들 따로", "공부할 필요 없어요.", "제 영상만 꾸준히 보시면",
    "어느 날 자연스럽게 외워져 있을 거예요.", "그냥 편하게 보세요.", "굳이 스트레스 받으면서", "천천히 해도 꾸준히 하면", "여러분은 꼭 한국어를 잘하게 될 거예요.",
    "그럼 다음 영상에서 만나요.",
]
# "공부할 필요 없어요."는 두 번 나온다 ("이 단어들 따로 …" / "굳이 스트레스 받으면서 …").
# 번역은 하나뿐이므로 앞줄(68·73번)을 양쪽 다 자연스럽게 이어지도록 맞췄다.

T = {}

T["en"] = [
    "Hello, everyone. I'm Mino.", "The weather is nice today, so", "I came to the mountain.", "The weather is cool,", "and there's just the right breeze,",
    "so it's perfect for exercising.", "Here's a sign.", "I go the way the sign points.", "On the other side, two ladies are walking toward me.", "As I walk, there are some stairs.",
    "There are stairs.", "I go up the stairs.", "After walking a while, I'm thirsty.", "I brought coffee from home,", "so I'm going to drink it.",
    "I take my tumbler out of my bag.", "I take out the tumbler.", "The coffee is inside the tumbler.", "I twist the lid to open it.", "I drink the coffee. I drink the coffee.",
    "I close the lid.", "I put it in my bag.", "Here comes an uphill path.", "Uphill.", "There's a railing beside the path.",
    "There's a railing.", "I hold the railing with my hand.", "I hold the railing.", "It keeps going uphill.", "The slope is steep.",
    "It's a little tiring.", "You can't go that way.", "Can't go.", "It's blocked off with a fence.", "Fence",
    "There's a map.", "I check where I am now.", "I check my location.", "Stones are piled up here.", "Koreans believe that if you stack stones high,",
    "your wish will come true.", "I pick up a stone.", "I stack one stone, too.", "Korean mountains have exercise machines.", "There are exercise machines.",
    "I twist my waist left and right.", "Left and right.", "Now I go down the mountain.", "A man is walking barefoot.", "Walking barefoot.",
    "I keep going down.", "Three ladies", "are chatting away.", "Three ladies are chatting away.", "The flowers are in bloom.",
    "A bee landed on a flower.", "When I got close, it flew away.", "On my way home, there was a cat.", "A cat.", "It closes its eyes.",
    "It looks sleepy.", "Sooo cute.", "Everyone, today", "I'd like to give you a tip.", "In Korean, 3,000 words —",
    "if you know just 3,000 words,", "you'll have no problem at all listening and speaking.", "And these words? On their own…", "you don't need to study them.", "If you just keep watching my videos,",
    "one day you'll find you've learned them naturally.", "Just relax and watch.", "Stressing yourself out…", "Even if you go slowly, if you keep at it,", "you'll definitely get good at Korean.",
    "See you in the next video!",
]

T["zh-Hans"] = [
    "大家好，我是米诺。", "今天天气很好，所以", "我来爬山了。", "天气也很凉爽，", "风吹得刚刚好，",
    "正适合运动。", "这是指示牌。", "我朝着指示牌指的方向走。", "对面有两位阿姨走过来。", "走着走着，出现了台阶。",
    "有台阶。", "我走上台阶。", "走着走着，口渴了。", "我从家里带了咖啡，", "我要喝咖啡。",
    "从包里拿出保温杯。", "拿出保温杯。", "咖啡在保温杯里。", "拧开盖子。", "喝咖啡。喝咖啡。",
    "盖上盖子。", "放进包里。", "出现了上坡路。", "上坡路。", "路边有栏杆。",
    "有栏杆。", "用手抓住栏杆。", "抓住栏杆。", "一直是上坡路。", "坡很陡。",
    "有点累。", "那边不能走。", "不能走。", "被栅栏挡住了。", "栅栏",
    "有地图。", "确认一下我现在的位置。", "确认位置。", "石头堆起来了。", "韩国人相信，把石头堆得高高的，",
    "愿望就会实现。", "捡起一块石头。", "我也堆上一块石头。", "韩国的山上有运动器材。", "有运动器材。",
    "左右扭腰。", "左右扭。", "现在下山。", "一位大叔光着脚走路。", "光着脚走路。",
    "继续往下走。", "三位阿姨", "正在聊天。", "三位阿姨正在聊天。", "花开了。",
    "蜜蜂落在花上。", "我一靠近，它就飞走了。", "回家的路上有一只猫。", "猫咪。", "闭上眼睛。",
    "好像困了。", "超级可爱。", "大家，今天", "我想给你们一个小建议。", "韩语的单词，3000个——",
    "只要会3000个，", "听和说就完全没问题。", "而且这些单词，单独……", "不需要专门去学。", "只要坚持看我的视频，",
    "总有一天会自然而然地记住。", "轻松地看就好。", "没必要给自己压力……", "就算慢慢来，只要坚持，", "你们一定会说好韩语的。",
    "那我们下个视频见！",
]

T["id"] = [
    "Halo semuanya. Aku Mino.", "Hari ini cuacanya bagus, jadi", "aku datang ke gunung.", "Cuacanya juga sejuk,", "anginnya bertiup pas,",
    "pas banget buat olahraga.", "Ini papan penunjuk.", "Aku jalan ke arah yang ditunjuk papan itu.", "Dari arah berlawanan, dua ibu-ibu berjalan ke arahku.", "Sambil jalan, ada tangga.",
    "Ada tangga.", "Aku naik tangga.", "Habis jalan, aku jadi haus.", "Aku bawa kopi dari rumah,", "aku mau minum kopi.",
    "Aku keluarkan tumbler dari tas.", "Aku keluarkan tumbler.", "Kopinya ada di dalam tumbler.", "Aku putar tutupnya untuk membukanya.", "Aku minum kopi. Aku minum kopi.",
    "Aku tutup tutupnya.", "Aku masukkan ke tas.", "Ada jalan menanjak.", "Jalan menanjak.", "Di samping jalan ada pegangan.",
    "Ada pegangan.", "Aku pegang pegangannya dengan tangan.", "Aku pegang pegangannya.", "Jalannya terus menanjak.", "Lerengnya curam.",
    "Agak capek.", "Ke sana nggak bisa lewat.", "Nggak bisa lewat.", "Ditutup pakai pagar.", "Pagar",
    "Ada peta.", "Aku cek posisiku sekarang.", "Cek posisi.", "Batu-batu ditumpuk.", "Orang Korea percaya, kalau menumpuk batu tinggi-tinggi,",
    "keinginan akan terkabul.", "Aku ambil satu batu.", "Aku juga menumpuk satu batu.", "Di gunung Korea ada alat olahraga.", "Ada alat olahraga.",
    "Aku putar pinggang ke kiri dan kanan.", "Ke kiri dan kanan.", "Sekarang aku turun gunung.", "Seorang bapak berjalan tanpa alas kaki.", "Berjalan tanpa alas kaki.",
    "Terus turun.", "Tiga ibu-ibu", "sedang mengobrol.", "Tiga ibu-ibu sedang mengobrol.", "Bunganya mekar.",
    "Lebah hinggap di bunga.", "Waktu aku mendekat, lebahnya terbang.", "Di jalan pulang, ada kucing.", "Kucing.", "Dia memejamkan mata.",
    "Kayaknya ngantuk.", "Lucu banget.", "Teman-teman, hari ini", "aku mau kasih satu tips.", "Bahasa Korea, 3.000 kata —",
    "kalau tahu 3.000 kata saja,", "mendengar dan berbicara sama sekali nggak masalah.", "Dan kata-kata ini, secara terpisah…", "nggak perlu dipelajari.", "Cukup tonton videoku secara rutin,",
    "suatu hari kalian akan hafal dengan sendirinya.", "Tonton saja dengan santai.", "Sampai stres segala…", "Pelan-pelan pun, asal rutin,", "kalian pasti akan jago bahasa Korea.",
    "Sampai jumpa di video berikutnya!",
]

T["pt-BR"] = [
    "Oi, pessoal. Eu sou Mino.", "Hoje o tempo está bom, então", "vim para a montanha.", "O tempo está fresquinho,", "o vento está na medida certa,",
    "perfeito para fazer exercício.", "Aqui tem uma placa.", "Vou na direção que a placa indica.", "Do outro lado, duas senhoras vêm caminhando.", "Andando, aparece uma escada.",
    "Tem uma escada.", "Subo a escada.", "De tanto andar, fiquei com sede.", "Trouxe café de casa,", "vou tomar o café.",
    "Tiro o copo térmico da bolsa.", "Tiro o copo térmico.", "O café está dentro do copo térmico.", "Giro a tampa para abrir.", "Tomo o café. Tomo o café.",
    "Fecho a tampa.", "Coloco na bolsa.", "Apareceu uma subida.", "Subida.", "Ao lado do caminho tem um corrimão.",
    "Tem um corrimão.", "Seguro o corrimão com a mão.", "Seguro o corrimão.", "Continua subindo.", "A ladeira é íngreme.",
    "Está um pouco cansativo.", "Por ali não dá para passar.", "Não dá.", "Está bloqueado com uma cerca.", "Cerca",
    "Tem um mapa.", "Confiro onde estou agora.", "Confiro a localização.", "Tem pedras empilhadas.", "Os coreanos acreditam que, se você empilhar pedras bem alto,",
    "seu desejo se realiza.", "Pego uma pedra.", "Eu também empilho uma pedra.", "As montanhas coreanas têm aparelhos de ginástica.", "Tem aparelhos de ginástica.",
    "Giro a cintura para os lados.", "Para um lado e para o outro.", "Agora vou descer a montanha.", "Um senhor está andando descalço.", "Andando descalço.",
    "Continuo descendo.", "Três senhoras", "estão batendo papo.", "Três senhoras estão batendo papo.", "As flores desabrocharam.",
    "Uma abelha pousou na flor.", "Quando cheguei perto, ela voou.", "No caminho de volta para casa, tinha um gato.", "Gatinho.", "Ele fecha os olhos.",
    "Parece que está com sono.", "Muito fofo.", "Pessoal, hoje", "quero dar uma dica para vocês.", "No coreano, 3 mil palavras —",
    "se você souber só 3 mil palavras,", "não terá nenhum problema para ouvir e falar.", "E essas palavras? Separadamente…", "não precisa estudar.", "Se você assistir aos meus vídeos com constância,",
    "um dia vai perceber que aprendeu tudo naturalmente.", "Só assista com calma.", "Se estressando à toa…", "Mesmo devagar, se for constante,", "com certeza você vai falar coreano bem.",
    "Então, até o próximo vídeo!",
]

T["fil"] = [
    "Kumusta, mga kaibigan. Ako si Mino.", "Maganda ang panahon ngayon, kaya", "pumunta ako sa bundok.", "Presko rin ang panahon,", "tama lang ang ihip ng hangin,",
    "kaya perfect para mag-ehersisyo.", "Ito ang karatula.", "Pupunta ako sa direksyong itinuturo ng karatula.", "Sa kabilang side, may dalawang ale na naglalakad papunta rito.", "Habang naglalakad, may hagdan.",
    "May hagdan.", "Umaakyat ako sa hagdan.", "Kakalakad, nauhaw ako.", "Nagdala ako ng kape mula sa bahay,", "iinom ako ng kape.",
    "Inilalabas ko ang tumbler mula sa bag.", "Inilalabas ko ang tumbler.", "Nasa loob ng tumbler ang kape.", "Pinipihit ko ang takip para buksan.", "Umiinom ako ng kape. Umiinom ako ng kape.",
    "Isinasara ko ang takip.", "Inilalagay ko sa bag.", "May paakyat na daan.", "Paakyat.", "May hawakan sa gilid ng daan.",
    "May hawakan.", "Hinahawakan ko ang hawakan gamit ang kamay.", "Hinahawakan ko ang hawakan.", "Tuloy-tuloy ang paakyat.", "Matarik ang dalisdis.",
    "Medyo nakakapagod.", "Hindi puwedeng dumaan doon.", "Hindi puwede.", "Nakaharang ang bakod.", "Bakod",
    "May mapa.", "Tinitingnan ko kung nasaan ako ngayon.", "Tinitingnan ko ang lokasyon.", "May mga batong nakapatong-patong.", "Naniniwala ang mga Koreano na kapag pinatong nang mataas ang mga bato,",
    "matutupad ang hiling mo.", "Pumupulot ako ng isang bato.", "Nagpapatong din ako ng isang bato.", "May mga exercise equipment sa mga bundok sa Korea.", "May mga exercise equipment.",
    "Pinipihit ko ang baywang pakaliwa't pakanan.", "Pakaliwa't pakanan.", "Ngayon, bababa na ako ng bundok.", "May manong na naglalakad nang nakayapak.", "Naglalakad nang nakayapak.",
    "Tuloy lang ang pagbaba.", "Tatlong ale", "ang nagkukuwentuhan.", "Tatlong ale ang nagkukuwentuhan.", "Namukadkad ang mga bulaklak.",
    "Dumapo ang bubuyog sa bulaklak.", "Paglapit ko, lumipad ito palayo.", "Pauwi, may pusa sa daan.", "Pusa.", "Pumipikit siya.",
    "Mukhang inaantok.", "Sobrang cute.", "Mga kaibigan, ngayon", "may ibibigay akong isang tip.", "Sa Korean, 3,000 na salita —",
    "kung alam mo lang ang 3,000 na salita,", "wala ka nang problema sa pakikinig at pagsasalita.", "At ang mga salitang ito, nang hiwalay…", "hindi mo kailangang pag-aralan.", "Basta panoorin mo lang ang mga video ko nang tuloy-tuloy,",
    "isang araw, kabisado mo na sila nang natural.", "Manood ka lang nang relaxed.", "Ang ma-stress pa…", "Kahit dahan-dahan, basta tuloy-tuloy,", "siguradong gagaling ka sa Korean.",
    "Sige, kita-kits sa susunod na video!",
]

T["ru"] = [
    "Всем привет. Я Мино.", "Сегодня отличная погода, поэтому", "вот я в горах.", "Погода прохладная,", "ветер дует в самый раз,",
    "идеально для тренировки.", "Вот указатель.", "Иду туда, куда показывает указатель.", "Навстречу идут две женщины.", "Иду — и вот лестница.",
    "Здесь лестница.", "Поднимаюсь по лестнице.", "От ходьбы захотелось пить.", "Кофе у меня с собой из дома,", "сейчас буду его пить.",
    "Достаю термокружку из сумки.", "Достаю термокружку.", "Кофе в термокружке.", "Откручиваю крышку и открываю.", "Пью кофе. Пью кофе.",
    "Закрываю крышку.", "Кладу в сумку.", "Начался подъём.", "Подъём.", "Вдоль тропы есть перила.",
    "Здесь перила.", "Держусь за перила рукой.", "Держусь за перила.", "Подъём всё продолжается.", "Склон крутой.",
    "Немного тяжело.", "Туда пройти нельзя.", "Нельзя.", "Там перегорожено забором.", "Забор",
    "Здесь карта.", "Проверяю, где я сейчас.", "Проверяю, где я.", "Здесь сложены камни.", "Корейцы верят: если сложить камни повыше,",
    "желание сбудется.", "Поднимаю один камень.", "Я тоже кладу один камень.", "В корейских горах есть тренажёры.", "Здесь тренажёры.",
    "Поворачиваю корпус влево и вправо.", "Влево и вправо.", "Теперь спускаюсь с горы.", "Мужчина идёт босиком.", "Идёт босиком.",
    "Спускаюсь дальше.", "Три женщины", "болтают.", "Три женщины болтают.", "Распустились цветы.",
    "Пчела села на цветок.", "Стоило подойти ближе — она улетела.", "По дороге домой встретилась кошка.", "Кошка.", "Закрывает глаза.",
    "Кажется, хочет спать.", "Ужасно милая.", "Друзья, сегодня", "хочу дать вам один совет.", "В корейском 3000 слов —",
    "если знать всего 3000 слов,", "слушать и говорить можно без всяких проблем.", "А эти слова отдельно…", "учить не нужно.", "Просто регулярно смотрите мои видео,",
    "и однажды вы заметите, что запомнили их сами собой.", "Смотрите расслабленно.", "Мучить себя стрессом…", "Даже если медленно, но регулярно,", "вы обязательно заговорите по-корейски хорошо.",
    "Увидимся в следующем видео!",
]

T["vi"] = [
    "Xin chào mọi người. Mình là Mino.", "Hôm nay thời tiết đẹp nên", "mình đã lên núi.", "Thời tiết mát mẻ,", "gió thổi vừa phải,",
    "rất hợp để tập thể dục.", "Đây là biển chỉ dẫn.", "Mình đi theo hướng biển chỉ dẫn.", "Phía đối diện, có hai cô đang đi tới.", "Đi một lúc thì có cầu thang.",
    "Có cầu thang.", "Mình leo cầu thang.", "Đi một lúc thì khát nước.", "Mình mang cà phê từ nhà,", "mình sẽ uống cà phê.",
    "Lấy bình giữ nhiệt ra khỏi túi.", "Lấy bình giữ nhiệt ra.", "Cà phê ở trong bình giữ nhiệt.", "Vặn nắp để mở.", "Uống cà phê. Uống cà phê.",
    "Đóng nắp lại.", "Bỏ vào túi.", "Đến đoạn dốc rồi.", "Đường dốc.", "Bên cạnh đường có lan can.",
    "Có lan can.", "Lấy tay nắm lan can.", "Nắm lan can.", "Vẫn là đường dốc.", "Dốc rất đứng.",
    "Hơi mệt một chút.", "Đằng kia thì không đi được.", "Không đi được.", "Bị chặn bằng hàng rào.", "Hàng rào",
    "Có bản đồ.", "Kiểm tra vị trí của mình bây giờ.", "Kiểm tra vị trí.", "Đá được xếp chồng lên.", "Người Hàn tin rằng nếu xếp đá thật cao",
    "thì điều ước sẽ thành hiện thực.", "Nhặt một hòn đá.", "Mình cũng xếp một hòn đá.", "Núi ở Hàn Quốc có dụng cụ tập thể dục.", "Có dụng cụ tập thể dục.",
    "Xoay eo sang trái, sang phải.", "Sang trái, sang phải.", "Giờ thì xuống núi.", "Một chú đang đi chân trần.", "Đi chân trần.",
    "Tiếp tục đi xuống.", "Ba cô", "đang tám chuyện.", "Ba cô đang tám chuyện.", "Hoa nở rồi.",
    "Con ong đậu trên bông hoa.", "Lại gần thì nó bay mất.", "Trên đường về nhà có một con mèo.", "Mèo.", "Nó nhắm mắt.",
    "Chắc là buồn ngủ.", "Dễ thương quá trời.", "Mọi người ơi, hôm nay", "mình muốn cho các bạn một mẹo.", "Tiếng Hàn, 3.000 từ —",
    "chỉ cần biết 3.000 từ thôi,", "là nghe và nói hoàn toàn không vấn đề gì.", "Và những từ này, riêng lẻ…", "không cần phải học đâu.", "Chỉ cần xem video của mình đều đặn,",
    "một ngày nào đó bạn sẽ tự nhiên nhớ hết.", "Cứ xem thoải mái thôi.", "Tự tạo áp lực cho mình…", "Dù chậm, nhưng đều đặn,", "các bạn nhất định sẽ giỏi tiếng Hàn.",
    "Hẹn gặp lại ở video sau nhé!",
]

T["es"] = [
    "Hola a todos. Soy Mino.", "Hoy hace buen tiempo, así que", "vine a la montaña.", "El clima está fresquito,", "el viento sopla justo bien,",
    "perfecto para hacer ejercicio.", "Aquí hay un letrero.", "Voy hacia donde indica el letrero.", "Del otro lado vienen caminando dos señoras.", "Caminando, aparecen unas escaleras.",
    "Hay escaleras.", "Subo las escaleras.", "De tanto caminar, me dio sed.", "Traje café de casa,", "así que voy a tomarlo.",
    "Saco el termo de la bolsa.", "Saco el termo.", "El café está dentro del termo.", "Giro la tapa para abrirlo.", "Tomo café. Tomo café.",
    "Cierro la tapa.", "Lo guardo en la bolsa.", "Apareció una subida.", "Cuesta arriba.", "Junto al camino hay una baranda.",
    "Hay una baranda.", "Me agarro de la baranda con la mano.", "Me agarro de la baranda.", "Sigue siendo cuesta arriba.", "La pendiente es empinada.",
    "Cuesta un poco.", "Por allá no se puede pasar.", "No se puede.", "Está cerrado con una cerca.", "Cerca",
    "Hay un mapa.", "Reviso dónde estoy ahora.", "Reviso mi ubicación.", "Hay piedras apiladas.", "Los coreanos creen que si apilas piedras bien alto,",
    "tu deseo se cumple.", "Recojo una piedra.", "Yo también apilo una piedra.", "En las montañas coreanas hay aparatos para hacer ejercicio.", "Hay aparatos para hacer ejercicio.",
    "Giro la cintura a izquierda y derecha.", "A izquierda y derecha.", "Ahora bajo la montaña.", "Un señor camina descalzo.", "Camina descalzo.",
    "Sigo bajando.", "Tres señoras", "están charlando.", "Tres señoras están charlando.", "Las flores ya florecieron.",
    "Una abeja se posó en la flor.", "Cuando me acerqué, se fue volando.", "De regreso a casa, había un gato.", "Un gatito.", "Cierra los ojos.",
    "Parece que tiene sueño.", "Qué ternura.", "Amigos, hoy", "les quiero dar un consejo.", "En coreano, 3000 palabras…",
    "si sabes solo 3000 palabras,", "no tendrás ningún problema para escuchar y hablar.", "Y estas palabras, por separado…", "no hace falta estudiarlas.", "Si ves mis videos con constancia,",
    "un día te darás cuenta de que ya te las sabes.", "Solo míralos con calma.", "Estresarte por eso…", "Aunque vayas despacio, si eres constante,", "seguro que vas a hablar bien coreano.",
    "¡Nos vemos en el próximo video!",
]

T["fr"] = [
    "Bonjour à tous. C'est Mino !", "Aujourd'hui il fait beau, alors", "me voici à la montagne.", "Il fait frais,", "le vent souffle juste comme il faut,",
    "c'est parfait pour faire du sport.", "Voici un panneau.", "Je vais dans la direction indiquée par le panneau.", "En face, deux dames arrivent à pied.", "En marchant, voici des escaliers.",
    "Il y a des escaliers.", "Je monte les escaliers.", "À force de marcher, j'ai soif.", "J'ai apporté du café de la maison,", "je vais boire du café.",
    "Je sors ma gourde isotherme du sac.", "Je sors la gourde.", "Le café est dans la gourde.", "Je tourne le bouchon pour l'ouvrir.", "Je bois du café. Je bois du café.",
    "Je ferme le bouchon.", "Je la range dans le sac.", "Voilà une montée.", "Une montée.", "Il y a une rambarde le long du chemin.",
    "Il y a une rambarde.", "Je tiens la rambarde avec la main.", "Je tiens la rambarde.", "Ça monte encore.", "La pente est raide.",
    "C'est un peu dur.", "On ne peut pas passer par là.", "On ne peut pas.", "C'est fermé par une clôture.", "Clôture",
    "Il y a une carte.", "Je vérifie où je suis maintenant.", "Je vérifie ma position.", "Des pierres sont empilées.", "Les Coréens croient que si on empile les pierres bien haut,",
    "le vœu se réalise.", "Je ramasse une pierre.", "Moi aussi, j'empile une pierre.", "Dans les montagnes coréennes, il y a des appareils de sport.", "Il y a des appareils de sport.",
    "Je tourne la taille à gauche et à droite.", "À gauche et à droite.", "Maintenant, je descends la montagne.", "Un monsieur marche pieds nus.", "Il marche pieds nus.",
    "Je continue à descendre.", "Trois dames", "papotent.", "Trois dames papotent.", "Les fleurs ont éclos.",
    "Une abeille s'est posée sur une fleur.", "En m'approchant, elle s'est envolée.", "Sur le chemin du retour, il y avait un chat.", "Un chat.", "Il ferme les yeux.",
    "On dirait qu'il a sommeil.", "Trop mignon.", "Tout le monde, aujourd'hui", "je voudrais vous donner une astuce.", "En coréen, 3 000 mots…",
    "si vous connaissez seulement 3 000 mots,", "vous n'aurez aucun problème pour écouter et parler.", "Et ces mots, séparément…", "pas besoin de les étudier.", "Regardez simplement mes vidéos régulièrement,",
    "et un jour, vous les aurez retenus naturellement.", "Regardez tranquillement.", "Vous stresser pour ça…", "Même lentement, avec de la régularité,", "vous parlerez forcément bien coréen.",
    "Rendez-vous dans la prochaine vidéo !",
]

T["de"] = [
    "Hallo zusammen. Hier ist Mino!", "Heute ist schönes Wetter, deshalb", "bin ich in die Berge gekommen.", "Es ist angenehm kühl,", "der Wind weht genau richtig,",
    "perfekt zum Sport machen.", "Hier ist ein Schild.", "Ich gehe in die Richtung, die das Schild zeigt.", "Von der anderen Seite kommen zwei Frauen auf mich zu.", "Beim Gehen kommt eine Treppe.",
    "Hier ist eine Treppe.", "Ich gehe die Treppe hoch.", "Vom Gehen habe ich Durst bekommen.", "Ich habe Kaffee von zu Hause mitgebracht,", "den trinke ich jetzt.",
    "Ich nehme meinen Thermobecher aus der Tasche.", "Ich nehme den Thermobecher heraus.", "Der Kaffee ist im Thermobecher.", "Ich drehe den Deckel auf.", "Ich trinke Kaffee. Ich trinke Kaffee.",
    "Ich mache den Deckel zu.", "Ich stecke ihn in die Tasche.", "Jetzt geht es bergauf.", "Bergauf.", "Neben dem Weg gibt es ein Geländer.",
    "Hier ist ein Geländer.", "Ich halte mich mit der Hand am Geländer fest.", "Ich halte mich am Geländer fest.", "Es geht weiter bergauf.", "Der Hang ist steil.",
    "Ein bisschen anstrengend.", "Dort entlang kann man nicht gehen.", "Geht nicht.", "Es ist mit einem Zaun abgesperrt.", "Zaun",
    "Hier ist eine Karte.", "Ich schaue, wo ich gerade bin.", "Ich prüfe meinen Standort.", "Hier sind Steine aufgestapelt.", "Koreaner glauben: Wenn man Steine hoch aufstapelt,",
    "geht ein Wunsch in Erfüllung.", "Ich hebe einen Stein auf.", "Ich lege auch einen Stein dazu.", "Auf koreanischen Bergen gibt es Fitnessgeräte.", "Hier sind Fitnessgeräte.",
    "Ich drehe die Hüfte nach links und rechts.", "Nach links und rechts.", "Jetzt gehe ich den Berg hinunter.", "Ein Mann läuft barfuß.", "Er läuft barfuß.",
    "Ich gehe weiter hinunter.", "Drei Frauen", "plaudern miteinander.", "Drei Frauen plaudern miteinander.", "Die Blumen blühen.",
    "Eine Biene hat sich auf eine Blume gesetzt.", "Als ich näher kam, flog sie weg.", "Auf dem Heimweg war da eine Katze.", "Eine Katze.", "Sie schließt die Augen.",
    "Sie ist wohl müde.", "Sooo süß.", "Leute, heute", "möchte ich euch einen Tipp geben.", "Im Koreanischen: 3.000 Wörter —",
    "wenn ihr nur 3.000 Wörter kennt,", "habt ihr beim Hören und Sprechen überhaupt keine Probleme.", "Und diese Wörter extra…", "müsst ihr nicht lernen.", "Schaut einfach regelmäßig meine Videos,",
    "dann habt ihr sie eines Tages ganz natürlich gelernt.", "Schaut einfach ganz entspannt.", "Mit Stress…", "Auch wenn es langsam geht – wenn ihr dranbleibt,", "werdet ihr bestimmt gut Koreanisch sprechen.",
    "Bis zum nächsten Video!",
]

T["ar"] = [
    "مرحبًا بالجميع. أنا مينو.", "الطقس جميل اليوم، لذلك", "جئت إلى الجبل.", "الجو منعش،", "والرياح تهب باعتدال،",
    "إنه مثالي لممارسة الرياضة.", "هذه لافتة.", "أمشي في الاتجاه الذي تشير إليه اللافتة.", "من الجهة المقابلة، تأتي سيدتان تمشيان.", "أثناء المشي، ظهر درج.",
    "هناك درج.", "أصعد الدرج.", "بعد المشي، أشعر بالعطش.", "أحضرت القهوة من البيت،", "سأشرب القهوة.",
    "أُخرج الكوب الحراري من الحقيبة.", "أُخرج الكوب الحراري.", "القهوة داخل الكوب الحراري.", "أدير الغطاء لأفتحه.", "أشرب القهوة. أشرب القهوة.",
    "أغلق الغطاء.", "أضعه في الحقيبة.", "ظهر طريق صاعد.", "طريق صاعد.", "بجانب الطريق يوجد درابزين.",
    "يوجد درابزين.", "أمسك الدرابزين بيدي.", "أمسك الدرابزين.", "الطريق لا يزال صاعدًا.", "المنحدر شديد.",
    "الأمر متعب قليلًا.", "لا يمكن المرور من هناك.", "لا يمكن.", "إنه مغلق بسياج.", "سياج",
    "هناك خريطة.", "أتحقق من مكاني الآن.", "أتحقق من الموقع.", "هناك حجارة مكدّسة.", "يؤمن الكوريون أنه إذا كُدّست الحجارة عاليًا،",
    "تتحقق الأمنية.", "ألتقط حجرًا.", "أنا أيضًا أضع حجرًا.", "في جبال كوريا توجد أجهزة رياضية.", "توجد أجهزة رياضية.",
    "أدير خصري يمينًا ويسارًا.", "يمينًا ويسارًا.", "الآن أنزل من الجبل.", "رجل يمشي حافي القدمين.", "يمشي حافي القدمين.",
    "أواصل النزول.", "ثلاث سيدات", "يتبادلن الأحاديث.", "ثلاث سيدات يتبادلن الأحاديث.", "تفتّحت الأزهار.",
    "حطّت نحلة على زهرة.", "عندما اقتربت، طارت بعيدًا.", "في طريق العودة إلى البيت، كانت هناك قطة.", "قطة.", "تغمض عينيها.",
    "يبدو أنها نعسانة.", "لطيفة جدًا.", "أصدقائي، اليوم", "أريد أن أقدّم لكم نصيحة.", "في اللغة الكورية، 3000 كلمة —",
    "إذا عرفتم 3000 كلمة فقط،", "فلن تواجهوا أي مشكلة في الاستماع والتحدث.", "وهذه الكلمات، بشكل منفصل…", "لا داعي لدراستها.", "فقط شاهدوا فيديوهاتي بانتظام،",
    "وذات يوم ستجدون أنكم حفظتموها بشكل طبيعي.", "شاهدوا براحة فقط.", "مع الضغط والتوتر…", "حتى لو تقدّمتم ببطء، مع الاستمرار", "ستتقنون الكورية بالتأكيد.",
    "أراكم في الفيديو القادم!",
]

T["ja"] = [
    "みなさん、こんにちは。ミノです。", "今日は天気がいいので、", "山に来ました。", "天気も涼しくて、", "風もちょうどよく吹いていて、",
    "運動するのにぴったりです。", "案内板です。", "案内板が指す方向に進みます。", "向こうから、おばさんが二人歩いてきます。", "歩いていると、階段があります。",
    "階段があります。", "階段を上ります。", "歩いていたら、のどが渇きました。", "家からコーヒーを持ってきたので、", "コーヒーを飲みます。",
    "かばんからタンブラーを出します。", "タンブラーを出します。", "コーヒーがタンブラーの中に入っています。", "ふたを回して開けます。", "コーヒーを飲みます。コーヒーを飲みます。",
    "ふたを閉めます。", "かばんに入れます。", "上り坂が出てきました。", "上り坂。", "道の横に手すりがあります。",
    "手すりがあります。", "手すりを手でつかみます。", "手すりをつかみます。", "ずっと上り坂です。", "坂が急です。",
    "ちょっと疲れます。", "あっちには行けません。", "行けません。", "フェンスでふさがれています。", "フェンス",
    "地図があります。", "今いる場所を確認します。", "場所を確認します。", "石が積まれています。", "韓国の人たちは、石を高く積むと",
    "願いがかなうと信じています。", "石をひとつ拾います。", "わたしも石をひとつ積みます。", "韓国の山には運動器具があります。", "運動器具があります。",
    "腰を左右にひねります。", "左右にひねります。", "では、山を下ります。", "おじさんが裸足で歩いています。", "裸足で歩いています。",
    "どんどん下ります。", "おばさんが三人", "おしゃべりしています。", "おばさんが三人、おしゃべりしています。", "花が咲きました。",
    "ハチが花にとまりました。", "近づいたら、飛んでいきました。", "帰り道にネコがいました。", "ネコ。", "目を閉じています。",
    "眠いみたいです。", "すごくかわいいです。", "みなさん、今日は", "ひとつアドバイスをしたいと思います。", "韓国語は、単語3000個——",
    "3000個だけ知っていれば、", "聞くのも話すのも全然問題ありません。", "そして、これらの単語を別に", "勉強する必要はありません。", "わたしの動画をコツコツ見ていれば、",
    "ある日自然に覚えているはずです。", "気楽に見てくださいね。", "わざわざストレスを感じながら", "ゆっくりでも、続けていれば", "みなさんはきっと韓国語が上手になります。",
    "では、次の動画で会いましょう。",
]

T["ms"] = [
    "Hai semua. Saya Mino.", "Hari ini cuaca baik, jadi", "saya datang ke gunung.", "Cuaca pun sejuk,", "angin bertiup sederhana,",
    "sangat sesuai untuk bersenam.", "Ini papan tanda.", "Saya pergi ke arah yang ditunjukkan papan tanda.", "Dari arah bertentangan, dua orang mak cik berjalan ke arah saya.", "Sambil berjalan, ada tangga.",
    "Ada tangga.", "Saya naik tangga.", "Lepas berjalan, saya rasa dahaga.", "Saya bawa kopi dari rumah,", "saya nak minum kopi.",
    "Saya keluarkan tumbler dari beg.", "Saya keluarkan tumbler.", "Kopi ada di dalam tumbler.", "Saya pusing penutup untuk membukanya.", "Saya minum kopi. Saya minum kopi.",
    "Saya tutup penutupnya.", "Saya masukkan ke dalam beg.", "Ada jalan mendaki.", "Jalan mendaki.", "Di tepi jalan ada pemegang tangan.",
    "Ada pemegang tangan.", "Saya pegang pemegang dengan tangan.", "Saya pegang pemegang.", "Jalan terus mendaki.", "Cerunnya curam.",
    "Agak memenatkan.", "Ke sana tak boleh lalu.", "Tak boleh lalu.", "Ia dihalang dengan pagar.", "Pagar",
    "Ada peta.", "Saya semak lokasi saya sekarang.", "Semak lokasi.", "Batu-batu disusun bertimbun.", "Orang Korea percaya, jika batu disusun tinggi,",
    "hajat akan tercapai.", "Saya kutip seketul batu.", "Saya juga susun seketul batu.", "Di gunung Korea ada alat senaman.", "Ada alat senaman.",
    "Saya pusingkan pinggang ke kiri dan kanan.", "Ke kiri dan kanan.", "Sekarang saya turun gunung.", "Seorang pak cik berjalan berkaki ayam.", "Berjalan berkaki ayam.",
    "Terus turun.", "Tiga orang mak cik", "sedang berbual.", "Tiga orang mak cik sedang berbual.", "Bunga dah mekar.",
    "Lebah hinggap di atas bunga.", "Bila saya dekat, ia terbang pergi.", "Dalam perjalanan pulang, ada kucing.", "Kucing.", "Ia pejamkan mata.",
    "Nampaknya mengantuk.", "Comel sangat.", "Semua, hari ini", "saya nak beri satu tip.", "Bahasa Korea, 3,000 perkataan —",
    "kalau tahu 3,000 perkataan saja,", "langsung tiada masalah untuk mendengar dan bercakap.", "Dan perkataan-perkataan ini, secara berasingan…", "tak perlu dipelajari.", "Cukup tonton video saya secara konsisten,",
    "satu hari nanti anda akan hafal secara semula jadi.", "Tonton saja dengan santai.", "Sampai tertekan…", "Walaupun perlahan, asalkan konsisten,", "anda pasti akan pandai berbahasa Korea.",
    "Jumpa lagi dalam video seterusnya!",
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
    assert len(KO) == len(set(KO)) == 76
    for lang, rows in T.items():
        assert len(rows) == len(KO), (lang, len(rows))
    idx = {k: i for i, k in enumerate(KO)}
    cues = parse(SRC)
    for _, key in cues:
        assert key in idx, f"번역표에 없는 문장: {key!r}"
    for lang, rows in T.items():
        out = "\n\n".join(f"{time}\n{rows[idx[key]]}" for time, key in cues) + "\n"
        path = os.path.join(HERE, f"S003_captions.{lang}.sbv")
        with open(path, "w", encoding="utf-8", newline="\r\n") as f:  # 원본과 같은 CRLF
            f.write(out)
        # 검증: 타임코드 개수·값이 원본과 같은지
        assert [t for t, _ in parse(path)] == [t for t, _ in cues], lang
        print(f"{lang}: {len(cues)}줄 OK")


if __name__ == "__main__":
    main()
