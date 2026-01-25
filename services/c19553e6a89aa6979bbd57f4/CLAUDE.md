# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SOFALookout is a multi-dimensional metrics monitoring system based on the Metrics 2.0 standard. It provides tools for metrics collection, processing, storage, and querying. The project consists of two main parts:

- **Client**: A Java library for instrumenting applications to collect metrics
- **Server/Gateway**: A monitoring service for collecting, processing, storing, and querying metrics

## Build Commands

```bash
# Full build (skip tests)
mvn clean install -DskipTests

# Run tests
mvn test

# Run a single test
mvn test -Dtest=TestClassName

# Format code (uses Formatter.xml)
mvn java-formatter:format

# Add license headers (uses HEADER file)
mvn license:format

# Pre-commit check
./check_format.sh
```

Requirements: Maven 3.2.5+, JDK 1.6+

## Architecture

### Core Modules

- **client/**: Java SDK for metrics instrumentation. Uses SPI for extensibility (implement `MetricsImporter` interface). Contains extensions for JVM (`lookout-ext-jvm`) and OS (`lookout-ext-os`) metrics.

- **gateway/**: Collects, processes, and exports metrics
  - `gateway/core`: Core gateway logic
  - `gateway/metrics/pipeline`: Metrics processing pipeline
  - `gateway/metrics/importer/*`: Adapters for external sources (Prometheus, OpenTSDB, Metricbeat, standard)
  - `gateway/metrics/exporter/*`: Exporters (Elasticsearch, standard)

- **server/**: Core monitoring service with storage and querying
  - `server/metrics/promql`: PromQL query engine (ported from Prometheus)
  - `server/metrics/storage-ext-es`: Elasticsearch storage backend
  - `server/metrics/interfaces`: Storage interfaces

- **boot/**: Spring Boot bootstrap applications
  - `gateway-bootstrap`: Runs the gateway service
  - `metrics-server-bootstrap`: Runs the server service
  - `all-in-one-bootstrap` (sofaark profile): Combined gateway + server

### Bootstrap Entry Points

- `com.alipay.sofa.lookout.all.boot.LookoutAllBootstrap` - All-in-one
- `com.alipay.sofa.lookout.boot.GatewayBootstrap` - Gateway only
- `com.alipay.sofa.lookout.boot.ServerBootstrap` - Server only

## Contributing Guidelines

- All new Java files must include the ASF license header (from HEADER file)
- Add `@author` tag to modified classes
- Use `Formatter.xml` for code formatting
- Follow [conventional commit messages](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)
- Include `Fixes gh-XXXX` in commit messages for issue fixes

## Documentation

- [README_EN.md](./README_EN.md) - Project overview
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Development guidelines
- [client/README.md](./client/README.md) - Client SDK documentation
- [WIKI](https://github.com/sofastack/sofa-lookout/wiki) - Full documentation