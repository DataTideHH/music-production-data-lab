# Power BI dashboard plan

Version 4 will add a Power BI dashboard concept for `music-production-data-lab`.

This document defines the intended Power BI model before the actual `.pbix` file is created.

The goal is to avoid building a random dashboard. The dashboard should communicate the data product clearly:

    public-safe CSV sample data
    -> reproducible SQLite build
    -> relational model
    -> Power BI semantic model
    -> dashboard pages
    -> portfolio-ready screenshots

## Version 4 scope

Version 4 should focus on:

- importing the public CSV model into Power BI
- defining relationships between tables
- creating a small number of useful DAX measures
- building a clean multi-page dashboard
- exporting screenshots for documentation
- keeping the `.pbix` file private until public-readiness is reviewed

Version 4 should not yet be a complex BI platform. It should be a small, understandable dashboard that demonstrates modeling, reporting and communication.

## Tables to import

Recommended first import:

| Table | Source file | Role in model |
|---|---|---|
| equipment | data/public/equipment_public.csv | Dimension table for public-safe equipment sample data |
| music_references | data/public/music_references_public.csv | Dimension table for artists, references and sound axes |
| soundchains | data/public/soundchains_public.csv | Fact-like workflow table for soundchain concepts |
| soundchain_equipment | data/public/soundchain_equipment_public.csv | Bridge/fact table connecting soundchains and equipment |

Optional later import:

| Table | Source | Role |
|---|---|---|
| SQLite build | db/music_production_data_lab.sqlite | Local generated database, not committed |
| SQL query output | exported CSV from example queries | Optional prepared reporting layer |

For Version 4, CSV import is enough. SQLite import can be tested later if useful.

## Power BI relationships

Recommended relationship model:

| From table | Column | To table | Column | Cardinality | Cross-filter direction |
|---|---|---|---|---|---|
| soundchain_equipment | soundchain_id | soundchains | soundchain_id | many-to-one | single |
| soundchain_equipment | equipment_id | equipment | equipment_id | many-to-one | single |
| soundchains | primary_reference_id | music_references | reference_id | many-to-one | single |
| soundchains | primary_instrument_id | equipment | equipment_id | many-to-one | single or inactive if ambiguous |
| soundchains | output_equipment_id | equipment | equipment_id | many-to-one | single or inactive if ambiguous |

Important modeling note:

The main active star-like model should be:

    soundchains
        -> soundchain_equipment
        -> equipment

and:

    soundchains
        -> music_references

The links from `soundchains` directly to `equipment` through `primary_instrument_id` and `output_equipment_id` are useful, but may create ambiguity. In Power BI, they may be kept inactive or handled carefully.

## Candidate measures

Recommended first DAX measures:

| Measure | Purpose |
|---|---|
| Equipment Items | Count equipment rows |
| Soundchains | Count soundchains |
| Music References | Count music references |
| Equipment Uses | Count rows in soundchain_equipment |
| Required Equipment Uses | Count required entries in soundchain_equipment |
| Optional Equipment Uses | Count optional entries in soundchain_equipment |
| Distinct Equipment Used | Count distinct equipment used in soundchains |
| Soundchains per Sound Axis | Count soundchains by sound_axis |
| Equipment Categories | Count distinct equipment categories |
| Hardware Items | Count equipment rows where is_hardware = true |
| Software Items | Count equipment rows where is_software = true |

Example DAX ideas:

    Equipment Items =
        COUNTROWS(equipment)

    Soundchains =
        COUNTROWS(soundchains)

    Equipment Uses =
        COUNTROWS(soundchain_equipment)

    Distinct Equipment Used =
        DISTINCTCOUNT(soundchain_equipment[equipment_id])

    Hardware Items =
        CALCULATE(
            COUNTROWS(equipment),
            equipment[is_hardware] = "true"
        )

    Software Items =
        CALCULATE(
            COUNTROWS(equipment),
            equipment[is_software] = "true"
        )

