# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ZDH is a **data collection, processing, monitoring, scheduling, and management一体化平台** (integrated big data platform). It's a Spring Boot web application (version 5.6.16-RELEASE) that provides:

- **Data ETL**: Extract, Transform, Load from/to multiple data sources (HDFS, Hive, JDBC, HTTP, Kafka, MongoDB, Redis, Cassandra, HBase, ES, SFTP)
- **Task Scheduling**: Quartz-based job scheduling system with dependency management
- **Data Quality**: Data validation and quality checks
- **Digital Marketing**: Customer management, labels, risk control, and marketing automation
- **Mock Services**: HTTP mock service integration

This is the **web management console** only. ETL processing is handled by separate services:
- `zdh_spark` (Spark-based ETL)
- `zdh_flinkx` (Flink SQL-based ETL)
- `zdh_mock` (HTTP mock service)
- `zdh_magic_mirror` (digital marketing modules)

## Required Environment

- **JDK 1.8** (strictly required - will not run on higher versions)
- **MySQL 8.0** (for application data and Quartz scheduling)
- **Redis** (for caching and session management)

## Development Commands

### Build
```bash
sh build.sh
```
This runs: `mvn clean package -Dmaven.test.skip=true`

### Run in Development
**⚠️ CRITICAL**: Must set environment variable before running:
```bash
export ZDH_RUN_MODE=prod  # or dev, tmp
# or for Windows:
set ZDH_RUN_MODE=prod
```

Then run with Maven:
```bash
mvn spring-boot:run
```

### Run from Built Package (5.1.1+)
```bash
cd zdh_web-5.6.16-RELEASE
sh bin/start.sh  # or sh bin/zdh_web.sh start
```

### Stop Application
```bash
sh bin/stop.sh
```

## Application Architecture

### Directory Structure
```
com.zyc.zdh/
├── annotation/           # Custom annotations (@MyMark, @White, @SortMark)
├── api/                  # API service interfaces (LoginService, PermissionApi)
├── aop/                  # AOP configuration and logging
├── cache/                # Redis-based caching layer
├── config/               # Spring configuration classes
│   ├── DruidDataSourceConfig.java
│   ├── QuartzConfig.java
│   ├── RedisConfig.java
│   ├── ShiroConfig.java
│   └── ...
├── controller/           # REST controllers (MVC layer)
│   ├── ZdhEtlController.java         # ETL task management
│   ├── ZdhDispatchController.java    # Scheduling
│   ├── ZdhDataSourcesController.java # Data source configs
│   ├── digitalmarket/    # Digital marketing modules
│   └── ...
├── dao/                  # MyBatis data access layer
├── service/              # Business logic layer
│   ├── EtlTaskService.java
│   ├── DispatchTaskService.java
│   └── impl/             # Service implementations
├── entity/               # Data models
├── jdbc/                 # Database utilities
├── job/                  # Quartz job implementations
├── shiro/                # Authentication/authorization
└── util/                 # Utility classes
```

### Key Components

**1. ETL Task Processing**
- Controllers: `ZdhEtlController`, `ZdhFlinkController`, `ZdhDataxController`, `ZdhJdbcController`
- Service: `EtlTaskService`
- Supports multiple engines: Spark, Flink, DataX, Kettle, JDBC

**2. Scheduling System**
- Quartz-based with MySQL persistence
- Clustered configuration (isClustered=true)
- Controller: `ZdhDispatchController`
- Service: `DispatchTaskService`
- Config: `QuartzConfig.java`

**3. Permission System**
- Apache Shiro integration
- Multi-dimensional permission control
- Controllers: `PermissionController`, `PermissionApiController`
- Service: `ZdhPermissionService`

**4. Data Sources**
- Supports: MySQL, PostgreSQL, Oracle, SQL Server, Hive, HDFS, Kafka, MongoDB, Redis, ElasticSearch, SFTP, etc.
- Controller: `ZdhDataSourcesController`
- Service: `DataSourcesService`

**5. Digital Marketing Module**
- Path: `controller/digitalmarket/`
- Features: Label management, customer segmentation, risk control, plugin system
- Sub-modules: label, plugin, ship, variable

## Configuration

### Environment Modes
- **prod**: Production environment
- **dev**: Development environment
- **tmp**: Temporary environment

Selected via `ZDH_RUN_MODE` environment variable, which maps to Spring Boot profiles.

### Key Configuration Files
- `release/conf/application-prod.properties` - Production config
- `release/conf/application-dev.properties` - Development config
- `release/conf/logback.xml` - Logging configuration

