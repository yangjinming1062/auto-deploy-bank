# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start

Spring AI Alibaba is a multi-module Maven project with Java 17+. The project includes:
- Core AI integration modules (Dashscope, models, advisors)
- Graph-based multi-agent framework
- Visual Studio UI with React frontend
- MCP integration
- Auto-configurations and Spring Boot starters

## Common Development Commands

### Java/Maven Build Commands

```bash
# Build entire project (skips tests)
make build
# or
mvn clean package -DskipTests

# Run all tests
make test
# or
mvn test

# Build specific module
mvn clean install -pl spring-ai-alibaba-core -am

# Run single test
mvn test -Dtest=StateGraphTest

# Format code (Spring Javaformat)
make format-fix
# or
mvn spring-javaformat:apply

# Apply Spotless (removes unused imports)
make spotless-apply
# or
mvn spotless:apply

# Check code style
make checkstyle-check
# or
mvn checkstyle:check
```

### Linting and Code Quality

```bash
# Run all linters
make lint

# Check code spelling
make codespell

# Check YAML files
make yaml-lint
make yaml-lint-fix

# Check licenses
make licenses-check
make licenses-fix

# Check for secrets
make secrets-check

# Check newlines
make newline-check
make newline-fix
```

### Working with Modules

This is a multi-module Maven project with the following key modules:

