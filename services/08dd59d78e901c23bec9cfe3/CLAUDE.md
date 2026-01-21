# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **hcp (Huizhi Charging Platform)** - a Spring Cloud-based micro-service platform for charging station management. It supports multi-tenant SaaS architecture, real-time device monitoring, and integrates with various charging protocols (including China Electric Power Council standards and YunKuaiChong protocol).

**Technology Stack:**
- Java 8, Spring Boot 2.7.18, Spring Cloud 2021.0.8, Spring Cloud Alibaba 2021.0.5.0
- MySQL 5.7-8.0, Redis, Nacos 2.1.1
- MyBatis-Plus, Seata (distributed transactions), Redisson
- Docker for deployment

## Repository Structure

```
hcp/
├── hcp-auth/              # Authentication service (port 39200)
├── hcp-gateway/           # API Gateway with Sentinel (port 38080)
├── hcp-visual/
│   └── hcp-monitor/       # Monitoring dashboard (port 39100)
├── hcp-modules/           # Business modules
│   ├── hcp-system/        # System management (port 39201)
│   ├── hcp-gen/           # Code generator (port 39202)
│   ├── hcp-file/          # File service (port 39300)
│   ├── hcp-job/           # Scheduled tasks (port 39204)
│   ├── hcp-mp/            # WeChat Mini Program support
│   ├── hcp-operator/      # Charging operator service
│   └── hcp-simulator/     # Charging simulator for testing
├── hcp-api/               # API definitions
│   └── hcp-api-system/    # System API contracts
├── hcp-common/            # Shared libraries
│   ├── hcp-common-core/           # Core utilities
│   ├── hcp-common-security/       # Security features
│   ├── hcp-common-swagger/        # API documentation
│   ├── hcp-common-datascope/      # Data permissions
│   ├── hcp-common-datasource/     # Multi-datasource support
│   ├── hcp-common-redis/          # Redis integration
│   ├── hcp-common-log/            # Logging
│   ├── hcp-common-mybatisplus/    # MyBatis-Plus enhancements
│   ├── hcp-common-message/        # SMS/Email messaging
│   └── hcp-common-seata/          # Distributed transactions
├── hcp-demo/              # Demo application (port 39203)
├── hcp-register/          # Nacos service
├── docker/                # Docker Compose configurations
│   ├── hcp-nacos (172.18.0.6:8848)
│   ├── hcp-mysql (172.18.0.2:3306)
│   ├── hcp-redis (172.18.0.3:6379)
│   ├── hcp-nginx (172.18.0.4:8001)
│   └── [all services as containers]
└── sql/                   # Database schemas
```

## Common Development Commands

### Build & Package

```bash
# Build all modules
mvn clean install

# Build specific module
mvn clean install -pl hcp-auth
mvn clean install -pl hcp-modules/hcp-system

# Build with specific profile (dev/local/prod)
mvn clean install -Pdev
mvn clean install -Plocal -pl hcp-system

# Package without running tests
mvn clean package -DskipTests
```

### Running Services

**Option 1: Using Spring Boot Maven Plugin**
```bash
# Run specific service
mvn spring-boot:run -pl hcp-gateway -Dspring-boot.run.profiles=dev
mvn spring-boot:run -pl hcp-modules/hcp-system -Dspring-boot.run.profiles=dev

# Run with JVM options
mvn spring-boot:run -pl hcp-auth -Dspring-boot.run.profiles=dev -Dspring-boot.run.jvmArguments="-Xms512m -Xmx1024m"
```

**Option 2: From bin/ directory (Windows batch files)**
```bash
cd bin
run-modules-system.bat  # Run system module
run-gateway.bat         # Run gateway
run-auth.bat            # Run auth service
run-monitor.bat         # Run monitor
```

**Option 3: Using JAR files (after building)**
```bash
java -Dfile.encoding=utf-8 -Xms512m -Xmx1024m -XX:MetaspaceSize=128m -XX:MaxMetaspaceSize=512m \
  -jar hcp-gateway/target/hcp-gateway.jar \
  --spring.profiles.active=dev
```

### Database Setup

**Using Docker Compose:**
```bash
cd docker
docker-compose up -d hcp-mysql hcp-redis hcp-nacos

# View logs
docker-compose logs -f hcp-mysql

# Initialize database (scripts in docker/mysql/db/)
```

**Manual MySQL setup:**
```bash
# Connect to MySQL
mysql -h127.0.0.1 -uroot -ppassword

# Import schemas (in sql/ directory)
mysql -h127.0.0.1 -uroot -ppassword vctgo_platform < sql/*.sql
```

### Configuration

Configuration is stored in **Nacos Config Center** with namespace `hcp`. Each service reads from:
- `application-{profile}.yml` in Nacos
- Local `bootstrap.yml` for service discovery settings

Key configuration locations:
- All services: `src/main/resources/bootstrap.yml` (service name, Nacos server, profile)
- Nacos configs: `{nacos-server}/nacos/v1/cs/configs` with dataId pattern `application-{profile}.yml`

### Testing

**No formal test infrastructure found** - this project focuses on runtime validation. To add tests:
```bash
# If tests are added
mvn test
mvn test -pl hcp-system
mvn test -Dtest=UserServiceTest
```

**Manual testing approach:**
1. Start infrastructure: `docker-compose up -d`
2. Start services in order:
   ```bash
   mvn spring-boot:run -pl hcp-register -Dspring-boot.run.profiles=dev
   mvn spring-boot:run -pl hcp-gateway -Dspring-boot.run.profiles=dev
   mvn spring-boot:run -pl hcp-auth -Dspring-boot.run.profiles=dev
   mvn spring-boot:run -pl hcp-modules/hcp-system -Dspring-boot.run.profiles=dev
   ```
