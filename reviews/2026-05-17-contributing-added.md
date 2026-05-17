# CONTRIBUTING.md Added — Keeper Beacon

**Date:** 2026-05-17
**Action:** Created `CONTRIBUTING.md`

## Why This Repo Needed It

Keeper Beacon is the fleet discovery and registry service — a core piece of the Cocapn infrastructure. Despite being published on PyPI (`pip install keeper-beacon`) and having a clear README, it had:

- No development setup instructions (venv, editable install)
- No testing guidance (pytest, coverage)
- No code style conventions (formatting, linting, type hints)
- No architecture documentation for the lighthouse metaphor

The README explains *what* it does and *how to install it*, but not *how to contribute*. For a PyPI-published package that's the entry point for fleet discovery, this was a significant gap.

## What the Contribution Workflow Looks Like

1. Fork and create a feature branch
2. Install with `pip install -e ".[dev]"`
3. Write tests in `tests/` matching the source structure
4. Run `pytest` and `ruff check src/`
5. Check type hints with `mypy` (if installed)
6. Open PR

## Special Notes

- **Published on PyPI**: Changes must maintain backward compatibility or follow semver. Version bumps happen via the `pyproject.toml`.
- **Lighthouse Metaphor**: The Keeper Beacon implements a specific architectural metaphor (lighthouse → radar → discovery → routing). Contributions should stay aligned with this concept.
- **Service Layer**: This package powers the Keeper service on port 8900. Consider both library consumers (importing keeper_beacon) and service consumers (HTTP API) when making changes.
