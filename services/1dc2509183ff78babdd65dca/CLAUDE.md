# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Forest is a declarative HTTP client framework for Java that allows you to call HTTP APIs using simple interface definitions with annotations. It supports multiple backends (HttpClient, OkHttp), various data formats (JSON, XML, Protobuf), and integrates with Spring/Spring Boot.

**Latest Version:** 1.8.0
**Java Version:** 1.8+
**License:** MIT

## Common Development Commands

### Building the Project
```bash
# Build entire project
mvn clean install

# Build without running tests
mvn clean install -DskipTests

# Compile only
mvn clean compile

# Package JARs
mvn clean package
```

### Running Tests
```bash
# Run all tests
mvn test

# Run tests for specific module
cd forest-core && mvn test
cd forest-spring && mvn test

# Run single test class
mvn test -Dtest=TestClassName

# Run with coverage report
mvn cobertura:cobertura

# Run integration tests (Spring Boot tests)
cd forest-test/forest-spring-boot-test && mvn test
cd forest-test/forest-spring-boot3-test && mvn test
```

### Running Examples
```bash
# Spring Boot examples
cd forest-examples/example-springboot && mvn spring-boot:run
cd forest-examples/example-springboot3 && mvn spring-boot:run

# Solon example
cd forest-examples/example-solon && mvn run
```

## Project Structure

### Modules
- **forest-core** - Core framework (main module)
- **forest-jaxb** - XML binding via JAXB
- **forest-jakarta-xml** - XML binding via Jakarta XML
- **forest-reactor** - Reactive support (Project Reactor)
- **forest-spring** - Spring integration
- **forest-spring-boot-starter** - Spring Boot 2.x starter
- **forest-spring-boot3-starter** - Spring Boot 3.x starter
- **forest-mock** - Testing utilities
- **forest-solon-plugin** - Solon framework integration
- **forest-test** - Integration tests (Spring Boot 2 & 3)
- **forest-examples** - Example projects

### Core Architecture

The framework follows a multi-layered architecture:

#### 1. **Annotation Layer** (`forest-core/src/main/java/com/dtflys/forest/annotation/`)
Request definitions using Java annotations:
- HTTP Methods: `@Get`, `@Post`, `@Put`, `@Patch`, `@Delete`, `@Head`, `@Options`, `@Trace`
- Data Binding: `@Query`, `@DataParam`, `@Header`, `@Body`, `@JSONBody`, `@XMLBody`, `@ProtobufBody`
- File Operations: `@DataFile`, `@DownloadFile`
- Authentication: `@BasicAuth`, `@OAuth2`
- Lifecycle: `@MethodLifeCycle`, `@ParamLifeCycle`, `@RequestAttributes`

#### 2. **Configuration Layer** (`forest-core/src/main/java/com/dtflys/forest/config/`)
- `ForestConfiguration` - Central configuration class
- Defines backends, converters, interceptors, SSL settings, retry policies
- Supports multiple named configurations

#### 3. **Proxy Layer** (`forest-core/src/main/java/com/dtflys/forest/proxy/`)
Dynamic proxy generation for client interfaces:
- `ProxyFactory` creates proxy instances
- `ForestGenericClient` handles invocation

#### 4. **HTTP Layer** (`forest-core/src/main/java/com/dtflys/forest/http/`)
Abstraction over HTTP clients:
- `ForestRequest` - Request builder and executor
- `ForestResponse` - Response wrapper
- `ForestCookie` - Cookie management
- Backends: HttpClient, OkHttp implementations

#### 5. **Lifecycle Layer** (`forest-core/src/main/java/com/dtflys/forest/lifecycles/`)
Extensibility points:
- `MethodAnnotationLifeCycle` - Method-level lifecycle hooks
- `ParamLifeCycle` - Parameter-level processing
- Built-in: authorization, file handling, base lifecycle

#### 6. **Serialization Layer** (`forest-core/src/main/java/com/dtflys/forest/converter/`)
Multiple data format converters:
- JSON: Fastjson2, Fastjson1, Jackson, Gson
- XML: JAXB, Jakarta XML
- Protobuf: Native support
- Binary, Form data, Text

## Key Components

### Forest Class (Main Entry Point)
Location: `forest-core/src/main/java/com/dtflys/forest/Forest.java`

Static facade providing:
```java
// Create client
Forest.client(MyApiInterface.class)

// Programmatic requests
Forest.get("http://example.com")
Forest.post("http://example.com")

// Configuration
Forest.config()
```

### ForestConfiguration
Central configuration managing:
- HTTP backend selection (HttpClient/OkHttp)
- Serialization converters
- Interceptors
- SSL/TLS settings
- Retry policies
- Cookie storage
- Logging
- Connection pooling

