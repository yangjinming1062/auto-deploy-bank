# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Elasticsearch repository - a distributed search and analytics engine, scalable data store, and vector database. Elasticsearch is built with Java and uses Gradle as its build system.

Key documentation:
- `README.asciidoc` - Project overview and quick start
- `BUILDING.md` - Build system guidelines and dependency management
- `TESTING.asciidoc` - Comprehensive testing guide
- `CONTRIBUTING.md` - Contribution process and guidelines
- `REST_API_COMPATIBILITY.md` - API compatibility guarantees

## Common Development Commands

### Building Distributions

Build for your local OS (outputs to `distribution/archives/`):
```bash
./gradlew localDistro
```

Build for specific platforms:
```bash
./gradlew :distribution:archives:linux-tar:assemble
./gradlew :distribution:archives:darwin-tar:assemble
./gradlew :distribution:archives:windows-zip:assemble
```

Build Docker images:
```bash
./gradlew buildDockerImage  # or buildDockerAarch64Image
```

### Running Elasticsearch

Run from source without building:
```bash
./gradlew run
```

Run with debugging enabled (port 5007):
```bash
./gradlew run --debug-jvm
```

Run with HTTPS:
```bash
./gradlew run --https
```

Run with trial license (enables paid features):
```bash
./gradlew run -Drun.license_type=trial
```

Run with specific distribution type (`oss` or default):
```bash
./gradlew run -Drun.distribution=oss
```

### Testing

Run all verification tasks (static checks, unit tests, integration tests):
```bash
./gradlew check
```

Run precommit checks only:
```bash
./gradlew precommit
```

Run unit tests for a specific module:
```bash
./gradlew :server:test
./gradlew :modules:aggregations:test
```

Run a single test:
```bash
./gradlew :server:test --tests org.elasticsearch.package.ClassName
```

Run all tests in a package:
```bash
./gradlew :server:test --tests 'org.elasticsearch.package.*'
```

Run integration tests:
```bash
./gradlew internalClusterTest
```

Run YAML REST tests:
```bash
./gradlew :rest-api-spec:yamlRestTest
```

Run Java REST tests:
```bash
./gradlew :modules:mapper-extras:javaRestTest
```

Run backwards compatibility tests:
```bash
./gradlew bwcTest
```

Debug tests (attach debugger on port 5005):
```bash
./gradlew :server:test --debug-jvm
```

Debug REST tests server (attach debugger on port 5007):
```bash
./gradlew :rest-api-spec:yamlRestTest --debug-server-jvm
```

Test with specific random seed:
```bash
./gradlew test -Dtests.seed=DEADBEEF
```

Repeat tests N times:
```bash
./gradlew :server:test -Dtests.iters=N --tests org.elasticsearch.package.ClassName
```

### Dependency Management

When adding/updating dependencies, Gradle dependency verification requires checksums in `gradle/verification-metadata.xml`. Generate/update them automatically:
```bash
./gradlew --write-verification-metadata sha256 precommit
```

### Testing Against Different Java Versions

Test against Java pre-release versions:
```bash
./gradlew clean test -Druntime.java=26-pre
```

### Viewing Available Tasks
```bash
./gradlew tasks
```

View project structure:
```bash
./gradlew projects
```

## Code Architecture

### Major Components

**Server Core** (`server/`):
- Main Elasticsearch server implementation
- Key packages: `action` (REST handlers), `cluster` (cluster management), `index` (index operations), `search` (search functionality), `indices` (index management), `http` (HTTP server)

**Modules** (`modules/`):
- Optional, loadable Elasticsearch features
- Examples: `aggregations`, `analysis-common`, `ingest-*` (ingest pipelines), `lang-*` (Painless scripting), `repository-*` (snapshot repositories), `mapper-*` (field mappers)

**Plugins** (`plugins/`):
- Optional plugins that can be installed separately
- Examples: analysis plugins (icu, kuromoji, nori, etc.), discovery plugins (ec2, gce), repository plugins (hdfs)

**X-Pack** (`x-pack/`):
- Commercial features and extensions (security, monitoring, ML, etc.)
- Includes additional plugins, qa tests, and tooling

**Client Libraries** (`client/`):
- REST client and utilities
- Includes `rest` (low-level REST client), `sniffer` (cluster sniffing)

**Distribution** (`distribution/`):
- Builds platform-specific packages (tar, zip, docker, deb, rpm)
- Includes packaging logic and tools

**Test Framework** (`test/framework/`):
- Shared testing utilities and base classes

**REST API Specification** (`rest-api-spec/`):
- JSON specifications for all REST APIs
- Used for client generation and API compatibility

### REST API Design

The REST API is formally specified in JSON files under `rest-api-spec/src/main/resources/rest-api-spec/api/`. Each API has:
- Stability level (`experimental`, `beta`, `stable`)
- URL paths and HTTP methods
- Request parameters and body specification
- Response format

