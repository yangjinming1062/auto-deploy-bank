# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start

The fastest way to get Shuup running locally is using Docker:

```bash
docker-compose up
```

Then open http://localhost:8000/sa and log in with username: `admin` password: `admin`

## Common Development Commands

### Python Environment Setup

Install dependencies:
```bash
pip install -r requirements-dev.txt
```

Install test dependencies:
```bash
pip install -r requirements-tests.txt
```

### Building Static Resources

Shuup requires building static resources for the frontend:

```bash
python setup.py build_resources
```

Custom build commands available via `python setup.py <command>`:
- `build_resources` - Build static resources for development
- `build_production_resources` - Build optimized production resources
- `build_messages` - Compile translations
- `build` - Run all build tasks

### Running Tests

Run all tests:
```bash
pytest shuup_tests/
```

Run with coverage:
```bash
pytest shuup_tests/ --cov shuup --cov-report html
```

Run browser tests (requires Firefox):
```bash
export SHUUP_BROWSER_TESTS=1
pytest shuup_tests/browser/front shuup_tests/browser/admin --splinter-headless
```

Run a specific test:
```bash
pytest shuup_tests/admin/test_something.py::test_function_name
```

Run tests without migrations:
```bash
pytest shuup_tests/ --nomigrations
```

### Code Style and Linting

Run all code style checks (these run in CI):
```bash
flake8 .
isort --check --diff .
black --check --diff .
```

Fix code style issues:
```bash
black .
isort .
```

Run sanity check and license header validation:
```bash
python _misc/check_sanity.py
python _misc/ensure_license_headers.py -s shuup
```

### Documentation

Build documentation:
```bash
pip install -r requirements-doc.txt
cd doc && make html
```

Generate API documentation:
```bash
./generate_apidoc.py
```

### Django Management Commands

Workbench (development Django instance):
```bash
python -m shuup_workbench migrate
python -m shuup_workbench runserver
python -m shuup_workbench shell
python -m shuup_workbench shuup_makemessages -l en  # Extract translations
python -m shuup_workbench compilemessages  # Compile translations
```

### Docker Commands

Development:
```bash
docker-compose up
docker-compose up --build  # Rebuild containers
docker-compose down  # Stop containers
```

Development override:
```bash
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up
```

## Code Architecture

### Overview

Shuup is a Django-based e-commerce platform with a modular architecture. It's composed of multiple Django apps within the `/home/ubuntu/deploy-projects/73855e46bae028bd7de1261d/shuup/` directory, each handling a specific domain of the e-commerce functionality.

### Core Directory Structure

```
shuup/
├── admin/              # Admin interface (Django admin extensions)
├── front/              # Customer-facing storefront
├── core/               # Core business logic (products, orders, customers)
├── campaigns/          # Marketing campaigns and promotions
├── customer_group_pricing/  # Customer-specific pricing
├── default_reports/    # Built-in reporting
├── default_tax/        # Tax calculation module
├── discounts/          # Discount system
├── gdpr/              # GDPR compliance features
├── importer/          # Data import utilities
├── notify/            # Notification system
├── order_printouts/   # Order document generation
├── reports/           # Reporting framework
├── simple_cms/        # Content management system
├── simple_supplier/   # Supplier management
├── tasks/             # Celery background tasks
├── themes/            # Theme system (legacy)
└── xtheme/            # Extended theming (replacement for themes/)
```

### Key Architectural Patterns

**1. Django App Modules**: Each functional area is a separate Django app with its own:
- `models.py` - Database models
- `views.py` - View logic
- `urls.py` - URL routing
- `apps.py` - App configuration
- `locale/` - Translations

**2. Provides System**: Shuup uses a "provides" pattern for extensibility. Components declare what they provide (e.g., `ProductTab`, `PaymentMethod`, `ShippingMethod`) and other modules can extend them without tight coupling.

**3. Frontend Architecture**:
- Admin: Bootstrap 3-based interface with Django admin
- Customer Front: Jinja2 templating (legacy version 2.5.0) with macro-based structure
- Themes: Jinja2-based theme system (being moved to separate addons in v4)

**4. Database Models**:
- **Product**: Central product model with variations, categories, prices
- **Shop**: Multi-store support (one database can serve multiple shops)
- **Order**: Order management with line items
- **Basket**: Shopping cart with persistence
- **Supplier**: Inventory and fulfillment management
- **Contact/Customer**: Customer information (not Django User)

**5. Pricing System**: Flexible pricing with multiple layers:
- Base price
- Customer group pricing
- Campaign discounts
- Quantity discounts

**6. Workflow System**: Custom workflow engine for order processing, approvals, and state management.

### Testing Architecture

Tests are organized by module in `/home/ubuntu/deploy-projects/73855e46bae028bd7de1261d/shuup_tests/`:
- `admin/` - Admin interface tests
- `browser/` - Selenium/browser-based integration tests
- `front/` - Customer storefront tests
- `functional/` - High-level functional tests
- `[module]/` - Unit tests for each module

Test utilities:
- `factory-boy` for test data generation
- `pytest-django` for Django integration
- `pytest-splinter` for browser automation
- Test databases managed via pytest fixtures

### Configuration and Settings

Key settings (via `shuup.core.settings`, `shuup.front.settings`, `shuup.admin.settings`):
- `SHUUP_DISABLED_MODULES` - Disable specific modules
- `SHUUP_DEFAULT_CURRENCY` - Default currency
- `SHUUP_MANAGER_STAFF_EMAIL` - Admin notifications
- `SHUUP_PRODUCT_MANUFACTURER_PAGE_SIZE` - Pagination
- `SHUUP_BROWSER_TESTS` - Enable browser testing
- `SHUUP_TESTS_CI` - CI mode flag

### Development Workflow

1. Install dependencies and build static resources
2. Run migrations: `python -m shuup_workbench migrate`
3. Create data (admin user, shops, products) via admin or shell
4. Run tests as you develop
5. Check code style before committing
6. Update translations if needed

### Important Notes

**Version Compatibility**:
- Python 3.6, 3.7, 3.8
- Django 1.11 - 2.2.x
- Jinja2 2.8.1 (older version, migration planned)

**Legacy Components**:
- `themes/` module uses deprecated Jinja2 features (migrating to addons in v4)
- JavaScript linting uses legacy ESLint 1.6.0

**Database Migrations**:
- Located in `shuup/[module]/migrations/`
- Migration from "shoop" to "shuup" brand available in `shoop-to-shuup.sql`

**CI/CD Pipeline**:
Three jobs in `.github/workflows/shuup.yml`:
1. **codestyle** - flake8, isort, black, sanity checks
2. **core** - Python 3.6/3.7/3.8 tests, migrations, messages
3. **browser** - Firefox-based integration tests

**Release Process**:
Documented in `setup.py` lines 17-38:
1. Update CHANGELOG.md
2. Update VERSION in setup.py
3. Update version in doc/conf.py
4. Commit changes
5. Tag with `git tag -a vX.Y.Z`
6. Push tag
7. Post-release commit

## Key Dependencies

**Core**:
- Django >=1.11,<2.3
- djangorestframework 3.11
- django-polymorphic 2.1.2
- django-parler 2.0.1

**Testing**:
- pytest 5.4.1
- pytest-cov 2.4.0
- pytest-django 3.9.0
- pytest-splinter 3.3.0
- factory-boy 2.7.0

**Build Tools**:
- setuptools with custom commands
- Babel 2.5.3 (translations)
- Node.js 12.21.0 (static resource building)