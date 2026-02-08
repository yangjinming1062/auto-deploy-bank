# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LifePhoton (FUNGA) is a Ktor-based Kotlin web application for gene function annotation using AI. The platform integrates cross-species genetic information for analysis.

**Tech Stack:**
- Kotlin 2.1.0 with Ktor 3.0.3 server framework
- PostgreSQL database with Ktorm ORM
- Gradle multi-module build system

## Build Commands

```bash
# Build the entire project
./gradlew build

# Build without running tests
./gradlew build -x test

# Run all tests
./gradlew test

# Run tests for a specific module
./gradlew :module:authentication:test

# Run the application (uses Booster as entry point)
./gradlew run

# Create shadow JAR (fat JAR with all dependencies)
./gradlew shadowJar

# Run in development mode
./gradlew run -Pdevelopment
```

## Architecture

### Plugin System

The application uses a plugin-based architecture where each module registers itself as a plugin:

1. **Plugin Definition**: Extend `Plugin` class and mark with `@AutoUse` annotation
   - Location: `module/*/src/main/kotlin/cn/revoist/lifephoton/module/<name>/<Name>.kt`
   - Example: `Homepage : Plugin()` with `@AutoUse` annotation

2. **Route Registration**: Two patterns available:

   **RoutePage pattern** (standalone endpoints):
   ```kotlin
   @AutoRegister("<plugin-id>")
   object Login : RoutePage("path", auth, inject) {
       override fun methods(): List<HttpMethod> = listOf(HttpMethod.Post)
       override suspend fun onPost(call: RoutingCall) { ... }
   }
   ```

   **RouteContainer pattern** (class-based routing):
   ```kotlin
   @RouteContainer("<plugin-id>", "<root-path>")
   object Views {
       @Route(GET, path = "/custom", auth = true)
       suspend fun methodName(call: RoutingCall) { ... }
   }
   ```

3. **Annotations**:
   - `@AutoUse`: Auto-loads the plugin at startup
   - `@AutoRegister(pluginId)`: Registers a RoutePage
   - `@RouteContainer(pluginId, rootPath)`: Groups routes under a common path
   - `@Route(method, path, auth, inject)`: Marks methods as HTTP endpoints

4. **Bootstrapping**: Entry point is `Booster.kt` in `common` module
   - Uses Reflections library to scan for annotated classes
   - Auto-discovers routes in `cn.revoist.lifephoton` package

### Module Structure

```
module/
├── common/           # Shared plugin framework, routing, data utilities
├── authentication/   # User auth, sessions, permissions, messaging
├── file-management/  # File upload/download handling
├── genome/           # Genome data services
├── mating-type-imputation/  # MTI analysis module
├── funga/            # FUNGA AI gene mining (core module)
├── homepage/         # Landing page
├── ai-assistant/     # AI assistant integration
├── fungi-pattern/    # Fungal pattern analysis
└── tester/           # Testing utilities
```

### Request Flow

1. Request hits Ktor server on port 8080
2. `Booster.pluginLoad()` scans for `@AutoRegister` and `@RouteContainer` classes
3. Routes are registered at `/<plugin-id>/<path>`
4. Event system (`EventBus`) handles lifecycle events

### Database

- PostgreSQL with Ktorm ORM
- Connection configured via `application.yaml`
- Use `Booster.database` for direct database access
- Plugin data managers: `plugin.dataManager.useDatabase(dbName)`

## Key Files

- `common/src/main/kotlin/cn/revoist/lifephoton/Booster.kt`: Application bootstrap
- `common/src/main/kotlin/cn/revoist/lifephoton/plugin/Plugin.kt`: Base plugin class
- `common/src/main/kotlin/cn/revoist/lifephoton/plugin/route/Route.kt`: Route annotations
- `src/main/resources/application.yaml`: Server configuration

## Configuration

Config files follow YAML format. Place in:
- `src/main/resources/application.yaml` (server config)
- `<module>/src/main/resources/` (module-specific config)

Access via `loadConfig("name")` or plugin's `getConfig(key, default)`.