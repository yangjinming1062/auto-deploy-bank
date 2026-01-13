# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **AndroidX (Android Jetpack)** repository - a collection of Android libraries that provide backward-compatible APIs and modern Android development practices. The project is split into many modules (activity, appcompat, core, lifecycle, navigation, etc.) and uses a Gradle-based build system with custom plugins.

The repository has a dual development workflow:
- **Primary**: AOSP Gerrit at `android.googlesource.com/platform/frameworks/support`
- **GitHub mirror**: External contributions accepted for a subset of libraries via pull requests

Libraries accepting GitHub contributions:
- activity, appcompat, biometric, collection, compose/runtime, core, datastore, fragment, lifecycle, lint, navigation, paging, room, work

## Common Commands

### Build and Test

```bash
# Build and run all tests (device + host)
./gradlew test connectedCheck

# Build without running tests
./gradlew assemble

# Run only unit tests
./gradlew test

# Run only connected tests (requires device/emulator)
./gradlew connectedCheck

# Run specific module tests
./gradlew :core:core:test

# Run specific test class
./gradlew :core:core:test --tests "androidx.core.view.TestClassName"

# Build specific module
./gradlew :core:core:assemble

# Run additional checks (lint, API validation, etc.)
./gradlew buildOnServer

# Skip benchmark tests when testing on emulator
./gradlew test connectedCheck \
  -x :room:room-benchmark:cC \
  -x :room:integration-tests:room-incremental-annotation-processing:test
```

### Code Style and Formatting

```bash
# Check Kotlin formatting (ktfmt)
./gradlew :core:core:ktCheck

# Automatically fix Kotlin formatting
./gradlew :core:core:ktFormat

# Run format check across entire project
./gradlew ktCheck
```

### API Management

```bash
# Update API files after API changes
./gradlew updateApi

# Update API for specific module
./gradlew :appcompat:appcompat-resources:updateApi

# Check API compatibility
./gradlew :core:core:checkApi
```

### Android Studio

```bash
# Launch Studio with specific project subset
PROJECT_PREFIX=:core:,:work: ./gradlew :studio

# Launch Studio for specific library (from playground-projects)
cd playground-projects/room-playground
./gradlew studio

# Launch Studio for all projects
./studiow all

# Clean and reinstall Studio
./studiow --clean main
```

### Utility Scripts

```bash
# Clean build with confirmation
./cleanBuild.sh assembleRelease

# Clean build without prompt
./cleanBuild.sh -y test connectedCheck

# Run full build as used by build servers
./busytown/androidx.sh
```

### Repository Sync (AOSP workflow)

```bash
# Sync changes (AOSP workflow)
repo sync -c -j32

# Create new branch
repo start branch_name .

# Upload for review
repo upload --cbr -t .

# Force sync if manifest changed
repo sync -j32 --force-sync
```

## Architecture

### Build System

- **Gradle** with configuration cache enabled (see `gradle.properties`)
- **Custom plugins** in `buildSrc/` directory - contains AndroidX-specific Gradle plugins, dependency management, and build logic
- **Module structure**: Each library is a separate Gradle subproject (e.g., `:core:core`, `:lifecycle:lifecycle-viewmodel`)
- **Binary dependencies**: Stored in `prebuilts/androidx/internal` and `prebuilts/androidx/external` for hermetic builds

### Typical Module Structure

```
library-name/
  ├── build.gradle                      # Module build configuration
  └── src/
      ├── main/
      │   ├── java/androidx/library/    # Kotlin/Java source
      │   └── AndroidManifest.xml
      ├── androidTest/                  # Instrumentation tests
      ├── test/                         # Unit tests
      └── api/                          # API tracking files
          ├── current.txt               # Current public API
          ├── 1.0.0.txt                 # Versioned API (stable releases)
          └── restricted_*.txt          # Restricted APIs
```

### High-Level Directory Structure

