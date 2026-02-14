# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Run all tests
mvn test -B

# Run a single test class (tests are in src/test/java/com/alibaba/json/bvt/)
mvn test -Dtest=ClassName -B

# Run a specific test method
mvn test -Dtest=ClassName#methodName -B

# Compile without running tests
mvn compile

# Package the JAR
mvn package -DskipTests
```

Note: Maven Surefire is configured to include only `**/bvt/**/*.java` tests by default. The test package is `com.alibaba.json.bvt` (legacy naming).

## Architecture Overview

Fastjson 1.x is a JSON processor (parser + generator) with a pluggable architecture centered around `ParserConfig` and `SerializeConfig`.

### Core Components

- **JSON.java** - Main public API entry point for `toJSONString()` and `parseObject()` methods
- **parser/** - Tokenization and deserialization pipeline
  - `DefaultJSONParser.java` - Main parser orchestrator
  - `JSONScanner.java` / `JSONReaderScanner.java` - Lexical analysis
  - `ParserConfig.java` - Parsing configuration and deserializer registry
  - `deserializer/` - Type-specific deserializers (ASMDeserializerFactory, JavaBeanDeserializer, etc.)
- **serializer/** - Serialization pipeline
  - `JSONSerializer.java` - Main serialization orchestrator
  - `SerializeWriter.java` - Buffered output writer
  - `SerializeConfig.java` - Serialization configuration and serializer registry
  - Individual `*Codec.java` and `*Serializer.java` classes for specific types
- **asm/** - Custom lightweight ASM bytecode library for generating fast serialization/deserialization code at runtime
- **util/** - Utility classes including `TypeUtils.java` (~3500 lines, handles reflection and generics)
- **annotation/** - User annotations: `@JSONField`, `@JSONType`, `@JSONCreator`, `@JSONPOJOBuilder`

### Key Design Patterns

- **SPI Registry**: `SerializeConfig` and `ParserConfig` maintain maps of type-to-serializer/deserializer mappings
- **Filter Chain**: `SerializeFilter` interface enables pre/post-processing during serialization
- **ASM Optimization**: The library generates bytecode via `ASMSerializerFactory` and `ASMDeserializerFactory` for hot paths
- **Feature Flags**: Both parsing (`Feature` enum) and serialization (`SerializerFeature` enum) use bitmask features

### Support Modules

The `support/` directory contains integrations with other frameworks:
- **spring/** - Spring Framework integration
- **jaxrs/** - JAX-RS (REST) integration
- **retrofit/** - Retrofit integration
- **hsf/** - Alibaba HSF protocol support
- **geo/** - Geographic data format support
- **moneta/** - JSR-354 Money/Currency support

## Compiler Target

Java 1.5+ (configured in pom.xml as `jdk.version=1.5`). The library maintains backward compatibility with older Java versions.

## Note on Version

This is fastjson 1.x. Fastjson 2.x has been released separately at https://github.com/alibaba/fastjson2 with improved performance and security.