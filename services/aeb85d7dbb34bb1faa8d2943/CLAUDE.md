# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **eladmin**, a Java enterprise admin management system (后台管理系统) built with Spring Boot 2.7.18. It features role-based access control, system monitoring, task scheduling, and comprehensive administrative capabilities.

**Technology Stack:**
- Spring Boot 2.7.18, Spring Security, Spring Data JPA
- MySQL 9.2.0, Redis, Quartz Scheduler
- JWT authentication, Druid connection pooling
- Knife4j (Swagger 3.0.3) for API documentation
- MapStruct for object mapping
- Maven as build tool

## Common Development Commands

### Building the Project
```bash
# Build entire project (from root directory)
mvn clean install

# Build specific module
mvn clean install -pl eladmin-system

# Build and run
mvn clean install -pl eladmin-system && java -jar eladmin-system/target/eladmin-system.jar

# Skip tests during build (note: tests are disabled by default in root POM)
mvn clean install -DskipTests=true
```

### Running the Application
```bash
# Main entry point
cd eladmin-system
mvn spring-boot:run

# Or run the packaged JAR
java -jar eladmin-system/target/eladmin-system.jar

# Run with specific profile
java -jar eladmin-system/target/eladmin-system.jar --spring.profiles.active=dev
```

### Database Operations
```bash
# Initialize database (MySQL required)
mysql -u root -p < sql/eladmin.sql
mysql -u root -p < sql/quartz.sql
```

### Code Generation
```bash
# Generate code using eladmin-generator
mvn clean install -pl eladmin-generator
# Then run the generator from the admin panel UI
```

## High-Level Architecture

### Maven Multi-Module Structure

The project is organized as a Maven multi-module application with the following modules:

**eladmin-system/** (Main Application)
- Entry point: `me.zhengjie.AppRun`
- Contains all core business logic
- Configuration: `src/main/resources/config/application.yml`

**eladmin-common/** (Shared Components)
- Base entities, DTOs, and MapStruct mappers in `me.zhengjie.common.base`
- AOP aspects in `me.zhengjie.common.aspect` (permission checking, rate limiting)
- Global configurations in `me.zhengjie.common.config`
- Utility classes in `me.zhengjie.common.utils`

**eladmin-logging/** (Audit System)
- System audit logs and operation tracking

**eladmin-tools/** (Third-Party Integrations)
- Email service (`me.zhengjie.tools.service`)
- Cloud storage (S3/local) (`me.zhengjie.tools.service`)
- Payment integration (Alipay)

**eladmin-generator/** (Code Generator)
- Freemarker templates for CRUD code generation
- Templates in `src/main/resources/template/`

### Module Organization Within eladmin-system

```
eladmin-system/
├── me.zhengjie/
│   ├── AppRun.java              # Main Spring Boot application
│   ├── sysrunner/               # Startup initialization
│   └── modules/
│       ├── system/              # Core system modules
│       │   ├── domain/          # JPA entities
│       │   ├── service/         # Business logic
│       │   ├── repository/      # Data access layer
│       │   ├── controller/      # REST endpoints
│       │   └── rest/            # Additional controllers
│       ├── security/            # JWT authentication
│       │   ├── service/         # Auth service, JWT utilities
│       │   └── rest/            # Login/logout endpoints
│       ├── quartz/              # Scheduled tasks
│       │   ├── domain/          # Quartz entities
│       │   ├── service/         # Job management
│       │   └── rest/            # Job controller
│       └── maint/               # Operations management
└── resources/
    ├── config/
    │   ├── application.yml      # Main configuration
    │   ├── application-dev.yml  # Development profile
    │   └── application-prod.yml # Production profile
    └── logback.xml              # Logging configuration
```

### Key Architectural Patterns

1. **Layered Architecture:**
   - Controller Layer (REST endpoints)
   - Service Layer (Business logic)
   - Repository Layer (Data access)
   - Domain Layer (JPA entities)

2. **Common Base Structure:**
   - All entities extend `BaseEntity` (`eladmin-common/me/zhengjie/common/base`)
   - All service implementations extend `BaseService`
   - All repositories extend `JpaRepository`
   - MapStruct mappers in `me.zhengjie.common.base.mapper`

3. **Security Model:**
   - JWT token-based authentication
   - Role-based access control (RBAC)
   - Custom `@PreAuthorize` annotations from `eladmin-common/annotation`
   - Single-user login limitation via Redis

4. **Configuration Patterns:**
   - Global configs in `eladmin-common/me/zhengjie/common/config`
   - Module-specific configs in `eladmin-system/resources/config/`

### Important Configuration Files

| File | Purpose |
|------|---------|
| `eladmin-system/src/main/resources/config/application.yml` | Main application settings (JWT, Redis, DB) |
| `eladmin-system/src/main/resources/config/application-dev.yml` | Dev environment overrides |
| `eladmin-system/src/main/resources/config/application-prod.yml` | Production environment overrides |
| `eladmin-system/src/main/resources/logback.xml` | Logging configuration |
| `eladmin-system/src/main/resources/spy.properties` | P6SQL monitoring |
| `sql/eladmin.sql` | Main database schema |
| `sql/quartz.sql` | Quartz scheduler tables |

### Database Schema

- **Main tables:** User, Role, Menu, Department, Permission
- **System tables:** Logs, Online sessions, User history
- **Quartz tables:** Job scheduling data

### API Documentation

When running the application, API documentation is available at:
- Swagger UI: `/doc.html`
- Knife4j documentation endpoint: `/api`

Access the Druid SQL monitoring dashboard at: `/druid/`

### Development Notes

**Default Test Credentials:** admin / 123456

**Key Features:**
- Real-time user sessions (Redis-backed)
- SQL monitoring with Druid
- System metrics via OSHI
- Remote server management (SSH)
- Code generation for CRUD operations
- Excel import/export (Apache POI)
- Email notifications
- Cloud storage integration (Amazon S3)

**Monitoring Endpoints:**
- Application metrics: `/actuator/metrics`
- Health check: `/actuator/health`
- Server info: `/api/monitor/server` (OSHI)

**Build Information:**
- Java Version: 1.8
- Spring Boot: 2.7.18
- Maven project with modules
- Tests are disabled by default in root POM

### Important Resources

- **README.md** - Comprehensive project documentation and feature list
- **Online Demo** - Available with admin/123456 credentials
- **Apache License 2.0** - Full license in LICENSE file