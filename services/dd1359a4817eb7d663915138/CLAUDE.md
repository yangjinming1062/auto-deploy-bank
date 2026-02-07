# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Apache Amoro is a Lakehouse management system built on open data lake formats. It provides self-optimizing, catalog services, and supports multiple table formats (Iceberg, Mixed-Iceberg, Mixed-Hive, Paimon, Hudi) and compute engines (Flink, Spark, Hive, Trino).

## Build Commands

```bash
# Full build
./mvnw clean package

# Build and skip tests
./mvnw clean package -DskipTests

# Build and skip frontend dashboard
./mvnw clean package -Pskip-dashboard-build

# Build with Hadoop 2.x (default is 3.x)
./mvnw clean package -DskipTests -Phadoop2

# Build with specific Flink version
./mvnw clean package -DskipTests -Dflink-optimizer.flink-version=1.20.0

# Build with specific Spark version
./mvnw clean package -DskipTests -Dspark.version=3.5.7

# Build Trino module (requires JDK 17)
./mvnw clean package -DskipTests -Pformat-mixed-format-trino,build-mixed-format-trino -pl 'amoro-format-mixed/amoro-mixed-trino' -am

# Run a single test
./mvnw test -pl <module> -Dtest=<TestClass>#<method>

# Format code (Spotless + google-java-format for Java, scalafmt for Scala)
./dev/reformat
```

**Requirements:**
- Java 11+ (required for most modules; JDK 17 required for Trino module)
- Maven wrapper included (./mvnw)

## Module Structure

| Module | Purpose |
|--------|---------|
| `amoro-common` | Core abstractions (catalog, table, client APIs) used by all modules |
| `amoro-ams` | Amoro Management Service - core server with optimizing, catalog, dashboard |
| `amoro-web` | Frontend dashboard (Vue.js, served by AMS on port 1630) |
| `amoro-optimizer` | Optimizer implementations: standalone, Flink, Spark |
| `amoro-format-iceberg` | Apache Iceberg format integration |
| `amoro-format-hudi` | Apache Hudi format integration |
| `amoro-format-paimon` | Apache Paimon format integration |
| `amoro-format-mixed` | Mixed format implementation with connectors for Flink, Spark, Hive, Trino |
| `amoro-metrics` | Metrics system (Prometheus integration) |

## Architecture

### AMS (Amoro Management Service)
Main components under `amoro-ams/src/main/java/org/apache/amoro/server/`:
- **`optimizing/`**: Self-optimizing service that handles table compaction, deduplication
- **`catalog/`**: Catalog management service
- **`dashboard/`**: REST API endpoints and Web UI controllers
- **`scheduler/`**: Job scheduling for optimizers
- **`table/`**: Table metadata and runtime management
- **`persistence/`**: Database layer (MySQL, PostgreSQL, Derby)
- **`terminal/`**: SQL CLI tools (Spark, Kyuubi)
- **`resource/`**: Container and resource management
- **`ha/`**: High availability support

### Table Formats
- **Iceberg**: Direct integration using Iceberg's engine-agnostic APIs
- **Mixed-Iceberg**: Enhanced format with optimized streaming updates and CDC
- **Mixed-Hive**: Upgrades Hive tables to lakehouse format while maintaining Hive compatibility
- **Paimon**: Metadata viewing and management
- **Hudi**: Integration for Hudi format tables

### Engine Connectors (amoro-format-mixed)
- `amoro-mixed-flink`: Flink connectors for Mixed format tables
- `amoro-mixed-spark`: Spark connectors for Mixed format tables
- `amoro-mixed-hive`: Hive table format support
- `amoro-mixed-trino`: Trino connector (JDK 17 required)

### Optimizers
Run as separate processes to asynchronously perform:
- Compaction of small files
- Sorting and deduplication
- Layout optimization
- Data expiration

Types: Standalone, Flink-based, Spark-based

## Key Dependencies (Shaded)

Amoro shades certain dependencies to avoid conflicts:
- `amoro-shade-guava-32`: Guava 32.1.1
- `amoro-shade-jackson-2`: Jackson 2.14.2
- `amoro-shade-zookeeper-3`: ZooKeeper 3.9.1
- `amoro-shade-thrift`: Thrift 0.20.0

Use shaded packages (e.g., `org.apache.amoro.shade.com.google.common`) when adding new dependencies that transitively pull in these libraries.

## Code Conventions

- **License headers**: All source files must include Apache License 2.0 header
- **Formatting**: Spotless with google-java-format for Java, scalafmt for Scala
- **Checkstyle**: Enforced at `tools/maven/checkstyle.xml`
- **Tests**: JUnit 4/5, Mockito for mocking
- **Logging**: SLF4J with Log4j2 implementation

## Database Configuration

AMS supports MySQL, PostgreSQL, and Derby. Default configuration uses Derby for local development. Config file location: `conf/config.yaml` (copy from `dist/src/main/amoro-bin/conf/config.yaml`).

## Starting Services

1. **Start AMS**: Run `AmoroServiceContainer` class in `amoro-ams` module (default port 1630)
2. **Start Optimizer**: Run `StandaloneOptimizer` with args `-a thrift://127.0.0.1:1261 -p 1 -g local`

## Contribution Notes

- PR title format: `[AMORO-{issue_number}][{module}] description`
- Link PR to issue with `fix/resolve #{issue_number}`
- Run `./dev/reformat` before committing
- Update config docs if modifying `ConfigOptions`: `UPDATE=1 ./mvnw test -pl amoro-ams -Dtest=ConfigurationsTest`