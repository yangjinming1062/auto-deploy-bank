# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Micrometer is a vendor-neutral application metrics facade for the most popular monitoring tools. It allows you to instrument your code with dimensional metrics using a vendor-neutral interface and decide on the monitoring backend at the last minute.

## Common Development Commands

### Building and Testing
- `./gradlew build` - Build the entire project and run tests
- `./gradlew test` - Run all unit tests (excluding Docker integration tests)
- `./gradlew dockerTest` - Run Docker-based integration tests (requires Docker daemon)
- `./gradlew :micrometer-core:test` - Run tests for a specific module
- `./gradlew :micrometer-core:test --tests "*TimerTest"` - Run specific test class
- `./gradlew check` - Run all checks including tests and formatting
- `./gradlew downloadDependencies` - Download all project dependencies
- `./gradlew pTML` - Publish Maven-style snapshot to local repository

### Code Quality and Formatting
- `./gradlew format` - Apply code formatting (Spring Javaformat plugin)
- `./gradlew checkFormat` - Check code formatting
- `./gradlew spotlessCheck` - Run Spotless formatting checks
- `./gradlew licenseFormat` - Fix license headers

### Running Benchmarks
- `./gradlew :micrometer-benchmarks-core:jmh` - Run JMH benchmarks

### Specific Module Examples
```bash
# Build and test only micrometer-core
./gradlew :micrometer-core:build

# Test a specific registry implementation
./gradlew :micrometer-registry-prometheus:test

# Run observation tests
./gradlew :micrometer-observation:test
```

### Notes on Building
- Micrometer targets **Java 8** but requires **JDK 11 or later** to build
- If Gradle cannot detect JDK 11+, it will download one automatically
- Benchmarks and documentation generation require **JDK 17+**
- The Gradle wrapper (`./gradlew`) should always be used for consistency

## Architecture

### Core Modules

**micrometer-commons** (`/micrometer-commons/`)
- Common utilities shared across modules
- Annotations (`@Nullable`, `@NonNull`, `@Contract`, etc.)
- `KeyValues` and `ValidatedKeyValue` for dimensional metadata
- Internal logging utilities

**micrometer-core** (`/micrometer-core/`)
- Main metrics library containing the core instrumentation APIs
- **MeterRegistry**: Central registry for creating and managing meters (micrometer-core:708)
- **Meter types**: `Counter`, `Gauge`, `Timer`, `DistributionSummary`, `LongTaskTimer`
- **Meter**: Base interface for all meters with measurements (micrometer-core:40)
- Meter configuration: filters, naming conventions, and tags
- Distribution statistics and histogram support

**micrometer-observation** (`/micrometer-observation/`)
- Higher-level observation API for tracing and monitoring
- **Observation**: Main abstraction for monitoring operations (micrometer-observation:138)
- **ObservationConvention**: Defines naming and tagging conventions
- Context propagation support for distributed tracing
- AOP integration via `@Observed` annotation

### Registry Implementations (`/implementations/`)
Vendor-specific registry implementations that export metrics to different monitoring backends:
- **Prometheus**: `micrometer-registry-prometheus`
- **Atlas**: `micrometer-registry-atlas`
- **Datadog**: `micrometer-registry-datadog`
- **CloudWatch**: `micrometer-registry-cloudwatch2`
- **Elastic**: `micrometer-registry-elastic`
- **InfluxDB**: `micrometer-registry-influx`
- **New Relic**: `micrometer-registry-new-relic`
- **Wavefront**: `micrometer-registry-wavefront`
- **Azure Monitor**: `micrometer-registry-azure-monitor`
- And many more...

### Additional Modules
- **samples/**: Example applications demonstrating integration with Spring Framework, Javalin, Jersey, JOOQ, Kotlin, Hazelcast
- **benchmarks/**: JMH performance benchmarks
- **docs/**: Reference documentation (published to https://micrometer.io/)
- **micrometer-test/**: Test utilities shared across modules
- **micrometer-bom**: Bill of Materials for dependency management

### Version-Specific Modules
- **micrometer-java11**: Java 11+ specific features
- **micrometer-java21**: Java 21+ specific features
- **micrometer-jetty11/12**: Jetty integration modules

## Code Style and Conventions

- **Formatting**: The [Spring Javaformat plugin](https://github.com/spring-io/spring-javaformat) is configured and should be applied instead of IDE formatting
- **Null Safety**: Uses JSpecify annotations (`@NonNull`, `@Nullable`, `@NullUnmarked`) with **NullAway** for enforcement
- **Error Prone**: Static analysis tool enabled (requires JDK 21+) with strict checks
- **License Headers**: Required in all source files (automatically applied via `licenseFormat`)
- **Checkstyle**: Code style checks enabled

## Testing Strategy

- **JUnit 5**: Primary testing framework
- **Test Tags**: Docker-based integration tests are tagged and excluded from standard test runs (use `dockerTest` task to run them)
- **Concurrency Tests**: JCStress tests for concurrent data structures in `concurrency-tests/`
- **Compatibility Tests**: Each registry implementation includes compatibility test suites

## Build Configuration Highlights

- **Gradle Version**: 9.2.1
- **Develocity Build Cache**: Configured at https://ge.micrometer.io for remote caching
- **Target Compatibility**: Java 8 (with Java 11+ for test compilation)
- **OSGi**: Modules are built with OSGi bundles for modularity
- **JAPICMP**: Binary compatibility checks against previous versions
- **Modular JARs**: Automatic module name generation for Java 9+

## Key Development Notes

- **No BOM published**: This project publishes resolved versions instead of using dependency management in a BOM
- **Module Registration**: If a meter with the same ID is registered multiple times, only the first registration succeeds (micrometer-core:61-62)
- **Reactive Context**: `MeterRegistry` implementations must be non-blocking and suitable for reactive contexts
- **Documentation**: Reference docs are in the `docs/` directory using Antora and are published to https://micrometer.io/