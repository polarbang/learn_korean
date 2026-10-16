# 마트 영상 아이콘 에셋

- 출처: [Microsoft Fluent Emoji](https://github.com/microsoft/fluentui-emoji) — MIT 라이선스 (상업적 이용 가능, 영상에 출처 표기 의무 없음)
- `3d/` — 3D 스타일 PNG (256×256, 투명 배경) · 자막 카드용 추천
- `color/` — 플랫 컬러 SVG (크기 자유 조절)
- 미리보기: `preview.html`을 브라우저로 열기

| 구분 | 단어 | Fluent 이모지 | 메모 |
|---|---|---|---|
| 타깃 | 마트 | Convenience store |  |
| 타깃 | 과일 | **합성**: Basket + Banana + Grapes + Red apple + Tangerine | 과일 바구니 (3D만 있음, color SVG 없음) |
| 타깃 | 채소 | Leafy green |  |
| 타깃 | 고기 | Cut of meat |  |
| 타깃 | 계란 | Egg |  |
| 타깃 | 우유 | Glass of milk |  |
| 타깃 | 가격 | Label | 가격표 |
| 타깃 | 카트 | Shopping cart |  |
| 타깃 | 봉투 | Shopping bags |  |
| 타깃 | 사다 | Money with wings | 돈을 쓰는 느낌 (봉투와 구분) |
| 타깃 | 찾다 | Magnifying glass tilted left |  |
| 타깃 | 고르다 | Thinking face | 고민하는 얼굴 |
| 타깃 | 담다 | Basket | 바구니 |
| 타깃 | 계산하다 | Credit card |  |
| 타깃 | 비싸다 | Money bag | 돈 자루 |
| 타깃 | 싸다 | Coin | 동전 |
| 타깃 | 필요하다 | Red exclamation mark | 느낌표 |
| 타깃 | 무겁다 | Person lifting weights | 역기 드는 사람 |
| 타깃 | 먼저 | Keycap 1 | 숫자 1 키캡 |
| 타깃 | 조금 | Pinching hand | 손가락으로 집는 손 |
| 타깃 | 맛있다 | Drooling face | 침 흘리는 얼굴 (대안: extra/맛있다_*) |
| 타깃 | 맵다 | Hot pepper | 고추 |
| 타깃 | 좋아하다 | Red heart | 빨간 하트 |
| 배경 | 걷다 | Person walking | 걷는 사람 (C2·C4 이동 장면) |
| 배경 | 많다 | **합성**: Red apple × 10 | 사과 피라미드 (3D만 있음). '조금'(집는 손)과 짝 |
| 배경 | 카드 | **직접 그림** (`make_card.py`) | 카드 앞면 (IC칩·카드 번호). 계산하다(카드 뒷면)와 구분. vocab: A2-N-095 |
| 배경 | 바코드 | **직접 그림** (`make_barcode.py`) | 흰 라벨 위 EAN-13 바코드 (880 한국 상품코드). 스캔 애니메이션: `mov/바코드_스캔.mov` |
| 배경 | 춥다 | Cold face | 얼어붙은 파란 얼굴 (vocab: A1-ADJ-017) |
| 배경 | 만두 | Dumpling | 만두 (vocab: A2-N-226) |
| 배경 | 맥주 | Beer mug | 맥주잔 (vocab: A1-N-169) |
| 배경 | 음료 | Cup with straw | 빨대 컵 (vocab: 음료수 A2-N-254) |
| 배경 | 유통기한 | **합성**: Tear-off calendar + Hourglass not done | 달력 + 모래시계 (3D만 있음). ⚠ B1 단어 |
| 배경 | 사과 | Red apple |  |
| 배경 | 바나나 | Banana |  |
| 배경 | 양파 | Onion |  |
| 배경 | 돼지고기 | Pig face | 돼지 얼굴 |
| 배경 | 소고기 | Cow face | 소 얼굴 |
| 배경 | 요리 | Pot of food | C23 다음 영상 예고용 |
| 배경 | 밥 | Cooked rice | C2 "집에 있어요" 그래픽 |
| 배경 | 과자 | Cookie |  |
| 배경 | 영수증 | Receipt |  |
| 배경 | 집 | House |  |
| 배경 | 쇼핑목록 | Memo | 메모지 (C3 목록 그래픽) |
| 배경 | 세일 | **합성**: Label + Red circle + "%" 글자 | 가격표에 할인 스티커 (3D만 있음) |

## 아이콘 없음 (사진·영상 캡처로 대체)
- **두부**, **파**, **김치** — 대응하는 이모지 없음. 촬영 영상에서 클로즈업 캡처 추천.

## 직접 그린 아이콘
- `3d/바코드.png` — 이모지에 바코드가 없어서 직접 그림. 실제로 스캔되는 EAN-13 규격 (8801234567893).
- `mov/바코드_스캔.mov` — 빨간 레이저가 1초 동안 위아래로 훑고, '삑' 하며 초록 테두리가 번쩍 (2초, ProRes 4444 투명 배경, CapCut용). 계산대 장면(C21~C22)용.
- 다시 만들기: `python make_barcode.py`
- `3d/카드.png` — 신용카드·체크카드 앞면 (IC칩, 비접촉 표시, 카드 번호). '계산하다' 아이콘(Fluent 카드 뒷면)과 헷갈리지 않게 앞면으로 그림. 다시 만들기: `python make_card.py`

## 합성 아이콘
Fluent Emoji 3D 아이콘을 겹쳐서 만든 것 (MIT 그대로 적용). `3d/`에만 있고 `color/`에는 없음.
- `3d/과일.png` — 바구니에 바나나·포도·사과·귤
- `3d/많다.png` — 사과 10개를 피라미드로 쌓음
- `3d/유통기한.png` — 달력 + 모래시계 (기한이 있는 날짜)
- `3d/세일.png` — 가격표 + 빨간 % 스티커 (`가격` 아이콘과 같은 가격표라 짝지어 쓰기 좋음)

## extra/ — 대체 후보
| 파일 | 설명 | 라이선스 |
|---|---|---|
| `과일_포도.png/.svg` | 기존 과일 아이콘 (포도 하나) | MIT (Fluent) |
| `많다_6개.png` | 사과 6개 피라미드 (많다 대안, 작게 띄울 때 더 잘 보임) | MIT (Fluent 합성) |
| `음료_팩.png` | 주스 팩 (음료 대안, 주스에도 사용 가능) | MIT (Fluent) |
| `유통기한_우유.png` | 달력 + 우유 컵 (유통기한 대안) | MIT (Fluent 합성) |
| `세일_SALE.png` | 빨간 원에 SALE 글자 | MIT (Fluent 합성) |
