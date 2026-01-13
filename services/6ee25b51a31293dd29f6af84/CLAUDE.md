# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About

Lavagna is a small, easy-to-use issue/project tracking software built with Java 8+, Spring Framework, and AngularJS. It supports MySQL, MariaDB, PostgreSQL, and HSQLDB databases. The application is packaged as a WAR file for deployment in servlet containers or as a self-contained executable WAR with embedded Jetty.

## Quick Start

Install dependencies:
```bash
npm install
mvn clean install
```

Launch the development server with HSQLDB (default):
```bash
mvn jetty:run
```

Then visit http://localhost:8080. If you get a 403 error, go to http://localhost:8080/setup and configure the application with demo data. Login with username: `user`, password: `user`.

## Common Commands

### Building and Running
```bash
# Development server (HSQLDB)
mvn jetty:run

# With HSQLDB and DB manager
mvn jetty:run -DstartDBManager

# Development server with MySQL profile
mvn jetty:run -Pdev-mysql

# Development server with PostgreSQL profile
mvn jetty:run -Pdev-pgsql

# Build for production
mvn clean package

# Run executable WAR with custom settings
mvn clean install
java -Ddatasource.dialect=HSQLDB -Ddatasource.url=jdbc:hsqldb:mem:lavagna -Ddatasource.username=sa -Ddatasource.password= -Dspring.profiles.active=dev -jar target/dependency/jetty-runner.jar --port 8080 target/*.war

# Debug mode
mvnDebug jetty:run
```

### Testing
```bash
# Run all tests (HSQLDB)
mvn test

# Run tests with MySQL
mvn test -Ddatasource.dialect=MYSQL

# Run tests with PostgreSQL
mvn test -Ddatasource.dialect=PGSQL

# Generate code coverage report
mvn clean test jacoco:report
# Open target/site/jacoco/index.html to view
```

### Linting and Code Quality
```bash
# Lint frontend code
npm run-script lint

# Fix linting issues
npm run-script lint-fix

# Check license headers and add them to new files
mvn com.mycila:license-maven-plugin:format
```

### Database Testing with Vagrant
```bash
# Initialize Vagrant (requires submodules)
git submodule update --init

# Boot Vagrant VMs (or specific one: pgsql / mysql)
vagrant up

# Run tests with Vagrant databases
mvn test -Ddatasource.dialect=PGSQL
mvn test -Ddatasource.dialect=MYSQL
```

### Documentation
```bash
# Build documentation
mvn clean stampo:build
# Output: target/generated-docs

# Serve documentation locally
mvn stampo:serve
# Visit: http://localhost:45001/
```

### Dependency Updates
```bash
# Check for dependency updates
mvn versions:display-dependency-updates
mvn versions:display-plugin-updates
```

### Maven Profiles
- `dev` (default): HSQLDB, port 8080
- `dev-mysql`: MySQL database
- `dev-pgsql`: PostgreSQL database
- `prod`: Production mode with HSQLDB

## Architecture

### Backend Structure

The application follows a layered architecture:

- **Configuration** (`io.lavagna.config`): Spring configuration classes including datasource, security, and web setup
  - `PersistenceAndServiceConfig.java`: Database and service configuration
  - `WebSecurityConfig.java`: Security configuration
  - `DataSourceConfig.java`: Database connection settings

- **Models** (`io.lavagna.model`): Data models, primarily written in Kotlin
  - `Board.kt`, `Card.kt`, `User.kt`, etc.: Core domain entities
  - `io.lavagna.model.apihook`: API hook models
  - `io.lavagna.model.util`: Utility model classes

- **Data Access** (`io.lavagna.query`): Query objects using NPJT (Named Parameter JDBC Template)
  - `BoardQuery.java`, `CardQuery.java`, `UserQuery.java`: Repository-style query interfaces
  - Direct SQL queries with parameter binding

