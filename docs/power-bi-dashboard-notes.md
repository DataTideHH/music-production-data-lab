# Power BI Dashboard Notes

## Current status

The project has three documented reporting pages:

1. Project Overview
2. Soundchain Analysis
3. Data Quality and Coverage

The repository contains:

- one reviewed Power BI overview export
- two deterministic data-backed page previews
- version-controlled DAX measures
- semantic-model documentation
- generated reporting datasets
- written findings

## Provenance of visual files

| File | Provenance |
|---|---|
| `images/powerbi-overview.png` | Reviewed export from the local Power BI report |
| `images/analysis-soundchain-preview.svg` | Generated static page preview; not a `.pbix` export |
| `images/analysis-data-quality-preview.svg` | Generated static page preview; not a `.pbix` export |

The distinction is intentional. The repository should never imply that a generated preview was exported from Power BI.

## Local implementation checklist

Before replacing a preview with a Power BI export:

- use only committed public-safe source or processed data
- confirm active/inactive relationships match `powerbi/model.md`
- implement and validate measures from `powerbi/measures.dax`
- verify KPI values against `data/processed/analysis_summary.csv`
- check that no private paths, notes or report metadata are visible
- export at a readable resolution
- update this provenance table

## Current KPI baseline

- Equipment Items: 30
- Soundchains: 12
- Equipment Uses: 53
- Equipment Coverage: 80%
- Average Steps per Soundchain: 4.42
- Maximum Steps in Soundchain: 7

These values are regenerated in CI and provide a review baseline for the local report.
