"""세션 단어 아이콘 에셋 관리.

명사는 정지 아이콘, 동사·형용사는 편집기에서 키프레임 모션을 줄 아이콘을 모은다.
메인 스타일은 Microsoft Fluent Emoji 3D (MIT). 한번 정한 아이콘은 icon_map.json에 저장해 재사용한다.

사용법:
  python assets.py fetch S002                     # 세션 단어에 아이콘 배정 + sessions/.../S002_assets/ 생성
  python assets.py candidates A2-N-075             # 자동 매칭 후보 상위 5개
  python assets.py set A2-N-260 --emoji "Kitchen knife" [--motion pop]
  python assets.py set A2-N-075 --file 받은파일.png --license "Flaticon (출처 표기 필요)"
  python assets.py set B1-N-114 --abstract       # 아이콘 없이 '장면 이미지 또는 생략'으로 확정
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / ".cache"
REPO = CACHE / "fluentui-emoji"
INDEX = CACHE / "emoji_index.json"
ICON_MAP = ROOT / "icon_map.json"
ICONS = ROOT / "icons"
VOCAB = ROOT / "vocab.json"
SESSIONS = ROOT / "sessions"

REPO_URL = "https://github.com/microsoft/fluentui-emoji.git"
FLUENT_LICENSE = "MIT (Fluent Emoji)"
AUTO_SCORE = 100  # 이모지 이름 완전 일치만 자동 확정

POS_CODE = {"명사": "N", "동사": "V", "형용사": "ADJ", "부사": "ADV"}

# 동사·형용사 추천 모션 (CLAUDE.md 프리셋). 없으면 none.
MOTION = {
    "rotate": "열다 닫다 돌다 돌리다 섞다 볶다 따르다",
    "slide": "가다 오다 걷다 타다 꺼내다 넣다 닦다 썰다 자르다",
    "shrink": "먹다 마시다 끄다 맛보다",
    "pop": "사다 받다 켜다 만들다 고르다 찾다 담다 계산하다 확인하다",
    "shake": "뜨겁다 춥다 차갑다 아프다 무섭다 맵다 짜다 무겁다 비싸다 목마르다 배고프다",
    "bounce": "좋다 재미있다 기쁘다 놀다 좋아하다 맛있다 싸다 많다 필요하다 배부르다 깨끗하다 싱겁다",
    "fade": "자다 쉬다 잊다 씻다 설거지하다",
}
MOTION_OF = {}
for preset, words in MOTION.items():
    for w in words.split():
        MOTION_OF.setdefault(w, preset)


# ---------- 공통 ----------
def load_json(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def vocab_index():
    doc = load_json(VOCAB, None)
    idx = {}
    for lv, poss in doc["levels"].items():
        for pos, b in poss.items():
            for st in b.values():
                for e in st:
                    idx[e["id"]] = dict(e, pos=pos, level=lv)
    return doc, idx


def default_motion(entry):
    if entry["pos"] in ("명사", "부사"):
        return "none"
    return MOTION_OF.get(entry["word"], "none")


# ---------- Fluent Emoji 저장소 / 인덱스 ----------
def ensure_repo():
    if (REPO / "assets").exists():
        return
    CACHE.mkdir(exist_ok=True)
    print("Fluent Emoji 저장소를 받는 중 (metadata + 3D만)…")
    run = lambda *a, **k: subprocess.run(a, check=True, **k)
    run("git", "clone", "--depth", "1", "--filter=blob:none", "--no-checkout", REPO_URL, str(REPO))
    run("git", "sparse-checkout", "init", "--no-cone", cwd=REPO)
    (REPO / ".git" / "info" / "sparse-checkout").write_text(
        "/assets/*/metadata.json\n/assets/*/3D/\n/assets/*/Default/3D/\n", encoding="utf-8")
    run("git", "checkout", cwd=REPO)


def load_index():
    if INDEX.exists():
        return load_json(INDEX, [])
    ensure_repo()
    items = []
    for meta in sorted((REPO / "assets").glob("*/metadata.json")):
        d = meta.parent
        pngs = list((d / "3D").glob("*.png")) or list((d / "Default" / "3D").glob("*.png"))
        if not pngs:
            continue
        m = json.loads(meta.read_text(encoding="utf-8"))
        items.append({
            "name": d.name,
            "cldr": m.get("cldr", d.name).lower(),
            "keywords": [k.lower() for k in m.get("keywords", [])],
            "file": pngs[0].relative_to(ROOT).as_posix(),
        })
    save_json(INDEX, items)
    return items


def emoji_by_name(index, name):
    for it in index:
        if it["name"].lower() == name.lower() or it["cldr"] == name.lower():
            return it
    return None


# ---------- 자동 매칭 ----------
def search_terms(meaning):
    m = re.sub(r"\([^)]*\)", "", meaning)
    terms = []
    for part in m.split("/"):
        t = re.sub(r"^(to|be|a|an|the)\s+", "", part.strip().lower())
        if t and t not in terms:
            terms.append(t)
    return terms


def score(item, term):
    words = set(re.findall(r"[a-z]+", item["cldr"]))
    if item["cldr"] == term:
        return 100
    if term in item["keywords"]:
        return 70 if " " not in item["cldr"] else 60
    if " " in term and term in item["cldr"]:
        return 55
    if term in words:
        return 40
    if any(term in k.split() for k in item["keywords"]):
        return 30
    return 0


def candidates(index, meaning, n=5):
    best = {}
    for term in search_terms(meaning):
        for it in index:
            s = score(it, term)
            if s and s > best.get(it["name"], (0,))[0]:
                best[it["name"]] = (s, term, it)
    ranked = sorted(best.values(), key=lambda x: (-x[0], len(x[2]["cldr"])))
    return ranked[:n]


# ---------- icon_map ----------
def icon_file(eid, word, src):
    ICONS.mkdir(exist_ok=True)
    dst = ICONS / f"{eid}_{word}{Path(src).suffix.lower()}"
    shutil.copyfile(src, dst)
    return dst.relative_to(ROOT).as_posix()


def assign_emoji(imap, entry, it, motion=None):
    imap[entry["id"]] = {
        "word": entry["word"], "source": "fluent", "name": it["name"],
        "file": icon_file(entry["id"], entry["word"], ROOT / it["file"]),
        "motion": motion or default_motion(entry), "license": FLUENT_LICENSE,
    }


# ---------- 명령 ----------
def session_words(doc, sid):
    for s in doc["sessions"]:
        if s["id"] == sid:
            return s, [(w, "new") for w in s["new_words"]] + [(w, "review") for w in s["review_words"]]
    sys.exit(f"세션 {sid}가 vocab.json에 없습니다. 먼저 vocab.py use로 기록하세요.")


def session_out_dir(sid):
    folder = SESSIONS / sid
    return (folder / f"{sid}_assets") if folder.is_dir() else (SESSIONS / f"{sid}_assets")


def is_abstract(entry):
    return entry["pos"] == "부사" or (entry["level"] in ("B1", "B2") and entry["pos"] != "명사")


def search_links(term):
    q = quote(term)
    return (f"[Flaticon](https://www.flaticon.com/search?word={q}%203d) · "
            f"[Icons8](https://icons8.com/icons/set/{quote(term.replace(' ', '-'))}--style-3d-fluency) · "
            f"[LottieFiles](https://lottiefiles.com/search?q={q}&category=animations)")


def cmd_fetch(a):
    doc, vidx = vocab_index()
    index = load_index()
    imap = load_json(ICON_MAP, {})
    sess, words = session_words(doc, a.session_id)

    rows, review, missing, abstract = [], [], [], []
    for eid, kind in words:
        e = vidx[eid]
        if eid not in imap:
            cands = candidates(index, e["meaning"])
            if cands and cands[0][0] >= AUTO_SCORE:
                assign_emoji(imap, e, cands[0][2])
            elif cands:
                review.append((e, cands))
            elif is_abstract(e):
                abstract.append(e)
            else:
                missing.append(e)
        rows.append((e, kind, imap.get(eid)))
    save_json(ICON_MAP, imap)

    out = session_out_dir(a.session_id)
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("[0-9][0-9]_*.*"):
        old.unlink()
    lines = [f"# {a.session_id} 아이콘 에셋 — {sess['situation']}", "",
             "| # | 단어 | 품사 | 구분 | 아이콘 | 출처 | 추천 모션 |", "|---|---|---|---|---|---|---|"]
    credits = []
    for n, (e, kind, m) in enumerate(rows, 1):
        tag = "새 단어" if kind == "new" else "복습"
        if m and m.get("file"):
            dst = out / f"{n:02d}_{e['word']}{Path(m['file']).suffix}"
            shutil.copyfile(ROOT / m["file"], dst)
            src = f"{m['source']} · {m['name']}"
            if m["source"] == "manual" and "MIT" not in m["license"]:
                credits.append(f"- {e['word']}: {m['name']} — {m['license']}")
            lines.append(f"| {n:02d} | {e['word']} | {e['pos']} | {tag} | ![]({dst.name}) | {src} | {m['motion']} |")
        elif m and m.get("source") == "abstract":
            lines.append(f"| {n:02d} | {e['word']} | {e['pos']} | {tag} | — | 장면 이미지 또는 생략 | none |")
        else:
            lines.append(f"| {n:02d} | {e['word']} | {e['pos']} | {tag} | ❓ | 미정 | {default_motion(e)} |")

    if review:
        lines += ["", "## 검토 필요", "자동 확정하지 않은 매칭. `python assets.py set <id> --emoji \"이름\"`으로 확정한다.", "",
                  "| 단어 | id | 뜻 | 후보 (점수) |", "|---|---|---|---|"]
        for e, cands in review:
            c = ", ".join(f"{it['name']} ({s})" for s, _, it in cands)
            lines.append(f"| {e['word']} | {e['id']} | {e['meaning']} | {c} |")
    if missing:
        lines += ["", "## 못 찾은 단어", "직접 찾아서 `python assets.py set <id> --file <경로> --license \"...\"`로 등록한다.", "",
                  "| 단어 | id | 검색어 | 링크 |", "|---|---|---|---|"]
        for e in missing:
            t = search_terms(e["meaning"])[0]
            lines.append(f"| {e['word']} | {e['id']} | {t} | {search_links(t)} |")
    if abstract:
        lines += ["", "## 추상어 (장면 이미지 또는 생략)", ""]
        lines += [f"- {e['word']} ({e['id']}, {e['meaning']})" for e in abstract]
    lines += ["", "## 출처 표기 (영상 설명란)", ""]
    lines += credits or ["- 표기 필요한 아이콘 없음. Fluent Emoji 3D와 그것을 합성한 자체 제작 아이콘은 MIT 라이선스로 별도 표기 불필요."]
    (out / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    done = sum(1 for _, _, m in rows if m)
    print(f"{a.session_id}: {len(rows)}개 중 {done}개 확정 · 검토 필요 {len(review)} · 못 찾음 {len(missing)} · 추상어 {len(abstract)}")
    print(f"→ {out.relative_to(ROOT)}/report.md")


def cmd_candidates(a):
    _, vidx = vocab_index()
    e = vidx.get(a.id) or sys.exit(f"없는 id: {a.id}")
    print(f"{e['word']} ({e['meaning']}) — 검색어: {', '.join(search_terms(e['meaning']))}")
    for s, term, it in candidates(load_index(), e["meaning"]):
        print(f"  {s:3d}  {it['name']:<35} [{term}]  {', '.join(it['keywords'][:6])}")


def cmd_set(a):
    _, vidx = vocab_index()
    e = vidx.get(a.id) or sys.exit(f"없는 id: {a.id}")
    imap = load_json(ICON_MAP, {})
    if a.emoji:
        it = emoji_by_name(load_index(), a.emoji) or sys.exit(f"이모지를 찾을 수 없음: {a.emoji}")
        assign_emoji(imap, e, it, a.motion)
    elif a.file:
        src = Path(a.file)
        if not src.exists():
            sys.exit(f"파일 없음: {src}")
        imap[a.id] = {"word": e["word"], "source": "manual", "name": a.name or src.stem,
                      "file": icon_file(a.id, e["word"], src), "motion": a.motion or default_motion(e),
                      "license": a.license or input("라이선스 (예: Flaticon, 출처 표기 필요): ").strip()}
    else:
        imap[a.id] = {"word": e["word"], "source": "abstract", "name": "", "file": "",
                      "motion": "none", "license": ""}
    save_json(ICON_MAP, imap)
    m = imap[a.id]
    print(f"{e['word']} ({a.id}) → {m['source']} {m['name']} {m['file']} [{m['motion']}]")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    f = sp.add_parser("fetch"); f.add_argument("session_id")
    c = sp.add_parser("candidates"); c.add_argument("id")
    s = sp.add_parser("set"); s.add_argument("id")
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--emoji"); g.add_argument("--file"); g.add_argument("--abstract", action="store_true")
    s.add_argument("--license"); s.add_argument("--name"); s.add_argument("--motion", choices=list(MOTION) + ["none"])
    a = p.parse_args()
    {"fetch": cmd_fetch, "candidates": cmd_candidates, "set": cmd_set}[a.cmd](a)


if __name__ == "__main__":
    main()
