# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

**Requirements:** JDK 21+ required to build.

```bash
# Build the project and run unit tests
./gradlew build

# Build IDE project files (run this once before opening in IntelliJ/Eclipse)
./gradlew ide

# Build with a custom webapp (from sonarqube-webapp repository)
WEBAPP_BUILD_PATH=/path/to/sonarqube-webapp/server/sonar-web/build/webapp ./gradlew build

# Generate license headers
./gradlew licenseFormat --rerun-tasks

# Run a single test class
./gradlew :server:sonar-db-dao:test --tests "org.sonar.db.permission.GroupPermissionDaoTest"

# Run a single test method
./gradlew :server:sonar-db-dao:test --tests "org.sonar.db.permission.GroupPermissionDaoTest.shouldFailToDeleteUserIfNotExists"

# List all dependencies
./gradlew dependencies

# Build the distribution (output in sonar-application/build/distributions/)
./gradlew dist
```

## Architecture Overview

SonarQube is a modular Gradle multi-module project with these major subsystems:

### Server Modules (`server/`)

| Module | Purpose |
|--------|---------|
| `sonar-main` | Application entry point, process management, cluster health monitoring |
| `sonar-process` | Process launching and supervision |
| `sonar-db-dao` | Data access layer for PostgreSQL, MySQL, Oracle, SQL Server |
| `sonar-db-migration` | Database schema migrations |
| `sonar-ce` | Compute Engine - orchestrates code analysis tasks |
| `sonar-ce-task` | CE task container and execution framework |
| `sonar-ce-task-projectanalysis` | Project analysis logic executed by CE |
| `sonar-webserver-*` | HTTP server (Tomcat embed), Web APIs, authentication, Elasticsearch integration |
| `sonar-alm-client` | Azure DevOps, Bitbucket, GitHub, GitLab API clients |
| `sonar-auth-*` | Authentication plugins (LDAP, SAML, GitHub, GitLab, Bitbucket) |
| `sonar-telemetry*` | Telemetry collection |

### Scanner/Analysis Modules (root level)

| Module | Purpose |
|--------|---------|
| `sonar-scanner-engine` | Local analysis scanner (CLI) - downloads plugins, fetches config, reports results |
| `sonar-scanner-protocol` | Protobuf definitions for scanner-server communication |
| `sonar-scanner-engine-shaded` | Fat JAR distribution of scanner engine |
| `sonar-ws` | Web service client/server (REST API) |
| `sonar-duplications` | Code duplication detection |
| `sonar-sarif` | SARIF report ingestion |
| `sonar-markdown` | Markdown processing |
| `sonar-plugin-api-impl` | Plugin API implementation |

### Plugin Modules (`plugins/`)

| Module | Purpose |
|--------|---------|
| `sonar-xoo-plugin` | Sample language plugin for testing (XOO) |
| `sonar-education-plugin` | Education/metrics plugin |

### Key Package Patterns

- **`org.sonar.server.*`** - Server-side components follow domain-driven patterns with packages like `component`, `issue`, `qualitygate`, `qualityprofile`
- **`org.sonar.ce.task.projectanalysis.*`** - Analysis steps organized into `step/` package with implementations for different analyses
- **`org.sonar.batch.bootstrapper`** - Scanner entry point that bootstraps the analysis
- **`org.sonar.scanner.*`** - Scanner-side components for local analysis
- **`org.sonar.db.*`** - DAO pattern with `dialect/` for database abstraction

## Source Structure

```
src/
  main/java/          # Java sources
  main/protobuf/      # Protocol Buffer definitions
  test/java/          # JUnit tests
  test/resources/     # Test fixtures and data
  it/java/            # Integration tests
  it/resources/       # Integration test resources
  bbt/java/           # Black-box tests
  bbt/resources/      # Black-box test resources
```

## Key Technologies

- **Java 21** (scanner-engine produces Java 17 bytecode for compatibility)
- **Gradle 8.14** with Kotlin DSL
- **Spring 7.x** (context, webmvc, security-saml2)
- **Elasticsearch 8.x** for issue/index storage
- **MyBatis** for database access
- **JUnit 5** (migration from JUnit 4 in progress)
- **Protocol Buffers** for scanner-server communication
- **Tomcat 11** embedded servlet container

## License Headers

All source files must include the LGPL-3.0 license header from `HEADER`. Run `./gradlew licenseFormat --rerun-tasks` to apply headers.

## Contributing

- External contributions are limited to minor cosmetic changes and typo fixes
- Follow SonarSource code style: https://github.com/SonarSource/sonar-developer-toolset#code-style
- Pre-commit hooks run secrets detection via sonar-secrets-pre-commit
- Pull requests are reviewed but may be closed if not aligned with roadmap