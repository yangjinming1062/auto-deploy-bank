# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

### Development Environment

This project uses `uv` to manage dependencies and the development environment.

- To install all dependencies for development:
  ```bash
  uv sync --extra all
  ```
- To run tests:
  ```bash
  uv run pytest
  ```
- To run the full test suite against all supported Python versions and other checks:
  ```bash
  uv run tox
  ```
- To run linting and style checks:
  ```bash
  pre-commit run --all-files
  ```

### Documentation

The documentation is built using Sphinx.

- To build the documentation:
  ```bash
  tox -e docs
  ```
  The generated HTML will be in the `doc/_build/dirhtml` directory.

### Running Examples

The `examples/` directory contains several examples of how to use Flask-Admin. To run an example (e.g., the SQLAlchemy example):

```bash
cd examples/sqla
uv run main.py
```

## High-Level Code Architecture

`flask_admin` is a Flask extension for adding admin interfaces to Flask applications. The core components are:

- **`flask_admin/base.py`**: Contains the main `Admin` class, which is the entry point for the extension.
- **`flask_admin/model/`**: Contains the model backends for different ORMs (SQLAlchemy, Peewee, etc.). This is where the logic for interacting with the database is located.
- **`flask_admin/contrib/`**: Contains the actual view implementations for each model backend.
- **`flask_admin/form/`**: Contains custom WTForms fields and utilities.
- **`flask_admin/templates/`**: Contains the Jinja2 templates for the admin interface.
- **`flask_admin/static/`**: Contains the static assets (CSS, JavaScript, images).
