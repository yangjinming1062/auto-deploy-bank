# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

wego is a campus community forum application with a Java Spring Boot backend and Vue.js frontend. It provides user authentication (SMS, password, GitHub/QQ OAuth), article management, likes/comments, follower system, notifications, and 1-on-1 messaging.

## Development Commands

### Backend (Java/Spring Boot)

```bash
# Build the project
mvn clean package

# Run the application
mvn spring-boot:run
# Or run WegoApplication.java directly (port 8081)
```

### Frontend (Vue.js)

Located in `/home/ubuntu/deploy-projects/0e5d5f18b9d955e2b8c33d80/web`:

```bash
# Install dependencies (use Node v15.14.0)
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Lint code
npm run lint
```

### Database Setup

Import `/home/ubuntu/deploy-projects/0e5d5f18b9d955e2b8c33d80/wego.sql` into MySQL 8.0. Database name: `wego`.

## Architecture

### Backend Layer Structure (MVC)

- **controller/** - REST API endpoints (ArticleController, UserController, LikeController, etc.)
- **service/** - Business logic with impl/ subdirectory for implementations
- **dao/** - MyBatis data access with annotation-based SQL queries
- **entity/** - JPA/Hibernate entity classes
- **vo/** - View objects for API responses

### Key Subsystems

**Async Event System** (`async/`):
- `EventModel` - Event data model with type, actorId, entityId, etc.
- `EventProducer` - Pushes events to Redis list queue
- `EventConsumer` - Polls queue and dispatches to handlers
- Handlers in `async/handler/` (LikeHandler, CommentHandler, FollowHandler)

**Redis Usage** (`redis/`):
- `JedisService` - Redis operations for caching, rankings, follow/fans sets
- Key prefixes: LikeKey, FollowKey, FansKey, UserTokenKey, VerifyCodeKey
- Used for async event queue and like count caching

**Elasticsearch** (`dao/ElasticSearchDao.java`):
- Full-text search for articles (title and content)
- Data synced from MySQL via Logstash
- Used when MySQL fuzzy queries become slow (>100K records)

**Quartz Scheduled Tasks** (`task/`):
- `LikeTask` - Syncs like counts from Redis to MySQL every 2 hours
- `AchieveValueTask` - Monthly achievement leaderboard reset

**WebSocket** (`websocket/ChatEndPoint.java`):
- 1-on-1 private messaging between users

**Configuration** (`config/`):
- `RedisConfig.java` - Jedis connection pool
- `QuartzConfig.java` - Job scheduling
- `WebSocketConfig.java` - STOMP messaging
- `CorsConfiguration.java` - Cross-origin settings
- OAuth configs for GitHub and QQ

## External Services

Configure in `application.properties`:
- **MySQL** (8.0) - Primary database
- **Redis** - Caching and async queue
- **Elasticsearch** (7.0.0) - Full-text search
- **Qiniu Cloud** - Image storage
- **Tencent Cloud SMS** - Phone verification
- **GitHub/QQ OAuth** - Third-party login

## Important Notes

- Spring Boot 2.3.0.RELEASE with Java 8
- Frontend uses Vue 2.6.x with ElementUI
- Use `tinyInt1isBit=false` when syncing MySQL to ES to avoid boolean type issues
- Quartz jobs sync Redis data to MySQL for consistency
- Frontend polls notification API every 3 seconds for async updates