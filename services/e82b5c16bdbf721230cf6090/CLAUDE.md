# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

This is a multi-module Maven project with 40+ independent Spring Boot demo applications. Each subproject contains its own `pom.xml`.

```bash
# Build a specific project
cd springboot-<project-name>
mvn clean package

# Run a specific project
java -jar target/<project-name>-*.jar

# Multi-module projects (e.g., springboot-agent, springboot-serverless)
cd springboot-<project-name>
mvn clean package -pl <module-name> -am

# Run with Java Agent (for agent-based projects)
java -javaagent:target/<project-name>-*-agent.jar -jar target/<project-name>-*.jar
```

## Architecture Overview

This is a collection of **Spring Boot demo projects** accompanying technical blog articles. Projects are independent and not structured as a unified mono-repo with shared dependencies.

### Project Categories

1. **Java Agent Projects** - Use JVM instrumentation for runtime modification:
   - `springboot-agent` - Multi-module project with agent + app modules
   - `springboot-hot-patch` - Runtime class/bean replacement using ASM bytecode manipulation
   - `springboot-online-debug` - Dynamic debug logging injection via Java Agent + ByteBuddy

2. **Multi-Module Projects**:
   - `springboot-agent` (agent/, app/)
   - `springboot-serverless` (function-hello/, function-user/, serverless-core/)
   - `springboot-package-segment` (demo/)

3. **Web Applications** - Standard Spring Boot web demos:
   - REST APIs, WebSocket apps, Web SSH, UI dashboards
   - Frontend resources in `src/main/resources/static/`

### Common Package Structure

```
src/main/java/<package>/
├── Application.java          # Spring Boot main class
├── controller/               # REST endpoints
├── service/                  # Business logic
├── config/                   # Spring configurations
├── model/ / entity/          # Data models
├── annotation/               # Custom annotations
├── agent/                    # Java Agent classes
└── instrumentation/          # Bytecode instrumentation
```

### Key Technologies

- Spring Boot 2.1.6 to 3.4.5 (version varies by project)
- Java 17+ for newer projects, Java 8 for older demos
- ASM 9.x for bytecode manipulation
- Spring Boot Maven Plugin for executable JARs

### Build Notes

- Projects using Java Agents package a separate `*-agent.jar` using `maven-jar-plugin` with manifest entries for `Agent-Class` and `Premain-Class`
- Some projects embed the agent via `spring-boot-maven-plugin` configuration
- Frontend resources are served from `src/main/resources/static/` or `src/main/resources/public/`