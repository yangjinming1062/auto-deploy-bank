# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Build & Run
```bash
# Build and install the project
mvn install

# Build and run tests
mvn test -DskipTests=false

# Run tests without building
mvn surefire:test -DskipTests=false

# Run a specific test
mvn test -DskipTests=false -Dtest=DeptModelTest

# Production deployment script
./bin/ag-admin.sh start|stop|restart|status
```

**Note:** Tests are skipped by default in `pom.xml:354`. Always use `-DskipTests=false` to run tests.

**Main Application:** `AgileBootAdminApplication` in `agileboot-admin` module

### Configuration

**Development Environment:**
- MySQL: `localhost:33067` (user: `root`, password: `12345`)
- Redis: `localhost:36379` (password: `12345`)
- Config: `agileboot-admin/src/main/resources/application-dev.yml`

**Embedded Testing (no external DB/Redis required):**
Set in `application.yml`:
```yaml
spring.profiles.active: basic,test
agileboot.embedded.mysql: true
agileboot.embedded.redis: true
```

**Database Setup:**
1. Use the latest SQL file in `/sql` directory (e.g., `agileboot-20230814.sql`)
2. Or run `./sql/combine.sh` to combine all SQL files

### Code Generation
Use `CodeGenerator` class to generate new database entities:
- Generates code in `agileboot-infrastructure/target/classes/`
- Supports MySQL and other databases (update `keywordsHandler` method per database type)

## High-Level Architecture

This is a **multi-module Maven project** with **Domain-Driven Design (DDD)** and **CQRS** architecture.

### Module Structure

**agileboot-admin** - REST API controllers
- Contains all `@RestController` classes
- Exposes HTTP endpoints for frontend consumption
- Uses Swagger/OpenAPI for documentation

**agileboot-domain** - Core business logic (DDD + CQRS)
- **command** - Request models for operations (Create/Update/Delete)
- **query** - Request models for queries (Read)
- **dto** - Response data transfer objects
- **model** - Domain models (DDD entities with business logic)
- **db** - Data access layer (Entity, Mapper, Service)
  - `entity` - MyBatis-Plus entities
  - `mapper` - MyBatis-Plus mappers
  - `service` - Database services (CRUD operations)
- `*ApplicationService` - Transaction layer coordinating domain models

**agileboot-infrastructure** - Configuration & integrations
- Database configuration
- Redis configuration
- Security configuration
- Custom annotations (rate limiting, permissions)
- AOP aspects

**agileboot-common** - Shared utilities
- Common exceptions
- Core DTOs
- Constants
- Utility classes

**agileboot-api** - Open API module (reserved for public API)

### Request Flow Patterns

**Query Flow** (Read operations):
```
Controller → *Query → ApplicationService → *Service (Db) → Mapper
```

**Command Flow** (Write operations):
```
Controller → *Command → ApplicationService → *Model → save/update
```

**Example - Add Department:**
1. `SysDeptController` receives `AddDeptCommand`
2. `DeptApplicationService.addDept()` coordinates the operation
3. `DeptModel` validates business rules and generates ancestors
4. `DeptModel.insert()` persists to database

### Development Patterns

**Domain Models:**
- Contain business logic validation
- Use Factory pattern (`*ModelFactory`)
- Examples: `DeptModel`, `UserModel`, `RoleModel`

**Testing Pattern:**
- Tests focus on Domain Models (not Controllers)
- Heavy use of Mockito mocking
- Test business logic validation rules
- Example: `DeptModelTest` tests validation methods

**Code Style:**
- Import GoogleStyle.xml for code formatting
- Lombok is used extensively (avoid manual getters/setters)
- All database operations use MyBatis-Plus
- JWT-based authentication with Spring Security

### Key Configuration Files

- `pom.xml` - Maven configuration, dependencies, test setup
- `application.yml` - Default profile (dev)
- `application-dev.yml` - Development environment config
- `application-basic.yml` - Base configuration (shared)
- `application-test.yml` - Test environment with embedded DB/Redis
- `GoogleStyle.xml` - Code formatting template
- `bin/ag-admin.sh` - Production deployment script

### Important Notes

- **Swagger UI:** http://localhost:8080/v3/api-docs (dev only, disabled in production)
- **Druid Monitor:** http://localhost:8080/druid/ (login: agileboot/123456)
- **Logging path:** Configure in `application-dev.yml:87` (default: `D:/logs/agileboot-dev`)
- **File storage:** Configure `agileboot.file-base-dir` in config files
- **Timezone:** Use Asia/Shanghai (JVM parameter in startup script)

### Embedded Dependencies

The project can run with embedded dependencies for development/testing:
- H2 database (instead of MySQL)
- Embedded Redis (in-memory, port conflicts possible on macOS)

### Database Design

- Simplified to ~10 tables (vs original Ruoyi's 20+ tables)
- Dictionary types replaced with Enums
- Master-slave datasource support (commented out example in config)
- Multi-level caching: Map → Guava → Redis

### Security Features

- JWT token authentication
- Rate limiting (annotations: `@RateLimit`)
- Menu-based permission control
- Data permission filtering
- XSS protection via JSON serialization
- Password encryption (transport level, requires HTTPS for production)