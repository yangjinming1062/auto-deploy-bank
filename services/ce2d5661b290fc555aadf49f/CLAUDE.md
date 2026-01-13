# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Apache Doris is a distributed SQL database with MPP (Massively Parallel Processing) architecture. It consists of two main components:
- **Frontend (FE)** - Java-based query coordinator and metadata manager
- **Backend (BE)** - C++ data storage and query execution engine

## Building

### Full Build
```bash
./build.sh
```

### Build Specific Components
```bash
# Build only Backend (C++)
./build.sh --be

# Build only Frontend (Java)
./build.sh --fe

# Build with clean
./build.sh --clean

# Build specific components
./build.sh --be --fe --broker --hive-udf --be-java-extensions
```

### Environment Variables for Build
- `USE_AVX2=0` - Disable AVX2 instruction set for older CPUs
- `ARM_MARCH=armv8-a+crc` - Specify ARM architecture (default: armv8-a+crc)
- `STRIP_DEBUG_INFO=ON` - Store debug info separately in `be/lib/debug_info`
- `DISABLE_BE_JAVA_EXTENSIONS=ON` - Skip Java UDF and scanner builds
- `DISABLE_JAVA_CHECK_STYLE=ON` - Skip Java style checks
- `DISABLE_BUILD_AZURE=ON` - Exclude Azure support from BE

### Thirdparty Libraries
Thirdparty libraries must be compiled first:
```bash
cd thirdparty
./build-thirdparty.sh
```

## Testing

### Backend Unit Tests (C++)
```bash
# Build and run all BE unit tests
./run-be-ut.sh --run

# Run specific test with filter
./run-be-ut.sh --run --filter=*TestSuiteName*
./run-be-ut.sh --run --filter=*TestClassName*
./run-be-ut.sh --run --filter=*TestMethodName*

# Build tests without running
./run-be-ut.sh

# Clean and rebuild tests
./run-be-ut.sh --clean

# Run with coverage
./run-be-ut.sh --clean --run --coverage
```

### Frontend Unit Tests (Java)
```bash
# Build and run all FE unit tests
./run-fe-ut.sh --run

# Run specific test class
./run-fe-ut.sh --run org.apache.doris.utframe.DemoTest

# Run specific test method
./run-fe-ut.sh --run org.apache.doris.utframe.DemoTest#testCreateDbAndTable+test2

# Run with coverage
./run-fe-ut.sh --run --coverage
```

### Regression Tests
```bash
# Build and run all regression tests
./run-regression-test.sh --run

# Run specific test suite
./run-regression-test.sh --run -s test_select

# Run tests by group
./run-regression-test.sh --run -g default

# Run tests by directory
./run-regression-test.sh --run -d demo,correctness/tmp

# Generate output files
./run-regression-test.sh --run -genOut

# Clean output before running
./run-regression-test.sh --clean --run test_select
```

## Project Structure

### Major Components
- **`be/`** - Backend (C++) source code
  - `src/` - C++ source files
  - `test/` - C++ unit tests
  - `benchmark/` - Performance benchmarks

- **`fe/`** - Frontend (Java) source code
  - `fe-core/src/main/java/` - Main Java source
  - `fe-core/src/test/java/` - Java unit tests
  - `fe-common/` - Common utilities
  - `be-java-extensions/` - Java extensions for BE

- **`gensrc/`** - Generated protocol and thrift files
  - `proto/` - Protocol buffer definitions
  - `thrift/` - Thrift service definitions
  - `script/` - Build scripts

- **`thirdparty/`** - External dependencies
- **`extension/`** - Third-party integrations (Spark, Flink, etc.)
- **`tools/`** - Utility tools for testing and deployment
- **`samples/`** - Example applications and demos

### Key Backend (C++) Subsystems
- **`be/src/olap/`** - Storage engine, tablet management, compaction
- **`be/src/vec/`** - Vectorized execution engine
- **`be/src/pipeline/`** - Pipeline execution framework
- **`be/src/runtime/`** - Query execution, memory management, load tasks
- **`be/src/service/`** - Network services, protocol handling
- **`be/src/io/`** - Storage I/O, file system abstraction
- **`be/src/exprs/`** - Expression evaluation framework
- **`be/src/udf/`** - User-defined function support

