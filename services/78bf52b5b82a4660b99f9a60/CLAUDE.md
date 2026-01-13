# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## CloudExplorer-Lite Overview

CloudExplorer-Lite is an open-source lightweight cloud management platform that supports managing multi-cloud infrastructure (公有云/私有云). It provides out-of-the-box features for virtual machine management, cloud billing, operational analysis, and security compliance.

**Technology Stack:**
- Frontend: Vue3.js + Element Plus + TypeScript + Vite
- Backend: Spring Boot 3.1.0 + Java 17
- Database: MySQL
- Infrastructure: Docker
- Microservices architecture with Eureka service discovery

## Common Development Commands

### Root Level Commands (Yarn Workspaces)

Install all dependencies:
```bash
yarn install
```

Build all frontends:
```bash
yarn build
```

Lint all frontends:
```bash
yarn lint
```

Dev all frontends:
```bash
yarn dev
```

### Module-Specific Commands

**Base Framework:**
```bash
yarn dev:base       # Start ce-base framework
yarn build:base     # Build ce-base
yarn lint:base      # Lint ce-base
```

**Management Center:**
```bash
yarn dev:manage     # Start management-center frontend
yarn build:manage   # Build management-center
yarn lint:manage    # Lint management-center
```

**Services:**
```bash
yarn dev:vm        # Start vm-service frontend
yarn build:vm      # Build vm-service
yarn lint:vm       # Lint vm-service

yarn dev:bill      # Start finance-management frontend
yarn build:bill    # Build finance-management
yarn lint:bill     # Lint finance-management

yarn dev:security  # Start security-compliance frontend
yarn build:security
yarn lint:security

yarn dev:operation # Start operation-analysis frontend
yarn build:operation
yarn lint:operation
```

**Individual Module Development:**
```bash
yarn workspace <module-name> run dev
yarn workspace <module-name> run build-only
yarn workspace <module-name> run lint
yarn workspace <module-name> run test:unit
```

### Maven Commands

Initialize VMware dependencies (run once after clone):
```bash
mvn initialize
```

Backend build:
```bash
mvn clean package -DskipTests
```

### Docker/Deployment

Build core Docker image:
```bash
./build-core-image.sh
```

Build service packages:
```bash
./build-service-packages.sh
```

Create Docker Compose:
```bash
./build-core-docker-compose.sh
```

## Project Architecture

### Directory Structure

```
/
├── framework/          # Core framework modules
│   ├── eureka/        # Service discovery (port: 8761)
│   ├── gateway/       # API Gateway (port: 8080)
│   ├── management-center/  # Management console
│   ├── provider/      # Cloud provider connectors
│   └── sdk/           # Shared frontend SDK (ce-base)
├── services/          # Microservices
│   ├── vm-service/    # Virtual machine management
│   ├── finance-management/  # Cloud billing
│   ├── security-compliance/  # Security & compliance
│   └── operation-analysis/   # Operational analytics
└── demo/              # Module template generator
```

### Microservices Architecture

The application uses a microservices architecture with:

1. **Eureka Service Discovery**: Handles service registration and discovery
2. **Gateway**: Spring Cloud Gateway that routes requests to microservices
   - Dynamic routing based on service names
   - BasePath handling with strip/prefix filters
   - Aggregates Swagger docs from all services
3. **Management Center**: Admin console backend/frontend
4. **Microservices**: Independent services with their own databases and functionality
   - Each service has both frontend (Vue3) and backend (Spring Boot)
   - Services register with Eureka and are discoverable via Gateway

### Frontend Architecture

- **Vite-based Vue 3** application with TypeScript
- **Element Plus** UI component library
- **Micro-frontend architecture**: Each service is a separate micro-app
- **Shared SDK**: `framework/sdk/frontend/commons` contains common components and utilities
- **Environment Configuration**: Each frontend has `.env.development`, `.env.production` files
- **Build System**: Vite with alias support (`@` for src, `@commons` for shared SDK)

### Backend Architecture

- **Spring Boot 3.1.0** with Java 17
- **Spring Cloud** for microservices (Eureka, Gateway)
- **MyBatis Plus** for ORM with Flyway migrations
- **Quartz** for scheduled tasks
- **JWT** authentication with custom headers (CE-TOKEN, CE-ROLE, CE-SOURCE)
- **Modular Design**: Each service is self-contained with its own:
  - Spring Boot application
  - Database schema (Flyway migrations)
  - REST API endpoints
  - Permission system (see Development Guidelines)
  - Scheduled jobs configuration

## Development Guidelines

### Environment Setup

1. Install JDK 17, Maven 3.8.8, Node.js (v19.8.1), and Docker
2. Enable corepack for Yarn: `corepack enable`
3. Run `mvn initialize` to set up VMware dependencies
4. Run `yarn install` to install all frontend dependencies

### API Authentication

Backend endpoints require these headers:
```
CE-TOKEN: <JWT token from login>
CE-ROLE: <ADMIN|ORGADMIN|USER>
CE-SOURCE: <organization/workspace id for non-admin users>
```

### Creating New Modules

Use the module template generator in `demo/src/test/java/CreateModuleUtil.java`:
1. Modify module name, display names, ports
2. Run the `createModule()` method
3. Update the new module's configuration files
4. Add dev/lint scripts to root `package.json`

### Permission System

Backend permissions are defined in each module's `PermissionConstants.java` and checked using:
```java
@PreAuthorize("@cepc.hasCePermission('USER:READ')")
```

Frontend permissions use the `v-hasPermission` directive or `permissionStore.hasPermission()`:
```html
<div v-hasPermission="'[vm-service]CLOUD_SERVER:STOP'"></div>
```

### Scheduled Jobs

Configure jobs in `JobConstants.java`. Two types:
- **Cron Expression Jobs**: Run on fixed schedule
- **Interval Jobs**: Run at fixed intervals
- **Groups**: SYSTEM_GROUP (system-wide) or per-cloud-account groups

## Key Configuration Files

### Frontend
- `/frontend/vite.config.ts`: Vite configuration with proxy setup
- `/frontend/env/.env.development`: Environment variables for dev
- `/frontend/env/.env.production`: Environment variables for production
- `.eslintrc.cjs`: ESLint configuration

### Backend
- `pom.xml`: Maven dependencies and modules
- `src/main/resources/application.yml`: Spring Boot configuration
- Module-specific config: `{module-name}.yml` in module root
- Logback configuration: `logback-spring.xml`

## Database Migrations

- **Flyway** is used for database migrations
- Migration files: `src/main/resources/db/migration/`
- Each module has its own migration files
- Tables are prefixed with module name

## Testing

### Frontend Testing
```bash
yarn workspace <module-name> run test:unit
# or
vitest --environment jsdom
```

### Backend Testing
```bash
mvn test
```

## Build and Deployment

The project uses a multi-stage build process:
1. **Java services** are built with Maven into JAR files
2. **Frontend** modules are built with Vite into static assets
3. **Docker images** are created for the core platform
4. **Service packages** are created as tar.gz archives with configs

## Important Notes

- Each service frontend runs on its own port (configurable in `.env` files)
- Services are proxied through the Gateway at `/service-name/**` paths
- Eureka metadata includes display names, icons, and ordering for UI
- All services share the same authentication mechanism (JWT)
- The platform uses a plugin architecture (PF4J) for cloud provider connectors
- Database changes should always be done via Flyway migrations
- API documentation is aggregated at the Gateway level and accessible via Swagger UI

## Security Contact

For security issues, contact: xin.bai@fit2cloud.com, support@fit2cloud.com, or 400-052-0755