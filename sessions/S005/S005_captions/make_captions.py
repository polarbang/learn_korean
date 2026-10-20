"""S005_captions.kr.sbv(한국어)를 13개 언어로 옮긴 .sbv 파일 생성.

타임코드·줄 구성은 원본 그대로 두고, 자막 문장만 언어별 번역으로 바꾼다.
번역은 문장 단위 표(KO 순서와 같은 순서)로 관리한다. 원본에 없는 문장이 있으면 에러.
실행: python make_captions.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "S005_captions.kr.sbv")

KO = [
    "안녕하세요. 미노예요.", "저는 오늘 다른 도시에 볼 일이 생겨서", "다른 도시에 가요.", "지금은 오후 2시인데", "7시, 8시",
    "7, 8시쯤에 버스를 타고 갈 거예요.", "버스를 타고 갈 거예요.", "한국에는 버스들이 모여 있는 장소가 있어요.", "터미널이라고 불러요. 버스 터미널.", "버스 터미널에 가면 버스가 엄청 많이 있어요.",
    "그중에서 자기가 가고 싶은", "지역으로 가는 버스를", "골라서 타면 돼요.", "그럼 한번 같이 가볼까요?", "지하철을 타고 터미널이 있는 역에 도착했어요.",
    "나가는 곳", "나가는 곳 방향을 따라가면 터미널로 갈 수 있어요.", "한국 사람들은 에스컬레이터를 타면", "항상 오른쪽에 서요.", "왼쪽은 걸어서 올라가는 사람들이 이용해요.",
    "지하철에서 나갈 때는 카드를 찍고 나가요.", "여기에 카드를 찍으면 돼요.", "이제 거의 다 왔어요.", "표지판이 가리키는 방향으로 조금만 더 가면", "터미널이 있어요.",
    "버스 터미널에 도착했어요.", "매표소에서 티켓을 살 수 있어요.", "무인 매표소예요.", "세 개가 붙어 있어요.", "티켓을 사거나",
    "온라인으로 미리 구입한 티켓을 출력해요.", "한국어를 몰라도", "영어, 중국어, 일본어로 바꿔서 볼 수 있어요.", "먼저 어디로 갈지를 골라요.", "도착지를 골라요. 도착지.",
    "도착지를 누르면", "갈 수 있는 곳들이 쭉 나와요.", "도착지를 고르고 나면", "시간 순서대로", "탈 수 있는 버스가 나와요.",
    "9시", "10시 30분", "11시 55분", "세 개의 버스가 있어요.", "버스를 선택하면 어디에 앉을지 골라요.",
    "이미 X 표시가 있는 곳은 못 골라요.", "다른 사람이 이미 예매한 좌석이에요.", "번호가 남아 있는 좌석 중에서 골라요.", "좌석을 고르고", "어린이인지 어른인지 고르고",
    "결제하면 돼요.", "저는 핸드폰 앱으로 미리 예매를 했어요.", "고속버스 티머니라는 앱이에요.", "8시 20분에 출발하는 버스를 예매했어요", "QR코드를 버스 탈 때 찍으면 돼요.",
    "가는데 1시간 50분이 걸려요.", "좌석은 7번 좌석이에요.", "사람들이 버스 출발을 기다리고 있어요.", "의자에 앉아서 기다리고 있어요.", "음식점이 많이 있어요.",
    "버스를 기다리다가 배가 고프면 밥을 먹어요.", "만두를 팔아요.", "국밥을 팔아요.", "밥을 먹고 나서 도넛도 먹을 수 있어요.", "8시 14분이에요.",
    "제가 타는 버스가 출발하기까지", "아직 5분 남았어요.", "자리에 앉아서 기다려요.", "버스를 타러 승강장으로 나가요.", "많은 버스가 기다리고 있어요.",
    "오늘 제가 탈 버스는 이 버스예요.", "버스에 타서 티켓을 찍어요.", "티켓을 찍어요.", "좌석 번호를 확인해요.", "좌석 번호를 확인하고 자리에 앉아요.",
    "8시 20분이에요.", "이제 버스가 출발해요.", "야간 버스는 출발하면 불을 꺼요.", "좌석 사이에 커튼이 있어요.", "커튼을 쳐요.",
    "커튼을 치면 프라이버시를 지킬 수 있어서 좋아요.", "좌석을 뒤로 내릴 수 있어요.", "끝까지 내리면 완전히 누워서 갈 수 있어요.", "저는 항상 버스를 타면 누워서 자요.", "항상 누워서 자요.",
    "10시 8분이에요.", "예상보다 2분 빨리 도착했어요.", "도착하면 버스 안 불을 켜요.", "이제 버스에서 내려요.", "버스에서 내려요.",
    "시간이 늦어서 사람이 거의 없어요.", "이제 빨리 숙소에 가서 쉬어야겠어요.", "다음 영상에서 만나요.",
]
# "갈 수 있는 곳들이 쭉 나와요."는 원본에서 두 번 연달아 나온다 (번역도 같은 문장 두 번).
# 출발 시각(8시 20분 등)은 저녁이므로, 24시간 표기가 자연스러운 fr·de는 20 h 20 / 20:20 Uhr로 옮겼다.
# 무인 매표소 화면의 9시·10시 30분·11시 55분은 오전·오후를 알 수 없어 그대로 둔다.

T = {}

T["en"] = [
    "Hello. I'm Mino.", "Today I have something to take care of in another city,", "so I'm going to another city.", "It's 2 p.m. right now, but", "7, 8 o'clock…",
    "Around 7 or 8, I'm going to take a bus there.", "I'm going to take a bus.", "In Korea, there's a place where lots of buses gather.", "It's called a terminal. A bus terminal.", "At a bus terminal, there are so many buses.",
    "Out of all of them, the area you want to go to —", "pick the bus that goes to that area", "and just get on.", "So, shall we go together?", "I took the subway and arrived at the station with the terminal.",
    "Exit", "If you follow the Exit signs, you can get to the terminal.", "When Koreans ride an escalator,", "they always stand on the right.", "The left side is for people walking up.",
    "When you leave the subway, you tap your card on the way out.", "You just tap your card here.", "We're almost there.", "If you go a little farther the way the sign points,", "there's the terminal.",
    "We've arrived at the bus terminal.", "You can buy tickets at the ticket office.", "These are self-service ticket machines.", "There are three of them side by side.", "You can buy a ticket",
    "or print a ticket you bought online in advance.", "Even if you don't know Korean,", "you can switch it to English, Chinese or Japanese.", "First, you choose where you're going.", "You choose the destination. Destination.",
    "When you tap Destination,", "all the places you can go show up.", "Once you've chosen a destination,", "in order of time,", "the buses you can take show up.",
    "9:00", "10:30", "11:55", "There are three buses.", "When you choose a bus, you choose where to sit.",
    "You can't choose the seats that already have an X.", "Those are seats someone else has already booked.", "You choose from the seats that still show a number.", "Choose your seat,", "choose child or adult,",
    "and just pay.", "I booked in advance with a phone app.", "It's an app called Express Bus T-money.", "I booked the bus leaving at 8:20.", "You just scan the QR code when you get on the bus.",
    "It takes 1 hour 50 minutes to get there.", "My seat is seat number 7.", "People are waiting for their buses to leave.", "They're sitting on chairs and waiting.", "There are lots of restaurants.",
    "If you get hungry while waiting for the bus, you eat here.", "They sell mandu (Korean dumplings).", "They sell gukbap (Korean rice soup).", "After eating, you can have a donut, too.", "It's 8:14.",
    "Until my bus leaves,", "there are still 5 minutes left.", "I sit down and wait.", "I head out to the platform to catch the bus.", "Lots of buses are waiting.",
    "This is the bus I'm taking today.", "I get on the bus and scan my ticket.", "I scan my ticket.", "I check the seat number.", "I check the seat number and sit down.",
    "It's 8:20.", "Now the bus is leaving.", "On night buses, they turn off the lights once the bus leaves.", "There are curtains between the seats.", "I draw the curtain.",
    "Drawing the curtain gives you privacy, which is nice.", "You can lean the seat back.", "If you lean it all the way back, you can lie down completely.", "I always lie down and sleep when I take a bus.", "I always lie down and sleep.",
    "It's 10:08.", "We arrived 2 minutes earlier than expected.", "When we arrive, they turn the lights on in the bus.", "Now I get off the bus.", "I get off the bus.",
    "It's late, so there's hardly anyone around.", "I should hurry to where I'm staying and rest.", "See you in the next video!",
]

T["zh-Hans"] = [
    "大家好，我是米诺。", "今天我在别的城市有点事，", "所以要去别的城市。", "现在是下午2点，", "7点、8点……",
    "我打算7、8点左右坐大巴去。", "坐大巴去。", "在韩国，有一个很多大巴聚在一起的地方。", "叫做客运站。巴士客运站。", "去了客运站，会有超级多的大巴。",
    "在这些大巴中，自己想去的", "地区的那辆大巴，", "选好坐上去就行了。", "那我们一起去看看吧？", "坐地铁到了有客运站的那一站。",
    "出口", "跟着出口的方向走，就能到客运站。", "韩国人坐扶梯的时候，", "总是站在右边。", "左边是留给走着上去的人用的。",
    "出地铁的时候要刷卡出站。", "在这里刷卡就行了。", "现在快到了。", "朝着指示牌指的方向再走一点点，", "就是客运站了。",
    "到巴士客运站了。", "在售票处可以买票。", "这是自助售票机。", "三台连在一起。", "可以买票，",
    "也可以打印提前在网上买好的票。", "就算不会韩语，", "也可以切换成英语、中文、日语来看。", "首先选要去哪里。", "选目的地。目的地。",
    "点一下目的地，", "能去的地方就会一排列出来。", "选好目的地后，", "按时间顺序", "会显示可以坐的大巴。",
    "9点", "10点30分", "11点55分", "有三班大巴。", "选好大巴后，选要坐哪里。",
    "已经有X标记的位置不能选。", "那是别人已经预订的座位。", "在还显示号码的座位中选。", "选好座位，", "选是儿童还是成人，",
    "然后付款就行了。", "我已经用手机App提前预订了。", "是一个叫“高速巴士T-money”的App。", "我订了8点20分出发的大巴。", "上车的时候扫一下二维码就行了。",
    "到那里要1小时50分钟。", "座位是7号座。", "大家在等大巴出发。", "坐在椅子上等着。", "有很多餐厅。",
    "等车的时候饿了就吃饭。", "有卖韩式饺子（mandu）。", "有卖汤饭（gukbap）。", "吃完饭还可以吃甜甜圈。", "现在8点14分。",
    "离我坐的大巴出发", "还有5分钟。", "坐在位子上等。", "去站台坐大巴。", "很多大巴在等着。",
    "今天我要坐的就是这辆大巴。", "上车后扫票。", "扫票。", "确认座位号。", "确认座位号后坐下。",
    "现在8点20分。", "大巴出发了。", "夜间大巴出发后会关灯。", "座位之间有帘子。", "拉上帘子。",
    "拉上帘子就能保护隐私，很好。", "座椅可以往后放。", "放到底的话，就能完全躺着去。", "我坐大巴的时候总是躺着睡觉。", "总是躺着睡。",
    "现在10点08分。", "比预计早到了2分钟。", "到站后会打开车里的灯。", "现在下车。", "下车。",
    "因为时间晚了，几乎没有人。", "现在得赶紧去住的地方休息了。", "那我们下个视频见！",
]

T["id"] = [
    "Halo. Aku Mino.", "Hari ini aku ada urusan di kota lain,", "jadi aku pergi ke kota lain.", "Sekarang jam 2 siang, tapi", "jam 7, jam 8…",
    "Sekitar jam 7 atau 8, aku akan naik bus ke sana.", "Aku akan naik bus.", "Di Korea, ada tempat di mana banyak bus berkumpul.", "Namanya terminal. Terminal bus.", "Kalau ke terminal bus, ada banyak sekali bus.",
    "Dari semua itu, ke daerah yang ingin kamu tuju —", "bus yang pergi ke daerah itu,", "tinggal pilih lalu naik.", "Yuk, kita pergi bareng?", "Aku naik kereta bawah tanah dan sampai di stasiun yang ada terminalnya.",
    "Pintu keluar", "Kalau ikuti arah pintu keluar, kamu bisa sampai ke terminal.", "Orang Korea kalau naik eskalator,", "selalu berdiri di sebelah kanan.", "Sebelah kiri dipakai orang yang naik sambil berjalan.",
    "Waktu keluar dari stasiun, kita tap kartu lalu keluar.", "Tinggal tap kartu di sini.", "Sekarang sudah hampir sampai.", "Kalau jalan sedikit lagi ke arah yang ditunjuk papan,", "ada terminalnya.",
    "Sudah sampai di terminal bus.", "Kamu bisa beli tiket di loket tiket.", "Ini mesin tiket mandiri.", "Ada tiga berjejer.", "Bisa beli tiket",
    "atau mencetak tiket yang sudah dibeli online sebelumnya.", "Walaupun tidak bisa bahasa Korea,", "kamu bisa ganti ke bahasa Inggris, Mandarin, atau Jepang.", "Pertama, pilih mau ke mana.", "Pilih tujuan. Tujuan.",
    "Kalau tekan Tujuan,", "tempat-tempat yang bisa dituju muncul berderet.", "Setelah memilih tujuan,", "sesuai urutan waktu,", "muncul bus yang bisa dinaiki.",
    "Jam 9", "Jam 10.30", "Jam 11.55", "Ada tiga bus.", "Setelah pilih bus, pilih mau duduk di mana.",
    "Kursi yang sudah ada tanda X tidak bisa dipilih.", "Itu kursi yang sudah dipesan orang lain.", "Pilih dari kursi yang nomornya masih ada.", "Pilih kursi,", "pilih anak-anak atau dewasa,",
    "lalu tinggal bayar.", "Aku sudah pesan duluan lewat aplikasi di HP.", "Nama aplikasinya Express Bus T-money.", "Aku pesan bus yang berangkat jam 8.20.", "Tinggal scan QR code waktu naik bus.",
    "Perjalanannya 1 jam 50 menit.", "Kursiku nomor 7.", "Orang-orang sedang menunggu bus berangkat.", "Mereka duduk di kursi sambil menunggu.", "Ada banyak tempat makan.",
    "Kalau lapar sambil menunggu bus, makan di sini.", "Ada yang jual mandu (pangsit Korea).", "Ada yang jual gukbap (nasi sup Korea).", "Setelah makan, bisa makan donat juga.", "Sekarang jam 8.14.",
    "Sampai bus yang aku naiki berangkat,", "masih ada 5 menit lagi.", "Aku duduk dan menunggu.", "Aku keluar ke peron untuk naik bus.", "Banyak bus sedang menunggu.",
    "Bus yang akan aku naiki hari ini adalah bus ini.", "Naik bus, lalu scan tiket.", "Scan tiket.", "Cek nomor kursi.", "Cek nomor kursi lalu duduk.",
    "Sekarang jam 8.20.", "Sekarang busnya berangkat.", "Bus malam mematikan lampu begitu berangkat.", "Ada tirai di antara kursi.", "Aku tutup tirainya.",
    "Kalau tirai ditutup, privasi terjaga, jadi enak.", "Kursinya bisa direbahkan ke belakang.", "Kalau direbahkan sampai habis, bisa benar-benar berbaring.", "Aku selalu tidur berbaring kalau naik bus.", "Selalu tidur berbaring.",
    "Sekarang jam 10.08.", "Sampai 2 menit lebih cepat dari perkiraan.", "Begitu sampai, lampu di dalam bus dinyalakan.", "Sekarang aku turun dari bus.", "Turun dari bus.",
    "Karena sudah malam, hampir tidak ada orang.", "Sekarang aku harus cepat ke penginapan dan istirahat.", "Sampai jumpa di video berikutnya!",
]

T["pt-BR"] = [
    "Oi. Eu sou Mino.", "Hoje surgiu um compromisso em outra cidade,", "então vou para outra cidade.", "Agora são 2 da tarde, mas", "7, 8 horas…",
    "Lá pelas 7 ou 8, vou pegar um ônibus para lá.", "Vou pegar um ônibus.", "Na Coreia, tem um lugar onde vários ônibus ficam reunidos.", "Chama-se terminal. Terminal de ônibus.", "No terminal de ônibus, tem muitos ônibus mesmo.",
    "Entre eles, para a região aonde você quer ir —", "o ônibus que vai para essa região,", "é só escolher e embarcar.", "Então, vamos juntos?", "Peguei o metrô e cheguei à estação onde fica o terminal.",
    "Saída", "Seguindo a direção da Saída, dá para chegar ao terminal.", "Quando os coreanos pegam a escada rolante,", "sempre ficam do lado direito.", "O lado esquerdo é para quem sobe andando.",
    "Para sair do metrô, você passa o cartão e sai.", "É só passar o cartão aqui.", "Agora estamos quase lá.", "Andando só mais um pouco na direção que a placa indica,", "fica o terminal.",
    "Chegamos ao terminal de ônibus.", "Dá para comprar passagens na bilheteria.", "Estas são as bilheterias automáticas.", "São três, uma do lado da outra.", "Você pode comprar a passagem",
    "ou imprimir a passagem que comprou online antes.", "Mesmo sem saber coreano,", "dá para mudar para inglês, chinês ou japonês.", "Primeiro, você escolhe para onde vai.", "Escolhe o destino. Destino.",
    "Ao tocar em Destino,", "aparecem todos os lugares para onde dá para ir.", "Depois de escolher o destino,", "em ordem de horário,", "aparecem os ônibus que você pode pegar.",
    "9h", "10h30", "11h55", "Tem três ônibus.", "Depois de escolher o ônibus, você escolhe onde vai sentar.",
    "Não dá para escolher os lugares que já têm um X.", "São assentos que outras pessoas já reservaram.", "Você escolhe entre os assentos que ainda mostram o número.", "Escolha o assento,", "escolha criança ou adulto",
    "e é só pagar.", "Eu já reservei antes pelo app no celular.", "É um app chamado Express Bus T-money.", "Reservei o ônibus que sai às 8h20.", "É só escanear o QR code quando for entrar no ônibus.",
    "A viagem leva 1 hora e 50 minutos.", "Meu assento é o número 7.", "As pessoas estão esperando o ônibus sair.", "Estão sentadas nas cadeiras, esperando.", "Tem vários restaurantes.",
    "Se der fome enquanto espera o ônibus, você come aqui.", "Vendem mandu (bolinho coreano recheado).", "Vendem gukbap (sopa coreana com arroz).", "Depois de comer, dá para comer um donut também.", "São 8h14.",
    "Até o meu ônibus sair,", "ainda faltam 5 minutos.", "Eu sento e espero.", "Vou para a plataforma pegar o ônibus.", "Tem muitos ônibus esperando.",
    "O ônibus que vou pegar hoje é este aqui.", "Entro no ônibus e escaneio a passagem.", "Escaneio a passagem.", "Confiro o número do assento.", "Confiro o número do assento e me sento.",
    "São 8h20.", "Agora o ônibus vai partir.", "No ônibus noturno, apagam as luzes quando ele parte.", "Tem cortinas entre os assentos.", "Fecho a cortina.",
    "Fechando a cortina, dá para ter privacidade, e isso é bom.", "Dá para reclinar o assento.", "Reclinando até o fim, dá para viajar totalmente na horizontal.", "Eu sempre deito e durmo quando pego ônibus.", "Sempre deito e durmo.",
    "São 10h08.", "Chegamos 2 minutos antes do previsto.", "Quando chega, acendem as luzes dentro do ônibus.", "Agora desço do ônibus.", "Desço do ônibus.",
    "Como já está tarde, quase não tem ninguém.", "Agora preciso ir logo para a hospedagem descansar.", "Até o próximo vídeo!",
]

T["fil"] = [
    "Hello. Ako si Mino.", "Ngayon, may aasikasuhin ako sa ibang lungsod,", "kaya pupunta ako sa ibang lungsod.", "Alas-2 ng hapon ngayon, pero", "alas-7, alas-8…",
    "Mga alas-7 o alas-8, sasakay ako ng bus papunta roon.", "Sasakay ako ng bus.", "Sa Korea, may lugar kung saan nagtitipon ang maraming bus.", "Tinatawag itong terminal. Bus terminal.", "Pag pumunta ka sa bus terminal, napakaraming bus.",
    "Sa lahat ng iyon, sa lugar na gusto mong puntahan —", "ang bus na papunta sa lugar na iyon,", "piliin mo lang at sumakay.", "Tara, sabay tayong pumunta?", "Sumakay ako ng subway at dumating sa istasyon na may terminal.",
    "Exit", "Kung susundan mo ang direksyon ng Exit, makakarating ka sa terminal.", "Kapag sumasakay ng escalator ang mga Koreano,", "lagi silang tumatayo sa kanan.", "Ang kaliwa ay para sa mga taong naglalakad paakyat.",
    "Paglabas ng subway, i-tap ang card bago lumabas.", "I-tap mo lang ang card dito.", "Malapit na tayo.", "Kung lalakad pa nang kaunti sa direksyong itinuturo ng karatula,", "nandoon ang terminal.",
    "Nakarating na tayo sa bus terminal.", "Puwedeng bumili ng ticket sa ticket office.", "Ito ang self-service ticket machine.", "Tatlo ang magkakatabi.", "Puwede kang bumili ng ticket",
    "o mag-print ng ticket na binili mo online nang maaga.", "Kahit hindi ka marunong mag-Korean,", "puwede mong palitan sa English, Chinese o Japanese.", "Una, piliin kung saan pupunta.", "Piliin ang destinasyon. Destinasyon.",
    "Pag pinindot mo ang Destinasyon,", "lalabas lahat ng lugar na puwede mong puntahan.", "Pagkatapos pumili ng destinasyon,", "ayon sa oras,", "lalabas ang mga bus na puwede mong sakyan.",
    "Alas-9", "10:30", "11:55", "May tatlong bus.", "Pag pumili ka ng bus, pipili ka kung saan uupo.",
    "Hindi mo mapipili ang mga upuang may X na.", "Mga upuan iyon na na-book na ng ibang tao.", "Pumili sa mga upuang may numero pa.", "Pumili ng upuan,", "piliin kung bata o adult,",
    "tapos magbayad ka lang.", "Ako, nag-book na ako nang maaga gamit ang app sa phone.", "Ang tawag sa app ay Express Bus T-money.", "Nag-book ako ng bus na aalis nang 8:20.", "I-scan mo lang ang QR code pag sasakay ka na ng bus.",
    "1 oras at 50 minuto ang biyahe.", "Upuan number 7 ang upuan ko.", "Naghihintay ang mga tao na umalis ang bus.", "Nakaupo sila sa mga upuan habang naghihintay.", "Maraming kainan dito.",
    "Kung magutom ka habang naghihintay ng bus, kumain ka rito.", "May nagbebenta ng mandu (Korean dumplings).", "May nagbebenta ng gukbap (Korean na sabaw na may kanin).", "Pagkatapos kumain, puwede ka ring kumain ng donut.", "8:14 na.",
    "Bago umalis ang bus na sasakyan ko,", "may 5 minuto pa.", "Uupo muna ako at maghihintay.", "Lalabas na ako sa platform para sumakay ng bus.", "Maraming bus ang naghihintay.",
    "Ito ang bus na sasakyan ko ngayon.", "Pagsakay sa bus, i-scan ang ticket.", "I-scan ang ticket.", "Tingnan ang numero ng upuan.", "Tingnan ang numero ng upuan at umupo.",
    "8:20 na.", "Aalis na ang bus.", "Sa night bus, pinapatay ang ilaw pag-alis.", "May kurtina sa pagitan ng mga upuan.", "Isasara ko ang kurtina.",
    "Pag isinara ang kurtina, may privacy ka, kaya maganda.", "Puwedeng i-recline ang upuan.", "Pag ni-recline hanggang dulo, puwede kang humiga nang tuluyan.", "Lagi akong nakahiga at natutulog pag sumasakay ng bus.", "Lagi akong nakahiga at natutulog.",
    "10:08 na.", "Dumating kami nang 2 minutong mas maaga kaysa inaasahan.", "Pagdating, binubuksan ang ilaw sa loob ng bus.", "Bababa na ako ng bus.", "Bababa ng bus.",
    "Dahil gabi na, halos walang tao.", "Kailangan ko nang pumunta agad sa tutuluyan ko at magpahinga.", "Sige, kita-kits sa susunod na video!",
]

T["ru"] = [
    "Привет! Я Мино.", "Сегодня у меня появились дела в другом городе,", "поэтому я еду в другой город.", "Сейчас 2 часа дня, но", "в 7, в 8…",
    "Около 7–8 часов я поеду туда на автобусе.", "Поеду на автобусе.", "В Корее есть место, где собирается много автобусов.", "Оно называется терминал. Автовокзал.", "На автовокзале очень-очень много автобусов.",
    "Из них — в тот район, куда вам нужно, —", "выбираете автобус, который туда идёт,", "и садитесь в него.", "Ну что, поедем вместе?", "На метро мы доехали до станции, где находится автовокзал.",
    "Выход", "Если идти по указателям «Выход», можно дойти до автовокзала.", "Корейцы на эскалаторе", "всегда стоят справа.", "Левая сторона — для тех, кто поднимается пешком.",
    "Выходя из метро, прикладываешь карту и выходишь.", "Карту нужно просто приложить вот сюда.", "Мы почти на месте.", "Если пройти ещё немного туда, куда показывает указатель,", "там будет автовокзал.",
    "Вот мы и на автовокзале.", "Билеты можно купить в кассе.", "Это билетные автоматы.", "Их три, стоят рядом.", "Можно купить билет",
    "или распечатать билет, заранее купленный онлайн.", "Даже если вы не знаете корейский,", "можно переключить на английский, китайский или японский.", "Сначала выбираем, куда ехать.", "Выбираем пункт назначения. Пункт назначения.",
    "Нажимаем на пункт назначения —", "и появляется целый список мест, куда можно поехать.", "Когда пункт назначения выбран,", "по порядку времени", "появляются автобусы, на которые можно сесть.",
    "9:00", "10:30", "11:55", "Есть три автобуса.", "Выбрав автобус, выбираем, где сидеть.",
    "Места, где уже стоит X, выбрать нельзя.", "Это места, которые уже забронировали другие люди.", "Выбираем из мест, где ещё виден номер.", "Выбираем место,", "выбираем — ребёнок или взрослый,",
    "и просто оплачиваем.", "У меня билет уже заранее забронирован через приложение в телефоне.", "Приложение называется Express Bus T-money.", "Мой автобус отправляется в 8:20.", "QR-код нужно просто отсканировать при посадке в автобус.",
    "Ехать 1 час 50 минут.", "Моё место — номер 7.", "Люди ждут отправления автобуса.", "Сидят на стульях и ждут.", "Здесь много кафе и ресторанов.",
    "Если, пока ждёшь автобус, проголодаешься — можно поесть здесь.", "Продают манду (корейские пельмени).", "Продают кукпап (корейский суп с рисом).", "После еды можно съесть ещё и пончик.", "Сейчас 8:14.",
    "До отправления моего автобуса", "осталось ещё 5 минут.", "Сажусь и жду.", "Выхожу на платформу, чтобы сесть в автобус.", "Ждёт много автобусов.",
    "Сегодня я еду вот на этом автобусе.", "Захожу в автобус и сканирую билет.", "Сканирую билет.", "Проверяю номер места.", "Проверяю номер места и сажусь.",
    "Сейчас 8:20.", "Автобус отправляется.", "В ночном автобусе после отправления выключают свет.", "Между сиденьями есть шторки.", "Задёргиваю шторку.",
    "Если задёрнуть шторку, есть личное пространство — это удобно.", "Спинку сиденья можно откинуть назад.", "Если откинуть до конца, можно ехать полностью лёжа.", "Я всегда сплю лёжа, когда еду на автобусе.", "Всегда сплю лёжа.",
    "Сейчас 10:08.", "Мы приехали на 2 минуты раньше, чем ожидалось.", "Когда приезжаем, в автобусе включают свет.", "Теперь выхожу из автобуса.", "Выхожу из автобуса.",
    "Уже поздно, поэтому людей почти нет.", "Теперь надо скорее идти туда, где я остановлюсь, и отдохнуть.", "Увидимся в следующем видео!",
]

T["vi"] = [
    "Xin chào. Mình là Mino.", "Hôm nay mình có việc ở thành phố khác,", "nên mình đi đến thành phố khác.", "Bây giờ là 2 giờ chiều, nhưng", "7 giờ, 8 giờ…",
    "Khoảng 7, 8 giờ mình sẽ đi xe buýt.", "Mình sẽ đi xe buýt.", "Ở Hàn Quốc có một nơi tập trung nhiều xe buýt.", "Người ta gọi là bến xe. Bến xe buýt.", "Đến bến xe buýt thì có cực kỳ nhiều xe.",
    "Trong số đó, đến vùng mà mình muốn đi —", "chiếc xe đi đến vùng đó,", "chỉ cần chọn rồi lên xe là được.", "Vậy chúng ta cùng đi thử nhé?", "Mình đi tàu điện ngầm và đến ga có bến xe.",
    "Lối ra", "Đi theo hướng Lối ra là có thể đến bến xe.", "Người Hàn khi đi thang cuốn", "luôn đứng bên phải.", "Bên trái dành cho người đi bộ lên.",
    "Khi ra khỏi tàu điện ngầm, quẹt thẻ rồi ra.", "Chỉ cần quẹt thẻ ở đây là được.", "Bây giờ sắp đến rồi.", "Đi thêm một chút theo hướng biển chỉ dẫn,", "là có bến xe.",
    "Đến bến xe buýt rồi.", "Có thể mua vé ở quầy bán vé.", "Đây là máy bán vé tự động.", "Có ba máy đặt cạnh nhau.", "Có thể mua vé",
    "hoặc in vé đã mua trước trên mạng.", "Dù không biết tiếng Hàn,", "cũng có thể đổi sang tiếng Anh, tiếng Trung, tiếng Nhật để xem.", "Đầu tiên, chọn nơi sẽ đi.", "Chọn điểm đến. Điểm đến.",
    "Bấm vào Điểm đến,", "các nơi có thể đi sẽ hiện ra một loạt.", "Chọn điểm đến xong,", "theo thứ tự thời gian,", "sẽ hiện ra các xe có thể đi.",
    "9 giờ", "10 giờ 30", "11 giờ 55", "Có ba chuyến xe.", "Chọn xe xong thì chọn chỗ ngồi.",
    "Chỗ đã có dấu X thì không chọn được.", "Đó là ghế người khác đã đặt rồi.", "Chọn trong những ghế vẫn còn số.", "Chọn ghế,", "chọn trẻ em hay người lớn,",
    "rồi thanh toán là xong.", "Mình đã đặt trước bằng ứng dụng trên điện thoại.", "Ứng dụng tên là Express Bus T-money.", "Mình đã đặt chuyến xe khởi hành lúc 8 giờ 20.", "Khi lên xe chỉ cần quét mã QR là được.",
    "Đi mất 1 tiếng 50 phút.", "Ghế của mình là ghế số 7.", "Mọi người đang chờ xe khởi hành.", "Họ ngồi trên ghế chờ.", "Có rất nhiều quán ăn.",
    "Nếu đói trong lúc chờ xe thì ăn cơm ở đây.", "Có bán mandu (bánh xếp Hàn Quốc).", "Có bán gukbap (canh cơm Hàn Quốc).", "Ăn cơm xong còn có thể ăn bánh donut nữa.", "Bây giờ là 8 giờ 14.",
    "Cho đến khi xe của mình khởi hành,", "vẫn còn 5 phút.", "Mình ngồi chờ.", "Mình ra bến để lên xe.", "Có nhiều xe buýt đang chờ.",
    "Chiếc xe hôm nay mình đi là chiếc này.", "Lên xe rồi quét vé.", "Quét vé.", "Kiểm tra số ghế.", "Kiểm tra số ghế rồi ngồi xuống.",
    "Bây giờ là 8 giờ 20.", "Xe bắt đầu khởi hành.", "Xe đêm khởi hành là tắt đèn.", "Giữa các ghế có rèm.", "Kéo rèm lại.",
    "Kéo rèm lại thì giữ được sự riêng tư, nên rất thích.", "Ghế có thể ngả ra sau.", "Ngả hết cỡ thì có thể nằm hẳn mà đi.", "Mình đi xe buýt lúc nào cũng nằm ngủ.", "Lúc nào cũng nằm ngủ.",
    "Bây giờ là 10 giờ 8 phút.", "Đến sớm hơn dự kiến 2 phút.", "Đến nơi thì bật đèn trong xe.", "Bây giờ mình xuống xe.", "Xuống xe.",
    "Vì muộn rồi nên gần như không có ai.", "Giờ mình phải mau về chỗ ở nghỉ ngơi thôi.", "Hẹn gặp lại ở video sau nhé!",
]

T["es"] = [
    "Hola. Soy Mino.", "Hoy me surgió algo que hacer en otra ciudad,", "así que voy a otra ciudad.", "Ahora son las 2 de la tarde, pero", "a las 7, a las 8…",
    "Hacia las 7 u 8 voy a ir en autobús.", "Voy a ir en autobús.", "En Corea hay un lugar donde se reúnen muchos autobuses.", "Se llama terminal. Terminal de autobuses.", "En una terminal de autobuses hay muchísimos autobuses.",
    "De todos ellos, a la zona a la que quieres ir —", "eliges el autobús que va a esa zona", "y te subes.", "Entonces, ¿vamos a verlo?", "Tomé el metro y llegué a la estación donde está la terminal.",
    "Salida", "Si sigues la dirección de Salida, puedes llegar a la terminal.", "Cuando los coreanos suben a una escalera mecánica,", "siempre se paran a la derecha.", "La izquierda la usan las personas que suben caminando.",
    "Al salir del metro, pasas la tarjeta y sales.", "Solo tienes que pasar la tarjeta aquí.", "Ya casi llegamos.", "Si caminas un poco más hacia donde indica el letrero,", "está la terminal.",
    "Llegamos a la terminal de autobuses.", "Puedes comprar boletos en la taquilla.", "Estas son las taquillas automáticas.", "Hay tres, una al lado de la otra.", "Puedes comprar un boleto",
    "o imprimir un boleto que compraste antes por internet.", "Aunque no sepas coreano,", "puedes cambiarlo a inglés, chino o japonés.", "Primero, eliges adónde vas.", "Eliges el destino. Destino.",
    "Al tocar Destino,", "aparecen en fila todos los lugares adonde puedes ir.", "Después de elegir el destino,", "en orden de horario", "aparecen los autobuses que puedes tomar.",
    "9:00", "10:30", "11:55", "Hay tres autobuses.", "Al elegir el autobús, eliges dónde sentarte.",
    "No puedes elegir los lugares que ya tienen una X.", "Son asientos que otras personas ya reservaron.", "Eliges entre los asientos que todavía muestran el número.", "Eliges el asiento,", "eliges niño o adulto",
    "y solo pagas.", "Yo reservé antes con una app del celular.", "Es una app que se llama Express Bus T-money.", "Reservé el autobús que sale a las 8:20.", "Solo tienes que escanear el código QR al subir al autobús.",
    "El viaje dura 1 hora y 50 minutos.", "Mi asiento es el número 7.", "La gente está esperando que salga el autobús.", "Esperan en las sillas.", "Hay muchos restaurantes.",
    "Si te da hambre mientras esperas el autobús, comes aquí.", "Venden mandu (empanadillas coreanas).", "Venden gukbap (sopa coreana con arroz).", "Después de comer, también puedes comer una dona.", "Son las 8:14.",
    "Para que salga mi autobús", "todavía faltan 5 minutos.", "Me siento y espero.", "Salgo al andén para tomar el autobús.", "Hay muchos autobuses esperando.",
    "Este es el autobús que voy a tomar hoy.", "Me subo al autobús y escaneo el boleto.", "Escaneo el boleto.", "Reviso el número de asiento.", "Reviso el número de asiento y me siento.",
    "Son las 8:20.", "Ahora el autobús sale.", "En los autobuses nocturnos, apagan la luz al salir.", "Hay cortinas entre los asientos.", "Cierro la cortina.",
    "Si cierras la cortina, tienes privacidad, y eso está muy bien.", "Puedes reclinar el asiento hacia atrás.", "Si lo reclinas hasta el fondo, puedes viajar totalmente en horizontal.", "Yo siempre me acuesto y duermo cuando viajo en autobús.", "Siempre me acuesto y duermo.",
    "Son las 10:08.", "Llegamos 2 minutos antes de lo previsto.", "Al llegar, encienden la luz dentro del autobús.", "Ahora me bajo del autobús.", "Me bajo del autobús.",
    "Como ya es tarde, casi no hay nadie.", "Ahora tengo que ir rápido al alojamiento a descansar.", "¡Nos vemos en el próximo video!",
]

T["fr"] = [
    "Bonjour. C'est Mino !", "Aujourd'hui, j'ai une affaire à régler dans une autre ville,", "alors je vais dans une autre ville.", "Là, il est 14 h, mais", "19 h, 20 h…",
    "Vers 19 h ou 20 h, je vais y aller en bus.", "Je vais y aller en bus.", "En Corée, il y a un endroit où plein de bus sont rassemblés.", "On l'appelle le terminal. La gare routière.", "Dans une gare routière, il y a énormément de bus.",
    "Parmi eux, vers la région où vous voulez aller —", "le bus qui va dans cette région,", "il suffit de le choisir et de monter.", "Alors, on y va ensemble ?", "En métro, nous voici à la station où se trouve la gare routière.",
    "Sortie", "En suivant la direction « Sortie », on peut aller jusqu'à la gare routière.", "Quand les Coréens prennent l'escalator,", "ils se tiennent toujours à droite.", "La gauche, c'est pour les gens qui montent en marchant.",
    "Pour sortir du métro, on badge sa carte et on sort.", "Il suffit de badger sa carte ici.", "On y est presque.", "Si on va encore un petit peu dans la direction du panneau,", "il y a la gare routière.",
    "Nous voici à la gare routière.", "On peut acheter des billets au guichet.", "Ce sont les guichets automatiques.", "Il y en a trois, côte à côte.", "On peut acheter un billet",
    "ou imprimer un billet acheté en ligne à l'avance.", "Même si vous ne parlez pas coréen,", "vous pouvez passer en anglais, chinois ou japonais.", "D'abord, on choisit où on va.", "On choisit la destination. La destination.",
    "Quand on appuie sur Destination,", "tous les endroits où on peut aller s'affichent.", "Une fois la destination choisie,", "par ordre d'horaire,", "s'affichent les bus qu'on peut prendre.",
    "9 h", "10 h 30", "11 h 55", "Il y a trois bus.", "Quand on choisit le bus, on choisit où s'asseoir.",
    "On ne peut pas choisir les places déjà marquées d'un X.", "Ce sont des places que d'autres ont déjà réservées.", "On choisit parmi les places qui affichent encore un numéro.", "On choisit sa place,", "on choisit enfant ou adulte,",
    "et il suffit de payer.", "Moi, j'ai réservé à l'avance avec une appli sur mon téléphone.", "C'est une appli qui s'appelle Express Bus T-money.", "J'ai réservé le bus qui part à 20 h 20.", "Il suffit de scanner le QR code en montant dans le bus.",
    "Le trajet dure 1 h 50.", "Ma place, c'est la place n° 7.", "Les gens attendent le départ du bus.", "Ils attendent sur des chaises.", "Il y a plein de restaurants.",
    "Si on a faim en attendant le bus, on mange ici.", "On vend des mandu (raviolis coréens).", "On vend du gukbap (soupe coréenne au riz).", "Après le repas, on peut aussi manger un donut.", "Il est 20 h 14.",
    "Avant le départ de mon bus,", "il reste encore 5 minutes.", "Je m'assois et j'attends.", "Je sors sur le quai pour prendre le bus.", "Beaucoup de bus attendent.",
    "Le bus que je prends aujourd'hui, c'est celui-ci.", "Je monte dans le bus et je scanne mon billet.", "Je scanne mon billet.", "Je vérifie le numéro de ma place.", "Je vérifie le numéro de ma place et je m'assois.",
    "Il est 20 h 20.", "Le bus part maintenant.", "Dans les bus de nuit, on éteint la lumière au départ.", "Il y a des rideaux entre les sièges.", "Je tire le rideau.",
    "En tirant le rideau, on préserve son intimité, c'est agréable.", "On peut incliner le siège vers l'arrière.", "Si on l'incline à fond, on peut voyager complètement à l'horizontale.", "Moi, quand je prends le bus, je m'allonge toujours pour dormir.", "Je m'allonge toujours pour dormir.",
    "Il est 22 h 08.", "Nous voici arrivés 2 minutes plus tôt que prévu.", "À l'arrivée, on rallume la lumière dans le bus.", "Maintenant, je descends du bus.", "Je descends du bus.",
    "Comme il est tard, il n'y a presque personne.", "Maintenant, je vais vite rejoindre mon logement pour me reposer.", "Rendez-vous dans la prochaine vidéo !",
]

T["de"] = [
    "Hallo. Hier ist Mino!", "Ich habe heute etwas in einer anderen Stadt zu erledigen,", "deshalb fahre ich in eine andere Stadt.", "Jetzt ist es 14 Uhr, aber", "19, 20 Uhr…",
    "Gegen 19 oder 20 Uhr fahre ich mit dem Bus hin.", "Ich fahre mit dem Bus.", "In Korea gibt es einen Ort, an dem viele Busse zusammenkommen.", "Man nennt ihn Terminal. Busterminal.", "Am Busterminal gibt es wahnsinnig viele Busse.",
    "Davon – in die Gegend, in die man fahren möchte –", "den Bus, der in diese Gegend fährt,", "sucht man sich aus und steigt ein.", "Also, sollen wir zusammen hinfahren?", "Mit der U-Bahn sind wir an der Station mit dem Terminal angekommen.",
    "Ausgang", "Wenn man der Richtung „Ausgang“ folgt, kommt man zum Terminal.", "Wenn Koreaner Rolltreppe fahren,", "stehen sie immer rechts.", "Links gehen die Leute, die zu Fuß hochlaufen.",
    "Beim Verlassen der U-Bahn hält man die Karte ans Lesegerät.", "Hier einfach die Karte dranhalten.", "Jetzt sind wir fast da.", "Wenn man noch ein kleines Stück in die Richtung des Schilds geht,", "kommt das Terminal.",
    "Wir sind am Busterminal angekommen.", "Am Ticketschalter kann man Tickets kaufen.", "Das sind Ticketautomaten.", "Es stehen drei nebeneinander.", "Man kann Tickets kaufen",
    "oder vorher online gekaufte Tickets ausdrucken.", "Auch wenn man kein Koreanisch kann,", "kann man auf Englisch, Chinesisch oder Japanisch umstellen.", "Zuerst wählt man, wohin man fährt.", "Man wählt das Ziel. Das Ziel.",
    "Wenn man auf Ziel tippt,", "erscheinen der Reihe nach alle Orte, zu denen man fahren kann.", "Wenn man das Ziel gewählt hat,", "nach Uhrzeit geordnet", "erscheinen die Busse, die man nehmen kann.",
    "9:00 Uhr", "10:30 Uhr", "11:55 Uhr", "Es gibt drei Busse.", "Wenn man einen Bus wählt, wählt man, wo man sitzen möchte.",
    "Plätze, die schon ein X haben, kann man nicht wählen.", "Das sind Plätze, die andere schon gebucht haben.", "Man wählt aus den Plätzen, die noch eine Nummer zeigen.", "Platz wählen,", "Kind oder Erwachsener wählen",
    "und dann einfach bezahlen.", "Ich habe vorher schon per Handy-App gebucht.", "Die App heißt Express Bus T-money.", "Ich habe den Bus um 20:20 Uhr gebucht.", "Den QR-Code scannt man einfach beim Einsteigen.",
    "Die Fahrt dauert 1 Stunde 50 Minuten.", "Mein Platz ist Platz Nummer 7.", "Die Leute warten auf die Abfahrt ihres Busses.", "Sie sitzen auf Stühlen und warten.", "Es gibt viele Restaurants.",
    "Wenn man beim Warten auf den Bus Hunger bekommt, isst man hier.", "Es gibt Mandu (koreanische Teigtaschen).", "Es gibt Gukbap (koreanische Suppe mit Reis).", "Nach dem Essen kann man auch noch einen Donut essen.", "Es ist 20:14 Uhr.",
    "Bis mein Bus abfährt,", "sind es noch 5 Minuten.", "Ich setze mich hin und warte.", "Ich gehe raus zum Bussteig, um in den Bus zu steigen.", "Viele Busse warten.",
    "Das ist der Bus, mit dem ich heute fahre.", "Ich steige ein und scanne mein Ticket.", "Ticket scannen.", "Ich prüfe die Platznummer.", "Ich prüfe die Platznummer und setze mich.",
    "Es ist 20:20 Uhr.", "Jetzt fährt der Bus los.", "Im Nachtbus wird das Licht nach der Abfahrt ausgeschaltet.", "Zwischen den Sitzen gibt es Vorhänge.", "Ich ziehe den Vorhang zu.",
    "Mit zugezogenem Vorhang hat man Privatsphäre, das ist schön.", "Man kann den Sitz nach hinten klappen.", "Ganz zurückgeklappt kann man komplett liegend fahren.", "Ich schlafe im Bus immer im Liegen.", "Immer im Liegen schlafen.",
    "Es ist 22:08 Uhr.", "Wir sind 2 Minuten früher als erwartet angekommen.", "Bei der Ankunft wird das Licht im Bus eingeschaltet.", "Jetzt steige ich aus dem Bus.", "Aus dem Bus aussteigen.",
    "Weil es spät ist, ist kaum jemand da.", "Jetzt sollte ich schnell zu meiner Unterkunft und mich ausruhen.", "Bis zum nächsten Video!",
]

T["ar"] = [
    "مرحبًا. أنا مينو.", "اليوم عندي أمر عليّ إنجازه في مدينة أخرى،", "لذلك سأذهب إلى مدينة أخرى.", "الساعة الآن الثانية ظهرًا، لكن", "السابعة، الثامنة…",
    "سأذهب بالحافلة حوالي السابعة أو الثامنة.", "سأذهب بالحافلة.", "في كوريا يوجد مكان تتجمع فيه الحافلات.", "يُسمّى المحطة. محطة الحافلات.", "في محطة الحافلات توجد حافلات كثيرة جدًا.",
    "ومن بينها، إلى المنطقة التي تريد الذهاب إليها —", "الحافلة المتجهة إلى تلك المنطقة،", "تختارها وتركبها فقط.", "إذن، هل نذهب معًا؟", "ركبت المترو ووصلت إلى المحطة التي فيها محطة الحافلات.",
    "المخرج", "إذا اتبعت اتجاه «المخرج» يمكنك الوصول إلى محطة الحافلات.", "عندما يركب الكوريون السلّم المتحرك", "يقفون دائمًا على اليمين.", "الجهة اليسرى يستخدمها من يصعدون مشيًا.",
    "عند الخروج من المترو، تمرّر البطاقة ثم تخرج.", "يكفي أن تمرّر البطاقة هنا.", "اقتربنا كثيرًا.", "إذا مشيت قليلًا بعد في الاتجاه الذي تشير إليه اللافتة،", "ستجد محطة الحافلات.",
    "وصلنا إلى محطة الحافلات.", "يمكنك شراء التذاكر من شباك التذاكر.", "هذه آلات تذاكر ذاتية الخدمة.", "هناك ثلاث آلات متجاورة.", "يمكنك شراء تذكرة",
    "أو طباعة تذكرة اشتريتها مسبقًا عبر الإنترنت.", "حتى لو لم تكن تعرف الكورية،", "يمكنك التبديل إلى الإنجليزية أو الصينية أو اليابانية.", "أولًا، تختار إلى أين ستذهب.", "تختار الوجهة. الوجهة.",
    "عندما تضغط على الوجهة،", "تظهر قائمة بكل الأماكن التي يمكنك الذهاب إليها.", "بعد اختيار الوجهة،", "وحسب ترتيب الوقت،", "تظهر الحافلات التي يمكنك ركوبها.",
    "الساعة 9", "الساعة 10:30", "الساعة 11:55", "هناك ثلاث حافلات.", "بعد اختيار الحافلة، تختار أين ستجلس.",
    "لا يمكنك اختيار الأماكن التي عليها علامة X.", "هذه مقاعد حجزها أشخاص آخرون.", "تختار من المقاعد التي ما زال رقمها ظاهرًا.", "تختار المقعد،", "وتختار طفل أو بالغ،",
    "ثم تدفع فقط.", "أنا حجزت مسبقًا عبر تطبيق على الهاتف.", "اسمه تطبيق Express Bus T-money.", "حجزت الحافلة التي تنطلق الساعة 8:20.", "يكفي أن تمسح رمز QR عند ركوب الحافلة.",
    "تستغرق الرحلة ساعة و50 دقيقة.", "مقعدي هو رقم 7.", "الناس ينتظرون انطلاق الحافلة.", "يجلسون على الكراسي وينتظرون.", "توجد مطاعم كثيرة.",
    "إذا جعت وأنت تنتظر الحافلة، تأكل هنا.", "يبيعون الماندو (فطائر كورية محشوة).", "يبيعون الغوكباب (حساء كوري بالأرز).", "وبعد الأكل يمكنك أن تأكل دونات أيضًا.", "الساعة 8:14.",
    "حتى تنطلق حافلتي", "ما زالت هناك 5 دقائق.", "أجلس وأنتظر.", "أخرج إلى الرصيف لركوب الحافلة.", "حافلات كثيرة تنتظر.",
    "هذه هي الحافلة التي سأركبها اليوم.", "أركب الحافلة وأمسح التذكرة.", "أمسح التذكرة.", "أتأكد من رقم المقعد.", "أتأكد من رقم المقعد ثم أجلس.",
    "الساعة 8:20.", "الآن تنطلق الحافلة.", "في الحافلة الليلية تُطفأ الأنوار بعد الانطلاق.", "توجد ستائر بين المقاعد.", "أُسدل الستارة.",
    "إسدال الستارة يحفظ خصوصيتك، وهذا جميل.", "يمكن إرجاع المقعد إلى الخلف.", "إذا أرجعته إلى الآخر، يمكن السفر في وضع الاستلقاء تمامًا.", "أنا دائمًا أستلقي وأنام عندما أركب الحافلة.", "دائمًا أستلقي وأنام.",
    "الساعة 10:08.", "وصلنا قبل الموعد المتوقع بدقيقتين.", "عند الوصول تُضاء الأنوار داخل الحافلة.", "الآن أنزل من الحافلة.", "أنزل من الحافلة.",
    "لأن الوقت متأخر، لا يكاد يوجد أحد.", "الآن عليّ أن أسرع إلى مكان إقامتي لأرتاح.", "أراكم في الفيديو القادم!",
]

T["ja"] = [
    "こんにちは。ミノです。", "今日はほかの町で用事ができたので", "ほかの町に行きます。", "今は午後2時ですが", "7時、8時…",
    "7時か8時ごろにバスに乗って行くつもりです。", "バスに乗って行きます。", "韓国にはバスが集まっている場所があります。", "ターミナルと呼びます。バスターミナル。", "バスターミナルに行くと、バスがものすごくたくさんあります。",
    "その中から、自分が行きたい", "地域へ行くバスを", "選んで乗ればいいです。", "では、一緒に行ってみましょうか？", "地下鉄に乗って、ターミナルがある駅に着きました。",
    "出口", "出口の方向について行けば、ターミナルに行けます。", "韓国の人はエスカレーターに乗ると", "いつも右側に立ちます。", "左側は歩いて上る人が使います。",
    "地下鉄から出るときは、カードをタッチして出ます。", "ここにカードをタッチすればいいです。", "もうすぐ着きます。", "案内板が指す方向にもう少し行くと", "ターミナルがあります。",
    "バスターミナルに着きました。", "切符売り場でチケットを買えます。", "無人の券売機です。", "3台並んでいます。", "チケットを買ったり",
    "オンラインで事前に買ったチケットを印刷したりします。", "韓国語がわからなくても", "英語、中国語、日本語に切り替えて見られます。", "まず、どこに行くかを選びます。", "到着地を選びます。到着地。",
    "到着地を押すと", "行ける場所がずらっと出てきます。", "到着地を選んだら", "時間順に", "乗れるバスが出てきます。",
    "9時", "10時30分", "11時55分", "バスが3本あります。", "バスを選んだら、どこに座るかを選びます。",
    "すでにXの印がある席は選べません。", "ほかの人がもう予約した座席です。", "番号が残っている座席の中から選びます。", "座席を選んで", "子どもか大人かを選んで",
    "支払えばOKです。", "私はスマホのアプリで事前に予約しました。", "「高速バスTmoney」というアプリです。", "8時20分に出発するバスを予約しました。", "QRコードをバスに乗るときにかざせばいいです。",
    "行くのに1時間50分かかります。", "座席は7番です。", "人々がバスの出発を待っています。", "椅子に座って待っています。", "飲食店がたくさんあります。",
    "バスを待っている間にお腹がすいたら、ご飯を食べます。", "マンドゥ（韓国の餃子）を売っています。", "クッパを売っています。", "ご飯を食べたあと、ドーナツも食べられます。", "8時14分です。",
    "私が乗るバスが出発するまで", "まだ5分あります。", "席に座って待ちます。", "バスに乗りに乗り場へ出ます。", "たくさんのバスが待っています。",
    "今日私が乗るバスはこのバスです。", "バスに乗って、チケットをかざします。", "チケットをかざします。", "座席番号を確認します。", "座席番号を確認して席に座ります。",
    "8時20分です。", "いよいよバスが出発します。", "夜行バスは出発すると電気を消します。", "座席の間にカーテンがあります。", "カーテンを閉めます。",
    "カーテンを閉めるとプライバシーが守れるのでいいです。", "座席を後ろに倒せます。", "最後まで倒すと、完全に横になって行けます。", "私はいつもバスに乗ると横になって寝ます。", "いつも横になって寝ます。",
    "10時8分です。", "予定より2分早く着きました。", "到着するとバスの中の電気をつけます。", "では、バスから降ります。", "バスから降ります。",
    "時間が遅いので、人がほとんどいません。", "さあ、早く宿に行って休まなきゃ。", "次の動画で会いましょう。",
]

T["ms"] = [
    "Hai. Saya Mino.", "Hari ini saya ada urusan di bandar lain,", "jadi saya pergi ke bandar lain.", "Sekarang pukul 2 petang, tapi", "pukul 7, pukul 8…",
    "Sekitar pukul 7 atau 8, saya akan naik bas ke sana.", "Saya akan naik bas.", "Di Korea, ada tempat di mana banyak bas berkumpul.", "Ia dipanggil terminal. Terminal bas.", "Di terminal bas, ada sangat banyak bas.",
    "Antara semua itu, ke kawasan yang anda mahu pergi —", "bas yang pergi ke kawasan itu,", "pilih saja dan naik.", "Jom, kita pergi bersama?", "Saya naik kereta api bawah tanah dan sampai di stesen yang ada terminal.",
    "Pintu keluar", "Kalau ikut arah pintu keluar, anda boleh sampai ke terminal.", "Orang Korea bila naik eskalator", "selalu berdiri di sebelah kanan.", "Sebelah kiri digunakan oleh orang yang berjalan naik.",
    "Bila keluar dari stesen, tap kad dan keluar.", "Tap kad di sini saja.", "Sekarang dah hampir sampai.", "Kalau jalan sikit lagi ke arah yang ditunjuk papan tanda,", "ada terminal.",
    "Dah sampai di terminal bas.", "Boleh beli tiket di kaunter tiket.", "Ini mesin tiket layan diri.", "Ada tiga bersebelahan.", "Boleh beli tiket",
    "atau cetak tiket yang dibeli dalam talian lebih awal.", "Walaupun tak tahu bahasa Korea,", "boleh tukar ke bahasa Inggeris, Cina atau Jepun.", "Mula-mula, pilih nak pergi ke mana.", "Pilih destinasi. Destinasi.",
    "Bila tekan Destinasi,", "semua tempat yang boleh dituju keluar berderet.", "Selepas pilih destinasi,", "mengikut urutan masa,", "keluar bas yang boleh dinaiki.",
    "Pukul 9", "Pukul 10.30", "Pukul 11.55", "Ada tiga bas.", "Selepas pilih bas, pilih nak duduk di mana.",
    "Tempat yang dah ada tanda X tak boleh dipilih.", "Itu tempat duduk yang orang lain dah tempah.", "Pilih antara tempat duduk yang nombornya masih ada.", "Pilih tempat duduk,", "pilih kanak-kanak atau dewasa,",
    "lepas tu bayar saja.", "Saya dah tempah awal guna aplikasi di telefon.", "Aplikasinya bernama Express Bus T-money.", "Saya tempah bas yang bertolak pukul 8.20.", "Imbas saja kod QR bila naik bas.",
    "Perjalanan ambil masa 1 jam 50 minit.", "Tempat duduk saya nombor 7.", "Orang ramai sedang menunggu bas bertolak.", "Mereka duduk di kerusi sambil menunggu.", "Ada banyak kedai makan.",
    "Kalau lapar semasa menunggu bas, makan di sini.", "Ada jual mandu (dumpling Korea).", "Ada jual gukbap (sup nasi Korea).", "Lepas makan, boleh makan donut juga.", "Sekarang pukul 8.14.",
    "Sampai bas saya bertolak,", "masih ada 5 minit lagi.", "Saya duduk dan tunggu.", "Saya keluar ke platform untuk naik bas.", "Banyak bas sedang menunggu.",
    "Bas yang saya akan naik hari ini ialah bas ini.", "Naik bas, lepas tu imbas tiket.", "Imbas tiket.", "Semak nombor tempat duduk.", "Semak nombor tempat duduk dan duduk.",
    "Sekarang pukul 8.20.", "Sekarang bas bertolak.", "Bas malam akan padam lampu selepas bertolak.", "Ada langsir di antara tempat duduk.", "Saya tutup langsir.",
    "Kalau tutup langsir, privasi terjaga, jadi bagus.", "Tempat duduk boleh disandarkan ke belakang.", "Kalau sandarkan habis, boleh baring sepenuhnya.", "Saya selalu baring dan tidur bila naik bas.", "Selalu baring dan tidur.",
    "Sekarang pukul 10.08.", "Sampai 2 minit lebih awal daripada jangkaan.", "Bila sampai, lampu dalam bas dinyalakan.", "Sekarang saya turun dari bas.", "Turun dari bas.",
    "Sebab dah lewat, hampir tiada orang.", "Sekarang saya kena cepat pergi ke penginapan dan berehat.", "Jumpa lagi dalam video seterusnya!",
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
    assert len(KO) == len(set(KO)) == 93
    for lang, rows in T.items():
        assert len(rows) == len(KO), (lang, len(rows))
    idx = {k: i for i, k in enumerate(KO)}
    cues = parse(SRC)
    for _, key in cues:
        assert key in idx, f"번역표에 없는 문장: {key!r}"
    for lang, rows in T.items():
        out = "\n\n".join(f"{time}\n{rows[idx[key]]}" for time, key in cues) + "\n"
        path = os.path.join(HERE, f"S005_captions.{lang}.sbv")
        with open(path, "w", encoding="utf-8", newline="\r\n") as f:  # 원본과 같은 CRLF
            f.write(out)
        # 검증: 타임코드 개수·값이 원본과 같은지
        assert [t for t, _ in parse(path)] == [t for t, _ in cues], lang
        print(f"{lang}: {len(cues)}줄 OK")


if __name__ == "__main__":
    main()
