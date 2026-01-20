# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Miyagi is a polyglot microservices sample showcasing Microsoft's Copilot Stack for building enterprise-grade AI-infused applications. The project demonstrates generative and traditional ML use cases using Semantic Kernel, Azure OpenAI, and various agent frameworks.

## Build Commands

### .NET Services (order-service, recommendation-service, sk-copilot-chat-api, chatgpt-plugin/dotnet)

```bash
# Build
dotnet build <project-path>/GBB.Miyagi.<ServiceName>.csproj

# Run
dotnet run --project <project-path>/GBB.Miyagi.<ServiceName>.csproj

# Watch mode (development)
dotnet watch run --project <project-path>/GBB.Miyagi.<ServiceName>.csproj

# Docker build
docker build -t <service-name> <service-path>
```

### Python Services (expense-service/python, recommendation-service/python, chatgpt-plugin/python)

```bash
# Install dependencies (Poetry-based)
poetry install

# Run FastAPI service
poetry run start
# or
uvicorn server.main:start --host 0.0.0.0 --port 8000

# Development
poetry run dev
```

### TypeScript Services (expense-service/typescript, ui/typescript)

```bash
# Install dependencies
yarn install

# Build TypeScript
yarn build

# Run development server (UI)
yarn dev
```

### Java Service (user-service)

```bash
# Build
mvn clean package

# Run
mvn spring-boot:run

# Docker build
docker build -t user-service services/user-service/java
```

## Architecture

```
/home/ubuntu/deploy-projects/35fa5498a8b585635e0b55ed/
├── services/           # Core microservices
│   ├── order-service/dotnet/           # Kafka-based order processing (Semantic Kernel)
│   ├── recommendation-service/          # Investment recommendations (both dotnet & python)
│   ├── sk-copilot-chat-api/dotnet/     # Chat API with memory (fork of Semantic Kernel's chat-copilot)
│   ├── expense-service/                 # Classification/analysis (python & typescript)
│   ├── user-service/java/               # Synthetic data generation (Spring Boot)
│   └── chatgpt-plugin/                  # ChatGPT plugin (python & dotnet/azure-function)
├── ui/typescript/       # Next.js frontend with Material-UI
├── agents/              # Agent framework examples (Assistants API, AutoGen, TaskWeaver)
├── sandbox/             # Experiments and use cases (LangChain, LlamaIndex, PromptFlow)
└── deploy/              # Infrastructure (Terraform, Bicep)
```

### Key Integration Patterns

1. **Semantic Kernel**: Native and semantic functions organized in `Plugins/` directories with `skprompt.txt` and `config.json`
2. **Memory/Vector Stores**: Qdrant, Azure Cognitive Search, Cosmos DB for semantic memory
3. **Event-Driven**: Kafka/Event Grid for async processing (order-service)
4. **Authentication**: Azure Identity with `DefaultAzureCredential` for secure service communication

### Service Communication

- Services use OAuth via Azure Identity for secure inter-service communication
- Configuration via `appsettings.json` and user-secrets for local development
- Environment variables required: Azure OpenAI endpoints/keys, Cosmos DB connection strings, etc.

## Development Workflow

1. Set required Azure services (Azure OpenAI, Cosmos DB, Azure Cognitive Search)
2. Configure environment variables or user-secrets for local authentication
3. Run individual services with appropriate build/run commands
4. Use Docker Compose for multi-service local development where available

## Common Patterns

- **Semantic Kernel Plugins**: Stored in `Plugins/<PluginName>/` with `skprompt.txt` and `config.json`
- **Controller/Endpoint Pattern**: REST APIs in `Controllers/` (dotnet) or FastAPI routes (python)
- **Configuration**: `appsettings.json` for defaults, environment overrides, or user-secrets for secrets