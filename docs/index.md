---
title: Music Production Data Lab
description: Public-safe relational data, Python, SQL, data quality and Power BI
---

# Music Production Data Lab

**Public-safe analytics project turning semi-structured music-production notes into validated relational data, reproducible Python/SQLite builds, SQL analysis and Power BI reporting evidence.**

[View repository](https://github.com/DataTideHH/music-production-data-lab) · [Run the project](https://github.com/DataTideHH/music-production-data-lab#quick-start) · [DataTideHH portfolio](https://datatidehh.de/)

---

## Why this project exists

The source domain contains heterogeneous objects and workflows: instruments, effects, amplification, software, recording hardware, references and ordered signal chains. The analytical problem is to make those concepts consistent, relational and reviewable without publishing private source material.

```text
semi-structured notes
-> curated public-safe CSV tables
-> Python validation
-> constrained SQLite model
-> SQL analysis and quality checks
-> Power BI reporting layer
```

---

## Current evidence

| Evidence | What it demonstrates |
|---|---|
| [Data model](data-model.md) | Entities, relationships and modelling decisions |
| [Data dictionary](data-dictionary.md) | Controlled values, keys and business rules |
| [Python workflow](python-import-notes.md) | Reproducible import and validation |
| [Testing and CI](testing-and-ci.md) | 12 tests plus Ubuntu and Windows automation |
| [SQL model](sqlite-model-notes.md) | Constraints, analytical queries and quality checks |
| [Power BI plan](power-bi-plan.md) | Semantic-model and reporting design |
| [Publication policy](publication-policy.md) | Public/private boundary |
| [Official references](official-references.md) | Primary technical documentation |

---

## Relational focus

The main analytical relationship is an ordered bridge between soundchains and equipment:

```text
soundchains
    1 -> n
soundchain_equipment
    n -> 1
equipment
```

The bridge supports equipment reuse, sequence analysis, required/optional roles and workflow-level reporting.

---

## Automated quality controls

The workflow checks:

- exact CSV structure and required values
- duplicate keys and soundchain positions
- controlled categorical values
- hardware/software classification
- foreign-key relationships
- public privacy classifications
- selected sensitive patterns
- SQLite integrity
- SQL quality queries that must return zero rows

GitHub Actions runs the same build on Ubuntu and Windows with Python 3.12.

---

## Power BI overview

![Power BI overview dashboard](images/powerbi-overview.png)

The published screenshot uses only reviewed public-safe sample data. The `.pbix` working file remains local.

---

## Portfolio relevance

This project demonstrates:

- data modelling from messy domain knowledge
- many-to-many relationship design
- data quality and governance basics
- reproducible Python and SQL workflows
- cross-platform validation
- reporting preparation and technical communication

The next increment will expand the curated analytical sample and publish stronger Power BI measures, screenshots and written findings.

---

## Related DataTideHH projects

- [Network Operations Data Lab](https://datatidehh.github.io/network-operations-data-lab/) — operational IT analytics
- [Hamburg District Data Basics](https://github.com/DataTideHH/hamburg-district-data-basics) — public/open-data analysis
- [Open-Meteo Germany Weather Ranking](https://github.com/DataTideHH/open-meteo-germany-weather-ranking) — API-based Python workflow
- [Spring Boot Process API Basics](https://datatidehh.github.io/spring-boot-process-api-basics/) — supporting API evidence
