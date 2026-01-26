# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

开放签 (OpenSign) is an electronic signature platform providing contract creation, signing, management, and verification. The system supports personal and enterprise identity verification, seal management, contract template configuration, and signing workflow control.

### Core Modules

**Backend (kaifangqian-parent):**
- `kaifangqian-tools` - Utility modules (ID generation, job scheduling, messaging, PDF processing)
- `kaifangqian-core` - Core framework (Shiro + JWT auth, MyBatis-Plus, Redisson, file storage)
- `kaifangqian-system` - Main application containing business logic modules

**Frontend (kaifangqian-web):**
- `opensign-web` - Main signing application (Vue 3 + Vite micro-frontend with qiankun)
- `opensign-manage` - Admin dashboard
- `opensign-mobile` - Mobile H5 app
- `opensign-tenant` - Tenant management portal
- `opensign-message` - Message service

## Build Commands

### Backend
```bash
cd kaifangqian-parent
mvn install              # Build all modules
cd kaifangqian-system
mvn spring-boot:run      # Run with dev profile
mvn test                 # Run tests (skipTests=false in parent pom)
```

### Frontend
```bash
cd kaifangqian-web/opensign-web
pnpm install             # Install dependencies
npm run dev              # Development server
npm run build            # Production build
npm run build:test       # Test environment build
npm run type:check       # TypeScript type checking
```

**Note:** PowerJob server (4.0.1) must be running before starting the backend application.

### Linting
```bash
# Frontend linting
npm run lint:eslint      # ESLint with auto-fix
npm run lint:prettier    # Prettier formatting
npm run lint:stylelint   # Style linting
npm run lint:lint-staged # Run all linters on staged files
```

### Production Frontend Deployment
All frontend apps (except handwriting and nginx-config) need to be built, then copied to `opensign-web/dist/opensign-web` and deployed via Nginx.

## Key Configuration

- **Backend config:** `kaifangqian-parent/kaifangqian-system/src/main/resources/application-prod.yml`
- **Environment variables:** MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USERNAME, MYSQL_PASSWORD, REDIS_HOST, REDIS_DATABASE
- **File storage:** Configure path in `file.{mac,linux,windows}.path` - fonts (simsun.ttc, simkai.ttf, simhei.ttf, simfang.ttf) must be installed or印章 images will be blank

## Database

- **Location:** `kaifangqian-parent/sql/opensign.sql`
- **Required:** MySQL 5.7+ or 8.0.27+
- **Includes:** PowerJob tables and initial data

## Technology Stack

- **Backend:** Java 8, Spring Boot 2.7.18, Shiro 1.13.0, MyBatis-Plus 3.5.8, Redisson 3.51.0
- **Frontend:** Vue 3.2.33, Vite 2.9, Ant Design Vue 3.2, Pinia, Vue Router, qiankun micro-frontend
- **PDF Processing:** Apache PDFBox 3.0.5, JasperReports 6.20.5, OFDRW (OFD format)
- **Cryptography:** BouncyCastle (RSA/SM2 digital signatures)

## Important Notes

- **JDK version:** Must use JDK 1.8+ (less than JDK 17)
- **Development:** IntelliJ IDEA with Lombok plugin required
- **Binary files:** Fonts, certificate files (.pfx, .jks) are excluded from Maven resource filtering
- **API context path:** `/resrun-paas`
- **Default port:** 8899
- **Tests:** Backend tests are skipped by default (`mvn test -DskipTests=false` to run)

## Architecture Highlights

- **Authentication:** Shiro + JWT with Redis session storage via shiro-redis
- **Multi-tenancy:** Platform supports multiple enterprises with data isolation
- **Business lines:** Configurable signing workflows (contracts, insurance, tenders, etc.)
- **Three-role seal separation:** 管理权 (management), 使用权 (usage), 审计权 (audit) for seal operations