# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Reference

**Primary build system**: `make` with `gsctl.py` utility for dependency management

**Python version**: Requires Python >= 3.8

**Key directories**:
- `python/` - Python client library
- `coordinator/` - Coordinator service for launching engines
- `analytical_engine/` - GRAPE-based analytical engine (C++)
- `interactive_engine/` - GIE with Gremlin support (Java + Rust)
- `learning_engine/` - Graph-Learn (GL) for GNNs
- `flex/` - GraphScope Flex (modular graph computing stack)
- `proto/` - Protocol buffer definitions
- `k8s/` - Kubernetes deployment artifacts

## Common Commands

### Setup and Dependencies
```bash
# Install development dependencies
python3 gsctl.py install-deps dev

# In China, use --cn flag for faster downloads
python3 gsctl.py install-deps dev --cn
```

### Building
```bash
# Build all components
make install [INSTALL_PREFIX=/opt/graphscope]

# Build components individually:
make analytical        # Analytical engine (GRAPE)
make interactive       # Interactive engine (GIE)
make learning          # Learning engine (Graph-Learn)
make coordinator       # Coordinator service
make client           # Python client library
make gsctl            # gsctl command-line utility

# Clean build artifacts
make clean
```

### Testing
```bash
# Run full test suite
make test

# Run end-to-end tests locally
python3 gsctl.py test e2e --local

# Run tests on Kubernetes
python3 gsctl.py test e2e --k8s --registry="docker.io" --tag="latest"

# Build and run specific engine tests:
# See docs/analytical_engine/dev_and_test.md
# See docs/interactive_engine/dev_and_test.md
# See docs/learning_engine/dev_and_test.md
```

### Documentation
```bash
# Build documentation
make graphscope-docs

# Open locally
open docs/_build/latest/html/index.html
```

### Code Formatting
```bash
# Format C++ code (Google style)
make graphscope_clformat

# Check C++ style (cpplint)
make graphscope_cpplint

# Python code uses black (automatic in pre-commit)
```

### Building Docker Images
```bash
# Build all images
python3 gsctl.py make-image all

# Build specific component images
python3 gsctl.py make-image analytical
python3 gsctl.py make-image interactive
python3 gsctl.py make-image learning
```

## Architecture Overview

GraphScope is a unified distributed graph computing platform with three engines coordinated by a central service:

### 1. Analytical Engine (`analytical_engine/`)
- Based on **GRAPE** system with PIE (Parallel, Isolated, Exchange) programming model
- C++ implementation (libgrape-lite)
- Supports parallel execution of sequential graph algorithms with minimal code changes
- Built with CMake
- Java SDK available via GraphX runner
- Artifacts: `analytical_engine/build/grape_engine`

**Key directories**:
- `core/` - Core GRAPE implementation
- `apps/` - Built-in graph algorithms
- `java/` - Java PIE SDK

### 2. Interactive Engine (`interactive_engine/`)
- Implements **Gremlin** query language for graph traversal
- Java + Rust hybrid architecture
- Supports distributed Gremlin queries with automatic parallelization
- Built with Maven (Java) and Cargo (Rust)
- Records: LDBC SNB Interactive benchmark leader
- Artifacts: `interactive_engine/assembly/target/graphscope.tar.gz`

**Key components**:
- `executor/` - Query execution engine (JRuntime, Groot)
- `compiler/` - Gremlin query compiler
- `frontend/` - Gremlin endpoint services
- `groot-*` - Graph storage and service components

### 3. Learning Engine (`learning_engine/`)
- **Graph-Learn** (GL) for Graph Neural Networks (GNNs)
- C++ backend with Python bindings via pybind11
- TensorFlow backend for neural network computation
- Built with CMake
- Artifacts: `learning_engine/graph-learn/graphlearn/cmake-build/built/lib/libgraphlearn_shared.so`

**Key directory**:
- `graph-learn/` - Main GL implementation (git submodule)

