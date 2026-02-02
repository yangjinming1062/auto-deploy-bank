# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

QConfig is a configuration management center by Qunar that provides centralized configuration management with real-time updates. The system consists of multiple components:

- **Server** - HTTP server that serves configurations and notifies clients of changes via long-polling
- **Admin** - Web UI for configuration management, publishing, and权限管理
- **Client** - Java client library that applications use to consume configurations
- **Common** - Shared beans, utilities, and application authentication interfaces
- **Server-Common** - Shared code between Server and Admin modules

## Build Commands

```bash
# Build all modules
mvn clean install

# Run all tests
mvn test

# Run tests in a specific module
mvn -pl <module> test

# Build a specific module with dependencies (e.g., client)
mvn -pl client -am install

# Skip tests during build
mvn clean install -DskipTests
```

## Architecture

### Data Flow
1. Users publish configurations through the Admin UI
2. Admin notifies all Server instances via HTTP
3. Servers maintain long-polling connections with Clients
4. Servers push configuration updates to Clients in real-time

### Server Design
- Uses **Eureka** for service discovery and coordination between server instances
- Two-level caching: memory cache (hot data) + disk cache (persisted data)
- Clients maintain persistent connections for real-time updates via **Netty**
-无状态的读设计，支持水平扩展

### Key Dependencies
- Spring Framework 4.3.x (MVC, JDBC, Security)
- MySQL with Tomcat JDBC connection pool
- Netty for HTTP long-polling
- Eureka 1.7.x for service discovery
- Jersey for REST APIs
- Logback for logging

## Development Setup

### Database Setup
Import schema from `admin/sql/main.sql` into MySQL. Optionally import `admin/sql/QConfig_data.sql` for sample configurations.

### Local Development (see doc/devStart.md for details)

1. **Start Server**:
   - Configure database in `common/src/main/resources/default.conf`
   - Run as Tomcat Server in IDE with JVM args: `-Dqconfig.server=IP:PORT`

2. **Start Admin**:
   - Run as Tomcat Server in IDE
   - Default credentials: `admin` / `123456`

3. **Client Development**:
   - Create `qconfig_test/{appCode}/` directory with config files in resources
   - Or specify server via: `-Dqconfig.server=IP:PORT`

### Configuration Files
- `common/src/main/resources/default.conf` - Server list and environment symbols
- Environment-specific configs use `qconfig_test/` directory in resources

## Module Structure

| Module | Packaging | Purpose |
|--------|-----------|---------|
| common | jar | Shared beans, utilities, ServerManagement interface |
| server-common | jar | Server/Admin shared code, DAOs, services |
| server | war | Config serving HTTP server with Eureka |
| admin | war | Web UI for config management |
| client | jar | Client library for consuming configs |
| demo | war | Example application using the client |