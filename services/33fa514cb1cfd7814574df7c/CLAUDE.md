# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PeopleInSpace is a Kotlin Multiplatform project demonstrating UI sharing across Android (Jetpack Compose), iOS (SwiftUI), Wear OS, Desktop, Web (Wasm), and JVM backend. It fetches data from The Space Devs API and Open Notify PeopleInSpace API to display information about people currently in space and the International Space Station position.

## Key Modules & Architecture

### `common/` - Shared Kotlin Multiplatform Module
Contains all business logic and shared UI components used across platforms:
- **Repository Pattern**: `PeopleInSpaceRepository` (common/src/commonMain/kotlin/dev/johnoreilly/common/repository/PeopleInSpaceRepository.kt) handles data fetching and caching
- **Database**: SQLDelight database (`PeopleInSpaceDatabase`) for local storage
- **DI**: Koin for dependency injection with expect/actual for platform-specific implementations
- **Remote**: Ktor-based API client for network requests
- **UI**: Shared Compose UI components used across all platforms
- **ViewModels**: Shared view models for state management

Platform-specific implementations:
- `androidMain/`: Android-specific (osmdroid for maps, Android drivers)
- `jvmMain/`: JVM/desktop specific implementations
- `iOSMain/`: iOS-specific (Darwin HTTP client, native drivers)
- `wasmJsMain/`: WebAssembly-specific (Web SQL driver)

### `backend/` - Ktor Server
JVM-based backend service exposing REST endpoints:
- `/astros.json`: Returns list of people in space
- `/iss-now.json`: Returns current ISS position
- `/astros_local.json`: Returns mock data for local testing
- Built with Ktor + Netty
- Can be deployed to Google App Engine

### Platform-Specific Modules

**`app/`** - Android application using Jetpack Compose

**`wearApp/`** - Wear OS application using Compose for Wear OS

**`PeopleInSpaceSwiftUI/`** - iOS application with SwiftUI

**`compose-desktop/`** - Desktop application using Compose for Desktop

**`compose-web/`** - Web application using Compose for Web (Wasm)

**`mcp-server/`** - Model Context Protocol server implementation

## Common Commands

### Building & Running

```bash
# Build all modules
./gradlew build

# Run specific platform apps
./gradlew :backend:run                      # Run Ktor backend
./gradlew :compose-desktop:run              # Run Desktop app
./gradlew :compose-web:wasmBrowserDevelopmentRun  # Run Web app (Wasm)

# Run Android app (requires Android Studio or device/emulator)
./gradlew :app:installDebug

# iOS app is located in PeopleInSpaceSwiftUI/ directory - open in Xcode

# Wear app (requires connected Wear OS device)
./gradlew :wearApp:installDebug
```

### Backend Deployment

```bash
# Build uber JAR for deployment
./gradlew :backend:shadowJar

# Deploy to Google App Engine
gcloud app deploy backend/build/libs/backend-all.jar --appyaml=backend/src/jvmMain/appengine/app.yaml
```

### Testing

```bash
# Run all tests
./gradlew test

# Run tests for specific module
./gradlew :common:test

# Run UI tests (Compose Multiplatform)
./gradlew :common:test --tests "*ComposeMultiplatformUiTests"

# Run mobile E2E tests with Maestro
maestro test maestro/PeopleInSpace.flow
```

### Code Quality & Dependency Management

```bash
# Check for dependency updates
./gradlew dependencyUpdates

# Clean build artifacts
./gradlew clean

# Build without tests
./gradlew assemble
```

### MCP Server Integration

```bash
# Build MCP server JAR
./gradlew :mcp-server:shadowJar

# The JAR will be at: mcp-server/build/libs/serverAll.jar
# See README.md for Claude Desktop integration instructions
```

## Key Dependencies (from gradle/libs.versions.toml)

- **Kotlin**: 2.2.21
- **Compose Multiplatform**: 1.9.3
- **Ktor**: 3.3.3 (HTTP client/server)
- **Koin**: 4.1.1 (DI)
- **SQLDelight**: 2.2.1 (Database)
- **Kotlinx Coroutines**: 1.10.2
- **Kotlinx Serialization**: 1.9.0
- **SKIE**: 0.10.8 (Swift interop enhancements)

## Development Notes

### API Endpoints
The app uses two main APIs:
- The Space Devs API for people in space data
- Open Notify API for ISS position (`http://api.open-notify.org`)

### Database Schema
SQLDelight database (`PeopleInSpaceDatabase`) at common/src/commonMain/sqldelight/dev/johnoreilly/peopleinspace/db/ stores:
- People in space data (name, craft, image URL, bio, nationality)
- Auto-generated queries via SQLDelight

### Dependency Injection Setup
Koin is configured with:
- Common module: Shared dependencies (HTTP client, JSON, repository)
- Platform modules: Expect/actual pattern for platform-specific implementations
  - Android: Android SqlDriver, Android HTTP engine
  - iOS: Native SqlDriver, Darwin HTTP engine
  - JVM: SQLite driver, Java HTTP engine

### Testing Strategy
- **Unit Tests**: In `common/src/commonTest/` using kotlin.test
- **UI Tests**: Compose Multiplatform tests using `runComposeUiTest`
- **E2E Tests**: Maestro flows for mobile testing

### Web (WASM) Specifics
The web client uses:
- SQL.js for browser-based SQL database
- Web workers for database operations
- npm dependencies configured in `common/build.gradle.kts`

### iOS Integration
- Uses Swift Package Manager integration via `multiplatform-swiftpackage` plugin
- Framework generated in `common/build/intermediate/`
- SKIE plugin enabled for enhanced Swift interoperability

### Maps Implementation
- Android: Uses osmdroid library
- Other platforms: Platform-specific map implementations

## Important File Locations

- **Version Catalog**: `gradle/libs.versions.toml`
- **Root Build Config**: `build.gradle.kts`, `settings.gradle.kts`, `gradle.properties`
- **Database Schema**: `common/src/commonMain/sqldelight/`
- **Shared Repository**: `common/src/commonMain/kotlin/dev/johnoreilly/common/repository/PeopleInSpaceRepository.kt`
- **Backend Server**: `backend/src/jvmMain/kotlin/Server.kt`
- **MCP Server**: `mcp-server/src/main/kotlin/`
- **iOS App**: `PeopleInSpaceSwiftUI/PeopleInSpaceSwiftUI/`
- **Maestro Tests**: `maestro/PeopleInSpace.flow`

## Platform-Specific Build Configurations

### Android
- Min SDK: 24
- Target SDK: 36
- Namespace: `dev.johnoreilly.peopleinspace`

### iOS
- Swift 5.9+ required
- iOS 14+ target
- Framework name: `common.framework`

### Desktop
- Uses Compose for Desktop
- Current OS detection for dependencies

### Web
- Wasm-based Kotlin/JS
- Browser development server
- Webpack for bundling

## Gradle Tasks

```bash
# Common tasks
./gradlew tasks                    # List all available tasks
./gradlew tasks --all             # List all tasks with details

# Module-specific tasks
./gradlew :common:tasks
./gradlew :app:tasks
./gradlew :backend:tasks
```