# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **mzt-biz-log** (version 1.0.1), a Spring Boot business operation logging framework that records "who", "when", "what", and "what was done" for business operations. It provides annotation-based logging with SpEL expression support, object diffing, and customizable functions.

**Key Problem Solved**: Automatically tracks business operation logs with support for custom templates, object diffing, conditional logging, and integration with Spring Boot/Spring MVC applications.

## Repository Structure

The project is a Maven multi-module repository with three modules:

- **bizlog-sdk** - Core logging SDK (annotations, AOP, parsing, diff utilities)
- **bizlog-server** - Test/demo server with example implementations and integration tests
- **bizlog-sdk-xml** - XML configuration support for Spring MVC (non-Boot) applications

## Common Commands

### Build & Compile
```bash
# Build all modules
mvn clean install

# Build specific module
mvn clean install -pl bizlog-sdk
mvn clean install -pl bizlog-server

# Skip tests during build
mvn clean install -DskipTests

# Compile without packaging
mvn clean compile
```

### Run Tests
Tests are located in the `bizlog-server` module and use H2 in-memory database with test resources in `bizlog-server/src/test/resources/`.

```bash
# Run all tests
mvn test

# Run tests for specific module
mvn test -pl bizlog-server

# Run a specific test class
mvn test -pl bizlog-server -Dtest=IOrderServiceTest

# Run tests with verbose output
mvn test -pl bizlog-server -Dtest=IOrderServiceTest#testDiff1
```

### Package
```bash
# Create JAR packages
mvn clean package

# Package specific module
mvn clean package -pl bizlog-sdk
```

### Code Quality (if configured)
```bash
# Run checkstyle (if configured)
mvn checkstyle:check

# Run spotbugs (if configured)
mvn spotbugs:check
```

## Architecture

### Core Components

**1. bizlog-sdk Module (Core Framework)**
- **Annotation Layer** (`starter/annotation/`):
  - `@LogRecord` - Main annotation for marking methods to log
  - `@EnableLogRecord` - Spring Boot enable annotation
  - `@DiffLogField`, `@DiffLogAllFields`, `@DiffLogIgnore` - Object diff annotations

- **AOP Layer** (`starter/support/aop/`):
  - `BeanFactoryLogRecordAdvisor` - Spring AOP advisor
  - `LogRecordInterceptor` - Intercepts annotated methods
  - `LogRecordOperationSource` - Extracts log record operations from methods

- **Parsing Layer** (`starter/support/parse/`):
  - `LogRecordValueParser` - Parses SpEL expressions in annotations
  - `LogFunctionParser` - Handles custom parse functions
  - `LogRecordExpressionEvaluator` - Evaluates SpEL expressions

- **Diff Utilities** (`util/diff/`):
  - `ArrayDiffer` - Compares array/list changes
  - `ArrayItemAccessor` - Accesses array items for diffing

**2. bizlog-server Module (Integration & Examples)**
- **Test Implementations**: Example services showing how to use the SDK
  - `OrderServiceImpl`, `UserServiceImpl`, `SkuServiceImpl` - Example business services
  - `DbLogRecordService` - Database-backed log record storage implementation

- **Custom Functions**: Example parse function implementations
  - `OrderParseFunction`, `SexParseFunction`, `IdentityParseFunction` - Custom function examples

- **Infrastructure**:
  - `repository/mapper/` - MyBatis Plus mappers for log persistence
  - `repository/po/` - PO objects for database
  - `ShiroConfig`, `ShiroTestRealm` - Authentication examples

**3. bizlog-sdk-xml Module (Spring MVC Support)**
- Provides XML-based configuration for non-Spring Boot Spring MVC applications
- `BizLogNamespaceHandler`, `BizLogBeanDefinitionParser` - Custom XML namespace support

### Key Extension Points

**For Application Developers:**

1. **IOperatorGetService** - Get current operator/user (implement to customize user retrieval)
   - Location: In SDK, used via Spring Bean
   - Example: `DefaultOperatorGetServiceImpl`

