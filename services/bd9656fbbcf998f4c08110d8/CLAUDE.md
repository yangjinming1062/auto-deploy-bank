# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Swagger Core is a Java implementation of the OpenAPI Specification (versions 3.0 and 3.1). It provides libraries to generate OpenAPI specifications from JAX-RS annotations and includes both standard `javax` and `jakarta` namespace support (with `-jakarta` suffixed artifacts).

Current version: 2.2.42-SNAPSHOT
Target Java: 11+ (compile target: Java 8)
Build tool: Apache Maven 3.0.4+

## Common Commands

### Build & Test
```bash
# Initial setup (first time only)
mvn -N

# Build and install all modules
mvn install

# Run tests
mvn test

# Run tests for a specific module
cd modules/swagger-core
mvn test

# Run a single test class
mvn test -Dtest=ModelResolverTest

# Run tests with coverage
mvn clean test

# Build without running tests
mvn clean install -DskipTests

# Run security checks
mvn clean install -Psecurity

# Run all checks including dependency convergence
mvn clean install
```

### Module-Specific Testing
```bash
# Test a specific module
cd modules/swagger-core && mvn test

# Test with verbose output
mvn test -X

# Run integration tests (failsafe)
mvn verify
```

### Documentation
```bash
# Generate Javadoc
mvn javadoc:javadoc

# Generate site
mvn site
```

### IDE Integration
- Import as Maven project in IntelliJ IDEA or Eclipse
- Java 11+ required in IDE
- Maven wrapper not included, use system Maven

## Architecture & Module Structure

### Core Modules

**swagger-annotations** (`modules/swagger-annotations/`)
- OpenAPI annotation definitions
- Java 8 source set
- Used by all other modules

**swagger-models** (`modules/swagger-models/`)
- POJO model classes representing OpenAPI specification
- Includes `OpenAPI`, `Operation`, `Components`, etc.
- Located in `io.swagger.v3.oas.models.*`

**swagger-core** (`modules/swagger-core/`)
- Core conversion logic and model resolution
- Jackson integration for serialization/deserialization
- Key classes:
  - `ModelConverter` interface - plugin point for custom converters
  - `ModelResolver` - main implementation for converting Java types
  - `AnnotatedType` - wrapper for types with additional metadata
  - `ModelConverters` - facade for model conversion
- JSON/YAML serialization support
- Located in `io.swagger.v3.core.converter.*` and `io.swagger.v3.core.jackson.*`

**swagger-integration** (`modules/swagger-integration/`)
- JAX-RS integration layer
- Scanner and reader implementations
- Connects JAX-RS annotations to OpenAPI model

**swagger-jaxrs2** (`modules/swagger-jaxrs2/`)
- JAX-RS 2.0 support
- Resource scanning and API generation
- Supports both `javax.ws.rs` and `jakarta.ws.rs`

**swagger-jaxrs2-servlet-initializer** (`modules/swagger-jaxrs2-servlet-initializer/`)
- Servlet container integration
- Auto-initialization support

**swagger-maven-plugin** (`modules/swagger-maven-plugin/`)
- Maven plugin to generate OpenAPI specs at build time
- Goal: `resolve`
- Can output JSON, YAML, or both formats

**swagger-eclipse-transformer-maven-plugin** (`modules/swagger-eclipse-transformer-maven-plugin/`)
- Eclipse-specific transformation plugin

**swagger-java17-support** (`modules/swagger-java17-support/`)
- Java 17+ specific enhancements
- Activated when JDK 17+ detected

**swagger-project-jakarta** (`modules/swagger-project-jakarta/`)
- Jakarta EE namespace variants
- Mirror of main modules with `-jakarta` suffix
- Contains: swagger-core-jakarta, swagger-jaxrs2-jakarta, etc.

### Key Package Structure

