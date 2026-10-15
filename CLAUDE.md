# 한국어 어휘 학습 세션 프로젝트

외국인 학습자용 한국어 어휘 학습 세션을 만드는 프로젝트다.
CEFR A1부터 B2까지 난이도를 점진적으로 올리며, 상황별 세션으로 어휘를 익히게 한다.

## 파일 구성
- `vocab.json` — 전체 어휘 3,237개. 레벨 → 품사 → 미사용/사용 구조. **직접 편집하지 말고 `vocab.py`로만 상태를 바꾼다.**
- `vocab.py` — 어휘 상태 관리 스크립트
- `upload_captions.py` — 회차 자막을 유튜브 영상에 한꺼번에 업로드 (아래 '유튜브 자막 업로드')
- **원칙**: 여러 회차에서 다시 쓰는 것은 `common_assets/`(강조 에셋)·`icons/`(단어 아이콘 원본), 한 회차에만 쓰는 것은 `sessions/S###/`에 둔다.
- `sessions/S###/` — 회차 하나의 재료를 모두 모은 폴더
  - `S###_상황.md` (세션 대본) · `S###_상황_학습.md` (학습 자료) · `S###_captions/` (자막 — 한국어 원본 `S###_captions.kr.sbv`, 번역 `S###_captions.<코드>.sbv`, 생성기 `make_captions.py`) · `S###_video_id.txt` (유튜브 영상 ID) · `S###_description.txt` · `S###_pinned_comment.txt` · `S###_assets/` (그 회차 아이콘 복사본 + `report.md`)
- `sessions/_template.md` — 세션 파일 양식 · `sessions/_study_template.md` — 학습 자료 양식
- `common_assets/` — 모든 영상에서 쓰는 공용 강조 에셋 (동그라미·원·네모·밑줄·화살표·체크·엑스·가리키는 손·숫자 1~9). `mov/`(CapCut용, git에 없음 — 생성기로 다시 만듦) · `png/` · 생성기 `make_overlays.py` · 원본 `_src/` · 설명 `README.md`
- `icons/` — 단어 아이콘 (아래 '아이콘 에셋 자동화'). 관리 스크립트는 루트의 `assets.py`
  - `library/` — 단어 id별 아이콘 원본 (`A1-N-001_사람.png`). 회차가 바뀌어도 재사용
  - `icon_map.json` — 단어 id → 아이콘 매핑. 한번 정한 아이콘은 여기 남아 다음 세션에서 재사용된다
  - `make_icons.py` · `made/` — Fluent에 없는 단어 아이콘 생성기와 그 결과 (Fluent 이모지 합성 또는 직접 그림). 새 단어가 생기면 `RECIPES`에 추가하고 `assets.py set --file`로 등록

## vocab.json 구조
- `levels.{A1|A2|B1|B2}.{명사|동사|형용사|부사}.{미사용|사용}` → 단어 목록
- 단어 필드: `id`(고유값, 예: A1-N-010), `word`, `meaning`(영어), `rank`(레벨·품사 안 빈도 순위, 1이 최고), `used_in`(사용된 세션 ID 목록)
- `sessions`: 세션 기록 (`id`, `level`, `situation`, `new_words`, `review_words`)
- 같은 단어가 품사·레벨이 다르면 별도 항목이다 (예: 안 = A1-N-080 inside / A1-ADV-002 not).

## 세션 제작 규칙
1. **레벨 진행**: A1 ~ A2 → B1 ~ B2 순서. 현재 레벨의 미사용 단어가 대부분 소진되면 다음 레벨로 넘어간다.
2. **새 단어 수**: 한 세션에 새 단어 20~30개가 기준이지만 숫자에 매이지 않는다. 그 상황에서 실제로 쓸 만한 단어가 더 있으면 넉넉히 넣어도 된다.
3. **단어 선택**: 미사용 단어 중 `rank`가 높은(숫자가 작은) 단어를 우선으로 고른다. 상황에 맞추기 위해 순위를 어느 정도 건너뛰는 것은 괜찮다.
4. **품사 균형**: 한 세션 안에 명사만 모으지 말고 동사·형용사·부사를 섞어서 실제 문장을 만들 수 있게 한다.
5. **상황 설정**: 단어를 자연스럽게 쓸 수 있는 구체적 상황으로 묶는다 (예: 마트에서, 부엌에서, 침실에서, 콘서트에 간 날). 레벨이 오를수록 상황도 복잡해진다 (A1 장보기 → B2 토론·뉴스 등).
6. **재사용**: 이미 사용한 단어도 다음 세션에서 다시 쓸 수 있다. 복습 단어(review)로 기록하며, 새 단어 수에는 포함하지 않는다.
7. **상위 레벨 단어는 조금만**: 세션 레벨보다 높은 레벨의 단어(예: A1~A2 세션의 B1~B2 단어)도 상황에 꼭 맞으면 소수(몇 개 정도) 넣어도 된다. 너무 많이 넣지는 않는다. 낮은 레벨의 이미 배운 단어는 자유롭게 써도 된다.
8. **대본은 컴팩트하게**: 같은 말을 쓸데없이 반복하기보다, 그 상황에서 실제로 쓸 만한 문장을 최대한 많이 담는다. Comprehensible input 방식으로, 행동과 말을 동시에 보여 줘서(냉장고를 열면서 "냉장고를 열어요") 별도 에셋 없이도 화면만 보고 뜻을 알 수 있게 한다.

