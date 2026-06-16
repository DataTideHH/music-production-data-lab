# music-production-data-lab

Structured data and documentation project for a personal music production setup.

## Overview

`music-production-data-lab` is a private-first data modeling and documentation project.

It turns unstructured notes about a real music production setup into structured, analysis-ready data. The project covers instruments, effects, amplifiers, cabinets, recording hardware, software, MIDI tools, music references, soundchains and example setups.

The purpose is not to publish a complete private gear collection. The purpose is to demonstrate a clean workflow for transforming real-world domain knowledge into documented datasets, a relational data model and later reproducible SQL, Python and BI analyses.

## Current status

Version 1.1 is a foundation release.

It contains:

- public-safe sample CSV files
- a first conceptual data model
- a documented CSV schema
- a project-purpose document
- a publication policy for private/public separation
- a repository structure prepared for later SQLite, Python, Power BI and Streamlit work

## Repository structure

    music-production-data-lab/
    ├── README.md
    ├── docs/
    │   ├── csv-schema.md
    │   ├── data-model.md
    │   ├── project-purpose.md
    │   └── publication-policy.md
    ├── data/
    │   ├── public/
    │   │   ├── equipment_public.csv
    │   │   ├── music_references_public.csv
    │   │   └── soundchains_public.csv
    │   └── private/
    │       └── .gitkeep
    └── sources/
        └── private/
            └── .gitkeep

## Data product idea

The project is designed as a small end-to-end data product:

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

## Data model focus

The central modeling challenge is the relationship between equipment, music references, soundchains and practical setups.

Examples:

- one equipment item can appear in multiple soundchains
- one soundchain can use multiple equipment items
- one reference artist can be linked to multiple sound axes
- one setup can be described as a practical workflow rather than as a simple inventory list

This makes the project useful for practicing:

- entity design
- category design
- many-to-many relationships
- data-quality rules
- public/private data separation
- documentation for reproducible analysis

## Public/private principle

Only curated public-safe sample data belongs in `data/public/`.

Private source files, full inventories, purchase notes, prices, serial numbers, personal working notes and original Word documents must not be committed.

Protected local folders:

    data/private/
    sources/private/

These folders are ignored by Git except for `.gitkeep` placeholder files.

## Planned technologies

- CSV for version-controlled source data
- Markdown for documentation
- SQLite and SQL for relational modeling
- Python and pandas for imports and data-quality checks
- Power BI for dashboarding
- Streamlit as an optional interactive explorer
- Flask only as an optional API extension
