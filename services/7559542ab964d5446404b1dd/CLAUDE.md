# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Full build with all tests and quality checks
./gradlew build

# Run tests only (parallel by default)
./gradlew test

# Run a specific test class
./gradlew :servicetalk-http-api:test --tests "io.servicetalk.http.api.*Test"

# Run specific test method
./gradlew :servicetalk-concurrent-api:test --tests "SingleTest.testMapError"

# Generate IntelliJ IDEA project files
./gradlew idea

# Update dependency lock files (after modifying gradle.properties)
./gradlew resolveAndLockAll --write-locks
```

## Architecture Overview

ServiceTalk is a JVM network application framework built on Netty, providing protocol-tailored APIs (HTTP/1.x, HTTP/2, gRPC) with multiple programming paradigms.

### Four Programming Paradigms

1. **Blocking-Aggregated**: Traditional request/response pattern (similar to `java.io`)
2. **Blocking-Streaming**: Blocking I/O with chunk processing
3. **Async-Aggregated**: Reactive `Single<T>` (similar to `CompletableFuture`)
4. **Async-Streaming**: Reactive `Publisher<T>` (ReactiveStreams compatible)

All paradigms can coexist in the same application and safely switch between them.

### Module Organization

- **Core Concurrency**: `servicetalk-concurrent-api` provides `Single<T>` and `Publisher<T>` async primitives
- **HTTP Layer**: `servicetalk-http-api` (API) + `servicetalk-http-netty` (Netty implementation)
- **gRPC Layer**: `servicetalk-grpc-api`, `servicetalk-grpc-netty`, `servicetalk-grpc-protobuf`
- **Transport**: `servicetalk-transport-api`, `servicetalk-transport-netty`
- **JAX-RS Integration**: Multiple Jersey variants (javax, jakarta9, jakarta10)

### Key Design Patterns

**Filter Pattern**: Extensibility through `*Filter` and `*FilterFactory` classes:
- `StreamingHttpServiceFilter` / `StreamingHttpServiceFilterFactory`
- `StreamingHttpClientFilter` / `StreamingHttpClientFilterFactory`
- `StreamingHttpConnectionFilter`

**Builder Pattern**: Configuration via builder classes:
- `HttpClients`, `HttpServers`, `GrpcClients`, `GrpcServers` factory classes
- `*ClientBuilder` interfaces for client configuration

**Delegation Pattern**: `AbstractDelegating*` base classes for wrapper implementations

### Execution Strategy & Offloading

ServiceTalk automatically offloads user code from the Netty event loop. The `HttpExecutionStrategy` interface controls which paths require offloading. Key APIs:
- `HttpExecutionStrategies`: Factory for common strategies
- `Executor` / `IoExecutor`: Thread execution control
- `ExecutionStrategyInfluencer`: Components that declare offloading requirements

### API Naming Conventions

- `*Client`: Client-side API
- `*Server`: Server-side API
- `*Connection`: Connection-level API
- `Blocking*`: Synchronous/blocking variants
- `Streaming*`: Chunked/publisher-based variants
- `Default*`: Default implementation of interfaces
- `Delegating*`: Wrapper that delegates to another instance

### Reactive Primitives (`servicetalk-concurrent-api`)

- **`Single<T>`**: Async computation completing with one value or error
- **`Publisher<T>`**: ReactiveStreams-compatible streaming
- **`Completable`**: Completion signal (success/failure, no value)

These support rich composition: `map`, `flatMap`, `zip`, `merge`, `concat`, `retry`, etc.

## Testing

- **Frameworks**: JUnit 5, TestNG (legacy), Mockito, Hamcrest, AssertJ
- **Benchmarking**: JMH (`servicetalk-benchmarks`)
- **Test Fixtures**: Modules use `testFixtures` for shared test utilities
- **Test Resources**: `servicetalk-test-resources` provides test certificates, certificates, etc.

## Java Version Support

- Minimum target: JDK 8
- CI tests against: JDK 8, 11, 17, 21, 25
- Some features (e.g., dependency analysis) require JDK 11+