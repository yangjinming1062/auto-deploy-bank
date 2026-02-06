# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hyperledger Besu is an Apache 2.0 licensed, MainNet-compatible Ethereum client written in Java. It implements the Ethereum JSON-RPC API and supports multiple consensus mechanisms (IBFT 2.0, QBFT, Clique).

**Key Technologies:**
- Java 21+ required to build
- Gradle build system with multi-module structure
- Dagger for dependency injection
- Vert.x for async networking
- RocksDB for storage

## Build Commands

```bash
# Standard build (includes spotlessCheck, build, checkLicense, javadoc)
./gradlew build

# Development build (applies spotless fixes first)
./gradlew dev

# Run unit tests
./gradlew test

# Run a single test
./gradlew :ethereum:core:test --tests "ClassName.methodName"

# Run integration tests (must have src/integration-test source set)
./gradlew integrationTest

# Run reference tests (Ethereum spec tests)
./gradlew referenceTests

# Run reference tests for a specific hardfork (e.g., Prague)
./gradlew referenceTests --tests "*ExecutionSpec*_prague_*"

# Run reference tests for a specific EIP
./gradlew referenceTests --tests "*eip7702*"

# Run devnet/pre-release reference tests
./gradlew referenceTestsDevnet

# Run JMH benchmarks
./gradlew :ethereum:core:jmh

# Run specific benchmark with filter
./gradlew :ethereum:core:jmh -Pincludes=SomeBenchmark

# Format code with Spotless
./gradlew spotlessApply

# Check code formatting
./gradlew spotlessCheck

# Build distribution (tar.gz and zip)
./gradlew distTar distZip

# Build Docker image
./gradlew distDocker

# Check for plugin API changes
./gradlew checkPluginAPIChanges
```

**Test Filtering for Reference Tests:**
- By hardfork: `--tests "*ExecutionSpecStateTest_cancun_*"`
- By EIP: `--tests "*eip4844*"`
- Combined: `--tests "*_prague_eip2537_*"`

**Performance Options:**
```bash
# Increase heap for memory-intensive tests
./gradlew referenceTests -Dorg.gradle.jvmargs="-Xmx8g"

# Control parallel test forks (default: half available processors)
GRADLE_MAX_TEST_FORKS=4 ./gradlew test

# Enable block tracing for debugging
./gradlew test -Dbesu.debug.traceBlocks=true
```

## Architecture

### Module Structure

```
besu (root)
├── app                    # CLI entry point, BesuCommand, logging configuration
├── config                 # Configuration parsing (TOML, CLI args)
├── crypto                 # Cryptographic operations (signatures, BLS)
├── datatypes              # Base data types (U256, UInt256, Hash)
├── ethereum
│   ├── api              # JSON-RPC API endpoints and handlers
│   ├── blockcreation    # Block proposal and transaction selection
│   ├── core             # EVM, state, blocks, transaction processing
│   ├── eth              # Ethereum wire protocol (p2p sync)
│   ├── evmtool          # Standalone EVM debugging tool
│   ├── p2p              # Peer-to-peer networking (RLPx, discovery)
│   ├── permissioning    # Node and account permissioning
│   ├── referencetests   # Ethereum spec test runners
│   ├── rlp              # RLP encoding/decoding
│   ├── trie             # Merkle Patricia Trie implementation
│   └── verkletrie       # Verkle trie for future state expansion
├── consensus
│   ├── clique          # Aura consensus (legacy)
│   ├── ibft            # IBFT 2.0 consensus
│   ├── qbft            # QBFT consensus
│   ├── common          # Consensus interfaces and utilities
│   └── merge           # Merge (PoS) consensus transition
├── evm                  # EVM implementation (opcodes, precompiles)
├── metrics              # Metrics collection (RockDB, Micrometer)
├── nat                  # NAT detection (UPnP, etc.)
├── platform             # Version and dependency BOM
├── plugin-api           # Plugin interface for extensions
├── plugins              # Plugins (e.g., RocksDB)
├── services
│   ├── kvstore         # Key-value storage abstractions
│   ├── pipeline        # Block processing pipeline
│   └── tasks           # Async task framework
├── testfuzz             # Fuzz testing infrastructure
├── testutil             # Test utilities
└── util                 # General utilities
```

### Key Entry Points

- **Main:** `org.hyperledger.besu.Besu` - Bootstrap class using Dagger DI
- **CLI:** `org.hyperledger.besu.cli.BesuCommand` - PicoCLI command implementation
- **EVM:** `org.hyperledger.besu.evm` - EVM implementation
- **State:** `org.hyperledger.besu.ethereum.core.WorldState` - Ethereum state

### Plugin System

Plugins implement `org.hyperledger.besu.plugin.BesuPlugin` and are discovered via Java ServiceLoader. Plugins receive a `ServiceManager` context during registration and must implement:
- `register(ServiceManager)` - Early initialization
- `start()` - Begin operation after external services start
- `stop()` - Cleanup on shutdown

## Code Style

- **Formatting:** Google Java Format (via Spotless plugin)
- **License Headers:** Apache 2.0 with "SPDX-License-Identifier"
- **Imports:** Order: `org.hyperledger`, `java`, empty line
- **Error Prone:** Custom checks enabled; some warnings converted to errors
- **Null Handling:** Uses JSR-305 annotations (`@Nullable`, `@NotNull`)

## Development Notes

### Dependency Injection

The project uses Dagger. Component classes follow the pattern `DaggerBesuComponent` generated from `BesuComponent`.

### Storage

- **World State:** Merkle Patricia Trie (in `ethereum:trie`)
- **Key-Value:** RocksDB abstraction layer (in `services:kvstore`, `plugins:rocksdb`)

### Networking

- P2P protocol implemented with Vert.x and Netty
- RLPx handshake and encrypted communication
- DiscV5 for node discovery

### Consensus Types

- **IBFT 2.0:** Finality-focused BFT consensus
- **QBFT:** QBFT variant of BFT
- **Clique:** Proof-of-Authority (Ethereum mainnet default pre-merge)
- **Merge:** Proof-of-Stake transition (after The Merge)

## Testing Notes

- Tests use JUnit 5 (`@ExtendWith`, `@Nested` patterns common)
- Mockito for mocking
- AssertJ for assertions
- Acceptance tests use DSL in `acceptance-tests:dsl`
- Reference tests run against official Ethereum test vectors

## DCO Sign-off

All commits must include a DCO sign-off. Use `git commit -s` to add it automatically.