```
androidx/
├── activity/            # Activity APIs
├── annotation/          # Annotation processing
├── appcompat/           # AppCompat compatibility
├── biometric/           # Biometric authentication
├── camera/              # CameraX APIs
├── collection/          # Collection utilities
├── compose/             # Jetpack Compose (UI toolkit)
├── core/                # Core Android APIs
├── fragment/            # Fragment APIs
├── lifecycle/           # Lifecycle-aware components
├── navigation/          # Navigation component
├── paging/              # Paging library
├── room/                # Room database
├── work/                # WorkManager
├── buildSrc/            # Custom Gradle plugins
├── development/         # Developer tools & scripts
├── docs/                # Project documentation
├── prebuilts/           # Hermetic build dependencies
├── samples/             # Sample applications
├── playground-projects/ # GitHub workflow projects
└── .github/workflows/   # GitHub Actions CI/CD
```

### Key Libraries Overview

- **Compose**: Modern declarative UI toolkit
- **Core**: Backward-compatible Android APIs (most widely used)
- **Activity/Fragment**: Android component APIs
- **Lifecycle**: Lifecycle-aware components (ViewModel, LiveData, etc.)
- **Navigation**: Type-safe navigation between screens
- **Room**: SQLite database abstraction
- **WorkManager**: Background processing and scheduling
- **CameraX**: Camera APIs with modern lifecycle awareness
- **DataStore**: Modern data storage (replaces SharedPreferences)

### Build System Architecture

**Gradle Configuration Cache** (Performance):
- Enabled in `gradle.properties` with strict failure on errors
- Speeds up builds by caching configuration phase
- Requires JDK 21 for full compatibility

**Custom Gradle Plugins** (`buildSrc/`):
- AndroidX-specific build logic
- Dependency management and version catalogs
- API tracking and validation
- Testing infrastructure setup

**Hermetic Builds** (`prebuilts/`):
- Binary dependencies stored in `prebuilts/androidx/internal` and `prebuilts/androidx/external`
- Ensures reproducible builds regardless of environment
- Contains compiled AARs, JARs, and native libraries

**Version Catalog** (`libraryversions.toml`):
- Centralized version management for all dependencies
- Each library has a version defined here
- Used across all Gradle modules for consistency

### CI/CD

**GitHub Actions** (`.github/workflows/`):
- `presubmit.yml` - Runs on PRs and pushes to check builds
- `integration_tests.yml` - Full integration test suite
- Test on API levels 19, 23, 26, 28, 30, 33, 34, 35, and 36

**AOSP CI** (Continuous Integration):
- All changes tested internally at Google
- Mirrored from Gerrit to AOSP for testing
- Required for merges to main branches

### Key Development Tools

Located in `development/`:
- `importMaven/` - Import new Maven dependencies with proper versioning
- `diagnose-build-failure/` - Classify and debug build failures
- `ktfmt.sh` - Kotlin code formatting
- `referenceDocs/` - Generate API documentation
- `studio/` - Android Studio launcher scripts
- `emulator/` - Preconfigured emulator setups

### Code Review

Review guidelines in `code-review.md`:
- **+2**: Submit-worthy (minor nits OK)
- **+1**: Needs other reviewers
- **-1**: Missing essential parts (tests, explanation, too large)
- **-2**: Causes project risk (use sparingly)

**PR Requirements** (GitHub workflow):
- Short and long description
- Test stanza describing testing steps
- Fixes stanza with bug ID
- Follow format in `CONTRIBUTING.md:180-189`

## Environment Setup

### Prerequisites

- JDK 21
- Android SDK
- Android NDK 23.1.7779620
- CMake 3.22.1

### Environment Variables

```bash
export JAVA_HOME="path/to/jdk21"
export ANDROID_SDK_ROOT="path/to/android/sdk"
```

### Git Configuration

```bash
# Required for rename detection across androidx package rename
git config --global merge.renameLimit 999999
git config --global diff.renameLimit 999999
```

## Important Notes

### API Changes

