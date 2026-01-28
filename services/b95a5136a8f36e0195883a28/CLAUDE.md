# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Build jar
./gradlew jar

# Run tests
./gradlew test                    # runs both unit and integration tests
./gradlew unitTest
./gradlew integrationTest
./gradlew test -Pkafka.test.run.flaky=true  # runs flaky tests

# Run specific test
./gradlew clients:test --tests RequestResponseTest
./gradlew streams:integration-tests:test --tests RestoreIntegrationTest
./gradlew core:test --tests kafka.api.ProducerFailureHandlingTest.testCannotSendToInternalTopic

# Force re-run tests without code change
./gradlew test --rerun-tasks

# Code quality checks
./gradlew checkstyleMain checkstyleTest spotlessCheck
./gradlew spotbugsMain spotbugsTest -x test

# Fix formatting
./gradlew spotlessApply

# Build binary release
./gradlew clean releaseTarGz

# Build documentation
./gradlew aggregatedJavadoc --no-parallel
./gradlew javadoc
./gradlew scaladoc
```

## Architecture Overview

Apache Kafka is a distributed event streaming platform with these main components:

### clients/
Pure Java client library for Kafka producers, consumers, and admin operations. Handles network communication, serialization, and protocol messaging. Minimum Java 11.

### core/
Scala-based broker implementation. Key packages:
- **server/** - Broker startup (KafkaBroker, BrokerServer), request handling (KafkaApis), and core services
- **network/** - SocketServer for handling client connections, RequestChannel for request processing
- **log/** - LogManager, partition logs, segment management, and storage
- **cluster/** - Partition and replica management
- **coordinator/** - Group and transaction coordination (GroupCoordinator, TransactionCoordinator)
- **raft/** - KRaft consensus protocol implementation (replacing ZooKeeper)

### streams/
Kafka Streams API for building stream processing applications. Pure Java with minimum Java 11. KStream, KTable, and state store abstractions.

### connect/
Kafka Connect framework for integrating with external systems. Submodules:
- **api/** - Connect API definitions
- **runtime/** - Connect worker and task execution
- **file/** - File source/sink connectors
- **json/** - JSON conversion
- **transforms/** - Built-in transformations

### server/
Core server components written in Java:
- **replica/** - Replica management and fetch operations
- **partition/** - Partition leadership and ISR management
- **quota/** - Client quota enforcement
- **purgatory/** - Delayed request handling (DelayedProduce, DelayedFetch)
- **config/** - Dynamic configuration management
- **metrics/** - Server-side metrics
- **share/** - Share group support for simplified consumer coordination

### metadata/
KRaft controller implementation handling cluster metadata management.

### raft/
Raft consensus protocol implementation used by KRaft mode for leader election and metadata management.

### server-common/, coordinator-common/, group-coordinator/
Shared utilities across server components.

## Important Notes

- **Java Version**: Java 17+ required for core development. Clients and streams modules target Java 11.
- **Scala Version**: Only Scala 2.13 is supported.
- **Protocol Definitions**: Message protocols are defined in JSON files at `clients/src/main/resources/common/message/`. Run `./gradlew processMessages processTestMessages` to regenerate code.
- **Header Required**: All source files must include the ASF license header. Run `./gradlew spotlessApply` to fix.
- **Checkstyle**: Enforces consistent coding style. Build will fail if checkstyle fails.