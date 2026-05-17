# Contributing to Keeper Beacon

> *The lighthouse keeper needs to know where every agent is.*

## Quick Start

Keeper Beacon is a Python package for fleet discovery and registry — agents appear on radar, get tracked and routed.

### Prerequisites
- Python 3.10+
- `pip` and `setuptools`

### Install for Development

```bash
# Clone
git clone https://github.com/SuperInstance/keeper-beacon.git
cd keeper-beacon

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests to verify setup
pytest
```

## Making Changes

1. **Fork the repo**
2. **Create a feature branch** (`git checkout -b feature/my-feature`)
3. **Make your changes**
4. **Test** — `pytest` (all tests must pass)
5. **Check types** — `mypy src/` (if installed)
6. **Format** — `ruff format src/`
7. **Commit** (`git commit -m "feat: add my feature"`)
8. **Push** (`git push origin feature/my-feature`)
9. **Open a PR**

## Code Style

### Python
- Python 3.10+ with type hints on all public functions
- Format with `ruff format` (line length 88)
- Lint with `ruff check src/`
- Google-style docstrings for public APIs
- Use `dataclasses` for data containers
- Prefer composition over inheritance for agent models

### Project Layout

```
keeper-beacon/
├── src/
│   └── keeper_beacon/        # Package source
│       ├── __init__.py       # Exports public API
│       ├── discovery.py      # Agent registration & heartbeats
│       ├── registry.py       # Central directory of active agents
│       ├── proximity.py      # Proximity scoring and matching
│       ├── matcher.py        # Capability-based task routing
│       └── models.py         # Data models (Agent, RegistryEntry, etc.)
├── tests/                    # Pytest test suite
├── dist/                     # Built distributions
└── pyproject.toml            # Build config and metadata
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=keeper_beacon

# Run specific test file
pytest tests/test_discovery.py

# Run with verbose output
pytest -v
```

### Writing Tests
- Unit tests in `tests/` matching source structure
- Test both registration and discovery flows
- Mock external dependencies (HTTP calls, timers)
- Test proximity scoring edge cases (empty registry, duplicate agents)

## Architecture Concepts

The Keeper Beacon implements the lighthouse metaphor:

- **Discovery** — Agents register with the beacon on startup via heartbeat
- **Registry** — Central directory of active fleet members with capabilities
- **Proximity** — Track which agents are near each other (same task, same room)
- **Matcher** — Route agents to tasks based on capabilities and proximity

The repo powers the Keeper service on port 8900. When making changes, consider:
- Does this maintain or improve the lighthouse metaphor?
- Can this component run standalone or does it need the full fleet?
- Are registry entries eventually consistent if the beacon restarts?

## Reporting Issues

Open an [Issue](https://github.com/SuperInstance/keeper-beacon/issues) with:
- Python version and OS
- Steps to reproduce
- Expected vs actual behavior

## Questions?

- Read the [README](README.md) for the lighthouse metaphor explanation
- Open a [Discussion](https://github.com/SuperInstance/keeper-beacon/discussions)
- Check existing [Issues](https://github.com/SuperInstance/keeper-beacon/issues)
