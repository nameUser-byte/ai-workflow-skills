"""Behavioral checks for the read-only CSV/visible-list comparator."""

import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/verify-with-evidence/scripts/compare_lists.py"
spec = importlib.util.spec_from_file_location("compare_lists", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.visible = self.root / "visible.json"
        self.exported = self.root / "export.csv"

    def prepare(self, visible, rows, fields=("ID", "메모")):
        self.visible.write_text(json.dumps(visible), encoding="utf8")
        with self.exported.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(fields)
            writer.writerows(rows)

    def compare(self):
        return module.compare(self.visible, self.exported, "ID")

    def test_matching_ids_and_quoted_unicode_memo(self):
        self.prepare(["R001", "R002"], [["R001", '검토, "확인"\n필요'], ["R002", "완료"]])
        self.assertEqual(self.compare()["result"], "PASS")

    def test_hidden_cancelled_row_is_detected(self):
        self.prepare(["R001", "R002"], [["R001", ""], ["R002", ""], ["R003", "취소"]])
        report = self.compare()
        self.assertEqual(report["result"], "MISMATCH")
        self.assertEqual(report["unexpected_in_csv"], ["R003"])
        self.assertEqual((report["visible_count"], report["csv_count"]), (2, 3))

    def test_same_count_with_wrong_id_is_detected(self):
        self.prepare(["R001", "R002"], [["R001", ""], ["R003", ""]])
        report = self.compare()
        self.assertEqual(report["missing_in_csv"], ["R002"])
        self.assertEqual(report["unexpected_in_csv"], ["R003"])

    def test_duplicate_ids_are_not_silently_accepted(self):
        self.prepare(["R001", "R001"], [["R001", ""], ["R001", ""]])
        report = self.compare()
        self.assertEqual(report["result"], "MISMATCH")
        self.assertEqual(report["duplicate_csv_ids"], ["R001"])

    def test_order_difference_is_reported(self):
        self.prepare(["R001", "R002"], [["R002", ""], ["R001", ""]])
        self.assertFalse(self.compare()["same_order"])

    def test_empty_filtered_result_matches_header_only_csv(self):
        self.prepare([], [])
        self.assertEqual(self.compare()["result"], "PASS")

    def test_missing_id_column_is_invalid_input(self):
        self.prepare(["R001"], [["R001", ""]], fields=("wrong", "메모"))
        with self.assertRaises(ValueError):
            self.compare()

    def test_row_width_mismatch_is_invalid_input(self):
        self.prepare(["R001"], [["R001"]])
        with self.assertRaises(ValueError):
            self.compare()

    def test_inputs_are_unchanged(self):
        self.prepare(["R001"], [["R001", "확인"]])
        before = [hashlib.sha256(p.read_bytes()).hexdigest() for p in (self.visible, self.exported)]
        self.compare()
        self.assertEqual(before, [hashlib.sha256(p.read_bytes()).hexdigest() for p in (self.visible, self.exported)])

    def test_cli_exit_codes_match_actual_outcome(self):
        for rows, code, result in (([["R001", ""]], 0, "PASS"), ([["R002", ""]], 1, "MISMATCH")):
            self.prepare(["R001"], rows)
            run = subprocess.run([sys.executable, str(SCRIPT), "--visible-ids", str(self.visible), "--csv", str(self.exported), "--id-column", "ID"], capture_output=True, text=True)
            self.assertEqual(run.returncode, code)
            self.assertEqual(json.loads(run.stdout)["result"], result)
        self.visible.write_text('{"not":"a list"}', encoding="utf8")
        run = subprocess.run([sys.executable, str(SCRIPT), "--visible-ids", str(self.visible), "--csv", str(self.exported), "--id-column", "ID"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(json.loads(run.stdout)["result"], "INPUT_ERROR")


if __name__ == "__main__":
    unittest.main()
