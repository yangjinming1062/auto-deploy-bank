# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**smart-cloud** is a Spring Cloud-based scaffolding framework (version 1.0.6) that provides enterprise-grade microservices infrastructure. Key features include:

- **Service Merge/Deploy**: Services can be merged (internal process communication) or deployed separately (RPC communication)
- **Security**: Interface encryption, signature verification, and sensitive data desensitization
- **API Management**: Auto-documentation via YAPI, rate limiting, multi-version support, idempotency checks
- **Observability**: Structured logging (Log4j2/Logback), method-level logging, SQL logging, service monitoring via Spring Boot Admin
- **Data Layer**: Multi-datasource support, sharding, MyBatis Plus integration
- **Testing**: Comprehensive mock support for Redis, RabbitMQ, Elasticsearch, and database integration tests

## Architecture

### Module Structure

```
smart-cloud (40 Maven modules total)
├── smart-api-core
│   ├── smart-api-annotation     # API permissions, encryption, signature annotations
│   └── smart-user-context       # User context management
├── smart-cloud-starter          # 22 Spring Boot starter modules
│   ├── smart-cloud-starter-web              # Web layer (logging, exception handling, validation)
│   ├── smart-cloud-starter-feign            # Feign RPC (with merge/split support)
│   ├── smart-cloud-starter-redis            # Redis & distributed locks
│   ├── smart-cloud-starter-rabbitmq         # RabbitMQ (with retry via delayed queues)
│   ├── smart-cloud-starter-mybatis-plus     # MyBatis Plus & dynamic datasource
│   ├── smart-cloud-starter-mp-shardingjdbc  # Sharding JDBC
│   ├── smart-cloud-starter-log4j2           # Log4j2 with desensitization
│   ├── smart-cloud-starter-logback          # Logback with desensitization
│   ├── smart-cloud-starter-method-log       # Method aspect logging
│   ├── smart-cloud-starter-mock             # Mock data generation
│   ├── smart-cloud-starter-monitor-*        # Service monitoring (Spring Boot Admin)
│   ├── smart-cloud-starter-rate-limit       # API rate limiting
│   ├── smart-cloud-starter-api-version      # API versioning
│   ├── smart-cloud-starter-job              # Scheduled tasks (XXL-Job)
│   ├── smart-cloud-starter-locale           # Internationalization
│   └── [8 more starters...]
├── smart-code-generate           # Code generation (Freemarker templates)
├── smart-common-pojo             # Common DTOs, VOs, BOs, DOs
├── smart-common-web              # Shared web utilities
├── smart-constants               # System-wide constants & error codes
├── smart-exception               # Exception hierarchy & handling
├── smart-mask                    # Data desensitization
├── smart-test                    # Testing utilities
│   ├── smart-cloud-starter-test              # Base test configuration
│   ├── smart-cloud-starter-test-mock-rabbitmq
│   ├── smart-cloud-starter-test-mock-redis
│   └── smart-cloud-test-core                 # Unit & integration test helpers
└── smart-utility                 # Utility classes
```

### Service Merge Architecture

The framework's unique **service merge feature** allows combining microservices into a single deployment:

- **Separate Deployment**: Services communicate via Feign (HTTP/RPC)
- **Merged Deployment**: FeignClient annotations are disabled, direct method calls replace HTTP requests
- Controlled by `SmartFeignClientCondition` in `smart-cloud-starter-feign`
- Bean name conflicts resolved via custom naming rules
- Configuration via `YamlScan` annotation and SPI

### Technology Stack

| Component | Technology |
|-----------|-----------|
| Core | Spring Boot 2.6.15, Spring Cloud 2021.0.9, Java 8 |
| Gateway | Spring Cloud Gateway |
| Service Discovery/Config | Nacos |
| RPC | OpenFeign 3.1.2 |
| Database | MyBatis Plus 3.5.1, Dynamic Datasource 3.5.1, Sharding JDBC 5.1.0 |
| Cache | Redis (Redisson 3.17.1) |
| MQ | RabbitMQ |
| Monitoring | Spring Boot Admin 2.6.7 |
| Logging | Log4j2/Logback with custom desensitization |
| Testing | H2, Embedded Redis/RabbitMQ/Elasticsearch |
| Code Quality | PMD (Alibaba p3c rules), JaCoCo coverage |
| Documentation | YAPI via IDEA plugin |

## Common Development Commands

### Build & Test

