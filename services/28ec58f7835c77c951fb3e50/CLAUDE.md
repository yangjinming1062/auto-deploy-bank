# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ThingsBoard is an open-source IoT platform for data collection, processing, visualization, and device management. It's a distributed, scalable system built on Java 17 with Spring Boot and a TypeScript/Angular frontend.

## Build & Development Commands

### Java Backend (Maven)

```bash
# Full clean build (skips tests)
./build.sh

# Build without running tests
mvn clean install -DskipTests

# Build specific module(s)
mvn clean install --projects <module1>,<module2> --also-make

# Run all tests
mvn test

# Run tests for specific module
mvn test --projects application

# Run single test class
mvn test -Dtest=DeviceControllerTest

# Run tests with tags (blackbox tests)
mvn test -Dgroups=blackbox

# Run tests with Allure reporting
mvn test && allure serve target/allure-results

# License header check
mvn license:check

# Format license headers
mvn license:format
```

### UI (Angular)

UI is located in `ui-ngx/` directory.

```bash
cd ui-ngx

# Install dependencies
npm install
# or
yarn install

# Development server
npm start
# or
yarn start

# Production build
npm run build:prod
# or
yarn build:prod

# Lint code
npm run lint
# or
yarn lint
```

## Architecture

### Module Structure

The project uses a modular architecture with the following key modules:

1. **application** - Main Spring Boot application entry point (`ThingsboardServerApplication.java:42`)
   - REST API controllers (Controller pattern)
   - WebSocket handlers
   - Main application configuration

2. **common** - Shared infrastructure across all modules
   - `data` - Data models and DTOs
   - `queue` - Message queue abstraction (Kafka, Pub/Sub, etc.)
   - `transport` - Protocol adapters (MQTT, HTTP, CoAP, LwM2M, SNMP)
   - `actor` - Akka-inspired actor system for processing
   - `cache` - Caching layer (Redis/Valkey)
   - `message` - Inter-service communication
   - `cluster-api` - Cluster management
   - `discovery-api` - Service discovery

3. **dao** - Data access layer
   - Supports both SQL (PostgreSQL) and NoSQL (Cassandra)
   - Entity and time-series data storage
   - Repository pattern implementation

4. **rule-engine** - Data processing pipeline
   - Rule chains for processing IoT data
   - Custom processors and rule nodes
   - Real-time analytics and alerts

5. **transport** - Device connectivity layer
   - `mqtt` - MQTT protocol support (including v5)
   - `http` - HTTP transport
   - `coap` - CoAP protocol
   - `lwm2m` - Lightweight M2M
   - `snmp` - SNMP protocol

6. **ui-ngx** - Angular frontend
   - Material Design UI
   - NgRx for state management
   - Real-time dashboards and widgets

7. **msa** - Microservices architecture
   - `tb-node` - Main ThingsBoard node service
   - `web-ui` - Standalone web UI service
   - `js-executor` - JavaScript execution service
   - Docker-based deployment configurations

8. **netty-mqtt** - Netty-based MQTT server implementation

### Key Technologies

- **Java 17** with **Spring Boot 3.4.8**
- **Protocol Buffers 3.25.5** for serialization
- **gRPC 1.68.1** for inter-service communication
- **Kafka 3.9.1** or **Google Pub/Sub** for messaging
- **Cassandra 4.17.0** for time-series data
- **PostgreSQL** for entity storage
- **Redis/Valkey** for caching
- **Netty 4.1.124** for transport layers
- **Angular 18** with **NgRx** for UI

### Configuration

Main configuration files:
- `application/src/main/resources/thingsboard.yml` - Main Spring configuration
- `.env` - Environment variables for microservices mode (docker/docker/README.md:1)

The application automatically loads `thingsboard` as the Spring config name unless overridden (`ThingsboardServerApplication.java:38`).

## Testing

### Test Structure

- **Unit tests** - JUnit 5 / TestNG with Mockito
- **Integration tests** - Spring Test with TestContainers
- **Blackbox tests** - Full system tests using Docker Compose (TestNG-based)
- **Allure** - Test reporting framework

### Running Tests

```bash
# All tests
mvn test

# Specific test class
mvn test -Dtest=DeviceServiceTest

# Tests matching pattern
mvn test -Dtest=*ServiceTest

# Integration tests only
mvn test -Dgroups=integration

# Skip tests
mvn clean install -DskipTests

# Run blackbox tests (requires Docker)
mvn test -Dgroups=blackbox -pl black-box-tests

# With Allure report
mvn test
allure generate target/allure-results
allure open
```

### Test Configuration

- Uses **TestContainers** for database and service dependencies
- Database tests use **DBUnit** for data setup
- Mock external services with **MockServer**
- Allure reports generated in `target/allure-results`

## Docker & Deployment

### Building Docker Images

```bash
# Build all Docker images
docker-compose build

# Build specific service
docker-compose build tb-node
```

### Running in Microservices Mode

See `docker/README.md:1` for complete setup instructions.

```bash
# Create log folders (requires sudo)
./docker/docker-create-log-folders.sh

# Install with demo data
./docker/docker-install-tb.sh --loadDemo

# Start services
./docker/docker-start-services.sh
```

Supports multiple database configurations:
- `postgres` - PostgreSQL only
- `hybrid` - PostgreSQL + Cassandra

Supports multiple cache configurations:
- `valkey` - Single node
- `valkey-cluster` - Cluster mode
- `valkey-sentinel` - Sentinel mode

## Security

Security vulnerabilities should be reported privately to **security@thingsboard.io** (security.md:8). Do not use GitHub issues for security reports.

## License

This project uses **Apache 2.0 License** (LICENSE:1).