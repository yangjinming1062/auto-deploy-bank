# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Wire is Square's protocol buffers compiler and runtime library. It reads `.proto` schema files and generates idiomatic code for Java, Kotlin, and Swift. The project also includes a gRPC client and supporting adapters for JSON serialization.

## Build System

This project uses Gradle with the Kotlin DSL. The build system includes:
- Custom build support plugins in `build-support/`
- Custom settings plugin for dependency resolution
- Spotless for code formatting (Google Java Format, ktlint for Kotlin)
- Kotlin Multiplatform for runtime (JVM, JS, Native, WASM)

### Common Commands

```bash
# Clean and run all checks (required before PRs)
./gradlew clean check

# Build a specific module
./gradlew :wire-compiler:build

# Build and install the compiler distributions
./gradlew :wire-compiler:installDist

# Format code
./gradlew spotlessApply

# Check formatting without applying
./gradlew spotlessCheck

# Run tests for a specific module
./gradlew :wire-runtime:test

# Run a single test class
./gradlew test --tests "WireCompilerTest"
./gradlew :wire-compiler:test --tests "com.squareup.wire.WireCompilerTest"

# Build Swift modules (when Swift is enabled)
./gradlew :wire-runtime-swift:build

# Build with only specific targets (faster iteration)
./gradlew :wire-compiler:compileKotlin
./gradlew :wire-compiler:compileJava

# Publish to local Maven repository
./gradlew publishToMavenLocal

# Build all artifacts
./gradlew build
```

### Module-Specific Commands

```bash
# Build and test the Gradle plugin with integration tests
./gradlew :wire-gradle-plugin:test

# Build the compiler and test against golden files
./gradlew :wire-compiler:test
./gradlew :wire-golden-files:...

# Run gRPC integration tests
./gradlew :wire-grpc-tests:test

# Run compatibility tests with protoc
./gradlew :wire-protoc-compatibility-tests:test
```

## Project Structure

### Core Components

- **wire-compiler** - Main compiler CLI that orchestrates schema loading, validation, and code generation
- **wire-schema** - Schema parsing, validation, profiling, and pruning. Provides `SchemaHandler` interface for custom code generators
- **wire-runtime** - Multiplatform runtime library (Kotlin/JVM, Kotlin/JS, Kotlin/Native, Kotlin/WASM) with protobuf readers/writers
- **wire-java-generator** - Generates Java code from schemas
- **wire-kotlin-generator** - Generates Kotlin code from schemas with coroutines support
- **wire-swift-generator** - Generates Swift code from schemas
- **wire-gradle-plugin** - Gradle plugin for Wire that automates code generation in builds

### Supporting Components

- **wire-grpc-client** - gRPC client for Kotlin
- **wire-grpc-mockwebserver** - Mock web server for testing gRPC
- **wire-gson-support** - Gson adapters for Wire messages
- **wire-moshi-adapter** - Moshi adapters for Wire messages
- **wire-reflector** - Schema reflection utilities
- **wire-schema-tests** - Tests for schema processing

### Key Architecture Patterns

1. **Schema Processing Pipeline** (wire-schema):
   - Load and parse `.proto` files
   - Link schema references
   - Apply profiles and options
   - Prune unused elements
   - Execute `SchemaHandler` for code generation

2. **Code Generation** (generators):
   - Each language has a dedicated generator module
   - Generators receive a processed `Schema` and `Target` configuration
   - Generated code includes message types, enums, services, and adapters

3. **Multiplatform Runtime** (wire-runtime):
   - Common API across platforms using Kotlin Multiplatform
   - Platform-specific implementations for I/O and protobuf encoding
   - Adapters for JSON serialization (Gson, Moshi)

4. **Gradle Integration** (wire-gradle-plugin):
   - Registers Wire tasks for code generation
   - Integrates generated sources with compilation
   - Supports multiple source roots and output configurations

## Code Style and Conventions

- **Formatting**: Enforced by Spotless (Google Java Format for Java, ktlint for Kotlin)
- **Licensing**: Apache 2.0 - see `gradle/license-header.txt`
- **API Stability**: Binary compatibility validation is enabled
- **Documentation**: Dokka for API docs (published to `/docs/3.x/{module}/`)
- **Testing**: JUnit for JVM tests, kotlin.test for Kotlin Multiplatform
- **Version**: Current version in `gradle.properties` (e.g., `6.1.0-SNAPSHOT`)

## Important Files

- `settings.gradle.kts` - Module inclusion and dependency substitution
- `build.gradle.kts` - Root build configuration
- `gradle.properties` - Version and Gradle configuration
- `build-support/` - Custom Gradle plugins for build configuration
- `gen-tests.gradle.kts` - Generated test infrastructure
- `wire-gradle-plugin-playground/` - Example Wire Gradle plugin usage

## Release Process

JVM releases are automated via GitHub Actions. See `RELEASING.md` for:
- Version updates (all `gradle.properties`)
- Git tagging process
- Sonatype/Maven Central publishing
- Swift CocoaPods publishing

## Development Notes

- Swift modules are conditionally included via `swift` project property
- Kotlin Multiplatform targets are conditionally enabled via `knative`, `kjs`, `kwasm` properties
- Internal build property `com.squareup.wire.internal=true` signals building within the repo
- Tests use golden file testing extensively (see `wire-golden-files/`)
- Integration tests for the Gradle plugin use fixture projects in `wire-gradle-plugin/src/test/projects/`

## Module Dependencies

The compiler orchestrates code generation by depending on:
- `wire-schema` (schema processing)
- `wire-kotlin-generator` (Kotlin codegen)
- `wire-java-generator` (Java codegen)
- `wire-swift-generator` (Swift codegen)

Generators depend on `wire-runtime` for common types and utilities.

## Testing Strategy

- **Unit Tests**: Standard JUnit tests for each module
- **Golden Files**: Generated code is compared against golden files in `wire-golden-files/`
- **Integration Tests**: Real-world scenarios in `wire-tests/`, `wire-grpc-tests/`
- **Gradle Plugin Tests**: Integration tests using fixture projects in `wire-gradle-plugin/src/test/projects/`
- **Compatibility Tests**: Wire vs protoc compatibility in `wire-protoc-compatibility-tests/`