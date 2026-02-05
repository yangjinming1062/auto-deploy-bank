# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MemShellParty is a memory shell generation tool for Java web servers. It's a multi-module Gradle project with the main purpose of generating various types of memory shells (in-memory web shells) for authorized security testing and research.

## Build Commands

```bash
# Build a specific module
./gradlew :generator:build
./gradlew :boot:build
./gradlew :packer:build

# Build all modules and publish to Maven Central
./gradlew publishAllToMavenCentral

# Run Spring Boot application (boot module)
./gradlew :boot:bootRun

# Build boot JAR (requires React frontend build first)
./gradlew :boot:bootJar
```

## Testing

Integration tests use Testcontainers and are computationally expensive. Run selectively:

```bash
# Run all unit tests for a module
./gradlew :generator:test

# Run specific integration tests (requires war files first)
./gradlew :vul:vul-webapp:war :vul:vul-webapp-jakarta:war
./gradlew :integration-test:test --tests '*.tomcat.*'

# Build vulnerability war files for testing
./gradlew :vul:vul-webapp:war
./gradlew :vul:vul-webapp-jakarta:war
./gradlew :vul:vul-webapp-expression:war
./gradlew :vul:vul-webapp-deserialize:war
```

## Module Architecture

### Core Modules

- **generator**: Core memshell generation using ByteBuddy and ASM. Compiles to Java 8.
- **packer**: Deserialization payloads (JAR, BCEL, etc.) for exploitation. Compiles to Java 8.
- **boot**: Spring Boot 3.x REST API that wraps generator/packer. Uses Undertow.
- **memshell-party-common**: Shared utilities for bytecode manipulation (ASM/ByteBuddy).
- **integration-test**: Docker-based integration tests using Testcontainers.
- **tools/***: Standalone shell client tools (Godzilla, Behinder, Suo5, AntSword).

### Vulnerability Test Modules (vul/*)

Test applications for various servers: vul-webapp, vul-webapp-jakarta, vul-webapp-expression, vul-webapp-deserialize, vul-springboot*, etc.

### Memshell Agent Modules (memshell-agent/*)

Playground modules demonstrating Agent-based memory shell techniques using ASM, Javassist, and ByteBuddy.

## Key Architecture Patterns

### Server/ShellType/ShellTool Triad

The core architecture uses three dimensions to generate memory shells:

1. **ServerType** (15+ servers): Tomcat, Jetty, Undertow, SpringWebMVC, WebLogic, etc.
2. **ShellType**: Servlet, Filter, Listener, Valve, WebSocket, Agent variants, Spring interceptors
3. **ShellTool**: Godzilla, Behinder, AntSword, Suo5, Command, NeoreGeorg, Proxy, Custom

### Generation Flow

```
MemShellGenerator.generate()
  -> ServerFactory.getServer(serverName)  // Returns AbstractServer
  -> ServerFactory.getShellInjectorPair() // Maps shell tool + type to (shellClass, injectorClass)
  -> ShellToolFactory.generateBytes()    // Generates shell bytecode via ByteBuddy/ASM
  -> InjectorGenerator.generate()        // Generates injector bytecode
  -> ResponseBodyGenerator (optional)    // Wraps as probe/payload
```

### ServerFactory Registry Pattern

All servers are registered via static blocks in `ServerFactory.java`:
```java
static {
    register(Server.Tomcat, Tomcat::new);
    register(Server.Jetty, Jetty::new);
    // ...
}
```

Each AbstractServer subclass defines supported ShellType->Injector mappings via `getShellInjectorMapping()`.

### Bytecode Generation

- **ByteBuddyShellGenerator**: Abstract base for ByteBuddy-based shell generation
- **ProcessorRegistry**: Applies builder/byte processors for code transformation
- **TargetJreVersionVisitorWrapper**: Adapts bytecode for JDK 6-21 compatibility

## Key Classes

| Location | Purpose |
|----------|---------|
| `generator/.../MemShellGenerator.java` | Main entry point for generation |
| `generator/.../ServerFactory.java` | Server registry and tool mapping |
| `generator/.../memshell/server/AbstractServer.java` | Base for all server adapters |
| `generator/.../memshell/ShellType.java` | Shell type constants |
| `generator/.../memshell/ShellTool.java` | Shell tool constants |
| `generator/.../ShellToolFactory.java` | Generates shell bytecode |
| `boot/.../controller/MemShellGeneratorController.java` | REST API endpoint |

## Java Version Requirements

- **Build**: JDK 17 (Gradle toolchain)
- **generator/packer output**: Java 8 (JDK 6-21 compatibility via bytecode adaptation)
- **boot module**: Java 17 runtime