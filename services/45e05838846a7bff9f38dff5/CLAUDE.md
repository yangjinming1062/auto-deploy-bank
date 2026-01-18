# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 1. Project Overview

**林风社交论坛** (linfeng-community) is a full-stack social forum/BBS application with multi-platform support (H5, WeChat Mini Program, Android/iOS App, and web admin panel). It follows a microservices-oriented architecture with Spring Boot backend and Vue.js/UniApp frontends.

**Current Version**: V1.24.0 (Application), 3.0.0 (Maven)

**Project Links**:
- Main Site: https://www.linfengtech.cn
- Mobile Demo: https://h5.linfeng.tech
- Admin Demo: https://dev.linfeng.tech
- PC Version: https://pc.linfeng.tech
- Gitee Repo: https://gitee.com/virus010101/linfeng-community

## 2. Tech Stack

### Backend (Java)
- **Framework**: Spring Boot 2.2.4.RELEASE
- **Language**: Java 8
- **ORM**: MyBatis Plus 3.3.1
- **Database**: MySQL 8.0.17
- **Cache**: Redis
- **Security**: Apache Shiro 1.12.0 + JWT
- **Build**: Maven 3.x

### Admin Frontend (Vue 2)
- **Framework**: Vue 2.5.16
- **UI Library**: Element UI 2.8.2
- **State**: Vuex 3.0.1
- **Build Tool**: Webpack 3.6.0 + Gulp

### Mobile Frontend (UniApp)
- **Framework**: UniApp
- **UI Library**: uView UI 1.8.4

## 3. Common Development Commands

### Backend (Maven)
```bash
# Run development server
mvn spring-boot:run

# Build production JAR (skip tests)
mvn clean package -Dmaven.test.skip=true

# Run tests
mvn test

# Install dependencies
mvn clean install

# Run with specific profile
mvn spring-boot:run -Dspring-boot.run.profiles=prod
```

### Admin Panel (Vue 2)
**Location**: `src/main/resources/static/linfeng-community-vue/`

```bash
# Install dependencies (requires Node.js 8.11.1+)
npm install

# Start development server
npm run dev
# or
npm start

# Build for production
npm run build

# Run linting
npm run lint

# Run tests (unit + e2e)
npm test

# Run only unit tests
npm run unit

# Run only e2e tests
npm run e2e
```

**Note**: Node.js version must be ≤ 14 for the admin panel to work properly.

### Mobile App (UniApp)
**Location**: `src/main/resources/static/linfeng-community-uniapp-ky/`

```bash
# Install dependencies
npm install

# Build commands (run in HBuilderX or use uni-app CLI):
# - H5: Build for browser
# - WeChat Mini Program: Build for WeChat
# - App: Build for Android/iOS
```

## 4. High-Level Architecture

This is a **monorepo** containing both backend API and frontend applications:

```
┌─────────────────────────────────────────────────────────────┐
│                    linfeng-community                        │
├─────────────────────────────────────────────────────────────┤
│  Backend (SpringBoot + Maven)                              │
│  └─ src/main/java/io/linfeng/                              │
│     ├── Applications.java (Main Entry)                     │
│     ├── config/        (Config Classes)                    │
│     ├── common/        (Utilities & Annotations)           │
│     ├── datasource/    (Database Configuration)            │
│     └── modules/       (Feature Modules)                   │
│        ├── sys/        (System Management)                 │
│        ├── admin/      (Admin Panel APIs)                  │
│        ├── app/        (Mobile App APIs)                   │
│        ├── job/        (Scheduled Tasks)                   │
│        └── oss/        (File Storage)                      │
│                                                              │
│  Frontend Applications                                     │
│  ├─ linfeng-community-vue/      (Admin Panel - Vue 2)     │
│  └─ linfeng-community-uniapp-ky/ (User App - UniApp)      │
└─────────────────────────────────────────────────────────────┘
```

### Backend Module Structure

**5 Core Modules** in `/src/main/java/io/linfeng/modules/`:

