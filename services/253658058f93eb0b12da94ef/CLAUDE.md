# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Apache ServiceComb Java Chassis is a Java SDK for rapid microservices development, providing service registration, discovery, dynamic routing, and service management. It's a multi-module Maven project using Java 17 and Spring Boot 3.x.

**Current version:** 3.4.0-SNAPSHOT (Java Chassis 3.x)
**JDK requirement:** OpenJDK 17
**Spring Boot version:** 3.5.4

## Common Commands

### Building and Testing

```bash
# Build and run all tests
mvn clean install

# Build and run integration tests (requires Docker)
mvn clean install -Pdocker -Pit

# Build with Docker machine
mvn clean install -Pdocker -Pit -Pdocker-machine

# Run tests without integration tests
mvn clean test

# Run a single test
mvn test -Dtest=TestClassName

# Run tests for a specific module
cd core && mvn test

# Skip tests during build
mvn clean install -DskipTests=true

# Generate test coverage report
mvn clean install -Pjacoco -Pit -Pcoverage
```

### Code Quality Checks

```bash
# Run checkstyle
mvn checkstyle:check

# Run spotbugs
mvn spotbugs:check

# Check license headers
mvn apache-rat:check

# Check for typos
typos

# Generate dependency vulnerability report
mvn org.owasp:dependency-check-maven:aggregate -Powasp-dependency-check
```

### Profile Activation

- **docker**: Builds Docker images for integration tests
- **it**: Includes integration tests and demo modules
- **jacoco**: Enables JaCoCo for coverage
- **coverage**: Includes coverage reporting modules
- **owasp-dependency-check**: Runs security vulnerability checks
- **release**: Prepares for release (includes distribution module, GPG signing, sources/javadoc generation)

## Code Architecture

### Module Structure

**core (java-chassis-core)**
- Central orchestration module containing the main ServiceComb runtime
- Depends on foundation-vertx, foundation-registry, swagger modules, and governance
- Integrates Spring Boot auto-configuration
- Contains tracing integration (Brave), validation (Hibernate Validator)

**foundations**
Foundation modules providing low-level capabilities:
- **foundation-spi**: Service Provider Interface definitions
- **foundation-vertx**: Vert.x integration and event bus
- **foundation-common**: Common utilities and helpers
- **foundation-config**: Configuration management
- **foundation-metrics**: Metrics collection and reporting
- **foundation-ssl**: SSL/TLS support
- **foundation-protobuf**: Protocol Buffers integration
- **foundation-registry**: Service registry abstraction
- **foundation-test-scaffolding**: Testing utilities

**handlers**
Chain of responsibility pattern for request processing:
- **handler-fault-injection**: Fault injection for testing
- **handler-flowcontrol-qps**: Rate limiting and QPS control
- **handler-governance**: Service governance policies
- **handler-loadbalance**: Load balancing strategies
- **handler-publickey-auth**: Public key authentication
- **handler-router**: Request routing logic
- **handler-tracing-zipkin**: Zipkin distributed tracing

**transports**
Communication layer implementations:
- **transport-highway**: High-performance binary protocol
- **transport-common**: Common transport utilities

**swagger**
OpenAPI/Swagger integration:
- **swagger-generator-core**: Core API generation logic
- **swagger-invocation-core**: Request invocation and processing

**providers**
Service provider implementations for different frameworks:
- **provider-pojo**: Plain Old Java Objects
- **provider-springmvc**: Spring MVC integration
- **provider-jaxrs**: JAX-RS (Jakarta RESTful Web Services)
- **provider-rest-common**: Common REST functionality

**service-registry**
Service discovery and registration implementations:
- **registry-local**: In-memory registry (development/testing)
- **registry-service-center**: Apache ServiceComb Service Center
- **registry-consul**: HashiCorp Consul
- **registry-nacos**: Alibaba Nacos
- **registry-zookeeper**: Apache ZooKeeper
- **registry-etcd**: etcd
- **registry-zero-config**: Huawei Zero Config
- **registry-lightweight**: Lightweight client-only registry

**spring-boot**
- Spring Boot 3.x integration and auto-configuration
- Spring Boot Starter

**edge**
- Edge service/gateway implementation for API gateway patterns

**tracing**
- Distributed tracing integration (Zipkin/Brave)

**metrics**
- Metrics collection, aggregation, and reporting

**dynamic-config**
- Dynamic configuration management and updates

**governance**
- Service governance engine for policies like rate limiting, circuit breaking

**demo**
- Example applications demonstrating various use cases:
  - demo-pojo, demo-jaxrs, demo-springmvc: Provider examples
  - demo-cse-v1, demo-cse-v2: CSE (Cloud Service Engine) scenarios
  - demo-edge: Edge service gateway example
  - demo-consul, demo-nacos, demo-etcd, demo-zookeeper: Registry integrations
  - demo-local-registry, demo-multi-registries: Registry testing
  - demo-filter: Filter chain examples
  - demo-crossapp, demo-multiple: Multi-service applications

### Key Development Practices

**Dependency Injection Pattern:**
- Uses Spring Boot's auto-configuration heavily
- Core module provides Spring Boot auto-configuration for all components
- SPI (Service Provider Interface) pattern extensively used in foundations module

**Request Processing Flow:**
Client Request → Transport Layer → Handlers Chain (governance, loadbalance, routing, tracing) → Provider

**Service Discovery:**
- Multiple registry implementations via registry module
- Service registry abstraction in foundation-registry
- Configurable discovery client selection

**Configuration:**
- Spring Boot configuration properties
- foundation-config module for additional configuration sources
- Dynamic configuration support via dynamic-config module

## Code Style and Quality Standards

**Checkstyle Configuration:**
- Configuration: `ci/checkstyle/checkstyle.xml`
- Suppressions: `ci/checkstyle/suppressions.xml`
- Enforces: No tabs, no trailing whitespace, proper imports, naming conventions

**Static Analysis:**
- SpotBugs with Medium threshold
- Configuration: `ci/spotbugs/exclude.xml`
- Integrated into build pipeline

**License Headers:**
- All files must have Apache License 2.0 header
- Validated by Apache RAT plugin
- See LICENSE and NOTICE files

**Testing:**
- Uses JUnit with JMockit for mocking
- Integration tests require Docker via maven-failsafe-plugin
- Forked test execution with 2 parallel forks
- JaCoCo for coverage reporting

**Typo Checking:**
- Configuration: `.typos.toml`
- Common exceptions: Vertx, VERTX (Vert.x framework terms)

## Integration Tests

Integration tests are in the `demo` module and require Docker. They test end-to-end scenarios including:
- Service registration and discovery
- Multiple transport protocols
- Handler chains
- Various service registry implementations

Run with: `mvn clean install -Pdocker -Pit`

## CI Pipeline

GitHub Actions workflows in `.github/workflows/`:
- **maven.yml**: Main build with compilation, testing, integration tests, and coverage
- **checkstyle.yml**: Code style validation
- **rat_check.yml**: License header validation
- **typo_check.yml**: Typo detection
- **linelint.yml**: Line length checks

CI build command:
```bash
mvn clean verify -Dcheckstyle.skip=true -B -Pdocker -Pjacoco -Pit -Pcoverage
```