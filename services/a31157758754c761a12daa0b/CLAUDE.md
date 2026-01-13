# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LangChain4j is a Java library that simplifies integrating Large Language Models (LLMs) into Java applications. It's a multi-module Maven project with 70+ modules providing unified APIs for 20+ LLM providers and 30+ vector stores. The library supports JDK 17+ (stable) and JDK 21+/25+ (additional/experimental modules).

## Common Development Commands

### Build & Test
```bash
# Build entire project
make build
# or
mvn -U -T12C clean package

# Run tests for a specific module
mvn test -pl langchain4j-core

# Run a single test class
mvn test -Dtest=MyTestClass -pl langchain4j-core

# Run tests with verbose output
mvn test -pl langchain4j-core -Dsurefire.printSummary=true

# Run integration tests
mvn test -pl integration-tests

# Run tests for all modules
mvn test
```

### Code Quality
```bash
# Check code formatting and style (without modifying)
make lint
# or
mvn -T12C -Pspotless spotless:check

# Automatically format code
make format
# or
mvn -T12C -Pspotless spotless:apply
```

### Documentation
```bash
# Build documentation site
cd docs && npm run build

# Serve documentation locally
cd docs && npm run start
```

### Other Useful Commands
```bash
# Install dependencies without building
mvn dependency:resolve

# Clean build artifacts
mvn clean

# Skip tests during build
mvn clean package -DskipTests

# Build with OpenRewrite modernization
mvn -Popenrewrite -Dspotless.check.skip=true org.openrewrite.maven:rewrite-maven-plugin:run
```

## High-Level Code Architecture

### Core Packages (langchain4j-core/)
The core library is organized into several key packages:

- **agent/** - AI agent implementations and orchestration
- **data/** - Data structures and types (documents, messages, embeddings, media)
- **model/** - LLM model abstractions and interfaces
- **rag/** - Retrieval-Augmented Generation components (query, content, pipeline)
- **memory/** - Chat memory management and conversation state
- **store/** - Storage interfaces (embedding stores, memory stores)
- **guardrail/** - Safety and validation mechanisms
- **observability/** - Logging, monitoring, and event tracking
- **invocation/** - Method invocation handling and execution
- **spi/** - Service Provider Interfaces for extensibility

### Module Organization

The project follows a clear module organization pattern:

1. **Core Modules** (langchain4j-core, langchain4j, langchain4j-kotlin)
2. **Model Providers** (20+ modules):
   - OpenAI: `langchain4j-open-ai`, `langchain4j-open-ai-official`
   - Google: `langchain4j-google-ai-gemini`, `langchain4j-vertex-ai*`
   - Anthropic: `langchain4j-anthropic`, `langchain4j-vertex-ai-anthropic`
   - Others: `langchain4j-mistral-ai`, `langchain4j-cohere`, `langchain4j-hugging-face`, etc.
3. **Vector Stores** (30+ modules):
   - Cloud: `langchain4j-pinecone`, `langchain4j-weaviate`, `langchain4j-qdrant`
   - Self-hosted: `langchain4j-elasticsearch`, `langchain4j-opensearch`, `langchain4j-milvus`
   - Cloud providers: `langchain4j-azure-ai-search`, `langchain4j-mongodb-atlas`
   - Databases: `langchain4j-pgvector`, `langchain4j-chroma`, `langchain4j-cassandra`
4. **Document Loaders**: `langchain4j-document-loader-*` modules for S3, GCS, GitHub, etc.
5. **Document Parsers**: `langchain4j-document-parser-*` modules for PDF, Word, Markdown, etc.
6. **Web Search Engines**: `langchain4j-web-search-engine-*` modules
7. **HTTP Clients**: `langchain4j-http-client*` modules with different implementations
8. **Experimental Modules**: `langchain4j-experimental*`, `langchain4j-agentic*`

### Key Configuration Files

- **Parent POM** (`langchain4j-parent/pom.xml`): Defines dependency versions, plugins, and shared configuration
- **Bill of Materials** (`langchain4j-bom/pom.xml`): Provides dependency version management for users
- **Spotless Configuration** (`pom.xml` in root): Code formatting rules with ratchet from `origin/main`
- **Detekt Configuration** (`detekt.yml`): Kotlin static analysis rules
- **Makefile**: Convenience wrapper for common commands

### Build Profiles

- **spotless**: Code formatting and style checking
- **openrewrite**: Code modernization and cleanup
- **jdk21**: Activates modules requiring JDK 21+ (jlama, gpu-llama3)

### Testing Strategy

- **Unit Tests**: JUnit 5 + AssertJ + Mockito Kotlin
- **Kotlin Tests**: Kotest framework for Kotlin modules
- **Integration Tests**: Separate `integration-tests/` module
- **TestContainers**: Used for testing database integrations
- **WireMock**: Used for testing HTTP client integrations

### Java Version Support

- **JDK 17** (minimum, stable): All core modules
- **JDK 21+** (additional features): JLama, GPU Llama 3 modules
- **JDK 25** (experimental/nightly): Some cutting-edge features

### CI/CD Pipeline

The project uses GitHub Actions with multiple workflows:
- `main.yaml`: Main CI build on every PR
- `nightly_jdk{17,21,25}.yaml`: Multi-JDK testing
- `release.yaml`, `snapshot_release.yaml`: Automated releases
- `docs.yaml`: Documentation deployment

### Important Dependencies

- **Jackson** (2.20.1): JSON processing
- **OkHttp** (4.12.0): HTTP client
- **Retrofit** (2.9.0): REST client
- **JUnit** (5.11.3): Testing framework
- **AssertJ** (4.0.0-M1): Test assertions
- **Mockito** (5.19.0): Mocking framework
- **TestContainers** (1.21.3): Integration testing
- **Jackson** (BOM): Version management

## Development Notes

- All modules use the Spotless Maven plugin with ratchet from `origin/main` - this means formatting is checked only against changes from the main branch
- The project uses gitflow-incremental-builder for faster builds by only building changed modules
- Version management is handled through the `langchain4j-parent` and `langchain4j-bom` modules
- Documentation is built using Docusaurus (React/Node.js) and deployed automatically
- No existing Cursor or Copilot rules - this file serves as the primary guidance

## Getting Help

- Documentation: https://docs.langchain4j.dev
- Examples: https://github.com/langchain4j/langchain4j-examples
- Discord: https://discord.gg/JzTFvyjG6R
- GitHub Discussions: https://github.com/langchain4j/langchain4j/discussions