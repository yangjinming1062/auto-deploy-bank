# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the **Grails Framework** repository - a multi-module Gradle project that builds the complete Grails web application framework. Grails is a framework for building web applications with the Groovy programming language, built on Spring Boot.

## Project Structure

The repository is organized into several categories of submodules:

- **Core Modules**: `grails-core`, `grails-bootstrap`, `grails-console`, `grails-shell`, `grails-logging`, `grails-spring`, `grails-codecs`, `grails-encoder`, `grails-databinding`
- **Web Layer**: `grails-web`, `grails-web-common`, `grails-web-boot`, `grails-web-mvc`, `grails-web-databinding`, `grails-web-fileupload`, `grails-web-url-mappings`
- **Plugins**: `grails-plugin-*` modules for controllers, datasource, domain-class, interceptors, i18n, mimetypes, rest, services, url-mappings, validation
- **Test Suites**: `grails-test-suite-*` (base, persistence, uber, web)
- **Build & Documentation**: `grails-dependencies`, `grails-bom`, `grails-docs`, `grails-gradle-model`

The main source directories follow standard Groovy/Java structure with `src/main/groovy`, `src/main/java`, `src/test/groovy`, and `src/test/java`.

## Build System

This project uses **Gradle** with the Gradle Wrapper (`./gradlew`). The build configuration is defined in:
- Root `build.gradle` - main build configuration, dependencies, and subproject setup
- `settings.gradle` - defines all submodules
- `gradle.properties` - version numbers for all dependencies

### Common Commands

```bash
# Build and install all modules to local Maven repository
./gradlew install

# Clean all build artifacts
./gradlew clean

# Run all tests
./gradlew test

# Run tests for a specific module
./gradlew :grails-core:test

# Run a single test (replace TestName with actual test class name)
./gradlew :grails-core:test -DsingleTest.single=TestName

# Run tests with debug options
./gradlew test -Ddebug.tests

# Build documentation
./gradlew docs

# Generate Javadoc and Groovydoc
./gradlew javadoc groovydoc

# Build complete distribution
./gradlew assemble

# Publish to Maven Local (also installs to local dist)
./gradlew publishToMavenLocal

# Check for bugs with Findbugs
./gradlew findbugs
```

### Memory Configuration

If encountering out-of-memory errors during builds, set Gradle options:

```bash
export GRADLE_OPTS="-Xmx2G -Xms2G -XX:NewSize=512m -XX:MaxNewSize=512m"
./gradlew install
```

## Testing

- **Framework**: Uses **Spock** for testing (version 2.0-groovy-3.0) and **JUnit 5**
- **Test Location**: `src/test/groovy` for Spock tests, `src/test/java` for JUnit tests
- **Retry Policy**: Tests automatically retry on failure (max 2 retries)
- **Test Exclusions**: `*TestCase.class` and `$*.class` files are excluded
- **Parallel Execution**: In CI, tests run with 2 parallel forks and 768m max heap; locally with 1024m max heap

## Java Compatibility

- **Target Version**: Java 8 (source and target compatibility)
- **Current Version**: 5.0.2-SNAPSHOT
- **Groovy Version**: 3.0.7

## Key Dependencies

- **Spring Framework**: 5.3.13
- **Spring Boot**: 2.5.6
- **Micronaut**: 3.0.3 (for reactive and cloud-native features)
- **GORM**: 7.1.0 (Grails Object Relational Mapping)
- **Hibernate**: 7.1.0
- **Spock**: 2.0-groovy-3.0
- **Servlet API**: 4.0.1

## Release Process

Releases follow a strict process documented in `RELEASE.md`:

1. Update versions in `gradle.properties`, `grails-bom/plugins.properties`, and `grails-bom/profiles.properties`
2. Ensure all snapshot dependencies are resolved
3. Set release version in `build.gradle` and `grails-core/src/test/groovy/grails/util/GrailsUtilTests.java`
4. Commit and tag: `git tag vXXX`
5. Push tags and wait for CI to complete
6. Run Maven Central sync: `./gradlew sWMC`
7. Update documentation and create GitHub release
8. Bump version to next snapshot and push

## CI/CD

- **CI**: Travis CI configuration in `.travis.yml`
- **Build Scans**: Published to Gradle Enterprise at https://ge.grails.org
- **Build Triggers**: Automatically triggers `grails3-functional-tests` build

## Maven Repositories

The project publishes to:
- **Snapshots**: `https://repo.grails.org/grails/libs-snapshots-local`
- **Releases**: Maven Central via Nexus staging
- **SDKMAN!**: Published to SDKMAN for Grails installation

## Important Notes

- Source encoding is **UTF-8** for all Java and Groovy files
- This is a **multi-release** build that produces both Java and Groovy artifacts
- Joint build with Groovy is configured to use a specific Groovy version from `gradle.properties`
- Some plugins (Findbugs, Nexus staging) are applied only to non-test-suite projects
- The project uses a custom `singleTest` task for running individual test cases