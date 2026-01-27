# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Generate all source code (required before first build)
./gradlew autogenerate

# Build and install to local Maven repository
./gradlew publishToMavenLocal

# Build all modules as jars in ejml/libraries
./gradlew createLibraryDirectory

# Compile all modules into a single jar at ejml/EJML.jar
./gradlew oneJarBin

# Run all tests
./gradlew test

# Run a single test class
./gradlew :main:ejml-core:test --tests "org.ejml.EjmlUnitTests"

# Run a specific test
./gradlew :main:ejml-core:test --tests "org.ejml.EjmlUnitTests.testMatrixCreation"

# Format code
./gradlew spotlessApply

# Build javadoc
./gradlew alljavadoc
```

## Project Overview

EJML (Efficient Java Matrix Library) is a linear algebra library for manipulating real/complex/dense/sparse matrices. It provides three distinct API styles:

1. **Procedural API** (Operations) - Full control over memory and algorithms via procedural functions like `CommonOps_DDRM.mult(A, B, C)`
2. **SimpleMatrix API** - Object-oriented, flow-styled API: `A.mult(B).plus(C)`
3. **Equations API** - Symbolic interface similar to Matlab: `eq.process("K = P*H'*inv( H*P*H' + R )")`

## Architecture

### Module Structure

| Module | Purpose |
|--------|---------|
| `ejml-core` | Core data structures, interfaces, utilities |
| `ejml-ddense` | Dense real 64-bit float algorithms |
| `ejml-fdense` | Dense real 32-bit float algorithms |
| `ejml-zdense` | Dense complex 64-bit float algorithms |
| `ejml-cdense` | Dense complex 32-bit float algorithms |
| `ejml-dsparse` | Sparse real 64-bit float algorithms |
| `ejml-fsparse` | Sparse real 32-bit float algorithms |
| `ejml-simple` | SimpleMatrix and Equations APIs |
| `ejml-experimental` | Experimental features and tests |
| `ejml-kotlin` | Kotlin extensions |
| `autocode` | Code generation tools |

### Matrix Naming Convention

Matrix class format: `<DataType>Matrix<Structure>` where:
- `<DataType>`: D (double), F (float), Z (complex double), C (complex float), B (binary)
- `<Structure>`: RMaj/RM (row-major), RBlock/RB (block), NxN/FN (fixed N×N), N/FN (fixed vector), CSC/CC (sparse column), Triplet/TR (sparse triplet)

Examples: `DMatrixRMaj` (double real row-major), `ZMatrixSparseCSC` (complex double sparse CSC)

### Operation Class Naming

Algorithm classes follow pattern: `<Type><Type><Abbreviation>`:
- First letter: data type (D, F, Z, C, B)
- Second letter: storage (D=dense, S=sparse)
- Last two letters: structure abbreviation

Examples: `CommonOps_DDRM` (double dense row-major ops), `CommonOps_DSCC` (double sparse CSC ops)

### Interface Patterns

**Decomposition Pattern:**
```java
boolean decompose(T orig);  // Compute decomposition
boolean inputModified();     // Check if input is modified
T getMatrixX(...);           // Get computed result
```

**Linear Solver Pattern:**
```java
void setA(Matrix A);         // Configure with coefficient matrix
void solve(Matrix B, Matrix X);  // Solve A*X = B
void invert(Matrix A_inv);   // Invert A
```

### Code Generation

Most operations for different data types are auto-generated from 64-bit double implementations. Code generators live in `main/ejml-*/generate/` directories. Always run `./gradlew autogenerate` after modifying code generators.

### Key Directories

- `main/ejml-core/src/org/ejml/` - Core interfaces and utilities
- `main/ejml-core/src/org/ejml/data/` - Matrix data structures
- `main/ejml-core/src/org/ejml/interfaces/` - Interface definitions
- `main/ejml-core/src/org/ejml/ops/` - Operations that work across types
- `main/ejml-ddense/src/org/ejml/dense/` - Dense 64-bit implementations
- `main/autocode/src/org/ejml/` - Code generation tools
- `examples/src/org/ejml/example/` - Usage examples

### Code Standards

- Java 17 toolchain, targets Java 11 bytecode
- Error-prone and NullAway are enforced for main source
- Spotless formatting with ratchet from `origin/SNAPSHOT`
- License header required on all files (from `docs/copyright.txt`)
- Auto-generated code has `@Generated` annotation