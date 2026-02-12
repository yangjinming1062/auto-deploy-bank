# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Quarkus is a Kubernetes-native Java framework designed for OpenJDK, GraalVM, and Mandrel. It offers fast startup times and low memory footprint through **build-time augmentation**. The project uses a multi-module Maven build with 165+ extensions.

## Build Commands

```bash
# Full build with tests (recommended)
./mvnw clean install

# Run unit tests only (skip integration tests)
./mvnw test -DskipITs

# Run a specific test class
./mvnw test -Dtest=ClassName -pl module-name

# Run integration tests only
./mvnw verify -DskipTests

# Build a specific module
./mvnw install -pl core/deployment -am

# Skip code formatting validation (format runs by default)
./mvnw test -Dno-format

# Native executable build
./mvnw install -Dnative -Dquarkus.native.native-image-xmx=6g

# Build without tests
./mvnw install -DskipTests

# Run in dev mode
./mvnw quarkus:dev -pl integration-tests/some-test
```

## Project Structure

- **core/** - Core framework with 7 modules:
  - `runtime/` - Runtime classes (logging, config, lifecycle, annotations)
  - `deployment/` - Build-time augmentation logic and build steps
  - `builder/` - Build chain engine managing the DAG of build steps
  - `processor/` - Annotation processing and metadata extraction
  - `devmode-spi/` - SPI for development mode
  - `launcher/` - Application startup for dev/prod modes
  - `class-change-agent/` - Hot reload support
- **extensions/** - 165+ extensions, each with `runtime/` and `deployment/` modules
- **integration-tests/** - 277+ integration test modules
- **devtools/** - Maven/Gradle plugins, CLI, codestarts
- **independent-projects/** - Standalone libraries (ArC CDI, Qute templating, testing tools)
- **test-framework/** - JUnit 5 extensions for Quarkus testing
- **tcks/** - MicroProfile TCK compliance tests
- **build-parent/** - Parent POM with plugin versions and build configurations

## Build-Time Augmentation Architecture

Quarkus shifts work from runtime to build time through a **Directed Acyclic Graph (DAG)** of build steps:

1. **Build Items** - Objects passed between build steps (e.g., `AdditionalBeanBuildItem`, `ApplicationInfoBuildItem`)
2. **Build Steps** - Methods annotated with `@BuildStep` in deployment modules that produce/consume Build Items
3. **Build Chain** - Executed by `core/builder` to orchestrate all build steps

### Example Build Step Pattern
```java
@BuildStep
AdditionalBeanBuildItem beans() {
    return AdditionalBeanBuildItem.unremovable(MyBean.class);
}
```

## Extension Architecture

Extensions follow a strict **runtime/deployment split**:

- **runtime module** - Classes the application developer depends on; packaged in user JARs
- **deployment module** - Build-time logic that registers capabilities and contributes build steps

Extensions are discovered via `META-INF/quarkus-extension.properties` files generated during build.

### Creating New Extensions

1. Create extension under `extensions/` with parent from `extensions/pom.xml`
2. Each extension needs `runtime/` and `deployment/` modules
3. Runtime modules declare capabilities via `quarkus-extension-maven-plugin`
4. Deployment modules contribute `@BuildStep` methods and depend on runtime

## Code Style

Code formatting and import sorting are active by default. Run `./mvnw format` to auto-format. Use `-Dno-format` or `-Dformat.skip` to disable during builds.

## Key Technologies

- **ArC** - Build-time oriented CDI implementation (no proxies at runtime)
- **Gizmo** - High-performance bytecode generation during deployment phase
- **SmallRye** - Jakarta EE specifications (OpenAPI, Config, Fault Tolerance, etc.)
- **Maven** - Build tool (3.9.0+)
- **Java** - Requires JDK 17+, recommended JDK 25
- **GraalVM/Mandrel** - For native executable compilation
- **JUnit 5** - Testing framework with Quarkus extensions