# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Baeldung Tutorials repository** - a massive collection of 200+ focused Java tutorials organized as a Maven multi-module project. Each module covers a single, well-defined area of development in the Java ecosystem, with heavy focus on Spring Framework (Spring, Spring Boot, Spring Security).

## Build System

### Maven Profiles

The project uses **Maven build profiles** to segregate modules by JDK version and test type:

| Profile | JDK Version | Test Type |
|---------|-------------|-----------|
| `default` | JDK 21 | Unit Tests only |
| `integration` | JDK 21 | Integration Tests only |
| `default-jdk17` | JDK 17 | Unit Tests only |
| `integration-jdk17` | JDK 17 | Integration Tests only |
| `default-jdk8` | JDK 8 | Unit Tests only |
| `integration-jdk8` | JDK 8 | Integration Tests only |
| `default-jdk22` | JDK 22 | Unit Tests only |
| `default-jdk23` | JDK 23 | Unit Tests only |
| `default-jdk24` | JDK 24 | Unit Tests only |
| `default-jdk25` | JDK 25 | Unit Tests only |
| `default-heavy` | JDK 17 | Unit Tests only (long-running projects) |
| `integration-heavy` | JDK 17 | Integration Tests only (long-running projects) |
| `parents` | N/A | Builds only parent modules |

## Common Commands

### Build Entire Repository

```bash
# Build with unit tests
mvn clean install -Pdefault,default-heavy

# Build with integration tests
mvn clean install -Pintegration,integration-heavy
```

### Build Specific Modules

```bash
# From module directory
cd spring-boot-modules/spring-boot-actuator
mvn clean install

# From root, targeting specific modules
mvn clean install --pl akka-modules,algorithms-modules -Pdefault
```

### Run Tests

```bash
# Unit tests (default profile or specific JDK)
mvn clean install -Pdefault
mvn clean install -Pdefault-jdk17
mvn clean install -Pdefault-jdk8

# Integration tests
mvn clean install -Pintegration
mvn clean install -Pintegration-jdk17
mvn clean install -Pintegration-jdk8
```

### Build Parent Modules First

If a module has a parent (e.g., `parent-boot-1`, `parent-spring-5`), build the parent first:

```bash
mvn clean install -Pparents
```

### Run Spring Boot Applications

```bash
cd <module-directory>
mvn spring-boot:run
```

## Module Structure

Each module follows standard Maven structure:
- `src/main/java/` - Production code
- `src/test/java/` - Test code

Test file naming conventions:
- `*UnitTest.java` - Unit tests
- `*IntegrationTest.java` or `*IntTest.java` - Integration tests
- `SpringContextTest.java` - Spring context tests
- `*LongRunningUnitTest.java` - Long-running unit tests
- `*ManualTest.java` - Manual tests
- `*LiveTest.java` - Live tests
- `*JdbcTest.java` - JDBC tests

## High-Level Architecture

### Organization by Technology

The repository is organized into major technology categories:

1. **Core Java** (`core-java-modules/`) - Java language features, JDK utilities
2. **Spring Framework** (`spring-*`, `spring-boot-*`) - Spring core, Boot, Security, etc.
3. **Persistence** (`persistence-modules/`) - JPA, Hibernate, Spring Data
4. **Libraries** (`libraries-*`) - Third-party library tutorials
5. **Web** (`web-modules/`) - Web frameworks, REST APIs
6. **Cloud** (`aws-*`, `gcp-*`, `azure-*`) - Cloud services
7. **Testing** (`testing-modules/`) - Testing frameworks and tools
8. **Messaging** (`messaging-modules/`) - Kafka, RabbitMQ, etc.

### Parent POMs

Several parent POMs exist for grouping related modules:
- `parent-boot-1`, `parent-boot-2`, `parent-boot-3`, `parent-boot-4` - Spring Boot versions
- `parent-spring-5`, `parent-spring-6`, `parent-spring-7` - Spring Framework versions

## IDE Usage

Import only the specific module you're working with - **do not import the entire repository**. Each module is self-contained and can be imported independently in Eclipse or IntelliJ.

## Key Development Notes

- The repository contains tutorials, not production code
- Many modules are standalone examples demonstrating specific Java/Spring concepts
- Some modules have dependencies on specific JDK versions (check the profile they belong to)
- Custom PMD rules are enforced (see `baeldung-pmd-rules.xml`)
- Logback is configured globally via `logback-config-global.xml`

## Disabled/Failing Modules

Some modules are in `default-disabled` or `integration-disabled` profiles due to:
- JDK compatibility issues
- External dependency requirements
- Known failures (referenced with JAVA-XXXXX issue numbers)

## Test Execution Behavior

**Default profiles** (e.g., `default`, `default-jdk17`) run:
- `SpringContextTest` (if present)
- All `*UnitTest.java` files

**Integration profiles** (e.g., `integration`, `integration-jdk17`) run:
- All `*IntegrationTest.java` files
- All `*IntTest.java` files

All profiles exclude:
- `*ManualTest.java`
- `*LiveTest.java`
- `*LongRunningUnitTest.java`
- `*JdbcTest.java`

## Build Tips

- Use `-Pdefault,default-heavy` to build everything with unit tests
- Use `--pl <module-name>` to build specific modules from root
- Always specify the correct JDK profile for your module
- Build parent modules first when needed using `-Pparents`