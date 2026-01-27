# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hazelnut Hydra (Bean Nuts Pinecone Hydra) is a distributed operating system and large-scale data analysis platform. It provides a PB-level data warehouse, knowledge base, search engine, and distributed crawler framework. The system is written in Java 11+ and built with Maven.

## Build Commands

```bash
# Build entire project
mvn clean install -DskipTests

# Build specific module
mvn clean install -pl Pinecones/Pinecone -DskipTests

# Run tests
mvn test

# Run single test class
mvn test -Dtest=UniTrieMaptronTest

# Package without running tests
mvn package -DskipTests
```

## Architecture

The project is organized into several core subsystems:

### Pinecones (基础运行支持库)
Foundation layer providing data structures and utilities:
- `Pinecone/` - Core utilities including custom collections (LinkedTreeMap, ScopeMap, TrieMap, MultiMap)
- `Slime/` - Big data support framework with block abstraction and mapper/querier systems
- `Summer/` - JSON/BSON libraries with customizable encoders/decoders
- `Ulfhedinn/` - Third-party API SDK wrappers

### Hydra (分布式操作系统框架)
Core distributed system framework:
- `hydra-architecture/` - System skeleton, kernel objects, distributed components
- `hydra-framework-runtime/` - Runtime support and component lifecycle management
- `hydra-framework-service/` - Service orchestration and task scheduling
- `hydra-framework-config/` - Distributed configuration registry (like Apollo)
- `hydra-framework-storage/` - Volume system and distributed file system (UOFS)
- `hydra-message-control/` - RPC framework (WolfMC) based on Netty
- `Radium/` - Crawler orchestration entry point (`Radium.java` is main class)

### Saurons (分布式爬虫框架)
Distributed crawler engine:
- `sauron-core/` - Core crawler framework
- `Shadow/` - Example search engine and crawler applications
- `Heistotron/` - Main heist (crawling task) implementations
- `Saurye/` - Data processing pipeline

### Sparta (中台服务组)
Middleware service group:
- `sparta-core-console/` - Core console services
- `sparta-api-uac/` - User authentication center API
- `sparta-api-uofs/` - Distributed file system API
- `sparta-ucdn-service/` - CDN service
- `sparta-uofs-service/` - File system service

### Walnuts (图形界面系统)
Graphical interface interaction system:
- `redstone-core/` - Core UI framework
- `sailor-stream-distribute-sdk/` - Distribution SDK

## Key Conventions

### Configuration
- JSON5 format used for all configuration files (`.json5` extension)
- Main configuration directory: `./system/setup/`
- System config: `./system/setup/config.json5`
- Heist (crawler) config: `./system/setup/heist.json5`
- Individual heist tasks: `./system/setup/heists/*.json5`

### Entry Points
- `Radium.java` (`Hydra/Radium/src/main/java/com/pinecone/radium/Radium.java`) - Main system bootstrap
- `MasterServgramOrchestrator.java` - Task/orchestration manager
- Configuration via command-line args: `--workingPath=...` and `--config=...`

### System Hierarchy
The system supports multiple service architectures:
- `H_MASTER` - Top-level master node
- `H_PALADIN` - Secondary master/worker
- `H_SLAVE` - Worker/slave node

### RPC and Messaging
- WolfMC RPC based on Netty supports JSON, BSON, and Protobuf
- Dual-channel duplex communication
- MessageExpress for Spring Controller-style messaging
- RabbitMQ integration for messaging

### Data Structures
- Custom collections in `com.pinecone.framework.unit` package
- `UniTrieMaptron` - Trie-based path map (e.g., `/a/b/c` keys)
- `ScopeMap` - Multi-scope lookup tree supporting inheritance
- `MultiScopeMap` - Multi-domain scoped maps

### Package Naming
- `com.pinecone.*` - Core framework
- `com.pinecone.hydra.*` - Distributed system
- `com.pinecone.radium.*` - Crawler orchestration
- `com.sauron.*` - Crawler implementations
- `com.pinecone.hydra.servgram.*` -小程序 (servgram/task orchestration) system

### Testing
- JUnit Jupiter (JUnit 5) for tests
- Test files located in `src/test/java/`
- Example: `UniTrieMaptronTest.java` demonstrates testing patterns