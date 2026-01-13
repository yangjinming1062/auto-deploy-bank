# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository is a collection of **Spring Boot demo projects** demonstrating various Java backend technologies. It also contains extensive learning documentation (in Chinese) covering Java, Spring Boot, and microservices patterns. The repository is structured as a tutorial/reference guide with practical working examples.

**Primary Language:** Java (8) with Spring Boot framework

## Repository Structure

```
/home/ubuntu/deploy-projects/6d3d50ae80c2a9b70050d132/
├── README.md              # Main documentation with learning resources
├── docs/                  # Extensive documentation (Java basics, concurrency, JVM, etc.)
├── springboot-jasypt/     # Jasypt encryption demo
├── springboot-minio/      # MinIO object storage demo
├── websocket/             # WebSocket demo (multi-module)
│   ├── sample-websocket/
│   ├── stomp-websocket/
│   └── mq-websocket/      # WebSocket + Redis + MyBatis
└── xxl-job-demo/          # XXL-Job distributed task scheduling
```

## Spring Boot Projects

### 1. springboot-jasypt
Demonstrates **Jasypt encryption** for securing sensitive configuration data (database passwords, connection strings, etc.).

**Key Technologies:**
- Spring Boot 2.1.7
- MySQL 8.0.15
- Druid connection pool
- Jasypt encryption
- Spring AOP
- Log4j2
- Lombok

**Configuration:** Uses Jasypt for encrypting sensitive properties in `application.yml` with `PASS(encrypted_value)` format

### 2. springboot-minio
Demonstrates **MinIO object storage** integration.

**Key Technologies:**
- Spring Boot 2.5.2
- MinIO Java client 8.2.1
- Apache Commons Lang3
- HuTool utilities
- JAXB (XML binding)

**Key Files:**
- `/src/main/java/com/java/family/minio/config/MinioProperties.java` - MinIO configuration properties
- `/src/main/java/com/java/family/minio/utils/MinioUtil.java` - MinIO utility class
- `/src/main/java/com/java/family/minio/controller/MinioController.java` - REST endpoints

### 3. websocket (Multi-module project)
Demonstrates **WebSocket messaging** patterns, including STOMP protocol support.

**Key Technologies:**
- Spring Boot 2.0.5
- STOMP over WebSocket
- Redis
- MyBatis
- Swagger 2.9.2
- Thymeleaf
- Log4j2

**Module: mq-websocket**
WebSocket with message queue integration for multi-user chat scenarios.

**Configuration:**
- WebSocket endpoints: `/chat-websocket` with SockJS fallback
- Message broker prefixes:
  - Client destinations: `/message/xxx`
  - Broadcast messages: `/topic/yyy`
  - User messages: `/user/xxx`

### 4. xxl-job-demo
Demonstrates **XXL-Job distributed task scheduling**.

**Key Technologies:**
- Spring Boot 2.2.6
- XXL-Job 2.2.0
- Custom task executors

## Common Development Tasks

### Prerequisites
- **Java:** Version 8 (projects configured for Java 8, though Java 17 is available in environment)
- **Maven:** Version 3.8.7 available at `/usr/bin/mvn`
- **Database:** MySQL required for jasypt and websocket projects

### Building Projects

**Build a single project:**
```bash
cd <project-directory>
mvn clean package
```

**Build specific projects:**

```bash
# Jasypt demo
cd springboot-jasypt && mvn clean package

# MinIO demo
cd springboot-minio && mvn clean package

# WebSocket demo
cd websocket && mvn clean package

# XXL-Job demo
cd xxl-job-demo && mvn clean package
```

### Running Applications

**Run with Maven:**
```bash
# For Maven parent projects (websocket)
mvn spring-boot:run

# For single module projects
cd <project-directory> && mvn spring-boot:run
```

**Run JAR file:**
```bash
java -jar target/<artifact-name>-0.0.1-SNAPSHOT.jar
```

### Testing

**Run all tests:**
```bash
mvn test
```

**Run tests for specific project:**
```bash
cd <project-directory> && mvn test
```

**Skip tests during build:**
```bash
mvn clean package -DskipTests
```

### Key Ports by Project

| Project | Port | Description |
|---------|------|-------------|
| springboot-jasypt | 8080 (default) | Jasypt encryption demo |
| springboot-minio | 8085 | MinIO storage demo |
| websocket/mq-websocket | Varies | STOMP WebSocket server |
| xxl-job-demo | 8080 (default) | XXL-Job executor |

## Code Architecture

All projects follow **standard Spring Boot layered architecture**:

```
src/main/java/{base-package}/
├── Application.java          # @SpringBootApplication main class
├── config/                   # Configuration classes (@Configuration)
├── controller/               # REST controllers (@RestController)
├── service/                  # Business logic (@Service)
├── model/ or entity/         # Data models
├── repository/               # Data access (@Repository)
├── utils/                    # Utility classes
└── annotation/               # Custom annotations
```

### Configuration Files

**Per-project locations:**
- `<project>/src/main/resources/application.yml` or `application.properties`

**Jasypt encryption:**
- Encrypted values use format: `PASS(encrypted_value)`
- Decryption key in `jasypt.encryptor.password`
- See `springboot-jasypt/src/main/resources/application.yml:11`

## Important Notes

1. **Chinese Documentation:** The `README.md` and `docs/` directory contain extensive documentation in Chinese about Java backend development, microservices, and distributed systems.

2. **No Tests:** Most demo projects do not include test files (spring-boot-starter-test dependency is present but no test implementations).

3. **Mixed Spring Boot Versions:** Projects use different Spring Boot versions (2.0.5 to 2.5.2), so dependencies and configurations may vary.

4. **Credentials in Config:** Some projects have hardcoded or encrypted credentials in configuration files.

5. **Multi-module Projects:** The `websocket` directory is a Maven multi-module project. Build/run from the parent directory or specific modules.

6. **Environment-Specific:** Each project may require specific infrastructure (MySQL, Redis, MinIO server, XXL-Job scheduler) for full functionality.

## Environment Requirements

**For springboot-jasypt:**
- MySQL server (configured in `application.yml`)
- Jasypt encryption key: `Y6M9fAJQdU7jNp5MW`

**For springboot-minio:**
- MinIO server at `http://192.168.47.148:9001`

**For websocket:**
- MySQL server
- Redis server

**For xxl-job-demo:**
- XXL-Job scheduler service (separate deployment)