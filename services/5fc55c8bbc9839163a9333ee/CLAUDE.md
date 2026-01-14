# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Java-based workflow engine (y9-flowable) providing business process automation capabilities. It includes form designers, process designers, and task management for full process lifecycle management. The project is part of the RiseSoft Digital Infrastructure (y9-core) ecosystem and requires it for authentication, organization, and role management.

**Tech Stack:**
- Backend: Spring Boot 2.7.10, Flowable 6.8.0, JDK 11, Maven
- Frontend: Vue 3.3.2, Vite 4.x, Element Plus, TypeScript, Pinia
- Database: MySQL 5.7/8.0, Redis 6.2+, Elasticsearch 7.9+
- Infrastructure: Nacos (config/discovery), Kafka, Druid connection pool

## Build Commands

### Backend (Maven)

```bash
# Clean and build all modules
mvn clean install -DskipTests

# Build specific module
mvn -pl y9-module-itemadmin clean install -DskipTests

# Build with specific profile
mvn clean install -DskipTests -Pdeploy-maven-central
```

### Frontend (npm)

```bash
# y9vue-itemAdmin
cd vue/y9vue-itemAdmin
npm install
npm run serve          # Development mode
npm run serve-local    # Local environment mode
npm run build          # Production build
npm run build-dev      # Development build
npm run build-local    # Local environment build

# y9vue-flowableUI
cd vue/y9vue-flowableUI
npm install
npm run serve          # Development mode
npm run serve-local    # Local environment mode
npm run build          # Production build
npm run build-dev      # Development build
npm run build-local    # Local environment build

# Optimize SVG icons
npm run svgo
```

## Architecture

### Module Structure

The project follows a layered architecture with Maven multi-module structure:

```
y9-flowable (root)
├── y9-module-flowableui    # Workflow UI and user interface
├── y9-module-itemadmin     # Task/item administration
├── y9-module-processadmin  # Process definition and management
└── y9-module-jodconverter  # Document preview service
```

### Common Module Sub-Pattern

Each feature module follows this pattern:

| Module Type | Purpose |
|------------|---------|
| `risenet-y9boot-api-feignclient-*` | Feign client for microservices API calls |
| `risenet-y9boot-api-interface-*` | REST API interface definitions |
| `risenet-y9boot-model-*` | JPA entities and data models |
| `risenet-y9boot-support-*-jpa-repository` | Spring Data JPA repositories |
| `risenet-y9boot-support-*` | Business layer (services + controllers) |
| `risenet-y9boot-webapp-*` / `risenet-y9boot-server-*` | Spring Boot application entry points |

### Code Organization (Java)

- **Controllers**: `net.risesoft.controller` - REST endpoints
- **Services**: `net.risesoft.service` - Business logic with interface/impl pattern
- **Repositories**: `net.risesoft.repository` / `net.risesoft.flowable.repository` - Data access
- **Entities**: `net.risesoft.entity` (tenant-specific) or `net.risesoft.y9public.entity` (shared)
- **Configuration**: `net.risesoft.y9.configuration`

### Frontend Organization (Vue)

- Components: `src/components` and plugin-based components (`y9plugin-*`)
- Views/Pages: `src/views` (28+ feature directories)
- State Management: Pinia stores in `src/store`
- Routing: Vue Router configuration in `src/router`
- API Services: Axios-based services in `src/api`
- Internationalization: `src/language` for i18n support
- Theming: `src/theme` for multi-theme support (default, green, blue, dark)
- Layouts: `src/layouts` for main application layout
- Process Modeling: BPMN.js 8.10.0 for browser-based BPMN editing

## External Dependencies

**Required External Services:**
- Nacos (v2.2.1) - Configuration and service discovery at `https://test.youshengyun.com:443`
- y9-core digital base - Authentication and organization management
- Kafka - Event streaming for multi-tenant events
- Redis - Caching and sessions
- MySQL - Primary database

**Key Configuration:** Configuration is primarily managed through Nacos. Local `application.yml` files define connection properties and feature toggles.

## Key Conventions

- Controller classes use `*RestController` or `*Controller` naming
- Service interfaces and implementations follow `*Service` / `*ServiceImpl` pattern
- JPA entities use `* PO` or `*Entity` naming with `Y9` prefix for tenant-specific entities
- REST APIs use context paths (e.g., `/server-flowableui`, `/server-itemadmin`)
- All modules inherit from `net.risesoft:y9-digitalbase` parent POM
- Multi-tenant support via Kafka events for cross-service synchronization
- 三员管理 (three-role management) for security compliance
- Path alias `@` maps to `src` in frontend projects

## Reference Documentation

- [Java开发规范手册](https://vue.youshengyun.com/files/内部Java开发规范手册.pdf)
- [Vue开发手册v1.0](https://vue.youshengyun.com/files/有生博大Vue开发手册v1.0.pdf)
- [工作流源码部署文档](https://vue.youshengyun.com/files/工作流源码部署文档.pdf)
- [API Documentation](https://docs.youshengyun.com/)

## Database Schema

The system uses multi-tenant database isolation with:
- `y9_public` - Shared public entities and configurations
- Tenant-specific tables identified by `TENANTID_` prefix or `tenantId` column
- Flowable tables prefixed with `ACT_` for process engine tables