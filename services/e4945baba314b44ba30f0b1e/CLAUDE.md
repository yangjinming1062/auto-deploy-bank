# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spring松客服 (CSKeFu) is an open-source intelligent customer service system built on Spring Boot 3.1.0 with Java 17. It's a comprehensive contact center solution with multi-channel support, agent monitoring, CRM, chatbot integration, and enterprise chat features.

**Key Technologies:**
- Spring Boot 3.1.0, Java 17, Maven (multi-module)
- MySQL 5.7, Redis 5.0, ActiveMQ 5.14
- Socket.IO for real-time WebSocket communication
- PugJS template engine (spring-pug4j)
- Docker for containerized deployment
- Spring Security, JPA, Quartz Scheduler

## Development Setup

### Prerequisites
- Java 17+
- Maven 3.6+
- Docker and Docker Compose
- MySQL 5.7, Redis, ActiveMQ (via Docker)

### Development Commands

**Start dependencies (dev environment):**
```bash
./scripts/dev.sh
```

**Build the application:**
```bash
cd contact-center/app
mvn clean package
```
or use the build script:
```bash
cd contact-center
./admin/package.sh
```

**Run tests:**
```bash
cd contact-center/app
mvn test                    # Run all tests
mvn test -Dtest=ClassName   # Run specific test class
```

**Build and run with Docker:**
```bash
# Build Docker image
cd contact-center/admin
./build.sh

# Start full stack (app + dependencies)
cd /repo-root
./scripts/start.sh
```

**Clean containers and data:**
```bash
./scripts/clean.container.sh
```

## Architecture Overview

### Project Structure
```
contact-center/
├── app/                          # Main application module
│   ├── src/main/java/com/cskefu/cc/
│   │   ├── Application.java      # Spring Boot entry point
│   │   ├── basic/                # Core utilities and context
│   │   ├── controller/           # MVC controllers (admin, api, apps, auth, resource)
│   │   ├── service/              # Business logic services
│   │   ├── aspect/               # AOP aspects (agent status, sync database, etc.)
│   │   ├── config/               # Spring configuration
│   │   ├── activemq/             # Message queue configuration
│   │   └── util/                 # Utilities (REST API, FreeSWITCH, ES, etc.)
│   └── pom.xml
├── root/                         # Parent POM with dependencies
│   └── pom.xml
├── config/
│   ├── sql/                      # Database initialization scripts
│   └── lib/                      # External libraries
└── admin/                        # Build and deployment scripts
```

### Key Packages
- **com.cskefu.cc.controller**: REST API endpoints organized by domain (admin, api, apps, auth)
- **com.cskefu.cc.service**: Business logic layer
- **com.cskefu.cc.aspect**: Cross-cutting concerns via AOP
- **com.cskefu.cc.util**: Utilities for external integrations (wechat, aliyun, etc.)

### Database & Infrastructure
The application uses a microservices-style deployment with Docker Compose:
- **contact-center**: Main Spring Boot app (ports 8035 HTTP, 8036 WebSocket)
- **mysql**: MySQL 5.7 database (port 8037)
- **redis**: Redis caching (port 8041)
- **activemq**: Message broker (ports 8051 Admin UI, 8052 JMS, 8053 MQTT)

See `docker-compose.yml` for complete service configuration.

## Build & Deployment

### Maven Build
The project uses a multi-module Maven structure:
- `contact-center/root/pom.xml` - Parent POM defining dependencies and plugins
- `contact-center/app/pom.xml` - Application module WAR packaging

Build the application:
```bash
mvn -DskipTests clean package  # Skip tests during build
```

The build process:
1. Compiles Java sources
2. Runs tests (if not skipped)
3. Packages as WAR file with Spring Boot
4. Generates git.properties for version tracking

### Docker Build
Docker image is built via:
```bash
cd contact-center/admin
./build.sh  # Calls package.sh, then builds Docker image with tags
```

The Docker image (`cskefu/contact-center:develop`) includes:
- Packaged WAR file
- Configuration files from `config/sql/`
- Embedded Tomcat

