# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

metasfresh is a responsive, Free and Open Source ERP System with a 3-tier architecture (backend API, web frontend, database). It's a monorepo containing:

- **Backend**: Java/Spring Boot microservices using Maven
- **Frontend**: React/Redux web application (HTML5/ReactJS/Redux)
- **E2E Tests**: Cypress tests for end-to-end testing
- **Database**: PostgreSQL with database migrations
- **Infrastructure**: Docker-based deployment with multiple services (RabbitMQ, Elasticsearch)

## Development Commands

### Building the Project (Windows)

```cmd
build.cmd
```
Builds all Docker images locally with the "local" qualifier. Requires GitHub PAT credentials in `docker-builds/mvn/local-settings.xml` for Maven dependencies.

**Note**: This is a Windows batch script for building the entire metasfresh stack.

### Running the Application Locally

```cmd
run.cmd
```
Starts the complete metasfresh stack using Docker Compose:
- Frontend: http://localhost (user: metasfresh, password: metasfresh)
- Mobile UI: http://localhost:8880/mobile (user: cynthia, password: metasfresh)

Stop with:
```cmd
docker-compose -f docker-builds/compose/compose.yml down
```

### Backend Development (Java/Spring Boot)

The backend uses Maven and is split into multiple modules under `backend/`. Key modules include:
- `de.metas.adempiere.adempiere` - Core ADempiere framework
- `de.metas.business` - Business logic
- `metasfresh-webui-api` - REST API service (runs on port 8080)

**Run backend API from Eclipse:**
- Main method: `/metasfresh-webui-api/src/main/java/de/metas/ui/web/WebRestApiApplication.java`
- First run: Add `-Dwebui-api-run-headless=false` to display DB connection dialog
- Optional: `-Dspring.boot.admin.url=http://localhost:9090 -Dmanagement.security.enabled=false`
- Disable Elasticsearch: `-Delastic_enable=false`
- Swagger UI: http://localhost:8080/swagger-ui/index.html

**Maven Commands:**
```bash
# Build specific module
mvn clean install -pl de.metas.business -am

# Run tests
mvn test

# Run single test
mvn test -Dtest=ClassName#methodName
```

### Frontend Development (React/Redux)

**Navigate to:** `frontend/`

**Commands:**
```bash
# Install dependencies
npm install

# Development server
npm start

# Build production
npm run build-prod

# Run tests
npm test
npm run test:watch  # watch mode

# Lint code
npm run lint
npm run lintfix  # auto-fix

# Style lint
npm run stylelint

# Storybook (component documentation)
npm run storybook
```

### Testing

#### JUnit Tests
```cmd
docker run --rm -v "$(pwd)/docker-builds/junit:/reports" metasfresh/metas-junit:local
```
Reports saved to `docker-builds/junit/`

#### Cucumber Tests
```cmd
cd docker-builds/cucumber
run.cmd
```
Takes 60-120 minutes. Results in `docker-builds/cucumber/cucumber_`

Post-test database image: `metasfresh/metas-db:local-postcucumber`
Run it: `docker run -it --rm -p 15432:5432 metasfresh/metas-db:local-postcucumber`

#### Cypress E2E Tests
```cmd
cd docker-builds/e2e
run.cmd
```
Takes ~120 minutes. Run Cypress UI:
```bash
cd e2e
npm run cypress:open
```

## Code Architecture

### Backend Structure (Java)

The backend follows a modular architecture with these major components:

**Core Modules:**
- `de.metas.adempiere.adempiere` - Base ADempiere framework (base, client, serverRoot)
- `de.metas.business` - Business logic (sales, purchasing, invoices, etc.)
- `de.metas.ui.web` - Web UI layer and REST APIs
- `metasfresh-webui-api` - Main REST API service
- `de.metas.migration` - Database migration tools

**Service Modules:**
- `de.metas.async` - Asynchronous processing
- `de.metas.report` - Report generation (JasperReports)
- `de.metas.edi` - Electronic Data Interchange
- `de.metas.manufacturing` - Manufacturing functionality
- `de.metas.handlingunits` - Warehouse and HU management

**Integration Modules:**
- `de.metas.externalsystem` - External system integrations
- `de.metas.banking` - Banking and payment integrations
- `de.metas.payment.*` - Payment processing (ESR, SEPA)

