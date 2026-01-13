# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is ThingsBoard (v4.3.0-SNAPSHOT), an open-source IoT platform for data collection, processing, visualization, and device management. It's a Java 17/Spring Boot 3.4.10 application with microservices architecture and an Angular 18 frontend.

## Build and Test Commands

### Building the Project

**Full build:**
```bash
./build.sh
```
This builds and formats license headers using Maven with parallel execution (-T2).

**Build specific modules:**
```bash
./build.sh msa/web-ui,msa/web-report
```

**Clean install with Docker images:**
```bash
mvn clean install -Ddockerfile.skip=false
```

**Build and push Docker images (AMD64/ARM64):**
```bash
mvn clean install -Ddockerfile.skip=false -Dpush-docker-image=true
```

**Build with protobuf:**
```bash
./build_proto.sh
```

### Running Tests

**Run all tests:**
```bash
mvn test
```

**Run tests for specific module:**
```bash
cd <module-directory>
mvn test
```

**Run tests with testcontainers (requires Docker):**
```bash
mvn test -Dtestcontainers.enabled=true
```

### Black Box Tests

Black box tests require Docker images to be built first. Run from `msa/black-box-tests/` directory:

**Run all black box tests:**
```bash
cd msa/black-box-tests
mvn clean install -DblackBoxTests.skip=false
```

**Run with specific configurations:**
```bash
# With Valkey SSL
mvn clean install -DblackBoxTests.skip=false -DblackBoxTests.redisSsl=true

# With Valkey cluster
mvn clean install -DblackBoxTests.skip=false -DblackBoxTests.redisCluster=true

# Hybrid mode (PostgreSQL + Cassandra)
mvn clean install -DblackBoxTests.skip=false -DblackBoxTests.hybridMode=true

# Run locally (without Docker)
mvn clean install -DblackBoxTests.skip=false -DrunLocal=true

# UI tests only
mvn clean install -DblackBoxTests.skip=false -Dsuite=uiTests

# All tests (black-box + UI)
mvn clean install -DblackBoxTests.skip=false -Dsuite=all
```

### Running the Application

**Run with default configuration:**
```bash
java -jar application/target/thingsboard-4.3.0-SNAPSHOT.jar
```

**Run with specific profile:**
```bash
java -jar application/target/thingsboard-4.3.0-SNAPSHOT.jar --spring.config.name=thingsboard
```

## Project Structure

### Maven Modules

The project is organized as a multi-module Maven project:

- **netty-mqtt** - Custom Netty-based MQTT implementation
- **common** - Shared modules across services
  - `actor/` - Actor system components
  - `cache/` - Caching utilities
  - `cluster-api/` - Cluster communication APIs
  - `dao-api/` - Data Access Object interfaces
  - `data/` - Shared data models
  - `message/` - Message passing utilities
  - `queue/` - Queue implementations
  - `transport/` - Protocol transports (MQTT, HTTP, CoAP, LwM2M, SNMP)
  - `util/` - Common utilities
- **rule-engine** - Rule Engine module for data processing
- **dao** - Data Access Layer
- **edqs** - Event Data Query Service
- **transport** - Protocol transports
- **ui-ngx** - Angular 18 frontend application
- **tools** - Utility tools
- **application** - Main Spring Boot application
- **msa** - Microservices Architecture
  - `tb/` - Main ThingsBoard service
  - `transport/` - Transport services (MQTT, HTTP, CoAP, LwM2M, SNMP)
  - `web-ui/` - Web UI service
  - `js-executor/` - JavaScript executor
  - `monitoring/` - Monitoring service
  - `black-box-tests/` - Integration tests
- **rest-client** - REST client for ThingsBoard
- **monitoring** - Platform monitoring

### Entry Points

**Main Application:**
- `application/src/main/java/org/thingsboard/server/ThingsboardServerApplication.java`

**Default Configuration:**
- `application/src/main/resources/thingsboard.yml`

## Architecture

### Microservices Architecture

ThingsBoard follows a microservices architecture with the following services:

