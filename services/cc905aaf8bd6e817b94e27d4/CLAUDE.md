# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a **Java rapid development framework** based on Spring Boot + Vue 3 with a microservices architecture. It's a digital infrastructure platform implementing a "three-person management" model (系统管理员/安全保密员/安全审计员) with support for multi-tenancy, containerization, and domestic (Chinese) IT ecosystems.

### Tech Stack

- **Backend**: Spring Boot 2.7.18, Spring Cloud 2021.0.8, JDK 11
- **Frontend**: Vue 3.3, Vite 4.x, Element Plus, TypeScript
- **Database**: MySQL 5.7/8.0, Redis 6.2+, Elasticsearch 7.9+
- **Other**: Kafka, Nacos, CAS 6.6.15

## Repository Structure

```
y9-digitalbase                    # Root multi-module Maven project
├── y9-digitalbase-common          # Common utilities and shared libraries
├── y9-digitalbase-dependencies    # Dependency management BOM
├── y9-digitalbase-example         # Example/demo projects
├── y9-digitalbase-idcode          # Unified code (MA码) module
├── y9-digitalbase-starter         # Spring Boot starters (auto-config)
├── y9-digitalbase-support         # Business support modules
├── y9-digitalbase-module          # Core business modules
│   ├── y9-module-platform         # Main platform service (port 8080)
│   ├── y9-module-sso              # Single sign-on server (port 7055)
│   ├── y9-module-log              # Logging service (port 7056)
│   └── y9-module-filemanager      # File management service
└── vue/y9vue-kernel-standard      # Frontend Vue 3 application
```

## Common Commands

### Backend (Maven)

```bash
# Build the entire project
mvn clean install

# Build without running tests
mvn clean install -DskipTests

# Build a specific module
cd y9-digitalbase-module/y9-module-platform/risenet-y9boot-server-platform
mvn clean package

# Run tests for a specific module
cd y9-digitalbase-module/y9-module-platform/risenet-y9boot-server-platform
mvn test

# Run a single test class
mvn test -Dtest=ClassName

# Package only (creates WAR/JAR)
mvn clean package -DskipTests

# Build with specific environment profile
# Profiles: env-local, env-dev, env-test, env-prod, env-demo
mvn clean install -Penv-dev

# Generate Javadoc
mvn javadoc:javadoc

# Run Spring Boot application
java -jar target/*.war
# or
mvn spring-boot:run

# Build Docker image (uses Jib plugin)
mvn clean package -DskipTests jib:build
```

### Frontend (Vue 3 + Vite)

```bash
cd vue/y9vue-kernel-standard

# Install dependencies
pnpm install
# or
npm install

# Development server
pnpm run serve
# or for local environment
pnpm run serve-local

# Build for production
pnpm run build

# Preview production build
pnpm run preview

# Optimize SVG icons
pnpm run svgo
```

### Code Quality

```bash
# Format Java code (requires Eclipse formatter config)
# Install "Adapter for Eclipse Code Formatter" plugin in IntelliJ IDEA
# Import formatter from: style/eclipse-formatter.xml

# Java style rules follow Alibaba P3C standards
# Use plugin: Alibaba Java Coding Guidelines (XenoAmess TPM)

# Frontend linting
cd vue/y9vue-kernel-standard
pnpm run lint
```

## Key Modules

### Core Platform (`y9-digitalbase-module/y9-module-platform`)

**Main service** running on port 8080 with context path `/server-platform`

Key components:
- `risenet-y9boot-server-platform` - Main REST API server
- `risenet-y9boot-support-platform-service` - Business logic layer
- `risenet-y9boot-support-platform-web` - Web controllers
- `risenet-y9boot-api-interface-platform` - API interfaces
- `risenet-y9boot-api-feignclient-platform` - Feign clients
- `risenet-y9boot-support-platform-jpa-repository` - Data access layer

### SSO Module (`y9-digitalbase-module/y9-module-sso`)

**Single Sign-On server** running on port 7055

