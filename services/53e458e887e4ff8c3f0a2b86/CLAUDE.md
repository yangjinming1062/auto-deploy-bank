# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LangGraph4j is a Java library for building stateful, multi-agent applications with LLMs, inspired by Python's LangGraph. It works with [LangChain4j](https://github.com/langchain4j/langchain4j) and [Spring AI](https://spring.io/projects/spring-ai). The library enables cyclical graph execution where nodes (agents, tools, custom logic) interact with shared state.

## Build Commands

```bash
# Build all modules (skip tests)
./mvnw -q -DskipTests install

# Run unit tests
./mvnw -q test

# Run a single test class
./mvnw test -Dtest=ClassName

# Run a specific test method
./mvnw test -Dtest=ClassName#methodName

# Build a specific module
cd module-name && ../mvnw install
```

**Requirements:** Java 17+ (Java 21+ for `javelit` module)

## Architecture

### Core Concepts

- **StateGraph<S extends AgentState>**: Primary class for defining graph structure. Parameterized by an `AgentState` type.
- **AgentState**: Shared state passed between nodes as a `Map<String, Object>`. Schema defined via `Map<String, Channel.Reducer>`.
- **Nodes**: Building blocks implementing `NodeAction<S>` or `AsyncNodeAction<S>`. Receive current state, return updates as `Map<String, Object>`.
- **Edges**: Define flow control - normal (unconditional) or conditional (dynamically determined based on state).
- **Checkpoints**: Save/restore graph state for debugging, resumption, and long-running processes via `CheckpointSaver` implementations.

### Module Structure

```
langgraph4j/
├── langgraph4j-core/              # Core: StateGraph, CompiledGraph, actions, checkpoints, hooks
├── langgraph4j-*-saver/           # Persistence: MySQL, Postgres, Oracle checkpoint savers
├── langgraph4j-opentelemetry/     # OpenTelemetry observability integration
├── langchain4j/                   # LangChain4j integration
│   ├── langchain4j-core/
│   └── langchain4j-agent/         # ReACT-style AgentExecutor
├── spring-ai/                     # Spring AI integration
│   ├── spring-ai-core/
│   ├── spring-ai-agent/           # ReACT-style AgentExecutor
│   └── spring-ai-agent-archetype/ # Maven archetype for projects
├── studio/                        # Web UI for visualization/debugging
│   ├── base/                      # Shared UI components
│   ├── jetty/                     # Jetty server implementation
│   ├── quarkus/                   # Quarkus server implementation
│   └── springboot/                # Spring Boot implementation
├── how-tos/                       # Jupyter notebooks with examples
├── javelit/                       # AG-UI Event Listener integration (Java 21+)
└── generator/                     # Code generation tools
```

### Key Packages in langgraph4j-core

- `org.bsc.langgraph4j.action` - Node and edge action definitions
- `org.bsc.langgraph4j.state` - State, channels, and reducers
- `org.bsc.langgraph4j.checkpoint` - Checkpoint/saver implementations
- `org.bsc.langgraph4j.hook` - Node and edge hooks for observability
- `org.bsc.langgraph4j.internal` - Internal implementation (node, edge, hook management)
- `org.bsc.langgraph4j.serializer` - State serialization (Jackson, Gson, Java serialization)
- `org.bsc.langgraph4j.subgraph` - Subgraph composition

### Integration Patterns

**LangChain4j Integration** (`langchain4j/`):
- `AgentExecutor`: ReACT-style agent that uses LangChain4j's chat model and tool definitions
- Tools annotated with `@Tool`, parameters with `@P` or `@ToolParam`

**Spring AI Integration** (`spring-ai/`):
- `AgentExecutor`: Similar ReACT agent using Spring AI's `ChatModel` and `@Tool` annotations
- Uses Spring AI's `ToolCallback` mechanism

**Studio** (`studio/`):
- Embeddable web application for visualizing, running, and debugging graphs
- Supports multiple server implementations (Jetty, Quarkus, Spring Boot)

**Javelit** (`javelit/`):
- AG-UI (Agent-Graph User Interface) protocol implementation for streaming events
- Enables real-time UI updates from agent graphs (Java 21+)

## Conventions

- **Java 17+** minimum supported version
- **Public APIs**: Keep stable; prefer additive changes over breaking modifications
- **Dependencies**: Minimize third-party dependencies in core modules
- **Logging**: Structured and minimal in production code
- **Code style**: Follow module-local patterns; scan similar modules for existing conventions
- **Testing**: Use `*Test.java` naming for unit tests, `*ITest.java` for integration tests

## Development Workflow

1. Use `rg` (ripgrep) for code search across the codebase
2. Avoid touching unrelated files in a single commit
3. When adding new public APIs, update relevant module README and/or add docs in `how-tos/`
4. Check `how-tos/` directory for example Jupyter notebooks demonstrating features

## Key Files

- `AGENT.md` - Agent-specific guidance (supplements this file)
- `README.md` - Full project documentation
- `generator/README.md` - Code generation tools documentation
- `how-tos/src/site/markdown/` - Markdown versions of example notebooks