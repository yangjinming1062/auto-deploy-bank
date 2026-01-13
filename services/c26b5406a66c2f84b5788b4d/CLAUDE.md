# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

**FlaskBB** - A classic forum software written in Python using the Flask microframework. Current version: **2.1.0** (Production/Stable).

## Development Setup

### Quick Start
```bash
# Create virtualenv and setup development instance
make devconfig    # Generate development config
make install      # Install dependencies and FlaskBB
make run          # Run development server (http://localhost:5000)
```

### Available Make Commands
- `make install` - Install dependencies and FlaskBB
- `make run` - Run development server with debug/reload
- `make test` - Run test suite via tox (Python 3.9-3.12)
- `make lint` - Run flake8 linter
- `make isort` - Sort Python imports
- `make clean` - Remove __pycache__, .pyc, .pyo files
- `make docs` - Build Sphinx documentation
- `make devconfig` - Generate development configuration
- `make frontend` - Run webpack dev server (watches flaskbb/themes/aurora)
- `make dist` - Create distribution packages (wheel, sdist)
- `make upload` - Upload to PyPI

### Testing
- **Framework**: pytest with coverage reporting
- **Run all tests**: `make test` or `tox`
- **Run specific test**: `pytest tests/<path_to_test> -vvl`
- **Run with coverage**: `pytest --cov flaskbb`
- **Multi-version testing**: tox tests Python 3.9, 3.10, 3.11, 3.12
- **Coverage reports**: `coverage report` (stored in tests/htmlcov/)

CI runs automatically on GitHub Actions (tests.yml) with Python 3.10-3.12

### Code Quality
- **Linter**: flake8 (B, E, F, W, B9 plugins) - Max complexity: 10, Line length: 88
- **Import sorting**: isort with known_first_party=flaskbb
- **Pre-commit hooks**: Ruff (auto-formatting enabled)
- **Run linting**: `make lint`

### FlaskBB CLI Commands
The `flaskbb` CLI is available after installation:
- `flaskbb run --debugger --reload` - Run dev server
- `flaskbb install` - Install FlaskBB
- `flaskbb makeconfig -d` - Generate config
- `flaskbb shell` - Interactive shell with app context
- `flaskbb db <alembic commands>` - Database migrations
- `flaskbb users --help` - User management
- `flaskbb plugins --help` - Plugin management
- `flaskbb themes --help` - Theme management
- `flaskbb translations --help` - Translation management

## Project Architecture

### Core Structure
```
flaskbb/
├── app.py              # Flask application factory (create_app)
├── extensions.py       # Flask extensions initialization
├── core/               # Business logic core
├── auth/               # Authentication module
├── forum/              # Forum features
├── user/               # User management
├── display/            # UI display logic
├── management/         # Admin interface
├── plugins/            # Plugin system (extensible)
├── themes/             # Theme system (default: Aurora)
├── tokens/             # Token management
├── utils/              # Helper utilities
├── cli/                # Command-line interface
├── migrations/         # Alembic migrations
├── translations/       # i18n (13 languages)
├── static/             # Web assets
└── templates/          # Jinja2 templates
```

### Flask Extensions (flaskbb/extensions.py:1-80)
- **db** - SQLAlchemy with session_options={"future": True}
- **whooshee** - Full-text search (Whoosh)
- **login_manager** - User authentication
- **mail** - Email notifications
- **cache** - Caching (Redis backend)
- **redis_store** - Redis integration
- **debugtoolbar** - Debug toolbar
- **alembic** - Database migrations
- **themes** - Theme system
- **babel** - Internationalization
- **csrf** - CSRF protection
- **limiter** - Rate limiting
- **celery** - Async task queue
- **allows** - Permission system
- ****__init__.py:19** imports `create_app` from flaskbb.app

### Key Features
- **Forum Software**: Topics, posts, forums, private messages
- **User System**: Groups, permissions, profiles, authentication
- **Admin Interface**: Group management, settings, moderation
- **Search**: Full-text search via Whoosh
- **Themes**: Customizable via flask-themes2 (Aurora theme included)
- **Plugins**: Extensible architecture with hook system
- **i18n**: 13 languages (DA, DE, ES, FR, NB_NO, PL, PT_BR, RU, SV_SE, UK, ZH_CN, ZH_TW, EN)
- **Task Queue**: Celery with Redis broker
- **Caching**: Redis-based caching

### Configuration
- **Development**: `make devconfig` creates config file
- **Default config**: `flaskbb/configs/default.py`
- **Test config**: `flaskbb/configs/testing.py`
- **Template**: `flaskbb/configs/config.cfg.template`
- **Config class**: setup.cfg:18-131 defines metadata, pytest, flake8, coverage settings
- **Logging**: Configurable via LOG_CONF_FILE (setup.cfg:63-140)
- **Database**: SQLAlchemy with naming conventions (setup.cfg:35-42)

### Entry Points
- **WSGI**: `wsgi.py` - Production WSGI entry
- **Dev server**: `flaskbb run` or `make run`
- **Celery worker**: `celery_worker.py`
- **CLI**: `flaskbb.cli` package with Click commands

### Dependencies (Key)
- Flask ecosystem (Flask, SQLAlchemy, WTForms, Login, Babel, etc.)
- Redis (caching, Celery broker)
- Celery (async tasks)
- Whoosh (full-text search)
- pytest (testing)
- Alembic (migrations)
- FlaskBBPluginManager (plugin architecture)

### Documentation
- **README.md** - Quickstart guide
- **CONTRIBUTING.md** - Contribution guidelines
- **Full docs** - https://flaskbb.readthedocs.io
- **Build docs**: `make docs` (Sphinx)

### Important Notes
- Pre-commit hooks: Ruff (v0.4.1) with auto-formatting
- Tests use pytest with auto-numprocesses
- Coverage stored in tests/htmlcov/
- Max line length: 88 chars
- Max complexity: 10
- Plugin system supports hooks via pluggy
- Themes system uses flask-themes2
- Translation system uses Flask-BabelPlus