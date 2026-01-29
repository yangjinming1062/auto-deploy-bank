# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

IQQ is a Java 8 desktop QQ client application using WebQQ protocol. The project follows a multi-module Maven structure with clear separation between API, core logic, protocol implementation, and UI.

## Build Commands

```bash
# Compile the project
mvn clean compile

# Build JAR with dependencies (main entry point: iqq.app.IMLauncher)
mvn package

# Run tests
mvn test
```

## Architecture

### Multi-Module Structure
- **api/**: Public interfaces and data beans (IMEvent, IMEventType, IMBridge, entity beans)
- **main/**: Core application - services, UI components, business logic
- **bridge-webqq/**: WebQQ protocol adapter connecting api to webqq-core library
- **skin-default/**: UI skin resources
- **resources/**: Application resources (icons, i18n files)

### Event-Driven Architecture

The app uses two parallel event systems that route events to annotation-marked handlers:

1. **IM Events** (protocol-level): `IMEventDispatcher` routes events annotated with `@IMEventHandler(IMEventType.XXX)`
2. **UI Events** (user interface): `UIEventDispatcher` routes events annotated with `@UIEventHandler(UIEventType.XXX)`

Both dispatchers use reflection to automatically find handler methods and invoke them when matching events are broadcast via `EventService.broadcast()`.

### Dependency Injection

- Spring Framework handles bean management via component scan (`@Configuration @ComponentScan("iqq.app")` in IMLauncher)
- Access beans via `IMContext.getBean(Class)` - returns Spring-managed singleton instances
- Services annotated with `@Service` are auto-discovered
- `@IMModule` and `@IMService` are custom marker annotations (primarily for documentation)

### Bridge Pattern

- `IMBridge` interface defines protocol-agnostic operations
- `WebQQBridge` implements this interface using webqq-core library
- `IMBridgeFactory` instantiates the bridge (currently defaults to TestBridge; swap to WebQQBridge for real QQ functionality)

### UI Layer

- Swing-based with WebLaF look-and-feel library
- `FrameManager` handles window lifecycle (login, verify frames)
- UI components under `ui/frame/panel/` organized by feature (chat, login, main)
- UI events broadcast through `EventService` to communicate with backend modules

### Data Flow

1. UI components fire `UIEvent` via `EventService.broadcast()`
2. `LogicModule` (Service) receives UI events and converts to `IMEvent`
3. `IMBridge` (WebQQBridge) handles IM events and communicates with webqq-core
4. Responses flow back through the chain to update UI

## Key Dependencies

- **webqq-core** (iqq.im): External library handling WebQQ protocol details
- **WebLaF**: Look and feel for Swing components
- **Jhrome**: Chromium-based embedded browser (for embedded content)
- **MapDB**: Embedded database for caching
- **NutZ**: Utility framework
- **Spring 4.0.5**: Dependency injection