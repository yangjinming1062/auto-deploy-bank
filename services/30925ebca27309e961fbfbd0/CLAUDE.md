# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Apache Doris is a distributed analytical database based on MPP (Massively Parallel Processing) architecture. It features a storage-compute integrated design with:
- **Frontend (FE)**: Java service handling query coordination, metadata management, and node management
- **Backend (BE)**: C++ service handling data storage and query execution
- **Cloud Mode**: Optional cloud-based deployment
- **Broker**: Java service for reading external storage data (HDFS, etc.)

## Repository Structure

```
.
├── be/                      # Backend (C++) - storage and query execution
│   ├── src/
│   │   ├── olap/           # Storage engine (columnar storage, tablet management)
│   │   ├── runtime/        # Runtime execution (query fragments, exchange nodes)
│   │   ├── pipeline/       # Pipeline execution engine
│   │   ├── io/             # IO operations (file readers, buffered readers)
│   │   ├── exprs/          # Expression evaluation
│   │   └── service/        # RPC service implementation
│   └── test/               # C++ unit tests (GTest)
│
├── fe/                      # Frontend (Java) - query planning and metadata
│   ├── fe-core/src/main/java/org/apache/doris/
│   │   ├── analysis/       # SQL parsing and analysis
│   │   ├── planner/        # Query planning and optimization (CBO/RBO/HBO)
│   │   ├── catalog/        # Metadata catalog management
│   │   ├── datasource/     # External data source management
│   │   ├── nereids/        # New optimizer engine
│   │   └── service/        # Frontend RPC service
│   └── fe-core/src/test/java/  # Java unit tests (JUnit)
│
├── gensrc/                  # Generated code from Proto/Thrift
│   ├── proto/              # Protocol buffer definitions
│   ├── thrift/             # Thrift service definitions
│   └── script/             # Generation scripts
│
├── thirdparty/             # Third-party dependencies
├── extension/              # Doris connectors (Flink, Spark, etc.)
├── docker/                 # Docker deployment files
├── tools/                  # Utilities (benchmarking, testing tools)
├── samples/                # Sample applications
├── ui/                     # Web UI (React/JavaScript)
└── webroot/                # Static web resources
```

## Common Development Commands

### Building

```bash
# Build all components (FE, BE, Broker, etc.)
./build.sh

# Build specific components
./build.sh --fe              # Frontend only
./build.sh --be              # Backend only
./build.sh --fe --be         # Both FE and BE
./build.sh --clean           # Clean and rebuild

# Build with custom options
USE_AVX2=0 ./build.sh --be    # Build BE without AVX2 instruction set
STRIP_DEBUG_INFO=ON ./build.sh --be  # Strip debug info for smaller binaries
-j 8 ./build.sh --be         # Parallel build with 8 jobs

# Build additional tools
./build.sh --meta-tool                 # Backend metadata tool
./build.sh --index-tool                # Inverted index tool
./build.sh --file-cache-microbench     # File cache microbenchmark
./build.sh --benchmark                 # Google Benchmark
./build.sh --cloud                     # Cloud mode
```

**Note**: Before building, ensure third-party dependencies are installed in `thirdparty/` directory. Use Docker-based compilation for consistent builds.

### Testing

```bash
# Backend unit tests (C++/GTest)
./run-be-ut.sh --run                     # Build and run all BE tests
./run-be-ut.sh --run --filter=TestName   # Run specific test
./run-be-ut.sh --clean                   # Clean and rebuild tests
./run-be-ut.sh --gdb                     # Debug with GDB
./run-be-ut.sh --coverage                # Generate coverage report
-j 8 ./run-be-ut.sh --run                # Parallel build for tests

# Frontend unit tests (Java/JUnit)
./run-fe-ut.sh --run                     # Build and run all FE tests
./run-fe-ut.sh --run org.apache.doris.utframe.Demo  # Run specific test class
./run-fe-ut.sh --run Demo#testMethod    # Run specific test method
./run-fe-ut.sh --coverage                # Generate coverage report

# Integration/Regression tests (Python)
./run-regression-test.sh --run           # Run all regression tests
./run-regression-test.sh -s suite_name   # Run specific test suite
./run-regression-test.sh -g group_name   # Run tests in specific group
./run-regression-test.sh -d test_dir     # Run tests in directory
./run-regression-test.sh -parallel 8     # Run with 8 threads

# Cloud tests
./run-cloud-ut.sh --run                  # Build and run cloud tests
```

**Note**: Backend tests must use `_test` suffix and be added to `be/test/CMakeLists.txt`. Test results are in `be/ut_build_ASAN/gtest_output/` for BE tests.

### Code Quality Checks

```bash
# Java code style (checkstyle)
cd fe && mvn clean checkstyle:check

# C++ code formatting (clang-format)
# Uses clang-format-16, configured via .clang-format
# Automated via GitHub Actions

# Shell script linting (shellcheck)
# Automated via GitHub Actions workflow
```

