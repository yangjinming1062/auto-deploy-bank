# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Master Password is a password generation algorithm and multi-platform application suite. It implements a deterministic password generation algorithm that creates unique passwords based on a master password, user name, and site information. The project has moved to [Spectre](https://gitlab.com/spectre.app) but this codebase remains as reference.

## Repository Structure

The project is organized into platform-specific modules:

- **platform-independent/**: Core algorithm and platform-agnostic code
  - **c/core/**: C implementation of the Master Password algorithm (contains algorithm versions v0-v3)
  - **java/algorithm/**: Java wrapper for the C algorithm with JNI bindings
  - **java/model/**: Data models for user, site, and password generation
  - **java/tests/**: Test suite using TestNG
  - **java/gui/**: Desktop Java GUI application (Swing-based)
  - **scripts/**: Utility scripts including word lists and password generators

- **platform-android/**: Android application (requires Android SDK)

- **platform-darwin/**: Apple platforms
  - iOS and macOS applications
  - Xcode workspace: `platform-darwin/MasterPassword.xcworkspace`

- **lib/**: External dependencies
  - libsodium for cryptographic functions
  - libjson-c for JSON support

## Build System

### Gradle (Java/Android)

The project uses Gradle 5.6.2. The wrapper is at `./gradlew`.

**Common Commands:**

```bash
# Build all components
./gradlew build

# Clean build artifacts
./gradlew clean

# Run Java tests only
./gradlew test

# Build specific module
./gradlew :masterpassword-algorithm:build
./gradlew :masterpassword-gui:build

# Build GUI with shadow JAR (for distribution)
./gradlew masterpassword-gui:shadowJar

# Build Android (requires local.properties with sdk.dir)
./gradlew masterpassword-android:assembleRelease
```

**Note**: The project requires JDK 8 (not JDK 9+) for Android builds. Set `JAVA_HOME` accordingly.

### C CLI Build

The C CLI uses a custom bash-based build system in `platform-independent/c/cli/`:

```bash
cd platform-independent/c/cli

# Build default target (mpw)
./build

# Build all targets
targets='all' ./build

# Build with debug flags
./build -d

# Build specific targets
targets='mpw-tests' ./build
targets='mpw-bench' ./build

# Clean build artifacts
./clean

# Run C tests
./mpw-tests
```

**Build Features:**
- `mpw_sodium=1` (default): Use libsodium for crypto (required)
- `mpw_json=1` (default): Enable JSON support via libjson-c (optional)
- `mpw_color=1` (default): Enable colorized identicon via libncurses (optional)
- `mpw_xml=1` (default): Enable XML parsing via libxml2 (required for tests)

Example: `mpw_json=0 ./build` to disable JSON support.

### Dependencies

**Required for C build:**
- GCC or Clang compiler
- libsodium
- libxml2

**Optional:**
- libjson-c (for JSON config support)
- libncurses or libtinfo (for colored output)

Build scripts will attempt to auto-detect and link these libraries.

## Testing

### Java Tests

```bash
# Run all tests
./gradlew test

# Run specific test class or method
./gradlew test --tests com.lyndir.masterpassword.MPAlgorithmTest

# Run with TestNG
./gradlew :masterpassword-tests:test
```

Test configuration is in `platform-independent/java/tests/build.gradle` (uses TestNG).

### C Tests

```bash
cd platform-independent/c/cli

# Build and run test suite
./build targets='mpw-tests'
./mpw-tests

# Test cases are defined in mpw_tests.xml (test vectors for algorithm v0-v3)
```

### CI/CD

GitLab CI pipeline (`.gitlab-ci.yml`) builds:
1. C CLI and runs tests
2. Java tests via Gradle
3. iOS/macOS apps via Xcodebuild

## Code Architecture

### Algorithm Implementation

The Master Password algorithm has evolved through 4 versions (v0-v3):

- **C Core** (`platform-independent/c/core/src/`): The canonical implementation
  - `mpw-algorithm.c/h`: Main algorithm entry points
  - `mpw-algorithm_v{0,1,2,3}.{c,h}`: Version-specific implementations
  - `base64.{c,h}` and `aes.{c,h}`: Utility functions
  - `mpw-marshal.{c,h}`: Data marshalling/unmarshalling

- **Java Algorithm** (`platform-independent/java/algorithm/`): JNI wrapper around C core
  - Provides Java API to the C algorithm
  - Handles native library loading

### Platform Architecture

1. **Core (C)**: Platform-independent algorithm implementation
2. **Bindings (Java)**: JNI bridge for Java-based platforms
3. **Applications**:
   - **CLI (C)**: Command-line interface
   - **GUI (Java)**: Desktop application (Swing)
   - **Android (Java)**: Mobile application
   - **iOS/macOS (Swift/Obj-C)**: Native Apple apps

### Data Flow

```
User Input (name, master password, site)
    ↓
Algorithm Version Selection (v0-v3)
    ↓
C Algorithm Core
    ↓
Site-specific Password Generation
    ↓
Output (formatted per type: Long, Medium, Short, PIN, Name, Phrase)
```

### Key Components

- **MPSite** (`platform-independent/java/model/`): Site-specific password parameters
- **MPUser**: User identity and master password handling
- **MPAlgorithm**: Java API for password generation
- **Test Vectors**: `platform-independent/c/cli/mpw_tests.xml` contains canonical test cases

## Important Notes

- **Project Status**: This project is no longer maintained; development has moved to Spectre
- **Android Builds**: Must use JDK 7 or 8 (not 9+)
- **Native Libraries**: The C core is built as a native library for JNI access
- **Test Coverage**: Algorithm has extensive test vectors covering all versions and edge cases
- **Versioning**: Algorithm versions are incremented for breaking changes (v0 → v1, etc.)

## Release Process

See `RELEASE.md` for release build commands:

```bash
# Desktop GUI
gradle --no-daemon clean masterpassword-gui:shadowJar

# Android (requires keystore passwords via mpw)
gradle --no-daemon clean masterpassword-android:assembleRelease
```

Release keystores are managed separately by the project maintainer.