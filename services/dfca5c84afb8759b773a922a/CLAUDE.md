# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

This is a **Maven-based Java project** with multiple components. All commands should be run from the repository root.

### Core Commands

- **Quick development build**: `./mvnw clean install -Dquickly`
  - Builds all components quickly, skips Optimize
- **Full build (no tests/checks)**: `./mvnw clean install -DskipChecks -DskipTests`
- **Full build without frontends**: `./mvnw clean install -DskipChecks -DskipTests -PskipFrontendBuild`
- **Build and test everything**: `./mvnw clean install`

### Linting & Formatting

- **Check formatting**: `./mvnw license:check spotless:check -T1C`
- **Auto-fix formatting**: `./mvnw license:format spotless:apply -T1C`
- **Run static checks**: `./mvnw verify -Dquickly -DskipChecks=false -P'!autoFormat,checkFormat,spotbugs' -T1C`

### Testing

- **Run unit tests**: `./mvnw verify -Dquickly -DskipTests=false -DskipITs -T1C`
- **Run integration tests**: `./mvnw verify -Dquickly -DskipTests=false -DskipUTs -T1C`
- **Run all tests**: `./mvnw verify -T1C`
- **Quick test build**: `./mvnw verify -Dquickly -DskipTests=false` (tests are skipped with `-Dquickly` by default)

### Docker & Distribution

- **Build Docker image**: `./mvnw install -DskipChecks -DskipTests -T1C && docker build -f camunda.Dockerfile --target app -t "camunda/camunda:current-test" --build-arg DISTBALL=dist/target/camunda-zeebe-*.tar.gz .`

### Build Profiling

To investigate build performance, add `-Dprofile` to any Maven command. This generates profiler reports in the `target` folder.

## Codebase Architecture

Camunda 8 Orchestration Cluster is a **distributed systems application** with a modular architecture built on Spring Boot. It orchestrates complex business processes using BPMN (Business Process Model and Notation).

### Main Application

The entry point is `StandaloneCamunda` (`dist/src/main/java/io/camunda/application/StandaloneCamunda.java`), a Spring Boot application that combines multiple modules:
- **Broker** (Zeebe engine)
- **Gateway** (gRPC/REST API)
- **Operate** (monitoring & troubleshooting)
- **Tasklist** (user task management)
- **Identity** (authentication & authorization)
- **Webapps** (shared web components)

### Core Components

#### 1. **Zeebe** (`/zeebe/`)
The cloud-native process engine. Key modules:
- `engine/` - Event stream processor implementation
- `broker/` - Zeebe broker (server-side)
- `gateway/` - gRPC gateway for client communication
- `gateway-protocol/` - gRPC API definitions
- `protocol/` - SBE (Simple Binary Encoding) protocol
- `bpmn-model/` - BPMN 2.0 process definition API
- `exporters/` - Data export implementations (Elasticsearch, OpenSearch, S3, etc.)
- `atomix/` - Transport, membership, consensus
- `journal/` & `logstreams/` - Append-only log implementation
- `scheduler/` - Actor scheduler
- `backup/` - Backup management system

#### 2. **Operate** (`/operate/`)
Monitoring and troubleshooting web application with:
- `webapp/` - Spring Boot backend
- `client/` - React frontend with Carbon Design System
- Elasticsearch/OpenSearch backend
- Runs on port 8080/operate

#### 3. **Tasklist** (`/tasklist/`)
User task management web application with:
- `webapp/` - Spring Boot backend
- `client/` - React frontend
- Elasticsearch/OpenSearch backend
- Runs on port 8080/tasklist

#### 4. **Identity** (`/identity/`)
Authentication and authorization component:
- OAuth2/OIDC integration
- User and role management
- Runs on port 8080/identity

#### 5. **Clients** (`/clients/`)
Client libraries for various languages:
- `clients/java/` - Java client
- `clients/camunda-spring-boot-starter/` - Spring Boot SDK

### Module Structure