1. **sys/** - System Management
   - User management, roles, permissions, menus
   - OAuth2 integration
   - Redisson operations
   - Controllers: UserController, RoleController, MenuController

2. **admin/** - Admin Panel APIs
   - Admin-specific functionality
   - Controllers: AdminController
   - DAOs, Services, Entities

3. **app/** - Mobile App APIs
   - Public-facing API controllers
   - Mobile-specific configuration
   - Custom annotations, resolvers, interceptors
   - Controllers: PostController, CircleController, CommentController, etc.

4. **job/** - Scheduled Tasks
   - Quartz-based job scheduling
   - Task implementations for background processing
   - Controllers: JobController

5. **oss/** - Object Storage Service
   - File upload/download
   - Multi-cloud storage (Qiniu, Aliyun OSS, Local)

### Configuration Files

**Backend Configs** (`/resources/`):
- `application.yml` - Main configuration
- `application-dev.yml` - Development profile
- `application-prod.yml` - Production profile
- `logback.xml` - Logging configuration

**Key Configurations** (in application.yml):
- Redis settings (database, host, port, pool)
- JWT secret and expiration
- File upload limits
- SMS settings
- Task executor pool

## 5. Development Setup Prerequisites

- **Java**: JDK 8 or higher
- **Node.js**: 8.11.1+ (≤ 14 for admin panel), 14+ recommended for mobile app
- **Redis**: 3.0+ (required - start before API)
- **MySQL**: 5.7 or higher
- **Maven**: 3.x
- **npm**: 5.6+

## 6. Key Features

- Multi-platform: H5, WeChat Mini Program, Android/iOS App
- Social features: Posts, comments, likes, follows, private messages
- Payment integration: WeChat Pay
- File storage: Multi-cloud (Qiniu, Aliyun OSS, Local)
- Security: JWT authentication, Shiro authorization
- Background jobs: Quartz-based scheduling
- Real-time communication: WebSocket
- API documentation: Swagger integration (Swagger Bootstrap UI)

## 7. Code Organization Notes

### Frontend Locations
- **Admin Panel**: `src/main/resources/static/linfeng-community-vue/`
- **User App**: `src/main/resources/static/linfeng-community-uniapp-ky/`

### Important Backend Patterns
- **Entities**: Located in each module's `entity/` directory
- **DAOs**: MyBatis Plus interfaces in `dao/` directory with XML mappers in `/resources/mapper/`
- **Services**: Business logic in `service/` with implementations in `impl/`
- **Controllers**: REST endpoints in `controller/` directory
- **Aspect-Oriented**: Custom aspects in `common/aspect/` (data source routing, logging)
- **Validation**: Custom validators in `common/validator/`

### Caching Strategy
- Redis is used extensively for performance
- Comments, likes, follows, hot posts, and circle post counts are cached
- Cache keys and strategies are module-specific

## 8. Database

- **Primary DB**: MySQL 8.0.17
- **ORM**: MyBatis Plus with XML mappers
- **Connection Pool**: Druid 1.1.13
- **Migration**: SQL files available in QQ群 (群1：640700429，群2：667859660)

## 9. Testing

- **Backend**: Maven Surefire Plugin (currently disabled by default in build)
  ```bash
  mvn test
  ```

- **Admin Panel**: Jest (unit) + Nightwatch (e2e)
  ```bash
  npm test
  ```

- **Mobile App**: No test configuration (test script placeholder only)

## 10. Build and Deployment

### Backend Build
```bash
mvn clean package -Dmaven.test.skip=true
# Generates: target/linfeng-community-3.0.0.jar
```

### Admin Panel Build
```bash
npm run build
# Uses Gulp build system
# Outputs to dist/
```

### Deployment Notes
- Redis must be started before the backend API
- Database schema must be initialized before running
- Frontend applications are served as static resources from the backend JAR
- Environment profiles: dev, test, prod

## 11. API Documentation

- Swagger UI available at: `/swagger-ui.html` (when running)
- Spring Boot banner in: `resources/banner.txt`

## 12. Important Resources

- **SQL Scripts**: Available in QQ群 files (640700429, 667859660)
- **Demo Accounts**: Pre-configured on demo sites
- **Documentation**: See README.md for version history and feature changelog
- **Open Source License**: Educational use only, not for commercial use

## 13. Troubleshooting

- **Admin panel build fails**: Check Node.js version (must be ≤ 14)
- **API won't start**: Ensure Redis and MySQL are running
- **Frontend changes not reflecting**: Clear browser cache and rebuild
- **Mobile app issues**: Use HBuilderX for proper UniApp compilation