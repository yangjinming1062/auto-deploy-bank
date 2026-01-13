# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Test Commands

### Quick Testing
- Run tests for a specific subproject: `./gradlew :<subproject>:quickTest` (e.g., `./gradlew :launcher:quickTest`)
- Run sanity checks: `./gradlew sanityCheck` (catches code style issues)
- Install Gradle locally: `./gradlew install -Pgradle_installPath=/any/path`
- Generate documentation: `./gradlew :docs:docs`

### Important Notes
- **DO NOT run `gradle build`** - The repository is massive and will take too long locally
- Use targeted testing instead of full builds
- Full test suites are executed on CI for multiple configurations

### Testing Framework
- Tests are written in [Spock framework](https://spockframework.org/spock/docs/)
- Mix of unit tests and integration tests
- Integration tests run entire Gradle builds with specific build files
- Link bug-fix tests to GitHub issues using `@Issue` annotation

## High-Level Architecture

Gradle is organized into **platforms** (coarse-grained components) and **architecture modules**:

### Core Automation Platform
Base platform providing general-purpose automation for defining and executing work:
- **core-runtime** (platforms/core-runtime): Provides runtimes/containers where code runs (Gradle client, daemon, worker processes)
- **core-configuration** (platforms/core-configuration): Build structure and work specification (project model, DSL)
- **core-execution** (platforms/core-execution): Efficient work execution (scheduling, execution, caching)

### Software Development Platform
Builds on core platform to add software development automation (compiling, testing, documenting, publishing, dependency management)

### JVM Platform
Builds on core and software platforms to support JVM-based software (Java, Kotlin, Scala)

### Extensibility Platform
Builds on core, software, and JVM platforms to support plugin development

### Native Platform
Builds on core and software platforms to support native software (Swift, C++, C)

### Cross-Cutting Modules
- **Enterprise integration** (platforms/enterprise): Gradle commercial product integration
- **IDE integration** (platforms/ide): IDE and tooling integration
- **Documentation** (platforms/documentation): Gradle documentation and samples

## Build Execution Model

Gradle runs in a client-server architecture:

1. **CLI Client** (`gradle`/`gradlew` command) connects to daemon
2. **Gradle Daemon** (long-running process) coordinates build lifecycle
3. **Worker Processes** started by daemon for specific work (compilation, test execution)

The daemon:
- Runs one request at a time
- Only acts in response to client requests
- Never runs user code in the background
- Handles task execution, caching, and state management

## Build State Model

Gradle tracks state in a hierarchy during build execution:
- **Build Process State**: Global state for entire build process (BuildProcessState)
- **Build Session State**: Single Gradle invocation state (BuildSessionState)
- **Build Tree State**: Entire build definition for execution (BuildTreeState)
- **Build State**: Individual build within definition (BuildState)
- **Project State**: Individual project state (ProjectState)

## Development Environment

### Requirements
- Adoptium JDK 17 (fixed version required for remote cache)
- IntelliJ IDEA CE or Ultimate (2021.2.2 or newer)
- IntelliJ setup: Open `build.gradle.kts` in root and select "Open as Project"

### Important Setup Notes
- Very first import takes a while (project is large)
- Revert Git changes to `.idea` folder after import
- Disable IntelliJ's folding of `org.gradle` package stacktraces (Editor → General → Console)
- Consider installing [Develocity IntelliJ plugin](https://plugins.jetbrains.com/plugin/27471-develocity) for build analysis

## Code Contribution Guidelines

### Required for All Changes
- Cover code with tests (see Testing.md)
- Add Javadoc for new public top-level types (follow Javadoc Style Guide)
- Use American English spelling (see ADR-0009)
- Add feature to release notes for new features

### Documentation
- Add documentation to User Manual and DSL Reference (platforms/documentation/docs/src/docs)
- Follow ErrorMessages Guide for error message changes
- Generate docs locally with `./gradlew :docs:docs`

### Error Messages
- Implement `ResolutionProvider` interface to add suggestions to "Try" section
- Use `NonGradleCause` interface to remove generic suggestions
- Use `CompilationFailedIndicator` for compilation failures

### Commit Guidelines
- Follow [seven rules of good commit messages](https://cbea.ms/git-commit/#seven-rules)
- [Sign off commits](https://git-scm.com/docs/git-commit#Documentation/git-commit.txt---signoff) for Developer Certificate of Origin
- Keep commits discrete and self-contained

## Copyright & Licensing

### New Files
Add Apache License 2.0 header to:
- Source files (`.java`, `.kt`, `.groovy`)
- Documentation files (`.adoc`, `.md`)

### Exempt Files (no header needed)
- Build scripts (`.kts`, `.groovy`)
- Auto-generated files
- Configuration files (`.gitignore`, etc.)
- Documentation samples and snippets
- Release notes and READMEs

## Project Structure

### Key Directories
- **subprojects/**: Historical subprojects (deprecated in favor of platforms/)
- **platforms/**: Architecture modules and platforms (main organization)
- **architecture/**: Architecture documentation (ADRs, architectural decisions)
- **build-logic/**: Build logic and infrastructure
- **testing/**: Test infrastructure and utilities
- **contributing/**: Contribution guides (Testing, Debugging, ErrorMessages, etc.)

## Working on the Codebase

### Finding Your Way Around
- Use `architecture/platforms.md` to understand where features should be implemented
- Check `architecture/runtimes.md` to understand which runtime your code runs in
- Review `architecture/build-state-model.md` to understand lifecycle constraints
- Look at existing tests in similar areas for examples (Testing.md)

### JVM Compatibility
- Some Gradle code still runs on Java 8 (be careful with Java 9+ features)
- Test across all supported operating systems (macOS, Windows, Linux)
- Normalize file paths in tests using `TextUtil` class

## Resources

- [Contributing Guide](CONTRIBUTING.md): General contribution guidelines
- [Testing Guide](contributing/Testing.md): Testing best practices
- [Debugging Guide](contributing/Debugging.md): How to debug tests and builds
- [ErrorMessages Guide](contributing/ErrorMessages.md): Error message guidelines
- [Architecture Documentation](architecture/): Detailed architecture docs
- [Good First Issues](https://github.com/gradle/gradle/labels/good%20first%20issue): Issues for new contributors
- [Help Wanted Issues](https://github.com/gradle/gradle/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22%F0%9F%8C%B3%20help%20wanted%22): More complex issues

## Community Support

- Gradle Slack: `#contributing` and `#community-support` channels
- [Gradle Forum](https://discuss.gradle.org/)
- Open an issue on GitHub to discuss changes before starting