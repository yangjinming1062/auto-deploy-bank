# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bokeh is an interactive visualization library for modern web browsers with two tightly coupled components:

1. **Python library** (`src/bokeh/`) - Server-side Python API for creating plots, dashboards, and data applications
2. **BokehJS** (`bokehjs/`) - Front-end TypeScript library that renders visualizations in browsers

The Python library serializes models to JSON and communicates with BokehJS via WebSocket protocol.

## Build Commands

### Python Package

```bash
# Install in editable mode (requires pre-built BokehJS)
pip install -e .

# Build from source with automatic BokehJS build
python setup.py develop

# Build wheel/sdist (requires BokehJS to be pre-built)
BOKEHJS_ACTION=install python -m build .
```

### BokehJS

```bash
cd bokehjs

# Full build (default task)
node make build

# Development build (faster, only lib)
node make dev

# Run tests
node make test

# Run linter
node make lint

# Available tasks: node make help
```

## Test Commands

```bash
# All unit tests
pytest tests/unit

# Single test file
pytest tests/unit/bokeh/models/test_plots.py

# Run tests matching pattern
pytest -k "test_plot"

# With coverage
pytest --cov=bokeh tests/unit

# Codebase quality checks (isort, flake8, eslint, json, license)
pytest tests/codebase

# Integration tests
pytest tests/integration

# Mypy type checking
mypy
```

**Note:** Examples tests (`tests/test_examples.py`) require a running Chrome/Chromium headless browser.

## Architecture

### Key Design Patterns

1. **HasProps Property System** (`bokeh/core/properties.py`, `has_props.py`): Models use descriptors for type-safe properties with validation, serialization, and change notification. Defines `Bool`, `String`, `Float`, `Array`, `Instance`, etc.

2. **Document Model** (`bokeh/document/`): Central container holding all models. Manages references, sessions, and JSON serialization for transmission to BokehJS via WebSocket.

3. **Protocol Bridge** (`bokeh/protocol/` ↔ `bokehjs/src/lib/protocol/`): JSON message format for Python↔BokehJS communication. Python serializes; BokehJS deserializes and renders.

4. **Model Mirror**: BokehJS (`bokehjs/src/lib/models/`) mirrors Python models (`bokeh/models/`) - changes to either may require corresponding updates.

### Distribution Bundles

BokehJS is split: `bokeh` (core), `bokeh-widgets`, `bokeh-tables`, `bokeh-api`, `bokeh-gl`, `bokeh-mathjax`.

## Code Quality

- **Pre-commit**: Run `pre-commit run --all-files` for code quality checks (isort, flake8, eslint, json validation, license)
- **Max line length**: 165 characters
- **Python typing**: MyPy configured with some modules typed, others ignore_errors