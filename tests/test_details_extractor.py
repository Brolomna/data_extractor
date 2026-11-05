import json
import tempfile
import unittest
from pathlib import Path

from details_extractor import extract_file, find_records, format_records


class DataExtractorTests(unittest.TestCase):
    def test_finds_nested_records_without_mixing_fields(self):
        data = {
            "list": [
                {"nickname": "Ada", "user_id": 10, "nationality": "GB", "head_url": "a.png"},
                {"nickname": "Lin", "user_id": 11, "nationality": "TW", "head_url": "b.png"},
            ]
        }
        records = list(find_records(data))
        self.assertEqual([record["nickname"] for record in records], ["Ada", "Lin"])
        self.assertEqual([record["user_id"] for record in records], [10, 11])

    def test_ignores_incomplete_objects(self):
        data = {"nickname": "Partial", "user_id": 12}
        self.assertEqual(list(find_records(data)), [])

    def test_formats_empty_result(self):
        self.assertEqual(format_records([]), "")

    def test_writes_report_and_overwrites_existing_output(self):
        data = {"list": {"nickname": "Ada", "user_id": 10, "nationality": "GB", "head_url": "a.png"}}
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.json"
            output = Path(directory) / "report.txt"
            source.write_text(json.dumps(data), encoding="utf-8")
            output.write_text("old content", encoding="utf-8")
            self.assertEqual(extract_file(source, output), 1)
            report = output.read_text(encoding="utf-8")
            self.assertIn("Nickname: Ada", report)
            self.assertNotIn("old content", report)

    def test_rejects_same_input_and_output_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "same.json"
            path.write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                extract_file(path, path)


if __name__ == "__main__":
    unittest.main()
