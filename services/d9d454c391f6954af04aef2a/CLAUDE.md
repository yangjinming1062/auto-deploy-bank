# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **jhipster-kotlin** (KHipster) - a JHipster blueprint that generates Kotlin-based Spring Boot applications. It extends generator-jhipster 8.x and replaces Java templates with Kotlin equivalents.

## Common Commands

```bash
# Install dependencies
npm install | yarn

# Run tests
npm test                          # Run all tests with vitest
npm run vitest                    # Run in watch mode
npm run update-snapshot           # Update test snapshots

# Linting and formatting
npm run lint                      # ESLint + EJS linting
npm run lint-fix                  # Auto-fix lint issues
npm run prettier-check            # Check formatting
npm run prettier-format           # Auto-format files

# Generate samples
khipster --defaults --skip-install                    # Default Maven app
khipster --build gradle --defaults --skip-install     # Default Gradle app
khipster generate-sample --app-sample sample-name     # CI sample generation

# Sync templates with upstream JHipster
khipster synchronize          # Check conflicts, press 'i' to sync each file
```

## Architecture

### Directory Structure
- **generators/** - Sub-generators following JHipster blueprint pattern
- **cli/** - CLI entry point (khipster command)
- **test/** - Integration tests with template fixtures
- **.blueprint/** - Blueprint-specific commands for CI/sample generation

### Generator Hierarchy

The project uses JHipster's priority-based generator pattern. The main generators are:

1. **kotlin** - Provides Kotlin build configuration (Maven/Gradle), replaces Java directories with Kotlin (`src/main/kotlin`, `src/test/kotlin`), and adds Kotlin dependencies/plugins
2. **spring-boot** - Main generator that composes detekt and spring-boot-v2, implements template file substitution (converts `.java` to `.kt`), and uses `customizeTemplatePaths` to prioritize Kotlin templates over upstream Java ones
3. **ktlint** - Downloads ktlint CLI and formats generated Kotlin files
4. **detekt** - Adds Detekt static analysis configuration
5. **migration** - Handles v7 to v8 template compatibility
6. **spring-boot-v2** - Provides JHipster 7 template compatibility

### Generator Pattern

Each generator extends `BaseApplicationGenerator` and implements priority methods:
```javascript
get [BaseApplicationGenerator.LOADING]() { ... }
get [BaseApplicationGenerator.COMPOSING]() { ... }
get [BaseApplicationGenerator.PREPARING]() { ... }
get [BaseApplicationGenerator.WRITING]() { ... }
get [BaseApplicationGenerator.POST_WRITING]() { ... }
```

### Template Substitution

The **spring-boot generator** uses `customizeTemplatePaths` to redirect Java template lookups to Kotlin templates:
- Looks for Kotlin templates in `generators/spring-boot/templates/`
- Falls back to upstream Java templates when no Kotlin version exists
- Files are processed through `convertToKotlinFile()` helper

### Test Structure
- **generators/*/generator.spec.js** - Unit tests for each generator
- **test/app.spec.js** - Full application generation tests
- **test/server.spec.js** - Server-side generation tests
- **test/templates/** - Expected output fixtures
- Uses Vitest with `generator-jhipster/testing` helpers

## Key Conventions

- Kotlin source directories: `src/main/kotlin`, `src/test/kotlin`
- Template files use `.ejs` extension with Kotlin-specific implementations
- Gradle catalog version management via `generators/kotlin/resources/gradle/libs.versions.toml`
- Priority queues: `loading` → `composing` → `preparing` → `writing` → `postWriting`