# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spring Initializr is an extensible API that generates JVM-based projects. It provides:
- Language generation for Java, Kotlin, and Groovy
- Build system abstraction for Apache Maven and Gradle
- `.gitignore` support
- Hook-points for custom resource generation

The production instance runs at https://start.spring.io.

## Prerequisites

- **Java 17** (configured via `.sdkmanrc` as `java=17.0.17-librca`)
- **Maven Wrapper** (use `./mvnw` commands, not system Maven)

## Common Commands

### Building and Testing

```bash
# Clean install all modules
./mvnw clean install

# Build with documentation (enables 'full' profile)
./mvnw clean install -Pfull

# Run validation (checkstyle, code formatting)
./mvnw validate

# Format code using Spring JavaFormat
./mvnw io.spring.javaformat:spring-javaformat-maven-plugin:apply

# Run a specific test
./mvnw test -pl initializr-generator -Dtest=GradleTaskTests

# Run tests for a specific module only
./mvnw test -pl initializr-web

# Skip tests during build
./mvnw clean install -DskipTests
```

### IDE Integration

- **Eclipse/IntelliJ**: Install Spring JavaFormat plugin for consistent code formatting
- The project includes m2e lifecycle mapping for Eclipse in `pom.xml` profiles

## Code Architecture

### Module Structure

1. **initializr-generator** (`initializr-generator/`): Core project generation library
   - `buildsystem/`: Build system abstractions (Maven, Gradle)
     - `maven/`: Maven build configuration and writing
     - `gradle/`: Gradle build configuration and writing
   - `language/`: Support for Java, Kotlin, Groovy
   - `project/`: Project description and generation logic
   - `packaging/`: Project packaging options
   - `io/`: File I/O utilities for project generation

2. **initializr-web** (`initializr-web/`): Web endpoints and Spring Boot integration
   - `controller/`: REST controllers
     - `ProjectGenerationController.java`: Main endpoint for project generation (line 1)
     - `ProjectMetadataController.java`: Metadata endpoint
     - `AbstractMetadataController.java`: Base metadata controller
   - `project/`: Request/response models and conversion
     - `ProjectRequest.java`: Web project request model
     - `ProjectGenerationInvoker.java`: Invokes project generation
   - `support/`: Supporting utilities and metadata providers
   - `autoconfigure/`: Spring Boot auto-configuration

3. **initializr-metadata** (`initializr-metadata/`): Metadata infrastructure
   - Defines capabilities (dependencies, types, versions)
   - `Dependency.java`: Dependency definition model
   - `InitializrConfiguration.java`: Overall configuration
   - `TypeCapability.java`: Project types (maven-project, gradle-project, etc.)

4. **initializr-generator-spring** (`initializr-generator-spring/`): Spring Boot conventions
   - Implements Spring-specific project structure and conventions
   - Used for typical Spring Boot project generation

5. **initializr-service-sample** (`initializr-service-sample/`): Sample implementation
   - `ServiceApplication.java`: Example Spring Boot application using Initializr

6. **Other modules**:
   - `initializr-generator-test`: Test infrastructure for project generation
   - `initializr-actuator`: Metrics and statistics endpoints
   - `initializr-bom`: Bill of Materials for dependency management
   - `initializr-version-resolver`: Extract version numbers from POM files
   - `initializr-docs`: Reference documentation
   - `initializr-parent`: Parent POM with common configuration

### Key Components

#### Project Generation Flow
1. **Web Layer** (`initializr-web`): Controller receives project request
2. **Request Processing**: `ProjectRequest` → `ProjectDescription` conversion
3. **Generation**: `ProjectGenerationInvoker` uses generator modules
4. **Build System**: Abstracted build system (Maven/Gradle) creates project files
5. **Output**: Archives (zip/tar.gz) returned to client

#### Build System Abstraction
- **BuildSystem** interface in `initializr-generator/buildsystem/`
- Implementations: `MavenBuildSystem`, `GradleBuildSystem`
- Writers handle file generation: `MavenBuildWriter`, `GradleBuildWriter`

## Development Conventions

### Code Style
- **Spring JavaFormat** is enforced via Maven plugin
- **Checkstyle** rules defined in `src/checkstyle/checkstyle.xml`
- All new Java files require:
  - ASF license header
  - Class-level Javadoc with `@author` tag

### Checkstyle
- Configuration: `src/checkstyle/checkstyle.xml`
- Suppressions: `src/checkstyle/checkstyle-suppressions.xml`
- NoHTTP checks: `src/checkstyle/nohttp-checkstyle.xml`
- Run `./mvnw validate` to check compliance

### Git Workflow
- All commits must include **Signed-off-by** trailer (Developer Certificate of Origin)
- Follow commit message conventions from https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
- Fix issues with `Fixes gh-XXXX` at end of commit message

## Configuration

### Maven Profiles
- **default**: Enabled by default, includes formatting and checkstyle
- **full**: Includes documentation generation
- **m2e**: Eclipse m2e lifecycle mapping

### Version Management
- Versions managed in root `pom.xml` via `${revision}` property
- Current version: `0.22.1-SNAPSHOT`

## Testing

### Test Structure
- Unit tests in each module's `src/test/java/`
- Integration tests in `initializr-web/src/test/java/`
- Full-stack integration tests in `AbstractFullStackInitializrIntegrationTests.java`

### Running Tests
```bash
# All tests
./mvnw test

# Specific module
./mvnw test -pl initializr-generator

# Specific test class
./mvnw test -pl initializr-generator -Dtest=GradleTaskTests

# Run with test logs
./mvnw test -pl initializr-web -Dtest=ProjectGenerationControllerIntegrationTests
```

## Documentation

- **README.adoc**: Project overview and getting started
- **CONTRIBUTING.adoc**: Contribution guidelines and development process
- **CODE_OF_CONDUCT.adoc**: Code of conduct
- Reference documentation generated in `initializr-docs` module
- Online docs: https://docs.spring.io/initializr/docs/current-SNAPSHOT/reference

## CI/CD

- GitHub Actions workflow: `.github/workflows/build.yml`
- Dependabot configuration: `.github/dependabot.yml`
- DCO (Developer Certificate of Origin) enforcement: `.github/dco.yml`