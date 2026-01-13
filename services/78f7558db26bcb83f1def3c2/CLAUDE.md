# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Test Commands

This is a Maven-based Java project using Java 8. All Maven commands should use the wrapper `./mvnw` to ensure consistent builds.

### Common Commands

```bash
# Clean and compile
./mvnw clean compile

# Run all tests
./mvnw test

# Run a specific test class
./mvnw test -Dtest=ClassName

# Run tests with coverage
./mvnw test -Djacoco.skip=false

# Build the entire project
./mvnw clean package -DskipTests

# Run only unit tests (skip integration tests)
./mvnw test -DskipIntegrationTests=true

# Check code quality (checkstyle, PMD)
./mvnw checkstyle:check
./mvnw pmd:check

# Format code according to project style
./mvnw license:format

# Run with checkstyle profile
./mvnw checkstyle:check -Pcheckstyle

# Build a specific module
./mvnw clean install -pl <module-name> -am

# Build Docker image
./mvnw clean package -Pimage -DskipTests
```

## High-Level Architecture

Seata is a distributed transaction solution for microservices architecture. It follows a three-role model:

### Core Components

1. **Transaction Coordinator (TC)** - `server/` module
   - Server-side component that maintains the status of global and branch transactions
   - Drives global commit or rollback decisions
   - Entry point: `io.seata.server.Server`

2. **Transaction Manager (TM)** - `tm/` module
   - Client-side component that defines the scope of global transactions
   - Begins, commits, or rolls back global transactions
   - Key class: `io.seata.tm.DefaultTransactionManager`

3. **Resource Manager (RM)** - `rm/` and `rm-datasource/` modules
   - Client-side component managing resources (databases, message queues, etc.)
   - Registers branch transactions and reports status to TC
   - Key classes: `io.seata.rm.DefaultResourceManager`, `io.seata.rm.AbstractRMHandler`

### Architecture Flow

1. TM asks TC to begin a new global transaction → TC generates XID
2. XID propagates through the microservice call chain
3. RM registers local transactions as branches of the global transaction
4. TM asks TC to commit/rollback the global transaction
5. TC drives all branch transactions to commit or rollback

### Key Modules

- **`core/`** - Core transaction logic, protocol definitions (request/response classes), RPC handlers, and storage abstractions
- **`server/`** - Transaction Coordinator server implementation, session management, and console
- **`tm/`** - Transaction Manager client API
- **`rm/`** - Resource Manager base classes
- **`rm-datasource/`** - Database-specific Resource Manager implementation (handles AT mode)
- **`saga/`** - Saga pattern implementation for long-running transactions
- **`spring/`** - Spring Framework integration
- **`spring-boot-starter/`** - Spring Boot auto-configuration
- **`integration/`** - Framework integrations (Dubbo, gRPC, SOFARPC, Motan, HTTP, BRPC, HSF)
- **`config/`** - Configuration modules for different config centers (Nacos, Apollo, Consul, etc.)
- **`discovery/`** - Service discovery integrations
- **`serializer/`** - Serialization utilities
- **`compressor/`** - Data compression support
- **`metrics/`** - Metrics and monitoring

### Transaction Modes

- **AT Mode** (Automatic) - `rm-datasource/` - Two-phase commit for databases with automatic undo
- **TCC Mode** - `tcc/` - Try-Confirm-Cancel pattern for resource reservations
- **Saga Mode** - `saga/` - Long-running transaction orchestration with compensating actions
- **XA Mode** - Integration with XA transaction standard

## Code Style

The project uses strict code quality checks via multiple tools:

- **Checkstyle**: Configuration in `style/seata_checkstyle.xml`
  - Required copyright headers on all source files
  - Prohibits `System.out.println` (use logging instead)
  - Enforces naming conventions
  - Run with: `./mvnw checkstyle:check -Pcheckstyle`

- **PMD**: Code quality analysis using Alibaba p3c-pmd rules
  - Located in root `pom.xml`
  - Run with: `./mvnw pmd:check`

- **License Check**: Automatic license header insertion
  - Run with: `./mvnw license:format` (part of checkstyle profile)

- **JaCoCo**: Code coverage reporting
  - Coverage reports generated during test phase

## Development Notes

- Target Java version: 1.8
- Main development branch: `develop`
- All PRs should target the `develop` branch
- Project uses Maven wrapper (`mvnw`) - do not use system Maven
- Spring Boot version: 2.5.13
- Configuration: Supports multiple config centers (Nacos, Apollo, Consul, etc.)
- Protocol: Custom RPC protocol defined in `core/src/main/java/io/seata/core/protocol/`

## Testing Strategy

- Unit tests: JUnit 5, Mockito, AssertJ
- Test location: `src/test/java/` in each module
- Integration tests: Located in `test/` module
- Property: Use `-DskipIntegrationTests=true` to skip integration tests

## Deployment

- Server can be built as a Docker image using the `image` profile
- Distribution packaging in `distribution/` module
- Deployment scripts in `script/server/` directory
- Client configuration scripts in `script/client/` directory

## Key Configuration Files

- `pom.xml` - Root Maven POM with build plugins and profiles
- `build/pom.xml` - Build configuration and dependency management
- `style/seata_checkstyle.xml` - Code style rules
- `style/copyright` - License header template
- `distribution/Dockerfile` - Container build definition