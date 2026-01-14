# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Test Commands

### Common Commands
- **Build the project**: `mvn clean install`
- **Run all tests**: `mvn test`
- **Run a single test class**: `mvn test -Dtest=WireMockStatusReporterTest`
- **Run a single test method**: `mvn test -Dtest=WireMockStatusReporterTest#user_whenProxying_AuthCorrectlyConfigured`
- **Fix code formatting**: `mvn spotless:apply`
- **Check code formatting (CI)**: `mvn spotless:check`
- **Run full CI build**: `mvn -D enable-ci clean install site "-Dsurefire.argLine=--add-opens java.base/java.net=ALL-UNNAMED"`
- **Build without slow/flaky tests**: `mvn clean install -Dtest -Dtest.exclude='**/AbuseLimitHandlerTest,**/GHRateLimitTest,**/GHPullRequestTest,**/RequesterRetryTest,**/RateLimitCheckerTest,**/RateLimitHandlerTest'`

### Integration Tests with GitHub Proxy
Tests support proxying to GitHub API using recorded WireMock data:

- **Run tests with proxy to GitHub**: `mvn install -Dtest.github.useProxy -Dtest=YourTestClass`
- **Create new WireMock snapshots**: `mvn install -Dtest.github.takeSnapshot -Dtest.github.org=false -Dtest=YourTestClass`
- **Use personal account instead of org**: `mvn install -Dtest.github.org=false -Dtest=YourTestClassName`

**Prerequisites for proxy testing**:
1. Create a Personal Access Token on GitHub
2. Set `GITHUB_OAUTH` environment variable to the token value

### Test Categories
- **Slow or flaky tests** are excluded by default and listed in `src/test/resources/slow-or-flaky-tests.txt`
- Integration tests run in the `integration-test` phase with multiple profiles:
  - `okhttp-test`: Tests with OkHttp connector
  - `httpclient-test-tracing`: Tests with HttpClient and trace logging
  - `slow-or-flaky-test`: Tests known to be slow or flaky (with retries)
  - `jwt0.11.x-test`: Tests for JWT 0.11.x compatibility

## Code Architecture

### Core Components

**Main Entry Point**: `org.kohsuke.github.GitHub`
- The primary class for interacting with the GitHub API
- Thread-safe and can be used concurrently
- Provides static factory methods for creating connections
- Location: `src/main/java/org/kohsuke/github/GitHub.java`

**HTTP Client**: `org.kohsuke.github.GitHubClient`
- Handles HTTP communication with GitHub's API
- Uses a pluggable `GitHubConnector` for different HTTP client implementations
- Thread-safe and manages rate limiting
- Location: `src/main/java/org/kohsuke/github/GitHubClient.java`

**Connector Pattern**: `org.kohsuke.github.connector.GitHubConnector`
- Abstraction for HTTP clients
- Default implementation uses `java.net.HttpURLConnection`
- Optional implementations:
  - `org.kohsuke.github.extras.okhttp3.OkHttpGitHubConnector` (OkHttp3)
  - `org.kohsuke.github.extras.HttpClientGitHubConnector` (Apache HttpClient)

**Authorization**: `org.kohsuke.github.authorization`
- `AuthorizationProvider`: Base interface for authentication
- `UserAuthorizationProvider`: For user-based authentication
- `DependentAuthorizationProvider`: For authorization that requires a GitHub instance (e.g., GitHub Apps)
- Implementations in `org.kohsuke.github.extras.authorization`

### API Object Model

**Repository of GitHub Domain Objects**: `org.kohsuke.github.*`
- Each GitHub entity (Repository, Issue, Pull Request, etc.) has a corresponding GH* class
- Named after GitHub's API resources (e.g., `GHRepository`, `GHIssue`, `GHPullRequest`)
- Most classes are in `src/main/java/org/kohsuke/github/`

**Builder Pattern**: Many API operations use builders (e.g., `GHRepositoryBuilder`, `GHIssueBuilder`)
- Fluent APIs for creating and updating GitHub resources
- Follow a consistent naming convention: `{Resource}{Operation}Builder`

**Paging and Iteration**:
- GitHub's API pagination is handled through `*Iterable` and `*Page` classes
- Examples: `GHArtifactsIterable`, `GHArtifactsPage`

### Internal Architecture

