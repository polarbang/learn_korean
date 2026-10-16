#!/usr/bin/env python3
"""한글 SBV에서 번역 표를 만들고 13개 언어의 SBV를 생성한다.

S005 이후 회차용. 번역 자체는 사람이 작성한다.

  python captions.py prepare S005
  python captions.py build S005
  python captions.py build S005 --only en ja
"""

import argparse
import csv
import os
import re
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LANGUAGES = (
    "en", "es", "zh-Hans", "fr", "id", "de", "pt-BR",
    "ar", "fil", "ja", "ru", "ms", "vi",
)
FIELDS = ("#", "ko", *LANGUAGES)
SID_RE = re.compile(r"S\d{3}\Z")
TIME_RE = re.compile(
    r"(?P<start>\d+:\d{2}:\d{2}\.\d{3}),(?P<end>\d+:\d{2}:\d{2}\.\d{3})\Z"
)


class CaptionError(Exception):
    pass


@dataclass(frozen=True)
class Cue:
    time: str
    text: str


def caption_paths(sid: str, root: Path = ROOT) -> tuple[Path, Path, Path]:
    if not SID_RE.fullmatch(sid):
        raise CaptionError(f"회차 ID 형식이 잘못됐습니다: {sid} (예: S005)")
    if int(sid[1:]) < 5:
        raise CaptionError("공통 자막 생성기는 S005부터 사용합니다. S001–S004는 기존 파일을 유지합니다")
    folder = root / "sessions" / sid / f"{sid}_captions"
    source = folder / f"{sid}_captions.kr.sbv"
    table = folder / f"{sid}_translations.tsv"
    return folder, source, table


def milliseconds(stamp: str) -> int:
    hours, minutes, rest = stamp.split(":")
    seconds, millis = rest.split(".")
    if int(minutes) >= 60 or int(seconds) >= 60:
        raise CaptionError(f"잘못된 타임코드: {stamp}")
    return ((int(hours) * 60 + int(minutes)) * 60 + int(seconds)) * 1000 + int(millis)


def read_sbv(path: Path) -> tuple[list[Cue], str]:
    try:
        raw = path.read_bytes()
    except FileNotFoundError as exc:
        raise CaptionError(f"자막 파일이 없습니다: {path}") from exc
    try:
        source = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise CaptionError(f"UTF-8 자막 파일이 아닙니다: {path}") from exc
    if b"\r\n" in raw and b"\n" in raw.replace(b"\r\n", b""):
        raise CaptionError(f"CRLF와 LF 줄바꿈이 섞여 있습니다: {path}")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    source = source.replace("\r\n", "\n")
    if "\r" in source:
        raise CaptionError(f"지원하지 않는 줄바꿈이 있습니다: {path}")
    source = source.strip("\n")
    if not source:
        raise CaptionError(f"빈 자막 파일입니다: {path}")

    cues = []
    for number, block in enumerate(re.split(r"\n[ \t]*\n", source), 1):
        parts = block.split("\n", 1)
        if len(parts) != 2:
            raise CaptionError(f"{path.name}의 {number}번 자막에 문장이 없습니다")
        time, phrase = parts
        match = TIME_RE.fullmatch(time)
        if not match:
            raise CaptionError(f"{path.name}의 {number}번 타임코드 형식 오류: {time}")
        if milliseconds(match["start"]) >= milliseconds(match["end"]):
            raise CaptionError(f"{path.name}의 {number}번 시작 시간이 종료 시간보다 늦습니다")
        phrase = phrase.strip()
        if not phrase:
            raise CaptionError(f"{path.name}의 {number}번 자막이 비어 있습니다")
        cues.append(Cue(time, phrase))
    return cues, newline


def unique_phrases(cues: list[Cue]) -> list[str]:
    return list(dict.fromkeys(cue.text for cue in cues))


def read_table(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            if tuple(reader.fieldnames or ()) != FIELDS:
                raise CaptionError(
                    f"번역 표의 열이 맞지 않습니다: {path}\n"
                    f"필요한 열: {', '.join(FIELDS)}"
                )
            rows = list(reader)
    except FileNotFoundError as exc:
        raise CaptionError(f"번역 표가 없습니다. 먼저 prepare를 실행하세요: {path}") from exc
    for number, row in enumerate(rows, 1):
        if None in row or any(value is None for value in row.values()):
            raise CaptionError(f"번역 표 {number}번 행의 열 개수가 맞지 않습니다")
        if row["#"] != str(number) or not row["ko"]:
            raise CaptionError(f"번역 표 {number}번 행의 번호나 한국어 문장이 잘못됐습니다")
    return rows


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=FIELDS, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temp, path)


