# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenRewrite is a distributed Java source refactoring tool with a custom Abstract Syntax Tree (AST) supporting Java 8+ language features. It encodes source code structure and formatting, allowing reconstruction of code with original formatting preserved.

## Build Commands

```bash
./gradlew build              # Full build with tests
./gradlew build -x test      # Build without tests
./gradlew test               # Run all tests
./gradlew test --tests "*.ChangeTest"  # Run specific test class
./gradlew clean              # Clean build artifacts
./gradlew javadoc            # Generate Javadoc
```

The project uses Gradle wrapper. Java 11+ is required.

## Project Structure

```
rewrite-core/           # Core AST framework and visitor pattern
  src/main/java/org/openrewrite/
    Tree.java           # Base interface for all AST nodes
    SourceVisitor.java  # Visitor pattern implementation
    Refactor.java       # Main refactoring orchestration
    Cursor.java         # Tree traversal position tracking
    Formatting.java     # Preserves original formatting
rewrite-java/           # Java-specific refactoring
  src/main/java/org/openrewrite/java/
    JavaParser.java     # Java source to AST parser
    tree/J.java         # Java AST node definitions
    refactor/           # Refactoring visitor implementations
    search/             # Search visitors (FindMethods, FindType, etc.)
    internal/grammar/   # ANTLR-generated parser files
  src/main/antlr/       # ANTLR grammar files (.g4)
```

## Architecture

**Tree & Visitor Pattern**: All AST nodes implement `Tree` interface. The `SourceVisitor<R>` class traverses trees via the visitor pattern with automatic tree walking. Subclasses override `defaultTo()` and `visitTree()` methods.

**Formatting Separation**: AST nodes separate content from formatting via `Formatting` objects. Each tree node has a UUID for identity tracking across transformations.

**Java AST (J)**: All Java-specific nodes extend the `J` interface which routes to `JavaSourceVisitor`. The `JavaPrintVisitor` reconstitutes source code with original formatting.

**Scoped Visitors**: Use `ScopedVisitorSupport` for visitors that need to track variable scopes. See `ScopedJavaRefactorVisitor` for examples.

**ANTLR Grammar**: Java grammar is defined in ANTLR4 (.g4 files). Run `./gradlew :rewrite-java:generateAntlrSources` to regenerate parser files after grammar changes.

**Method Matching**: Use `MethodMatcher` for pattern-matching method signatures (supports wildcards like `java.util.List.*(..)`).

## Key Conventions

- All source files require the Apache License 2.0 header (enforced by gradle-license-plugin)
- Java 11 source/target compatibility with Kotlin stdlib for tests
- Lombok annotations are used extensively; build must run annotation processors
- Use `withFormatting()` and `withPrefix()`/`withSuffix()` to create modified tree copies
- Return typed `Optional` using `whenType(Class)` for type-safe casting

## Dependencies

- **ANTLR 4.8-1**: Parser generation
- **Jackson**: JSON/ Smile serialization
- **Koloboke**: High-performance collections
- **JUnit 5**: Testing framework
- **AssertJ**: Fluent assertions