## 세션 제작 절차
1. `python vocab.py stats`로 현황을 확인한다.
2. `python vocab.py sessions`로 마지막 세션 번호와 지금까지의 상황을 확인한다 (상황이 겹치지 않게).
3. `python vocab.py unused <레벨> --limit 60`으로 후보 단어를 본다.
4. 상황을 정하고 새 단어 20~30개(+필요하면 복습 단어)를 고른다.
5. `sessions/_template.md` 양식으로 `sessions/S###_상황.md`를 작성한다.
6. 세션 파일을 완성한 뒤 기록한다:
   ```
   python vocab.py use S001 --level A1 --situation "마트에서" --new A1-N-010 A1-N-068 ... --review A1-N-001 ...
   ```
   - 단어 이름으로도 지정할 수 있지만, 동음이의어가 있으면 id로 지정해야 한다.
   - 잘못 기록했으면 `python vocab.py undo S001` 후 다시 기록한다.
7. `python vocab.py find <단어>`로 반영 결과를 확인한다.
8. `python assets.py fetch S###`로 아이콘을 모은다 (아래 '아이콘 에셋 자동화').
9. `report.md`의 '검토 필요' 항목을 확인하고 `set`으로 확정한다.
10. 못 찾은 단어는 먼저 `icons/make_icons.py`로 Fluent 이모지를 합성하거나 직접 그려서 `set --file`로 등록한다. 그래도 안 되는 것만 사용자에게 알린다.
11. 세션 파일의 새 단어로 `sessions/S###/S###_상황_학습.md` 학습 자료를 만든다 (양식 `sessions/_study_template.md`, 아래 규칙).

