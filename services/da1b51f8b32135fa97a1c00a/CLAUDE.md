# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

**Maven (primary build system):**
```bash
# Build all modules
mvn clean install

# Build and skip tests
mvn clean install -DskipTests

# Run smoke tests (enabled by default)
mvn test

# Build without smoke tests
mvn test -Dnosmoke

# Build specific module
cd findbugs && mvn clean install
```

**Ant (legacy build):**
```bash
ant compile     # Compile main findbugs and plugins
ant test        # Run smoke tests
ant clean       # Clean all build artifacts
```

**Note:** Requires JDK 8.x specifically (not JDK 7 or 9).

## Project Overview

FindBugs is a static analysis tool for Java bytecode that detects potential bugs. Note: FindBugs development has continued as [SpotBugs](https://spotbugs.github.io).

## Architecture

**Multi-module Maven structure:**
- `findbugs/` - Core analysis engine
- `plugins/` - 8 plugin modules (cloud integrations, poweruser features)
- `eclipsePlugin/` - Eclipse IDE integration
- `findbugsTestCases/` - Test case suite for bug detection
- `webCloudProtocol/` - Cloud service protocol definitions

**Core packages in `findbugs/src/java/edu/umd/cs/findbugs/`:**
- `detect/` - 400+ bug detector implementations
- `ba/` - Bytecode analysis infrastructure
- `classfile/` - Class file parsing
- `bugReporter/` - Bug reporting and filtering
- `cloud/` - Cloud-based bug tracking
- `visitclass/` - ASM visitor pattern classes

**Key patterns:**
- **Plugin system**: Detectors loaded dynamically via `PluginLoader`, each implementing `Detector` interface
- **Visitor pattern**: ASM-based class file traversal for bytecode analysis
- **Bytecode manipulation**: Uses BCEL 6.0 and ASM 5.0.2 for low-level analysis

## Source Structure

- Main source: `src/java/` (not `src/main/java/`)
- Tests: `src/junit/`
- Resources included alongside Java sources in same directories

## Key Dependencies

- BCEL 6.0 - Bytecode engineering
- ASM 5.0.2 - Bytecode manipulation
- dom4j 1.6.1 + Jaxen 1.1.6 - XML processing
- JUnit 4.11 - Testing