**Note**: Checkstyle config is in `fe/` directory. Clang-format config is in `.clang-format` at repo root. All checks run automatically in CI for PRs.

### Generate Code

```bash
# Generate Thrift/Proto files
cd gensrc && make clean && make all

# Or from root
make -C gensrc clean
make -C gensrc
```

## Development Workflow

### Setting Up Development Environment

1. **Install dependencies**:
   - For FE: Maven 3.x, Java 17
   - For BE: CMake 3.19+, C++17 compiler (GCC/Clang), Make/Ninja
   - Third-party libraries: Install via `thirdparty/install_*` scripts or use Docker

2. **Environment setup**:
   ```bash
   # Source environment
   source env.sh

   # On macOS, setup automatic via Homebrew
   # See env.sh lines 40-97 for macOS-specific configuration
   ```

### Making Changes

1. **Build affected components**: After modifying proto/thrift, rebuild gensrc, then FE/BE
2. **Run relevant tests**: Unit tests for changed component + regression tests
3. **Check code style**: Run checkstyle for Java changes, clang-format for C++ changes
4. **Rebuild cleanly**: Use `--clean` flag before final build

### Key Technical Areas

**Storage Engine (be/src/olap/)**:
- Columnar storage with encoding/compression
- Tablet management and compaction
- Multiple storage models: Aggregate, Unique, Duplicate, Primary Key
- Indexing: Bloom Filter, Inverted Index, Min/Max, Sorted Compound

**Query Execution (be/src/runtime/, be/src/pipeline/)**:
- MPP distributed execution
- Vectorized execution engine
- Pipeline execution model
- Runtime filter pushdown

**Query Planning (fe/fe-core/src/main/java/org/apache/doris/planner/)**:
- CBO (Cost-Based Optimizer)
- RBO (Rule-Based Optimizer)
- HBO (History-Based Optimizer)
- Distributed query planning

**Metadata Management (fe/fe-core/src/main/java/org/apache/doris/catalog/)**:
- Database/Table metadata
- Partition management
- Resource management

## Useful File Locations

**Build and Config**:
- `env.sh` - Environment setup and dependencies
- `build.sh` - Main build script
- `thirdparty/` - Third-party libraries

**Source Code**:
- `be/src/olap/olap_data.h` - Main storage engine header
- `be/src/runtime/exec_env.h` - Backend execution environment
- `fe/fe-core/src/main/java/org/apache/doris/planner/Planner.java` - Main query planner
- `fe/fe-core/src/main/java/org/apache/doris/catalog/Catalog.java` - Metadata catalog

**Test Files**:
- `be/test/olap/` - Storage engine tests
- `fe/fe-core/src/test/java/org/apache/doris/utframe/` - Frontend unit tests
- `pytest/` - Integration tests

**Generated Files**:
- `gensrc/proto/*.pb.*` - Protocol buffer generated code
- `gensrc/thrift/*.cpp` - Thrift generated C++ code

## CI/CD

**Automated Checks** (see `.github/workflows/`):
- Code checks (shellcheck, clang-format, checkstyle)
- Build and test workflows
- Coverage reports
- Regression tests

**PR Requirements**:
- Pass all unit tests (FE and BE)
- Pass regression tests
- Pass code style checks
- Maintain test coverage

## Architecture Highlights

**MPP Architecture**: Queries are distributed across BE nodes with exchange nodes shuffling data between fragments.

**Columnar Storage**: Data stored by columns for better compression and vectorized scan performance.

**Vectorized Execution**: All operators use SIMD instructions for better CPU utilization (5-10x speedup).

**Pipeline Execution**: Breaks queries into pipeline stages to avoid thread explosion and improve CPU utilization.

**Materialized Views**: Supports both strongly-consistent single-table MVs and asynchronously refreshed multi-table MVs.

**External Data Sources**: Unified query across Hive, Iceberg, Hudi, MySQL, Elasticsearch via external catalogs.

## Dependencies

**Build Requirements**:
- Java 17+ (Maven 3.x)
- CMake 3.19+ (Ninja recommended)
- C++17 compiler (GCC 10+ or Clang 10+)
- Python 3.x (for regression tests)
- Thrift, Protocol Buffers

**Third-Party Libraries** (see `thirdparty/`):
- Apache Arrow
- Apache Iceberg/Hudi
- Google Benchmark
- OpenTelemetry
- And many others (see `thirdparty/install_*` scripts)

## Additional Resources

- **Documentation**: https://doris.apache.org/docs/
- **Developer Guide**: See `docs/` directory
- **Contributing Guide**: `CONTRIBUTING.md`
- **Mailing List**: dev@doris.apache.org
- **Issue Tracking**: GitHub Issues