# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ByteX is an Android bytecode optimization platform based on Android Gradle Transform API and ASM. It provides a plugin architecture where independent bytecode plugins can run separately or be automatically merged into a single Transform for efficiency.

## Build Commands

```bash
# Build all modules
./gradlew clean build

# Build without tests (faster)
./gradlew assemble

# Publish to local gradle_plugins directory (required after code changes)
./publish.sh

# Publish to Maven
./publish.sh -m

# Publish snapshot to Maven
./publish.sh -m -t

# Run tests
./gradlew test

# Debug a plugin (requires remote debug configuration in IDE)
./gradlew clean :example:assembleDouyinCnRelease -Dorg.gradle.debug=true --no-daemon
```

## Architecture

### Core Modules

- **base-plugin**: The ByteX host plugin that orchestrates all transformations
- **common**: Shared library with class graph building, logging, and plugin interfaces
- **TransformEngine**: Low-level engine for reading/writing class files with multi-threaded concurrent processing
- **GradleToolKit**: Gradle API abstractions for project/variant introspection
- **PluginConfig/PluginConfigProcessor**: Annotation-based plugin registration system
- **HookProguard**: ProGuard configuration hook and resolution

### Plugin Directory Structure

Each plugin is a separate module. Open-source plugins include:
- `access-inline-plugin`, `const-inline-plugin`, `getter-setter-inline-plugin`: Method/field inlining
- `shrink-r-plugin`: R file optimization
- `closeable-check-plugin`: Resource leak detection
- `refer-check-plugin`: Dead code/field reference checking
- `method-call-opt-plugin`: Method call optimization
- `SourceFileKiller`: Debug info stripping

### Plugin Development

**Creating a new plugin:**

1. Create a new module directory and `build.gradle` with:
   ```groovy
   apply from: rootProject.file('gradle/plugin.gradle')
   dependencies {
       compile project(':TransformEngine')
   }
   ```

2. Register plugin in `settings.gradle` with module name ending in `-plugin`

3. Create Extension class (configuration bean) extending `BaseExtension`

4. Create Plugin class extending `CommonPlugin<Extension, Context>`

5. Register via `@PluginConfig("bytex.pluginid")` annotation or `META-INF/gradle-plugins/bytex.pluginid.properties`

**Key plugin methods:**
```java
@Override
protected Context getContext(Project project, AppExtension android, Extension extension) {
    return new Context(project, android, extension);
}

@Override
public boolean transform(@Nonnull String relativePath, @Nonnull ClassVisitorChain chain) {
    chain.connect(new YourClassVisitor(extension));
    return true; // return false to delete the class
}

@Override
public boolean transform(@Nonnull String relativePath, @Nonnull ClassNode node) {
    // Alternative: work with ASM Tree API directly
    return true;
}
```

### TransformFlow

ByteX processes classes through `TransformFlow` pipelines. The default `MainTransformFlow` has three phases:
1. **traverse**: Analyze all class files (read-only)
2. **traverseAndroidJar**: Build class graph from Android SDK
3. **transform**: Modify and write class files

Plugins can customize the flow by overriding `provideTransformFlow()` for advanced use cases.

### Class Graph

When running in `MainTransformFlow`, plugins automatically get access to a complete class graph via `context.getClassGraph()`. This contains all class relationships from project classes, JARs, and Android SDK.

### Logging

Use `context.getLogger()` for plugin-specific logging. Logs are written to:
- `app/build/ByteX/${variantName}/${extension_name}/${logFile}`
- HTML report at `app/build/ByteX/ByteX_report_${transformName}.html`

## Configuration Properties (gradle.properties)

| Property | Description |
|----------|-------------|
| `bytex.enableHtmlLog` | Generate HTML report (default: true) |
| `bytex.enableRAMCache` | Enable memory cache for incremental builds (default: true) |
| `bytex.${extension}.alone` | Run plugin independently (default: false) |
| `bytex.globalIgnoreClassList` | File with classes to ignore on exception |

## Key Dependencies

- ASM: `9.2` (see `gradle/ext.gradle`)
- Gradle: `3.5.3`
- Kotlin: `1.3.21`
- Android Gradle Plugin: See `gradle/ext.gradle`

## Development Notes

- Branch management: Features merge to `develop` first, then `master`. Bugfixes can go directly to `master` then sync to `develop`.
- Module naming: lowercase with hyphens, end plugin modules with `-plugin`
- Package naming: `com.ss.android.ugc.bytex.${feature}`
- Comments: English preferred for core code