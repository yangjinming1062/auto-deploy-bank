# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Conductor is a microservices workflow orchestration engine built at Netflix and now maintained by Orkes. It enables developers to create distributed, asynchronous workflows that define interactions between services, databases, and external systems with resilience, scalability, and observability.

## Technology Stack

- **Backend**: Java 17, Spring Boot 3.3.5
- **Build System**: Gradle (uses Gradle wrapper - `./gradlew`)
- **UI**: React 18 with TypeScript, Material-UI
- **Persistence**: Redis (default), PostgreSQL, MySQL, Cassandra
- **Indexing**: Elasticsearch 7.x (default), OpenSearch 2.x
- **APIs**: REST and gRPC
- **Testing**: JUnit 5 with Spring Boot Test
- **Code Formatting**: Spotless with Google Java Format

## Repository Structure

Key modules (all prefixed with `conductor-`):

### Core Components
- **`server/`** - Main Spring Boot application (`Conductor.java` is entry point)
- **`core/`** - Orchestration engine (workflow execution, state machine, reconciliation)
- **`rest/`** - REST API layer
- **`grpc/`, `grpc-server/`, `grpc-client/`** - gRPC support

### Persistence Layer (pluggable)
- `redis-persistence/` - Default Redis persistence
- `postgres-persistence/` - PostgreSQL support
- `mysql-persistence/` - MySQL support
- `cassandra-persistence/` - Cassandra support
- `common-persistence/` - Shared persistence utilities
- `sqlite-persistence/` - SQLite support
- `es7-persistence/`, `es6-persistence/`, `os-persistence/` - Indexing backends

### Task & Event Modules
- `http-task/` - HTTP task type
- `json-jq-task/` - JSON transformation task
- `kafka/`, `kafka-event-queue/` - Kafka event handling
- `awssqs-event-queue/` - AWS SQS integration
- `amqp/`, `nats/`, `nats-streaming/` - Message queue integrations
- `azureblob-storage/`, `awss3-storage/`, `postgres-external-storage/` - Storage providers

### Utilities
- `test-harness/` - Integration testing framework with sample workflows
- `test-util/` - Testing utilities
- `annotations/` - Java annotations
- `annotations-processor/` - Annotation processing
- `ui/` - React web UI (requires Node 14+, uses yarn)

## Common Development Commands

### Building
```bash
# Build all modules
./gradlew build

# Build specific module
./gradlew :conductor-server:build

# Clean build
./gradlew clean build
```

### Running the Server

#### Development (Spring Boot)
```bash
# Run server with default config (in-memory, no persistence)
./gradlew :conductor-server:bootRun

# Run with specific config file
CONFIG_PROP=config-redis.properties ./gradlew :conductor-server:bootRun

# Configuration files are in docker/server/config/
```

#### Docker (recommended for local development with persistence)
```bash
# Start complete stack (server + Redis + Elasticsearch + UI)
docker compose -f docker/docker-compose.yaml up

# Access points:
# - REST API: http://localhost:8080
# - UI: http://localhost:8127
# - Swagger UI: http://localhost:8080/swagger-ui/index.html
```

### Running the UI
```bash
cd ui
yarn install
yarn start
```

### Testing
```bash
# Run all tests
./gradlew test

# Run tests for specific module
./gradlew :conductor-core:test

# Run integration tests
./gradlew :conductor-test-harness:test

# Run tests with coverage
./gradlew test jacocoTestReport
```

### Code Formatting

Auto-formatting is enforced via pre-commit hook:
```bash
# Install pre-commit hook
ln -s ../../hooks/pre-commit .git/hooks/pre-commit

# Manual formatting
./gradlew spotlessApply

# Check formatting without applying
./gradlew spotlessCheck
```

### Database Configurations

Available configurations in `docker/server/config/`:
- `config-redis.properties` - Redis + Elasticsearch (default)
- `config-redis-os.properties` - Redis + OpenSearch
- `config-postgres.properties` - PostgreSQL only
- `config-postgres-es7.properties` - PostgreSQL + Elasticsearch
- `config-mysql.properties` - MySQL + Elasticsearch

## Architecture Overview

Conductor uses a **worker-task queue architecture**:

1. **State Machine Evaluator** - Orchestrates workflows, schedules tasks to queues, monitors task states
2. **Task Queues** - Distributed FIFO queues per task type
3. **Task Workers** - Poll server via HTTP/gRPC every 100ms, execute tasks, update status
4. **Data Stores** - Persistent storage for workflow metadata, task queues, execution history
5. **APIs** - REST/gRPC for programmatic access

### Workflow Execution Flow
1. Client starts workflow → returns workflow ID
2. Conductor schedules first task to its queue
3. Workers poll and receive task
4. Worker executes and updates status (IN_PROGRESS, COMPLETED, FAILED)
5. On completion, Conductor schedules next tasks
6. Process repeats until workflow completes

### Key Packages in `core/`
- `core/execution/` - Workflow and task execution engine
- `core/events/` - Event handling and queue management
- `core/reconciliation/` - Workflow repair and consistency
- `core/dao/` - Data access objects
- `model/` - Domain models (Workflow, Task, etc.)
- `metrics/` - Monitoring and metrics

## Development Notes

- **Java Toolchain**: Project uses Java 17 with toolchain auto-provisioning
- **Spring Boot**: Server uses Spring Boot 3.3.5 with auto-configuration
- **Exclusions**: Logback is excluded; uses Log4j2 instead
- **Lombok**: Widely used for boilerplate reduction
- **Jackson**: For JSON serialization (version 2.18.0)
- **gRPC**: Uses protobuf for serialization

### Module Dependencies
- `server` depends on `core` + chosen persistence module + indexing backend
- `core` contains orchestration logic and DAOs
- Persistence modules are pluggable - only include needed one
- Test harness uses real workflow JSON files in `test-harness/src/test/resources/`

### Configuration
- External config via `CONDUCTOR_CONFIG_FILE` environment variable or system property
- Spring Boot external configuration precedence applies
- Database connection and queue settings configured via properties files

### Testing
- Integration tests in `test-harness/` use sample workflows in JSON
- Pre-commit hook runs Spotless formatter automatically
- Tests use JUnit 5 Platform with Spring Boot test support
- Example workflow files available in test resources for reference

## Useful Resources

- **Documentation**: `docs/` directory with dev guides
- **Architecture**: `docs/devguide/architecture/index.md`
- **API Docs**: http://localhost:8080/swagger-ui/index.html (when server running)
- **Community**: [Conductor Slack](https://join.slack.com/t/orkes-conductor/shared_invite/zt-2vdbx239s-Eacdyqya9giNLHfrCavfaA)
- **Building from Source**: `docs/devguide/running/source.md`