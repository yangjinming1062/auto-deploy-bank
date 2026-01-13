# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Reference

**Project Type**: Java (Maven) - Redis/Valkey Java Client and Real-Time Data Platform

**Main Entry Point**: `org.redisson.Redisson` - factory class with static `create()` methods

**Current Version**: 3.52.1-SNAPSHOT

## Common Commands

### Build & Test
```bash
# Build project without tests
mvn clean verify -DskipTests

# Build project with tests
mvn clean verify

# Run all tests
mvn test

# Run single test class
mvn test -Dtest=RedissonAtomicLongTest

# Run specific test method
mvn test -Dtest=RedissonAtomicLongTest#testSetIfAbsents

# Run tests with unit-test profile (enables tests)
mvn test -P unit-test

# Run checkstyle validation
mvn checkstyle:check

# Compile only
mvn compile

# Package JAR
mvn package
```

**Prerequisites for testing**:
- Docker must be running
- Redis/Valkey instances are spawned automatically by tests (no manual setup needed)
- JDK 21 required for building (source compatibility: JDK 8+, test compatibility: JDK 21)

## Architecture Overview

### Multi-Module Structure
```
redisson-parent (pom)
├── redisson                    # Core module - main Java client
├── redisson-all               # Aggregator artifact
├── redisson-spring-data       # Spring Data Redis integration
├── redisson-spring-boot-starter
├── redisson-hibernate         # Hibernate cache integration
├── redisson-micronaut         # Micronaut integration
├── redisson-quarkus           # Quarkus integration
├── redisson-helidon           # Helidon integration
├── redisson-tomcat           # Tomcat session manager
└── redisson-mybatis          # MyBatis cache integration
```

### Core Architecture

**Main Components**:

1. **Connection Layer** (`org.redisson.connection`)
   - Manages connections to Redis/Valkey
   - Supports multiple deployment modes: Single, Cluster, Sentinel, Master-Slave, Replicated
   - Built on Netty for asynchronous I/O

2. **Client API** (`org.redisson.client`)
   - Protocol handling and command encoding/decoding
   - Multiple codec implementations (Kryo, Jackson, Protobuf, etc.)

3. **Distributed Objects** (`org.redisson`)
   - **Collections**: RMap, RSet, RList, RQueue, RDeque, RSortedSet, RScoredSortedSet, RBitSet
   - **Locks**: RLock, RFairLock, RReadWriteLock, RRedLock, RMultiLock
   - **Counters**: RAtomicLong, RAtomicDouble, RLongAdder, RDoubleAdder
   - **Services**: RRemoteService, RExecutorService, RSchedulerService
   - **Other**: RBucket, RBloomFilter, RHyperLogLog, RGeospatial, RStream

4. **API Variants**
   - **Synchronous/Asynchronous**: Main `RedissonClient` interface with `RFuture` return types
   - **Reactive**: Project Reactor-based (`RedissonReactiveClient`)
   - **RxJava3**: Observable-based (`RedissonRxClient`)

5. **Configuration** (`org.redisson.config`)
   - Central `Config` class
   - Type-safe configuration builders for each deployment mode
   - Supports YAML/JSON parsing via `Config.fromYAML()` / `Config.fromJSON()`

6. **Spring Integration** (`org.redisson.spring`)
   - Spring Cache abstraction
   - Spring Session management
   - Spring Transaction support
   - Spring Data Redis integration

7. **Live Objects** (`org.redisson.liveobject`)
   - Entity persistence with automatic field mapping to Redis
   - Interceptors for field access/mutation

### Key Packages

- `org.redisson.api` - Public API interfaces
- `org.redisson.client` - Low-level Redis protocol client
- `org.redisson.codec` - Serialization codecs (Kryo, Jackson, etc.)
- `org.redisson.command` - Command execution layer
- `org.redisson.misc` - Utility classes
- `org.redisson.pubsub` - Publish/subscribe implementation
- `org.redisson.reactive` - Reactive API implementation
- `org.redisson.rx` - RxJava3 API implementation
- `org.redisson.transaction` - Transaction support

### Configuration Patterns

```java
// Single server
Config config = new Config();
config.useSingleServer().setAddress("redis://127.0.0.1:6379");

// Cluster
config.useClusterServers().addNodeAddress("redis://127.0.0.1:7181");

// Sentinel
config.useSentinelServers()
    .setMasterName("mymaster")
    .addSentinelAddress("redis://127.0.0.1:26379");

// From YAML
Config config = Config.fromYAML(new File("config.yaml"));
```

### Connection Modes

- **Single** - Single Redis/Valkey node
- **Cluster** - Redis/Valkey cluster
- **Sentinel** - Redis Sentinel for high availability
- **Master-Slave** - Manual master-slave setup
- **Replicated** - Redis/Valkey replicated mode
- **Multi-Cluster** - Multiple clusters
- **Multi-Sentinel** - Multiple sentinel groups
- **Proxy** - Proxy mode

### API Usage Patterns

```java
// Create client
RedissonClient redisson = Redisson.create(config);

// Get distributed objects
RMap<String, String> map = redisson.getMap("myMap");
RLock lock = redisson.getLock("myLock");
RAtomicLong counter = redisson.getAtomicLong("myCounter");

// Reactive API
RedissonReactiveClient reactive = redisson.reactive();
RMapReactive<String, String> reactiveMap = reactive.getMap("myMap");

// RxJava3 API
RedissonRxClient rx = redisson.rxJava();
RMapRx<String, String> rxMap = rx.getMap("myMap");
```

## Development Notes

### Code Style
- Checkstyle configuration in `checkstyle.xml`
- License headers required in all Java files (Apache 2.0)
- Runs automatically during `mvn verify`

### Testing Framework
- JUnit Jupiter (JUnit 5)
- Testcontainers for Redis/Valkey instances
- AssertJ for assertions
- ~2000+ unit tests

### Dependencies
- **Netty** - Network transport layer
- **Reactor** - Reactive streams support
- **Jackson** - JSON processing
- **JCache API** - Cache abstraction

### Breaking Changes
Recent releases have breaking changes - see CHANGELOG.md for details. Notable changes include:
- Method renames in vector similarity APIs
- CredentialsResolver API changes
- Various parameter renames

## Important Files

- `pom.xml` - Parent POM with plugin management
- `redisson/pom.xml` - Core module dependencies
- `checkstyle.xml` - Code style rules
- `header.txt` - License header template
- `CHANGELOG.md` - Version history and breaking changes
- `.github/workflows/maven.yml` - CI build configuration

## Documentation Links

- Getting Started: `docs/getting-started.md`
- Configuration: Full docs at https://redisson.org/docs/configuration/
- Objects & Collections: https://redisson.org/docs/data-and-services/
- Spring Integration: `docs/microservices-integration.md`

## Module-Specific Notes

### redisson
Core Java client - modify this for Redis/Valkey protocol changes, distributed object implementations, connection management.

### redisson-spring-data
Integration with Spring Data Redis - versioned subdirectories for different Spring Boot/Data versions.

### redisson-spring-boot-starter
Auto-configuration for Spring Boot applications.

### Other Integration Modules
- `redisson-hibernate` - Versions for Hibernate 4, 5, 52, 53, 6, 7
- `redisson-quarkus` - Versions for Quarkus 1.6, 2.0, 3.0 (with cache/CDI submodules)
- `redisson-micronaut` - Versions for Micronaut 2.0, 3.0, 4.0
- `redisson-helidon` - Versions for Helidon 2.0, 3.0, 4.0
- `redisson-tomcat` - Versions for Tomcat 7, 8, 9, 10, 11