# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KnowStreaming is a cloud-native Kafka management platform by Didi (滴滴出行). It provides comprehensive Kafka cluster management, monitoring, operations, and governance capabilities for Apache Kafka versions 0.10.x to 3.x.x, supporting both ZK and Raft modes.

- **Version**: 3.4.0
- **License**: Apache License 2.0
- **Documentation**: https://doc.knowstreaming.com/product
- **Demo**: https://demo.knowstreaming.com (admin/admin)

## Architecture

This is a **layered microservices architecture** with 13 Maven modules:

### Core Backend Modules
- **km-rest** - REST API layer (40+ controllers with Swagger)
- **km-core** - Core services and business logic
- **km-biz** - Business layer managers
- **km-persistence** - Data access (MySQL + Elasticsearch)
- **km-common** - Shared beans (DTOs, VOs, Entities), constants, utilities

### Supporting Modules
- **km-collector** - Metrics collection from Kafka clusters
- **km-task** - Background task management (Logi-Job)
- **km-console** - Frontend packages (2 React micro-frontends)

### Extension Modules
- **km-extends/km-account** - User account management
- **km-extends/km-monitor** - Monitoring extensions
- **km-enterprise/km-ha** - High availability features
- **km-dist** - Distribution & deployment artifacts

### Frontend Structure (km-console/packages/)
- **layout-clusters-fe** - Cluster management UI
- **config-manager-fe** - Configuration management UI

### Key Architectural Patterns
- **REST Layer** (`km-rest`): Versioned APIs (/api/v3/), global exception handling
- **Business Logic Layer** (`km-biz`): Manager classes for domain operations
- **Core Services Layer** (`km-core`): Service interfaces, Kafka/ZK management, JMX clients
- **Persistence Layer** (`km-persistence`): MyBatis-Plus DAOs, MariaDB + ES 6.6.2
- **Common Layer** (`km-common`): Shared components, converters, formatters
- **Micro-frontends**: React with single-spa module federation

## Technology Stack

### Backend
- **Framework**: Spring Boot 2.3.7, Spring 5.3.19
- **Database**: MariaDB (metadata), Elasticsearch 6.6.2 (metrics)
- **Cache**: Caffeine 2.8.8
- **Kafka**: 2.8.1 (clients), 3.x support
- **Security**: Logi-Security 2.10.13
- **Scheduling**: Logi-Job 1.0.23
- **Monitoring**: Micrometer + Prometheus
- **Build**: Maven (Java 8+)

### Frontend
- **Framework**: React 16.12.0 + TypeScript 4.6.4
- **UI**: Ant Design 4.6.2, KnowDesign 1.3.7
- **Build**: Webpack 4.40.0, Lerna (monorepo)
- **Routing**: React Router 5.2.1
- **Architecture**: Single-spa micro-frontends

## Common Development Commands

### Backend (Java/Spring Boot)
```bash
# Build all modules
mvn clean install

# Skip tests during build
mvn clean install -DskipTests

# Build specific module
cd km-rest && mvn clean package

# Run tests
mvn test

# Run single test
mvn test -Dtest=ClassName#methodName

# Run with coverage
mvn test jacoco:report

# Package without running tests (faster)
mvn package -DskipTests

# Clean build
mvn clean
```

### Frontend (React/TypeScript)
```bash
# Install dependencies (uses Chinese mirror)
cd km-console
npm run i

# Clean install
npm run clean

# Start development servers (both frontends)
npm run start

# Build for production
npm run build

# Lint code
npx eslint packages/**/*.{js,tsx}

# Format code
npx prettier --write packages/**/*.{js,tsx,css}
```

### Docker Deployment
```bash
# Start all services (manager + UI + MySQL + ES)
cd km-dist/docker
docker-compose up -d

# View logs
docker-compose logs -f knowstreaming-manager

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Production Deployment
```bash
# Start production server
bin/startup.sh

# Check logs
tail -f logs/start.out
tail -f logs/km_gc.log

# The startup script:
# - Auto-detects JAVA_HOME
# - Sets JVM: -Xms2g -Xmx2g -Xmn1g
# - Enables GC logging with rotation
# - Starts Spring Boot app from libs/ks-km.jar
```

## Key Configuration Files

- **Root POM**: `pom.xml` - Manages all 13 modules and dependencies
- **Backend Config**: `km-rest/src/main/resources/application.yml`
- **Log Config**: `km-rest/src/main/resources/logback-spring.xml`
- **Frontend Root**: `km-console/package.json` - Lerna workspace configuration
- **Docker Compose**: `km-dist/docker/docker-compose.yml`
- **Start Script**: `bin/startup.sh` - Production launcher

## Code Organization

### Java Package Structure
```
com.xiaojukeji.know.streaming.km
├── rest/                    # REST layer
│   └── api/v3/             # Versioned APIs
├── core/                   # Core services
│   ├── service/            # Service interfaces
│   ├── service/impl/       # Service implementations
│   ├── register/           # Bean registration
│   └── watcher/            # Zookeeper watchers
├── biz/                    # Business logic
│   └── manager/            # Domain managers
├── common/                 # Shared components
│   ├── bean/               # DTOs, VOs, Entities
│   ├── constant/           # Constants
│   ├── converter/          # Data converters
│   └── utils/              # Utilities
└── persistence/            # Data access
    ├── dao/                # MyBatis DAOs
    └── mysql/              # MySQL entities