**JSON Serialization**: Jackson
- `com.fasterxml.jackson.databind` for JSON processing
- `jackson-datatype-jsr310` for Java 8+ date/time types
- Custom configuration in `GitHubClient`

**Internal Packages**:
- `org.kohsuke.github.internal`: Internal implementation details (not API-stable)
- `org.kohsuke.github.internal.graphql`: GraphQL-specific utilities
- `org.kohsuke.github.function`: Functional utilities

**Examples**: `org.kohsuke.github.example`
- Located in `src/main/java/org/kohsuke/github/example/`
- Contains usage examples and sample code

### API Stability and Compatibility

**Bridge Method Injection**:
- Uses `bridge-method-injector` to maintain backward compatibility
- Profile `bridged` generates bridged methods for API compatibility

**API Compatibility Checking**:
- `japicmp-maven-plugin` checks binary compatibility between versions
- Excludes internal packages from compatibility checks
- Runs in the `verify` phase

**GraalVM Native Image Support**:
- Native image configuration in `src/main/resources/META-INF/native-image/`
- Used for Spring Boot AOT (Ahead-Of-Time) processing
- Tested with `AotIntegrationTest`

## Development Practices

### Code Quality Tools

**SpotBugs** (Bytecode analysis):
- Runs in the `verify` phase
- Configured with `spotbugs-maven-plugin`
- Fail-on-error is configurable via property

**Spotless** (Code formatting):
- Eclipse formatter configuration in `src/build/eclipse/formatter.xml`
- Import order in `src/build/eclipse/eclipse.importorder`
- Runs as part of CI (`spotless:check`)

**SortPom** (POM validation):
- Validates Maven POM dependencies are sorted
- Runs in the `validate` phase

**JaCoCo** (Code coverage):
- Coverage requirements: 70% for bundles, 50% for classes
- Integration test coverage (`jacoco-it.exec`)
- Coverage checks may halt build on CI (`jacoco.haltOnFailure=true` in CI)

### Test Infrastructure

**WireMock**:
- Used for stubbing GitHub API responses
- Test data stored in `src/test/resources/org/kohsuke/github/{TestClass}/wiremock/`
- Each test method gets its own directory with JSON responses and mappings

**Test Configuration**:
- `src/test/resources/application-test.yml`: Spring Boot test configuration
- `src/test/resources/slow-or-flaky-tests.txt`: List of tests to exclude by default
- `src/test/resources/test-trace-logging.properties`: Trace logging configuration

### Dependency Management

**Key Dependencies**:
- Jackson (JSON): `jackson-databind`, `jackson-datatype-jsr310`
- HTTP Clients: OkHttp3 (optional), Apache HttpClient (optional)
- JWT: `io.jsonwebtoken` (JJWT) for GitHub App authentication (optional)
- Testing: JUnit 5, WireMock, Mockito, Hamcrest

**Build Tools**:
- Maven compiler plugin: Java 11 source/target
- Bridge method annotation processor
- Spring Boot plugin for AOT processing

### Key Configuration Files

- `pom.xml`: Maven build configuration with profiles for CI, release, bridged builds
- `src/build/eclipse/formatter.xml`: Code formatting rules
- `src/build/eclipse/eclipse.importorder`: Import organization
- `.github/workflows/`: GitHub Actions CI/CD workflows
- `src/test/resources/slow-or-flaky-tests.txt`: Tests excluded from default runs

## Project Structure

```
src/
├── main/
│   ├── java/org/kohsuke/github/
│   │   ├── GitHub.java                    # Main API entry point
│   │   ├── GitHubClient.java              # HTTP client implementation
│   │   ├── authorization/                 # Authentication providers
│   │   ├── connector/                     # HTTP connector abstractions
│   │   ├── extras/                        # Optional implementations (OkHttp, HttpClient)
│   │   ├── internal/                      # Internal implementation (not API-stable)
│   │   ├── function/                      # Functional utilities
│   │   └── example/                       # Usage examples
│   └── resources/
│       └── META-INF/native-image/         # GraalVM native image config
└── test/
    ├── java/                              # Test classes using WireMock
    └── resources/
        ├── org/kohsuke/github/            # WireMock test data
        ├── slow-or-flaky-tests.txt        # Excluded test patterns
        └── test-trace-logging.properties  # Logging config
```