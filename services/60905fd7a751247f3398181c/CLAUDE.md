# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Universal Pathlib (`universal_pathlib`) is a Python library that extends the `pathlib_abc` API to provide a `pathlib.Path`-like interface for various filesystem backends via `fsspec`. It enables consistent pathlib-style code across local filesystems, cloud storage (S3, GCS, Azure), and other storage systems.

**Key Dependencies:**
- `fsspec >=2024.5.0` - filesystem_spec abstraction layer
- `pathlib-abc >=0.5.1,<0.6.0` - pathlib interface definitions
- Python 3.9+ support

## Development Commands

This project uses [nox](https://nox.thea.codes/) for task automation with `uv` as the venv backend.

```bash
# Install nox
uv tool install nox

# List available sessions
nox --list-sessions

# Run full CI pipeline (lint + tests + type-checking + type-safety)
nox

# Run tests only
nox --session=tests

# Run specific test file
nox --session=tests -- upath/tests/implementations/test_local.py

# Run tests with coverage
nox --session=tests -- --cov=upath --cov-report=html

# Run linters (black, isort, flake8, bandit, pyupgrade)
nox --session=lint

# Run type checking with mypy
nox --session=type_checking

# Run type safety tests (pytest-mypy-plugins)
nox --session=typesafety

# Build distribution packages
nox --session=build

# Build documentation
nox --session=docs-build

# Serve documentation with live reload
nox --session=docs-serve
```

## Architecture

### Core Components

- **`upath/core.py`**: Main `UPath` class implementing the pathlib interface backed by fsspec. Contains ~2200 lines with extensive type overloads for protocol dispatch.
- **`upath/_chain.py`**: Chain parsing for handling chained/multipart URL paths (experimental).
- **`upath/_flavour.py`**: Path flavour system wrapping fsspec filesystem path operations.
- **`upath/_protocol.py`**: Protocol detection and compatibility utilities.
- **`upath/registry.py`**: Registry system mapping protocols to UPath implementations. Uses entry points for discovery.

### Filesystem Implementations (`upath/implementations/`)

Each filesystem has a dedicated module with a `Path` subclass:
- **`local.py`**: `PosixUPath`, `WindowsUPath`, `FilePath` - Local filesystem paths
- **`cloud.py`**: `S3Path`, `GCSPath`, `AzurePath`, `HfPath` - Cloud storage
- **`memory.py`**: `MemoryPath` - In-memory ephemeral filesystem
- **`http.py`**: `HTTPPath`, `HTTPSPath` - HTTP(S)-based filesystems
- **Other**: `GitHubPath`, `FTPPath`, `SFTPPath`, `SMBPath`, `WebdavPath`, `TarPath`, `ZipPath`, `DataPath`, `HDFSPath`, `CachedPath`

### Extension Points

- **`upath/extensions.py`**: Contains `ProxyUPath` for extending UPath API with custom methods.
- **`upath/types.py`**: Type definitions including `ReadablePathLike`, `WritablePathLike`, `JoinablePathLike`.

### Key Design Patterns

1. **Protocol Dispatch**: `UPath.__new__()` dispatches to registered subclasses based on protocol (e.g., `UPath("s3://...")` returns `S3Path`). See registry system and `get_upath_class()`.

2. **Lazy Filesystem Instantiation**: The `fs` property caches the fsspec filesystem instance on first access.

3. **Path vs URLPath**: The `path` property returns the filesystem-appropriate path (stripped of protocol), while `__str__()` returns the full URI.

4. **Storage Options**: Authentication and filesystem options passed as kwargs (e.g., `UPath("s3://bucket", anon=True)`).

5. **Customization Methods**:
   - `_parse_storage_options()` - Extract options from URL
   - `_fs_factory()` - Control filesystem instantiation
   - `_transform_init_args()` - Modify init arguments

### Testing Structure

- **`upath/tests/implementations/`**: Tests for each filesystem implementation
- **`upath/tests/pathlib/`**: CPython pathlib compatibility tests
- **`typesafety/`**: pytest-mypy-plugins type safety tests
- **Fixtures**: `upath/tests/conftest.py` provides filesystem fixtures

## Code Style

- **Formatting**: black (88 char line length), isort
- **Linting**: flake8 with bugbear and comprehensions plugins
- **Upgrades**: pyupgrade (--py39-plus)
- **Security**: bandit
- **Type Checking**: mypy with strict settings, ignores for pydantic/fsspec modules
- **Pre-commit**: Configured in `.pre-commit-config.yaml`

## Important Conventions

1. **Protocol strings**: Use lowercase (e.g., `"s3"`, `"memory"`, not `"S3"`)
2. **PathLike protocol**: Only `PosixUPath`, `WindowsUPath`, `FilePath` implement `os.PathLike`
3. **Unsupported operations**: Raise `UnsupportedOperation` (Python 3.13+) or `NotImplementedError`
4. **Deprecation warnings**: Use `_protocol_dispatch=False` is deprecated; use `ProxyUPath` instead