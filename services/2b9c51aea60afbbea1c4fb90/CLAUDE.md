# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Azure Application Insights Java SDK - a Java agent that extends OpenTelemetry Java Agent to provide Azure Application Insights telemetry. The agent instruments applications at runtime without code changes.

## Build Commands

```bash
# Build complete agent JAR
./gradlew assemble

# Agent JAR output location
# agent/agent/build/libs/applicationinsights-agent-<version>.jar

# Run all unit tests
./gradlew test

# Run a specific unit test
./gradlew :agent:agent-tooling:test --tests "*ConfigurationTest"

# Run a specific smoke test (containerized integration test)
./gradlew :smoke-tests:apps:HttpClients:smokeTest --tests "*HttpClientTest\$Tomcat8Java8Test"

# Apply code formatting
./gradlew spotlessApply

# Check code formatting
./gradlew spotlessCheck

# Regenerate dependency lock files after updating dependencies
./gradlew resolveAndLockAll --write-locks

# Regenerate license reports after updating dependencies
./gradlew generateLicenseReport --no-build-cache
```

## Architecture

### Multi-Module Structure

```
agent/
├── agent/                    # Final agent JAR assembly (shadow plugin)
├── agent-bootstrap/          # Bootstrap classloader components (loaded early)
├── agent-tooling/            # Core agent logic & Azure exporters (agent classloader)
├── agent-profiler/           # JFR-based profiling system
├── instrumentation/          # Custom instrumentation modules (azure-functions, methods)
└── runtime-attach/           # Dynamic attach support

smoke-tests/
├── framework/                # Shared test infrastructure
└── apps/                     # Containerized test applications

classic-sdk/                 # Legacy 2.x SDK (maintained for compatibility)
```

### Agent JAR Assembly (agent/agent/build.gradle.kts)

The agent JAR is built in 3 steps:
1. **Relocate** distro-specific libraries to avoid conflicts
2. **Isolate** classes to `inst/` directory with `.classdata` extensions
3. **Merge** with upstream OpenTelemetry agent, excluding duplicates

### Classloader Architecture

- **Bootstrap classloader**: Minimal classes loaded early (`agent-bootstrap`)
- **Agent classloader**: Application Insights logic isolated from instrumented app (`agent-tooling`)
- **Application classloader**: User code with instrumentation applied

### Configuration Pattern

- Main configuration: `Configuration.java` in agent-tooling (JSON-based)
- Environment variables: `APPLICATIONINSIGHTS_CONNECTION_STRING`, `APPLICATIONINSIGHTS_PROFILER_ENABLED`
- Entry point: `Agent.java` in agent module (wraps OpenTelemetry Agent)

### Dependency Management

- Centralized in `dependencyManagement/` module
- All subprojects use `failOnVersionConflict()` resolution strategy
- Dependency locking enabled for reproducible builds (`gradle.lockfile`)

## Build Conventions (buildSrc/)

- **ai.java-conventions**: Base Java setup with JDK 21 toolchain, targets Java 8 bytecode
- **ai.javaagent-instrumentation**: Plugin for OpenTelemetry instrumentation modules
- **ai.smoke-test-war**: WAR-based smoke test applications
- **ai.shadow-conventions**: JAR shadowing with relocation rules
- **ai.spotless-conventions**: Code formatting (Google Java Format + import order)

## Smoke Tests

Smoke tests use Docker containers to test the agent in realistic environments:
- Framework: `smoke-tests/framework/` - shared test infrastructure with Fake Ingestion
- Pattern: Each abstract test class has nested static classes for different environments:
  ```java
  abstract class HttpClientTest {
    @Environment(TOMCAT_8_JAVA_8)
    static class Tomcat8Java8Test extends HttpClientTest {}
  }
  ```
- Assertions: `DependencyAssert`, `RequestAssert`, `MetricAssert`

## Key Files

- `agent/agent/build.gradle.kts` - Agent assembly process
- `agent/agent/src/main/java/.../Agent.java` - Agent entry point
- `agent/agent-tooling/src/main/java/.../configuration/Configuration.java` - Main configuration
- `buildSrc/src/main/kotlin/*.gradle.kts` - Build conventions
- `dependencyManagement/build.gradle.kts` - Centralized dependencies

## Style Guide

Follow the [OpenTelemetry Java Instrumentation style guide](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/contributing/style-guideline.md).

## Bisecting OpenTelemetry Agent Regressions

1. Update `dependencyManagement/build.gradle.kts` to use SNAPSHOT version
2. Clone and bisect upstream repo
3. Run `./gradlew publishToMavenLocal` then test with `./gradlew :smoke-tests:apps:YourApp:smokeTest`