```bash
# Build all modules
mvn clean install

# Run all tests
mvn clean test

# Run tests with PMD analysis
mvn clean test pmd:pmd -T 4

# Build without running tests
mvn clean install -DskipTests=true

# Test a single module
mvn test -pl <module-name>

# Test specific test class
mvn test -pl <module-name> -Dtest=ClassName

# Skip PMD during build
mvn clean install -DskipPMD=true
```

### Code Quality

```bash
# Run PMD analysis
mvn pmd:pmd

# Generate PMD report
mvn pmd:check

# Check code coverage (JaCoCo)
mvn clean test jacoco:report
```

### Deployment

```bash
# Deploy to Maven Central (requires credentials)
mvn clean deploy -Pdeploy
```

### IDE Integration

- Requires Java 8 and Maven 3.6+
- Lombok is used extensively - ensure annotation processing is enabled
- Use IntelliJ IDEA with the **yapi_upload** plugin for API documentation

## Testing Strategy

### Test Layers

1. **Unit Tests**: Use `smart-cloud-test-core` for base test classes
2. **Integration Tests**: Mock external dependencies:
   - Redis → `embedded-redis`
   - RabbitMQ → `rabbitmq-mock`
   - Elasticsearch → `embedded-elasticsearch`
   - Database → H2 in-memory database
3. **Service RPC**: Mock with Mockito for integration tests
4. **Nacos/Sentinel**: Disabled during integration tests to reduce dependencies

### Test Configuration

- Tests disable Nacos via Spring profiles
- Use H2 for database testing (alternative: transaction rollback or table cleanup)
- Podam for test data generation

## Error Codes

Common error codes in `smart-constants`:

| Code | Message |
|------|---------|
| 200 | Success |
| 101 | Verification failed |
| 102 | Data does not exist |
| 103 | Data already exists |
| 400 | Signature error |
| 401 | Unauthorized access |
| 409 | Duplicate commit |
| 417 | Failed to acquire lock |
| 419 | Session expired |
| 500 | Server exception |
| 2001 (web) | Parameter object cannot be null |
| 3001-3003 (es) | Elasticsearch datasource errors |

## Key Features & Usage

### Log Desensitization
- Implement via custom Jackson serializers
- Use `@MaskRule` annotation on fields
- Applied to web logs, Feign logs, SQL logs, MQ consumer logs

### Interface Mocking
- Automatic mock data generation via reflection
- Customizable mock rules via annotations
- Integrated with `smart-cloud-starter-mock`

### Service Monitoring
- Spring Boot Admin for service health (CPU, memory, GC, threads)
- Custom interface failure rate tracking via actuator
- WeChat Work notifications for service offline/online events

### API Documentation
- Automatically generated via IDEA **yapi_upload** plugin
- Uploaded to YAPI server
- Supports versioning and detailed parameter documentation

### Configuration Encryption
- Use Jasypt for sensitive config encryption
- Format: `ENC(encrypted_value)`
- Supports multi-key encryption

### Distributed Locking
- Redis-based locks via Redisson
- `@DistributedLock` annotation (in `smart-cloud-starter-redis`)
- Support for lock timeout and retry configuration

## CI/CD

### GitHub Actions Workflows

- **build.yml**: Runs on push/PR to `dev` branch
  - JDK 8, Maven, parallel build (`-T 4`)
  - Executes `mvn clean test pmd:pmd`
  - Uploads coverage to Codecov

- **deploy.yml**: Triggers on GitHub release
  - Deploys to Maven Central
  - Requires OSSRH credentials and GPG keys
  - Maven profiles: `clean deploy -Pdeploy -Dmaven.test.skip=true`

### Coverage Requirements

- Codecov threshold: 65-100%
- Ignored paths: test files, SqlMapper files, docs, annotations, pojos, constants
- Project-based coverage tracking

## Important Resources

- **Repository**: https://github.com/smart-cloud/smart-cloud
- **Examples**: https://github.com/smart-cloud/smart-cloud-examples
- **YAPI Plugin**: https://github.com/smart-cloud/yapi_upload
- **Documentation**: See `README.md` (Chinese) and `README_EN.md` (English)

## Development Notes

- **Java Version**: Strictly Java 8 (compatibility issues with newer versions)
- **Lombok**: Widely used - enable annotation processing
- **Spring Boot**: Version 2.6.15 (not 3.x)
- **Service Naming**: Custom bean naming rules to avoid conflicts when merging services
- **Configuration Loading**: Uses `YamlScan` annotation and Spring SPI for YAML auto-loading
- **Transaction Management**: Seata integration for distributed transactions