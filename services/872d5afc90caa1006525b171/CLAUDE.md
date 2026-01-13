# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build System

This project uses Gradle 9.2.1 with the Gradle wrapper. All commands should use `./gradlew` from the project root.

### JDK Requirements

- **main branch**: JDK 25 (use Bellsoft Liberica, HotSpot JVM)
- **3.* branches**: JDK 17
- **Earlier branches**: JDK 1.8

SDKMAN! is configured (`.sdkmanrc`) to provision the recommended JDK. Use `sdk env install` to set up your environment.

### Common Build Commands

```bash
# Build everything
./gradlew build

# Run tests only (unit, integration, smoke, and system tests)
./gradlew test

# Run only unit tests
./gradlew :core:spring-boot:test

# Run a specific test class
./gradlew :core:spring-boot:test --tests "*ApplicationTests"

# Run integration tests
./gradlew :integration-test:spring-boot-integration-tests:integrationTest

# Run smoke tests
./gradlew :smoke-test:spring-boot-smoke-test-simple:bootTest

# Format code (Spring JavaFormat)
./gradlew format

# Run checkstyle
./gradlew checkstyleMain checkstyleTest

# Run all verification (tests + checkstyle)
./gradlew check

# Build documentation
./gradlew :core:spring-boot-docs:asciidoc

# Publish to local Maven cache
./gradlew publishToMavenLocal
```

## Project Architecture

### Module Structure

The project is organized into several key areas:

1. **platform/** - Dependency management
   - `spring-boot-dependencies` - Bill of Materials (BOM) defining all dependency versions
   - `spring-boot-internal-dependencies` - Internal dependency constraints

2. **core/** - Core Spring Boot modules
   - `spring-boot` - Main framework
   - `spring-boot-autoconfigure` - Auto-configuration engine
   - `spring-boot-autoconfigure-processor` - Annotation processor for auto-configuration metadata
   - `spring-boot-test` - Testing support
   - `spring-boot-test-autoconfigure` - Testing auto-configuration
   - `spring-boot-testcontainers` - Testcontainers integration
   - `spring-boot-docker-compose` - Docker Compose support
   - `spring-boot-properties-migrator` - Configuration properties migration tool

3. **module/** - Feature modules (100+ modules)
   - Integration modules for data, web, security, cloud, messaging, etc.
   - Each feature typically has its own module with `-autoconfigure` companion
   - Examples: `spring-boot-actuator`, `spring-boot-data-jpa`, `spring-boot-webflux`

4. **build-plugin/** - Build plugins
   - `spring-boot-gradle-plugin` - Official Gradle plugin
   - `spring-boot-maven-plugin` - Official Maven plugin
   - `spring-boot-antlib` - Ant tasks

5. **test-support/** - Test utilities
   - Shared test support classes and fixtures

6. **integration-test/** - Integration tests
   - Full integration tests that require Docker (Testcontainers)

7. **smoke-test/** - Smoke tests
   - End-to-end tests for specific features using real Spring Boot applications

8. **system-test/** - System tests
   - Highest-level tests for deployment and image building

9. **cli/** - Spring Boot CLI tool

10. **buildSrc/** - Custom Gradle plugins and build logic
    - Defines conventions applied to all subprojects
    - Custom plugins for auto-configuration, testing, documentation, etc.

### Key Build Concepts

- **Conventions Plugin** (`buildSrc/src/main/java/org/springframework/boot/build/ConventionsPlugin.java`):
  Applies Java, Maven publishing, Kotlin, Eclipse, and other conventions to all projects.

- **Architecture Plugin**: Enforces architectural constraints (prevents circular dependencies, ensures proper layering)

- **Auto-Configuration Plugin**: Processes `@ConfigurationProperties` and generates metadata

- **Test Plugins**: Different test types (unit, integration, smoke, system) each have their own Gradle plugin

## Development Workflow

### Code Style and Quality

- Code formatting: Spring JavaFormat plugin (applied automatically via conventions)
- Checkstyle: Configured via `buildSrc`, run with `./gradlew checkstyleMain checkstyleTest`
- Architecture checks: Automatically enforced by the ArchitecturePlugin
- All new Java files must include ASF license header
- All new Java files should have Javadoc with `@author` tag

### Working with Auto-Configuration

Auto-configuration classes are processed at build time:
- Location: `core/spring-boot-autoconfigure/src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`
- Metadata generation: `@ConfigurationProperties` classes generate metadata in `spring-boot-autoconfigure-processor`
- Do not manually edit the `AutoConfiguration.imports` file - it's auto-generated

### Testing

This project has multiple test layers:

1. **Unit tests** - Standard JUnit tests in each module
2. **Integration tests** (`integration-test/`) - Require Docker, test full functionality
3. **Smoke tests** (`smoke-test/`) - Test complete applications end-to-end
4. **System tests** (`system-test/`) - Test deployment and packaging

Tests using Docker/Testcontainers will be automatically skipped if Docker is not available. If running Docker tests, ensure at least 20GB disk space is available.

### Running Specific Test Types

```bash
# Run all tests in a specific module
./gradlew :module:spring-boot-actuator:test

# Run smoke tests for a specific feature
./gradlew :smoke-test:spring-boot-smoke-test-actuator:bootTest

# Run integration tests with Docker
./gradlew :integration-test:spring-boot-actuator-integration-tests:integrationTest

# Run a specific test method
./gradlew :core:spring-boot:test --tests "*.ApplicationTests.shouldLoadCustomBanner"
```

## IDE Setup

### Eclipse

Use the Eclipse Installer with the setup file in `/eclipse/spring-boot-project.setup`.

Or manually:
1. Install Buildship plugin
2. Install Spring JavaFormat plugin
3. Import as "Gradle → Existing Gradle Project"

### IntelliJ IDEA

1. Open the project by selecting the root `build.gradle` file
2. Or use "Project from Version Control" with the GitHub URL
3. The project includes `.idea/` directory with code style and copyright settings

### Windows Git Configuration

When cloning on Windows, set Git config to handle long paths:
```bash
git config --global core.longPaths true
```

## Contributing Guidelines

- All commits must include a "Signed-off-by" trailer (Developer Certificate of Origin)
- Follow commit message conventions: https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
- Run `./gradlew check` before committing (runs tests + checkstyle)
- If modifying buildSrc, fix format violations with `./gradlew -p buildSrc format`
- Add yourself as `@author` in modified Java files
- Unset `SPRING_PROFILES_ACTIVE` before running tests if set in environment

## Important Files

- `gradle.properties` - Version numbers and build configuration
- `settings.gradle` - Included modules and plugin management
- `buildSrc/` - Custom Gradle plugins and conventions
- `CONTRIBUTING.adoc` - Detailed contribution guidelines
- `.sdkmanrc` - SDKMAN! configuration for JDK versions
