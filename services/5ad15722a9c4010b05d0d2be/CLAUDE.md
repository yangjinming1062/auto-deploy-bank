# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Apache Gobblin is a highly scalable distributed data management solution for structured and heterogeneous data. It's designed for ELT (Extract, Load, Transform) patterns with inline transformations, supporting both stream and batch execution modes at petabyte scale.

**Key Capabilities:**
- Ingestion and export from various sources to data lakes (HDFS, S3, ADLS)
- Data organization (compaction, partitioning, deduplication)
- Lifecycle and compliance management (retention, GDPR deletions)
- Stream/batch ingestion (especially Kafka to data lake)
- Cross-platform data sync (federated data lake)

**Architecture Documentation**: See `gobblin-docs/Gobblin-Architecture.md` for detailed architecture diagrams and flow documentation.

## Common Development Commands

### Building and Testing

```bash
# Build without tests
./gradlew assemble

# Build with tests (requires Maven 3.5.3+)
./gradlew build

# Build distribution without tests (faster)
./gradlew build -x findbugsMain -x test -x rat -x checkstyleMain

# Run tests only
./gradlew test

# Run single test
./gradlew test --tests "fully.qualified.TestClassName"

# Run specific test group
./gradlew -PrunTestGroups=group1 test

# Skip specific test groups
./gradlew -PskipTestGroup=group1 test

# Run findbugs
./gradlew findbugs

# Run checkstyle
./gradlew checkstyle

# Run Apache RAT license checker
./gradlew rat

# Print version
./gradlew printVersionName
```

### Module-Specific Builds

```bash
# Build only a specific module
./gradlew :gobblin-core:build

# Test only a specific module
./gradlew :gobblin-core:test

# Assemble only (compile + jars, no tests)
./gradlew :gobblin-api:assemble
```

### Working with Gobblin Flavors (Module Customization)

Gobblin supports customizable distributions through "flavors" that control which modules are included:

```bash
# Build with minimal flavor (no optional modules)
./gradlew -PgobblinFlavor=minimal build

# Build with standard flavor (default - includes common components)
./gradlew -PgobblinFlavor=standard build

# Build with full flavor (all non-conflicting modules)
./gradlew -PgobblinFlavor=full build

# Build with custom flavor (user-customized)
./gradlew -PgobblinFlavor=custom build
```

**Flavor Files Location**: `gobblin-distribution/gobblin-flavor-<FLAVOR>.gradle`

### Version-Specific Builds

```bash
# Build with specific Hadoop version
./gradlew -PhadoopVersion=2.8.0 build

# Build with specific Hive version
./gradlew -PhiveVersion=2.3.0 build

# Build with specific Pegasus version
./gradlew -PpegasusVersion=11.0.0 build

# Build distribution excluding Hadoop dependencies
./gradlew -PexcludeHadoopDeps build

# Build distribution excluding Hive dependencies
./gradlew -PexcludeHiveDeps build
```

### Development Utilities

```bash
# View project dependency graph
./gradlew dotProjectDependencies

# Clean build artifacts
./gradlew clean

# Run with test output visible
./gradlew -PprintTestOutput test

# Run code coverage (Jacoco)
./gradlew -PjacocoBuild test

# Stop Gradle daemon
ligradle --stop
```

### Building Distribution

The final distribution will be created at:
```
build/gobblin-distribution/distributions/
```

## Code Architecture

### Module Structure

Gobblin uses a modular architecture with the following major components:

**Core Modules** (always included):
- `gobblin-api` - Core APIs and interfaces
- `gobblin-core` - Core job execution engine and constructs
- `gobblin-core-base` - Base functionality shared across core modules
- `gobblin-runtime` - Runtime execution engine
- `gobblin-runtime-hadoop` - Hadoop-specific runtime
- `gobblin-utility` - Utility classes and helpers
- `gobblin-metrics-libs` - Metrics infrastructure
- `gobblin-metastore` - State and metadata storage
- `gobblin-config-management` - Configuration management
- `gobblin-data-management` - Data lifecycle operations

**Service & Deployment**:
- `gobblin-service` - Gobblin-as-a-Service control plane
- `gobblin-rest-service` - REST API service
- `gobblin-restli` - Rest.li-based services
- `gobblin-cluster` - Cluster deployment mode
- `gobblin-yarn` - YARN deployment mode
- `gobblin-aws` - AWS-specific integrations

