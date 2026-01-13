# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a comprehensive Spring Boot tutorial repository containing 72+ lab modules demonstrating various Spring Boot and Spring Cloud features. Each lab is a self-contained Spring Boot application with multiple sub-modules showcasing different aspects of a technology.

**Important**: Most modules are commented out in the parent `pom.xml`. To activate a module for development, uncomment its `<module>` entry in `/home/ubuntu/deploy-projects/b0c750ccb1be265c53274f1e/pom.xml:11-116`.

## Common Development Commands

All commands assume Maven is available. Most labs use Spring Boot 2.x.

### Building and Running

```bash
# Build a specific lab module
cd lab-<number>-<name>
mvn clean compile

# Run a Spring Boot application
mvn spring-boot:run

# Package as JAR
mvn clean package

# Build without running tests (useful for quick builds)
mvn clean compile -DskipTests
```

### Testing

```bash
# Run all tests in a module
cd lab-<number>-<name>
mvn test

# Run a specific test class
mvn test -Dtest=UserControllerTest

# Run tests with verbose output
mvn test -X

# Run tests for a specific module from parent
mvn test -pl lab-<number>-<name>
```

The repository has 300+ test cases across various labs, primarily using JUnit 5 with `@Test` annotations. Test files are located in `src/test/java/`.

### Maven Options

```bash
# Clean build
mvn clean

# Skip tests during build
mvn clean install -DskipTests

# Build specific module
mvn clean install -pl lab-72-minio

# Build with all sub-modules
mvn clean install -am -pl lab-72-minio

# Run with specific profile
mvn spring-boot:run -Dspring-boot.run.profiles=dev
```

## Project Structure

### Root Directory Structure

```
/home/ubuntu/deploy-projects/b0c750ccb1be265c53274f1e/
├── pom.xml                          # Parent POM (all modules listed, mostly commented out)
├── README.md                        # Comprehensive tutorial index
├── lab-01-spring-security/          # Spring Security examples
├── lab-02-spring-security-oauth/    # OAuth 2.0 examples
├── lab-03-kafka/                    # Kafka integration
├── lab-04-rabbitmq/                 # RabbitMQ integration
├── lab-07/                          # Gateway benchmarks (Spring Cloud Gateway, Zuul)
├── lab-11-spring-data-redis/        # Redis examples (Jedis, Redisson)
├── lab-12-mybatis/                  # MyBatis integration
├── lab-13-spring-data-jpa/          # JPA examples
├── lab-15-spring-data-es/           # Elasticsearch integration
├── lab-16-spring-data-mongo/        # MongoDB integration
├── lab-21/                          # Caching examples (Ehcache, Redis, Caffeine)
├── lab-22/                          # Validation examples
├── lab-23/                          # SpringMVC examples
├── lab-24/                          # Swagger/OpenAPI documentation
├── lab-27/                          # WebFlux examples
├── lab-28/                          # Scheduled tasks (Quartz)
├── lab-29/                          # Async tasks
├── lab-31/                          # RocketMQ integration
├── lab-32/                          # ActiveMQ integration
├── lab-42/                          # Unit testing examples
├── lab-47/                          # Spring Boot Auto-configuration
├── lab-48-hot-swap/                 # Hot deployment
├── lab-49/                          # Lombok integration
├── lab-55/                          # MapStruct object mapping
├── lab-64/                          # gRPC integration
├── lab-68-spring-security-oauth/    # OAuth 2.0 detailed examples
├── lab-72-minio/                    # MinIO object storage (currently active)
├── labx-01...labx-30/               # Spring Cloud modules (Nacos, Ribbon, Feign, etc.)
└── httpRequests/                    # HTTP client request examples
```

### Typical Lab Module Structure

Each lab follows standard Spring Boot structure:

```
lab-<number>-<name>/
├── pom.xml                          # Spring Boot dependencies
└── src/
    ├── main/
    │   ├── java/
    │   │   └── cn/iocoder/springboot/lab<number>/
    │   │       ├── Application.java      # @SpringBootApplication
    │   │       ├── controller/           # REST controllers
    │   │       ├── service/              # Business logic
    │   │       ├── repository/           # Data access
    │   │       ├── config/               # Configuration classes
    │   │       └── dataobject/           # Entity/DO classes
    │   └── resources/
    │       ├── application.yml           # Configuration
    │       └── static/                   # Static resources
    └── test/
        └── java/
            └── .../                      # Test classes with @Test methods
```

## Active Module

**lab-72-minio** is the only uncommented module in the parent POM, demonstrating MinIO object storage integration. It contains:
- MinIO client configuration
- REST controller for file upload/download operations
- Standard Spring Boot 2.6.4 setup

## Technology Stack

The repository covers:

**Spring Boot Features**:
- Web MVC, WebFlux, WebSocket
- Data Access (JPA, MyBatis, JDBC Template, Redis, MongoDB, Elasticsearch)
- Security (Spring Security, OAuth 2.0, Shiro)
- Messaging (Kafka, RabbitMQ, RocketMQ, ActiveMQ)
- Caching, Validation, Scheduled Tasks
- Testing (JUnit, TestContainers)
- Configuration Management
- Observability (Actuator, Prometheus, Grafana, SkyWalking)

**Spring Cloud**:
- Service Discovery (Nacos, Eureka, Consul)
- Load Balancing (Ribbon)
- Service Calls (Feign, Dubbo, gRPC)
- API Gateway (Spring Cloud Gateway, Zuul)
- Configuration (Config Server, Nacos, Apollo)
- Circuit Breakers (Sentinel, Hystrix, Resilience4j)
- Distributed Transactions (Seata)
- Messaging (Stream, Bus)

## Key Patterns

1. **Each lab demonstrates one specific feature** - don't expect complex multi-module applications
2. **Lab READMEs contain tutorial links** - check the `.md` file in each lab directory for the corresponding article
3. **Multiple examples per lab** - many labs have subdirectories like `lab-springmvc-23-01`, `lab-springmvc-23-02` showing different approaches
4. **Test-first approach** - most functionality has corresponding test cases in `src/test/java`
5. **Configuration via application.yml** - standard Spring Boot configuration files in `src/main/resources`

## Development Workflow

1. **Activate modules** by uncommenting in parent `pom.xml`
2. **Run specific lab**: `cd lab-<number> && mvn spring-boot:run`
3. **Check tests**: `mvn test` to verify functionality
4. **Read tutorial**: Each lab directory has a `.md` file linking to the full article
5. **Test endpoints**: Use `httpRequests/` directory or tools like `curl`/`Postman`

## Important Notes

- Most modules use Spring Boot 2.1.x - 2.6.x range
- Some modules require external services (databases, message queues, etc.)
- The parent POM lists all modules but most are commented out
- Each lab is independent - changing one doesn't affect others
- Test dependencies are provided via `spring-boot-starter-test`