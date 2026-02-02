# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Build the all-in-one jar
./gradlew shadowJar

# Run all tests
./gradlew test

# Run a single test class
./gradlew test --tests "mirror.SyncLogicTest"

# Run a single test method
./gradlew test --tests "mirror.SyncLogicTest.handlesNewerRemoteUpdateWinning"

# Check for dependency updates
./gradlew dependencyUpdates
```

## Project Overview

Mirror is a two-way, real-time file synchronization tool for a desktop+laptop development workflow. It syncs files between machines while supporting IDE usage on the less powerful machine.

**Key components:**

- `Mirror.java` - CLI entry point using Airline; provides `server` and `client` commands
- `MirrorServer.java` - gRPC server that accepts client connections and manages sessions
- `MirrorClient.java` - gRPC client that connects to server and manages sync sessions
- `MirrorSession.java` - Core session logic; instantiated on both server and client after connection
- `SyncLogic.java` - Steady-state two-way sync diffing algorithm
- `UpdateTree.java` - In-memory tree tracking local and remote file metadata
- `FileWatcher.java` / `WatchmanFileWatcher.java` - Native file system event listeners

## Architecture

**Communication Layer (gRPC):**
- `mirror.proto` defines the service: `TimeCheck`, `InitialSync`, `StreamUpdates`, `Ping`
- Both sides run gRPC servers and clients simultaneously for bidirectional streaming
- Clients send session ID as first streaming message to identify which session on server

**Sync Flow:**
1. Initial sync: Both sides scan their files and exchange state
2. Steady state: FileWatcher detects changes → Queue → SyncLogic → Diff → SaveToLocal/SaveToRemote

**Threading Model:**
- `Queues` class holds three `BlockingQueue`s: `incomingQueue`, `saveToLocal`, `saveToRemote`
- `MirrorSession` runs multiple `TaskLogic` implementations in a `TaskPool`:
  - `FileWatcher` - watches for local file changes
  - `SyncLogic` - diffs trees and decides actions
  - `SaveToLocal` / `SaveToRemote` - writes files to disk or sends to remote
  - `QueueWatcher` - monitors queue overflow

**Conflict Resolution:**
- Modification time is the source of truth
- Newer modtime wins; deletes use preserved modtime to break ties
- Directory modtimes are intentionally ignored to prevent spam from child writes
- Last-write-wins for disconnected conflicts (no sophisticated merge)

**File Watching:**
- Prefers Watchman (Facebook's file watcher) when available
- Falls back to Java's `WatchService`
- Watchman provides more reliable inotify handling for large directories

**Key Files:**
- `src/main/proto/mirror.proto` - gRPC service definition
- `src/main/java/mirror/Update.java` - Protobuf message class for file updates
- `src/main/java/mirror/UpdateTree.java` - Dual local/remote metadata tracking
- `src/main/java/mirror/UpdateTreeDiff.java` - Compares local vs. remote states
- `src/main/java/mirror/PathRules.java` - `.gitignore` pattern matching