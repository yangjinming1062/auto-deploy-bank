# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**renren-security** is a lightweight, permission-based Java rapid development platform built with SpringBoot, Shiro, and MyBatis-Plus. It implements front-end/back-end separation with token-based authentication and includes a code generator for accelerated development.

**Technology Stack:**
- Spring Boot 2.7.1
- Apache Shiro 1.9 (security)
- MyBatis-Plus 3.5.2 (ORM)
- Druid 1.2.11 (database connection pool)
- Quartz 2.3 (scheduling)
- Redis (caching)
- Knife4j 2.0.9 (API documentation)
- Vue 2.x (frontend)

## Architecture

### Module Structure

The project is a multi-module Maven application with five main modules:

```
renren-security (parent pom)
├── renren-common              # Shared utilities and common code
├── renren-dynamic-datasource  # Multi-datasource support
├── renren-admin               # Admin backend (main web application)
├── renren-api                 # REST API service
└── renren-generator           # Code generation tool
```

### Code Organization

Each module follows a layered architecture pattern:

**Standard package structure:**
```
io.renren.modules.{module}/
├── controller/    # REST controllers (@RestController)
├── service/       # Business logic layer (@Service)
├── dao/           # Data access layer (MyBatis @Mapper)
├── entity/        # Database entities (MyBatis-Plus @TableName)
├── dto/           # Data Transfer Objects
├── enums/         # Java Enums
├── redis/         # Redis utilities
└── excel/         # Excel import/export utilities
```

**Configuration files:**
- `src/main/resources/mapper/` - MyBatis XML mapper files
- `src/main/resources/i18n/` - Internationalization messages

**renren-admin module breakdown:**
- `modules/sys/` - Core system management (users, roles, menus, departments, parameters, dictionary)
- `modules/job/` - Quartz scheduled tasks management
- `modules/log/` - System logging and operation tracking
- `modules/oss/` - File storage service (Qiniu, Aliyun OSS, Tencent Cloud COS)
- `modules/security/` - Shiro security configuration and token management

## Common Development Commands

### Build Commands
```bash
# Build all modules
mvn clean install

# Build without running tests
mvn clean install -DskipTests

# Build specific module
cd renren-admin && mvn clean install

# Package as WAR/JAR
mvn clean package
```

### Running the Application

**Admin Backend (Primary Application):**
```bash
# Build first
cd renren-admin
mvn clean install -DskipTests

# Run with dev profile
mvn spring-boot:run -Dspring-boot.run.profiles=dev

# Or run the main class directly
java -jar target/renren-admin.jar --spring.profiles.active=dev
```

**Access Points:**
- Admin UI: http://localhost:8080/renren-admin
- API Docs (Swagger): http://localhost:8080/renren-admin/doc.html
- Druid Admin: http://localhost:8080/renren-admin/druid/ (for database monitoring)

**API Service:**
```bash
cd renren-api
mvn spring-boot:run -Dspring-boot.run.profiles=dev
```

**Code Generator:**
```bash
cd renren-generator
mvn spring-boot:run -Dspring-boot.run.profiles=dev
# Then visit: http://localhost:8081/generator.html
```

### Testing

```bash
# Run all tests (note: tests are skipped by default in renren-admin/pom.xml)
mvn test

# Run tests for specific module
cd renren-admin && mvn test

# Run single test class
mvn test -Dtest=ClassName

# Run specific test methods
mvn test -Dtest=ClassName#methodName

# Run with Maven wrapper (if available)
mvnw clean install
```

**Test Files Location:**
- `renren-admin/src/test/java/io/renren/DynamicDataSourceTest.java` - Multi-datasource testing
- `renren-admin/src/test/java/io/renren/RedisTest.java` - Redis caching operations
- `renren-admin/src/test/java/io/renren/service/DynamicDataSourceTestService.java` - Test service

**Note:** The `maven-surefire-plugin` in renren-admin has `skipTests=true` by default. Override with `-DskipTests=false` when needed.

### Code Generation

The project includes a built-in code generator for rapid development:

1. Configure `renren-generator/src/main/resources/generator.properties`:
   - Set package name, module name, author
   - Configure database table prefix
   - Adjust type mappings if needed

2. Run the generator:
   ```bash
   cd renren-generator
   mvn spring-boot:run
   ```

3. Configure database connection in the web interface at `http://localhost:8081/generator.html`

4. Generate code for tables (outputs entity, DAO, service, controller, Vue files)

**Template Location:** `renren-generator/src/main/resources/template/` (can be customized)

## Database Setup

