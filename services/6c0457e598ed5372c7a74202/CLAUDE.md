# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an **IoT (Internet of Things) Technical Guide** - a comprehensive multi-module Maven project containing 30+ standalone Spring Boot applications and tutorials covering various IoT technologies and patterns. Each `IOT-Guide-*` module demonstrates a specific IoT concept or technology.

## Project Structure

```
IOT-Technical-Guide/
├── pom.xml                           # Parent POM with dependency management
├── README.md                         # Main documentation (Chinese)
├── .travis.yml                       # Travis CI configuration
├── IOT-Guide-*/                      # 30+ Spring Boot modules
│   ├── IOT-Guide-MQTT/               # MQTT broker implementation
│   ├── IOT-Guide-Coap/               # CoAP protocol implementation
│   ├── IOT-Guide-HTTP/               # HTTP device management
│   ├── IOT-Guide-DB-MongoDB/         # MongoDB integration
│   ├── IOT-Guide-DB-PostgreSQL/      # PostgreSQL integration
│   ├── IOT-Guide-RealTime-Backend/   # WebSocket backend
│   ├── IOT-Guide-RealTime-Fontend/   # Angular 5 frontend
│   ├── IOT-Guide-JWT-*/              # JWT authentication examples
│   ├── IOT-Guide-OAuth2.0-*/         # OAuth2 implementation
│   ├── IOT-Guide-RuleEngine-*/       # Rule engine examples
│   ├── IOT-Guide-Gateway-*/          # Gateway implementations (Modbus, OPC-UA)
│   ├── IOT-Guide-Docker/             # Docker examples
│   ├── IOT-Guide-Kubernates/         # Kubernetes examples
│   └── ... (other IoT modules)
└── doc/                              # Additional documentation
```

## Common Development Commands

### Maven Commands (Java Modules)

```bash
# Build entire project
mvn clean verify

# Build without running tests
mvn clean verify -DskipTests=true

# Install all modules to local repository
mvn clean install

# Run tests for all modules
mvn test

# Skip Javadoc generation during build
mvn clean verify -Dmaven.javadoc.skip=true

# Build a specific module
cd IOT-Guide-MQTT && mvn clean install

# Run a specific Spring Boot module
cd IOT-Guide-MQTT && mvn spring-boot:run

# Run tests for a specific module
cd IOT-Guide-MQTT && mvn test
```

**Note:** Each module has its own `mainClass` configured in `spring-boot-maven-plugin`. For example, MQTT module's main class is `iot.technology.mqtt.MqttServerApp` (see `/home/ubuntu/deploy-projects/6c0457e598ed5372c7a74202/IOT-Guide-MQTT/pom.xml:80`).

### Angular Frontend Commands

```bash
cd IOT-Guide-RealTime-Fontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run unit tests
npm test

# Run linter
npm run lint

# Run e2e tests
npm run e2e
```

## Architecture & Technology Stack

### Core Technologies (Per Module)

- **Java 8** - Primary language
- **Spring Boot 2.0.5.RELEASE** - Application framework
- **Spring Framework 5.0.9.RELEASE** - Core Spring
- **Spring Data JPA** - Data access
- **Spring Security** - Authentication/authorization
- **Maven** - Build tool
- **JUnit 4.13.1** - Testing framework
- **Logback** - Logging

### IoT Protocols & Frameworks

- **MQTT** (`IOT-Guide-MQTT/`) - Message broker with Netty
- **CoAP** (`IOT-Guide-Coap/`) - California framework 2.6.3
- **HTTP/HTTPS** (`IOT-Guide-HTTP/`) - REST APIs
- **WebSocket** (`IOT-Guide-RealTime-*/`) - Real-time communication
- **gRPC/ProtoBuf** (`IOT-Guide-Grpc-Protobuf/`) - Service communication
- **LwM2M** (`IOT-Guide-Lwm2m/`) - Device management
- **BACnet** (`IOT-Guide-Bacnet/`) - Building automation
- **Modbus/OPC-UA** (`IOT-Guide-Gateway-*/`) - Industrial protocols

### Databases

- **MySQL 8.0.16** (`IOT-Guide-DB/`)
- **PostgreSQL** (`IOT-Guide-DB-PostgreSQL/`)
- **MongoDB** (`IOT-Guide-DB-MongoDB/`)
- **H2** (embedded testing)