**Data Sources & Sinks**:
- `gobblin-salesforce` - Salesforce connector
- `gobblin-kafka-08/09` - Kafka connectors (version-specific)
- `gobblin-example` - Sample job configurations and examples

**Extensibility** (`gobblin-modules/`):
Optional modules with external dependencies that can be included based on needs. See "Module System" section below.

### Module System (gobblin-modules/)

Gobblin uses a plugin-style module system to support customization without conflicting dependencies:

**Location**: `gobblin-modules/` contains optional components with external dependencies

**Common Modules**:
- `gobblin-kafka-08/09` - Kafka connectors (API version conflicts)
- `gobblin-azkaban` - Azkaban scheduler integration
- `gobblin-elasticsearch` - Elasticsearch writer
- `gobblin-couchbase` - Couchbase writer
- `gobblin-crypto-provider` - Encryption provider
- `gobblin-helix` - Helix/ZK state store
- `google-ingestion` - Google Analytics/Drive/Webmaster sources
- `gobblin-azure-datalake` - Azure Data Lake filesystem
- `gobblin-compliance` - Data compliance and GDPR deletion
- `gobblin-metrics-graphite` - Graphite metrics reporter

**Module Dependency Pattern**:
```gradle
// In a module's build.gradle
dependencies {
    compile project(':gobblin-api')
    compile project(':gobblin-core')
    compile externalDependency.kafkaClient
}
```

### Core Constructs (gobblin-docs/Gobblin-Architecture.md)

Gobblin jobs are composed of pluggable constructs in a task flow:

1. **Source** - Partitions data into WorkUnits and creates Extractors
2. **Extractor** - Extracts data records from sources
3. **Converter** - Transforms schema and data (chainable, supports 1:0, 1:1, 1:N mappings)
4. **QualityChecker** - Validates data (row-level and task-level, MANDATORY/OPTIONAL)
5. **ForkOperator** - Splits task flow into multiple branches for different sinks
6. **DataWriter** - Writes data to sinks (HDFS, Kafka, JDBC, etc.)
7. **DataPublisher** - Commits and publishes job output

**Task Flow Pattern** (same across all deployment modes):
```
Source → WorkUnits → Tasks → Extractors → Converters → QualityCheckers → ForkOperator → Writers → Publishers
```

### Deployment Modes

1. **Standalone** - Single node, thread pool execution
2. **Hadoop MapReduce** - Tasks run in Hadoop mappers
3. **YARN** - Native YARN application
4. **Gobblin-as-a-Service** - Control plane for programmatic orchestration

**JobLauncher Abstractions**:
- `LocalJobLauncher` - Standalone mode
- `MRJobLauncher` - MapReduce mode
- Different launchers configured via `launcher.type` property

## Testing Framework

- **Framework**: TestNG (not JUnit)
- **Test Directories**: `src/test/` in each module
- **Test Groups**: Uses TestNG groups for categorization
- **Excluded by default**: Groups 'ignore' and 'performance'
- **Configuration**: Each module can override test behavior

**Test Output**:
- Logs to `test-output/` directory
- Configure with `-PprintTestOutput` for verbose output

**Running Tests**:
```bash
# All tests
./gradlew test

# Single module
./gradlew :gobblin-core:test

# With output
./gradlew -PprintTestOutput :gobblin-api:test

# Specific class
./gradlew test --tests "org.apache.gobblin.source.TestClass"

# Specific method
./gradlew test --tests "org.apache.gobblin.source.TestClass#testMethod"
```

## Documentation System

**Location**: `gobblin-docs/` (MkDocs-based)

**Building Docs Locally**:
```bash
# Install MkDocs
pip install mkdocs

# Serve documentation locally
mkdocs serve

# Build static docs
mkdocs build
```

**Main Documentation Files**:
- `Getting-Started.md` - Quick start guide
- `Gobblin-Architecture.md` - System architecture and design
- `user-guide/` - End-user documentation
- `developer-guide/` - Developer documentation and guides
- `sources/` - Source-specific documentation
- `sinks/` - Writer-specific documentation

## Build Configuration

**Gradle Configuration**:
- **Gradle Version**: 5.6.4 (wrapper included)
- **Java Version**: Java 8+ (Java 17+ may have compatibility issues with Gradle 5.6.4)
- **Daemon**: Enabled by default in `gradle.properties` for faster builds
- **Parallel**: Enabled for faster builds
- **Configuration on Demand**: Enabled for faster configuration

