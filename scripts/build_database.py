#!/usr/bin/env python3
"""
Build a reproducible SQLite database from the public CSV sample data.

Project: music-production-data-lab
Version: 3.0

This script:
- validates public CSV file structure
- checks primary keys
- checks for sensitive terms in public CSV data
- creates a SQLite database from sql/schema.sql
- imports the public CSV rows
- validates foreign key integrity
- runs SQL example queries
- runs data-quality queries and expects them to return no rows

The generated SQLite database is a local build artifact and should not be committed.
"""

from __future__ import annotations

import argparse
import csv
import re
import sqlite3
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "public"
SQL_DIR = PROJECT_ROOT / "sql"
DEFAULT_DB_PATH = PROJECT_ROOT / "db" / "music_production_data_lab.sqlite"

TABLE_FILES = {
    "equipment": DATA_DIR / "equipment_public.csv",
    "music_references": DATA_DIR / "music_references_public.csv",
    "soundchains": DATA_DIR / "soundchains_public.csv",
    "soundchain_equipment": DATA_DIR / "soundchain_equipment_public.csv",
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
    "equipment": "equipment_id",
    "music_references": "reference_id",
    "soundchains": "soundchain_id",
}

SENSITIVE_TERMS = [
    "serial",
    "invoice",
    "price",
    "purchase",
    "rechnung",
    "seriennummer",
    "kaufpreis",
]


class BuildError(RuntimeError):
    """Raised when the reproducible build or validation fails."""


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise BuildError(f"Missing CSV file: {path}")

    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        columns = reader.fieldnames or []

    if not rows:
        raise BuildError(f"CSV file has no data rows: {path}")

    return columns, rows


def validate_csv_files() -> dict[str, list[dict[str, str]]]:
    print("Validating public CSV files...")

    data: dict[str, list[dict[str, str]]] = {}

    for table_name, path in TABLE_FILES.items():
        columns, rows = read_csv_rows(path)
        expected = EXPECTED_COLUMNS[table_name]

        if columns != expected:
            raise BuildError(
                f"Unexpected columns in {path}\n"
                f"Expected: {expected}\n"
                f"Actual:   {columns}"
            )

        data[table_name] = rows
        print(f"OK: {path.relative_to(PROJECT_ROOT)} -> {len(rows)} rows, {len(columns)} columns")

    for table_name, key_column in PRIMARY_KEYS.items():
        values = [row[key_column] for row in data[table_name]]
        duplicates = sorted({value for value in values if values.count(value) > 1})

        if duplicates:
            raise BuildError(f"Duplicate primary key values in {table_name}: {duplicates}")

    validate_public_data_terms(data)

    print("OK: CSV structure and primary keys are valid")
    return data


def validate_public_data_terms(data: dict[str, list[dict[str, str]]]) -> None:
    pattern = re.compile("|".join(re.escape(term) for term in SENSITIVE_TERMS), re.IGNORECASE)

    matches: list[str] = []

    for table_name, rows in data.items():
        for row_index, row in enumerate(rows, start=2):
            for column_name, value in row.items():
                if pattern.search(value or ""):
                    matches.append(f"{table_name} row {row_index} column {column_name}: {value}")

    if matches:
        detail = "\n".join(matches)
        raise BuildError(f"Potential sensitive terms found in public CSV data:\n{detail}")

    print("OK: no obvious sensitive terms found in public CSV data")


def create_database(db_path: Path) -> sqlite3.Connection:
    schema_path = SQL_DIR / "schema.sql"

    if not schema_path.exists():
        raise BuildError(f"Missing schema file: {schema_path}")

    db_path.parent.mkdir(parents=True, exist_ok=True)

    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")

    schema_sql = schema_path.read_text(encoding="utf-8")
    conn.executescript(schema_sql)

    print(f"OK: created SQLite database at {db_path.relative_to(PROJECT_ROOT)}")
    return conn


def insert_rows(conn: sqlite3.Connection, table_name: str, rows: list[dict[str, str]]) -> None:
    columns = list(rows[0].keys())
    column_sql = ", ".join(columns)
    placeholder_sql = ", ".join("?" for _ in columns)

    sql = f"INSERT INTO {table_name} ({column_sql}) VALUES ({placeholder_sql})"

    values = [[row[column] for column in columns] for row in rows]

    conn.executemany(sql, values)
    print(f"OK: imported {len(rows)} rows into {table_name}")


def import_data(conn: sqlite3.Connection, data: dict[str, list[dict[str, str]]]) -> None:
    print("Importing CSV data into SQLite...")

    insert_order = [
        "equipment",
        "music_references",
        "soundchains",
        "soundchain_equipment",
    ]

    with conn:
        for table_name in insert_order:
            insert_rows(conn, table_name, data[table_name])


def strip_sql_comments(statement: str) -> str:
    lines = []
    for line in statement.splitlines():
        stripped = line.strip()
        if stripped.startswith("--"):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def sql_statements_from_file(path: Path) -> Iterable[str]:
    sql_text = path.read_text(encoding="utf-8")
    for raw_statement in sql_text.split(";"):
        cleaned = strip_sql_comments(raw_statement)
        if cleaned:
            yield raw_statement.strip()


def run_sql_file(conn: sqlite3.Connection, path: Path, expect_empty: bool) -> None:
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
                    f"Data-quality query returned rows in {path.name}, statement {statement_count}"
                )

    print(f"OK: executed {statement_count} statements from {path.relative_to(PROJECT_ROOT)}")


def validate_database(conn: sqlite3.Connection) -> None:
    print("Validating SQLite database...")

    foreign_key_errors = conn.execute("PRAGMA foreign_key_check;").fetchall()
    if foreign_key_errors:
        raise BuildError(f"Foreign key errors found: {foreign_key_errors}")

    for table_name in TABLE_FILES:
        count = conn.execute(f"SELECT COUNT(*) AS row_count FROM {table_name}").fetchone()["row_count"]
        if count <= 0:
            raise BuildError(f"Table {table_name} has no rows after import")
        print(f"OK: {table_name} contains {count} rows")

    run_sql_file(conn, SQL_DIR / "example_queries.sql", expect_empty=False)
    run_sql_file(conn, SQL_DIR / "data_quality_queries.sql", expect_empty=True)

    print("OK: database validation completed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the local SQLite database from public CSV sample data."
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="Output SQLite database path. Default: db/music_production_data_lab.sqlite",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    db_path = args.db if args.db.is_absolute() else PROJECT_ROOT / args.db

    try:
        data = validate_csv_files()
        conn = create_database(db_path)

        try:
            import_data(conn, data)
            validate_database(conn)
        finally:
            conn.close()

    except BuildError as error:
        print(f"ERROR: {error}")
        return 1

    print()
    print("Build completed successfully.")
    print(f"SQLite database: {db_path.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
