# Power BI semantic-model and reporting plan

A first public-safe overview screenshot is already published. The next reporting increment should strengthen analytical evidence rather than add many decorative pages.

## Data sources

| Table | Source | Role |
|---|---|---|
| equipment | `data/public/equipment_public.csv` | equipment dimension |
| music_references | `data/public/music_references_public.csv` | reference dimension |
| soundchains | `data/public/soundchains_public.csv` | workflow entity |
| soundchain_equipment | `data/public/soundchain_equipment_public.csv` | ordered bridge/fact table |

The generated SQLite database is a validated local build artifact. CSV remains the simplest Power BI source for the current sample.

## Relationships

| From | To | Cardinality | Direction |
|---|---|---|---|
| soundchain_equipment[soundchain_id] | soundchains[soundchain_id] | many-to-one | single |
| soundchain_equipment[equipment_id] | equipment[equipment_id] | many-to-one | single |
| soundchains[primary_reference_id] | music_references[reference_id] | many-to-one | single |

The direct soundchain links to primary instrument and output equipment are role-playing relationships. Keep them inactive or model them through duplicated role dimensions if they are needed in reports; do not introduce ambiguous active filter paths.

## Core measures

```DAX
Equipment Items =
    COUNTROWS(equipment)

Soundchains =
    COUNTROWS(soundchains)

Equipment Uses =
    COUNTROWS(soundchain_equipment)

Distinct Equipment Used =
    DISTINCTCOUNT(soundchain_equipment[equipment_id])

Required Equipment Uses =
    CALCULATE(
        COUNTROWS(soundchain_equipment),
        soundchain_equipment[required_or_optional] = "required"
    )

Optional Equipment Uses =
    CALCULATE(
        COUNTROWS(soundchain_equipment),
        soundchain_equipment[required_or_optional] = "optional"
    )

Unused Equipment =
    [Equipment Items] - [Distinct Equipment Used]
```

The next PR should store reviewed measures in `powerbi/measures.dax`.

## Recommended pages

### 1. Overview

- source-table KPIs
- equipment by category
- hardware versus software
- workflows by type and complexity
- short data-flow explanation

### 2. Soundchain analysis

- ordered chain matrix
- equipment reuse count
- required versus optional stages
- chain length and complexity
- filters for sound axis and workflow type

### 3. Data quality and governance

- data-quality status by table
- privacy classification
- unused records and coverage
- explanation of public/private separation
- reproducible-build and CI status

## Evidence standard

Each published page should include:

- a clear analytical question
- documented DAX
- a reviewed screenshot
- two or three written findings
- limitations of the small public sample

The `.pbix` file remains local until an explicit public-readiness review.

## Public-readiness checks

Before publishing any screenshot:

- only committed public-safe sample data is visible
- no private notes, paths, user names, prices or serial numbers appear
- titles describe analytics and workflows, not personal wealth or inventory
- labels are readable at repository-page scale
- findings are supported by the displayed data