### Backend System
Two HTTP backends available:
1. **HttpClient** (Apache HttpClient 4.5.x)
2. **OkHttp** (Square OkHttp 3.14.x)

Switch backends via:
```java
Forest.config().backend("okhttp3"); // or "httpclient"
```

## Request Definition Pattern

### Interface-Based Declarative Style
```java
public interface MyClient {
    @Get("http://api.example.com/users/{id}")
    User getUser(@Var("id") String id);

    @Post("http://api.example.com/users")
    @JSONBody
    User createUser(@JSONBody User user);
}
```

### Programmatic Style
```java
Forest.post("/api/users")
    .contentType("application/json")
    .addBody(user)
    .execute(User.class);
```

## Spring Integration

### Configuration
Use `@ForestScan` to scan client interfaces:
```java
@SpringBootApplication
@ForestScan(basePackages = "com.example.clients")
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### Dependency Injection
```java
@Autowired
private MyClient myClient;
```

### Spring Boot Starters
- `forest-spring-boot-starter` - Spring Boot 2.x
- `forest-spring-boot3-starter` - Spring Boot 3.x

## Data Serialization

### JSON Support
Multiple JSON libraries supported:
- Fastjson2 (default for 1.8.x)
- Fastjson1
- Jackson
- Gson

### XML Support
- JAXB annotations
- Jakarta XML (for Jakarta EE)

### Protobuf Support
Direct protobuf serialization:
```java
@Post(url = "/message", contentType = "application/octet-stream")
String sendMessage(@ProtobufBody MyProtobufMessage message);
```

## Testing

### Unit Tests
Located in `forest-core/src/test/java/`
- Uses JUnit 4
- MockWebServer for HTTP mocking
- Mockito for object mocking

### Integration Tests
Located in `forest-test/`
- `forest-spring-boot-test` - Spring Boot 2.x integration
- `forest-spring-boot3-test` - Spring Boot 3.x integration

### Test Patterns
```java
// Common test structure
public class MyTest {
    @Rule
    public MockServerRule server = new MockServerRule(this);

    @Test
    public void testSomething() {
        // Configure mock server
        server.mock().get("/api/test").reply(200).body("success");

        // Test client
        String result = Forest.get("http://localhost:8080/api/test").execute(String.class);
        assertThat(result).isEqualTo("success");
    }
}
```

## Customization Points

### Custom LifeCycles
Implement `MethodAnnotationLifeCycle` or `ParamLifeCycle`:
```java
public class MyLifeCycle implements MethodAnnotationLifeCycle<MyAnnotation, Object> {
    @Override
    public boolean beforeExecute(ForestRequest request) {
        // Custom logic before request
        return true;
    }
}
```

### Custom Filters
Implement `Filter` interface:
```java
public class MyFilter implements Filter {
    @Override
    public Object doFilter(ForestRequest request, Map<String, Object> data) {
        // Transform request
        return request;
    }
}
```

### Custom Converters
Extend `ForestConverter` for custom data formats.

## Examples

### Basic Examples
- `forest-examples/example-springboot` - Spring Boot 2 example
- `forest-examples/example-springboot3` - Spring Boot 3 example
- `forest-examples/example-solon` - Solon framework example
- `forest-examples/example-chatgpt` - ChatGPT API integration
- `forest-examples/example-deepseek` - DeepSeek API integration

## Development Notes

### Version Management
Uses Maven `flatten-maven-plugin` with `${revision}` property for flexible versioning.

### Dependencies
Key dependencies declared in root `pom.xml`:
- Spring Framework 5.3.20
- Spring Boot 2.7.18
- OkHttp 3.14.9
- Apache HttpClient 4.5.13
- Jackson 2.18.2
- Fastjson2 2.0.53

### CI/CD
Travis CI configuration (`.travis.yml`) runs:
- `mvn cobertura:cobertura` - Code coverage
- Uploads to codecov.io

### Code Coverage
Uses Cobertura for code coverage. View reports in `target/site/cobertura/`

## Important Considerations

1. **Java 8+**: Project compiled with Java 8, avoid using newer Java features
2. **Backward Compatibility**: Maintains compatibility with Java 8 runtime
3. **Spring Boot Versions**: Separate starters for Spring Boot 2 and 3
4. **Testing**: MockServerRule is commonly used for integration testing
5. **Documentation**: Official docs at https://forest.kim/

## Common Issues & Solutions

### Backend Selection
Ensure correct backend dependency on classpath for desired HTTP client.

### JSON Converter
If using Jackson, ensure jackson-databind is on classpath. Forest auto-selects based on available libraries.

### Spring Boot Integration
Remember to use `@ForestScan` annotation, not just component scanning.

### Test Configuration
Look at `forest-test/forest-spring-boot-test/src/test/resources/application-*.yml` for test configuration examples.