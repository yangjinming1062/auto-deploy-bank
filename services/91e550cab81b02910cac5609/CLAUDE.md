# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Build all projects
./gradlew build

# Build without tests
./gradlew assemble

# Run all tests
./gradlew test

# Run a single test class
./gradlew :flashback-core-impl:test --tests "com.linkedin.flashback.matchrules.MatchRuleUtilsTest"

# Run tests in a specific module
./gradlew :flashback-core-impl:test

# Generate IntelliJ IDEA project files
./gradlew idea

# Start the Flashback admin server (Rest.li API)
./gradlew :flashback-admin:startAdminServer --Args="-port 1234"

# Clean build artifacts
./gradlew clean
```

## Dependencies Between Modules

```
flashback-admin → flashback-smartproxy → flashback-netty, flashback-core-impl, mitm
flashback-test-util → flashback-smartproxy, flashback-netty, flashback-core-impl
flashback-smartproxy → flashback-netty, flashback-core-impl, mitm
flashback-netty → flashback-core-impl
```

## Project Overview

Flashback is an HTTP/HTTPS mocking library that records and replays HTTP transactions ("scenes") for testing without external network dependencies. It operates as a MITM (Man-in-the-Middle) proxy supporting both HTTP and HTTPS protocols.

## Architecture

### Module Structure

- **flashback-core-impl**: Core domain models (Scene, MatchRule), serialization/deserialization, HTTP request/response wrappers
- **flashback-netty**: Netty-specific builders and mappers for converting between Netty HTTP types and Flashback's serializable types
- **flashback-smartproxy**: Main proxy logic - `FlashbackRunner` (entry point), `RecordController` (record mode), `ReplayController` (playback mode)
- **flashback-admin**: Rest.li API (`FlashbackAdminResource`) for remote proxy control via HTTP endpoints
- **flashback-test-util**: `FlashbackBaseTest` base class for integration tests
- **mitm**: Generic MITM proxy infrastructure (not Flashback-specific) - `ProxyServer`, SSL/TLS certificate generation, connection flow handling

### Key Concepts

**Scene**: Contains recorded HTTP request/response pairs stored as JSON. Supports two modes:
- `RECORD`: Intercepts and stores client requests and server responses
- `PLAYBACK`: Matches incoming requests against recorded scenes and returns responses

**MatchRule**: `BiPredicate<RecordedHttpRequest, RecordedHttpRequest>` interface for flexible request matching. Implementations include `MatchUri`, `MatchBody`, `MatchHeaders`, `MatchMethod`, and composite rules via `CompositeMatchRule`.

**ProxyModeController**: Interface with two implementations per connection:
- `RecordController`: Forwards requests to server, records request/response pairs
- `ReplayController`: Matches requests against scenes, returns recorded responses

### Request Flow

1. `FlashbackRunner` starts `ProxyServer` (Netty-based) configured with `ProxyModeControllerFactory`
2. For each client connection, a new `RecordController` or `ReplayController` is created
3. **Record mode**: Client request → RecordController → Server → RecordController (records response) → Client
4. **Playback mode**: Client request → RecordController → MatchScene → Return recorded response

### Serialization

Scenes are serialized to JSON using Jackson. Key classes:
- `SceneSerializer` / `SceneDeserializer`: Serialize/deserialize scenes to/from JSON files
- `RecordedHttpRequest` / `RecordedHttpResponse`: Serializable representations of HTTP messages
- `RecordedHttpExchange`: Pairs a request with its corresponding response

## Testing

Tests use **TestNG** (not JUnit). The `FlashbackBaseTest` class provides helper methods:
- `withMatchRule(MatchRule, Callable)`: Execute code with a specific match rule
- `withScene(String/SceneConfiguration, Callable)`: Execute code with a specific scene
- Override `flashbackTestClassSetUp()` to configure default scene/mode

## Important File Patterns

- Match rule implementations: `flashback-core-impl/src/main/java/com/linkedin/flashback/matchrules/`
- Proxy controllers: `flashback-smartproxy/src/main/java/com/linkedin/flashback/smartproxy/proxycontroller/`
- Netty mappers: `flashback-netty/src/main/java/com/linkedin/flashback/netty/`
- MITM proxy core: `mitm/src/main/java/com/linkedin/mitm/proxy/`

## Contribution Guidelines

Per CONTRIBUTING.md:
- All new features must include tests that pass
- Bug fixes must include a test case demonstrating the error it fixes
- Large features require opening an issue first for discussion
- Security vulnerabilities should be reported to security@linkedin.com (not filed on GitHub)