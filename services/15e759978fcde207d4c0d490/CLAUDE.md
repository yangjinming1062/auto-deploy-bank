# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Frappe Framework is a metadata-driven, full-stack low-code web framework with Python backend and Vue 3 frontend. It uses MariaDB/PostgreSQL as database, Redis for caching, and esbuild for asset bundling.

**Python**: >=3.10, <3.13
**Node**: >=18

## Common Commands

### Building Assets (Frontend)
```bash
# Build assets for production
npm run build

# Production build with optimization
npm run production

# Watch mode for development
npm run watch
```

JavaScript/CSS bundling is handled by esbuild (see `esbuild/esbuild.js`). The framework includes multiple bundles:
- `libs.bundle.js` - External libraries
- `desk.bundle.js` - Desk UI components
- `form.bundle.js` - Form components
- `list.bundle.js` - List view
- `controls.bundle.js` - Form controls
- `report.bundle.js` - Report views
- `telemetry.bundle.js` - Telemetry
- `billing.bundle.js` - Billing

### Python Testing
Tests use a custom test runner (`frappe/test_runner.py`) with unittest framework:

```bash
# Run all tests for a site
bench --site [site-name] test

# Run tests for a specific doctype
bench --site [site-name] test [DoctypeName]

# Run tests for a specific module
bench --site [site-name] test --module [ModuleName]

# Run a specific test file
bench --site [site-name] test [TestModule] [TestClass] [test_method_name]

# Run with verbose output
bench --site [site-name] test --verbose

# Run with profiling
bench --site [site-name] test --profile

# Generate JUnit XML output for CI
bench --site [site-name] test --junit-xml-output=test-output.xml
```

Database backends tested: MariaDB 10.6 and PostgreSQL 12.4 in CI.

### Code Quality

Python linting and formatting with **ruff** (configured in `pyproject.toml`):
- Line length: 110 characters
- Pre-commit hooks: `pre-commit install`

```bash
# Run ruff linter with auto-fix
ruff --fix

# Format with ruff
ruff format
```

Pre-commit hooks (`.pre-commit-config.yaml`):
- Trailing whitespace removal
- Yaml/JSON/Toml validation
- Python AST checking
- ruff (lint + format)
- prettier (JS/Vue/SCSS)
- eslint (JavaScript)

### Installation & Setup

**Development installation** uses Bench (Frappe's CLI tool). See:
- [Development installation docs](https://frappeframework.com/docs/user/en/installation)
- [Docker installation](https://github.com/frappe/frappe_docker)

## Architecture Overview

### Backend (Python)

**Core Framework** (`frappe/`):
- `app.py` - WSGI application entry point with request middleware stack
- `hooks.py` - Application hooks configuration (assets, permissions, lifecycle events)
- `__init__.py` - Main initialization and module preloading

**Database Layer** (`frappe/database/`):
- `database.py` - Core database connection and query execution
- `query.py` - SQL query builder with parameter binding
- `schema.py` - Schema management and migration utilities
- `mariadb/` and `postgres/` - Database-specific implementations
- **Query Builder**: Modern query builder in `frappe/query_builder/` replacing old ORM patterns

**Document Model** (`frappe/model/`):
- `base_document.py` - Base class for all documents
- `document.py` - Core Document class with CRUD operations
- `meta.py` - DocType metadata and field definitions
- `db_query.py` - Database query interface for list views and reports
- `naming.py` - Document naming series and generation
- `rename_doc.py` - Document renaming with references update

**Core System** (`frappe/core/`):
- `doctype/` - Core DocTypes (DocType, User, Role, File, etc.)
- Contains fundamental models required for framework operation

**Desk/UI** (`frappe/desk/`):
- `listview.py` - List view configuration and data loading
- `query_report.py` - Query-based report engine
- `reportview.py` - List view query processing and filtering
- `search.py` - Global search implementation
- `doctype/` - Desk-specific UI components for various DocTypes

**Website** (`frappe/website/`):
- Website rendering and routing
- Static file serving
- Page templates and web forms

**Tests** (`frappe/tests/`):
- Unit tests with custom fixtures and test utilities
- `test_runner.py` - Custom test runner with site initialization
- `utils.py` - Test helpers (mocking, fixtures, etc.)

### Frontend (JavaScript/TypeScript)

**Public Assets** (`frappe/public/`):
- `js/` - Client-side JavaScript modules
  - Vue 3 components
  - Desk UI components
  - Form controls and widgets
- `scss/` - Styling (Bootstrap 4.6 based)
- `css/` - Compiled stylesheets

**Build System** (`esbuild/`):
- `esbuild.js` - Main build configuration
- Individual plugins for Vue, SCSS, and HTML processing
- Multiple entry points for different bundles

**Testing** (`cypress/`):
- End-to-end UI tests with Cypress
- Coverage reporting with nyc

### Key Patterns

1. **Metadata-Driven**: DocTypes define structure via JSON metadata (in `frappe/core/doctype/` and other modules), no ORM models needed
2. **Hooks System**: `hooks.py` defines lifecycle events, asset inclusion, permissions, and integrations
3. **Single Source of Truth**: DocType metadata in JSON drives both database schema and UI
4. **Desk vs Website**: Separate interfaces for app/desk (authenticated users) and website (public pages)
5. **API-First**: REST API via `/api/method/[name]` with RPC-style endpoints

## Important Hooks (hooks.py)

Common hooks used in apps built on Frappe:

- `app_name`, `app_title`, `app_publisher` - App metadata
- `app_include_js`, `app_include_css` - Assets bundled into app
- `web_include_js`, `web_include_css` - Website assets
- `before_install`, `after_install` - Installation lifecycle
- `permission_query_conditions`, `has_permission` - Row-level security
- `on_login`, `on_logout` - Session hooks
- `notification_config` - User notifications
- `website_route_rules` - URL routing for website
- `calendars` - Calendar DocTypes for scheduling
- `leaderboards` - Dashboard metrics configuration

## Development Notes

- **Database Changes**: Schema changes via `frappe.database.schema` classes, applied through migration system
- **Performance**: Built-in caching layer with Redis, query result caching
- **Background Jobs**: RQ (Redis Queue) for async tasks
- **Internationalization**: Translation system in `frappe/translate.py` with `.po` files
- **PDF Generation**: WeasyPrint for server-side PDFs
- **Email**: Built-in email queue and delivery system

## Testing Notes

- Tests run in isolated site context with `frappe.init()` and `frappe.connect()`
- MariaDB and PostgreSQL both supported via `frappe.database.mariadb` and `frappe.database.postgres`
- Test fixtures via `frappe.tests.fixtures`
- UI tests in Cypress separate from Python unit tests
- Test timeouts: SLOW_TEST_THRESHOLD = 2 seconds in test_runner.py

## Resources

- [Official Documentation](https://frappeframework.com/docs)
- [API Reference](https://frappeframework.com/docs/user/en/api)
- [Development Guide](https://frappeframework.com/docs/user/en/guides)
- [StackOverflow](https://stackoverflow.com/questions/tagged/frappe)