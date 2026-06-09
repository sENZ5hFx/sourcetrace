# Changelog

All notable changes to sourcetrace are documented here.  
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
Versioning: [Semantic Versioning](https://semver.org/)

---

## [Unreleased]

### Added
- `pyproject.toml` with locked ruff config (`UP007`, `E`, `F`, `B`, `I`, `W`)
- Full test suite: `tests/test_certifier.py`, `test_ledger.py`, `test_verifier.py`, `test_api.py`
- `requirements-dev.txt` separating dev/test deps from runtime
- `__init__.py` for `core/` and `api/` packages
- `.editorconfig` for consistent IDE behavior
- `.python-version` pinned to 3.11
- `storage/.gitkeep` — ensures storage dir tracked in git
- IP Integrity Guard CI job — blocks merges missing IP protection files
- IP Audit Timestamp CI workflow — auto-commits timestamped audit entries
- GitHub issue templates (bug, feature) and PR template
- `CHANGELOG.md` (this file)
- Copyright headers on all Python source files

### Fixed
- `typing.Optional` → `X | None` across all modules (ruff UP007)
- `api/models.py` mutable default `metadata: Optional[dict] = {}` → `dict | None = None`
- Import ordering normalized (ruff I)
- CI workflow simplified — removed fragile dep-detection logic in favor of `requirements-dev.txt`

---

## [1.0.0] — 2024

### Added
- Initial CLP engine: certifier, ledger, verifier
- FastAPI endpoints: `/health`, `/certify`, `/verify/{id}`, `/chain`, `/ledger`, `/bundle/export`
- SQLite-backed append-only ledger with `GENESIS` sentinel
- IP protection files: `IP_DISCLOSURE.md`, `PATENT.md`, `TRADEMARK.md`, `LDIR_CLAIMS.md`, `LICENSE`, `NOTICE`, `COPYRIGHT_AND_ATTRIBUTIONS.md`
- GitHub Actions CI: structure guard, lint, test
- Dependabot configured for pip and GitHub Actions
