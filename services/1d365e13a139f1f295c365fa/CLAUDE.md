# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Reactor Netty is a Java reactive streams library providing non-blocking and backpressure-ready TCP/HTTP/UDP/QUIC clients & servers based on Netty framework. It implements the Reactive Streams specification using Project Reactor.

**Current Version:** 1.3.2-SNAPSHOT
**Java Requirements:** Java 8+ (multi-release JAR supporting 8, 11, 17)
**Key Dependencies:** Netty 4.2.7.Final, Project Reactor 3.8.2

## Common Development Commands

```bash
# Build entire project with tests
./gradlew build

# Run tests only
./gradlew test

# Run tests for specific module
./gradlew :reactor-netty-core:test
./gradlew :reactor-netty-http:test

# Run single test
./gradlew test --tests "TcpServerTests"

# Run tests in debug mode (listen on port 5005)
./gradlew test --debug-jvm

# Check code formatting (without fixing)
./gradlew spotlessCheck

# Fix code formatting
./gradlew spotlessApply

# Run Checkstyle
./gradlew checkstyle

# Generate Javadoc
./gradlew javadoc
./gradlew aggregateJavadoc

# Publish to local Maven repository
./gradlew publishToMavenLocal

# Clean build artifacts
./gradlew clean
```

## Project Architecture

### Module Structure

The project is organized as 7 Gradle subprojects:

1. **`reactor-netty-core`** - Core networking foundation
   - TCP/UDP transport abstractions
   - Connection pooling (ConnectionProvider)
   - Event loop management (LoopResources)
   - Entry points: `TcpServer`, `TcpClient`, `UdpServer`, `UdpClient`

2. **`reactor-netty-http`** - HTTP protocol implementation
   - HTTP/1.1, HTTP/2, HTTP/3 support
   - WebSocket support
   - Entry points: `HttpServer`, `HttpClient`, `HttpResources`

3. **`reactor-netty-http-brave`** - Brave tracing integration
   - Distributed tracing support for HTTP

4. **`reactor-netty-quic`** - QUIC protocol implementation
   - HTTP/3 support via QUIC transport

5. **`reactor-netty-examples`** - Usage examples and patterns

6. **`reactor-netty-graalvm-smoke-tests`** - GraalVM native image tests

7. **`reactor-netty`** - BOM (Bill of Materials) aggregation module

### Architecture Pattern

**Reactor Pattern with Reactive Streams:**
- Non-blocking I/O using Netty's event loop model
- Backpressure support via Project Reactor's Flux/Mono
- Event-driven, asynchronous processing
- Publisher/Subscriber pattern throughout

### Key Package Structure

```
reactor.netty
├── reactor.netty.tcp          - TCP server/client
├── reactor.netty.http         - HTTP server/client
│   ├── reactor.netty.http.client
│   ├── reactor.netty.http.server
│   └── reactor.netty.http.websocket
├── reactor.netty.udp          - UDP server/client
├── reactor.netty.quic         - QUIC server/client
├── reactor.netty.transport    - Transport abstractions
├── reactor.netty.channel      - Channel operations
├── reactor.netty.resources    - Connection pooling, loop resources
├── reactor.netty.observability - Metrics and tracing
└── reactor.netty.contextpropagation - Context propagation
```

### Multi-release JAR Configuration

The project is configured as a multi-release JAR supporting:
- Java 8 (base layer)
- Java 11 (META-INF/versions/11/)
- Java 17 (META-INF/versions/17/)

This allows leveraging newer Java features while maintaining Java 8 compatibility.

## Testing Framework

- **JUnit 5.14.1** for unit tests
- **Test Retry Plugin** - Flaky tests are retried (max 10 failures, 1 retry)
- **BlockHound integration** - Detects blocking calls in reactive code
- **Netty Leak Detection** - Paranoid level enabled for connection leak detection
- **Reactor-specific tracing** - Context propagation testing

Test configuration includes:
- IPv4/IPv6 preference system properties
- BlockHound agent for blocking call detection
- Channel leak detection

## Code Quality Tools

- **Spotless** - Code formatting with Eclipse formatter
- **Checkstyle** - Static analysis (see `codequality/checkstyle.xml`)
- **Error Prone** - Static analysis for bug detection
- **JaCoCo** - Test coverage reporting

## Building and Publishing

The project uses Gradle with the Gradle Wrapper. CI/CD is handled via GitHub Actions with workflows for:
- Multi-JDK testing
- GraalVM compatibility checks
- Netty snapshot compatibility
- Automated publishing to Maven Central
- CodeQL security analysis

## Dependencies and BOM

The project maintains strict version management for:
- **Reactor Core:** 3.8.2-SNAPSHOT
- **Netty:** 4.2.7.Final
- **Micrometer** (optional) - Metrics
- **Brave/Zipkin** (optional) - Tracing

The `reactor-netty` module acts as a BOM (Bill of Materials) for dependency management.

## Documentation

- **Reference Manual:** Antora-based documentation in `docs/` directory using AsciiDoc
- **Javadoc:** Aggregated Javadoc generation available via `aggregateJavadoc`
- **Examples:** Comprehensive examples in `reactor-netty-examples` module
- **Workshops:** External workshop available at https://violetagg.github.io/reactor-netty-workshop/

## Important Implementation Notes

### Connection Management

- HTTP connections are pooled via `HttpResources` (global pool)
- TCP connections use `ConnectionProvider` for pooling
- Resources should be properly disposed to prevent leaks
- `DisposableServer` handles server lifecycle

### Backpressure

- Implemented throughout via Project Reactor's backpressure
- Publishers must respect demand from subscribers
- Non-blocking all the way through the stack

### Observability

- Micrometer integration for metrics
- Brave/Zipkin integration for tracing
- Context propagation support via `ContextPropagation`
- Logging integrated with SLF4J

## Getting Started Example (from README.md)

```java
// Simple HTTP Server
HttpServer.create()
    .port(0)
    .route(routes -> routes.post("/test/{param}", (request, response) ->
        response.sendString(request.receive()
            .asString()
            .map(s -> s + ' ' + request.param("param") + '!')
            .log("http-server"))))
    .bindNow();

// Simple HTTP Client
HttpClient.create()
    .port(server.port())
    .post()
    .uri("/test/World")
    .send(ByteBufFlux.fromString(Flux.just("Hello")))
    .responseContent()
    .aggregate()
    .asString()
    .log("http-client")
    .block();
```

## Support and Resources

- **Issue Tracking:** https://github.com/reactor/reactor-netty/issues
- **Stack Overflow:** tag `reactor-netty`
- **Gitter:** https://gitter.im/reactor/reactor-netty
- **Reference Docs:** https://projectreactor.io/docs/netty/release/reference/index.html
- **API Docs:** https://projectreactor.io/docs/netty/release/api/