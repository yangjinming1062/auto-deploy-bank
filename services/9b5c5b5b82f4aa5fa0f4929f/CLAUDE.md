# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the t-digest Java library - a data structure for accurate online accumulation of rank-based statistics such as quantiles and trimmed means. The project is divided into three Maven modules:

- **core** - The main t-digest implementation with unit tests (default active profile)
- **quality** - Accuracy testing and quality assessment tools
- **benchmark** - Performance benchmarking suite

## Common Commands

### Building and Testing

```bash
# Build and test the core module only (default, fastest)
mvn clean test

# Build and test all modules
mvn -Pall clean test

# Run tests with slow tests enabled (quality module)
mvn clean test -DrunSlowTests=true

# Run quality tests only
cd quality && mvn test

# Run benchmarks
cd benchmark && mvn test

# Build without running tests
mvn clean package

# Run a specific test class
mvn test -Dtests=**/TDigestTest

# Install artifacts to local repository
mvn install

# Generate Javadoc
mvn javavadoc:javadoc
```

### Build Requirements

- **Java**: Version 1.8+ (project targets Java 1.7/1.8 compatibility)
- **Maven**: Version 3+

### CI/CD

The project uses GitHub Actions (see `.github/workflows/maven.yml`) with:
- Matrix testing on Ubuntu and Windows
- Java versions 8 and 11
- Command: `mvn -V --no-transfer-progress clean test`

## Code Architecture

### Core Components

The main t-digest implementation is in `core/src/main/java/com/tdunning/math/stats/`:

**Primary Interfaces and Classes:**
- `TDigest.java` - Main public interface for t-digest functionality
- `AbstractTDigest.java` - Abstract base class for digest implementations
- `MergingDigest.java` - Legacy merge-based digest implementation (~35KB, core algorithm)
- `AVLTreeDigest.java` - More recent AVL-tree based implementation (~22KB, better performance)
- `Centroid.java` - Represents a cluster centroid (mean + count)

**Helper Classes:**
- `ScaleFunction.java` - Controls cluster size distribution, critical for accuracy (~24KB)
- `Sort.java` - Stable sorting utilities (~29KB, including mergesort)
- `Simple64.java` - 64-bit computing utilities (~48KB)
- `AVLGroupTree.java`, `IntAVLTree.java` - AVL tree implementations
- `Dist.java` - Statistical distribution utilities

**Histogram Implementations:**
- `FloatHistogram.java` - Log-scale histogram for positive values
- `LogHistogram.java` - Enhanced FloatHistogram with quadratic updates
- `Histogram.java` - Base histogram interface

### Key Implementation Details

1. **Two Major Digest Types:**
   - `MergingDigest`: Uses clustering with merge operations
   - `AVLTreeDigest`: Uses AVL tree for better performance

2. **Scale Functions**: Four different scale functions in `ScaleFunction.java` control accuracy/size tradeoffs:
   - Uniform scaling (legacy)
   - K-squared law (default)
   - Law of the iterated logarithm
   - Normal scale function

3. **Serialization**: Digests implement `Serializable` with `toBytes()` and `fromBytes()` methods for persistence.

4. **No Runtime Dependencies**: The core library has zero runtime dependencies.

### Test Structure

Unit tests in `core/src/test/java/com/tdunning/math/stats/`:
- `TDigestTest.java` - Main test suite
- `MergingDigestTest.java`, `AVLTreeDigestTest.java` - Specific implementation tests
- `ScaleFunctionTests.java` - Scale function validation
- `SerializationTest.java` - Serialization/deserialization tests
- `*HistogramTest.java` - Histogram implementation tests

### Known Issues and Notes

- AVLTreeDigest has known issues with large numbers of repeated data points (documented in release notes)
- Sort operations must be stable for correct behavior
- The quality module generates large data files during testing
- Java 8+ required; CI tests on Java 8 and 11

### Package Structure

```
com.tdunning.math.stats
├── TDigest                    - Main interface
├── AbstractTDigest            - Base implementation
├── MergingDigest             - Merge-based algorithm
├── AVLTreeDigest             - AVL-tree based algorithm
├── Centroid                  - Cluster representation
├── ScaleFunction             - Accuracy controls
├── Sort                      - Stable sorting
├── FloatHistogram            - Log-scale histogram
├── LogHistogram              - Enhanced histogram
└── [other utilities]
```

## Documentation

- **README.md** - Project overview, algorithm description, installation
- **RELEASE-NOTES.md** - Release history, bug fixes, known issues
- **quality/README.md** - Accuracy testing methodology
- **docs/** - Research papers, proofs, figures
- **docs/proofs/** - Formal proofs of correctness and bounds