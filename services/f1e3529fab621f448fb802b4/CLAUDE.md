# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Addax** is a versatile open-source ETL (Extract, Transform, Load) tool written in Java, supporting 50+ SQL/NoSQL data sources through a plugin-based architecture. It's a fork and evolution of Alibaba's DataX with improved architecture and active maintenance.

- **Type**: Java 17 ETL platform
- **Build System**: Maven (multi-module with 75 modules)
- **Architecture**: Plugin-based modular design
- **License**: Apache 2.0
- **Current Version**: 6.0.8-SNAPSHOT

## Common Commands

### Building the Project

```bash
# Full build with all modules
mvn clean package

# Distribution build (creates deployable package)
mvn package -Pdistribution

# Faster build (skip tests, docs, sources)
export MAVEN_OPTS="-DskipTests -Dmaven.javadoc.skip=true -Dmaven.source.skip=true -Dgpg.skip=true"
mvn clean package

# Build specific module
./build-module.sh <module-name>

# Build Docker image
./build-docker.sh

# Build documentation
./build-docs.sh
```

### Running Addax

```bash
# Execute a job configuration
bin/addax.sh job/job.json

# Run server mode
bin/addax-server.sh

# Windows batch file
bin/addax.bat job/job.json

# Python wrapper (for Windows)
python bin/addax.py job/job.json
```

### Documentation

```bash
# Install documentation dependencies
pip install mkdocs-material

# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve -a 0.0.0.0:8888

# Deploy documentation
export version=4.1.5
git checkout $version
mike deploy -p $version
```

### Development Utilities

```bash
# Install Addax system-wide
./install.sh

# Encrypt passwords for configuration
bin/encrypt_password.sh

# Install plugins
bin/install_plugins.sh

# Performance profiling
python bin/perftrace.py

# Data profiling
python bin/dxprof.py

# Create minimal distribution
./shrink_package.sh
```

## Architecture

### Project Structure

Addax uses a **Maven multi-module architecture** with 75 modules organized as follows:

```
addax-all (parent POM)
├── core/                      # Core ETL engine and framework
│   ├── src/main/java/         # Core Java classes
│   └── src/main/bin/          # Execution scripts (addax.sh, etc.)
├── lib/                       # Shared library modules
│   ├── addax-rdbms/          # RDBMS utilities
│   └── addax-storage/        # Storage utilities
├── plugin/                    # Plugin modules
│   ├── reader/               # Data reader plugins (25+)
│   │   ├── mysqlreader/
│   │   ├── postgresqlreader/
│   │   ├── mongodbreader/
│   │   └── [20+ more readers...]
│   └── writer/               # Data writer plugins (28+)
│       ├── mysqlwriter/
│       ├── postgresqlwriter/
│       ├── mongodbwriter/
│       └── [20+ more writers...]
└── server/                   # Server component
```

### Core Components

- **Entry Point**: `com.wgzhao.addax.core.Engine` (core/src/main/java/com/wgzhao/addax/core/Engine.java)
  - Initializes JobContainer
  - Handles plugin loading
  - Orchestrates ETL execution

- **Execution Scripts**: Located in `core/src/main/bin/`
  - `addax.sh` - Main execution script
  - `addax-server.sh` - Server mode
  - `encrypt_password.sh` - Password encryption utility
  - `install_plugins.sh` - Plugin installation
  - `perftrace.py` - Performance profiling
  - `dxprof.py` - Data profiling

### Plugin System

The plugin architecture supports **50+ data sources**:

**Reader Plugins** (25+):
- Databases: MySQL, PostgreSQL, Oracle, SQL Server, MongoDB, Cassandra, Redis
- File Systems: HDFS, S3, FTP, Excel, TxtFile
- NoSQL: HBase, InfluxDB, Elasticsearch
- Messaging: Kafka, Stream
- And more...

**Writer Plugins** (28+):
- Same sources as readers plus: Doris, StarRocks, Greenplum, Paimon, Iceberg

All plugins follow a consistent interface pattern and are dynamically loaded at runtime.

### Supported Data Sources