### Environment Configuration
Key environment variables (see `docker-compose.yml`):
- `DB_PASSWD`: Database password (default: 123456)
- `CC_JAVA_XMX/XMS`: JVM heap memory (default: 12288m/2048m)
- `CC_WEB_PORT/CC_SOCKET_PORT`: HTTP/WebSocket ports (default: 8035/8036)
- `SPRING_DATASOURCE_URL/USERNAME/PASSWORD`: Database connection
- `SPRING_DATA_REDIS_HOST/PORT/PASSWORD`: Redis connection
- `SPRING_ACTIVEMQ_BROKER_URL`: ActiveMQ connection
- Module toggles: `CSKEFU_MODULE_CALLOUT`, `CSKEFU_MODULE_CONTACTS`, `CSKEFU_MODULE_CHATBOT`

## Testing

Unit tests are located in `app/src/test/java/` using JUnit 4.

Run tests:
```bash
cd contact-center/app
mvn test
```

Test classes follow naming convention `*Test.java`. Key test files include:
- `CronToolsTest.java`
- `ACDComposeContextTest.java`
- `MainContextTest.java`

## CI/CD

**CircleCI Pipeline:**
- Located at `.circleci/config.yml`
- Builds and pushes Docker image on `develop` branch
- Uses `cimg/openjdk:17.0.7` image
- Build steps:
  1. Checkout code
  2. Build contact-center Docker image
  3. Push to DockerHub

**Build process:**
```bash
cd contact-center && ./admin/build.sh
```

## Key Configuration Files

- **docker-compose.yml**: Full-stack deployment configuration
- **contact-center/Dockerfile**: Container image definition
- **contact-center/app/pom.xml**: Application build configuration
- **contact-center/root/pom.xml**: Parent POM with dependencies
- **contact-center/config/sql/**: Database initialization scripts
- **sample.env**: Environment variable template

## Development Guidelines

### Adding New Features
1. Follow Spring Boot MVC pattern (controller → service → repository)
2. Use AOP aspects for cross-cutting concerns (see `com.cskefu.cc.aspect`)
3. Add corresponding tests in `src/test/java`
4. Update database schema in `config/sql/` if needed
5. Document REST APIs in `config/postman/` if applicable

### Working with Databases
- MySQL schema initialization: `config/sql/*.sql`
- JPA entities in `com.cskefu.cc.model`
- Spring Data JPA repositories for data access
- Database migrations tracked via SQL files

### External Integrations
- **WeChat**: `com.chatopera.cc.wechat`
- **Aliyun SMS**: `aliyun-java-sdk-dysmsapi`
- **Chatopera Bot**: SDK for chatbot integration
- **FreeSWITCH**: VoIP integration utilities
- **Redis**: Caching and session storage
- **ActiveMQ**: Asynchronous messaging

## Common Tasks

**Add a new REST API endpoint:**
```java
@Controller
@RequestMapping("/api/newendpoint")
public class NewController {
    @Autowired
    private NewService newService;

    @RequestMapping(method = RequestMethod.GET)
    @ResponseBody
    public ResponseEntity<?> list() {
        return ResponseEntity.ok(newService.findAll());
    }
}
```

**Integrate with Redis:**
```java
@Autowired
private RedisTemplate<String, Object> redisTemplate;

// Use for caching
redisTemplate.opsForValue().set(key, value);
```

**Send messages via ActiveMQ:**
```java
@Autowired
private JmsTemplate jmsTemplate;

jmsTemplate.convertAndSend("queue.name", messageObject);
```

## Important Notes

- The project uses **Java 17** - ensure compatibility when adding dependencies
- **PugJS** is used instead of traditional JSP/Thymeleaf for templating
- **WAR packaging** with embedded Tomcat (Spring Boot traditionally uses JAR)
- **Chinese language** comments and documentation throughout codebase
- **Chatopera Nexus** (https://nexus.chatopera.com) hosts custom dependencies
- **Spring Boot 3.1.0** with Java 17+ requirement (see issue #714)

## References

- [Documentation Center](https://docs.cskefu.com/)
- [Developer Setup Guide](https://docs.cskefu.com/docs/osc/engineering)
- [GitHub Issues](https://github.com/cskefu/cskefu/issues)
- [REST API Documentation](https://docs.cskefu.com/docs/osc/restapi)