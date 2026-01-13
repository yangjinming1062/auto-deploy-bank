# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Apache Geode is a distributed, in-memory data management platform providing real-time, consistent access to data-intensive applications across widely distributed cloud architectures. The project is a multi-module Gradle build with ~40+ subprojects.

## Common Development Commands

### Build Commands
- `./gradlew build` - Build the entire project
- `./gradlew devBuild` - Developer build (assemble + spotless formatting)
- `./gradlew generate` - Generate all compiler-generated sources (required for IDE setup)
- `./gradlew assemble` - Compile and jar all projects without running tests

### Code Formatting
- `./gradlew spotlessApply` - Apply code formatting to all files
- `./gradlew spotlessCheck` - Verify code formatting compliance
- Uses Spotless with Google Java Style (see `etc/eclipse-java-google-style.xml`)

### Testing Commands
- `./gradlew test` - Run all unit tests
- `./gradlew integrationTest` - Run integration tests
- `./gradlew distributedTest` - Run distributed tests (multiple cluster members)
- `./gradlew acceptanceTest` - Run acceptance tests (end-user perspective)
- `./gradlew upgradeTest` - Run upgrade/compatibility tests

### Running Individual Tests
```bash
# Run specific test class
./gradlew geode-core:test --tests ArrayUtilsTest

# Run specific distributed test
./gradlew geode-core:distributedTest --tests ConnectionPoolDUnitTest

# Run test by category
./gradlew geode-core:distributedTest -PtestCategory=org.apache.geode.test.junit.categories.GfshTest
```

View test results at `build/reports/combined/index.html`

### IntelliJ IDEA Setup

1. Run `./gradlew --parallel generate` first to create compiler-generated sources
2. Import the project: File → Open → select `build.gradle`
3. Configure project SDK to Java 1.8+
4. Set build/run tools to use Gradle (IntelliJ IDEA → Preferences → Build Tools → Gradle)
5. Import code style scheme from `etc/intellij-java-modified-google-style.xml` as "GeodeStyle"
6. Import Apache copyright from `etc/intellij-apache-copyright-notice.xml`
7. Set auto-reload for build scripts
8. Rebuild project (Build → Rebuild Project)

## Code Architecture

### Module Organization

**Core Modules:**
- `geode-core` - Main distributed system implementation (cache, regions, membership)
- `geode-gfsh` - Command-line shell for cluster management
- `geode-assembly` - Distribution packaging and installation scripts

**Feature Modules:**
- `geode-lucene` - Full-text search integration
- `geode-wan` - Wide-area network replication
- `geode-cq` - Continuous query support
- `geode-memcached` - Memcached protocol compatibility
- `geode-connectors` - External data source connectors
- `geode-management` - Cluster management and monitoring
- `geode-pulse` - Web-based monitoring UI

**Test Modules:**
- `geode-dunit` - Distributed unit testing framework
- `geode-junit` - Testing utilities and test category definitions
- `geode-concurrency-test` - Concurrency stress testing

**Legacy Support:**
- `geode-old-client-support` - Backward compatibility layers
- `geode-old-versions/*` - Old version compatibility tests (versions 1.0.0-1.15.0)

### Test Organization (in geode-core/src)
- `main/` - Production code
- `test/` - Unit tests
- `integrationTest/` - Integration tests
- `distributedTest/` - Multi-node distributed tests
- `acceptanceTest/` - End-to-end acceptance tests
- `upgradeTest/` - Version compatibility and rolling upgrade tests

### Key Packages in geode-core
- `org.apache.geode.cache` - Cache and region APIs
- `org.apache.geode.internal.cache` - Internal cache implementation
- `org.apache.geode.distributed` - Cluster membership and configuration
- `org.apache.geode.management` - Management and monitoring APIs

## Code Style Requirements

**Spotless rules enforced:**
- No wildcard imports
- No Awaitility (use GeodeAwaitility instead)
- Remove unused imports
- Specific modifier order: public/protected/private, abstract/default, static, final, transient, volatile, synchronized, native, strictfp
- Remove unhelpful javadoc stubs (@param/@throws/@return without description)
- Remove empty Javadocs and block comments
- Unix line endings
- Trailing whitespace trimmed
- Newline at end of file

**Import organization:** See `etc/eclipseOrganizeImports.importorder`

## Build Configuration

**Gradle properties** (`gradle.properties`):
- Version: 1.15.1-build.0 (development)
- Minimum Gradle: 6.8
- Parallel builds enabled
- JVM args: -Xmx3g
- Local build cache enabled

**Dependency management:**
- Custom dependency management in `build-tools/geode-dependency-management`
- Maven Central + Spring repository
- Version constraints via BOMs in `boms/` directory

## Contribution Workflow

See `.github/PULL_REQUEST_TEMPLATE.md`:
1. JIRA ticket required
2. Rebase against `develop` branch
3. Single squashed commit preferred
4. `./gradlew build` must pass
5. Unit tests required for changes
6. New dependencies must be ASF 2.0 compatible

## CI/CD Integration

**Concourse CI:** Build pipeline at `ci/` directory
- Automated testing across multiple test types
- Docker-based distributed testing (`dunitDockerImage: apachegeode/geode-build`)
- Parallel test execution

## Development Notes

- **JDK Version:** Requires Java 1.8+ (compileJVMVer and testJVMVer)
- **SCM Integration:** Git commit info embedded in builds via `writeBuildInfo` task
- **Source Generation:** Several modules use code generation (see `generate` task)
- **License Headers:** All files require Apache license header
- **Build Cache:** Local Gradle build cache enabled for faster rebuilds

## Distribution

After build:
- Installation location: `geode-assembly/build/install/apache-geode/`
- Distribution archives: `geode-assembly/build/distributions/`
- Verify with: `./geode-assembly/build/install/apache-geode/bin/gfsh version`

## Troubleshooting

- **IDE errors:** Run `./gradlew generate` to create compiler-generated sources
- **Build failures:** Check Concourse CI pipeline for expected test failures
- **Format violations:** Run `./gradlew spotlessApply` to fix automatically
- **Missing dependencies:** Run `./gradlew --refresh-dependencies`