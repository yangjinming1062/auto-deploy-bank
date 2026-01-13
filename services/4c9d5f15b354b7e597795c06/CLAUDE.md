# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **java-sec-code**, an educational Java project demonstrating common security vulnerabilities. It's a Spring Boot 1.5.1 application with MyBatis ORM, MySQL database, and Spring Security authentication.

## Architecture

The application follows a standard Spring MVC layered architecture:

- **Controllers** (`src/main/java/org/joychou/controller/`): Each controller demonstrates a specific vulnerability type (SQL injection, XSS, RCE, XXE, SSRF, etc.)
- **Security Configuration** (`src/main/java/org/joychou/security/WebSecurityConfig.java`): Spring Security setup with CSRF, CORS, and authentication
- **Application Configuration** (`src/main/java/org/joychou/config/WebConfig.java`): Centralized configuration for security settings, SSRF protection, JSONP callbacks
- **Data Layer** (`src/main/java/org/joychou/dao/`, `mapper/`): MyBatis DAOs and XML mappers for database access
- **Utilities** (`src/main/java/org/joychou/util/`): Helper classes (JWT, HTTP, cookie utilities)
- **Main Application** (`src/main/java/org/joychou/Application.java`): Spring Boot entry point

Vulnerability demonstrations are organized by controller:
- `/rce/*` - Remote Code Execution (Runtime.exec, ProcessBuilder, ScriptEngine, Yaml, Groovy)
- `/sqli/*` - SQL Injection
- `/xss/*` - Cross-Site Scripting
- `/xxe/*` - XML External Entity
- `/ssrf/*` - Server-Side Request Forgery
- `/deserialization/*` - Java Deserialization
- `/fastjson/*` - FastJSON vulnerabilities
- And many more...

## Common Commands

### Build & Run
```bash
# Build the project
mvn clean package

# Run with Maven (requires MySQL running)
mvn spring-boot:run

# Run as JAR (after building)
java -jar target/java-sec-code-1.0.0.jar

# Build and run JAR (no tests)
mvn clean package -DskipTests
java -jar target/java-sec-code-1.0.0.jar

# Run tests
mvn test

# Run single test class
mvn test -Dtest=QLExpressTest
```

### Docker Deployment
```bash
# Start application and MySQL
docker-compose up

# Stop and remove containers
docker-compose down

# Pull latest images then start
docker-compose pull && docker-compose up
```

### Tomcat Deployment
```bash
# Build WAR package
mvn clean package

# Copy WAR to Tomcat webapps (adjust paths as needed)
cp target/java-sec-code-1.0.0.war /path/to/tomcat/webapps/

# Access at: http://localhost:8080/java-sec-code-1.0.0/
```

**Note**: For Tomcat, change packaging from `jar` to `war` in `pom.xml` first.

### Database Setup

**Manual Setup:**
- MySQL database: `java_sec_code`
- Username: `root`
- Password: `woshishujukumima`
- Connection URL: `jdbc:mysql://localhost:3306/java_sec_code`

Execute the SQL script:
```bash
mysql -u root -p < src/main/resources/create_db.sql
```

**Docker Setup:**
The docker-compose.yml automatically starts MySQL. The database is initialized with the users table.

## Access & Authentication

- **Application URL**: http://localhost:8080
- **Login Page**: http://localhost:8080/login

**Default Users:**
- admin / admin123 (ADMIN role)
- joychou / joychou123 (USER role)

**Public Endpoints** (no login required):
- Static resources: `/css/**`, `/js/**`
- Vulnerability demos: `/rce/**`, `/xxe/**`, `/fastjson/**`, `/xstream/**`, `/ssrf/**`, `/deserialize/**`, `/test/**`, `/ws/**`, `/shiro/**`, `/spel/**`, `/qlexpress/**`

## Testing Examples

Test RCE endpoint:
```bash
curl "http://localhost:8080/rce/runtime/exec?cmd=whoami"
```

Test SQL Injection:
```bash
curl "http://localhost:8080/sqli/vuln1?username=admin' OR '1'='1"
```

## Key Configuration Files

- **`src/main/resources/application.properties`**: Main configuration (database, CSRF, JSONP, SSRF settings)
- **`src/main/java/org/joychou/security/WebSecurityConfig.java`**: Security rules, CSRF configuration, CORS
- **`src/main/java/org/joychou/config/WebConfig.java`**: Property loading for filters and security checks
- **`src/main/resources/create_db.sql`**: Database initialization script
- **`src/main/resources/logback-online.xml`**: Logging configuration for production

## Development Notes

- Spring Boot version: **1.5.1.RELEASE**
- Java version: **1.8**
- Packaging: Defaults to `jar` (can be changed to `war` for Tomcat)
- MyBatis for database ORM with XML mappers
- Thymeleaf for server-side HTML templating
- Swagger enabled for API documentation at `/swagger-ui.html`
- Spring Boot Actuator enabled (security disabled) for monitoring endpoints

## Adding New Vulnerabilities

1. Create controller in `src/main/java/org/joychou/controller/`
2. Add `@RestController` and `@RequestMapping` annotations
3. Document the vulnerability and fix in comments
4. Update `src/main/resources/application.properties`:
   - Add endpoint to `joychou.no.need.login.url` if testing without authentication
   - Add to CSRF exclusion list if needed: `joychou.security.csrf.exclude.url`
5. Test the vulnerability and remediation

## Vulnerability Test Classes

Located in `src/main/test/org/test/`:
- `QLExpressTest.java`: QLExpress expression engine security tests
- `XStreamTest.java`: XStream deserialization security tests

Run individual test:
```bash
mvn test -Dtest=QLExpressTest
```