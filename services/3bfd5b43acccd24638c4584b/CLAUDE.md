# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ARX is an open source data anonymization software for protecting sensitive personal data. It provides utility-focused anonymization with support for multiple privacy models (k-anonymity, l-diversity, t-closeness, d-presence, differential privacy) and various data transformation techniques.

## Build Commands

### Ant (Primary Build System)
```bash
# Run all tests
ant test

# Build release JARs (Linux, Windows, macOS)
ant release

# Compile source only
ant compile

# Generate Javadoc
ant javadoc

# Run benchmark tests
ant benchmark
```

### Maven (Experimental Support)
```bash
# Install local dependencies first
./install_deps.sh

# Build with Maven (platform-specific profile required)
# Profiles: gtk-64 (Linux), win-64 (Windows), osx-64 (macOS)
mvn clean package compile -P gtk-64 -Dcore=true -DskipTests

# Build core only (no GUI)
mvn clean package compile -P gtk-64 -Dcore=true -DskipTests
```

### Running Single Tests
```bash
# Using Ant - specify test class
ant compileTest
# Then run specific test by editing build.xml batchtest includes
```

## Architecture

### Source Structure

- **`src/main/org/deidentifier/arx/`** - Core anonymization engine
  - `ARXAnonymizer.java` - Main entry point for anonymization
  - `Data.java` - Data input/output handling
  - `ARXConfiguration.java` - Configuration for anonymization process
  - `criteria/` - Privacy criterion implementations (k-anonymity, l-diversity, etc.)
  - `algorithm/` - Core anonymization algorithms
  - `framework/` - Optimization framework and lattice structure
  - `metric/` - Utility and quality metrics
  - `io/` - Input/output handlers (CSV, database, etc.)
  - `risk/` - Re-identification risk analysis
  - `dp/` - Differential privacy implementations
  - `aggregates/` - Quality and classification measures

- **`src/gui/org/deidentifier/arx/gui/`** - SWT-based graphical interface
  - `view/impl/` - GUI view implementations
  - `model/` - GUI model classes
  - `worker/` - Background workers for long-running tasks
  - `Main.java` - GUI entry point

- **`src/test/`** - JUnit test suite
- **`src/example/`** - Example usage code

### Key Design Patterns

1. **Data Handles**: Input/output handled through `DataHandle*` interfaces (DataHandleInput, DataHandleOutput, DataHandleInternal)
2. **Lattice Optimization**: Uses a lattice structure (`ARXLattice`) for exploring generalization hierarchies
3. **Criteria Pattern**: Privacy criteria are pluggable implementations in `criteria/` package
4. **Metrics**: Two metric versions exist (`metric/` v1 and `metric/v2` v2)

### Main API Entry Points

- `ARXAnonymizer` - Primary class for performing anonymization
- `Data` - Factory for creating data handles from various sources
- `ARXConfiguration` - Configuration builder for anonymity criteria and parameters
- `ARXListener` - Interface for monitoring anonymization progress

## Dependencies

- Java 1.8+
- SWT (platform-specific) for GUI
- Eclipse RCP/JFace for interface components
- Apache Commons (lang, math, io, validator)
- Apache POI for Excel support
- Various local libraries in `lib/ant/`

## Development Notes

- Both Ant and Maven builds require platform-specific SWT libraries
- The project uses a custom logging setup with Log4j 2.x
- Tests use JUnit 4 and require `data/` directory as test resource
- Local Maven dependencies must be installed via `install_deps.sh` before Maven build