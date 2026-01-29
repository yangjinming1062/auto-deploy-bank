# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Elasticsearch-Hadoop is an Elastic library that provides native integration between Elasticsearch and Apache Hadoop ecosystems (MapReduce, Hive, Spark). It enables real-time search and analytics by reading/writing data between Elasticsearch and Hadoop components.

## Build Commands

```bash
# Build the project and run unit tests
./gradlew build

# Run only unit tests (no integration tests)
./gradlew test

# Run integration tests (requires Elasticsearch fixture)
./gradlew integrationTest

# Build distribution zip
./gradlew distZip

# Run a single test class
./gradlew :mr:test --tests "org.elasticsearch.hadoop.mr.TestClassName"

# Run a single test method
./gradlew :spark-core:test --tests "org.elasticsearch.spark.rdd.TestClassName.testMethod"

# Generate dependency report
./gradlew generateDependenciesReport

# Check license headers and dependencies
./gradlew precommit
```

**Note:** The build requires JVM 8+ (Oracle recommended). Set `JAVA_HOME`, `RUNTIME_JAVA_HOME`, or similar environment variables to specify Java installations. Multiple Java versions can be configured for cross-compilation.

## Architecture

### Module Structure

The project is a multi-module Gradle build with the following key components:

- **mr** (`elasticsearch-hadoop-mr`): Core MapReduce integration providing `EsInputFormat` and `EsOutputFormat` for Hadoop MapReduce jobs
- **hive** (`elasticsearch-hadoop-hive`): Hive storage handler for reading/writing to Elasticsearch using external tables
- **spark/core** (`elasticsearch-spark`): Spark Core RDD integration for reading/writing to Elasticsearch
- **spark/sql-30** (`elasticsearch-spark-30`): Spark SQL/DataFrame integration for Spark 3.x with Scala 2.12/2.13 variants
- **thirdparty**: Shaded third-party dependencies (Jackson, Commons HTTPClient)
- **dist**: Distribution assembly combining all modules
- **test/shared**: Shared test utilities and fixtures
- **qa/kerberos**: Kerberos integration tests

### Key Dependencies (from gradle.properties)

- **Hadoop**: 2.7.6 (default), 3.1.2, 2.2.0
- **Hive**: 3.1.3
- **Spark**: 3.4.3 (spark30), with support for Scala 2.12 and 2.13
- **Jackson**: 1.8.8 (shaded)

### Core Source Packages

The main implementation resides in `mr/src/main/java/org/elasticsearch/hadoop/`:

- **mr/**: Hadoop MapReduce InputFormat/OutputFormat implementations (`EsInputFormat.java`, `EsOutputFormat.java`)
- **rest/**: Low-level REST client for communicating with Elasticsearch
- **serialization/**: JSON serialization layer with Schema handling
- **util/**: Shared utilities including settings, version compatibility
- **cfg/**: Configuration property handling (`es.*` prefix)
- **handler/**: Error handling pipeline

### Spark Variants

The Spark module uses a custom `SparkVariantPlugin` to build multiple Scala/Spark combinations:

- **spark30scala213**: Default - Spark 3.4.3 with Scala 2.13
- **spark30scala212**: Feature variant - Spark 3.4.3 with Scala 2.12

Each variant compiles separate source sets and produces distinct artifacts with capability-based dependencies.

### Shading Strategy

The project shades problematic dependencies in the `thirdparty` module:

- `commons-httpclient` → `org.elasticsearch.hadoop.thirdparty.apache.commons.httpclient`
- `jackson-mapper-asl`, `jackson-core-asl` → `org.elasticsearch.hadoop.thirdparty.codehaus.jackson`

This avoids version conflicts with Hadoop/Spark's Jackson dependencies.

### Configuration Properties

All configuration uses the `es` prefix. The `es.internal` namespace is reserved for internal use:

```java
es.resource=<index/type or index pattern>
es.query=<query URI or QueryDSL>
es.nodes=<ES host>
es.port=<REST port>
```

## Development Notes

### Adding New Dependencies

1. Add dependency to appropriate module's `build.gradle`
2. If non-transitive, the build plugin automatically handles dependency flattening
3. Run `gradlew updateShas` to update license SHAs
4. Ensure license file exists in module's `licenses/` directory

### Integration Tests

Integration tests use the `itest` source set and require:
- An embedded Elasticsearch node (started via `es.hadoop.cluster` plugin)
- Test JAR built separately with `itestJar` task
- System property `es.hadoop.job.jar` pointing to the test JAR

### License Headers

Run `gradlew licenseHeaders` to check/add Apache License headers to new files.

### CI/CD

- **Buildkite**: Main CI pipeline defined in `.buildkite/pipeline.py`
- **Gradle Enterprise**: Build scans published to `https://gradle-enterprise.elastic.co` on CI
- **Tests Trigger**: `.buildkite/tests.trigger.sh` runs on CI