from __future__ import annotations

import csv
from contextlib import closing
import importlib.util
import shutil
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "scripts" / "build_database.py"
SPEC = importlib.util.spec_from_file_location("build_database", MODULE_PATH)
assert SPEC and SPEC.loader
build_database = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = build_database
SPEC.loader.exec_module(build_database)


class BuildDatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "project"
        shutil.copytree(REPOSITORY_ROOT / "data", self.project_root / "data")
        shutil.copytree(REPOSITORY_ROOT / "sql", self.project_root / "sql")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def csv_path(self, name: str) -> Path:
        return self.project_root / "data" / "public" / name

    def read_rows(self, name: str) -> tuple[list[str], list[dict[str, str]]]:
        path = self.csv_path(name)
        with path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader.fieldnames or []), list(reader)

    def write_rows(
        self,
        name: str,
        fieldnames: list[str],
        rows: list[dict[str, str]],
    ) -> None:
        path = self.csv_path(name)
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def test_successful_build_has_expected_tables_and_counts(self) -> None:
        output = self.project_root / "db" / "test.sqlite"

        summary = build_database.build_database(
            project_root=self.project_root,
            db_path=output,
        )

        self.assertEqual(
            summary.row_counts,
            {
                "equipment": 10,
                "music_references": 8,
                "soundchains": 5,
                "soundchain_equipment": 16,
            },
        )
        self.assertTrue(output.exists())

        with closing(sqlite3.connect(output)) as connection:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }
        self.assertTrue(
            {"equipment", "music_references", "soundchains", "soundchain_equipment"}
            <= tables
        )

    def test_duplicate_primary_key_is_rejected(self) -> None:
        name = "equipment_public.csv"
        fields, rows = self.read_rows(name)
        rows.append(dict(rows[0]))
        self.write_rows(name, fields, rows)

        with self.assertRaisesRegex(build_database.BuildError, "Duplicate key values"):
            build_database.validate_csv_files(self.project_root)

    def test_missing_csv_is_rejected(self) -> None:
        self.csv_path("music_references_public.csv").unlink()

        with self.assertRaisesRegex(build_database.BuildError, "Missing CSV file"):
            build_database.validate_csv_files(self.project_root)

    def test_wrong_column_structure_is_rejected(self) -> None:
        name = "equipment_public.csv"
        fields, rows = self.read_rows(name)
        fields.remove("public_notes")
        trimmed = [{key: value for key, value in row.items() if key in fields} for row in rows]
        self.write_rows(name, fields, trimmed)

        with self.assertRaisesRegex(build_database.BuildError, "Unexpected columns"):
            build_database.validate_csv_files(self.project_root)

    def test_unknown_foreign_key_is_rejected(self) -> None:
        name = "soundchains_public.csv"
        fields, rows = self.read_rows(name)
        rows[0]["primary_reference_id"] = "REF-9999"
        self.write_rows(name, fields, rows)

        with self.assertRaisesRegex(build_database.BuildError, "unknown primary_reference_id"):
            build_database.validate_csv_files(self.project_root)

    def test_invalid_privacy_level_is_rejected(self) -> None:
        name = "equipment_public.csv"
        fields, rows = self.read_rows(name)
        rows[0]["privacy_level"] = "private"
        self.write_rows(name, fields, rows)

        with self.assertRaisesRegex(build_database.BuildError, "invalid privacy_level"):
            build_database.validate_csv_files(self.project_root)

    def test_invalid_hardware_software_combination_is_rejected(self) -> None:
        name = "equipment_public.csv"
        fields, rows = self.read_rows(name)
        rows[0]["is_hardware"] = "true"
        rows[0]["is_software"] = "true"
        self.write_rows(name, fields, rows)

        with self.assertRaisesRegex(build_database.BuildError, "exactly one"):
            build_database.validate_csv_files(self.project_root)

    def test_duplicate_soundchain_position_is_rejected(self) -> None:
        name = "soundchain_equipment_public.csv"
        fields, rows = self.read_rows(name)
        duplicate_position = dict(rows[1])
        duplicate_position["equipment_id"] = "EQP-0008"
        rows.append(duplicate_position)
        self.write_rows(name, fields, rows)

        with self.assertRaisesRegex(build_database.BuildError, "Duplicate key values"):
            build_database.validate_csv_files(self.project_root)

    def test_sensitive_public_value_is_rejected(self) -> None:
        name = "equipment_public.csv"

        for sensitive_note in (
            "Invoice 12345 is stored privately.",
            "price 9999",
            "purchase 12345",
        ):
            with self.subTest(sensitive_note=sensitive_note):
                fields, rows = self.read_rows(name)
                rows[0]["public_notes"] = sensitive_note
                self.write_rows(name, fields, rows)

                with self.assertRaisesRegex(
                    build_database.BuildError,
                    "Potentially sensitive content",
                ):
                    build_database.validate_csv_files(self.project_root)

        fields, rows = self.read_rows(name)
        rows[0]["public_notes"] = "Use the Snowball microphone for this workflow."
        self.write_rows(name, fields, rows)

        build_database.validate_csv_files(self.project_root)

    def test_existing_custom_output_requires_overwrite(self) -> None:
        output = Path(self.temp_dir.name) / "custom.sqlite"
        output.write_bytes(b"existing")

        with self.assertRaisesRegex(build_database.BuildError, "--overwrite"):
            build_database.build_database(
                project_root=self.project_root,
                db_path=output,
            )

    def test_existing_custom_output_can_be_replaced_explicitly(self) -> None:
        output = Path(self.temp_dir.name) / "custom.sqlite"
        output.write_bytes(b"existing")

        summary = build_database.build_database(
            project_root=self.project_root,
            db_path=output,
            overwrite=True,
        )

        self.assertEqual(summary.database_path, output.resolve())
        with closing(sqlite3.connect(output)) as connection:
            self.assertEqual(
                connection.execute("SELECT COUNT(*) FROM equipment").fetchone()[0],
                10,
            )

    def test_external_output_path_is_supported(self) -> None:
        output = Path(self.temp_dir.name) / "external" / "build.sqlite"

        summary = build_database.build_database(
            project_root=self.project_root,
            db_path=output,
        )

        self.assertEqual(summary.database_path, output.resolve())
        self.assertEqual(
            build_database.display_path(summary.database_path, self.project_root),
            str(output.resolve()),
        )


if __name__ == "__main__":
    unittest.main()
