# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PacketProxy is a Java/Kotlin desktop application for intercepting and inspecting TCP/UDP network traffic. It supports multiple protocols beyond HTTP including HTTP/2, HTTP/3, QUIC, WebSocket, MQTT, gRPC, and more. The application provides a GUI for testing web applications and finding vulnerabilities.

## Build & Run Commands

```bash
# Build the project
./gradlew build

# Run all tests
./gradlew test

# Run a specific test class
./gradlew test --tests "packetproxy.common.StringUtilsTest"

# Run the application (requires display/GUI)
./gradlew run

# Check code formatting
./gradlew spotlessCheck

# Auto-fix code formatting
./gradlew spotlessApply
```

## Architecture

### Source Layout

- **src/main/java/core/packetproxy/** - Core Java source code (456 files)
- **src/main/kotlin/core/packetproxy/** - Kotlin source code (38 files)
- **src/test/java/** - JUnit tests for Java code
- **src/test/kotlin/** - JUnit tests for Kotlin code

### Key Packages

| Package | Purpose |
|---------|---------|
| `packetproxy.model` | Database-backed models using ORMLite (Server, Packet, ClientCertificate, Config, etc.) |
| `packetproxy.controller` | Application controllers (InterceptController, ResendController, PacketsController) |
| `packetproxy.encode` | Protocol encoders/decoders - extends `Encoder` abstract class |
| `packetproxy.gui` | Swing-based GUI components (GUIMain, GUIHistory, GUIOption*, etc.) |
| `packetproxy.extensions` | Optional extensions (RandomnessExtension, SampleEncoders) |
| `packetproxy.http/` `http2/` `http3/` | HTTP protocol implementations |
| `packetproxy.quic/` | QUIC protocol implementation |
| `packetproxy.websocket/` | WebSocket support |
| `packetproxy.common` | Utilities (Utils, StringUtils, ClientKeyManager, etc.) |

### Core Abstractions

**Encoder (encode/Encoder.java)**: Abstract base class for all protocol handlers. Implement `getName()`, `checkDelimiter()`, and encode/decode methods. Handles client-to-server and server-to-client message transformation.

**Extension (model/Extension.java)**: Base class for extensions that can provide custom panels and encoders. Extend and override `createPanel()` and `historyClickHandler()`.

**Server (model/Server.java)**: Database model representing upstream servers with IP, port, encoder selection, and SSL configuration.

**Proxy (Proxy.java)**: Base Thread class for handling proxy connections. Subclasses implement specific proxy behaviors.

### Database

Uses SQLite via ORMLite for persistence. Key tables: servers, packets, client_certificates, configs, extensions, listen_ports, modifications, filters.

### UI Framework

Swing-based GUI with FlatLaf look and feel. Main entry point is `packetproxy.PacketProxy` which launches `GUIMain`.

## Code Style

- **Java**: Google Java Format (configured via Spotless)
- **Kotlin**: ktfmt with Google style
- **Encoding**: UTF-8 for all files
- **License**: Apache License 2.0 - include license header on new files

## Testing

Tests use JUnit Jupiter. Test files follow naming convention `*Test.java`. Run individual tests with `--tests "package.path.ClassName"`.

## Contribution Notes

- No strict coding style guidelines required
- All contributions require signing the DeNA CLA before merge
- Submit pull requests for any improvements