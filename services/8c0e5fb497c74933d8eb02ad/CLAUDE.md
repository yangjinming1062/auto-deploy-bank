# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Apache StreamPark is a streaming application development framework and cloud-native real-time computing platform. It provides:

- A **development framework** for Apache Flink and Apache Spark to simplify stream processing application development
- A **management platform** (console) for deploying, managing, and monitoring streaming applications
- Support for both batch and stream processing
- Multi-engine/multi-version support for Flink and Spark
- Compatibility with standalone clusters, YARN, and Kubernetes

## High-Level Architecture

### Core Modules

1. **streampark-common** - Shared utilities, constants, enums, and common abstractions used across all modules
   - Located in: `streampark-common/src/main/java/org/apache/streampark/common/`
   - Contains: constants, enums, utility classes

2. **streampark-flink** - Flink integration layer with multiple sub-modules:
   - `streampark-flink-client` - Client APIs for Flink application interaction
   - `streampark-flink-connector` - Custom Flink connectors
   - `streampark-flink-core` - Core Flink abstractions
   - `streampark-flink-kubernetes` - Kubernetes-specific Flink support
   - `streampark-flink-packer` - Application packaging utilities
   - `streampark-flink-shims` - Version-specific compatibility layer (supports multiple Flink versions)
   - `streampark-flink-sqlclient` - SQL client for Flink
   - `streampark-flink-udf` - User-defined functions support

3. **streampark-spark** - Spark integration layer:
   - `streampark-spark-cli` - Command-line interface
   - `streampark-spark-client` - Client APIs
   - `streampark-spark-connector` - Custom Spark connectors
   - `streampark-spark-core` - Core Spark abstractions
   - `streampark-spark-sqlclient` - SQL client for Spark

4. **streampark-console** - Web-based management platform:
   - `streampark-console-service` - Spring Boot backend service
     - Uses Spring Boot 2.7.11
     - MyBatis Plus for database access
     - PostgreSQL 42.5.1 and MySQL support
     - Undertow as servlet container
     - Shiro for authentication
     - P6SQLy for SQL logging
   - `streampark-console-webapp` - Vue 3 frontend
     - Vite build tool
     - TypeScript
     - pnpm package manager
     - Based on vue-vben-admin

5. **streampark-e2e** - End-to-end test suite
   - Uses Selenium WebDriver with TestContainers
   - Follows Page Object Model design pattern
   - Docker-based test environments

## Common Development Commands

### Building the Project

```bash
# Full production build (includes shaded jars, webapp, and distribution)
./build.sh

# Or using Maven directly with all profiles
./mvnw -Pshaded,webapp,dist -DskipTests clean install

# Build only specific modules
./mvnw -pl streampark-common -am clean install
./mvnw -pl streampark-flink/streampark-flink-core clean install
```

### Running Tests

```bash
# Run all unit tests
./mvnw clean test

# Run tests for specific module
./mvnw -pl streampark-console/streampark-console-service test

# Run a single test class
./mvnw test -Dtest=ClassNameTest

# Run with specific Java version (CI tests on Java 8 and 11)
JAVA_HOME=/path/to/java8 ./mvnw test

# Run only unit tests (skip integration tests)
./mvnw clean test

# Run E2E tests (requires Docker)
cd streampark-e2e
./mvnw test
```

### Code Quality Checks

```bash
# Check code style (checkstyle)
./mvnw checkstyle:check

# Check code formatting (spotless)
./mvnw spotless:check

# Format code
./mvnw spotless:apply
```

### Frontend Development (streampark-console-webapp)

```bash
# Install dependencies
pnpm install

# Start development server
pnpm serve

# Build for production
pnpm build

# Lint code
pnpm lint:fix

# Type check
pnpm type-check
```

### Running the Console Locally

```bash
# 1. Build the project
./build.sh

# 2. Set up database (MySQL or PostgreSQL)
# Execute schema and data SQL files from:
# streampark-console/streampark-console-service/src/main/assembly/script/

# 3. Configure application
# Edit: streampark-console/streampark-console-service/src/main/resources/application.yml

# 4. Start the service
cd streampark-console/streampark-console-service
./target/streampark-console-service-2.2.0-SNAPSHOT/bin/startup.sh

# Or use Maven
./mvnw spring-boot:run -pl streampark-console/streampark-console-service
```

