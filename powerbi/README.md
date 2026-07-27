# Power BI Evidence

This folder documents the semantic model and DAX layer used for the public-safe reporting concept.

## Current evidence

- `docs/images/powerbi-overview.png` is the existing reviewed Power BI overview export.
- `docs/images/analysis-soundchain-preview.svg` is a data-backed static preview for the intended Soundchain Analysis page.
- `docs/images/analysis-data-quality-preview.svg` is a data-backed static preview for the intended Data Quality and Coverage page.
- `measures.dax` contains the version-controlled measure definitions.
- `model.md` documents relationships, directions and implementation decisions.

The two SVG files are reviewed analytical design previews based on the generated metrics, not screenshots exported from a `.pbix` file. They make the intended reporting pages reviewable without misrepresenting their provenance. After the local Power BI report is updated, reviewed `.pbix` exports can replace the previews.

## Source tables

| Power BI table | Source | Model role |
|---|---|---|
| `equipment` | `data/public/equipment_public.csv` | Equipment dimension |
| `music_references` | `data/public/music_references_public.csv` | Reference dimension |
| `soundchains` | `data/public/soundchains_public.csv` | Workflow dimension |
| `soundchain_equipment` | `data/public/soundchain_equipment_public.csv` | Ordered bridge/fact table |
| `analysis_summary` | `data/processed/analysis_summary.csv` | Generated KPI reference table |

## Publication boundary

The `.pbix`, `.pbit`, `.pbip` and local Power BI working directories remain ignored. Only reviewed public-safe exports, model documentation and DAX definitions belong in the repository.
