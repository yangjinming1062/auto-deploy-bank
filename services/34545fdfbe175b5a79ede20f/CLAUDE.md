# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

- **Build the project (runs tests & checks):**
  ```bash
  ./gradlew build
  ```

- **Build without running tests:**
  ```bash
  ./gradlew assemble
  ```

- **Run all checks ( Spotless, Checkstyle, etc.):**
  ```bash
  ./gradlew check
  ```

- **Build distribution packages:**
  ```bash
  ./gradlew distZip
  ```

- **Build all distribution packages:**
  ```bash
  ./gradlew assembleLinuxX64 assembleLinuxArm64 assembleMacX64 assembleMacArm assembleWindows
  ```

## Run Commands

- **Run the application (OmegaT GUI):**
  ```bash
  ./gradlew run
  ```

## Test Commands

- **Run all tests:**
  ```bash
  ./gradlew test
  ```

- **Run a single test class:**
  ```bash
  ./gradlew test --tests "org.omegat.BundleTest"
  ```

- **Run integration tests:**
  ```bash
  ./gradlew testIntegration
  ```

- **Run acceptance tests:**
  ```bash
  ./gradlew testAcceptance
  ```

## Architecture

This is the OmegaT project, a Java-based Computer Assisted Translation (CAT) tool.

- **Core Source (`src/`)**: Contains the main application logic, UI (`gui/`), core functionality, and plugins.
- **Modules (`language-modules/`)**: Individual subprojects for language-specific support (e.g., Hunspell dictionaries, Morfologik stemmers). Each language module (e.g., `de`, `fr`) is a separate Gradle subproject.
- **Utilities (`aligner/`, `spellchecker/`, `machinetranslators/` etc)**: Standalone subprojects or modules for specific features like file alignment, spellchecking, and machine translation integration.
- **Main Entry Point**: `org.omegat.Main` (`src/org/omegat/Main.java`).
- **Build System**: Uses Gradle with custom plugins defined in `build-logic/`.