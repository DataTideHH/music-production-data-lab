# CSV schema

The files in `data/public/` are curated public-safe source tables. Executable rules are defined in `scripts/build_database.py` and `sql/schema.sql`; controlled values are documented in [Data dictionary](data-dictionary.md).

## Tables

| File | Key | Purpose |
|---|---|---|
| `equipment_public.csv` | `equipment_id` | Equipment and software dimension |
| `music_references_public.csv` | `reference_id` | Reference and sound-axis dimension |
| `soundchains_public.csv` | `soundchain_id` | Workflow concepts |
| `soundchain_equipment_public.csv` | `soundchain_id + position_in_chain` | Ordered bridge between workflows and equipment |

## Structural rules

- Headers must match the documented order exactly.
- Required fields may not be blank.
- Keys must be unique.
- `position_in_chain` must be a positive integer and unique within a soundchain.
- Foreign-key values must resolve to public source rows.
- Controlled values must match the data dictionary.
- Every public entity must use `privacy_level = public_sample`.

## Public-data rules

The public CSV layer must not contain complete private inventories, invoices, prices, purchase dates, serial numbers, storage details or original private source documents.

The automated validator detects selected forbidden columns and value patterns. Human review remains mandatory before publication.
