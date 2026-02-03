# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BeiDou-Server is a MapleStory game server written in Java (backend) with a Vue.js web admin panel. It is forked and optimized from Cosmic. The project consists of two main modules:

- **gms-server**: Spring Boot 3.2.3 + Netty game server (Java 21)
- **gms-ui**: Admin web interface (Vue 3 + Arco Design)

## Common Commands

### Server (gms-server)
```bash
# Requires MySQL 8 running first
cd gms-server
mvn clean package -DskipTests  # Build JAR
java -jar target/BeiDou.jar    # Run server

# API docs available at http://localhost:8686/swagger-ui/index.html
```

### Frontend (gms-ui)
```bash
cd gms-ui
yarn install          # Install dependencies (use Node v20.15.0)
yarn dev              # Start dev server (http://localhost:8787)
yarn build            # Production build
yarn type:check       # TypeScript type check
```

## Architecture

### Server Structure (`gms-server/src/main/java/org/gms/`)

- **`net/`**: Network layer using Netty - handles client connections, packet encoding/decoding, and opcode management
- **`server/`**: Game server logic including maps, skills, inventory, quests, NPCs, and mobs
- **`controller/`**: REST API controllers following API versioning convention in `constants/api/ApiConstant.java`
- **`dao/`**: MyBatis-Flex mappers and entities for database access
- **`scripting/`**: GraalJS script engine for quest/event scripts
- **`constants/`**: Game constants, opcodes, and enums
- **`config/`**: Spring configuration classes
- **`provider/`**: WZ data providers (game assets like items, maps, skills)
- **`aop/`**: AOP filters and interceptors (e.g., `ServerFilter` for API security)

### Frontend Structure (`gms-ui/src/`)

- **`views/`**: Page components organized by feature (account, dashboard, game)
- **`router/`**: Vue Router configuration with guards
- **`api/`**: API client functions
- **`store/`**: Pinia state management
- **`components/**: Reusable UI components
- **`config/`**: Vite and build configuration
- **`locale/**: i18n translations

### API Versioning

REST APIs use versioned endpoints. Controllers use `ApiConstant.LATEST` (currently `v1`) as base path. To create a new version:
1. Add new constants in `ApiConstant.java` (e.g., `V2 = "v2"`)
2. Update `LATEST` to point to the new version
3. For breaking changes, explicitly annotate old controllers with specific version tags

### Database

- MySQL 8 with Flyway for migrations
- Auto-creates database on startup if it doesn't exist
- Uses Druid connection pool
- MyBatis-Flex for ORM

### Key Configurations

- Server port: 8686 (API), 8484 (login)
- Frontend dev port: 8787
- JWT authentication (30min expiry by default)
- WZ data and scripts support i18n: `wz-zh-CN`, `wz-en-US`, etc.