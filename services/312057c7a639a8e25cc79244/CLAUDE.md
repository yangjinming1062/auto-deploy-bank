# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

urllib3 is a Python HTTP client library with thread-safe connection pooling, file post support, and SSL/TLS verification. It supports Python 3.9+ (CPython and PyPy) including free-threaded builds.

## Commands

### Development Setup
```bash
# Install all dependencies (uses uv for package management)
uv sync --dev --frozen

# Install nox for running test sessions
python -m pip install --user --upgrade nox
```

### Running Tests
```bash
# Run tests for a specific Python version (3.12)
nox -s test-3.12

# Run all test sessions for multiple Python versions
nox -s test

# Run a single test file, class, or method
nox -s test-3.12 -- test/test_connection.py::TestHTTPConnection::test_is_verified

# Run integration tests
nox -s test_integration

# Run with additional pytest arguments after --
nox -s test-3.12 -- -v -k "test_name"
```

### Code Quality
```bash
# Format code (black, isort, pyupgrade)
nox -s format

# Run linting and type checking
nox -s lint

# Run mypy type checking separately
nox -s mypy

# Run pre-commit hooks on all files
pre-commit run --all-files
```

### Documentation
```bash
# Build documentation
nox -s docs
```

### Downstream Testing
```bash
# Test against botocore
nox -s downstream_botocore

# Test against requests
nox -s downstream_requests
```

### Building
```bash
# Build sdist/wheel
python -m build
```

## Architecture

### Core Modules

- **`__init__.py`**: Public API exports (HTTPConnectionPool, PoolManager, ProxyManager, request(), etc.)
- **`_base_connection.py`**: BaseHTTPConnection and BaseHTTPSConnection abstract classes defining the connection interface
- **`connection.py`**: HTTPConnection and HTTPSConnection implementations with socket/SSL handling
- **`connectionpool.py`**: HTTPConnectionPool and HTTPSConnectionPool - manages pools of connections with LIFO queue
- **`poolmanager.py`**: PoolManager and ProxyManager - high-level abstraction that manages multiple connection pools with key-based pooling
- **`response.py`**: HTTPResponse and BaseHTTPResponse - handles response parsing, decompression (gzip, deflate, brotli, zstd), and chunked transfer decoding
- **`_request_methods.py`**: RequestMethods mixin providing request() methods to pools

### Utility Modules (`src/urllib3/util/`)

- **`url.py`**: URL parsing, normalization, and handling (Url class, parse_url())
- **`retry.py`**: Retry logic for retrying failed requests
- **`timeout.py`**: Timeout configuration (Timeout class with total, connect, read, write timeouts)
- **`ssl_.py`**: SSL context creation and certificate verification
- **`ssltransport.py`**: SSL/TLS transport over sockets
- **`connection.py`**: Connection utility functions (is_connection_dropped(), create_connection())
- **`request.py`**: Request header and body utilities
- **`response.py`**: Response utilities (is_fp_closed(), is_response_to_head())
- **`wait.py`**: Wait utilities for async operations

### Data Structures (`src/urllib3/_collections.py`)

- **HTTPHeaderDict**: Case-insensitive HTTP header container with support for duplicate headers
- **RecentlyUsedContainer**: Thread-safe LRU cache with RLock protection and dispose callbacks

### HTTP/2 Support (`src/urllib3/http2/`)

- **`connection.py`**: HTTP/2 connection implementation using h2 library
- **`probe.py`**: HTTP/2 capability detection
- Uses h2 library when available; falls back to HTTP/1.1

### Contrib Modules (`src/urllib3/contrib/`)

- **`pyopenssl.py`**: OpenSSL wrapper integration
- **`socks.py`**: SOCKS proxy support via PySocks
- **`emscripten/`**: Pyodide/Emscripten WebAssembly support

### Testing

- **`test/`**: Unit tests with mocked connections
- **`test/with_dummyserver/`**: Integration tests requiring running dummyserver
- **`dummyserver/`**: Test servers (Quart/Hypercorn-based) for HTTP, HTTPS, and proxy testing

### Key Design Patterns

1. **Connection Pooling**: ConnectionPool uses `queue.LifoQueue` for efficient connection reuse with connection eviction callbacks
2. **PoolKey**: NamedTuple defining unique pool identity based on scheme, host, port, SSL options, timeout, etc.
3. **PoolManager**: Manages a dictionary of connection pools keyed by PoolKey, supports proxy routing
4. **Thread Safety**: RLock used in RecentlyUsedContainer; connection pools use internal locking for thread safety
5. **Decompression Chain**: Response uses ContentDecoder chain (e.g., gzip -> deflate) based on Content-Encoding headers

### Critical Type Aliases

- `_TYPE_BODY`: Union of bytes, str, Iterable, IO, and None for request bodies
- `_TYPE_TIMEOUT`: Union of Timeout object, float, and special sentinel values