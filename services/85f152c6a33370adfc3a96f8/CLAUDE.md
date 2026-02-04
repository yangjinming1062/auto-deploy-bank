# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Shadowhook is an Android inline hook library supporting armeabi-v7a and arm64-v8a architectures for Android 4.1+ (API 16+). It provides function hooking and instruction interception capabilities for production apps with a focus on stability, compatibility, and performance.

## Build Commands

```bash
# Build all modules (debug + release)
./gradlew assemble

# Build release AAR for publishing
./gradlew assembleRelease

# Run code quality checks
./gradlew checkstyle

# Run system tests
./gradlew test

# Clean build artifacts
./gradlew clean

# Publish to local maven (for testing)
./gradlew publishToMavenLocal

# Build with Address Sanitizer (ASAN) for debugging
./gradlew assembleDebug -DuseASAN=true
```

## Architecture

```
shadowhook/src/main/cpp/
├── shadowhook.c          # Public API entry point, initialization
├── sh_*.c                # Core modules:
│   ├── sh_hub.c/h       # Hook task hub - manages hook operations
│   ├── sh_linker.c/h    # Android linker integration, ELF parsing
│   ├── sh_task.c/h      # Hook task scheduling and execution
│   ├── sh_switch.c/h    # Context switching for arm/arm64
│   ├── sh_elf.c/h       # ELF file parsing utilities
│   ├── sh_enter.c/h     # Hook entry point trampoline
│   ├── sh_recorder.c/h  # Hook/intercept operation recording
│   ├── sh_safe.c/h      # Signal-safe operations
│   ├── sh_island.c/h    # Island hooking for discontinuous memory
│   └── sh_jni.c         # JNI bindings
├── arch/
│   ├── arm/             # 32-bit ARM (thumb/arm mode) assembly & trampolines
│   └── arm64/           # 64-bit ARM assembly & trampolines
├── include/             # Public header (shadowhook.h)
├── common/              # Utility functions (logging, signal handling)
└── third_party/         # xDL (ELF dlopen handling), bsd queue/tree, lss
```

### Key Modules

- **sh_hub.c**: Central hub that orchestrates hook operations and tracks hook state
- **sh_linker.c**: Hooks Android linker functions to intercept library loading events
- **sh_switch.c**: Handles ARM/ARM64 context switching and signal-based trampoline execution
- **sh_task.c**: Manages deferred hook tasks queued during library loading
- **sh_elf.c**: Low-level ELF parsing for symbol resolution and address lookup

## Code Style

- **C/C++**: Follow `.clang-format` (Google-based, 110 column limit)
- **Java**: Follow `checkstyle.xml`
- Run `./gradlew checkstyle` to validate Java code

## Branch Strategy

- `main` branch: Latest release/tagged versions only
- `dev` branch: Active development branch
- Submit all PRs to `dev` branch

## Configuration

Key Gradle properties in `gradle.properties`:
- `android.useAndroidX=true` - AndroidX enabled
- `android.nonTransitiveRClass=true` - Non-final R class IDs
- `android.nonFinalResIds=false` - Final resource IDs (API 34+)

Build variants controlled by:
- `dependencyOnLocalLibrary`: Use local shadowhook vs. Maven dependency
- `useASAN`: Enable Address Sanitizer for native debugging