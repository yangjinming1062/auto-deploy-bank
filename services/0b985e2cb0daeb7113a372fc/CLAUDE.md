# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **multi-module Maven repository** containing 230+ Java learning study projects. Each module (`study-*`) demonstrates a specific Java technology, framework, or concept. The project is for educational purposes - studying various Java technologies across the industry.

## Build Commands

```bash
# Build all modules
mvn clean install

# Build a specific module (from root)
mvn clean install -pl study-spring-boot

# Run a single module
mvn clean install -pl study-spring-boot -am

# Skip tests
mvn clean install -DskipTests

# Run tests for a specific module
mvn test -pl study-spring-boot

# Compile only (no tests)
mvn compile -pl study-spring-boot
```

**Note**: The parent `pom.xml` targets Java 1.8 but runs on Java 17 in this environment.

## Repository Structure

- **Root pom.xml**: Parent POM defining all 230+ modules with version management
- **study-***: Individual learning modules (Spring Boot, Redis, Docker, AI, etc.)
- **bage-***: Custom Spring Boot starters and libraries
- **study-vue-npm**: Frontend Vue.js modules (separate npm projects)

### Module Pattern

Most modules follow this structure:
```
{module-name}/
├── pom.xml                          # Module POM with parent reference
└── src/
    ├── main/
    │   ├── java/com/bage/study/     # Source code (package per feature)
    │   │   └── {category}/
    │   │       └── Application.java # Spring Boot main class
    │   └── resources/
    │       ├── application.properties
    │       ├── META-INF/
    │       ├── templates/           # Thymeleaf templates
    │       └── static/              # Static assets
    └── test/
        └── java/com/bage/study/     # Unit tests
```

### Java Package Convention

Source packages follow: `com.bage.study.{technology-name}` (e.g., `com.bage.study.springboot.restresponse`)

## Key Technologies

- **Framework**: Spring Boot (2.x and 3.x), Spring Cloud, Spring MVC
- **Database**: MySQL, H2, MongoDB, Redis, Oracle, ClickHouse, TiDB, Oceanbase
- **Messaging**: RabbitMQ, ActiveMQ, Pulsar, Kafka
- **Security**: Shiro, Spring Security, OAuth2, JWT, CAS
- **Cache**: Redis, Ehcache, Caffeine
- **Testing**: JUnit, Mockito, JMockit
- **Build**: Maven plugins, Docker, Kubernetes
- **Observability**: Arthas, SkyWalking, Zipkin, ELK, Loki
- **AI/ML**: Deep learning modules, LLM integrations
- **Frontend**: Vue.js, Flutter (some modules)

## Common Module Types

1. **Spring Boot Web Apps**: Main class annotated with `@SpringBootApplication`, `@RestController`
2. **Maven Plugins**: Custom plugins in `study-maven-plugin`
3. **Libraries**: Shared utilities in `study-utils`, `study-domain-generator`
4. **Starters**: Custom Spring Boot starters in `bage-spring-boot-starter-*`