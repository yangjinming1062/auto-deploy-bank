# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Building Spark

Spark is built using [Apache Maven](https://maven.apache.org/). The Maven-based build is the build of reference. Building Spark requires:
- Maven 3.9.9+
- Java 17 or 21
- Scala 2.13

### Quick Build
```bash
./build/mvn -DskipTests clean package
```

The `build/mvn` script is a self-contained Maven wrapper that automatically downloads Maven and Scala. It honors existing `mvn` but ensures correct versions.

### Environment Setup
Set `MAVEN_OPTS` for memory-intensive builds:
```bash
export MAVEN_OPTS="-Xss64m -Xmx2g -XX:ReservedCodeCacheSize=1g"
```
If not set, `build/mvn` will automatically add these options.

### Building Specific Profiles
- **YARN**: `-Pyarn -Dhadoop.version=3.4.1`
- **Hive + JDBC**: `-Phive -Phive-thriftserver`
- **Kubernetes**: `-Pkubernetes`
- **All profiles**: `-Pyarn -Phive -Phive-thriftserver -Pkubernetes`

### Building Submodules Individually
```bash
./build/mvn -pl :spark-streaming_2.13 clean install
```

## Running Tests

### All Tests
```bash
./dev/run-tests
```

### Individual Tests by Module
```bash
# Core module
./build/mvn -pl :spark-core_2.13 test

# SQL module
./build/mvn -pl :spark-sql_2.13 test

# Streaming module
./build/mvn -pl :spark-streaming_2.13 test
```

### Running Specific Test Classes
```bash
# Maven format
./build/mvn test -Dtest=org.apache.spark.scheduler.SparkSuite

# PySpark tests
python/python/run-tests --testnames pyspark.sql.test.tests
```

### Python Tests
```bash
# All PySpark tests
python/run-tests

# Specific test module
python/run-tests --testnames pyspark.sql.tests.test_profiler
```

See `dev/run-tests.py` for detailed test selection options including parallel execution and module filtering.

## Code Style & Linting

### Scala/Java
```bash
# Scala style checks
./dev/lint-scala

# Java style checks (via SBT)
./dev/lint-java

# Scala style for specific module
cd core && ../dev/scalastyle
```

### Python
```bash
# All Python checks (compile, black, flake8, mypy, custom errors)
./dev/lint-python

# Reformat Python code
./dev/reformat-python
```

### R
```bash
./dev/lint-r
```

## Creating Distribution
```bash
./dev/make-distribution.sh --name custom-spark --pip --r --tgz -Psparkr -Phive -Phive-thriftserver -Pyarn -Pkubernetes
```

## Architecture Overview

### Project Structure
Apache Spark 4.2.0-SNAPSHOT is a multi-module Maven project organized as follows:

**Core Modules:**
- `core/` - Core Spark engine (RDDs, scheduler, executor, etc.)
- `sql/` - Spark SQL engine
  - `sql/api/` - SQL language API definitions
  - `sql/catalyst/` - Query optimizer and analyzer
  - `sql/core/` - SQL execution engine
  - `sql/hive/` - Hive integration
  - `sql/connect/` - Spark Connect feature
- `streaming/` - Legacy Spark Streaming (DStreams)
- `mllib/` - Machine learning library
- `graphx/` - Graph processing library
- `common/` - Shared utilities
  - `common/unsafe/` - Unsafe memory operations
  - `common/network-common/` - Network transport layer
  - `common/network-shuffle/` - Shuffle data exchange
  - `common/sketch/` - Streaming algorithms
  - `common/kvstore/` - Key-value store
  - `common/utils/` - Common utilities
  - `common/variant/` - Variant type support
- `examples/` - Example applications

**Language Bindings:**
- `python/pyspark/` - Python API for Spark
- `R/` - R language binding (deprecated)

### Key Components

**SQL Engine (sql/):**
The SQL engine has a sophisticated multi-layer architecture:
- **API Layer** (`sql/api/`): Type-safe SQL language APIs and parser definitions
- **Catalyst** (`sql/catalyst/`): Query optimizer with tree-based intermediate representation
  - Analyzer: Resolves names and types
  - Optimizer: Applies optimization rules (e.g., predicate pushdown, constant folding)
  - Planner: Converts logical plans to physical plans
- **Execution Layer** (`sql/core/`): Physical query execution, columnar storage (Parquet, ORC)
- **Connect** (`sql/connect/`): Remote Spark session protocol

**Core Engine (core/):**
- **RDD (Resilient Distributed Dataset)**: Fundamental data abstraction
- **Scheduler**: Task scheduling and execution (DAGScheduler → TaskScheduler)
- **Storage**: Block manager for data storage and shuffling
- **Runtime**: Executor and driver runtime management

**Common Infrastructure (common/):**
- Network layer for shuffle and block transfer
- Unsafe memory management for off-heap operations
- Sketching algorithms (Count-Min Sketch, Bloom filters)
- Distributed key-value store

### Build Profiles

Maven profiles control feature compilation:
- `hive`: Enable Hive metastore integration
- `yarn`: YARN cluster integration
- `kubernetes`: Kubernetes deployment support
- `sparkr`: R package building
- `hadoop-provided`: Exclude Hadoop from assembly (for YARN)
- `jvm-profiler`: JVM profiler support

### Interactive Shells
```bash
# Scala shell
./bin/spark-shell

# Python shell
./bin/pyspark

# Run examples
./bin/run-example SparkPi
```