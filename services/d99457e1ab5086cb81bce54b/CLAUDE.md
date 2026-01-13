# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastBee is an open-source IoT (Internet of Things) platform built with a Spring Boot backend and Vue.js frontend. It's designed for smart home, office, community, agricultural monitoring, water conservancy, and industrial control applications.

**Technology Stack:**
- **Backend**: Spring Boot 2.5.15, MyBatis Plus, Spring Security, MySQL, Redis, TDengine
- **Frontend**: Vue 2.6, Element UI, Vuex, Axios
- **Protocols**: MQTT (Netty-based broker), SIP (GB/T28181 for video), WebSocket
- **Database**: MySQL 5.7, Redis 7.0, TDengine for time-series data
- **Infrastructure**: Docker, Nginx, ZLMediaKit (video streaming)

## Development Commands

### Backend (Spring Boot)

```bash
# Navigate to Spring Boot directory
cd springboot

# Build all modules
mvn clean install

# Build without running tests
mvn clean install -DskipTests

# Run single test
mvn test -Dtest=TestClassName

# Run specific test method
mvn test -Dtest=TestClassName#testMethod

# Run all tests
mvn test

# Package application
mvn clean package -DskipTests

# Run the application using the management script
cd springboot/fastbee-admin
./fastbee.sh start   # start the application
./fastbee.sh stop    # stop the application
./fastbee.sh restart # restart the application
./fastbee.sh status  # check application status

# Run with specific profile
java -jar fastbee-admin.jar --spring.profiles.active=prod
```

**Important:** The main entry point is `fastbee-admin` module (com.fastbee.FastBeeApplication.java:18). The default port is 8080.

**Configuration Files:**
- `springboot/fastbee-admin/src/main/resources/application.yml` - Main configuration
- `springboot/fastbee-admin/src/main/resources/application-dev.yml` - Development profile
- `springboot/fastbee-admin/src/main/resources/application-prod.yml` - Production profile

### Frontend (Vue.js)

```bash
# Navigate to Vue directory
cd vue

# Install dependencies (use npmmirror for faster downloads in China)
npm install
# or
npm install --registry=https://registry.npmmirror.com

# Start development server
npm run dev

# Build for production
npm run build:prod

# Build for staging
npm run build:stage

# Preview production build
npm run preview

# Lint code
npm run lint
```

**Development URL:** http://localhost:80 (frontend), http://localhost:8080 (backend API)

### Database Setup

```bash
# Start MySQL and Redis using Docker
cd docker/data
docker-compose up -d mysql redis

# Initialize database
# Import fastbee.sql from springboot/sql/fastbee.sql into MySQL
```

## High-Level Architecture

### Backend Architecture (Spring Boot Multi-Module)

The backend follows a modular architecture with clear separation of concerns:

**Core Modules:**
- **`fastbee-admin`** (web): Main application entry point, hosts the web interface and REST APIs
- **`fastbee-server`** (service): Core business logic and service layer
- **`fastbee-common`** (common): Shared utilities, constants, annotations, and helpers
- **`fastbee-framework`** (framework): Core framework components, security configuration
- **`fastbee-gateway`** (gateway): API gateway and routing logic

**Protocol & Integration Modules:**
- **`fastbee-protocol`** (protocol): Protocol handlers for MQTT, Modbus, and other IoT protocols
- **`fastbee-service`** (iot-service): IoT-specific services (device management, product management, monitoring)
- **`fastbee-plugs`** (plugs): Plugin management system
- **`fastbee-open-api`** (open-api): Public REST APIs for external integrations

**Key Components:**
- **MQTT Broker**: Netty-based MQTT server running on port 1883 (WebSocket on 8083)
- **SIP Server**: GB/T28181 protocol implementation for video surveillance (port 5061/UDP)
- **Message Queue**: RocketMQ integration for async messaging
- **Database Layer**: MyBatis Plus with dynamic data source support (multi-tenant capable)
- **Time-Series Data**: TDengine integration for IoT device data storage

### Frontend Architecture (Vue.js)

**Directory Structure:**
- **`src/views/`**: Page-level components (dashboard, device management, product management, etc.)
- **`src/api/`**: REST API client definitions for backend communication
- **`src/components/`**: Reusable Vue components
- **`src/layout/`**: Layout components (header, sidebar, tabs)
- **`src/router/`**: Vue Router configuration
- **`src/store/`**: Vuex store modules for state management
- **`src/utils/`**: Utility functions and helpers

**Key Features:**
- Element UI component library
- Responsive design
- Role-based access control (RBAC)
- Real-time data updates (WebSocket)
- Charts and data visualization (ECharts)
- Video streaming integration

### System Integration

