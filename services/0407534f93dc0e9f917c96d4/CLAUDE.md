# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Yudao Cloud** is a Java-based Spring Cloud microservices platform. It's a production-ready, enterprise-grade system with:
- **Backend**: Java 8 + Spring Boot 2.7.18 + Spring Cloud Alibaba 2021
- **Architecture**: 16 microservices modules with Spring Cloud
- **Build Tool**: Maven (multi-module)
- **Testing**: 116+ JUnit 5 tests with custom `BaseDbUnitTest` framework
- **CI/CD**: GitHub Actions (tests on Java 8, 11, 17)

See the full [README.md](README.md) for complete documentation, demo URLs, and feature lists.

## High-Level Architecture

### Core Modules Structure

```
yudao-dependencies/    # Maven BOM for dependency management
yudao-framework/       # Core framework (20+ Spring Boot starters)
yudao-server/          # Main application server
yudao-gateway/         # API Gateway service
yudao-module-system/   # System management (users, roles, permissions)
yudao-module-infra/    # Infrastructure (config, cache, files)
yudao-module-bpm/      # Business Process Management (Flowable)
yudao-module-pay/      # Payment module (Alipay, WeChat)
yudao-module-report/   # Reporting module
yudao-module-member/   # Member center
yudao-module-mp/       # WeChat Mini-Program
yudao-module-mall/     # E-commerce (product, trade, promotion)
yudao-module-erp/      # Enterprise Resource Planning
yudao-module-crm/      # Customer Relationship Management
yudao-module-ai/       # AI/LLM integration (commented out)
yudao-module-iot/      # Internet of Things
yudao-ui/              # Frontend UIs (separate repos: Vue2/Vue3/Uni-app)
sql/                   # Database initialization (MySQL, PostgreSQL, Oracle, etc.)
script/                # Deployment scripts and IDE configs
```

### Technology Stack

- **Registry & Config**: Nacos 2.3.2
- **Gateway**: Spring Cloud Gateway 3.4.1
- **Database**: MyBatis Plus, MySQL/PostgreSQL/Oracle/SQL Server/DB2, Redis 5/6
- **Security**: Spring Security 5.7.5 + Token + Redis
- **Messaging**: Event, Redis, RabbitMQ, Kafka, RocketMQ 5.2.0
- **Workflow**: Flowable 6.8.0
- **Monitoring**: SkyWalking 8.12.0, Spring Boot Admin 2.7.10
- **Build**: Maven with Lombok + MapStruct annotation processing

### Microservices Infrastructure

- **Service Discovery & Config**: Nacos
- **API Gateway**: yudao-gateway module
- **Service Protection**: Sentinel 1.8.6
- **Distributed Transactions**: Seata 1.6.1
- **Scheduled Tasks**: XXL-Job 2.3.1
- **Distributed Lock/Idempotency/Rate Limit**: Redis-based implementation

## Common Development Commands

### Building the Project

```bash
# Build entire project (runs tests by default)
mvn -B package

# Build without running tests
mvn -B package -Dmaven.test.skip=true

# Clean build
mvn clean package

# Build specific module
mvn -B package -pl yudao-module-system

# Build with parallel threads
mvn -B package -T 4
```

### Running Tests

Tests are executed automatically via Maven Surefire Plugin (JUnit 5):

```bash
# Run all tests
mvn test

# Run specific module tests
mvn test -pl yudao-module-system

# Run specific test class
mvn test -Dtest=RoleServiceImplTest

# Run tests with custom BaseDbUnitTest framework
# Tests extend BaseDbUnitTest for database unit testing
```

The project includes 116+ unit tests with a custom testing framework (`yudao-spring-boot-starter-test`) providing `BaseDbUnitTest` for database unit testing.

### Docker Deployment

```bash
# Start all services with Docker Compose
cd script/docker/
docker-compose up -d

# This starts:
# - Nacos (registry & config)
# - SkyWalking APM
# - All microservices
# - MySQL, Redis dependencies
```

**Note**: Docker Compose uses host networking mode and includes SkyWalking APM integration with health checks.

### Development Workflow

1. **IDE Setup**:
   - Import project as Maven project in IntelliJ IDEA
   - Configure HTTP Client environment using `script/idea/http-client.env.json`
   - Lombok and MapStruct annotation processing configured in pom.xml

2. **Database Setup**:
   - Choose database from `/sql/` directory (MySQL, PostgreSQL, Oracle, etc.)
   - Import initialization scripts
   - Configure connection in `application.yaml`