Key components:
- `risenet-y9boot-webapp-sso` - Main SSO application
- `risenet-y9boot-webapp-sso-jpa` - SSO with JPA persistence
- `risenet-y9boot-common-sso` - Shared SSO components

Supports OAuth 2.0, CAS, OIDC protocols

### Logging Module (`y9-digitalbase-module/y9-module-log`)

**Logging service** running on port 7056

Components:
- `risenet-y9boot-server-log` - Core logging service
- `risenet-y9boot-server-log-jpa` - Logging with JPA
- `risenet-y9boot-support-log-service` - Logging business logic
- `risenet-y9boot-support-log-web` - Logging web layer
- `risenet-y9boot-api-feignclient-log` - Feign clients

### Starter Modules (`y9-digitalbase-starter`)

Auto-configuration Spring Boot starters:
- `risenet-y9boot-starter-security` - Security configuration
- `risenet-y9boot-starter-web` - Web MVC configuration
- `risenet-y9boot-starter-jpa-public` - Public JPA repositories
- `risenet-y9boot-starter-jpa-tenant` - Multi-tenant JPA
- `risenet-y9boot-starter-cache-redis` - Redis caching
- `risenet-y9boot-starter-kafka` - Kafka integration
- `risenet-y9boot-starter-liquibase` - Database migration
- `risenet-y9boot-starter-permission` - Permission system
- `risenet-y9boot-starter-sso-oauth2-resource` - OAuth2 resource server
- And more...

## Development Workflow

### 1. Set Up Development Environment

Required:
- JDK 11
- Maven 3.6+
- Node.js 16+ and pnpm/npm
- MySQL 5.7/8.0
- Redis 6.2+
- Kafka (optional)
- Elasticsearch (optional)

### 2. Configure Database

Default MySQL connection (in `application.yml`):
```yaml
datasource:
  druid:
    y9-public:
      url: jdbc:mysql://localhost:3306/y9_public
      username: root
      password: 111111
```

Create database and import schema:
- Liquibase is used for schema migration
- Initial data loaded via Liquibase changelogs

### 3. Run Core Services

Start services in this order:

```bash
# 1. Start SSO (port 7055)
cd y9-digitalbase-module/y9-module-sso/risenet-y9boot-webapp-sso-jpa
mvn spring-boot:run

# 2. Start Platform (port 8080)
cd y9-digitalbase-module/y9-module-platform/risenet-y9boot-server-platform
mvn spring-boot:run

# 3. Start Logging (port 7056)
cd y9-digitalbase-module/y9-module-log/risenet-y9boot-server-log-jpa
mvn spring-boot:run

# 4. Start Frontend (port 5173)
cd vue/y9vue-kernel-standard
pnpm run serve
```

### 4. Access Points

- **Frontend**: http://localhost:5173/kernel-standard
- **Platform API**: http://localhost:8080/server-platform
- **SSO API**: http://localhost:7055
- **Logging API**: http://localhost:7056/server-log

## Configuration

### Environment Profiles

| Profile | Purpose | Directory |
|---------|---------|-----------|
| env-local | Local development | `src/main/resources/profiles/local` |
| env-dev | Team development | `src/main/resources/profiles/dev` |
| env-test | Testing | `src/main/resources/profiles/test` |
| env-prod | Production | `src/main/resources/profiles/prod` |
| env-demo | Demo | `src/main/resources/profiles/demo` |

Activate profile:
```bash
mvn spring-boot:run -Dspring-boot.run.profiles=env-dev
```

### Key Configuration Files

- `pom.xml` - Maven configuration, dependencies, plugins
- `application.yml` - Spring Boot configuration
- `smart-doc.json` - API documentation configuration
- `src/main/resources/profiles/{env}/` - Environment-specific configs

### Nacos Configuration

The platform uses Nacos for external configuration:

```yaml
spring:
  cloud:
    nacos:
      config:
        enabled: true
        namespace: test
        group: DEFAULT_GROUP
```

Default disabled in test config (`config.enabled: false`)

## Code Style and Standards

### Java Style

