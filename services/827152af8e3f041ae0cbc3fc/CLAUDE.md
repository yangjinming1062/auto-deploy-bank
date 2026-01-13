# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of **Spring Boot tutorial projects** from the "Spring Boot实战合集" series by CodeSheep (程序羊). Each subdirectory contains an independent Spring Boot example demonstrating different Spring Boot features and integrations.

## Language & Build System

- **Language**: Java 1.8+
- **Build Tool**: Maven (all projects use `pom.xml`)
- **Framework**: Spring Boot (mostly version 2.0.x)
- **Parent POM**: Most projects extend `spring-boot-starter-parent`

## Common Development Commands

All commands should be run from within individual project directories:

```bash
# Build the project
mvn clean package

# Build without running tests
mvn clean package -DskipTests

# Run tests
mvn test

# Run a specific test class
mvn test -Dtest=ClassName

# Run Spring Boot application
mvn spring-boot:run

# Run with specific profile
mvn spring-boot:run -Dspring-boot.run.profiles=dev

# Clean build
mvn clean
```

**Note**: Projects in subdirectories require navigating to those directories first. For multi-module projects (like `springbt_sso_jwt`), run commands from the root directory to build all modules.

## Architecture & Structure

Each project follows the standard Maven Spring Boot structure:

```
project-root/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── {package}/
│   │   │       ├── Application.java (Spring Boot main class)
│   │   │       ├── config/
│   │   │       ├── controller/
│   │   │       ├── service/
│   │   │       ├── repository/
│   │   │       └── entity/
│   │   └── resources/
│   │       └── application.yml
│   └── test/
│       └── java/
└── README.md
```

### Multi-Module Projects

Some projects are multi-module Maven projects:
- **springbt_sso_jwt**: Contains 3 modules (server, client1, client2)
- **springbt_uid_generator**: Contains 2 modules (uid-generator, uid-consumer)
- **spring_boot_admin2.0_demo**: Contains 2 modules (sba_server_2_0, sba_client_2_0)

For multi-module projects, the parent `pom.xml` uses `<modules>` to define sub-projects.

## Project Catalog

### Security & Authentication
- **springbt_security_jwt**: JWT-based authentication system
- **springbt_sso_jwt**: SSO with Spring Security OAuth2 + JWT (multi-module)

### Caching
- **springbt_guava_cache**: Guava Cache integration
- **springbt_ehcache**: Ehcache implementation
- **springbt_evcache**: EVCache integration

### Monitoring & Admin
- **springbt_admin_server**: Application monitoring with Spring Boot Admin
- **spring_boot_admin2.0_demo**: Spring Boot Admin 2.0 examples (multi-module)

### Databases & Persistence
- **springbt_mybatis_sqlserver**: MyBatis with SQL Server
- **springboot_es_demo**: Elasticsearch integration
- **springbt_uid_generator**: UidGenerator for unique IDs (multi-module)
- **springbt_vesta**: Vesta ID generator

### Utilities & Integrations
- **springbt_watermark**: Image upload with watermarks
- **kotlin_with_springbt**: Kotlin + Spring Boot hybrid project

### Custom Starters
- **id-spring-boot-starter**: Custom ID generation starter
- **test-id-spring-boot-starter**: Test ID starter

## Configuration Patterns

Most projects use `application.yml` with these common patterns:

```yaml
server:
  port: XXXX

spring:
  profiles:
    active: dev
```

Database configurations vary by project. Some use MySQL, H2, or other databases as specified in their README files.

## Testing

All projects include:
- Standard JUnit tests in `src/test/java`
- Spring Boot Test annotations
- Test resources in `src/test/resources`

Test execution follows standard Maven lifecycle:
```bash
mvn test
```

## Key Technical Notes

1. **Spring Boot Version**: Most projects use Spring Boot 2.0.x (2.0.6.RELEASE, 2.0.8.RELEASE)
2. **Java Version**: Java 1.8
3. **Chinese Documentation**: All README files are in Chinese
4. **No CI/CD**: No GitHub Actions or CI configuration files present
5. **No Wrapper Scripts**: Standard Maven commands require `mvn` installed
6. **External Dependencies**: Some projects require external services (MySQL, Elasticsearch, etc.)

## Development Approach

This is a **tutorial/educational repository**. Each project is:
- Self-contained example
- Focused on demonstrating specific Spring Boot features
- Documented with detailed README files
- Intended for learning and reference

When making changes:
- Respect the educational nature of the code
- Maintain compatibility with Spring Boot 2.0.x
- Keep explanations clear and practical
- Test changes in the context of the specific feature being demonstrated

## Author Information

- Author: CodeSheep (程序羊)
- Blog: https://www.codesheep.cn
- GitHub: https://github.com/hansonwang99