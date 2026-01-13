# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Apache Solr project - a blazing-fast, open source, multi-modal search platform built on Apache Lucene. It powers full-text, vector, and geospatial search at many of the world's largest organizations.

## Development Requirements

- **Java**: Java 21 JDK or later required (Eclipse Temurin recommended from https://adoptium.net/)
- **Python**: Python 3 required for documentation validation
- **Build System**: Gradle (use `./gradlew` wrapper - it handles Gradle version automatically)

## Architecture

Solr is structured as a multi-module Gradle project with a composite build alongside Apache Lucene:

### Main Modules

- **core**: Core Solr search server functionality
- **solrj**: Solr Java client for interacting with Solr servers
- **server**: Embedded Jetty server for running Solr
- **api**: Solr APIs
- **test-framework**: Shared test utilities
- **modules/**: Optional Solr modules:
  - analysis-extras, clustering, cross-dc, cuvs, opentelemetry
  - extraction, gcs-repository, jwt-auth, langid, llm, ltr
  - s3-repository, scripting, sql
- **webapp**: Admin UI web application
- **ui**: Modern web-based admin interface
- **documentation**: Build tooling for documentation
- **solr-ref-guide**: Solr Reference Guide (Antora-based)
- **packaging**: Creates distribution packages
- **docker**: Docker image build
- **benchmark**: Performance benchmarking tools
- **example**: Example configurations and data

### Build Configuration Files

- **build.gradle**: Main build configuration with extensive task definitions
- **settings.gradle**: Project structure and included builds
- **gradle/libs.versions.toml**: Version catalog for all dependencies
- **gradle/**: Extensive Gradle configuration scripts organized by concern

## Common Development Commands

### Building and Running

```bash
# Create a development Solr distribution
./gradlew dev

# Run the dev Solr instance
cd ./solr/packaging/build/dev
bin/solr start

# Build final Solr artifacts
./gradlew assemble

# Create dev distribution (slim version without contribs/modules)
./gradlew devSlim

# Create full development distribution (includes contribs/modules)
./gradlew devFull
```

### Testing

```bash
# Run all tests
./gradlew test

# Run tests for a specific module
./gradlew :solr:core:test

# Run a specific test class
./gradlew :solr:core:test --tests "*TestClassName*"

# Clean and run all tests
./gradlew clean test
```

**Testing Notes:**
- Tests use extensive randomization for finding edge cases
- Each test has a reproducible seed (shown in "reproduce with" message)
- Some tests are flaky on certain systems but pass on Jenkins
- When tests fail, use the "reproduce with" command for debugging

### Validation and Code Quality

```bash
# Run all validation tasks (includes linting, dependency checks, tests)
./gradlew check

# Format code and update licenses
./gradlew tidy updateLicenses check -x test

# Pre-commit validation (run before creating PR)
./gradlew tidy updateLicenses check -x test

# List all available tasks
./gradlew help
```

**Pre-commit Requirement:**
Before creating a PR, always run: `./gradlew tidy updateLicenses check -x test`

This will:
- Format your code according to project style
- Update licenses for any changed dependencies
- Run all validation and linting checks
- Skip tests (run tests separately)

### Documentation

```bash
# Build documentation
./gradlew -p solr documentation

# Build the reference guide (Antora-based)
./gradlew -p solr/solr-ref-guide build

# Validate documentation (requires Python 3)
./gradlew -p solr documentation
```

## Development Workflow

### For New Contributors

1. **Fork** the repository on GitHub
2. **Create a JIRA issue** at https://issues.apache.org/jira/projects/SOLR/issues
3. **Create a branch** in your fork for the issue
4. **Make changes** and test thoroughly
5. **Run pre-commit**: `./gradlew tidy updateLicenses check -x test`
6. **Open a PR** against the `main` branch
7. **Title format**: `SOLR-12345: Your change description`
8. **Use draft PRs** for work-in-progress

**Look for issues labeled "newdev"** for beginner-friendly starting points: https://s.apache.org/newdevolr

### Code Style Guidelines

- Follow existing code style in files you edit
- Do NOT reformat unrelated code in the same PR
- Remove obsolete code rather than commenting it out
- Add comments for non-obvious functionality
- Keep changes focused on the specific issue
- Write unit tests for new functionality
- Update documentation as needed

## Key Documentation

- **dev-docs/**: Developer documentation (README.adoc has index)
- **dev-docs/solr-source-code.adoc**: Building, testing, and running Solr from source
- **dev-docs/how-to-contribute.adoc**: Detailed contribution workflow
- **CONTRIBUTING.md**: High-level contribution guide
- **help/**: Additional plain-text help files (auto-generated from Gradle)

## Testing and Debugging

Solr's test suite uses randomization which helps find edge cases. Key points:

1. **Reproducible**: Each test run includes a seed for reproducibility
2. **Debugging**: Use the "reproduce with" command from test output
3. **Flaky tests**: Some tests fail intermittently on certain systems
4. **Randomization**: Controlled by `tests.seed` system property
5. **Parallel testing**: Tests may run in parallel by default

**Running a failing test repeatedly:**
```bash
# Use the exact command from "reproduce with:" message
./gradlew :solr:core:test --tests "*TestName*" -Dtests.seed=ABC123
```

## Useful Information

- **Admin UI**: http://localhost:8983/solr/ (after starting dev Solr)
- **Version**: Currently at 11.0.0-SNAPSHOT (see build.gradle line 53)
- **Lucene Version**: Uses Lucene 10.3.2 (see gradle/libs.versions.toml)
- **Python**: Required for documentation validation
- **Java versions**: Main project uses Java 21+, SolrJ uses separate version requirement

## Module-Specific Notes

### Testing Specific Modules

```bash
# Core Solr functionality
./gradlew :solr:core:test

# Java client library
./gradlew :solr:solrj:test

# Test framework
./gradlew :solr:test-framework:test

# Optional modules
./gradlew :solr:modules:analysis-extras:test
./gradlew :solr:modules:clustering:test
```

### Working with Dependencies

Dependencies are managed via **gradle/libs.versions.toml** (version catalog). Key dependency groups:

- **Apache Lucene**: Core search library
- **Jetty**: Embedded server
- **Jackson**: JSON processing
- **Zookeeper**: Coordination service
- **Curator**: Zookeeper client
- **Various contrib libraries** (Tika, OpenNLP, etc.)

## Troubleshooting

### Build Issues

```bash
# Clean everything
./gradlew clean

# Clean and start fresh
./gradlew clean build -x test

# Check Gradle version
./gradlew --version
```

### Test Failures

1. Check if test fails without your changes (compare to main branch)
2. Use the "reproduce with" command
3. Some tests are known flaky - ask on dev list if unsure
4. Never add @Ignore without community consensus

### Documentation Issues

- Ensure Python 3 is on PATH
- Run: `./gradlew -p solr documentation`
- Check dev-docs/ for documentation building details

## Contact and Support

- **Developer Mailing List**: See https://solr.apache.org/community.html
- **Slack**: #solr-dev channel
- **IRC**: #solr-dev on libera.chat
- **JIRA**: https://issues.apache.org/jira/browse/SOLR