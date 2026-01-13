# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Micro-Service-Skeleton** is a Spring Cloud-based microservices foundation framework implementing OAuth 2.0 with JWT authentication and dynamic permission control. It provides a complete user-role-permission management system with URL-level access control.

**Documentation**: See README.md for detailed architecture explanation and implementation details.

## Architecture

This is a Maven multi-module project with the following structure:

```
Micro-Service-Skeleton-Parent (2.0.0)
├── mss-common          # Shared utilities, VO classes, constants
├── mss-oauth (uaa)     # Authentication center - OAuth 2.0 + JWT + Spring Security
├── mss-gateway         # API Gateway - Spring Cloud Gateway with JWT validation
├── mss-upms            # User Permission Management Service - RBAC management
└── mss-monitor         # Monitoring service - Actuator + Hystrix
```

### Module Dependencies

- **mss-common**: Shared across all modules (JWTConstants, Result, UserVo, RoleVo, MenuVo, Authority, Md5Utils, StatusCode)
- **mss-oauth**: Depends on mss-common, provides authentication services
- **mss-gateway**: Depends on mss-common, routes requests and validates JWT tokens
- **mss-upms**: Depends on mss-common, manages users/roles/permissions, uses MyBatis-Plus
- **mss-monitor**: Standalone monitoring with Hystrix circuit breaker

### Core Technologies

- **Spring Boot**: 2.2.10.RELEASE
- **Spring Cloud**: Hoxton.SR8
- **Spring Cloud Alibaba**: 2.2.1.RELEASE
- **Nacos**: 1.3 (service discovery & config)
- **JWT**: nimbus-jose-jwt 9.1.1
- **Spring Security**: OAuth 2.0 + JWT authentication
- **Database**: MySQL with Druid connection pool
- **ORM**: MyBatis Plus 2.2.0 + TK MyBatis 2.0.4
- **Cache**: Redis (session & permission storage)
- **Gateway**: Spring Cloud Gateway with WebFlux
- **API Documentation**: Swagger 2.9.2
- **Circuit Breaker**: Hystrix

### Authentication Flow

1. **Login** (`/login`): User credentials → mss-oauth → JWT token generated → Stored in Redis
2. **Gateway Validation**: All requests → AuthFilter → JWT verification → Permission check → Route to service
3. **Permission Model**: User → Roles → Permissions (URL-based)
4. **Dynamic Revocation**: Role/permission changes → Clear Redis cache → Force re-authentication

**Key Classes**:
- `mss-oauth`: WebSecurityConfig, UserDetailsServiceImpl, JWTAuthenticationFilter, JWTAuthorizationFilter
- `mss-gateway`: AuthFilter (GlobalFilter), ExclusionUrl config
- `mss-common`: JWTConstants, Result<T>, UserVo, RoleVo, MenuVo, Authority

### External Dependencies

**Required Infrastructure** (all default to localhost):
- **Nacos Server**: 127.0.0.1:8848 (discovery & config)
- **MySQL**: Default port 3306, database `zuul-auth`
- **Redis**: 127.0.0.1:6379, password `123456`

Database schema located at `/other/db/zuul-auth.sql` includes:
- OAuth tables: `oauth_client_details`, `oauth_access_token`, `oauth_refresh_token`
- RBAC tables: `sys_user`, `sys_role`, `sys_menu`, `sys_user_role`, `sys_privilege`
- Default users: admin/test1/test2 (password: same as username, BCrypt hashed)

## Development Commands

### Build & Test

```bash
# Build all modules
mvn clean install -DskipTests

# Build specific module
mvn clean install -pl mss-gateway -am

# Run tests (note: surefire plugin is configured to skip tests by default)
mvn test

# Run tests for specific module
mvn test -pl mss-upms

# Skip tests and build
mvn clean package -DskipTests
```

### Run Services

Each module has a `@SpringBootApplication` main class:

