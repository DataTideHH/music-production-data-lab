# Build Verification

## Automated environments

The required GitHub Actions jobs validate the workflow on:

| Job | Platform | Python |
|---|---|---|
| Python 3.12 (Ubuntu) | `ubuntu-latest` | 3.12 |
| Python 3.12 (Windows) | `windows-latest` | 3.12 |

## Validated workflow

```text
public CSV source data
-> structural and governance validation
-> SQLite schema and import
-> reporting views
-> analytical SQL
-> zero-row data-quality SQL
-> deterministic reporting outputs
-> stale-output check
```

## Expected row counts

| Table | Rows |
|---|---:|
| equipment | 30 |
| music_references | 12 |
| soundchains | 12 |
| soundchain_equipment | 53 |

## Generated outputs

- `data/processed/analysis_summary.csv`
- `data/processed/equipment_usage_summary.csv`
- `data/processed/soundchain_analysis.csv`
- `docs/generated-analysis-summary.md`

CI regenerates these four files and uses `git diff --exit-code` to ensure that the committed reporting layer matches the source data and SQL model.

## Reviewed visual evidence

- `docs/images/analysis-soundchain-preview.svg`
- `docs/images/analysis-data-quality-preview.svg`

These SVGs are data-backed page-design previews. They are reviewed separately and are not represented as generated reporting outputs or exports from a `.pbix` file.

## Local platform commands

iMac/macOS:

```bash
/usr/local/bin/python3.12 -m unittest discover -s tests -p "test_*.py" -v
/usr/local/bin/python3.12 scripts/build_database.py
/usr/local/bin/python3.12 scripts/generate_analysis_report.py
```

ThinkPad/Windows:

```powershell
py -3.12 -m unittest discover -s tests -p "test_*.py" -v
py -3.12 scripts\build_database.py
py -3.12 scripts\generate_analysis_report.py
```