**Deployment Architecture (Docker):**
```
┌─────────────┐
│   Nginx     │  Port 80/443 (Frontend + Reverse Proxy)
└──────┬──────┘
       │
       ├─────────────┐
       │             │
┌──────▼──────┐ ┌────▼──────┐
│   Java      │ │ ZLMediaKit│  Port 554/1935 (Video Streaming)
│  (Backend)  │ │ (Media)   │
│  Port 8080  │ └───────────┘
│  Port 1883  │
│  Port 5061  │
└──────┬──────┘
       │
       ├───────┬────────┐
       │       │        │
┌──────▼┐ ┌────▼┐ ┌────▼┐
│ MySQL │ │Redis│ │ TD  │
│3306   │ │6379 │ │ 0   │
└───────┘ └─────┘ └─────┘
```

**Default Ports:**
- 80/443: Nginx (frontend)
- 8080: Spring Boot Admin (backend API)
- 1883: MQTT Broker
- 8083: MQTT WebSocket
- 5061: SIP Server
- 3306: MySQL
- 6379: Redis

### Key Configuration

**Backend Configuration (application.yml:1-105):**
- Server port: 8080
- Active profile: dev (development) or prod (production)
- File upload path: `D:/uploadPath` (configure per environment)
- Token configuration: 30-minute expiration, configurable secret
- Druid connection pool with web monitoring enabled
- Captcha type: math or char
- MQTT broker: Port 1883, WebSocket port 8083

## Testing Strategy

**Backend Tests:**
- Unit tests located in `src/test/java` within each module
- Run all tests: `mvn test`
- Run specific test: `mvn test -Dtest=ClassName`
- Integration tests: Use `@SpringBootTest` annotation
- Mock external services: Use `@MockBean`

**Frontend Tests:**
- Linting: `npm run lint` (ESLint with auto-fix)
- Pre-commit hooks configured via husky and lint-staged
- ESLint configuration: `.eslintrc.js`

**Test Data:**
- Database initialization: `springboot/sql/fastbee.sql`
- Mock data can be added via test resources

## Database Schema

**Main Database (MySQL):**
- Tables prefixed with system-related (`sys_`), device-related (`iot_`), and protocol-related (`protocol_`)
- Based on RuoYi framework with IoT extensions
- Supports multi-tenant architecture via dynamic data sources

**Cache (Redis):**
- Session storage
- Token management
- Frequently accessed device status
- Rate limiting

**Time-Series (TDengine):**
- Device telemetry data
- Historical measurements
- High-performance time-series queries

## Common Development Tasks

### Adding a New REST API Endpoint

1. **Backend:**
   - Create controller in `fastbee-admin/src/main/java/com/fastbee/web/controller/`
   - Service layer in `fastbee-server/src/main/java/com/fastbee/service/`
   - Domain model in respective module
   - Update MyBatis Plus mapper if needed

2. **Frontend:**
   - Add API method in `src/api/` directory
   - Create/update Vue component in `src/views/`
   - Add route in `src/router/`
   - Update menu/permission if needed

### Adding a New IoT Protocol

1. Create protocol handler in `fastbee-protocol` module
2. Implement protocol parser/codec
3. Add configuration in `application.yml`
4. Register protocol in the gateway
5. Update device connection logic

### Modifying Database Schema

1. Create migration script in `springboot/sql/`
2. Update MyBatis Plus domain models
3. Regenerate mapper files if using generator
4. Update DTOs and VOs
5. Test with dev profile

## Troubleshooting

**Common Issues:**

1. **Port Already in Use:**
   - Check `application.yml:13-14` for port configuration
   - Kill process: `lsof -ti:8080 | xargs kill -9`

2. **Database Connection Failed:**
   - Verify MySQL is running: `docker-compose ps`
   - Check credentials in `application-dev.yml:56-70`
   - Ensure database exists and schema is imported

3. **Frontend Build Failures:**
   - Clear node_modules: `rm -rf node_modules && npm install`
   - Update Node.js version (requires >= 8.9)
   - Use legacy OpenSSL provider if needed (already in scripts)

4. **MQTT Connection Issues:**
   - Check broker port 1883 is accessible
   - Verify firewall settings
   - Check WebSocket path `/mqtt` for browser clients

5. **Hot Reload Not Working:**
   - Ensure `spring.devtools.restart.enabled: true` in `application.yml:46-48`

**Logs:**
- Backend logs: Console output or `logs/fastbee-admin.log` when using the script
- Frontend logs: Browser developer console
- Database logs: Check MySQL container logs

## Documentation References

- Project Documentation: https://fastbee.cn/doc/
- RuoYi Framework: http://doc.ruoyi.vip/ruoyi-vue/
- EMQX Documentation: https://www.emqx.io/docs/zh/v5.0/
- uCharts (Vue Charts): https://www.ucharts.cn
- Commercial Version Demo: https://iot.fastbee.cn/