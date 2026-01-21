# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Ztuo/BIZZAN** is an open-source digital cryptocurrency trading exchange platform built with a Java Spring Cloud microservices architecture. The system supports spot trading, OTC (over-the-counter) trading, wallet operations, real-time market data, and includes both web and mobile (Android/iOS) frontends.

## High-Level Architecture

### Backend Services (00_Framework)
The backend is a Spring Cloud microservices ecosystem with the following key modules:

1. **cloud** - Spring Cloud Eureka service registry (port 7000)
2. **ucenter-api** - User management service (authentication, registration, profiles)
3. **exchange-api** - Trading API (orders, balances, history)
4. **market** - Market data service (prices, K-line charts, real-time trades)
5. **exchange** - Core matching engine (in-memory order matching, high-performance)
6. **wallet** - Cryptocurrency wallet service (deposits, withdrawals)
7. **otc-api** - Over-the-counter trading service
8. **chat** - Real-time communication (WebSocket/SpringSocket)
9. **admin** - Administrative interface service

**Critical Architecture Notes:**
- The `exchange` module is the **core matching engine** that processes orders entirely in memory using Java queues for maximum performance. It automatically loads unfinished orders from MongoDB on startup and sends trade records to the `market` module via Kafka.
- The `market` module handles database persistence and real-time WebSocket pushes to clients (SpringSocket for web, Netty for mobile).
- Services communicate through **Kafka** for event streaming and **Eureka** for service discovery.
- Database schema auto-migration is enabled via JPA: `spring.jpa.hibernate.ddl-auto=update`

### Frontend Applications
- **05_Web_Front** - Main trading web interface (Vue 2 + iView)
- **04_Web_Admin** - Administrative dashboard (Vue 2 + iView)
- **02_App_Android** & **03_APP_IOS** - Mobile applications

### Wallet RPC Services (01_wallet_rpc)
Independent cryptocurrency node services:
- bitcoin, eth, ltc, bch, bsv, eos, usdt, erc-token, etc.
- Each implements RPC interfaces for deposit/withdrawal operations

## Common Commands

### Backend Development (00_Framework)

**Build all services:**
```bash
cd 00_framework
mvn clean install -DskipTests
```

**Run a single service:**
```bash
cd 00_framework/{module-name}
mvn spring-boot:run
```

**Build specific modules (build core modules first):**
```bash
# Compile core dependencies first (required for QueryDSL)
mvn clean install -pl core,exchange-core,otc-core -am

# Then build other modules
mvn clean install
```

**Skip tests during build:**
```bash
mvn clean install -DskipTests
```

**Required IDE Setup:**
- Install **Lombok plugin** in your IDE (IntelliJ/Eclipse)
- JDK 1.8 or higher
- Maven 3.x

**Configuration Files:**
- Service configs: `00_Framework/{module}/src/main/resources/dev/application.properties`
- Profile-specific: `00_Framework/config/application-{dev|test|prod}.properties`

### Frontend Development

**Web Frontend (05_Web_Front):**
```bash
cd 05_Web_Front
npm install
npm run dev      # Hot reload on localhost:8080
npm run build    # Production build
npm run lint     # Lint code
```

**Admin Frontend (04_Web_Admin):**
```bash
cd 04_Web_Admin
npm install
npm run dev      # Development server
npm run build    # Production build
```

**Node Requirements:**
- Node.js 9.11.2 (05_Web_Front)
- npm 5.6.0

### Service Startup Sequence

**Production deployment order:**
```bash
# 1. Start infrastructure
# - MySQL, MongoDB, Redis, Kafka, Zookeeper

# 2. Start cloud registry first
java -jar cloud.jar

# 3. Start core services
java -jar market.jar
java -jar exchange.jar

# 4. Start API services
java -jar exchange-api.jar
java -jar ucenter-api.jar
java -jar otc-api.jar
java -jar chat.jar
java -jar wallet.jar
java -jar admin.jar
```

## Dependencies

