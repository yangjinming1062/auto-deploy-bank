# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Java Design Patterns** repository - a comprehensive collection of design pattern implementations in Java with 175+ pattern modules. Each module contains a complete, production-quality implementation of a specific design pattern with comprehensive documentation, real-world examples, and tests.

## Technology Stack

- **Language**: Java 21
- **Build Tool**: Maven (multi-module: 175+ modules)
- **Testing**: JUnit 5.11.4
- **Key Libraries**: Spring Boot 3.4.4, SLF4J, Mockito 5.14.2, Lombok 1.18.38, MongoDB 5.4.0
- **Code Quality**: Google Java Format (Spotless), SonarCloud, Checkstyle, JaCoCo

## Common Commands

```bash
# Build the entire project
./mvnw clean install

# Run all tests
./mvnw test

# Run tests with coverage
./mvnw clean verify

# Run a specific pattern module
cd singleton && ../mvnw clean install

# Format code
./mvnw spotless:check
./mvnw spotless:apply  # Apply formatting fixes

# Run SonarQube analysis
./mvnw clean verify org.sonarsource.scanner.maven:sonar-maven-plugin:sonar

# Install without running tests (useful for quick builds)
./mvnw clean install -DskipTests
```

## Project Structure

### Multi-Module Maven Architecture

The project uses a **multi-module Maven structure** with 175 pattern modules organized by category:

- **Behavioral** (38 patterns): Observer, Strategy, Command, State, etc.
- **Structural** (33 patterns): Adapter, Decorator, Facade, Proxy, etc.
- **Architectural** (23 patterns): MVC, Microservices, Event-Driven, etc.
- **Concurrency** (21 patterns): Actor, Promise, Reactor, etc.
- **Creational** (14 patterns): Singleton, Factory, Builder, etc.
- **Data Access** (11 patterns): Repository, DAO, etc.
- Plus others

### Pattern Module Structure

Each pattern follows a consistent structure:

```
pattern-name/
├── pom.xml                    # Module Maven configuration
├── README.md                  # Comprehensive documentation with real-world examples
├── src/
│   ├── main/java/com/iluwatar/pattern/
│   │   ├── App.java           # Entry point demonstrating the pattern
│   │   └── [pattern implementation classes]
│   └── test/java/com/iluwatar/pattern/
│       ├── AppTest.java       # Tests
│       └── [pattern-specific tests]
└── etc/                       # Optional: diagrams, resources
```

### Key Configuration Files

- **Root**: `pom.xml` (main Maven POM)
- **Formatting**: `.editorconfig`, `lombok.config`, `checkstyle-suppressions.xml`
- **License**: MIT License (automatically applied via maven-license-plugin)
- **CI/CD**: `.github/workflows/` (maven-ci.yml, maven-pr-builder.yml, presubmit.yml)

## Development Workflow

### Contributing

- Guidelines: See GitHub Wiki → https://github.com/iluwatar/java-design-patterns/wiki/01.-How-to-contribute
- PR Template: `.github/PULL_REQUEST_TEMPLATE.md`
- **Simple workflow**: Fork → Create feature branch → PR → Merge

### Code Quality Standards

- **Formatting**: Google Java Format enforced via Spotless plugin
- **Coverage**: Minimum 80% test coverage via JaCoCo
- **Static Analysis**: SonarCloud integration (runs in CI)
- **Checkstyle**: Configured in `checkstyle-suppressions.xml`
- **Lombok**: Configured for generated annotations and LOGGER fields

### Pattern Documentation Standards

Each pattern's README.md must include:
- Intent and description
- Real-world analogy
- Programmatic examples
- Applicability and trade-offs
- Related patterns
- References to classic texts (GoF, Fowler, etc.)

### CI/CD Pipeline

**Main Workflow** (`.github/workflows/maven-ci.yml`):
- Triggers on push to master
- JDK 21 (Temurin)
- Maven build with SonarCloud analysis
- Uses Xvfb for tests requiring display
- Caches Maven repository and Sonar packages

## Codebase Characteristics

### Self-Contained Modules

Each pattern module is **completely independent**:
- Own `pom.xml` with specific dependencies
- Own tests and test dependencies
- Own documentation
- Can be built independently via `mvnw clean install`

### Localization

The project is **highly internationalized** with 20 language translations available in `/localization/`:
- Arabic, Bengali, Danish, German, Greek, Spanish, Persian, French, Hindi, Indonesian, Italian, Japanese, Korean, Marathi, Nepali, Portuguese, Russian, Sinhala, Turkish, Urdu

### Test Patterns

Each module includes comprehensive tests:
- `AppTest.java` - Tests the main entry point
- Pattern-specific test classes for complex patterns
- Mockito for mocking
- Integration tests via Spring Boot Test where applicable

## Development Tips

### Working with Specific Patterns

```bash
# Build just one pattern
cd adapter && ../mvnw clean test

# View a specific pattern's documentation
cat singleton/README.md

# Run pattern-specific tests
cd singleton && ../mvnw test
```

### Code Quality Checks

```bash
# Check formatting without fixing
./mvnw spotless:check

# Fix formatting
./mvnw spotless:apply

# Run full code quality checks
./mvnw clean verify
```

### Docker Support

Some patterns (e.g., `caching/`) include `docker-compose.yml` for testing with external services:

```bash
cd caching
docker-compose up -d
# Run tests
docker-compose down
```

## Important Notes

1. **License Headers**: Automatically applied/verified via maven-license-plugin
2. **No `.cursorrules` or Copilot instructions**: None found in repository
3. **Lombok Configuration**: Pre-configured in `lombok.config` for consistency
4. **EditorConfig**: Ensure IDE respects `.editorconfig` for formatting consistency
5. **Maven Wrapper**: Always use `./mvnw` instead of `mvn` to ensure version consistency
6. **No Single Entry Point**: This is a library/reference project, not an application
7. **Focus on Examples**: Each pattern's `App.java` is the primary demonstration

## Project Stats

- **387 contributors** (see `.all-contributorsrc`)
- **175+ pattern modules**
- **Active since 2014**
- **20 language translations**
- **MIT License**

This repository serves as both an educational resource and a production-ready reference for implementing design patterns in enterprise Java applications.