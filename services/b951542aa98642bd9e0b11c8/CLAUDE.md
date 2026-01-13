# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Building the Application
```bash
./gradlew clean build          # Build entire project
./gradlew bootRun             # Run application on-the-fly
./gradlew tasks               # List all available Gradle tasks
```

### Running Individual Tests
```bash
# Run tests for specific modules
./gradlew :application:core:test
./gradlew :application:dataproviders:test
./gradlew :application:entrypoints:test
./gradlew :application:configuration:test
./gradlew :acceptance-tests:test
./gradlew :integration-tests:test
```

### Building and Running
```bash
# Build and run from JAR
./gradlew clean build
java -jar application/build/clean-architecture-example.jar

# Or run directly with Spring Boot
./gradlew bootRun
```

The application runs on **http://localhost:8080**:
- Endpoint: `http://localhost:8080/broadbandaccessdevice/device1.exlon.com/`
- A scheduled job runs every 5 seconds (visible in logs)

### IDE Setup
- **IntelliJ**: Open `build.gradle` - IntelliJ will load everything
- **Eclipse**: Install Gradle plugin, import as Gradle project

## Project Structure

This is a **Clean Architecture** Java application demonstrating Clean Architecture principles with a telecommunications Network Inventory domain.

### Modules
- **application:core** - Entities and Use Cases (pure business logic)
- **application:dataproviders** - Data access (database & network I/O)
- **application:entrypoints** - REST API controllers and scheduled jobs
- **application:configuration** - Spring configuration and DI wiring
- **acceptance-tests** - BDD tests using Yatspec
- **integration-tests** - Integration tests for entrypoints/dataproviders

### Core Architecture (Clean Architecture)

The application follows Clean Architecture with strict dependency rules. Dependencies must always point inward toward the core.

```
┌─────────────────────────────────────┐
│           ENTRYPOINTS               │  ← REST controllers, Jobs
│    (Spring MVC @RestController)     │     (Framework-dependent)
└─────────────┬───────────────────────┘
              │ depends on
              ▼
┌─────────────────────────────────────┐
│              CORE                   │  ← Use Cases & Entities
│   (Business Logic - Plain Java)     │     (Framework-independent)
│                                     │
│  Use Cases:                         │
│  • GetCapacityForExchangeUseCase    │
│  • ReconcileBroadbandAccess...      │
│  • GetBroadbandAccessDevice...      │
│                                     │
│  Entities:                          │
│  • Exchange                         │
│  • BroadbandAccessDevice            │
│  • Capacity                         │
└─────────────┬───────────────────────┘
              │ implements interfaces
              ▼
┌─────────────────────────────────────┐
│          DATAPROVIDERS              │  ← Database & Network I/O
│   (Implement use case interfaces)   │     (Framework-dependent)
└─────────────┬───────────────────────┘
              │ configured in
              ▼
┌─────────────────────────────────────┐
│          CONFIGURATION              │  ← Spring DI, wiring
│      (Main class, config)           │     (Framework-dependent)
└─────────────────────────────────────┘
```

#### Core (Entities & Use Cases)
**Location:** `application/core/src/main/java/com/clean/example/core/`

**Entities** - Plain Java objects, no frameworks, no annotations:
- `entity/Exchange` - Exchange entity (code, name, postCode)
- `entity/BroadbandAccessDevice` - Device entity (hostname, serialNumber, type, exchange)
- `entity/Capacity` - Capacity information
- `entity/DeviceType` - Device type enum

**Use Cases** - Business actions, pure Java with dependency injection:
- **exchange/getcapacity/GetCapacityForExchangeUseCase** - Get available ports for exchange
- **broadbandaccessdevice/reconcile/ReconcileBroadbandAccessDevicesUseCase** - Reconcile device data from reality vs model
- **broadbandaccessdevice/getdetails/GetBroadbandAccessDeviceDetailsUseCase** - Get device details by hostname

Use cases define interfaces (e.g., `GetDeviceDetails`) that dataproviders implement. Core has NO dependencies on outer layers.

#### Dataproviders
**Location:** `application/dataproviders/src/main/java/com/clean/example/dataproviders/`