### Important Configurations
```properties
# Server
server.port=8081
myid=1  # Unique ID per instance (1,2,3... for clustering)

# Database
spring.datasource.url=jdbc:mysql://127.0.0.1:3306/zdh
spring.datasource.username=zyc
spring.datasource.password=123456

# Redis
spring.redis.hostName=127.0.0.1
spring.redis.port=6379

# Quartz Scheduler
zdh.schedule.quartz.auto.startup=true
zdh.schedule.org.quartz.jobStore.isClustered=true
```

## Database Schema

Database: MySQL 8.0
Schema Location: `release/db/zdh.sql`

Key Tables:
- `zdh_etl_task` - ETL task configurations
- `zdh_dispatch_task` - Scheduled jobs
- `zdh_data_sources` - Data source configurations
- `zdh_user`, `zdh_role`, `zdh_permission` - User management
- `QRTZ_*` - Quartz scheduler tables (must be uppercase)

## Key Dependencies

**Core Framework**
- Spring Boot 2.3.4.RELEASE
- Spring MVC + Shiro (authentication)
- MyBatis + MySQL
- Quartz 2.3.2 (scheduling)
- Redis (caching)

**Data Processing**
- Hadoop 2.7.5 (HDFS)
- Kafka 2.3.14 (messaging)
- Spark (via zdh_spark service)
- Flink (via zdh_flinkx service)
- Elasticsearch 7.6.1
- Kettle 9.4.0.1-467 (ETL)

**Others**
- Druid (database pooling)
- FastJSON
- PageHelper (pagination)
- Sentinel (flow control)
- POI (Excel processing)

## Development Notes

### Adding New Features

1. **New ETL Task Type**
   - Create controller in `controller/` directory
   - Implement service in `service/impl/`
   - Add data model in `entity/`
   - Update MyBatis mapper in `mapper/`

2. **Database Changes**
   - Modify `release/db/zdh.sql`
   - Run SQL scripts manually (no migrations)
   - Update base mappers if needed (path: `src/main/java/com/zyc/notscan/base/`)

3. **New Permissions**
   - Define in `zdp.init.roles` config (application-prod.properties)
   - Update Shiro realm if needed

### Testing
No formal test framework configured. Tests are skipped during build (`-Dmaven.test.skip=true`).

### Code Generation
- MyBatis generator plugin configured in `pom.xml`
- Config: `src/main/resources/mybatis-generator.xml`
- Run: `mvn mybatis-generator:generate`

### API Documentation
- Swagger/OpenAPI 3 via springdoc-openapi
- Access: `http://host:port/api-docs`
- Config in `OpenApiConfig.java`

## Deployment

### Production Deployment
1. Build: `sh build.sh`
2. Deploy the generated `zdh_web-5.6.16-RELEASE` directory
3. Configure MySQL and Redis
4. Update `conf/application-prod.properties` with correct database/Redis URLs
5. Set `ZDH_RUN_MODE=prod`
6. Start: `sh bin/start.sh`

### Clustering
- Multiple instances with different `myid` values
- Quartz clustering enabled for distributed scheduling
- Redis for shared session/cache

## Important Considerations

⚠️ **JDK Version**: Strictly requires JDK 1.8. Application will fail to start on newer versions.

⚠️ **Environment Variable**: `ZDH_RUN_MODE` MUST be set before application starts or it will exit with error.

⚠️ **Database Tables**: Quartz tables must use uppercase names (QRTZ_*).

⚠️ **No Tests**: Build skips tests. Manual testing required.

⚠️ **Separate ETL Services**: This is only the web console. Actual data processing runs in separate services (zdh_spark, zdh_flinkx, etc.).

## Troubleshooting

**Application won't start**
- Verify JDK 1.8: `java -version`
- Check `ZDH_RUN_MODE` environment variable is set
- Verify MySQL and Redis are running
- Check logs in `web.log`

**Quartz jobs not executing**
- Verify MySQL connection
- Check Quartz tables exist and are uppercase
- Ensure clustering is properly configured

**ETL tasks not running**
- This is the web console only
- Check zdh_spark/zdh_flinkx services are running
- Verify task is properly dispatched to execution service

## Related Repositories

- **zdh_spark**: https://github.com/zhaoyachao/zdh_server (Spark ETL)
- **zdh_flinkx**: https://github.com/zhaoyachao/zdh_flinkx (Flink ETL)
- **zdh_mock**: https://github.com/zhaoyachao/zdh_mock (Mock service)
- **zdh_magic_mirror**: https://github.com/zhaoyachao/zdh_magic_mirror (Digital marketing)

## Additional Resources

- Blog: https://blog.csdn.net/zhaoyachao123/article/details/113913947
- Demo: http://zycblog.cn:8081/login (user: zyc, pwd: 123456)