**JVM Settings** (from `gradle.properties`):
```properties
org.gradle.jvmargs=-Xms512m -Xmx4096m
```

**Key Gradle Scripts** (in `gradle/scripts/`):
- `testSetup.gradle` - TestNG configuration and test reporting
- `dependencyDefinitions.gradle` - Dependency versions
- `configureSubprojects.gradle` - Subproject configuration
- `rat.gradle` - Apache RAT license checker configuration
- `javaPlugin.gradle` - Java compilation settings

## IDE Support

**Configuration Files**:
- `gradle/scripts/idesSetup.gradle` - IDE integration
- `.gitignore` - Excludes IDE-specific files

**Generating IDE Files**:
```bash
# Generate IntelliJ project files
./gradlew idea

# Generate Eclipse project files
./gradlew eclipse
```

## Key Configuration Files

- `build.gradle` - Main build script with all plugin configurations
- `settings.gradle` - Submodule definitions
- `gradle.properties` - JVM and Gradle daemon settings
- `config/checkstyle/checkstyle.xml` - Code style rules
- `gobblin-distribution/build.gradle` - Distribution packaging
- `.codecov_bash` - Code coverage configuration

## Code Style and Quality

**Style Enforcement**:
- **Checkstyle**: Configured via `config/checkstyle/checkstyle.xml`
- **FindBugs**: Static analysis tool
- **License**: Apache RAT checks for proper licensing

**License Headers**:
All source files must have Apache License 2.0 header (see `HEADER` file).

**Running Quality Checks**:
```bash
./gradlew checkstyleMain
./gradlew findbugsMain
./gradlew rat
```

## Sample Projects

**Location**: `gobblin-example/`

Contains sample job configurations and example code demonstrating:
- How to configure Gobblin jobs
- Source/Writer implementations
- Converter usage patterns
- Deployment examples

## External Dependencies

**Managed Dependencies**: Defined in `gradle/scripts/dependencyDefinitions.gradle`

**Common Dependency Conflicts**:
- Kafka versions (0.8, 0.9, 1.0) - resolved via `gobblin-modules`
- Hadoop versions - configurable via `-PhadoopVersion`
- Hive versions - configurable via `-PhiveVersion`

## Environment Setup

**Requirements**:
- Java 1.8 or higher (Java 17+ may require Gradle compatibility adjustments)
- Gradle 5.6.4 (wrapper provided)
- Maven 3.5.3+ (for full test builds)
- Python 3+ (for MkDocs documentation building)

**Initial Setup**:
```bash
# Clone repository
git clone https://github.com/apache/gobblin.git

# Build project
./gradlew assemble

# Run tests
./gradlew test
```

## Important Notes

1. **TestNG Only**: This project uses TestNG for testing, not JUnit. When writing tests, import TestNG classes.

2. **Modular Design**: Gobblin's strength is its extensibility. Use `gobblin-modules/` for new integrations that might conflict with existing dependencies.

3. **Flavor System**: When adding new functionality that depends on external libraries, create a module and include it in appropriate flavors.

4. **State Management**: Gobblin maintains job state across runs for incremental processing. Understand state stores before modifying job execution logic.

5. **Documentation**: Update `gobblin-docs/` for any user-facing changes. Documentation builds automatically with PR merges.

6. **Backward Compatibility**: Gobblin is used in production at scale. Maintain backward compatibility unless explicitly breaking for architectural reasons.

7. **License Compliance**: All new files must include Apache License 2.0 header. Run `./gradlew rat` before submitting PRs.

8. **Performance at Scale**: Code changes should consider performance implications at petabyte scale. Review `gobblin-metrics-libs/` for monitoring capabilities.

## Where to Start

1. **New Contributors**: Read `gobblin-docs/developer-guide/Contributing.md`
2. **Understanding Architecture**: Start with `gobblin-docs/Gobblin-Architecture.md`
3. **Running First Job**: Check `gobblin-example/` and `gobblin-docs/Getting-Started.md`
4. **Building Gobblin**: See `gobblin-docs/user-guide/Building-Gobblin.md`
5. **Module Development**: Review `gobblin-docs/developer-guide/GobblinModules.md`

## Development Tips

- Use `./gradlew :module-name:build` to build just the modules you're changing
- Run `./gradlew rat` before creating PRs to check license compliance
- Test with `-PprintTestOutput` to see detailed test execution logs
- Use `gobblinFlavor` property to test your module in different distribution configurations
- Check `gradle.properties` for JVM tuning when running large test suites