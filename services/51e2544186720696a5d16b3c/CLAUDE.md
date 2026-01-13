# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Building

jBPM uses Maven for building. The project is organized as a multiproject build with ~15 major modules.

**Quick build:**
```bash
mvn clean install -DskipTests
```

**Full build (with tests):**
```bash
mvn clean install
```

**Run a single test:**
```bash
# Run a specific test class
mvn test -Dtest=ClassName

# Run a specific test method
mvn test -Dtest=ClassName#methodName

# Run tests for a specific module
cd jbpm-flow
mvn test
```

**Build profiles:**
- `fullProfile` - includes jbpm-distribution module (use with `-Dfull=true`)
- `run-code-coverage` - enables JaCoCo code coverage (use with `-Drun-code-coverage=true`)
- `mariadb` - uses MariaDB instead of H2
- `community-only` - excludes productized modules (activated when productized!=true)

**Build with code coverage:**
```bash
mvn clean install -Prun-code-coverage
```

## Testing

The project uses JUnit for testing. Tests are organized within each module's `src/test/java` directory.

**Run all tests:**
```bash
mvn test
```

**Skip tests during build:**
```bash
mvn clean install -DskipTests
```

**Run integration tests:**
```bash
cd jbpm-container-test/jbpm-in-container-test
mvn test
```

Some modules (jbpm-flow) have special profiles like `protobufProfile` that generate code from protobuf definitions.

## Database Configuration

Default database is H2 (in-memory). To use MariaDB:
```bash
mvn clean install -Pmariadb
```

Properties used for database configuration:
- `maven.hibernate.dialect`
- `maven.jdbc.driver.class`
- `maven.jdbc.url`
- `maven.jdbc.username`
- `maven.jdbc.password`

See pom.xml for MariaDB/MySQL/PostgreSQL profile configurations.

## Code Style

**Checkstyle:** Only validates Apache license header. Configuration is in root pom.xml (lines 42-59).

**Spotbugs:** Enabled with `spotbugs.failOnViolation` property.

## High-Level Architecture

jBPM is a business process management toolkit organized into the following core modules:

### Core Engine Modules
- **jbpm-flow** - Core BPM execution engine and process runtime
- **jbpm-flow-builder** - Compilation and building of BPMN2 processes
- **jbpm-bpmn2** - BPMN 2.0 process definition support
- **jbpm-bpmn2-emfextmodel** - EMF-based BPMN2 model extensions

### Persistence & Query
- **jbpm-persistence** - JPA persistence layer for process state
- **jbpm-query-jpa** - JPA-based querying for process instances

### Runtime Management
- **jbpm-runtime-manager** - Runtime management and deployment strategies

### Services
- **jbpm-services** - Service layer with multiple implementations:
  - EJB-based services
  - CDI-based services
  - Core services
  - Executor service for async work

### Human Task Management
- **jbpm-human-task** - Human task service for user interactions:
  - Core task service
  - JPA persistence
  - Audit trail
  - Workitems integration

### Work Items
- **jbpm-workitems** - Reusable work item handlers:
  - Email, REST, WebService
  - JMS, BPMN2 tasks
  - Template system for custom work items

### Additional Capabilities
- **jbpm-case-mgmt** - Case management (CMMN) support
- **jbpm-human-task** - Human task orchestration
- **jbpm-services** - Business process services
- **jbpm-audit** - Audit trail and history logging
- **jbpm-event-emitters** - Event emission to external systems (Kafka, Elasticsearch)
- **jbpm-xes** - XES export for process mining

### Testing & Examples
- **jbpm-test** - Core testing utilities and helpers
- **jbpm-test-util** - Shared testing utilities
- **jbpm-test-coverage** - Test coverage reporting
- **jbpm-examples** - Example applications
- **jbpm-container-test** - Integration testing in containers (WildFly/EAP)

### Distribution
- **jbpm-distribution** - Packaging and distribution (included with `-Dfull=true`)
- **jbpm-installer** - Installation and setup tools

## Key Classes/Entry Points

Common entry points to understand the codebase:
- Process runtime in `jbpm-flow`
- BPMN2 process definitions in `jbpm-bpmn2`
- Runtime managers in `jbpm-runtime-manager`
- Service abstractions in `jbpm-services/jbpm-services-api`
- Human task service in `jbpm-human-task/jbpm-human-task-core`

## Contribution Guidelines

**Pull Request Process:**
1. CI builds use build-chain tool for cross-repository dependencies
2. To trigger Jenkins builds: comment "Jenkins retest this" on the PR
3. Full downstream build: "Jenkins run fdb"
4. Compile downstream build: "Jenkins run cdb"
5. Upstream build: "Jenkins run upstream"
6. Backporting: add labels like `backport-<branch-name>` to auto-create backport PRs

**Before Contributing:**
Read the [Developing Drools and jBPM](https://github.com/kiegroup/droolsjbpm-build-bootstrap/blob/main/README.md) guide.

**Required Files:**
All source files must include the Apache 2.0 license header (checked by checkstyle).

## Deployment Options

jBPM supports multiple deployment models:
- Traditional JEE applications (WAR/EAR)
- SpringBoot or Thorntail (uberjar)
- Standalone Java programs

See http://jbpm.org/ for more information.

## Development Requirements

- Java 1.8 or higher
- Maven 3.x
- Git client

## External Dependencies

The project depends on:
- Drools (for rule engine integration)
- KIE (knowledge is everything) parent BOM
- Kie-soup BOM
- KIE DMN BOM

See dependencyManagement section in root pom.xml (lines 155-191).

## Process Mining

The jbpm-xes module provides XES export for process mining. See jbpm-xes/README.md for details on exporting process logs to XES format for tools like Celonis, ProM, or Disco.