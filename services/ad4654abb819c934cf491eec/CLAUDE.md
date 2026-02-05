# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MemShellParty is a memory shell generation tool for Java web servers. It generates injectable memory shell bytecode for various Java application servers (Tomcat, Jetty, Spring, etc.) supporting multiple shell tools (Godzilla, Behinder, Suo5, AntSword).

## Build Commands

```bash
# Compile a specific module (recommended to avoid building all)
./gradlew :generator:build       # Core generator module
./gradlew :boot:build            # SpringBoot UI server
./gradlew :packer:build          # Packer module

# Run unit tests
./gradlew :generator:test
./gradlew :boot:test

# Build all modules to Maven Central
./gradlew publishAllToMavenCentral

# Build boot JAR (full application)
./gradlew :boot:bootjar -x test
```

## Development Commands

**Backend (SpringBoot + Gradle):**
```bash
./gradlew :boot:bootRun
```

**Frontend (React + Bun):**
```bash
cd web
bun install
bun run dev
```

**Full production build:**
```bash
cd web && bun install && bun run build
./gradlew :boot:bootjar -x test
```

## Module Architecture

The project uses a multi-module Gradle structure:

| Module | Purpose |
|--------|---------|
| `boot` | SpringBoot 3.x application serving the web UI and API |
| `generator` | Core memory shell generation using ByteBuddy and ASM |
| `packer` | Deserialization payload generators for exploit chains |
| `memshell-party-common` | Shared utilities (ByteBuddy, ASM, JNA, Commons) |
| `tools/*` | Client implementations (Godzilla, Behinder, Suo5, AntSword) |
| `memshell-agent/*` | Agent-based memory shell playgrounds (ASM, Javassist, ByteBuddy) |
| `integration-test` | Docker/Testcontainers-based integration tests |
| `vul/*` | Vulnerable web applications for testing |

## Core Concepts

### Server Types

Supported servers are defined in `ServerType.java`. Each server has corresponding injectors in `generator/src/main/java/.../injector/{server}/`:

- `tomcat/` - Tomcat valves, filters, listeners, servlets
- `jetty/` - Jetty handlers, filters
- `undertow/` - Undertow handlers, filters
- `springwebmvc/` - Spring MVC interceptors, controllers
- `springwebflux/` - Spring WebFlux handlers, filters
- `weblogic/`, `websphere/`, etc.

### Memory Shell Generation Flow

`MemShellGenerator.java` orchestrates the generation:

1. `ShellToolFactory.generateBytes()` - Generates shell class bytecode
2. `InjectorGenerator.generate()` - Generates injector class bytecode for the specific server
3. Optional probe embedding for detection testing

### Shell Types

Enum in `ShellType.java` includes: `Godzilla`, `Behinder`, `Suo5`, `AntSword`, `Agent`, `Command`, `Proxy`, `Custom`, and various bypass variants.

## Key Technologies

- **ByteBuddy / ASM** - Bytecode manipulation for shell generation
- **SpringBoot 3.x** - Web UI backend (Java 17)
- **Generator modules** - Java 8 target compatibility
- **Bun + React Router** - Frontend build and dev
- **Testcontainers** - Integration testing with real servers
- **Jakarta Servlet** - Modern servlet API (Jakarta namespace)

## Testing

```bash
# Run specific server integration tests (after building target war files)
./gradlew :integration-test:test --tests '*.tomcat.*'
./gradlew :integration-test:test --tests '*.jetty.*'

# Build test targets first
./gradlew :vul:vul-webapp:war :vul:vul-webapp-jakarta:war
```

Integration tests require significant time and Docker resources. Unit tests (`generator:test`, `boot:test`) are faster for basic validation.

## Versioning

- `generator`, `packer`, `memshell-party-common` are published to Maven Central
- `boot` is packaged as a Docker image for the full application
- Version is managed in `build.gradle.kts` (`version = "2.5.0"`)