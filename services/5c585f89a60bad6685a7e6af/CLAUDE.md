# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VProfile v2 is a Java Spring MVC web application that provides user account management with the following features:
- User registration and login with Spring Security
- Profile management with comprehensive user details
- Caching via Memcached
- Message queuing via RabbitMQ
- Search functionality via ElasticSearch
- MySQL database persistence

## Technology Stack

- **Framework**: Spring MVC 4.2.0
- **Security**: Spring Security 4.0.2 with BCrypt password encoding
- **Data Access**: Spring Data JPA 1.8.2 with Hibernate 4.3.11
- **Database**: MySQL 8
- **View Layer**: JSP with JSTL
- **Build Tool**: Maven 3
- **Servlet Container**: Tomcat 8 (configured) or Jetty (for development)
- **Caching**: Memcached (spymemcached client)
- **Messaging**: RabbitMQ 1.7.1
- **Search**: ElasticSearch 5.6.4
- **Testing**: JUnit 4.10, Mockito, Spring Test
- **Code Coverage**: JaCoCo 0.8.4

## Architecture

The application follows standard Spring MVC layered architecture:

- **Controller Layer** (`src/main/java/com/visualpathit/account/controller/`):
  - `UserController.java` - Handles user registration, login, profile CRUD, and integrations with Memcached/RabbitMQ
  - `FileUploadController.java` - Handles file uploads
  - `ElasticSearchController.java` - Provides search functionality

- **Service Layer** (`src/main/java/com/visualpathit/account/service/`):
  - `UserService` interface with `UserServiceImpl` implementation
  - `SecurityService` and `SecurityServiceImpl` for authentication
  - `ProducerService`/`ConsumerService` for RabbitMQ messaging
  - `UserDetailsServiceImpl` for Spring Security user details

- **Repository Layer** (`src/main/java/com/visualpathit/account/repository/`):
  - Spring Data JPA repositories for data access

- **Model Layer** (`src/main/java/com/visualpathit/account/model/`):
  - `User.java` - JPA entity with extensive profile fields
  - `Role.java` - Security role entity

- **Utils** (`src/main/java/com/visualpathit/account/utils/`):
  - `MemcachedUtils.java` - Caching utilities
  - `RabbitMqUtil.java` - Message queue utilities
  - `ElasticsearchUtil.java` - Search utilities

- **Validator** (`src/main/java/com/visualpathit/account/validator/`):
  - `UserValidator.java` - Form validation for user registration

## Key Configuration Files

### Spring Configuration (XML-based)
- `src/main/webapp/WEB-INF/web.xml` - Main web application configuration
- `src/main/webapp/WEB-INF/appconfig-root.xml` - Root application context
- `src/main/webapp/WEB-INF/appconfig-mvc.xml` - MVC configuration
- `src/main/webapp/WEB-INF/appconfig-security.xml` - Spring Security configuration
- `src/main/webapp/WEB-INF/appconfig-data.xml` - Data access configuration
- `src/main/webapp/WEB-INF/appconfig-rabbitmq.xml` - RabbitMQ configuration

### Application Properties
- `src/main/resources/application.properties` - Database and service endpoints configuration
- `src/main/resources/logback.xml` - Logging configuration
- `src/main/resources/validation.properties` - Validation messages

### Build Configuration
- `pom.xml` - Maven build configuration with dependencies and plugins
- `Jenkinsfile` - CI/CD pipeline configuration

## Common Development Commands

### Build the Project
```bash
mvn clean install -DskipTests
```

### Run Unit Tests
```bash
mvn test
```

### Run Integration Tests
```bash
mvn verify -DskipUnitTests
```

### Run Both Unit and Integration Tests
```bash
mvn verify
```

### Run Checkstyle Analysis
```bash
mvn checkstyle:checkstyle
```

### Generate Code Coverage Report
```bash
mvn clean install
# Reports generated in target/site/jacoco/
```

### Run Development Server (Jetty)
```bash
mvn jetty:run
```
Then access the application at `http://localhost:8080/`

### Build WAR File Only
```bash
mvn clean package
# WAR file will be in target/vprofile-v2.war
```

### Run a Single Test Class
```bash
mvn test -Dtest=UserControllerTest
```

### Skip Tests During Build
```bash
mvn clean install -DskipTests
```

## Database Setup

1. Import the database schema and initial data:
   ```bash
   mysql -u <username> -p accounts < src/main/resources/db_backup.sql
   ```

2. The database includes:
   - `user` table - stores user account and profile information
   - `role` table - stores security roles
   - `user_role` table - many-to-many join table

3. Update `application.properties` if database connection details change

## External Service Dependencies

The application requires several external services (configured in `application.properties`):
- **MySQL**: `db01:3306/accounts`
- **Memcached**: Active at `mc01:11211`, Standby at `127.0.0.1:11211`
- **RabbitMQ**: `rmq01:5672` (username: test, password: test)
- **ElasticSearch**: `192.168.1.85:9300` (cluster: vprofile, node: vprofilenode)

## Deployment Infrastructure

### Ansible
- `ansible/vpro-app-setup.yml` - Automates Tomcat8 installation and WAR deployment
- Downloads artifacts from Nexus repository
- Includes backup and rollback functionality
- Deploys to `/usr/local/tomcat8/webapps/ROOT.war`

### Vagrant
Multiple provisioning configurations for different environments:
- `vagrant/Automated_provisioning_WinMacIntel/`
- `vagrant/Automated_provisioning_MacOSM1/`
- `vagrant/Manual_provisioning_WinMacIntel/`
- `vagrant/Manual_provisioning_MacOSM1/`

## CI/CD Pipeline

The Jenkins pipeline (`Jenkinsfile`) includes:
1. **BUILD** - Compiles and packages the application
2. **UNIT TEST** - Runs unit tests
3. **INTEGRATION TEST** - Runs integration tests
4. **CODE ANALYSIS WITH CHECKSTYLE** - Code quality checks
5. **CODE ANALYSIS with SONARQUBE** - Static code analysis
6. **Publish to Nexus Repository Manager** - Deploys to Nexus

Pipeline uses:
- JDK 17
- Maven 3.9
- SonarQube for code quality
- Nexus 3 for artifact repository

## Important Notes

- Spring Security uses BCrypt password encoding with strength 11
- CSRF protection is disabled in security config (`appconfig-security.xml:15`)
- Application uses JSP views located in `src/main/webapp/WEB-INF/views/`
- File uploads are limited to 100KB (`appconfig-mvc.xml:29`)
- The application uses JPA/Hibernate with MySQL connector version 8.0.32
- Java 8 is configured as both source and target compatibility
- Database backup is located at `src/main/resources/db_backup.sql`