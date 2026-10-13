#!/usr/bin/env python3
"""한국어 어휘 트래커 — vocab.json의 미사용/사용 상태를 관리한다.

사용법:
  python vocab.py stats                         레벨·품사별 사용/미사용 현황
  python vocab.py unused A1 [--pos 명사] [--limit 40]
                                                미사용 단어를 빈도순으로 출력
  python vocab.py find 사과                      단어 검색 (id, 상태, 사용 세션)
  python vocab.py sessions                      세션 기록 출력
  python vocab.py use S001 --level A1 --situation "마트에서" \\
        --new A1-N-010 과일 ... --review A1-N-001 ...
                                                세션 기록 + 새 단어를 '사용'으로 이동
  python vocab.py undo S001                     세션 기록과 사용 처리를 되돌림
단어는 id(A1-N-010) 또는 단어 자체(과일)로 지정할 수 있다.
같은 단어가 여러 개면 id로 지정해야 한다.
"""
import argparse, json, os, re, sys

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vocab.json")
LEVELS = ["A1", "A2", "B1", "B2"]
POS = ["명사", "동사", "형용사", "부사"]
ID_RE = re.compile(r"^(A1|A2|B1|B2)-(N|V|ADJ|ADV)-\d{3}$")


def load():
    with open(PATH, encoding="utf-8") as f:
        return json.load(f)


def save(doc):
    """단어 하나당 한 줄로 저장 (git diff를 읽기 쉽게)."""
    j = lambda o: json.dumps(o, ensure_ascii=False)
    lines = ["{", f' "meta": {j(doc["meta"])},', ' "sessions": [']
    lines.append(",\n".join(f"  {j(s)}" for s in doc["sessions"]))
    lines.append(" ],")
    lines.append(' "levels": {')
    lv_blocks = []
    for lv in LEVELS:
        pos_blocks = []
        for p in POS:
            b = doc["levels"][lv][p]
            parts = []
            for st in ("미사용", "사용"):
                items = sorted(b[st], key=lambda e: e["rank"])
                body = ",\n".join(f"     {j(e)}" for e in items)
                parts.append(f'    "{st}": [\n{body}\n    ]' if items else f'    "{st}": []')
            pos_blocks.append(f'   "{p}": {{\n' + ",\n".join(parts) + "\n   }")
        lv_blocks.append(f'  "{lv}": {{\n' + ",\n".join(pos_blocks) + "\n  }")
    lines.append(",\n".join(lv_blocks))
    lines.append(" }")
    lines.append("}")
    tmp = PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    json.load(open(tmp, encoding="utf-8"))  # 검증
    os.replace(tmp, PATH)


def all_entries(doc):
    for lv in LEVELS:
        for p in POS:
            for st in ("미사용", "사용"):
                for e in doc["levels"][lv][p][st]:
                    yield lv, p, st, e


def resolve(doc, key):
    hits = [(lv, p, st, e) for lv, p, st, e in all_entries(doc)
            if (e["id"] == key if ID_RE.match(key) else e["word"] == key)]
    if not hits:
        sys.exit(f"[오류] '{key}' 항목을 찾을 수 없습니다.")
    if len(hits) > 1:
        opts = ", ".join(f'{e["id"]}({e["meaning"]})' for *_, e in hits)
        sys.exit(f"[오류] '{key}' 항목이 여러 개입니다. id로 지정하세요: {opts}")
    return hits[0]


def cmd_stats(doc, a):
    tu = tn = 0
    print(f'{"레벨":<4} {"품사":<5} {"사용":>5} {"미사용":>6} {"전체":>5}')
    for lv in LEVELS:
        for p in POS:
            b = doc["levels"][lv][p]
            u, n = len(b["사용"]), len(b["미사용"])
            tu += u; tn += n
            print(f"{lv:<5} {p:<5} {u:>5} {n:>6} {u+n:>5}")
    print(f"합계        {tu:>5} {tn:>6} {tu+tn:>5}  (세션 {len(doc['sessions'])}개)")