## 학습 자료 규칙 (`sessions/S###/S###_상황_학습.md`)
- 독자는 외국인 학습자. 설명 문구는 영어로 쓴다.
- **Notion 게시**: 작성 후 Notion MCP로 상위 페이지 "Learn Korean with Mino - Study Notes"(id `3f045badf81c80f89033d08067b0a291`) 아래에 하위 페이지로 만든다.
  - 제목: `Ep. N · <영상 제목(영어)>` (S001 → Ep. 1, 상위 페이지 이름에 Study Notes가 있으므로 붙이지 않음), 상황에 맞는 이모지 아이콘.
  - 맨 위에 📺 callout: 어느 유튜브 영상의 학습 자료인지 + 영상 링크 자리.
  - 표는 Notion `<table>` 태그로, 예문의 로마자·번역 줄은 탭 들여쓰기(번호 목록의 하위 줄), ⚠ 불규칙 설명은 노란 callout.
  - **레이아웃**: 섹션 순서는 How to read → Nouns → Verbs → Adjectives → Adverbs → Expressions → Grammar Point. 해당 단어가 없는 섹션은 만들지 않는다 (Expressions는 표현이 있을 때만).
    - 섹션 제목은 한국어 먼저, 영어는 괄호: `명사 (Nouns)` · `동사 (Verbs)` · `형용사 (Adjectives)` · `부사 (Adverbs)` · `표현 (Expressions)` · `문법 (Grammar): <문형> (<뜻>)`. How to read this page만 영어 그대로 (처음 읽는 안내라 한글을 못 읽어도 이해되게).
    - 섹션 제목(H2)에 번호를 붙이지 않고 색 배경으로 구분한다 (How to read gray · Nouns blue · Verbs green · Adjectives yellow · Adverbs orange · Expressions pink · Grammar purple). `---` 구분선은 쓰지 않는다.
    - 목차(`<table_of_contents/>`)는 넣지 않는다 (토글 제목까지 단어가 전부 나열되어 너저분함).
    - 영상 타임스탬프(장면 링크)는 넣지 않는다.
    - 동사·형용사·부사·표현의 각 단어는 토글 제목(`### 사다 {toggle="true"}` — 제목에는 단어만. 뜻·발음은 섹션 맨 위 표에 있으므로 넣지 않음)으로, 내용은 탭 들여쓰기해서 접히게.
    - How to read this page 마지막 항목에 토글 안내를 넣는다: "In **동사 (Verbs)**, **형용사 (Adjectives)** and **부사 (Adverbs)**, each word is folded. Tap the word (▸) to open it and see its forms and example sentences." 표현 섹션이 있으면 "In **동사 (Verbs)**, **형용사 (Adjectives)**, **부사 (Adverbs)** and **표현 (Expressions)**, …". (Notion 전용 — md 파일에는 토글이 없으므로 넣지 않음)
    - Grammar Point는 제목(H2)에만 보라색 배경을 주고, 내용은 callout 없이 일반 본문으로 쓴다 (callout은 기본색도 배경이 깔림).
  - Notion 마크다운 주의: `[ ]`는 `\[ \]`로 이스케이프, 빈칸은 `___` 대신 전각 `＿＿` (밑줄이 굵게/기울임으로 바뀜).
  - 토글 제목을 고칠 때는 `update_content`의 old_str/new_str에 ` {toggle="true"}`까지 꼭 포함한다. 제목 글자만 바꾸면 토글이 풀리고 안의 내용이 밖으로 빠져나온다. 수정 후 fetch로 토글 유지 확인.
  - **이모지는 최소한만**: 페이지 아이콘, 맨 위 📺 callout, ⚠ 불규칙 callout 아이콘 정도. 섹션 제목·표·본문에는 넣지 않는다.
- **단어 선정**: 영상의 새 단어를 전부 넣지 않고, 아래 기준으로 핵심만 고른다. vocab.json에는 영상의 새 단어를 전부 기록한다 (노트는 그 일부).
  1. **뺀다**: vocab.json 목록(3,237개)에 없는 단어 · 위치어(위, 안, 옆, 저쪽, 좌우 등) · 잇는 말(그리고, 그래서 등) · 수(하나, 둘 등) · 뜻이 뻔한 외래어나 영어권에서 이미 아는 말(커피, 마트, 카트, 프라이팬, 텀블러, 김치 등) · 고유명사(한국 등) · 복습 단어.
  2. **레벨로 거르지 않는다**: 영상에 자연스럽게 나온 B레벨 단어도 그대로 넣는다.
  3. **개수 상한**: Nouns 10 · Verbs+Adjectives 합쳐서 14 · Adverbs 4 · Expressions 3 (합계 약 30). 넘으면 장면의 핵심 단어 > rank 순으로 고른다.
  4. 시간 표현(오늘, 지금, 이제)은 넣는다.
- **Expressions**: 두 단어 이상이 한 뜻을 이루는 표현(수다를 떨다 등)은 Verbs가 아니라 Expressions 섹션에 넣는다. 활용형 표는 넣지 않는다 — 필요하면 짧은 설명 한 줄(영상에서 들린 형태 등) + 예문.
- **단어 목록**: 고른 단어를 품사별로 나눠 각 섹션 맨 위에 `Korean | Meaning | Sound` 표로 넣는다 (품사 열 없음, 영상에 나온 순서). 명사는 Nouns 섹션의 표, 동사·형용사·부사·표현은 각 섹션 제목 바로 아래 표 → 그 아래 단어별 토글.
- **발음**: 로마자만 쓴다 (한글 발음 표기 X). 철자가 아니라 **실제 소리** 기준, 음절은 하이픈으로 (찾다 chat-tta, 찾아요 cha-ja-yo, 많이 ma-ni).
- **명사**: Nouns 표에만 넣고 끝 (표 외의 표현 방식은 검토 중).
- **동사·형용사**: 단어별로
  - 활용형 표 — 기본형(Dictionary form)과 활용형 (표 앞에 "Same word, different endings" 같은 안내 문구는 넣지 않는다). 동사는 Present(-아요/어요)·Past(-았어요)·Future(-(으)ㄹ 거예요), 형용사는 Present·Past. 표 열은 `구분 | Korean | Sound`만 (뜻 열 없음 — 같은 뜻이고 시제만 다르므로). 변하지 않는 어간을 **굵게** 표시해 같은 단어임을 보여 준다.
  - 불규칙 활용(ㅂ, 르 등)은 ⚠ 한 줄로 어떻게 바뀌는지 설명.