**Vertical Modules:**
- `de.metas.vertical.pharma.*` - Pharma-specific functionality
- `vertical-healthcare_ch` - Swiss healthcare integration

### Frontend Structure (React/Redux)

**Source Layout:**
```
frontend/src/
├── actions/          # Redux actions
├── api/             # API client functions
├── components/      # React components
├── constants/       # Application constants
├── containers/      # Redux-connected components
├── pages/           # Page components
├── reducers/        # Redux reducers
├── routes/          # React Router configuration
├── services/        # Business logic services
├── store/           # Redux store configuration
└── __tests__/       # Frontend tests
```

Key Technologies:
- React 16.14
- Redux + Redux-Thunk
- React Router v5
- Bootstrap 4.3
- Webpack 5
- Jest + React Testing Library

### Microservices Architecture

**Docker Compose Services (from `docker-builds/compose/compose.yml`):**

1. **db** (PostgreSQL) - Port 15432
2. **rabbitmq** - Message broker (ports 5672, 15672)
3. **search** (Elasticsearch 7.17.8) - Full-text search (ports 9200, 9300)
4. **webapi** - REST API service (port 8080, debug 8789)
5. **app** - Application service (port 8282, debug 8788)
6. **frontend** - React web UI (port 80/443)

**Additional Services:**
- `metas-api` - API build artifact
- `metas-app` - Application build artifact
- `metas-edi` - EDI processing
- `metas-externalsystems` - External integrations
- `metas-mobile` - Mobile web UI

### Database Architecture

- **PostgreSQL** as primary database
- Database migrations via `de.metas.migration` module
- Versioned database state stored in Docker images
- Post-cucumber test database snapshots available for debugging

### Build and CI/CD

**CI/CD Pipeline:**
- GitHub Actions (`.github/workflows/cicd.yaml`)
- Test results: https://metasfresh.testspace.com/
- Docker images pushed with tags: `<mfversion>-<branch>.<buildnr>`

**Version Format:**
- CI builds: `<mfversion>.3-<qualifier>.<buildnr>`
- Local builds: `<mfversion>.3-local.<buildnr>`

### Key Configuration Files

- `backend/pom.xml` - Maven parent POM with all modules
- `docker-builds/compose/compose.yml` - Docker Compose configuration
- `docker-builds/compose/.env` - Environment variables for compose
- `docker-builds/version.info` - Version information
- `frontend/package.json` - Frontend dependencies and scripts

### Common Development Patterns

**Backend:**
- Spring Boot applications with `@RestController` for APIs
- Database entities following ADempiere patterns
- Message-driven processing via RabbitMQ
- Async processing with `@Async` and `@EventListener`

**Frontend:**
- Redux for state management
- Connected components in `containers/`
- Pure components in `components/`
- API calls through `services/` layer
- React Router for navigation

### Testing Patterns

- **Unit Tests**: JUnit 5 with Spring Boot Test
- **Integration Tests**: Spring Test with test containers
- **Cucumber**: BDD tests in `backend/de.metas.cucumber/src/test/resources/`
- **Cypress**: E2E tests in `e2e/` directory
- **Jest**: Frontend unit tests with React Testing Library

## Development Guidelines

**Git:**
- Use sparse checkout for large repository: `git sparse-checkout init --clone`
- Pull specific directories: `git sparse-checkout set frontend`
- Fork from `master` branch
- Contribute via pull requests

**Code Quality:**
- PMD rules configured in `.pmd` files
- ESLint for frontend code
- Stylelint for CSS
- Java code follows Adempiere patterns

**Documentation:**
- Developer docs: https://docs.metasfresh.org/index.html
- User docs: https://docs.metasfresh.org/pages/webui/index_en
- Forum: https://forum.metasfresh.org/

## Troubleshooting

**Build fails with 401 Unauthorized:**
- Add GitHub PAT to `docker-builds/mvn/local-settings.xml`
- PAT needs only "packages read" scope

**Elasticsearch errors in dev:**
- Add `-Delastic_enable=false` to API startup

**Frontend build issues:**
- Clear node_modules: `rm -rf frontend/node_modules`
- Reinstall: `cd frontend && npm install`

**Database connection issues:**
- Check Docker Compose services are running: `docker ps`
- Verify db service health: `docker-compose -f docker-builds/compose/compose.yml ps db`