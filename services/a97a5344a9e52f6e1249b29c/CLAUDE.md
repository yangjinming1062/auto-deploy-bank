# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains Docker build configuration for **PassAndroid**, an Android APK building container. The actual Android project source code is copied into the Docker container during build time (see `COPY . .` in Dockerfile).

## Build Commands

### Build APK with Docker
```bash
# Build and run the Android builder container
docker-compose up --build

# Or build directly with Docker
docker build -t passandroid-builder .
```

### Run Container for APK Output
```bash
# The built APK will be available at ./target/passandroid.apk
docker-compose up android-builder
```

## Architecture

### Build Container (Dockerfile)
- **Base Image**: Eclipse Temurin 17 JDK (eclipse-temurin:17-jdk-jammy)
- **Android SDK**: Version 35 (platform, build-tools, cmdline-tools)
- **Build System**: Gradle (wrapper at `./gradlew`)

### JitPack Dependencies Disabled
Some JitPack dependencies from `com.github.ligi` are unavailable and have been commented out in the build:
- TouchImageView, LoadToast, ExtraCompats, KAXT, KAXTUI, tracedroid
- snackengage-playrate, snackengage-amazonrate

### Container Resource Limits
- CPUs: 1.0 reserved, 2.0 limit
- Memory: 1G reserved, 4G limit
- GRADLE_OPTS: `-Xmx4g` (4GB heap)

## Key Build Steps (in Dockerfile order)

1. Install system dependencies (unzip, curl, bash, git)
2. Download and install Android SDK command-line tools
3. Accept SDK licenses and install platform-tools, platforms, build-tools
4. Copy project source into `/app`
5. Disable unavailable JitPack dependencies in `android/build.gradle`
6. Comment out unavailable library usages in Kotlin source files
7. Run Gradle assembleDebug with flags: `-x lint --no-daemon --max-workers=2`
8. Copy built APK to `/app/output/passandroid.apk` and `/app/target.jar`

## Notes

- The `android/` directory in the source contains the actual Gradle project
- Gradle wrapper (`./gradlew`) is expected at repository root
- Build output is placed in `/app/output/` inside the container, mounted to `./target` on host
- JitPack dependencies may need to be re-enabled or replaced if the original project is recovered