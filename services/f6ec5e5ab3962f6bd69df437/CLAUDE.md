# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

IQQ is a desktop QQ (Tencent QQ) instant messaging client written in Java. It's a multi-module Maven project with a modular architecture featuring a clean separation between API definitions, UI, and protocol implementations.

## Repository Structure

- **api/** - API module defining IM interfaces, bean objects, and event system
- **main/** - Main application code containing UI layer, services, and business logic
- **bridge-webqq/** - WebQQ protocol implementation following a bridge pattern
- **skin-default/** - Default UI skin resources
- **resources/** - Application resources (icons, screenshots, i18n bundles)
- **pom.xml** - Root Maven POM with multi-module configuration

## Architecture

### Core Architecture

The application uses **Spring Framework** for dependency injection with annotation-based configuration:

- **Entry Point**: `main/src/main/java/iqq/app/IMLauncher.java:32` - Initializes Spring context and shows login frame
- **Context Management**: `main/src/main/java/iqq/app/core/context/IMContext.java:30` - Singleton providing access to Spring ApplicationContext
- **Spring Configuration**: `main/src/main/resources/spring-config.xml:8` - Component scanning for `iqq.app` package

### Design Patterns

1. **Bridge Pattern** - Protocol implementations are separated from the main application via bridge modules (see `bridge-webqq/src/main/resources/bridge.xml:2`)

2. **Service Layer** - Core services in `main/src/main/java/iqq/app/core/service/`:
   - `EventService` - Event management
   - `I18nService` - Internationalization
   - `SkinService` - UI theming
   - `ResourceService` - Resource management
   - `TaskService` - Background task handling

3. **Query Layer** - Data access queries in `main/src/main/java/iqq/app/core/query/`:
   - `BuddyQuery` - Friend list operations
   - `GroupQuery` - Group operations
   - `AccountQuery` - Account management
   - `MsgQuery` - Message operations

4. **Module Pattern** - Business logic modules in `main/src/main/java/iqq/app/core/module/LogicModule.java:23`

### UI Architecture

- **Framework**: Swing-based desktop UI with WebLaF (Web Look and Feel) library
- **Main Window**: `main/src/main/java/iqq/app/ui/IMFrame.java:28`
- **UI Management**: `main/src/main/java/iqq/app/ui/manager/FrameManager.java`
- **Event System**: UI events in `main/src/main/java/iqq/app/ui/event/`
- **Actions**: User actions in `main/src/main/java/iqq/app/ui/action/`

### API Module

The `api/` module defines the core interfaces and data structures:

- **Beans**: `api/src/main/java/iqq/api/bean/` - IMEntity, IMUser, IMBuddy, IMRoom, IMMsg, etc.
- **Events**: `api/src/main/java/iqq/api/event/` - IMEvent, IMEventDispatcher, IMEventListener
- **Content Types**: `api/src/main/java/iqq/api/bean/content/` - Message content items (text, images, faces)

### Protocol Bridge

The `bridge-webqq/` module implements WebQQ protocol:

- **Bridge Factory**: `bridge-webqq/src/main/java/iqq/bridge/IMBridgeFactory.java`
- **Implementation**: `bridge-webqq/src/main/java/iqq/bridge/webqq/WebQQBridge.java`
- **Configuration**: `bridge-webqq/src/main/resources/bridge.xml:5`
- **External Dependency**: Uses `webqq-core` library (version 1.2-SNAPSHOT)

## Common Development Tasks

### Building the Project

```bash
# Build all modules
mvn clean package

# Build only specific module
mvn clean package -pl api -am
mvn clean package -pl main -am
mvn clean package -pl bridge-webqq -am
```

### Running the Application

After building:
```bash
java -jar main/target/iqq-main-3.0.0-SNAPSHOT-jar-with-dependencies.jar
```

Or from the project root:
```bash
java -cp main/target/iqq-main-3.0.0-SNAPSHOT-jar-with-dependencies.jar iqq.app.IMLauncher
```

### Running Tests

```bash
# Run all tests
mvn test

# Run tests for specific module
mvn test -pl main

# Run a specific test class
mvn test -pl main -Dtest=ClassName
```

### Dependency Management

The project uses both Maven dependencies and local JARs:

- **Maven Dependencies**: Declared in POM files (Spring 4.0.5, Logback, MapDB, etc.)
- **Local Libraries**: Required JARs stored in `main/lib/`:
  - `weblaf-1.29.jar` - UI look and feel
  - `jhrome-2.0.jar` - Browser component

These local libraries are referenced in `main/pom.xml:46` with `systemPath` scope.

## Key Configuration Files

- **pom.xml** - Multi-module Maven configuration, main class: `iqq.app.IMLauncher`
- **main/config.xml** - Application configuration (location in `main/config.xml`)
- **main/src/main/resources/spring-config.xml** - Spring component scanning
- **main/src/main/resources/logback.xml** - Logging configuration
- **resources/i18n/** - Internationalization bundles (appBundle.properties, appBundle_zh_CN.properties)
- **.gitignore** - Git ignore rules

## Dependencies

### Core Dependencies (from pom.xml)
- **Spring Framework** 4.0.5.RELEASE - Dependency injection
- **WebLaF** 1.29 (local) - UI look and feel
- **Jhrome** 2.0 (local) - Browser component
- **Logback** 1.0.13 - Logging
- **Nutz** 1.b.49 - Utility framework
- **MapDB** 0.9.8 - Embedded database
- **XStream** 1.4.8 - XML serialization
- **Pinyin4J** 2.5.0 - Chinese pinyin support

### External Modules
- **webqq-core** 1.2-SNAPSHOT - WebQQ protocol core library (from GitHub: im-qq/webqq-core)

## Version Information

- **Project Version**: 3.0.0-SNAPSHOT
- **Java Version**: 1.8 (source/target in pom.xml:132-133)
- **Build Tool**: Maven 3.x

## Development Notes

1. **UI Thread**: The application uses Swing, so UI updates must be on the Event Dispatch Thread (see `IMLauncher.java:33`)

2. **Internationalization**: UI strings are externalized to properties files in `resources/i18n/` with Chinese (zh_CN) and default bundles

3. **Event System**: The application uses a custom event system (see `api/src/main/java/iqq/api/event/IMEventDispatcher.java`)

4. **Shutdown Handling**: Graceful shutdown hook is registered in `IMLauncher.java:58`

5. **Application Directory**: Set via `app.dir` system property in `IMLauncher.java:49`

6. **Resource Loading**: Resources and skins are copied to classpath during build (see `pom.xml:116-124`)

7. **Data Storage**: Uses MapDB for embedded data storage (see `main/src/main/java/iqq/app/core/store/IMDataStore.java`)

## Testing

Test sources are located in:
- `main/src/test/java/` - Unit tests for main module
- `bridge-webqq/src/main/java/iqq/bridge/test/` - Tests for WebQQ bridge

The project uses JUnit 4.10 for testing.

## Related Repositories

- **IQQ UI**: https://github.com/im-qq/iqq.git
- **IQQ Core**: https://github.com/im-qq/webqq-core.git
- **Original Project**: https://code.google.com/p/iqq/