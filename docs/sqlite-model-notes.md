# SQLite Model Notes

The repository contains an executable relational SQLite layer.

## Tables

- `equipment`
- `music_references`
- `soundchains`
- `soundchain_equipment`

## Reporting views

- `vw_equipment_usage`
- `vw_soundchain_analysis`

The views centralize reuse, coverage, complexity and dependency calculations used by SQL review, generated CSV outputs and Power BI.

## Main relationship

```text
soundchains
    1 -> n
soundchain_equipment
    n -> 1
equipment
```

The bridge primary key is `(soundchain_id, position_in_chain)`, reflecting the rule that one ordered position contains one item.

## Constraints

The schema enforces:

- primary and foreign keys
- positive chain positions
- public-only privacy levels
- controlled statuses and categories
- exactly one true hardware/software flag
- valid workflow, complexity and role values

Python performs the same important checks before insertion and adds contiguous-position plus direct-role validation for clearer error messages.

## SQL layers

- `schema.sql` creates constrained tables and reporting views.
- `example_queries.sql` contains 16 analytical queries.
- `data_quality_queries.sql` contains 17 checks that must return zero rows.

The build also runs `PRAGMA foreign_key_check` and `PRAGMA integrity_check`.

## Power BI note

The bridge table is the active equipment relationship. Direct soundchain links to primary instrument and output equipment describe special roles and remain available as inactive relationships to avoid ambiguous filter paths.
