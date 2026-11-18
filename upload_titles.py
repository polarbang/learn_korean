"""영상 제목 번역(video_titles.tsv)을 유튜브 영상에 한꺼번에 올린다.

video_titles.tsv: 탭으로 구분, 첫 줄은 머리글.
  video   en   zh-Hans   id   pt-BR   fil   ru   vi   es   fr   de   ar   ja   ms
  - video: 유튜브 URL 또는 영상 ID
  - en: 기본 제목 (영어). 유튜브의 현재 제목과 다르면 경고만 하고 기본 제목은 바꾸지 않는다.
  - 나머지 열: 언어별 번역 제목 (빈 칸은 건너뜀). 한국어는 넣지 않는다.

영상의 기본 언어(snippet.defaultLanguage)를 en으로 맞추고, 기존 번역(설명글 번역 포함)은 유지한 채
표에 있는 언어의 제목만 덮어쓴다.

사용법:
  python upload_titles.py --dry-run     # 올리지 않고 검사·예상 할당량만
  python upload_titles.py               # 전체 업로드
  python upload_titles.py --only ja es  # 일부 언어만
  python upload_titles.py --video https://youtu.be/XXXXXXXXXXX   # 이 영상만 (새 영상 추가 시)

할당량: 영상 정보 조회 50편당 1, 영상 1편 수정 50 → 하루 기본 10,000으로 약 190편.
"""
import argparse
import csv
import sys

from upload_captions import ROOT, video_id_from, youtube_client

TABLE = ROOT / "video_titles.tsv"
DEFAULT_LANG = "en"
LANGS = ["zh-Hans", "id", "pt-BR", "fil", "ru", "vi", "es", "fr", "de", "ar", "ja", "ms"]
COST_LIST, COST_UPDATE = 1, 50
MAX_LEN = 100
KEEP_SNIPPET = ("title", "description", "tags", "categoryId", "defaultLanguage", "defaultAudioLanguage")


def load_table(only):
    if not TABLE.exists():
        sys.exit(f"번역표가 없습니다: {TABLE.name}")
    with TABLE.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    langs = only or LANGS
    unknown = set(langs) - set(LANGS)
    if unknown:
        sys.exit(f"지원하지 않는 언어: {', '.join(sorted(unknown))}")
    errors, videos = [], {}
    for n, row in enumerate(rows, start=2):
        vid = video_id_from((row.get("video") or "").strip())
        if vid in videos:
            errors.append(f"{n}행: 영상 중복 {vid}")
        titles = {}
        for lang in [DEFAULT_LANG] + langs:
            t = (row.get(lang) or "").strip()
            if not t:
                continue
            if len(t) > MAX_LEN:
                errors.append(f"{n}행 {lang}: {len(t)}자 (최대 {MAX_LEN})")
            if "<" in t or ">" in t:
                errors.append(f"{n}행 {lang}: 제목에 < > 사용 불가")
            titles[lang] = t
        missing = [l for l in langs if l not in titles]
        if missing:
            print(f"  ! {vid}: 번역 없음 {', '.join(missing)} (건너뜀)")
        videos[vid] = titles
    if errors:
        sys.exit("번역표 오류:\n  " + "\n  ".join(errors))
    return videos


def main():
    ap = argparse.ArgumentParser(description="영상 제목 번역을 유튜브에 올린다")
    ap.add_argument("--only", nargs="+", metavar="LANG", help="이 언어만 (예: ja es)")
    ap.add_argument("--video", nargs="+", metavar="URL", help="이 영상만 (URL 또는 ID)")
    ap.add_argument("--dry-run", action="store_true", help="올리지 않고 검사만")
    a = ap.parse_args()

    videos = load_table(a.only)
    if a.video:
        wanted = [video_id_from(v) for v in a.video]
        missing = [v for v in wanted if v not in videos]
        if missing:
            sys.exit(f"번역표에 없는 영상: {', '.join(missing)}")
        videos = {v: videos[v] for v in wanted}
    langs = a.only or LANGS
    cost = COST_LIST * -(-len(videos) // 50) + COST_UPDATE * len(videos)
    print(f"영상 {len(videos)}편 · 언어 {len(langs)}개 · 예상 할당량 약 {cost} (하루 기본 10,000)")
    if a.dry_run:
        for vid, titles in videos.items():
            print(f"  {vid}  {titles.get(DEFAULT_LANG, '(en 없음)')}")
        return

    from googleapiclient.errors import HttpError

    yt = youtube_client()
    ids = list(videos)
    current = {}
    for i in range(0, len(ids), 50):
        resp = yt.videos().list(part="snippet,localizations", id=",".join(ids[i:i + 50])).execute()
        current.update({item["id"]: item for item in resp.get("items", [])})
    used = COST_LIST * -(-len(ids) // 50)

    for vid, titles in videos.items():
        item = current.get(vid)
        if not item:
            print(f"  ✗ {vid}: 영상을 찾을 수 없음 (내 채널 영상인지 확인)")
            continue
        snippet = {k: item["snippet"][k] for k in KEEP_SNIPPET if k in item["snippet"]}
        if titles.get(DEFAULT_LANG) and titles[DEFAULT_LANG] != snippet["title"]:
            print(f"  ! {vid}: 표의 en 제목이 유튜브 제목과 다름 (유튜브: {snippet['title']})")
        if snippet.get("defaultLanguage") != DEFAULT_LANG:
            print(f"  · {vid}: 기본 언어 {snippet.get('defaultLanguage') or '없음'} → {DEFAULT_LANG}")
            snippet["defaultLanguage"] = DEFAULT_LANG
        locs = item.get("localizations", {})
        for lang in langs:
            if lang in titles:
                locs[lang] = {**locs.get(lang, {}), "title": titles[lang]}
        locs.pop(DEFAULT_LANG, None)
        try:
            yt.videos().update(part="snippet,localizations",
                               body={"id": vid, "snippet": snippet, "localizations": locs}).execute()
        except HttpError as e:
            reason = e.error_details[0].get("reason", "") if e.error_details else ""
            if reason == "quotaExceeded":
                sys.exit(f"오늘 할당량을 다 썼습니다 ({vid}부터 실패). 내일 다시 실행하세요.")
            sys.exit(f"{vid} 업로드 실패: {e}")
        used += COST_UPDATE
        print(f"  ✓ {vid}  {snippet['title']}")
    print(f"완료 · 사용한 할당량 약 {used}")


if __name__ == "__main__":
    main()
