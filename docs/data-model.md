# Data model

The repository models a curated public sample of music-production equipment, references and workflows. The current state is relational and executable: the CSV files are validated, imported into SQLite and checked by SQL.

## Entity relationship model

```mermaid
erDiagram
    EQUIPMENT ||--o{ SOUNDCHAIN_EQUIPMENT : used_in
    SOUNDCHAINS ||--|{ SOUNDCHAIN_EQUIPMENT : contains
    MUSIC_REFERENCES ||--o{ SOUNDCHAINS : primary_reference
    EQUIPMENT ||--o{ SOUNDCHAINS : primary_instrument
    EQUIPMENT ||--o{ SOUNDCHAINS : output_equipment

    EQUIPMENT {
        text equipment_id PK
        text category
        text public_name
        text status_public
        text setup_domain
        text primary_role
        text is_hardware
        text is_software
        text privacy_level
    }

    MUSIC_REFERENCES {
        text reference_id PK
        text artist_or_band
        text sound_axis
        text importance_public
        text reference_role
        text dashboard_group
        text privacy_level
    }

    SOUNDCHAINS {
        text soundchain_id PK
        text chain_name
        text workflow_type
        text primary_reference_id FK
        text primary_instrument_id FK
        text output_equipment_id FK
        text complexity_level
        text privacy_level
    }

    SOUNDCHAIN_EQUIPMENT {
        text soundchain_id PK,FK
        integer position_in_chain PK
        text equipment_id FK
        text role_in_chain
        text required_or_optional
        text sequence_group
    }
```

## Core entities

### `equipment`

Public-safe equipment and software records. `equipment_id` is the stable key. Exactly one of `is_hardware` and `is_software` must be true.

### `music_references`

Reference artists or bands mapped to sound axes, learning goals and production concepts.

### `soundchains`

Workflow concepts such as guitar signal chains or recording workflows. A soundchain may have one primary reference, one primary instrument and one output item.

### `soundchain_equipment`

Bridge table connecting soundchains and equipment in an ordered sequence. The current business rule permits one item per `position_in_chain` within a soundchain, so the primary key is:

```text
soundchain_id + position_in_chain
```

## Relationship decisions

The bridge table is the principal relationship for equipment usage. The direct `primary_instrument_id` and `output_equipment_id` links describe special roles and may be inactive role-playing relationships in Power BI to avoid ambiguous filter paths.

The current model deliberately keeps one `primary_reference_id` per soundchain. A later analytical extension may add a `soundchain_references` bridge when multiple references need to be represented.

## Data flow

```text
data/public/*.csv
-> Python structural and business-rule validation
-> SQLite tables and constraints
-> analytical SQL
-> zero-row data-quality checks
-> Power BI semantic model
```

## Boundaries

This is a normalized analytical sample, not a complete asset register. Private source material, prices, serial numbers, purchase information and storage details remain outside the repository.
