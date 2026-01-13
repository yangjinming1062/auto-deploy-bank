# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SuperSonic is a next-generation AI+BI platform that unifies **Chat BI** (powered by LLM) and **Headless BI** (powered by semantic layer) paradigms. It enables natural language querying of data through Text2SQL with semantic model context, reducing LLM hallucination and complexity.

## Technology Stack

- **Backend**: Java 21, Spring Boot 3.3.9, Maven
- **AI/ML**: LangChain4j for LLM integration, embedding models
- **Database**: MySQL, PostgreSQL, H2 (testing), plus support for Oracle, StarRocks, SAP HANA, DuckDB, Trino, Presto, Kyuubi, ClickHouse, OpenSearch
- **Frontend**: Node.js/pnpm web application in `/webapp`
- **Build**: Maven with Spotless code formatting (Eclipse formatter)
- **Testing**: JUnit 5, Mockito, TestNG

## Module Architecture

### Core Modules

1. **common** - Shared utilities, SQL parsing, date handling, configuration
2. **auth** - Authentication and authorization (agent-level, dataset/column/row-level access control)
3. **chat** - Chat BI interface (api, server)
4. **headless** - Semantic modeling and query processing (api, server, core, chat)
5. **launchers** - Application entry points:
   - `chat` - Chat service launcher
   - `headless` - Headless service launcher
   - `standalone` - Combined chat+headless service
   - `common` - Shared launcher utilities

### Key Components (from README)

- **Knowledge Base**: Extracts schema information from semantic models, builds dictionary/index
- **Schema Mapper**: Identifies schema element references in queries
- **Semantic Parser**: Combines rule-based and LLM-based parsers
- **Semantic Corrector**: Validates and corrects semantic query statements
- **Semantic Translator**: Converts semantic queries to SQL
- **Chat Plugin**: Extends functionality with third-party tools
- **Chat Memory**: Manages historical query trajectories for few-shot prompting

## Development Workflow

### Prerequisites

- **Java 21** (required)
- **Maven 3.x**
- **pnpm** (for webapp development)

### Common Commands

#### Maven Build Commands
```bash
# Clean install (runs tests)
mvn clean install

# Package without running tests
mvn package

# Run only tests
mvn test

# Run specific test class
mvn test -Dtest=ClassName

# Run specific test method
mvn test -Dtest=ClassName#methodName

# Skip tests
mvn clean install -DskipTests

# Format code with Spotless
mvn spotless:apply

# Check code format
mvn spotless:check
```

#### Frontend (Webapp) Commands
```bash
cd webapp

# Install dependencies
pnpm install

# Start development server
./start-fe-dev.sh
# or
./start-fe-pnpm-workspace-dev.sh

# Production build
./start-fe-prod.sh
```

#### Application Startup
```bash
# Start standalone service (chat + headless)
./assembly/bin/supersonic-daemon.sh start

# Or build from release
# Download from: https://github.com/tencentmusic/supersonic/releases
assembly/bin/supersonic-daemon.sh start

# Docker deployment
docker-compose up -d
# Access at http://localhost:9080
```

### Configuration

Application configurations are in:
- `launchers/chat/src/main/resources/application.yaml` - Chat service config
- `launchers/headless/src/main/resources/application.yaml` - Headless service config
- `launchers/standalone/src/main/resources/application.yaml` - Standalone config

Available profiles:
- `local` - Local development
- `h2` - H2 database (default for testing)
- `postgres` - PostgreSQL database

Key settings:
- Server port: 9080 (configurable)
- Swagger UI: `/swagger-ui.html`
- API docs: `/v3/api-docs`
- Database type: Set via `S2_DB_TYPE` environment variable

### Code Style

- **Formatter**: Eclipse formatter configured in `java-formatter.xml`
- **Import Order**: `javax,java,scala,#`
- **Spotless**: Automatically applied during `mvn validate` phase
- Run `mvn spotless:apply` before committing

### Testing

