# Testing and CI

The repository uses Python 3.12 and the standard library only.

## Test suites

### Database workflow tests

`tests/test_build_database.py` covers:

- successful build with 30 equipment rows, 12 references, 12 soundchains and 53 bridge rows
- expected tables and reporting views
- duplicate keys
- missing CSV files
- changed column structure
- invalid foreign keys
- invalid privacy values
- invalid hardware/software classification
- duplicate chain positions
- sensitive public values and a serial-pattern false-positive regression
- custom output overwrite protection
- external output paths

### Reporting workflow tests

`tests/test_generate_analysis_report.py` covers:

- creation of all four generated reporting artifacts
- expected KPI values
- deterministic usage ordering

## Local commands

macOS/Linux:

```bash
python3.12 -m py_compile \
  scripts/build_database.py \
  scripts/generate_analysis_report.py \
  tests/test_build_database.py \
  tests/test_generate_analysis_report.py

python3.12 -m unittest discover -s tests -p "test_*.py" -v
python3.12 scripts/build_database.py
python3.12 scripts/generate_analysis_report.py
```

Windows PowerShell:

```powershell
py -3.12 -m py_compile `
  scripts\build_database.py `
  scripts\generate_analysis_report.py `
  tests\test_build_database.py `
  tests\test_generate_analysis_report.py

py -3.12 -m unittest discover -s tests -p "test_*.py" -v
py -3.12 scripts\build_database.py
py -3.12 scripts\generate_analysis_report.py
```

## GitHub Actions

Both required jobs run on pull requests and `main`:

- `Python 3.12 (Ubuntu)`
- `Python 3.12 (Windows)`

Each job:

1. compiles scripts and tests
2. runs all 14 unit tests
3. builds the validated SQLite database
4. regenerates the four processed reporting outputs
5. fails when the four committed generated outputs are stale

The Windows job uploads test diagnostics only when a failure occurs.

## Visual evidence boundary

The two SVG page previews are reviewed design artifacts based on the same generated metrics. They are not emitted by the reporting generator and are not presented as exports from a `.pbix` file. CI validates the source data, metrics and committed reporting datasets; visual review remains a separate publication step.
