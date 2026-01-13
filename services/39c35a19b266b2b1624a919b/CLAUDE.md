# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**django-SHOP** is a RESTful e-commerce framework built on Django (version 1.2.4). It's designed as the e-commerce counterpart to django-CMS, focusing on modularity, flexibility, and RESTful APIs. The framework uses a **product-centric approach** where product models reflect their physical properties rather than using a predefined database schema.

Key principles:
- Product models are defined based on product properties, not vice versa
- Component-based page composition using django-CMS plugins
- Dual support for HTML views and RESTful services
- Programmable cart modifiers for taxes, shipping, and discounts
- Workflow-based order fulfillment using finite state machines
- Modular architecture allowing third-party extensions

## Development Commands

### Testing
```bash
# Run all tests
tox

# Run tests for specific Python/Django version
tox -e py37-django22

# Run tests directly with pytest
cd tests
pytest

# Run a single test file
pytest test_cart.py

# Run a specific test
pytest test_cart.py::test_add_cart_item
```

Test configuration is in `pytest.ini` with settings module `testshop.settings`. Tests use pytest-factoryboy with fixtures defined in `tests/conftest.py`.

### Development Workflow
```bash
# Install development dependencies
pip install -r tests/requirements.txt

# Run migrations for test project
cd tests
python manage.py makemigrations testshop

# Use the shop management command (in testshop)
python manage.py shop --help
```

### Multi-Version Testing
The project supports testing across multiple Python and Django versions via tox:
- Python: 3.6, 3.7, 3.8
- Django: 2.1, 2.2, 3.0

See `tox.ini` for the complete test matrix.

## Code Architecture

### Core Components

**Models** (`shop/models/`):
- Abstract base models that must be materialized in the implementing project
- Core models: Product, Cart, Order, Customer, Address, Notification
- Default implementations in `shop/models/defaults/` (Commodity, CartModel, OrderModel, etc.)
- Uses `django_polymorphic` for model inheritance

**Views** (`shop/views/`):
- Class-based views organized by function: cart, catalog, checkout, order, auth
- Dual interface: traditional HTML rendering and REST API endpoints

**Serializers** (`shop/serializers/`):
- Django REST Framework serializers for API responses
- Separate serializers for different contexts (catalog, cart, checkout, order)
- Default serializers in `shop/serializers/defaults/`

**Modifiers** (`shop/modifiers/`):
- Pluggable system for cart calculations (taxes, shipping, discounts)
- Payment modifiers in `shop/payment/`
- Shipping modifiers in `shop/shipping/`

**Cascade Plugins** (`shop/cascade/`):
- django-CMS plugins for building shop pages
- Plugins for cart, catalog, checkout, order management
- Extensible via plugin base classes

**REST API** (`shop/rest/`):
- API endpoints configured in `shop/urls/rest_api.py`
- Custom renderers and filters for shop-specific needs

### Configuration

All configuration is centralized in `shop/conf.py` via the `app_settings` object. Key settings:
- `SHOP_APP_LABEL`: Required setting identifying the project implementing the shop
- `SHOP_DEFAULT_CURRENCY`: Default currency (EUR)
- `SHOP_CUSTOMER_SERIALIZER`: Customer serializer class
- `SHOP_PRODUCT_SUMMARY_SERIALIZER`: Product serialization for list views
- `SHOP_MONEY_FORMAT`: Currency formatting string
- `SHOP_DECIMAL_PLACES`: Decimal places for money fields

### URL Patterns

URLs are modularized in `shop/urls/`:
- `rest_api.py`: REST API endpoints
- `auth.py`: Authentication endpoints
- `payment.py`: Payment processing endpoints

### Money Handling

Custom money implementation in `shop/money/`:
- `Money` class for currency operations
- Database field integration with `MoneyField`
- ISO 4217 currency support
- Serialization for REST API

### Email Authentication

Separate package in `email_auth/` for email-based authentication.

### Deferred Model Mapping

The framework uses a deferred mapping system (`shop/deferred.py`) to handle foreign key relationships to abstract models. This allows the shop's abstract models to reference concrete models from the implementing project.

## Key Files

- `shop/apps.py`: Django app configuration, performs sanity checks on startup
- `shop/management/commands/shop.py`: Management command with subcommands for shop operations
- `shop/conf.py`: Central configuration object with all shop settings
- `shop/exceptions.py`: Custom exceptions (e.g., ProductNotAvailable)
- `shop/signals.py`: Django signals for shop events
- `tests/conftest.py`: Test fixtures using pytest-factoryboy

## Dependencies

Key dependencies (see `setup.py`):
- Django >=2.1,<3.1
- django-cms >=3.7 (for page composition)
- djangorestframework >=3.9,<4 (for REST API)
- django-fsm (finite state machine for order workflows)
- django-filer (file management)
- django_polymorphic (model inheritance)
- django-rest-auth (authentication for REST API)

## Testing Architecture

Tests are in the `tests/` directory with a test project `tests/testshop/`. Uses:
- pytest for test execution
- factory_boy for model factories
- pytest-factoryboy for fixture injection
- Django test client and DRF APIClient for requests

Factory definitions are registered in `conftest.py` and can be used directly in tests.

## Documentation

Full documentation is available at: https://django-shop.readthedocs.io/en/latest/

For development, a demo shop can be quickly set up using the Cookiecutter template at: https://github.com/awesto/cookiecutter-django-shop