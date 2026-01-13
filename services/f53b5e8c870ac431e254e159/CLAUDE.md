# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Chinese parking management system** (停车场管理系统) with integrated charging pile functionality. It's a large-scale IoT cloud platform built with Spring Cloud Alibaba microservices architecture, designed for parking lot operations, charging infrastructure, and property management.

**Tech Stack:**
- **Backend**: Java 8, Spring Boot 2.6, Spring Cloud Alibaba, Dubbo 3.2
- **Authentication**: OAuth2 + JWT
- **Database**: MySQL (primary), MongoDB (non-critical data), Redis (cache)
- **Messaging**: Netty 4 for real-time communication
- **File Storage**: FastDFS/MinIO/Aliyun OSS/Qiniu Cloud
- **Microservices Registry**: Nacos, Zookeeper
- **Distributed Transactions**: Seata
- **Circuit Breaker**: Sentinel

## Common Commands

### Building the Project

```bash
# Build all modules from parent directory
cd cf-framework-parent
mvn clean install

# Build specific module
mvn clean install -pl cf-ucenter -am
```

### Running the Application

```bash
# Package the project
./package.sh

# Start all services (runs all JARs in sequence with delays)
./start.sh

# Stop all services (kills processes on ports 8080-8100)
./stop.sh
```

### Service Startup Order

Services must be started in this specific order (handled by `start.sh`):
1. SMS service (port 8080)
2. User center service (port 8081)
3. User center auth (port 8082)
4. User center API (port 8083)
5. User center admin (port 8084)
6. File service (port 8085)
7. Payment service (port 8086)
8. File API (port 8087)
9. Car park service (port 8088)
10. Payment API (port 8089)
11. Car park API (port 8090)
12. Car park admin (port 8091)
13. Payment admin (port 8092)
14. Ad service (port 8093)
15. Ad API (port 8094)
16. Ad admin (port 8095)

## Architecture Overview

### Module Structure

The project follows a **layered microservices architecture** with domain-driven design. Each business module contains these layers:

- **-domain**: Entity models and value objects
- **-dao**: Data access layer (MyBatis)
- **-interface**: Service interfaces and DTOs
- **-service**: Business logic implementation
- **-api**: REST API controllers (external-facing)
- **-admin**: Admin panel controllers (internal management)

### Core Modules

**cf-framework-*** (Shared):
- `cf-framework-common`: Common utilities, configurations, annotations
- `cf-framework-model`: Shared data models
- `cf-framework-utils`: Helper classes and utilities

**cf-ucenter**: User management and authentication
- User registration, login, OAuth2/JWT token management
- Permissions and role-based access control
- **Ports**: 8081-8084

**cf-sms**: SMS notification service
- SMS sending via Aliyun SMS
- **Port**: 8080

**cf-pay**: Payment processing
- WeChat Pay, Alipay, UnionPay integration
- Supports payment splitting per parking lot
- **Ports**: 8086, 8089, 8092

**cf-file**: File storage service
- Integration with FastDFS, MinIO, Aliyun OSS
- **Ports**: 8085, 8087

**cf-car-park** (in cf-internet-of-things/cf-car-park):
- Core parking management functionality
- Camera integration for license plate recognition
- Parking record management, fee calculation
- **Ports**: 8088, 8090, 8091

**cf-charging** (in cf-internet-of-things/cf-charging):
- Electric vehicle charging pile management
- Charging session tracking, billing

**cf-chat**: Instant messaging (IM)
- Real-time chat functionality
- WebSocket-based communication using Netty 4

**cf-ad**: Advertisement management
- Banner ads, promotional content

**cf-position**: Geographic position/location data

**cf-logistics**: Logistics management module

### Data Storage

- **MySQL 5.6+**: Critical business data (parking records, payments, users)
- **MongoDB**: Non-critical data (chat messages, notifications, ads)
- **Redis**: Caching layer for sessions, frequently accessed data
- **Zookeeper**: Service registry and configuration center

### Service Communication

- **Dubbo RPC**: Inter-service communication
- **REST APIs**: External client communication
- **Netty 4**: Real-time messaging (IM, hardware communication)

## Configuration

Each service has configuration files in `src/main/resources/`:
- `application.yml`: Main configuration
- `config/`: Environment-specific configs
- `logback-spring.xml`: Logging configuration

**Important**: OAuth2 requires public/private key pairs to be configured in the admin directory. See README.md for setup instructions.

## Database

- Schema: `caifeng.sql`
- Pre-built database: `caifeng-db.ndm2`
- **Required**: MySQL 5.6+, MongoDB, Redis

## Hardware Integration

The system integrates with parking hardware (cameras, barriers, charging stations):
- Cameras push recognition data via HTTP
- Long connections (Netty) send control commands back to hardware
- Validates hardware IDs and serial numbers to prevent unauthorized data

## Development Notes

- **Language**: All code comments and documentation are in Chinese
- **Spring Boot Version**: 2.6 (upgradeable to 3.0)
- **Java Version**: 1.8+
- **Architecture Pattern**: Microservices with domain-driven design
- **Build Tool**: Maven
- **No Unit Tests**: The project appears to have minimal or no automated tests

## Key Files

- `README.md`: Comprehensive documentation in Chinese
- `start.sh`: Service startup orchestration script
- `stop.sh`: Service shutdown script
- `package.sh`: Build and packaging script
- `nginx.conf`: Reverse proxy configuration
- `plan.txt`: Project planning document

## Development Recommendations

- Start services individually during development using `java -jar` commands
- Check service logs in `./log/` directory
- Use `netstat -nlp` to verify service ports
- Configure OAuth2 keys before running authentication-dependent services
- Refer to online documentation: https://www.showdoc.com.cn/cfzhv3/10115551424871318