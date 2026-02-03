# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CodeLocator is a debugging toolkit containing an Android SDK and an Android Studio/IntelliJ IDEA plugin. It enables developers to inspect View hierarchies, Activity/Fragment information, and navigate from UI elements to source code. Used by major ByteDance apps including TikTok, Douyin, and CapCut.

## Build Commands

### CodeLocatorPlugin (IntelliJ IDEA Plugin)

```bash
cd CodeLocatorPlugin

# Build the plugin (outputs to build/distributions)
./gradlew build

# Run IntelliJ IDEA with the plugin installed for testing
./gradlew runIde

# Build and prepare sandbox with required assets
./gradlew prepareSandbox
```

### CodeLocatorApp (Android SDK)

```bash
cd CodeLocatorApp

# Build all modules
./gradlew assembleDebug

# Build a specific Lancet module (e.g., for Activity code navigation)
./gradlew :CodeLocatorLancetActivity:assembleDebug

# Publish SDK to local Maven for testing
./gradlew publish

# Publish all Lancet modules
./gradlew :CodeLocatorLancetAll:publish

# Clean build artifacts
./gradlew clean
```

## Architecture

### CodeLocatorPlugin (IntelliJ IDEA Platform)

**Location:** `CodeLocatorPlugin/`

A sidebar plugin for Android Studio that communicates with the Android app via ADB.

**Key packages:**
- `panels/` - UI components including `CodeLocatorWindow.kt` (main window), `MainPanel.kt`, and various tree/table panels for View, Activity, Fragment, and File information
- `device/` - ADB device connection and communication (`DeviceManager.kt`)
- `parser/` - Parsers for data received from Android app (`DumpInfoParser.kt`, `JumpParser.kt`, `UixInfoParser.kt`)
- `processor/` - View property processors for rendering view attributes (`TextProcessor.kt`, `LayoutProcessor.kt`, etc.)
- `utils/` - Platform utilities (`MacHelper.kt`, `WindowsHelper.kt`, `OSHelper.kt`)
- `listener/` - Plugin lifecycle (`CodeLocatorStartupActivity.java`, `CodeLocatorProjectManagerListener.java`)

**Entry point:** `CodeLocatorWindowFactory.kt` registers `CodeLocatorWindow` as a tool window in Android Studio's sidebar.

### CodeLocatorApp (Android SDK)

**Location:** `CodeLocatorApp/`

**Core modules:**
- `CodeLocatorCore/` - Main SDK providing View inspection, Activity/Fragment tracking, and data collection
- `CodeLocatorModel/` - Data models shared between plugin and SDK (serializable via Gson)
- `app/` - Demo application showcasing SDK integration

**Lancet AOP modules** (code navigation via bytecode weaving):
- `CodeLocatorLancetActivity/` - Jump to Activity start code
- `CodeLocatorLancetXml/` - Jump to XML layout files
- `CodeLocatorLancetView/` - Jump to `findViewById`, `OnClickListener`, `OnTouchListener`
- `CodeLocatorLancetToast/` - Jump to Toast.show() code
- `CodeLocatorLancetDialog/` - Jump to Dialog.show() code
- `CodeLocatorLancetPopup/` - Jump to PopupWindow show code
- `CodeLocatorLancetAll/` - Combines all Lancet modules

**Key SDK packages (CodeLocatorCore):**
- `analyzer/` - `ViewInfoAnalyzer`, `ActivityInfoAnalyzer`, `FragmentInfoAnalyzer` for collecting UI metadata
- `hook/` - `CodeLocatorLayoutInflator` for intercepting layout inflation
- `receiver/` - `CodeLocatorReceiver` handles communication from the IDE plugin

**Integration:** Add as dependency:
```gradle
implementation "com.bytedance.tools.codelocator:codelocator-core:2.0.4"

// For code navigation, apply Lancet plugin and add:
debugImplementation "com.bytedance.tools.codelocator:codelocator-lancet-all:2.0.4"
```

## Communication Protocol

The plugin and Android SDK communicate via:
1. **ADB commands** - Plugin sends broadcast intents to the app
2. **File-based data** - App writes JSON data to shared storage, plugin reads and parses it
3. **Key classes:** `CodeLocatorReceiver` (Android) ↔ `DeviceManager` (IDE)

## Development Notes

- The plugin targets IntelliJ IDEA 2022.1+ (`sinceBuild: 213`)
- Java 11 source/target compatibility for both plugin and SDK
- The Android SDK uses AndroidX (API 16+) and Retrofit-compatible Gson for serialization
- Lancet modules useASM 6 bytecode manipulation for method interception