See `support_data_sources.md` for the complete list of 50+ supported databases and file formats including:
- **Relational**: MySQL, PostgreSQL, Oracle, SQL Server, DB2, SAP HANA
- **NoSQL**: MongoDB, Cassandra, HBase, Redis, InfluxDB
- **Big Data**: Hive, Kudu, Doris, StarRocks, ClickHouse, Iceberg
- **Cloud Storage**: S3, MinIO
- **File Formats**: Excel, Parquet, ORC, Avro, JSON, CSV
- **Messaging**: Kafka

## Code Style Guidelines

- **IDE**: IntelliJ IDEA with [Airlift's Code Style](https://github.com/airlift/codestyle)
- **Java Version**: 17 (source/target: 17)
- **Exception Handling**: Use `AddaxException` with categories (e.g., `AddaxException(REQUIRE_VALUE, "missing required parameter")`)
- **Streams**: Use Java 8 Stream API cautiously (avoid in performance-sensitive areas)
- **Operators**: Avoid ternary operators for non-trivial expressions
- **Licensing**: Include Apache License 2.0 header in every file

## Versioning

Follow **Semantic Versioning (SemVer)**:
- **x.y.z** format
- **z (Patch)**: Bug fixes, performance improvements (backward compatible)
- **y (Minor)**: New features, module adjustments (may break backward compatibility)
- **x (Major)**: Significant changes, often incompatible with previous versions

## Build Configuration

- **Main POM**: `/home/ubuntu/deploy-projects/f1e3529fab621f448fb802b4/pom.xml` (63,533 bytes) - 75 modules, dependency management
- **Assembly Descriptor**: `package.xml` - Creates distribution packages
- **CI/CD**: GitHub Actions workflows in `.github/workflows/`
  - `maven-publish.yml` - Automated releases
  - `docs.yml` - Documentation builds
  - `verify.yml` - Verification pipeline

## Documentation

Documentation system using **MkDocs** with Material theme:
- **Source**: `docs/` directory
- **Languages**: English (`docs/en/`) and Chinese support
- **Config**: `mkdocs.yml`
- **Build**: Run `mkdocs build` or `python3 -m pip install mkdocs-material && mkdocs build`
- **Online**: https://wgzhao.github.io/Addax/

Key documentation files:
- `docs/quickstart.md` - Getting started guide
- `docs/setupJob.md` - Job configuration guide
- `docs/commandline.md` - CLI reference
- `docs/plugin_development.md` - Plugin development guide
- `docs/reader/` - Reader plugin documentation
- `docs/writer/` - Writer plugin documentation

## Testing

**Note**: No unit tests detected in the current codebase. Testing is performed via:
- Integration tests (external)
- Sample job configurations (`docs/assets/jobs`)
- Plugin-specific testing
- Manual testing

## Runtime Requirements

- **Java**: JDK 17 (compilation), JRE 17 (runtime)
- **Python**: 2.7+ / 3.7+ (only needed for Python scripts on Windows)
- **Memory**: Depends on data volume (configurable via job settings)

## Installation Methods

1. **Docker** (recommended):
   ```bash
   docker pull quay.io/wgzhao/addax:latest
   docker run -ti --rm quay.io/wgzhao/addax:latest /opt/addax/bin/addax.sh /opt/addax/job/job.json
   ```

2. **Installation Script**:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/wgzhao/Addax/master/install.sh)"
   ```
   - Installs to: `/usr/local` (macOS), `/opt/addax/` (Linux)

3. **From Source**:
   ```bash
   git clone https://github.com/wgzhao/addax.git
   cd addax
   mvn clean package
   ```

## Deployment

After `mvn package -Pdistribution`, distribution is created in:
- `target/addax-<version>/` - Complete distribution
- `target/addax-<version>-bin.zip` - Zipped distribution

Docker images are published to: `quay.io/wgzhao/addax:latest`

## Related Projects

- **[addax-admin](https://github.com/wgzhao/addax-admin)** - Web-based management tool
- **[addax-ui](https://github.com/wgzhao/addax-ui)** - Frontend for addax-admin

## Key Files

- `pom.xml` - Main Maven build file (75 modules)
- `package.xml` - Assembly descriptor for distribution
- `core/src/main/java/com/wgzhao/addax/core/Engine.java` - Main entry point
- `core/src/main/bin/addax.sh` - Primary execution script
- `mkdocs.yml` - Documentation configuration
- `difference.md` - Comparison with original DataX
- `support_data_sources.md` - Complete list of supported sources