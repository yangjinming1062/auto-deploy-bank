# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Quarkus is a Cloud Native, (Linux) Container First framework for writing Java applications. It unifies imperative and reactive programming models and is based on standards and frameworks like JAX-RS, Hibernate ORM, Netty, Eclipse Vert.x, and MicroProfile.

## Build Commands

```bash
# Quick build (skips tests, docs, native builds)
./mvnw -Dquickly

# Fast build - skips more, faster iteration
./mvnw -e -DskipDocs -DskipTests -DskipITs -Dinvoker.skip -DskipExtensionValidation -Dskip.gradle.tests -Dtruststore.skip clean install

# Build with multiple threads (0.8 threads per CPU core)
./mvnw install -T0.8C

# Format code (Eclipse formatter)
./mvnw process-sources -Denforcer.skip -Dprotoc.skip

# Build docs
./mvnw -DquicklyDocs && ./mvnw -f docs clean install
```

### Testing

```bash
# Run a single test in an integration test module
./mvnw test -f integration-tests/<name>/ -Dtest=TestName

# Run integration tests in native mode (required for @QuarkusIntegrationTest tests)
./mvnw verify -f integration-tests/<name>/ -Dnative

# Run Maven Invoker tests
./mvnw verify -f integration-tests/<path>/ -Dinvoker.test=test-name

# Skip test modules entirely
./mvnw install -Dno-test-modules
```

### Building Specific Modules

```bash
# Build an extension and all its submodules
./mvnw install -f extensions/<extension>/

# Build a single module of an extension
./mvnw install -f extensions/<extension>/deployment

# Build with relocations (for compatibility testing)
./mvnw -Dquickly -Prelocations
```

## Architecture

### Directory Structure

- **core/** - Core runtime and deployment modules (builder, class-change-agent, deployment, devmode-spi, launcher, processor, runtime)
- **extensions/** - 165+ extensions, each with runtime, deployment, and spi modules
- **integration-tests/** - Integration test modules (~277 directories)
- **independent-projects/** - Standalone projects (Arc DI, Qute templating, JUnit virtual threads, RESTEasy Reactive, tools)
- **devtools/** - Developer tools including CLI and Maven plugins
- **tcks/** - Technology Compatibility Kits (MicroProfile)
- **test-framework/** - Shared test utilities
- **docs/** - Asciidoc documentation
- **bom/** - Bill of Materials artifacts
- **relocations/** - Relocation artifacts for compatibility

### Extension Model

Each extension follows a multi-module structure:
- **runtime/** - User-facing artifacts, configurations, and runtime behavior
- **deployment/** - Build-time logic, processors, and default configurations
- **spi/** - Service Provider Interface for extending the extension

Extension metadata is defined in `runtime/src/main/resources/META-INF/quarkus-extension.yaml`.

Key extensions include:
- **arc/** - CDI implementation (dependency injection)
- **resteasy-reactive/** and **resteasy/** - JAX-RS REST frameworks
- **hibernate-orm/** - JPA/database ORM
- **vertx/** - Reactive engine
- **kubernetes/** - Kubernetes integration
- **grpc/** - gRPC support

### Key Dependencies

- Jakarta EE APIs (jakarta.*)
- SmallRye (MicroProfile implementations)
- Hibernate (ORM, Validator, Search)
- gRPC, Netty, Undertow

### Build Configuration

- Maven-based with `./mvnw` wrapper
- Requires Java 17+ (Java 21 recommended)
- Parent POM: `independent-projects/parent/pom.xml`
- Extension parent: `extensions/pom.xml`

## Development Notes

- Code style is enforced via Eclipse formatter (`independent-projects/ide-config/`)
- No `@author` tags in Javadoc - use Git history for attribution
- Lambda expressions and streams should be minimized in runtime code
- All contributions require DCO sign-off
- CI runs on GitHub Actions with incremental builds via gitflow-incremental-builder

## Common Tasks

### Adding a new extension

Extensions are typically created using the Quarkus CLI or Maven archetype. See `independent-projects/tools/extension-maven-plugin/` for the Maven-based approach.

### Updating extension metadata

Edit `runtime/src/main/resources/META-INF/quarkus-extension.yaml`. If adding/removing extensions, rebuild `devtools/bom-descriptor-json` without `-Dincremental`.

### Updating dependencies to extensions

Run `./update-extension-dependencies.sh` to refresh extension dependencies.