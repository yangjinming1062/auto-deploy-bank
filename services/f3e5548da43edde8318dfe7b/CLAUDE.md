# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## WxJava - WeChat Java SDK Overview

WxJava is a comprehensive Java SDK for WeChat development, supporting multiple WeChat platforms including Official Accounts, Mini Programs, WeChat Pay, Enterprise WeChat, Open Platform, Channels/Video Accounts, and Qidian. The project is a Maven multi-module build with 8 core SDK modules plus framework integrations.

**Current Version**: 4.7.9.B
**Java Requirement**: JDK 8+ (minimum target)
**Build Tool**: Maven 3.6+

## Quick Start Commands

### Initial Setup
```bash
# First-time setup (compiles all 34 modules - ~4-5 minutes)
mvn clean compile -DskipTests=true --no-transfer-progress

# Package without tests (~2-3 minutes)
mvn clean package -DskipTests=true --no-transfer-progress

# Verify code style (~45-60 seconds)
mvn checkstyle:check --no-transfer-progress
```

**Important**: Never interrupt Maven builds. Initial compilation takes ~4 minutes due to the 34-module structure.

### Development Workflow
```bash
# Incremental compile after changes
mvn compile --no-transfer-progress

# Check code style
mvn checkstyle:check --no-transfer-progress

# Complete build validation
mvn clean package -DskipTests=true --no-transfer-progress

# Analyze dependencies
mvn dependency:tree --no-transfer-progress

# Check for dependency updates
./others/check-dependency-updates.sh
```

### Testing
**Note**: Tests are disabled by default in `pom.xml` (`<skip>true</skip>`). To run tests:

```bash
# Run all tests (requires test-config.xml with real API credentials)
mvn test

# Run single test
mvn test -Dtest=TestClassName
```

**Test Requirements**:
- Test framework: TestNG (not JUnit)
- Requires `src/test/resources/test-config.xml` with real WeChat API credentials
- 298 test files exist across modules
- Without credentials, tests will fail

## Project Architecture

### Core SDK Modules (Build Order)
1. **weixin-graal** - GraalVM native image support
2. **weixin-java-common** - Foundation utilities and base classes (all modules depend on this)
3. **weixin-java-mp** - Official Accounts API
4. **weixin-java-pay** - WeChat Pay API
5. **weixin-java-miniapp** - Mini Programs API
6. **weixin-java-cp** - Enterprise WeChat API
7. **weixin-java-open** - Open Platform API
8. **weixin-java-channel** - Channels/Video Account API
9. **weixin-java-qidian** - Qidian API

### Framework Integration
- **spring-boot-starters/** - Spring Boot auto-configuration starters
- **solon-plugins/** - Solon framework plugins
- **weixin-graal/** - GraalVM native image support

### Module Package Structure
Each SDK module follows this pattern:
```
src/main/java/me/chanjar/weixin/{module}/
├── api/          # API interfaces
├── bean/         # Model/POJO classes
├── config/       # Configuration classes
├── util/         # Utility classes
├── builder/      # Builder patterns (especially for XML responses)
├── constant/     # Constants
└── enums/        # Enumerations
```

Key areas:
- **API Implementation**: `*/service/impl/` directories
- **Configuration**: `*/config/` directories
- **Beans/Models**: `*/bean/` directories
- **Utilities**: `weixin-java-common/*/util/` directories

## Development Guidelines

### Code Style
- **Enforced by Checkstyle**: Google Java Style Guide
- **Indentation**: 2 spaces (not tabs)
- **Configuration**: `.editorconfig` and `quality-checks/google_checks.xml`
- **IDE**: IntelliJ IDEA recommended (project optimized for IDEA)
- **Lombok**: Extensively used - ensure annotation processing is enabled

### Branch and PR Strategy
- **Target Branch**: All PRs must target `develop` branch
- **Source Branches**: Feature branches from `develop`
- **Release Branch**: `release` branch contains stable releases only
- **CI**: CircleCI builds on every commit

### Build Profile
- **Release Profile**: Use `mvn clean deploy -P release` for publishing
- **Native Image**: Profile `native-image` available for GraalVM builds

## Key Files and Locations

### Configuration
- `pom.xml` - Root Maven configuration and dependency management
- `quality-checks/google_checks.xml` - Checkstyle rules
- `.editorconfig` - IDE formatting rules

### CI/CD
- `.circleci/config.yml` - CircleCI build configuration

### Documentation
- `README.md` - Project overview and Maven dependencies
- `CONTRIBUTING.md` - Contribution guidelines
- `demo.md` - Demo project references
- Module-specific README files in each starter directory

### Testing Resources
- `*/src/test/resources/test-config.sample.xml` - Test configuration template
- Contains WeChat API credentials needed for testing

## Common Development Tasks

### Building Specific Modules
```bash
cd weixin-java-mp
mvn clean compile --no-transfer-progress
```

### Version Management
```bash
# Display property updates
mvn versions:display-property-updates --no-transfer-progress

# Deploy to Maven Central (requires credentials)
mvn clean deploy -P release --no-transfer-progress
```

### Troubleshooting
- **OutOfMemoryError**: Set `MAVEN_OPTS="-Xmx2g"`
- **Checkstyle failures**: Verify IDE `.editorconfig` support
- **Compilation failures**: Run `mvn clean` first
- **Slow builds**: Use `--no-transfer-progress` flag

## SDK Usage Patterns

### Maven Dependencies
```xml
<dependency>
  <groupId>com.github.binarywang</groupId>
  <artifactId>weixin-java-mp</artifactId>
  <version>4.7.0</version>
</dependency>
```

Available modules:
- `weixin-java-miniapp` - Mini Programs
- `weixin-java-pay` - WeChat Pay
- `weixin-java-open` - Open Platform
- `weixin-java-mp` - Official Accounts
- `weixin-java-cp` - Enterprise WeChat
- `weixin-java-channel` - Channels/Video Accounts

### Framework Integrations
Spring Boot starters available for each module in `spring-boot-starters/` directory. See module-specific READMEs for configuration details.

## Dependency Management

### Core Dependencies
- **HttpClient**: 4.5.13
- **Jackson**: 2.18.4 (BOM)
- **Gson**: 2.13.1
- **Lombok**: 1.18.30
- **SLF4J**: 1.7.30
- **TestNG**: 7.5.1 (not JUnit)
- **Jetty**: 9.4.57.v20241219 (must be 9.x for JDK 8 support)

### Redis Support (Optional)
- `jedis` 3.3.0
- `redisson` 3.23.3 (optional)
- `spring-data-redis` 2.3.3.RELEASE (optional)

## Performance Notes
- **Initial build**: 4-5 minutes (34 modules + dependency downloads)
- **Incremental builds**: 30-60 seconds (after initial build)
- **Checkstyle**: ~50 seconds (should run frequently)
- **Memory**: Increase Maven options if OutOfMemoryError occurs

## Project Characteristics
- **Type**: SDK library project (not an application)
- **Purpose**: Provide WeChat API client implementations
- **Focus**: API functionality and compatibility with WeChat platform changes
- **Architecture**: Modular design with common utilities centralized