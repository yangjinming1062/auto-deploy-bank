# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the Glide Android image loading library repository - a fast and efficient media management and image loading framework for Android that wraps media decoding, memory and disk caching, and resource pooling.

## Project Structure

- **library/** - Core Glide library (Java)
  - Main entry point: `com.bumptech.glide.Glide` (singleton)
  - Key packages: `load/` (decoders, encoders, data loading), `engine/` (load engine), `request/` (request management), `manager/` (lifecycle management), `module/` (configuration)

- **integration/** - Optional integration modules
  - `okhttp3/` - OkHttp 3.x network stack
  - `volley/` - Volley network stack
  - `ktx/` - Kotlin extensions and utilities
  - `compose/` - Jetpack Compose integration
  - `recyclerview/` - RecyclerView integration
  - `concurrent/` - Coroutines support
  - Other integrations: avif, cronet, gifencoder, recyclerview, sqljournaldiskcache

- **annotation/** - Annotation processing
  - `compiler/` - Java annotation processor
  - `ksp/` - Kotlin Symbol Processing (KSP) processor

- **samples/** - Example applications
  - flickr, giphy, svg, gallery, contacturi, imgur - sample apps demonstrating usage

- **instrumentation/** - Android instrumentation tests
- **testutil/** - Testing utilities
- **third_party/** - Third-party dependencies (gif_decoder, disklrucache)

## Development Commands

### Building
```bash
# Build entire project
./gradlew build

# Build specific module
./gradlew :library:assemble
./gradlew :integration:okhttp3:assemble

# Build samples
./gradlew :samples:flickr:build
./gradlew :samples:giphy:build
```

### Testing
```bash
# Run all unit tests
./gradlew test

# Run tests for specific module
./gradlew :library:test
./gradlew :integration:ktx:test

# Run single test class
./gradlew :library:test --tests "com.bumptech.glide.GlideTest"

# Run instrumentation tests (requires device/emulator)
./gradlew connectedAndroidTest

# Run specific instrumentation test
./gradlew :instrumentation:assembleAndroidTest
```

### Code Quality
```bash
# Run all checks (checkstyle, lint, ktfmt, violations)
./gradlew check

# Check Kotlin formatting
./gradlew ktfmtCheck

# Format Kotlin code
./gradlew ktfmtFormat

# Run checkstyle
./gradlew checkstyle
```

### Running Samples
```bash
# Install and run specific sample app
./gradlew :samples:flickr:run
./gradlew :samples:giphy:run
./gradlew :samples:svg:run
./gradlew :samples:contacturi:run
./gradlew :samples:gallery:run
./gradlew :samples:imgur:run
```

### Other Useful Commands
```bash
# Clean build artifacts
./gradlew clean

# Generate documentation
./gradlew dokkaHtmlMultiModule

# Build JAR
./gradlew jar

# Assemble release artifacts
./gradlew assemble
```

## High-Level Architecture

Glide follows a layered architecture with these key components:

1. **Glide Singleton** (`library/src/main/java/com/bumptech/glide/Glide.java`)
   - Main entry point for the library
   - Manages Engine, BitmapPool, MemoryCache, RequestManagerRetriever
   - Provides static methods like `Glide.with(context)`

2. **Engine** (`library/src/main/java/com/bumptech/glide/load/engine/`)
   - Core loading engine that coordinates decoding, caching, and resource management
   - Manages active resources and cache

3. **RequestManager** (`library/src/main/java/com/bumptech/glide/RequestManager.java`)
   - Lifecycle-aware request management
   - Associates with Activities/Fragments/Views to manage load lifecycles

4. **LoadPath** (`library/src/main/java/com/bumptech/glide/load/engine/LoadPath.java`)
   - Defines the data flow pipeline from data source to decoded resource

5. **Registry System** (`library/src/main/java/com/bumptech/glide/provider/`)
   - `ResourceDecoderRegistry` - registry of decoders
   - `ResourceEncoderRegistry` - registry of encoders
   - `ModelLoaderRegistry` - registry of model loaders

6. **Module System** (`library/src/main/java/com/bumptech/glide/module/`)
   - `AppGlideModule` - Application-level configuration
   - `LibraryGlideModule` - Library-level configuration
   - Used for registering components and configuring Glide behavior

## Configuration

- **Android SDK Requirements**:
  - Minimum API: 14
  - Compile API: 26+
  - Version: 5.0.5 (see `gradle.properties`)

- **Environment**:
  - Set `ANDROID_HOME` or add `local.properties` with `sdk.dir=...`
  - Requires Android Support Repository installed

## Key Build Information

- **JVM Args**: Configured in `gradle.properties` (`org.gradle.jvmargs=-Xmx4096M`)
- **Code Style**: ktfmt for Kotlin, Checkstyle for Java (config: `checkstyle.xml`)
- **Testing**: Uses Robolectric for unit tests, JUnit for instrumentation
- **CI**: GitHub Actions workflow in `.github/workflows/build.yml`

## Important Notes

- ProGuard rules are bundled in `library/proguard-rules.txt` and applied automatically
- Code style is enforced via CI; all warnings treated as errors
- Integration libraries are optional dependencies that can be included as needed
- Annotation processing supports both Java annotation processor and KSP