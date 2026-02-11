# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The `cryptography` library is the Python cryptographic standard library. It provides both high-level recipes (Fernet, utils) and low-level primitives (hazmat). The project has a hybrid Python/Rust architecture where:

- **Python** provides the public API and high-level interfaces
- **Rust** implements core cryptographic operations via PyO3 bindings
- **CFFI** provides bindings to OpenSSL C library functions

## Build & Test Commands

```bash
# Install development dependencies
pip install -e ".[test,pep8test,nox,ssh]"

# Run all Python tests
nox -s tests

# Run a specific test file or path
nox -s tests -- tests/x509/test_x509.py

# Run Rust tests
nox -s rust

# Run linting (ruff + mypy + check-sdist)
nox -s flake

# Full local development workflow (format, lint, build, test)
nox -s local

# Build documentation
nox -s docs

# Build in development mode (useful for live debugging)
maturin develop --release --uv
```

## Architecture

### Python Module Hierarchy

```
cryptography/
├── x509/              # X.509 certificate & CSR handling
├── hazmat/            # "Hazardous Materials" - low-level crypto
│   ├── primitives/   # Symmetric ciphers, hashes, HMAC, KDF, asymmetric
│   ├── bindings/     # Rust (_rust) and OpenSSL CFFI bindings
│   ├── decrepit/     # Deprecated/legacy algorithms
│   └── backends/     # Backend selector logic
├── fernet.py          # High-level symmetric encryption
└── utils.py           # Utility functions
```

### Rust Workspace Crates

The `src/rust/` directory contains a Cargo workspace with these crates:

| Crate | Purpose |
|-------|---------|
| `cryptography-rust` | Main library; PyO3 module exports |
| `cryptography-cffi` | CFFI bindings for low-level functions |
| `cryptography-crypto` | Core cryptographic primitives |
| `cryptography-key-parsing` | Private/public key parsing |
| `cryptography-openssl` | OpenSSL integration & FIPS |
| `cryptography-x509` | X.509 certificate handling |
| `cryptography-x509-verification` | Certificate verification policies |

Rust modules expose submodules to Python via PyO3:
- `cryptography.hazmat.bindings._rust` - main Rust module
- `cryptography.hazmat.bindings._rust.openssl` - OpenSSL operations
- `cryptography.hazmat.bindings._rust.x509` - X.509 operations

### Key Integration Points

- **build.rs**: Detects OpenSSL/LibreSSL/BoringSSL/AWS-LC at build time, sets cfg flags
- **OpenSSL version flags**: `CRYPTOGRAPHY_OPENSSL_309_OR_GREATER`, `CRYPTOGRAPHY_OPENSSL_320_OR_GREATER`, etc.
- **Backend flags**: `CRYPTOGRAPHY_IS_LIBRESSL`, `CRYPTOGRAPHY_IS_BORINGSSL`, `CRYPTOGRAPHY_IS_AWSLC`
- **ASN1**: Uses `asn1` Rust crate for DER encoding/decoding

### Test Organization

- `tests/` - Python tests with pytest
- `tests/hazmat/primitives/` - Primitive-specific tests
- `tests/x509/` - X.509 tests
- `tests/wycheproof/` - Wycheproof vector tests
- Rust tests are in `src/rust/**/tests/` and run via `cargo test`

### Adding New Features

1. **Python-only**: Add to appropriate `src/cryptography/` submodule
2. **Rust implementation**: Add to relevant crate in `src/rust/`, expose via `lib.rs` pymodule
3. **New primitives**: May require updates to `src/rust/build.rs` for build-time detection
4. **Test vectors**: Add to `vectors/cryptography_vectors/` directory

## Configuration

- **Ruff**: `pyproject.toml` [tool.ruff] - line-length 79, specific ignore rules
- **Mypy**: `pyproject.toml` [tool.mypy] - strict mode enabled
- **Coverage**: `pyproject.toml` [tool.coverage.run]
- **Pytest**: `pyproject.toml` [tool.pytest.ini_options]
