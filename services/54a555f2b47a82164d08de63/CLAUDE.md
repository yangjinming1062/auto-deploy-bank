# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AsyncHBase is an alternative, fully asynchronous, non-blocking, thread-safe Java HBase client library. Unlike the standard HBase client (HTable), only one instance of `HBaseClient` is needed per application/cluster regardless of the number of tables or threads.

## Build Commands

```bash
# Build everything (jar + unit tests)
make

# Run unit tests
make check

# Run a specific test class
make run CLASS=TestHBaseClient ARGS='testName'

# Run integration tests (requires HBASE_HOME to point to HBase installation)
HBASE_HOME=/path/to/hbase make integration ARGS='test f'

# Speed up integration test reruns
TEST_NO_TRUNCATE=1 HBASE_HOME=/path/to/hbase make integration

# Generate Maven pom.xml
make pom.xml

# Build with Maven
mvn install

# Generate Javadoc
make doc

# Clean build artifacts
make clean    # Basic cleanup
make distclean # Full cleanup including jar and api docs
```

**Requirements:** GNU Make, Java 6+, protoc 2.5.0

## Architecture

### Core Components

- **HBaseClient** (`src/HBaseClient.java`) - Main entry point; single instance per application manages all region connections, ZooKeeper coordination, and RPC routing
- **RegionClient** (`src/RegionClient.java`) - Handles communication with a specific region server; manages connection pooling, RPC batching, and retry logic
- **HBaseRpc** (`src/HBaseRpc.java`) - Abstract base for all RPC request types (GetRequest, PutRequest, DeleteRequest, etc.)
- **Scanner** (`src/Scanner.java`) - Handles server-side scan operations with batch fetching

### Exception Model

All exceptions extend `HBaseException` (a `RuntimeException`). No checked exceptions are used. Key exception categories:
- **RecoverableException** - Retriable failures (region moved, NSRE)
- **NonRecoverableException** - Permanent failures (no such family, table not found)
- Region-specific exceptions (RegionOfflineException, RegionMovedException, etc.)

### RPC Request Flow

1. Client creates an `HBaseRpc` subclass (GetRequest, PutRequest, DeleteRequest, etc.)
2. `HBaseClient` routes to appropriate `RegionClient` based on table/region location
3. `RegionClient` serializes request via Protocol Buffers and sends over Netty
4. Response decoded and returned via `Deferred` callback chain

### Dependencies

- **Netty** - Async network I/O and channel management
- **ZooKeeper** - Region location discovery and cluster coordination
- **Protocol Buffers** - RPC serialization (definitions in `protobuf/` directory)
- **Guava** - Utilities and caching
- **SLF4J + Logback** - Logging (configured via `logback.xml`)

### Package Structure

```
src/
├── org/hbase/async/           # Main package
│   ├── HBaseClient.java       # Core client
│   ├── RegionClient.java      # Region server connection
│   ├── HBaseRpc.java          # RPC base + request types
│   ├── Scanner.java           # Scan implementation
│   ├── Bytes.java             # Byte utilities
│   ├── auth/                  # Auth providers (Kerberos, Simple)
│   ├── protobuf/              # Custom protobuf utilities
│   └── jsr166e/               # Concurrent utilities
protobuf/                       # .proto definitions for HBase RPC
test/                           # Unit and integration tests
third_party/                    # Dependency management (Make includes)
```

## Code Conventions

From HACKING guide:
- Local variables use `snake_case` naming
- No checked exceptions; all extend `HBaseException`
- Document all exceptions in Javadoc
- Document synchronization requirements for thread-safety
- Lines should not exceed 80 characters
- All code must be properly Javadoc'd including private members