# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Warehouse Management System built with Spring Boot 2.2.1, Shiro authentication, MyBatis-Plus, and LayUI frontend. Chinese-language project with ~103 Java source files.

## Build & Run Commands

```bash
# Build the project
./mvnw clean package -DskipTests

# Run development server (port 8888)
./mvnw spring-boot:run

# Run with specific profile
./mvnw spring-boot:run -Dspring.profiles.active=dev

# Run tests
./mvnw test

# Generate code (run CodeGenerator.main() from IDE or compile and execute)
java -cp target/classes:target/test-classes com.yeqifu.generator.CodeGenerator
```

**Prerequisites:**
- MySQL 5.7+ on port 3306, database `warehouse` (see `warehouse.sql`)
- Default credentials: root/123456
- Server runs on port 8888
- Java 1.8+

## Architecture

### Package Structure
- **`com.yeqifu.sys`** - System module (authentication, RBAC, logs, permissions)
- **`com.yeqifu.bus`** - Business module (customers, providers, goods, inventory, sales)

Each package follows layered architecture:
```
{module}/
├── entity/          # MyBatis-Plus @TableName entities
├── mapper/          # Extends BaseMapper<T>
├── service/         # I{Entity}Service extends IService<T>
├── service/impl/    # ServiceImpl<I{Entity}Service, Entity>
├── controller/      # @RestController @RequestMapping
├── cache/           # Custom cache aspects (CachePool)
└── vo/              # View objects for form binding
```

### Core Technologies
- **Shiro** - Authentication/Authorization with custom `UserRealm` (MD5+Salt)
- **MyBatis-Plus** - ORM with auto-generated CRUD (BaseMapper, IService)
- **Thymeleaf** - Server-side templating with Shiro dialect integration
- **Hutool** - Utility library (captchas, PinyinUtils)
- **Druid** - Connection pool with `/druid` monitoring
- **Swagger 2** - API docs at `/swagger-ui.html`

### Key Patterns

**Response Wrapper:**
- `DataGridView` - Paginated list responses (code, msg, count, data)
- `ResultObj` - Operation result constants (ADD_SUCCESS, DELETE_ERROR, etc.)
- Controllers return these wrappers from `@RestController` methods

**Authentication Flow:**
1. `LoginController.login()` validates captcha and credentials
2. Shiro's `UserRealm.doGetAuthenticationInfo()` queries user via `IUserService`
3. Password verified with MD5+Salt (2 hash iterations)
4. `ActiverUser` stored in session with permissions from role-permission mapping

**Authorization:**
- `@RequiresPermissions("code:code")` annotations protect endpoints
- `UserRealm.doGetAuthorizationInfo()` loads permissions for authenticated user
- Super admin (type=0) receives `*:*` wildcard permission

**Caching:**
- `CachePool.CACHE_CONTAINER` - Static HashMap holding entity data by key pattern
- `CacheAspect` / `BusinessCacheAspect` - @Cache annotations via Spring AOP
- `CachePool.syncData()` reloads all entities from DB

**Entity Relationships:**
- Goods → Provider (many-to-one via providerid)
- Inport/Outport/Sales/Salesback → Goods + Provider/Customer (transactions)
- User → Dept (many-to-one), User ↔ Role (many-to-many)

**Database Conventions:**
- Primary keys: `id` AUTO_INCREMENT
- Soft delete: `available` flag (1=enabled, 0=disabled)
- Foreign keys: `tablenameid` format (e.g., `providerid`, `goodsid`)

## Common Development Tasks

**Adding a new entity:**
1. Create entity in `{module}/entity/` with `@TableName`
2. Create mapper extending `BaseMapper<Entity>` (no implementation needed)
3. Create service interface `IEntityService extends IService<Entity>`
4. Create service impl `EntityServiceImpl extends ServiceImpl<IEntityService, Entity>`
5. Create controller with `@RestController @RequestMapping`
6. Add XML mapper if custom queries needed (`resources/mapper/**/*Mapper.xml`)

**Front-end templates:** `src/main/resources/templates/{module}/{entity}/`
- Thymeleaf templates using LayUI components
- Table data loaded via AJAX to `/entity/loadAllEntity`

**Configuration:**
- `application.yml` - Datasource, Shiro, MyBatis-Plus settings
- Custom properties bound via `@ConfigurationProperties(prefix = "shiro")`

**API Endpoints:**
- All endpoints return JSON, no view resolution
- Pagination uses `page` and `limit` parameters in Vo classes
- Query params for filtering via MyBatis-Plus `QueryWrapper`
- Login: POST `/login/login` with `loginname`, `pwd`, `code` params
- Captcha: GET `/login/getCode`

## Important Notes

- `@Lazy` injection on services in `UserRealm` to avoid circular dependency with cache aspects
- Custom `QueryWrapper` conditions use chained builders with conditional `eq()`/`like()`
- File uploads handled via `FileController`, temp files appended with `_temp`, upload path in `file.properties`
- Druid monitor available at `/druid` (root/123456)
- Default images: `/images/noDefaultImage.jpg` (goods), `/images/defaultUserTitle.jpg` (user)