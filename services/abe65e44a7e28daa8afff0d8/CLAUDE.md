# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

king-admin is a前后端分离的基础权限管理后台 with separate frontend (AngularJS 1.x) and backend (Spring Boot) projects.

## Frontend (king-admin-angularjs)

### Commands

```bash
cd king-admin-angularjs

# Install dependencies (requires bower for frontend assets)
npm install -g gulp cnpm bower
cnpm install
bower install

# Development server with live reload (port 5000)
gulp serve

# Build for production (outputs to static/)
gulp

# Linting
gulp scripts
```

### Architecture

```
src/
├── app/
│   ├── app.js                 # Main Angular module (KingAdmin)
│   ├── pages/
│   │   ├── pages.module.js    # Pages router module
│   │   ├── config/            # Auth interceptor, state handler, permissions
│   │   ├── home/              # Dashboard page with widgets
│   │   ├── sys/               # System management (user, role, menu)
│   │   ├── dict/              # Dictionary management
│   │   ├── charts/            # Chart pages
│   │   └── common/            # Shared components
│   └── theme/
│       ├── components/        # UI components
│       ├── directives/        # Custom directives
│       ├── filters/           # Custom filters
│       └── services/          # Theme services
├── sass/                      # SCSS stylesheets
└── assets/                    # Static assets
```

**Main modules:** `KingAdmin` (root), `KingAdmin.pages`, `KingAdmin.theme`

**Key dependencies:** Angular 1.4.8, ui-router, Bootstrap 3.3.5, smart-table, xeditable, Chart.js, toastr

**Proxy routes:** `/api`, `/sys`, `/druid`, `/management` (proxied to backend on port 8080)

## Backend (king-admin-java)

### Commands

```bash
cd king-admin-java

# Build
mvn install -Dmaven.test.skip=true

# Run
mvn spring-boot:run
# Or run KingAdminJavaApplication.java directly
```

### Architecture

```
src/main/java/com/oukingtim/
├── KingAdminJavaApplication.java  # Spring Boot entry point
├── config/                        # Shiro, Mybatis, Druid configuration
├── domain/                        # Entity classes
├── mapper/                        # MyBatis mappers
├── service/                       # Business logic layer
│   └── impl/                      # Service implementations
├── web/                           # REST controllers
│   └── vm/                        # View models/Request objects
└── util/                          # Utility classes
```

**Key dependencies:** Spring Boot 1.5.4, MyBatis-Plus, Shiro 1.3.2, Druid, MySQL, fastjson

## Database

Run `king-admin.sql` in MySQL to initialize the database schema.

## Running Full Stack

1. Start backend: `cd king-admin-java && mvn spring-boot:run` (port 8080)
2. Start frontend: `cd king-admin-angularjs && gulp serve` (port 5000)
3. Access at http://localhost:5000

## Deployment

Build frontend with `gulp` to generate static files in `static/`, then copy to backend's `src/main/resources/static/` for combined deployment.