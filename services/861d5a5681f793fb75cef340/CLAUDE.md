# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Redis Manager is a comprehensive Redis cluster management platform that supports monitoring, installation, management, alerting, and basic data operations for Redis clusters (cluster, master-replica, and sentinel modes).

**Technology Stack:**
- **Backend:** Java 8 + Spring Boot 2.1.5 + Maven
- **Frontend:** Vue.js 2.5.2 + Element UI 2.12.0 + Webpack
- **Database:** MySQL 8.0
- **Cache:** Redis 4.x+ (via Jedis 3.1.0)
- **Containerization:** Docker
- **Service Discovery:** Eureka (Spring Cloud Netflix)

## Repository Structure

```
/
├── bin/                          # Runtime scripts
│   ├── start.sh                  # Start application
│   └── stop.sh                   # Stop application
├── build/
│   └── start.sh                  # Build script (Maven + Webpack)
├── docker/                       # Docker configuration
├── documents/                    # Documentation and UI screenshots
├── redis-manager-dashboard/      # Backend (Spring Boot)
│   ├── src/main/java/com/newegg/ec/redis/
│   │   ├── RedisManagerApplication.java  # Entry point
│   │   ├── controller/           # REST controllers
│   │   ├── dao/                  # Data access (MyBatis)
│   │   ├── service/              # Business logic
│   │   └── util/                 # Utility classes
│   └── src/main/resources/
│       └── application.yml       # Configuration
├── redis-manager-ui/             # Frontend (Vue.js)
│   └── redis-manager-vue/        # Vue app
├── sql/
│   └── redis_manager.sql         # Database schema
└── README.md                     # Project documentation (Chinese)
```

## Common Development Commands

### Backend (Spring Boot)

```bash
cd redis-manager-dashboard

# Build JAR without tests
mvn clean package -Dmaven.test.skip=true

# Build with tests
mvn clean install

# Run a single test class
mvn test -Dtest=ClassName

# Run specific test method
mvn test -Dtest=ClassName#methodName

# Build production distribution
cd ../build && ./start.sh
```

### Frontend (Vue.js)

```bash
cd redis-manager-ui/redis-manager-vue

# Install dependencies
npm install

# Start development server with hot reload
npm run dev

# Build for production (outputs to redis-manager-dashboard/src/main/resources/static)
npm run build

# Lint code
npm run lint
```

### Running the Application

**Using build script:**
```bash
cd build
./start.sh

# Start the application
cd ../bin
./start.sh

# Stop the application
./stop.sh
```

**Default URL:** http://localhost:8182

**Default Credentials:** admin/admin (configurable in application.yml)

## Architecture

### Backend Architecture

**Spring Boot Application** (`com.newegg.ec.redis.RedisManagerApplication.java`):
- **RESTful Controllers** (`controller/`): Handle HTTP requests for clusters, nodes, monitoring, alerts
- **Data Access Layer** (`dao/`): MyBatis DAOs for database operations
- **Service Layer** (`service/`): Business logic for cluster management, monitoring, installation
- **Utilities** (`util/`): SSH operations, Redis config parsing, Linux info collection

**Key Dependencies:**
- **MySQL:** Data persistence (clusters, nodes, users, operations, alerts)
- **Jedis:** Redis connectivity
- **Quartz:** Scheduled monitoring tasks
- **Eureka:** Service discovery (embedded server)
- **Docker Java:** Container management
- **SSH2:** Remote machine operations

**Configuration** (`application.yml`):
- Server port: 8182 (override with `SERVER_PORT`)
- Database: MySQL with HikariCP (configure via `DATASOURCE_URL`, `DATASOURCE_USERNAME`, `DATASOURCE_PASSWORD`)
- Authentication: admin/admin (override with `RM_AUTH_USERNAME`, `RM_AUTH_PASSWORD`)
- Monitoring: 15-day data retention (configurable)
- Redis Installation: Docker, Machine, Humpback methods

### Frontend Architecture

