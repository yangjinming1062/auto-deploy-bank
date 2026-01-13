# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-Level Architecture

Lowcoder is an open-source low-code platform for building internal and customer-facing applications. The architecture consists of three main services:

### Frontend (`client/`)
- **Technology**: React + TypeScript + Vite
- **Structure**: Monorepo using Yarn workspaces with multiple packages:
  - `packages/lowcoder`: Main application UI
  - `packages/lowcoder-core`: Core functionality and DSL
  - `packages/lowcoder-comps`: UI component library
  - `packages/lowcoder-cli`: CLI tool for plugin development
  - `packages/lowcoder-sdk`: SDK for integration
- **Port**: 3000 (development), built static files served by API service in production
- **Key Features**: Visual editor, component system, query builder, theme system

### API Service (`server/api-service/`)
- **Technology**: Java 17 + Spring Boot + Maven
- **Structure**: Multi-module Maven project:
  - `lowcoder-server`: Main Spring Boot application (port 8080)
  - `lowcoder-plugins`: Java-based data source plugins (PostgreSQL, MongoDB, etc.)
  - `lowcoder-domain`: Domain models and DTOs
  - `lowcoder-infra`: Infrastructure utilities
  - `lowcoder-sdk`: Shared SDK components
- **Database**: MongoDB (primary data store)
- **Cache**: Redis (session management, caching)
- **Main Class**: `org.lowcoder.api.ServerApplication`

### Node Service (`server/node-service/`)
- **Technology**: Node.js + TypeScript + Express
- **Purpose**: JavaScript execution engine and TypeScript-based data source plugins
- **Port**: 6060
- **Plugins Location**: `src/plugins/` (custom plugins can be added here)
- **Built-in Plugins**: REST API, GraphQL, Redis, Google Sheets, ClickHouse, and more

## Common Development Commands

### Frontend Development
```bash
cd client

# Install dependencies
yarn install

# Start development server
yarn start
# or for Windows:
yarn start-win

# Build for production
yarn build
# or Enterprise edition:
yarn build:ee

# Run tests
yarn test

# Lint and fix code
yarn lint

# Build core packages
yarn build:core

# Test core packages
yarn test:core
```

**Single Test Examples**:
```bash
# Test specific package
yarn workspace lowcoder-core test

# Run Jest on a specific test file
yarn test -- --testPathPattern=ComponentName.test.tsx
```

### Node Service Development
```bash
cd server/node-service

# Install dependencies
yarn install

# Start in development mode with hot reload
yarn dev

# Debug mode (breakpoints enabled)
yarn debug

# Build for production
yarn build

# Run in production
yarn start

# Run tests
yarn test

# Generate OpenAPI plugin from specification
yarn genOpenApiPlugin
```

### API Service Development
```bash
cd server/api-service

# Build all modules and plugins
mvn clean package

# Run from JAR (requires built JAR)
java -Dpf4j.mode=development -Dspring.profiles.active=lowcoder \
  -Dpf4j.pluginsDir=lowcoder-plugins \
  -jar lowcoder-server/target/lowcoder-api-service.jar

# Debug configuration (VS Code launch.json):
# Main class: org.lowcoder.api.ServerApplication
# VM args: -Dpf4j.mode=development -Dpf4j.pluginsDir=server/api-service/lowcoder-plugins \
#          -Dspring.profiles.active=lowcoder-local-dev \
#          -XX:+AllowRedefinitionToAddDeleteMethods --add-opens java.base/java.nio=ALL-UNNAMED
```

### Full Stack Development
**Option 1: Docker (Simplest)**
```bash
# Start all services using prebuilt image
docker run -d --name lowcoder -p 3000:3000 -v "$PWD/stacks:/lowcoder-stacks" \
  lowcoderorg/lowcoder-ce

# Or build from source
docker build -f ./deploy/docker/Dockerfile -t lowcoder-dev .
docker run -d --name lowcoder-dev -p 3000:3000 -v "$PWD/stacks:/lowcoder-stacks" lowcoder-dev
```

**Option 2: Docker Compose**
```bash
cd deploy/docker

# All-in-one deployment
docker compose up -d

# Multi-service deployment
docker compose -f docker-compose-multi.yaml up -d
```

