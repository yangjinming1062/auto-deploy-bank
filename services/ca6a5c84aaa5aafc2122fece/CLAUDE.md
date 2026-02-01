# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a monorepo containing Spring Boot starters for LangChain4j integrations. It provides auto-configuration for various LLM providers (OpenAI, Anthropic, Ollama, etc.) and the core LangChain4j Spring Boot starter.

## Build Commands

```bash
# Build and run all tests
mvn clean verify

# Build and deploy (CI uses this)
mvn -U -B --fail-at-end -DskipOllamaITs clean deploy

# Skip integration tests (run only unit tests)
mvn clean test

# Run integration tests
mvn verify

# Skip Ollama integration tests specifically
mvn verify -DskipOllamaITs

# License compliance check
mvn -U -B -P compliance org.honton.chas:license-maven-plugin:compliance

# Run a single test
mvn test -Dtest=ClassName#methodName

# Run tests in a specific module
mvn test -pl langchain4j-open-ai-spring-boot-starter
```

## Architecture

### Monorepo Structure

- **Parent POM** (`pom.xml`): Defines versions, dependency management, and plugins for all modules
- **langchain4j-spring-boot-starter**: Core starter with @AiService annotation support and RAG auto-configuration
- **langchain4j-http-client-spring-restclient**: Custom HTTP client implementation using Spring's RestClient
- **Integration starters** (e.g., `langchain4j-open-ai-spring-boot-starter`): Provider-specific auto-configuration

### Spring Boot Auto-Configuration Pattern

Each integration starter follows this pattern:

```
module/src/main/
├── java/dev/langchain4j/{provider}/spring/
│   ├── AutoConfig.java          # @AutoConfiguration class with @Bean methods
│   ├── Properties.java          # Top-level configuration properties class
│   ├── {Model}Properties.java   # Record classes for each model type
│   └── ...
└── resources/META-INF/spring/
    └── org.springframework.boot.autoconfigure.AutoConfiguration.imports
        # Contains: dev.langchain4j.{provider}.spring.AutoConfig
```

Properties use the prefix `{provider}.chat-model`, `{provider}.embedding-model`, etc.

### Core Module Architecture

**langchain4j-spring-boot-starter** contains:

- `AiServicesAutoConfig`: Scans for `@AiService` annotated interfaces and auto-wires ChatModels, StreamingChatModels, ChatMemories, ContentRetrievers, RetrievalAugmentors, and ModerationModels
- `RagAutoConfig`: Auto-configures RAG components
- `ClassPathAiServiceScanner`: Custom annotation processor for scanning AI services
- `AiServiceWiringMode`: Enum for AUTOMATIC vs EXPLICIT bean wiring

### Key Technologies

- Java 17+ (CI tests against 17, 21, 22, 23)
- Spring Boot 3.3.8
- Maven with wrapper (`./mvnw`)
- Testcontainers for integration tests
- JUnit Pioneer for test utilities

## Module Naming Convention

Integration starters follow the pattern: `langchain4j-{provider}-spring-boot-starter`

Example modules:
- `langchain4j-open-ai-spring-boot-starter`
- `langchain4j-anthropic-spring-boot-starter`
- `langchain4j-ollama-spring-boot-starter`
- `langchain4j-azure-open-ai-spring-boot-starter`