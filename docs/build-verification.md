# Build verification

Version 3.1 documents the first cross-platform build verification for `music-production-data-lab`.

## Verified systems

The reproducible database build has been verified on:

| System | OS | Python command | Result |
|---|---|---|---|
| iMac | macOS Sonoma via OCLP | `python3 scripts/build_database.py` | successful |
| ThinkPad | Windows 11 / PowerShell 7 | `py -3.12 scripts\build_database.py` | successful |

## Verified workflow

The verified workflow is:

    CSV
    -> Python validation
    -> SQLite database build
    -> SQL example queries
    -> SQL data-quality queries

## Current build result

The build script validates the public CSV files, creates a local SQLite database and imports the sample data.

Expected row counts:

| Table | Rows |
|---|---:|
| equipment | 10 |
| music_references | 8 |
| soundchains | 5 |
| soundchain_equipment | 16 |

## Build artifacts

The generated SQLite database is a local build artifact:

    db/music_production_data_lab.sqlite

The `db/` folder is ignored by Git. The database file must not be committed.

## Why this matters

The project is no longer only a static documentation repository. It now has a reproducible local data workflow that works on both macOS and Windows.

This supports the portfolio story:

    unstructured notes
    -> public-safe CSV sample data
    -> documented schema
    -> Python validation
    -> SQLite import
    -> SQL analysis
    -> data-quality checks
