# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the **Ktor Samples** repository - a collection of 35+ independent sample projects demonstrating various features of the [Ktor framework](https://ktor.io). Each sample is a standalone application showcasing different capabilities like WebSockets, client usage, database integration, deployment options, and more.

## Project Structure

The repository is organized into thematic subdirectories:

- **Applications** (`/chat`, `/fullstack-mpp`, `/httpbin`, `/kweet`, `/reverse-proxy`, `/reverse-proxy-ws`, `/youkube`, `/version-diff`, `/postgres`, `/mongodb`, `/mvc-web`, `/opentelemetry`) - Full-featured applications
- **Server** (`/di-kodein`, `/filelisting`, `/location-header`, `/sse`, `/structured-logging`, `/openapi`) - Server-side features
- **Client** (`/client-mpp`, `/client-multipart`, `/client-tools`, `/client-native-image`) - Client-side usage
- **Deployment** (`/graalvm`, `/native-image-server-with-yaml-config`, `/maven-google-appengine-standard`) - Deployment and packaging
- **Testing** (`/jwt-auth-tests`) - Testing strategies

Each sample is independently buildable and testable with its own `build.gradle.kts` or `pom.xml`.

## Common Commands

### Building and Testing

```bash
# Build and test ALL samples (requires JDK 24)
./build-all.sh

# For a specific Gradle-based sample
cd <sample-directory>
./gradlew clean check --console=plain

# For Maven-based samples (maven-google-appengine-standard)
cd maven-google-appengine-standard
./mvnw clean test
# or
mvn clean test

# Run a specific sample
./gradlew run
```

Each sample directory contains a `README.md` with specific run instructions and dependencies. Many samples require additional setup:

- **Database samples** (`postgres`, `mongodb`) - Require Docker for database containers
- **Multiplatform samples** (`client-mpp`, `fullstack-mpp`) - Require Android SDK for Android builds, Xcode for iOS builds
- **Native image samples** (`graalvm`, `native-image-server-with-yaml-config`, `client-native-image`) - Require GraalVM installation

### Linting

Detekt is configured via `.github/workflows/detekt-analysis.yml` for static analysis:

```bash
# Run Detekt locally (download from v1.15.0 release)
detekt --input <directory-path>
```

### Development Dependencies

- **JDK 24** - Required for building all samples
- **Gradle** - Most samples use Gradle wrapper (`./gradlew`)
- **Docker** - Required for database samples (`postgres`, `mongodb`)
- **Android SDK** - For Android builds in multiplatform samples
- **Xcode** - For iOS builds in multiplatform samples
- **GraalVM** - For native image samples

## Architecture Patterns

Each sample demonstrates specific Ktor patterns:

- **Modular Design**: Each sample is self-contained with clear separation of concerns
- **Multiplatform Support**: Several samples use Kotlin Multiplatform for shared code across JVM/JS/Native
- **Server Architecture**: JVM-based server applications using Netty or other engines
- **Client Architecture**: HTTP/WebSocket clients for various platforms (JVM, JS, Android, iOS)
- **Database Integration**: Samples integrate with PostgreSQL, MongoDB using various ORMs
- **Template Engines**: Some samples use FreeMarker for server-side rendering
- **Sessions & Authentication**: Samples demonstrate session management and JWT authentication
- **Testing**: Samples include integration tests using `ktor-server-test-host`

## Key Build System Details

- **Kotlin Version**: 2.2.21
- **Ktor Version**: 3.3.3 (via BOM)
- **Default JVM Toolchain**: JDK 17 for compilation
- **Build Script**: Each Gradle project uses the Kotlin DSL (`build.gradle.kts`)
- **Packaging**: Most samples produce executable JARs or run directly via `./gradlew run`

## Sample Selection Guide

When working with samples, consider:

1. **For Server Development**: Look in the `/server` or `/applications` directories
2. **For Client Development**: Check `/client` directory, especially `client-mpp` for multiplatform
3. **For Deployment**: Review `/deployment` samples for GraalVM and App Engine options
4. **For Database**: `postgres` and `mongodb` samples show different persistence approaches
5. **For WebSockets**: `chat` and `reverse-proxy-ws` demonstrate real-time communication
6. **For Testing**: `jwt-auth-tests` shows test strategies for secured endpoints

## Important Notes

- Each sample is independent - changes don't affect other samples
- Samples are arranged by complexity: start with simpler ones like `filelisting` before complex ones like `youkube`
- Many samples use different Ktor plugins and features - check the `build.gradle.kts` for dependencies
- Some samples may have platform-specific requirements (macOS for iOS, Docker for databases)
- All samples use the same Ktor version via the BOM for consistency