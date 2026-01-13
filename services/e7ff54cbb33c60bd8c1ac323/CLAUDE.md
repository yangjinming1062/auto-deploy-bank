# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start

**Build the project:**
```bash
mvn -DskipTests package
```

**Run the application:**
```bash
mvn spring-boot:run -pl easyreport-web
```

Then access the application at `http://localhost:8080`

## Project Overview

EasyReport is a simple, easy-to-use Web Report System for Java. It converts SQL query results into report pages with support for:
- Row/Column spanning (RowSpan/ColSpan)
- Excel export
- Chart visualization
- Fixed headers and left columns
- Scheduled tasks
- Big data query engines (Hive, Presto, HBase, Drill, Impala)
- REST API services
- Report permission control

## Maven Module Architecture

The project uses a multi-module Maven structure (Spring Boot 2.0.4.RELEASE):

### Core Modules

- **easyreport-common** - Shared utilities, enums, pairs, tree structures
- **easyreport-mybatis** - MyBatis configuration and data access layer
- **easyreport-support** - Supporting utilities and helpers
- **easyreport-meta** - Metadata management (data sources, reports, categories)
  - `domain/` - POJO entities
  - `service/` - Business logic
  - `data/` - MyBatis mappers
  - `form/` - Form objects

- **easyreport-engine** - Report generation engine
  - `ReportBuilder` interface and implementations
  - `AbstractReportBuilder`, `HorizontalStatColumnReportBuilder`, `VerticalStatColumnReportBuilder`
  - `ReportDirector` orchestrates report building
  - `ReportGenerator` generates final reports
  - `DataExecutor` executes queries
  - `query/` - Query parsing and execution
  - `dbpool/` - Database connection pooling (C3P0, Druid, DBCP2)

- **easyreport-queryer** - Query engine for multiple data sources
- **easyreport-scheduler** - Quartz-based scheduled tasks
- **easyreport-membership** - User management and authentication (Shiro-based)
- **easyreport-web** - Spring Boot web application
  - Controllers: `common/`, `home/`, `member/`, `report/`, `schedule/`
  - Views: Thymeleaf templates in `templates/`
  - Static assets: jQuery, EasyUI, vendor libraries in `static/`
  - Configuration: `config/`, `spring/`
  - Entry point: `WebApplication.java`

## Key Configuration

- **Main config:** `easyreport-web/src/main/resources/application.yml`
- **Property files by environment:**
  - Development: `src/main/filters/dev.properties` (default)
  - Test: `src/main/filters/test.properties`
  - Production: `src/main/filters/prod.properties`
- **Database schema:** `schema.sql` and `data.sql` (H2 in-memory by default)
- **MyBatis mappers:** `easyreport-web/src/main/resources/mybatis/`

## Database & Data Sources

**Default metadata database:** H2 (configured in application.yml)
**Supported data sources:**
- MySQL, Oracle, PostgreSQL, SQLServer
- Hive, Presto, HBase, Drill, Impala (via easyreport-queryer)

## Testing

Run tests for a specific module:
```bash
cd easyreport-web && mvn test
```

Run tests for all modules:
```bash
mvn test
```

CI pipeline (Travis CI) runs: `mvn install -DskipTests=true`

## API Documentation

- Swagger UI available at: `http://localhost:8080/swagger-ui.html`
- Spring Boot Admin for monitoring

## Security

- Apache Shiro for authentication and authorization
- Configuration in `easyreport-web/src/main/java/com/easytoolsoft/easyreport/web/config/`

## Frontend Stack

- **jQuery** with extensions
- **jQuery Validation**
- **EasyUI** for UI components
- **Juicer** for templating
- AMD module pattern in `static/js/`

## Build Profiles

The project uses Maven profiles:
- `dev` (default): Development settings
- `test`: Testing environment
- `prod`: Production deployment

## Docker Support

Docker builds via Spotify maven plugin in easyreport-web module.

## Technology Stack Highlights

- Spring Boot 2.0.4.RELEASE
- MyBatis 3.4.2 with Spring Boot Starter
- Apache Shiro 1.3.2 for security
- Thymeleaf 3.0.9 with Layout Dialect
- Quartz 2.2.3 for scheduling
- FastJSON 1.2.47 for JSON processing
- Apache Velocity 1.7 for templating
- Aviator 2.3.3 for expression evaluation
- Apache POI 3.15 for Excel export
- Java 8

## Development Notes

- Property placeholders (e.g., `@server.port@`) are resolved via Maven filtering
- Frontend assets are in `static/` with vendor libraries in `static/vendor/`
- The engine follows Builder pattern for report generation
- MyBatis is used for both metadata and report data queries
- The web module aggregates all other modules as dependencies