1. **tb-node** - Core ThingsBoard server handling most functionality
2. **Transport services**:
   - MQTT (Netty-based implementation)
   - HTTP/HTTPS
   - CoAP
   - LwM2M
   - SNMP
3. **Web UI** - Angular frontend served as a service
4. **JS Executor** - JavaScript rule execution
5. **EDQS** - Event Data Query Service
6. **Monitoring** - Platform monitoring
7. **VC Executor** - Version Control executor

### Key Technologies

- **Java 17** - Primary language
- **Spring Boot 3.4.10** - Application framework
- **Maven** - Build system
- **Angular 18** - Frontend framework
- **TestNG** - Testing framework
- **Allure** - Test reporting
- **Testcontainers** - Integration testing with Docker
- **Protocol Buffers 3.25.5** - Inter-service communication
- **gRPC 1.76.0** - RPC framework
- **Cassandra** - Scalable database option
- **PostgreSQL** - Primary database
- **Redis** - Caching and queues

### Protocol Support

The platform supports multiple IoT protocols:
- MQTT/MQTT over WebSocket
- HTTP/HTTPS
- CoAP
- LwM2M (Lightweight M2M)
- SNMP

### Cloud Integrations

- AWS (SQS, SNS, Lambda)
- Google Cloud (Pub/Sub)
- Azure

## Development Notes

### Lombok

The project uses Lombok extensively. Ensure your IDE has Lombok plugin installed. Configuration file: `lombok.config`

### Protobuf

When modifying `.proto` files, run `./build_proto.sh` to regenerate Java classes.

### Database Migrations

Database schema migrations are managed by Flyway. Migration files are in `application/src/main/resources/db/migrations/`

### Licensing

All source files must include the Apache 2.0 license header. The build script automatically formats license headers using:
```bash
mvn license:format
```

### IDE Configuration

No specific Cursor or Copilot rules exist. Standard Java/Spring Boot/Angular project setup applies.

### Configuration Profiles

- `default` - Standard configuration
- `download-dependencies` - Downloads sources and javadocs

### Docker

Multiple Dockerfiles exist for different services. Images are published to `thingsboard/` organization on Docker Hub.

### Testing Strategy

- **Unit tests** - TestNG, run with `mvn test`
- **Integration tests** - TestNG + Testcontainers
- **Black box tests** - Full system tests in `msa/black-box-tests/`

## Useful Commands

**Check Docker images:**
```bash
docker image ls | grep thingsboard
```

**Run PostgreSQL locally for testing:**
```bash
# Using Docker
docker run -d --name postgres-tb -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=thingsboard postgres:14
```

**Run Cassandra locally for testing:**
```bash
# Using Docker
docker run -d --name cassandra-tb -p 9042:9042 -p 7000:7000 -p 7001:7001 -p 7199:7199 -p 9160:9160 -p 14001:14001 cassandra:4.0
```

**Run Redis locally for testing:**
```bash
# Using Docker
docker run -d --name redis-tb -p 6379:6379 redis:7-alpine
```

## Documentation

- Main README: `/home/ubuntu/deploy-projects/19bc5f63b373d23950accdfe/README.md`
- Docker README: `/home/ubuntu/deploy-projects/19bc5f63b373d23950accdfe/docker/README.md`
- Black box tests: `/home/ubuntu/deploy-projects/19bc5f63b373d23950accdfe/msa/black-box-tests/README.md`
- Security policy: `/home/ubuntu/deploy-projects/19bc5f63b373d23950accdfe/security.md`
- Project website: https://thingsboard.io/
- Documentation: https://thingsboard.io/docs/

## Dependencies

Key dependencies are managed via Spring Boot BOM. Major versions:
- Spring Boot: 3.4.10
- Spring Security: Integrated with Spring Boot
- Netty: 4.1.128.Final
- Cassandra Driver: 4.17.0
- Kafka Client: 3.9.1
- Redis (Jedis): 5.1.5
- JWT (jjwt): 0.12.5
- Protocol Buffers: 3.25.5
- gRPC: 1.76.0