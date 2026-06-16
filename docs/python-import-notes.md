# Python import notes

Version 3.0 introduces a reproducible Python import workflow.

The goal is to turn the public CSV sample data into a local SQLite database and validate the import.

## Added file

    scripts/build_database.py

## What the script does

The script:

- reads the public CSV files from `data/public/`
- validates the expected CSV columns
- checks primary key uniqueness
- checks public CSV data for obvious sensitive terms
- creates a local SQLite database from `sql/schema.sql`
- imports the CSV rows into SQLite
- validates foreign key integrity
- runs `sql/example_queries.sql`
- runs `sql/data_quality_queries.sql` and expects no result rows

## Build command

Run from the repository root:

    python3 scripts/build_database.py

Default output:

    db/music_production_data_lab.sqlite

The `db/` folder is ignored by Git. The generated SQLite database is a local build artifact and should not be committed.

## Why this matters

This turns the project from static documentation into a reproducible data workflow:

    CSV
    -> Python validation
    -> SQLite database
    -> SQL analysis

This is relevant for data and process analysis because it demonstrates:

- import logic
- schema alignment
- primary key checks
- relationship validation
- data-quality checks
- reproducible local builds

## Current limitation

Version 3.0 still uses only the Python standard library.

A later version can add pandas-based checks, richer logging, automated tests or a Streamlit explorer.
