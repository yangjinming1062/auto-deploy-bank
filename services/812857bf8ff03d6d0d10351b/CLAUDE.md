# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Building

```bash
# Build the entire project
mvn clean install

# Build only a specific module
cd agent/core && mvn clean install

# Build without running integration tests
mvn clean install -DskipITs

# Run with Checker Framework (required for builds with TARGET=checker)
travis-build/travis-build.sh checker
```

The first `mvn clean install` will automatically install Node.js, Bower, and Grunt locally under the `ui` directory.

Binary distribution is built under `agent/dist/target`.

### Testing

```bash
# Run all tests
mvn test

# Run all tests including integration tests
mvn verify

# Run a specific test class
mvn test -Dtest=TransactionTest

# Run a specific test method
mvn test -Dtest=TransactionTest#testNestedTimers

# Run integration tests only
mvn failsafe:integration-test

# Run a specific integration test
mvn failsafe:integration-test -Dit.test=WeavingIT

# Run tests for a specific module
cd agent/core && mvn test
```

### UI Development

```bash
# From the ui directory, serve UI with live reload (port 9000)
cd ui && ./grunt serve

# Build and deploy UI assets (done automatically during Maven build)
cd ui && ./grunt

# Serve UI with demo backend
cd ui && ./grunt serve:demo
```

When running `./grunt serve`, it:
- Serves web assets on http://localhost:9000 without concat/minify
- Reverse proxies API requests to http://localhost:4000
- Watches for file changes and performs live reload

To work on the UI with sample data, run `org.glowroot.ui.sandbox.UiSandboxMain` under a debugger. This starts Glowroot and generates sample traces. Connect browser to http://localhost:4000.

### Microbenchmarks

```bash
cd agent/benchmarks

# Build benchmarks
mvn clean package

# Run benchmarks
java -jar target/benchmarks.jar -jvmArgs -javaagent:path/to/glowroot.jar
```

### Running Glowroot

To test the complete application:
1. Build with `mvn clean install`
2. Start central collector: `central/target/glowroot-central-<version>/bin/glowroot-central.sh`
3. Run application with agent: `java -javaagent:agent/dist/target/glowroot-<version>/glowroot.jar -jar your-app.jar`
4. Open browser to http://localhost:4000

## Code Architecture

### Overview

Glowroot is an Application Performance Monitoring (APM) tool consisting of:

- **Agent** (`agent/`): Java agent that uses bytecode manipulation to monitor application performance
- **Central** (`central/`): Centralized collection server (requires Java 17+)
- **UI** (`ui/`): AngularJS-based web interface
- **Wire API** (`wire-api/`): Protocol Buffer definitions for agent-central communication
- **Plugins** (`agent/plugins/`): Instrumentation plugins for various frameworks and libraries

### Key Modules

#### Agent Modules

- **agent/core**: Core agent functionality including:
  - Bytecode weaving (`weaving/`) - modifies classes at load time
  - Transaction tracking and trace collection (`model/`, `impl/`)
  - Configuration management (`config/`)
  - Live JVM monitoring (`live/`)
  - Central collector communication (`central/`, `collector/`)

- **agent/embedded**: Embedded collector that runs in the same JVM as the monitored application (uses embedded H2 database)

- **agent/shaded/**: Shaded third-party dependencies under `org.glowroot.agent.shaded` to avoid version conflicts

- **agent/plugins/**: Instrumentation plugins for:
  - Web: servlet, jsp, jaxrs, jaxws, jakarta-servlet
  - Data: jdbc, hibernate, cassandra, mongodb, elasticsearch
  - Messaging: jms, kafka
  - Frameworks: spring, struts, ejb, jsf, grails, play
  - Utilities: redis, netty, quartz, executor, mail, logger, http-client

- **agent/integration-tests**: Integration tests using the test harness in `agent/it-harness/`

- **agent/ui-sandbox**: Development tool that runs Glowroot with sample trace data

#### Central Module

The centralized collection server that receives data from multiple agents:
- **repo/**: Storage layer (Cassandra backend)
- **CollectorServiceImpl**: Receives trace data from agents via gRPC
- **RollupService**: Aggregates metrics across time windows
- **SyntheticMonitorService**: Manages synthetic monitoring
- **CentralAlertingService**: Handles alerting

#### UI Module

AngularJS-based SPA (Single Page Application):
- **app/**: Source assets (HTML, JS, CSS, templates)
- Built using Grunt (Bower for dependencies, concat/minify, LESS compilation)
- Served on port 9000 during development, proxied to port 4000 at runtime

#### Shared Modules

- **common/**: Shared utilities and data models
- **common2/**: Additional shared components (config, utilities)
- **wire-api/**: Protocol Buffer message definitions for agent-central communication

### Dependency Shading

All third-party libraries used by the agent are shaded under `org.glowroot.agent.shaded` to eliminate jar version conflicts with the monitored application. The shading is done in the `agent/shaded/` modules.

### Weaving Architecture

The agent uses bytecode manipulation to instrument applications:
- Classes are woven at load time using a Java agent
- Advice is applied to matched methods based on plugin configurations
- The `weaver8` module handles Java 8+ bytecode
- Support for lambda expression weaving and method handles

### Storage Modes

Glowroot supports two deployment modes:

1. **Embedded Mode**: Agent includes embedded collector with H2 database
2. **Central Mode**: Agents send data to centralized `central` server (Cassandra backend)

## Development Notes

- Uses **Immutables** annotation processing for boilerplate reduction
- Uses **Checker Framework** with Nullness and Tainting checkers (run via checker profile)
- Uses **Error Prone** for additional compile-time checks
- **SonarQube** for code quality analysis (https://sonarcloud.io)
- All agent dependencies are shaded to prevent conflicts
- Build requires Java 11+ and Maven 3.8.0+
- Agent requires Java 8+, Central requires Java 17+
- Integration tests use both custom classloader and real `-javaagent` JVM spawning modes