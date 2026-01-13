# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Apache Camel 4.17.0-SNAPSHOT is a Java-based integration framework that provides routing and mediation rules through domain-specific languages (Java, XML, Groovy, YAML). The project is organized as a multi-module Maven project with the following main modules:

- **core/** - Core Camel runtime and APIs (camel-api, camel-base, camel-core-engine, camel-main, camel-support, etc.)
- **components/** - 300+ integration components (activemq, aws, azure, http, kafka, etc.)
- **dsl/** - Domain-specific language implementations (Java, XML, YAML, Kamelet)
- **tooling/** - Development tools (Camel JBang, archetypes)
- **tests/** - Integration tests
- **test-infra/** - Reusable test infrastructure for simulating external services

## Development Requirements

- **Java**: Version 17 or higher (tested with OpenJDK)
- **Maven**: Version 3.9.6 or higher (use bundled `./mvnw` wrapper)
- **Memory**: At least 3.5GB RAM, 10GB disk space
- **Build Configuration**: `.mvn/jvm.config` sets JVM options (-Xmx3584m, G1GC, etc.)

## Common Build Commands

### Fast Build (Recommended for Development)
```bash
mvn clean install -Dquickly
```
Skips optional artifacts and tests for quick iteration (completes in ~30 minutes).

### Full Build with Tests
```bash
mvn clean install
```
Runs all unit tests (takes several hours).

### Build Specific Module
```bash
cd components/camel-aws2-s3
mvn clean install -Dquickly
```

### Run Tests
```bash
# All tests
mvn test

# Specific test class
mvn test -Dtest=MyTestClass

# Integration tests
mvn verify

# Run with test infra
mvn test -Dtestinfra.enabled=true
```

### Code Quality Checks
```bash
# Format code
mvn formatter:format

# Sort imports
mvn impsort:sort

# Check coding style
mvn clean install -Psourcecheck
```

### Build Profiles
```bash
# Build for deployment (source jars, javadoc, etc.)
mvn -Pfastinstall,deploy clean install

# Build source jars only
mvn -Pfastinstall,source-jar clean install

# Release build
mvn clean install -Prelease
```

### Maven Daemon (Faster Builds)
Experienced contributors can use `mvnd` instead of `mvn` for parallel builds:
```bash
mvnd clean install -Dquickly
```

## Testing Infrastructure

Camel provides reusable test infrastructure in `test-infra/` for:
- Message brokers (Kafka, NATS, RabbitMQ, etc.)
- Cloud services (AWS, Azure, GCP)
- Databases (PostgreSQL, MongoDB, etc.)

Usage example with JUnit 5:
```java
@RegisterExtension
static NatsService service = NatsServiceFactory.createService();
```

## Code Architecture

### Core Components

1. **camel-api** - Base APIs and interfaces
2. **camel-core-engine** - Core runtime engine
3. **camel-base** - Base implementation
4. **camel-support** - Utility classes and helpers
5. **camel-main** - Standalone Camel runtime

### Integration Components
Each component in `components/` follows a standard structure:
- `src/main/java/` - Component implementation
- `src/test/java/` - Unit tests
- `pom.xml` - Maven configuration

### DSL Implementation
- `camel-java-joor-dsl` - Java DSL using jOOR
- `camel-xml-jaxb-dsl` - XML DSL
- `camel-yaml-dsl` - YAML DSL
- `camel-kamelet-main` - Kamelet support

### Pattern: Route Definitions
Routes are typically defined using:
```java
from("timer:tick")
    .log("Hello ${body}")
    .to("direct:next");
```

## Development Guidelines

### Contributing Best Practices
- Follow existing code style (auto-formatted during full build)
- Write unit tests with proper assertions (no System.out logging)
- Use test-infra for external service simulation
- Avoid creating unnecessary Maven profiles
- Use default surefire/failsafe configurations when possible
- Reference JIRA issues in commit messages: `CAMEL-9999: Your message`

### Code Quality Requirements
- Camel 4 auto-formats code during full build (`mvn verify`)
- Manual formatting: `mvn formatter:format` and `mvn impsort:sort`
- Style checking: `-Psourcecheck` profile
- All tests must have assertions (no logging-only tests)

### Creating Reproducers
For bug reports, prefer:
1. JUnit test case in the relevant module
2. Sample project with Camel JBang
3. Route files or Kamelets

Example reproducer creation:
```bash
mvn archetype:generate -B \
    -DarchetypeGroupId=org.apache.camel.archetypes \
    -DarchetypeArtifactId=camel-archetype-java \
    -DarchetypeVersion=4.17.0-SNAPSHOT \
    -Dpackage=org.apache.camel \
    -DgroupId=org.apache.camel.reproducer \
    -DartifactId=reproducer-for-my-issue \
    -Dversion=1.0.0-SNAPSHOT
```

## Virtual Threads Support

To enable Virtual Threads (requires JDK 21+):
```bash
mvn clean install -Dcamel.threads.virtual.enabled=true
```

## Key Files and Directories

- `pom.xml` - Root Maven POM (version 4.17.0-SNAPSHOT)
- `.mvn/jvm.config` - JVM settings
- `Jenkinsfile` - CI/CD pipeline
- `mvnw` - Maven wrapper script
- `docs/` - Documentation (Antora-based)
- `buildingtools/` - Build tooling and license headers

## CI/CD Information

- **CI Server**: https://ci-builds.apache.org/job/Camel/
- **Issue Tracker**: https://issues.apache.org/jira/browse/CAMEL
- **SonarQube**: https://sonarcloud.io/project/overview?id=apache_camel

## Testing Tips

### Component Testing
When testing components that need external services:
1. Use test-infra services from `test-infra/camel-test-infra-*`
2. Register as JUnit 5 extensions
3. Access via service methods (varies by service)

### Core Testing
Core tests are in `core/camel-core/src/test/java/org/apache/camel/`

### Integration Tests
Located in `tests/` directory with the pattern:
- Component-specific integration tests in respective `components/*/src/test/`
- End-to-end tests in `tests/`

## Maven Configuration Notes

- Root POM uses Apache parent (version 35)
- Enforces Maven 3.9.6+ and Java 17+
- License headers checked via `license-maven-plugin`
- Code formatting via `formatter-maven-plugin` and `impsort-maven-plugin`
- Multiple profiles for different build types (quickly, release, deploy, source-jar)

## Documentation

- **Contributing**: `docs/main/modules/contributing/pages/index.adoc`
- **Building**: `docs/main/modules/contributing/pages/building.adoc`
- **User Manual**: Available at https://camel.apache.org/manual/
- **Component Catalog**: https://camel.apache.org/components/latest/
