# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Koloboke is a family of Java projects around collections, consisting of:
- **Koloboke Collections API** (`lib/api`): Carefully designed extension of Java Collections Framework with primitive specializations
- **Koloboke Compile** (`compile`): Annotation processor that generates collection implementations at compile time
- **Koloboke Implementation Library** (`lib/impl`): Efficient implementations of the collections API

## Build Requirements

- Java 8 compiler required for building (`JAVA_HOME` must point to JDK 8)
- JDK 9 required in a sibling `jdk-9` directory for some builds
- JDK 6 and JDK 7 required in sibling `jdk1.6` and `jdk1.7` directories for meta project development
- Gradle 2.0 (via wrapper)

## Build Commands

```bash
# Build meta projects (code generators like jpsg, template processors)
./gradlew :buildMeta

# Build main projects without running tests or findbugs
./gradlew buildMain -x test -x findbugsMain -x findbugsTest

# Rebuild meta projects (code generators)
./gradlew :cleanMeta :buildMeta

# Rebuild main projects from lib/, benchmarks/, or root
./gradlew cleanMain buildMain

# Build for specific Java version (6 or 8)
./gradlew cleanMain buildMain -PlibTargetJava=8
```

## Architecture

### Code Generation System

This project uses a template-based code generation system:

1. **jpsg** (Java Pattern Stream Generator): A custom code generation framework (`jpsg/`)
   - Defines `.jbbm` template files with placeholders for types and configurations
   - Processes templates via annotation processors to generate specialized implementations

2. **Template Processors** (`lib/template-processors`):
   - `MethodGeneratingProcessor`: Generates method implementations from templates
   - `FunctionProcessor`: Generates functional interface specializations
   - `Jdk8FunctionReplacer`: Replaces Java 6/7 function types with Java 8 equivalents

3. **Generated Code**:
   - Templates are in `src/main/javaTemplates/` directories
   - Generated code goes to `build/generated-src/jpsg/`
   - Generated sources are added to compilation via `sourceSets*.output.classesDir`

### Module Structure

| Module | Purpose |
|--------|---------|
| `lib/api` | Public collection interfaces (Map, Set, etc.) |
| `lib/impl-common` | Shared implementation utilities (hash tables, equivalence) |
| `lib/impl` | Concrete implementations of API interfaces |
| `lib/template-processors` | Annotation processors for template processing |
| `lib/impl-generator` | Generates impl from templates |
| `compile` | `@KolobokeMap`/`@KolobokeSet` annotation processor |
| `jpsg/core` | Core code generation framework |
| `jpsg/gradle-plugin` | Gradle plugin for jpsg tasks |

### Key Configuration Properties

- `libTargetJava`: Target Java version for lib modules (6 or 8, default 6)
- `javadocExecutable`: Path to javadoc executable for Javadoc generation
- `jdkSrc`: Path to uncompressed JDK sources for Javadoc links

## IDE Setup

```bash
./gradlew idea
```

Then open project in IntelliJ IDEA. Annotation processor auto-generation is configured for IntelliJ.

## Running Tests

```bash
# Run tests for a specific project
./gradlew :lib:api:test

# Run single test class
./gradlew :lib:impl:test --tests "*HashIntIntMapTest*"
```

## Key Concepts

### Collections Primitive Specializations

The library provides specialized collections for primitive types:
- `HashIntIntMap`, `HashLongObjMap`, `HashObjDoubleMap`, etc.
- Avoids boxing/unboxing overhead for performance-critical code

### Hash Configuration

Uses configurable hash tables via `HashConfig`:
- Linear probing by default (growth factor must be 2.0)
- Quadratic hashing available for custom growth factors
- Load factors configured via `HashConfig.fromLoads(min, ideal, max)`

### Mutability Options

- `Mutable`: Full read/write operations
- `Updatable`: Only `clear()`, throws `UnsupportedOperationException` on removes
- `Immutable`: No modifications after creation