# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Apache SeaTunnel Web is a web console for managing SeaTunnel data pipeline jobs. It provides a UI for job management, datasource configuration, virtual tables, and job scheduling. The system integrates with Apache SeaTunnel Zeta Engine to execute data synchronization jobs.

## Build Commands

### Backend (Java/Maven)

```bash
# Full production build
sh build.sh code

# Direct Maven build
./mvnw clean package -DskipTests -Pci

# Run tests
./mvnw clean verify -DskipUT=false -Dcheckstyle.skip=true -Dlicense.skipAddThirdParty=true

# Run single test
./mvnw test -Dtest=UserControllerTest -pl seatunnel-server/seatunnel-app

# Check code style
./mvnw --batch-mode --quiet --no-snapshot-updates clean spotless:check
```

### Frontend (Vue 3 + TypeScript)

```bash
cd seatunnel-ui

# Install dependencies (use pnpm-safe install)
npm run install:safe

# Development server
npm run dev

# Production build
npm run build:prod

# Lint
npm run lint

# Prettier format
npm run prettier
```

## Architecture

### Module Structure

- **seatunnel-server**: Core backend API server (Spring Boot 2.7)
  - **seatunnel-app**: Main application with controllers, services, and DAL
  - **seatunnel-server-common**: Shared server utilities
  - **seatunnel-dynamicform**: Dynamic form handling

- **seatunnel-web-common**: Shared domain models and utilities

- **seatunnel-datasource**: Datasource plugin system
  - **datasource-plugins-api**: Plugin SPI interfaces
  - **seatunnel-datasource-client**: Client for connecting to datasource plugins
  - **datasource-plugins-***: Individual datasource implementations (JDBC MySQL, PostgreSQL, Oracle, Kafka, MongoDB, S3, etc.)

- **seatunnel-ui**: Frontend Vue 3 application (port 5173)

- **seatunnel-web-dist**: Distribution packaging

### Backend Patterns

**Layer Structure:**
```
Controller -> Service -> DAL
            |          |
         Request    Mapper
         Response   Entity
```

**Key Patterns:**
- Controllers extend `BaseController` and return `Result<T>` wrapper objects
- Services use interface-based design (`IJobService`, `IJobServiceImpl`)
- DAL uses MyBatis-Plus with `BaseMapper<T>` and custom query methods
- Entities are in `dal/entity/` directory with MyBatis-Plus annotations
- Request/Response DTOs are in `domain/request/` and `domain/response/`

**API Response Format:**
All endpoints return `Result<T>` with `code`, `msg`, and `data` fields.

**Error Handling:**
- Use `SeatunnelErrorEnum` for standardized error codes
- Throw `ParamValidationException` for parameter validation errors

**Transaction Management:**
- Use `@Transactional` on service methods for write operations

**Permission Checking:**
- Use `permissionCheck()` method with `ResourceType` and `AccessType` enums
- Get current user via `UserContextHolder.getAccessInfo()`

### Datasource Plugin System

Plugins implement `DataSourceFactory` interface and are registered via `@AutoService(DataSourceFactory.class)` annotation.

**Required Methods:**
- `factoryIdentifier()`: Returns unique plugin identifier (e.g., "JdbcMySQL")
- `supportedDataSources()`: Returns `Set<DataSourcePluginInfo>` describing supported datasources
- `createChannel()`: Returns `DataSourceChannel` instance

**Plugin Location:** `seatunnel-datasource/seatunnel-datasource-plugins/`

**Example Structure:**
```
datasource-jdbc-mysql/
├── pom.xml
└── src/main/java/org/apache/seatunnel/datasource/plugin/mysql/jdbc/
    ├── MysqlDataSourceConfig.java      # Plugin metadata and config
    ├── MysqlJdbcDataSourceFactory.java # Factory implementation
    ├── MysqlJdbcDataSourceChannel.java # Data channel operations
    └── MysqlOptionRule.java            # UI form options
```

### Job Execution Flow

1. User creates job via UI/API with DAG configuration
2. `JobController.createJob()` receives `JobCreateReq`
3. `JobServiceImpl.createJob()` validates and coordinates:
   - `IJobDefinitionService`: Creates job definition
   - `IJobTaskService`: Saves plugin tasks
   - `IJobConfigService`: Saves job configuration
4. Job submitted to SeaTunnel Zeta Engine via Java Client
5. `JobExecutorServiceImpl` handles execution and monitoring

## Configuration

**Required Environment Variables:**
- `SEATUNNEL_HOME`: Path to SeaTunnel Zeta Engine installation
- `ST_WEB_BASEDIR_PATH`: Path to datasource shade package directory

**Database Configuration:**
- Edit `seatunnel-server/seatunnel-app/src/main/resources/application.yml`
- Configure MySQL connection, JWT secret key
- Copy `connectors/plugin-mapping.properties` to resources

**Running the Backend:**
- Run `SeatunnelApplication.java` with VM args: `-DSEATUNNEL_HOME=${your_seatunnel_install_path}`

## Database

**Initialization:**
```bash
# Edit database config
edit seatunnel-server/seatunnel-app/src/main/resources/script/seatunnel_server_env.sh

# Initialize database
sh seatunnel-server/seatunnel-app/src/main/resources/script/init_sql.sh
```

## Key Dependencies

- **Java**: 1.8 (minimum), tested with 8 and 11
- **Spring Boot**: 2.7.18
- **MyBatis-Plus**: 3.5.12
- **Vue 3**: 3.2.47 with Naive UI components
- **Build**: Maven 3.8+ with Maven Wrapper

## Testing

- Unit tests: `seatunnel-server/seatunnel-app/src/test/java/`
- Integration tests: `seatunnel-web-it/src/test/java/`
- Controller tests use wrapper classes for mocking

## Code Style

- **Java**: Spotless for formatting (run `mvnw spotless:apply` to fix)
- **Frontend**: ESLint + Prettier
- **License**: Apache License 2.0 - all files must have license header