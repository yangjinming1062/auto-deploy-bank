# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Wagtail is a Django-based content management system focused on user experience and developer flexibility. The codebase is organized as a standard Django project with extensive admin functionality, a REST API, and a React-based frontend built with Webpack.

## High-Level Architecture

The main `wagtail/` package contains:

- **admin/** - Core admin interface (views, templates, panels, tests)
- **models/** - Core models (Page, Site, etc.)
- **images/** - Image management and rendition system
- **documents/** - Document storage and serving
- **search/** - Elasticsearch/PostgreSQL search integration
- **api/** - REST API endpoints (v2)
- **snippets/** - Reusable content snippets
- **blocks/** - StreamField block definitions
- **sites/** - Multi-site support
- **contrib/** - Optional modules (forms, redirects, etc.)
- **locale/** - Internationalization translations

Frontend assets live in `client/` and are compiled to `wagtail/admin/static/wagtailadmin/`. The frontend uses React, Draft.js, Redux, and various UI libraries.

## Common Development Commands

### Initial Setup

```bash
# Install Python dependencies in development mode
pip install -e .[testing,docs] --config-settings editable-mode=strict

# Install Node dependencies
npm ci

# Build frontend assets
npm run build

# Install pre-commit hooks
pre-commit install
```

### Testing

```bash
# Run all Python tests
python runtests.py

# Run tests for a specific module
python runtests.py wagtail
python runtests.py wagtail.images
python runtests.py wagtail.tests.test_blocks.TestIntegerBlock

# Run tests against PostgreSQL
python runtests.py --postgres

# Run tests against Elasticsearch
python runtests.py --elasticsearch8

# Run JavaScript unit tests
npm run test:unit

# Run integration tests (requires Django server running)
npm run test:integration

# Run tests with coverage
coverage run runtests.py
coverage report -m
coverage html
```

### Linting and Formatting

```bash
# Check all code style (Python, JS, CSS, docs)
make lint

# Fix all code style issues
make format

# Or run individually:
ruff check . --fix    # Python lint/fix
ruff format .         # Python formatting
npm run fix           # JS/CSS formatting
djhtml --check        # Template formatting
```

### Frontend Development

```bash
# Build assets in production mode
npm run build

# Watch and rebuild assets during development
npm start

# Run Storybook pattern library
npm run storybook

# TypeScript type checking
npm run lint:ts
```

### Documentation

```bash
# Build Sphinx documentation
cd docs/
make html

# Build with live reload
cd docs/
make livehtml
```

## Testing Matrix

Wagtail tests against multiple Python/Django versions via tox:

- **Python**: 3.10, 3.11, 3.12, 3.13
- **Django**: 4.2, 5.1, 5.2 (stable), main
- **Databases**: SQLite, PostgreSQL, MySQL, SQL Server
- **Search**: Elasticsearch 7, Elasticsearch 8, no Elasticsearch

Example tox environments:
```bash
tox -l  # List all environments
tox -e py312-dj51-sqlite-noelasticsearch  # Run specific env
```

## Key Configuration Files

- **pyproject.toml** - Python dependencies, pytest config
- **tox.ini** - Multi-version testing configuration
- **package.json** - Node dependencies and npm scripts
- **runtests.py** - Test runner with database/search options
- **Makefile** - Common development commands
- **.eslintrc.js** - JavaScript linting
- **stylelint.config.mjs** - CSS linting
- **ruff.toml** - Python linting/formatting
- **.pre-commit-config.yaml** - Pre-commit hooks

## Development Notes

- Frontend assets are **not committed** - run `npm run build` before packaging releases
- Static files are compiled from `client/` to `wagtail/admin/static/wagtailadmin/`
- Integration tests use Puppeteer and target a running Django server on port 8000
- Browser support: Firefox ESR, Chrome last 2, Edge last 2, Safari last 3, iOS last 2
- Accessibility target: WCAG 2.1 AA level
- The `wagtail/test/` directory contains a test project for UI/integration testing

## Module-Specific Testing

Test paths follow module structure:
- `wagtail/admin/tests/` - Admin interface tests
- `wagtail/images/tests/` - Image functionality tests
- `wagtail/documents/tests/` - Document tests
- `wagtail/search/tests/` - Search tests
- `wagtail/tests/` - Core functionality tests

## Build and Release

```bash
# Create release packages (requires npm build first)
python -m build

# Install from local build
pip install dist/wagtail-*.whl
```

## Environment Variables

Key test environment variables:
- `DATABASE_ENGINE` - Database backend
- `DATABASE_NAME/HOST/PASSWORD/PORT` - Database credentials
- `ELASTICSEARCH_URL` - Elasticsearch instance
- `ELASTICSEARCH_VERSION` - ES version (7 or 8)
- `USE_EMAIL_USER_MODEL` - Use email-based auth
- `DISABLE_TIMEZONE` - Disable timezone support
- `TEST_ORIGIN` - Test server URL for integration tests