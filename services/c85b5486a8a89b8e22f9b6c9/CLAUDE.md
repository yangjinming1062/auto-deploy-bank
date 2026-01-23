# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Full build with tests
./gradlew build

# Run tests only
./gradlew test

# Run a single test class
./gradlew :core:test --tests "org.spongepowered.configurate.*"

# Check (build + tests + static analysis)
./gradlew check

# API compatibility check against last release
./gradlew apiDiff

# Apply code formatting
./gradlew spotlessApply

# Generate Javadoc
./gradlew aggregateJavadoc
```

## Project Overview

Configurate is a node-based configuration library for Java supporting multiple formats (JSON, HOCON, YAML, XML). The project uses Gradle with a multi-module structure.

### Module Structure

- **core** - The core library containing the node API, `ConfigurationNode`, `ConfigurationLoader`, serialization (`TypeSerializer`), and the `ValueSource` system
- **format/** - Format loaders: `gson`, `hocon`, `jackson`, `xml`, `yaml` (each extends `AbstractConfigurationLoader`)
- **extra/** - Optional features: `kotlin` (Kotlin extensions), `guice` (Guice integration), `dfu2-7` (Mojang DataFixerUpper integration)
- **tool** - CLI tool for configuration operations
- **bom** - Maven Bill of Materials for dependency management
- **examples** - Usage examples

### Key Architecture Concepts

**ConfigurationNode** - The core interface representing a node in the config tree. Nodes can hold scalar values, map children, or list children. Navigate with `node.node(path)` and get/set values with type serializers.

**ConfigurationLoader<N>** - Interface for loading/saving config to a specific format. Each format module implements this, extending `AbstractConfigurationLoader.Builder`.

**TypeSerializer** - Converts between `ConfigurationNode` and Java objects. Registered in `TypeSerializerCollection` available via `ConfigurationOptions`.

**Null Handling** - Uses `checker-qual` annotations (`@Nullable`, `@NonNull`) instead of `Optional`. Avoid `Optional` in the codebase.

### Build Requirements

- **To build**: Java 17+ required (handled by Gradle toolchains)
- **Runtime**: Java 8+
- Multi-release JAR: Source set includes `main` (Java 8 compatible) and alternate versions for Java 10 (immutable collections) and Java 16 (records)

### Code Conventions

- Follow [Sponge code style guidelines](https://docs.spongepowered.org/stable/en/contributing/implementation/codestyle.html)
- Use `checker-qual` nullability annotations, not `Optional`
- Mark local variables and method parameters `final` when unchanged
- Lambda unused parameters: use `$` as name (e.g., `$ -> ...`)
- Minimize Guava usage; prefer JDK equivalents
- License headers required on all files (see `LICENSE_HEADER`)