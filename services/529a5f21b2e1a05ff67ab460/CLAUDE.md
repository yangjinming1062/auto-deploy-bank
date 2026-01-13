# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **Liferay Portal** repository - a Java-based enterprise portal platform. It's a large enterprise application with a modular OSGi-based architecture, containing approximately 1000+ modules spanning various features (commerce, analytics, content management, collaboration, etc.).

## High-Level Architecture

### Core Components

- **portal-kernel**: Core portal APIs and interfaces (public contracts)
- **portal-impl**: Core portal implementation (private business logic)
- **portal-web**: Web layer and servlets (JSPs, servlets, web utilities)
- **modules/apps/**: Application modules (portlets, services, UI components)
- **modules/core/**: Framework and foundation modules
- **modules/frontend/**: Frontend-related modules (JS, CSS, themes)

### Module Types

Modules follow OSGi bundle conventions with these common patterns:

- **`*-api`**: Public API contracts (interfaces)
- **`*-impl`**: Implementation classes (service builders, business logic)
- **`*-web`**: Web layer (portlets, taglibs, controllers)
- **`*-test`**: Test modules (integration/unit tests)
- **`*-service`**: Service layer modules

Each module has:
- `build.gradle`: Gradle build configuration (inherits from `build-portal.gradle`)
- `bnd.bnd`: OSGi bundle descriptor (metadata, imports, exports, version)
- `src/`: Java source code

### Workspaces

The `/workspaces/` directory contains reference implementations and example projects:
- **liferay-sample-workspace**: Basic development workspace
- **liferay-marketplace-workspace**: Marketplace application example
- Other workspaces for specific features (commerce integrations, payment gateways)

Workspaces use the Liferay Workspace Gradle plugin and support client extensions.

## Build System

### Primary Build Tool: ANT

The main build system uses **Ant** (not Gradle) for portal compilation:

```bash
# Main build targets
ant clean          # Clean build artifacts
ant compile        # Compile portal and modules
ant all            # Full build: compile + deploy + package
ant jar            # Build JAR artifacts
ant deploy         # Deploy to app server
ant dist           # Create distribution
ant test           # Run tests
```

### Module Build System: Gradle

Individual modules use **Gradle** for building:

```bash
# From a module directory
./gradlew build                    # Build the module
./gradlew deploy                   # Deploy to Liferay home
./gradlew clean                    # Clean build artifacts
./gradlew compileJava -DcompileJava.lint=deprecation,unchecked  # Compile with warnings
```

### Gradle Workspaces

For workspace development:

```bash
# From a workspace directory
./gradlew build                    # Build all modules
./gradlew deploy                   # Deploy all modules
./gradlew initBundle              # Initialize Liferay bundle
./gradlew createToken              # Create auth token for remote deployment
```

### Java Version Requirements

- **Portal Source**: Java 7 compatibility by default (Java 8 features opt-in)
- **Modules**: To use Java 8 features, add to `build.gradle`:
  ```gradle
  sourceCompatibility = "1.8"
  targetCompatibility = "1.8"
  ```

### Node.js Frontend Build

Many modules use Node.js for frontend builds (React components, Sass compilation, bundling):

```bash
# In module with package.json
npm run build          # Build frontend assets
npm run format         # Format code (Prettier)
npm run checkFormat    # Check code formatting

# Or using node-scripts
node-scripts build
node-scripts format
```

Package managers:
- **Yarn**: Primary package manager (configured in workspace properties)
- **npm**: Alternative

## Testing

### Test Types

- **Unit Tests**: `-test` modules with `test/` directories
- **Integration Tests**: `portal-test/` directory
- **ServiceBuilder Tests**: Tests for generated services

### Running Tests

```bash
# Portal-wide tests
ant test                        # Run portal tests
ant compile-test               # Compile tests

# Module tests (from module directory)
./gradlew test                 # Run unit tests
./gradlew testIntegration      # Run integration tests
./gradlew check                # Run all checks
```

### Testing Tools

- **Jest**: For JavaScript/React component tests (in frontend modules)
- **JUnit**: For Java unit tests
- **Poshi**: Liferay's integration testing framework (in workspaces)

## Development Environment

### Required Tools

- **Java 8+** (for development; portal supports Java 7 compatibility)
- **Ant 1.10+** (main build system)
- **Gradle 8.5+** (module builds)
- **Yarn** or **npm** (frontend builds)
- **Node.js** (for frontend development)

### IDE Support

- **Liferay Dev Studio**: Official IDE (Eclipse-based)
- **IntelliJ IDEA**: With Liferay plugin
- **Visual Studio Code**: With extensions

### Server Configuration

The build system uses these properties (in `build.properties`, `app.server.properties`):

```properties
app.server.type=tomcat                    # Application server type
app.server.portal.dir=/path/to/portal     # Portal deployment directory
liferway.home=/path/to/liferay-home       # Liferay home directory
```

## Code Style and Conventions

### Java Code Style

- **Source Formatter**: Liferay's custom source formatter (see `/source-formatter.properties`)
- **Imports**: Sorted and organized by groups (static, java, javax, com.liferay, etc.)
- **Copyright**: Header template in `copyright.txt`
- **Package Naming**: Reverse domain (`com.liferay.portal.kernel.*`)

### Gradle Files

- Use **double quotes** (unless single quotes required)
- **No `def` for local variables** - use explicit types
- **Sort dependencies alphabetically** within configurations
- **Order**: buildscript → apply plugins → ext → initialization → tasks → properties
- **Configuration-based dependencies**: Unit tests → `testCompile`, integration tests → `testIntegrationCompile`

### Module Marker Files

Special marker files control module behavior:

| File | Purpose |
|------|---------|
| `.lfrbuild-portal` | Include in `ant all` build |
| `.lfrbuild-portal-private` | Deploy to private branch |
| `.lfrbuild-portal-public` | Deploy to public branch |
| `.lfrbuild-static` | Deploy to `osgi/static` |
| `.lfrbuild-tool` | Deploy to `tools/` directory |
| `.lfrbuild-app-server-lib` | Deploy to `WEB-INF/lib` |

See `/modules/README.md` for complete list.

### JavaScript/TypeScript

- **Linting**: ESLint with `@liferay/eslint-plugin` (version 1.6.0)
- **Formatting**: Prettier (version 3.2.5) with `@liferay/prettier-plugin`
- **Styling**: Stylelint with `@liferay/stylelint-plugin`

```bash
# Format all frontend code
npm run format

# Check formatting
npm run checkFormat
```

## OSGi and Bundle Development

### Bundle Structure

OSGi bundles are built using **BND tools**:

- **Export-Package**: Controls which packages are exported from the bundle
- **Import-Package**: Declares dependencies on other bundles
- **Private-Package**: Packages included but not exported
- **Bundle-Version**: Semantic versioning (see marker files)

### ServiceBuilder

Many modules use ServiceBuilder for CRUD operations:

- **`service.xml`**: Service definition (entities, columns, relationships)
- **Generated code**: Service stubs, persistence layer, finders
- **Location**: Typically in `*-service` modules

## Deployment

### Deploy Directories

- **OSGi Modules**: `${liferay.home}/osgi/portal` (default)
- **Static Bundles**: `${liferay.home}/osgi/static`
- **App Server Libraries**: `${app.server.portal.dir}/WEB-INF/lib`
- **Themes**: `${liferay.home}/osgi/portal-war`
- **Deploy Folder**: `${liferay.home}/deploy` (plugins, LAR files)

### Building for Production

```bash
# Full production build
ant all clean

# Build specific modules
ant -Dmodule.name=module-path all

# Build with profile
ant all -Dbuild.profile=dxp
```

## Configuration Files

Key configuration files:

- **`build.xml`**: Main Ant build file
- **`build-common.xml`**: Shared build logic
- **`build.properties`**: Build properties and paths
- **`bnd.bnd`**: OSGi bundle descriptor (in modules)
- **`source-formatter.properties`**: Code style rules
- **`app.server.properties`**: Application server paths
- **`gradle.properties`** (in workspaces): Workspace configuration

### Common Build Properties

```properties
# In build.properties
build.profile=portal                    # Build profile (portal/dxp)
app.server.type=tomcat                  # App server type
parallel.thread.count=4                 # Parallel build threads
database.type=hypersonic                # Database type
```

## Resources and Documentation

- **Portal Documentation**: https://portal.liferay.dev/
- **Modules README**: `/modules/README.md`
- **Workspace Plugin**: `/modules/sdk/gradle-plugins-workspace/README.md`
- **Contributing Guide**: `/CONTRIBUTING.md`
- **Liferay Community**: https://liferay.dev/

## Common Development Workflows

### 1. Create a New Module

```bash
# Use Blade CLI or create manually
mkdir -p modules/apps/my-app/my-app-api
mkdir -p modules/apps/my-app/my-app-impl
mkdir -p modules/apps/my-app/my-app-web

# Add build.gradle, bnd.bnd, and source code
# Add .lfrbuild-portal marker file if needed
```

### 2. Add ServiceBuilder to Module

```xml
<!-- my-app-service/service.xml -->
<entity name="MyEntity" local-service="true" remote-service="true">
  <column name="entityId" type="long" primary="true" />
  <column name="name" type="String" />
</entity>
```

### 3. Fix Build Errors

```bash
# Clean and rebuild
ant clean
ant compile

# Or for specific module
cd modules/apps/my-app
./gradlew clean build
```

### 4. Run Portal Locally

```bash
# Build and deploy
ant all

# Start app server (configured in app.server.properties)
# Tomcat: ${app.server.tomcat.dir}/bin/catalina.sh run
```

## Key Architecture Patterns

1. **Modular OSGi**: Dynamic module loading and dependency management
2. **ServiceBuilder**: CRUD service generation with persistence
3. **MVC Pattern**: Portlets follow Model-View-Controller
4. **API/Impl Separation**: Clean separation between public APIs and implementations
5. **Frontend Bundling**: Node.js-based asset compilation and bundling
6. **Theme System**: Extensible theming with Freemarker and Sass

## Notes

- This is a **large-scale enterprise application** (500k+ LOC)
- **Backward compatibility** is critical - many deprecated APIs remain supported
- **Semantic versioning** is enforced for public APIs (see marker files)
- **Cross-module dependencies** should use APIs, not implementations
- **Performance testing** is integrated with Testray integration
- **CI/CD**: Jenkins builds on merge, with various test suites

## Quick Reference

```bash
# Most common commands
ant clean              # Clean everything
ant compile            # Compile portal
ant all                # Full build (compile + deploy)
./gradlew :modules:apps:my-app:build  # Build specific module
./gradlew deploy       # Deploy to Liferay home
npm run format         # Format frontend code
```