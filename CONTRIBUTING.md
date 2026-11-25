# Contributing

The [Home Assistant engineering standard](docs/HA_ENGINEERING_STANDARD.md) is mandatory for all changes, including those produced by AI agents. Read [ARCHITECTURE.md](ARCHITECTURE.md) before changing behavior and consult the [audit register](docs/AUDIT_REGISTER.md).

Run the following from a complete Git checkout using a Python version supported by the targeted Home Assistant release:

    python scripts/check_integration.py
    python -m unittest discover -s scripts -p 'test_*.py'
    python -m pytest tests/ --cov=custom_components.gls --cov-fail-under=95
    ruff check .
    ruff format --check .
    mypy custom_components/gls --ignore-missing-imports

The pinned test environments are requirements/ha-minimum.txt (Python 3.13, HA 2025.12.0), requirements-dev.txt (Python 3.13, HA 2026.2.3), and requirements/ha-current.txt (Python 3.14, HA 2026.10.4). Install the matching file in an isolated environment. The latter is the latest available compatible test harness, not necessarily the latest Core release. Run hassfest, HACS and the security checks in CI. See #34 for reproducible test dependency/minimum-version coverage work and #35 for additional security automation. Record exact dependency versions and checks actually run.

Every PR must link its issue(s), explain user impact, add regression tests and relevant docstrings, update documentation/translations/changelog, and record the results. No release without validated version, artifact and compatibility checks. Do not add unrelated changes, secrets or raw production data. Preserve applicable upstream license notices.
