# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flower is a reactive microservice framework built on Apache Pekko (formerly Akka). It enables developers to build reactive systems by implementing fine-grained services that are orchestrated into flows via message passing. Services communicate asynchronously through messages - the return value of one service becomes the input to subsequent services.

Key characteristics:
- **Message-driven**: Services communicate via messages; no direct method calls between services
- **Actor-based**: Built on Pekko Actor model for concurrency and fault tolerance
- **Flow orchestration**: Services are composed through `.flow` configuration files or programmatically
- **Weak coupling**: Services are only coupled through message types, not code dependencies

## Build Commands

```bash
# Full build (runs checkstyle, license formatting, tests, and creates jars)
./mvnw clean install

# Build skipping tests
./mvnw clean install -DskipTests=true

# Build with checkstyle validation (checkstyle runs by default in 'validate' phase)
./mvnw clean install -Dcheckstyle.skip=false

# Run all tests
./mvnw test

# Run a specific test class
./mvnw test -Dtest=ClassName

# Run a specific test method
./mvnw test -Dtest=ClassName#methodName

# Generate code coverage report
./mvnw cobertura:cobertura

# Format license headers
./mvnw license:format

# Skip javadoc generation (faster builds)
./mvnw clean install -Dmaven.javadoc.skip=true
```

## Architecture Overview

### Core Concepts

**Service Interface**: The fundamental building block. Implement `Service<P, R>` where `P` is the input message type and `R` is the output type.

```java
@FlowerService
public class MyService implements Service<User, User> {
    public User process(User message, ServiceContext context) throws Throwable {
        // business logic
        return processedMessage;
    }
}
```

**Flow Patterns**:
- **Sequential**: `A -> B -> C` (simple chain)
- **Forking**: `A -> B` and `A -> C` (parallel execution)
- **Aggregation**: `B -> D` and `C -> D` (collect parallel results)
- **Conditional**: Route to different services based on message type or content

**Actor Model**: Services are wrapped in Pekko actors (`ServiceActor`), enabling:
- Asynchronous message processing without blocking
- Supervision and fault tolerance
- Distributed message passing across nodes

### Module Structure

| Module | Purpose |
|--------|---------|
| `flower.common` | Core interfaces (`Service`, `FlowerService`), annotations, utilities, lifecycle管理 |
| `flower.core` | Framework engine: `ServiceFactory`, `ServiceFlow`, `ServiceActor`, `FlowRouter`, actor system |
| `flower.web` | Spring integration: `FlowerController`, `SpringFlowerFactory`, Spring Boot auto-configuration |
| `flower.boot.starter` | Spring Boot starter with auto-configuration support |
| `flower.center` | Standalone service registry center application |
| `flower.registry` | Registry client SPI and implementations (Zookeeper, Redis via Redisson) |
| `flower.serializer` | Message serialization (Hessian, Protostuff, FastJSON, FastJSON2) |
| `flower.filter` | Filter chain for request/response processing (includes OpenTracing support) |
| `flower.config` | Configuration parsing (`flower.yml`) |
| `flower.container` | Service container implementation |
| `flower.ddd` | Domain-driven design utilities and patterns |
| `flower.test` | Testing utilities and base classes |
| `flower.sample` | Example applications demonstrating usage patterns |

### Message Flow Sequence

```
1. Client → FlowRouter (message channel)
2. FlowRouter → ServiceActor[service1]
3. ServiceActor[service1] → Service.process(message)
4. Return value → Message → ServiceActor[service2]
5. Repeat until flow completion
```

### Key Classes in flower.core

- `Service<P, R>`: Core service contract (functional interface)
- `FlowerService`: Marker interface extended by `Service`
- `ServiceFactory`: Loads services and manages registration
- `ServiceFlow`: Builds and manages service orchestration (DAG)
- `ServiceActor`: Pekko Actor that wraps and invokes a service
- `FlowRouter`: Creates concurrent message channels for a flow
- `ServiceContext`: Provides runtime context (transaction ID, attachments, web context)

### Flow Initialization Sequence

1. `FlowerFactory` initializes and creates `ServiceFactory`
2. Services are registered via `@FlowerService` annotation scanning or `.services` files
3. `ServiceFlow` builds flow definitions from `.flow` files or programmatically
4. `ServiceActorFactory` creates actor routers (pools) for each service
5. `FlowRouter` creates message channels for concurrent flow processing

### Distributed Deployment

- `flower.center` runs as a standalone registry service
- Business services register themselves via `Registry` SPI
- Gateway services orchestrate flows across multiple service nodes
- Remote actors handle cross-node message passing using Pekko remote

## Configuration

Flower uses `flower.yml` for configuration:
```yaml
name: "ServiceName"
host: "127.0.0.1"
port: 25003
basePackage: com.example.service
registry:
  - url: "flower://registry-host:8096?application=AppName"
```

### Service Definition Files (`.services`)
```
serviceName = com.example.MyService
```

### Flow Definition Files (`.flow`)
```
serviceA -> serviceB
serviceA -> serviceC
serviceB -> serviceD
serviceC -> serviceD
```

## Development Conventions

### Code Style
- Checkstyle configuration: `conf/flower-checkstyle.xml`
- 4-space indentation
- Maximum line length: 120 characters

### Licensing
- All `.java` files require Apache License 2.0 header
- Run `./mvnw license:format` to auto-add/update headers

### Testing Stack
- JUnit 4 for tests
- Mockito for mocking
- Awaitility for async assertions
- Logback for test logging

## Technology Stack

- **Java**: 1.8 minimum
- **Maven**: 3.0+
- **Actor System**: Apache Pekko 1.1.4 (Scala 2.13)
- **Serialization**: Hessian 4.0.60, Protostuff 1.5.2, FastJSON 1.2.83, FastJSON2 2.0.57
- **Web**: Jetty 9.4.57, Servlet 4.0.1
- **Database**: MySQL 8.x, Druid 1.0.12, MyBatis 3.5.6
- **Distributed Coordination**: Redisson 3.22.0 (Redis), ZooKeeper via registry plugins