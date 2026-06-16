# SQLite model notes

Version 2.0 introduces the first SQL layer for `music-production-data-lab`.

The goal is not yet to generate a production database. The goal is to document how the current CSV model maps to a relational SQLite structure.

## Files

Version 2.0 adds:

- `sql/schema.sql`
- `sql/example_queries.sql`
- `sql/data_quality_queries.sql`
- `docs/sqlite-model-notes.md`

## Current relational tables

The first relational model contains four tables:

- `equipment`
- `music_references`
- `soundchains`
- `soundchain_equipment`

## Main relationship

The most important relationship is between soundchains and equipment.

A soundchain can use multiple equipment items.

An equipment item can appear in multiple soundchains.

This is modeled through the relationship table:

    soundchain_equipment

Conceptually:

    soundchains
        1 -> n
    soundchain_equipment
        n -> 1
    equipment

## Foreign key logic

The model prepares these relationships:

    soundchains.primary_reference_id -> music_references.reference_id
    soundchains.primary_instrument_id -> equipment.equipment_id
    soundchains.output_equipment_id -> equipment.equipment_id
    soundchain_equipment.soundchain_id -> soundchains.soundchain_id
    soundchain_equipment.equipment_id -> equipment.equipment_id

## Why text booleans are used for now

The public CSV files currently use `true` and `false` values for fields such as `is_hardware` and `is_software`.

For version 2.0, the SQLite schema keeps these fields as text with checks. This keeps the schema close to the CSV files.

A later Python import script can transform these values into integer booleans if needed.

## How this supports future work

Version 2.0 prepares:

- SQL practice
- relationship modeling
- data-quality checks
- later Python import scripts
- later Power BI modeling
- later Streamlit exploration

## Planned next step

Version 3 can add a Python script that reads the CSV files, creates a SQLite database and imports the public sample data reproducibly.
