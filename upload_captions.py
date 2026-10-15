"""회차 자막(sessions/S###/S###_captions/S###_captions.<언어>.sbv)을 유튜브 영상에 한꺼번에 올린다.

같은 언어 트랙이 이미 있으면 덮어쓰고(update), 없으면 새로 만든다(insert).
파일 이름의 kr은 업로드할 때 유튜브 언어 코드 ko로 바꾼다.

준비: client_secret.json (Google Cloud OAuth 데스크톱 클라이언트)을 이 폴더에 둔다.
     처음 실행하면 브라우저 로그인. 토큰은 .cache/youtube_token.json에 저장된다
     (OAuth 앱이 '테스트' 상태면 7일마다 다시 로그인).

사용법:
  python upload_captions.py S004 --video https://youtu.be/XXXXXXXXXXX   # 영상 ID는 회차 폴더에 저장됨
  python upload_captions.py S004                    # 저장된 영상 ID 사용
  python upload_captions.py S004 --only en ja       # 일부 언어만
  python upload_captions.py S004 --dry-run          # 올리지 않고 대상만 확인

할당량: 기본 하루 10,000. 자막 하나 올릴 때 400 (덮어쓰기 450) → 14개 언어 ≈ 5,700, 하루 영상 1편.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SESSIONS = ROOT / "sessions"
CLIENT_SECRET = ROOT / "client_secret.json"
TOKEN = ROOT / ".cache" / "youtube_token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
LANG_TO_YOUTUBE = {"kr": "ko"}  # 파일 이름 코드 → 유튜브 언어 코드
COST_INSERT, COST_UPDATE, COST_LIST = 400, 450, 50


def video_id_from(text):
    m = re.search(r"(?:youtu\.be/|v=|shorts/|live/)([\w-]{11})", text)
    if m:
        return m.group(1)
    if re.fullmatch(r"[\w-]{11}", text):
        return text
    sys.exit(f"영상 ID를 찾을 수 없습니다: {text}")


def session_dir(sid):
    d = SESSIONS / sid
    if not d.is_dir():
        sys.exit(f"회차 폴더가 없습니다: {d.relative_to(ROOT)}")
    return d


def caption_files(sid, only):
    folder = session_dir(sid) / f"{sid}_captions"
    files = {}
    for p in sorted(folder.glob(f"{sid}_captions.*.sbv")):
        code = p.name[len(f"{sid}_captions."):-len(".sbv")]
        files[LANG_TO_YOUTUBE.get(code, code)] = p
    if only:
        wanted = {LANG_TO_YOUTUBE.get(c, c) for c in only}
        missing = wanted - files.keys()
        if missing:
            sys.exit(f"자막 파일이 없는 언어: {', '.join(sorted(missing))}")
        files = {k: v for k, v in files.items() if k in wanted}
    if not files:
        sys.exit(f"올릴 자막이 없습니다: {folder.relative_to(ROOT)}/{sid}_captions.<언어>.sbv")
    return files


def resolve_video(sid, arg):
    saved = session_dir(sid) / f"{sid}_video_id.txt"
    if arg:
        vid = video_id_from(arg)
        saved.write_text(vid + "\n", encoding="utf-8")
        return vid
    if saved.exists():
        return saved.read_text(encoding="utf-8").strip()
    sys.exit(f"영상 ID가 없습니다. --video <유튜브 URL>로 한 번 알려 주세요 (저장 위치: {saved.relative_to(ROOT)})")


def youtube_client():
    from google.auth.exceptions import RefreshError
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    if not CLIENT_SECRET.exists():
        sys.exit("client_secret.json이 없습니다 (Google Cloud → Clients → Desktop app → Download JSON).")
    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES) if TOKEN.exists() else None
    if creds and not creds.valid and creds.refresh_token:
        try:
            creds.refresh(Request())
        except RefreshError:  # 테스트 앱은 7일마다 만료
            creds = None
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
        creds = flow.run_local_server(port=0)
    TOKEN.parent.mkdir(exist_ok=True)
    TOKEN.write_text(creds.to_json(), encoding="utf-8")
    return build("youtube", "v3", credentials=creds)


def main():
    ap = argparse.ArgumentParser(description="회차 자막을 유튜브에 한꺼번에 올린다")
    ap.add_argument("session_id")
    ap.add_argument("--video", help="유튜브 URL 또는 영상 ID (한 번 주면 회차 폴더에 저장)")
    ap.add_argument("--only", nargs="+", metavar="LANG", help="이 언어만 (예: en ja kr)")
    ap.add_argument("--dry-run", action="store_true", help="올리지 않고 대상만 출력")
    a = ap.parse_args()

    files = caption_files(a.session_id, a.only)
    vid = resolve_video(a.session_id, a.video)
    print(f"{a.session_id} → https://youtu.be/{vid} · 자막 {len(files)}개: {', '.join(files)}")
    if a.dry_run:
        print(f"예상 할당량 최대 {COST_LIST + COST_UPDATE * len(files)} (하루 기본 10,000)")
        return

    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload

    yt = youtube_client()
    existing = {}
    for item in yt.captions().list(part="snippet", videoId=vid).execute().get("items", []):
        s = item["snippet"]
        if s.get("trackKind") != "asr":  # 자동 생성 자막은 건드리지 않음
            existing[s["language"]] = item["id"]
    used = COST_LIST
    for lang, path in files.items():
        media = MediaFileUpload(str(path), mimetype="application/octet-stream")
        try:
            if lang in existing:
                yt.captions().update(part="snippet", media_body=media,
                                     body={"id": existing[lang], "snippet": {"isDraft": False}}).execute()
                used += COST_UPDATE
                print(f"  덮어씀  {lang:8} {path.name}")
            else:
                yt.captions().insert(part="snippet", media_body=media,
                                     body={"snippet": {"videoId": vid, "language": lang, "name": "",
                                                       "isDraft": False}}).execute()
                used += COST_INSERT
                print(f"  추가    {lang:8} {path.name}")
        except HttpError as e:
            reason = e.error_details[0].get("reason", "") if e.error_details else ""
            if reason == "quotaExceeded":
                sys.exit(f"오늘 할당량을 다 썼습니다 ({lang}부터 실패). 내일 --only로 남은 언어만 다시 올리세요.")
            sys.exit(f"{lang} 업로드 실패: {e}")
    print(f"완료 · 사용한 할당량 약 {used}")


if __name__ == "__main__":
    main()
