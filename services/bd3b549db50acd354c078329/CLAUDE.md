# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RackShift is an open-source bare-metal server management platform covering discovery, out-of-band management, RAID configuration, firmware updates, and OS installation. The project follows a multi-module Maven architecture with Spring Boot backend and Vue.js frontend.

## Technology Stack

- **Backend**: Spring Boot 2.3.1, Java 8, MyBatis, MySQL, Shiro (authentication), Flyway (migrations)
- **Frontend**: Vue.js 2.6, Element UI, Vue CLI 4.4, Axios
- **Database**: MySQL 5.7
- **Build**: Maven (multi-module)
- **CI/CD**: Jenkins (see Jenkinsfile)

## Project Structure

```
rackshift/
├── rackshift-server/          # Main Spring Boot application (port 8082)
│   ├── src/main/java/io/rackshift/
│   │   ├── Application.java          # Main entry point
│   │   ├── controller/               # REST controllers
│   │   ├── service/                  # Business logic
│   │   ├── model/                    # Data models
│   │   ├── mybatis/                  # MyBatis mappers
│   │   ├── engine/                   # Workflow engine (taskgraph/taskobject)
│   │   ├── job/                      # Job execution
│   │   ├── strategy/                 # Hardware vendor strategies
│   │   ├── security/                 # Authentication/authorization
│   │   └── config/                   # Configuration
│   └── src/main/resources/
│       ├── application.properties    # Spring Boot configuration
│       ├── db/migration/             # Flyway database migrations
│       └── schemas/                  # JSON schemas for tasks
├── rackshift-web/             # Vue.js frontend application
│   ├── src/
│   │   ├── main.js
│   │   ├── components/               # Vue components
│   │   └── ...
│   ├── public/
│   ├── package.json
│   └── vue.config.js
├── rackshift-proxy/           # Proxy service for hardware vendors
├── rackshift-dhcp-proxy/      # DHCP proxy service
├── rackshift-plugin/          # Hardware vendor plugins
│   ├── metal-plugin-sdk/           # Plugin SDK
│   ├── dell-metal-plugin/          # Dell plugin
│   ├── inspur-metal-plugin/        # Inspur plugin
│   ├── hp-metal-plugin/            # HP plugin
│   ├── h3c-metal-plugin/           # H3C plugin
│   └── ...
└── docker-compose.yml         # Docker orchestration
```

## Common Development Commands

### Backend Development

```bash
# Build the entire project (including all modules)
mvn clean install

# Build a specific module
cd rackshift-server
mvn clean install

# Build without running tests
mvn clean install -DskipTests

# Run the server
cd rackshift-server
mvn spring-boot:run

# Run a specific test
mvn test -Dtest=TestClassName

# Run all tests
mvn test

# Generate MyBatis mapper files
mvn mybatis-generator:generate

# Run Flyway migrations (requires MySQL running)
mvn flyway:migrate
```

### Frontend Development

```bash
# Install dependencies (in rackshift-web directory)
npm install

# Run development server with hot reload
npm run serve

# Build for production
npm run build

# Lint and fix code
npm run lint

# Windows-specific commands (if needed)
npm run wserve    # Dev server on Windows
npm run wbuild    # Build on Windows
```

### Database Management

The application uses Flyway for database migrations. Migrations are located in:
- `rackshift-server/src/main/resources/db/migration/`

MySQL configuration (see `application.properties`):
- Default user: `root`
- Default password: `admin`
- Database: `rackshift`

### Docker Deployment

```bash
# Build Docker images
docker-compose build

# Start all services (including MySQL)
docker-compose up -d

# Start with host networking mode (required for bare-metal management)
docker-compose up -d
```

Note: The application uses host networking mode (`network_mode: host`) which is required for bare-metal server management over physical networks.

## Architecture Notes

### Backend Architecture

1. **Engine Module**: Contains the workflow execution engine with:
   - `taskgraph/` - Workflow definition and management
   - `taskobject/` - Task execution objects
   - `basetask/` - Base task implementations

