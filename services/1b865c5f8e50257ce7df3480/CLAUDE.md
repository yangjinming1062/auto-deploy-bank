# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Abixen Platform is a microservices-based enterprise software platform built with Spring Boot. The architecture follows a modular microservices pattern where new functionality is implemented as separate Spring Boot microservices that integrate with the platform through a CMS and configuration system.

**Technology Stack:**
- Java 11+ with Spring Boot 2.6.1
- Spring Cloud 2021.0.0 for microservices
- AngularJS/Frontend with Gulp build system
- PostgreSQL databases
- Docker & Docker Compose for deployment
- Eureka (service discovery), Config Server, Hystrix
- Zipkin (distributed tracing), ELK stack (logging), Grafana (monitoring)

## Architecture

**Microservices (in order of startup):**
1. **Eureka** (`abixen-platform-eureka`) - Service registry/discovery on port 8761
2. **Configuration Server** (`abixen-platform-configuration`) - Centralized config on port 8888
3. **Hystrix Dashboard** (`abixen-platform-hystrix-dashboard`) - Circuit breaker monitoring on port 8989
4. **Gateway** (`abixen-platform-gateway`) - API gateway on port 9090 (requires Redis)
5. **Core** (`abixen-platform-core`) - Core CMS functionality (ports vary by profile)
6. **Business Intelligence Service** (`abixen-platform-business-intelligence-service`) - BI/reporting module
7. **Web Content Service** (`abixen-platform-web-content-service`) - Articles/content management
8. **Web Client** (`abixen-platform-web-client`) - Frontend application (WAR deployment)
9. **Zipkin** (`abixen-platform-zipkin`) - Distributed tracing on port 9411

**Common Package Structure:**
Each microservice follows this pattern:
- `com.abixen.platform.[service].application/` - Business logic, DTOs, converters, services
- `com.abixen.platform.[service].domain/` - Domain models and repositories
- `com.abixen.platform.[service].infrastructure/` - Configuration, persistence, utilities
- `com.abixen.platform.[service].interfaces/` - REST controllers (web/, client/)

## Build Commands

**Maven is the primary build tool.**

```bash
# Build entire platform (skips Docker build)
mvn clean install -DskipDocker

# Run tests only
mvn test

# Run tests with coverage
mvn clean org.jacoco:jacoco-maven-plugin:prepare-agent install -DskipDocker

# Build specific module
cd abixen-platform-core && mvn clean install

# Run single test class
mvn test -Dtest=ClassName

# Run with specific profile
mvn spring-boot:run -Dspring-boot.run.profiles=dev

# Skip Docker build during install
mvn clean install -DskipDocker

# Run Sonar analysis
mvn sonar:sonar -DskipDocker
```

## Running the Platform

**Script-based startup (recommended for development):**
```bash
# Start all services in order
./abixen-platform-run.sh

# Check logs
tail -f nohup.out
```

**Docker Compose (recommended for full environment with logging/monitoring):**
```bash
# Start all components with central logging (consumes ~5GB)
docker-compose up -d

# Scale specific service
docker-compose scale web-client=2

# Check logs
docker-compose logs -f [service-name]

# Access services:
# - Web Client: http://localhost:8080
# - Eureka: http://localhost:8761
# - Kibana (logs): http://localhost:5601
# - Grafana (metrics): http://localhost:3000 (admin/admin)
```

**Linux Elasticsearch Fix:**
If Elasticsearch fails to start with `vm.max_map_count` error:
```bash
sudo sysctl -w vm.max_map_count=262144
```

## Development Requirements

**Code Quality Standards (from CONTRIBUTING.md):**
- Use IntelliJ IDEA with default formatting
- Commit messages must reference an issue from the backlog
- Unit test coverage: 80% or higher (enforced by CI)
- File encoding: UTF-8 with LF line endings
- All code must be properly formatted
- Pull requests must contain single commit

**CI/CD:**
- Travis CI with SonarCloud integration
- Build: `mvn clean org.jacoco:jacoco-maven-plugin:prepare-agent install sonar:sonar -DskipDocker -B -e -V`
- SonarQube analysis runs on every push

