# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
mvn clean install          # Build and install to local repository
mvn clean package          # Package as JAR
mvn spring-boot:run        # Run application directly
mvn test                   # Run unit tests
mvn clean                  # Clean build artifacts

# With profiles
mvn clean install -Pdev    # Development profile
mvn clean install -Ppro    # Production profile
```

## Technology Stack

- **Backend:** Spring Boot 2.0.3.RELEASE, MyBatis 3.4.4, Apache Shiro 1.3.2
- **Templating:** Thymeleaf (LEGACYHTML5 mode)
- **Database:** MySQL with Alibaba Druid connection pool
- **Caching:** Ehcache with Redis backup
- **Workflow:** Activiti 5.22.0
- **Frontend:** jQuery, Bootstrap, Bootstrap Table, Layer, jsTree, Summernote
- **Java Version:** 1.8

## Project Structure

```
bootdo/
├── src/main/java/com/bootdo/
│   ├── common/          # Shared utilities, configs, aspects, base classes
│   ├── system/          # User, role, menu, dept management (core module)
│   ├── blog/            # Content management (articles, links, categories)
│   ├── activiti/        # Workflow engine and process designer
│   └── oa/              # Office automation (notifications, leave requests)
└── src/main/resources/
    ├── mybatis/         # MyBatis mapper XML files
    ├── static/          # CSS, JS, frontend assets
    └── templates/       # Thymeleaf templates by module
```

## Architecture Overview

This is a layered enterprise application following standard Spring Boot patterns:

1. **Controller Layer** (`*/controller/`): REST APIs and page controllers. All extend `BaseController` for user context.
2. **Service Layer** (`*/service/`): Business logic with interface-based design. Implementations in `impl/` subdirectory.
3. **DAO Layer** (`*/dao/`): MyBatis mapper interfaces with XML configurations in `resources/mybatis/`
4. **Domain Layer** (`*/domain/`): Entity classes and value objects

**Key shared components** in `common/`:
- `config/`: Druid, Cache, Quartz, Web, Async configurations
- `aspect/`: AOP for logging (@Log annotation) and other cross-cutting concerns
- `utils/`: ShiroUtils, DateUtils, etc.
- `exception/`: Custom exception handlers
- `filter/`: XSS filtering (JSoup-based)

## Database Configuration

- **Database required:** MySQL database named `bootdo`
- **Default credentials:** admin / 111111 (configured in `application-dev.yml`)
- **Upload path:** `c:/var/uploaded_files/` (configurable)
- **Default port:** 80

## Important Notes

- MyBatis mappers use underscore-to-camel case mapping
- Shiro uses Ehcache for session and authorization caching
- All controllers extend `BaseController` for shared functionality
- Passwords are SHA1 hashed (irreversible)
- Double validation: client-side (JQuery Validation) and server-side
- API documentation via Swagger 2 (springfox 2.6.1)