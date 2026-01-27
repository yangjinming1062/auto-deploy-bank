# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Soot - A Java analysis framework built on the Soot bytecode optimization framework. This is a Java 8+ project for analyzing and transforming Java bytecode.

## Build Commands

```bash
# Compile the project
mvn compile

# Run all tests
mvn test

# Run a single test class
mvn test -Dtest=AppTest

# Run checkstyle validation
mvn checkstyle:check

# Full build (skip tests)
mvn clean package -DskipTests

# Full build with verification
mvn clean verify
```

## Architecture

This is a Java Maven project using the Soot framework for bytecode analysis:

- **Main Entry Point**: `de.upb.App` - Initializes Soot framework with options for whole-program analysis
- **Port**: 40932 (exposed in Docker)
- **Soot Configuration**: Prepends classpath, whole-program mode, line numbers preserved

The project is currently minimal with a single main application class that initializes Soot for future bytecode analysis capabilities.

## Code Style

- Google Java Style guide enforced via Checkstyle
- Max line length: 100 characters
- Checkstyle configuration: `codingstyle/google_checkstyle.xml`
- Custom formatter: `codingstyle/soot_reloaded_formatter.xml`
- Import order: `codingstyle/soot_reloaded_import.importorder`
- Checkstyle is configured to not fail the build (`failOnViolation=false`)

## Dependencies

- **Soot** (4.0.0) - Java bytecode analysis framework
- **SLF4J** (1.7.25) - Logging facade
- **Guava** (24.0-jre) - Google utilities
- **Apache Commons Lang** (3.5) - Language utilities
- **JUnit 4** + **PowerMock** - Testing framework

## Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# The service exposes port 40932
```

## Key Files

- `pom.xml` - Maven configuration with checkstyle and shade plugins
- `Dockerfile` - Multi-stage build (Maven builder + JRE 17 runtime)
- `docker-compose.yaml` - Service configuration with resource limits (2 CPU, 4GB memory)