**Frontend Build (AngularJS/Gulp):**
Each microservice with frontend components has:
```bash
npm install  # Install Node dependencies
bower install  # Install Bower dependencies
gulp build  # Build frontend assets
gulp  # Development mode with livereload
```

**Code Style:**
- Checkstyle configuration: `checkstyle.xml`
- JSHint configuration: `.jshintrc`
- JSCS configuration: `.jscsrc`

## Configuration

**Database Configuration:**
Each microservice has its own PostgreSQL database:
- Core: `abixen_platform_core`
- Business Intelligence: `abixen_platform_businessintelligence_service`
- Web Content: `abixen_platform_web_content_service`

Default credentials in `docker-compose.yml`:
- User: `abixen`
- Password: `fy2Lkxw201sV`
- Port (Web Content): `5434`

**Spring Profiles:**
- `dev` - Development profile (used by most services)
- Services use `-Dspring.profiles.active=dev` when starting

**Required External Services:**
- Redis (required by Gateway)
- RabbitMQ (for AMQP messaging)
- PostgreSQL instances per microservice

## Key Services

**Gateway Service** (`abixen-platform-gateway`):
- Entry point for all client requests
- Requires Redis session store
- Routes requests to appropriate microservices
- Port: 9090

**Core Service** (`abixen-platform-core`):
- Central CMS functionality
- Page and module management
- User authentication and authorization
- Stores images in mounted volume: `data/image-library`

**Business Intelligence Service** (`abixen-platform-business-intelligence-service`):
- Chart and table visualization
- Supports H2, MySQL, PostgreSQL, Oracle, MSSQL
- Can use Excel/CSV files as data sources
- Port: varies

**Web Content Service** (`abixen-platform-web-content-service`):
- Article management system
- Simple web content (rich text editor)
- Advanced web content (structures and templates)
- Port: varies

**Web Client** (`abixen-platform-web-client`):
- AngularJS-based frontend
- WAR deployment
- Port: 8080 (configured in docker-compose)

## Service Discovery & Configuration

- **Eureka** (http://localhost:8761) - All microservices register here
- **Config Server** (http://localhost:8888) - Centralized configuration
- Services must wait for Eureka and Config Server to be healthy before starting

## Logging & Monitoring

**Centralized Logging (ELK Stack):**
- Logs sent to Logstash via GELF protocol (port 12201/udp)
- Elasticsearch stores logs (port 9200)
- Kibana provides UI (http://localhost:5601)

**Metrics & Monitoring:**
- Jolokia exposes JMX metrics over HTTP
- Telegraf collects metrics and sends to InfluxDB
- Grafana provides dashboards (http://localhost:3000, admin/admin)

## Known Issues

- Not all translations are complete
- Multi Visualization Service UI needs optimization
- CSS improvements needed in some areas
- Minor technical debt exists

## Documentation

- General documentation: https://github.com/abixen/abixen-platform/wiki
- Docker-specific docs: `docker/README.md`
- Architecture diagrams: `documentation-image/`

## Adding New Microservices

To create a new module/microservice:
1. Create new Spring Boot microservice following the package structure
2. Implement required interfaces for Abixen Platform integration
3. Register service with Eureka
4. Configure in platform CMS for business administrators to use
5. Build using Maven with `-DskipDocker` flag
6. Deploy via Docker Compose or run script

## Troubleshooting

**Services won't start:**
- Check Eureka is running (port 8761)
- Check Config Server is running (port 8888)
- Verify Redis is running (required for Gateway)
- Check database connections

**Port conflicts:**
- Eureka: 8761
- Config: 8888
- Hystrix: 8989
- Gateway: 9090
- Web Client: 8080
- Zipkin: 9411
- Kibana: 5601
- Grafana: 3000

**Memory issues:**
- Docker Compose uses ~5GB RAM
- Individual services use 512MB-1024MB heap (configured in docker-compose.yml)