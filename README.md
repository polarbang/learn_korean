# learn_korean

외국인 학습자용 한국어 어휘 학습 세션 제작 프로젝트. 작업 규칙과 절차는 [CLAUDE.md](CLAUDE.md)에 있다.

## 새 기기 설정
```
pip install -r requirements.txt
```
- Python 3, git 필요. `python assets.py fetch S###`를 처음 실행하면 Fluent Emoji 저장소를 `.cache/`에 받아 검색 인덱스를 만든다 (`assets/icons/make_icons.py`도 이 캐시를 쓴다).
- `assets/common/mov/`(CapCut용 MOV, 약 190MB)는 저장소에 없다. 새 기기에서 `python assets/common/make_overlays.py`를 실행하면 같은 파일이 만들어진다 (ffmpeg는 imageio-ffmpeg에 포함).
