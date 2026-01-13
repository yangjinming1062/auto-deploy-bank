# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Discord4J is a fast, powerful, unopinionated, reactive Java/Kotlin library for building Discord bots using the official Discord Bot API. It follows the reactive-streams protocol using Project Reactor for asynchronous, non-blocking operations.

## Architecture

Discord4J is a **modular** project with the following modules:

- **common** - Base utilities and models shared across modules
- **rest** - Low-level REST API client for Discord HTTP endpoints with rate limiting
- **gateway** - WebSocket client for Discord Gateway events, state management, and shard coordination
- **voice** - Voice connection support for sending/receiving audio
- **core** - High-level API combining rest + gateway + voice modules (the main entry point for most users)
- **oauth2** - OAuth2 authentication flows

### Key Components

- **Reactive Design**: All modules use Project Reactor (`Mono`, `Flux`) for async operations
- **Shard Management**: Built-in support for sharding through `GatewayBootstrap`, `GatewayClientGroupManager`
- **Event System**: Event-driven architecture in `discord4j.core.event.domain.*`
- **Entity Objects**: Rich domain models in `discord4j.core.object.entity.*`
- **State Management**: Cached entity state in `discord4j.core.state.*`

### Main Entry Points

- `DiscordClient` (`core/src/main/java/discord4j/core/DiscordClient.java`) - Entry point for REST-only operations
- `GatewayBootstrap` (`core/src/main/java/discord4j/core/shard/GatewayBootstrap.java`) - Entry point for Gateway connections
- `DiscordClientBuilder` (`core/src/main/java/discord4j/core/DiscordClientBuilder.java`) - Fluent builder for client configuration

## Development Commands

### Build and Test
```bash
# Build entire project
./gradlew build

# Run tests
./gradlew test

# Run tests for specific module
./gradlew :core:test
./gradlew :rest:test
./gradlew :gateway:test

# Run single test class
./gradlew test --tests "discord4j.core.util.PermissionUtilTest"

# Run tests with output
./gradlew test --info

# Clean build
./gradlew clean build

# Assemble JARs without running tests
./gradlew assemble
```

### Code Quality
```bash
# Run all checks (tests + verification)
./gradlew check

# Generate Javadoc
./gradlew javadoc

# Build without running tests (faster iteration)
./gradlew build -x test
```

### Dependency Management
```bash
# Check for dependency updates
./gradlew dependencyUpdates

# Download all dependencies to Gradle cache
./gradlew downloadDependencies
```

### Publishing
```bash
# Publish to Sonatype (requires credentials)
./gradlew publishToSonatype closeAndReleaseSonatypeStagingRepository

# Publish without tests (release only)
./gradlew -x test publishToSonatype closeAndReleaseSonatypeStagingRepository
```

## Contributing Guidelines

- **Branching Strategy**: Changes are merged forward from oldest supported branch to master. If stable releases are on `3.2.x`, PRs should target that branch.
- **Style Requirements**:
  - Follow `.editorconfig` settings (space indents)
  - All new files need LGPL 3 boilerplate header
  - Maintain JavaDocs for public APIs
- **Issue Tracker**: Not for support - use Discord server or GitHub Discussions
- **Testing**: Write tests for new functionality; examples in `core/src/test/java/discord4j/core/Example*.java`

## Module-Specific Information

### Core Module
- **Location**: `core/`
- **Purpose**: High-level API combining REST + Gateway + Voice
- **Examples**: `core/src/test/java/discord4j/core/Example*.java`
- **Key Packages**:
  - `discord4j.core.event` - Event system
  - `discord4j.core.object.entity` - Discord entity models
  - `discord4j.core.shard` - Sharding logic
  - `discord4j.core.state` - State management and caching

### REST Module
- **Location**: `rest/`
- **Purpose**: Low-level REST API client with rate limiting
- **Key Packages**:
  - `discord4j.rest.service` - Service classes for each Discord endpoint
  - `discord4j.rest.request` - Request routing and rate limiting
  - `discord4j.rest.route` - Route definitions

### Gateway Module
- **Location**: `gateway/`
- **Purpose**: WebSocket client for Gateway events
- **Key Packages**:
  - `discord4j.gateway.json` - Gateway message formats
  - `discord4j.gateway.state` - State management
  - `discord4j.gateway.limiter` - Rate limiting for identify calls

### Voice Module
- **Location**: `voice/`
- **Purpose**: Voice connection support
- **Examples**: `core/src/test/java/discord4j/core/ExampleVoiceBot.java`

## Important Notes

### Intents
Since September 1, 2022, Discord requires bots to enable the "MESSAGE_CONTENT" intent to access message content. Configure intents using:
```java
GatewayDiscordClient client = DiscordClient.create(token)
    .gateway()
    .setEnabledIntents(IntentSet.nonPrivileged().or(IntentSet.of(Intent.MESSAGE_CONTENT)))
    .login()
    .block();
```

### Java Version
- Target: Java 8+ (tested on 8, 11, 17, 21 via CI)
- JavaDocs link configuration handled in `build.gradle:86-111`

### Dependency Management
- Uses Reactor BOM for dependency versions
- Jackson BOM for JSON processing
- Immutables for value types
- See `build.gradle:27-41` for version constants

## Testing Matrix

The project is tested on:
- Java versions: 8, 11, 17, 21
- OS: ubuntu-latest
- See `.github/workflows/gradle.yml` for CI configuration