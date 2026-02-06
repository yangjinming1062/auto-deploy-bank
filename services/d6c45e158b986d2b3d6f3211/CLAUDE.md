# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Genie is a federated Big Data orchestration and execution engine developed by Netflix. It's a multi-module Gradle project that orchestrates job execution across compute clusters, handling binary management, job submission, and monitoring.

## Build Commands

```bash
# Full build with all tests
./gradlew build

# Run unit tests only (skip integration tests)
./gradlew test

# Run integration tests (requires database - set INTEGRATION_TEST_DB env var)
INTEGRATION_TEST_DB=mysql ./gradlew genie-web:integrationTest
INTEGRATION_TEST_DB=postgresql ./gradlew genie-web:integrationTest

# Run a single test class
./gradlew :genie-web:test --tests "com.netflix.genie.web.data.services.JobPersistenceServiceImplTest"

# Run a single test method
./gradlew :genie-web:test --tests "com.netflix.genie.web.data.services.JobPersistenceServiceImplTest.getJobId"

# Build Docker images (requires Docker running)
./gradlew dockerBuildAllImages

# Build documentation
./gradlew asciidoctor javadoc

# Build without running checks
./gradlew build -x check
```

## Architecture

### Module Structure

The project is organized into three deployment tiers:

**Server Tier:**
- `genie-web` - Main Spring Boot application containing the REST API and job orchestration logic
- `genie-app` - Self-contained server deployment (fat JAR wrapping genie-web)
- `genie-swagger` - Swagger/OpenAPI configuration for REST API documentation

**Agent Tier:**
- `genie-agent` - Agent library for job execution on remote nodes
- `genie-agent-app` - Self-contained agent CLI application
- `genie-client` - REST client library for interacting with Genie servers

**Shared Libraries:**
- `genie-common` - Common utilities (no external dependencies)
- `genie-common-internal` - Internal shared code (Spring dependencies)
- `genie-common-external` - External client-facing shared code
- `genie-proto` - Protocol Buffers definitions and gRPC services
- `genie-test` / `genie-test-web` - Testing utilities

**Other:**
- `genie-ui` - React-based web UI for job visualization
- `genie-demo` - Demo application with Docker Compose
- `genie-docs` - Documentation templates

### Key Package Categories

**Server (genie-web):**
- `com.netflix.genie.web.apis.rest.v3.controllers` - REST API v3 endpoints
- `com.netflix.genie.web.agent.*` - Agent communication, launching, and lifecycle
- `com.netflix.genie.web.data.services` - Data persistence and JPA repositories
- `com.netflix.genie.web.data.entities` - JPA entities (JobEntity, ClusterEntity, CommandEntity, ApplicationEntity)
- `com.netflix.genie.web.jobs.*` - Job execution workflow and lifecycle
- `com.netflix.genie.web.selectors.*` - Resource selection strategies (cluster, command)

**Agent (genie-agent):**
- `com.netflix.genie.agent.cli` - Command-line interface arguments
- `com.netflix.genie.agent.execution` - Execution context and services
- `com.netflix.genie.agent.rpc` - gRPC communication with server

### API Architecture

**REST API (v3):**
- Resources: Applications, Clusters, Commands, Jobs
- Hateoas-enabled with ModelAssembler pattern
- Spring Data JPA for persistence (PostgreSQL, MySQL, MariaDB, H2)

**gRPC API (v4):**
- Proto definitions in `genie-proto`
- Agent-server communication for job control
- Services: JobSubmission, HeartBeat, JobKill, FileStreaming

### Data Layer

- Uses JPA/Hibernate with Spring Data repositories
- Database migrations via Flyway (`db/migration` in genie-web)
- Supports PostgreSQL, MySQL, MariaDB for production; H2 for tests
- Entities follow naming patterns: `*Entity` with `*Repository` for persistence
- DTO conversion between entities and API responses via `EntityV3DtoConverters`/`EntityV4DtoConverters`

## Key Technologies

- **Build**: Gradle with Java 8 toolchain (builds on JDK 17)
- **Framework**: Spring Boot 2 (legacy modules) and Spring Boot 3 (agent, web)
- **Communication**: gRPC + Protocol Buffers, REST (Spring MVC)
- **Database**: Spring Data JPA with Flyway migrations
- **Discovery**: Apache Curator (Zookeeper integration)
- **Testing**: Spock framework with Groovy, JUnit 5, Testcontainers
- **Observability**: Micrometer + Zipkin/Brave for tracing

## Code Standards

- Checkstyle configured (see `config/checkstyle/checkstyle.xml`)
- SpotBugs for bug detection (see `config/spotbugs/excludeFilter.xml`)
- All Java code uses Project Lombok for boilerplate reduction
- Mockito available via Spock mocking annotations
- JCIP annotations for thread-safety documentation

## Common Patterns

- **Repositories**: Extend `JpaRepository` or custom repository interfaces in `*Repository` classes
- **Services**: Interface + Impl pattern in `services/impl/`
- **REST Controllers**: Use `ModelAssembler` classes for Hateoas response building
- **Retry Logic**: Spring Retry with `@Retryable` annotation and `DataServiceRetryAspect`
- **Events**: Spring ApplicationEvents for async notification
- **Aspects**: Used for metrics, retry, and cross-cutting concerns