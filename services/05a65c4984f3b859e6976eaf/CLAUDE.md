# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Quarkus is a Kubernetes-native Java framework. It's a multi-module Maven project with a unique build architecture based on **build chains** and **build items**.

## Build Commands

```bash
# Full build (skip tests, docs, and format validation)
./mvnw clean install -DskipTests -Dformat.skip -Denforcer.skip -DskipDocs

# Build with tests
./mvnw test

# Run integration tests
./mvnw verify -pl integration-tests -am

# Build native executable
./mvnw package -Dnative

# Run a single test class
./mvnw test -pl core/deployment -Dtest=QuarkusAugmentorTest

# Run a single test method
./mvnw test -pl core/deployment -Dtest=QuarkusAugmentorTest#testAugmentorFailure

# Dev mode (live coding)
./mvnw quarkus:dev -pl <module>

# Skip format validation only
./mvnw clean install -Dformat.skip

# Skip format validation (enforce format checking)
./mvnw clean install -Dno-format
```

Maven 3.9.12 is required. The project uses Maven Wrapper (`./mvnw`).

Code formatting (Java formatter, import sorting) and Kotlin formatting (ktfmt) are active by default. Disable with `-Dno-format` or skip individual checks with `-Dformat.skip`.

## Architecture

### Build Chain System

Quarkus uses a custom build chain mechanism defined in `core/builder/`:
- **BuildStep**: Individual build tasks annotated with `@BuildStep`
- **BuildItem**: Data objects passed between build steps (in `core/deployment/src/main/java/io/quarkus/deployment/builditem/`)
- **BuildChainBuilder**: Constructs the dependency graph of build steps

Extension build steps produce and consume build items to transform the application during augmentation.

#### Common BuildItem Types

| Type | Purpose |
|------|---------|
| `FeatureBuildItem` | Declares extension name for logging |
| `CapabilityBuildItem` | Registers capability for other extensions to consume |
| `CombinedCapabilityBuildItem` | Combines multiple capabilities |
| `NativeImageBuildItem` | GraalVM configuration |
| `GeneratedClassBuildItem` | Runtime class generation |
| `ProductionPropertyBuildItem` | Configuration properties |

#### Build Item Production Patterns

- **Single**: `BuildItem` - produced once per build
- **Optional**: `OptionalSupplierBuildItem` / `OptionalBuildItem` - may not be produced
- **Multiple**: `MultiBuildItem` - can be produced multiple times
- **Flexible**: `FlexibleBuildItem` - combines optional and multiple

### Core Modules (`core/`)

| Module | Purpose |
|--------|---------|
| `runtime/` | Runtime classes included in the final application |
| `deployment/` | Build steps that run during augmentation, produces build items |
| `processor/` | Annotation processor for CDI and config |
| `builder/` | Core build chain infrastructure |
| `devmode-spi/` | SPI for dev mode extensions |
| `launcher/` | Application launcher |
| `class-change-agent/` | Hot reload agent |

### Extension Structure

Each extension follows this pattern (e.g., `extensions/arc/`):

```
extension/
├── deployment/    # Build steps for this extension
├── runtime/       # Runtime classes provided to applications
├── runtime-dev/   # Dev mode utilities (optional)
└── test-supplement/  # Additional test support (optional)
```

### Independent Projects (`independent-projects/`)

Core libraries that Quarkus depends on, maintained as separate concerns:

| Project | Purpose |
|---------|---------|
| `arc/` | Quarkus CDI implementation - a build-time CDI container |
| `qute/` | Type-safe template engine |
| `resteasy-reactive/` | Reactive JAX-RS implementation |
| `bootstrap/` | Application model and class loading |
| `enforcer-rules/` | Maven enforcer rules for dependency management |
| `extension-maven-plugin/` | Maven plugin for extension development |
| `revapi/` | API compatibility checking configuration |
| `tools/` | Shared build tools and utilities |

### Extension Categories (`extensions/`)

Extensions are organized by functional area:

- **Plumbing**: Arc, scheduler, quartz
- **HTTP**: Vert.x HTTP, RESTEasy (classic/reactive), Undertow, websockets
- **Data Access**: Hibernate ORM/Reactive, Panache, Agroal, JDBC, MongoDB, Redis
- **Reactive**: Mutiny, Vert.x, gRPC, Reactive messaging (Kafka, AMQP, MQTT, Pulsar, RabbitMQ)
- **Security**: Security, OIDC, JWT, Elytron, Keycloak
- **Monitoring**: SmallRye Health, Micrometer, OpenTelemetry
- **Cloud**: Kubernetes, Amazon Lambda, Azure Functions, Google Cloud Functions
- **Messaging**: Kafka, RabbitMQ, AMQP, Pulsar
- **Integration**: Spring compatibility, Funqy

### Deployment ClassLoader Pattern

Quarkus uses a two-classloader architecture:
1. **Runtime ClassLoader**: Loads runtime dependencies only
2. **Deployment ClassLoader**: Loads deployment-time dependencies (build steps, processors)

This keeps the final application JAR lean.

### Code Generation System

Extensions can register code generators that run during build. Implement `CodeGenProvider` to add generators for:
- Configuration schema generation
- Schema migrations (Flyway, Liquibase)
- OpenAPI schema generation
- GraphQL schema generation

## Module Hierarchy

The main parent POMs are:
1. `build-parent/pom.xml` - Plugin versions, dependency versions
2. `extensions/pom.xml` - Extension aggregation
3. `core/pom.xml` - Core module aggregation
4. `integration-tests/pom.xml` - Integration test modules (activated via profile `test-modules`)

## Development Notes

- API compatibility is checked via RevAPI. Run `jbang revapi-update` to update API checks.
- Extensions register capabilities via `CapabilityBuildItem` for discoverability
- Use `@Record` annotation to access recorder objects for runtime value capture
- Build steps should avoid heavy computation - consider using `Supplier` for deferred execution

### Testing (`test-framework/`)

Quarkus provides a rich testing framework:

| Module | Purpose |
|--------|---------|
| `junit/` | Main `@QuarkusTest` annotation and utilities |
| `junit-component/` | Testing for CDI components |
| `junit-mockito/` | Mockito integration |
| `common/` | Shared test utilities |
| `devmode-test-utils/` | Dev mode testing support |
| `kubernetes-client/` | Kubernetes test infrastructure |
| `mongodb/` | MongoDB test containers |
| `oidc-server/` | OIDC test server |

### Dev Services

Most extensions include Dev Services - auto-started test containers for databases (PostgreSQL, MySQL, MongoDB, etc.), message brokers (Kafka, RabbitMQ), and services (Elasticsearch, Redis). Enabled automatically in `@QuarkusTest`.

### DevUI (`extensions/devui/`)

The dev console (`/q/dev`) provides runtime insights, configuration editing, health checks, and metrics. Extensions can contribute via `DevUIBuildItem`.