## Dashboard pages

### Page 1: Project Overview

Purpose:

Show the project as a small data product, not as a gear collection.

Suggested visuals:

- KPI cards:
  - Equipment Items
  - Soundchains
  - Music References
  - Equipment Uses
- Bar chart:
  - Equipment count by category
- Donut or bar chart:
  - Hardware vs. software
- Text box:
  - CSV -> Python -> SQLite -> SQL -> Power BI

Business/portfolio message:

This page should make clear that the project demonstrates structured data modeling and reproducible analysis.

### Page 2: Equipment Model

Purpose:

Show how heterogeneous items are categorized.

Suggested visuals:

- Bar chart:
  - Equipment by category
- Matrix:
  - category, subcategory, public_name, primary_role
- Slicer:
  - setup_domain
- Slicer:
  - is_hardware / is_software
- Table:
  - equipment_id, public_name, category, setup_domain, data_quality_status

Business/portfolio message:

This page demonstrates category design, schema thinking and public-safe data handling.

### Page 3: Soundchain Analysis

Purpose:

Show the relationship between soundchains and equipment.

Suggested visuals:

- Matrix:
  - chain_name -> position_in_chain -> public_name -> role_in_chain
- Bar chart:
  - equipment usage count by public_name
- Bar chart:
  - required vs optional equipment uses
- Slicer:
  - sound_axis
- Slicer:
  - workflow_type

Business/portfolio message:

This page demonstrates a many-to-many relationship through a bridge table.

### Page 4: Music References and Sound Axes

Purpose:

Show how references, learning goals and workflows are connected.

Suggested visuals:

- Bar chart:
  - references by dashboard_group
- Bar chart:
  - soundchains by sound_axis
- Table:
  - artist_or_band, sound_axis, learning_focus, production_focus
- Slicer:
  - importance_public
- Slicer:
  - reference_role

Business/portfolio message:

This page demonstrates how domain knowledge can be mapped into structured analysis categories.

### Page 5: Data Quality and Public-Safe Status

Purpose:

Show that the project includes data-quality and publication-safety thinking.

Suggested visuals:

- KPI cards:
  - rows by table
  - public_sample records
- Table:
  - data_quality_status by table
- Bar chart:
  - privacy_level counts
- Text box:
  - private source files are not committed
  - generated SQLite database is ignored by Git

Business/portfolio message:

This page demonstrates data governance basics, public/private separation and reproducible project hygiene.

## Screenshot and export plan

The `.pbix` file should stay private until the public-readiness review is complete.

Public-safe repo exports can include:

| File | Purpose |
|---|---|
| docs/images/powerbi-overview.png | Screenshot of Page 1 |
| docs/images/powerbi-equipment-model.png | Screenshot of Page 2 |
| docs/images/powerbi-soundchain-analysis.png | Screenshot of Page 3 |
| docs/images/powerbi-data-quality.png | Screenshot of Page 5 |
| docs/power-bi-dashboard-notes.md | Explanation of model and visuals |

Do not commit:

- private `.pbix` files without review
- screenshots containing private data
- exported full private datasets
- Power BI cache files or temporary exports

## Recommended Version 4 deliverables

Version 4 should add:

    docs/power-bi-plan.md
    docs/power-bi-dashboard-notes.md
    docs/images/.gitkeep

Later, after the dashboard is built and reviewed:

    docs/images/powerbi-overview.png
    docs/images/powerbi-equipment-model.png
    docs/images/powerbi-soundchain-analysis.png
    docs/images/powerbi-data-quality.png

## Public-readiness criteria

Before any Power BI screenshot is published:

- only public-safe sample data is visible
- no private notes are visible
- no prices, serial numbers or purchase details are visible
- no full private inventory is visible
- dashboard title and labels emphasize data modeling, not gear collection
- README explains the dashboard as part of a data product
