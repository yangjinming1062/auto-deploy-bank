# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

htm.java is a Java implementation of Hierarchical Temporal Memory (HTM), ported from Numenta's NuPIC Python project. It implements the core HTM algorithms for building sensorimotor inference systems.

**Minimum Java version:** 8

## Build Commands

```bash
# Run all tests and benchmarks
gradle check

# Run tests without benchmarks (faster)
gradle -Pskipbench check

# Maven commands
mvn clean test              # Run tests with JaCoCo coverage
mvn clean verify            # Full verification including tests
```

## Architecture

### Core HTM Algorithms (`src/main/java/org/numenta/nupic/algorithms/`)

| Class | Purpose |
|-------|---------|
| `SpatialPooler` | Learns spatial patterns from input; initializes with `init(Connections)` |
| `TemporalMemory` | Learns temporal sequences; uses same `Connections` object as SpatialPooler |
| `SDRClassifier` | Supervised learning for classification/regression on SDRs |
| `CLAClassifier` | CLA (Convolutional List Attention) classifier variant |
| `AnomalyLikelihood` | Statistical anomaly detection |
| `Anomaly` | Real-time anomaly scoring |

### Network API (`src/main/java/org/numenta/nupic/network/`)

The high-level fluent API for building HTM networks:

```java
Network network = Network.create("name", parameters)
    .add(Network.createRegion("r1")
        .add(Network.createLayer("l1", parameters)
            .add(new SpatialPooler())
            .add(new TemporalMemory())
            .add(Sensor.create(...))));
```

Key classes:
- `Network` - Top-level container; creates Regions and Layers
- `Region` - Container for Layers; manages inter-layer connections
- `Layer` - Contains algorithmic components (SP, TM, classifiers, sensors)
- `ManualInput` - Low-level API for manual data injection
- `Persistence` - Network serialization/deserialization

### Encoders (`src/main/java/org/numenta/nupic/encoders/`)

Convert raw data into Sparse Distributed Representations (SDRs):

| Encoder | Use Case |
|---------|----------|
| `ScalarEncoder` | Continuous numeric values |
| `DateEncoder` | Date/time features (day of week, time of day, etc.) |
| `CategoryEncoder` | Discrete categories |
| `MultiEncoder` | Combines multiple encoders |
| `RandomDistributedScalarEncoder` | Random binary SDRs for scalars |
| `CoordinateEncoder` / `GeospatialCoordinateEncoder` | Spatial coordinates |

Base class: `Encoder` with generic `encode()` method producing `int[]` SDRs.

### Model Data Structures (`src/main/java/org/numenta/nupic/model/`)

| Class | Purpose |
|-------|---------|
| `Connections` | Central configuration/state object shared by SP and TM |
| `Column` | Contains cells; receives input via proximal dendrite |
| `Cell` | HTM cell with dendrite segments |
| `Synapse` | Connection between cells |
| `Segment` | Collection of synapses on a cell's dendrite |
| `Pool` | Permanence tracking for synapses |
| `SDR` | Immutable sparse distributed representation |

### Utilities (`src/main/java/org/numenta/nupic/util/`)

Key utilities:
- `SparseMatrix`, `SparseBinaryMatrix`, `SparseObjectMatrix` - Efficient sparse data structures
- `ArrayUtils` - Array manipulation helpers
- `Topology` - Grid/layout utility
- `GroupBy2` - Grouping/iteration utility

## Parameters

`Parameters.java` defines configuration keys:
```java
Parameters.KEY.COLUMN_DIMENSIONS
Parameters.KEY.CELLS_PER_COLUMN
Parameters.KEY.INPUT_DIMENSIONS
Parameters.KEY.POTENTIAL_PCT
Parameters.KEY.SYNAPE_PERMANENCE_DECCREMENT
Parameters.KEY.SYNAPE_PERMANENCE_INCREMENT
// ... and many more
```

Use `Parameters.getDefaultParameters()` as base and `union()` to combine.

## Tests

90+ JUnit tests in `src/test/java/org/numenta/nupic/`

Test structure mirrors source:
- `algorithms/` - SP, TM, classifier tests
- `encoders/` - Encoder tests
- `network/` - Network API tests
- `integration/` - Full integration tests

Run specific test:
```bash
mvn test -Dtest=SpatialPoolerTest
```

## Benchmarks

JMH benchmarks in `src/jmh/` - run automatically with `gradle check`.

## Packaging

Both Gradle and Maven builds produce:
- Main JAR (`htm.java-0.6.13.jar`)
- Fat/uber JAR with all dependencies
- Javadoc JAR
- Sources JAR

Publish to Sonatype OSSRH for Maven Central deployment.

## Key Files

- `build.gradle` - Gradle build with JMH benchmarking
- `pom.xml` - Maven build with JaCoCo coverage
- `EclipseFormatRules.xml` - Code formatting rules
- `.travis.yml` - CI configuration (Maven + JaCoCo + Coveralls)