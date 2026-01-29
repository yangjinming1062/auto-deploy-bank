# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Build all modules
./gradlew build

# Build fat JAR with all dependencies (main desktop application)
./gradlew :desktop:fatJar
# Output: desktop/build/libs/PowerTunnel-<version>-all.jar

# Build SDK fat JAR
./gradlew :sdk:fatJar

# Build Core fat JAR
./gradlew :core:fatJar

# Run desktop application
./gradlew run

# Run tests
./gradlew test

# Run single test class
./gradlew :core:test --tests "ClassName"
```

## Project Architecture

PowerTunnel is a multi-module Gradle project (Java 8) implementing an extensible proxy server built on LittleProxy.

### Module Structure

- **sdk** - Plugin API for extending proxy functionality. Plugins implement `PowerTunnelPlugin` and register listeners via `registerProxyListener()`. Configuration is stored via `readConfiguration()`/`saveConfiguration()`.

- **core** - Main proxy server implementation. `PowerTunnel` class implements `PowerTunnelServer` interface and manages:
  - Plugin loading via `PluginLoader` (parses `plugin.ini` manifests)
  - Proxy server lifecycle (start/stop)
  - Listener registration with priority ordering
  - Configuration management

- **desktop** - Swing GUI application. Entry point is `Main.java` which:
  - Parses CLI arguments via `ArgumentParser`
  - Launches either `ConsoleApp` or `GraphicalApp`
  - Uses `ServerConfiguration` for settings
  - Supports system tray, native look-and-feel, and auto-proxy setup on Windows

- **littleproxy** - LittleProxy dependency wrapper (xyz.rogfam:littleproxy:2.0.5) with SSL/MITM support via LittleProxy-mitm

- **sample-plugin** - Example plugin demonstrating:
  - `onProxyInitialization()` hook
  - Request/response interception via `ProxyListener`
  - MITM certificate handling

### Key Classes

- `io.github.krlvm.powertunnel.PowerTunnel` - Core server implementation
- `io.github.krlvm.powertunnel.LittleProxyServer` - LittleProxy wrapper
- `io.github.krlvm.powertunnel.plugin.PluginLoader` - JAR plugin loader
- `io.github.krlvm.powertunnel.sdk.PowerTunnelServer` - Server interface for plugins
- `io.github.krlvm.powertunnel.sdk.proxy.ProxyListener` - Request/response interceptor interface
- `io.github.krlvm.powertunnel.sdk.plugin.PowerTunnelPlugin` - Base class for plugins

### Plugin System

Plugins are JAR files placed in the `plugins` directory. Each plugin must include `plugin.ini` manifest with:
```
id, version, versionCode, name, mainClass, targetSdkVersion
```

Plugins receive `PowerTunnelServer` instance via `attachServer()` and can intercept traffic by registering `ProxyListener` callbacks with optional priority values.