## Database Configuration

StreamPark supports both MySQL and PostgreSQL. Database initialization files are located in:
- `streampark-console/streampark-console-service/src/main/assembly/script/schema/` - Database schemas
- `streampark-console/streampark-console-service/src/main/assembly/script/data/` - Initial data
- `streampark-console/streampark-console-service/src/main/assembly/script/upgrade/` - Upgrade scripts by version

## Important Configuration Files

- **pom.xml** - Root Maven project descriptor (line 29: `<version>2.2.0-SNAPSHOT</version>`)
- **streampark-console/streampark-console-service/src/main/resources/application.yml** - Backend configuration
- **streampark-console/streampark-console-webapp/vite.config.ts** - Frontend Vite configuration
- **streampark-console/streampark-console-webapp/package.json** - Frontend dependencies
- **streampark-console/streampark-console-service/pom.xml** - Backend dependencies (Spring Boot 2.7.11)

## Key Technologies & Versions

### Backend (Java)
- Java 8/11 (CI tests both versions)
- Spring Boot 2.7.11
- MyBatis Plus 3.5.3.1
- Scala 2.12.17
- Flink 1.20.1
- Spark 3.1.2
- PostgreSQL/MySQL

### Frontend (TypeScript/Vue)
- Node.js 16+
- Vue 3
- Vite
- pnpm 8.1.0
- TypeScript

### Testing
- JUnit Jupiter
- TestContainers
- Selenium WebDriver

## Testing Patterns

### Unit Tests
- Location: `src/test/java/` in each module
- Use JUnit Jupiter (`org.junit.jupiter`)
- Mock with Mockito or Spring's test support

### E2E Tests
- Location: `streampark-e2e/streampark-e2e-case/src/test/java/`
- Use `@StreamPark` annotation to set up Docker environment
- Example: `@StreamPark(composeFiles = "docker/basic/docker-compose.yaml")`
- Follow Page Object Model - create page classes for each UI section
- Test videos saved to temporary directory (e.g., `/var/folders/.../PASSED-[test]-timestamp.mp4`)

### Running E2E Tests Locally
```bash
# With Docker (recommended)
cd streampark-e2e
./mvnw test

# Without Docker (requires local services)
./mvnw test -Dlocal=true

# Mac M1 specific
./mvnw test -Dm1_chip=true
```

## CI/CD Workflows

GitHub Actions workflows (`.github/workflows/`):
- **unit-test.yml** - Unit tests, code style checks, license header validation (runs on Java 8, 11)
- **backend.yml** - Backend-specific tests
- **frontend.yml** - Frontend build and tests
- **e2e.yml** - End-to-end test suite
- **docker-push.yml** - Docker image publishing
- **codeql-analysis.yml** - Security analysis

## Version Compatibility

The project uses the Flink Shims module (`streampark-flink-shims`) to maintain compatibility across multiple Flink versions. Key version mappings:
- Flink version: 1.20.1
- Scala binary version: 2.12
- Shims version: 1.14

## Development Tips

1. **Multi-module builds**: Use `-pl` and `-am` flags to build specific modules and their dependencies
2. **Profile activation**: The `shaded`, `webapp`, and `dist` profiles are required for full builds
3. **Hot reload**: Frontend supports hot reload with `pnpm serve`
4. **Database changes**: Always update the upgrade scripts when modifying schema
5. **License headers**: All files must include the Apache License header (automatically checked in CI)
6. **Code style**: Checkstyle and Spotless are enforced in CI
7. **Async operations**: Backend uses async executors - be aware of async patterns in service layer

## Deployment

After building with `./build.sh`, distribution artifacts are created in the `dist/` directory. The console service can be started with:
```bash
cd dist/streampark-console-service-2.2.0-SNAPSHOT/bin
./startup.sh
```

## Documentation

- Main README: `README.md`
- Console service scripts: `streampark-console/streampark-console-service/src/main/assembly/script/README.md`
- E2E testing guide: `streampark-e2e/README.md`
- Frontend docs: `streampark-console/streampark-console-webapp/README.md`
- Online docs: https://streampark.apache.org/docs/get-started