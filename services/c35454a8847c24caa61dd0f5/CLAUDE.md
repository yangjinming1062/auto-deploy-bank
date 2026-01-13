# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**MuJing (幕境)** is an English learning desktop application built with Kotlin and Jetpack Compose for Desktop. It enables context-based vocabulary learning using movies, TV shows, and documents. Users can extract vocabulary from video content (MKV), subtitles, or documents (PDF/TXT) and learn words with authentic video clips. The app features a video player with danmaku (bullet comments), spaced repetition algorithm (FSRS), and Anki deck support.

## Common Commands

### Development

```bash
# Build the application
./gradlew build

# Run the application in development mode
./gradlew run

# Run distributable (produces executable in build/compose/binaries/main/app/)
./gradlew runDistributable

# Run a single test
./gradlew test --tests "com.mujingx.fsrs.FSRSTest"
./gradlew test --tests "com.mujingx.data.DictionaryTest"

# Run all tests
./gradlew test

# Run tests that must execute last (excluded from regular test run)
./gradlew testLast

# Build native packages (platform-specific)
./gradlew packageDmg          # macOS
./gradlew packageDeb          # Linux Debian package
./gradlew packageMsi          # Windows MSI installer

# Clean build artifacts
./gradlew clean

# Build Rust JNI library for zstd compression
./gradlew buildRustZstdJni

# Decompress dictionary database (ecdict.7z -> ecdict.db)
./gradlew decompressDictionary
```

### Project Configuration

- **Kotlin Version**: 2.2.21
- **Compose Version**: 1.9.3 (fixed due to FileKit dependency)
- **Main Class**: `com.mujingx.MainKt` (`src/main/kotlin/com/mujingx/Main.kt:35`)
- **Gradle JVM Args**: `-Xmx4096m -Dfile.encoding=UTF-8` (configured in gradle.properties)

## High-Level Architecture

### Architecture Pattern
**MVVM (Model-View-ViewModel)** with reactive state management using Jetpack Compose

### Key Components

#### 1. UI Layer (`src/main/kotlin/com/mujingx/ui/`)
- **App.kt**: Main application component (892 lines) - manages window, navigation, and global state
- **WordScreen**: Vocabulary learning interface with spelling exercises, pronunciation playback
- **Player**: VLC-based video player with danmaku overlay system for learning words
- **SubtitleScreen**: Subtitle browser for reading and transcription exercises
- **TextScreen**: Document/PDF reader with vocabulary highlighting
- **Search**: Vocabulary search and filtering
- **FlatLaf Integration**: Modern UI theming (FlatLightLaf/FlatDarkLaf)

#### 2. Data Layer (`src/main/kotlin/com/mujingx/data/`)
- SQLite database for vocabulary storage
- ECDICT dictionary integration (compressed in dict/ecdict.7z)
- Repository pattern for data access
- Vocabulary categorization (familiar, hard, new words)

#### 3. Player Layer (`src/main/kotlin/com/mujingx/player/`)
- **VLCJ 4.11.0** backend for video playback
- Danmaku (bullet comments) rendering overlay
- Subtitle synchronization and navigation
- Video clip extraction for vocabulary context

#### 4. FSRS Algorithm (`src/main/kotlin/com/mujingx/fsrs/`)
- **Free Spaced Repetition Scheduler** implementation
- Optimizes review scheduling for vocabulary retention
- **APKG Support**: Import/export Anki decks (`src/main/kotlin/com/mujingx/fsrs/apkg/`)
- **Zstd Compression**: Rust JNI library for efficient data storage (`rust-zstd-jni/`)

#### 5. Video Processing (`src/main/kotlin/com/mujingx/ffmpeg/`)
- **FFmpeg** integration for video/audio processing
- Subtitle extraction from MKV videos using EBML reader
- Video clip generation for vocabulary contexts

#### 6. State Management (`src/main/kotlin/com/mujingx/state/`)
- `AppState`: Global application state holder
- `ScreenType`: Navigation state (WordScreen, Player, SubtitleScreen, TextScreen)
- ViewModels for each screen
- Compose state hoisting patterns

#### 7. Event System (`src/main/kotlin/com/mujingx/event/`)
- **EventBus**: Decoupled event communication
- Window keyboard event handling

#### 8. External Libraries (JAR files in `lib/`)
- **ebml-reader-0.1.1.jar**: EBML (MKV) parsing for subtitle extraction
- **jacob-1.20.jar**: Java-COM Bridge for Windows integration
- **subtitleConvert-1.0.3.jar**: Subtitle format conversion (SRT, ASS, etc.)

### Native Components

#### Rust JNI Library (`rust-zstd-jni/`)
- Provides zstd compression for vocabulary data
- Built via Cargo with Gradle integration
- Used in FSRS algorithm for efficient storage

#### Platform Resources (`resources/`)
- FFmpeg binaries for each platform (linux/, macos-arm64/, macos-x64/, windows/)
- VLC plugins and libraries
- Whisper models (downloaded during testing)

### Database Schema

Main tables (SQLite):
- Vocabulary table (words, definitions, examples)
- Learning progress (FSRS scheduling data)
- Media associations (video files, timestamps, subtitles)

### Entry Point

**Main.kt:35**: `fun main() = application { init(); App() }`
- Initializes FileKit for file dialogs
- Sets up FlatLaf theme based on system dark mode
- Launches main App composable

## Testing

### Framework
- **JUnit Jupiter 5.9.2** with Vintage Engine (JUnit 4 compatibility)
- 24 test files across multiple packages

### Test Categories
1. **FSRS Tests**: Spaced repetition algorithm validation
2. **APKG Tests**: Anki deck format parsing/generation
3. **Zstd Tests**: Native library integration
4. **Dictionary Tests**: Word database operations
5. **Subtitle Tests**: Format conversion and parsing
6. **Player Tests**: Video playback and danmaku rendering
7. **UI Tests**: Compose UI testing with UI Test JUnit4

### Important Test Notes
- Some tests automatically download Whisper models
- JNI tests may have platform-specific requirements
- Run `testLast` for tests that must execute in isolation

## Build System

- **Gradle 8.x** with Kotlin DSL
- Jetpack Compose for Desktop plugin
- Platform-specific packaging configured in build.gradle.kts
- Separate `RemoveConfig` subproject for cleanup utility

## CI/CD (GitHub Actions)

- **Test.yml**: Cross-platform testing (Windows, macOS Intel/ARM)
- **Build Package.yml**: Automated packaging
- **FFmpeg builds**: Platform-specific binary compilation
- **UI Test.yml**: Automated UI testing

## Resources

### Important Files
- **build.gradle.kts**: Main build configuration (498 lines) - contains all custom tasks
- **settings.gradle.kts**: Plugin management and repository configuration
- **gradle.properties**: Kotlin 2.2.21, Compose 1.9.3, JVM args

### Documentation
- **README.md**: User-facing documentation (Chinese) with feature demos
- **Privacy Policy.md**: Privacy policy
- **License**: GPLv3

## Development Notes

- **No linter configured**: No ktlint, checkstyle, or PMD setup
- **Chinese comments**: Source code is extensively documented in Chinese
- **Cross-platform**: Supports Windows, macOS (Intel/ARM), Linux
- **UTF-8 encoding**: Required throughout (configured in gradle.properties)
- **VLC dependency**: Required for video playback functionality
- **Main library dependencies**: VLCJ, FlatLaF, OpenNLP, Ktor, PDFBox, SQLite JDBC