# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Kotlin∇ is a type-safe symbolic differentiation framework for the JVM, written in pure Kotlin. It provides automatic and symbolic differentiation with compile-time shape safety for tensors (scalars, vectors, matrices).

## Build Commands

```bash
# Build the project
./gradlew build

# Run all tests in core module
cd core && ../gradlew allTests

# Run main library tests only
./gradlew :kotlingrad:jvmTest

# Run samples as tests
./gradlew :samples:test

# Generate type-level code (required before building)
./gradlew genShapes

# Generate API documentation
./gradlew dokkaHtml
```

## Running Samples

```bash
./gradlew HelloKotlingrad       # Basic differentiation example
./gradlew Plot2D                # 2D function plotting
./gradlew Plot3D                # 3D function plotting
./gradlew MLP                   # Multilayer perceptron training
./gradlew VisualizeDFG          # Render dataflow graphs
./gradlew LinearRegression      # Linear regression demo
./gradlew VariableCapture       # Variable binding demo
```

## Architecture

### Module Structure

- **core** (`/core`): Main library (`kotlingrad`), contains:
  - `src/commonMain/kotlin/ai/hypergraph/kotlingrad/api/`: Core API (Scalar, Vector, Matrix, Tensor)
  - `src/commonMain/gen/`: Auto-generated type-level code (arity, shape types)
  - `src/jvmMain/`: JVM-specific integrations (GraalVM, graphviz)
- **samples** (`/samples`): Usage examples with various applications
- **shipshape** (`/shipshape`): Code generation plugin for type-level constructs

### Core Concepts

**Expressions as DAGs**: Functions are represented as directed acyclic graphs using sealed classes (`Fun`, `SFun`, `VFun`, `MFun`). Operators construct symbolic expressions without computation; evaluation is lazy.

**Differentiation vs Evaluation**:
- **Differentiation**: Top-down substitution applying algebraic rules (sum rule, product rule)
- **Evaluation**: Bottom-up propagation of numerical values when all variables are bound

**Shape Safety**: Uses a subtype hierarchy of type-level integers (`D3 <: D2 <: D1 <: D0`) to enforce tensor dimension compatibility at compile time. Max dimension is 12 (configurable in `shipshape/build.gradle.kts`).

**Key Interfaces**:
- `Group<T>`, `Ring<T>`, `Field<T>`: Algebraic structures with F-bounded quantification
- `Fun<X>`: Base sealed class for all expressions
- `Scalar<X>`, `Vec<X, D>`, `Mat<X, R, C>`: Tensor types with shape-encoded generics

### Type-Level Code Generation

The `shipshape` plugin generates type-safe constructors and operators in `core/src/commonMain/gen/ai/hypergraph/kotlingrad/`. Run `./gradlew genShapes` after modifying dimension limits in `shipshape/build.gradle.kts`.

## Key Entry Points

- `core/src/commonMain/kotlin/ai/hypergraph/kotlingrad/api/Scalar.kt`: Core scalar differentiation
- `samples/src/main/kotlin/ai/hypergraph/kotlingrad/samples/HelloKotlingrad.kt`: Recommended starting point
- `core/src/commonMain/kotlin/ai/hypergraph/kotlingrad/api/Vector.kt`, `Matrix.kt`: Tensor APIs

## Tests

Tests use Kotest for property-based testing. Key test categories:
- Numerical gradient checking against analytical derivatives
- Finite difference approximation validation
- Shape safety verification (should fail to compile for mismatched shapes)

## Publishing

```bash
./gradlew publishAllPublicationsToSonatypeRepository
# Then close and release at https://s01.oss.sonatype.org/index.html#stagingRepositories
```