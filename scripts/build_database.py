#!/usr/bin/env python3
"""Build and validate the public SQLite data product.

The workflow is intentionally dependency-free and targets Python 3.12.
It validates the committed public CSV files, builds a SQLite database,
executes analytical SQL, and requires all data-quality queries to return no rows.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sqlite3
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = PROJECT_ROOT / "db" / "music_production_data_lab.sqlite"

TABLE_FILES = {
    "equipment": "equipment_public.csv",
    "music_references": "music_references_public.csv",
    "soundchains": "soundchains_public.csv",
    "soundchain_equipment": "soundchain_equipment_public.csv",
}

EXPECTED_COLUMNS = {
    "equipment": [
        "equipment_id",
        "category",
        "subcategory",
        "brand",
        "model",
        "public_name",
        "status_public",
        "setup_domain",
        "primary_role",
        "is_hardware",
        "is_software",
        "analog_digital",
        "mono_stereo",
        "power_category",
        "power_notes_public",
        "data_quality_status",
        "privacy_level",
        "public_notes",
    ],
    "music_references": [
        "reference_id",
        "artist_or_band",
        "sound_axis",
        "importance_public",
        "reference_role",
        "learning_focus",
        "production_focus",
        "gear_anchor_public",
        "tuning_notes_public",
        "dashboard_group",
        "data_quality_status",
        "privacy_level",
        "public_notes",
    ],
    "soundchains": [
        "soundchain_id",
        "chain_name",
        "target_sound",
        "sound_axis",
        "workflow_type",
        "tuning_context",
        "primary_reference_id",
        "primary_instrument_id",
        "output_equipment_id",
        "output_context",
        "complexity_level",
        "status_public",
        "privacy_level",
        "public_description",
    ],
    "soundchain_equipment": [
        "soundchain_id",
        "equipment_id",
        "position_in_chain",
        "role_in_chain",
        "required_or_optional",
        "sequence_group",
        "public_notes",
    ],
}

PRIMARY_KEYS = {
    "equipment": ("equipment_id",),
    "music_references": ("reference_id",),
    "soundchains": ("soundchain_id",),
    "soundchain_equipment": ("soundchain_id", "position_in_chain"),
}

REQUIRED_FIELDS = {
    "equipment": ("equipment_id", "category", "public_name", "status_public", "privacy_level"),
    "music_references": (
        "reference_id",
        "artist_or_band",
        "sound_axis",
        "data_quality_status",
        "privacy_level",
    ),
    "soundchains": (
        "soundchain_id",
        "chain_name",
        "workflow_type",
        "complexity_level",
        "status_public",
        "privacy_level",
    ),
    "soundchain_equipment": (
        "soundchain_id",
        "equipment_id",
        "position_in_chain",
        "role_in_chain",
        "required_or_optional",
        "sequence_group",
    ),
}

ALLOWED_VALUES: Mapping[str, Mapping[str, set[str]]] = {
    "equipment": {
        "category": {
            "instrument",
            "effect",
            "amplification",
            "recording_hardware",
            "midi_controller",
            "software",
            "power_utility",
        },
        "status_public": {"available", "planned", "reference"},
        "is_hardware": {"true", "false"},
        "is_software": {"true", "false"},
        "analog_digital": {"analog", "digital", "hybrid", "not_applicable"},
        "mono_stereo": {"mono", "stereo", "both", "not_applicable"},
        "data_quality_status": {"sample", "verified", "needs_verification"},
        "privacy_level": {"public_sample"},
    },
    "music_references": {
        "importance_public": {"core", "context"},
        "reference_role": {
            "playing_reference",
            "sound_design_reference",
            "songwriting_reference",
            "rhythm_reference",
            "production_reference",
        },
        "data_quality_status": {"sample", "verified", "needs_verification"},
        "privacy_level": {"public_sample"},
    },
    "soundchains": {
        "workflow_type": {"guitar_signal_chain", "recording_workflow"},
        "complexity_level": {"basic", "intermediate", "advanced"},
        "status_public": {"draft_public_sample", "verified_public_sample"},
        "privacy_level": {"public_sample"},
    },
    "soundchain_equipment": {
        "required_or_optional": {"required", "optional", "swap_candidate"},
        "sequence_group": {
            "input",
            "input_output",
            "gain_stage",
            "modulation",
            "midi",
            "software",
            "output",
        },
    },
}

FORBIDDEN_COLUMN_TOKENS = {
    "serial",
    "serial_number",
    "invoice",
    "purchase_price",
    "purchase_date",
    "storage_location",
    "private_condition",
}

SENSITIVE_WORD_PATTERNS = (
    re.compile(r"\b(?:serial|serial number|seriennummer|invoice|rechnung|kaufpreis)\b", re.IGNORECASE),
    re.compile(r"\b(?:purchase price|purchase date|storage location)\b", re.IGNORECASE),
)
CURRENCY_PATTERN = re.compile(
    r"(?:[$€£]\s?\d[\d.,]*|\b\d[\d.,]*\s?(?:EUR|USD|GBP)\b)",
    re.IGNORECASE,
)
SERIAL_VALUE_PATTERN = re.compile(r"\b(?:S/N|SN)[:#\s-]*[A-Z0-9-]{6,}\b", re.IGNORECASE)


class BuildError(RuntimeError):
    """Raised when validation or database construction fails."""


@dataclass(frozen=True)
class BuildSummary:
    database_path: Path
    row_counts: dict[str, int]


def display_path(path: Path, project_root: Path) -> str:
    """Return a stable human-readable path for repository-local or external files."""
    try:
        return str(path.resolve().relative_to(project_root.resolve()))
    except ValueError:
        return str(path.resolve())


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise BuildError(f"Missing CSV file: {path}")

    try:
        with path.open(newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            columns = reader.fieldnames or []
    except (OSError, UnicodeError, csv.Error) as error:
        raise BuildError(f"Unable to read CSV file {path}: {error}") from error

    if not rows:
        raise BuildError(f"CSV file has no data rows: {path}")

    return columns, rows


def _duplicate_keys(rows: Sequence[dict[str, str]], columns: Sequence[str]) -> list[str]:
    values = [tuple((row.get(column) or "").strip() for column in columns) for row in rows]
    duplicates = [value for value, count in Counter(values).items() if count > 1]
    return ["/".join(value) for value in sorted(duplicates)]


def _validate_required_fields(table_name: str, rows: Sequence[dict[str, str]]) -> None:
    errors: list[str] = []
    for row_index, row in enumerate(rows, start=2):
        for column in REQUIRED_FIELDS[table_name]:
            if not (row.get(column) or "").strip():
                errors.append(f"{table_name} row {row_index}: required field {column!r} is empty")

    if errors:
        raise BuildError("\n".join(errors))


def _validate_allowed_values(table_name: str, rows: Sequence[dict[str, str]]) -> None:
    errors: list[str] = []
    for row_index, row in enumerate(rows, start=2):
        for column, allowed in ALLOWED_VALUES.get(table_name, {}).items():
            value = (row.get(column) or "").strip()
            if value not in allowed:
                errors.append(
                    f"{table_name} row {row_index}: invalid {column}={value!r}; "
                    f"allowed: {', '.join(sorted(allowed))}"
                )

    if errors:
        raise BuildError("\n".join(errors))


def _validate_equipment_nature(rows: Sequence[dict[str, str]]) -> None:
    errors: list[str] = []
    for row_index, row in enumerate(rows, start=2):
        pair = ((row.get("is_hardware") or "").strip(), (row.get("is_software") or "").strip())
        if pair not in {("true", "false"), ("false", "true")}:
            errors.append(
                f"equipment row {row_index}: exactly one of is_hardware and is_software must be true"
            )

    if errors:
        raise BuildError("\n".join(errors))


def _validate_positions(rows: Sequence[dict[str, str]]) -> None:
    errors: list[str] = []
    seen: set[tuple[str, int]] = set()

    for row_index, row in enumerate(rows, start=2):
        raw_position = (row.get("position_in_chain") or "").strip()
        try:
            position = int(raw_position)
        except ValueError:
            errors.append(
                f"soundchain_equipment row {row_index}: position_in_chain must be an integer"
            )
            continue

        if position <= 0:
            errors.append(
                f"soundchain_equipment row {row_index}: position_in_chain must be positive"
            )

        key = ((row.get("soundchain_id") or "").strip(), position)
        if key in seen:
            errors.append(
                f"soundchain_equipment row {row_index}: duplicate position {position} "
                f"for soundchain {key[0]}"
            )
        seen.add(key)

    if errors:
        raise BuildError("\n".join(errors))


def _validate_foreign_keys(data: Mapping[str, Sequence[dict[str, str]]]) -> None:
    equipment_ids = {row["equipment_id"] for row in data["equipment"]}
    reference_ids = {row["reference_id"] for row in data["music_references"]}
    soundchain_ids = {row["soundchain_id"] for row in data["soundchains"]}
    errors: list[str] = []

    for row_index, row in enumerate(data["soundchains"], start=2):
        reference_id = row["primary_reference_id"]
        if reference_id and reference_id not in reference_ids:
            errors.append(
                f"soundchains row {row_index}: unknown primary_reference_id {reference_id!r}"
            )

        for column in ("primary_instrument_id", "output_equipment_id"):
            equipment_id = row[column]
            if equipment_id and equipment_id not in equipment_ids:
                errors.append(f"soundchains row {row_index}: unknown {column} {equipment_id!r}")

    for row_index, row in enumerate(data["soundchain_equipment"], start=2):
        if row["soundchain_id"] not in soundchain_ids:
            errors.append(
                f"soundchain_equipment row {row_index}: unknown soundchain_id "
                f"{row['soundchain_id']!r}"
            )
        if row["equipment_id"] not in equipment_ids:
            errors.append(
                f"soundchain_equipment row {row_index}: unknown equipment_id "
                f"{row['equipment_id']!r}"
            )

    if errors:
        raise BuildError("\n".join(errors))


def validate_public_data_safety(data: Mapping[str, Sequence[dict[str, str]]]) -> None:
    matches: list[str] = []

    for table_name, rows in data.items():
        columns = rows[0].keys()
        for column in columns:
            normalized = column.strip().lower()
            if normalized in FORBIDDEN_COLUMN_TOKENS:
                matches.append(f"{table_name}: forbidden public column {column!r}")

        for row_index, row in enumerate(rows, start=2):
            for column_name, value in row.items():
                text = value or ""
                if any(pattern.search(text) for pattern in SENSITIVE_WORD_PATTERNS):
                    matches.append(
                        f"{table_name} row {row_index} column {column_name}: "
                        "sensitive term pattern"
                    )
                if CURRENCY_PATTERN.search(text):
                    matches.append(
                        f"{table_name} row {row_index} column {column_name}: "
                        "currency-like value"
                    )
                if SERIAL_VALUE_PATTERN.search(text):
                    matches.append(
                        f"{table_name} row {row_index} column {column_name}: "
                        "serial-like value"
                    )

    if matches:
        raise BuildError(
            "Potentially sensitive content found in public CSV data:\n" + "\n".join(matches)
        )


def validate_csv_files(project_root: Path) -> dict[str, list[dict[str, str]]]:
    data_dir = project_root / "data" / "public"
    data: dict[str, list[dict[str, str]]] = {}

    print("Validating public CSV files...")
    for table_name, filename in TABLE_FILES.items():
        path = data_dir / filename
        columns, rows = read_csv_rows(path)
        expected = EXPECTED_COLUMNS[table_name]

        if columns != expected:
            raise BuildError(
                f"Unexpected columns in {display_path(path, project_root)}\n"
                f"Expected: {expected}\n"
                f"Actual:   {columns}"
            )

        _validate_required_fields(table_name, rows)
        _validate_allowed_values(table_name, rows)

        duplicates = _duplicate_keys(rows, PRIMARY_KEYS[table_name])
        if duplicates:
            raise BuildError(f"Duplicate key values in {table_name}: {duplicates}")

        data[table_name] = rows
        print(
            f"OK: {display_path(path, project_root)} -> "
            f"{len(rows)} rows, {len(columns)} columns"
        )

    _validate_equipment_nature(data["equipment"])
    _validate_positions(data["soundchain_equipment"])
    _validate_foreign_keys(data)
    validate_public_data_safety(data)

    print("OK: CSV structure, keys, controlled values, relationships and safety checks")
    return data


def sql_statements_from_file(path: Path) -> Iterable[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise BuildError(f"Unable to read SQL file {path}: {error}") from error

    buffer = ""
    for line in text.splitlines(keepends=True):
        buffer += line
        if sqlite3.complete_statement(buffer):
            statement = buffer.strip()
            buffer = ""
            if statement:
                yield statement

    if buffer.strip():
        raise BuildError(f"Incomplete SQL statement in {path}")


def create_database(db_path: Path, schema_path: Path) -> sqlite3.Connection:
    if not schema_path.exists():
        raise BuildError(f"Missing schema file: {schema_path}")

    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")

    try:
        conn.executescript(schema_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, sqlite3.Error) as error:
        conn.close()
        raise BuildError(f"Unable to create SQLite schema: {error}") from error

    return conn


def insert_rows(
    conn: sqlite3.Connection,
    table_name: str,
    rows: Sequence[dict[str, str]],
) -> None:
    columns = list(rows[0].keys())
    column_sql = ", ".join(columns)
    placeholder_sql = ", ".join("?" for _ in columns)
    statement = f"INSERT INTO {table_name} ({column_sql}) VALUES ({placeholder_sql})"
    values = [[row[column] for column in columns] for row in rows]

    conn.executemany(statement, values)
    print(f"OK: imported {len(rows)} rows into {table_name}")


def import_data(
    conn: sqlite3.Connection,
    data: Mapping[str, Sequence[dict[str, str]]],
) -> None:
    print("Importing CSV data into SQLite...")
    with conn:
        for table_name in (
            "equipment",
            "music_references",
            "soundchains",
            "soundchain_equipment",
        ):
            insert_rows(conn, table_name, data[table_name])


def run_sql_file(conn: sqlite3.Connection, path: Path, expect_empty: bool) -> int:
    if not path.exists():
        raise BuildError(f"Missing SQL file: {path}")

    statement_count = 0
    for statement in sql_statements_from_file(path):
        statement_count += 1
        cursor = conn.execute(statement)

        if cursor.description is not None:
            rows = cursor.fetchall()
            if expect_empty and rows:
                raise BuildError(
                    f"Data-quality query returned {len(rows)} row(s) in "
                    f"{path.name}, statement {statement_count}"
                )

    print(f"OK: executed {statement_count} statements from {path.name}")
    return statement_count


def validate_database(
    conn: sqlite3.Connection,
    sql_dir: Path,
) -> dict[str, int]:
    print("Validating SQLite database...")
    foreign_key_errors = conn.execute("PRAGMA foreign_key_check;").fetchall()
    if foreign_key_errors:
        raise BuildError(f"Foreign key errors found: {foreign_key_errors}")

    integrity_result = conn.execute("PRAGMA integrity_check;").fetchone()[0]
    if integrity_result != "ok":
        raise BuildError(f"SQLite integrity check failed: {integrity_result}")

    row_counts: dict[str, int] = {}
    for table_name in TABLE_FILES:
        row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        if row_count <= 0:
            raise BuildError(f"Table {table_name} has no rows after import")
        row_counts[table_name] = int(row_count)
        print(f"OK: {table_name} contains {row_count} rows")

    run_sql_file(conn, sql_dir / "example_queries.sql", expect_empty=False)
    run_sql_file(conn, sql_dir / "data_quality_queries.sql", expect_empty=True)
    print("OK: database validation completed")
    return row_counts


def _prepare_output_path(
    db_path: Path,
    default_db_path: Path,
    overwrite: bool,
) -> None:
    if db_path.exists() and db_path.resolve() != default_db_path.resolve() and not overwrite:
        raise BuildError(
            f"Output database already exists: {db_path}. "
            "Pass --overwrite to replace a custom output file."
        )


def build_database(
    project_root: Path = PROJECT_ROOT,
    db_path: Path | None = None,
    overwrite: bool = False,
) -> BuildSummary:
    project_root = project_root.resolve()
    default_db_path = project_root / "db" / "music_production_data_lab.sqlite"
    requested_path = db_path or default_db_path
    if not requested_path.is_absolute():
        requested_path = project_root / requested_path
    requested_path = requested_path.resolve()

    _prepare_output_path(requested_path, default_db_path, overwrite)
    data = validate_csv_files(project_root)
    sql_dir = project_root / "sql"

    requested_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{requested_path.name}.",
        suffix=".tmp",
        dir=requested_path.parent,
    )
    os.close(descriptor)
    temporary_path = Path(temp_name)

    try:
        conn = create_database(temporary_path, sql_dir / "schema.sql")
        try:
            import_data(conn, data)
            row_counts = validate_database(conn, sql_dir)
        finally:
            conn.close()

        os.replace(temporary_path, requested_path)
    except (BuildError, sqlite3.Error, OSError, UnicodeError) as error:
        temporary_path.unlink(missing_ok=True)
        if isinstance(error, BuildError):
            raise
        raise BuildError(str(error)) from error

    return BuildSummary(database_path=requested_path, row_counts=row_counts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the validated public SQLite data product."
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="Output database path. Default: db/music_production_data_lab.sqlite",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacement of an existing custom --db output file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        summary = build_database(
            project_root=PROJECT_ROOT,
            db_path=args.db,
            overwrite=args.overwrite,
        )
    except BuildError as error:
        print(f"ERROR: {error}")
        return 1

    print()
    print("Build completed successfully.")
    print(f"SQLite database: {display_path(summary.database_path, PROJECT_ROOT)}")
    for table_name, row_count in summary.row_counts.items():
        print(f"Rows {table_name}: {row_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
