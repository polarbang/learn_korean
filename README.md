# learn_korean

외국인 학습자용 한국어 어휘 학습 세션 제작 프로젝트. 작업 규칙과 절차는 [CLAUDE.md](CLAUDE.md)에 있다.

S006부터는 **촬영할 장면과 꼭 말할 내용 기획 → 자연스럽게 촬영 → 촬영자가 최종 대본 작성 → 전체 난이도 검토 → 필요한 에셋 후보 선정** 순서로 진행한다. S001–S005는 그대로 둔다. 자막·학습 자료는 필요할 때 완성 대본을 기준으로 만든다. [촬영 기획 양식](sessions/_template.md), [대본 수준 검토 양식](sessions/_script_review_template.md), [에셋 후보판 양식](sessions/_asset_candidates_template.md)을 사용한다.

## S006 이후 자막 만들기

사용자가 준 한국어 자막을 `sessions/S006/S006_captions/S006_captions.kr.sbv`에 저장한 뒤 실행한다.

```
python captions.py prepare S006
```

생성된 `sessions/S006/S006_captions/S006_translations.tsv`에서 각 한국어 문장의 13개 언어 번역을 채우고 아래 명령을 실행한다. 같은 한국어 문장은 한 번만 번역한다.

```
python captions.py build S006
python upload_captions.py S006 --dry-run
```

한국어 원본이 바뀌면 `python captions.py prepare S006 --refresh`를 실행한다. 기존 번역표는 백업되고, 바뀌지 않은 문장의 번역은 유지된다. 특정 언어만 다시 만들 때는 `python captions.py build S006 --only en ja`를 사용한다. 업로드는 영상 URL을 받은 뒤 `python upload_captions.py S006 --video <영상 URL>`로 진행한다.

## 새 기기 설정
```
pip install -r requirements.txt
```
- Python 3.10 이상, git 필요. `python assets.py fetch S###`를 처음 실행하면 Fluent Emoji 저장소를 `.cache/`에 받아 검색 인덱스를 만든다 (`icons/make_icons.py`도 이 캐시를 쓴다).
- 유튜브 자막 업로드(`upload_captions.py`)를 쓰려면 `client_secret.json`(Google Cloud OAuth 클라이언트, 저장소에 없음)을 기존 기기에서 복사해 이 폴더에 넣는다. 처음 실행할 때 브라우저 로그인 한 번 (토큰은 기기마다 `.cache/`에 따로 저장).
- `common_assets/mov/`(CapCut용 MOV, 약 190MB)는 저장소에 없다. 새 기기에서 `python common_assets/make_overlays.py`를 실행하면 같은 파일이 만들어진다 (ffmpeg는 imageio-ffmpeg에 포함).
