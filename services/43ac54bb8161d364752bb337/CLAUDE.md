# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NDBench (Netflix Data Benchmark) is a pluggable cloud-enabled benchmarking tool for data store systems. It supports multiple data stores (Cassandra, Redis, DynamoDB, Elasticsearch, Geode, JanusGraph, Dynomite) and allows dynamic configuration changes during benchmark runs.

## Build Commands

**Build the project:**
```bash
./gradlew build
```

**Run tests:**
```bash
./gradlew test
```

**Run a single test:**
```bash
./gradlew :ndbench-core:test --tests "com.netflix.ndbench.core.NdbenchDriverTest"
```

**Start the web application (development mode):**
```bash
./gradlew appRun
```

## Architecture

### Multi-Module Gradle Project

The project uses a multi-module structure defined in `settings.gradle`:

- **ndbench-api** - Plugin interfaces and annotations for benchmark clients
- **ndbench-core** - Main benchmark driver logic, resources, and configuration
- **ndbench-web** - WAR packaged web application with Jersey/Guzzle REST API
- **ndbench-*-plugins** - Plugin implementations for various data stores (cass, dynamodb, dax, es, geode, janusgraph, dyno, cockroachdb)
- **ndbench-aws** - AWS-specific discovery and configuration
- **ndbench-cli** - Command-line interface

### Plugin System

Plugins implement `NdBenchClient` interface and are discovered via Java's ServiceLoader mechanism using the `@NdBenchClientPlugin` annotation. The plugin architecture:

1. **Core API** (`ndbench-api` module):
   - `NdBenchClient` interface - Main client contract with `readSingle()`, `writeSingle()`, `init()`, `shutdown()` methods
   - `NdBenchMonitor` - Monitoring/metrics interface
   - `DataGenerator` - Data generation interface
   - `@NdBenchClientPlugin` - Guice binding annotation for plugin discovery

2. **Plugin Implementation Pattern**:
   - Create a class implementing `NdBenchClient`
   - Annotate with `@NdBenchClientPlugin("pluginName")`
   - Create a Guice module extending `NdBenchClientPluginGuiceModule`
   - Add to `META-INF/services/com.netflix.ndbench.api.plugin.NdBenchClient`

### Key Components (ndbench-core)

- **NdBenchDriver** - Core benchmark orchestrator managing read/write operations and rate limiting
- **Resource REST endpoints** (`core/resources`) - `NdBenchResource`, `NDBenchConfigResource`, `NDBenchClusterResource`
- **Generators** (`core/generators`) - Key and data generators (Random, Zipfian, SlidingWindow patterns)
- **Operations** (`core/operations`) - Read/Write operation execution logic
- **Discovery** (`core/discovery`) - `IClusterDiscovery` implementations for AWS, CF, Local environments

### Dependency Injection

Uses Google Guice for DI. Main module is `NdBenchGuiceModule`. Web listener configures Jersey + Guice in `InjectedWebListener`.

### Configuration

- Uses Archaius2 for configuration management
- Environment-specific configs via `DISCOVERY_ENV` variable (AWS, CF, Local)
- Default properties in `laptop.properties` for local development

## Contribution Guidelines

- Active development branch is `dev`, stable is `master`
- Submit PRs to `dev` branch
- For major features, create an issue first for discussion