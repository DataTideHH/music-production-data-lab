#!/usr/bin/env python3
"""Generate deterministic reporting datasets from the validated public sample."""

from __future__ import annotations

import csv
import sqlite3
import sys
import tempfile
from pathlib import Path
from typing import Iterable, Mapping, Sequence

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import build_database  # noqa: E402

PROJECT_ROOT = SCRIPT_DIR.parent


def scalar(connection: sqlite3.Connection, statement: str) -> int | float:
    value = connection.execute(statement).fetchone()[0]
    if value is None:
        raise build_database.BuildError(f"Analysis query returned no value: {statement}")
    return value


def rows_as_dicts(connection: sqlite3.Connection, statement: str) -> list[dict[str, object]]:
    return [dict(row) for row in connection.execute(statement).fetchall()]


def metric_rows(connection: sqlite3.Connection) -> list[dict[str, object]]:
    equipment = int(scalar(connection, "SELECT COUNT(*) FROM equipment"))
    used = int(scalar(connection, "SELECT COUNT(*) FROM vw_equipment_usage WHERE coverage_status <> 'unused'"))
    uses = int(scalar(connection, "SELECT COUNT(*) FROM soundchain_equipment"))
    chains = int(scalar(connection, "SELECT COUNT(*) FROM soundchains"))

    definitions: Sequence[tuple[str, int | float, str, str]] = (
        ("equipment_items", equipment, "items", "Curated public-safe equipment records."),
        ("hardware_items", int(scalar(connection, "SELECT COUNT(*) FROM equipment WHERE is_hardware = 'true'")), "items", "Hardware records in the analytical sample."),
        ("software_items", int(scalar(connection, "SELECT COUNT(*) FROM equipment WHERE is_software = 'true'")), "items", "Software records in the analytical sample."),
        ("music_references", int(scalar(connection, "SELECT COUNT(*) FROM music_references")), "references", "Curated sound and production references."),
        ("soundchains", chains, "workflows", "Modelled guitar and recording workflows."),
        ("guitar_signal_chains", int(scalar(connection, "SELECT COUNT(*) FROM soundchains WHERE workflow_type = 'guitar_signal_chain'")), "workflows", "Amplifier-oriented guitar workflows."),
        ("recording_workflows", int(scalar(connection, "SELECT COUNT(*) FROM soundchains WHERE workflow_type = 'recording_workflow'")), "workflows", "Interface and DAW workflows."),
        ("equipment_uses", uses, "uses", "Ordered bridge-table equipment roles."),
        ("distinct_equipment_used", used, "items", "Equipment used in at least one workflow."),
        ("equipment_coverage_percent", round(100 * used / equipment, 1), "percent", "Share of equipment used in at least one workflow."),
        ("unused_equipment_items", equipment - used, "items", "Items outside the current workflow sample."),
        ("required_uses", int(scalar(connection, "SELECT COUNT(*) FROM soundchain_equipment WHERE required_or_optional = 'required'")), "uses", "Required workflow stages."),
        ("optional_uses", int(scalar(connection, "SELECT COUNT(*) FROM soundchain_equipment WHERE required_or_optional = 'optional'")), "uses", "Optional workflow stages."),
        ("swap_candidate_uses", int(scalar(connection, "SELECT COUNT(*) FROM soundchain_equipment WHERE required_or_optional = 'swap_candidate'")), "uses", "Alternative workflow stages."),
        ("average_steps_per_soundchain", round(uses / chains, 2), "steps", "Average ordered stages per workflow."),
        ("maximum_steps_in_soundchain", int(scalar(connection, "SELECT MAX(total_steps) FROM vw_soundchain_analysis")), "steps", "Largest workflow in the current sample."),
        ("reused_equipment_items", int(scalar(connection, "SELECT COUNT(*) FROM vw_equipment_usage WHERE soundchain_usage_count >= 2")), "items", "Equipment reused across at least two workflows."),
        ("verified_equipment_items", int(scalar(connection, "SELECT COUNT(*) FROM equipment WHERE data_quality_status = 'verified'")), "items", "Equipment records marked verified."),
        ("equipment_items_needing_verification", int(scalar(connection, "SELECT COUNT(*) FROM equipment WHERE data_quality_status = 'needs_verification'")), "items", "Equipment records explicitly flagged for review."),
    )
    return [
        {"metric_name": name, "metric_value": format_number(value), "unit": unit, "interpretation": meaning}
        for name, value, unit, meaning in definitions
    ]


