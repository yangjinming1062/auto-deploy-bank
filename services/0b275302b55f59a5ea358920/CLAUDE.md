# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **Event-Sourcing + CQRS money transfer example application** demonstrating microservices architecture with polyglot persistence. The application provides a REST API for creating customers, bank accounts, and transferring money between accounts. It implements **event sourcing** and **Command Query Responsibility Segregation (CQRS)** patterns using the [Eventuate platform](http://eventuate.io/).

## Architecture

The application consists of **5 microservices** that communicate via events:

1. **Customers Service** (Port 8083) - Command-side service for creating customers
2. **Accounts Service** (Port 8080) - Command-side service for creating accounts
3. **Transactions Service** (Port 8082) - Command-side service for money transfers
4. **Customers View Service** (Port 8084) - Query-side service with MongoDB view for customers
5. **Accounts View Service** (Port 8081) - Query-side service with MongoDB view for accounts
6. **API Gateway Service** (Port 8080) - Facade in front of all services

**Key Architectural Patterns:**
- **Event Sourcing**: All state changes are stored as events in an Eventuate event store
- **CQRS**: Command-side services handle updates; query-side services handle reads with denormalized views
- **Event-driven**: Services communicate asynchronously through events
- **Deployment flexibility**: Can be deployed as microservices or as a monolith (see `scala-spring/monolithic-service/`)

## Directory Structure

```
/
├── java-spring/              # Main Java Spring Boot implementation (active)
│   ├── accounts-service/         # Account command-side service
│   ├── accounts-view-service/    # Account query-side service
│   ├── transactions-service/     # Transfer command-side service
│   ├── customers-service/        # Customer command-side service
│   ├── customers-view-service/   # Customer query-side service
│   ├── api-gateway-service/      # API Gateway facade
│   ├── common-backend/           # Shared backend utilities
│   ├── common-auth/              # Authentication utilities
│   ├── common-swagger/           # Swagger/OpenAPI configuration
│   ├── testutil/                 # Test utilities
│   ├── backend-integration-tests/# Service integration tests
│   ├── rest-api-integration-tests/# REST API tests
│   └── e2e-test/                 # End-to-end tests
│
├── scala-spring/             # Scala Spring Boot version (outdated, lags behind Java)
│   ├── accounts-command-side-service/
│   ├── transactions-command-side-service/
│   └── monolithic-service/       # Monolithic version of the app
│
├── js-frontend/              # React + Redux frontend (Port 3000 in dev)
│   ├── src/
│   │   ├── actions/
│   │   ├── components/
│   │   ├── reducers/
│   │   ├── views/
│   │   └── utils/
│   └── webpack.config.js
│
├── prebuilt-web-client/      # Prebuilt frontend assets
└── _build-and-test-all.sh    # Build and test all services
```

Each service follows Spring Boot conventions:
```
service-name/
├── src/
│   ├── main/
│   │   ├── java/net/chrisrichardson/eventstore/javaexamples/banking/[service]/
│   │   │   ├── backend/           # Domain models, commands, events
│   │   │   ├── web/               # REST controllers
│   │   │   └── [Service]Main.java # Application entry point
│   │   └── resources/
│   │       └── application.properties
│   └── test/
│       └── java/                  # Unit and integration tests
├── build.gradle
└── Dockerfile
```

## Common Development Commands

### Building and Running (Eventuate SaaS)

```bash
# Build all Java services
cd java-spring
./gradlew assemble

# Start services with Docker Compose
docker-compose up -d

# Access application at http://$DOCKER_HOST_IP:8080
```

### Building and Running (Eventuate Local)

```bash
# Build with local event store
cd java-spring
./gradlew assemble -P eventuateDriver=local

# Start with local infrastructure
export DOCKER_HOST_IP=<your-ip>
docker-compose -f docker-compose-eventuate-local.yml up -d

# Access at http://$DOCKER_HOST_IP:8080
```

**Note:** `DOCKER_HOST_IP` must be an IP address or resolvable hostname, not `localhost`.

### Testing

