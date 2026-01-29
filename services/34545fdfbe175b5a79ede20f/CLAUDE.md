# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Build all and run main tests
./gradlew build

# Quick build without documentation (skips containerized manual/HTML builds)
./gradlew build -PforceSkipDocumentBuild

# Run OmegaT from source
./gradlew run

# Build specific module JAR
./gradlew aligner:jar

# Build distribution packages
./gradlew installDist
./gradlew linux        # Linux distributions (deb/rpm)
./gradlew mac          # Mac distributions
./gradlew win          # Windows distributions (requires InnoSetup)

# Run tests
./gradlew test                    # All unit tests
./gradlew test --tests "ClassName"  # Specific test class
./gradlew testOnJava17            # Tests on Java 17
./gradlew testOnJava21            # Tests on Java 21
./gradlew testIntegration         # Team project integration tests

# Code quality checks
./gradlew check                   # All verification tasks
./gradlew spotlessCheck           # Code formatting check
./gradlew spotlessChangedApply    # Auto-format changed files
./gradlew spotbugsMain            # Static analysis

# Generate Javadoc
./gradlew javadoc
```

## Architecture Overview

OmegaT is a multi-module Java application (CAT tool) with a component-based architecture.

### Central Access Point: Core Class

All components are accessible through `Core` class static methods:
- `Core.getMainWindow()`, `Core.getEditor()`, `Core.getProject()`, `Core.getMatcher()`, etc.
- Components must implement specific interfaces and only be accessed via their interfaces

### Key Components (in `src/org/omegat/core/`)

| Component | Interface | Purpose |
|-----------|-----------|---------|
| Project | `IProject` | Manages loaded project data (`RealProject` / `NotLoadedProject` implementations) |
| Editor | `IEditor` | Translation editor pane |
| Matcher | `IMatcher` | Fuzzy match finder (TM, glossary, search) |
| SpellChecker | `ISpellChecker` | Spell checking |
| Segmenter | `Segmenter` | Source text segmentation rules |

### Event System

OmegaT uses an event-driven architecture via `CoreEvents`:
- `IProjectEventListener` - project open/close/compile/save events
- `IEntryEventListener` - active file/entry changes
- `IEditorEventListener` - editor state changes
- `IFontChangedEventListener` - UI font changes

Events are executed on the Swing Event Dispatch Thread (EDT).

### Threading Model

- UI operations run on the Swing EDT
- Long-running tasks use `SwingWorker` and lock the UI
- `SaveThread` auto-saves projects every 10 minutes (the only persistent background thread)

### Plugin System

Internal plugins are defined in `Plugins.properties` and bundled in `/modules` directory. External plugins go in `/plugins`.

Plugin types: `filter`, `tokenizer`, `machinetranslator`, `glossary`, `dictionary`, `theme`, `repository`, `script`, `miscellaneous`

### File Filter Architecture

Three filter generations (packages `filters2`, `filters3`, `filters4`):
- **filters2**: Legacy text-based formats (PO, Properties, HTML, LaTeX, etc.)
- **filters3**: Simple XML (ODF, DocBook, XHTML, etc.) - StAX-based
- **filters4**: Complex XML (MS Office OpenXML, XLIFF/SDLXliff, etc.)

FilterMaster orchestrates all filters and auto-detects file formats.

### Submodules Structure

| Module | Path | Purpose |
|--------|------|---------|
| machinetranslators | `machinetranslators/*/` | MT service connectors (Google, Yandex, Apertium, etc.) |
| language-modules | `language-modules/*/` | Language-specific tokenizers/dictionaries |
| spellchecker | `spellchecker/*/` | Hunspell, Morfologik, Lucene spell checkers |
| aligner | `aligner/` | Translation alignment tool |
| theme | `theme/` | UI theming |
| firsttime-wizard | `firsttime-wizard/` | First-run configuration wizard |
| tipoftheday | `tipoftheday/` | Tips of the day feature |

### Source Tree Layout

```
src/org/omegat/
  core/           # Core components (data, events, threads, team)
  gui/            # Swing UI components (editor, matches, glossary, etc.)
  filters2/       # Legacy file filters
  filters3/       # XML file filters (StAX-based)
  filters4/       # Complex XML file filters
  tokenizer/      # Default tokenizer
  languagetools/  # LanguageTool integration
  util/           # Utility classes
  externalfinder/ # External search integration
test/src/         # Unit tests
test/data/        # Test data files
test-integration/ # Integration tests (team project concurrency)
```

## Key Coding Conventions

### Style Requirements
- Line length: max 120 characters (80 for comments)
- Indentation: 4 spaces (no tabs)
- No asterisk imports - expand all imports
- GPL3 copyright header required on all files
- Bundle properties must be ASCII/7-bit clean (UTF-8 planned for v6.1+)

### GUI Development
- Use NetBeans GUI Builder for `.form` files (do not hand-edit)
- Follow MVC pattern: View classes in `gui/`, Controllers separate
- Use `OStrings.getString()` from Bundle for labels
- Set component labels in Controller using `Mnemonics.setLocalizedText()`

### API Design
- Stable APIs must be in `org.omegat.core` package
- Deprecate rather than remove APIs (affects plugins)
- Modules go in `/modules`, plugins in `/plugins`

### Logging
- Uses Java Util Logging (JUL) with `logger.properties`
- Configure with `-Djava.util.logging.config.file=/path/to/logger.properties`

## Development Notes

- Java 11+ required to build; Java 17+ for Linux deb/rpm packaging
- Docker/nerdctl required for documentation building (HTML manuals)
- Use `./gradlew spotlessChangedApply` before committing
- Checkstyle config: `config/checkstyle/checkstyle.xml`
- IDE configs: `assets/eclipse-formatting.xml`, `assets/intellij-Project.xml`