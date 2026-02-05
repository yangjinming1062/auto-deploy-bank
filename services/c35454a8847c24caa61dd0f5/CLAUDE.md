# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MuJing (幕境) is an English vocabulary learning application that helps users learn words through real context from movies, TV shows, and documents. Features include contextual learning, video playback with danmaku (floating word annotations), spaced repetition (FSRS), subtitle extraction, and dictation exercises.

## Build Commands

```bash
# Build the project
./gradlew build

# Run the application
./gradlew run

# Run tests (excludes JNI tests requiring cargo)
./gradlew test

# Run a single test class
./gradlew test --tests "com.mujingx.fsrs.FSRSServiceTest"

# Package for distribution
./gradlew packageDmg         # macOS DMG
./gradlew packageMsi         # Windows MSI
./gradlew packageDeb         # Linux DEB

# Build Rust JNI library manually (if needed)
cd rust-zstd-jni && cargo build --release
```

**Requirements**: Java 21, Kotlin 2.2.21, Compose 1.9.3, cargo (for Rust JNI)

## Architecture

### Technology Stack
- **UI**: Jetpack Compose for Desktop with FlatLaf theming
- **Video**: VLCj with embedded VLC libraries
- **Database**: SQLite (ecdict dictionary, vocabulary storage)
- **Compression**: Rust JNI (zstd) for Anki apkg files
- **Spaced Repetition**: Custom FSRS implementation
- **TTS**: Platform-specific implementations (Azure, Mac TTS, Windows SAPI, eSpeak)

### Key Modules

| Package | Purpose |
|---------|---------|
| `ui/` | Compose UI screens (word screen, subtitle screen, text screen), dialogs, components |
| `state/` | Global state management (GlobalState, AppState) with persistence |
| `player/` | Video playback, danmaku rendering, caption handling |
| `fsrs/` | Spaced repetition algorithm, flashcard management, Anki apkg support |
| `data/` | Vocabulary, dictionary, file persistence |
| `lyric/` | Subtitle parsing and synchronization |
| `tts/` | Text-to-speech abstractions for cross-platform audio |
| `event/` | EventBus for decoupled communication |
| `ffmpeg/` | FFmpeg utilities for video processing |

### Data Flow

1. **Main Entry**: `Main.kt` initializes FileKit, FlatLaf theme, and launches `App.kt`
2. **State Management**: `GlobalState` holds user preferences (theme, volumes, window state); `AppState` holds runtime state (current vocabulary, learning progress)
3. **Word Learning**: User selects vocabulary -> `WordScreen` displays words -> `PlayerComponent` plays associated video -> `DanmakuManager` shows word annotations
4. **Vocabulary Creation**: Extract words from video subtitles or documents -> `Lyric` parser -> `Vocabulary` data structure -> SQLite storage

### State Persistence

- Global settings saved to `~/.config/MuJing/config.json` (or platform equivalent)
- Vocabulary files stored in user config directory as JSON
- Dictionary (ecdict) embedded as SQLite database (extracted from `dict/ecdict.7z` on first build)

### Rust JNI Integration

The `rust-zstd-jni/` module provides zstd compression for Anki `.apkg` files. Built automatically during Gradle build:
- Exposes `compressBytes()` and `decompressBytes()` via JNI
- Must be built before tests; excluded from CI test runs without cargo

### Important Implementation Notes

- UTF-8 encoding required: JVM args `-Dfile.encoding=UTF-8`
- Window positioning uses Compose's `WindowPlacement` enum
- Vocabulary persistence uses `kotlinx.serialization` with `Json` configuration
- VLC discovery: embedded VLC for Windows/macOS, native discovery on Linux
- Danmaku system uses `TimelineSynchronizer` for word-to-video alignment