def format_number(value: int | float) -> str:
    if isinstance(value, float):
        return f"{value:.2f}".rstrip("0").rstrip(".")
    return str(value)


def csv_text(fieldnames: Sequence[str], rows: Iterable[Mapping[str, object]]) -> str:
    from io import StringIO

    buffer = StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row[field] for field in fieldnames})
    return buffer.getvalue()


def markdown_summary(metrics: Sequence[Mapping[str, object]], equipment: Sequence[Mapping[str, object]], chains: Sequence[Mapping[str, object]]) -> str:
    metric = {row["metric_name"]: row["metric_value"] for row in metrics}
    lines = [
        "# Generated Analysis Summary", "",
        "This file is generated from the committed public CSV data by `scripts/generate_analysis_report.py`.", "",
        "## Current sample", "",
        "| Metric | Value |", "|---|---:|",
        f"| Equipment records | {metric['equipment_items']} |",
        f"| Music references | {metric['music_references']} |",
        f"| Soundchains | {metric['soundchains']} |",
        f"| Ordered equipment uses | {metric['equipment_uses']} |",
        f"| Equipment coverage | {metric['equipment_coverage_percent']}% |",
        f"| Average steps per soundchain | {metric['average_steps_per_soundchain']} |", "",
        "## Most reused equipment", "", "| Equipment | Category | Soundchain uses |", "|---|---|---:|",
    ]
    for row in equipment[:5]:
        lines.append(f"| {row['public_name']} | {row['category']} | {row['soundchain_usage_count']} |")
    lines += ["", "## Largest workflows", "", "| Soundchain | Type | Complexity | Steps |", "|---|---|---|---:|"]
    for row in chains[:5]:
        lines.append(f"| {row['chain_name']} | {row['workflow_type']} | {row['complexity_level']} | {row['total_steps']} |")
    lines += ["", "## Scope note", "", "These figures describe a curated public-safe analytical sample, not a complete private inventory.", ""]
    return "\n".join(lines)


def generate_analysis_outputs(project_root: Path = PROJECT_ROOT) -> list[Path]:
    project_root = project_root.resolve()
    with tempfile.TemporaryDirectory() as temporary_directory:
        database = Path(temporary_directory) / "analysis.sqlite"
        build_database.build_database(project_root=project_root, db_path=database)
        connection = sqlite3.connect(database)
        connection.row_factory = sqlite3.Row
        try:
            metrics = metric_rows(connection)
            equipment = rows_as_dicts(connection, "SELECT equipment_id, public_name, category, subcategory, status_public, data_quality_status, soundchain_usage_count, coverage_status FROM vw_equipment_usage ORDER BY soundchain_usage_count DESC, public_name")
            chains = rows_as_dicts(connection, "SELECT soundchain_id, chain_name, workflow_type, sound_axis, complexity_level, primary_reference, total_steps, required_steps, optional_steps, swap_candidate_steps FROM vw_soundchain_analysis ORDER BY total_steps DESC, chain_name")
        finally:
            connection.close()

    outputs = {
        project_root / "data/processed/analysis_summary.csv": csv_text(("metric_name", "metric_value", "unit", "interpretation"), metrics),
        project_root / "data/processed/equipment_usage_summary.csv": csv_text(("equipment_id", "public_name", "category", "subcategory", "status_public", "data_quality_status", "soundchain_usage_count", "coverage_status"), equipment),
        project_root / "data/processed/soundchain_analysis.csv": csv_text(("soundchain_id", "chain_name", "workflow_type", "sound_axis", "complexity_level", "primary_reference", "total_steps", "required_steps", "optional_steps", "swap_candidate_steps"), chains),
        project_root / "docs/generated-analysis-summary.md": markdown_summary(metrics, equipment, chains),
    }
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    return list(outputs)


def main() -> int:
    try:
        written = generate_analysis_outputs()
    except build_database.BuildError as error:
        print(f"ERROR: {error}")
        return 1
    print("Generated analysis outputs:")
    for path in written:
        print(f"- {path.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
