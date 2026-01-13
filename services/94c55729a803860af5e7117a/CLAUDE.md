# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Helidon 4.4.0-SNAPSHOT** is Oracle's Java microservices framework providing two programming models:
- **Helidon MP**: MicroProfile 6.0 (Jakarta EE) for enterprise Java developers
- **Helidon SE**: Functional-style API for reactive programming

Built on **Java 21 with Virtual Threads** and the new **Níma WebServer**, Helidon 4 provides high throughput with the simplicity of thread-per-request programming. The project consists of **29 top-level Maven modules** with 7,319+ Java source files.

## Common Development Commands

### Building the Project

```bash
# Full build (requires JDK 21)
mvn install

# Build specific module
cd helidon-webserver
mvn install

# Build examples
./etc/scripts/build-examples.sh
```

### Code Quality Checks

```bash
# Run checkstyle validation
mvn validate -Pcheckstyle
# Or for full codebase
./etc/scripts/checkstyle.sh

# Verify copyright headers
mvn validate -Pcopyright
# Or for full codebase
./etc/scripts/copyright.sh

# Run SpotBugs static analysis
mvn verify -Pspotbugs

# Build Javadoc
mvn package -Pjavadoc
```

### Testing

```bash
# Run all tests
mvn test

# Run tests for specific module
cd helidon-webserver && mvn test

# Run integration tests
cd tests/integration && mvn test

# Run functional tests
cd tests/functional && mvn test

# Smoke tests
./etc/scripts/smoketest.sh

# Run a single test class
mvn test -Dtest=MyTestClass

# Run a specific test method
mvn test -Dtest=MyTestClass#myTestMethod
```

### Security Scanning

```bash
# OWASP dependency check
./etc/scripts/owasp-dependency-check.sh
```

## Code Architecture & Structure

### Module Organization

The project uses a **flat package structure** with these main categories:

**Core Framework:**
- `webserver/` - Níma HTTP server (Java 21 Virtual Threads)
- `webclient/` - HTTP client
- `http/` - HTTP protocol implementation
- `config/` - Configuration management
- `security/` - Security framework and providers
- `health/` - Health check support
- `metrics/` - Metrics and monitoring
- `tracing/` - Distributed tracing

**MicroProfile (Jakarta EE):**
- `microprofile/` - MP specifications implementation (Config, Health, Metrics, etc.)
- `jersey/` - JAX-RS/Jersey integration

**Reactive & Streaming:**
- `reactive/` - Reactive streams support
- `messaging/` - Message-driven microservices
- `graphql/` - GraphQL support
- `grpc/` - gRPC support

**Integration & Extensions:**
- `integrations/` - CDI, JPA, JTA, OCI, Micronaut, Vault integrations
- `fault-tolerance/` - Circuit breakers, retries, timeouts
- `cors/` - Cross-Origin Resource Sharing
- `websocket/` - WebSocket support
- `openapi/` - OpenAPI/Swagger support

**Utilities:**
- `common/` - Shared utilities
- `logging/` - Logging framework
- `scheduling/` - Task scheduling
- `json/` - JSON processing
- `data/` - Database client
- `validation/` - Bean validation
- `builder/` - Code-generated builders

### Package Naming Convention

- **Group ID**: `io.helidon.${project_module}`
- **Package**: `io.helidon.${project_module}.${module_name}`
- **Flat structure**: Each module has a single implementation package
- **Optional SPI package**: `io.helidon.${module}.spi` for service provider interfaces

### Key Design Patterns

1. **Builder Pattern**: All configuration classes use builders with code generation (`helidon-builder`)
   - Hidden constructors only
   - `builder()` static method
   - Immutable final fields
   - See `builder/README.md` for details

2. **Configuration**: Everything possible in config must be possible programmatically
   - Config keys use lower-case with dashes (e.g., `token-endpoint-uri`)
   - Supports Required, Default, and Optional properties

3. **JPMS (Java Modules)**: Each released module has `module-info.java`
   - Services declared in `module-info.java` only
   - `META-INF/services` generated automatically

## Development Guidelines (from DEV-GUIDELINES.md)

### Exception Handling
- Use **unchecked Throwables** (RuntimeException descendants) in public APIs
- Never use RuntimeException directly - create module-specific descendants
- Only use checked exceptions when implementing interfaces that require them

### Null Safety
- **No `null` in public APIs** - use `Optional` for return values
- For setter methods with null: create unset method instead (e.g., `unsetHost()`)
- Never use `Optional` as a parameter type

### Method Naming
- **No verbs**: Use direct property names
  - `port(int newPort)` and `int port()`
  - `authenticate(boolean atn)` and `boolean authenticate()`
- Boolean: use without verb unless ambiguous (`isAuthenticated()`)

### Fluent API
- Use fluent API in builders and control methods
- Example: `Server server = Server.create().start()`

### Testing Standards
- **JUnit 5** with **Hamcrest assertions**
- Use: `assertThat(actualValue, is(expectedValue))`
- Common imports:
  - `import static org.hamcrest.MatcherAssert.assertThat;`
  - `import static org.hamcrest.CoreMatchers.*;`
- For multiple assertions: `assertAll()`
- For exceptions: `assertThrows()`

## Build System

- **Maven 3.9.9+** with **Maven Wrapper** (`.mvn/` directory)
- **JDK 21** required
- Dependencies managed in `bom/pom.xml` (Bill of Materials)
- All module versions inherited from parent POM
- 29 top-level modules in reactor build

## CLI Tool

Helidon provides a CLI for project scaffolding:

```bash
# macOS
curl -O https://helidon.io/cli/latest/darwin/helidon
chmod +x ./helidon
sudo mv ./helidon /usr/local/bin/

# Linux
curl -O https://helidon.io/cli/latest/linux/helidon
chmod +x ./helidon
sudo mv ./helidon /usr/local/bin/

# Windows
PowerShell -Command Invoke-WebRequest -Uri "https://helidon.io/cli/latest/windows/helidon.exe" -OutFile "C:\Windows\system32\helidon.exe"
```

## CI/CD

GitHub Actions workflows in `.github/workflows/`:
- `release.yaml` - Release pipeline
- `snapshot.yaml` - Snapshot builds
- `nightly.yaml` - Nightly tests
- `validate.yml` - PR validation

## Important Files

- `pom.xml` (85.8 KB) - Main build configuration with 29 modules
- `README.md` - Project overview and quick start
- `DEV-GUIDELINES.md` - Comprehensive development rules
- `CHANGELOG.md` - Detailed change history
- `CONTRIBUTING.md` - Contribution guidelines
- `SECURITY.md` - Security policies
- `etc/scripts/` - Build and release automation scripts

## Documentation

- Latest docs: <https://helidon.io/docs/latest>
- Javadocs: <https://helidon.io/docs/latest/javadoc>
- Upgrade guides for Helidon 3→4 migration (API changes)
- White paper: <https://www.oracle.com/a/ocom/docs/technical-brief--helidon-report.pdf>

## License

Apache License 2.0