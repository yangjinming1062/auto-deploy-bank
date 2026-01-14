# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ShakaApktool is a fork of [Apktool](http://ibotpeaches.github.io/Apktool/) for Android APK decompilation and recompilation. It includes modified versions of:
- **Apktool** - APK decoding/building
- **smali/baksmali** - DEX disassembly/assembly

The project uses Git submodules for the upstream Apktool and smali repositories.

## Build Commands

```bash
# Build all modules
./gradlew build

# Run tests (smali module tests require dex generation first)
./gradlew test

# Build fat JAR (executable CLI)
./gradlew :shaka:cli:fatJar

# Build release with ProGuard
./gradlew release

# Clean build artifacts
./gradlew clean
```

Note: Gradle 3.5 requires Java 8. Java 17+ is not compatible without upgrading Gradle.

## Module Architecture

```
shaka:lib          - Core utilities and resources (aapt binaries, i18n)
shaka:smali        - DEX assembly/disassembly (fork of JesusFreke/smali)
shaka:apktool      - APK decompilation/recompilation (fork of iBotPeaches/Apktool)
shaka:cli          - Command-line interface using JCommander
```

### Module Dependencies
- `lib` → No dependencies (base module)
- `smali` → `lib` (via AspectJ weaving)
- `apktool` → `smali` and `lib`
- `cli` → `apktool` (produces fat JAR)

### Key Frameworks
- **AspectJ** - AOP woven into all modules except `lib` via `shaka:build.gradle`
- **ANTLR/JFlex** - Grammar generation in `smali` module (`-PgenGrammarSource=true`)
- **JCommander** - CLI argument parsing in `cli` module

## CLI Command Structure

The main entry point is `com.rover12421.shaka.cli.Main` using JCommander with three command groups:

**Apktool Commands:**
- `decode` - Decompile APK
- `build` - Rebuild APK
- `install-framework` - Install framework files
- `publicize-resources` - Make resources public
- `empty-framework-dir` - Clean framework directory

**baksmali Commands:**
- `disassemble` - Disassemble DEX to smali
- `deodex` - Deodex odex files
- `dump` - Dump DEX content
- `list` - List DEX content

**smali Commands:**
- `assemble` - Assemble smali to DEX

## Important Resources

- **ShakaAapt**: Native binaries (aapt) for multiple platforms in `lib/src/main/resources/ShakaAapt/`
- **i18n**: Language files in `lib/src/main/resources/lang/` (en_US, zh_CN, zh_TW)
- **Version Info**: Generated from git at build time - format: `version-branch-hash-date`