- **Services** (`io.lavagna.service`): Business logic layer
  - `BoardRepository.java`, `CardRepository.java`: Data repository layer
  - `CardService.java`, `BoardService.java`: Core business logic
  - `io.lavagna.service.importexport`: Import/export functionality
  - `io.lavagna.service.mailreceiver`: Email integration
  - `io.lavagna.service.calendarutils`: Calendar-related utilities

- **Web/API** (`io.lavagna.web`): REST API and web layer
  - `io.lavagna.web.api`: REST endpoints
    - `BoardController.java`, `CardController.java`, `UserController.java`
    - `SearchController.java`, `CalendarController.java`
    - `SetupController.java`
  - `io.lavagna.web.security`: Authentication and authorization
    - `io.lavagna.web.security.login.oauth`: OAuth providers (Google, GitHub, etc.)
  - `io.lavagna.web.support`: Web support utilities

### Database Layer

- Uses **NPJT** (Named Parameter JDBC Template) for type-safe SQL queries
- Database migrations via **Flyway**
- Connection pooling with **HikariCP**
- Supports multiple dialects: HSQLDB, MySQL, PostgreSQL

### Frontend Structure

The frontend is built with **AngularJS** (not modern Angular):

- `src/main/webapp/app/`: Main application
  - `components/`: UI components (board, card, dashboard, charts, etc.)
  - `services/`: AngularJS services for API communication
  - `directives/`: Custom directives (drag-and-drop, permissions, etc.)
  - `filters/`: Data filters
  - `ui/`: UI utilities and components
- `src/main/webapp/app-login/`: Login application
- `src/main/webapp/setup/`: Setup/configuration UI
- Linting configured via `.eslintrc` with Angular-specific plugins

### Key Technologies

- **Backend**: Java 8, Kotlin, Spring Framework 5.3.x
- **Build**: Maven, Jetty Maven Plugin, Spring Boot (for repackaging)
- **Database**: HSQLDB (dev), MySQL 8.0+, PostgreSQL 9.1+
- **Frontend**: AngularJS, JavaScript, HTML, CSS
- **Real-time**: WebSocket support via Spring
- **Testing**: JUnit 4, Mockito, JaCoCo for coverage
- **Static Analysis**: Error Prone compiler plugin, PMD, FindBugs
- **Documentation**: Stampo (static site generator)
- **Logging**: Log4j 2.x
- **Security**: Spring Security, OAuth (Google, GitHub, etc.)

### IDE Configuration

- Use **UTF-8 encoding** and **120 characters line width**
- Requires Java **and Kotlin** aware IDE (IntelliJ or Eclipse)
- For Eclipse: Install Kotlin plugin and add "Kotlin nature" to project

## Development Notes

### Code Standards
- Frontend code must pass ESLint checks (`npm run-script lint`)
- New Java/Kotlin files must have GPL-3 license header (use `mvn com.mycila:license-maven-plugin:format`)
- Java 8 compatibility required
- Error Prone compiler enabled for additional static analysis

### Database Configuration
- Default development uses HSQLDB (in-memory)
- For production, configure MySQL with UTF-8 collation: `CREATE DATABASE lavagna CHARACTER SET utf8 COLLATE utf8_bin;`
- Database migrations can be disabled with: `datasource.disable.migration=true`

### Testing Approach
- Unit tests in `src/test/java`
- Integration tests using Spring Test framework
- Mock services with Mockito
- Test coverage via JaCoCo (see `target/site/jacoco/index.html`)

### Performance Monitoring
- Angular performance stats: https://github.com/kentcdodds/ng-stats
- JavaScript stats: https://github.com/mrdoob/stats.js/

## Build Profiles

Maven profiles in `pom.xml`:

1. **dev** (active by default)
   - HSQLDB, port 8080, dev mode

2. **dev-mysql**
   - MySQL connection (root/empty password by default)

3. **dev-pgsql**
   - PostgreSQL connection (postgres/password)

4. **prod**
   - Production mode with HSQLDB

5. **sign-artifacts**
   - GPG signing for releases (activated with `-Dsign=true`)