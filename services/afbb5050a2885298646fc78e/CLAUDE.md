# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Compile the project
mvn compile

# Run all tests (bvt tests only per pom.xml configuration)
mvn test

# Run a single test class
mvn test -Dtest=com.alibaba.json.bvt.JSONObjectTest

# Run a specific test method
mvn test -Dtest=com.alibaba.json.bvt.JSONObjectTest#testParseObject

# Package the JAR
mvn package

# Skip tests during build
mvn package -DskipTests
```

## Project Overview

Fastjson is a Java JSON library (version 1.x) that provides JSON serialization and deserialization. The project uses Maven for build management and targets **Java 1.5** compatibility.

**Note:** FASTJSON 2.0.x is the recommended version for new projects, offering better performance and security. This is the legacy 1.x branch.

## Architecture

The main source code is organized into these key packages:

- **`com.alibaba.fastjson.JSON`** - Main entry point with `toJSONString()` and `parseObject()` methods
- **`parser/`** - JSON parsing layer
  - `JSONLexer` / `JSONLexerBase` / `JSONScanner` / `JSONReaderScanner` - Tokenization and lexical analysis
  - `DefaultJSONParser` - Main parser orchestration
  - `ParserConfig` - Parser configuration and feature flags
  - `deserializer/` - Type-specific deserializers (Object, Collection, Enum, Date, etc.)
- **`serializer/`** - JSON serialization layer
  - `JSONSerializer` - Main serialization orchestration
  - `SerializeConfig` - Serializer configuration
  - Type-specific serializers (DateCodec, CollectionCodec, EnumSerializer, etc.)
  - `ASMSerializerFactory` - Generates bytecode for high-performance serialization
- **`asm/`** - Bytecode generation utilities for ASM-based optimization
- **`annotation/`** - User-facing annotations (`@JSONField`, `@JSONType`)
- **`support/`** - Third-party integrations (Spring, Guava, Hibernate, etc.)

## Test Organization

- Tests are located in `src/test/java/com/alibaba/json/bvt/` (Business Verification Tests)
- The surefire plugin is configured to only run tests matching `**/bvt/**/*.java`
- Nearly 3000 test files covering parsing, serialization, and integrations
- Tests are often named after GitHub issues they fix (e.g., `issue_1234`, `bugfix_5678`)

## Key Concepts

- **Features** - Parser behavior flags controlled via `Feature` enum (e.g., `Feature.SortFeidFastMatch`, `Feature.AutoTypeSupport`)
- **SerializerFeature** - Serializer behavior flags (e.g., `SerializerFeature.WriteMapNullValue`, `SerializerFeature.WriteClassName`)
- **Type References** - Used for generic type preservation: `TypeReference<List<T>>`
- **Filters** - `SerializeFilter` and `ParseProcess` extensions for custom processing
- **Symbol Table** - `SymbolTable` for string interning optimization during parsing
- **Annotations**
  - `@JSONField` - Field-level serialization/deserialization control (name, format, ordinal, etc.)
  - `@JSONType` - Class-level type configuration (serializer, deserializer, features)

## Optional Dependencies

The project uses optional dependencies for framework integrations in `support/`:
- Spring (WebMVC, WebSocket)
- Apache CXF (JAX-RS)
- Guava
- Hibernate Validator
- javax.servlet, javax.ws.rs

These are marked `provided` in pom.xml to avoid transitive dependency conflicts.