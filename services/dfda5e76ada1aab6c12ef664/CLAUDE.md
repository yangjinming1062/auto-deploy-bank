# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**IntelliJ as a Service (ijaas)** - An IntelliJ IDEA plugin that runs a TCP server providing Java autocompletion and linting for Vim. This is a Google 20% project (not an official Google product).

## Build Commands

```bash
# Build plugin ZIP (outputs to build/distributions/ijaas-*.zip)
./gradlew buildPlugin

# Run a test IntelliJ instance with the plugin
./gradlew runIdea

# Specify IntelliJ version
./gradlew buildPlugin -Pintellij.version=IC-2017.2.6

# Run with custom port (for testing)
./gradlew runIdea -Dijaas.port=5801
```

## Development Workflow

To test changes, run two separate IntelliJ instances:
1. Primary development: `./gradlew runIdea`
2. Testing instance: `./gradlew buildPlugin && install plugin from dist/*.zip in primary IntelliJ`

Connect Vim with: `USE_DEV_IJAAS=1 IJAAS_PORT=5801 vim`

## Architecture

### Two Components

**IntelliJ Plugin (Java)** - `src/com/google/devtools/intellij/ijaas/`
- `IjaasServer.java`: TCP server (default port 5800, configurable via `-Dijaas.port`) handling JSON-RPC style requests
- `IjaasHandler.java`: Interface for request handlers
- `BaseHandler.java`: Abstract base class handling background thread execution and 10-second timeout
- `IjaasStartupActivity.java`: Plugin entry point via `postStartupActivity` extension
- Handlers in `handlers/` package process specific RPC methods

**Vim Plugin (VimScript)** - `vim/`
- `autoload/ijaas.vim`: Core functions (`ijaas#complete`, `ijaas#buf_write_post`, `ijaas#organize_import`)
- `ftplugin/java/ijaas.vim`: Sets up `omnifunc=ijaas#complete` and `:OrganizeImport` command

### Request/Response Protocol

JSON-RPC style: `[request_id, {"method": "...", "params": {...}}]` → `[request_id, {"result": ...}]`

### RPC Methods

| Method | Handler | Purpose |
|--------|---------|---------|
| `echo` | EchoHandler | Test echo |
| `java_complete` | JavaCompleteHandler | Code completion via IntelliJ API |
| `java_src_update` | JavaSrcUpdateHandler | Run inspections, return problems |
| `java_get_import_candidates` | JavaGetImportCandidatesHandler | Suggest import statements |

### Key Patterns

- Handlers extend `BaseHandler<ReqT, ResT>` for background execution and timeout handling
- `JavaCompleteHandler` uses `CodeCompletionHandlerBase` and extracts `LookupElement` items
- `JavaSrcUpdateHandler` combines `CodeSmellDetector` + `InspectionEngine` for linting
- Vim connects via channel expression (`ch_open`), sends JSON, parses response

## Code Style

Google Java Format is enforced via `google-java-format` plugin.