# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**bk-ci** is Tencent's open-source CI/CD platform written in multiple languages (Kotlin/Java, Go, Vue.js, Lua, Shell). It provides pipeline management, code inspection, repository management, credential management, environment management, a development store, build acceleration, and artifact repository.

**Architecture**: Microservices-based architecture with:
- **Frontend**: Vue.js SPA applications
- **Backend**: Kotlin/Spring Boot microservices
- **Gateway**: OpenResty (Nginx + Lua)
- **Agent**: Go-based build agent with Kotlin worker

## Common Development Commands

### Backend (Kotlin/Gradle)

**Location**: `src/backend/ci/`

**Build**:
```bash
cd src/backend/ci
./gradlew clean build          # Full build with tests
./gradlew build -x test        # Build without tests
```

**Run Tests**:
```bash
./gradlew test                 # Run all tests
./gradlew test --tests "*ClassName*"  # Run specific test class
./gradlew test --tests "*Package.*"   # Run tests in package
```

**Lint & Format**:
```bash
./gradlew ktlintFormat         # Format Kotlin code
./gradlew ktlintCheck          # Check Kotlin code style
```

**License Check**:
```bash
./gradlew licenseCheck         # Check license compliance
./gradlew licenseFormat        # Format license headers
```

**Build Specific Microservice**:
```bash
./gradlew :core:process:boot-process:build   # Build process microservice
./gradlew :core:dispatch:boot-dispatch:build # Build dispatch microservice
```

**Database Regeneration**:
```bash
# JOOQ requires DB connection - configure in gradle.properties first
./gradlew clean build
```

**Requirements**:
- JDK 8+
- Gradle 6.7+
- MySQL 5.7+ (for JOOQ code generation)
- Database must be initialized from `support-files/sql` before building

### Frontend (Vue.js)

**Location**: `src/frontend/`

**Setup**:
```bash
cd src/frontend
pnpm install                   # Install dependencies
```

**Development**:
```bash
pnpm run build:dev            # Build all frontend apps for dev
pnpm start                    # Install dependencies for all sub-projects
```

**Production Build**:
```bash
pnpm run public               # Build for production
pnpm run build:test           # Build for test environment
pnpm run build:master         # Build for master environment
pnpm run build:external       # Build for external users
```

**Requirements**:
- Node.js 20.17.0+
- pnpm 9+

**Linting**:
- ESLint configured with pre-commit hooks via husky
- Lint-staged automatically fixes JS/TS/Vue files on commit

### Agent (Go)

**Location**: `src/agent/`

**Build**:
```bash
# Don't use cross-compilation
cd src/agent
build_linux.sh                # Linux build
build_windows.bat             # Windows build
build_macos.sh                # macOS build
```

**Output**: `src/agent/bin/` contains:
- devopsAgent.exe / devopsAgent_linux / devopsAgent_macos
- devopsDaemon.exe / devopsDaemon_linux / devopsDaemon_macos
- upgrader.exe / upgrader_linux / upgrader_macos

**Requirements**:
- Go 1.12+

### Gateway

No compilation required (Lua scripts + Nginx configs)

## Architecture Overview

### Core Components

1. **Gateway** (`src/gateway/`):
   - OpenResty-based API gateway
   - User authentication and authorization
   - Consul-based service discovery routing
   - Lua scripts handle auth, routing, and dynamic configuration

2. **Frontend** (`src/frontend/`):
   - Multiple Vue.js SPAs:
     - `devops-nav`: Main entry point
     - `devops-pipeline`: Pipeline management
     - `devops-codelib`: Code repository management
     - `devops-ticket`: Credential management
     - `devops-environment`: Environment management
     - `devops-atomstore`: Plugin/Template store
   - Mounted via Iframe or UMD

3. **Backend Microservices** (`src/backend/ci/core/`):
   - `project`: Project management (foundational service)
   - `log`: Build log collection and querying
   - `ticket`: Credential management
   - `repository`: Code repository integration
   - `artifactory`: Artifact storage (generic/maven/npm/pypi/oci/docker/helm)
   - `environment`: Build agent management
   - `store`: Plugin/template marketplace
   - `process`: Pipeline orchestration (core service)
   - `dispatch`: Build agent dispatch/scheduling
   - `plugin`: Extension service for third-party integrations
   - `worker`: Task executor (Kotlin `agent.jar`)

