# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Spring Initializr is a JVM-based project generator that provides an extensible API to generate projects with implementations for Java, Kotlin, and Groovy, supporting both Maven and Gradle build systems.

## Common Commands

### Building the Project
```bash
# Build all modules
./mvnw clean install

# Build including documentation (requires 'full' profile)
./mvnw clean install -Pfull

# Skip tests
./mvnw clean install -DskipTests
```

### Code Quality and Formatting
```bash
# Format code using Spring JavaFormat
./mvnw io.spring.javaformat:spring-javaformat-maven-plugin:apply

# Run validation (checkstyle + nohttp + spring-javaformat)
./mvnw validate

# Run only checkstyle validation
./mvnw checkstyle:check

# Format, validate, and run tests
./mvnw clean verify
```

### Testing
```bash
# Run all tests
./mvnw test

# Run tests for a specific module
./mvnw test -pl initializr-generator

# Run a single test class
./mvnw test -Dtest=ProjectGeneratorTests

# Run tests with more verbose output
./mvnw test -X
```

### Running the Service
```bash
# Run the sample service application
cd initializr-service-sample
../mvnw spring-boot:run

# Or from the root with module selection
./mvnw spring-boot:run -pl initializr-service-sample
```

## Project Structure

This is a multi-module Maven project with the following architecture:

### Module Overview
- **initializr-web**: Spring Boot web application exposing REST endpoints for project generation
- **initializr-generator**: Core project generation library
- **initializr-metadata**: Metadata infrastructure defining project capabilities and options
- **initializr-generator-spring**: Spring Boot-specific conventions and templates
- **initializr-generator-test**: Test infrastructure for project generation
- **initializr-actuator**: Actuator endpoints for statistics and diagnostics
- **initializr-version-resolver**: Extracts version numbers from POM files
- **initializr-service-sample**: Sample custom service implementation
- **initializr-bom**: Bill of Materials for dependency management
- **initializr-parent**: Parent POM with shared configuration
- **initializr-docs**: Documentation

### Key Architectural Components

#### Web Layer (`initializr-web`)
The web module provides Spring MVC controllers that expose the project generation API:
- `ProjectGenerationController`: Base controller for project generation endpoints
- `DefaultProjectGenerationController`: Default implementation handling project creation requests
- `ProjectMetadataController`: Serves metadata about available project options
- `CommandLineMetadataController`: Command-line interface support

The web layer uses `ProjectRequest` objects to capture user input and converts them to `ProjectDescription` for the generator.

#### Generation Layer (`initializr-generator`)
The generator module is the core of the system:
- `ProjectGenerator`: Main entry point that creates a `ProjectGenerationContext` with all available configurations
- `ProjectDescription`: Immutable description of the project to generate
- `MutableProjectDescription`: Builder-style class for constructing project descriptions
- `ProjectGenerationContext`: Spring `ApplicationContext` specific to each generated project
- `ProjectGenerationConfiguration`: Spring `@Configuration` classes that contribute to project generation

The generator uses Spring's `SpringFactoriesLoader` mechanism to discover and load `ProjectGenerationConfiguration` classes dynamically. Each configuration can contribute beans, templates, or other resources to the generated project.

#### Metadata Layer (`initializr-metadata`)
Defines the model for available project options:
- `InitializrMetadata`: Root metadata object containing all capabilities
- `DependenciesCapability`, `TypeCapability`, `JavaVersionCapability`, etc.: Define available options for each project aspect
- `Dependency`, `Repository`, `Bom`: Core metadata entities

#### Build System Support
The generator supports both Maven and Gradle:
- **Maven**: `MavenBuildSystem`, `MavenPom`, `MavenBuildWriter`
- **Gradle**: `GradleBuildSystem`, `GradleBuild`, `GradleBuildWriter`
  - Both Kotlin DSL and Groovy DSL variants

### Configuration

#### Service Configuration (`initializr-service-sample`)
Custom services are configured via `application.yaml` with the `initializr` key. The sample shows:
- Supported languages (Java, Kotlin, Groovy)
- Java versions
- Dependency groups
- Build tool types (Maven, Gradle)
- Packaging options

Example configuration structure:
```yaml
initializr:
  env:
    kotlin:
      default-version: "1.9.22"
  group-id:
    value: org.acme
  dependencies:
    - name: Web
      content:
        - name: Web
          id: web
  languages:
    - name: Java
      id: java
      default: true
```

## Development Conventions

### Code Style
- Code is automatically formatted using [Spring JavaFormat](https://github.com/spring-io/spring-javaformat/)
- Checkstyle rules are enforced via `src/checkstyle/checkstyle.xml`
- No HTTP checkstyle rules in `src/checkstyle/nohttp-checkstyle.xml` ensure no plain HTTP URLs
- All source files must have ASF license headers
- Javadoc is required for all public classes with at least `@author` tag

### Testing
- JUnit Jupiter is used for testing
- AssertJ for assertions
- Mockito for mocking
- The `initializr-generator-test` module provides test utilities for validating generated projects
- Tests are integration-focused, validating the complete generation process

### Dependency Management
- BOM (Bill of Materials) is provided in `initializr-bom` module
- Dependencies are managed through the parent POM
- The project uses Maven wrapper (`./mvnw`) - no local Maven installation required

### Git Commit Messages
Follow the standard format described in [A Note About Git Commit Messages](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html):
- First line is 50 characters or less
- Followed by a blank line
- Detailed description wrapped at 72 characters
- Include `Fixes gh-XXXX` for issue fixes

### License and DCO
All commits must include a "Signed-off-by" trailer indicating agreement to the Developer Certificate of Origin. This is a DCO (Developer Certificate of Origin) process, not a CLA (Contributor License Agreement).

## Key Dependencies

The project heavily uses:
- Spring Framework (Spring MVC, Spring Context, Spring HATEOAS)
- Spring Boot (auto-configuration, Actuator)
- Spring JavaFormat (code formatting)
- Checkstyle (code conventions)
- Apache Commons (Compress, Text)
- JMustache (template rendering)
- JUnit Jupiter, AssertJ, Mockito (testing)

## How Project Generation Works

1. **Request**: Web layer receives a `ProjectRequest` with user preferences
2. **Conversion**: Request is converted to a `ProjectDescription`
3. **Context Creation**: `ProjectGenerator` creates a dedicated `ProjectGenerationContext` for this project
4. **Configuration Discovery**: Spring `SpringFactoriesLoader` discovers all `ProjectGenerationConfiguration` classes on the classpath
5. **Bean Registration**: Each configuration contributes beans to the context
6. **Generation**: `ProjectAssetGenerator` instances query the context and generate project assets
7. **Output**: Project structure is written to disk as ZIP/TAR archive

This architecture allows for highly customizable generation with clear separation of concerns between metadata, web, generation logic, and build system support.