### Prerequisites
- MySQL 8.0+ (primary database)
- Oracle 11g+ (supported)
- SQL Server 2012+ (supported)
- PostgreSQL 9.4+ (supported)

### Setup Steps

1. Create database `renren_security` with UTF-8 encoding
2. Import SQL script from `renren-admin/db/`:
   - `mysql.sql` - MySQL database structure
   - `oracle.sql` - Oracle database structure
   - `postgresql.sql` - PostgreSQL database structure
   - `sqlserver.sql` - SQL Server database structure

3. Configure database connection in `renren-admin/src/main/resources/application-dev.yml`:
   ```yaml
   spring:
     datasource:
       druid:
         url: jdbc:mysql://localhost:3306/renren_security?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Shanghai&nullCatalogMeansCurrent=true
         username: renren
         password: 123456
   ```

4. **Default Login:** admin / admin

### Redis Configuration (Optional)

Redis is used for caching. Configure in `application.yml`:
```yaml
spring:
  redis:
    database: 0
    host: 192.168.10.10
    port: 6379
    password:
    timeout: 6000ms
```

Enable/disable via `renren.redis.open: false/true`

## Configuration Files

### Key Configuration Locations
- **Root:** `pom.xml` - Parent POM with dependencies
- **renren-admin:** `src/main/resources/application.yml` - Base configuration
- **renren-admin:** `src/main/resources/application-dev.yml` - Dev environment settings
- **renren-admin:** `src/main/resources/application-test.yml` - Test environment
- **renren-admin:** `src/main/resources/application-prod.yml` - Production settings
- **renren-generator:** `src/main/resources/generator.properties` - Code generator settings

### Profile-specific Settings
- **dev** - Development with MySQL, disabled caching
- **test** - Testing environment
- **prod** - Production with optimizations

## Development Workflow

### New Module Development
1. Generate skeleton code using the code generator
2. Customize generated templates in `renren-generator/src/main/resources/template/`
3. Implement business logic in `service/` layer
4. Add REST endpoints in `controller/` layer
5. Configure MyBatis mappers in `resources/mapper/` directory
6. Update data permissions and security annotations as needed

### Adding New API Endpoints
1. Create entity in `entity/` package
2. Create DAO mapper in `dao/` package and corresponding XML in `resources/mapper/`
3. Create service interface and implementation in `service/` package
4. Create controller with `@RestController` annotation
5. Add Swagger documentation annotations
6. Implement token-based authentication via Shiro

### Security Model
- **Authentication:** Shiro + JWT token
- **Authorization:** RBAC (Role-Based Access Control) with data permissions
- **Data Scoping:** Control access by department/user hierarchy
- **XSS Protection:** Built-in filtering and sanitization

## Testing

Test files are located in `src/test/java/`:
- `DynamicDataSourceTest.java` - Multi-datasource functionality
- `RedisTest.java` - Redis caching operations
- `DynamicDataSourceTestService.java` - Test service

## Key Dependencies

All versions managed in parent `pom.xml`:
- Spring Boot 2.7.1
- MyBatis-Plus 3.5.2
- Druid 1.2.11
- Knife4j 2.0.9 (Swagger/OpenAPI)
- Hutool 5.7.22 (Utility library)
- Joda-Time 2.10.14 (Date handling)

## Docker Support

Use `docker-compose.yml` to run all services:
```bash
# Build all images first
mvn clean install -DskipTests

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services:
- **renren-admin:** http://localhost:8080/renren-admin (port 8080)
- **renren-api:** http://localhost:8081 (port 8081)

**Build Docker images manually:**
```bash
# Build admin image
cd renren-admin
mvn clean package docker:build

# Build API image
cd renren-api
mvn clean package docker:build
```

## IDE Requirements

**Required Plugins:**
- **Lombok** - Must install Lombok plugin for IDE (IntelliJ/Eclipse) to resolve generated getters/setters

**Recommended IDE:**
- IntelliJ IDEA
- Eclipse with Spring Boot plugins

## Important Notes

1. **Code Style:** Follow standard Java conventions (CamelCase for classes, camelCase for methods)
2. **Database Migrations:** Use provided SQL scripts; maintain consistency across environments
3. **API Documentation:** Auto-generated via Knife4j at `/doc.html`
4. **Data Permissions:** Use `@DataFilter` annotation for automatic data scoping
5. **File Uploads:** Handled via `modules/oss/` with support for Qiniu, Aliyun, Tencent Cloud
6. **Scheduled Tasks:** Configure in `modules/job/` using Quartz annotations

## Documentation

- Project Documentation: https://www.renren.io/guide/security
- Community Forum: https://www.renren.io/community
- Frontend Project: https://gitee.com/renrenio/renren-ui