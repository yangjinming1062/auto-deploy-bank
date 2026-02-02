# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Full project build
./gradlew clean build

# Run all tests
./gradlew test

# Run a single test class
./gradlew test --tests "io.crnk.core.repository.ResourceRepositoryBaseTest"

# Run a specific test method
./gradlew test --tests "io.crnk.core.repository.ResourceRepositoryBaseTest.findOne"

# Build without tests (faster)
./gradlew assemble

# Build Java documentation
./gradlew javadoc

# Run JaCoCo code coverage report
./gradlew jacocoRootReport
```

## Project Overview

Crnk is an implementation of the [JSON API specification](https://jsonapi.org/) in Java. It's a multi-module Gradle project organized into several functional areas:

### Core Modules

- **crnk-core**: Main implementation containing:
  - `boot/` - `CrnkBoot` class for framework initialization
  - `engine/` - HTTP request handling, document mapping, registry, filtering
  - `repository/` - `ResourceRepository` and `ResourceRepositoryBase` interfaces for data access
  - `resource/` - Resource annotations (`@JsonApiResource`, `@JsonApiId`) and meta-models
  - `queryspec/` - QuerySpec for filtering, sorting, and pagination
  - `module/` - Module system for extensibility

- **crnk-client**: JSON API client implementation
- **crnk-meta**: Meta-model for working with resource information
- **crnk-reactive**: Reactive/RxJava support
- **crnk-validation**: Bean validation integration
- **crnk-security**: Security features
- **crnk-operations**: Atomic operations (bulk updates)
- **crnk-home**: Home repository and discovery endpoint

### Setup Modules (Framework Integration)

Located in `crnk-setup/`:
- `crnk-setup-spring` - Spring Framework
- `crnk-setup-spring-boot1` / `crnk-setup-spring-boot2` - Spring Boot
- `crnk-setup-servlet` - Servlet API
- `crnk-setup-cdi` - CDI/Jakarta EE
- `crnk-setup-rs` - JAX-RS
- `crnk-setup-vertx` - Vert.x
- `crnk-setup-guice` - Google Guice

### Data Access Modules

Located in `crnk-data/`:
- `crnk-data-jpa` - JPA/Hibernate integration with `JpaEntityRepositoryBase`
- `crnk-data-activiti` - Activiti BPM integration
- `crnk-data-facet` - Faceted search support

### Code Generation Modules

Located in `crnk-gen/`:
- `crnk-gen-java` - Java code generation from resource definitions
- `crnk-gen-typescript` - TypeScript client bindings
- `crnk-gen-openapi` - OpenAPI/Swagger generation
- `crnk-gen-asciidoc` - Documentation generation

### Frontend Modules

- **crnk-ui** - Angular 4 UI for exploring JSON API endpoints
- **crnk-client-angular-ngrx** - Angular NgRx integration

## Key Architectural Patterns

### Repository Pattern

Resources are accessed through `ResourceRepository` interface. Extend `ResourceRepositoryBase` for convenience:

```java
@JsonApiResource(type = "vote")
public class Vote {
    @JsonApiId
    private UUID id;
    private int stars;
}

public class VoteRepository extends ResourceRepositoryBase<Vote, UUID> {
    public VoteRepository() {
        super(Vote.class);
    }

    @Override
    public ResourceList<Vote> findAll(QuerySpec querySpec) {
        return querySpec.apply(votes.values());
    }
}
```

### Module System

Use `SimpleModule` or implement `Module` interface to extend Crnk:

```java
SimpleModule module = new SimpleModule("my-module");
module.addRepository(MyRepository.class);
boot.addModule(module);
```

### QuerySpec

All queries use `QuerySpec` for consistent filtering, sorting, pagination, and field selection:

```java
QuerySpec querySpec = new QuerySpec(Task.class);
querySpec.addFilter(new FilterSpec(Arrays.asList("name"), FilterOperator.EQ, "myTask"));
querySpec.setLimit(10);
querySpec.setOffset(0);
ResourceList<Task> tasks = repository.findAll(querySpec);
```

## Test Conventions

- JUnit 5 (Jupiter) is used for testing
- Tests located in `src/test/java` parallel to main sources
- Integration tests use in-memory servers (Jersey, Spring Boot Test)
- Angular tests use Karma/Jasmine (in `crnk-ui` and `crnk-client-angular-ngrx`)

## Code Style

- Follows default IntelliJ IDEA code style settings
- Java 8+ compatibility
- SLF4J for logging
