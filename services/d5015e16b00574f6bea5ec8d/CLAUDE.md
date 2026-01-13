# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a **comprehensive Spring Boot and Spring Cloud learning repository** with 50,000+ lines of example code across 72+ Spring Boot labs (lab-01 to lab-72) and 30+ Spring Cloud labs (labx-01 to labx-30). Each lab demonstrates real-world usage of specific technologies in the Java Spring ecosystem.

**Key Characteristics:**
- Educational resource created by YunaiV (芋道) for Spring Boot learning
- Multi-module Maven project with individual Spring Boot applications per lab
- All modules currently commented out in root pom.xml (see README.md line 1-3 for guidance)
- Examples cover the entire Spring Boot and Spring Cloud ecosystem

## Repository Structure

```
/home/ubuntu/deploy-projects/d5015e16b00574f6bea5ec8d/
├── pom.xml                          # Parent POM (modules commented out)
├── README.md                        # Comprehensive documentation (410+ lines)
├── lab-01-spring-security/          # Spring Security examples
├── lab-03-kafka/                    # Kafka messaging examples
├── lab-11-spring-data-redis/        # Redis caching examples
├── lab-12-mybatis/                  # MyBatis data access
├── lab-23/                          # SpringMVC REST APIs
├── lab-30/                          # Dubbo RPC examples
├── lab-52/                          # Seata distributed transactions
├── lab-58/                          # Feign declarative calls
├── lab-64/                          # gRPC examples
├── lab-67/                          # Netty examples
├── labx-01-spring-cloud-alibaba-nacos-discovery/  # Nacos service discovery
├── labx-08-spring-cloud-gateway/    # Spring Cloud Gateway
└── ... (70+ more labs)
```

**Naming Convention:**
- `lab-XX-name/` - Spring Boot specific labs
- `labx-XX-name/` - Spring Cloud ecosystem labs

## Build System & Commands

### Maven Build

**Package Manager:** Maven 3.6+

**Root Build Configuration:**
```xml
GroupId: cn.iocoder.springboot.labs
ArtifactId: labs-parent
Packaging: pom
Version: 1.0-SNAPSHOT
Parent: Spring Boot Starter Parent (varies by lab)
```

**Common Commands:**

```bash
# Build a specific lab module
mvn clean install -pl lab-03-kafka/lab-03-kafka-demo

# Build with tests
mvn clean test

# Run a specific lab
mvn spring-boot:run -Dspring-boot.run.profiles=prod
mvn spring-boot:run -pl lab-03-kafka/lab-03-kafka-demo

# Run tests only
mvn test -pl lab-03-kafka/lab-03-kafka-demo

# Skip tests during build
mvn clean install -DskipTests

# Clean build
mvn clean
```

**Important:** All modules are commented out in root pom.xml. Uncomment modules as needed before building.

### Testing Framework

- **Framework:** JUnit 4/5 + Spring Boot Test
- **Location:** `src/test/java/` per module
- **Patterns:** `@SpringBootTest`, Mock MVC, embedded databases (H2)

```bash
# Run all tests in a module
mvn test -pl lab-42

# Run single test class
mvn test -Dtest=UserServiceTest -pl lab-12-mybatis
```

### Production Deployment

Some labs include deployment automation scripts:

```bash
# Deploy using provided script
cd lab-41 && ./deploy.sh
cd labx-16 && ./deploy.sh

# These scripts include: backup, stop, transfer, start, health check
```

## Code Architecture

### Typical Lab Structure

Each lab follows Spring Boot standard structure:

```
lab-XX/
├── pom.xml
├── sub-module/
│   ├── pom.xml
│   └── src/
│       ├── main/
│       │   ├── java/cn/iocoder/springboot/labXX/
│       │   │   ├── Application.java          # @SpringBootApplication main class
│       │   │   ├── config/                   # @Configuration classes
│       │   │   ├── controller/               # @RestController endpoints
│       │   │   ├── service/                  # @Service business logic
│       │   │   ├── repository/               # Data access layer
│       │   │   └── message/                  # Message models/consumers
│       │   └── resources/
│       │       └── application.yaml          # Spring Boot configuration
│       └── test/
│           └── java/...                      # JUnit tests
└── 《芋道 XXX 入门》.md                        # Chinese documentation
```

### Main Entry Points

Each module contains a main class following this pattern:

