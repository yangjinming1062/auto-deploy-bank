# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

21-Points Health is a health monitoring application generated with JHipster 7.9.3. It tracks blood pressure, weight, and points for a gamified health experience.

## Development Commands

### Backend (Gradle)
```bash
./gradlew -x webapp                    # Start backend without rebuilding frontend
./gradlew test                         # Run unit tests (excludes integration tests)
./gradlew integrationTest             # Run integration tests
./gradlew test integrationTest        # Run both unit and integration tests
./gradlew -Pprod clean bootJar        # Build production JAR
./gradlew checkstyleNohttp            # Run checkstyle
```

### Frontend (npm/Angular)
```bash
npm install                            # Install dependencies
npm start                              # Start dev server with HMR (port 4200)
npm run lint                           # Run ESLint
npm run lint:fix                       # Fix linting issues automatically
npm test                               # Run Jest unit tests
npm run test -- --watch               # Run tests in watch mode
npm run e2e                            # Run Cypress E2E tests (requires running backend)
npm run prettier:format               # Format code with Prettier
```

### Combined Development
```bash
./gradlew -x webapp && npm start      # Run both backend and frontend dev servers
npm run build-watch                   # Build with watch mode + backend
```

### Docker Services
```bash
docker-compose -f src/main/docker/postgresql.yml up -d    # Start PostgreSQL
docker-compose -f src/main/docker/elasticsearch.yml up -d # Start Elasticsearch
```

## Architecture

### Backend (Java/Spring Boot)
Standard JHipster package structure in `src/main/java/org/jhipster/health/`:

- **config/** - Spring configuration classes (Security, Database, Cache, etc.)
- **domain/** - JPA entities with Elasticsearch annotations
- **repository/** - Spring Data JPA repositories + Elasticsearch search repos
- **service/** - Business logic layer, DTOs, mappers
- **web/rest/** - REST controllers, error handling, ViewModels (vm/)
- **security/** - JWT authentication, user details, authorities

### Frontend (Angular 14)
Angular modules in `src/main/webapp/app/`:

- **account/** - User registration, login, password management, settings
- **admin/** - Health checks, metrics, logs, configuration, user management
- **entities/** - BloodPressure, Points, Preferences, Weight entities
- **home/** - Landing page
- **layouts/** - Main shell, navbar, footer, error pages
- **core/** - Interceptors, services, guards, configuration
- **shared/** - Shared components, language translation, models

### Database & Search
- **Liquibase** for database migrations (`src/main/resources/config/liquibase/`)
- **PostgreSQL** for production, **H2** for development/testing
- **Elasticsearch** integration for full-text search on entities

### Key Technologies
- **Spring Security** with JWT tokens for authentication
- **Spring Data JPA** with declarative repository pattern
- **MapStruct** for entity-DTO mapping
- **ngx-webstorage** for local storage session management
- **JHipster generated tests** using ArchUnit for architectural validation

## Important Conventions

### REST Resources
- Use `@Transactional` on controller classes (not methods)
- Follow JHipster naming: `ENTITY_NAME` constant, `create/update/delete` methods
- Use `BadRequestAlertException` for validation errors
- Elasticsearch indexing happens on entity create/update via SearchRepository

### Frontend Components
- Component selector prefix: `jhi` (kebab-case)
- Directive selector prefix: `jhi` (camelCase attribute)
- Use services for API communication, stored in `core/services` or entity folders
- Jest tests co-located with components: `*.component.spec.ts`

### Testing
- Backend integration tests end with `IT` suffix
- Jest tests use `jest-preset-angular` with ts-jest
- Cypress E2E tests in `src/test/javascript/cypress/`