# Build verification

The reproducible data workflow is verified locally and in GitHub Actions.

## Automated verification

| Job | Runtime | Scope |
|---|---|---|
| Python 3.12 (Ubuntu) | Ubuntu latest | compile, 12 tests, temporary SQLite build |
| Python 3.12 (Windows) | Windows latest | compile, 12 tests, temporary SQLite build |

See [Testing and CI](testing-and-ci.md).

## Active local platforms

| System | Platform | Command |
|---|---|---|
| iMac | macOS Sonoma on Intel | `python3.12 scripts/build_database.py` |
| ThinkPad | Windows 11 / PowerShell 7 | `py -3.12 scripts\build_database.py` |

## Verified workflow

```text
public CSV files
-> Python structure and business-rule validation
-> temporary SQLite build
-> relational import
-> integrity and foreign-key checks
-> analytical SQL
-> zero-row data-quality checks
-> atomic publication of the local database
```

Expected committed sample row counts:

| Table | Rows |
|---|---:|
| equipment | 10 |
| music_references | 8 |
| soundchains | 5 |
| soundchain_equipment | 16 |

The generated database is a local artifact under `db/` and is ignored by Git.
