# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **mall-learning** tutorial repository - a comprehensive learning project for the mall e-commerce system. It's a Maven-based multi-module Spring Boot project that demonstrates modern Java development practices through progressive modules.

**Key Documentation:**
- Main tutorial site: https://www.macrozheng.com
- Project documentation: `/docs/README.md`
- Parent POM: `/pom.xml` (Spring Boot 2.7.5, Java 8)

## Technology Stack

- **Core:** Spring Boot 2.7.5, Java 8, Maven
- **Data:** MyBatis 3.5.10, MySQL 8.0.29, Druid 1.2.14
- **Cache/Search:** Redis, Elasticsearch 7.x
- **NoSQL:** MongoDB
- **Messaging:** RabbitMQ
- **Security:** Spring Security + JWT
- **API Docs:** Swagger 3.0.0 (springfox)
- **Storage:** MinIO (S3-compatible), Aliyun OSS
- **Utilities:** Lombok, Hutool 5.8.9

## Project Structure

```
/home/ubuntu/deploy-projects/65015220be34a8abff3e6846/
├── pom.xml                          # Parent POM with all dependencies
├── README.md                        # Main project documentation
├── docs/                            # Documentation site source
│   ├── architect/                   # Architecture tutorials
│   ├── database/                    # Database design docs
│   ├── deploy/                      # Deployment guides
│   ├── technology/                  # Technical deep-dives
│   └── reference/                   # Technology references
├── mall-tiny/                       # Complete integrated module
├── mall-tiny-01 through mall-tiny-08  # Incremental learning modules
├── mall-tiny-generator/             # MyBatis code generation utility
├── mall-tiny-docker/                # Docker containerization examples
└── mall-tiny-{redis,rabbit,swagger,etc.}  # Technology-specific modules
```

Each module is an independent Spring Boot application demonstrating specific technologies or integrations. The numbering (01-08) represents the recommended learning sequence.

## Common Development Commands

### Building & Running

```bash
# Build entire project
mvn clean install

# Build specific module
mvn clean install -pl mall-tiny-01

# Run specific module
mvn -pl mall-tiny-01 spring-boot:run

# Skip tests during build (default in parent POM)
mvn clean install -DskipTests

# Run with specific profile
mvn -pl mall-tiny spring-boot:run -Dspring-boot.run.profiles=dev
```

### Testing

```bash
# Run all tests in project
mvn test

# Run tests for specific module
mvn test -pl mall-tiny-mybatis

# Run specific test class
mvn test -pl mall-tiny-mybatis -Dtest=MyBatisBaseTest

# View test reports
cat target/surefire-reports/*.txt
```

Tests use JUnit 5 and follow the pattern:
- Location: `/src/test/java/`
- Example: `mall-tiny-mybatis/src/test/java/com/macro/mall/tiny/test/MyBatisBaseTest.java`

### Code Generation

The `mall-tiny-generator` module generates MyBatis code from database schemas:

```bash
# Generate code for all tables configured in generatorConfig.xml
mvn -pl mall-tiny-generator mybatis-generator:generate

# Generate code for specific module
mvn -pl mall-tiny-01 mybatis-generator:generate
```

Configuration: `src/main/resources/generatorConfig.xml`

MyBatis generator creates:
- Model classes: `com.macro.mall.tiny.mbg.model`
- Mapper interfaces: `com.macro.mall.tiny.mbg.mapper`
- XML mappers: `src/main/resources/com/**/mapper/`

### Docker Operations

Containerization examples in `mall-tiny-docker`:

```bash
# Build Docker image
mvn -pl mall-tiny-docker clean package docker:build

# Run with docker-compose (includes MySQL)
cd mall-tiny-docker/src/main/docker
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker logs mall-tiny-docker
```

Docker configuration:
- Dockerfile: `src/main/docker/Dockerfile`
- Compose file: `src/main/docker/docker-compose.yml`
- Exposed ports: 8080 (app), 3306 (MySQL)

## Code Architecture

Each module follows standard Spring Boot layered architecture:

```
com.macro.mall.tiny/
├── MallTinyApplication.java       # Main application class
├── common/                        # Common utilities & constants
├── component/                     # Spring components (e.g., login handler)
├── config/                        # Configuration classes
│   ├── MyBatisConfig.java         # MyBatis configuration
│   ├── SecurityConfig.java        # Spring Security config
│   ├── Swagger2Config.java        # API documentation config
│   └── RedisConfig.java           # Redis configuration
├── controller/                    # REST controllers
├── service/                       # Business logic layer
├── dao/                           # Data access layer (MyBatis mappers)
├── domain/                        # Request/Response DTOs
├── mbg/                           # Generated MyBatis code
│   ├── model/                     # Entity models
│   └── mapper/                    # Mapper interfaces
└── nosql/                         # NoSQL repositories (MongoDB)
```

