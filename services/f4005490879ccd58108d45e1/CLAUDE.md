# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Girder is a web-based data management platform developed by Kitware. It's a Python server (CherryPy) with a Backbone.js web client, supporting MongoDB for data storage and plugins for extensibility.

## Development Commands

### Install Dependencies
```bash
# Create virtual environment and install all dependencies
python3 -m venv girder_env
source girder_env/bin/activate
pip install --upgrade pip
pip install --editable .[sftp,mount] --editable clients/python --requirement requirements-dev.txt

# Install web client dependencies
npm ci
```

### Run Python Linting
```bash
tox -e lint
```

### Run Python Tests
```bash
# Run all pytests
tox -e pytest

# Run single test file
pytest test/test_file.py

# Run single test
pytest test/test_user.py::testHasOtpEnabled

# Run with mock MongoDB (no MongoDB required)
pytest --mock-db test/test_user.py

# Run with real MongoDB (default)
pytest --mongo-uri mongodb://localhost test/test_user.py

# Keep database after test (for debugging)
pytest --keep-db test/test_user.py
```

### Run Web Client Linting
```bash
npm run lint
```

### Build Web Client
```bash
girder build --dev
```

### Run Development Server
```bash
# Start Girder server
girder-server
# or
girder serve
```

### Other Development Tasks
```bash
# Update public symbols list (required when adding new public APIs)
python scripts/publicNames.py > scripts/publicNames.txt

# Format Python code
tox -e format
```

## Architecture

### Core Python Components (`girder/`)

- **`girder/api/`** - REST API endpoints built on CherryPy
  - `rest.py` - Base classes for REST resources (`Resource`, `RestException`)
  - `describe.py` - API documentation generation (OpenAPI/Swagger)
  - `v1/` - Version 1 API endpoints (collection, file, folder, item, user, etc.)

- **`girder/models/`** - MongoDB document models and business logic
  - `model_base.py` - Base model class with CRUD, access control, caching
  - `user.py`, `folder.py`, `item.py`, `file.py`, `collection.py`, `group.py` - Core entities
  - `assetstore.py` - File storage backend abstraction (filesystem, S3, GridFS)
  - `upload.py` - Chunked file upload handling
  - `token.py` - Authentication tokens
  - `setting.py` - System settings

- **`girder/utility/`** - Server utilities
  - `server.py` - CherryPy server setup
  - `acl_mixin.py` - Access control list mixing
  - `filesystem_assetstore_adapter.py`, `s3_assetstore_adapter.py`, `gridfs_assetstore_adapter.py` - Storage backends
  - `mail_utils.py` - Email sending
  - `_cache.py` - Dogpile caching configuration

- **`girder/plugin.py`** - Plugin system using `GirderPlugin` base class and entrypoints

- **`girder/events.py`** - Event system for loose coupling between components

- **`girder/web_client/`** - Backbone.js web client (JavaScript, Stylus, Pug templates)

### Plugins (`plugins/`)

Each plugin is a Python package with a `GirderPlugin` subclass. Standard structure:
```
plugins/<plugin_name>/
  girder_<plugin_name>/
    __init__.py          # Defines GirderPlugin class with load() method
    constants.py         # Plugin constants
    <module>_rest.py     # API endpoints
    models/
      __init__.py
      <model>.py        # Model classes
    web_client/          # Frontend (optional)
      src/
      package.json
```

Example plugin `load()` pattern:
```python
class MyPlugin(GirderPlugin):
    CLIENT_SOURCE_PATH = 'web_client'

    def load(self, info):
        info['apiRoot'].myresource = MyResource()
        ModelImporter.registerModel('mymodel', MyModel, 'myplugin')
        events.bind('event.name', 'myplugin', handlerFunction)
```

### Testing (`pytest_girder/`, `test/`)

pytest-girder provides fixtures:
- `db` - MongoDB test database (real or mocked with `--mock-db`)
- `server` - CherryPy test server with request method
- `admin` - Admin user fixture
- `user` - Regular user fixture (depends on admin)
- `fsAssetstore` - Filesystem assetstore for testing uploads

Test files use pytest markers to load plugins:
```python
@pytest.mark.plugin('myplugin')
def test_feature(server, user):
    ...
```

### Client (`clients/python/`)

Python client library (`girder_client`) for interacting with Girder servers.

## Key Patterns

### Access Control
Models inherit from `AclMixin` to implement permission system with specific access levels (READ, WRITE, ADMIN).

### REST Resources
API endpoints extend `Resource` class, using `@access` decorator for permission control and `@describeRoute` for OpenAPI docs.

### Events
Loose coupling via `events.bind('event.name', 'handlerId', callback)` and `events.trigger('event.name', info)`.

### Settings
System settings stored in MongoDB, accessed via `Setting().get(SettingKey.<KEY>)`.

## Dependency Order

When installing editable packages, order matters:
1. pytest_girder
2. plugins/jobs (core dependency)
3. Other plugins