```bash
# Run all tests
cd java-spring
./gradlew test

# Run end-to-end tests (requires running services)
./gradlew :e2e-test:test

# Build, start services, run all tests, then clean up
./_build-and-test-all.sh

# Build and test with Java opts
cd java-spring
./build-and-test-all.sh

# Test single module
./gradlew :accounts-service:test
./gradlew :transactions-service:test
./gradlew :customers-service:test
```

### Frontend Development

```bash
cd js-frontend

# Install dependencies
npm install

# Build for production
npm run build

# Run in development mode (Port 3000)
npm run start-dev

# Watch mode (rebuilds on changes)
npm run watch

# Run E2E tests
npm run e2e-setup    # First time only
npm run test-e2e
```

### Service Management

```bash
# Set environment variables
cd java-spring
source set-env.sh

# Show service URLs
./show-urls.sh

# Wait for services to be ready
./wait-for-services.sh <host> <ports...>

# Access MongoDB CLI
./mongodb-cli.sh

# Test API with curl examples
./handy-curl-commands.sh
```

### Docker Operations

```bash
# Stop and remove all containers
docker-compose down

# Rebuild and restart
docker-compose build
docker-compose up -d

# View logs
docker-compose logs -f [service-name]

# Set Eventuate credentials
export EVENTUATE_API_KEY_ID=your-id
export EVENTUATE_API_KEY_SECRET=your-secret
```

## Service Dependencies

All services require:
- **Eventuate credentials**: `EVENTUATE_API_KEY_ID` and `EVENTUATE_API_KEY_SECRET` (for SaaS)
- **MongoDB**: Required by view services for denormalized read models

View services depend on MongoDB:
- Accounts View Service
- Customers View Service

API Gateway depends on all other services and MongoDB.

## Key Configuration

- `java-spring/gradle.properties` - Gradle configuration
- `java-spring/docker-compose.yml` - Docker Compose for SaaS
- `java-spring/docker-compose-eventuate-local.yml` - Docker Compose for local development
- `js-frontend/package.json` - Frontend dependencies and scripts
- `js-frontend/webpack.config.js` - Webpack bundler configuration

## API Endpoints

Access through API Gateway (Port 8080):

- `POST /customers` - Create customer
- `GET /customers` - Get all customers
- `GET /customers/{id}` - Get customer by ID
- `POST /accounts` - Create account
- `GET /accounts/{id}` - Get account by ID
- `POST /transfers` - Transfer money
- `GET /transfers/{id}` - Get transfer by ID

Direct service access (for testing):
- Customers Service: 8083
- Accounts Command Service: 8080
- Accounts View Service: 8081
- Transactions Service: 8082
- Customers View Service: 8084

See `java-spring/handy-curl-commands.sh` for usage examples.

## Development Tips

1. **Services are independently deployable** - Each service has its own `build.gradle`, `Dockerfile`, and can be built/tested separately.

2. **Event-driven communication** - Services communicate via events published to Eventuate. Do not make synchronous calls between services.

3. **CQRS pattern** - Command-side services (create/modify) are separate from query-side services (read). View services subscribe to events and update MongoDB.

4. **Gradle wrapper** - Use `./gradlew` instead of `gradle` to ensure consistent versions.

5. **Test organization**:
   - `src/test/java` - Unit tests
   - `backend-integration-tests/` - Service integration tests
   - `rest-api-integration-tests/` - REST API tests
   - `e2e-test/` - End-to-end tests with Docker

6. **Frontend build** - Frontend uses Webpack 1.x and requires `npm run build` before Docker builds (see `js-frontend/webpack.config.js:88`).

## Testing Strategy

- **Unit tests**: Run with `./gradlew test`
- **Integration tests**: Run with `./gradlew :backend-integration-tests:test`
- **E2E tests**: Use `_build-and-test-all.sh` or `./build-and-test-all.sh` which handles Docker orchestration, waits for services, runs tests, and cleans up.

For a single test:
```bash
./gradlew :customers-service:test --tests "*CustomerTest"
```