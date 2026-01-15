# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CDAP (Cask Data Application Platform) is an integrated, open-source application development platform for the Hadoop ecosystem. It provides data and application abstractions to simplify development, deployment, and management of data-intensive applications supporting batch and real-time processing (MapReduce, Spark, Spark Streaming).

## Build Commands

### Common Commands

```bash
# Build all modules
mvn clean package

# Build without running tests
mvn clean package -DskipTests

# Run all tests (fail at end)
MAVEN_OPTS="-Xmx2048m" mvn test -fae

# Run tests, skipping HBase compatibility tests
MAVEN_OPTS="-Xmx2048m" mvn test -Pskip-hbase-compat-tests -fae

# Build a specific module with dependencies
mvn clean package -pl [module] -am

# Run a specific test class/method
MAVEN_OPTS="-Xmx2048m" mvn -Dtest=TestClass,TestMore*Class,TestClassMethod#methodName \
  -DfailIfNoTests=false test

# Run App-Template tests
MAVEN_OPTS="-Xmx2048m" mvn test -fae -am -amd -P templates -pl cdap-app-templates/cdap-etl

# Run fast tests only (skip SlowTests)
mvn test -Ptest-fast

# Run fast and slow tests, but not xslow
mvn test -Ptest-slow

# Generate checkstyle report
mvn checkstyle:check

# Run checkstyle only
mvn clean package -DskipTests
```

### Building Distributions

```bash
# Build CDAP Sandbox distribution ZIP
MAVEN_OPTS="-Xmx2048m" mvn clean package \
  -pl cdap-standalone,cdap-app-templates/cdap-etl,cdap-app-templates/cdap-program-report \
  -am -amd -DskipTests -P templates,dist,release,unit-tests

# Build distributions (rpm, deb, tgz)
MAVEN_OPTS="-Xmx2048m" mvn clean package -DskipTests \
  -P templates,dist,release,rpm-prepare,rpm,deb-prepare,deb,tgz,unit-tests
```

### IDE Setup

For IntelliJ/Eclipse, first build the UI packages:
```bash
mvn clean package -pl cdap-ui -am -DskipTests -P dist
```

If Spark module errors occur in IDE, generate test sources:
```bash
mvn clean generate-test-sources -P templates,spark-dev
```

### Test Output

To see test output to stdout instead of files:
```bash
mvn -Dsurefire.redirectTestOutputToFile=false ...
```

## Architecture Overview

### Major Components

| Module | Purpose |
|--------|---------|
| **cdap-api** | Developer APIs for creating applications (Programs, Datasets, Services) |
| **cdap-runtime-spi** | Service Provider Interfaces for extensibility (Provisioners, Monitors) |
| **cdap-common** | Shared infrastructure (Configuration, Discovery, Security, Guice modules) |
| **cdap-data-fabric** | Dataset framework, Transaction management, Data storage |
| **cdap-app-fabric** | Application lifecycle, Program lifecycle, Provisioning |
| **cdap-gateway** | HTTP routing (NettyRouter), Authentication, Audit |
| **cdap-tms** | Transactional Messaging System (pub/sub for events) |
| **cdap-watchdog** | Metrics collection, Log aggregation |
| **cdap-master** | Distributed deployment orchestration (ServiceMain classes) |
| **cdap-security** | Authentication, Authorization, Secure store |
| **cdap-runtime-ext-*** | Platform extensions (Dataproc, EMR, Kubernetes) |
| **cdap-spark-core3_2.12** | Spark program integration |
| **cdap-app-templates** | ETL pipeline templates and Hydrator plugins |

### Key Patterns

1. **Guice Dependency Injection**: Comprehensive use of Guice modules for service wiring (e.g., AppFabricServiceRuntimeModule, DataFabricModules)

2. **Service Discovery**: Zookeeper-based with DiscoveryService and EndpointStrategy for locating backend services

3. **REST API Gateway**: NettyRouter handles HTTP routing to AppFabric, Dataset, Metrics, Logging, and Messaging services

4. **Idle Services**: Most components extend `AbstractIdleService` for lifecycle management

5. **Configuration-Driven**: CConfiguration and SConfiguration drive runtime behavior throughout the system

6. **Handler Chain**: HTTP requests flow through authentication, audit, and business logic handlers

7. **Message Pub/Sub**: TMS handles async events (program start/complete notifications)

8. **SPI Pattern**: Extensible provisioners, storage backends, and authentication mechanisms

### Main Entry Points

- **Standalone mode**: `io.cdap.cdap.StandaloneMain` - single-node development (in cdap-standalone)
- **Distributed mode**: `io.cdap.cdap.master.environment.*.ServiceMain` classes - individual services (in cdap-master)

### Request Flow

Client → NettyRouter → Path Lookup & Authentication → Service Discovery (Zookeeper) → Target Service (AppFabric/Dataset/Metrics/Logging/Messaging) → Dataset/Metadata/Transactions

## Code Style

The project uses Checkstyle with Google Java Style guidelines:

- **Max line length**: 120 characters
- **Line endings**: LF (Unix style)
- **Package naming**: Lowercase with dots (`^[a-z]+(\.[a-z][a-z0-9]*)*$`)
- **Class naming**: PascalCase
- **Method/field naming**: camelCase
- **No star imports** (`AvoidStarImport`)
- **Javadoc required**: Public/protected methods and types
- **Suppression comments**: `CHECKSTYLE.OFF: checkname` / `CHECKSTYLE.ON: checkname`

Configuration: `checkstyle.xml` with suppressions in `suppressions.xml`

## Key Dependencies

- **Hadoop 3.3.6**: HDFS, YARN, MapReduce
- **Spark 3.3.2** (Scala 2.12): Batch and streaming processing
- **Guice 4.0**: Dependency injection
- **Netty 4.1.75**: HTTP server/communication
- **Dropwizard 3.1.2**: Metrics
- **Tephra 0.15.0-incubating**: Transaction management
- **Apache Twill 1.4.0**: YARN application deployment
- **Guava 13.0.1**: Core utilities

## Testing Framework

- **JUnit 4.11**: Primary testing framework
- **Mockito 3.9.0**: Mocking
- **PowerMock 2.0.9**: Static method mocking
- **Test groups**: `SlowTests`, `XSlowTests` for categorization
- **Test naming**: Matches `**/*Test.java`, `**/Test*.java`, `**/*TestCase.java`