```
io.swagger.v3.core/
├── converter/          # Type conversion and model resolution
├── jackson/           # Jackson serialization integration
├── filter/            # OpenAPI spec filtering
└── util/              # Utility classes (AnnotationsUtils, Json, etc.)

io.swagger.v3.oas.models/
├── OpenAPI.java       # Root specification object
├── Operation.java     # Operation model
├── Components.java    # Reusable components
├── PathItem.java      # Path item definition
├── media/             # Schema models
├── parameters/        # Parameter models
├── responses/         # Response models
└── security/          # Security models

io.swagger.v3.oas.annotations/
# OpenAPI annotation definitions for Java code
```

### Jakarta vs javax Support

Since version 2.1.7, Swagger Core provides parallel artifact sets:
- Standard artifacts: `swagger-jaxrs2` (uses `javax.ws.rs`)
- Jakarta artifacts: `swagger-jaxrs2-jakarta` (uses `jakarta.ws.rs`)
- Both provide identical functionality, just different namespaces

Use Jakarta artifacts for modern Java EE/Web applications, javax for legacy support.

## Development Workflow

### Prerequisites
- Java 11 or higher
- Apache Maven 3.0.4+ (not 2.1.0 or 2.2.0 due to GPG/checksum issues)
- Jackson 2.4.5+

### First Build
```bash
mvn -N  # Bootstrap build
mvn install  # Full build with tests
```

### Testing
- Uses TestNG for testing (`org.testng:testng:7.10.2`)
- Test sources in `src/test/java`
- Mockito for mocking (`org.mockito:mockito-core:2.28.2`)
- REST Assured for integration testing
- Code coverage requirements: 90% line and complexity

Run tests with:
```bash
mvn test
```

### CI/CD Workflow

The project uses GitHub Actions with the following workflows:

1. **maven.yml** - Build, test, and deploy master branch
2. **maven-pulls.yml** - Build and test PRs
3. **maven-v1.yml** - Support for 1.5 branch (OpenAPI 2.0)
4. **maven-v1-pulls.yml** - PR testing for 1.5 branch

### Release Process

Releases are semi-automated with two-phase process:

1. **Prepare Release** (`prepare-release.yml`)
   - Creates release notes from merged PRs
   - Drafts release with tag
   - Bumps versions
   - Builds and tests
   - Opens PR for review

2. **Release** (`release.yml`)
   - Deploys to Maven Central
   - Publishes Javadoc to gh-pages
   - Publishes Gradle plugin
   - Publishes GitHub release
   - Creates next snapshot PR
   - Updates Wiki

See `CI/CI.md` for complete release documentation.

### Dependency Management

Key dependencies controlled in root `pom.xml`:
- Jackson: `2.19.2`
- TestNG: `7.10.2`
- Mockito: `2.28.2`
- Jersey: `2.46`
- Jakarta WS RS: `2.1.6`
- SnakeYAML: `2.3`
- SLF4J: `2.0.9`

## Important Notes

### OSGi Bundle Support
- Uses bnd-maven-plugin for OSGi packaging
- Exports all packages except `*.internal`
- Contracts defined for JavaJAXRS and JavaServlet

### Java Version Compatibility
- Compiler release: Java 8 (bytecode target)
- Requires Java 11+ to build
- Java 17+ modules activate additional features

### Security
- Security contact: security@swagger.io
- OWASP dependency check available via `mvn clean install -Psecurity`

### Build Profiles
- `security` - Runs OWASP dependency check
- `release` - Signs artifacts with GPG
- `java-17-modules` - Activates Java 17+ specific modules

### Code Style
- Google Java Style formatting
- Maven Enforcer Plugin enforces dependency convergence
- JaCoCo for code coverage (90% minimum)

### Sample Applications
- Sample applications moved to separate repo: https://github.com/swagger-api/swagger-samples/tree/2.0

## Documentation Links

- Wiki: https://github.com/swagger-api/swagger-core/wiki
- Getting Started: https://github.com/swagger-api/swagger-core/wiki/Swagger-2.X---Getting-started
- OpenAPI 3.1 Support: https://github.com/swagger-api/swagger-core/wiki/Swagger-2.X---OpenAPI-3.1
- Jakarta Namespace: https://github.com/swagger-api/swagger-core/wiki/Swagger-2.X---Getting-started
- Maven Central: https://repo1.maven.org/maven2/io/swagger/core.v3/swagger-project/