**Vue.js Single Page Application**:
- **Entry:** `src/main.js` - Vue app initialization
- **Router:** Vue Router for client-side routing
- **State Management:** Vuex for centralized state
- **UI Components:** Element UI component library
- **HTTP Client:** Axios for API communication
- **Charts:** ECharts and Highcharts for data visualization

**Key Features:**
- Cluster dashboard and monitoring
- Cluster import and creation (Docker/Machine/Humpback)
- Node management (start, stop, restart, failover, etc.)
- Alert configuration (email, DingTalk, WeChat)
- Data operations (query, scan, CRUD)

### Database Schema

**MySQL Database:** `redis_manager` (UTF-8)

Schema file: `/sql/redis_manager.sql`

Main tables:
- **Clusters and Nodes:** Cluster metadata and Redis node information
- **Users and Groups:** Authentication and authorization
- **Monitoring Data:** Metrics and slow logs
- **Operations:** Audit trail of cluster operations
- **Alerts:** Alert rules and history

## Configuration

### Environment Variables

**Database:**
- `DATASOURCE_URL`: MySQL connection URL
- `DATASOURCE_USERNAME`: MySQL username
- `DATASOURCE_PASSWORD`: MySQL password
- `DATASOURCE_DATABASE`: Database name (default: redis_manager)

**Application:**
- `SERVER_PORT`: Application port (default: 8182)
- `RM_AUTH_USERNAME`: Admin username (default: admin)
- `RM_AUTH_PASSWORD`: Admin password (default: admin)

**Redis Installation:**
- `REDIS_MANAGER_INSTALLATION_CURRENT_HOST`: Current host IP for installations
- Redis package paths and Docker host configuration in `application.yml`

### Development Setup Requirements

- Java 8+
- Maven 3.5+
- Node.js 6.0+ & npm 3.0+
- MySQL 8.0+
- Redis (for connection testing)
- Docker (optional, for container-based installations)

## Docker Deployment

```bash
# Pull from DockerHub
sudo docker run -d --net=host --name redis-manager \
  -e DATASOURCE_DATABASE='redis_manager' \
  -e DATASOURCE_URL='jdbc:mysql://127.0.0.1:3306/redis_manager' \
  -e DATASOURCE_USERNAME='root' \
  -e DATASOURCE_PASSWORD='******' \
  reasonduan/redis-manager
```

See `docker/README.md` for additional configuration options.

## Testing

**Backend Tests:** Located in `redis-manager-dashboard/src/test/java/`
- `RedisClientTest.java`: Redis client connectivity tests
- `DockerClientOperationTest.java`: Docker operations tests
- `NodeInfoServiceTest.java`: Node info service tests
- `LinuxInfoUtilTest.java`: Linux system info utilities
- `RedisConfigUtilTest.java`: Redis configuration utilities
- `SSH2UtilTest.java`: SSH connection tests
- `StringUtilTest.java`: String utility tests

Run tests: `mvn test` in `redis-manager-dashboard/`

**Frontend Linting:** ESLint configured in `package.json`

## Documentation

- **README.md** (root): Main project documentation in Chinese
- **docker/README.md**: Docker deployment guide
- **documents/**: UI screenshots and feature documentation
- **documents/plane.md**: Development notes (v2.1.0 features)
- **documents/contact/**: Contact information (DingTalk, WeChat)

**User Manual:** https://github.com/ngbdf/redis-manager/wiki/

## Key Implementation Notes

1. **Static Resources:** Frontend build outputs to `redis-manager-dashboard/src/main/resources/static/`
2. **Eureka Server:** Embedded at `/eureka-ui` (for service registry)
3. **Quartz Scheduling:** Handles periodic monitoring data collection
4. **Multi-deployment Support:** Docker, Physical Machine, Humpback installation methods
5. **Authentication:** Simple username/password (LDAP support available via config)
6. **Monitoring Data Retention:** Default 15 days (configurable via `RM_MONITOR_DATA_KEEP_DAYS`)