2. **ILogRecordService** - Save/query log records (implement for custom storage)
   - Methods: `record()`, `queryLog()`, `queryLogByBizNo()`
   - Use cases: Store in database, ES, or other storage

3. **IParseFunction** - Create custom parse functions
   - Methods: `functionName()`, `executeBefore()`, `apply()`
   - Example: Convert ID to readable name (`OrderParseFunction`)

4. **IDiffItemsToLogContentService** - Customize object diff output
   - Override default diff behavior

### Configuration

**Spring Boot Configuration** (`application.yml`):
```yaml
mzt:
  log:
    record:
      updateTemplate: __fieldName from __sourceValue to __targetValue
      useEqualsMethod: java.time.LocalDate,java.time.Instant
      diffLog: false  # Don't log if no changes
```

**Enable in Application**:
```java
@SpringBootApplication
@EnableLogRecord(tenant = "your.tenant.name", joinTransaction = true)
@EnableTransactionManagement(order = 0)
public class Main {
    public static void main(String[] args) {
        SpringApplication.run(Main.class, args);
    }
}
```

### Dependencies

**Core SDK** (bizlog-sdk):
- Spring Boot 2.3.4
- java-object-diff 0.95 (for object comparison)
- Hibernate Validator 6.1.5
- Lombok 1.18.12

**Server Module** (bizlog-server):
- Spring Boot Starter Web/Test
- MyBatis Plus 3.4.2
- Druid 1.2.0
- H2 Database (for testing)
- Shiro 1.7.1
- Guava 32.0.0
- Hutool 5.8.21

## Testing

**Test Configuration**: H2 in-memory database at `jdbc:h2:mem:test`

**Test Base Class**: `bizlog-server/src/test/java/com/mzt/logserver/BaseTest.java`
- Sets up Spring Boot test context
- Configures MyBatis Plus mappers
- Component scanning for test services

**SQL Schema**: `bizlog-server/src/test/resources/sql/create.sql`

**Key Test Classes**:
- `IOrderServiceTest` - Tests order logging with diff functionality
- `IUserServiceTest` - Tests user operations
- `ISkuServiceTest` - Tests SKU operations
- `LogRecordValueParserTest` - Tests SpEL parsing
- `LogRecordOperationSourceTest` - Tests annotation parsing

## Usage Examples

**Basic Logging**:
```java
@LogRecord(
    success = "{{#order.purchaseName}} placed order for {{#order.productName}}",
    type = LogRecordType.ORDER,
    bizNo = "{{#order.orderNo}}"
)
public boolean createOrder(Order order) {
    return orderService.create(order);
}
```

**Object Diff**:
```java
@LogRecord(
    success = "Updated order {_DIFF{#oldOrder, #newOrder}}",
    type = LogRecordType.ORDER,
    bizNo = "{{#newOrder.orderNo}}"
)
public boolean updateOrder(Order oldOrder, Order newOrder) {
    return orderService.update(newOrder);
}
```

**Custom Function**:
```java
@Component
public class OrderParseFunction implements IParseFunction {
    public String functionName() { return "ORDER"; }
    public String apply(Object orderId) {
        return orderService.getOrderName((Long) orderId) + "(" + orderId + ")";
    }
}
```

## Important Notes

1. **Transaction Management**: To make logs rollback with business logic, set `joinTransaction = true` in `@EnableLogRecord` and `@EnableTransactionManagement(order = 0)`

2. **Bean Loading Order**: Some classes may not work if initialized before the log record advisor - ensure proper Spring bean ordering

3. **Context Variables**: Use `LogRecordContext.putVariable()` to add variables accessible in SpEL expressions, `putGlobalVariable()` for cross-method variables

4. **Method Execution**: Log recording happens after method execution, so SpEL sees the modified parameter values

5. **No Changes, No Log**: By default, if object diff shows no changes, no log is recorded (configurable via `mzt.log.record.diffLog`)

## Deployment

This is a library project - publish to Maven Central or private repository:

```bash
# Deploy to Sonatype OSSRH (requires GPG signing and credentials)
mvn clean deploy
```

The `bizlog-server` module has `maven.deploy.skip=true` to prevent deployment as it's for testing only.