### Message Queues & Streaming

- **Apache Kafka** - High-throughput messaging
- **RabbitMQ** - Message broker
- **Apache Flink 1.9.0** - Stream processing (`IOT-Guide-Flink/`)

### Security

- **JWT** (`IOT-Guide-JWT-*`) - Token-based auth
- **OAuth 2.0** (`IOT-Guide-OAuth2.0-*`) - Authorization framework
- **Bucket4j** (`IOT-Guide-RateLimiting/`) - Rate limiting

### DevOps

- **Docker** (`IOT-Guide-Docker/`) - Containerization
- **Kubernetes** (`IOT-Guide-Kubernates/`) - Orchestration
- **Travis CI** - Continuous integration (.travis.yml)

## Key Module Examples

### MQTT Broker (`IOT-Guide-MQTT/`)
- Custom MQTT v3.1/v3.1.1/v5.0 broker implementation
- Netty-based transport layer
- Queue-based message storage
- Main class: `iot.technology.mqtt.MqttServerApp`

### Rule Engine Examples
- `IOT-Guide-RuleEngine-EasyRules/` - Easy Rules framework
- `IOT-Guide-RuleEngine-ThingsBoard/` - ThingsBoard patterns
- `IOT-Guide-RuleEngine-Introduce/` - Introduction

### Authentication Examples
- `IOT-Guide-JWT-Without-JPA/` - JWT without database
- `IOT-Guide-JWT-JPA/` - JWT with JPA
- `IOT-Guide-JWT-Refresh/` - JWT refresh tokens
- `IOT-Guide-OAuth2.0-Authorization Server/` - Auth server
- `IOT-Guide-OAuth2.0-Resource/` - Resource server

### Real-time Applications
- `IOT-Guide-RealTime-Backend/` - Spring WebSocket backend
- `IOT-Guide-RealTime-Fontend/` - Angular 5 frontend with WebSocket

### Gateway Implementations
- `IOT-Guide-Gateway-Modbus/` - Modbus protocol gateway
- `IOT-Guide-Gateway-OPC(UA)/` - OPC-UA gateway
- `IOT-Guide-Gateway/` - Generic gateway patterns

## Build Configuration

The parent `pom.xml` (/) manages:
- **Dependency versions** for all modules (lines 89-123)
- **Common dependencies** like Lombok (lines 125-130)
- **Maven plugins** configuration (lines 397-436)

All modules extend this parent POM and define their specific dependencies and build configurations.

## Testing

Each module follows standard Maven project structure:
```
module/
├── src/
│   ├── main/java/    # Application code
│   ├── main/resources/
│   │   └── application.yml  # Spring Boot configuration
│   └── test/java/    # JUnit test cases
```

Run tests:
```bash
# All modules
mvn test

# Specific module
cd IOT-Guide-MQTT && mvn test
```

## Environment Requirements

- **Java 8** (OpenJDK 8 in Travis CI)
- **Maven 3.x**
- **Node.js & npm** (for Angular frontend)
- **MySQL/PostgreSQL/MongoDB** (depending on module requirements)

## CI/CD

- **Travis CI** configured in `.travis.yml`
- Builds with OpenJDK 8
- Runs: `mvn clean verify -DskipTests=true -Dmaven.javadoc.skip=true`

## Important Notes

1. **Each module is independent** - Can be built and run separately
2. **Chinese documentation** - README.md and docs are in Chinese
3. **Version alignment** - Modules use Spring Boot 2.0.5 and Spring 5.0.9
4. **Test database** - H2 is used for testing across modules
5. **Actor framework** - Custom actor implementation in `IOT-Guide-Actor/`

## Module Dependencies

Some modules depend on others (e.g., `IOT-Guide-MQTT` depends on `IOT-Guide-TSL` - see `/home/ubuntu/deploy-projects/6c0457e598ed5372c7a74202/IOT-Guide-MQTT/pom.xml:52-54`). The dependency chain is managed in the parent POM's `<dependencyManagement>` section (lines 132-395).

## Getting Started

1. Build the entire project: `mvn clean verify`
2. Choose a module based on your IoT technology interest
3. Navigate to the module directory
4. Run the module: `mvn spring-boot:run`
5. For frontend: `cd IOT-Guide-RealTime-Fontend && npm install && npm start`