- **부사**: 예문만 (발음은 섹션 표에 있으므로 `**Sound:**` 줄 없음. "Adverbs never change their form." 같은 안내 문구도 넣지 않는다). 필요하면 쓰임 설명 한 줄.
- **예문 정확성**: 예문 속 단어가 표에 적은 뜻으로 쓰였는지 확인한다 (예: 다 = all인데 "다 볶았어요"는 '끝까지 다 했다'는 뜻이라 맞지 않음).
- **예문**: 동사·형용사·부사마다 2~3개. 각 예문은 한글(타깃 단어 굵게) / 로마자(이탤릭) / 영어 번역.
  - 1개는 영상 상황 안의 문장, 나머지는 영상 밖의 다른 상황. 영상 대사와 똑같다고 표시하지 않는다 (🎬 표시 X — 촬영하며 대사가 바뀔 수 있음).
  - 단어는 세션 레벨 범위까지만 (상위 레벨 단어 금지). 문법은 -아요/어요, -았어요, -(으)ㄹ 거예요, -고 싶어요, 그래서/그리고 수준으로 제한.
- **문법 포인트 (맨 끝, 1개)**: 영상 대사에 나온 문형 중 세션 레벨에 맞는 것 하나 (예: S001 `A은/는 B보다 [형용사]`). 조사가 받침에 따라 바뀌는 문형이면(은/는, 이/가, 을/를) 짧은 설명 한 줄 + 예문에 두 형태가 모두 나오게 한다.
  - 한두 줄 설명 → 공식(`A은/는 B보다 [adjective]` = …) → 예문 하나를 덩어리로 나눈 표(뜻/한글/로마자) → 이번 세션 단어로 만든 예문 2~3개 → "Your turn" 빈칸 한 줄.

## 자막 번역 규칙
사용자가 한국어 자막 파일(.sbv)을 주면 아래 **13개 언어**로 모두 번역한다.

| 코드 | 언어 | 코드 | 언어 |
|---|---|---|---|
| `en` | 영어 | `es` | 스페인어 |
| `zh-Hans` | 중국어(간체) | `fr` | 프랑스어 |
| `id` | 인도네시아어 | `de` | 독일어 |
| `pt-BR` | 포르투갈어(브라질) | `ar` | 아랍어 |
| `fil` | 필리핀어 | `ja` | 일본어 |
| `ru` | 러시아어 | `ms` | 말레이어 |
| `vi` | 베트남어 | | |

- **방법**: 이전 회차의 `sessions/S###/S###_captions/make_captions.py`를 참고해 같은 방식으로 만든다. 한국어 원문 문장 목록(KO, 중복 제거)과 언어별 번역 표(T[코드], KO와 같은 순서)를 두고, 원본의 타임코드·줄 구성은 그대로 둔 채 문장만 바꾼다. 원본에 번역 표에 없는 문장이 있으면 에러로 멈추게 한다.
- **파일**: 사용자가 준 한국어 자막은 `sessions/S###/S###_captions/S###_captions.kr.sbv`로 저장한다.
- **출력**: `sessions/S###/S###_captions/S###_captions.<코드>.sbv`, 원본과 같은 줄바꿈(CRLF)·UTF-8. 생성 후 언어별로 타임코드 개수·값이 원본과 일치하는지 검증한다.
- **번역**: 기계 번역 API 없이 직접, 장면 맥락에 맞게 한다.
  - "미노 쌤"처럼 성별이 드러날 수 있는 표현은 성별 중립으로 (예: es "tu profe", de "Hier ist Mino!", ru "С вами Мино!", vi "Mình là Mino đây!"). 러시아어·프랑스어처럼 1인칭 과거형에 성별이 붙는 언어는 '우리' 주어나 성별 없는 형태로 바꾼다.
  - 층수: 지상층을 따로 세는 나라는 한국 "2층" → 1st floor (fr premier étage, de erster Stock, pt-BR primeiro andar, ms tingkat 1).
  - 한국 음식 이름(라면·만두·김치)은 영어·유럽어에서 ramyeon/mandu 등 한국어 이름을 살리고, 필요하면 괄호로 현지 설명.
  - 문장이 단계적으로 완성되는 자막(예: "소고기는… → 소고기는 돼지고기보다… → …비싸요")은 번역도 같은 흐름이 되게.