def next_backup(path: Path) -> Path:
    number = 1
    while True:
        backup = path.with_name(f"{path.name}.bak{number}")
        if not backup.exists():
            return backup
        number += 1


def prepare(sid: str, root: Path = ROOT, refresh: bool = False) -> str:
    _, source, table = caption_paths(sid, root)
    cues, _ = read_sbv(source)
    phrases = unique_phrases(cues)
    if table.exists() and not refresh:
        raise CaptionError(
            f"번역 표가 이미 있습니다: {table}\n"
            "한글 자막을 고친 뒤 표를 갱신하려면 prepare --refresh를 사용하세요."
        )
    previous = {}
    backup = None
    if table.exists():
        previous = {row["ko"]: row for row in read_table(table)}
        backup = next_backup(table)
        shutil.copy2(table, backup)
    rows = []
    for number, phrase in enumerate(phrases, 1):
        row = {field: "" for field in FIELDS}
        row["#"], row["ko"] = str(number), phrase
        if phrase in previous:
            row.update({lang: previous[phrase][lang] for lang in LANGUAGES})
        rows.append(row)
    write_table(table, rows)
    repeated = sum(count - 1 for count in Counter(cue.text for cue in cues).values())
    message = (
        f"{sid}: 자막 {len(cues)}개 → 번역할 문장 {len(phrases)}개 "
        f"(반복 {repeated}개 재사용)\n번역 표: {table}"
    )
    if backup:
        removed = len(set(previous) - set(phrases))
        message += f"\n기존 번역 {len(previous)}개 중 제거된 문장 {removed}개 · 백업: {backup}"
    return message


def build(
    sid: str, root: Path = ROOT, only: tuple[str, ...] | None = None
) -> str:
    folder, source, table = caption_paths(sid, root)
    cues, newline = read_sbv(source)
    phrases = unique_phrases(cues)
    rows = read_table(table)
    if [row["ko"] for row in rows] != phrases:
        raise CaptionError(
            "한글 자막과 번역 표의 문장·순서가 다릅니다. "
            f"python captions.py prepare {sid} --refresh로 갱신하세요."
        )
    selected = tuple(dict.fromkeys(only or LANGUAGES))
    invalid = set(selected) - set(LANGUAGES)
    if invalid:
        raise CaptionError(f"지원하지 않는 언어: {', '.join(sorted(invalid))}")
    missing = [
        f"{row['#']}번 {lang}: {row['ko']}"
        for row in rows
        for lang in selected
        if not row[lang].strip()
    ]
    if missing:
        preview = "\n".join(missing[:12])
        extra = f"\n... 외 {len(missing) - 12}개" if len(missing) > 12 else ""
        raise CaptionError(f"번역이 비어 있습니다 ({len(missing)}개):\n{preview}{extra}")
    translations = {
        lang: {row["ko"]: row[lang].strip().replace("\r\n", "\n") for row in rows}
        for lang in selected
    }
    for lang, mapping in translations.items():
        if any("\n\n" in phrase or "\r" in phrase for phrase in mapping.values()):
            raise CaptionError(f"{lang} 번역에 빈 줄 또는 잘못된 줄바꿈이 있습니다")
    for lang, mapping in translations.items():
        content = "\n\n".join(
            f"{cue.time}\n{mapping[cue.text]}" for cue in cues
        ) + "\n"
        path = folder / f"{sid}_captions.{lang}.sbv"
        temp = path.with_name(path.name + ".tmp")
        temp.write_bytes(content.replace("\n", newline).encode("utf-8"))
        generated, _ = read_sbv(temp)
        if [cue.time for cue in generated] != [cue.time for cue in cues]:
            temp.unlink()
            raise CaptionError(f"생성된 {lang} 자막의 타임코드가 달라졌습니다")
        os.replace(temp, path)
    return f"{sid}: {len(selected)}개 언어 · 언어별 {len(cues)}개 자막 생성 및 타임코드 검증 완료"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare", help="한글 SBV에서 번역 표 생성")
    prep.add_argument("session_id")
    prep.add_argument("--refresh", action="store_true", help="한글 자막 변경 내용을 반영하고 기존 번역 보존")
    output = commands.add_parser("build", help="번역 표에서 다국어 SBV 생성")
    output.add_argument("session_id")
    output.add_argument("--only", nargs="+", choices=LANGUAGES)
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            print(prepare(args.session_id, refresh=args.refresh))
        else:
            print(build(args.session_id, only=tuple(args.only) if args.only else None))
    except CaptionError as exc:
        print(f"[오류] {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
