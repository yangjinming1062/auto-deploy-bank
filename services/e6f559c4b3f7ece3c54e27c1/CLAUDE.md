# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Apollo is a reliable configuration management system for microservices architecture. It's a Java Spring Boot-based multi-module Maven project with four main services:

- **apollo-configservice**: Configuration service that serves configuration to clients
- **apollo-adminservice**: Admin service for configuration management and administration
- **apollo-portal**: Web UI portal for managing configurations
- **apollo-assembly**: Assembly module that runs all services together for development

## High-Level Architecture

The project follows a modular microservices architecture:

```
apollo-assembly (bootstrap)
    ├── apollo-configservice (port 8080)
    ├── apollo-adminservice (port 8090)
    └── apollo-portal (port 8070)
```

Additional support modules:
- **apollo-common**: Shared utilities and common components
- **apollo-biz**: Business logic layer
- **apollo-audit**: Audit logging functionality (4 sub-modules)
- **apollo-buildtools**: Build tools and code style templates
- **apollo-build-sql-converter**: SQL conversion utilities

The system uses Spring Boot with Spring Cloud, Eureka for service discovery, and requires a MySQL database.

## Common Development Commands

### Build Commands
```bash
# Build all modules without running tests
./mvnw clean package -DskipTests

# Build specific modules with dependencies
./mvnw clean package -pl apollo-configservice,apollo-adminservice -am -DskipTests

# Build for release (used by build.sh script)
./mvnw clean package -DskipTests -pl apollo-configservice,apollo-adminservice -am -Dapollo_profile=github -Dspring_datasource_url=$url -Dspring_datasource_username=$user -Dspring_datasource_password=$pass
```

### Test Commands
```bash
# Run all tests
./mvnw test

# Run a single test class
./mvnw test -Dtest=ConfigServiceTest

# Run a specific test method
./mvnw test -Dtest=ConfigServiceTest#testReleaseConfig

# Run tests for specific module
./mvnw test -pl apollo-configservice

# Run with more verbose output
./mvnw test -Dverbose=true
```

### Code Quality
```bash
# FindBugs static analysis
./mvnw findbugs:check

# Generate FindBugs report
./mvnw findbugs:findbugs

# Check for dependency updates
./mvnw versions:display-dependency-updates
./mvnw versions:display-plugin-updates
```

## Local Development

### Starting Apollo for Development

The recommended approach is to run `apollo-assembly` in your IDE:

**Main class**: `com.ctrip.framework.apollo.assembly.ApolloApplication`

**Required VM options**:
```
-Dapollo_profile=github,auth
```

**Optional VM options** (for MySQL instead of H2):
```bash
-Dspring.config-datasource.url=jdbc:mysql://your-mysql-server:3306/ApolloConfigDB?useUnicode=true&characterEncoding=UTF8
-Dspring.config-datasource.username=apollo-username
-Dspring.config-datasource.password=apollo-password
-Dspring.portal-datasource.url=jdbc:mysql://your-mysql-server:3306/ApolloPortalDB?useUnicode=true&characterEncoding=UTF8
-Dspring.portal-datasource.username=apollo-username
-Dspring.portal-datasource.password=apollo-password
```

**Optional log file location**:
```
-Dlogging.file.name=/your-path/apollo-assembly.log
```

### Access Points After Startup
- ConfigService: http://localhost:8080 (health check: /health)
- AdminService: http://localhost:8090 (health check: /health)
- Portal UI: http://localhost:8070 (default credentials: apollo/admin)

### Running Individual Services

If you prefer to run services independently instead of via assembly:

- **Portal**: `com.ctrip.framework.apollo.portal.PortalApplication`
- **ConfigService**: `com.ctrip.framework.apollo.configservice.ConfigServiceApplication`
- **AdminService**: `com.ctrip.framework.apollo.adminservice.AdminServiceApplication`

## Code Style

The project follows [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html).

Code style templates are available in `apollo-buildtools/style/`:
- `intellij-java-google-style.xml` - IntelliJ IDEA
- `eclipse-java-google-style.xml` - Eclipse

All new Java files should have a simple Javadoc class comment. Conventional commits format is used - see [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

## Module Dependencies

Module dependency structure (lowest to highest):
```
apollo-buildtools
apollo-common
apollo-build-sql-converter
    → apollo-common
apollo-audit-* (4 sub-modules)
    → apollo-common
apollo-biz
    → apollo-common, apollo-audit-*
apollo-configservice
    → apollo-biz, apollo-common
apollo-adminservice
    → apollo-biz, apollo-common
apollo-portal
    → apollo-biz, apollo-common
apollo-assembly
    → all above modules
```

## Configuration Files

Key configuration files:
- Root `pom.xml`: Main project configuration, dependency management
- Module `pom.xml` files: Individual module dependencies and build configuration
- `src/main/resources/application.yml` (per module): Spring Boot configuration
- Database initialization scripts: `scripts/sql/profiles/mysql-default/`

## Database Setup

For full development, you'll need MySQL 5.6.5+ with two databases:
- ApolloConfigDB: Stores configuration data
- ApolloPortalDB: Stores portal metadata

SQL initialization scripts are in `scripts/sql/profiles/mysql-default/`:
- `apolloconfigdb.sql`: Config service database
- `apolloportaldb.sql`: Portal database

Alternatively, use H2 in-memory database for simpler local development.

## Testing

The project uses JUnit 5 (Jupiter) for testing with JUnit Vintage for backward compatibility. Tests are located in `src/test/java` directories.

Test resources are in `src/test/resources` with configuration files and JSON fixtures for testing (e.g., `apollo-biz/src/test/resources/json/`).

## Deployment

Production build script: `scripts/build.sh`

This script:
1. Packages apollo-configservice and apollo-adminservice with GitHub profile
2. Packages apollo-portal with GitHub and auth profiles

Docker images can be built with:
```bash
mvn docker:build -pl apollo-configservice,apollo-adminservice,apollo-portal
```

## Important Notes

- Java 8+ required
- Project uses Maven wrapper (`./mvnw`) - no need to install Maven locally
- Default profile is `github` for database configuration
- Add `auth` profile for simple authentication (added in 0.9.0+)
- Assembly module is for development only - production deployments use individual services
- Log files default to `/opt/logs/[service-name].log` in production
- Uses Eureka for service registration/discovery
- Audit logging is available via apollo-audit modules
- Spring Boot 2.7.x and Spring Cloud 2021.x

## Documentation

- Development guide: `docs/en/contribution/apollo-development-guide.md`
- Deployment guides: `docs/en/deployment/`
- Design documents: `docs/en/design/`
- Client SDK guides: `docs/en/client/`
- User guide: `docs/en/portal/apollo-user-guide.md`

## Release Process

See `docs/en/contribution/apollo-release-guide.md` for complete release procedures. Quick reference:
1. Update version numbers
2. Validate changes
3. Create Git tag
4. Build packages using `scripts/build.sh`
5. Create GitHub release
6. Publish Docker images
7. Update Helm charts
8. Announce release