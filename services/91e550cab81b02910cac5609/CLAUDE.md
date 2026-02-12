# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flashback is an HTTP/HTTPS mocking proxy library for testing purposes. It records HTTP transactions ("scenes") and replays them, enabling tests to run without external network connections. It supports flexible request matching via customizable match rules and can generate SSL certificates on the fly for HTTPS mocking.

## Build Commands

```bash
# Build all projects
./gradlew build

# Run all tests (TestNG framework)
./gradlew test

# Run a specific test class
./gradlew test --tests "GzipCompressorTest"

# Run a specific test method
./gradlew test --tests "SceneAccessLayerTest.testCanReplayScene"

# Start the admin server
./gradlew startAdminServer -PArgs="--port 1234"

# Or using the wrapper script
./startAdminServer.sh --port 1234
```

## Architecture

### Module Structure

- **flashback-core-impl**: Core functionality including scene management, match rules, serialization, and HTTP decorators (compression, encoding)
- **flashback-netty**: Netty-based HTTP request/response builders and mappers for converting between Netty and Flashback domain objects
- **flashback-smartproxy**: Proxy controllers (RecordController, ReplayController) that implement the record/replay logic using SceneAccessLayer
- **flashback-admin**: Rest.li-based admin API (FlashbackAdminResource) for controlling the proxy remotely via HTTP
- **mitm**: Man-in-the-middle proxy infrastructure for HTTPS support, including SSL/TLS certificate generation via CertificateAuthority
- **flashback-test-util**: Testing utilities for integrating Flashback into test suites
- **flashback-all**: Meta project aggregating all dependencies

### Key Classes

- `SceneAccessLayer`: Central class for reading/writing HTTP exchanges to scenes and looking up matching recordings
- `FlashbackRunner`: Entry point that orchestrates the proxy; created via Builder with mode (RECORD/PLAYBACK), sceneAccessLayer, and SSL config
- `FlashbackAdminResource`: Rest.li resource exposing admin actions (startFlashback, changeScene, changeMatchRule, shutDownFlashback)
- `MatchRule` / `NamedMatchRule`: Interface and factory for request matching strategies (matchEntireRequest, matchSimpleUri, etc.)
- `Scene`: Represents a recorded HTTP transaction sequence with configuration (root path, mode, name)
- `CertificateAuthority`: Generates SSL certificates dynamically for HTTPS mocking

### Request Flow

1. Admin API receives startFlashback action with sceneMode, sceneName, matchRule, scenePath
2. FlashbackRunner is built and started, creating a MITM proxy server
3. In RECORD mode: requests pass through to real servers, responses are captured to scene
4. In PLAYBACK mode: requests are matched against scene using MatchRule, responses served from recorded data
5. Scenes are JSON-serialized via SceneWriter/SceneReader for persistence

### Scene Modes

- `RECORD`: Capture new HTTP transactions to memory, dump to disk on scene change/shutdown
- `PLAYBACK`: Serve responses from recorded scene only
- `SEQUENTIAL_PLAYBACK`: Serve responses in order from recorded scene
- `SEQUENTIAL_RECORD`: Record new responses sequentially while preserving existing ones