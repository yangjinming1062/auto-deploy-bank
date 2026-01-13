# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Alluxio is a Distributed Caching Platform for large-scale data. It bridges the gap between computation frameworks and storage systems, enabling computation applications to connect to numerous storage systems through a common interface.

## Architecture

Alluxio follows a master-worker architecture:

### Core Modules
- **core/common**: Common utilities and constants shared across modules
- **core/client**: Client-side API for interacting with Alluxio
- **core/server**: Server-side components including:
  - **master**: Metadata management, handles file system operations (block, file, job, meta submodules)
  - **worker**: Data management, caches and serves data blocks (block/page submodules)
  - **proxy**: Proxy service for AlluxioFUSE
- **core/transport**: gRPC and Protocol Buffer definitions for RPC communication
- **job**: Job service for asynchronous operations
- **table**: Structured data support (tables, catalogs)
- **underfs**: Underlying storage system adapters (S3, HDFS, Ozone, etc.)

### Key Components
- **Master**: Manages namespace, tracks file metadata, coordinates workers
- **Worker**: Stores data in memory/disk, serves block data to clients
- **Job Master/Worker**: Handles asynchronous operations (load balancing, replication)
- **Client**: Applications interact with Alluxio through the client API

## Common Development Commands

### Building
```bash
# Full build without tests
mvn clean install -DskipTests

# Fast parallel build (skip checks)
mvn -T 2C clean install \
    -DskipTests \
    -Dmaven.javadoc.skip=true \
    -Dfindbugs.skip=true \
    -Dcheckstyle.skip=true \
    -Dlicense.skip

# Compile only
mvn clean compile -DskipTests
```

### Testing
```bash
# Run all unit and integration tests
mvn test

# Run a single test
mvn -Dtest=<AlluxioTestClass>#<testMethod> -DfailIfNoTests=false test

# Run tests for a specific module
mvn test -pl underfs/hdfs

# Run tests with different Hadoop version
mvn test -pl underfs/hdfs -Phadoop-2 -Dhadoop.version=2.7.0

# Run HDFS UFS contract tests (requires real HDFS deployment)
mvn test -pl underfs/hdfs -PufsContractTest -DtestHdfsBaseDir=hdfs://ip:port/alluxio_test

# Redirect logs to STDOUT
mvn test -Dtest.output.redirect=false -Dalluxio.root.logger=DEBUG,CONSOLE
```

### Code Quality
```bash
# Check code style
mvn checkstyle:checkstyle

# Run SpotBugs analysis
mvn spotbugs:spotbugs

# Verify licenses
mvn license:check
```

### Local Testing
```bash
# Format Alluxio (requires build first)
./bin/alluxio format

# Start local cluster
./bin/alluxio-start.sh local SudoMount

# Run integration tests
./bin/alluxio runTests

# Stop local cluster
./bin/alluxio-stop.sh local

# Format masters
./bin/alluxio formatMasters

# Format worker
./bin/alluxio formatWorker
```

### gRPC and Protocol Buffers
When modifying `.proto` files in `core/transport/src/grpc/` or `core/transport/src/proto/`:
```bash
mvn clean install -Pgenerate -pl "org.alluxio:alluxio-core-transport"
```

### Environment Requirements
- **Java**: Version 8
- **Maven**: 3.3.9 or later
- **Git**: Required for building
- **Optional**: Docker for isolated build environment (`alluxio/alluxio-maven` image available)

### Memory Settings
If encountering `OutOfMemoryError` during build:
```bash
export MAVEN_OPTS="-Xmx2g -XX:MaxPermSize=512M -XX:ReservedCodeCacheSize=512m"
```

## IDE Configuration

### IntelliJ IDEA
1. Import project as Maven project
2. Enable 'developer' Maven profile in View > Tool Windows > Maven
3. Mark generated sources directories:
   - `core/transport/target/generated-sources/protobuf/`
   - `core/common/target/generated-sources/java-templates/`
4. Install IntelliJ Checkstyle plugin and configure with `docs/resources/intellij_checkstyle_plugin.png`
5. Import formatter from `docs/resources/alluxio-code-formatter-eclipse.xml`
6. Configure import layout according to `docs/resources/intellij_imports.png`

### Running Alluxio in IntelliJ
```bash
# Install run configurations
dev/intellij/install-runconfig.sh

# Restart IntelliJ and configure:
# - conf/alluxio-site.properties (master/job.master hostname settings)
# - conf/log4j.properties (enable console logging)

# Start processes in this order:
# 1. AlluxioMaster
# 2. AlluxioJobMaster
# 3. AlluxioWorker
# 4. AlluxioJobWorker
```

## Code Style

- **Java Style**: Google Java style with these deviations:
  - Maximum line length: **100 characters**
  - Member variables prefixed with `m` (e.g., `private WorkerClient mWorkerClient;`)
  - Static variables prefixed with `s` (e.g., `private static String sUnderFSAddress;`)
  - Third-party imports grouped together
- **Bash Style**: Google Shell style, compatible with Bash 3.x

## Build Profiles

### Hadoop Versions
Build with different HDFS versions:
```bash
mvn install -pl underfs/hdfs \
   -P<PROFILE> -Dufs.hadoop.version=<VERSION>

# Profiles: ufs-hadoop-1, ufs-hadoop-2, ufs-hadoop-3
```

### Other Profiles
- `generate`: Regenerate gRPC/ProtoBuf code
- `hadoop-2`, `hadoop-3`: Build with specific Hadoop major version
- `ufsContractTest`: Run UFS contract tests

## Module Structure

```
alluxio/
├── core/                          # Core Alluxio components
│   ├── common/                    # Common utilities and constants
│   ├── client/                    # Client APIs
│   ├── server/                    # Server components
│   │   ├── master/                # Master service (metadata, namespace)
│   │   ├── worker/                # Worker service (data storage)
│   │   └── proxy/                 # Proxy service (FUSE)
│   └── transport/                 # gRPC/ProtoBuf definitions
├── job/                           # Asynchronous job service
├── table/                         # Structured data support
├── underfs/                       # Underlying storage adapters
│   ├── hdfs/                      # HDFS UFS
│   ├── s3a/                       # S3 UFS
│   └── ...                        # Other UFS implementations
├── webui/                         # Web UI (React/TypeScript)
├── examples/                      # Example applications
├── stress/                        # Performance testing tools
└── tests/                         # Integration tests
```

## Important Notes

- The codebase uses gRPC for client-server communication (defined in `core/transport/src/grpc/`)
- Protocol Buffers are used for journal entries (defined in `core/transport/src/proto/`)
- Web UI is a separate Node.js/React application in the `webui/` directory
- AlluxioFUSE provides POSIX API through the `proxy` module
- Page-based storage (experimental) is in `core/server/worker/src/main/java/alluxio/worker/page/`
- The `alluxio` CLI tool in `bin/` provides cluster management commands

## Troubleshooting

- If protolock error occurs: ensure `-Dskip.protoc` is NOT in build command
- If SCM buildnumber NPE occurs: add `-Dmaven.buildNumber.revisionOnScmFailure=<version>`
- First build takes long due to dependency downloads
- Use Docker image `alluxio/alluxio-maven` for reproducible builds