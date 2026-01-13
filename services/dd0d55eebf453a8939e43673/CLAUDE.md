# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hello Java Security is a vulnerability demonstration project that combines vulnerability scenarios with secure coding practices to help security and development teams understand vulnerability principles. The project showcases 35+ common security vulnerabilities with intentionally vulnerable code examples.

- **Default Credentials**: admin/admin
- **Default Port**: 8888
- **Default Login**: http://localhost:8888/login
- **Version**: 1.15
- **Status**: DEV/Beta

## Critical Requirements

- **JDK 1.8 is REQUIRED** - Higher Java versions will cause errors (see pom.xml:20)
- **MySQL Database** required (configured in docker-compose.yml:8.3.0)
- **Default MySQL credentials**: root/1234567, database: test

## Common Commands

### Build the Project
```bash
mvn clean package -DskipTests
```
This creates the JAR at `target/javasec-1.15.jar`

### Run Locally (Dev Mode)
```bash
java -jar target/javasec-1.15.jar --spring.profiles.active=dev
```

### Run with Docker Compose
```bash
mvn clean package -DskipTests
docker-compose up
```
This starts both MySQL and the application.

### Build and Run with Docker Only
```bash
./deploy.sh
```
Builds Docker image and runs on port 80.

### CodeQL Security Analysis
```bash
./codeql.sh
```
Runs CodeQL analysis and outputs to `codeql.csv`.

### Testing
```bash
mvn test
# Run specific test
mvn test -Dtest=HelloApplicationTests
```
Note: Only basic integration tests exist; most functionality requires manual testing via web UI.

## Architecture

The project is organized by vulnerability types in the `src/main/java/com/best/hello/controller` directory:

```
controller/
├── ComponentsVul/     # Vulnerable third-party components (Fastjson, XStream, Jackson)
├── Deserialization/   # Java deserialization vulnerabilities
├── IDOR/              # Insecure Direct Object References
├── JNDI/              # JNDI injection attacks
├── LogicFlaw/         # Business logic flaws
├── RCE/               # Remote Code Execution
├── RMI/               # RMI vulnerabilities
├── SQLI/              # SQL Injection (JDBC, Hibernate, MyBatis)
├── XSS/               # Cross-Site Scripting
├── XXE/               # XML External Entity
├── CSRF.java          # Cross-Site Request Forgery
├── CSVInjection.java  # CSV injection
├── CORS.java          # CORS misconfigurations
├── DoS.java           # Denial of Service
├── IPForgery.java     # IP forgery
├── JWT.java           # JWT vulnerabilities
├── Login.java         # Authentication
├── Redirect.java      # Open redirects
├── SSTI.java          # Server-Side Template Injection
├── SpEL.java          # Spring Expression Language injection
├── Traversal.java     # Directory traversal
├── Unauth.java        # Authorization bypasses
└── XPathInjection.java # XPath injection
```

### Key Packages

- **controller**: 45+ vulnerability demonstration endpoints organized by category
- **config**: Spring configuration classes (Swagger2.java)
- **entity**: JPA/entity classes for database models
- **mapper**: MyBatis mapper interfaces and XML files in `src/main/resources/mapper/`
- **util**: Security utilities (JwtUtils, Security, HttpClientUtils, CookieUtils, RegexUtils)
- **test**: Test classes (only HelloApplicationTests exists)

### Database Layer

- **MyBatis ORM** for data access with mapper XML files
- Database initialization script at `src/main/resources/db.sql`
- MySQL 8.3.0 as the database server

### Configuration Files

- `src/main/resources/application.properties`: Main configuration with Actuator exposure
- `src/main/resources/application-dev.properties`: Development profile (port 8888)
- `src/main/resources/application-docker.properties`: Docker profile
- `src/main/resources/db.sql`: MySQL initialization script
- `src/main/resources/ESAPI.properties`: OWASP ESAPI security library configuration

### Key Dependencies

- **Spring Boot 2.4.1** with web, JDBC, test, actuator starters
- **MyBatis 2.2.2** for ORM
- **MySQL Connector 8.0.28** for database connectivity
- **Fastjson 1.2.41** (vulnerable version for RCE demonstration)
- **XStream 1.4.10** (vulnerable version for XML deserialization)
- **Jackson 2.11.0** for JSON processing
- **Swagger2 2.9.2** for API documentation
- **Log4j 2.8.2** (for Log4Shell vulnerability demonstration)
- **Groovy 2.5.6** for command execution demonstrations
- **Thymeleaf & Freemarker** for template rendering

### Template and Static Resources

Templates are in `src/main/resources/templates/` with subdirectories organized by vulnerability type. Static resources (JS, CSS) are also organized within these template subdirectories. Each vulnerability category has its own HTML template.

### Exposed Endpoints

- **Actuator**: All management endpoints exposed (`management.endpoints.web.exposure.include=*`)
- **Swagger UI**: Available at `/swagger-ui.html` for API exploration
- **API Docs**: `/v2/api-docs` for Swagger documentation

### Application Profiles

- **dev**: Default profile for local development (port 8888)
- **docker**: Profile for Docker container deployment

## Vulnerability Categories Implemented

Each controller typically demonstrates BOTH vulnerable and secure coding patterns:

1. **SQL Injection**: JDBC, Hibernate, MyBatis with parameterized query safeguards
2. **XSS**: Reflected, Stored, DOM-based with various output encoding strategies
3. **RCE**: Command execution, Expression evaluation vulnerabilities
4. **Deserialization**: Java deserialization, XMLDecoder, SnakeYAML exploits
5. **SSTI**: Template injection vulnerabilities in Thymeleaf/Freemarker
6. **SpEL**: Spring Expression Language injection attacks
7. **SSRF**: Server-Side Request Forgery examples
8. **IDOR**: Insecure Direct Object Reference vulnerabilities
9. **Directory Traversal**: Path traversal attack vectors
10. **Open Redirect**: Unvalidated redirect vulnerabilities
11. **CSRF**: Cross-Site Request Forgery protections and bypasses
12. **File Upload**: Unrestricted file upload vulnerabilities
13. **XXE**: XML External Entity attack vectors
14. **Actuator**: Exposed management endpoint risks
15. **Fastjson**: Deserialization RCE vulnerability
16. **XStream**: XML deserialization RCE exploit
17. **Log4Shell**: Log4j JNDI lookup vulnerability (CVE-2021-44228)
18. **JNDI**: JNDI injection attack patterns
19. **DoS**: Denial of Service attack examples
20. **XPath**: XPath injection vulnerabilities
21. **IP Forgery**: HTTP header manipulation attacks
22. **JWT**: JWT token vulnerabilities and attacks
23. **Password Reset**: Business logic flaws in password reset flow

## Security Notes

- This is intentionally VULNERABLE code for educational and training purposes
- **DO NOT deploy in production environments**
- All dependencies with known CVEs are included intentionally to demonstrate vulnerabilities
- **DO NOT add security patches or fixes** unless specifically requested
- Focus on understanding vulnerability mechanics, exploitation, and secure coding patterns
- Code comments typically highlight both the vulnerability and potential remediation approaches

## Development Notes

- Uses ESAPI security library with configuration in `ESAPI.properties`
- Includes OWASP Java Encoder for output encoding demonstrations
- Each vulnerability category shows contrast between vulnerable and secure implementations
- Demonstrates real-world vulnerability patterns found in enterprise applications
- Most security vulnerabilities are paired with their secure alternatives in the same controller
- Frontend uses Bootstrap 4.6.0 and Codemirror 5.62.0 for interactive demos