# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Butter Knife is a field and method binding library for Android views that uses annotation processing to generate boilerplate code. **This project is now deprecated** - users should switch to [Android View Binding](https://developer.android.com/topic/libraries/view-binding). Only critical AGP integration bug fixes are being considered.

The library provides:
- `@BindView` - Eliminates `findViewById` calls
- `@OnClick` and other listener annotations - Eliminates anonymous inner-classes
- Resource annotations (`@BindString`, `@BindColor`, etc.) - Eliminates resource lookups
- Grouped view operations with `@BindViews`

## Repository Structure

This is a multi-module Gradle project with the following modules:

- **butterknife** - Main Android library module that users depend on
- **butterknife-annotations** - Contains all annotation definitions
- **butterknife-compiler** - Annotation processor that generates binding code using JavaPoet
- **butterknife-runtime** - Runtime classes for view binding and unbinding
- **butterknife-gradle-plugin** - Gradle plugin for R2 generation in library modules
- **butterknife-lint** - Lint rules for Butterknife
- **butterknife-reflect** - Reflection-based implementation (alternative to annotation processing)
- **butterknife-integration-test** - Integration tests
- **sample** - Example applications demonstrating usage (app/ and library/ modules)

### Key Architecture Components

**Annotation Processing Flow:**
1. `ButterKnifeProcessor` (butterknife-compiler/src/main/java/butterknife/compiler/ButterKnifeProcessor.java:1) scans annotated code
2. Generates binding classes (e.g., `ExampleActivity_ViewBinding.java`) using JavaPoet
3. Generated code lives under `butterknife/internal/` in runtime module

**Core Runtime Classes:**
- `ButterKnife.java` (butterknife/src/main/java/butterknife/ButterKnife.java:1) - Main entry point with `bind()` methods
- `ViewCollections.java` (butterknife-runtime/src/main/java/butterknife/ViewCollections.java:1) - Handles grouped view operations
- `Action.java` & `Setter.java` (butterknife-runtime/src/main/java/butterknife/Action.java:1) - Interfaces for batch operations

## Common Development Commands

### Building and Testing

```bash
# Clean and build all modules
./gradlew clean assemble

# Build including Android tests
./gradlew clean assemble assembleAndroidTest

# Run code quality checks (checkstyle + unit tests)
./gradlew check

# Run full CI checks (including connected Android tests)
./gradlew check connectedCheck

# Run only checkstyle
./gradlew checkstyle

# Run unit tests for a specific module
./gradlew :butterknife-compiler:test

# Run Android tests for a specific module
./gradlew :butterknife:connectedAndroidTest
```

### Working with Modules

```bash
# Build only the compiler module
./gradlew :butterknife-compiler:assemble

# Test only the compiler module
./gradlew :butterknife-compiler:test

# Build runtime module
./gradlew :butterknife-runtime:assemble
```

### Code Quality

The project uses:
- **Checkstyle** - Configuration in `checkstyle.xml`. Run with `./gradlew checkstyle`
- **Error Prone** - Static analysis tool configured in `build.gradle:82-86`
- **Java 8** - Required for all modules (see `build.gradle:14-17`)

### Releasing (Maintainers Only)

See `RELEASING.md` for the complete process. Summary:

1. Update version in `gradle.properties` (remove SNAPSHOT)
2. Update `CHANGELOG.md`
3. Update `README.md` with new version
4. Commit changes: `git commit -am "Prepare for release X.Y.Z."`
5. Upload artifacts: `./gradlew clean uploadArchives`
6. Promote in [Sonatype Nexus](https://oss.sonatype.org/)
7. Create git tag: `git tag -a X.Y.Z -m "Version X.Y.Z"`
8. Update to next SNAPSHOT version
9. Push: `git push && git push --tags`

## Build Configuration

**Key build properties** (gradle.properties):
- `GROUP=com.jakewharton`
- `VERSION_NAME=10.2.4-SNAPSHOT`
- Java 8 required (`compileOptions.sourceCompatibility = JavaVersion.VERSION_1_8`)
- Min SDK: 14, Compile SDK: 28
- Aapt2 disabled (see line 21 in gradle.properties)

**Android Requirements:**
- Android Gradle Plugin 3.3+ (minimum for incremental annotation processing support)
- Compile SDK 28
- Java 8 language features

## Testing

**Unit Tests:** Located in `src/test/` for each module. Run with `./gradlew :module:test`

**Android Tests:** Located in `src/androidTest/` for Android modules. Run with `./gradlew :module:connectedAndroidTest`

**Integration Tests:** In `butterknife-integration-test/` module with its own test app

**CI Configuration:** `.travis.yml` runs:
- `./gradlew clean assemble assembleAndroidTest` (install)
- `./gradlew check connectedCheck` (script)

Note: Travis CI sets up an Android emulator for running instrumentation tests.

## Important Notes

1. **Deprecated:** The library is in maintenance mode. View Binding is the recommended replacement.

2. **Library Modules:** When using in library projects, apply the Butterknife gradle plugin and use `R2` references instead of `R` (see README.md:95-103).

3. **Annotation Processing:** The compiler module uses incremental annotation processing (added in version 10.2.0) which improves build performance.

4. **Reflection Backend:** `butterknife-reflect` module provides a reflection-based alternative without code generation, useful for certain scenarios.

5. **Generated Code:** The annotation processor generates binding classes in the same package as the target class, named `{TargetClass}_ViewBinding`.

6. **Unbinding:** Generated code creates `Unbinder` instances to manage view unbinding (important for activities/fragments lifecycle).

7. **Checkstyle Suppression:** Checkstyle is disabled for `butterknife-gradle-plugin` (see build.gradle:103-121).