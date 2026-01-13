# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Chroma is an open-source embedding database (vector database) written in Python, Rust, and Go. The core engine is in Rust with Python and JavaScript clients. The distributed system includes multiple services communicating via protocol buffers.

**Core Technologies:**
- **Rust**: Core distributed system (worker, frontend, query-service, sysdb, etc.)
- **Python**: Client API, server mode, tests (`chromadb/`)
- **Go**: System Database coordinator (`go/`)
- **Protocol Buffers**: Service communication (`idl/`)

## Common Development Commands

### Python (Client & Server)

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_dev.txt
pip install -e .  # Install in editable mode
pre-commit install

# Build Rust bindings
maturin dev

# Run tests
pytest chromadb/test/
pytest chromadb/test/test_api.py::test_name -v  # Run specific test
python -m pytest chromadb/test/property/ -n auto  # Run property tests in parallel

# Build distribution
python -m build

# Linting/Formatting
black chromadb/
flake8 chromadb/
mypy chromadb/
pre-commit run --all-files  # Run all pre-commit hooks
```

### Go (SysDB Coordinator)

```bash
cd go/

# Generate protobuf
make proto

# Build
make build

# Test (must run sequentially due to flaky parallel tests)
make test

# Lint
make lint

# Clean
make clean
```

### Rust (Core Services)

```bash
# Test entire workspace
cargo test

# Test specific crate
cargo test -p chroma-worker
cargo test -p chroma-frontend

# Build specific service
cargo build -p chroma-worker
cargo build -p chroma-query-service

# Run benchmarks
cargo bench -p chroma-worker

# Lint
cargo clippy
```

### Distributed Development (Kubernetes)

Requires Docker, local Kubernetes cluster ([OrbStack](https://orbstack.dev/) for Mac, [Kind](https://kind.sigs.k8s.io/) for Linux), [Tilt](https://docs.tilt.dev/), and [Helm](https://helm.sh).

```bash
# Start distributed cluster (exposes Chroma on port 8000)
tilt up

# View Tilt dashboard
open http://localhost:10350/

# Clean up
tilt down

# Development workflow
# Changes to Rust files automatically rebuild and deploy when tilt up is running
```

### Protocol Buffers

```bash
# Generate Python gRPC code
cd idl/
make proto_python

# Generate Go gRPC code
make proto_go

# Note: These files are generated - don't edit directly
# Python files go to chromadb/proto/
# Go files go to go/pkg/proto/
```

## High-Level Architecture

### Service Architecture

The distributed system consists of multiple services managed by Kubernetes and Tilt:

1. **query-service** (Rust): Handles vector queries and retrievals
2. **sysdb** (Go): System Database coordinator managing metadata
3. **log-service** (Rust): Handles write-ahead logging
4. **frontend-service** (Rust): HTTP/gRPC frontend API
5. **postgres**: Metadata persistence
6. **worker** (Rust): Background processing tasks

All services communicate via Protocol Buffers defined in `idl/chromadb/proto/`:
- `chroma.proto`: Core data types
- `coordinator.proto`: SysDB coordination
- `logservice.proto`: Logging service API
- `query_executor.proto`: Query execution
- `heapservice.proto`: Storage heap service

### Core Components

**Rust Crates (in `rust/`):**
- `chroma/`: Python client library for distributed mode
- `worker/`: Background task processing
- `frontend/`: HTTP/gRPC API server
- `sysdb/`: System database abstractions
- `segment/`: Vector segment storage
- `index/`: Vector indexing (HNSW, IVF, etc.)
- `blockstore/`: Persistent key-value storage
- `storage/`: Object storage abstractions (S3, etc.)
- `memberlist/`: Cluster membership management
- `python_bindings/`: PyO3 bindings

**Python (in `chromadb/`):**
- `api/`: Public API
- `server/`: Single-node server mode
- `db/`: Database implementations
- `segment/`: Segment management
- `test/`: Test suite (property, stress, distributed)

**Go (in `go/`):**
- `pkg/sysdb/coordinator/`: SysDB coordinator implementation
- `pkg/memberlist_manager/`: Cluster membership
- `pkg/proto/`: Generated protobuf code

### Data Model

- **Tenants** → **Databases** → **Collections** → **Segments**
- Collections contain embeddings with metadata
- Segments store data in different formats (vector, metadata, document)
- Multi-tenant support with tenant/database hierarchy

### Persistence

- **Metadata**: PostgreSQL via SysDB coordinator
- **Embeddings**: Distributed across worker nodes
- **WAL**: Write-ahead logging via log-service
- **Object Storage**: S3 for large embeddings (s3heap crate)

## Development Notes

### Version Management

The project uses `setuptools_scm` for automatic versioning from Git tags:
- Tagged commits: exact version (e.g., `0.0.1`)
- Untagged commits: patch increment + `devN` (e.g., `0.0.2-dev5`)
- Unclean working tree: `+dirty` suffix

Check version: `python -m setuptools_scm`

### Testing Strategy

1. **Unit Tests**: `pytest` for Python, `cargo test` for Rust, `make test` for Go
2. **Property Tests**: `chromadb/test/property/` - stateful testing
3. **Integration Tests**: `chromadb/test/distributed/` - distributed system tests
4. **Stress Tests**: `chromadb/test/stress/` - performance testing

**Running Tests:**
- **Python**: `pytest chromadb/test/test_api.py -v`
- **Rust**: `cargo test -p chroma-worker`
- **Go**: `make test` (sequentially)
- **All CI**: GitHub Actions workflows in `.github/workflows/`

### Code Quality

**Pre-commit hooks** (`.pre-commit-config.yaml`):
- Black (Python formatting)
- Flake8 (linting)
- MyPy (type checking)
- Prettier (JavaScript)

**Linting Tools:**
- Rust: `cargo clippy`
- Python: `flake8`, `mypy`
- Go: `golangci-lint`

### IDE Setup

- **VSCode/Cursor**: Install `rust-analyzer` extension for Rust development
- **CodeLLDB**: For Rust debugging
- Python development: Standard Python extensions

### Key Configuration Files

- `pyproject.toml`: Python project configuration, dependencies, and tools
- `Cargo.toml`: Rust workspace configuration
- `Tiltfile`: Local Kubernetes development setup
- `docker-compose*.yml`: Docker development environments
- `.github/workflows/`: CI/CD pipelines

### Release Process

1. Update version in `chromadb/__init__.py` (format: `__version__ = "A.B.C"`)
2. Create PR with `[RELEASE] A.B.C` title
3. Add "release" label to PR
4. Merge after checks pass
5. Tag commit: `git tag A.B.C <SHA>` and push: `git push origin A.B.C`
6. GitHub Actions releases to PyPI, DockerHub, and JS client

### Debugging Distributed Chroma

Set breakpoints in Kubernetes pods:
```bash
# Access query-service pod
kubectl exec -it query-service-0 -n chroma -- /bin/sh

# Install debugger
apt-get update && apt-get install gdb

# Set breakpoint
gdb
(gdb) b <relative_file_path>:<lineno>
```

### Testing with Tilt

**Important**: Keep `tilt up` running for distributed tests or they will fail. Tilt auto-rebuilds Rust code on changes.

## Important Notes

- Generated protobuf files should NOT be edited directly
- Pre-commit hooks must pass before committing
- Python and Rust tests are required in CI
- Version numbers are auto-generated from Git
- All distributed system development requires Kubernetes cluster
- Property tests in `chromadb/test/property/` test stateful systems and may take longer