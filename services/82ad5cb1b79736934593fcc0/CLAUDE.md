# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

JetLinks is an enterprise-grade IoT platform built with Java 8, Spring Boot 2.7.x, WebFlux, Netty, Vert.x, and Reactor. It provides out-of-the-box device access, rule engine, data storage, and visualization for IoT applications.

**Key Documentation:**
- [Product Documentation](https://hanta.yuque.com/px7kg1/yfac2l)
- [Quick Start](https://hanta.yuque.com/px7kg1/yfac2l/raspyc4p1asfuxks)
- [Development Documentation](https://hanta.yuque.com/px7kg1/nn1gdr)

## Common Commands

### Build and Run

```bash
# Build the entire project
./mvnw clean install

# Build without running tests
./mvnw clean install -Dmaven.test.skip=true

# Run single test
./mvnw test -Dtest=ClassName

# Run tests with coverage
./mvnw test

# Build production JAR
./mvnw clean install -Pbuild
cd jetlinks-standalone && java -jar target/jetlinks-standalone.jar
```

### Development Environment

**Option 1: Using Docker Compose (Recommended for quick start)**
```bash
# Start full stack (PostgreSQL, Redis, Elasticsearch, JetLinks, UI)
cd docker/run-all
docker-compose up -d

# Access the platform at http://localhost:9000
```

**Option 2: Dev Environment (Infrastructure only)**
```bash
# Start only infrastructure services
cd docker/dev-env
docker-compose up -d

# Then run JetLinks locally
cd jetlinks-standalone
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev
```

**Option 3: Embedded Mode (Self-contained, for testing)**
```bash
# Uses embedded H2 database and embedded Elasticsearch
cd jetlinks-standalone
./mvnw spring-boot:run -Dspring-boot.run.profiles=embedded
# Access at http://localhost:8848
```

### Docker Operations

```bash
# Build Docker image
cd jetlinks-standalone
docker build -t jetlinks-community .

# Or use the convenience script
./build-and-push-docker.sh

# Run with docker-compose (from project root)
docker-compose -f docker/run-all/docker-compose.yml up -d
```

## Architecture

### High-Level Structure

```
jetlinks-community/
├── jetlinks-components/        # Shared components and modules
│   ├── common-component/       # Core utilities, configs, auth
│   ├── network-component/      # MQTT, TCP, HTTP, UDP protocols
│   ├── gateway-component/      # Device gateway services
│   ├── protocol-component/     # Device protocol support
│   ├── rule-engine-component/  # Rule engine for automation
│   ├── timeseries-component/   # Time-series data handling
│   ├── elasticsearch-component/# Elasticsearch integration
│   ├── notify-component/       # Notifications (SMS, email, etc.)
│   └── ...
├── jetlinks-manager/           # Business logic modules
│   ├── authentication-manager/ # User & permission management
│   ├── device-manager/         # Device management
│   ├── rule-engine-manager/    # Rule engine management
│   └── ...
├── jetlinks-standalone/        # Main application entry point
│   └── JetLinksApplication.java
└── simulator/                  # Device simulator for testing
```

### Key Components

**1. Device Access Layer**
- **Network Component** (`jetlinks-components/network-component/`): Handles multiple protocols (MQTT, TCP, HTTP, CoAP, UDP)
- **Gateway Component** (`jetlinks-components/gateway-component/`): Message gateway and device routing
- **Protocol Component** (`jetlinks-components/protocol-component/`): Pluggable protocol support via SPI

**2. Business Logic Layer**
- **Device Manager** (`jetlinks-manager/device-manager/`): Device lifecycle management
- **Authentication Manager** (`jetlinks-manager/authentication-manager/`): RBAC and data permissions
- **Rule Engine** (`jetlinks-components/rule-engine-component/`): Event processing and automation
- **Things Component** (`jetlinks-components/things-component/`): Device model management

**3. Data Layer**
- **PostgreSQL**: Primary business data storage (via R2DBC)
- **Elasticsearch**: Time-series data, logs, and full-text search
- **Redis**: Caching and session management
- **TDengine** (optional): Time-series database

### Technology Stack

- **Web Framework**: Spring Boot 2.7.18 with WebFlux (reactive)
- **Database**: PostgreSQL 11+ with R2DBC (reactive relational driver)
- **Search**: Elasticsearch 7.x
- **Cache**: Redis
- **Reactive Programming**: Project Reactor
- **Network**: Netty 4.1.x, Vert.x 4.x
- **Build**: Maven (Java 8 compatible)
- **ORM**: hsweb-easy-orm with reactive support

### Main Application Entry

`jetlinks-standalone/src/main/java/org/jetlinks/community/standalone/JetLinksApplication.java:32`
- Uses `@SpringBootApplication` with component scanning
- Enables reactive features: `@EnableEasyormRepository`, `@EnableAopAuthorize`
- Excludes traditional JDBC (`DataSourceAutoConfiguration`)
- Enables CORS and access logging

### Configuration Files

**Production Configuration:**
- `jetlinks-standalone/src/main/resources/application.yml:1`
  - PostgreSQL + external Elasticsearch + Redis
  - Port: 8848
  - Profile: `dev`

**Embedded Development Configuration:**
- `jetlinks-standalone/src/main/resources/application-embedded.yml:1`
  - H2 database + embedded Elasticsearch
  - Port: 8848 (same)
  - Auto-configured for development

### Protocol Support

The platform supports multiple device protocols through the network component:
- **MQTT** (`network-component/mqtt-component/`)
- **TCP** (`network-component/tcp-component/`)
- **HTTP** (`network-component/http-component/`)
- **CoAP** and **UDP** (via Vert.x)

### CI/CD

- **Build System**: GitHub Actions (`.github/workflows/maven.yml:1`)
- **Build Command**: `./mvnw clean install -Dmaven.test.skip=true -Pbuild`
- **Docker Registry**: Aliyun ACR (`registry.cn-shenzhen.aliyuncs.com/jetlinks/jetlinks-community`)
- **Triggers**: Push to `master`, `2.0`, `2.1`, `2.2` branches

### Testing

- **Test Framework**: JUnit 5 (Jupiter)
- **Reactive Testing**: reactor-test
- **Testcontainers**: 1.17.4 (for integration tests)
- **Coverage**: JaCoCo 0.8.7 (configured in pom.xml)

Test files follow naming patterns: `*Test.java`, `*Tests.java`, `*TestCase.java`