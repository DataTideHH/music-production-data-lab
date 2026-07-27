from __future__ import annotations

import csv
import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "scripts" / "generate_analysis_report.py"
SPEC = importlib.util.spec_from_file_location("generate_analysis_report", MODULE_PATH)
assert SPEC and SPEC.loader
generate_analysis_report = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = generate_analysis_report
SPEC.loader.exec_module(generate_analysis_report)


class GenerateAnalysisReportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "project"
        shutil.copytree(REPOSITORY_ROOT / "data", self.project_root / "data")
        shutil.copytree(REPOSITORY_ROOT / "sql", self.project_root / "sql")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_generated_outputs_are_complete_and_data_backed(self) -> None:
        paths = generate_analysis_report.generate_analysis_outputs(self.project_root)

        self.assertEqual(len(paths), 4)
        for path in paths:
            self.assertTrue(path.exists(), path)

        summary_path = self.project_root / "data" / "processed" / "analysis_summary.csv"
        with summary_path.open(newline="", encoding="utf-8") as file:
            rows = {row["metric_name"]: row for row in csv.DictReader(file)}

        self.assertEqual(rows["equipment_items"]["metric_value"], "30")
        self.assertEqual(rows["soundchains"]["metric_value"], "12")
        self.assertEqual(rows["equipment_uses"]["metric_value"], "53")
        self.assertEqual(rows["equipment_coverage_percent"]["metric_value"], "80")

        generated_markdown = (
            self.project_root / "docs" / "generated-analysis-summary.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Equipment records | 30", generated_markdown)
        self.assertIn("Equipment coverage | 80%", generated_markdown)

    def test_equipment_usage_output_is_sorted_by_reuse(self) -> None:
        generate_analysis_report.generate_analysis_outputs(self.project_root)

        usage_path = (
            self.project_root
            / "data"
            / "processed"
            / "equipment_usage_summary.csv"
        )
        with usage_path.open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))

        usage_counts = [int(row["soundchain_usage_count"]) for row in rows]
        self.assertEqual(usage_counts, sorted(usage_counts, reverse=True))
        self.assertEqual(usage_counts[0], 5)


if __name__ == "__main__":
    unittest.main()
