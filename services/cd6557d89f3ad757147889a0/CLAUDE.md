# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of 70+ Spring Boot tutorial projects demonstrating various Spring Boot features and integrations. Each subdirectory is a standalone, runnable Spring Boot application with its own `pom.xml`.

## Common Commands

All commands run from within individual project directories (where `pom.xml` exists).

### Build and Run
```bash
mvn clean install          # Build the project
mvn spring-boot:run        # Run the application
java -jar target/*.jar     # Run compiled JAR
```

### Testing
```bash
mvn test                                    # Run all tests
mvn test -Dtest=EmployeeRepositoryTests     # Run specific test class
mvn test -Dtest=EmployeeControllerIT        # Run integration test
```

### IDE
Open any project folder directly in IntelliJ IDEA or Eclipse as a Maven project.

## Architecture Patterns

Each Spring Boot project follows standard patterns:

**Project Structure:**
```
<project>/
├── src/main/java/<package>/
│   ├── Application.java          # @SpringBootApplication entry point
│   ├── controller/               # REST controllers (@RestController)
│   ├── service/                  # Business logic (@Service)
│   ├── repository/               # Data access (@Repository)
│   ├── model/ or entity/         # Domain entities (@Entity)
│   ├── config/                   # Configuration classes (@Configuration)
│   └── exception/                # Custom exceptions
├── src/main/resources/
│   ├── application.properties    # or application.yml
│   └── static/                   # Static assets (JS, CSS)
├── src/test/java/                # Unit and integration tests
└── pom.xml
```

**Common Dependencies (in pom.xml):**
- `spring-boot-starter-web` - REST API support
- `spring-boot-starter-data-jpa` - JPA/Hibernate ORM
- `spring-boot-starter-security` - Authentication
- `spring-boot-starter-test` - Testing (JUnit, Mockito)
- Database drivers: mysql-connector-java, h2, postgresql, etc.

**Test Annotations:**
- `@DataJpaTest` - Slice test for JPA repositories
- `@SpringBootTest` - Full integration test
- `@RunWith(SpringRunner.class)` - JUnit 4 runner
- JUnit 5 projects exclude vintage engine and use `maven-surefire-plugin`

## Database Configuration

Most projects use external databases (MySQL, PostgreSQL, MongoDB). Configure connection in `src/main/resources/application.properties`:
```properties
spring.datasource.url=jdbc:mysql://localhost:3306/dbname
spring.datasource.username=root
spring.datasource.password=password
```

Some testing examples use H2 in-memory database (`com.h2database:h2`).

## Project Categories

- **CRUD APIs**: springboot2-jpa-crud-example, springboot-crud-rest
- **Database Mappings**: springboot-hibernate-*-mapping (one-to-one, one-to-many, many-to-many)
- **Security**: Springboot-Security-Project, Spring security JWT
- **Messaging**: Springboot-ActiveMQ-Sample, springboot2-jms-activemq
- **Cloud**: spring-cloud-loadbalance, Project-4.SpringBoot-AWS-S3
- **Testing**: springboot-testing-examples, springboot2-junit5-example
- **Templating**: springboot-thymeleaf-*, springboot-jsp-*