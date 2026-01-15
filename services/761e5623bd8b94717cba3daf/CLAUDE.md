# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FlyFish (飞鱼) is a data visualization coding platform. Users can create data models quickly and generate visualization solutions through drag-and-drop. The platform consists of 4 microservices:

| Service | Port | Technology |
|---------|------|------------|
| lcapWeb | 8089 | React frontend, nginx static resources |
| lcapCodeServer | 8081 | Online code editor (VS Code-based) |
| lcapServer | 7001 | Egg.js Node.js backend |
| lcapDataServer | 18532 | Spring Boot Java data source service |

## Build Commands

### Frontend (lcapWeb)
```bash
cd lcapWeb
npm install                    # Install dependencies
npm start                      # Development server (port 8089)
npm run build                  # Build for production (outputs to dist/)
npm run analyze               # Analyze bundle size
npm run build-omp             # OMP-specific build
```

### Backend (lcapServer)
```bash
cd lcapServer
npm install
npm run dev                   # Development mode with hot reload
npm run debug                 # Debug mode
npm run build                 # Build changelog
```

### Data Server (lcapDataServer)
```bash
cd lcapDataServer
mvn clean package -Dmaven.test.skip=true  # Build JAR
mvn spring-boot:run                         # Run in dev mode
mvn package -P prod                         # Production build
```

## Architecture

### Frontend (lcapWeb)
- **Framework**: React 16.14 with single-spa micro-frontend framework (Qiankun)
- **State Management**: @chaoswise/cw-mobx (MobX wrapper)
- **Styling**: styled-components, less, CSS modules
- **Routing**: react-router-dom v5
- **API**: @chaoswise/request (axios wrapper)
- **UI Components**: @chaoswise/ui (Ant Design-based)

**Key Directories:**
- `src/pages` - Page components
- `src/components` - Reusable components
- `src/stores` - MobX stores (namespace-based pattern)
- `src/hooks` - Custom React hooks
- `src/services` - API service layer
- `src/config` - Router and micro-app configuration

**State Store Pattern:**
```javascript
// Store definition uses namespace, state, effects, reducers, computeds
export default {
  namespace: 'storeName',
  state: { count: 0 },
  effects: { *asyncAction() { /* async logic */ } },
  reducers: { increment(state) { state.count++ } },
  computeds: { double() { return state.count * 2 } }
};
```

### Backend (lcapServer)
- **Framework**: Egg.js (Node.js)
- **Database**: MongoDB with Mongoose ODM
- **Validation**: Joi (egg-joi)
- **HTTP Client**: axios (egg-axios)
- **Authentication**: JWT (jsonwebtoken 7.4.1)

**Key Directories:**
- `app/controller` - Request handlers
- `app/service` - Business logic
- `app/model` - MongoDB schemas
- `app/middleware` - Custom middleware
- `app/router.js` - Route definitions

### Data Server (lcapDataServer)
- **Framework**: Spring Boot 2.3.12
- **Build**: Maven multi-module
- **Modules**: lcap-api, lcap-server

**Supported Data Sources:** MySQL, PostgreSQL, ClickHouse, SQL Server, Oracle, MariaDB, Dameng, Elasticsearch, Kafka

**Key Directories:**
- `lcap-server/src/main/java` - Application code
- `lcap-server/src/main/resources` - Configuration (dev/test/prod profiles)

## Configuration

### Environment Configurations
- lcapServer: `config/config.{env}.js` (development, test, prod, docker, docp)
- lcapDataServer: `lcap-server/src/main/resources/application-{profile}.yml`
- lcapWeb: `src/config/env.js`

### MongoDB Connection
Default: `mongodb://127.0.0.1:27017/flyfish`

## Common Development Tasks

### Running Full Stack Locally
1. Start MongoDB
2. Start lcapDataServer: `cd lcapDataServer && mvn spring-boot:run`
3. Start lcapServer: `cd lcapServer && npm run development`
4. Start lcapWeb: `cd lcapWeb && npm start`
5. Access: `http://localhost:7001`

### Database Operations
```bash
# Initialize development database
cd lcapServer && npm run upgrade-database
```

### Component Development
The component development environment is located in `lcapWeb/www/`. Configure `web/screen/config/env.js` with the API domain.

### Micro-Frontend Sub-app Development
For sub-applications integrated via Qiankun:
```bash
npm start                      # Standalone development
npm run build                  # Build with MICRO_TYPE=child
```
Set `__webpack_public_path__` based on `window.__POWERED_BY_QIANKUN__`.