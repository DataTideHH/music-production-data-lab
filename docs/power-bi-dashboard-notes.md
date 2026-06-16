# Power BI dashboard notes

This document will track implementation notes for the future Power BI dashboard.

## Current status

Power BI dashboard implementation has not started yet.

Version 4 planning is documented in:

    docs/power-bi-plan.md

## Intended dashboard purpose

The dashboard should show that `music-production-data-lab` is a small data product.

It should demonstrate:

- data modeling
- relationship modeling
- public-safe reporting
- workflow analysis
- data-quality awareness
- portfolio-ready communication

## Initial dashboard pages

Planned pages:

1. Project Overview
2. Equipment Model
3. Soundchain Analysis
4. Music References and Sound Axes
5. Data Quality and Public-Safe Status

## Data source recommendation

Initial Power BI source:

    data/public/*.csv

The generated SQLite database can be tested later, but the first dashboard should stay close to the version-controlled CSV files.

## Public export rule

Screenshots may be exported later only after a public-readiness review.

The `.pbix` file should remain private until explicitly reviewed.
