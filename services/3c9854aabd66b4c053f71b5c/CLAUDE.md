# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Kestra is an open-source, event-driven orchestration platform built with Java (Micronaut) and Vue.js. It allows users to define workflows in YAML and execute both scheduled and event-driven tasks.

## Repository Structure

The codebase is organized into multiple Gradle modules:

- **`core/`**: Core framework containing task definitions, flow models, execution engine, triggers, and validations
- **`cli/`**: Command-line interface and server entry point (`io.kestra.cli.App`)
- **`webserver/`**: REST API server implementation with Swagger documentation
- **`ui/`**: Vue.js 3 frontend application with TypeScript and Vite
- **`worker/`**: Task execution workers
- **`executor/`**: Task execution engine
- **`scheduler/`**: Workflow scheduling
- **`processor/`**: Task processing engine
- **`script/`**: Script execution engine for multiple languages
- **`model/`**: Data models and DTOs
- **`jdbc-*`**: Database connectors (H2, MySQL, PostgreSQL)
- **`storage-local/`**: Local file storage implementation
- **`repository-memory/`**: In-memory repository for development
- **`runner-memory/`**: In-memory execution runner for development
- **`platform/`**: Platform-specific implementations and BOM
- **`tests/`**: Integration test framework
- **`e2e-tests/`**: End-to-end test suite
- **`jmh-benchmarks/`**: Performance benchmarks

## Development Environment

### Prerequisites
- Java 21+
- Node.js 22+ and npm
- Python 3, pip, and python venv
- Docker & Docker Compose
- Gradle (wrapper included)

### Configuration

**Backend Configuration** (`cli/src/main/resources/application-override.yml`):

Local mode (H2 database):
```yaml
micronaut:
  server:
    cors:
      enabled: true
      configurations:
        all:
          allowedOrigins:
            - http://localhost:5173
```

Standalone mode (PostgreSQL):
```yaml
kestra:
  repository:
    type: postgres
  storage:
    type: local
    local:
      base-path: "/app/storage"
  queue:
    type: postgres

datasources:
  postgres:
    url: jdbc:postgresql://host.docker.internal:5432/kestra
    driverClassName: org.postgresql.Driver
    username: kestra
    password: k3str4

flyway:
  datasources:
    postgres:
      enabled: true
      locations:
        - classpath:migrations/postgres
```

**Frontend Configuration** (`ui/.env.development.local`):
```bash
VITE_API_URL=http://localhost:8080
```

## Common Development Commands

### Backend (Root directory)
```bash
# Build the entire project
./gradlew build

# Clean and rebuild
./gradlew clean build

# Build without running tests
./gradlew build -x test -x integrationTest -x testCodeCoverageReport --refresh-dependencies

# Run all tests
./gradlew test

# Run tests for a specific module
./gradlew :core:test
./gradlew :cli:test
./gradlew :webserver:test

# Run in local mode (H2 database)
./gradlew runLocal

# Run in standalone mode (PostgreSQL)
./gradlew runStandalone

# Run local development server
./gradlew :cli:bootRun

# Execute single test class
./gradlew :core:test --tests "*FlowServiceTest"

# Execute single test method
./gradlew :core:test --tests "*FlowServiceTest.testGetFlow"

# Check code formatting
./gradlew spotlessCheck

# Apply code formatting
./gradlew spotlessApply

# Run OWASP dependency check
./gradlew dependencyCheckAnalyze
```

### Frontend (`ui/` directory)
```bash
cd ui

# Install dependencies
npm install

# Run development server (port 5173)
npm run dev

# Run tests
npm run test

# Run tests with coverage
npm run test:coverage

# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Build for production
npm run build

# Build and preview
npm run build && npm run preview
```

### Using Makefile (Development convenience)
```bash
# Install Kestra locally to ~/.kestra/current
make install

# Install plugins from Kestra API
make install-plugins

# Start with PostgreSQL backend
make start-standalone-postgres

# Start with local (in-memory) backend
make start-standalone-local

# Build executable
make build-exec

# Run all tests
make test

# Build Docker image
make build-docker
```

### End-to-End Tests
```bash
# Build and start E2E tests
./build-and-start-e2e-tests.sh
```

## Architecture Overview

### Backend Architecture
- Built on **Micronaut** framework (Java 21)
- **Modular design**: Each module has a specific responsibility (execution, scheduling, storage, etc.)
- **Plugin system**: Extensible via plugins loaded from `KESTRA_PLUGINS_PATH`
- **Repository pattern**: Pluggable storage backends (H2, PostgreSQL, MySQL)
- **Queue system**: Pluggable message queues for task distribution
- **Storage abstraction**: Local and cloud storage implementations

