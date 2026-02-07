# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal blog website built with Spring Boot 3.0.5 and Java 17. Deployed as a WAR file running on embedded Tomcat.

## Build Commands

```bash
# Build the project (outputs to target/newblog.war)
mvn clean package

# Run locally for development
mvn spring-boot:run

# Run with specific profile
mvn spring-boot:run -Dspring.profiles.active=dev
```

## Architecture

### Core Components
- **Controllers** (`controller/`) - REST endpoints and page controllers using `@Controller` and `@ResponseBody`
- **Services** (`service/`) - Business logic layer with interfaces in `service/` and implementations in `service/impl/`
- **Models** (`model/`) - Entity classes (Blog, User, Category, etc.) and data transfer objects
- **DAOs** (`dao/`) - MyBatis-Plus mapper interfaces for database access

### Key Subsystems
- **Lucene Search** (`lucene/BlogIndex.java`) - Full-text search with Chinese analyzer and autocomplete
- **WebSocket** (`websocket/`) - Real-time communication for server monitoring updates
- **Task Scheduling** (`task/`, `config/ScheduledConfig.java`) - Scheduled jobs for analytics and maintenance
- **Logging** (`log/`, `logback-spring.xml`) - Kafka appender integration for centralized logging
- **JMX** (`jmx/`) - Server metrics monitoring via JMX beans

### Configuration
- **Profiles**: `dev`, `prod` (see `application-dev.yml`, `application-prod.yml`)
- **Common config**: `application-common.yml` - Server port, cache, MVC view settings
- **Environment variables**: `load.properties` for credentials and API keys
- **System property**: `myblog.path` - Base path for Lucene indexes

### View Layer
- JSP-based views in `src/main/webapp/` with prefix `/` and suffix `.jsp`
- Static resources (Bootstrap, jQuery, ECharts) in `webapp/`

### Data Flow
- Controllers receive HTTP requests → call Services → access DAOs → return ModelAndView or JSON
- Redis caching via `RedisTemplate` with custom key generator (`cache/`)
- MyBatis-Plus for ORM with PageHelper for pagination

## Database

- MySQL with MyBatis-Plus mappers in `resources/mapper/`
- Connection configured in profile-specific yml files
- Uses `jakarta.servlet.jsp.jstl` for JSP taglibs

## Testing

Test files in `src/test/java/`:
- `BaseTest.java`, `CacheTest.java`, `MyBatisTest.java`, `SpringTest.java`
- Tests currently use commented-out SpringJUnit4ClassRunner setup

## Technology Stack

| Category | Technology |
|----------|------------|
| Framework | Spring Boot 3.0.5, Java 17 |
| ORM | MyBatis-Plus |
| Cache | Redis |
| Search | Lucene 7.1.0 with SmartChineseAnalyzer |
| Database | MySQL |
| Views | JSP + JSTL |
| Real-time | WebSocket |
| Monitoring | Spring Actuator, Prometheus |
| Logging | Logback with Kafka appender |
| HTTP Client | Apache HttpClient, RestTemplate |
| Utils | Guava, Gson, Joda-Time, Jsoup |