def cmd_unused(doc, a):
    lv = a.level.upper()
    for p in ([a.pos] if a.pos else POS):
        items = sorted(doc["levels"][lv][p]["미사용"], key=lambda e: e["rank"])[: a.limit]
        print(f"\n[{lv} {p}] 미사용 {len(doc['levels'][lv][p]['미사용'])}개 중 상위 {len(items)}개")
        for e in items:
            print(f'  {e["id"]}  {e["word"]}  — {e["meaning"]}')


def cmd_find(doc, a):
    found = False
    for lv, p, st, e in all_entries(doc):
        if a.word in e["word"]:
            found = True
            used = ", ".join(e["used_in"]) or "-"
            print(f'{e["id"]}  {e["word"]}  ({e["meaning"]})  [{st}]  세션: {used}')
    if not found:
        print("결과 없음")


def cmd_sessions(doc, a):
    if not doc["sessions"]:
        print("세션 기록 없음"); return
    for s in doc["sessions"]:
        print(f'{s["id"]}  {s["level"]}  {s["situation"]}  새 단어 {len(s["new_words"])}개 / 복습 {len(s["review_words"])}개')


def cmd_use(doc, a):
    sid = a.session_id
    if any(s["id"] == sid for s in doc["sessions"]):
        sys.exit(f"[오류] 세션 {sid}는 이미 있습니다.")
    new_ids, rev_ids = [], []
    for key in a.new:
        lv, p, st, e = resolve(doc, key)
        if st == "사용":
            print(f'[알림] {e["word"]}({e["id"]})는 이미 사용됨 → 복습 단어로 기록합니다.')
            rev_ids.append(e["id"]); continue
        new_ids.append(e["id"])
    for key in a.review or []:
        lv, p, st, e = resolve(doc, key)
        if st == "미사용":
            print(f'[알림] {e["word"]}({e["id"]})는 아직 미사용 → 새 단어로 기록합니다.')
            new_ids.append(e["id"]); continue
        rev_ids.append(e["id"])
    new_ids = list(dict.fromkeys(new_ids)); rev_ids = list(dict.fromkeys(rev_ids))
    for key in new_ids:
        lv, p, st, e = resolve(doc, key)
        b = doc["levels"][lv][p]
        b["미사용"].remove(e); e["used_in"].append(sid); b["사용"].append(e)
    for key in rev_ids:
        lv, p, st, e = resolve(doc, key)
        e["used_in"].append(sid)
    doc["sessions"].append({"id": sid, "level": a.level.upper(), "situation": a.situation,
                            "new_words": new_ids, "review_words": rev_ids})
    save(doc)
    print(f"{sid} 기록 완료: 새 단어 {len(new_ids)}개, 복습 {len(rev_ids)}개")
    if not 20 <= len(new_ids) <= 30:
        print(f"[주의] 새 단어가 {len(new_ids)}개입니다 (기준 20~30개 — 상황에 맞으면 더 많아도 됨).")


def cmd_undo(doc, a):
    s = next((s for s in doc["sessions"] if s["id"] == a.session_id), None)
    if not s:
        sys.exit(f"[오류] 세션 {a.session_id}가 없습니다.")
    for key in s["new_words"] + s["review_words"]:
        lv, p, st, e = resolve(doc, key)
        e["used_in"] = [x for x in e["used_in"] if x != s["id"]]
        if not e["used_in"] and st == "사용":
            b = doc["levels"][lv][p]; b["사용"].remove(e); b["미사용"].append(e)
    doc["sessions"].remove(s)
    save(doc)
    print(f'{s["id"]} 되돌림 완료')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("stats")
    u = sp.add_parser("unused"); u.add_argument("level"); u.add_argument("--pos", choices=POS); u.add_argument("--limit", type=int, default=40)
    f = sp.add_parser("find"); f.add_argument("word")
    sp.add_parser("sessions")
    us = sp.add_parser("use"); us.add_argument("session_id"); us.add_argument("--level", required=True)
    us.add_argument("--situation", required=True); us.add_argument("--new", nargs="+", required=True); us.add_argument("--review", nargs="*")
    ud = sp.add_parser("undo"); ud.add_argument("session_id")
    a = ap.parse_args()
    doc = load()
    {"stats": cmd_stats, "unused": cmd_unused, "find": cmd_find, "sessions": cmd_sessions,
     "use": cmd_use, "undo": cmd_undo}[a.cmd](doc, a)


if __name__ == "__main__":
    main()
