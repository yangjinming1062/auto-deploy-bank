# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Full build with tests
./mvnw install

# Run tests without installing
./mvnw test

# Run a specific test class
./mvnw test -Dtest=FunctionInvokerTests

# Run a specific test method
./mvnw test -Dtest=FunctionInvokerTests#testHandleRequest

# Skip tests
./mvnw install -DskipTests

# Build with specific Maven profile
./mvnw install -Pcore          # Core modules only (context, web)
./mvnw install -Pcentral       # All central modules (includes samples, adapters)

# Build single module
./mvnw install -pl spring-cloud-function-context

# Format code (Spring Java Format)
./mvnw spring-javaformat:apply

# Run checkstyle
./mvnw checkstyle:check

# Build docs
./mvnw install -pl docs
```

**Requirements:**
- JDK 17+
- Docker (for integration tests requiring middleware like Redis)

**Note:** The `spring` Maven profile is already active via `.mvn/maven.config` for Spring milestone/snapshot repositories.

## Project Overview

Spring Cloud Function promotes a functional programming model for Spring applications. Functions can be plain Java methods, `Supplier`, `Function`, or `Consumer` beans that are auto-registered with a catalog.

### Core Modules

| Module | Purpose |
|--------|---------|
| `spring-cloud-function-core` | Core interfaces (`FunctionInvocationHelper`) and fundamental abstractions |
| `spring-cloud-function-context` | Main implementation - function registration, catalog, type discovery, JSON mapping |
| `spring-cloud-function-web` | HTTP/Web support (Spring MVC and WebFlux) for exposing functions as endpoints |
| `spring-cloud-function-adapters` | Cloud platform adapters (AWS Lambda, Azure Functions, GCP Functions, gRPC) |
| `spring-cloud-function-integration` | Spring Integration support |
| `spring-cloud-function-kotlin` | Kotlin-specific function support |
| `spring-cloud-function-dependencies` | BOM for dependency management |

### Architecture

**Function Invocation Flow:**
1. Function beans (`Supplier<T>`, `Function<I, O>`, `Consumer<T>`) are discovered in the Spring context
2. `BeanFactoryAwareFunctionRegistry` wraps each function with `FunctionRegistration` and registers it in the `FunctionCatalog`
3. When invoked, `FunctionInvocationWrapper` handles:
   - Type conversion (JSON → POJO, etc.)
   - Reactive/impedance matching (`Flux` ↔ single value)
   - Function composition (`foo|bar`)
4. `RoutingFunction` handles dynamic routing based on `spring.cloud.function.definition` header

**Key Classes:**
- `FunctionInvocationWrapper` - Core proxy that wraps every function; handles type conversion, composition, and reactive support
- `FunctionCatalog` - Interface for looking up functions by name
- `BeanFactoryAwareFunctionRegistry` - Default implementation integrating with Spring's bean factory
- `FunctionRegistration` - Metadata wrapper for function beans
- `RoutingFunction` - Routes messages to target functions; handles `spring.cloud.function.definition`
- `FunctionalSpringApplication` - Bootstrapper for standalone functional Spring applications

**Type System:**
- `FunctionTypeUtils` - Discovers and validates function types from class definitions
- Supports `POJO`, `Flux<T>`/`Mono<T>`, and `Message<T>` types transparently

**Cloud Adapters:**
Each platform adapter (AWS Lambda, Azure Functions, GCP Functions) follows this pattern:
- Implements platform-specific entry point (e.g., `RequestStreamHandler` for AWS)
- Bootstraps Spring `ApplicationContext` on cold start
- Converts platform events to `Message<T>` format
- Invokes function via `FunctionCatalog` and converts output back to platform format

### Functional Bean Definitions

Spring Cloud Function supports functional bean definitions without `@Configuration` classes:

```java
@Bean
public Function<String, String> uppercase() {
    return s -> s.toUpperCase();
}

// Or using FunctionalSpringApplication
FunctionalSpringApplication.run(MyConfiguration.class, "--spring.cloud.function.definition=uppercase");
```

### Message Model

Functions can work with:
- Plain POJOs: `Function<Person, String>`
- Reactive types: `Function<Flux<String>, Flux<String>>`
- Spring Messages: `Function<Message<T>, Message<R>>`

### Configuration Properties

Key properties:
- `spring.cloud.function.definition` - Which function to invoke (required for routing)
- `spring.cloud.function.routing-expression` - SpEL expression for dynamic routing
- `spring.cloud.function.web.export.enabled` - Export functions via HTTP (default: true)
- `spring.cloud.function.stream.supplier` / `spring.cloud.function.stream.function` - For Spring Cloud Stream integration

### Samples

The `spring-cloud-function-samples/` directory contains comprehensive examples:
- `function-sample` - Basic function sample
- `function-sample-aws*/` - AWS Lambda deployment examples
- `function-sample-azure*/` - Azure Functions examples
- `function-sample-gcp*/` - Google Cloud Functions examples
- `function-sample-pojo` - POJO-based functions
- `function-sample-kotlin-web` - Kotlin web functions

## Code Conventions

- Follow Spring Framework code format conventions
- ASF license header required on all Java files
- Add `@author` tag to new classes
- Use Checkstyle (configured via spring-cloud-build)
- All commits require Signed-off-by (DCO)