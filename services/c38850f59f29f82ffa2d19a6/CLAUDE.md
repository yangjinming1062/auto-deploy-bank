# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Build entire project
mvn clean package -DskipTests

# Build specific module
mvn clean package -DskipTests -pl mall-admin

# Run development environment
mvn spring-boot:run -pl mall-admin

# Generate MyBatis code from database (in mall-mbg)
mvn mybatis-generator:generate

# Build Docker image
mvn package -DskipTests docker:build
```

## Project Architecture

This is a Spring Boot 2.3.0 e-commerce platform with a multi-module Maven structure:

```
mall (parent POM)
├── mall-common          # Shared utilities, API responses, exception handling
├── mall-mbg             # MyBatis Generator code (model + mapper)
├── mall-security        # Spring Security + JWT authentication module
├── mall-admin           # Admin management API (port 8080)
├── mall-search          # Elasticsearch-based search API (port 8081)
├── mall-portal          # Customer-facing API (port 8085)
└── mall-demo            # Demo/test module (port 8082)
```

### Module Dependencies
- `mall-admin`, `mall-search`, `mall-portal` depend on `mall-security`, `mall-mbg`, and `mall-common`
- `mall-mbg` generates code from the database schema (document/sql/mall.sql)

### Technology Stack
- **Framework**: Spring Boot 2.3.0 + Spring Security
- **ORM**: MyBatis with PageHelper pagination
- **Database**: MySQL 5.7, MongoDB (mall-portal), Elasticsearch 7.6.2 (mall-search)
- **Cache**: Redis 5.0
- **Message Queue**: RabbitMQ 3.7.14
- **API Docs**: Swagger 2.9.2 (springfox)
- **Storage**: Aliyun OSS, MinIO
- **Logging**: Logstash + Kibana (ELK)

### Response Pattern

All API responses use `CommonResult<T>` wrapper:
```java
CommonResult.success(data)
CommonResult.failed("error message")
CommonResult.failed(ErrorCodeEnum)
CommonResult.validateFailed()
```

Error codes implement `IErrorCode` interface. Use `Asserts.fail()` to throw exceptions.

### Standard Controller Patterns

Controllers follow these conventions:
- Use `@Controller` (not `@RestController`)
- Methods return `CommonResult<T>` with `@ResponseBody`
- Annotate with `@Api` and `@ApiOperation` for Swagger
- Mapping: `/product/**`, `/order/**`, etc.
- Pagination: `pageSize` and `pageNum` parameters; wrap with `CommonPage<T>`

### Swagger Configuration

Each module has a `SwaggerConfig` extending `BaseSwaggerConfig`:
- Defines API base package and title
- mall-search has security disabled; other modules use JWT via Authorization header
- Swagger UI available at `/swagger-ui.html`

### Security Configuration

- JWT tokens stored in `Authorization` header with `Bearer ` prefix
- Token expiration: 7 days (604800 seconds)
- Config in `application.yml` under `jwt` and `secure.ignored.urls`
- Spring Security filters: `JwtAuthenticationTokenFilter` before `UsernamePasswordAuthenticationFilter`

### Configuration Profiles

- `application-dev.yml`: Local development (localhost databases)
- `application-prod.yml`: Docker production (uses service names like `db`, `redis`)

Key middleware:
- MySQL: `localhost:3306` (dev) / `db:3306` (prod)
- Redis: `localhost:6379` (dev) / `redis:6379` (prod)
- Elasticsearch: `localhost:9200` (dev) / `es:9200` (prod)

### Database

Schema in `document/sql/mall.sql`. Run against MySQL before starting the application.

## Code Conventions

- Models (entity classes) in `mall-mbg/src/main/java/com/macro/mall/model`
- Mapper interfaces in `mall-mbg/src/main/java/com/macro/mall/mapper`
- Custom DAOs in module's `dao/` package
- Services in module's `service/` package
- Controllers in module's `controller/` package
- DTOs/request params in module's `dto/` package