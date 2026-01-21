# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start

This is the **Kogito Runtimes** project - a cloud-native business automation platform that implements the CNCF Serverless Workflow specification. Kogito supports both Quarkus and Spring Boot runtimes.

### Requirements
- Java 17 or later
- Maven 3.9.6 or later
- Optional: Docker for integration tests

## Common Commands

### Build Commands
```bash
# Full build (includes all tests)
make build
# or
./mvnw clean install

# Quick build (skips slow tests/plugins for faster iteration)
make build-quickly
# or
./mvnw clean install -Dquickly

# Run unit tests only
make quick-test
# or
./mvnw clean verify -DquickTests

# Run all tests (unit + integration)
make test
# or
./mvnw clean verify

# Run a single test
./mvnw test -Dtest=ClassName#methodName

# Generate test coverage report
mvn clean verify -Ptest-coverage
# Report generated in: target/site/jacoco/
```

### Additional Commands
```bash
# Clean build artifacts
make clean
# or
./mvnw clean

# Deploy artifacts
make deploy
# or
./mvnw deploy

# Show project dependencies
make tree
# or
./mvnw dependency:tree

# Format copyright headers
mvn com.mycila:license-maven-plugin:format

# Run specific Maven command
make mvn cmd="<your-maven-command>"
```

### Build Chain Commands (for cross-repo builds)
```bash
# Build upstream projects
make build-upstream

# Build projects from a PR
make build-pr pr_link="<pr-url>"
```

## Code Architecture

### Main Modules

**1. `/api`** - Core API definitions
   - `kogito-api`: Base API definitions for processes, rules, and decisions
   - `kogito-services`: Common service implementations
   - `kogito-events-*`: Event handling APIs
   - `kogito-timer`: Timer/scheduling functionality

**2. `/jbpm`** - Business Process Management
   - `jbpm-flow`: Core BPMN engine
   - `jbpm-flow-builder`: BPMN process compiler
   - `jbpm-bpmn2`: BPMN 2.0 XML support
   - `jbpm-usertask`: Human task management

**3. `/drools`** - Rules Engine (Drools integration)
   - `kogito-drools`: Rule evaluation engine
   - `kogito-dmn`: Decision Model Notation (DMN)
   - `kogito-pmml`: Predictive Model Markup Language
   - `kogito-scenario-simulation`: Test simulation framework

**4. `/kogito-codegen-modules`** - Code Generation
   - `kogito-codegen-api`: Generator API contract
   - `kogito-codegen-core`: Code generation orchestration
   - `kogito-codegen-processes`: Process (BPMN) code generation
   - `kogito-codegen-decisions`: DMN decision code generation
   - `kogito-codegen-rules`: Rules code generation
   - `kogito-codegen-events`: Event handling code generation

**5. `/kogito-serverless-workflow`** - Serverless Workflow Implementation
   - Implements CNCF Serverless Workflow spec v0.8
   - Runtime executor and builders
   - OpenAPI, REST, gRPC, and Kafka integrations
   - Expression support (jq, jsonpath)

**6. `/quarkus`** - Quarkus Integration
   - Quarkus extensions for Kogito
   - Integration tests
   - Native image compilation support

**7. `/springboot`** - Spring Boot Integration
   - Spring Boot starters
   - Auto-configuration
   - Integration tests

**8. `/addons`** - Optional Extensions
   - Monitoring, tracing, persistence
   - Events, messaging, jobs
   - Kubernetes, Knative integration

### Code Generation Architecture

The codegen system follows a plugin architecture:

1. **Generator Interface** (`kogito-codegen-api`): Each component (processes, rules, decisions) implements the `Generator` interface
2. **ApplicationGenerator** (`kogito-codegen-core`): Main entry point that orchestrates all generators
3. **Build Context** (`KogitoBuildContext`): Platform-specific context (Quarkus/Spring/Java) shared across generators
4. **Generated Files**: Generators produce `GeneratedFile` instances without writing to disk directly

Generators can be wired manually or via SPI (Service Provider Interface) using `ApplicationGeneratorDiscovery`.

### Testing Strategy

- **Unit Tests**: Use `@QuarkusTest` for Quarkus-specific unit tests
- **Integration Tests**: Use `@QuarkusIntegrationTest` (*IT.java) for failsafe-plugin, static resources available in `META-INF/resources/`
- **Code Generation Tests**: Use `kogito-codegen-integration-tests` module for testing generated code compilation and execution
- **Parameterized Tests**: Use `KogitoContextTestUtils.contextBuilders()` to test across different build contexts (Quarkus/Spring/Java)

## Development Guidelines

### IDE Setup

Configure Eclipse or IDEA code style using files in `/kogito-build/kogito-ide-config/src/main/resources/`:
- `eclipse-format.xml`: Code formatter
- `eclipse.importorder`: Import organization

For IntelliJ IDEA, install the "Eclipse Code Formatter" plugin and configure it to use the Eclipse formatter settings.

### Contribution Guidelines

- All PRs must reference an existing GitHub issue
- One issue per PR
- Branch naming convention: `Fix_#<issue-number>` or `Fix_#<issue-number>-<description>`
- Do NOT use `@author` tags in Javadoc
- Dependencies must be Apache 2.0 compatible and available in Maven Central or JBoss Nexus
- No fat jars or shaded jars allowed
- Include tests for all new features

### License and Copyright

Copyright headers are enforced during build. Run `mvn com.mycila:license-maven-plugin:format` to automatically format files.

## Key Technologies

- **Maven** - Build system (use `./mvnw` wrapper)
- **Quarkus** - Primary runtime (especially for Serverless Workflow)
- **Spring Boot** - Secondary runtime
- **jbpm** - BPMN engine
- **Drools** - Rules engine
- **TestContainers** - Integration testing (requires Docker)

## Known Issues

- TestContainers may fail with "Can not connect to Ryuk at localhost" on some Docker for Mac versions
- Workaround: `export TESTCONTAINERS_RYUK_DISABLED=true`

## Resources

- **Documentation**: https://kie.apache.org/docs/documentation/
- **Examples**: https://github.com/apache/incubator-kie-kogito-examples
- **Serverless Workflow Spec**: https://serverlessworkflow.io/
- **GitHub Issues**: https://github.com/apache/incubator-kie-issues/issues
- **Zulip Chat**: https://kie.zulipchat.com/