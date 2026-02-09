# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bokeh is an interactive visualization library for modern web browsers. It consists of two main components:

1. **Python library** (`src/bokeh/`): High-level API for creating plots, dashboards, and data applications
2. **BokehJS** (`bokehjs/`): TypeScript/JavaScript library that handles rendering and interactivity in the browser

The Python and BokehJS components are tightly coupled—Python code serializes model definitions and data to JSON, which BokehJS deserializes and renders.

## Common Commands

### Python Development

```bash
# Install in editable mode (builds BokehJS automatically)
pip install -e .

# Build wheel/sdist packages
python -m build .

# Run unit tests
pytest tests/unit

# Run codebase checks (code quality, flake8, isort, etc.)
pytest tests/codebase

# Run integration tests (if re-enabled)
pytest tests/integration

# Run examples tests
pytest tests/test_examples.py

# Type checking with mypy
mypy
```

### BokehJS Development

```bash
cd bokehjs

# Install dependencies
npm ci

# Build BokehJS
node make build

# Run tests
node make test

# Run linter
node make lint

# Start dev server for testing
node make dev-build && node make test:spawn:headless
```

### Pre-commit Hooks

Pre-commit runs codebase checks that include code quality, ESLint, isort, flake8, JSON validation, license checks, and Windows filename checks:

```bash
pre-commit run --all-files
```

## Architecture

### Python Side (`src/bokeh/`)

- **core/**: Fundamental building blocks including:
  - `properties.py`: Property descriptor system for models
  - `has_props.py`: Base class for all models with property initialization
  - `serialization.py`: JSON encoding/decoding for communicating with BokehJS
  - `validation.py`: Error and warning code definitions

- **models/**: User-facing model classes (axes, plots, glyphs, tools, etc.)
  - These Python models must stay synchronized with their TypeScript counterparts in BokehJS
  - Changes often require updates in both `src/bokeh/models/` and `bokehjs/src/lib/models/`

- **plotting/**: High-level `figure()` function for creating plots

- **server/**: Bokeh server implementation for real-time interactivity

- **io/**: Input/output utilities (saving, exporting, showing plots)

### BokehJS Side (`bokehjs/src/lib/`)

- **core/**: Core TypeScript infrastructure mirroring Python's core
- **models/**: TypeScript model implementations that mirror Python models
- **api/**: High-level APIs for working with Bokeh programmatically
- **protocol/**: WebSocket protocol for server communications
- **document/**: Document model managing the object graph

### Build System

- Python's `setup.py` triggers BokehJS build before packaging
- BokehJS uses its own `make` build system (`bokehjs/make/`) written in TypeScript
- BokehJS builds to `bokehjs/build/js/` and the outputs are copied to `src/bokeh/server/static/`

## Key Conventions

- Tests use `pytest` with `asyncio_mode = "strict"`
- Python code follows type hints with mypy (many modules have `ignore_errors = true` pending migration)
- Codebase checks enforce consistent styling via pytest-based tests
- JavaScript/TypeScript code uses ESLint and the BokehJS `make lint` command
- License headers (BSD-3-Clause) required on all files

## Important Files

- `pyproject.toml`: Python project configuration, pytest settings, mypy configuration
- `bokehjs/package.json`: BokehJS npm configuration
- `setup.py`: Custom build hooks that invoke BokehJS build
- `.pre-commit-config.yaml`: Pre-commit hooks configuration
- `tests/codebase/`: Non-test code quality checks