# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RuoYi-Flowable-Plus is a Java-based backend management system that extends RuoYi-Vue-Plus with Flowable workflow engine support. It provides online process design, form design, and task management capabilities.

**Tech Stack:**
- Backend: Java 8/11, Spring Boot 2.7.9, MyBatis Plus 3.5.3.1, Flowable 6.8.0
- Security: Sa-Token (JWT-based authentication)
- Frontend: Vue 2.6.12, Element UI 2.15.12, bpmn-js for BPMN design
- Database: MySQL (primary), supports Oracle/Postgres/SQL Server via dynamic datasource
- Cache: Redis via Redisson
- Scheduling: XXL-JOB 2.3.1

## Build Commands

**Backend (Maven):**
```bash
# Build all modules
mvn clean install

# Run tests with profile (local/dev/prod)
mvn test -Pdev

# Skip tests during build
mvn clean install -DskipTests
```

**Frontend (Node.js >= 8.9):**
```bash
cd ruoyi-ui

# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build:prod

# Lint code
npm run lint
```

**Profile Activation:**
- `local`: Local development config (debug logging)
- `dev`: Development environment (default, debug logging)
- `prod`: Production environment (warn logging)

## Architecture

### Module Organization

The project is a modular Maven multi-module build:

| Module | Purpose |
|--------|---------|
| `ruoyi-admin` | Main entry point - web controllers and API endpoints |
| `ruoyi-framework` | Core framework configs, security (Sa-Token), AOP, interceptors |
| `ruoyi-system` | Business logic - users, roles, menus, configurations |
| `ruoyi-flowable` | Flowable engine integration, listeners, workflow utilities |
| `ruoyi-oss` | Object storage service (S3, Aliyun OSS) |
| `ruoyi-sms` | SMS service integration (Aliyun, Tencent) |
| `ruoyi-job` | Scheduled task management (XXL-JOB) |
| `ruoyi-generator` | Code generation from database tables |
| `ruoyi-common` | Shared entities, constants, enums, utilities |
| `ruoyi-ui` | Vue frontend source code |

### Key Configuration

- **Primary config**: `ruoyi-admin/src/main/resources/application.yml`
- **Database profiles**: `application-{local|dev|prod}.yml` in same directory
- **Swagger/OpenAPI docs**: SpringDoc configured in application.yml
- **Flowable config**: `flowable.*` properties in application.yml

### Important Package Structures

**ruoyi-framework:**
- `config/` - Spring configuration classes
- `satoken/` - Authentication/authorization setup
- `aspectj/` - AOP aspects (logging, rate limiting)
- `web/` - Request handling, file upload, result wrappers
- `interceptor/` - MyBatis interceptors (data permission, encryption)

**ruoyi-system:**
- `core/` - Core service implementations
- `config/` - System-specific configurations
- `flow/` - Business flow utilities
- `factory/` - Service factories (e.g., UserIdUserFactory)

**ruoyi-flowable:**
- `domain/` - Flowable domain entities
- `service/` - Workflow service implementations
- `listener/` - Flowable event listeners
- `runner/` - Startup runners for process deployment

### Security & Data Access

- **Authentication**: Sa-Token with JWT tokens (`Authorization` header, Bearer prefix)
- **Data Permission**: `PlusDataPermissionInterceptor` provides row-level access control
- **Encryption**: MyBatis interceptors for sensitive field encryption/decryption
- **XSS Filtering**: Configurable XSS protection on `/system/*`, `/monitor/*`, `/tool/*`

### Database Conventions

- **Id Generation**: `ASSIGN_ID` (snowflake) for primary keys
- **Logic Delete**: 2 = deleted, 0 = not deleted
- **Field Strategy**: `NOT_NULL` for inserts and updates
- **Mapper Location**: `classpath*:mapper/**/*Mapper.xml`

## Development Notes

- Controllers are located in `ruoyi-admin/src/main/java/com/ruoyi/web/controller/`
- Tests use JUnit with `@Tag` annotations matching profile names (local/dev/prod)
- API documentation available at `/swagger-ui.html` when running
- Default admin credentials: `admin` / `admin123`
- Demo mode enabled by default (`ruoyi.demoEnabled: true`)

## Database Initialization

Database scripts are in `script/sql/`:
- Initialize with `script/sql/mysql/schema.sql`
- Updates applied via incremental migration scripts