- **Framework**: JUnit 5 (junit-jupiter)
- **Mocking**: Mockito-inline
- **Location**: `src/test/java` in each module
- Test execution: `mvn test` or via IDE

Example test patterns:
```bash
# Run all tests
mvn test

# Run tests in specific module
cd headless && mvn test

# Run single test
mvn test -Dtest=DateUtilsTest

# Run with coverage (if configured)
mvn jacoco:report
```

### Database Support

SuperSonic supports multiple databases:
- MySQL, PostgreSQL, Oracle, H2
- StarRocks, SAP HANA, DuckDB
- Trino, Presto, Kyuubi
- ClickHouse, OpenSearch

Connection configurations are managed in application.yaml files. Different profiles (h2, postgres, etc.) load appropriate configurations.

### LLM Integration

LangChain4j is used for LLM integration:
- OpenAI, local AI models
- Embedding models (BGE, MiniLM)
- Vector stores (Chroma, Milvus, OpenSearch, PGVector)

Configuration in application.yaml:
```yaml
dev.langchain4j: DEBUG
dev.ai4j.openai4j: DEBUG
```

### API Documentation

- **Swagger UI**: http://localhost:9080/swagger-ui.html
- **OpenAPI 3 docs**: http://localhost:9080/v3/api-docs
- **Knife4j**: Enhanced Swagger UI with grouping

### Build Profiles

- **Development**: Use `-Pdev` (if configured) or default
- **Production**: Use application-prod.yaml or environment variables

### CI/CD

GitHub Actions workflows in `.github/workflows/`:
- `ubuntu-ci.yml` - Ubuntu build (Java 21)
- `mac-ci.yml` - macOS build
- `windows-ci.yml` - Windows build
- `centos-ci.yml` - CentOS build
- `docker-publish.yml` - Docker image publishing

CI runs:
- `mvn -B package --file pom.xml`
- `mvn test`

### Troubleshooting

#### Port Already in Use
```bash
# Kill process on port 9080
lsof -ti:9080 | xargs kill -9
```

#### Database Connection Issues
- Check `S2_DB_TYPE` environment variable
- Verify database credentials in configuration
- For H2: default configuration in application.yaml

#### Build Failures
```bash
# Clean and rebuild
mvn clean install

# Update dependencies
mvn dependency:resolve

# Check for formatting issues
mvn spotless:check
```

#### LLM/API Issues
- Check LangChain4j logging (DEBUG level enabled)
- Verify API keys/credentials in configuration
- Test with different embedding models

### Resources

- **Documentation**: https://supersonicbi.github.io/
- **GitHub**: https://github.com/tencentmusic/supersonic
- **Releases**: https://github.com/tencentmusic/supersonic/releases
- **Online Demo**: http://117.72.46.148:9080

### Project Structure

```
supersonic/
├── assembly/          # Build output, scripts
├── auth/              # Authentication module
├── benchmark/         # Performance benchmarking
├── chat/              # Chat BI (api, server)
├── common/            # Shared utilities
├── docker/            # Docker configuration
├── evaluation/        # Evaluation framework
├── headless/          # Headless BI (api, server, core, chat)
├── launchers/         # Application entry points
│   ├── chat/
│   ├── headless/
│   ├── standalone/
│   └── common/
└── webapp/            # Frontend (Node.js/pnpm)
```

### Development Tips

1. **Multi-module Maven**: Each module can be built independently but `mvn clean install` from root builds all
2. **Hot reload**: Use Spring Boot devtools (if configured) for faster iteration
3. **Frontend integration**: Webapp communicates with backend via REST APIs on port 9080
4. **Semantic modeling**: Use Headless BI interface to build models before querying via Chat BI
5. **Testing**: Run integration tests with different database profiles (h2, postgres)

### Extensibility

SuperSonic is designed with SPI (Service Provider Interface) for extensibility:
- Custom parsers
- Database adapters
- Chat plugins
- Embedding models
- Vector stores

Look for `@SPI` annotations and `META-INF/services` files for extension points.