### Key Frontend (Java) Subsystems
- **`org.apache.doris/nereids/`** - New query optimizer and planner
- **`org.apache.doris/catalog/`** - Metadata and catalog management
- **`org.apache.doris/planner/`** - Query planning and optimization
- **`org.apache.doris/analysis/`** - SQL parsing and analysis
- **`org.apache/doris/load/`** - Data loading infrastructure
- **`org.apache/doris/mysql/`** - MySQL protocol implementation
- **`org.apache/doris/httpv2/`** - HTTP API endpoints
- **`org/apache/doris/common/`** - Shared utilities and helpers

## Development Workflow

### Code Generation
Generate protocol and thrift files before building:
```bash
./generated-source.sh
```

### Configuration
- **`conf/be.conf`** - Backend configuration
- **`conf/fe.conf`** - Frontend configuration
- **`env.sh`** - Build environment setup

### Key Build Files
- **`be/CMakeLists.txt`** - C++ build configuration
- **`fe/pom.xml`** - Maven build configuration
- **`gensrc/Makefile`** - Code generation build

### Code Style
- Backend C++: Follow [Backend C++ Coding Specification](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=240883637)
- Backend C++ uses `.clang-format` and `.clang-tidy` for formatting
- Frontend Java uses Maven Checkstyle plugin

## Working with Submodules

Some third-party dependencies are managed as submodules:
```bash
git submodule update --init --recursive
```

If submodule update fails, the build scripts will automatically download and extract the required dependencies.

## Common Development Tasks

### Running Individual Test Files
**BE (C++):**
```bash
# After building tests
cd be/ut_build_ASAN/test
./doris_be_test --gtest_filter=TestSuiteName.TestMethodName
```

**FE (Java):**
```bash
cd fe
mvn test -Dtest=TestClassName -Dcheckstyle.skip=true
```

### Debugging BE Tests
BE tests use AddressSanitizer (ASAN) by default. GTest XML output is written to `be/ut_build_ASAN/gtest_output/`.

### Building with Custom Flags
```bash
# Build BE with custom compiler flags
EXTRA_CXX_FLAGS="-DDEBUG" USE_AVX2=0 ./build.sh --be

# Build FE with specific Maven options
cd fe && mvn clean install -DskipTests -Dmaven.test.failure.ignore=false
```

## Environment Setup

### Prerequisites
- JDK 8 or 11 (JAVA_HOME required)
- Maven 3.6+
- CMake 3.19+
- C++ compiler (GCC 9+ or Clang 12+)
- Python 3 (for regression tests)
- Node.js (for UI components)

### Initial Setup
```bash
source env.sh
# On macOS: source custom_env.sh (created automatically)
```

## Important Notes

1. **Three-tier Architecture**: Doris uses FE (coordinator) + BE (storage/compute) architecture. Both are horizontally scalable.

2. **Metadata Management**: FE nodes maintain full metadata copies. Three FE roles: Master (writes), Follower (read/replication), Observer (read-only query).

3. **Storage**: BE uses columnar storage with multiple data models (Duplicate/Unique/Aggregate) and various indexes (MinMax, BloomFilter, Inverted).

4. **Query Engine**: Vectorized MPP execution engine with CBO/RBO/HBO optimizers and Pipeline execution model.

5. **External Connectors**: Integrations available for Spark (spark-doris-connector), Flink (flink-doris-connector), and other ecosystem tools.

6. **Testing Strategy**: Three-tier testing - unit tests (BE C++ / FE Java) → regression tests (Python framework) → integration tests (deployment environments).

## Documentation and Resources

- **Official Website**: https://doris.apache.org/
- **Documentation**: https://doris.apache.org/docs/
- **GitHub Issues**: https://github.com/apache/doris/issues
- **Developer Mailing List**: dev@doris.apache.org
- **Community Slack**: Invitation link in README.md