# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Reference

### Common Commands

**Python/Django:**
```bash
# Run all tests
python -m pytest cms/tests/
python manage.py test  # Alternative using Django test runner

# Run a single test file
python manage.py test cms.tests.test_admin

# Install Python dependencies
pip install -e .
uv pip install -e .  # Faster alternative

# Lint Python code (Ruff)
ruff check .
ruff format .

# Install test requirements for specific Django versions
pip install -r test_requirements/django-4.2.txt

# Runspell check (codespell)
codespell
```

**JavaScript/Frontend:**
```bash
# Install Node dependencies
npm install
./scripts/install-npm-dependencies.sh

# Lint JavaScript
gulp lint

# Run unit tests (Karma + Jasmine)
gulp unitTest

# Run integration tests (CasperJS)
gulp integrationTest

# Build frontend assets (Webpack + Gulp)
gulp build

# Watch mode for development
gulp watch

# Generate icon fonts
gulp icons

# Compile Sass
gulp sass
```

**Documentation:**
```bash
# Build documentation
cd docs && make html

# Run spell check on docs
cd docs && make spelling
```

**Releasing:**
```bash
# Generate changelog
./scripts/make-changelog

# Make release
./scripts/make-release
```

## Code Architecture

### High-Level Structure

Django CMS is a hierarchical, enterprise-grade content management system with three main components:

1. **cms/** - Core Django CMS application (431 Python files)
   - Manages hierarchical pages with draft/publish workflows
   - Plugin system for extensible content blocks
   - Admin interface with toolbar
   - Multi-site and multilingual support
   - Version control system

2. **menus/** - Navigation menu system
   - Template tags for menu rendering
   - Extensible navigation architecture
   - Integration with django-treebeard for tree structures

3. **cms/static/cms/** - Frontend assets
   - JavaScript modules (toolbar, clipboard, sideframe, etc.)
   - Sass stylesheets compiled to CSS
   - jQuery-based widgets
   - Webpack 3.0 bundles
   - Icon fonts and images

### Key Python Modules

**Core Models** (`cms/models/`):
- `page.py` - Page model with hierarchical tree structure (django-treebeard)
- `placeholder.py` - Content placeholder system for plugins
- `pluginmodel.py` - Plugin base classes and rendering
- `title.py` - Multi-language title translations

**Plugin System** (`cms/plugin_*.py`):
- `plugin_pool.py` - Plugin registration and discovery
- `cms_plugins.py` - Base plugin class
- `plugin_base.py` - Plugin rendering engine

**Admin & Toolbar**:
- `admin/` - Django admin extensions
- `cms_toolbars.py` - Toolbar customization system
- `toolbar/` - Frontend toolbar functionality

**API & Integration**:
- `api.py` - Public API functions
- `cms_menus.py` - Menu system integration
- `signals/` - Django signals for plugin/page events

### Frontend Architecture

**JavaScript Modules** (`cms/static/cms/js/`):
- `modules/` - Core CMS modules (toolbar, clipboard, sideframe)
- `widgets/` - Form widgets and UI components
- `dist/` - Webpack bundles
- `libs/` - Third-party libraries (jQuery, jsTree, etc.)

**Build System**:
- Webpack 3.0 - Module bundling with CommonsChunkPlugin
- Gulp 4.0 - Task automation (lint, test, build)
- Babel - ES6+ transpilation
- Sass - CSS preprocessing

### Plugin System Architecture

The plugin system is one of django CMS's core features:

1. **Plugin Pool** (`cms/plugin_pool.py`) - Registers and discovers all available plugins
2. **Plugin Base Classes** (`cms/plugin_base.py`) - Provides rendering and admin interfaces
3. **Placeholder System** (`cms/models/placeholder.py`) - Defines content areas where plugins can be added
4. **CMS Plugins** (`cms/cms_plugins.py`) - Concrete plugin implementations

Plugins can be:
- Rendered in admin for content editing
- Rendered on frontend with templates
- Nested hierarchically
- Extended by third-party applications

### Database Support

Tested and supported:
- **PostgreSQL** (primary)
- **MySQL**

Run tests with specific databases using test requirements:
```bash
pip install -r test_requirements/postgresql.txt
python manage.py test
```

## Development Standards

### Code Quality

**Python**:
- Line length: 119 characters
- Primary linter: **Ruff** (configured in `pyproject.toml`)
- Legacy linter: Flake8
- Import sorting: Ruff isort
- Format style: Ruff format (double quotes)
- Pre-commit hooks enforce: pyupgrade, django-upgrade, ruff, codespell

**JavaScript**:
- Line length: 119 characters
- Linter: **ESLint** (configured in `.eslintrc.js`)
- Use single quotes in JS code
- Max complexity: 10
- Max parameters: 3

**Styling**:
- Sass/SCSS with 4-space indentation
- Autoprefixer for CSS compatibility
- Source maps for debugging

### Testing Standards

**Python Tests** (`cms/tests/`):
- 58 test files
- Uses Django TestCase
- Coverage tracked with coverage.py
- Uploaded to Codecov

**JavaScript Tests** (`cms/tests/frontend/`):
- Unit tests: Karma + Jasmine
- Integration tests: CasperJS + djangocms-casper-helpers
- Tests run via Gulp tasks

**Test Commands**:
```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test cms.tests.test_page:TestPageApi

# Frontend unit tests
gulp unitTest

# Integration tests
gulp integrationTest
```

### Commit Messages

Follow **Conventional Commits** specification (https://conventionalcommits.org/):
```
feat: add new plugin for video content
fix: resolve issue with page slug generation
docs: update installation guide for Django 5.2
```

### Branching Strategy

- **main** - Primary development branch
- Pull requests target `main` branch
- Security fixes backported to older branches by core team

## Important Notes

### Django & Python Compatibility

- **Python**: 3.9, 3.10, 3.11, 3.12, 3.13
- **Django**: 4.2, 5.0, 5.1, 5.2
- Test matrix covers all combinations in CI

### Project Configuration

**Build System**: setuptools with setuptools-scm for version management

**Key Files**:
- `pyproject.toml` - Python packaging and tool configuration (Ruff, codespell)
- `setup.py` - Legacy wrapper (calls setuptools)
- `.eslintrc.js` - ESLint configuration
- `.babelrc` - Babel transpilation
- `webpack.config.js` - Webpack bundling
- `gulpfile.js` - Gulp task definitions
- `.pre-commit-config.yaml` - Pre-commit hooks

### Documentation

- **User Docs**: https://docs.django-cms.org/
- **Developer Docs**: `docs/` directory (Sphinx)
- **README**: `README.rst` - Project overview
- **Contributing**: `CONTRIBUTING.rst` - Contribution guidelines
- **Security**: `SECURITY.md` - Security policy

### Community

- **Discord**: https://discord-support-channel.django-cms.org
- **Association**: https://www.django-cms.org/en/memberships/
- **Code of Conduct**: Enforced in all community spaces
- **Work Groups**: Join contributor teams for different topics

### Security

- Report security issues privately (see `SECURITY.md`)
- Security analysis with CodeQL in CI
- Dependencies scanned in CI pipeline

## Third-Party Dependencies

**Core Django CMS** (`pyproject.toml`):
- Django >= 4.2
- django-classy-tags >= 0.7.2
- django-formtools >= 2.1
- django-treebeard >= 4.3
- django-sekizai >= 0.7

**Frontend** (`package.json`):
- jQuery (DOM manipulation)
- Jasmine (testing)
- CasperJS (integration testing)
- Webpack 3.0 (bundling)
- Gulp 4.0 (task runner)
- Babel (transpilation)
- Sass (CSS preprocessing)

## Release Process

1. Generate changelog: `./scripts/make-changelog`
2. Update version (setuptools-scm handles this from git tags)
3. Create release: `./scripts/make-release`
4. CI publishes to PyPI automatically
5. Documentation updated on ReadTheDocs

## CI/CD

**GitHub Actions** (13 workflows):
- **test.yml** - Python tests (Django × Python × DB matrix)
- **linters.yml** - Ruff linting
- **frontend.yml** - Frontend tests
- **docs.yml** - Documentation build
- **publish-to-test-pypi.yml** / **publish-to-live-pypi.yml** - Release automation
- CodeQL security analysis
- Spell checking

Tests run on:
- Python 3.9-3.13
- Django 4.2-5.2
- PostgreSQL & MySQL