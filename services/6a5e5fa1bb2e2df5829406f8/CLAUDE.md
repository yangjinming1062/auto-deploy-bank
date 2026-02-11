# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **pyca/cryptography** library - a major Python cryptography library providing cryptographic recipes and primitives. It uses a hybrid Python/Rust architecture:

- **Python** (`src/cryptography/`) - Public API, hazmat primitives, high-level interfaces
- **Rust** (`src/rust/`) - Performance-critical code via PyO3 bindings
- **CFFI** (`src/_cffi_src/`) - Bindings to OpenSSL C library

## Common Commands

### Development Setup
```bash
# Install development environment (lint, type check, build, test)
nox -e local

# Install package in editable mode for C binding development
pip install -e .
```

### Running Tests
```bash
# Run all Python tests with coverage
nox -e tests

# Run specific test file
nox -e tests -- tests/x509/test_certificate.py

# Run specific test class
nox -e tests -- tests/test_fernet.py::TestFernet

# Run specific test method
nox -e tests -- tests/test_fernet.py::TestFernet::test_init

# Run Rust tests
nox -e rust

# Run tests in random order
nox -e tests-randomorder

# Build in debug mode (faster builds, slower tests)
nox -e tests-rust-debug
```

### Linting and Type Checking
```bash
# Run all linting (ruff, mypy, check-sdist)
nox -e flake

# Run just ruff
ruff check
ruff format --check

# Run mypy
mypy src/cryptography/ tests/ noxfile.py
```

### Documentation
```bash
# Build docs (requires libenchant)
nox -e docs

# Link check
nox -e docs-linkcheck
```

## Architecture

### Python/Rust Integration Pattern

Most cryptographic primitives follow this pattern:

**Python side** (`src/cryptography/hazmat/primitives/hashes.py`):
- Defines abstract base classes (`HashAlgorithm`, `HashContext`)
- Algorithm parameter classes (`SHA256`, `BLAKE2b`, etc.)
- Imports implementation from `cryptography.hazmat.bindings._rust.openssl`
- Registers Rust classes as implementations of ABCs

```python
from cryptography.hazmat.bindings._rust import openssl as rust_openssl

class HashContext(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, data: Buffer) -> None: ...

Hash = rust_openssl.hashes.Hash
HashContext.register(Hash)
```

**Rust side** (`src/rust/src/backend/hashes.rs`):
- Implements `#[pyclass]` structs with `#[pymethods]`
- Uses PyO3 to expose as Python classes
- Wraps OpenSSL operations via the `openssl` Rust crate

```rust
#[pyo3::pyclass(module = "cryptography.hazmat.bindings._rust.openssl.hashes")]
pub(crate) struct Hash { ... }

#[pyo3::pymethods]
impl Hash {
    #[new]
    pub(crate) fn new(...) -> CryptographyResult<Hash> { ... }
}
```

### Key Python Modules
- `cryptography/` - Public API
  - `fernet.py` - High-level symmetric encryption (Fernet)
  - `utils.py` - Utility functions
  - `exceptions.py` - Exception classes
- `cryptography/hazmat/` - Cryptographic primitives (the "hazardous materials" layer)
  - `primitives/` - Low-level primitives (ciphers, hashes, KDFs, asymmetric crypto)
  - `bindings/` - CFFI and Rust bindings (`_rust/` for PyO3, `openssl/` for CFFI)
  - `backends/` - Backend support (OpenSSL)
  - `decrepit/` - Deprecated/legacy ciphers (3DES, RC4, etc.)

### Rust Crates (Cargo workspace)
- `cryptography-rust` - Main crate, exports PyO3 modules (src/rust/src/lib.rs)
  - `src/backend/` - OpenSSL operations (aead, ciphers, hashes, hmac, kdf, keys, rsa, ec, etc.)
  - `src/x509/` - X.509 certificate parsing and verification
- `cryptography-cffi` - FFI helpers for Rust/OpenSSL interop
- `cryptography-crypto` - Core crypto primitives (AEAD, hashes, MACs, ciphers)
- `cryptography-key-parsing` - Private key parsing (PEM/DER)
- `cryptography-openssl` - OpenSSL wrapper types
- `cryptography-x509` - X.509 certificate handling
- `cryptography-x509-verification` - Certificate verification policy

### CFFI Bindings
Bindings to OpenSSL live in `src/_cffi_src/openssl/`. When modifying these:
1. Recompile with `pip install -e .` or `nox -e local` to test changes
2. Use `CONDITIONAL_NAMES` in `_conditional.py` for version-gated features
3. Follow C style guidelines (no parameter names, C-style comments, 80-char lines)
4. Define `Cryptography_HAS_*` constants for feature detection

### Build System
- **Build backend**: `maturin` (for Rust/Python interop)
- **Python dependencies**: Managed via `pyproject.toml`
- **Rust MSRV**: 1.83.0
- **Python version**: 3.8+ (excluding 3.9.0, 3.9.1)

### Test Configuration
- Tests use `pytest` with `pytest-xdist` for parallel execution
- Coverage tracking for both Python (`coverage.py`) and Rust (`llvm-cov`)
- Backend fixture in `conftest.py` provides OpenSSL backend for tests
- Tests verify error stack is clear before and after each test

## Adding New Features

1. **Python-only additions**: Add to the appropriate module in `src/cryptography/`
2. **Rust implementations**: Add to the relevant module in `src/rust/src/backend/` and export from `lib.rs`
3. **New OpenSSL functions**: Add to CFFI bindings in `src/_cffi_src/openssl/` with conditional compilation
4. **New algorithms**: Typically require implementations in both Python (algorithm params) and Rust (backend operations)