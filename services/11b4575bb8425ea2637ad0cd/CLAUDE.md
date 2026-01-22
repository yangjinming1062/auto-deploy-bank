# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Oracle Coherence Community Edition is a scalable, fault-tolerant, distributed in-memory data grid. It provides a `Map<K,V>` interface implementation where data is partitioned across cluster nodes. Key capabilities include:
- Distributed caching with queries, aggregations, and map/reduce processing
- PartitionedService for data partitioning across cluster nodes
- InvocationService for running tasks on cluster members
- Pub/sub messaging via distributed Topics
- Repository API for Domain-Driven Design patterns
- Coherence-concurrent: distributed coordination primitives (Atomics, Executors, Locks)
- Polyglot client support (C++, .NET, JavaScript, Go, Python)

## Build Commands

```bash
# Build all modules with tests
cd prj && mvn clean install

# Build without tests
mvn clean install -DskipTests

# Build coherence.jar only (without -Pmodules)
mvn -am -pl coherence clean install -DskipTests

# Build specific module with dependencies and tests
mvn -Pmodules -am -pl test/functional/persistence clean verify

# Build coherence.jar skipping TDE compilation
mvn -am -pl coherence clean install -DskipTests -Dtde.compile.not.required
```

## Test Commands

```bash
# Run unit tests for a specific module
cd prj && mvn test -pl coherence-core

# Run a single test class
mvn test -pl coherence-core -Dtest=ClassNameTest

# Run a single test method
mvn test -pl coherence-core -Dtest=ClassNameTest#testMethodName

# Run integration tests
mvn failsafe:integration-test -pl coherence

# Run tests with static lambda validation
mvn -Pmodules test -Dcoherence.lambdas=static

# Run tests with security manager
mvn test -Psecurity-manager

# Run with production mode
mvn test -Ptest-production-mode

# Enable code coverage
mvn test -Dcode.coverage.enabled=true
```

## Architecture

### Core Module Structure

- **coherence-core**: Low-level clustering, data partitioning, storage, and network protocols
- **coherence-core-21**: Java 21+ specific optimizations
- **coherence-core-24**: Java 24+ specific optimizations
- **coherence-core-components**: TDE-based (Tangosol Data Engine) compiled components
- **coherence**: Main shaded JAR that bundles all core modules
- **coherence-grpc**: gRPC service for polyglot access
- **coherence-cdi**: CDI integration for microservices
- **coherence-concurrent**: Distributed concurrent utilities
- **coherence-json**: JSON serialization support
- **coherence-protobuf**: Protocol Buffers support
- **coherence-jcache**: JCache (JSR-107) implementation
- **coherence-lucene**: Lucene indexing for queries

### Key Packages

- `com.tangosol.net`: Cluster service, CacheFactory, NamedMap, NamedCache interfaces
- `com.tangosol.internal.net`: BackingMap, storage implementations
- `com.tangosol.util`: Query filters, aggregators, entry processors
- `com.oracle.coherence.repository`: Repository API implementation
- `com.oracle.coherence.concurrent`: Distributed concurrency primitives

### Critical Services

1. **Cluster Service (Service 0)**: Maintains cluster membership, handles member death detection
2. **PartitionedService**: Manages data partitioning across storage-enabled members
3. **InvocationService**: Runs tasks on specific cluster members
4. **ProxyService**: Provides network access for extend clients

## Code Conventions

### File Structure
Single public class per file. Structure: package → imports → Javadoc → class declaration with sections separated by `//----- -----` comments.

### Naming Conventions (Intent Prefixes)

| Prefix | Type | Example |
|--------|------|---------|
| `f` | boolean flag | `fReady` |
| `n` | number | `nCount` |
| `c` | counter | `cItems` |
| `i` | index | `iIndex` |
| `s` | string | `sName` |
| `map` | Map | `mapConfig` |
| `list` | List | `listItems` |
| `set` | Set | `setKeys` |
| `a` | array | `aItems` (followed by type prefix) |
| `e` | exception | `e` or `t` |
| `bin` | Binary | `binKey` |
| `binEntry` | BinaryEntry | `binEntry` |
| `proc` | Processor | `proc` |
| `incptr` | EventInterceptor | `incptr` |

### Member Variables
- Instance mutable: `m_` prefix (e.g., `m_mapCache`)
- Static mutable: `s_` prefix
- Instance final: `f_` prefix
- Static final: `CONSTANT_NAME` (all caps with underscores)

### Braces and Spacing
- 4 spaces for block indentation
- Control structures (`if`, `for`, `while`) require braces even for single statements
- Space after control keywords: `if (condition)` not `if(condition)`
- Line length: 120 characters max (78 for older code)
- Assignment operators aligned horizontally: `int i = 0; String s = "x";`

### Important Restrictions
- Never use Java's interruptible methods (`Thread.sleep`, `Object.wait`, `Lock.lockInterruptibly`); use `com.oracle.coherence.common.base.Blocking` instead
- Avoid nested lambdas (breaks remoting support)
- Use `@Override` annotation for non-obvious method overrides

### File Headers
```java
/*
 * Copyright (c) 2000, 2025, Oracle and/or its affiliates.
 *
 * Licensed under the Universal Permissive License v 1.0 as shown at
 * http://oss.oracle.com/licenses/upl.
 */
```

## Development Notes

### Remote Lambdas
Coherence supports serializable lambdas (`Remote<T>` interface) for execution on remote nodes. Nested lambdas are prohibited as they break remoting. Extract inner lambdas to local variables.

### TDE (Tangosol Data Engine)
Legacy component system using `.cdb` files. See `DEV-GUIDELINES.md` TDE section for IDE setup.

### Profile Structure
- `coherence` profile: Always active, builds core modules
- `modules` profile: Builds extended functionality (must run separately after coherence profile)
- `IntelliJ` profile: IDE-specific module set
- `stage1-14`: Test segmentation profiles for parallel CI execution

### Java Version
Requires JDK 17+. CI runs on JDK 24. Use Helidon 3 for Java < 21.