```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### Configuration Management

**Configuration Files:**
- `application.yaml` / `application.properties` - Spring Boot configuration
- Environment profiles (dev, test, prod)
- Technology-specific configs (Kafka, Redis, MySQL, etc.)

**Example Configuration** (Kafka from lab-03):
```yaml
spring:
  kafka:
    bootstrap-servers: 127.0.0.1:9092
    producer:
      acks: 1
      retries: 3
    consumer:
      auto-offset-reset: earliest
```

## Technology Coverage

### Spring Boot Labs (lab-01 to lab-72)

**Core Technologies:**
- **Security:** Spring Security, Shiro, OAuth2 (labs 01, 02, 33, 68)
- **Data Access:** MyBatis, JPA, JdbcTemplate, Redis, MongoDB, Elasticsearch (labs 11-21)
- **Web Development:** SpringMVC, WebFlux, Validation, WebSocket (labs 22-27)
- **RPC:** Dubbo, Feign, gRPC, SOFARPC, Motan, Netty (labs 30, 58, 62-67)
- **Message Queues:** Kafka, RabbitMQ, RocketMQ, ActiveMQ (labs 03-04, 31-32)
- **Transactions:** Seata distributed transactions (lab 52, 53)
- **Monitoring:** Actuator, Prometheus, Grafana, CAT, Sentry (labs 34-36, 51, 61)
- **Configuration:** Apollo, Nacos config management (labs 43-45)
- **File Storage:** MinIO object storage (lab 72)
- **Performance:** Tomcat/Jetty/Undertow benchmarks (labs 05-07)

### Spring Cloud Labs (labx-01 to labx-30)

**Core Components:**
- **Service Discovery:** Nacos, Eureka, Consul, Zookeeper (labx-01, 22, 25, 27)
- **Load Balancing:** Ribbon (labx-02)
- **API Gateway:** Spring Cloud Gateway, Zuul (labx-08, 21)
- **Service Communication:** Feign, gRPC (labx-03, 30)
- **Circuit Breakers:** Sentinel, Hystrix, Resilience4j (labx-04, 23)
- **Config Centers:** Nacos, Apollo, Spring Cloud Config (labx-05, 09, 12)
- **Event-Driven:** Spring Cloud Stream, Spring Cloud Bus (labx-06, 10-11, 18-20, 29)
- **Distributed Transactions:** Seata (labx-17)

## Development Workflows

### HTTP Client Testing

**IDEA HTTP Client Format** - Pre-recorded requests in `/httpRequests/`:
- 410+ saved HTTP requests in `http-requests-log.http`
- Located in `lab-71-http-debug/`
- Use IntelliJ IDEA HTTP Client to replay requests

### Infrastructure Dependencies

Many labs require **external services** running separately:
- Databases: MySQL, Redis, MongoDB, Elasticsearch
- Message Queues: Kafka, RabbitMQ, RocketMQ, ActiveMQ
- Service Discovery: Nacos, Eureka, Consul
- Monitoring: Prometheus, Grafana

**Setup Requirements:**
- Install and configure external services before running labs
- Check `application.yaml` for connection details
- Use Docker Compose when available for infrastructure

### Documentation

Each lab includes Chinese markdown documentation:
- Located in each lab directory
- Links to detailed tutorials at iocoder.cn
- Step-by-step learning guides

**Key Documentation Locations:**
- `/home/ubuntu/deploy-projects/d5015e16b00574f6bea5ec8d/README.md` - Master index with all 72+ labs
- Individual lab directories contain specific 《芋道 XXX 入门》.md files

## Important Notes

1. **Modules are commented out** in root pom.xml - Uncomment modules before building
2. **Multi-version support** - Different labs use different Spring Boot versions (1.5.x to 2.6.x)
3. **External dependencies required** - Infrastructure services must be running separately
4. **Modular architecture** - Each lab is completely independent
5. **Educational purpose** - Examples are designed for learning, not production
6. **Chinese documentation** - Primary documentation is in Chinese

## Quick Start

1. **Find the lab you need** using README.md as index
2. **Uncomment the module** in root pom.xml
3. **Setup infrastructure** (databases, message queues, etc.)
4. **Build and run:**
   ```bash
   mvn clean install -pl lab-XX
   mvn spring-boot:run -pl lab-XX
   ```
5. **Check documentation** in lab directory for detailed walkthrough