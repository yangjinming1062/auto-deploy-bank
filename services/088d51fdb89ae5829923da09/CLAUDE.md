# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Build and test all modules
./gradlew test

# Run checkstyle and all tests
./gradlew check

# Build the entire project
./gradlew build

# Clean build artifacts
./gradlew clean

# Run tests for a specific module only
./gradlew :jgiven-core:test

# Generate HTML5 report from test results
./gradlew :jgiven-tests:jgivenHtml5Report

# Run a single test class
./gradlew :jgiven-core:test --tests "com.tngtech.jgiven.impl.ScenarioExecutorTest"
```

## Project Overview

JGiven is a BDD (Behavior-Driven Development) testing framework for Java that allows writing scenarios in plain Java using a fluent, domain-specific API. Test reports are generated in HTML5, AsciiDoc, and plain text formats.

## Architecture

### Core Modules

- **jgiven-core**: The heart of JGiven containing:
  - `impl/` - Scenario execution engine (ScenarioExecutor, ScenarioModelBuilder, stage creation via ByteBuddy)
  - `report/` - Report generators for HTML5, AsciiDoc, JSON, and plain text formats
  - `format/` - Step value formatting
  - `annotation/` - Custom annotations (@Given, @When, @Then, @Stage)

- **jgiven-junit / jgiven-junit5 / jgiven-testng**: Integration adapters for respective test frameworks

- **jgiven-spring / jgiven-spring-junit4 / jgiven-spring-junit5**: Spring framework integration with dependency injection support

- **jgiven-tests**: Integration tests written using JGiven that test all framework features

- **jgiven-examples**: Standalone example projects (junit5, spring-boot, selenium, kotlin, scala, etc.)

### Key Concepts

1. **Stages**: Modular components that share state via injection. Each stage class contains Given/When/Then methods.

2. **Scenario Execution**: `ScenarioExecutor` orchestrates step execution, handles failures, and records results.

3. **Report Generation**: After test execution, JSON files are written to `build/reports/jgiven/json`, then processed by report generators.

4. **ByteBuddy**: Used at runtime to create dynamic proxy classes for stage implementations.

## Code Style

- Do not reformat existing files - follow the existing code style
- A checkstyle configuration is available in `./checkstyle.xml`
- The project uses tabs for indentation

## Development Notes

- Generated source files are created from templates in `jgiven-core/src/main/templates` during the build process
- Translations are generated from `.properties` files in `src/main/translations`
- JDK 11+ is required to build
- Android builds require `ANDROID=true` and `ANDROID_SDK_ROOT` environment variables