3. Access Gateway at `http://localhost:38080`
4. Monitor at `http://localhost:39100` (Spring Boot Admin)

## Architecture Overview

### Service Dependencies & Communication Flow

```
Client (Web/APP/MiniProgram)
    ↓
Nginx (Port 8001)
    ↓
Spring Cloud Gateway (38080) ← Entry point with Sentinel flow control
    ↓
Internal Services (Registered in Nacos):
    ├── hcp-auth (39200) ← JWT-based authentication
    ├── hcp-system (39201) ← User/Role/Permission management
    ├── hcp-gen (39202) ← Code generation
    ├── hcp-job (39204) ← Quartz scheduled tasks
    ├── hcp-file (39300) ← File upload/storage (OSS, COS, etc.)
    ├── hcp-mp ← WeChat Mini Program integration
    ├── hcp-operator ← Charging station operator logic
    └── hcp-simulator ← Hardware simulation for testing
```

### Key Integration Patterns

**1. Multi-Tenancy**
- Implemented via `hcp-common-mybatisplus` tenant plugin
- All services support tenant isolation through `tenant_id` column
- Configured in `MyBatisPlusProperties`

**2. Distributed Transactions**
- Seata integration via `hcp-common-seata`
- Annotation: `@GlobalTransactional` for saga management
- Supports multi-datasource scenarios

**3. Data Source Management**
- `hcp-common-datasource` provides dynamic datasource switching
- Supports multiple database types via `dynamic-datasource-spring-boot-starter`
- Configured per-service in Nacos config

**4. Security Model**
- JWT tokens via `hcp-auth`
- RBAC (Role-Based Access Control) in `hcp-system`
- Data scope filtering via `hcp-common-datascope`
- All services use `@EnableHcpFeignClients` for service-to-service calls

**5. API Documentation**
- Swagger/OpenAPI 3 via `hcp-common-swagger`
- Annotate controllers with `@ApiOperation`
- Access docs at `{service}/doc.html`

### Critical Configuration Points

**Service Ports (default dev profile):**
- Gateway: 38080
- Auth: 39200
- System: 39201
- Gen: 39202
- Demo: 39203
- Job: 39204
- File: 39300
- Monitor: 39100

**Nacos Configuration:**
- Server: localhost:8848
- Namespace: `hcp`
- Each service must have `bootstrap.yml` with correct `spring.application.name`

**Redis Configuration:**
- Host: 172.18.0.3:6379 (Docker) or localhost:6379
- Used for: Caching, distributed locks, queues (Redisson)

**MySQL Configuration:**
- Host: 172.18.0.2:3306 (Docker) or localhost:3306
- Database: `vctgo_platform`
- Username: root, Password: password

## Development Workflow

### Starting Development Environment

1. **Start infrastructure:**
   ```bash
   cd docker
   docker-compose up -d
   ```

2. **Wait for Nacos to be ready (10-15 seconds)**

3. **Configure services in Nacos:**
   - Login to Nacos: http://localhost:8848/nacos (nacos/nacos123)
   - Create namespace: `hcp`
   - Add config for each service: `application-dev.yml`

4. **Start services (order matters):**
   ```bash
   # Core services first
   mvn spring-boot:run -pl hcp-gateway -Dspring-boot.run.profiles=dev
   mvn spring-boot:run -pl hcp-auth -Dspring-boot.run.profiles=dev
   mvn spring-boot:run -pl hcp-modules/hcp-system -Dspring-boot.run.profiles=dev

   # Business services
   mvn spring-boot:run -pl hcp-modules/hcp-file -Dspring-boot.run.profiles=dev
   mvn spring-boot:run -pl hcp-modules/hcp-gen -Dspring-boot.run.profiles=dev
   mvn spring-boot:run -pl hcp-visual/hcp-monitor -Dspring-boot.run.profiles=dev
   ```

### Adding a New Service

1. Create module in appropriate directory
2. Add to parent `pom.xml` modules list
3. Create `src/main/java/{package}/XxxApplication.java`
4. Add required `@EnableXxx` annotations (from `hcp-common-*`)
5. Create `src/main/resources/bootstrap.yml`
6. Configure Nacos config entry
7. Document API in Swagger

### Code Generation

The `hcp-gen` module provides CRUD code generation:
- Design database table structure
- Access: http://localhost:39202
- Generate: Entity, Mapper, Service, Controller, VO, HTML pages
- Supports multi-datasource and dynamic tenant

## Important Notes

- **Build Profile:** Default is `dev`. Use `-Pprod` for production builds
- **Java Version:** Strictly Java 8 - do not upgrade without testing
- **Nacos Dependency:** All services require Nacos for config and discovery
- **Test Infrastructure:** Minimal - rely on integration testing via Docker
- **Legacy References:** Some batch files reference old `vctgo-*` naming - use `hcp-*` consistently
- **Documentation:** SpringDoc-based API docs available at `/doc.html` per service
- **Monitoring:** Spring Boot Admin UI at http://localhost:39100 (hcp-monitor)

## Service Communication

Services communicate via:
1. **Feign Clients:** Use `@EnableHcpFeignClients` and `@FeignClient` annotations
2. **REST Templates:** For synchronous HTTP calls
3. **Message Queues:** For async events (RabbitMQ/Kafka if configured)
4. **Direct Database:** For shared data access (not recommended between services)

All inter-service calls go through the Gateway (38080) or use direct Feign client registration.