- When modifying public APIs, **must** run `./gradlew updateApi` before submitting
- API files are tracked in `api/` directory (current.txt + versioned files)
- Breaking changes require major version bump (or only allowed in alpha versions)
- May need to update `buildSrc/src/main/kotlin/androidx/build/LibraryVersions.kt` for frozen APIs (beta/rc/stable)

### Testing

- **100% public API coverage** expected for tests
- Bug fixes must include regression tests
- Test APKs preserved after runs: `android.injected.androidTest.leaveApksInstalledAfterRun=true`
- Use `@Suppress` for valid lint violations (see `CONTRIBUTING.md:164`)

### Code Style

- **ktfmt** for Kotlin formatting (runs automatically on `repo upload`)
- Use `./gradlew :module:ktCheck` to verify style locally
- Use `./gradlew :module:ktFormat` to auto-fix style issues

### Contribution Workflow

**GitHub PR Workflow** (for accepted libraries):
1. Fork repository, create PR to `androidx-main`
2. Sign CLA at https://cla.developers.google.com/
3. PR reviewed on GitHub, approved by Googler
4. Mirrored to AOSP Gerrit for testing
5. Merged in AOSP and mirrored back to GitHub

**AOSP Gerrit Workflow** (all libraries):
1. Use `repo start` to create branch
2. Make changes, commit with `git`
3. Upload with `repo upload --cbr -t .`
4. Reviewed on Gerrit, merged by project owners

### Build Configuration

Key settings in `gradle.properties`:
- Compile SDK: 34 (latest stable: 36, target: 36)
- JDK 21 required: `android.java.installations.fromEnv=ANDROIDX_JDK21`
- Configuration cache: enabled with strict failure on errors
- Dependency verification: disabled for faster builds
- KSP with K2 compiler: `kapt.use.k2=true`

### Troubleshooting

**Build Issues:**
```bash
# Clean build
./gradlew --clean [tasks]

# Kill Gradle daemons if debugger issues
./gradlew --stop

# Check for deleted files
repo status
```

**Studio Issues:**
- Sync project: File > Sync Project with Gradle Files
- Reinstall: `./studiow --clean main <project>`
- Set SDK manually if prompted incorrectly: `<project-root>/prebuilts/fullsdk-<platform>`

**Test Failures:**
- See `development/diagnose-build-failure/README.md` for failure classification
- Disable benchmark tests on emulator (see command above)
- View verbose logs in GitHub Actions for CI failures

### Working Directory

Most development happens in subdirectories:
- `frameworks/support/` (AOSP checkout)
- `playground-projects/` (GitHub workflow for specific libraries)

**Note**: The root directory contains all library modules - you can work directly in any library folder (e.g., `core/core/`, `lifecycle/lifecycle-viewmodel/`).

### Documentation References

For additional information, refer to these files:

- **`README.md`** - Project overview, getting started, and contribution guidelines
- **`CONTRIBUTING.md`** - Detailed contribution guide with PR templates and requirements
- **`docs/onboarding.md`** - New contributor onboarding and environment setup
- **`docs/testing.md`** - Comprehensive testing guidelines
- **`code-review.md`** - Code review etiquette and best practices
- **`development/diagnose-build-failure/README.md`** - Build failure troubleshooting

See the main `docs/` directory for more documentation on specific topics.

### Working in This Repository

**Common Development Patterns**:

1. **Find the right module**: Use `./gradlew projects` to list all available modules
2. **Understand API scope**: Check `module/api/current.txt` for public APIs before making changes
3. **Run targeted tests**: Always run tests for the specific module you're modifying
4. **Update APIs when needed**: If you change public APIs, always run `./gradlew updateApi`
5. **Use playground projects**: For experimental work or isolated development, use `playground-projects/`

**Key Tips**:
- Most development happens directly in library directories (e.g., `activity/activity/`)
- All libraries use the same Gradle structure and build conventions
- Changes to common APIs (core, lifecycle) require extra review
- Always test on multiple API levels (GitHub Actions test 9 different API levels)
- Breaking changes are only allowed in alpha versions