# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RuoYi AI is an enterprise-level AI assistant platform built on Spring Boot 3.4, integrating multiple AI platforms (FastGPT, Coze, DIFY), supporting RAG technology, knowledge graphs, digital humans, and AI workflow orchestration. The system provides multi-model support (OpenAI GPT-4, Azure, ChatGLM, Tongyi, Zhipu AI) and includes real-time streaming conversations via SSE/WebSocket.

**Main Entry Point**: `ruoyi-admin/src/main/java/org/ruoyi/RuoYiAIApplication.java:1`

## Development Commands

### Build & Run
```bash
# Build all modules (requires Java 17+ and Maven)
mvn clean package -Pprod

# Build specific profile (dev/prod)
mvn clean package -Pdev
mvn clean package -Pprod

# Run tests
mvn test

# Run specific test class
mvn test -Dtest=ClassName

# Run single test method
mvn test -Dtest=ClassName#methodName

# Start application in dev mode
cd ruoyi-admin && mvn spring-boot:run -Pdev

# Or after building
java -jar ruoyi-admin/target/ruoyi-admin.jar --spring.profiles.active=dev
```

### Docker Deployment
```bash
# Build Docker image
docker build -t ruoyi-ai-backend:v20251013 .

# Start with docker-compose
docker compose up -d

# View logs
docker logs -f <container_name>

# View container status
docker compose ps
```

See `docs/RuoYi-AI 后端部署教程（Docker 部署版）.md:1` for detailed deployment instructions.

## Code Architecture

### Module Structure
- **`ruoyi-admin`** (ruoyi-admin:1): Main Spring Boot application entry point. Contains main configuration, WebSocket support, and core application logic
- **`ruoyi-common`** (ruoyi-common:1): Shared components and utilities across all modules
- **`ruoyi-modules`** (ruoyi-modules:1): Core business modules
  - `ruoyi-system` (ruoyi-modules/ruoyi-system:1): System management (users, roles, permissions)
  - `ruoyi-chat` (ruoyi-modules/ruoyi-chat:1): AI chat service supporting multiple AI platforms
  - `ruoyi-graph` (ruoyi-modules/ruoyi-graph:1): Knowledge graph functionality with Neo4j
  - `ruoyi-workflow` (ruoyi-modules/ruoyi-workflow:1): AI workflow orchestration using LangGraph4j
  - `ruoyi-generator` (ruoyi-modules/ruoyi-generator:1): Code generation tools
  - `ruoyi-aihuman` (ruoyi-modules/ruoyi-aihuman:1): Digital human integration
  - `ruoyi-wechat` (ruoyi-modules/ruoyi-wechat:1): WeChat integration
- **`ruoyi-modules-api`** (ruoyi-modules-api:1): API interfaces and DTOs for modules
- **`ruoyi-extend`** (ruoyi-extend:1): Extended functionality
  - `ruoyi-ai-copilot` (ruoyi-extend/ruoyi-ai-copilot:1): AI coding assistant
  - `ruoyi-mcp-server` (ruoyi-extend/ruoyi-mcp-server:1): MCP (Model Context Protocol) server

### Key Technologies
- **Framework**: Spring Boot 3.4.4 with Spring AI integration
- **AI Integration**: LangChain4j, OpenAI, FastGPT, Coze, DIFY
- **Database**: MySQL 8.0 (primary), Redis (cache), Neo4j (knowledge graph), Milvus/Weaviate (vector database)
- **ORM**: MyBatis Plus with dynamic data sources
- **Authentication**: Sa-Token with JWT
- **Build Tool**: Maven with Java 17
- **Real-time Communication**: WebSocket and SSE (Server-Sent Events)

### Configuration Files
- **Main Config**: `ruoyi-admin/src/main/resources/application.yml:1` - Core application settings
- **Dev Config**: `ruoyi-admin/src/main/resources/application-dev.yml:1` - Development environment settings
- **Prod Config**: `ruoyi-admin/src/main/resources/application-prod.yml:1` - Production environment settings (to be created)
- **Parent POM**: `pom.xml:1` - Maven configuration and dependency management

### Database & Dependencies
- **SQL Scripts**: `script/sql/ruoyi-ai.sql:1` - Initial database schema
- **Port**: 6039 (configurable via `server.port` in application.yml:27)
- **Required Services**: MySQL (3306), Redis (6379), optional Neo4j (7687), Weaviate (6038), MinIO (9000)

### Profile Configuration
The project uses Maven profiles for environment management:
- **local**: For local development with debug logging
- **dev**: Default development profile with debug logging
- **prod**: Production profile with warn logging

Active profile is configured in `application.yml:72` and can be overridden with `--spring.profiles.active=<profile>`.

### Key Integration Points

#### AI Configuration (application.yml:321)
```yaml
spring:
  ai:
    openai:
      api-key: sk-xx
      base-url: https://api.pandarobot.chat/
```

#### Vector Store (application.yml:338)
```yaml
vector-store:
  type: weaviate  # or milvus
  weaviate:
    host: 127.0.0.1:6038
```

#### Knowledge Graph (application.yml:364)
```yaml
knowledge:
  graph:
    enabled: false  # Enable to use Neo4j knowledge graph
    database-type: neo4j
```

#### WebSocket (application.yml:312)
```yaml
websocket:
  enabled: true
  path: /resource/websocket
```

### Testing
Tests use JUnit with Maven Surefire plugin. Tests are categorized by profiles:
- Run dev profile tests: `mvn test -Pdev`
- Run prod profile tests: `mvn test -Pprod`
- Exclude integration tests using `@Tag("exclude")`

### API Documentation
- Swagger/OpenAPI docs available at: `http://localhost:6039/v3/api-docs`
- Knife4j UI at: `http://localhost:6039/doc.html`
- API authentication via `Authorization` header with Bearer token

### Security Configuration
Security exclusions in `application.yml:117`:
- Chat endpoints (`/chat/send`, `/chat/upload`)
- File upload (`/resource/oss/upload`)
- Static resources
- Swagger documentation
- Model list (`/system/model/modelList`)

### Documentation
- **Full Documentation**: https://doc.pandarobot.chat
- **Deployment Guide**: `docs/RuoYi-AI 后端部署教程（Docker 部署版）.md:1`
- **Workflow Module**: `docs/工作流模块说明.md:1`

### Common Development Tasks

#### Adding a New Module
1. Create module directory under `ruoyi-modules/`
2. Add module to parent `pom.xml:392`
3. Create corresponding API module under `ruoyi-modules-api/`
4. Configure MyBatis Plus scanning in `application.yml:183`

#### Database Changes
1. Modify SQL scripts in `script/sql/`
2. Update entity classes with MyBatis Plus annotations
3. Regenerate if using MyBatis Plus code generation

#### Adding AI Model Support
1. Configure model parameters in `application.yml`
2. Add model provider implementation in `ruoyi-modules/ruoyi-chat`
3. Update security exclusions if needed

### Deployment Notes
- Default admin credentials: `admin` / `admin123` (change in production)
- Health checks available at `/actuator/health`
- Logs location: `./logs/sys-console.log` (configurable in `application.yml:305`)
- Ensure proper configuration of MySQL, Redis, and optional services before production deployment