# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Armeria is a Java microservice framework built on top of Netty, supporting HTTP/2, gRPC, Thrift, and more. It's a reactive, asynchronous client/server library with rich integration capabilities.

**Main entry points:**
- Server: `com.linecorp.armeria.server.Server` (core/src/main/java/com/linecorp/armeria/server/Server.java:1)
- Client: `com.linecorp.armeria.client.Client` interface (core/src/main/java/com/linecorp/armeria/client/Client.java:44)

## Building and Testing

### Common Commands

```bash
# Build all modules
./gradlew build

# Run tests
./gradlew test

# Run a single test
./gradlew test --tests "com.example.armeria.MyTestClass"

# Run tests for specific module
./gradlew :core:test

# Checkstyle and linting
./gradlew check
./gradlew lint

# Generate sources (for proto/thrift)
./gradlew generateSources

# Build with coverage
./gradlew build -Pcoverage

# Enable leak detection
./gradlew test -Pleak

# Disable linting (for faster builds)
./gradlew build -PnoLint
```

### Test Options

- **Java version testing:**
  ```bash
  ./gradlew test -PbuildJdkVersion=17 -PtestJavaVersion=11
  ```

- **Transport type selection:**
  ```bash
  ./gradlew test -PtransportType=epoll  # or nio, io_uring, kqueue
  ```

- **Enable Blockhound (reactive streams checking):**
  ```bash
  ./gradlew test -Pblockhound
  ```

- **Retry flaky tests:**
  ```bash
  ./gradlew test -Pretry
  ```

- **Skip web-based tests:**
  ```bash
  ./gradlew test -PnoWeb
  ```

## Code Architecture

### Module Structure

The project uses a **flag-based Gradle module system** defined in `settings.gradle` and `gradle/scripts/settings-flags.gradle`:

**Core modules:**
- `:core` - Main Armeria library (Java 8+, supports shading and native image)
- `:client` - Client-side abstractions and implementations
- `:server` - Server-side abstractions and implementations
- `:common` - Common utilities, HTTP abstractions, and data structures

**Integration modules (examples):**
- `:grpc`, `:grpc-kotlin`, `:grpc-reactor`, `:grpc-scala` - gRPC integrations
- `:thrift` - Apache Thrift integration
- `:spring*` - Spring Boot integrations (multiple modules)
- `:kotlin` - Kotlin support
- `:reactor3` - Project Reactor integration
- `:rxjava2`, `:rxjava3` - RxJava integrations
- `:graphql`, `:graphql-kotlin`, `:graphql-sangria` - GraphQL support
- `:dropwizard2` - Dropwizard integration
- `:retrofit2` - Retrofit integration
- `:resilience4j2` - Resilience4j integration

**Utility modules:**
- `:annotation-processor` - Annotation processing for code generation
- `:testing-internal` - Internal testing utilities
- `:benchmarks` - Performance benchmarks (JMH, GHZ)
- `:bom` - Maven Bill of Materials for dependency management
- `:version-catalog` - Published version catalog

### Key Dependencies

Managed in `dependencies.toml`:
- **Netty** - Core networking (multiple versions for compatibility)
- **Jackson** - JSON processing
- **Jetty** - Servlet container support
- **SLF4J/Logback** - Logging
- **gRPC** - RPC framework
- **Thrift** - RPC protocol
- **Reactor** - Reactive streams
- **Checkstyle** - Code style enforcement
- **Error Prone & NullAway** - Static analysis

### Build System

- **Gradle** with custom scripts in `gradle/scripts/`
- **Version catalogs** via `dependencies.toml` (TOML format)
- **Flag-based configuration** using `includeWithFlags` directive
- **Multi-Java version support** (Java 8-24+)
- **Native image support** with GraalVM (for select modules)
- **Shading** and class relocation for dependency isolation

## Development Practices

- **Error Prone** and **NullAway** are enabled by default (disable with `-PnoLint`)
- **JUnit 5** for testing (Jupiter engine)
- **Checkstyle** configuration in `settings/checkstyle/`
- **Kotlin** projects use ktlint for code style
- **Protobuf/Thrift** source generation via `generateSources` task
- **Maven Central** publishing via Nexus staging

## Project-Specific Notes

- Minimum Java version: 8 (for consuming), varies by module (check flags like `java11`, `java17`)
- Release requires JDK 25 (see `build.gradle:330`)
- All Java projects except `:core` depend on `:core`
- Shaded JARs use ProGuard trimming for size optimization
- Context propagation is a first-class concept throughout the codebase
- Built-in support for multiple transport types (NIO, epoll, io_uring, kqueue)