### Key Configuration Files

- **application.yml:** Module-specific configuration
  - Server port, datasource, Redis, Elasticsearch, MongoDB, RabbitMQ settings
  - MinIO/S3 configuration
  - JWT token configuration
  - Security ignored paths (Swagger, static resources, etc.)

- **generatorConfig.xml:** MyBatis code generation configuration
  - Database connection properties (references `generator.properties`)
  - Table definitions for code generation
  - Custom comment generators and plugins

### Module Dependencies

Most modules depend on the parent POM which provides:
- Spring Boot dependencies and version management
- Common properties (Java 8, UTF-8 encoding)
- MyBatis, Druid, Lombok, Hutool versions
- Aliyun Maven mirror for faster downloads

Individual modules add specific technology dependencies:
- **mall-tiny-01:** Basic Spring Boot + MyBatis + MySQL
- **mall-tiny-swagger:** Adds Swagger API documentation
- **mall-tiny-redis:** Adds Redis caching
- **mall-tiny:** Complete integration of all technologies
- **mall-tiny-generator:** Standalone code generation utility

## Database Setup

The project uses MySQL with the following pattern:

1. **Schema:** `mall_tiny` (default database name)
2. **Credentials:** Typically `root:root` (local development)
3. **Tables:** Generated via MyBatis Generator from `generatorConfig.xml`
4. **Connection:** Configured in `application.yml`

Example modules generate tables like:
- `pms_brand` (Product Management - Brand)
- `ums_admin` (User Management System - Admin)
- `ums_role` (User Management System - Role)

## API Documentation

Swagger 3.0 integration provides API docs at `/swagger-ui/`:

- **Config:** `com.macro.mall.tiny.config.Swagger2Config.java`
- **URL:** http://localhost:8080/swagger-ui/ (when running)
- **Ignored paths:** Configured in `application.yml` under `secure.ignored.urls`

## Module-Specific Notes

### mall-tiny-generator
- **Purpose:** Standalone MyBatis code generation utility
- **Usage:** Run `mybatis-generator:generate` to create model/mapper code
- **Output:** Generates to `src/main/java/com/macro/mall/tiny/mbg/` and resources

### mall-tiny-docker
- **Purpose:** Demonstrates containerization
- **Features:** Dockerfile + docker-compose with MySQL
- **Profile:** Runs with `spring.profiles.active=prod`

### mall-tiny-mybatis
- **Purpose:** MyBatis features demonstration
- **Tests:** Contains comprehensive test examples
- **Focus:** CRUD operations, advanced queries, mapper usage

### mall-tiny-stream
- **Purpose:** Java 8 Stream API demonstration
- **Tests:** StreamApiTest.java shows practical Stream operations

## Key Learning Path

Recommended sequence based on module numbers:
1. **mall-tiny-01:** Spring Boot + MyBatis basics
2. **mall-tiny-02:** Incremental feature
3. **mall-tiny-03:** Another feature increment
4. **...** (continue through 08)
5. **mall-tiny:** Complete integrated example
6. **mall-tiny-{tech}:** Deep dives into specific technologies

Each module builds upon previous ones, adding new technologies or integrations.

## Important Notes

- **skipTests=true** by default in parent POM - tests don't run during build unless explicitly enabled
- **MyBatis Generator** requires database connection - configure in `generator.properties`
- **Swagger** access requires URLs to be in `secure.ignored.urls` whitelist
- **Redis/Elasticsearch/MongoDB/RabbitMQ** must be running locally for full functionality
- **MinIO** runs on port 9000 (not 9001 as commonly used)
- Each module has its own `application.yml` - check before running
- Generated MyBatis code (in `/mbg/` directories) can be regenerated at any time

## Development Tips

- Start with `mall-tiny-01` for basic setup understanding
- Use `mall-tiny-generator` to regenerate code after schema changes
- Check module-specific `pom.xml` for unique dependencies
- Review `application.yml` for database/service connection details
- Use Spring profiles to manage environment-specific configs
- Reference `/docs/` directory for detailed tutorials and explanations