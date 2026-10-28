import tempfile
import unittest
from pathlib import Path

import captions


class CaptionWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.folder, self.source, self.table = captions.caption_paths("S006", self.root)
        self.folder.mkdir(parents=True)
        self.times = [
            "0:00:01.000,0:00:02.000",
            "0:00:03.000,0:00:04.000",
            "0:00:05.000,0:00:06.000",
        ]
        self.source.write_bytes(
            (
                f"{self.times[0]}\n안녕하세요\n\n"
                f"{self.times[1]}\n오늘은\n커피를 마셔요.\n\n"
                f"{self.times[2]}\n안녕하세요\n"
            ).replace("\n", "\r\n").encode("utf-8")
        )

    def test_prepare_and_build_all_languages_preserves_cues(self):
        message = captions.prepare("S006", self.root)
        self.assertIn("번역할 문장 2개", message)
        rows = captions.read_table(self.table)
        self.assertEqual([row["ko"] for row in rows], ["안녕하세요", "오늘은\n커피를 마셔요."])
        for row in rows:
            for lang in captions.LANGUAGES:
                row[lang] = f"{lang} 번역 {row['#']}"
        rows[1]["en"] = "Today I\nhave coffee."
        captions.write_table(self.table, rows)

        captions.build("S006", self.root)

        for lang in captions.LANGUAGES:
            output = self.folder / f"S006_captions.{lang}.sbv"
            raw = output.read_bytes()
            self.assertIn(b"\r\n", raw)
            self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))
            cues, newline = captions.read_sbv(output)
            self.assertEqual(newline, "\r\n")
            self.assertEqual([cue.time for cue in cues], self.times)
            self.assertEqual(cues[0].text, cues[2].text)
        en_cues, _ = captions.read_sbv(self.folder / "S006_captions.en.sbv")
        self.assertEqual(en_cues[1].text, "Today I\nhave coffee.")

    def test_missing_translation_stops_before_creating_files(self):
        captions.prepare("S006", self.root)
        rows = captions.read_table(self.table)
        for row in rows:
            row["en"] = "English"
        rows[1]["en"] = ""
        captions.write_table(self.table, rows)

        with self.assertRaisesRegex(captions.CaptionError, "번역이 비어"):
            captions.build("S006", self.root, only=("en",))
        self.assertFalse((self.folder / "S006_captions.en.sbv").exists())

    def test_refresh_keeps_unchanged_translations_and_backs_up_table(self):
        captions.prepare("S006", self.root)
        rows = captions.read_table(self.table)
        rows[0]["en"] = "Hello"
        rows[1]["en"] = "Coffee"
        captions.write_table(self.table, rows)
        self.source.write_text(
            f"{self.times[0]}\n안녕하세요\n\n{self.times[1]}\n새 문장\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(captions.CaptionError, "--refresh"):
            captions.build("S006", self.root, only=("en",))
        captions.prepare("S006", self.root, refresh=True)

        updated = captions.read_table(self.table)
        self.assertEqual([row["ko"] for row in updated], ["안녕하세요", "새 문장"])
        self.assertEqual([row["en"] for row in updated], ["Hello", ""])
        backup = self.table.with_name(self.table.name + ".bak1")
        self.assertEqual([row["en"] for row in captions.read_table(backup)], ["Hello", "Coffee"])

    def test_earlier_sessions_are_rejected(self):
        with self.assertRaisesRegex(captions.CaptionError, "S006부터"):
            captions.caption_paths("S005", self.root)


if __name__ == "__main__":
    unittest.main()
