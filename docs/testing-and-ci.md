# Testing and CI

The project targets Python 3.12 and uses only the standard library.

## Local tests

macOS/Linux:

```bash
python3.12 -m py_compile scripts/build_database.py tests/test_build_database.py
python3.12 -m unittest discover -s tests -p "test_*.py" -v
python3.12 scripts/build_database.py
```

Windows PowerShell:

```powershell
py -3.12 -m py_compile scripts/build_database.py tests/test_build_database.py
py -3.12 -m unittest discover -s tests -p "test_*.py" -v
py -3.12 scripts\build_database.py
```

## Test coverage

The 12 unit tests cover:

1. successful database build and row counts
2. duplicate primary keys
3. missing CSV files
4. unexpected CSV columns
5. unknown foreign keys
6. invalid privacy classifications
7. inconsistent hardware/software flags
8. duplicate soundchain positions
9. sensitive public values
10. custom output overwrite protection
11. explicit custom output replacement
12. output paths outside the repository

The database build additionally runs SQLite integrity and foreign-key checks, analytical SQL and zero-row data-quality queries.

## GitHub Actions

`.github/workflows/ci.yml` runs two independent jobs:

- `Python 3.12 (Ubuntu)`
- `Python 3.12 (Windows)`

Each job compiles the workflow and tests, runs the unit-test suite and builds a temporary SQLite database. Generated databases are not committed.

## Required status checks

After the workflow is proven on the default branch, both jobs should be required before merging to `main`.
