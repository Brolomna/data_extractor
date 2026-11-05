import csv
import json
import tempfile
import unittest
from pathlib import Path

from details_extractor import extract_file, find_records, format_text


class DataExtractorTests(unittest.TestCase):
    def setUp(self):
        self.record = {
            "nickname": "Ada",
            "user_id": 10,
            "nationality": "GB",
            "head_url": "a.png",
        }

    def test_finds_nested_records_without_mixing_fields(self):
        data = {"list": [self.record, {**self.record, "nickname": "Lin", "user_id": 11}]}
        records = list(find_records(data))
        self.assertEqual([record["nickname"] for record in records], ["Ada", "Lin"])
        self.assertEqual([record["user_id"] for record in records], [10, 11])

    def test_ignores_incomplete_objects(self):
        self.assertEqual(list(find_records({"nickname": "Partial", "user_id": 12})), [])

    def test_finds_matching_parent_and_nested_objects(self):
        nested_record = {**self.record, "nickname": "Nested"}
        parent = {**self.record, "nested": nested_record}
        records = list(find_records(parent))
        self.assertEqual([record["nickname"] for record in records], ["Ada", "Nested"])

    def test_formats_empty_result(self):
        self.assertEqual(format_text([]), "")

    def test_writes_text_report_and_replaces_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / "input.json", Path(directory) / "report.txt"
            source.write_text(json.dumps({"list": self.record}), encoding="utf-8")
            output.write_text("old content", encoding="utf-8")
            self.assertEqual(extract_file(source, output), 1)
            self.assertIn("Nickname: Ada", output.read_text(encoding="utf-8"))
            self.assertNotIn("old content", output.read_text(encoding="utf-8"))

    def test_writes_valid_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / "input.json", Path(directory) / "report.csv"
            source.write_text(json.dumps([self.record]), encoding="utf-8")
            self.assertEqual(extract_file(source, output, "csv"), 1)
            with output.open(encoding="utf-8", newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(rows[0]["nickname"], "Ada")
            self.assertEqual(rows[0]["user_id"], "10")

    def test_writes_valid_json(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / "input.json", Path(directory) / "report.json"
            source.write_text(json.dumps([self.record]), encoding="utf-8")
            self.assertEqual(extract_file(source, output, "json"), 1)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))[0], self.record)

    def test_rejects_same_input_and_output_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "same.json"
            path.write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                extract_file(path, path)


if __name__ == "__main__":
    unittest.main()
