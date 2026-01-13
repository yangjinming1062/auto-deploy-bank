# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Apache Dubbo is a high-performance, Java-based open-source RPC framework. The codebase is a Maven multi-module project with 19 core modules providing transparent interface-based RPC, intelligent load balancing, automatic service registration and discovery, and visualized service governance.

## Development Commands

### Build and Test
- **Build entire project**: `mvn clean install` (requires Java 1.8)
- **Run tests**: `mvn clean test`
- **Run single test class**: `mvn test -Dtest=TestClassName`
- **Run specific test method**: `mvn test -Dtest=TestClassName#testMethod`
- **Build specific module**: `cd dubbo-<module> && mvn clean install`
- **Run checkstyle**: `mvn checkstyle:check` (using codestyle/checkstyle.xml)
- **Skip tests during build**: `mvn clean install -DskipTests`

### Code Style Configuration
- Import IntelliJ code style: `codestyle/dubbo_codestyle_for_idea.xml`
- Line length limit: 120 characters
- Checkstyle config: `codestyle/checkstyle.xml`
- Checkstyle suppressions: `codestyle/checkstyle-suppressions.xml`

## Architecture

The project follows a layered architecture with clear separation of concerns:

### Core Modules
- **dubbo-common**: Common utilities, thread local, timer, serialization utilities
- **dubbo-rpc**: RPC core APIs (Invoker, Protocol, Exporter, Invocation, Result), filter chain, proxy
- **dubbo-remoting**: Network transport layer (Netty, HTTP, gRPC implementations)
- **dubbo-cluster**: Cluster management (load balancing, routing, directory, configurator, merger)
- **dubbo-registry**: Service registry implementations (Zookeeper, Consul, etc.)
- **dubbo-config**: Configuration layer (ApplicationConfig, RegistryConfig, ServiceConfig, ReferenceConfig)
- **dubbo-metadata**: Service metadata reporting and retrieval
- **dubbo-serialization**: Serialization protocols (Hessian, JSON, Kryo, Protobuf, etc.)
- **dubbo-filter**: Filter implementations (validation, caching)
- **dubbo-monitor**: Monitoring and metrics
- **dubbo-container**: Standalone container for running Dubbo services
- **dubbo-plugin**: Extension plugin system
- **dubbo-compatible**: Backward compatibility layer
- **dubbo-spring-boot**: Spring Boot integration

### RPC Flow
1. **Provider**: Exposes services via `ServiceConfig` → `Protocol` → `Exporter`
2. **Consumer**: References services via `ReferenceConfig` → `Cluster` → `Directory` → `Invoker`
3. **Transport**: `dubbo-remoting` handles network communication
4. **Cluster**: `dubbo-cluster` provides load balancing, routing, failover
5. **Registry**: `dubbo-registry` manages service discovery

### Key Extension Points
- **Protocol**: `org.apache.dubbo.rpc.Protocol` - service export/import
- **Invoker**: `org.apache.dubbo.rpc.Invoker` - service invocation
- **Filter**: `org.apache.dubbo.rpc.Filter` - intercept RPC calls
- **Router**: `org.apache.dubbo.rpc.cluster.router.Router` - request routing
- **LoadBalance**: `org.apache.dubbo.rpc.cluster.LoadBalance` - load balancing strategy
- **Registry**: `org.apache.dubbo.registry.Registry` - service registry
- **Serialization**: `org.apache.dubbo.common.serialize.Serialization` - data serialization

## Development Guidelines

### Code Conventions (from CONTRIBUTING.md)
- All new files must include ASF license header
- Add Javadoc class comments with at least @date tag
- No @author tags (use Git for attribution)
- Provide sufficient unit tests for new features
- Maximum line length: 120 characters

### Testing
- Framework: JUnit Jupiter (junit-jupiter)
- Mocking: Mockito
- Assertions: Hamcrest
- Test location: `src/test/java/`

### Profiles
- **checkstyle**: Enables checkstyle validation (`mvn -Pcheckstyle`)
- **sources**: Generates source JARs (`mvn -Psources`)
- **release**: Release profile with Javadoc and GPG signing
- **licenseCheck**: Validates third-party licenses

## CI/CD
- **Jenkins**: Nightly builds at 2:00 and 14:00 CST
- **GitHub Actions**: Build and test workflow (see .github/workflows/)
- **Requirements**: Java 1.8, Maven 3.x

## Useful Resources
- [Developer Guide](https://dubbo.apache.org/docs/v2.7/dev/build/)
- [User Manual](https://dubbo.apache.org/docs/v2.7/user/preface/background/)
- [Samples](https://github.com/apache/dubbo-samples)
- [Mailing List](mailto:dev@dubbo.apache.org)