# music-production-data-lab

Structured data and documentation project for a personal music production setup.

## Project purpose

music-production-data-lab turns unstructured music production notes into structured, analysis-ready data.

The project covers instruments, effects, amplifiers, cabinets, recording hardware, software, MIDI tools, music references, soundchains and example setups.

The goal is not to publish a complete private gear collection. The goal is to demonstrate a clean data modeling and documentation workflow based on a real-world domain.

## Version 1 scope

Version 1 focuses on the foundation:

- CSV-based public sample datasets
- A first documented data model
- A clear project purpose
- A publication policy separating public and private information
- A repository structure that can later support SQLite, SQL queries, Python checks, Power BI and Streamlit

## Planned roadmap

| Version | Scope |
|---|---|
| v1 | CSV, README, data model |
| v2 | SQLite schema and SQL example queries |
| v3 | Python import script and data-quality checks |
| v4 | Power BI dashboard |
| v5 | Streamlit explorer |
| v6 | Optional Flask API |

## Current repository structure

    music-production-data-lab/
    ├── README.md
    ├── docs/
    │   ├── data-model.md
    │   ├── project-purpose.md
    │   └── publication-policy.md
    ├── data/
    │   ├── public/
    │   │   ├── equipment_public.csv
    │   │   ├── soundchains_public.csv
    │   │   └── music_references_public.csv
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
    -> SQL / Python analysis
    -> dashboard or explorer

## Public/private principle

The public version contains curated sample data and project documentation only.

Private information such as full inventories, purchase notes, prices, serial numbers, personal working notes, original Word source files or copyrighted third-party material must not be committed to the public repository.

## Tech direction

Planned technologies:

- CSV for version-controlled source data
- Markdown for documentation
- SQLite and SQL for relational modeling
- Python / pandas for imports and data-quality checks
- Power BI for dashboarding
- Streamlit as an optional interactive explorer
- Flask only as an optional API extension
