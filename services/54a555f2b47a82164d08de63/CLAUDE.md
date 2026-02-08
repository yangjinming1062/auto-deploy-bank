# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
make              # Build the project (requires javac and protoc v2.5.0)
make check        # Run unit tests
make run CLASS=TestScanner   # Run a single unit test
make jar          # Build the JAR only
make pom.xml      # Generate Maven pom.xml from template
make doc          # Generate Javadoc in build/api
make clean        # Clean build artifacts
make distclean    # Remove all generated files including JAR and docs
```

**Integration tests** (requires running HBase instance):
```bash
HBASE_HOME=/path/to/hbase make integration ARGS='test f'
# Speed up subsequent runs: TEST_NO_TRUNCATE=1 HBASE_HOME=... make integration ARGS='test f'
# Run single test: TEST_NAME=XXX HBASE_HOME=... make integration ARGS='test f'
```

## Architecture

This is an asynchronous, non-blocking, thread-safe Java client for HBase.

**Main Entry Point**: `org.hbase.async.HBaseClient`
- Instantiate once per cluster (unlike HTable which is table-per-instance)
- Thread-safe, designed for multi-threaded applications
- Uses `Deferred` pattern (returns `Deferred<T>` instead of blocking)

**Key Components**:
- `HBaseClient`: Main client class - handles cluster connection, region location caching, and RPC dispatch
- `RegionClient`: Per-region RPC connection manager. Extends Netty's `ReplayingDecoder` for response decoding. Manages RPC IDs, serialization/deserialization, and in-flight RPC tracking
- `Scanner`: Asynchronous table scanner with callback-based results
- Request classes: `GetRequest`, `PutRequest`, `DeleteRequest`, `AtomicIncrementRequest`, etc.
- Filter classes: `FamilyFilter`, `RowFilter`, `ColumnPrefixFilter`, etc. (implement `ScanFilter`)
- `auth/`: Authentication providers (Kerberos via `KerberosClientAuthProvider`, simple auth)
- `jsr166e/`: Backported concurrency utilities (`LongAdder`, `Striped64`)

**Asynchronous Flow**:
1. Client creates request (e.g., `GetRequest`) and passes to `HBaseClient`
2. `HBaseClient` locates region via region cache or ZK/metadata lookup
3. Request routed to appropriate `RegionClient` for that region
4. `RegionClient` serializes request to Protocol Buffers, sends via Netty
5. Response decoded by `RegionClient` (state machine via `ReplayingDecoder`)
6. Original `Deferred` resolved with result or exception via callback chain

**RPC Protocol**: Protobuf-based HBase RPC. Protocol buffer files in `protobuf/` generate Java classes in `build/src/org/hbase/async/generated/`.

## Coding Conventions

Follow existing code style when editing. Key conventions from `HACKING`:

- **Local variables**: `snake_case` (e.g., `local_variable_name`)
- **Fields/methods**: standard `camelCase`
- **No checked exceptions**: All derive from `HBaseException` (RuntimeException)
- **Lines**: Keep under 80 characters
- **Javadoc**: Required for everything, including private members
- **Thread safety**: Document synchronization requirements in Javadoc
- **Performance**: Avoid object allocation in loops; reuse objects to minimize GC pressure
- **Exceptions**: Fine-grained types with recovery data

## Key Dependencies

- **Netty 3.2.x**: Non-blocking network I/O, channel pipeline, timers
- **stumbleupon-async**: `Deferred<T>` Promise type, `Callback<T,R>`, `DeferredGroupException`
- **Protobuf 2.5.0**: RPC serialization (protoc v2.5.0 required)
- **ZooKeeper**: Region location discovery via ZK quorum
- **Guava**: Collections, caching (`LoadingCache`), utilities
- **SLF4J + Logback**: Logging facade and implementation

## Directory Structure

```
src/
  *.java                          # Core classes (HBaseClient, RegionClient, Scanner, etc.)
  auth/                           # Kerberos/simple authentication providers
  jsr166e/                        # Concurrent utilities (LongAdder, Striped64)
  protobuf/ZeroCopyLiteralByteString.java  # Zero-copy protobuf optimization
test/
  BaseTest*.java                  # Test base classes (mock Netty, ZK, region handling)
  Test*.java                      # Unit tests
  TestIntegration.java            # Integration tests (real HBase required)
  auth/                           # Auth provider tests
```