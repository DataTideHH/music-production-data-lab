# SQLite model notes

The repository contains an executable relational SQLite layer.

## Tables

- `equipment`
- `music_references`
- `soundchains`
- `soundchain_equipment`

## Main relationship

```text
soundchains
    1 -> n
soundchain_equipment
    n -> 1
equipment
```

The bridge primary key is `(soundchain_id, position_in_chain)`, reflecting the current rule that one ordered position contains one item.

## Constraints

The schema enforces:

- primary and foreign keys
- positive chain positions
- public-only privacy levels
- controlled statuses and categories
- exactly one true hardware/software flag
- valid workflow, complexity and role values

Python performs the same important checks before insertion to provide clearer error messages.

## SQL layers

- `schema.sql` creates the constrained model.
- `example_queries.sql` answers analytical questions.
- `data_quality_queries.sql` contains checks that must return zero rows.

The build also runs `PRAGMA foreign_key_check` and `PRAGMA integrity_check`.

## Power BI note

The bridge table is the main equipment relationship. Direct soundchain links to primary instrument and output equipment describe special roles and may be inactive in Power BI to avoid ambiguous filter paths.
