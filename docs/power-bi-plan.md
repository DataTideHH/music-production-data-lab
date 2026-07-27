# Power BI Reporting Plan

The Power BI layer communicates the relational workflow model rather than presenting a gear inventory.

## Reporting questions

1. How much of the curated equipment sample is represented in workflows?
2. Which items are reused across multiple workflows?
3. Which soundchains are structurally largest?
4. How do required, optional and swap-candidate roles differ?
5. How do recording workflows differ from guitar signal chains?
6. Which records still require data-quality review?

## Source model

| Table | Role |
|---|---|
| `equipment` | Equipment dimension |
| `music_references` | Reference dimension |
| `soundchains` | Workflow dimension |
| `soundchain_equipment` | Ordered bridge/fact table |
| `analysis_summary` | Generated KPI reference table |

The active analytical path uses the bridge table:

```text
equipment 1 -> n soundchain_equipment n <- 1 soundchains
                                        n -> 1 music_references
```

Direct links from `soundchains` to the primary instrument and output equipment are retained as inactive role-playing relationships to avoid ambiguous filter paths.

## Page 1: Project Overview

Purpose: explain the end-to-end data product.

Visuals:

- Equipment Items
- Soundchains
- Music References
- Equipment Uses
- equipment by category
- hardware/software split
- pipeline text: CSV -> Python -> SQLite -> SQL -> Power BI

Current evidence: `docs/images/powerbi-overview.png`.

## Page 2: Soundchain Analysis

Purpose: explain complexity, reuse and dependency roles.

Visuals:

- Average Steps per Soundchain
- Maximum Steps in Soundchain
- Recording Workflows
- total steps by soundchain
- most reused equipment
- required/optional/swap-candidate mix
- ordered chain matrix
- workflow type and complexity slicers

Current design evidence: `docs/images/analysis-soundchain-preview.svg`.

## Page 3: Data Quality and Coverage

Purpose: expose coverage and governance rather than hiding incomplete records.

Visuals:

- Equipment Coverage %
- Reused Equipment Items
- Unused Equipment Items
- Verified Equipment Items
- Equipment Items Needing Verification
- reused/single-use/unused distribution
- quality-status table
- public/private boundary note

Current design evidence: `docs/images/analysis-data-quality-preview.svg`.

## DAX

Version-controlled measures are stored in `powerbi/measures.dax`. Model decisions are documented in `powerbi/model.md`.

## Public evidence rule

The existing overview PNG is a reviewed Power BI export. The two SVG pages are deterministic, data-backed previews and explicitly identify themselves as previews. They must not be described as `.pbix` exports.

When the local Power BI report is updated, reviewed exports can replace the two previews without committing the `.pbix` working file.
