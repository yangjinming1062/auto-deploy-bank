# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

### Installation

To install dependencies, run:
```
make install
```

### Development

To run the application in development mode:
```
export FLASK_APP=alerta FLASK_DEBUG=1
pip install -e .
flask run
```

### Linting

To check for linting and type errors:
```
make lint
```

### Testing

To run all tests:
```
TOXENV=ALL make test
```

To run tests for a specific database:
```
# For PostgreSQL
TOXENV=postgres make test

# For MongoDB
TOXENV=mongodb make test
```

To run a single test:
```
# For PostgreSQL
TOXENV="postgres -- tests/test_queryparser.py::PostgresQueryTestCase::test_boolean_operators" make test

# For MongoDB
TOXENV="mongodb -- tests/test_search.py::QueryParserTestCase::test_boolean_operators" make test
```

## High-level Code Architecture and Structure

This is a Flask-based application with a standard project structure.

- **`alerta/app.py`**: The main application entry point.
- **`alerta/settings.py`**: Contains the application's configuration.
- **`alerta/database/`**: Contains database-related modules.
- **`alerta/models/`**: Defines the data models for the application.
- **`alerta/views/`**: Contains the API endpoints.
- **`alerta/webhooks/`**: Contains webhook integrations.
- **`alerta/auth/`**: Handles authentication and authorization.
- **`alerta/plugins/`**: For custom plugins and integrations.
- **`tests/`**: Contains all the tests for the application.