Implement interfaces defined by use cases:
- **database/** - H2 database access
- **network/** - Network device access (simulated)

These implement the data access interfaces that use cases depend on.

#### Entrypoints
**Location:** `application/entrypoints/src/main/java/com/clean/example/entrypoints/`

**REST Controllers** - Spring MVC @RestController:
- `rest/exchange/capacity/GetCapacityForExchangeEndpoint` - GET `/broadbandaccessdevice/{hostname}/`
- `rest/broadbandaccessdevice/GetBroadbandAccessDeviceEndpoint` - GET endpoint for device details

**Jobs** - Scheduled background jobs:
- `job/broadbandaccessdevice/ReconcileBroadbandAccessDeviceJob` - Runs every 5 seconds

Entry points trigger use cases and convert results to appropriate formats (DTOs for REST).

#### Configuration
**Location:** `application/configuration/src/main/java/com/clean/example/configuration/`

Spring configuration and dependency injection:
- `Application.java` - Main Spring Boot class (`com.clean.example.Application`)
- `*Configuration.java` - Configuration classes for wiring components

## Testing Strategy (Testing Pyramid)

Tests run in order: **Unit Tests** → **Acceptance Tests** → **Integration Tests**

### Unit Tests (TDD)
**Location:** `*/src/test/java/` in each module
- JUnit 4 + Mockito + AssertJ
- Test individual classes in isolation
- Aim for 100% coverage
- Fast execution

Run with: `./gradlew :application:core:test` etc.

### Acceptance Tests (BDD)
**Location:** `acceptance-tests/`
- Uses **Yatspec** framework
- Test use cases in isolation (no GUI, no DB)
- Business-facing documentation
- Demonstrate business requirements

Output: `build/reports/yatspec/com/clean/example/`

Run with: `./gradlew :acceptance-tests:test`

### Integration Tests
**Location:** `integration-tests/`
- Spring Test framework
- Test integration with external systems (database, HTTP)
- Test one layer in isolation (e.g., just REST endpoint)
- Slower execution

Run with: `./gradlew :integration-tests:test`

### Test Execution Order
Gradle ensures tests run in correct order via `mustRunAfter`:
1. Unit tests for all application modules
2. Acceptance tests
3. Integration tests

## Technology Stack

- **Java 8**
- **Spring Boot 1.3.3.RELEASE**
- **Spring 4.2.5.RELEASE**
- **Build tool:** Gradle 2.11
- **Database:** H2 (development)
- **Testing:**
  - Unit: JUnit 4, Mockito, AssertJ
  - Acceptance: Yatspec (BDD)
  - Integration: Spring Test

## Domain Model

**Network Inventory System** for telecommunications:

**Entities:**
- **Exchange** - Telecommunications exchange (has devices, capacity)
- **BroadbandAccessDevice** - Network device with hostname, serial number, type
- **Capacity** - Available ports/capacity information
- **DeviceType** - Types of network devices

**Use Cases:**
1. **Get Capacity for Exchange** - Calculate available ports in an exchange
2. **Reconcile Broadband Access Devices** - Sync device data from reality vs stored model
3. **Get Device Details** - Retrieve device information by hostname

**REST Endpoints:**
- `GET /broadbandaccessdevice/{hostname}/` - Get device details
- `GET /capacityforexchange/{exchangeCode}` - Get exchange capacity

**Scheduled Jobs:**
- **ReconcileBroadbandAccessDeviceJob** - Runs every 5 seconds, logs "Job Starting: ReconcileBroadbandAccessDeviceJob..."

## Key Clean Architecture Principles Implemented

1. **Dependency Rule** - Dependencies point inward; core has no knowledge of outer layers
2. **Framework Independence** - Core is plain Java, no Spring annotations
3. **Use Case Centric** - Business logic is in use cases, not in controllers or entities
4. **Interface Definition** - Use cases define interfaces; dataproviders implement them
5. **Screaming Architecture** - Package structure reveals business domain
6. **Test Isolation** - Each layer can be tested independently
7. **Decoupling over DRY** - Accept some duplication to maintain architectural boundaries

## Development Notes

- Core module should NEVER depend on Spring, Jakarta, or any framework
- Use cases throw business exceptions (e.g., `DeviceNotFoundException`, `ExchangeNotFoundException`)
- Controllers handle framework-specific exceptions and convert to HTTP responses
- DTOs in entrypoints separate API contracts from core entities
- H2 schema is in `application/dataproviders/src/main/resources/h2-schema.sql`