- 원어민 검수 전 번역이라는 점을 사용자에게 알린다.

### 유튜브 자막 업로드 (`upload_captions.py`)
사용자가 영상을 **비공개로 먼저 올리고** URL을 주면, 그 회차 자막 전부(한국어 포함 14개)를 한 번에 올린다.
```
python upload_captions.py S004 --video https://youtu.be/XXXXXXXXXXX
```
- 영상 ID는 `sessions/S###/S###_video_id.txt`에 저장돼 다음부터는 `--video` 없이 실행된다. 번역을 고친 뒤 다시 실행하면 같은 언어 트랙을 덮어쓴다.
- 먼저 `--dry-run`으로 대상 언어를 확인한다. 일부 언어만 올리려면 `--only en ja`.
- 할당량: 하루 10,000 기본, 14개 언어 한 번에 약 5,700 → 하루 영상 1편. 할당량이 다 되면 다음 날 `--only`로 남은 언어만 올린다.
- 인증: 루트의 `client_secret.json`(git 제외)과 `.cache/youtube_token.json`. OAuth 앱이 테스트 상태라 7일마다 브라우저 로그인이 다시 필요하다 — 로그인 창이 뜨면 사용자에게 알린다.
- 유튜브 언어 코드: 파일 이름의 `kr`은 업로드 때 `ko`로 바꾼다 (나머지는 파일 이름 코드 그대로).

## 유튜브 설명글 규칙
사용자가 영상 설명글을 요청하면 아래 형식으로 짧게 쓴다 (영어). 결과물은 `sessions/S###/S###_description.txt`.

```
Comprehensible Korean Input for Beginners | <상황 (영어, 소문자 위주)>

<한 줄 초대: Come ... with me in/on ...!>
Learn everyday Korean words naturally — from <영상 첫 장면> to <마지막 장면>.

This video is perfect for beginners who want to improve
their Korean listening skills in a real-life situation.

#learnkorean  #koreanvocabulary   #koreanforbeginners   #studykorean  #koreanlistening   #comprehensibleinput
```

- 첫 줄은 영상 제목. 형식 그대로 `Comprehensible Korean Input for Beginners | ...`.
- 본문은 3문단 정도로 짧게. 단어 목록·문법·학습 노트 링크·자막 언어 목록·이모지는 넣지 않는다.
- 해시태그는 위 6개 고정.

## 고정 댓글 규칙
설명글과 함께 고정 댓글도 만든다. 결과물은 `sessions/S###/S###_pinned_comment.txt`.

```
📒 Study notes for this video: <이번 회차 Notion 학습 노트 링크>

<상황 이모지> <한국어 질문 (여러분은 …?)>
<같은 질문 영어> Tell me in the comments!

Try writing it in Korean
<빈칸 문장 (＿＿ 사용)>
(<로마자, 빈칸 포함>)
= <영어 뜻>

예시 (Example):
<예문 1> <이모지>
<예문 2> <이모지>

Don't worry about mistakes — 틀려도 괜찮아요! I'll reply to as many as I can 😊

Feel free to ask me any questions in the comments. I'll reply ASAP!
```

- 질문과 빈칸 문장은 그 회차의 **문법 포인트**로 답할 수 있게 만든다 (S002 `위에` 회차 → `저는 집에서 ＿＿을/를 만들어요`).
- 조사가 받침에 따라 바뀌면 빈칸에 두 형태를 다 쓰고(`을/를`, `이/가`), 예시 두 개가 각각 다른 형태가 되게 한다.
- 빈칸은 전각 `＿＿`. 마지막 두 문단은 고정 문구.

## 세션 ID 규칙
- S001부터 세 자리 순번. 파일명은 `S001_마트에서.md`.


## 아이콘 에셋 자동화

영상에서 새 단어가 나올 때 한글 자막 위에 아이콘(명사)이나 움직이는 아이콘(동사·형용사)을 띄운다.
세션마다 필요한 아이콘을 자동으로 모으고, 못 찾은 단어만 사람이 직접 찾게 한다.

### 구현할 것: `assets.py` (vocab.py와 별도 파일)

**아이콘 출처 우선순위**
1. Microsoft Fluent Emoji 3D (github.com/microsoft/fluentui-emoji, MIT 라이선스): 메인 스타일
2. 못 찾은 단어는 사람이 Flaticon / Icons8 / LottieFiles에서 비슷한 3D 스타일로 직접 찾는다.

