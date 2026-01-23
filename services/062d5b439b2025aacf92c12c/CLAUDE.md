# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PowerJob is an enterprise-grade distributed job scheduling and computing framework. It consists of three main components:

- **Server**: Central scheduling node that manages jobs, workflows, and workers
- **Worker**: Task executor that runs jobs on worker nodes
- **Client**: API for submitting and managing jobs remotely

## Build & Development Commands

```bash
# Full build (development profile, skip tests)
mvn clean package -Pdev -DskipTests

# Build specific module
mvn -pl powerjob-server clean package -Pdev -DskipTests

# Run tests
mvn test

# Run single test class
mvn test -Dtest=ClassNameTest

# Run single test method
mvn test -Dtest=ClassNameTest#methodName

# Build for release (with javadoc, sources, GPG signing)
mvn clean package -Prelease
```

## Project Structure

```
powerjob/
├── powerjob-common/           # Shared utilities, models, enums, serialization
├── powerjob-client/           # Client API for job submission
├── powerjob-worker/           # Worker core (task execution, persistence, actors)
├── powerjob-worker-spring-boot-starter/  # Spring Boot auto-configuration
├── powerjob-worker-agent/     # Standalone agent with embedded server
├── powerjob-worker-samples/   # Example applications
├── powerjob-server/           # Server modules
│   ├── powerjob-server-core/  # Core scheduling logic (dispatch, workflow)
│   ├── powerjob-server-common/   # Server utilities
│   ├── powerjob-server-remote/   # Remote communication handlers
│   ├── powerjob-server-persistence/ # Storage service (file, S3, DB)
│   ├── powerjob-server-extension/  # Extension points
│   └── powerjob-server-starter/    # Spring Boot entry point
├── powerjob-remote/           # RPC framework
│   ├── powerjob-remote-framework/   # Base communication framework (Actor model)
│   └── powerjob-remote-impl-*/      # Transport implementations (Akka, HTTP)
└── powerjob-official-processors/    # Built-in processor implementations
```

## Architecture

### Communication Layer (Actor Model)

The system uses an Actor-based messaging model via `powerjob-remote-framework`:

- **Actors**: Process messages asynchronously using the Actor model
- **RemoteEngine**: Manages actor lifecycle and message routing
- **Transporters**: Handle network communication (Akka or HTTP implementations)
- **CSInitializerFactory**: Creates client/server connection initializers

Worker nodes expose actors: `TaskTrackerActor`, `ProcessorTrackerActor`, `WorkerActor`

### Server Core Components

- **DispatchService**: Distributes tasks to workers based on strategies
- **Scheduler services**: Handle timing strategies (CRON, fixed rate, delay)
- **Workflow engine**: Manages DAG-based workflow execution
- **Instance service**: Tracks job instance lifecycle

### Worker Core Components

- **ExecutorManager**: Manages processor thread pools
- **ProcessorLoader**: Loads user-defined job processors
- **TaskPersistenceService**: Local task state persistence (H2 + HikariCP)
- **ServerDiscoveryService**: Locates and connects to server nodes

## Key Configuration Files

- Server: `powerjob-server/powerjob-server-starter/src/main/resources/application.properties`
- Server profiles: `application-daily.properties`, `application-product.properties`
- Logging: `logback-dev.xml`, `logback-product.xml`

## Java Version

Java 8 is required (`java.version=1.8`).

## Testing Framework

JUnit 5 (`junit-jupiter`) is used for unit tests. Tests use standard Maven layout under `src/test/java/`.