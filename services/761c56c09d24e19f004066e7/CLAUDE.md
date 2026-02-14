# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bokeh is an interactive visualization library for modern web browsers. It consists of two major components:

1. **Python library** (`src/bokeh/`) - Provides high-level Python API for creating plots, handles document state, and serves applications via Tornado
2. **BokehJS** (`bokehjs/src/lib/`) - TypeScript/JavaScript library that renders visualizations in the browser

The Python library serializes plots to JSON, which BokehJS consumes via WebSocket or embedded messages to render interactive visualizations.

## Build Commands

### Python Package
```bash
# Install in development mode
pip install -e .

# Build wheel/sdist (requires BokehJS to be built first)
python setup.py sdist bdist_wheel

# Or using build module
python -m build .
```

### BokehJS (Required Before Python Tests)
```bash
cd bokehjs

# Install dependencies (use npm ci for CI, npm install for dev)
npm ci

# Build BokehJS (outputs to bokehjs/build/js/)
node make build

# Dev build (faster, unminified)
node make dev-build

# Lint TypeScript code
node make lint

# Run all BokehJS tests
node make test

# Run specific test types
node make test:unit        # Unit tests
node make test:integration # Integration tests with visual baselines
node make test:defaults    # Default values tests
```

## Testing

### Python Tests
```bash
# Run all unit tests
pytest tests/unit

# Run a specific test file
pytest tests/unit/bokeh/document/test_document.py

# Run tests matching a pattern
pytest -k "test_property"

# Run with coverage
pytest --cov=bokeh tests/unit

# Codebase checks (isort, flake8, eslint validation, etc.)
pytest tests/codebase

# Type checking with mypy
mypy

# Run examples tests (requires BokehJS build + headless Chrome)
pytest tests/test_examples.py
```

### Pre-commit Hooks
```bash
pre-commit install  # Install git hooks
pre-commit run --all-files  # Run all checks
```

## Architecture

### Python Source Structure (`src/bokeh/`)

- **core/** - Low-level primitives: property system, serialization, validation, property mixins, enums
- **models/** - Visual model definitions: plots, axes, glyphs, renderers, tools, widgets, ranges, scales
- **document/** - Document state management, events, callbacks, JSON serialization, module handling
- **application/** - Application handlers for scripts, notebooks, directories
- **server/** - Tornado-based web server for hosting Bokeh apps with websocket connections
- **client/** - WebSocket client connections for communicating with server sessions
- **protocol/** - Message protocol (1.0 and 2.0) for client-server communication
- **io/** - Input/output utilities (save, export, show functions, Jupyter integration)
- **command/** - CLI commands (bokeh info, json, serve, sphinx)
- **plotting/** - High-level `figure()` API for creating plots with automatic tools
- **embed/** - Embedding utilities for standalone documents
- **sphinxext/** - Sphinx extensions for Bokeh documentation

### BokehJS Source Structure (`bokehjs/src/lib/`)

- **core/** - Core framework: property system, DOM utilities, formatting, logging, theming, serialization
- **models/** - TypeScript model classes mirroring Python models
- **document/** - Document state management and events
- **protocol/** - Message protocol implementation
- **client/** - WebSocket client session handling
- **api/** - Public API exports and convenience functions
- **embed/** - Embedding in web pages
- **testing.ts** - Testing utilities

### Data Flow

1. User creates plots using Python API (`bokeh.plotting.figure()`)
2. Document serializes models to JSON (via `core/serialization.py`)
3. JSON is sent to BokehJS via protocol (websocket or custom messages)
4. BokehJS deserializes JSON into TypeScript model objects (via `core/util/refs`)
5. Views render models to HTML/Canvas elements
6. Interactivity is handled by BokehJS, with callbacks communicating back to Python

### Property System

The `HasProps` class (Python: `core/has_props.ts`, TypeScript: `core/has_props`) provides:
- Automatic property initialization from keyword arguments
- Type validation and conversion
- Change notifications via `on_change` and `on_next_change`
- Serialization/deserialization support
- Dependency tracking for derived properties (DataSpec, etc.)

Property types are defined in `core/property/` directories for each language.

### Serialization Key Points

- `core/properties.py` - Defines Python property types and their serialization
- `core/serialization.py` - Handles JSON encoding/decoding with custom serializers
- `core/json_encoder.py` - Custom JSON encoder for Bokeh types in document exports

## Development Notes

### BokehJS Build Dependencies
- Node.js >= 16.0, npm >= 8.0
- Chrome/Chromium for testing (headless mode via `node make test:spawn:headless`)

### Python Dependencies
- Minimum Python 3.8
- Runtime: Jinja2, contourpy, numpy, packaging, pandas, pillow, PyYAML, tornado, xyzservices
- Dev: pytest, mypy, flake8, isort, pre-commit, colorama

### Environment Variables
- `BOKEHJS_ACTION` - "build" (default), "install", or skip with custom value
- `BOKEH_IN_DOCKER` - Set to "1" when running in Docker (disables Chrome --no-sandbox)

### Adding New Models

When adding new model classes:
1. **Python**: Extend `Model` in `bokeh/models/`, register in `models/__init__.py`
2. **TypeScript**: Extend `Model` in `bokehjs/src/lib/models/`, register in `models/main.ts`
3. Add corresponding property types in `core/properties.py`
4. Add serialization support if using custom types
5. Add tests in `tests/unit/`

### Adding New Property Types

1. **Python**: Create property class in `core/property/`, add to `properties.py` exports
2. **TypeScript**: Create property class in `core/properties/`, register in property mixins
3. Add `synced: boolean` attribute for cross-language synchronization
4. Add tests in `tests/unit/bokeh/core/property/`

## Key Configuration Files

- `pyproject.toml` - Python project configuration, pytest settings, mypy configuration
- `bokehjs/package.json` - BokehJS package definition and npm scripts
- `bokehjs/make/tasks/` - Build task definitions in TypeScript
- `bokehjs/eslint.json` - TypeScript linting rules
- `.pre-commit-config.yaml` - Pre-commit hooks (code quality, eslint, isort, flake8, etc.)
- `.flake8` - Python flake8 configuration (max-line-length: 165)
- `bokehjs/tsconfig.json` - TypeScript compilation configuration