**Fluent Emoji 저장소 처리**
- 처음 실행할 때 `.cache/fluentui-emoji`에 shallow clone 한다 (`.gitignore`에 `.cache/` 추가).
- 구현 전에 실제 저장소 구조를 먼저 확인한다. (`assets/<이모지 이름>/metadata.json`, `3D/` 폴더, 피부색 변형이 있는 이모지는 `Default/3D/` 아래에 있는 것으로 알려져 있음)
- metadata의 이름(cldr)과 keywords로 검색 인덱스를 만들어 `.cache/emoji_index.json`에 저장한다.

**단어별 아이콘 매핑: `icons/icon_map.json`**
- 한번 정한 아이콘은 다음 세션에서도 재사용한다 (같은 단어는 항상 같은 그림 → 스타일 통일).
- 형식: `{"A1-N-xxx": {"word": "문", "source": "fluent" | "manual", "name": "Door", "file": "icons/library/A1-N-xxx_문.png", "motion": "rotate", "license": "MIT (Fluent Emoji)"}}`
- 실제 이미지 파일은 `icons/library/` 폴더에 모은다.

**명령어**
| 명령 | 기능 |
|---|---|
| `python assets.py fetch S001` | 세션의 새 단어+복습 단어에 아이콘 배정. icon_map에 있으면 재사용하고, 없으면 자동 검색한다 |
| `python assets.py set <id> --emoji "Red apple"` | 특정 이모지로 직접 지정 |
| `python assets.py set <id> --file <경로>` | 직접 받은 파일(Flaticon, Lottie 등) 등록. source는 manual, license는 사용자 입력 |
| `python assets.py candidates <id>` | 자동 매칭 후보 상위 5개 보기 |

**자동 매칭 규칙**
- 검색어는 `meaning`에서 만든다: 괄호 안 설명은 제거하고, `/`로 나뉜 뜻은 각각 검색한다 (예: "time/hour" → time, hour).
- 이모지 이름 완전 일치를 최우선으로 하고, 그다음 keywords 일치를 본다.
- 확신이 낮은 매칭은 자동 확정하지 않고 '검토 필요'로 분류한다.
- `fetch`가 끝나면 Claude가 검토 목록을 직접 보고, 뜻에 맞는 후보를 `set`으로 확정한다.
  예: '배'는 stomach/ship/pear 중 영상 상황에 맞는 것을 고른다.

**fetch 결과물: `sessions/S###/S###_assets/`** (세션 폴더가 없으면 만든다)
- ⚠ fetch는 이 폴더의 번호 붙은 파일(`01_…`)과 `report.md`를 새로 만든다. 직접 넣은 사진이나 손으로 고친 report가 있는 회차(예: S003)에는 다시 실행하기 전에 확인한다.
- 세션 단어의 아이콘 파일 복사본: `01_문.png`, `02_열다.png` … (세션 파일의 단어 순서대로 번호)
- `report.md`:
  - 단어 / 아이콘 / 출처 / 추천 모션 표
  - **못 찾은 단어 목록**: 단어마다 영어 검색어와 바로 열 수 있는 검색 링크 (Flaticon, Icons8, LottieFiles)
  - **추상어 표시**: 아이콘으로 표현하기 어려운 단어 (주로 B1–B2: 가치, 관점 등)는 '장면 이미지 또는 생략'으로 표시
  - 출처 표기가 필요한 아이콘 목록 (영상 설명란 크레딧용)

### 품사별 표현 규칙
- **명사**: 정지 아이콘
- **동사·형용사**: 아이콘에 편집 프로그램에서 키프레임 모션을 준다. 아래 프리셋 중 하나를 `motion` 필드에 추천한다.

| 프리셋 | 움직임 | 어울리는 단어 예시 |
|---|---|---|
| rotate | 살짝 회전 | 열다, 닫다, 돌다 |
| slide | 옆으로 이동 | 가다, 오다, 걷다, 타다 |
| shrink | 작아지며 사라짐 | 먹다, 마시다, 끄다 |
| pop | 커지며 등장 | 사다, 받다, 켜다, 만들다 |
| shake | 좌우로 흔들림 | 뜨겁다, 춥다, 아프다, 무섭다 |
| bounce | 위아래로 통통 | 좋다, 재미있다, 기쁘다, 놀다 |
| fade | 서서히 흐려짐 | 자다, 쉬다, 잊다 |
| none | 움직임 없음 | 명사, 표현이 애매한 단어 |
