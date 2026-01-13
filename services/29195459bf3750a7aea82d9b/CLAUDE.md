# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Apache NiFi is an easy to use, powerful, and reliable system to process and distribute data. It's a Java-based data flow and distribution platform with a web-based UI for designing, controlling, and monitoring data flows. The project includes several sub-projects: Apache NiFi (main dataflow engine), Apache NiFi Registry (flow versioning), and Apache NiFi MiNiFi (lightweight edge agent).

## Requirements

- **Java 21** (minimum version enforced by maven-enforcer-plugin)
- **Python 3.10+** (optional, for Python-based processors)
- **Maven 3.9.11+** (provided via Maven Wrapper - use `./mvnw`)

## Common Commands

### Building

```bash
# Build all modules with parallel execution
./mvnw install -T1C

# Build with code compliance checks (Checkstyle, PMD, Apache RAT)
./mvnw install -T1C -P contrib-check

# Build only the main NiFi distribution (skips optional modules)
./mvnw install -T1C -am -pl :nifi-assembly

# Clean build
./mvnw clean install -T1C
```

### Testing

```bash
# Run unit tests
./mvnw test

# Run tests for a specific module
./mvnw test -pl :nifi-commons

# Run a specific test class
./mvnw test -Dtest=TestClassName

# Run tests matching a pattern
./mvnw test -Dtest="*Test"

# Run integration tests only
./mvnw verify -P integration-tests

# Skip unit tests, run only integration tests
./mvnw verify -P integration-tests -P skip-unit-tests

# Run tests with parallel execution
./mvnw test -T1C
```

### Code Quality

```bash
# Run Checkstyle checks
./mvnw checkstyle:check

# Run PMD analysis
./mvnw pmd:check

# Run Apache RAT license checks
./mvnw rat:check

# Run all contrib-check validations
./mvnw validate -P contrib-check
```

### Working with NARs (NiFi Archives)

NiFi uses a custom NAR (NiFi Archive) packaging format for extensions. Key commands:

```bash
# Build a NAR module
./mvnw clean install -pl :nifi-standard-processors -am

# The NAR plugin is configured in pom.xml with:
# <artifactId>nifi-nar-maven-plugin</artifactId>
# with extensions=true
```

NARs are created for:
- Framework NARs (nifi-server-nar, nifi-jetty-nar)
- Extension bundles (all processors and controller services)
- Framework extensions

## Code Architecture

### Core Modules

- **nifi-commons** - Shared utilities and common components used across NiFi
  - Expression language parser
  - Security utilities
  - Web client libraries
  - Metrics and monitoring
  - Property encryption
  - JSON/Record processing utilities

- **nifi-framework-bundle** - Core framework implementation
  - **nifi-framework** - Core runtime (flow controller, processors, scheduling)
  - **nifi-framework-extensions** - Built-in framework extensions
  - **nifi-framework-nar** - Framework NAR bundling
  - **nifi-server-nar** / **nifi-jetty-nar** - Server and Jetty NARs

- **nifi-extension-bundles** - All processor and controller service extensions
  - Each bundle contains processors for specific services (AWS, Azure, Kafka, etc.)
  - Structured as individual Maven modules
  - Packaged as NARs for deployment

- **nifi-assembly** - Binary distribution assembly
  - Creates the final NiFi distribution zip
  - Contains run scripts, configuration, and all NARs

- **nifi-registry** - Flow versioning and registry service
- **nifi-stateless** - Stateless dataflow engine
- **nifi-toolkit** - CLI utilities for NiFi administration
- **minifi** - Lightweight edge agent (separate sub-project)
- **c2** - Command and control framework

### Packaging Types

- **pom** - Parent/aggregator modules
- **nar** - NiFi Archive (custom format for NiFi extensions)
- **jar** - Standard Java libraries
- **war** - Web archives (for certain web components)

## Code Quality Standards

### Checkstyle
- Configuration: `checkstyle.xml` (in repository root)
- Max line length: 200 characters
- Enforced via `maven-checkstyle-plugin`

### PMD
- Configuration: `pmd-ruleset.xml`
- Rulesets: Best practices, code style, unused code
- Excludes: Generated sources, ANTLR parsers

### Unit Testing
- Framework: JUnit 5 (junit-jupiter)
- Mocking: Mockito
- Test pattern: `*Test.java` or `Test*.java`
- Location: `src/test/java`
- Test output redirected to files by default

### Integration Testing
- Framework: Maven Failsafe Plugin
- Profile: `integration-tests`
- Pattern: `*ITSpec.java` (excluded from surefire)
- Executed during `verify` phase

## Key Development Practices

### NAR Development
- Extensions (Processors, Controller Services) must be packaged as NARs
- NARs are loaded at runtime by the NiFi framework
- Use `nifi-nar-maven-plugin` for packaging
- Each NAR can contain multiple related processors/services
- Documentation generation is enforced for NARs

### Dependency Management
- Root `pom.xml` manages all dependency versions via dependencyManagement
- Bills of Materials (BOM) used for:
  - Jetty (`jetty-bom`, `jetty-ee11-bom`)
  - Jackson (`jackson-bom`)
  - Jersey (`jersey-bom`)
  - Spring (`spring-framework-bom`, `spring-security-bom`)
  - And many others

### Logging
- SLF4J for logging facade
- Logback for implementation
- Configuration: `logback.xml` in runtime

### Security
- BouncyCastle for cryptography
- TLS/SSL throughout
- Single sign-on support (OIDC, SAML)
- Encrypted configuration properties

## IDE Support

- Project uses Maven - import into any Maven-capable IDE
- Checkstyle and PMD integration available in most IDEs
- Java 21 language level required
- Generated sources in `target/generated-sources/` should be excluded from code reviews

## Web UI

NiFi includes a frontend web application built with:
- Node.js (managed via frontend Maven plugin)
- Angular/TypeScript
- Built as part of the Maven build process
- Deployed as part of the NiFi Assembly

## API Documentation

- REST API documentation via Swagger/OpenAPI
- Javadoc generated during build
- Available at: https://javadoc.io/doc/org.apache.nifi/nifi-api

## License Compliance

All source files must include the Apache License 2.0 header. The `contrib-check` profile includes:
- Apache RAT license checker
- Ensures proper license headers
- Checks for approved licenses only

## Performance Considerations

- Uses Java 21 features (GC, performance improvements)
- Netty for async I/O
- Back-pressure handling built into framework
- Clustering support for horizontal scaling
- Write-ahead logging (WAL) for provenance

## Testing Infrastructure

- TestContainers used for integration tests requiring external services
- Mock framework for unit testing
- Headless mode for tests (`java.awt.headless=true`)
- Parallel test execution supported (`-T1C`)

## Resources

- [NiFi Documentation](https://nifi.apache.org/documentation/)
- [Developer Guide](https://nifi.apache.org/documentation/nifi-latest/html/developer-guide.html)
- [User Guide](https://nifi.apache.org/documentation/nifi-latest/html/user-guide.html)
- [Apache NiFi Jira](https://issues.apache.org/jira/browse/NIFI) - for issue tracking
- [Dev Mailing List](https://mail-archives.apache.org/mod_mbox/nifi-dev)
- [Slack Community](https://apachenifi.slack.com/)