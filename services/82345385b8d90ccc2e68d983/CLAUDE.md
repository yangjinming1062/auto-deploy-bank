# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jiron Cloud is a comprehensive data development platform built on Spring Cloud. The platform integrates multiple big data tools including Datavines (data quality), DolphinScheduler (workflow scheduling), OpenMetadata (metadata management), Dinky (real-time processing), and FlinkCDC (data integration).

## Technology Stack

- **Java**: 1.8
- **Framework**: Spring Boot 2.7.18, Spring Cloud 2021.0.8, Spring Cloud Alibaba 2021.0.5.0
- **Build Tool**: Maven
- **Database**: MySQL 5.7
- **Cache**: Redis
- **Service Discovery**: Nacos
- **Deployment**: Docker, docker-compose

## Repository Structure

### Core Modules

- **jiron-gateway** (port 8080) - Spring Cloud Gateway entry point
- **jiron-auth** (port 9200) - Authentication and authorization service
- **jiron-common** - Shared common modules:
  - jiron-common-core - Core utilities and constants
  - jiron-common-security - Security configuration
  - jiron-common-datasource - Multi-datasource support
  - jiron-common-log - Logging annotation
  - jiron-common-redis - Redis support
  - jiron-common-seata - Distributed transactions (Seata)
  - jiron-common-sensitive - Data masking
  - jiron-common-datascope - Data permission scope
  - jiron-common-swagger - Swagger API documentation
  - jiron-common-translation - Internationalization
- **jiron-api** - API interfaces for remote services:
  - jiron-api-system - System API (user, dept, role, etc.)
  - jiron-api-dolphinscheduler - DolphinScheduler integration
- **jiron-modules** - Business modules:
  - jiron-system (port 9201) - System management (user, role, dept, menu, dict, notice, log)
  - jiron-gen (port 9202) - Code generation
  - jiron-job (port 9203) - Job scheduling (XXL-JOB)
  - jiron-file (port 9300) - File management
- **jiron-visual** - Monitoring and visualization:
  - jiron-monitor (port 9100) - Spring Boot Admin monitoring

## Common Development Commands

### Build Commands

```bash
# Build all modules (skip tests by default)
mvn clean package -DskipTests

# Build specific module
mvn clean package -DskipTests -pl jiron-gateway -am

# Compile only (no packaging)
mvn clean compile

# Run tests (if any exist)
mvn test
```

### Development Workflow

1. **Initialize Database**:
   - Import SQL files from `/sql` directory:
     - jiron-cloud.sql (main schema)
     - jiron-cloud-config.sql (configuration data)
     - jiron-cloud-seata.sql (Seata distributed transaction tables)

2. **Start Infrastructure Services** (MySQL, Redis, Nacos):
   ```bash
   cd docker
   sh deploy.sh base
   ```

3. **Build Application JARs**:
   ```bash
   mvn clean package -DskipTests
   ```

4. **Copy JARs to Docker Context**:
   ```bash
   cd docker
   sh copy.sh
   ```

5. **Start Application Services**:
   ```bash
   sh deploy.sh modules
   ```

6. **Open Required Ports** (if firewall enabled):
   ```bash
   sh deploy.sh port
   ```

### Docker Operations

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose stop

# Remove all containers
docker-compose rm

# View logs
docker-compose logs -f [service_name]
```

### Deployment Scripts

- **deploy.sh**: Main deployment script
  - `port` - Open required firewall ports
  - `base` - Start infrastructure (MySQL, Redis, Nacos)
  - `modules` - Start application services
  - `stop` - Stop all services
  - `rm` - Remove all services

- **copy.sh**: Copies build artifacts to Docker context

### Service Ports

- 80 - Nginx (frontend)
- 8080 - Gateway
- 8848 - Nacos
- 9100 - Monitor
- 9200 - Auth
- 9201 - System
- 9202 - Gen
- 9203 - Job
- 9300 - File
- 3306 - MySQL
- 6379 - Redis

## Key Architecture Patterns

### Service Discovery & Configuration
- Uses **Nacos** for service discovery and configuration management
- Each service registers with Nacos on startup

### Authentication Flow
- Gateway handles authentication and routing
- `jiron-auth` service manages JWT token generation and validation
- Security context maintained via thread-local storage

### Data Access Pattern
- **Dynamic Datasource**: Supports multiple data sources with `@Master` and `@Slave` annotations
- **Data Scope**: Implements row-level permission control via `@DataScope` annotation
- **Distributed Transactions**: Uses Seata for cross-service transaction management

### Common Utilities
Located in `jiron-common-core`:
- `StringUtils`, `DateUtils`, `Convert` - General utilities
- `JwtUtils` - JWT token handling
- `ServletUtils` - HTTP request/response utilities
- `ExcelUtil` - Excel import/export
- `PageUtils` - Pagination support
- `BeanUtils` - Bean property copying
- `ReflectUtils` - Reflection utilities
- Exception hierarchy in `com.jiron.common.core.exception`

### API Design
- Standardized response format: `R<T>` or `AjaxResult`
- RESTful API endpoints
- Swagger documentation available at `/doc.html`
- Global exception handling with `@ControllerAdvice`

## Database Configuration

Default database settings (in docker-compose.yml):
- **Database**: ry-cloud
- **Username**: root
- **Password**: password
- **MySQL Version**: 5.7

## Configuration Files

- **Nacos Configuration**: `./docker/nacos/conf/application.properties`
- **Redis Configuration**: `./docker/redis/conf/redis.conf`
- **Nginx Configuration**: `./docker/nginx/conf/nginx.conf`
- **Database Schema**: `/sql/jiron-cloud.sql`

## Important Notes

1. **Build Target**: JAR files are built to `/target` directories and must be copied to Docker context using `copy.sh` before deployment

2. **Test Coverage**: No test files detected in the repository - build skips tests by default

3. **Dependency Versions**: Versions managed in parent `pom.xml` properties section

4. **Thread Safety**: Uses `TransmittableThreadLocal` for maintaining context across thread pools

5. **XSS Protection**: Gateway includes XSS filter configuration

6. **File Upload**: Configured via `jiron-file` module with upload path in Docker volume

## Service Dependencies

### Base Infrastructure (must start first):
- MySQL → Nacos (depends on MySQL)

### Application Services:
- Gateway → Redis
- Auth → Redis
- System → Redis, MySQL
- Gen → MySQL
- Job → MySQL
- File → (standalone)
- Nginx → Gateway

## Access URLs

- **Gateway**: http://localhost:8080
- **Nacos Console**: http://localhost:8848/nacos
- **Monitor**: http://localhost:9100
- **API Documentation**: http://localhost:8080/doc.html