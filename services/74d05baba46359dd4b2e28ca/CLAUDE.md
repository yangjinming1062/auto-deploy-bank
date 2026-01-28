# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

htm.java is a Java implementation of Hierarchical Temporal Memory (HTM), a computational theory of intelligence. It's a community-supported port of Numenta's NuPIC (Python) project. The library provides algorithms for learning temporal patterns and making predictions using Sparse Distributed Representations (SDR).

## Build Commands

```bash
# Quick sanity check (runs tests without benchmarks)
gradle -Pskipbench check

# Full build with benchmarks
gradle check

# Create fat JAR with all dependencies
gradle fatJar

# Run single test class
gradle test --tests "SpatialPoolerTest"

# Maven equivalent
mvn test
```

## Architecture

### Data Flow
```
Input → Encoders → SpatialPooler → TemporalMemory → Classifier
                ↓                    ↓
           (feed-forward)     (temporal memory)
```

### Core Components

**Encoders** (`src/main/java/org/numenta/nupic/encoders/`): Convert raw input data (scalars, categories, dates, coordinates) into Sparse Distributed Representations (SDR). Key encoders include:
- `ScalarEncoder` - for continuous values
- `CategoryEncoder` - for discrete categories
- `DateEncoder` - extracts time-based features
- `MultiEncoder` - combines multiple encoders

**Algorithms** (`src/main/java/org/numenta/nupic/algorithms/`): Core HTM algorithms:
- `SpatialPooler` - learns feed-forward connections, produces stable SDR output
- `TemporalMemory` - learns temporal sequences via cell/segment/synapse structures
- `SDRClassifier` - pattern classification using softmax over SDR bits

**Model** (`src/main/java/org/numenta/nupic/model/`): Data structures separating state from logic:
- `Connections` - centralized state container for SP and TM (the "single source of truth")
- `Cell`, `Column`, `Segment`, `Synapse` - HTM structural elements
- `Pool` - tracks synapse permanences and connected inputs

**Network API** (`src/main/java/org/numenta/nupic/network/`): Fluent API for composing HTM networks:
- `Network` - top-level container holding Regions
- `Region` - container for Layers
- `Layer` - holds algorithm components (Sensor, SpatialPooler, TemporalMemory, Classifier)
- Uses RxJava Observables for reactive stream processing via `observe()` and `subscribe()`

### Configuration

`Parameters.java` uses enum-based keys (`Parameters.KEY`) for all configuration:
- `KEY.COLUMN_DIMENSIONS`, `KEY.CELLS_PER_COLUMN` - TM topology
- `KEY.ACTIVATION_THRESHOLD`, `KEY.MIN_THRESHOLD` - TM learning thresholds
- `KEY.POTENTIAL_PCT`, `KEY.GLOBAL_INHIBITION` - SP parameters

## Key Design Patterns

1. **Separation of data and logic**: `Connections` holds all state; algorithms operate on it
2. **Observable streams**: `network.observe()` returns `Observable<Inference>` for reactive programming
3. **Fluent builder API**: `Network.create(...).add(Region.create().add(Layer.create()...))`
4. **Sparse matrices**: Custom `SparseMatrix` implementations for memory-efficient large arrays

## Testing

- Tests use JUnit 4
- Test patterns mirror NuPIC Python tests for compatibility verification
- Integration tests in `integration/` package test complete network pipelines
- 92 test files covering encoders, algorithms, network API, and serialization

## Important Notes

- Minimum Java 8
- Uses Apache GNU Affero Public License (AGPL)
- Synchronized with NuPIC Python algorithms; check README versioning table for sync status