```

### API Structure
- **Base Path**: `/api/v3/`
- **Pattern**: RESTful with Result<T> wrapper
- **Documentation**: Swagger/OpenAPI at `/swagger-ui.html`
- **Controllers**: ~40+ controllers in km-rest/src/main/java

## Development Workflow

### Prerequisites
- **Java**: JDK 8+ (JAVA_HOME required)
- **Maven**: 3.6+
- **Node.js**: 14+ (for frontend)
- **Database**: MariaDB + Elasticsearch (via Docker compose)

### Local Development Setup
1. **Backend**: `mvn clean install -DskipTests` in root
2. **Frontend**: `cd km-console && npm run i && npm run start`
3. **Dependencies**: Use Docker Compose for MySQL + ES
4. **Access**: UI at http://localhost:3000, API at http://localhost:8080

### Building for Production
```bash
# Full build (backend + frontend)
mvn clean install -DskipTests
cd km-console && npm run build

# Copy artifacts to km-dist
# Frontend builds go to km-rest/src/main/resources/static/
```

## Key Features

- **Multi-cluster Management**: Support for multiple Kafka clusters
- **Zero Intrusion**: Works with native Kafka 0.10.x to 3.x.x
- **Real-time Monitoring**: JMX-based metrics with Elasticsearch storage
- **Cluster Operations**: Topic CRUD, partition management, consumer group monitoring
- **Health Analysis**: Multi-dimensional cluster health inspection
- **Replication**: Topic replica migration and expansion
- **Connect Management**: Kafka Connect cluster and connector management
- **Security**: ACL and user management
- **Mirror Maker 2**: Cross-cluster replication
- **Load Balancing**: Cluster rebalancing capabilities

## Dependencies

### Critical Backend Dependencies
- MariaDB Java Client 3.0.5
- MyBatis-Plus 3.4.2
- Elasticsearch 6.6.2
- Caffeine 2.8.8
- Kafka Clients 2.8.1
- Zookeeper 3.6.3
- Logi-Security 2.10.13
- Logi-Job 1.0.23
- Swagger 2.9.2

### Critical Frontend Dependencies
- React 16.12.0
- TypeScript 4.6.4
- Ant Design 4.6.2
- Webpack 4.40.0
- Lerna 5.5.0

## Important Notes

1. **API Versioning**: All REST APIs are versioned under `/api/v3/`
2. **Database Migration**: MySQL schema stored in `km-persistence/src/main/resources/db/migration/`
3. **Metrics Storage**: Time-series metrics go to Elasticsearch, metadata to MariaDB
4. **Thread Pools**: Configured in application.yml per domain (cluster, broker, topic, etc.)
5. **Frontend Build**: Frontend packages built separately, results copied to backend static resources
6. **Chinese Mirror**: npm uses `https://registry.npmmirror.com` in npm scripts
7. **Log Format**: Uses logstash encoder for structured logging
8. **Health Checks**: Spring Boot Actuator endpoints at `/actuator/health`

## Environment Variables

### Required for Production
- `SERVER_MYSQL_ADDRESS` - MariaDB connection
- `SERVER_MYSQL_DB` - Database name (know_streaming)
- `SERVER_MYSQL_USER` - Database user (root)
- `SERVER_MYSQL_PASSWORD` - Database password
- `SERVER_ES_ADDRESS` - Elasticsearch endpoint
- `JAVA_OPTS` - JVM parameters

## Testing

- **Framework**: JUnit 5 with Testcontainers
- **Integration Tests**: Use Testcontainers for ES/MySQL
- **Location**: `src/test/java` in each module
- **Command**: `mvn test` or `mvn test -Dtest=ClassName`

## Useful Resources

- **Product Website**: https://knowstreaming.com
- **Documentation**: https://doc.knowstreaming.com/product
- **Demo Environment**: https://demo.knowstreaming.com
- **GitHub**: https://github.com/didi/KnowStreaming
- **Chinese Community**: 知识星球 (Knowledge Planet) - https://z.didi.cn/5gSF9