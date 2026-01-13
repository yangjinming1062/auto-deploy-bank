# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Apache Ignite 2.x is a distributed database for high-performance computing with in-memory speed. It's a mature, enterprise-grade platform with multi-tier storage (memory, disk, Intel Optane), ACID compliance, ANSI-99 SQL support, and native persistence.

## Common Development Commands

### Building the Project

**Full Java build (skip tests)**:
```bash
./mvnw clean install -Pall-java,licenses -DskipTests
```

**Build with .NET and C++ platforms** (requires doxygen, docfx, .NET Core SDK 3.1, PowerShell):
```bash
./mvnw clean install -Pall-java,licenses,platforms -DskipTests -DclientDocs
```

**Run tests**:
```bash
./mvnw clean test -U -Plgpl,examples,-clean-libs,-release -Dmaven.test.failure.ignore=true -DfailIfNoTests=false -Dtest=%TEST_PATTERN%
```
Example test patterns:
- `org.apache.ignite.testsuites.IgniteBasicTestSuite` (run a test suite)
- `GridCacheLocalAtomicFullApiSelfTest#testGet` (run a specific test)

**Check test suite coverage**:
```bash
./mvnw test -Pcheck-test-suites
```

**Run code style checks**:
```bash
./mvnw clean validate -Pcheck-style
```

**Check license headers (Apache RAT)**:
```bash
./mvnw clean validate -Pcheck-licenses
```

**Generate Javadoc**:
```bash
./mvnw initialize -Pjavadoc
```

**Build release package**:
```bash
./mvnw initialize -Prelease
```
Output: `apache-ignite-<version>-bin.zip` in `./target/bin/`

**Build slim edition**:
```bash
./mvnw initialize -Prelease -Dignite.edition=apache-ignite-slim
```

**Test JCache TCK compliance**:
```bash
./mvnw test -P-release,jcache-tck -pl :ignite-core -am
```

### Platform-Specific Builds

**C++ platform** (see `modules/platforms/cpp/DEVNOTES.txt`)

**Package builds**:
```bash
# RPM package
packaging/package.sh --rpm

# DEB package
packaging/package.sh --deb

# Both
packaging/package.sh --rpm --deb
```

### Key Build Profiles

- `all-java` - Builds all Java modules
- `licenses` - Processes licenses
- `platforms` - Builds .NET and C++ components
- `release` - Release packaging
- `check-style` - Code style validation (Checkstyle)
- `check-test-suites` - Validates test suite coverage
- `check-licenses` - License header validation
- `lgpl` - Includes LGPL-licensed components
- `numa-allocator` - NUMA allocator support (Linux only)
- `examples` - Example projects
- `javadoc` - Documentation generation

## Code Architecture and Structure

### Multi-Module Maven Project

The project is organized into **40+ Maven modules** (`modules/` directory), each implementing specific functionality:

**Core modules**:
- `core` - Main Ignite functionality
- `indexing` - SQL and query processing
- `binary` - Binary serialization framework
- `spring` - Spring Framework integration
- `calcite` - SQL query engine integration
- `rest-http` - REST API implementation

**Client modules**:
- `clients` - Client API implementations
- `rest` - REST client support

**Platform modules**:
- `platforms/dotnet` - .NET/C# API
- `platforms/cpp` - C++ API

**Integration modules**:
- `kubernetes` - Kubernetes support
- `zookeeper` - ZooKeeper service discovery
- `cassandra` - Apache Cassandra integration
- `h2` - H2 database integration
- `kafka` - Apache Kafka streaming

**Utility modules**:
- `checkstyle` - Code style configuration
- `codegen`, `codegen2` - Code generation tools
- `ducktests` - Python-based testing framework
- `yardstick` - Performance benchmarking

### Main Entry Point

**`org.apache.ignite.Ignite`** (`modules/core/src/main/java/org/apache/ignite/Ignite.java`)
- Primary interface for all Ignite APIs
- Retrieved via `Ignition.start(configFile)` or `Ignition.ignite(instanceName)`

**Key APIs provided by Ignite interface**:
- `IgniteCache` - Distributed caching and SQL queries
- `IgniteTransactions` - ACID-compliant distributed transactions
- `IgniteCompute` - Distributed computing (MapReduce)
- `IgniteServices` - Service grid functionality
- `IgniteMessaging` - Topic-based messaging
- `IgniteEvents` - Event handling
- Distributed atomic data structures (Long, Reference, Sequence, etc.)
- `IgniteScheduler` - Cron-based job scheduling

### Test Organization

- Each module has tests in `src/test/java/`
- Test classes follow patterns: `*SelfTest.java`, `*Test.java`
- Test suites organize related tests: `org.apache.ignite.testsuites.*`
- Python-based testing in `modules/ducktests/` for cross-platform scenarios

### Configuration and Scripts

- `bin/ignite.sh/bat` - Main Ignite startup script
- `bin/control.sh/bat` - Cluster control utility
- `config/` - Configuration templates
- `.idea/inspectionProfiles/Project_Default.xml` - IntelliJ IDEA inspection profile
- `checkstyle/checkstyle.xml` - Checkstyle configuration

### Dependencies and Tech Stack

- **Language**: Java 11 (compiler source/target)
- **Build**: Maven 3.8.4 (use `./mvnw` wrapper)
- **Testing**: JUnit, Hamcrest, Mockito 3.12.4
- **CI**: GitHub Actions (`.github/workflows/commit-check.yml`), Apache Jenkins
- **Core libraries**: Spring 5.3.39, Jackson 2.19.0, Log4j2 2.22.0, Jetty 11.0.24
- **SQL**: Apache Calcite, H2 1.4.197
- **Search**: Lucene 8.11.2
- **Protocols**: gRPC 1.62.2

### Development Guidelines

**Code Style**:
- Enforced via Checkstyle 8.45 (PuppyCrawl rules)
- Configuration: `checkstyle/checkstyle.xml`
- Key rules: UTF-8 encoding, import ordering (STANDARD → SPECIAL → THIRD_PARTY → STATIC), redundant import checks, empty catch block detection

**IntelliJ IDEA Setup**:
- Use provided abbreviation plugin and code inspection profile
- Import `checkstyle/checkstyle-suppressions.xml` for Checkstyle integration
- Apply code style from `.idea/codeStyles/Project.xml`

**License**:
- Apache License 2.0 (main)
- LGPL components for some modules (Schedule)
- License headers validated by Apache RAT

### Documentation Resources

- **Technical Documentation**: https://ignite.apache.org/docs/latest/
- **JavaDoc**: https://ignite.apache.org/releases/latest/javadoc/
- **.NET APIs**: https://ignite.apache.org/releases/latest/dotnetdoc/api/
- **C++ APIs**: https://ignite.apache.org/releases/latest/cppdoc/
- **Apache Wiki**: https://cwiki.apache.org/confluence/display/IGNITE
- **Project Setup Guide**: https://cwiki.apache.org/confluence/display/IGNITE/Project+Setup
- **Coding Guidelines**: https://cwiki.apache.org/confluence/display/IGNITE/Coding+Guidelines

### Apache Ignite vs Ignite 3

- This repository contains **Ignite 2.x**
- Ignite 3.x is in a separate repository: https://github.com/apache/ignite-3
- Both versions are actively developed

### Important Notes

- Use Maven wrapper (`./mvnw`) for all builds to ensure consistency
- Most development builds should run with `-DskipTests`
- CI/CD pipeline runs comprehensive checks including style, test suites, and Javadoc validation
- The project uses OSGi for modular architecture
- Service discovery via ZooKeeper for cluster formation
- Supports multiple storage tiers: memory, disk, Intel Optane