3. **API Testing**:
   - Use IntelliJ IDEA HTTP Client with environments configured in `script/idea/http-client.env.json`
   - Base URLs: Local and Gateway environments pre-configured
   - API documentation via Knife4j (Swagger) at `/doc.html`

## Code Generation & Development Tools

### Built-in Code Generator (`yudao-module-infra`)

The platform includes a comprehensive code generator that creates:
- Java backend code (Controller, Service, Mapper, POJO)
- Vue frontend code
- SQL scripts
- Unit tests
- API documentation

Supports:
- Single table CRUD
- Tree table (hierarchical data)
- Master-slave table (parent-child relationships)

### Key Configuration Files

- **Root `pom.xml`**: Manages dependencies across all modules, includes Huawei Cloud and Aliyun Maven mirrors
- **`lombok.config`**: Lombok configuration for consistent code generation
- **`application.yaml`**: Spring Boot configurations per module (16 total)
- **16 `Dockerfile`**: Individual service containerization
- **`.github/workflows/maven.yml`**: CI/CD pipeline with multi-Java version testing

## Testing Framework Details

### Custom Test Framework

The project uses a custom test starter: `yudao-spring-boot-starter-test`

- **Base Class**: `BaseDbUnitTest` for database unit testing
- **Framework**: JUnit 5 (Jupiter) + Mockito
- **Test Structure**: Tests follow standard Maven structure (`src/test/java/`)
- **Examples**:
  - Service tests: `RoleServiceImplTest`, `DeptServiceImplTest`
  - Controller tests: `OAuth2OpenControllerTest`
  - Client tests: SMS clients, Mail services

### Test Execution

```bash
# Via Maven Surefire Plugin (configured in pom.xml)
mvn test

# Skip tests during build
mvn -B package -Dmaven.test.skip=true
```

## Multi-Database Support

The platform supports 9+ databases:
- MySQL 5.7/8.0+
- PostgreSQL
- Oracle
- SQL Server
- MariaDB
- DB2
- OpenGauss
- Kingbase
- DM (达梦)

Database-specific SQL scripts are in the `/sql/` directory with initialization and migration files.

## Frontend Architecture

**Important**: Frontend code is in separate repositories:
- Vue3 + element-plus: `yudao-ui-admin-vue3`
- Vue3 + vben (ant-design-vue): `yudao-ui-admin-vben`
- Vue2 + element-ui: `yudao-ui-admin-vue2`
- Uni-app admin: `yudao-ui-admin-uniapp`
- Uni-app mall: `yudao-mall-uniapp`

The `/yudao-ui/` directory contains placeholder README files with links to actual frontend repos.

Demo URLs (from README.md):
- Vue3 + element-plus: <http://dashboard-vue3.yudao.iocoder.cn>
- Vue3 + vben: <http://dashboard-vben.yudao.iocoder.cn>
- Vue2 + element-ui: <http://dashboard.yudao.iocoder.cn>

## Version Information

- **Current**: `master` branch = JDK 8 + Spring Boot 2.7.18
- **Alternative**: `master-jdk17` branch = JDK 17/21 + Spring Boot 3.2

See README.md section "版本说明" for details on full vs. lite editions.

## Key Dependencies in yudao-framework

The `yudao-framework` module provides 20+ Spring Boot starters including:
- Web, Security, Mybatis, MQ (Message Queue)
- Job (scheduled tasks), WebSocket, Monitor
- Common utilities and shared components

These starters encapsulate common functionality across all microservices.

## CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/maven.yml`):
- Tests on Java 8, 11, and 17
- Ubuntu Latest runner
- Temurin JDK distribution
- Maven caching for faster builds
- Push-triggered builds

## Important Notes

1. **Lombok & MapStruct**: Annotation processing is configured in pom.xml. Ensure IDE has annotation processing enabled.

2. **API Documentation**: Available via Knife4j at `/doc.html` endpoint (SpringDoc OpenAPI 3).

3. **Multi-tenant Support**: Built-in SaaS multi-tenancy with tenant management module.

4. **Security**: Spring Security + Token-based authentication with Redis backend, supports SSO.

5. **Code Quality**: 113,770 lines of Java code with 42,462 lines of comments (as documented in README.md).

6. **Documentation**: Comprehensive README.md (399 lines) includes architecture diagrams, feature lists, and technology stack details.

7. **License**: MIT License - 100% free for personal and commercial use.

## Quick Start Resources

- Quick Start Guide: <https://cloud.iocoder.cn/quick-start/>
- Video Tutorials: <https://cloud.iocoder.cn/video/>
- Migration Guide (Full → Lite): <https://cloud.iocoder.cn/migrate-module/>
- BPM Documentation: <https://doc.iocoder.cn/bpm/>