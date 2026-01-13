# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **SonarQube** repository - an open-source platform for continuous code quality inspection. SonarQube provides the capability to not only show the health of an application but also to highlight issues newly introduced.

## Build System

- **Build Tool**: Gradle 8.14.3
- **Wrapper**: `./gradlew` (executable)
- **Java Version**: JDK 17+ (required)
- **Main Build File**: `build.gradle` at root
- **Settings File**: `settings.gradle`

## Common Development Commands

### Building and Testing

```bash
# Build the entire project (compiles, runs unit tests)
./gradlew build

# Build and run all tests without packaging
./gradlew assemble

# Run a specific test
./gradlew :server:sonar-webserver:org.sonar.server.platform.monitoring.DatabaseMonitoringTest

# Run tests for a specific module
./gradlew :server:sonar-webserver:test

# Run tests for sonar-main module
./gradlew :server:sonar-main:test

# Clean build artifacts
./gradlew clean

# Build for IDE (quicker build for initial IDE setup)
./gradlew ide
```

### License and Code Style

```bash
# Fix source headers by applying HEADER.txt
./gradlew licenseFormat --rerun-tasks

# List dependencies
./gradlew dependencies

# Upgrade Gradle wrapper
./gradlew wrapper --gradle-version 5.2.1
```

### Running SonarQube

After building, the distribution is generated in `sonar-application/build/distributions/`. Unzip and start:

```bash
# Linux
bin/linux-x86-64/sonar.sh start

# macOS
bin/macosx-universal-64/sonar.sh start

# Windows
bin\windows-x86-64\StartSonar.bat
```

## Architecture Overview

### High-Level Components

1. **sonar-application** - Application entry point and distribution packaging
   - Main class: `org.sonar.application.App` (sonar-application/src/main/java/org/sonar/application/App.java:83)
   - Packages the complete SonarQube server including:
     - Web server components
     - Compute Engine (CE)
     - Elasticsearch
     - Scanner engine
     - Database drivers