```bash
# Start Authentication Center (mss-oauth)
cd mss-oauth && mvn spring-boot:run

# Start Gateway (mss-gateway)
cd mss-gateway && mvn spring-boot:run

# Start User Permission Management (mss-upms)
cd mss-upms && mvn spring-boot:run

# Start Monitor (mss-monitor)
cd mss-monitor && mvn spring-boot:run
```

**Default Ports**:
- uaa (mss-oauth): 8080 (configured in application.yml)
- mss-gateway: Gateway default (check application.yml)
- mss-upms: 8081 (configured in application.yml)
- mss-monitor: check application.yml

### Database & Code Generation

**Initialize Database**:
```bash
# Import SQL schema
mysql -u root -p < other/db/zuul-auth.sql
```

**Generate MyBatis Files** (mss-upms):
```bash
cd mss-upms
mvn mybatis-generator:generate
```

Configuration: `src/test/resources/generatorConfig.xml`

### Configuration

Each module uses:
- `bootstrap.yml`: Nacos config (application name, Nacos server address)
- `application.yml`: Module-specific config (Redis, database, routing, exclusions)

**Configuration Files**:
- mss-gateway: `src/main/resources/application.yml` - Gateway routes, exclusion URLs, Redis config
- mss-oauth: `src/main/resources/bootstrap.yml` + `application.yml` - OAuth config, Nacos
- mss-upms: `src/main/resources/bootstrap.yml` + `application.yml` - Database config, Nacos

### Important Configuration Values

**Gateway Exclusion URLs** (mss-gateway/application.yml):
- `/goods-center/goods/list`
- `/goods-center/goods/detail`
- `/uaa/login`

**JWT Token Expiry**: 2 hours (hardcoded in JWTAuthenticationFilter)

**Redis Key Format**: `JWT{userId}:{MD5(jwtToken)}` with suffix `:Authorities`

## Key Implementation Details

### Permission System

The system implements URL-level permissions through:
1. **Database**: `sys_menu.url` stores endpoint patterns
2. **Authentication**: Spring Security UserDetails with authorities from DB
3. **Gateway Validation**: AntPathMatcher compares request path against user's authorities
4. **Dynamic Updates**: Clearing Redis keys forces re-authentication

### Service Discovery

All services register with Nacos with these application names:
- `uaa` (mss-oauth)
- `gateway` (mss-gateway)
- `mss-upms`
- `mss-monitor`

### API Documentation

Swagger 2.0 available at (when running):
- mss-upms: `http://localhost:8081/swagger-ui.html`

## Common Tasks

### Adding a New Service

1. Create module directory with `pom.xml` inheriting parent
2. Add Nacos discovery dependency
3. Create `bootstrap.yml` with application name and Nacos config
4. Register with mss-common for shared classes
5. Implement main Application class
6. Add database schema if needed

### Modifying Permissions

1. Update `sys_menu` table with new URL patterns
2. Assign menus to roles in `sys_privilege`
3. Assign roles to users in `sys_user_role`
4. Clear relevant Redis keys to force re-authentication

### Testing Authentication

```bash
# Login to get JWT token
curl -X POST http://localhost:8080/login \
  -d "username=admin&password=admin"

# Use token to access protected resource
curl -H "Authorization: Bearer {token}" \
  http://localhost:8080/mss-upms/order/list
```

### Debugging JWT Issues

1. Check token format (Bearer prefix)
2. Verify token hasn't expired (2-hour TTL)
3. Check Redis contains user authorities
4. Confirm user has required role/permissions in DB

## Notes

- **Java Version**: 1.8
- **Test Framework**: JUnit 5 (spring-boot-starter-test)
- **Maven Compiler**: Configured to use Java 1.8
- **MyBatis Generator**: Available in mss-upms for code generation
- **Lombok**: Used throughout for getters/setters/logging
- **Session Management**: Stateless (SessionCreationPolicy.STATELESS)