# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an educational codebase for learning Spring Security and OAuth2 with Spring Boot. It contains tutorial projects demonstrating various authentication and authorization patterns.

## Build Commands

All projects use Gradle with the wrapper:

```bash
# Build the project
./gradlew build

# Run the application
./gradlew bootRun

# Run tests
./gradlew test

# Run a specific test class
./gradlew test --tests "LearnSpringSecurityApplicationTests"

# Clean build artifacts
./gradlew clean

# Create executable jar
./gradlew bootJar
```

## Main Projects

### 71-spring-security
Spring Security tutorial demonstrating:
- **Basic Auth**: `BasicAuthSecurityConfiguration.java` - In-memory and JDBC-based user authentication with BCrypt password encoding
- **JWT**: `JwtSecurityConfiguration.java` - Token-based authentication using RSA key pairs (2048-bit), Nimbus JOSE library
- **H2 Database**: Embedded in-memory database for testing user storage

### 72-oauth
OAuth2 client configuration with Google provider
- Configure OAuth credentials in `application.properties`

### Angular Frontend
Located in `frontend/todo/`
```bash
npm install
npm start  # ng serve
```

## Key Technologies

- **Java 21** with Spring Boot 3.2.2
- **Gradle** (wrapper included)
- **Spring Security 6.x** using lambda-based DSL (`auth -> auth.xxx()`)
- **H2 Database** (embedded)
- **JUnit 5** (useJUnitPlatform())
- **Nimbus JOSE + JWT** library for JWT handling

## Architecture Notes

### Security Configuration Pattern (Spring Boot 3)
All security configurations use the modern lambda-based DSL and `@Bean`-based `SecurityFilterChain`:

```java
http.authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
    .httpBasic(Customizer.withDefaults())
    .csrf(csrf -> csrf.disable())
```

### JWT Implementation
- Keys generated programmatically at runtime via `KeyPairGenerator`
- RSA keys (2048-bit) created in `keyPair()` bean
- JWK Set exposed via `jwkSource()` bean
- Encoder uses `NimbusJwtEncoder`, decoder uses `NimbusJwtDecoder`

### Testing Users
Default test users (password is BCrypt encoded "dummy"):
- Username: `in28minutes`, Role: `USER`
- Username: `admin`, Roles: `ADMIN`, `USER`

### Package Structure
- Security configs in `{root-package}/basic/`, `{root-package}/jwt/`
- Resources/REST controllers in `{root-package}/resources/`
- OAuth app in `com.in28minutes.learnoauth`

## Documentation

Step-by-step guides are in project directories:
- `71-spring-security/Step*.md` - Progressive security implementations
- `99-reuse/01-spring-security.md` - Reusable configuration snippets
- `00-spring-boot-3-updates.md` - Spring Boot 3 migration notes