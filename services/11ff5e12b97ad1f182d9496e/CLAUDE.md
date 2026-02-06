# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Open Liberty is a lightweight, open-source Java application server implementing the Jakarta EE and MicroProfile specifications. It's built using OSGi bundles with Gradle as the build system and bnd tools for bundle configuration.

## Build Commands

```bash
# Initialize the build environment
cd dev
./gradlew cnf:initialize

# Build the runtime (assembles all bundles)
./gradlew assemble

# Run unit tests only
./gradlew test

# Build and run a FAT test project
./gradlew build.example_fat:buildandrun

# Full build (assemble + test)
./gradlew build
```

**Prerequisites:**
- `JAVA_HOME` must point to a Java 17 or Java 21 SDK
- If using Java 17, also set `JAVA_21_HOME` to a Java 21 SDK for compilation
- Default JVM args: `-Xmx6400m` (configured in `dev/gradle.properties`)

## Architecture

### OSGi Bundle Structure

Most modules are OSGi bundles using `bnd.bnd` files for configuration. A typical bundle project contains:

```
dev/<project-name>/
├── bnd.bnd           # Bundle manifest and build configuration
├── src/              # Source code (not tests)
├── resources/        # Non-Java resources
├── test/             # Unit tests (JUnit)
├── fat/              # FAT test sources (see below)
└── publish/          # Test servers, applications for FATs
```

### FAT Tests (Functional Acceptance Tests)

FAT tests use ShrinkWrap for application packaging and the componenttest framework. Structure:

```
fat/src/com/ibm/ws/<feature>/
├── FATSuite.java     # Test suite entry point with @SuiteClasses
└── <TestClass>.java  # Test classes extending FATServletClient or FATRunner

test-applications/    # ShrinkWrap application sources
```

Common FAT test patterns:
- `@RunWith(FATRunner.class)` - Required for FAT tests
- `@Server("ServerName")` - Injects LibertyServer (servers live in `publish/servers/`)
- `@TestServlet(servlet = MyServlet.class, contextRoot = "app")` - Defines test servlets
- `@Mode(TestMode.LITE|FULL|QUARANTINE)` - Test execution modes
- `ShrinkHelper.defaultApp(server, "appName", "package.to.include")` - Package test apps
- `RepeatTests` @ClassRule for running tests across feature versions (EE8, EE9, EE10, EE11)

### Feature Modules

Features are defined in `com.ibm.websphere.appserver.features/` and `io.openliberty.*` directories. Each feature contains:
- `features/` - Feature manifest files
- `bnd.bnd` - Bundle configuration with `-dsannotations` for OSGi DS components

### Key Directories

- `dev/cnf/` - Central build configuration, resources, and dependency indexes
- `dev/wlp-gradle/` - Gradle configuration and shared build scripts
- `dev/fattest.simplicity/` - FAT test framework (componenttest classes)
- `dev/build.sharedResources/` - Shared test resources and libraries

## Code Standards

- **License Header**: All files must include the EPL 2.0 license header (see existing files for exact format)
- **Commits**: Must be GPG/SSH signed (see https://github.com/OpenLiberty/open-liberty/wiki/Signing-commits)
- **Pull Requests**: Target the `integration` branch
- **Tests**: All PRs must have passing builds and be reviewed by a team member

## Dependency Management

Dependencies are managed through bnd repositories configured in `dev/cnf/`:
- `oss_dependencies.maven` - Open source dependencies
- `oss_ibm.maven` - IBM-specific open source
- Dependency conflicts are resolved via Artifactory if configured in `~/gradle.startup.properties`