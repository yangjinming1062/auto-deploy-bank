# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a monorepo containing code samples from www.opencodez.com. Each top-level directory is an independent project demonstrating a specific technology or integration pattern. Projects are not interconnected and can be developed separately.

## Build Commands

### Java Projects (Maven)

Most Java projects include the Maven wrapper. From a project directory:

```bash
# Build the project
./mvnw clean install

# Build without running tests
./mvnw clean install -DskipTests

# Run tests
./mvnw test

# Run a single test class
./mvnw test -Dtest=ClassName

# Run a single test method
./mvnw test -Dtest=ClassName#methodName

# Package as JAR/WAR
./mvnw package

# Run the application (Spring Boot)
./mvnw spring-boot:run
```

### Node.js Projects

```bash
# Install dependencies
npm install

# Start with nodemon (development)
npm start

# Run tests (note: most projects have placeholder tests)
npm test
```

## Project Categories

### Java/Spring Boot (Most Projects)
- **Spring Boot versions**: 1.4.0.RELEASE to 2.0.x.RELEASE
- **Java version**: 1.8
- **Common frameworks**: Spring Boot Starter, Spring Data JPA, Spring Cloud (for microservices)
- **Databases**: MySQL, H2 (for testing)
- **Build output**: JAR (most) or WAR (demo project)

### Node.js Projects
- **node-rest-api**: Express.js REST API with MySQL
- **node-web-server**: Basic web server
- **demo**: Express.js with database integration

### Other
- **Python**: keras-text-classification (Keras text classification)
- **Oracle**: Oracle job scheduler scripts

## Architecture Patterns

### Spring Boot REST API Pattern
Most projects follow a layered architecture:
- `src/main/java/com/opencodez/` - Main application
- `src/main/java/com/opencodez/controller/` - REST controllers
- `src/main/java/com/opencodez/repository/` - Spring Data JPA repositories
- `src/main/java/com/opencodez/model/` or `entity/` - JPA entities
- `src/main/java/com/opencodez/service/` - Business logic services
- `src/main/resources/` - Configuration files (application.properties/yml)

### Microservices (microservices/ directory)
Multi-module project with Eureka service discovery:
- `spring-discovery-server/` - Eureka Server
- `spring-client-employee-service/` - Sample microservice
- `spring-client-employer-service/` - Sample microservice
- Uses Spring Cloud Netflix (Eureka, Ribbon, Feign)

## Dependencies by Project Type

### Typical Maven Dependencies
- Spring Boot starters (web, data-jpa, test, security, etc.)
- MySQL connector
- c3p0 connection pooling
- Tomcat/Jasper for JSP support
- Spring Cloud Netflix for microservices

### Typical Node.js Dependencies
- express
- mysql
- body-parser
- cors
- babel-* for ES6 transpilation

## Configuration

Spring Boot projects typically use:
- `src/main/resources/application.properties` or `application.yml`
- External database configuration via properties

Node.js projects use:
- `server.js` or `app.js` for configuration
- `schema.sql` for database schema