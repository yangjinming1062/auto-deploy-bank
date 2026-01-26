# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PowerJob is an enterprise job scheduling middleware with distributed computing ability. It enables task scheduling and distributed computation with features including CRON scheduling, MapReduce, workflow (DAG), and multiple execution modes (standalone, broadcast, map, map-reduce).

## Build Commands

```bash
# Build project (skip tests for faster builds)
mvn -B clean package -Pdev -DskipTests

# Run all tests
mvn test

# Run single test class
mvn test -Dtest=TestClassName

# Run specific test in a module
mvn test -pl powerjob-server/powerjob-server-starter -Dtest=ServiceTest

# Build with release profile (for publishing to Maven Central)
mvn --batch-mode clean deploy -pl powerjob-worker,powerjob-client,powerjob-worker-spring-boot-starter,powerjob-official-processors,powerjob-worker-agent -DskipTests -Prelease -am
```

**Note**: The `dev` profile is active by default; `-Pdev` is optional. Java 8 is required.

## Development with Docker Compose

```bash
# Start all services (MySQL, server, worker samples)
docker-compose up

# Access points after startup:
# - Server UI: http://localhost:10010
# - Worker Sample App: http://localhost:8081
```

## Architecture

### Core Modules

- **powerjob-server** - Scheduling server with multiple sub-modules:
  - `powerjob-server-core` - Core scheduling logic (DispatchService, scheduler, workflow engine)
  - `powerjob-server-starter` - Spring Boot entry point with web controllers
  - `powerjob-server-persistence` - JPA repository layer for data storage
  - `powerjob-server-remote` - Remote transport layer for worker communication
  - Other modules: auth, extension, migrate, monitor

- **powerjob-worker** - Worker SDK that runs task processors:
  - Main entry: `PowerJobWorker` class
  - Uses Actor model: `TaskTrackerActor`, `ProcessorTrackerActor`, `WorkerActor`
  - `core/executor/` - Task execution engine
  - `processor/` - Processor loading and execution (BuiltIn, JarContainer)
  - `actors/` - Message handling actors for server communication

- **powerjob-remote** - Pluggable remote communication framework:
  - `powerjob-remote-framework` - Base transport abstractions using Actor model
  - `powerjob-remote-impl-akka` - Akka-based implementation (default)
  - `powerjob-remote-impl-http` - HTTP-based implementation

- **powerjob-common** - Shared constants, enums, utilities, and request/response models
- **powerjob-client** - Client SDK for OpenAPI interaction with server
- **powerjob-worker-spring-boot-starter** - Spring Boot auto-configuration integration
- **powerjob-official-processors** - Built-in processor implementations

### Communication Pattern

1. Server uses `DispatchService` to dispatch jobs to Workers
2. Server ↔ Worker communication uses remote framework (Actor-based Akka by default)
3. Workers report status back via actors
4. Task results stored via TaskPersistenceService (configurable strategy)

### Task Execution Types

- **STANDALONE**: Single worker executes the task
- **BROADCAST**: All registered workers execute the task
- **MAP**: Task is split into sub-tasks distributed across workers
- **MAP_REDUCE**: Map phase followed by reduce phase for distributed computing

### Timing Strategies

- **CRON**: Cron expression based scheduling
- **FIXED_RATE**: Fixed rate execution (every N milliseconds)
- **FIXED_DELAY**: Fixed delay between executions (wait N ms after completion)
- **API**: OpenAPI triggered execution (manual triggering)

### Task Trackers

Workers use TaskTrackers to manage task execution:
- **LightTaskTracker**: For STANDALONE and BROADCAST execution (simple task tracking)
- **HeavyTaskTracker**: For MAP and MAP_REDUCE execution (handles sub-task distribution and status aggregation)

### Key Components

- **DispatchService** (`powerjob-server-core`) - Routes jobs to workers
- **InstanceManager** - Manages job instance lifecycle
- **TransportService** - Server-side remote communication handler
- **ExecutorManager** - Worker-side thread pool and task execution
- **ProcessorLoader** - Loads and manages task processors
- **TaskTracker** - Worker-side task execution tracking (LightTaskTracker, HeavyTaskTracker)
- **WorkflowEngine** - DAG-based workflow execution and dependency management

## powerjob-common Module Structure

The common module contains:
- **Enums**: ExecuteType, TimeExpressionType, InstanceStatus, Protocol, ProcessorType, LogLevel, etc.
- **Constants**: OmsConstant, RemoteConstant, OpenAPIConstant, WorkflowContextConstant
- **Models**: InstanceDetail, TaskDetailInfo, AlarmConfig, PEWorkflowDAG, SystemMetrics
- **Request/Response**: HTTP and internal RPC request/response classes
- **Serialization**: JsonUtils for JSON serialization
- **Utilities**: CommonUtils, NetUtils, HttpUtils, DigestUtils, CollectionUtils

## Technology Stack

- Java 8
- Maven (multi-module)
- Spring Boot (server)
- Akka / HTTP (remote transport)
- JPA with MySQL (default persistence)

## Configuration

Server configuration uses `application.properties` or `application.yml`:
- `spring.datasource.*`: Database configuration
- `oms.*`: PowerJob server settings
- Port 7700: Akka/HTTP remote communication
- Port 10086: HTTP API (OpenAPI)
- Port 10010: Server web UI

## Actor Pattern

The remote framework uses an Actor-based message passing pattern:
- Classes extending `Actor` base class with `@Actor(path = "...")` annotation
- Message handlers use `@Handler(path = "...")` annotation
- Server ↔ Workers communicate via Actor messages over the remote transport

**Worker Actors:**
- `TaskTrackerActor` - Receives task scheduling requests from server
- `WorkerActor` - Handles worker registration and health reporting
- `ProcessorTrackerActor` - Manages processor information and status