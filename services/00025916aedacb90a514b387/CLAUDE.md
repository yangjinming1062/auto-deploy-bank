# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DevoxxGenie is an IntelliJ IDEA plugin that provides AI-powered code assistance using local and cloud-based Large Language Models (LLMs). It integrates with providers like Ollama, OpenAI, Anthropic, Mistral, Groq, Gemini, and more. The plugin supports RAG (Retrieval-Augmented Generation), MCP (Model Context Protocol), streaming responses, and Test-Driven Generation (TDG).

## Development Commands

### Gradle Tasks

```bash
# Build the plugin
./gradlew build

# Build plugin distribution (creates ZIP in build/distributions)
./gradlew buildPlugin

# Run all tests
./gradlew test

# Run a specific test
./gradlew test --tests ClassName.methodName

# Run IntelliJ IDEA with the plugin loaded for testing
./gradlew runIde

# Verify plugin (includes tests + plugin verification)
./gradlew verifyPlugin

# Clean build artifacts
./gradlew clean

# Publish plugin to JetBrains Marketplace (requires PUBLISH_TOKEN env var)
./gradlew publishPlugin
```

### Task Automation

This project uses [Task](https://taskfile.dev/) for automation. Install Task first, then:

```bash
# Show all available tasks
task

# Build and test
task build-and-test

# Run plugin in IDE
task run-ide

# Generate changelog for a release
task generate-changelog VERSION=0.8.0

# Preview changelog changes without applying them
task preview-changes VERSION=0.8.0
```

Requirements for changelog automation:
- GitHub CLI (`gh`) - Install with `brew install gh`
- `jq` for JSON processing - `brew install jq`
- Python 3 (usually pre-installed)
- Authenticate with GitHub: `gh auth login`

## Code Architecture

### Core Components

1. **UI Layer** (`src/main/java/com/devoxx/genie/ui/`)
   - `panel/` - Main UI panels (UserPromptPanel, ChatResponsePanel, ConversationPanel)
   - `window/` - Tool window factories (DevoxxGenieToolWindowFactory)
   - `listener/` - Event listeners for UI interactions

2. **Controller Layer** (`src/main/java/com/devoxx/genie/controller/`)
   - `PromptExecutionController` - Central controller for prompt handling
   - Manages prompt submission, execution flow, and UI coordination

3. **Service Layer** (`src/main/java/com/devoxx/genie/service/`)
   - `PromptExecutionService` - Core service orchestrating LLM interactions
   - `rag/` - RAG (Retrieval-Augmented Generation) services
   - `mcp/` - Model Context Protocol server integration
   - `projectscanner/` - Project indexing and code scanning
   - `tdg/` - Test-Driven Generation functionality

4. **Chat Model Layer** (`src/main/java/com/devoxx/genie/chatmodel/`)
   - `ChatModelFactory` - Factory for creating LLM chat models
   - `cloud/` - Cloud provider integrations (OpenAI, Anthropic, Mistral, Groq, Gemini, Azure OpenAI, DeepInfra, OpenRouter, Bedrock)
   - `local/` - Local provider integrations (Ollama, GPT4All, LMStudio)

5. **Core Module** (`core/`)
   - Shared library module containing LLM integrations using Langchain4J
   - References model files and common LLM utilities

### Prompt Execution Flow

The plugin processes prompts through a well-defined flow:

1. **Input**: `UserPromptPanel` captures user prompt → `PromptSubmissionListener`
2. **Controller**: `PromptExecutionController.handlePromptSubmission()` initiates execution
3. **Service**: `PromptExecutionService.executeQuery()` handles token calculation, RAG settings
4. **Dispatch**: `ChatPromptExecutor.executePrompt()` sends to selected LLM provider
5. **Model Factory**: `ChatModelFactory.getModels()` retrieves appropriate model
6. **LLM Execution**: Factory-specific implementation (OpenAI, Anthropic, Ollama, etc.)
7. **Response Handling**:
   - **Streaming**: `StreamingPromptExecutor` → `ChatStreamingResponsePanel`
   - **Non-streaming**: `PromptExecutionService` → `ChatResponsePanel`
8. **Display**: Response rendered in `ChatResponsePanel` with metadata and code formatting

See `docs/prompt_flow.png` for a visual diagram of this workflow.

### Key Technical Details

- **Language**: Java (minimum JDK 17)
- **Framework**: IntelliJ Platform SDK
- **LLM Integration**: [Langchain4J](https://github.com/langchain4j/langchain4j) v1.0.0-beta3
- **Database**: ChromaDB (for RAG vector storage, running in Docker)
- **Build System**: Gradle with Shadow plugin
- **Testing**: JUnit 5, Mockito, AssertJ
- **Minimum IntelliJ Version**: 2023.3.4 (build 233)
- **Plugin ID**: `com.devoxx.genie`

### Project Structure

```
DevoxxGenieIDEAPlugin/
├── core/                          # Shared library module (LLM integrations)
├── src/main/java/com/devoxx/genie/
│   ├── action/                    # IntelliJ actions
│   ├── chatmodel/                 # LLM provider integrations
│   │   ├── cloud/                 # Cloud providers (OpenAI, Anthropic, etc.)
│   │   └── local/                 # Local providers (Ollama, GPT4All, etc.)
│   ├── controller/                # Controllers (PromptExecutionController)
│   ├── model/                     # Data models
│   ├── service/                   # Business logic services
│   │   ├── mcp/                   # MCP server integration
│   │   ├── rag/                   # RAG/vector search
│   │   └── tdg/                   # Test-Driven Generation
│   ├── ui/                        # User interface
│   │   ├── panel/                 # UI panels
│   │   ├── listener/              # Event listeners
│   │   └── window/                # Tool windows
│   └── util/                      # Utility classes
├── src/test/                      # Test suite
├── src/main/resources/
│   ├── META-INF/plugin.xml        # Plugin configuration
│   └── icons/                     # Plugin icons
├── Taskfile.yml                   # Task automation
└── build.gradle.kts              # Build configuration
```

## Common Development Tasks

### Adding a New LLM Provider

1. Create a factory class in `src/main/java/com/devoxx/genie/chatmodel/cloud/` (for cloud) or `local/` (for local)
2. Implement the provider's integration using Langchain4J
3. Register the new provider in `ChatModelFactory`
4. Update UI to include the provider selection

Example path:
- Create: `src/main/java/com/devoxx/genie/chatmodel/cloud/yourprovider/YourProviderChatModelFactory.java`
- Modify: `src/main/java/com/devoxx/genie/chatmodel/ChatModelFactory.java`

### Modifying the UI

- **Main chat window**: `src/main/java/com/devoxx/genie/ui/panel/ChatResponsePanel.java`
- **Prompt input**: `src/main/java/com/devoxx/genie/ui/panel/UserPromptPanel.java`
- **Tool window**: `src/main/java/com/devoxx/genie/ui/window/DevoxxGenieToolWindowFactory.java`

### Working with RAG

- **Indexing service**: `src/main/java/com/devoxx/genie/service/rag/ProjectIndexerService.java`
- **Semantic search**: `src/main/java/com/devoxx/genie/service/rag/SemanticSearchService.java`
- **ChromaDB integration**: `src/main/java/com/devoxx/genie/service/chromadb/`

### Modifying Prompt Behavior

- **Prompt commands**: `src/main/java/com/devoxx/genie/service/prompt/command/`
- **Prompt execution**: `src/main/java/com/devoxx/genie/service/prompt/PromptExecutionService.java`
- **Prompt strategies**: `src/main/java/com/devoxx/genie/service/prompt/strategy/`

### Testing

Test structure follows the main code structure:
- Service tests: `src/test/java/com/devoxx/genie/service/`
- Chat model tests: `src/test/java/com/devoxx/genie/chatmodel/`

Run tests with:
```bash
./gradlew test
```

## Build Configuration

Key files:
- `build.gradle.kts` - Main build configuration
- `settings.gradle.kts` - Project settings and module inclusion
- `gradle.properties` - Gradle properties
- `src/main/resources/META-INF/plugin.xml` - Plugin descriptor

Dependencies are organized around Langchain4J for LLM integrations, with additional libraries for:
- Retrofit (HTTP client)
- SQLite JDBC
- Docker Java
- JTokkit (tokenization)
- CommonMark (Markdown rendering)

## Documentation

- **Main README**: `README.md` - Project overview and feature documentation
- **Plugin Guide**: `DEVOXXGENIE.md` - Auto-generated project documentation (can be enhanced)
- **Task Automation**: `TASKFILE_README.md` - How to use Task for changelog automation
- **Docusaurus docs**: `docusaurus/` - User-facing documentation site

## Release Process

1. Update version in `build.gradle.kts`
2. Generate changelog: `task generate-changelog VERSION=X.Y.Z`
3. Review and commit changes
4. Verify plugin: `./gradlew verifyPlugin`
5. Publish: `PUBLISH_TOKEN=xxx ./gradlew publishPlugin`

## Additional Notes

- The project uses the Shadow plugin to create fat JARs with all dependencies
- MCP support is experimental and being actively developed
- RAG feature requires Docker for ChromaDB vector database
- Token cost calculation is available for cloud LLM providers
- Chat memory is configurable (default: 10 messages total)