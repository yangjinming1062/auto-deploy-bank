# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains example code for two editions of the book "Spring Cloud微服务" (Spring Cloud Microservices):

- **Spring-Cloud-Book-Code-1**: First edition with a monolithic structure containing ~20 microservices
- **Spring-Cloud-Book-Code-2**: Second edition organized by chapters (ch-2 through ch-21), with individual examples for each chapter

## Build System

All projects use **Maven** as the build tool. Each microservice is an independent Maven project with its own `pom.xml`.

### Common Commands

```bash
# Build a specific service (from the service directory)
mvn clean package

# Build without running tests
mvn clean package -DskipTests

# Run a single test
mcd <service-directory>
mvn test -Dtest=TestClassName

# Compile only
mvn compile

# Skip compilation and run tests
mvn test -DfailIfNoTests=false
```

## Architecture

### Microservices Pattern (First Edition)

The first edition implements a complete microservices architecture with the following components:

- **Service Discovery**: Eureka (`fangjia-eureka`)
- **API Gateway**: Zuul (`fangjia-fsh-api`)
- **Service-to-Service Communication**: Feign clients (`fangjia-api-client`)
- **Monitoring**: Spring Boot Admin (`fangjia-boot-admin`)
- **Circuit Breaker**: Hystrix (`fangjia-hystrix-dashboard`)
- **Distributed Tracing**: Zipkin (`fangjia-zipkin`)
- **Task Scheduling**: `fangjia-job`
- **Database Sharding**: Multiple sharding examples (`fangjia-sjdbc-*`)
- **Business Services**:
  - User Service (`fangjia-fsh-user-service`)
  - House Service (`fangjia-fsh-house-service`)
  - Substitution Service (`fangjia-fsh-substitution-service`)
  - Auth Service (`fangjia-auth-service`)

### Key Dependencies by Version

**First Edition (Spring-Cloud-Book-Code-1)**:
- Spring Boot: `1.5.4.RELEASE`
- Spring Cloud: `Dalston.SR4`
- Java: 1.8

**Second Edition (Spring-Cloud-Book-Code-2)**:
- Spring Boot: `2.0.6.RELEASE` (varies by chapter)
- Spring Cloud: `Finchley.SR2` (varies by chapter)
- Java: 1.8

## Project Structure

### Spring-Cloud-Book-Code-1

Each service follows the standard Maven directory structure:
```
fangjia-<service-name>/
├── pom.xml
└── src/
    └── main/
        ├── java/
        │   └── com/fangjia/
        │       └── <service-package>/
        └── resources/
            └── application.properties (or application.yml)
```

Common packages include:
- `com.fangjia.common`: Shared utilities and base classes
- `com.fangjia.eureka`: Eureka server implementation
- `com.fangjia.api`: API gateway components
- Individual service packages for each microservice

### Spring-Cloud-Book-Code-2

Organized by chapter with multiple examples per chapter:
```
ch-<number>/
├── <example-name>/
│   ├── pom.xml
│   └── src/
│       ├── main/
│       │   ├── java/
│       │   │   └── com/cxytiandi/
│       │   └── resources/
│       └── test/ (occasionally present)
```

## Development Workflow

### Starting a Service

Each service is a Spring Boot application with a main class annotated with `@SpringBootApplication`:

```bash
# Navigate to service directory
cd Spring-Cloud-Book-Code-1/fangjia-<service-name>

# Build and run
mvn clean package
java -jar target/<artifact-id>-1.0.jar
```

Or run directly with Maven:
```bash
mvn spring-boot:run
```

### Service Dependencies

Services communicate via:
- **Eureka**: Service discovery and registration
- **Feign**: Declarative REST client for inter-service calls
- **Ribbon**: Client-side load balancing

### Configuration

Services use Spring Boot's `application.properties` or `application.yml` for configuration. See individual service README files for specific configuration requirements.

## Important Notes

1. **Import Strategy**: Import services one at a time into your IDE, not all at once, to avoid dependency conflicts
2. **Chapter Examples**: The second edition is organized by chapters - import examples from specific chapters based on your learning needs
3. **External Dependencies**: Some services require external dependencies (Redis, databases, etc.) - check the blog post at http://cxytiandi.com/blog/detail/20517 for setup instructions
4. **No Tests**: Most services don't include automated tests - manual testing is expected

## Additional Resources

- **Author Blog**: http://cxytiandi.com/blogs/yinjihuan
- **Book Articles**: See README.md for a comprehensive list of corresponding articles
- **QQ Group**: 626640827 (Spring Cloud technical exchange)
- **WeChat**: jihuan900 (for joining WeChat group)

## Common Service Types

- **Eureka Server**: Service registry and discovery
- **Gateway**: API gateway using Zuul or Spring Cloud Gateway
- **Business Services**: Domain-specific microservices (user, house, etc.)
- **Utility Services**: Authentication, common libraries
- **Monitoring**: Admin dashboard, Hystrix dashboard, Zipkin tracing