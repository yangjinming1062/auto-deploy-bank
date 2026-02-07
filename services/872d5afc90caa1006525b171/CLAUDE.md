# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Build all modules without running tests
./gradlew publishToMavenLocal

# Full build with all tests
./gradlew build

# Run verification (tests + checkstyle)
./gradlew check

# Format code using Spring JavaFormat
./gradlew format

# Check code format violations
./gradlew checkstyleMain checkstyleTest

# Run tests for a specific project
./gradlew :core:spring-boot:test

# Run a single test class
./gradlew :core:spring-boot:test --tests "org.springframework.boot.env.EnvironmentPostProcessorTests"

# Run Docker integration tests (requires Docker)
./gradlew :spring-boot-gradle-plugin:dockerTest
```

**Requirements:** JDK 17 minimum, JDK 25.0.2+ recommended. Uses Gradle wrapper. The build uses STABLE_CONFIGURATION_CACHE.

## Project Structure

This is a multi-module Gradle build for Spring Boot. The project is organized into several major categories:

| Directory | Purpose |
|-----------|---------|
| `platform/` | BOM (Bill of Materials) dependency management - source of truth for versions |
| `core/` | Core framework: spring-boot, spring-boot-autoconfigure, test infrastructure |
| `module/` | Feature modules with auto-configuration AND library dependencies (e.g., spring-boot-data-jpa) |
| `starter/` | Dependency-less starters that aggregate modules (e.g., spring-boot-starter-web) |
| `loader/` | Custom class loaders and JAR tools including the jarmode-tools |
| `build-plugin/` | Gradle and Maven plugins for building Spring Boot applications |
| `cli/` | Spring Boot CLI command-line tool |
| `integration-test/` | Large-scale integration tests |
| `smoke-test/` | End-to-end application smoke tests |
| `system-test/` | Deployment and container image system tests |
| `configuration-metadata/` | Configuration processor and metadata generation |
| `documentation/` | Reference documentation and actuator docs |
| `buildpack/` | Cloud Native Buildpack support |
| `buildSrc/` | Build conventions and custom Gradle plugins |

**Version management:** All dependency versions are defined in `gradle.properties` and consumed via `platform/spring-boot-dependencies`.

**Gradle project naming:** Projects use the pattern `group:artifact` (e.g., `:module:spring-boot-web`, `:starter:spring-boot-starter`). Use `./gradlew projects` to list all available projects.

## Architecture Patterns

### Auto-Configuration
Auto-configuration classes are in `core/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/` organized by feature (e.g., `jdbc/`, `web/`, `data/`). Each auto-configuration:
- Uses `@AutoConfiguration` annotation (Spring Boot 3.x pattern)
- Declares `@AutoConfigureBefore`/`@AutoConfigureAfter` for ordering
- References `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` for auto-discovery (not spring.factories in new code)

### Module vs Starter Pattern
**`module/`** projects contain both the actual library integration AND auto-configuration. Example: `module:spring-boot-data-jpa` includes Hibernate integration and JPA auto-configuration.

**`starter/`** projects are dependency-less aggregators that depend only on modules. Example: `starter:spring-boot-starter-web` depends on `module:spring-boot-web`, `module:spring-boot-autoconfigure-classic`, etc.

### Configuration Properties
Configuration properties classes use `@ConfigurationProperties` and are validated. Metadata is auto-generated in `spring-configuration-metadata.json` for IDE support.

## Code Conventions

- **Sign-offs**: All commits require a Signed-off-by trailer (DCO). Use `git commit -s` or add manually.
- **License headers**: Required on all source files (Apache 2.0)
- **Formatting**: Spring JavaFormat is enforced via `./gradlew format`
- **Assertions**: Use AssertJ (`assertThat*` methods), not JUnit assertions
- **Mocking**: Use BDDMockito (`given()` instead of `when()`)
- **Imports**: See `config/checkstyle/checkstyle.xml` and `config/checkstyle/import-control.xml` for restrictions
- **Javadoc**: Required on public classes with `@author` tag

## Testing

Tests follow conventions based on module type:
- **Test slices**: Use `@SpringBootTest` with sliced context via `@AutoConfigure*` annotations
- **Test support**: Projects in `test-support/` provide shared testing infrastructure
- **Docker tests**: Use Testcontainers via `spring-boot-docker-test-support`

## Key Dependencies

Versions are managed centrally in `gradle.properties`:
- Spring Framework: `${springFrameworkVersion}`
- Jackson: `${jackson2Version}`
- Kotlin: `${kotlinVersion}`