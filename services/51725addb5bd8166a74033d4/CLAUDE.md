# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ELADMIN is a full-stack admin management system (前后端分离) built with:
- **Backend:** Spring Boot 2.7.18, Java 8, MyBatis-Plus 3.5.3.1, Spring Security + JWT, Redis + Redisson
- **Frontend:** Vue 2.7.16, Element-UI 2.15.14, Vuex, Vue Router
- **Database:** MySQL with Quartz distributed scheduler

**Docs:** https://eladmin.vip | **Demo:** https://eladmin.vip/demo (admin / 123456)

## Build Commands

### Backend (Maven)

```bash
# Build all modules (skips tests by default)
mvn clean package -DskipTests

# Build with tests
mvn clean package

# Build specific module
mvn -pl eladmin-system clean package
```

### Frontend (npm)

```bash
# Install dependencies
npm install

# Development server at localhost:8013
npm run dev

# Production build
npm run build:prod

# Staging build
npm run build:stage

# Run linting (pre-commit hooks via husky + lint-staged)
npm run lint

# Run unit tests (Jest)
npm run test:unit
```

**Node requirement:** >= 8.9 (recommended: 12+)

## Architecture

### Backend Modules (Maven multi-module)

- `eladmin-common` - Shared utilities, annotations, base entities, and global config (Redis, MyBatis-Plus, Swagger/Knife4j)
- `eladmin-system` - Main application entry point (`me.zhengjie.AppRun`), server port 8000, core modules
- `eladmin-logging` - Audit logging with AOP
- `eladmin-tools` - Third-party integrations (email, S3-compatible cloud storage, Alipay)
- `eladmin-generator` - CRUD scaffolding code generator

**Key backend packages under `eladmin-system/src/main/java/me/zhengjie/`:**
- `modules/security` - Authentication & authorization (JWT, Spring Security)
- `modules/system` - User, role, menu, department management
- `modules/quartz` - Distributed scheduled tasks
- `modules/monitor` - Server monitoring, SQL monitoring (Druid)

### Frontend Structure

- `src/api/` - REST API clients organized by feature
- `src/components/` - Reusable Vue components (Crud, Dict, Permission directives)
- `src/views/` - Page components (system, monitor, maint, tools, generator)
- `src/router/` - Dynamic routing configuration
- `src/store/` - Vuex modules for state management
- `src/utils/` - Utility functions (encryption, request handling)

**Entry:** `src/main.js` | **API Docs:** `/doc.html` (Swagger/Knife4j)

## Coding Conventions

### Backend (Java)
- Java 8 features: lambdas, streams
- Lombok for reducing boilerplate
- Fastjson2 for JSON processing (replaces Jackson)
- Custom security annotations: `@AnonymousGetMapping`, permission annotations
- Unified exception handling via `me.zhengjie.exception` package

### Frontend (Vue.js)
- Component file naming: PascalCase (e.g., `Crud.vue`)
- Other files: lowercase with hyphens
- ESLint config: single quotes, no semicolons, 2-space indentation
- Vue component limits: max 10 attributes per line

## Important Notes

### RSA Password Encryption
Frontend encrypts passwords with a public key; backend decrypts with the private key. Configuration in `application.yml`.

### Linux node-sass Installation
If node-sass fails to install:
```bash
npm install --unsafe-perm
# or
npm install --unsafe-perm node-sass
```

### Database Setup
Import SQL scripts from `/sql/`:
- `eladmin.sql` - Main schema
- `quartz.sql` - Quartz scheduler tables

### Redis Configuration
Environment variables: `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`, `REDIS_PWD`