- **Standard**: Alibaba P3C coding conventions
- **Formatter**: Eclipse formatter (see `style/eclipse-formatter.xml`)
- **Line length**: 120 characters max
- **IDE Setup**: Install "Adapter for Eclipse Code Formatter" in IntelliJ IDEA

### Import Order

Configured in `style/eclipse.importorder`

### Frontend Style

- **Linting**: ESLint + Prettier
- **Formatter**: Prettier
- **Language**: TypeScript 4.6+
- **Build**: Vite 4.x

### Documentation

- **JavaDoc**: Required for public APIs (can be generated with `mvn javadoc:javadoc`)
- **API Docs**: Generated using smart-doc-maven-plugin
  - Outputs to: `target/`, formats: HTML, Markdown

## Testing

### Backend Tests

```bash
# Run all tests
mvn test

# Run specific test class
mvn test -Dtest=UserServiceTest

# Run tests with coverage
mvn test jacoco:report

# Run integration tests only
mvn test -Dtest=*IntegrationTest
```

Test locations:
- `src/test/java` - Test classes
- `src/test/resources` - Test resources
- `src/test/resources/application.yml` - Test configuration

### Frontend Tests

```bash
cd vue/y9vue-kernel-standard
pnpm run test:unit
```

## Database Management

### Liquibase (Migration)

Auto-enabled for both public and tenant databases:
```yaml
y9:
  feature:
    liquibase:
      public-enabled: true
      tenant-enabled: true
```

Migration files location: `src/main/resources/db/changelog/`

### Multi-Tenant Data Source

The framework supports dynamic multi-tenant databases:
- Tenant datasource naming: `y9_{tenantShortName}_{randomStr}`
- Configuration in `y9-digitalbase-common/risenet-y9boot-common-tenant-datasource`

## API Documentation

Auto-generated using smart-doc:

```bash
# Generate during build
mvn clean package

# Output locations:
# - target/classes/static/doc/ - HTML docs
# - target/classes/static/doc/markdown - Markdown docs
```

Access API docs at: `http://localhost:8080/server-platform/doc.html`

## Common Issues & Solutions

### 1. Port Conflicts

Default ports:
- Platform: 8080
- SSO: 7055
- Logging: 7056
- Frontend: 5173

Change in `application.yml`:
```yaml
server:
  port: 8081
```

### 2. Nacos Connection Issues

If Nacos is not configured, ensure it's disabled:
```yaml
spring:
  cloud:
    nacos:
      config:
        enabled: false
      discovery:
        enabled: false
```

### 3. Database Connection Issues

Verify MySQL is running and credentials are correct in `application.yml`

### 4. Redis Issues

Ensure Redis is running on port 6379 with password (default: 111111)

### 5. Maven Build Fails

Try cleaning and rebuilding:
```bash
mvn clean install -U -DskipTests
```

### 6. Frontend Build Issues

Clear node_modules and reinstall:
```bash
cd vue/y9vue-kernel-standard
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

## Important Notes

1. **Three-Person Management**: The platform implements a unique security model with System Admin (系统管理员), Security Officer (安全保密员), and Security Auditor (安全审计员) roles

2. **Multi-Tenancy**: Built-in support for multi-tenant data isolation

3. **CAS SSO**: Single Sign-On is mandatory - all services require authentication

4. **API Security**: All `/api/*` endpoints are protected by OAuth2 resource server

5. **Chinese Localization**: Designed for Chinese government/enterprise use with built-in support for MA codes (统一标识码)

6. **Code Generation**: There's a separate code generator project: https://gitee.com/risesoft-y9/y9-code-generator

## Documentation Links

- **Project Docs**: https://docs.youshengyun.com/
- **Source Code**: https://gitee.com/risesoft-y9/y9-core
- **Demo**: https://demo.youshengyun.com/kernel-standard/
- **Default Credentials**:
  - System Admin: `systemManager` / `Risesoft@2024`
  - Security Officer: `securityManager` / `Risesoft@2024`
  - Security Auditor: `auditManager` / `Risesoft@2024`