The root `pom.xml` defines these modules:
- `bom/` - Bill of Materials for dependency management
- `dist/` - Distribution packaging (tar.gz/zip)
- `build-tools/` - Build utilities
- `clients/` - Client libraries
- `zeebe/` - Process engine core
- `operate/` - Monitoring tool
- `tasklist/` - User task management
- `identity/` - Auth service
- `webapps-common/`, `webapps-schema/`, `webapps-backup/` - Shared web components
- `authentication/` - Authentication configuration
- `db/`, `search/`, `schema-manager/` - Database and search layer
- `service/` - Internal services
- `security/` - Security components
- `configuration/` - Configuration management

## Running Locally

### Prerequisites
- **JDK 21** (required for most modules; some client libraries use Java 8)
- **Elasticsearch or OpenSearch** (for Operate, Tasklist, Identity)

### Quick Start with Docker Compose

Each component has a `Makefile` for local development:

```bash
# Tasklist
cd tasklist && make env-up

# Operate
cd operate && make env-up

# With Identity
cd operate && make env-identity-up
```

Components will be available at:
- REST API: http://localhost:8080
- gRPC API: http://localhost:26500
- Management API: http://localhost:9600/actuator

### Running from Distribution

1. Build the project: `./mvnw install -DskipChecks -DskipTests`
2. Extract: `dist/target/camunda-zeebe-X.Y.Z-SNAPSHOT.tar.gz`
3. Start: `CAMUNDA_HOME/bin/camunda`

### IntelliJ Development

See `CONTRIBUTING.md` for detailed IntelliJ setup instructions. Key points:
1. Run a full build first
2. Use provided run configuration `StandaloneCamunda DEV`
3. Main class: `io.camunda.application.StandaloneCamunda`
4. Active profiles: `identity,tasklist,operate,broker,consolidated-auth,dev,insecure`

## Testing Guidelines

- Follow `docs/testing.md` and files in `docs/testing/`
- Tests are executed via Maven: `./mvnw verify`
- Use `-Dquickly` for faster builds (skips Optimize and some checks)
- Test troubleshooting: See `CONTRIBUTING.md` section on common issues

## Code Style & Standards

- **Formatting**: Managed by Maven Spotless plugin (Google Java Format)
- **License headers**: Auto-fixed by Maven during build
- **Checkstyle violations**: Must be fixed manually
- **Markdown formatting**: Also handled by Spotless

Always run `./mvnw license:format spotless:apply -T1C` before committing.

## Development Profiles

Key Spring profiles:
- `dev` - Development mode
- `broker` - Zeebe broker
- `gateway` - API gateway
- `operate` - Operate component
- `tasklist` - Tasklist component
- `identity` - Identity component
- `consolidated-auth` - Unified authentication
- `insecure` - Disable security (development only)

## Important Notes

1. **Architecture Streamlining**: The deployment and build process is being simplified (see CONTRIBUTING.md)
2. **macOS Apple Silicon**: Requires Rosetta for protobuf builds
3. **Search Engines**: Operate, Tasklist, and Identity use Elasticsearch/OpenSearch
4. **Profile-based Builds**: Use `-Dquickly` to skip Optimize during development
5. **Component Licensing**: Different modules use different licenses (Camunda License 1.0 vs Apache 2.0)

## Finding Documentation

- Component-specific docs: Check README.md in each module directory
- Zeebe engine: `/zeebe/engine/README.md`
- Testing: `docs/testing.md`
- Architecture guides: Files in `docs/`
- REST controllers: `docs/rest-controller.md`
- RDBMS: `docs/rdbms.md`
- Identity: `docs/identity.md`

## Git Workflow

- **Branch naming**: `issueId-description` (e.g., `123-adding-bpel-support`)
- **Never force push to main**: Use `git push --force-with-lease` for feature branches
- **Commit messages**: Follow guidelines in CONTRIBUTING.md
- **Lint before commit**: Always format and check code before pushing