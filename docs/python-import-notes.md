# Python build workflow

`scripts/build_database.py` turns the committed public CSV files into a validated local SQLite database.

## Runtime

- Python 3.12
- standard library only

## Workflow

1. Read the four public CSV files as UTF-8.
2. Validate headers, required values and keys.
3. Validate controlled values and cross-field business rules.
4. Validate relationships before database insertion.
5. Scan for selected public-safety risks.
6. Build a temporary SQLite database.
7. Import all rows in dependency order.
8. Run integrity, foreign-key, analytical and quality checks.
9. Atomically replace the requested output only after success.

## Commands

macOS/Linux:

```bash
python3.12 scripts/build_database.py
```

Windows PowerShell:

```powershell
py -3.12 scripts\build_database.py
```

Custom outputs are protected from accidental replacement:

```bash
python3.12 scripts/build_database.py --db /tmp/music-lab.sqlite
python3.12 scripts/build_database.py --db /tmp/music-lab.sqlite --overwrite
```

## Error contract

Validation and filesystem failures produce an `ERROR:` message and exit code 1. Successful builds print the database path and row count for each table.

See [Testing and CI](testing-and-ci.md) for automated failure-path coverage.
