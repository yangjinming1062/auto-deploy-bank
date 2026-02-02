# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Full clean build
./gradlew clean build

# Run all unit tests
./gradlew test

# Run tests for a specific module
./gradlew :core:test
./gradlew :datalake:test
./gradlew :environment:test

# Run checkstyle
./gradlew checkstyleMain checkstyleTest

# Run spotbugs
./gradlew spotbugsMain spotbugsTest

# Build a specific service
./gradlew :core:build
./gradlew :autoscale:build
./gradlew :datalake:build
./gradlew :environment:build
./gradlew :freeipa:build
./gradlew :redbeams:build
./gradlew :externalized-compute:build
./gradlew :environment-remote:build

# Show dependency insight for a specific module
./gradlew :core:dependencyInsightSpecific -Pdependency=com.amazonaws
```

## Architecture Overview

Cloudbreak is a multi-service platform for provisioning and managing cloud data platforms. The codebase follows a layered architecture with clear separation between API, service, and infrastructure layers.

### Core Services (Boot Applications)

Each service is an independent Spring Boot application with its own REST API and database:

| Service | Module | Port | Description |
|---------|--------|------|-------------|
| **Cloudbreak (Core)** | `core` | 9091 | Main cluster provisioning service |
| **Periscope** | `autoscale` | 8085 | Autoscaling service |
| **Datalake** | `datalake` | 8086 | DataLake management |
| **FreeIPA** | `freeipa` | 8090 | FreeIPA management |
| **Redbeams** | `redbeams` | 8087 | Database (RDS) management |
| **Environment** | `environment` | 8088 | Environment management |
| **Remote Environment** | `environment-remote` | 8092 | Remote environment proxy |
| **Externalized Compute** | `externalized-compute` | 8091 | External compute management |
| **Mock Thunderhead** | `mock-thunderhead` | 10080 | Mock UMS/auth service |
| **Mock Infrastructure** | `mock-infrastructure` | 10090 | Mock cloud infrastructure |

### Module Organization

Services are organized following domain-driven design principles:

- **`*-api`**: API definitions (DTOs, request/response objects, REST controllers)
- **`*-common`**: Shared utilities and common code
- **`cloud-*`**: Cloud provider implementations (AWS, Azure, GCP, YARN, mock)
- **`template-manager-*`**: Template processing (blueprints, recipes, CM templates)
- **`orchestrator-*`**: Cluster orchestrator implementations (Salt, YARN)

### Key Architectural Patterns

#### Flow-Based State Machine
Services use Spring State Machine for complex orchestration flows. The `flow` module provides the core infrastructure, with each service defining its own state machine configurations:

```
flow/
├── controller/     # Flow management controllers
├── core/           # Core state machine logic
├── event/          # Flow events
├── reactor/        # Event handlers (Sensors, Reactors)
└── domain/         # Flow persistence models
```

Each service implements flows in its `core/flow2` package with configurations like:
- `*FlowConfig.java` - State machine configuration
- `*FlowChainConfig.java` - Flow chain configuration
- `*Actions.java` - State actions
- `*Events.java` - Flow events
- `*State.java` - State definitions

#### Cloud Provider Abstraction
The `cloud-api` module defines the cloud-agnostic SPI. Each provider implements:
- `CloudConnector` - Entry point for cloud operations
- `ResourceConnector` - Resource lifecycle operations (instances, volumes, networks)
- `Authenticationenticator` - SSH key and credential handling
- `Provisioner` - Resource provisioning

#### REST API Pattern
API endpoints follow consistent conventions:
- Controllers in `controller/v4/` package
- Exception mappers in `controller/mapper/` package
- Request/response DTOs use `@Schema` annotations with `requiredMode = REQUIRED`
- Collections in responses default to mutable empty collections

#### Repository Pattern
Data access follows Spring Data JPA conventions:
- Entities in `domain/` or `repository/entity/` packages
- Repositories extend `JpaRepository` or custom base interfaces
- Services delegate to repositories for data operations

#### Converter Pattern
DTO-to-entity conversions use dedicated converter classes in `converter/`:
- `*InitConverter.java` - Default value initialization
- `*ViewConverter.java` - Entity to view DTO
- `*Converter.java` - Bidirectional entity/DTO conversion

### Database Migrations

Schema changes use MyBatis Migrations (not Flyway/Liquibase). Migration scripts are in:
- `core/src/main/resources/schema/`
- `autoscale/src/main/resources/schema/`
- `datalake/src/main/resources/schema/`
- `environment/src/main/resources/schema/`
- `freeipa/src/main/resources/schema/`
- `redbeams/src/main/resources/schema/`
- `externalized-compute/src/main/resources/schema/`
- `environment-remote/src/main/resources/schema/`

Create new migrations using:
```bash
cbd migrate <database_name> new "Description"
```

### Configuration

Application configuration follows Spring Boot conventions:
- `src/main/resources/application.yml` - Base configuration
- `src/main/resources/application-dev.yml` - Development overrides
- `buildInfo` task generates `application.properties` with version info

### Common Development Tasks

1. **Running a service locally** (with CBD):
   ```bash
   export CB_LOCAL_DEV_LIST=cloudbreak,datalake,freeipa
   cbd start
   ```

2. **Testing cloud provider integration**: Use `mock-infrastructure` and `mock` provider

3. **Generating flow graphs**:
   ```bash
   make generate-flow-graphs
   ```

4. **Rebuilding resources** (after template/config changes):
   ```bash
   ./gradlew rebuildOutResources
   ```

### CM Repository Credentials

Some dependencies require Cloudera Manager repository credentials. Set these in `~/.gradle/gradle.properties`:
```
defaultCmPrivateRepoUser=your-username
defaultCmPrivateRepoPassword=your-password
```

### Code Style

- Import order: static all → java.* → javax.* → jakarta.* → org.* → com.* → all other imports
- Use strings instead of enums on API boundaries for backward compatibility
- Mark essential API fields as `@Schema(requiredMode = REQUIRED)` with default values
- Prefer primitive types over wrappers; if using wrappers, provide default values
- Collections in responses should default to mutable empty collections