# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

aiohttp is an async HTTP client/server framework for Python using asyncio. It provides both client (`aiohttp.ClientSession`) and server (`aiohttp.web`) APIs with WebSocket support.

## Common Commands

```bash
# Install development dependencies
make install

# Build and install with Cython extensions (required for full development)
make .develop

# Run linters and formatters
make fmt           # pre-commit hooks (black, isort, flake8)
make lint          # fmt + mypy

# Run tests (requires .develop)
make test          # pytest -q
make vtest         # pytest -s -v (includes dev_mode tests)
make vvtest        # pytest -vv

# Run tests without Cython extensions (useful for debugging)
AIOHTTP_NO_EXTENSIONS=1 pytest tests/

# Run a single test file
pytest tests/test_client_functional.py

# Run a specific test
pytest tests/test_client_functional.py::test_simple_get -vvs

# Build documentation
make doc           # Build HTML docs
make doc-spelling  # Check documentation spelling

# Clean build artifacts
make clean
```

## Code Architecture

### Core Modules

**Client API (`aiohttp/client.py`):**
- `ClientSession` - Main HTTP client interface for making requests
- `TCPConnector` - Connection pool and management
- `ClientRequest`/`ClientResponse` - HTTP request/response handling

**Server API (`aiohttp/web.py`):**
- `Application` - Main web application container
- `Request` - HTTP request object
- `Response` - HTTP response object
- `web_urldispatcher.py` - Routing system (UrlDispatcher, RouteDef, etc.)
- `web_protocol.py` - Low-level HTTP protocol handler

**WebSocket Support:**
- `web_ws.py` - Server-side WebSocket (`WebSocketResponse`)
- `client_ws.py` - Client-side WebSocket (`ClientWebSocketResponse`)
- `http_websocket.py` - WebSocket protocol utilities
- `_websocket/` - Cython-optimized WebSocket parser/reader

### HTTP Processing Pipeline

1. **HTTP Parser** (`_http_parser.pyx`, `http_parser.py`):
   - Cython extension for fast HTTP parsing
   - Handles incoming HTTP data from llhttp (vendor/llhttp)

2. **HTTP Writer** (`_http_writer.pyx`, `http_writer.py`):
   - Writes HTTP responses

3. **Connector** (`connector.py`):
   - Manages connection pools
   - Handles DNS resolution (`resolver.py`)
   - TCP/Unix socket management

### Key Components

- **helpers.py** - Utility functions (BasicAuth, ETag, timeout handling)
- **cookiejar.py** - HTTP cookie management
- **multipart.py** - Multipart form data handling
- **payload.py** - Request/response payload encoding
- **streams.py** - Async stream readers (`StreamReader`, `DataQueue`)
- **tracing.py** - Request tracing/observability (`TraceConfig`)

### File Organization

```
aiohttp/
├── client.py, client_*.py    # Client-side implementation
├── web.py, web_*.py          # Server-side implementation
├── http_parser.py            # Pure Python fallback parser
├── http_writer.py            # Response writing
├── http_websocket.py         # WebSocket protocol
├── _http_parser.pyx          # Cython HTTP parser (fast path)
├── _http_writer.pyx          # Cython HTTP writer
├── _websocket/               # WebSocket Cython extensions
├── connector.py              # Connection pooling
├── resolver.py               # DNS resolution
├── cookiejar.py              # Cookie management
├── multipart.py              # Form data
├── payload.py                # Payload encoding
└── streams.py                # Async streams
```

### Cython Extensions

Performance-critical code uses Cython (`.pyx` files):
- `_http_parser.pyx` - HTTP response parsing (Cython fast path, pure Python fallback in `http_parser.py`)
- `_http_writer.pyx` - HTTP request writing
- `_websocket/*.pyx` - WebSocket frame parsing and masking

Rebuild extensions after modifying `.pyx` files:
```bash
make cythonize
make .develop
```

### Vendor Dependencies

- `vendor/llhttp/` - C HTTP parser library (git submodule, generated sources in `vendor/llhttp/build/`)
- After modifying llhttp, regenerate with: `make generate-llhttp`

## Development Workflow

1. Clone with submodules: `git clone --recurse-submodules https://github.com/aio-libs/aiohttp.git`
2. Install dependencies: `make install`
3. Build with Cython extensions: `make .develop`
4. Run formatters: `make fmt`
5. Make changes and run tests: `make test`

## Code Style

- Formatted with **black** (line-length: 88)
- Imports sorted with **isort**
- Type checked with **mypy** (strict settings in `.mypy.ini`)
- Flake8 for linting (see `setup.cfg` for ignore rules)
- Pre-commit hooks enforce formatting (see `.pre-commit-config.yaml`)

Run `make fmt` to apply all formatting automatically.

## Testing Notes

- Tests use `pytest` with `pytest-xdist` for parallel execution (`--numprocesses=auto`)
- Default test run excludes tests marked with `dev_mode`
- Run `make vtest` to include `dev_mode` tests
- Use `-s` flag to disable output capturing for debugging
- Use `--lf` to re-run only failed tests
- Use `-m dev_mode` to run only dev_mode tests

## Changelog Entries

Changes are managed via towncrier. Create changelog files in `CHANGES/` with format `{issue_number}.{type}.rst`:

- `bugfix` - Bug fixes
- `feature` - New features and behaviors
- `breaking` - Backward incompatible breaking changes
- `deprecation` - Deprecations (removal in next major release)
- `doc` - Documentation improvements
- `packaging` - Packaging updates and notes for downstreams
- `contrib` - Contributor-facing changes (build, CI, tests)
- `misc` - Miscellaneous internal changes

Use `:user:`name`` for author attribution. Example:

```rst
Added new feature X to improve Y -- by :user:`username`.
```

See `CHANGES/.TEMPLATE.rst` for the template.

## Dependencies

**Core dependencies** (defined in `pyproject.toml`):
- multidict - Multi-value dict implementation
- yarl - URL parsing and manipulation
- frozenlist - Immutable list for HTTP/2 support
- aiosignal - Signal handling
- aiohappyeyeballs - Happy Eyeballs algorithm for connection resumption

**Optional speedups** (install with `pip install -e ".[speedups]"`):
- aiodns - Fast DNS resolution
- Brotli - Brotli compression
- backports.zstd - Zstandard compression (Python < 3.14)