2. **server/** - Server-side components organized by functional area:
   - **sonar-main** - Main process orchestration, lifecycle management
   - **sonar-process** - Process management and inter-process communication
   - **sonar-webserver** - HTTP web server (multiple modules):
     - `sonar-webserver-core` - Core web server
     - `sonar-webserver-api` - Web API infrastructure
     - `sonar-webserver-webapi` - REST API endpoints
     - `sonar-webserver-auth` - Authentication modules
   - **sonar-ce** - Compute Engine (analysis processing)
     - `sonar-ce` - CE orchestrator
     - `sonar-ce-task` - Task execution
     - `sonar-ce-task-projectanalysis` - Project analysis workflows
   - **sonar-db-*** - Database layer
     - `sonar-db-core` - Core database utilities
     - `sonar-db-dao` - Data Access Objects
     - `sonar-db-migration` - Schema migrations
   - **sonar-server-common** - Shared server components
   - **sonar-auth-*** - Authentication providers (LDAP, SAML, GitHub, GitLab, etc.)

3. **sonar-core** - Core shared libraries and utilities

4. **sonar-scanner-engine** - Scanner engine for code analysis
   - Analyzes projects and sends results to SonarQube server
   - Used by SonarQube scanners (Maven, Gradle, etc.)

5. **sonar-plugin-api-impl** - Plugin API implementation

6. **sonar-testing-harness** - Testing utilities and test infrastructure

### Module Dependencies (from sonar-application/build.gradle:57-92)

The `sonar-application` module brings together:
- `server:sonar-ce` - Compute Engine
- `server:sonar-main` - Main process
- `server:sonar-process` - Process management
- `server:sonar-webserver` - Web server
- `sonar-core` - Core utilities
- `sonar-plugin-api-impl` - Plugin system
- `sonar-scanner-engine-shaded` - Scanner engine (shaded JAR)
- `sonar-shutdowner` - Shutdown handler

### Key Configuration

- **Main Manifest**: `sonar-application/build.gradle:53` specifies Main-Class as `org.sonar.application.App`
- **BlackBoxTest**: `buildSrc/src/main/groovy/org.sonar.build/BlackBoxTest.groovy` - Base class for integration tests
- **Testing**: Uses JUnit Jupiter (JUnit 5) - see `server:sonar-process/build.gradle:43-46`

### UI/Webapp Notes

The UI is **NOT** part of this repository. It lives in a separate repository: [sonarqube-webapp](https://github.com/SonarSource/sonarqube-webapp).

When building locally, the webapp is downloaded from Maven Central. For UI changes:

```bash
# Build UI changes
cd /path/to/sonarqube-webapp/server/sonar-web
yarn install  # first time only
yarn build

# Build sonarqube using custom webapp
cd /path/to/sonarqube
WEBAPP_BUILD_PATH=/path/to/sonarqube-webapp/server/sonar-web/build/webapp ./gradlew build
```

## Development Environment

### IDE Setup

1. Build first: `./gradlew build` or quick build: `./gradlew ide`
2. Open `build.gradle` as a project in IntelliJ or Eclipse

### Gradle Tasks

```bash
# See all available tasks
./gradlew tasks

# See all tasks (including advanced ones)
./gradlew tasks --all

# Code coverage verification
./gradlew jacocoTestCoverageVerification

# Generate coverage report
./gradlew jacocoTestReport
```

### Test Types

- **Unit Tests**: Standard JUnit tests in `src/test/java/`
- **BlackBox Tests**: Integration tests extending `BlackBoxTest` (in buildSrc)
- **Integration Tests**: Files ending with `IT.java` or tests in `it/` directories

## Module Structure Summary

```
sonarqube/
├── build.gradle              # Root build configuration
├── buildSrc/                 # Custom Gradle plugins and tasks
├── server/                   # Server-side components
│   ├── sonar-main/           # Application orchestration
│   ├── sonar-process/        # Process management
│   ├── sonar-webserver/      # HTTP server & web API
│   │   ├── sonar-webserver-core/
│   │   ├── sonar-webserver-webapi/
│   │   └── sonar-webserver-auth/
│   ├── sonar-ce/             # Compute Engine
│   ├── sonar-db-*/           # Database layer
│   └── sonar-server-common/  # Shared components
├── sonar-application/        # Distribution packaging & entry point
├── sonar-core/               # Core utilities
├── sonar-scanner-engine/     # Scanner engine for code analysis
├── sonar-plugin-api-impl/    # Plugin API implementation
└── sonar-testing-harness/    # Testing utilities
```

## Key Entry Points

- **Main Application**: `org.sonar.application.App.start()` (sonar-application/src/main/java/org/sonar/application/App.java:41)
  - Loads settings
  - Configures logging
  - Initializes file system
  - Creates and schedules processes (Web server, Compute Engine)
  - Waits for termination signals

## Important Notes

1. **JDK Requirement**: JDK 17+ is required (build.gradle:19-21)
2. **CI Integration**: Uses Cirrus CI (see `.cirrus/` directory)
3. **SonarQube Plugin**: Uses `org.sonarqube` Gradle plugin
4. **Shadow JAR**: Uses Shadow plugin to create fat JARs for distribution
5. **Elasticsearch**: Includes embedded Elasticsearch server
6. **ServiceLoader**: Uses SPI (Service Loader) for extensibility
7. **Clustering**: Supports cluster deployments (see `server/sonar-main/src/main/java/org/sonar/application/cluster/`)

## External Dependencies

- **Elasticsearch**: Search and indexing
- ** Hazelcast**: Clustering support
- **H2/PostgreSQL/MS SQL**: Database drivers
- **Logback**: Logging
- **Spring**: Dependency injection and web infrastructure
- **Guava**: Google utilities
- **Protobuf**: Serialization

## Additional Resources

- [Project Documentation](https://docs.sonarsource.com/sonarqube)
- [Contributing Guide](docs/contributing.md)
- [Code Style](https://github.com/SonarSource/sonar-developer-toolset#code-style)