- **spring-ai-alibaba-core** - Core AI capabilities (Dashscope, Chat, Advisors)
- **spring-ai-alibaba-graph-core** - Graph-based multi-agent framework
- **spring-ai-alibaba-studio** - Visual UI (React frontend + Java backend)
- **spring-ai-alibaba-mcp** - MCP (Model Context Protocol) integration
- **spring-ai-alibaba-a2a** - A2A (Agent-to-Agent) communication
- **auto-configurations/** - Spring Boot auto-configurations
- **spring-ai-alibaba-spring-boot-starters/** - Spring Boot starter dependencies

### Frontend Development (Studio)

The studio module contains a React/TypeScript frontend:

```bash
# Install dependencies
npm run re-install

# Build for Java backend
npm run build:subtree:java

# Build for Python backend
npm run build:subtree:python

# Lint frontend code
npm run lint
```

Frontend requirements:
- Node.js >= v20
- Umi 4 framework
- Monorepo structure with packages: main, spark-flow, spark-i18n

### Running Studio Server

The studio server requires Docker services (RocketMQ):

```bash
# 1. Start middleware services
cd spring-ai-alibaba-studio/spring-ai-alibaba-studio-server/docker/middleware
chmod a+x ./run.sh
sudo ./run.sh
# Wait 60 seconds for RocketMQ initialization

# 2. Start backend
cd spring-ai-alibaba-studio/spring-ai-alibaba-studio-server/spring-ai-alibaba-studio-server-admin
mvn spring-boot:run

# 3. Start frontend (in another terminal)
cd spring-ai-alibaba-studio/spring-ai-alibaba-studio-server/frontend/packages/main
npm run dev
```

Access at http://localhost:8000

## Code Architecture

### Core Module (spring-ai-alibaba-core)

Located at `spring-ai-alibaba-core/src/main/java/com/alibaba/cloud/ai/`, provides:

- **dashscope/** - Dashscope LLM integration
- **advisor/** - AI advisors and middleware
- **agent/** - Agent implementations
- **model/** - Model abstractions
- **tool/** - Tool integrations
- **document/** - Document processing
- **evaluation/** - AI evaluation frameworks
- **transformer/** - Data transformers

### Graph Framework (spring-ai-alibaba-graph-core)

Located at `spring-ai-alibaba-graph-core/src/main/java/com/alibaba/cloud/ai/graph/`, implements a LangGraph-inspired framework:

- **State management** - Graph state handling
- **Nodes** - ReAct agents, supervisors, workflow nodes
- **Streaming** - Native streaming support
- **Persistence** - Checkpoints, stores (Redis, MongoDB, FileSystem)
- **Scheduling** - Scheduled agent tasks
- **Serialization** - Plain text and Jackson serializers
- **Human-in-the-loop** - State modification and execution resumption

Key test patterns show usage of:
- `StateGraph` - Main graph orchestration
- `Store` implementations - For persistence
- `Saver` implementations - For checkpoints
- `Serializer` - For state serialization

### Studio Module

Split into client and server components:

**Server** (`spring-ai-alibaba-studio/spring-ai-alibaba-studio-server/`):
- Java backend for administration
- Docker middleware configuration (RocketMQ)
- Plugin system integration

**Client** (`spring-ai-alibaba-studio/spring-ai-alibaba-studio-client/`):
- Configuration and OpenAPI specs

**Frontend** (`spring-ai-alibaba-studio/spring-ai-alibaba-studio-server/frontend/`):
- **packages/main** - Main workbench (Umi 4 SPA)
  - Workflow editor integration
  - Agent/MCP/Plugin management
  - Knowledge base management
  - Model service configuration
- **packages/spark-flow** - Visual workflow editor
  - XYFlow-based node editing
  - Automatic layout (ELK.js)
  - State management (Zustand)
- **packages/spark-i18n** - Internationalization

### MCP Integration

Module: `spring-ai-alibaba-mcp/`

- **MCP Registry** - Nacos-based MCP server discovery
- **MCP Router** - MCP routing and load balancing
- Supports transforming HTTP/Dubbo services to MCP servers

### A2A Integration

Module: `spring-ai-alibaba-a2a/`

- Agent-to-agent communication
- Based on a2a-sdk
- Registry, client, and server implementations

## Configuration

### Maven Configuration

- **Parent POM**: `/pom.xml` - Defines all modules, dependencies, and build plugins
- **Version**: Uses `${revision}` property (currently `1.0.0.4-SNAPSHOT`)
- **Java Version**: 17 (see `java.version` property)
- **Spring Boot**: 3.4.8
- **Spring AI**: 1.0.1

### Code Style

The project enforces:
- **Spring Javaformat** - Automatic formatting
- **Checkstyle** - Code style rules (tools/src/checkstyle/checkstyle.xml)
- **Spotless** - Import removal and additional formatting
- **License headers** - Apache 2.0 header required

Checkstyle config is at `tools/src/checkstyle/checkstyle.xml`

### Dependencies

Key dependencies managed in root POM:
- Dashscope SDK Java 2.15.1
- Spring Boot 3.4.8
- Spring AI 1.0.1
- Nacos 3.1.0
- MCP 0.10.0
- OpenTelemetry 1.38.0
- A2A SDK 0.2.5.Beta2

## Testing

- Uses **JUnit 5** and **Testcontainers** for testing
- Test configuration in `pom.xml` with surefire plugin
- Test classes typically follow `*Test.java` naming
- Integration tests use various store implementations (Redis, MongoDB, etc.)

## CI/CD

- **GitHub Actions**: `.github/workflows/`
  - `build-and-test.yml` - Main CI pipeline
  - Multiple workflows for different platforms
- **Local CI**: Use `make` commands for pre-commit checks
- **Secrets scanning**: gitleaks configured (`.gitleaks.toml`)

## Module-Specific README Files

Each major module has its own README with detailed information:
- `/spring-ai-alibaba-bom/README.md` - Bill of Materials
- `/spring-ai-alibaba-graph-core/README.md` - Graph framework
- `/spring-ai-alibaba-mcp/spring-ai-alibaba-mcp-router/README.md` - MCP router
- `/spring-ai-alibaba-studio/*/README.md` - Studio components

## Version Requirements

- **JDK**: 17 or higher
- **Node.js**: v20 or higher (for frontend)
- **Maven**: Uses `mvnd` (Maven Daemon) for faster builds

## Important Notes

1. **Multi-module builds**: Use `-pl` and `-am` flags to build specific modules
2. **Code formatting**: Always run `make format-fix` or `mvn spotless:apply` before committing
3. **Checkstyle**: Must pass `mvn checkstyle:check` without errors
4. **Dependencies**: Some require Spring Milestones repository (see CONTRIBUTING.md)
5. **Frontend**: Requires Node.js >= v20 and specific build commands
6. **Studio**: Requires Docker for middleware services (RocketMQ)

## Development Workflow

1. Create feature branch from main
2. Develop and run local CI: `make test` and `make lint`
3. Format code: `make format-fix` and `make spotless-apply`
4. Check style: `make checkstyle-check`
5. Build entire project: `make build`
6. Run tests: `make test`
7. Submit PR following commit message format: `type(module): description`

See `CONTRIBUTING.md` for detailed contribution guidelines.