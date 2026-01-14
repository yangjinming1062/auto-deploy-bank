# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TDuck (填鸭表单) is a form/survey collection platform built with Spring Boot. The backend is a multi-module Maven project with 7 modules handling different aspects of the platform including forms, user accounts, storage, webhooks, and WeChat integration.

## Tech Stack

- **Framework**: Spring Boot 2.7.8
- **Java Version**: 1.8
- **Database**: MySQL 8.0+
- **ORM**: MyBatis Plus 3.5.3
- **Build Tool**: Maven
- **API Documentation**: SpringDoc OpenAPI (Swagger UI at /swagger-ui.html)
- **Caching**: EhCache
- **File Storage**: Aliyun OSS, Qiniu, Upyun, AWS S3, Local

## Module Architecture

The project is structured as a Maven multi-module architecture:

- **tduck-api** (`tduck-api/`): Main Spring Boot application entry point with web controllers, configurations, filters, interceptors, and resolvers
- **tduck-common** (`tduck-common/`): Shared utilities, common entities, constants, and base classes used across modules
- **tduck-form** (`tduck-form/`): Form creation, management, and response handling logic
- **tduck-account** (`tduck-account/`): User authentication, authorization, and account management
- **tduck-storage** (`tduck-storage/`): File upload/download management with support for multiple cloud providers
- **tduck-webhook** (`tduck-webhook/`): Webhook event notifications for form submissions
- **tduck-wx-mp** (`tduck-wx-mp/`): WeChat Mini Program integration

## Key Configuration Files

- **Root POM** (`pom.xml`): Multi-module Maven configuration with dependency management
- **API Config** (`tduck-api/src/main/resources/application.yml`): Development configuration (active profile: prod)
- **Production Config** (`tduck-api/src/main/resources/application-prod.yml`): Production database and external service settings
- **Docker Compose** (`docker/docker-compose.yaml`): MySQL and application container setup

## Build Commands

### Maven Commands

```bash
# Build all modules
mvn clean package -DskipTests

# Build specific module (from project root)
mvn clean package -pl tduck-api -am

# Run with specific profile
mvn spring-boot:run -Dspring-boot.run.profiles=prod

# Run tests
mvn test

# Run single test class
mvn test -Dtest=CacheTest

# Skip tests during build
mvn clean package -DskipTests
```

### Docker Deployment

```bash
# Using Docker Compose (recommended for development)
cd docker
docker-compose up -d

# Using Docker directly
docker run -d \
  --name tduck-platform \
  --restart=always \
  -p 8999:8999 \
  -e SPRING_DATASOURCE_URL="jdbc:mysql://127.0.0.1:3310/tduck-v4?useSSL=false&useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai&tinyInt1isBit=false&nullCatalogMeansCurrent=true" \
  -e SPRING_DATASOURCE_USERNAME=root \
  -e SPRING_DATASOURCE_PASSWORD=tduck@tduck \
  -v /upload:/application/BOOT-INF/lib/upload \
  tduckcloud/tduck-platform
```

## Running the Application

### Development Mode

1. **Start MySQL database:**
   ```bash
   cd docker
   docker-compose up -d mysql
   ```

2. **Run the application:**
   ```bash
   mvn spring-boot:run -pl tduck-api
   ```

3. **Access the application:**
   - API Base URL: http://localhost:8999
   - Swagger UI: http://localhost:8999/swagger-ui.html
   - API Docs: http://localhost:8999/v3/api-docs

4. **Default login credentials:**
   - Username: admin@tduckcloud.com
   - Password: 123456
   - ⚠️ Change default password immediately after first login

### Profile Configuration

- **Development**: Uses `application.yml` with dev settings
- **Production**: Uses `application-prod.yml` (active by default)
- **Custom profiles**: Create `application-{profile}.yml` and run with `-Dspring-boot.run.profiles={profile}`

## Database Configuration

