# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Redis Manager is a Redis one-stop management platform supporting cluster monitoring, installation (Docker/Machine/Humpback), management, alerting, and basic data operations. It consists of a Java/Spring Boot backend and a Vue.js frontend.

## Technology Stack

- **Backend**: Java 8, Spring Boot 2.1.5, MySQL 8.0, Eureka Service Discovery, Jetty
- **Frontend**: Vue 2.5, Element UI, ECharts/Highcharts, Vuex, Vue Router
- **Database**: MySQL with HikariCP connection pool
- **Build Tools**: Maven (backend), npm/webpack (frontend)

## Architecture

### Backend Structure (redis-manager-dashboard/)
```
src/main/java/com/newegg/ec/redis/
├── RedisManagerApplication.java       # Spring Boot entry point
├── controller/                        # REST controllers
│   ├── ClusterController.java         # Cluster operations
│   ├── NodeManageController.java      # Node management
│   ├── MonitorController.java         # Monitoring endpoints
│   ├── InstallationController.java    # Installation workflows
│   ├── AlertRuleController.java       # Alert management
│   └── ...                            # Other controllers
├── service/                           # Business logic layer
├── dao/                               # Data access layer (MyBatis)
├── entity/                            # Entity models
├── client/                            # Redis client connections
├── plugin/                            # Modular plugins
│   ├── install/                       # Installation implementations
│   │   ├── DockerClientOperation.java
│   │   ├── MachineClientOperation.java
│   │   └── HumpbackClientOperation.java
│   ├── alert/                         # Alert services
│   └── rct/                           # RDB analysis tools
├── util/                              # Utilities
│   ├── RedisClusterInfoUtil.java
│   ├── SSH2Util.java                  # SSH operations for machine installs
│   └── ...
└── config/                            # Configuration classes
```

### Frontend Structure (redis-manager-ui/redis-manager-vue/src/)
```
src/
├── main.js                    # Vue entry point
├── App.vue                    # Root component
├── router/index.js            # Route definitions
├── vuex/                      # State management
├── api/                       # Backend API calls
├── components/                # Reusable Vue components
├── utils/                     # Frontend utilities
└── assets/                    # Static assets
```

## Common Commands

### Backend Development
```bash
# Build backend (requires MySQL running)
cd redis-manager-dashboard
mvn clean package -DskipTests

# Run tests
mvn test

# Run single test class
mvn test -Dtest=SSH2UtilTest

# Run Spring Boot application
mvn spring-boot:run

# Start from built distribution (after running build.sh)
cd ../
./bin/start.sh

# Stop application
./bin/stop.sh
```

### Frontend Development
```bash
# Install dependencies
cd redis-manager-ui/redis-manager-vue
npm install

# Start dev server (hot reload on localhost:8080)
npm run dev

# Build for production
npm run build

# Lint code
npm run lint

# Build with bundle analyzer
npm run build --report
```

### Full Build & Deployment
```bash
# Build complete application (backend + frontend)
cd redis-manager-ui/redis-manager-vue
npm install
npm run build
cd ../..
cd build
./build.sh

# The build script:
# 1. Cleans previous builds
# 2. Packages Vue frontend into backend static resources
# 3. Builds backend JAR with Maven
# 4. Copies configs and dependencies
# 5. Creates distribution in redis-manager-dashboard/target/
```

### Docker
```bash
# Build Docker image
cd docker
docker build -t redis-manager .

# Run container
sudo docker run -d --net=host --name redis-manager \
  -e DATASOURCE_DATABASE='redis_manager' \
  -e DATASOURCE_URL='jdbc:mysql://127.0.0.1:3306/redis_manager?useUnicode=true&characterEncoding=utf-8&serverTimezone=GMT%2b8' \
  -e DATASOURCE_USERNAME='root' \
  -e DATASOURCE_PASSWORD='******' \
  redis-manager
```

## Database Setup

1. Create database: `CREATE DATABASE redis_manager DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;`
2. Configure connection in `redis-manager-dashboard/src/main/resources/application.yml`
3. Database schema is managed via MyBatis - check DAO interfaces in `dao/` package

## Configuration

Main configuration file: `redis-manager-dashboard/src/main/resources/application.yml`

Key configurations:
- `spring.datasource.*` - Database connection settings
- `redis-manager.auth` - Authentication credentials
- `redis-manager.monitor` - Monitoring data retention settings
- `redis-manager.installation` - Installation paths and settings
- `server.port` - Default: 8182

Override via environment variables:
- `DATASOURCE_URL`, `DATASOURCE_USERNAME`, `DATASOURCE_PASSWORD`
- `SERVER_PORT`
- `RM_AUTH_USERNAME`, `RM_AUTH_PASSWORD`

## Key Features & Modules

1. **Cluster Management** (`ClusterController`, `NodeManageController`)
   - Import existing clusters
   - Node operations: Forget, Replicate Of, Failover, Move Slot
   - Start/Stop/Restart/Delete operations
   - Config modifications

2. **Monitoring** (`MonitorController`)
   - Real-time Redis metrics (Memory, Clients, etc.)
   - Redis Info, Config, Slow Log viewing
   - Metrics storage with configurable retention (default: 15 days)

3. **Installation** (`InstallationController`, `plugin/install/`)
   - Docker installation
   - Physical machine installation (via SSH)
   - Humpback installation
   - Redis package management

4. **Alerting** (`AlertRuleController`, `plugin/alert/`)
   - Email, WeChat, DingTalk alerts
   - Configurable alert rules
   - Alert channel management

5. **Data Operations** (`DataOperationController`)
   - Query and Scan operations
   - Basic CRUD on Redis data

6. **RDB Analysis** (`RDBAnalyzeController`, `plugin/rct/`)
   - RDB file analysis
   - Report generation

## Testing

Backend tests use JUnit 4 in `src/test/java/`:
```bash
cd redis-manager-dashboard
mvn test                              # Run all tests
mvn test -Dtest=SSH2UtilTest         # Run specific test
mvn test -Dtest='*UtilTest'          # Run all *UtilTest classes
```

Test examples:
- `SSH2UtilTest.java` - SSH operations testing
- `RedisClientTest.java` - Redis client testing
- `DockerClientOperationTest.java` - Docker integration testing

## Development Notes

- Frontend static files are served from `src/main/resources/static/` in the backend
- Frontend build output should be copied to backend static resources during full build
- The `build/build.sh` script handles this integration
- Server runs on port 8182 by default
- Uses Jetty (not Tomcat) as embedded servlet container
- Eureka service discovery is included but configured as standalone (register-with-eureka: false)

## Important Classes

- `RedisManagerApplication.java:1` - Main Spring Boot application entry point
- `IndexController.java:1` - Serves the frontend index page
- `RedisClusterInfoUtil.java` - Core Redis cluster information utility
- `SSH2Util.java` - SSH operations for machine-based installations
- `DockerClientOperation.java` - Docker installation implementation

## API Design

RESTful APIs are organized by feature in controllers:
- `/cluster/*` - Cluster operations
- `/node/*` - Node management
- `/monitor/*` - Monitoring endpoints
- `/installation/*` - Installation workflows
- `/alert/*` - Alert configuration
- `/user/*` - User management