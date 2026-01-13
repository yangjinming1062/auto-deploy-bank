# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-level Architecture

CacheCloud is a Java-based Redis cloud management platform built with Spring Boot. It follows a multi-module Maven project structure:

- `cachecloud-parent`: The parent POM, defining common dependencies and build configurations.
- `cachecloud-web`: The main web application, packaged as a WAR file. It includes the frontend (Freemarker templates) and backend logic for managing Redis instances.
- `cachecloud-custom`: A module for custom extensions and integrations.
- `redis-ecs`: Likely related to Redis deployment on ECS.

The application uses a MySQL database to store metadata about Redis instances, applications, users, and monitoring data. The database schema is versioned with SQL scripts in the `cachecloud-web/sql` directory.

## Common Commands

### Building

The project is built using Maven. To build the entire project, run:

```bash
mvn clean install
```

### Running

The application can be run as a Spring Boot application. The main class is `com.sohu.cache.ApplicationStarter`.

### Testing

Tests are written using JUnit and can be run with Maven:

```bash
mvn test
```