### Key Backend Concepts
- **Flows**: Declarative YAML workflow definitions
- **Tasks**: Individual units of work within flows
- **Triggers**: Schedule or event-based flow initiation
- **Inputs & Variables**: Dynamic data handling
- **Executions**: Runtime instances of flows
- **Workers**: Execute tasks (can be distributed)

### Frontend Architecture
- **Vue.js 3** with Composition API
- **TypeScript** for type safety
- **Vite** for build tooling
- **Pinia** for state management
- **Vue Router** for navigation
- Component-based architecture in `src/components/`

### UI Key Features
- **Topology Editor**: Visual DAG editor for flows
- **Code Editor**: YAML editor with syntax highlighting and validation
- **Execution Dashboard**: Monitor running and completed workflows
- **Flow Repository**: Browse and manage flows by namespace

## Testing Strategy

- **Unit tests**: JUnit 5 + Mockito + AssertJ in `src/test/java/`
- **Integration tests**: Micronaut test framework in `tests/` module
- **E2E tests**: Playwright for UI testing in `e2e-tests/` module
- **Backend tests**: `./gradlew test`
- **Frontend tests**: `npm test` in `ui/` directory
- **Coverage**: Jacoco for code coverage, SonarCloud for analysis

Tests are configured with:
- Max heap size: 4GB
- Default locale: en_US
- Environment variables for secrets (base64 encoded)
- Parallel execution support (commented out in build.gradle)

## Code Style Guidelines

- **Java**: 4 spaces, follow Micronaut patterns, enable annotation processors
- **YAML/JSON/CSS**: 2 spaces
- **Frontend**: ESLint + Prettier configuration in `.eslintrc.cjs`, `.prettierignore`
- **EditorConfig**: Configured in `.editorconfig`
- **Architecture**: Follow hexagonal architecture patterns with clear module boundaries

## Running in Development

### Backend
```bash
# Local mode (H2, fastest for development)
./gradlew runLocal

# Standalone mode (PostgreSQL, full production-like)
./gradlew runStandalone
```

Access backend at http://localhost:8080

### Frontend
```bash
cd ui
npm run dev
```

Access UI at http://localhost:5173

Ensure CORS is configured in `application-override.yml` to allow `http://localhost:5173`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MICRONAUT_ENVIRONMENTS` | Config environments | `local,override` |
| `KESTRA_PLUGINS_PATH` | Plugin directory | `local/plugins` |
| `KESTRA_WORKER_THREADS` | Worker threads | `4` |
| `NODE_OPTIONS` | Node.js heap size | `--max-old-space-size=4096` |

## Common Development Tasks

### Adding a New Task Type
1. Create task class in `core/src/main/java/io/kestra/core/models/tasks/`
2. Implement `Task` interface
3. Add validation annotations
4. Create tests in `core/src/test/java/`
5. Update documentation

### Adding a New Plugin
1. Follow [Plugin Developer Guide](https://kestra.io/docs/plugin-developer-guide/)
2. Build JAR and place in `KESTRA_PLUGINS_PATH`
3. Test with both local and standalone modes

### Database Changes
1. Create Flyway migration in `webserver/src/main/resources/migrations/`
2. Test with all database backends (H2, PostgreSQL, MySQL)
3. Update `application-override.yml` examples

## Known Development Issues

- **Gradle permission**: Use `chmod +x gradlew` if needed
- **Memory issues**: Increase Node.js heap with `NODE_OPTIONS=--max-old-space-size=4096`
- **CORS**: Must configure backend for frontend dev server
- **Database connection**: Use `host.docker.internal` from devcontainer instead of `localhost`
- **Build failures**: Run `./gradlew clean` to clear Gradle cache

## Useful Resources

- [Kestra Documentation](https://kestra.io/docs)
- [Plugin Developer Guide](https://kestra.io/docs/plugin-developer-guide/)
- [Micronaut Documentation](https://docs.micronaut.io/)
- [Vue.js Documentation](https://vuejs.org/)
- [GitHub Issues](https://github.com/kestra-io/kestra/issues)
- [Slack Community](https://kestra.io/slack)

## Deployment Modes

### Local Mode
- Uses H2 in-memory database
- Repository and queue in-memory
- Fastest for development
- Run: `./gradlew runLocal`

### Standalone Mode
- Uses PostgreSQL (or MySQL)
- Production-like configuration
- Persistent storage
- Run: `./gradlew runStandalone` or `make start-standalone-postgres`

Both modes load plugins from `KESTRA_PLUGINS_PATH` (default: `local/plugins`).