4. **Agent** (`src/agent/`):
   - Go-based binary running on build machines
   - `DevopsDaemon`: Process supervisor
   - `DevopsAgent`: Communicates with dispatch/environment, manages worker
   - Spawns Kotlin `worker-agent.jar` for actual task execution

### Service Dependencies

```
process (orchestration)
    ↓
dispatch ← → environment ← → agent
    ↓                   ↓
ticket ← → repository ← → worker
    ↓
artifactory
    ↓
store
```

### Data Layer

- **MySQL/MariaDB**: Primary relational data store
- **Redis**: Caching and distributed locks
- **ElasticSearch**: Log storage
- **RabbitMQ**: Event-driven messaging
- **Consul**: Service discovery
- **FileSystem/Object Storage**: Artifact storage (S3, COS)

### Module Structure Pattern

Each microservice follows a consistent structure:
- `api-{service}`: API definitions/contracts
- `biz-{service}`: Business logic implementation
- `boot-{service}`: Spring Boot application entry point
- `model-{service}`: JOOQ-generated data models
- `common`: Shared utilities (in `src/backend/ci/core/common/`)

### Worker Sub-modules (`src/backend/ci/core/worker/`)

- `worker-agent`: Main agent process
- `worker-api-sdk`: Backend communication APIs
- `worker-common`: Common utilities
- `worker-plugin-archive`: Built-in archive tasks
- `worker-plugin-scm`: Built-in SCM tasks

## Key Development Notes

### Build System

- **Backend**: Gradle with custom `com.tencent.devops.boot` plugin
- **Frontend**: pnpm monorepo with Nx
- **Build outputs**: `src/backend/ci/release/`
- **Artifact naming**: `boot-{service}.jar` for microservices, `boot-assembly.jar` for monolith

### Configuration

- Backend config in `gradle.properties`:
  - `DB_HOST`, `DB_USERNAME`, `DB_PASSWORD`: Database connection
  - `MAVEN_REPO_URL`, `MAVEN_REPO_SNAPSHOT_URL`: Maven repositories
  - `MAVEN_REPO_DEPLOY_URL`: For deploying artifacts
- Frontend uses environment-specific configs in build commands
- Gateway config in `src/gateway/lua/init.lua`

### Database

- **JOOQ** for code generation requires live database connection
- Initialize from `support-files/sql` before first build
- Regenerate PO models after schema changes: `./gradlew clean build`

### Testing

- Backend: JUnit with MockK for mocking
- Frontend: ESLint for linting (no unit tests configured)
- Pre-commit hooks via husky/lint-staged

### Deployment Modes

- **Microservices**: Default - each service runs independently
- **Monolith**: Set `service_name="bk-ci"` in `init.lua` or empty for standalone

### Commit Message Convention

```
<tag>: <summary> issue #<number>
```

**Tags**:
- `feature/feat`: New features
- `bug/fix/bugfix`: Bug fixes
- `refactor/perf`: Refactoring/optimization
- `test`: Test additions
- `docs`: Documentation
- `info`: Comments
- `format`: Code formatting
- `merge`: Branch merges
- `depend`: Dependency changes
- `chore`: Build scripts/tasks
- `del`: Breaking changes/removals

### Contributing Workflow

1. Create issue with problem, use case, design, implementation details
2. Submit design document to `docs/features/`
3. Team confirms requirements and schedule
4. Implement with tests and documentation
5. Submit PR with code and docs
6. Review and merge (prefer incremental PRs over large single提交s)

### Important Files

- `docs/overview/architecture.md`: Detailed architecture
- `docs/overview/code_framework.md`: Code organization
- `docs/overview/source_compile.md`: Build instructions
- `CONTRIBUTING.md`: Contribution guidelines
- `support-files/sql`: Database initialization scripts
- `support-files/template`: Deployment configuration templates
- `scripts/`: Installation and setup automation

### Extending the Platform

- **Custom Plugins**: Use Java SDK in `src/backend/ci/pipeline-plugin/bksdk/`
- **New Microservices**: Follow existing module structure patterns
- **Platform Integrations**: Extend through `plugin` service
- **Custom Tasks**: Develop using Worker Plugin SDK

### Common Issues

- **DB Connection**: JOOQ generation fails without initialized database
- **Cross-Compilation**: Agent must be built on target OS
- **Environment**: Node.js version must match `.nvmrc` (20.17.0+)
- **Dependencies**: Backend requires JDK 8, Gradle 6.7+, MySQL 5.7+