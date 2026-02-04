# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a monorepo containing **50+ example modules** for [LangChain4j](https://github.com/langchain4j/langchain4j), a Java library for building LLM-powered applications. Each module demonstrates a specific integration (OpenAI, Azure, Anthropic, vector databases, etc.) or use case (RAG, agents, memory, tools, etc.).

## Build Commands

**Note:** Before first use, make the Maven wrapper executable:
```bash
chmod +x mvnw
```

**Build the entire monorepo:**
```bash
./mvnw clean install
```

**Build a specific example module:**
```bash
./mvnw -pl open-ai-examples clean package
```

**Build with dependencies (fat JAR):** (for tutorials and other-examples)
```bash
./mvnw -pl tutorials -Pcomplete package
```

**Skip tests:**
```bash
./mvnw -pl module-name -DskipTests
```

## Java Version

Requires **Java 17** or later.

## Architecture

Each module is a **standalone example** demonstrating one or more LangChain4j features:

- **AI Providers:** `open-ai-examples`, `anthropic-examples`, `azure-open-ai-examples`, `bedrock-examples`, `google-ai-gemini-examples`, `mistral-ai-examples`, `ollama-examples`, `vertex-ai-gemini-examples`, `watsonx-ai-examples`
- **Vector Databases:** `chroma-example`, `elasticsearch-example`, `milvus-example`, `neo4j-example`, `opensearch-example`, `pinecone-example`, `pgvector-example`, `qdrant-example`, `redis-example`, `weaviate-example`, `jvector-example`, `google-alloydb-example`, `oracle-example`, `yugabytedb-example`
- **Frameworks:** `spring-boot-example`, `quarkus-example`, `helidon-examples`, `jakartaee-microprofile-example`, `payara-micro-example`, `wildfly-example`
- **Specialized:** `customer-support-agent-example`, `agentic-tutorial`, `rag-examples`, `mcp-example`, `mcp-github-example`, `other-examples`, `tutorials`

All examples use the main `dev.langchain4j:langchain4j-bom` for dependency management.

## Code Style

- Examples use **static nested classes** (e.g., `static class MyExample`) to group related examples
- API keys are loaded from `ApiKeys.java` - each example module has its own with placeholders
- **Never commit actual API keys** - use environment variables or `.env` files in development
- Prettier config: 4-space tab width, 120 character line width

## Important Notes

- Issues should be opened in the [main LangChain4j repository](https://github.com/langchain4j/langchain4j/issues/new/choose), not in this examples repo
- Each module can be imported and run independently in an IDE
- Tutorials in `tutorials/src/main/java` demonstrate core concepts from basic to advanced