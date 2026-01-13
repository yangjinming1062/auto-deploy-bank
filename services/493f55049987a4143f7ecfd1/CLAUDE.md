# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Lemuroid is an open-source Android emulation platform based on Libretro, providing support for 20+ game systems including NES, SNES, Genesis, N64, PlayStation, and many more. The app targets both mobile and Android TV devices with a focus on ease of use and Android integration.

## Project Structure

Lemuroid uses a multi-module Gradle architecture:

- **lemuroid-app** - Main application module with UI and game logic
- **lemuroid-app-ext-free** / **lemuroid-app-ext-play** - Product flavor extensions for different app variants
- **lemuroid-cores** - Dynamic feature modules containing emulator cores (20+ cores as separate dynamic features)
- **retrograde-app-shared** - Shared UI components for TV and mobile
- **retrograde-util** - Utility library
- **lemuroid-touchinput** - Touch input handling
- **lemuroid-metadata-libretro-db** - Libretro database for game metadata
- **baselineprofile** - Baseline performance profiles
- **lemmiroid_app** - Legacy/alternative app variant

## Common Development Commands

### Building the App

```bash
# Build debug APK
./gradlew assembleDebug

# Build release APK
./gradlew assembleRelease

# Build specific flavor combination (e.g., free + bundle)
./gradlew assembleFreeBundleDebug

# Build Google Play variant with dynamic features
./gradlew assemblePlayDynamicDebug

# Install and run on connected device
./gradlew installDebug

# Build APKs for all variants
./gradlew build
```

### Running the App

```bash
# Launch on connected device
./gradlew lemuroid-app:installDebug
adb shell am start -n com.swordfish.lemuroid/.app.mobile.main.LemuroidMobileMainActivity

# For TV variant
adb shell am start -n com.swordfish.lemuroid/.app.tv.main.LemuroidTvMainActivity
```

### Linting and Formatting

```bash
# Run ktlint check
./gradlew ktlintCheck

# Format code with ktlint
./gradlew ktlintFormat
```

### Gradle Tasks

```bash
# Clean build artifacts
./gradlew clean

# List all tasks
./gradlew tasks

# Run with profile for performance analysis
./gradlew assembleDebug --profile

# Build with configuration cache (already enabled in gradle.properties)
./gradlew assembleDebug
```

### Dynamic Features (Google Play Variant)

Google Play variant uses dynamic feature delivery for emulator cores. To build with dynamic features:

```bash
# Include dynamic core modules in build
./gradlew :lemuroid-app:assemblePlayDynamicDebug -Pdynamic

# Build individual core dynamic feature
./gradlew :lemuroid_core_ppsspp:assembleDebug
```

## Build Configuration

### Product Flavors

The app uses two flavor dimensions:

1. **opensourcedimension**: `free` (F-Droid) vs `play` (Google Play - includes closed-source components)
2. **coresdimension**: `bundle` (all cores bundled) vs `dynamic` (cores downloaded on-demand)

Valid flavor combinations:
- `freeBundle` - F-Droid variant with all cores bundled
- `playDynamic` - Google Play variant with dynamic core download
- `freeDynamic` - Open-source cores as dynamic features
- `playBundle` - All cores bundled in Play Store (large APK)

### SDK Configuration

- **Compile SDK**: 35
- **Target SDK**: 35
- **Min SDK**: 23 (Android 6.0)
- **Java Version**: 17

### Key Dependencies

- **Kotlin**: 2.0.21 with Compose plugin
- **Compose BOM**: 2024.02.02 (Material3)
- **Dagger**: 2.19 (Dependency Injection)
- **Room**: 2.6.1 (Database)
- **Navigation**: 2.5.2 (Compose & Fragment)
- **LibretroDroid**: 0.13.1 (Emulation engine)

## Code Architecture

### UI Architecture

- **Jetpack Compose** with Material3 design system for modern UI
- **Android TV support** via Leanback library with separate TV/mobile feature modules
- **Navigation Component** with Compose integration for navigation
- **MVVM** pattern with ViewModels and StateFlow
- **Hilt/Dagger** for dependency injection

### Feature Organization

Code is organized by feature in `lemuroid-app/src/main/java/com/swordfish/lemuroid/app/`:

- **mobile/** - Mobile-specific features (games, settings, search, etc.)
- **tv/** - Android TV-specific features
- **shared/** - Shared components (game library, input, savesync, storage, etc.)
- **mobile/shared/compose/** - Shared Compose UI components

Key features:
- **game** - Game playback and emulation
- **games** - Game library and browsing
- **settings** - App configuration (general, input, cores, bios, save sync)
- **systems** - System selection and core management
- **input** - Touch controls and gamepad support
- **gamemenu** - In-game menu (save states, options, etc.)

### Database

- **Room** for local game metadata, save states, and settings
- Games are scanned and indexed from device storage
- Metadata stored in `lemuroid-metadata-libretro-db` module

### Emulation

- Libretro cores loaded via **LibretroDroid** library
- Cores packaged as dynamic features (Google Play) or bundled (F-Droid)
- Save states managed automatically
- Touch controls customizable via `lemuroid-touchinput` module

## Key Files

- `build.gradle.kts` - Root build configuration with linting and dependencies
- `settings.gradle.kts` - Module inclusion and dynamic feature configuration
- `buildSrc/src/main/java/deps.kt` - All dependency versions centralized
- `gradle.properties` - Gradle JVM args and Android configuration
- `debug.keystore` - Debug signing key (already configured)

## Development Notes

- Code uses **ktlint** for formatting (configured in root build.gradle.kts)
- No traditional unit tests present in the codebase
- Configuration cache enabled in gradle.properties for faster builds
- Uses Kotlin serialization for JSON handling
- MultiDex enabled for large app size
- R8/ProGuard enabled for release builds

## Important Build Configurations

- Sign configs reference `release.jks` for release builds (not in repo)
- Debug builds use `debug.keystore` in root directory
- Lint is configured to allow some violations (see build.gradle.kts:108-110)
- Compose compiler metrics enabled via kotlinExtension version
- Some lint warnings disabled: MissingTranslation, ExtraTranslation, EnsureInitializerMetadata

## Repository Information

- **Main README**: `README.md` - Contains app description, supported systems, and features
- **Crowdin**: Translation managed via https://crowdin.com/project/lemuroid
- **Downloads**: F-Droid and Google Play Store distribution

## Recent Version Information

- Current version: 1.17.0 (versionCode 231)
- Version tag note: "Always remember to update Cores Tag!" (versionName in lemuroid-app/build.gradle.kts:14)