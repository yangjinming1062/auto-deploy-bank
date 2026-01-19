# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**spring-boot-quick** is a comprehensive collection of 80+ Spring Boot example modules demonstrating enterprise Java integrations. Created by developer "vector4wang", it serves as a practical reference library for Spring Boot patterns and integrations.

**Status**: As of March 7, 2025, the project is no longer actively maintained (author transitioned to Go development).

## Common Commands

### Build & Install
```bash
# Build all modules
mvn clean install

# Build specific module (replace module-name)
mvn clean install -pl quick-jwt

# Build with dependency updates
mvn clean install -U

# Package without running tests
mvn clean package -DskipTests
```

### Testing
```bash
# Run all tests
mvn test

# Run tests for specific module
mvn test -pl quick-jwt

# Run single test class (from module directory)
mvn test -Dtest=UserControllerTest
```

**Note**: Tests are skipped by default in the parent `quick-platform/pom.xml`. Override with `-DskipTests=false` if needed.

## Project Structure

### Maven Multi-Module Architecture

The project uses a **multi-module Maven structure** with two parent POMs:
- **Root POM** (`/pom.xml`): Aggregates all 80+ modules
- **Platform POM** (`quick-platform/pom.xml`): Centralized dependency management (478 lines)

### Module Categories

The modules are organized by functionality:

**Core & Framework:**
- `quick-platform` - Dependency management parent
- `quick-modules` - Modular development example
- `quick-starter` - Custom starter template
- `quick-framework` - Framework utilities

**Web & API:**
- `quick-swagger` - API documentation (Swagger 2)
- `quick-rest-template` - REST client examples
- `quick-feign` - Feign client for microservices
- `quick-graphql` - GraphQL integration

**Database & Persistence:**
- `quick-jdbc` - JDBC template examples
- `quick-jpa` - JPA/Hibernate integration
- `quick-mybatis-druid` - MyBatis + Druid monitoring
- `quick-multi-data` - Multi-datasource configuration
- `quick-sharding-jdbc` - Database sharding

**Security:**
- `quick-shiro` - Apache Shiro authentication
- `quick-spring-shiro` - Spring Shiro integration
- `quick-shiro-cas` - Shiro + CAS SSO
- `quick-oauth2` - OAuth 2.0 implementation
- `quick-jwt` - JWT authentication
- `quick-hmac` - HMAC authentication

**Messaging:**
- `quick-rabbitmq` - RabbitMQ integration
- `quick-activemq` / `quick-activemq2` - ActiveMQ integration
- `quick-kafka` - Apache Kafka integration
- `quick-rocketmq` - Alibaba RocketMQ
- `quick-multi-rabbitmq` - Multi-broker RabbitMQ

**Microservices & Cloud:**
- `quick-dubbo` - Dubbo service framework
- `quick-dubbo-nacos` - Dubbo + Nacos registry
- `quick-feign` - Feign client
- `quick-config-server` - Spring Cloud Config Server
- `quick-nacos-common-config` - Nacos configuration

**Data Stores:**
- `quick-redis` - Redis integration
- `quick-mongodb` - MongoDB integration
- `quick-hbase` - HBase integration
- `quick-oss` - Object storage service

**Other Technologies:**
- `quick-cache` - Caching strategies
- `quick-mail` - Email sending
- `quick-log` - Log4j2 logging
- `quick-logback` - Logback logging
- `quick-batch` - Spring Batch processing
- `quick-async` - Async processing
- `quick-sse` - Server-Sent Events
- `quick-undertow` - Undertow embedded server
- `quick-i18n` - Internationalization

**Deployment & Packaging:**
- `quick-package-assembly` - Maven assembly with startup scripts
- `quick-package-assembly-multi-env` - Multi-environment deployment
- `quick-container` - Docker & K3s Kubernetes examples
- `quick-vue` - Vue.js frontend integration

### Standard Module Structure

Each module follows Spring Boot conventions:
```
src/
├── main/
│   ├── java/com/quick/{module}/
│   │   ├── {ModuleName}Application.java  # @SpringBootApplication entry point
│   │   ├── controller/                   # REST endpoints
│   │   ├── service/                      # Business logic
│   │   ├── entity/                       # Data models
│   │   └── config/                       # Configuration classes
│   └── resources/
│       └── application.yml               # or .properties
└── test/
    ├── java/
    └── resources/
        └── application.yml
```

## Key Configuration Files

### Dependency Management (`quick-platform/pom.xml`)
**Spring Boot 2.3.4.RELEASE**
- Manages all dependency versions centrally
- Spring Cloud Alibaba 2.2.5.RELEASE
- Database: MyBatis 3.5.6, Druid 1.1.10, MySQL 8.0.28
- Security: Apache Shiro 1.9.1, JWT support
- Messaging: RabbitMQ, Kafka, ActiveMQ, RocketMQ
- Microservices: Dubbo 2.7.11, Feign 8.18.0, Nacos

### Application Configuration
Each module has configuration in `src/main/resources/`:
- `application.yml` - YAML format (most modules)
- `application.properties` - Properties format (some older modules)

Example database config:
```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3308/testdb
    username: root
    password: 123456
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
```

### Module Documentation
- **Root README.md** (329 lines) - Comprehensive overview and module descriptions
- **Individual READMEs** - 29 module-specific README files with API docs and usage examples

## Development Notes

### Testing
- Framework: JUnit with spring-boot-starter-test
- Tests are **skipped by default** globally
- Override per-module: `mvn test -DskipTests=false`

### Version Recommendations
The README advises against using the latest versions. It recommends **(latest-1|2) versions for stability**.

### Entry Points
Main application classes use `@SpringBootApplication` annotation:
```java
@SpringBootApplication(scanBasePackages = {"com.app"})
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### Deployment Scripts
Some modules include shell scripts:
- `quick-package-assembly/src/main/bin/start.sh` - JAR launcher
- `quick-package-assembly/src/main/bin/stop.sh` - Process termination

### Health Check Endpoints
Most web modules expose Spring Boot Actuator endpoints:
- `/health` - Application health (no auth required)
- `/metrics` - Application metrics (requires auth)
- `/autoconfig` - Auto-configuration report
- `/beans` - All Spring beans
- Full list in `quick-mybatis-druid/README.md:125-138`

## Notable Integration Patterns

### Multi-Datasource (`quick-multi-data`)
- Uses Druid for connection pooling and monitoring
- Separate datasource configurations for different databases

### API Documentation (`quick-swagger`)
- Swagger 2 integration
- For `@RequestBody` with date parameters, use `@JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")` in model fields
- See module README for details

### Custom Starter (`quick-starter`)
- Template for creating Spring Boot starters
- Includes auto-configuration and properties support

### Exception Handling (`quick-exception`)
- Global exception handling for 404, 400, 500 errors
- Returns JSON responses

### JSP Integration (`quick-jsp`)
- Spring Boot with JSP support (non-standard)
- Requires specific Maven WAR plugin configuration
- See `README.md:218-260` for setup details

## CI/CD

- `.travis.yml` - Travis CI configuration
- `.github/workflows/github2gitee.yml` - GitHub to Gitee mirroring (disabled)

## Important URLs

- Author's Blog: http://blog.wangxc.club
- CSDN: http://blog.csdn.net/qqhjqs
- Related Project (Elasticsearch): https://github.com/vector4wang/quick-elasticsearch
- Crawlers: https://github.com/vector4wang/Crawlers

## Contact

For issues with this codebase, the author can be contacted at: **vector4wang@qq.com**