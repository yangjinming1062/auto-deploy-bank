# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Build and install all modules
./mvnw install

# Build with skip tests
./mvnw install -DskipTests

# Run only unit tests (integration tests excluded by default)
./mvnw test

# Run a specific test class
./mvnw test -Dtest=ClassName

# Run integration tests
./mvnw verify

# Build documentation (Antora)
./mvnw antora -pl spring-shell-docs
```

## Project Overview

Spring Shell is a Spring-powered framework for building CLI applications. The project is a multi-module Maven build requiring Java 17.

### Core Modules

- **spring-shell-core**: Core interfaces and abstractions. Contains the `@Command`, `@Option`, `@Argument`, and `@EnableCommand` annotations.
- **spring-shell-jline**: JLine 3.x integration providing interactive terminal capabilities (input parsing, styling, history, completion).
- **spring-shell-autoconfigure**: Spring Boot auto-configuration. Configures shell runners, command registration, and UI components.
- **spring-shell-starters**: Spring Boot starters. Use `spring-shell-starter` for the main dependency, or specialized starters (`spring-shell-starter-jansi`, `spring-shell-starter-jna`, etc.).
- **spring-shell-test** / **spring-shell-test-autoconfigure**: Testing utilities including `ShellTester` for interactive shell testing.
- **spring-shell-docs**: Antora-based documentation.
- **spring-shell-samples**: Example applications demonstrating usage patterns.

### Key APIs

**Command Registration:**
- `@EnableCommand({Class1.class, Class2.class})` - Enable command scanning for annotated classes
- `@Command(name = "foo", description = "...", group = "...")` - Annotate methods as commands
- `@Option(shortName = 'n', longName = "name", required = true, defaultValue = "...")` - Options/flags
- `@Argument(index = 0, defaultValue = "...")` - Positional arguments

**Customization:**
- Implement `CommandRegistryCustomizer` to programmatically modify `CommandRegistry` beans
- Implement `CommandAvailability` to dynamically control command availability

## Development Notes

- Uses Spring Java Format plugin for code formatting (enforced during `validate` phase)
- Code quality: ErrorProne and NullAway annotations are configured in the compiler
- All commits require a Signed-off-by trailer (Developer Certificate of Origin)
- Main branch contains work for 4.0.0 (currently 4.0.0-SNAPSHOT)

## Dependency Management

Managed versions in root pom.xml:
- Spring Boot 4.0.0
- Spring Framework 7.0.1
- JLine 3.30.6
- Java 17 target