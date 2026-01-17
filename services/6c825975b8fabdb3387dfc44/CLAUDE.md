# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**COMSAT** (Concurrent Scalable Web Apps) is a Java library that integrates [Quasar fibers](http://puniverse.github.io/quasar/) with various web and enterprise technologies. The project implements a **fibers-per-request model** where traditional blocking I/O operations are converted to lightweight threads, allowing thousands of concurrent requests with minimal memory overhead.

## Common Development Commands

### Prerequisites
- Java 7 minimum (Java 8 required for some features)
- Gradle (use wrapper or install locally)

### Core Operations
```bash
# Install to local Maven repository (default task)
gradle install

# Build entire project (compile, test, package)
gradle build

# Run all tests
gradle test

# Run tests for specific module
gradle :comsat-servlet:test
cd comsat-servlet && gradle test

# Run single test class
gradle test --tests co.paralleluniverse.fibers.servlet.FiberHttpServletTest

# Run specific test method
gradle test --tests "*.FiberHttpServletTest.test*"

# Clean build artifacts
gradle clean

# Generate Javadoc for all modules
gradle javadoc

# Check for dependency updates
gradle dependencyUpdates

# Apply license headers
gradle licenseFormatMain
```

### Testing Strategy
- **JUnit 4.12** for all tests
- Use Java agent for Quasar bytecode instrumentation during tests
- Tests in `comsat-test-war` require additional server setup (Jetty/Tomcat/Undertow)
- CI tests run when `CI=true` environment variable is set: `CI=true gradle test`

## Architecture

### Multi-Module Structure
The project contains **24 core modules** plus **30+ Spring Boot sample applications**:

**Core Web Modules:**
- `comsat-actors-api` - Web Actors API (HTTP/SSE/WebSocket actors)
- `comsat-actors-netty`, `comsat-actors-servlet`, `comsat-actors-undertow` - Server implementations
- `comsat-servlet` - Servlet integration (fiber-per-request servlets)

**Framework Integrations:**
- `comsat-jersey-server` - JAX-RS (Jersey) integration
- `comsat-dropwizard` - Dropwizard framework integration
- `comsat-spring-webmvc` / `comsat-spring-boot` / `comsat-spring-security` - Spring ecosystem

**HTTP Clients:**
- `comsat-httpclient` - Apache HttpClient integration
- `comsat-okhttp`, `comsat-retrofit` - Modern HTTP clients

**Database:**
- `comsat-jdbc`, `comsat-jdbi`, `comsat-jooq` - JDBC-based integrations

**Other:**
- `comsat-mongodb-allanbank`, `comsat-kafka`, `comsat-shiro` - Third-party integrations
- `comsat-test-utils`, `comsat-test-war` - Testing infrastructure

### Key Technologies
- **Quasar Fibers**: Lightweight threads (`co.paralleluniverse:quasar-core:0.7.6`)
- **Build**: Gradle 2.x with multi-module setup
- **Web Servers**: Jetty 9.2.14, Tomcat 8.0.33, Undertow 1.3.19
- **Frameworks**: Jersey 2.22.2, Spring 4.2.5, Spring Boot 1.3.3, Dropwizard 0.9.2

### Build Configuration
- **Root `build.gradle`** (672 lines) defines:
  - Multi-module dependency management
  - Quasar instrumentation setup
  - Java agent configuration for tests
  - Javadoc with external links (Quasar, Servlet API, Jersey, Spring)
  - Maven publishing and artifact signing
- **Instrumentation**: Quasar automatically instruments bytecode to convert blocking operations to fibers
- **Test Setup**: `co.paralleluniverse:quasar-core:0.7.6:junit` added to test classpath

## Important Documentation

### Primary Sources
- **`README.md`** - Main project documentation with module dependencies table
- **`CONTRIBUTING.md`** - Branch strategy: `release` branch for bugfixes, `master` for features
- **`docs/`** directory - Jekyll-based documentation site
- **`NOTICE`** - Third-party license attributions

### Key Release Information
- Current version: **0.7.1-SNAPSHOT**
- Previous releases: 0.1.0 - 0.7.0 (documented in `docs/index.md`)
- Requires Contributor License Agreement for contributions

## CI/CD & Publishing

- **Travis CI** builds on Java 7 and Java 8
- Auto-deploys documentation to gh-pages
- **Maven Central** publishing via Sonatype OSSRH
- Source/Javadoc JARs generated automatically
- Artifact signing with GPG

## Sample Applications

Located in the `samples/` directory, the project includes **30+ Spring Boot sample applications** demonstrating:
- Different embedded containers (Tomcat, Jetty, Undertow)
- SSL configuration
- JPA integration
- Spring Security
- Various COMSAT modules in action

## Development Tips

- **Multi-container testing**: Modules like `comsat-servlet` run parameterized tests against Jetty, Tomcat, and Undertow
- **CI optimization**: Set `CI=true` for faster CI builds (runs only essential tests)
- **IDE support**: Gradle IntelliJ integration via `.gradle` files
- **Dependency management**: Uses Ben Manes Versions Plugin for update checking
- **License compliance**: Automated header checking/formatting required