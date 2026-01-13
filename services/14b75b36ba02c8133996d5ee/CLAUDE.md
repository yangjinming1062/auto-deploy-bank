# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **zlt-microservices-platform** - an enterprise-grade microservices platform based on Spring Cloud. It's a multi-module Maven project with Java 17, Spring Boot 3.1.6, and Spring Cloud 2022.0.4. The platform provides a complete microservices solution including authentication (Spring Authorization Server), API gateway, monitoring, configuration management, and business services.

**Documentation**: https://www.kancloud.cn/zlt2000/microservices-platform/919418
**Demo**: http://zlt2000.cn (admin/admin)

## Module Architecture

### Core Modules

**zlt-commons** - Contains reusable Spring Boot Starters:
- `zlt-common-core` - Core utilities
- `zlt-common-spring-boot-starter` - Common functionality
- `zlt-db-spring-boot-starter` - Database operations (MyBatis-Plus, Druid)
- `zlt-redis-spring-boot-starter` - Redis integration (Redisson)
- `zlt-log-spring-boot-starter` - Logging utilities
- `zlt-auth-client-spring-boot-starter` - OAuth2/JWT client support
- `zlt-elasticsearch-spring-boot-starter` - Elasticsearch integration
- `zlt-oss-spring-boot-starter` - Object storage (Aliyun OSS, Qiniu, AWS S3, FastDFS)
- `zlt-loadbalancer-spring-boot-starter` - Load balancing and Feign
- `zlt-sentinel-spring-boot-starter` - Sentinel integration
- `zlt-zookeeper-spring-boot-starter` - Zookeeper integration

**zlt-uaa** - Authentication server (port 8000)
- Spring Authorization Server 1.1.3
- OAuth2 + JWT + RBAC implementation
- Supports multi-tenant application isolation

**zlt-gateway** - API Gateway (port 9900)
- Spring Cloud Gateway
- Routes requests to microservices

**zlt-monitor** - Monitoring suite
- `sc-admin` - Spring Boot Admin (port 6500) for application monitoring
- `log-center` - Centralized logging (port 7200)

**zlt-business** - Business services
- `user-center` - User management (port 7000)
- `file-center` - File service (port 5000)
- `search-center` - Search service (port 7100)
- `code-generator` - Code generator (port 7300)

**zlt-register** - Service Discovery
- Nacos (port 8848)

**zlt-config** - Configuration Center
- Nacos Config

**zlt-web** - Frontend applications
- Layui and React frontends (port 8066)

**zlt-demo** - Example implementations
- Seata, RocketMQ, Sharding-JDBC, SSO, WebSocket demos

## Development Commands

### Build and Test

```bash
# Build entire project (skips tests by default)
mvn clean package

# Build and run tests
mvn clean package -DskipTests=false

# Run a single test
mvn test -Dtest=ClassName#methodName

# Skip tests during build
mvn clean package -Dmaven.test.skip=true
```

### Run Specific Services

```bash
# Start Nacos (standalone mode)
cd zlt-register/nacos/bin
./startup.sh -m standalone

# Start specific service
cd zlt-uaa
mvn spring-boot:run

# Or use Maven with profile
mvn spring-boot:run -Dspring-boot.run.profiles=dev
```

### Docker Operations

Build Docker images:
```bash
mvn clean package docker:build -DskipTests
```

Docker images are available for: zlt-uaa, user-center, zlt-doc

### Maven Tips

```bash
# Build specific module
mvn clean install -pl zlt-commons -am

# Skip integration tests
mvn clean install -Dit.test='!*IT'

# Run with specific profile
mvn spring-boot:run -Dspring-boot.run.profiles=dev,devdb

# Clean and rebuild from scratch
mvn clean
mvn dependency:resolve
mvn compile
```

## Technology Stack

- **JDK**: 17
- **Spring Boot**: 3.1.6
- **Spring Cloud**: 2022.0.4
- **Spring Cloud Alibaba**: 2022.0.0.0
- **Spring Authorization Server**: 1.1.3
- **Database**: MySQL 8, Druid 1.2.18, MyBatis-Plus 3.5.4.1
- **Cache**: Redis with Redisson 3.25.0
- **Search**: Elasticsearch 7.13.4
- **Message Queue**: RocketMQ (in demos)
- **Monitoring**: Spring Boot Admin 3.1.8, SkyWalking, ELK
- **Object Storage**: Aliyun OSS, Qiniu, AWS S3, FastDFS
- **Distributed Transactions**: Seata (in demos)
- **API Docs**: Knife4j 4.3.0

## Configuration

Services use Spring profiles. Key configuration files:
- `bootstrap.yml` - Bootstrap configuration (Nacos discovery/config)
- `application.yml` - Service configuration

Default profiles:
- `dev` - Development
- `prod` - Production

## Testing

Test structure:
- JUnit 5 + Spring Boot Test
- Test classes are in `src/test/java`
- Integration tests available in `zlt-demo` modules

Run tests:
```bash
# All tests
mvn test

# Specific module
cd zlt-commons && mvn test

# With coverage
mvn jacoco:report
```

## Key Development Notes

1. **Authentication**: All services should integrate with UAA using `zlt-auth-client-spring-boot-starter`
2. **Configuration**: Externalized to Nacos. Check `bootstrap.yml` for discovery/config server settings
3. **Database**: MyBatis-Plus is the ORM. Use `@MapperScan` for DAO interfaces
4. **API Documentation**: Knife4j provides Swagger UI at `/doc.html`
5. **Starters**: Use the provided Spring Boot Starters for consistent cross-cutting concerns
6. **Port Allocation**: Each service has a dedicated port (see architecture section)
7. **Multi-tenancy**: Application-based isolation. Check UAA for tenant management

## Common Development Tasks

### Adding a New Service

1. Create module directory structure
2. Add to parent `pom.xml` modules section
3. Configure `bootstrap.yml` with Nacos discovery/config
4. Integrate with `zlt-auth-client-spring-boot-starter`
5. Add `application.yml` with service configuration
6. Create Dockerfile (optional)

### Creating a New Starter

1. Create module under `zlt-commons/`
2. Add auto-configuration class in `src/main/java`
3. Add `spring.factories` in `src/main/resources/META-INF/`
4. Create `pom.xml` with `spring-boot-configuration-processor`
5. Document configuration properties

### Debugging Services

```bash
# Enable debug logging
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005"

# Or add to application.yml
logging:
  level:
    com.zlt: DEBUG
```

## Important Resources

- **Online Docs**: https://www.kancloud.cn/zlt2000/microservices-platform/919418
- **Project Updates**: https://www.kancloud.cn/zlt2000/microservices-platform/936235
- **F&Q**: https://www.kancloud.cn/zlt2000/microservices-platform/981382
- **Gitee**: https://gitee.com/zlt2000/microservices-platform
- **GitHub**: https://github.com/zlt2000/microservices-platform

## Notes

- Maven surefire plugin is configured to skip tests by default in `pom.xml:417-425`
- The project uses Aliyun Maven repository mirror
- Code generation is available in `zlt-business/code-generator`
- Demo applications in `zlt-demo` showcase various integration patterns