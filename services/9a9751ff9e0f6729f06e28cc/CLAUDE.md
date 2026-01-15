# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **multi-module Maven parent project** containing 80+ independent blog tutorial code examples from [rieckpil.de](https://rieckpil.de/). Most tutorials demonstrate Spring Boot testing, Java/Jakarta EE, and cloud integrations (AWS, Azure).

## Common Commands

```bash
# Build and test all parent modules (Spring Boot projects)
./mvnw verify -B

# Apply Spotless code formatting
./mvnw spotless:apply -B

# Run all tests with verbose output
./mvnw verify -C -B

# Run a single module
cd spring-boot-datajpatest && ../mvnw verify -B

# Run a single test class
./mvnw test -Dtest=BookRepositoryTest -B
```

## Project Structure

- **Root `pom.xml`**: Parent POM with 80+ modules defined
- **Module structure**: Each tutorial is an independent module in its own directory
- **Build scripts**: `buildJdk{8,11,17}Projects.sh` build non-parent projects
- **Spotless**: Google Java Format style enforced (configured in `spotless.importorder`)
- **Testing conventions**:
  - Unit tests: `*Test.java` (run with `maven-surefire-plugin`)
  - Integration tests: `*IT.java` or `*WT.java` (run with `maven-failsafe-plugin`)

## Key Dependencies (Managed at Parent Level)

- Spring Boot 3.3.0
- Java 21
- Testcontainers BOM
- Spotless 2.43.0

## Development Notes

- Each module has its own `pom.xml` inheriting from the parent
- React/TypeScript frontends exist in: `guide-to-jakarta-ee-with-react-and-postgresql/frontend`, `jakarta-ee-react-file-handling/src/main/frontend`, `microprofile-jwt-keycloak-auth/frontend`, etc.
- Some projects use Gradle instead of Maven (see `kotlin-javascript-transpiling-gradle`)
- Renovate is configured to auto-update Maven and Gradle dependencies (disabled for npm)