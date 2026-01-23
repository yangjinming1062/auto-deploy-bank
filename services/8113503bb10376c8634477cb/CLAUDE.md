# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

XXL-JOB is a distributed task scheduling framework with a central调度中心 (scheduling center) and distributed 执行器 (executors). The system uses a central-based scheduler with HA support, and tasks execute distributedly across executor clusters.

## Build & Test Commands

```bash
# Build all modules (skips tests by default)
mvn clean package -DskipTests

# Build with GPG signing (release profile)
mvn clean package -Prelease

# Run all tests
mvn test

# Run a specific test class
mvn test -Dtest=XxlJobInfoDaoTest

# Run a specific test method
mvn test -Dtest=XxlJobInfoDaoTest#testList

# Build single module (e.g., core only)
mvn clean package -pl xxl-job-core -am

# Install to local Maven repository
mvn install -DskipTests
```

**Prerequisites:** Java 17, Maven 3.6+

## Module Structure

- **xxl-job-core**: Shared core library containing:
  - `biz/` - RPC interfaces (AdminBiz, ExecutorBiz) and client implementations
  - `executor/` - Task execution framework (XxlJobExecutor)
  - `handler/` - Built-in job handlers and annotation processing (@XxlJob)
  - `server/` - Embedded Netty HTTP server for executor RPC
  - `glue/` - Dynamic code execution (Groovy, script support)
  - `thread/` - Execution threads, schedule threads
  - `context/` - Job context (XxlJobContext, ShardingUtil)
  - `enums/` - Route strategies, glue types, trigger status

- **xxl-job-admin**: Scheduling center web application (Spring Boot)
  - `controller/` - REST APIs and FreeMarker views (JobInfo, JobLog, JobGroup, JobUser, JobApi)
  - `service/` - Business logic layer (XxlJobService)
  - `dao/` - MyBatis mappers for xxl_job tables
  - `core/scheduler/` - Cron parsing and schedule triggering
  - `core/route/` - Executor routing strategies (First, Last, Round, Random, etc.)
  - `core/trigger/` - Trigger execution logic
  - `core/alarm/` - Failure notification (email, custom implementations)
  - `core/complete/` - Callback handling after job execution

- **xxl-job-executor-samples**: Example executors
  - `xxl-job-executor-sample-springboot`: Spring Boot integration
  - `xxl-job-executor-sample-frameless`: Lightweight embeddable executor
  - `xxl-job-executor-sample-ai`: AI integration with Spring AI, Ollama, Dify

## Architecture Patterns

### RPC Communication
- **Admin → Executor**: HTTP via Netty embedded server (ExecutorBiz client)
- **Executor → Admin**: HTTP callback for job results (AdminBiz client)
- Access token authentication via `xxl.job.accessToken`

### Scheduling Flow
1. SchedulerThread monitors xxl_job_info for tasks due to execute
2. Cron expression parsing via CronExpression class
3. TriggerThread acquires DB lock and triggers job execution
4. Route strategy selects target executor from registry
5. HTTP request sent to executor's Netty server
6. Executor runs handler and sends callback response
7. CompleteThread processes callback, logs results, triggers child jobs

### Key Data Flow
- `xxl_job_registry`: Executor heartbeats (app_name → address)
- `xxl_job_info`: Job definitions with schedule config
- `xxl_job_log`: Execution records with trigger/execute status
- `xxl_job_group`: Executor app_name groupings

## Configuration Files

- **xxl-job-admin/src/main/resources/application.properties**: Admin server config
  - DB connection: `spring.datasource.url`
  - Email: `spring.mail.*`
  - Access token: `xxl.job.accessToken`
  - Trigger pool sizes: `xxl.job.triggerpool.fast/slow.max`
  - Log retention: `xxl.job.logretentiondays`

- **doc/db/tables_xxl_job.sql**: Database schema with initial data

## Key Extension Points

- Implement `IJobHandler` for custom job handlers
- Extend `JobHandler` annotation for new handler types
- Implement `ExecutorBiz` for custom executor RPC
- Extend alarm mechanism in `core/alarm/`
- Add route strategies in `core/route/strategy/`

## Database Conventions

- Primary key: `id` (AUTO_INCREMENT)
- Timestamps: `add_time`, `update_time` (DATETIME)
- Soft delete: Not used; status flags instead
- All tables prefixed with `xxl_job_`

## Tech Stack

- Spring Boot 3.4.5 / Spring 6.2.6
- MyBatis with HikariCP
- Netty 4.2 (embedded HTTP server)
- Groovy 4.0 (GLUE dynamic execution)
- FreeMarker (admin UI templates)