# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MyBatis-Plus is a powerful enhanced toolkit of MyBatis that simplifies database CRUD operations. It provides auto-configuration, wrapper-based query builders, Lambda-style APIs, and an extensible plugin system.

## Build Commands

```bash
# Build all modules
./gradlew build

# Run all tests (excludes mysql/phoenix tests by default)
./gradlew test

# Run tests for a specific module
./gradlew :mybatis-plus-core:test

# Run a single test class
./gradlew test --tests "com.baomidou.mybatisplus.core.conditions.QueryWrapperTest"

# Run a specific test method
./gradlew test --tests "com.baomidou.mybatisplus.core.conditions.QueryWrapperTest.testQueryWrapper"

# Generate javadoc
./gradlew javadoc

# Create sources jar
./gradlew sourcesJar
```

## Module Structure

The project is organized as a multi-module Gradle build:

| Module | Purpose |
|--------|---------|
| `mybatis-plus-annotation` | Core annotations: `@TableName`, `@TableId`, `@TableField`, `@Version`, `@TableLogic`, `@EnumValue` |
| `mybatis-plus-core` | Core functionality: `BaseMapper`, wrapper classes (`QueryWrapper`, `LambdaQueryWrapper`, `UpdateWrapper`), table metadata reflection (`TableInfoHelper`), SQL injection prevention |
| `mybatis-plus-extension` | Extended features: `IService`/`ServiceImpl`, Active Record (`Model`), plugin system (`MybatisPlusInterceptor` with pagination, tenant isolation, optimistic locking), chain wrappers |
| `mybatis-plus` | Integration module combining core and extension (both Java and Kotlin support) |
| `mybatis-plus-boot-starter` | Spring Boot auto-configuration with `MybatisPlusProperties` |
| `mybatis-plus-boot-starter-test` | Spring Boot test helper for auto-configuring MyBatis-Plus |

## Key Architectural Patterns

### Annotation-Based Table Mapping
Entity classes use annotations to map to database tables. `TableInfoHelper` uses reflection to extract metadata from annotated classes at runtime:

```java
@TableName("user")
public class User {
    @TableId(type = IdType.AUTO)
    private Long id;
    @TableField("user_name")
    private String name;
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;
    @Version
    private Integer version;
}
```

### Wrapper-Based Query Building
All queries use wrapper classes for type-safe, flexible conditions:

- `QueryWrapper` - String-based column references
- `LambdaQueryWrapper` - Lambda-based column references (type-safe)
- `UpdateWrapper` - For update operations with where conditions
- Chain wrappers: `QueryChainWrapper`, `LambdaQueryChainWrapper`, `UpdateChainWrapper`

### Interceptor-Based Plugin System
`MybatisPlusInterceptor` chains inner interceptors for cross-cutting concerns:
- `PaginationInnerInterceptor` - Automatic paging with dialect support
- `TenantLineInnerInterceptor` - Multi-tenant isolation
- `OptimisticLockerInnerInterceptor` - Optimistic locking via `@Version`
- `BlockAttackInnerInterceptor` - SQL injection prevention
- `DataPermissionInterceptor` - Row-level data permissions

### SQL Injection via Method Injection
`AbstractMethod` implementations are injected into mappers via `SqlInjector`:
- `Insert`, `DeleteById`, `UpdateById`, `SelectById` - Basic CRUD
- `InsertBatchSomeColumn` - Batch insert
- `LogicDeleteBatchByIds` - Soft delete with `@TableLogic`
- `AlwaysUpdateSomeColumnById` - Selective column updates

## Code Style

- **Indentation**: 4 spaces (EditorConfig)
- **Encoding**: UTF-8
- **Line endings**: LF
- **License header**: Required on all Java/Kotlin files (Apache 2.0, updated year)
- **Import order**: static imports first, then java.*, javax.*, org.*, com.*, default package
- **Java version**: 1.8+

## Common Development Tasks

### Adding a New Annotation
1. Define the annotation in `mybatis-plus-annotation`
2. Process it in `TableInfoHelper.addTableInfo` or relevant handler
3. Add tests in `mybatis-plus-core/src/test/java`

### Adding a New CRUD Method
1. Create `AbstractMethod` subclass in `mybatis-plus-core/src/main/java/.../injector/methods/`
2. Register in `DefaultSqlInjector.getMethodList()`
3. Add tests to verify SQL generation

### Adding a New Plugin Interceptor
1. Implement `InnerInterceptor` interface
2. Add to `MybatisPlusInterceptor` chain in `mybatis-plus-extension`
3. Test with multiple database dialects

## Database Support

Supported databases include: MySQL, PostgreSQL, Oracle, SQL Server, DB2, H2, SQLite, Firebird, Kingbase, DM (达梦). Database-specific features are handled via:
- `DbType` enum in annotations
- `IDialect` implementations for pagination
- `IKeyGenerator` implementations for key generation