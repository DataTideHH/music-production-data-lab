# Python Data Workflow

The repository contains two dependency-free Python 3.12 workflows.

## Database build

`scripts/build_database.py`:

1. reads the four public CSV files
2. validates headers, required values and keys
3. validates controlled values and cross-field rules
4. validates relationships before insertion
5. scans for selected publication-safety risks
6. builds a temporary SQLite database
7. imports rows in dependency order
8. runs integrity, analytical and zero-row quality checks
9. atomically replaces the requested output only after success

## Reporting generator

`scripts/generate_analysis_report.py`:

1. builds a validated temporary database
2. queries the reporting views
3. generates three reporting CSV files
4. generates a Markdown KPI summary
5. writes the four outputs deterministically for CI comparison

## Commands

macOS/Linux:

```bash
python3.12 scripts/build_database.py
python3.12 scripts/generate_analysis_report.py
```

Windows PowerShell:

```powershell
py -3.12 scripts\build_database.py
py -3.12 scripts\generate_analysis_report.py
```

Custom database outputs are protected from accidental replacement:

```bash
python3.12 scripts/build_database.py --db /tmp/music-lab.sqlite
python3.12 scripts/build_database.py --db /tmp/music-lab.sqlite --overwrite
```

## Error contract

Validation and filesystem failures produce an `ERROR:` message and exit code 1. Successful workflows print the generated paths and row counts.

See [Testing and CI](testing-and-ci.md) for automated failure-path and stale-output coverage.

## Visual reporting artifacts

The two SVG page previews under `docs/images/` are reviewed design evidence based on the generated metrics. They are maintained separately from the reporting generator and explicitly identify themselves as previews rather than `.pbix` exports.