**Infrastructure Services Required:**
- MySQL 5.5.16+ (primary database)
- MongoDB 3.6.13+ (K-line data, order history)
- Redis 3.2.100+ (caching, sessions)
- Kafka 2.11-2.2.1 (message queue)
- Zookeeper (Kafka coordination)

**External Services:**
- Alibaba Cloud OSS (file storage)
- SMS gateway (for 2FA)
- SMTP server (email verification)
- Blockchain nodes (Bitcoin, Ethereum, etc.)

## Configuration Management

**Key Configuration Properties:**

Database (MySQL):
```
spring.datasource.url=jdbc:mysql://...
spring.datasource.username=...
spring.datasource.password=...
```

Redis:
```
redis.host=...
redis.port=6379
redis.password=...
```

MongoDB:
```
spring.data.mongodb.uri=mongodb://...
```

Kafka:
```
spring.kafka.bootstrap-servers=...
```

**Development Tips:**
- Enable SQL logging for debugging: `spring.jpa.show-sql=true`
- Use profile-based configs: `-Dspring.profiles.active=dev|test|prod`
- All modules use JPA auto-migration (no manual schema updates needed)

## Service Ports (Default)

- cloud: 7000
- exchange: 6003
- market: 6004
- ucenter-api: 6001
- exchange-api: 6002
- admin: 6010
- chat: 6008
- wallet: 6007
- otc-api: 6006

## Technical Stack

**Backend:**
- Spring Boot 1.5.22
- Spring Cloud Edgware.RELEASE
- Spring Data JPA (QueryDSL for type-safe queries)
- MySQL, MongoDB
- Redis, Kafka
- Shiro (authentication)
- Netty (mobile push)

**Frontend:**
- Vue 2.5.x
- iView/View Design UI framework
- WebSocket (SpringSocket)
- Webpack 3.x

## Development Workflow

1. **Backend Development:**
   - Import `00_framework` as Maven project in IDE
   - Install Lombok plugin
   - Build core modules first (core, exchange-core, otc-core)
   - Start services via `mvn spring-boot:run` or IDE run configs

2. **Frontend Development:**
   - Each frontend is independent (separate package.json)
   - Use `npm run dev` for hot reload during development
   - Configure API endpoints in `src/config/api.js` (admin) or `src/main.js` (web)

3. **Testing Integration:**
   - Access service registry: http://localhost:7000
   - Frontend proxies configured via Nginx (see DEVELOP.md)
   - WebSocket endpoints support real-time updates

## Key Implementation Details

**Matching Engine (exchange):**
- In-memory order book using Java queues
- Processes orders without database IO for speed
- Auto-reloads unfinished orders on startup from MongoDB
- Sends trade events to Kafka consumed by market module

**Market Data (market):**
- Database persistence layer
- Real-time WebSocket pushes to connected clients
- SpringSocket for web clients
- Netty-based push for mobile clients

**Security:**
- Apache Shiro for authentication/authorization
- Redis-based session management
- JPA/Hibernate with QueryDSL for type-safe queries
- FastJSON 1.2.75+ (patches security vulnerabilities)

## Common Development Issues

1. **Lombok errors:** Install Lombok plugin in IDE
2. **QueryDSL errors:** Build core modules before other modules
3. **Missing dependencies:** Run `mvn clean install` from 00_framework root
4. **Redis Keyspace notifications:** Set `notify-keyspace-events=Egx` in Redis config
5. **MongoDB startup delays:** exchange module loads large order history on first run

## API Documentation

- REST APIs exposed by service modules
- WebSocket endpoints for real-time data in market module
- Service discovery via Eureka (http://localhost:7000)
- Admin panel for testing API endpoints

## Resources

- **README.md** - Chinese project documentation and deployment guide
- **README-EN.md** - English project documentation
- **DEVELOP.md** - Detailed local development instructions
- **09_DOC/** - Infrastructure setup guides (Redis, Kafka, MySQL, etc.)