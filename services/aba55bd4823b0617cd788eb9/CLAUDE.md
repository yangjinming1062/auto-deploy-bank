# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains a comprehensive Spring Boot 3.5.6 tutorial with 11 numbered sections, each containing multiple standalone demo projects. Each project is self-contained and demonstrates specific Spring Boot features. The projects are arranged in a learning progression from basic concepts to advanced topics.

## Repository Structure

- **01-spring-boot-overview**: Basic Spring Boot setup, DevTools, Actuator, properties, CLI
- **02-spring-boot-spring-core**: Core Spring concepts and dependency injection
- **03-spring-boot-hibernate-jpa-crud**: JPA and Hibernate basics with CRUD operations
- **04-spring-boot-rest-crud**: REST APIs with Spring Boot
- **05-spring-boot-rest-security**: Securing REST APIs with Spring Security
- **06-spring-boot-spring-mvc**: Spring MVC fundamentals and form handling
- **07-spring-boot-spring-mvc-crud**: Full CRUD operations with Spring MVC and Thymeleaf
- **08-spring-boot-spring-mvc-security**: Security for web applications
- **09-spring-boot-jpa-advanced-mappings**: Advanced JPA mappings (one-to-one, one-to-many, many-to-many)
- **10-spring-boot-aop**: Aspect-Oriented Programming concepts
- **11-appendix**: Additional resources and references

## Build System

- **Build Tool**: Maven
- **Java Version**: 17
- **Spring Boot Version**: 3.5.6
- **Package Structure**: `src/main/java` and `src/main/resources`
- **Base Package**: `com.luv2code.springboot.demo`

Each project has its own `pom.xml` with the Spring Boot parent POM. Some projects include the Maven wrapper (`mvnw`) for convenience.

## Common Commands

### Navigate to a specific project:
```bash
cd 04-spring-boot-rest-crud/01-spring-boot-rest-crud-hello-world
```

### Build the project:
```bash
./mvnw clean package
# or
mvn clean package
```

### Run the application:
```bash
./mvnw spring-boot:run
# or
mvn spring-boot:run
```

### Run a specific test:
```bash
./mvnw test -Dtest=ClassName
# or
mvn test -Dtest=ClassName
```

### Run all tests:
```bash
./mvnw test
# or
mvn test
```

### Skip tests during build:
```bash
./mvnw clean package -DskipTests
# or
mvn clean package -DskipTests
```

### Run from target directory (after build):
```bash
java -jar target/mycoolapp-0.0.1-SNAPSHOT.jar
```

## Project Architecture

Each Spring Boot project follows standard conventions:

```
project-root/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/luv2code/springboot/demo/
│   │   │       └── {project-name}/
│   │   │           └── {ProjectName}Application.java  # @SpringBootApplication main class
│   │   └── resources/
│   │       └── application.properties                 # Configuration
│   └── test/
│       └── java/
└── pom.xml
```

Common patterns across projects:
- Main class annotated with `@SpringBootApplication`
- REST controllers use `@RestController` for REST APIs
- Web controllers use `@Controller` with Thymeleaf views
- Data JPA repositories extend `JpaRepository`
- Service layer classes use `@Service`
- Data access objects use `@Repository`
- Configuration classes use `@Configuration`

## Key Dependencies by Section

- **Overview (01)**: spring-boot-starter-web, spring-boot-starter-actuator, spring-boot-devtools
- **REST CRUD (04-05)**: spring-boot-starter-web, spring-boot-starter-data-jpa, spring-boot-starter-security
- **Spring MVC (06-07)**: spring-boot-starter-web, spring-boot-starter-thymeleaf
- **Security (05, 08)**: spring-boot-starter-security (with BCrypt password encoding)
- **JPA Advanced (09)**: spring-boot-starter-data-jpa, hibernate-core
- **AOP (10)**: spring-boot-starter-aop, aspectjweaver

## Accessing Applications

- **REST APIs**: http://localhost:8080/api/endpoint
- **Web Applications**: http://localhost:8080
- **Actuator Endpoints**: http://localhost:8080/actuator (when enabled)
- **H2 Console**: http://localhost:8080/h2-console (when H2 database is used)

## Database Configuration

Most projects use H2 in-memory database by default (configured in `application.properties`). Example H2 console URL: `jdbc:h2:mem:testdb`

## Development Notes

- Each project is independent and can be run separately
- Projects demonstrate incremental learning - later projects build on earlier concepts
- Some projects include SQL scripts in the `spring-boot-employee-sql-script` directory
- All projects include comprehensive comments in the code
- Test classes follow the naming pattern `{ClassName}Test` and use JUnit 5