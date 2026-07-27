# Power BI Semantic Model

## Recommended relationships

| From | Column | To | Column | Cardinality | Direction | Status |
|---|---|---|---|---|---|---|
| `soundchain_equipment` | `soundchain_id` | `soundchains` | `soundchain_id` | many-to-one | single | active |
| `soundchain_equipment` | `equipment_id` | `equipment` | `equipment_id` | many-to-one | single | active |
| `soundchains` | `primary_reference_id` | `music_references` | `reference_id` | many-to-one | single | active |
| `soundchains` | `primary_instrument_id` | `equipment` | `equipment_id` | many-to-one | single | inactive |
| `soundchains` | `output_equipment_id` | `equipment` | `equipment_id` | many-to-one | single | inactive |

The active analytical path is the bridge-table model:

```text
equipment 1 -> n soundchain_equipment n <- 1 soundchains
                                        n -> 1 music_references
```

The direct instrument and output links are role-playing relationships. Keeping them inactive avoids ambiguous filter paths while preserving explicit workflow metadata.

## Data types

- identifiers: Text
- `position_in_chain`: Whole number
- hardware/software flags: Text in source, used as controlled categorical values
- generated metric values: Decimal number where applicable
- percentage measures: Percentage format with one decimal place
- count measures: Whole number

## Report pages

### 1. Project Overview

Purpose: communicate the end-to-end data product and top-level KPIs.

Recommended visuals:

- Equipment Items
- Soundchains
- Music References
- Equipment Uses
- equipment category distribution
- hardware/software split
- workflow pipeline text

### 2. Soundchain Analysis

Purpose: explain workflow complexity, reuse and required/optional roles.

Recommended visuals:

- Average Steps per Soundchain
- Maximum Steps in Soundchain
- Recording Workflows
- bar chart: total steps by chain
- matrix: chain -> position -> item -> role
- bar chart: most reused equipment
- slicers: workflow type, complexity, sound axis

### 3. Data Quality and Coverage

Purpose: demonstrate governance, coverage and explicit review status.

Recommended visuals:

- Equipment Coverage %
- Reused Equipment Items
- Unused Equipment Items
- Verified Equipment Items
- Equipment Items Needing Verification
- stacked bar: reused / single-use / unused
- table: records requiring review
- publication-boundary note

## Formatting

Use the DataTideHH Navy/Teal visual language:

- Navy: `#0A2F4F`
- Teal: `#0B92B6`
- Light teal: `#43C4DF`
- Paper: `#FAFAF7`

The report should remain compact, legible and evidence-oriented rather than decorative.
