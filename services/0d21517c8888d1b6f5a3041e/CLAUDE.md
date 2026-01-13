# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🛠️ Common Commands

### Build & Run
```bash
# Build entire project
mvn clean install -DskipTests

# Build specific module
cd ruoyi-admin && mvn clean package

# Run application (default dev profile)
cd ruoyi-admin && mvn spring-boot:run

# Run with specific profile
mvn spring-boot:run -Dspring-boot.run.profiles=prod

# Run main class directly
cd ruoyi-admin && java -jar target/ruoyi-admin.jar
```

### Testing
```bash
# Run all tests
mvn test

# Run tests with specific tag (using Maven profiles)
mvn test -Pdev

# Run single test class
mvn test -Dtest=UserServiceTest

# Run specific test method
mvn test -Dtest=UserServiceTest#testFindById
```

### Development Profiles
- **local**: Local development with debug logging
- **dev** (default): Development environment
- **prod**: Production environment with warn-level logging

### Docker & Deployment
```bash
# Build Docker image
script/deploy/build-docker-images/scripts/build-ruoyi-admin-image.sh

# One-step deployment (China)
script/deploy/one-step-script/deploy-cn.sh

# One-step deployment (International)
script/deploy/one-step-script/deploy-en.sh
```

### Database
```bash
# Initialize database
mysql -u root -p < script/sql/ruoyi-ai.sql

# Or use deploy script
script/deploy/deploy/update_ruoyi-qi-sql.sh
```

## 🏗️ Architecture Overview

### Project Structure
This is a **Spring Boot 3.4** enterprise application using Maven multi-module architecture:

- **ruoyi-admin** (Port 6039): Web service entry point, HTTP controllers
- **ruoyi-modules**: Business functionality modules
  - `ruoyi-system`: User management, roles, permissions
  - `ruoyi-chat`: AI chat functionality and third-party API integration (FastGPT, Coze, DIFY)
  - `ruoyi-generator`: Code generation tools
- **ruoyi-common**: Shared utilities and components
  - Core, Security, Redis, MyBatis, OSS, Excel, SMS, Mail, etc.
- **ruoyi-extend**: Extended AI features
  - `ruoyi-ai-copilot`: AI coding assistant
  - `ruoyi-mcp-server`: Model Context Protocol server
- **ruoyi-modules-api**: API definitions and interfaces

### Key Technologies
- **Framework**: Spring Boot 3.4.4, Spring AI, Langchain4j
- **Database**: MySQL 8.0, MyBatis-Plus, Dynamic Datasource
- **Cache**: Redis with Redisson
- **Auth**: Sa-Token + JWT
- **AI Integration**: OpenAI, FastGPT, Coze, DIFY
- **Vector DB**: Milvus, Weaviate, Qdrant (for RAG)
- **Build**: Maven 3.x, Java 17

### Configuration Files
- Main config: `ruoyi-admin/src/main/resources/application.yml`
- Dev config: `ruoyi-admin/src/main/resources/application-dev.yml`
- Local config: `ruoyi-admin/src/main/resources/application-local.yml`
- Database schema: `script/sql/ruoyi-ai.sql`

### Entry Point
Main application class: `ruoyi-admin/src/main/java/org/ruoyi/RuoYiAIApplication.java`

### Module Dependencies
```
ruoyi-admin
├── ruoyi-system
├── ruoyi-chat
└── ruoyi-generator

ruoyi-modules/* (all depend on)
├── ruoyi-common-* (shared utilities)
└── ruoyi-modules-api (interfaces)
```

## 🔌 Key Integration Points

### AI Platforms
- **FastGPT**: `/chat/send` endpoint supports FastGPT API integration
- **Coze**: ByteDance Coze official SDK integration
- **DIFY**: Java client for workflow and knowledge base management
- **OpenAI**: Spring AI OpenAI client configuration

### Vector Database Setup
Docker Compose for Weaviate available at: `script/docker/weaviate/docker-compose.yml`

### Third-Party Services
- **Redis**: Cache and session management
- **MySQL**: Primary database
- **OSS**: File storage (AWS S3 compatible)
- **SMS**: Aliyun/Tencent SMS services
- **Mail**: Email notifications

## 📝 Development Notes

### API Documentation
- Swagger/OpenAPI docs enabled via SpringDoc
- Bearer token authentication required (configurable in `application.yml`)
- API key header: `Authorization: Bearer {token}`

### Database Configuration
- Default connection: `jdbc:mysql://127.0.0.1:3306/ruoyi-ai`
- Username/Password: `root/root` (dev)
- Supports multiple database types: MySQL, Oracle, PostgreSQL, SQLServer

### Multi-Tenant Support
- Disabled by default (`tenant.enable: false`)
- Configuration in `application.yml` under `tenant` section

### WebSocket
- Enabled for real-time communication
- Path: `/resource/websocket`
- CORS allowed origins configurable

### Security Exclusions
Public endpoints (no auth required) configured in `security.excludes`:
- `/system/model/modelList` (model info)
- `/chat/send` (chat interface)
- `/resource/oss/upload` (file upload)
- Static resources and error pages

## 🚀 Deployment

### Container Orchestration
Docker deployment scripts available in `script/deploy/`:
- One-step deployment scripts for different regions
- Kubernetes-ready Docker images
- Docker Compose configurations

### Environment Setup
Required services:
- MySQL 8.0+
- Redis 6.0+
- (Optional) Vector database: Weaviate/Milvus/Qdrant

### Documentation
- Full documentation: https://doc.pandarobot.chat
- Live demos available at https://web.pandarobot.chat and https://admin.pandarobot.chat