# Power BI dashboard notes

## Current status

A first public-safe overview page has been implemented and published as a reviewed screenshot:

![Power BI overview dashboard](images/powerbi-overview.png)

The `.pbix` working file remains local and ignored by Git.

## Current purpose

The dashboard is evidence of the reporting layer around the relational sample. It should present the repository as a small data product rather than a gear collection.

## Planned analytical pages

The next reporting increment should focus on three complete pages:

1. **Overview** — source-table KPIs, categories and workflow counts
2. **Soundchain analysis** — ordered equipment use, reuse, complexity and optional stages
3. **Data quality and governance** — quality status, privacy status and model coverage

Five sparse pages are not the objective. A smaller set of complete pages with documented findings is stronger.

## Version-controlled evidence to add

```text
powerbi/
├── README.md
├── measures.dax
├── model.md
└── findings.md
```

Reviewed screenshots may be committed after checking that they contain only public-safe sample data.