### 4. Coordinator (`coordinator/`)
- Orchestrates all three engines
- Launches engine pods in Kubernetes clusters
- Manages Vineyard distributed in-memory data store
- Python-based service (gscoordinator package)
- Handles session management and workload scheduling

### 5. Python Client (`python/`)
- User-facing Python API (`import graphscope`)
- Provides unified interface to all engines
- Edges, vertices, and property graph abstractions
- NetworkX compatibility layer
- Artifacts: Python wheel packages

### 6. Flex (`flex/`)
- **GraphScope Flex**: LEGO-like modular graph computing stack
- Modular, user-friendly evolution of GraphScope
- Built with CMake
- Includes:
  - `coordinator/` - Flex coordinator
  - `interactive/` - Interactive services
  - `engines/` - Engine implementations
  - `storages/` - Storage backends

## Development Workflow

### Using Dev Container (Recommended)
```bash
# Use pre-configured dev container with all dependencies
docker run --name dev -it --shm-size=4096m \
  registry.cn-hongkong.aliyuncs.com/graphscope/graphscope-dev:latest
```

VSCode devcontainer config available in `.devcontainer/`

### Development with Local Build
1. Install dependencies: `python3 gsctl.py install-deps dev`
2. Build components: `make install`
3. Run tests: `make test`
4. Format code: `make graphscope_clformat`

## Proto Files and RPC

Protocol buffer definitions in `proto/` define the RPC interface between client and engines:
- `types.proto` - Core data types, OperationType, OutputType
- `coordinator_service.proto` - Coordinator RPC interface
- `engine_service.proto` - Engine RPC interface
- `graph_def.proto` - Graph representation
- `op_def.proto` - Operation definitions
- `message.proto` - Message structures

Generated code lives in:
- `python/graphscope/proto/` - Python bindings
- `coordinator/graphscope_runtime/proto/` - Coordinator runtime
- Engine-specific proto implementations

## Build Artifacts Location

After building, artifacts are located in:
- Analytical engine: `analytical_engine/build/`
- Interactive engine: `interactive_engine/assembly/target/`
- Learning engine: `learning_engine/graph-learn/graphlearn/cmake-build/built/`
- Python client: `python/`
- Coordinator: `coordinator/`
- Default install location: `/opt/graphscope` (configurable via `INSTALL_PREFIX`)

## Key Configuration

- **Build type**: `release` (default) or `debug` via `BUILD_TYPE`
- **NetworkX support**: `ON` (default) via `NETWORKX`
- **Java SDK**: `OFF` (default) via `ENABLE_JAVA_SDK`
- **Tests**: `OFF` (default) via `BUILD_TEST`
- **GraphLearn-Torch**: `ON` (default) via `WITH_GLTORCH`

## Session Workflow (Kubernetes)

For distributed deployment:
1. Client creates session: `sess = graphscope.session(with_dataset=True)`
2. Coordinator launches engine pods with Vineyard instances
3. Load graphs via Vineyard's distributed in-memory store
4. Execute queries/analytics/learning tasks
5. Close session: `sess.close()` (releases k8s resources)

## Important Notes

- **Git submodules**: Learning engine uses `learning_engine/graph-learn` as submodule
- **Vineyard**: Distributed in-memory data store for cross-engine data sharing
- **Pre-commit hooks**: Configured in `.pre-commit-config.yaml`
- **CI**: Uses Cirrus CI (`.cirrus.yml`) and GitHub Actions
- **Code style**: Google C++ style for C++, black for Python
- **Pull requests**: Use `[BUGFIX-1234]` or `[FEATURE-2345]` prefix format

## Useful Resources

- Main docs: https://graphscope.io/docs
- Try online: https://try.graphscope.io
- GraphScope Flex: https://github.com/alibaba/GraphScope/tree/main/flex
- GRAPE: https://github.com/alibaba/libgrape-lite
- Vineyard: https://github.com/v6d-io/v6d
- Graph-Learn: https://github.com/alibaba/graph-learn
- LDBC SNB Interactive benchmark: http://ldbcouncil.org/benchmarks/snb-interactive/