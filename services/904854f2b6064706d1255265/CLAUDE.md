# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

JanusGraph is a distributed graph database optimized for storing and querying large graphs with billions of vertices and edges across a multi-machine cluster. It's built on Apache TinkerPop 3.7.3 and supports multiple storage backends.

## Build Commands

**Prerequisites:**
- Java 8 or higher (Java 11 supported via profile)
- Maven 3.2.5+

**Common Build Commands:**

```bash
# Build without tests
mvn clean install -DskipTests=true

# Build with default tests
mvn clean install

# Build with TinkerPop tests
mvn clean install -Dtest.skip.tp=false

# Build distribution archive
mvn clean install -Pjanusgraph-release -Dgpg.skip=true -DskipTests=true

# Build documentation
mvn --quiet clean install -DskipTests=true -pl janusgraph-doc -am
```

**Backend-specific builds:**
```bash
# Cassandra/CQL tests (requires Docker)
mvn clean install -pl janusgraph-cql -Pcassandra3-murmur
mvn clean install -pl janusgraph-cql -Pscylladb

# Elasticsearch tests (requires Docker)
mvn clean install -pl janusgraph-es

# Solr tests (requires Docker)
mvn clean install -pl janusgraph-solr
mvn clean install -pl janusgraph-solr -Psolr8

# HBase tests (requires Docker)
mvn clean install -pl janusgraph-hbase
```

**Documentation:**
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve
```

## Test Commands

JanusGraph uses JUnit 5 with test categories configured via Maven properties.

**Running Tests:**
```bash
# Run all tests
mvn clean test

# Run single test
mvn test -Dtest=FullClassName#methodName

# Run specific test category
mvn test -Dtest.skip.mem=false          # Memory tests
mvn test -Dtest.skip.perf=false         # Performance tests
mvn test -Dtest.skip.tp=false           # TinkerPop tests

# With TinkerPop tests included
mvn clean install -Dtest.skip.tp=false
```

**Test Categories:**
- **Default tests** (enabled by default): Core functionality tests
- **MEMORY_TESTS** (disabled): Tests under memory pressure (`-Dtest.skip.mem=false`)
- **PERFORMANCE_TESTS** (disabled): Speed/performance tests (`-Dtest.skip.perf=false`)
- **TinkerPop tests** (disabled): Apache TinkerPop compatibility tests (`-Dtest.skip.tp=false`)

**Backend Test Examples:**
```bash
# CQL with specific Cassandra version
mvn clean install -pl janusgraph-cql -Pcassandra3-murmur \
  -Dcassandra.docker.version=3.11.2

# Elasticsearch with specific version
mvn clean install -pl janusgraph-es -Delasticsearch.docker.version=6.0.0
```

## Code Style

**Checkstyle:**
```bash
# Checkstyle runs automatically during 'validate' phase
mvn validate

# Can also be run separately
mvn checkstyle:check
```

Checkstyle configuration enforces:
- Package declaration requirements
- Import organization (THIRD_PARTY_PACKAGE > STANDARD_JAVA > STATIC)
- No redundant imports or unused imports
- One top-level class per file
- Custom import ordering rules

## Architecture Overview

**Maven Modules:**
- `janusgraph-core` - Core graph database engine
- `janusgraph-driver` - Client driver and connectivity
- `janusgraph-grpc` - gRPC service implementation
- `janusgraph-server` - Gremlin Server integration
- `janusgraph-backend-testutils` - Testing utilities
- `janusgraph-test` - Test framework and helpers
- Storage backends: `janusgraph-cql`, `janusgraph-berkeleyje`, `janusgraph-hbase`, `janusgraph-bigtable`, `janusgraph-es`, `janusgraph-lucene`, `janusgraph-scylla`
- `janusgraph-hadoop` - Hadoop integration
- `janusgraph-dist` - Distribution packaging
- `janusgraph-examples` - Example applications
- `janusgraph-doc` - Documentation

**Core Package Structure (janusgraph-core):**
- `org.janusgraph.core` - Public API (JanusGraph, JanusGraphFactory, Transaction, etc.)
- `org.janusgraph.graphdb` - Core graph database implementation
  - `database/` - Database management, transactions, serialization
  - `query/` - Query processing and optimization
  - `types/` - Schema type system
  - `tinkerpop/` - Apache TinkerPop integration
  - `olap/` - OLAP/computer integration
- `org.janusgraph.diskstorage` - Storage layer abstraction
  - `keycolumnvalue/` - Key-column-value store interface
  - `indexing/` - Index management
  - `locking/` - Distributed locking
  - `configuration/` - Configuration system
  - `common/` - Common storage utilities
- `org.janusgraph.util` - Utility classes

**Key Classes:**
- `JanusGraphFactory` - Graph factory for creating graph instances
- `StandardJanusGraph` - Main graph implementation
- `Backend` - Storage backend interface
- `StoreManager` - Storage engine management

## Development Workflow

**Prerequisites:**
1. Sign the Contributor License Agreement (CLA)
2. Configure git with name/email matching CLA
3. Set up fork and clone locally

**Branch Naming:**
- Feature branches must be prefixed with `Issue_#_`
- Always branch from `master`

**Pull Requests:**
- Review-Then-Commit (RTC) process
- Requires 2 committer approvals (or 1 if author is committer)
- Or 1 approval + 1 week review period for lazy consensus
- All PRs must be associated with an issue
- Commit messages should use `git commit -s` to sign DCO
- Auto-backporting enabled via labels (e.g., `backport/v0.6`)

**Key Files:**
- `pom.xml` - Maven configuration with profiles for different backends
- `BUILDING.md` - Detailed build instructions
- `TESTING.md` - Comprehensive testing documentation
- `CONTRIBUTING.md` - Contribution guidelines
- `docs/development.md` - Development process and governance

## Important Notes

- **Java Version**: Project uses Java 8 by default, Java 11 via `java-11` profile
- **Testing**: Many tests require Docker (Elasticsearch, Cassandra, Solr, HBase)
- **Checkstyle**: Enforces strict code style - violations will fail CI
- **Documentation**: Configuration reference auto-generated via Maven
- **Snapshots**: Use `mvn clean install` not `mvn deploy` for local builds
- **Dependencies**: Guava upgrade requires full test suite run (see pom.xml:935)

## Environment Setup

**Required:**
- Java 8+
- Maven 3.2.5+
- Git

**Optional (for full testing):**
- Docker (for backend tests)
- Python 3 + pip3 (for documentation)

## Additional Resources

- Project Homepage: https://janusgraph.org
- Documentation: https://docs.janusgraph.org
- GitHub: https://github.com/JanusGraph/janusgraph
- Mailing Lists: janusgraph-users@lists.lfaidata.foundation, janusgraph-dev@lists.lfaidata.foundation