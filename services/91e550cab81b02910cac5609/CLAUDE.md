# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flashback is an HTTP/HTTPS mocking library for testing purposes. It records HTTP transactions and replays them later, enabling tests without external network connections. It supports partial matching via customizable match rules and can generate SSL certificates on the fly for HTTPS mocking.

## Build Commands

```bash
# Full build
./gradlew build

# Clean build artifacts
./gradlew clean

# Build without running tests
./gradlew build -x test

# Run all tests
./gradlew test

# Run tests for a specific module
./gradlew :flashback-core-impl:test

# Run a specific test class
./gradlew test --tests "*SceneAccessLayerTest"

# Run a specific test method
./gradlew test --tests "*SceneAccessLayerTest.testCanReplayScene"

# Start the admin REST API server
./gradlew :flashback-admin:startAdminServer --Args="-port 1234"

# Or use the startup script directly
./startAdminServer.sh -port 1234

# Generate IntelliJ IDEA project files
./gradlew idea
```

## Architecture

### Module Structure

- **flashback-core-impl**: Core functionality - Scene management, HTTP serialization/deserialization, MatchRule implementations
- **flashback-netty**: Netty HTTP message builders and response mappers for converting between Netty and internal HTTP representations
- **flashback-smartproxy**: Main proxy server entry point - FlashbackRunner, RecordController, ReplayController
- **mitm**: Man-in-the-middle infrastructure - Certificate generation, SSL/TLS handling, proxy connection flows
- **flashback-admin**: Rest.li-based admin API server for remote proxy control
- **flashback-test-util**: FlashbackBaseTest base class for integration tests
- **flashback-all**: Meta-project aggregating all dependencies

### Core Concepts

**Scene**: Container for recorded HTTP transactions. Created via SceneFactory from SceneConfiguration. Stores requests/responses in memory and optionally serializes to JSON files.

**SceneMode**: Four modes:
- `RECORD`: Records incoming requests and forward responses
- `PLAYBACK`: Matches requests against recorded scene and replays responses
- `SEQUENTIAL_RECORD`: Records in sequence, plays back in sequence
- `SEQUENTIAL_PLAYBACK`: Sequential matching without rules

**MatchRule**: Interface (`BiPredicate<RecordedHttpRequest, RecordedHttpRequest>`) for matching incoming requests to recorded ones. Implementations:
- `MatchUri`, `MatchMethod`, `MatchHeaders`, `MatchBody` - Single aspect matchers
- `CompositeMatchRule` - Combines multiple rules
- `MatchRuleWhitelistTransform`, `MatchRuleBlacklistTransform` - Filter fields for comparison

**FlashbackRunner**: Main proxy bootstrap class. Creates ProxyServer in record or replay mode with SSL support. Use the Builder pattern to configure:
```java
new FlashbackRunner.Builder()
    .mode(SceneMode.PLAYBACK)
    .sceneAccessLayer(new SceneAccessLayer(scene, matchRule))
    .host("localhost").port(5555)
    .certificateAuthority(certificateAuthority)
    .rootCertificateInputStream(certStream).rootCertificatePassphrase("changeit")
    .build()
```

**ProxyModeController**: Per-connection controller handling request/response flow. Two implementations:
- `RecordController`: Forwards requests to server, records response
- `ReplayController`: Matches request against scene, returns recorded response

### Key Classes

- `SceneAccessLayer`: Bridges FlashbackRunner with Scene; handles matching and playback
- `RecordedHttpRequest/Response`: Serializable HTTP messages stored in scenes
- `NettyHttpResponseMapper`: Converts RecordedHttpResponse to Netty FullHttpResponse
- `FlashbackAdminResource`: Rest.li resource exposing admin actions (startFlashback, changeScene, shutDownFlashback)
- `FlashbackBaseTest`: TestNG base class providing Flashback integration for tests

### Data Flow

1. Client connects to FlashbackRunner proxy
2. FlashbackRunner creates per-connection ProxyModeController (RecordController or ReplayController)
3. RecordController: Client request → Server → Response → Scene
4. ReplayController: Client request → Match against Scene via MatchRule → Return recorded Response or 400

### Important Notes

- **Test Framework**: Uses TestNG (`org.testng.annotations`), not JUnit
- **SSL Certificates**: HTTPS support requires CertificateAuthority configuration and root certificate with passphrase
- **Sensitive Data**: Scenes may contain API keys, tokens, secrets. Use match rule transformations to mask sensitive fields
- **Dependency Management**: TestNG is a `testCompile` dependency, not `compile`
- **Netty Version**: 4.0.27.Final - legacy Netty version
- **Contribution Requirements**: All new features must include tests; bug fixes must include a test case demonstrating the fix