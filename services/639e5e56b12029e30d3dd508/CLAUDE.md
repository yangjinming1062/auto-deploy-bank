# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Capsule is an immutable (persistent) collections library for Java 11+ built entirely around **CHAMP tries** (Compressed Hash-Array Mapped Prefix-tries). CHAMP is an evolutionary improvement over traditional HAMTs (Hash-Array Mapped Tries), offering better performance for iteration, equality checking, and memory footprint. The library is designed for standalone use and for embedding in domain-specific languages.

**Key interfaces**: `Set`, `Map`, `SetMultimap`, `BinaryRelation` (all in root package)
**Core implementation**: `core/` package - persistent trie-based collections
**Trie logic**: `core/trie/` - Node interfaces (SetNode, MapNode, MultimapNode) and transformers
**Utilities**: `util/` - iterators, functions, stream collectors, and collection abstractions

## Build Commands

Both Gradle and Maven are supported:

```bash
# Gradle (primary)
./gradlew clean build              # Build and test
./gradlew test                     # Run tests
./gradlew jmh                     # Build JMH benchmarks

# Maven (alternative)
mvn -B compile test               # Build and test
mvn test                          # Run tests
mvn test -Dtest=ClassName         # Run single test class
mvn test -Dtest=ClassName#method  # Run single test method
mvn license:check                 # Verify license headers
mvn license:format                # Auto-add license headers
```

## Running Benchmarks

```bash
./benchmark.zsh              # Run all benchmarks (time + memory)
./benchmark.zsh time         # Runtime performance only
./benchmark.zsh space        # Memory footprint only
```

JMH benchmark sources are in `src/jmh/java/io/usethesource/capsule/jmh/`. Results are written to `log-jmh-persistent-collections-*.txt`.

## Architecture

The library uses a unified trie-based architecture:

1. **Trie Nodes** (`core/trie/`): SetNode, MapNode, MultimapNode - recursive immutable data structures using bitmap-based slot arrays for compact storage
2. **Transformers** (`core/trie/`): BottomUpImmutableNodeTransformer - composes nodes using HAMT/CHAMP semantics with structural sharing for persistence
3. **Public APIs** (`core/`): PersistentTrieSet, PersistentTrieMap, PersistentTrieSetMultimap - concrete implementations with transient (mutable builder) variants
4. **Factories** (`factory/`): DefaultSetFactory - creates immutable instances
5. **Utilities** (`util/`): AbstractSpecializedImmutableSet/Map - base classes for type-specific specializations

Key design patterns:
- **Immutable/Transient Duality**: Collections have `Immutable` and `Transient` nested interfaces. Transient views allow efficient bulk mutations, then `.freeze()` converts back to immutable with structural sharing.
- **Mutation Methods**: Use `__` prefix (`__insert`, `__put`, `__remove`) to distinguish from standard Java collection semantics.
- **Bitmap Encoding**: Immutable trie nodes use bitmap indexing to compactly represent sets of child nodes, enabling O(log n) operations with structural sharing.

## Code Standards

- **License headers**: All source files must include the BSD 2-Clause license header (see `LICENSE.header-template`). Run `mvn license:format` to auto-apply.
- **Java version**: Code must be compatible with Java 11 (compile target is 11)
- **Testing**: Tests use JUnit 5 + junit-quickcheck for property-based testing

## Interactive Exploration

```bash
./gradlew clean build
jshell --class-path ./build/libs/capsule-*-SNAPSHOT.jar
```