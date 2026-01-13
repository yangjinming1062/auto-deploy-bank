# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Apache Curator is a Java/JVM client library for Apache ZooKeeper, a distributed coordination service. It provides a high-level API framework and utilities to make using ZooKeeper much easier and more reliable.

## Build System

This is a Maven-based multi-module project (Java 8+). Use Maven commands for all build operations:

- **Full build**: `mvn clean install`
- **Build without tests**: `mvn clean install -DskipTests`
- **Run all tests**: `mvn test`
- **Run tests for specific module**: `mvn test -pl curator-framework`
- **Run single test class**: `mvn test -Dtest=BasicTests`
- **Run single test method**: `mvn test -Dtest=BasicTests#testExpiredSession`
- **Format code**: `mvn spotless:check` (fails if formatting issues)
- **Apply formatting**: `mvn spotless:apply`
- **Generate JavaDoc**: `mvn javadoc:javadoc`

The project uses Spotless with Palantir Java Format for code formatting (version 2.38.0). All code must pass Spotless checks before merging.

## Module Architecture

The project is structured into several modules that build upon each other:

### Core Modules

**curator-client** (`curator-client/`)
- Low-level ZooKeeper client abstractions
- Connection management, retry logic, and session handling
- Base utilities like `CuratorZookeeperClient`, `RetryPolicy` implementations
- Dependencies: ZooKeeper, SLF4J

**curator-framework** (`curator-framework/`)
- High-level API that wraps curator-client
- Main entry point: `CuratorFramework` interface and `CuratorFrameworkFactory`
- Provides fluent builder API for client configuration
- Exports: `org.apache.curator.framework.*`

**curator-recipes** (`curator-recipes/`)
- Implementation of common ZooKeeper recipes/patterns
- Includes: Leader Election, Distributed Locks, Barriers, Counters, Caches, etc.
- Built on top of curator-framework
- Exports: `org.apache.curator.framework.recipes.*`

### Extensions

**curator-x-async** (`curator-x-async/`)
- Java 8+ asynchronous DSL for Curator operations
- Provides reactive-style API for ZooKeeper operations

**curator-x-discovery** (`curator-x-discovery/`)
- Service discovery framework built on Curator
- Allows services to register and discover each other via ZooKeeper

**curator-x-discovery-server** (`curator-x-discovery-server/`)
- REST-based service discovery server
- Provides HTTP API for service discovery

### Testing & Examples

**curator-test** (`curator-test/`)
- Testing utilities and base test classes
- Includes `BaseClassForTests` for integration testing with embedded ZooKeeper
- Test helpers and timing utilities

**curator-test-zk35/36/37/38** (`curator-test-zk*/`)
- ZooKeeper version-specific compatibility tests
- Ensures Curator works across different ZooKeeper versions

**curator-examples** (`curator-examples/`)
- Working example code for all major Curator features
- Includes examples for: async operations, caching, discovery, leader election, locking, pub-sub, modeled APIs

### Dependency Chain

```
curator-client ← curator-framework ← curator-recipes
                            ↓
                    curator-x-async, curator-x-discovery
```

## Key Dependencies

- **ZooKeeper**: 3.9.3
- **JUnit**: 5.6.2 (Jupiter)
- **AssertJ**: 3.23.1
- **SLF4J**: 1.7.25 (logging)
- **Guava**: 32.0.0-jre (shaded in final JARs)
- **Jackson**: 2.18.1 (JSON processing)
- **Awaitility**: 4.1.1 (async testing)
- **Spotless**: 2.39.0 (code formatting)

## Important Code Locations

### Main Entry Points

- `curator-framework/src/main/java/org/apache/curator/framework/CuratorFramework.java` - Main client interface
- `curator-framework/src/main/java/org/apache/curator/framework/CuratorFrameworkFactory.java` - Client factory and builder

### Recipes

- `curator-recipes/src/main/java/org/apache/curator/framework/recipes/locks/` - Distributed locks
- `curator-recipes/src/main/java/org/apache/curator/framework/recipes/leader/` - Leader election
- `curator-recipes/src/main/java/org/apache/curator/framework/recipes/cache/` - Caching utilities
- `curator-recipes/src/main/java/org/apache/curator/framework/recipes/barriers/` - Barriers and barriers

### Testing

- `curator-test/src/main/java/org/apache/curator/test/BaseClassForTests.java` - Base test class with embedded ZooKeeper
- `curator-test/src/main/java/org/apache/curator/test/Timing.java` - Test timing utilities

## Development Notes

- All modules use OSGi bundle packaging for modularity
- Guava is shaded to avoid version conflicts with downstream apps
- Tests use JUnit 5 (Jupiter) with AssertJ assertions
- Test output is redirected to files by default (`redirectTestOutputToFile=true`)
- Surefire runs with single-threaded execution (`threadCount=1`, `reuseForks=false`)
- Java 9+ requires `--add-opens` flags for certain packages (configured in pom.xml)
- CLIRR plugin checks for binary compatibility across releases
- Jersey 1.x is used (upgrading to 2.x is complex and provides unclear benefits)

## Example Usage Patterns

Creating a client:
```java
CuratorFramework client = CuratorFrameworkFactory.newClient(
    connectString,
    retryPolicy
);
client.start();
```

Working with recipes:
```java
InterProcessMutex lock = new InterProcessMutex(client, lockPath);
lock.acquire();
// do work
lock.release();
```

See `curator-examples/` directory for comprehensive examples of all features.

## Important Files

- Root `pom.xml` - Main build configuration, dependency management, Spotless setup
- `curator-examples/src/main/java/pubsub/README.md` - Detailed example of pub-sub pattern using modeled APIs
- `asf.yaml` - GitHub workflow configuration for Apache Foundation
- `licenserc.toml` - License header configuration