The application uses MySQL with the following default settings:
- **Host**: localhost:3306
- **Database**: tduck
- **Username**: root
- **Password**: root (development) or tduck@mysql (docker)
- **Character Set**: utf8mb4
- **Collation**: utf8mb4_unicode_ci

The database schema is automatically initialized via:
- **Docker**: `docker/init-db/tduck-v5.sql`
- **Manual setup**: Execute the SQL file against your MySQL instance

## External Service Configuration

### Mail Configuration
- **Development**: SMTP server in `application.yml`
- **Production**: Configure in `application-prod.yml`
- **Default**: 163.com SMTP (test credentials)

### WeChat Integration
Configure in `application-prod.yml`:
```yaml
wx:
  mp:
    configs:
      - appId: your_app_id
        secret: your_secret
        token: your_token
        aesKey: your_aes_key
```

### File Storage Providers
Supported providers (configured per environment):
- Aliyun OSS
- Qiniu
- Upyun
- AWS S3
- Local storage

## Code Structure Patterns

### API Layer (`tduck-api/src/main/java/com/tduck/cloud/api/`)
```
├── config/          # Spring configurations (security, caching, etc.)
├── web/
│   ├── controller/  # REST controllers
│   ├── filter/      # Request filters
│   ├── interceptor/ # Request interceptors
│   └── resolver/    # Argument resolvers
├── listener/        # Application event listeners
├── handler/         # Exception handlers
├── exception/       # Custom exceptions
├── util/            # Utility classes
└── annotation/      # Custom annotations
```

### Package Naming
All modules use the base package: `com.tduck.cloud.{module-name}`

### Entity Management
- MyBatis Plus is used for ORM
- Entities use `@TableName` annotation
- Auto-generated ID strategy: AUTO (database ID auto-increment)

## Testing

The project uses:
- **Test Framework**: JUnit 4
- **Spring Test**: `@SpringBootTest` with webEnvironment
- **Test Location**: `src/test/java/` in each module

Example test class:
```java
@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class CacheTest {
    @Autowired
    CacheUtils cacheUtils;

    @Test
    public void testMethod() {
        // test code
    }
}
```

## Logging Configuration

- **Framework**: Logback
- **Default Level**: DEBUG for `com.tduck.cloud` package
- **Config File**: `application-prod.yml` references `classpath:logback-spring.xml`
- **Request Tracing**: Configurable via `platform.request.trace-log`

## Important Development Notes

1. **Multi-module Dependencies**: The `tduck-api` module depends on all other modules. When modifying common code, rebuild dependent modules with `-am` flag.

2. **Profile-Specific Config**: Production profile is active by default in `application.yml`. Always verify which profile is active when debugging configuration issues.

3. **Database Migration**: Use `docker/init-db/tduck-v5.sql` for database initialization. For schema changes, you'll need to update this file or use a migration tool.

4. **API Documentation**: Swagger UI is automatically generated and available at `/swagger-ui.html` when the application starts.

5. **File Upload Limits**:
   - Max file size: 1000MB
   - Max request size: 1000MB
   - Configure in `application.yml` under `spring.servlet.multipart`

6. **Caching**: EhCache is enabled. Clear cache during development if you encounter stale data.

7. **JWT Configuration**:
   - Secret: `f6f31a5f2136758f86b67cde583cb125` (default, should change in production)
   - Expiration: 7 days (604800 seconds)
   - Header name: `token`

## Docker Development

The `docker/` directory provides a complete development environment:

```bash
cd docker
docker-compose up -d
```

This starts:
- MySQL 8.0.36 (port 3306)
- TDuck Platform (port 8999)
- Persistent volumes for MySQL data and uploaded files

## Useful Resources

- **Online Demo**: https://www.tduckcloud.com
- **Documentation**: https://doc.tduckcloud.com
- **Frontend Repository**: https://gitee.com/TDuckApp/tduck-front
- **Issue Tracker**: https://gitee.com/TDuckApp/tduck-platform/issues