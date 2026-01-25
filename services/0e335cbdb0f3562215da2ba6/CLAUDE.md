# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the source code for **Pro Spring 5** (Apress, 2017) - a collection of standalone Spring Framework examples organized by chapter. Each subdirectory contains multiple modules demonstrating specific Spring features.

## Build Commands

```bash
# Full build with tests
gradle clean build

# Build without tests
gradle build -x test

# Build and copy dependencies to build/libs
gradle clean build copyDependencies
```

## Requirements

- **Java 8** minimum
- **Gradle 5.x** recommended ( AspectJ plugin in chapter05:aspectj-aspects requires Gradle 4.0+)

## Project Structure

- `chapterXX/` - Directory per book chapter (02-18)
- `chapterXX:module-name/` - Individual Gradle subprojects
- Each module is self-contained with its own `build.gradle` and source code

## Dependency Management

Central version definitions are in `build.gradle`. Declare dependencies in module `build.gradle` using these shared versions:

```groovy
dependencies {
    compile project(':chapter03:constructor-injection')
    testCompile spring.test
    testCompile testing.junit
}
```

Key dependency groups defined in root `build.gradle`:
- `spring` - Spring Framework modules (context, tx, jdbc, orm, etc.)
- `boot` - Spring Boot starters (web, data-jpa, security, etc.)
- `hibernate` - Hibernate/ORM libraries
- `testing` - JUnit, Mockito, EasyMock, DBUnit
- `db` - Database drivers (MySQL, H2, Derby, etc.)

## Common Patterns

Each example module typically has:
- `src/main/java/com/apress/prospring5/ch{X}/` - Java sources
- `src/main/resources/spring/` - Spring XML configuration files
- `src/main/resources/logback.xml` - Logging configuration
- `src/test/java/` - Test classes using JUnit 4

Run individual test classes:
```bash
gradle :chapter03:collections:test --tests "*CollectionInjection"
```