YAML REST tests (`rest-api-spec/src/yamlRestTest/resources/`) are the preferred way to test REST APIs as they're shared across all official Elasticsearch clients.

### Build System Structure

The Gradle build uses a composite build pattern with three sub-projects:

1. **build-conventions** - Build conventions applied to all projects
2. **build-tools** - Public build logic for plugin authors (published as `org.elasticsearch.gradle:build-tools:<version>`)
3. **build-tools-internal** - Internal Elasticsearch-specific build logic

Key build guidelines:
- Use task avoidance API (`tasks.register` not `task`)
- Register test clusters lazily (`testClusters.register`)
- Dependencies managed via `build-tools-internal/version.properties`
- Component metadata rules handle transitive dependencies

### Dependency Management

Elasticsearch uses strict dependency management:
- All dependency versions in `build-tools-internal/version.properties`
- Transitive dependencies explicitly controlled via component metadata rules
- Gradle dependency verification with SHA256 checksums required
- Common patterns:
  - `ExcludeAllTransitivesRule` - exclude all transitive deps
  - `ExcludeOtherGroupsTransitiveRule` - keep same-group deps only
  - `ExcludeByGroup` - exclude specific group

### Test Architecture

Test base classes (in order of preference):
1. `ESTestCase` - Unit tests
2. `ESSingleNodeTestCase` - Single node integration tests (lightweight)
3. `ESIntegTestCase` - Multi-node in-JVM tests (for cluster behavior)
4. `ESRestTestCase` - REST API integration tests via HTTP
5. `ESClientYamlSuiteTestCase` - YAML-based REST tests (preferred for REST testing)

Test locations:
- Unit/integration tests: alongside source in `src/test/java/`
- QA tests: in `qa/` subprojects (can run in parallel)
- Packaging tests: destructive tests (run on ephemeral systems only)
- BWC tests: test upgrades from previous versions

## Development Notes

### Adding New Tests

- **Prefer unit tests** over integration tests when possible
- **Use YAML REST tests** for API functionality (shared with clients)
- **Use REST tests** (`ESRestTestCase`) for realistic integration testing
- **Refactor code to enable unit testing** if it's hard to test

### API Changes

When modifying REST APIs:
1. Update JSON spec in `rest-api-spec/src/main/resources/rest-api-spec/api/`
2. Add/modify YAML tests in `rest-api-spec/src/yamlRestTest/resources/`
3. Ensure backward compatibility (stable APIs: additions only within major version)
4. Mark experimental features appropriately
5. Update REST compatibility docs if needed

### Module/Plugin Development

- **Modules** (`modules/`) - built into Elasticsearch distributions
- **Plugins** (`plugins/`) - optional, installable separately
- Both use the `elasticsearch.esplugin` Gradle plugin
- Build tools for plugin authors are published from `build-tools/`

### Working with Dependencies

When adding dependencies:
1. Add version to `build-tools-internal/version.properties`
2. Add dependency to appropriate `build.gradle`
3. Configure transitive dependencies via component metadata rules
4. Generate checksums: `./gradlew --write-verification-metadata sha256 precommit`
5. Update tests if needed (FIPS mode considerations for security features)

### FIPS 140-2 Considerations

Some tests run in FIPS 140-2 mode:
- JKS/PKCS#12 keystores cannot be used (use PEM instead)
- Passwords must be >14 chars when using PBKDF2
- Hostname verification cannot be disabled
- Private keys must be >2048 bits
- Mute tests with `assumeFalse("reason", inFipsJvm())` or YAML skip feature

## Project Structure Quick Reference

```
/                          # Root
├── server/                # Core Elasticsearch server
│   └── src/main/java/org/elasticsearch/
│       ├── action/        # REST actions and handlers
│       ├── cluster/       # Cluster state and management
│       ├── index/         # Index operations and shard management
│       ├── search/        # Search execution and aggregations
│       ├── indices/       # Index management
│       ├── http/          # HTTP server
│       └── rest/          # REST controller layer
├── modules/               # Optional Elasticsearch modules
├── plugins/               # Optional installable plugins
├── x-pack/                # Commercial features (security, ML, etc.)
├── client/                # Client libraries
├── distribution/          # Packaging and distribution builds
├── rest-api-spec/         # REST API JSON specifications
└── test/                  # Test framework and fixtures
```

## Important Files

- `gradle/verification-metadata.xml` - Dependency checksums (auto-generated)
- `build-tools-internal/version.properties` - All dependency versions
- `muted-tests.yml` - Tests disabled due to known issues
- `rest-api-spec/README.markdown` - REST API specification format
- `settings.gradle` - Gradle project structure
- `build.gradle` (root) - Root build configuration