2. **Plugin System**: Uses a vendor-agnostic plugin architecture:
   - Hardware vendors (Dell, Inspur, HP, H3C) implement interfaces from `metal-plugin-sdk`
   - Plugins enable support for different out-of-band management protocols (IPMI, WSMan, etc.)

3. **Configuration**: Main configuration is in `application.properties`:
   - Database connection: HikariCP connection pool
   - Flyway migration settings
   - RabbitMQ for messaging
   - File upload limits: 10GB max file size, 20GB max request size

4. **Authentication**: Uses Apache Shiro for authentication and authorization

5. **API Documentation**: Swagger is integrated (springfox-swagger2 2.9.2)

### Frontend Architecture

1. **Vue.js 2.6** with Element UI components
2. **Internationalization**: Supports multiple languages (see `src/i18n/`)
3. **API Communication**: Uses Axios for HTTP requests to the backend
4. **Development**: Runs on port 8080, proxies API calls to backend on 8082
5. **Build Process**: Frontend is built and statically served by the Spring Boot backend

### Multi-Module Build Process

The Jenkins pipeline (Jenkinsfile) shows the standard build flow:
1. Build the frontend (`cd rackshift-web && cnpm install && cnpm run build`)
2. Copy frontend dist files to `rackshift-server/src/main/resources/static`
3. Build the backend (`mvn clean install`)
4. Build Docker images for server and dhcp-proxy

## Important Configuration

### Server Ports
- Main application: 8082
- Frontend dev server: 8080
- MySQL: 3306
- RabbitMQ: 5672

### Environment Variables
- `web.server.port` - Server port (default: 8082)
- External configuration file: `/opt/rackshift/conf/rackshift.properties`

### Java Version
- Target: Java 8 (both source and compiled)
- Spring Boot version: 2.3.1.RELEASE

## Testing

There are limited tests in the codebase:
- `rackshift-server/src/test/` contains basic integration tests
- Test classes: `TestApi.java`, `TestH3C.java`, `I18NTest.java`

To run tests:
```bash
cd rackshift-server
mvn test
```

## Database Migrations

Flyway is configured for database schema management:
- Migration files: `rackshift-server/src/main/resources/db/migration/`
- Migration table: `rackshift_version`
- Auto-migration is enabled on startup (`spring.flyway.enabled=true`)
- Baseline on migrate is enabled (`spring.flyway.baseline-on-migrate=true`)

## CI/CD

The project uses Jenkins for CI/CD (see Jenkinsfile):
- Builds on the 'metersphere' node
- Stages:
  1. **Build**: Installs frontend dependencies, builds frontend, builds dhcp-proxy
  2. **Docker build & push**: Creates Docker images and pushes to registry

## Development Tips

1. **Frontend Integration**: The frontend build output is copied to `rackshift-server/src/main/resources/static/` during the build process

2. **Database Connection**: Ensure MySQL is running before starting the application or running migrations

3. **Plugin Development**: New hardware vendor plugins should follow the pattern in existing plugins and implement the interfaces from `metal-plugin-sdk`

4. **Task Engine**: The workflow system uses JSON-based task definitions located in `rackshift-server/src/main/resources/schemas/`

5. **Logging**: Logs are written to `/opt/rackshift/logs/rackshift/`

6. **Development Workflow**:
   - Start MySQL (or use docker-compose)
   - Run Flyway migrations
   - Start backend: `mvn spring-boot:run` (in rackshift-server)
   - Start frontend: `npm run serve` (in rackshift-web, port 8080)

## Documentation

- Project documentation: https://docs.rackshift.io/
- Main README: `/home/ubuntu/deploy-projects/bd3b549db50acd354c078329/README.md` (Chinese)
- English README: `/home/ubuntu/deploy-projects/bd3b549db50acd354c078329/README_EN.md`

## License

The project is licensed under GPL v3.