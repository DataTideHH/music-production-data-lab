# music-production-data-lab

Structured data and documentation project for a personal music production setup.

## Overview

`music-production-data-lab` is a private-first data modeling and documentation project.

It transforms unstructured working notes about a real music production setup into structured, analysis-ready data. The project covers instruments, effects, amplifiers, recording hardware, software, MIDI tools, music references, soundchains and practical workflows.

The goal is not to publish a complete private gear collection. The goal is to demonstrate how real-world domain knowledge can be turned into documented datasets, a relational data model and later reproducible SQL, Python and BI analyses.

## Portfolio value

This project is designed to show practical data and process analysis skills:

- turning semi-structured notes into clean tabular data
- defining stable identifiers and categories
- separating public-safe sample data from private source material
- preparing data for SQLite, SQL and Power BI
- modeling many-to-many relationships
- documenting assumptions and data-quality boundaries
- building a small but realistic data product from a real domain

## Current status

Version 1.2 is a refined foundation release.

It contains:

- public-safe sample CSV files
- a first relationship table for soundchains and equipment
- a documented CSV schema
- a conceptual data model prepared for SQLite
- a recruiter- and internship-oriented portfolio positioning document
- a publication policy for private/public separation

## Repository structure

    music-production-data-lab/
    ├── README.md
    ├── docs/
    │   ├── csv-schema.md
    │   ├── data-model.md
    │   ├── portfolio-positioning.md
    │   ├── project-purpose.md
    │   └── publication-policy.md
    ├── data/
    │   ├── public/
    │   │   ├── equipment_public.csv
    │   │   ├── music_references_public.csv
    │   │   ├── soundchain_equipment_public.csv
    │   │   └── soundchains_public.csv
    │   └── private/
    │       └── .gitkeep
    └── sources/
        └── private/
            └── .gitkeep

## Data product idea

    unstructured notes
    -> structured CSV files
    -> documented data model
    -> relational schema
    -> SQL and Python analysis
    -> dashboard or explorer

## Version roadmap

| Version | Scope |
|---|---|
| v1 | CSV files, README, data model and publication policy |
| v2 | SQLite schema and SQL example queries |
| v3 | Python import script and data-quality checks |
| v4 | Power BI dashboard |
| v5 | Streamlit explorer |
| v6 | Optional Flask API |

## Current CSV files

| File | Purpose |
|---|---|
| `equipment_public.csv` | Public-safe sample equipment data |
| `music_references_public.csv` | Public-safe music reference and sound-axis data |
| `soundchains_public.csv` | Public-safe soundchain and workflow concepts |
| `soundchain_equipment_public.csv` | Relationship table between soundchains and equipment |

## Data model focus

The central modeling challenge is the relationship between equipment, music references, soundchains and practical setups.

Examples:

- one equipment item can appear in multiple soundchains
- one soundchain can use multiple equipment items
- one reference artist can inform multiple soundchains
- one setup can be described as a workflow instead of a simple inventory list

This makes the project useful for practicing entity design, many-to-many relationships, data-quality rules and dashboard preparation.

## Public/private principle

Only curated public-safe sample data belongs in `data/public/`.

Private source files, full inventories, purchase notes, prices, serial numbers, personal working notes and original Word documents must not be committed.

Protected local folders:

    data/private/
    sources/private/

These folders are ignored by Git except for `.gitkeep` placeholder files.


## Reproducible database build

Version 3.0 adds a Python-based build step.

Run from the repository root:

    python3 scripts/build_database.py

The script validates the public CSV files, creates a local SQLite database, imports the data and runs SQL-based data-quality checks.

Default generated database:

    db/music_production_data_lab.sqlite

The `db/` folder is ignored by Git. Generated SQLite databases are local build artifacts and should not be committed.

## Planned technologies

- CSV for version-controlled source data
- Markdown for documentation
- SQLite and SQL for relational modeling
- Python and pandas for imports and data-quality checks
- Power BI for dashboarding
- Streamlit as an optional interactive explorer
- Flask only as an optional API extension