### Prerequisites
- **Java**: OpenJDK 17 required for API service
- **Node.js**: v14.18+ or v16+ for frontend and node service
- **Yarn**: v3.x (configured in `.yarnrc.yml`)
- **Maven**: v3.8+ for API service
- **MongoDB**: Required for API service (or use Docker)
- **Redis**: Required for API service (or use Docker)

Start local databases with Docker:
```bash
docker run -d --name lowcoder-mongodb -p 27017:27017 -e MONGO_INITDB_DATABASE=lowcoder mongo
docker run -d --name lowcoder-redis -p 6379:6379 redis
```

## Environment Configuration

### Docker Environment
Configure via files in `deploy/docker/`:
- `default.env`: Default environment variables
- `default-multi.env`: Defaults for multi-service deployment
- `override.env`: Your custom overrides

Key variables:
- `LOWCODER_API_SERVICE_URL`: API service URL (default: http://localhost:8080)
- `LOWCODER_NODE_SERVICE_URL`: Node service URL (default: http://localhost:6060)
- `LOWCODER_PUBLIC_URL`: Frontend URL (default: localhost:3000)
- `LOWCODER_MONGODB_URL`: MongoDB connection
- `LOWCODER_REDIS_URL`: Redis connection
- `LOWCODER_NODE_SERVICE_SECRET`: Secret for API-Node service communication (MUST change in production)

### API Service Configuration
Configuration files in `server/api-service/lowcoder-server/src/main/resources/`:
- `application-lowcoder.yml`: Default configuration
- `application-lowcoder-local-dev.yml`: Local development overrides
- Profiles controlled by `-Dspring.profiles.active=<profile>`

### Frontend Environment
Set environment variables before build/start:
```bash
export LOWCODER_API_SERVICE_URL=http://localhost:3000
```

## Plugin Development

### Java Plugins (API Service)
Location: `server/api-service/lowcoder-plugins/`

Built-in plugins:
- PostgreSQL, MySQL, MongoDB, Redis
- ClickHouse, Elasticsearch, Oracle, MS SQL, Snowflake

Each plugin is a separate Maven module. To develop a new plugin:
1. Create new module following existing plugin structure
2. Add to parent `pom.xml` modules list
3. Implement required interfaces
4. Rebuild with `mvn clean package`

### TypeScript Plugins (Node Service)
Location: `server/node-service/src/plugins/`

Built-in plugins: REST API, GraphQL, Google Sheets, SMTP, etc.

Plugin interface:
```typescript
interface DataSourcePlugin {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: string;
  dataSourceConfig: ConfigView;
  queryConfig: QueryConfig;
  validateDataSourceConfig: Validator;
  run: RunFunc;
}
```

### UI Components
Use the Lowcoder CLI to create component plugins:
```bash
cd client
yarn create lowcoder-plugin my-component
cd my-component
yarn start
```
Components export via `src/index.ts` and publish with `yarn build --publish`

## Testing Strategy

- **Frontend**: Jest + Testing Library (`yarn test` in `client/`)
- **Node Service**: Jest (`yarn test` in `server/node-service/`)
- **API Service**: JUnit 5 (run via Maven: `mvn test`)

## Deployment

All services are containerized with Docker:
- **All-in-one image**: Single container with all services
- **Multi-service**: Separate containers for each service
- **Kubernetes**: Helm charts in `deploy/helm/`

See `deploy/docker/README.md` for detailed deployment options and environment variables.

## Key Files and Locations

- **Frontend Entry**: `client/packages/lowcoder/src/index.tsx`
- **API Entry**: `server/api-service/lowcoder-server/src/main/java/org/lowcoder/api/ServerApplication.java`
- **Node Service Entry**: `server/node-service/src/server.ts`
- **Plugin Registry**: `server/api-service/lowcoder-plugins/pom.xml`
- **Docker Compose**: `deploy/docker/docker-compose.yaml`
- **API OpenAPI Spec**: `server/api-service/api-examples.http`

## Version Information

- **Current Version**: 2.7.5 (defined in `pom.xml` and `package.json` files)
- **Node Engine**: v14.18+ or v16+
- **Java Version**: 17+

## Development Workflow

1. Start infrastructure (MongoDB + Redis via Docker)
2. Build API service: `cd server/api-service && mvn clean package`
3. Start Node service: `cd server/node-service && yarn dev`
4. Start Frontend: `cd client && yarn start`
5. Access application at http://localhost:3000

For production builds, use `yarn build` (frontend) and `mvn package` (API), then deploy via Docker or Kubernetes.