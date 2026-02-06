# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

JdonFramework is a Domain Events framework supporting Domain-Driven Design (DDD) + CQRS + EventSourcing patterns with asynchronous, non-blocking message processing using LMAX Disruptor.

## Build Commands

```bash
# Build with Maven (primary build system)
mvn clean package

# Build with Gradle
./gradlew build

# Run tests
mvn test

# Run a single test class
mvn test -Dtest=TestClassName

# Run a single test method
mvn test -Dtest=TestClassName#testMethodName

# Generate JavaDoc
mvn javadoc:javadoc

# Install to local Maven repository
mvn install
```

## Architecture

### Core Concepts

**Domain Models** (`@Model` annotation): Aggregate roots that live in memory with state. Annotated classes are managed by the container with automatic caching and lifecycle management.

**Event Processing**:
- `@Send("topic")` - Produces messages to a topic/queue from a domain model method
- `@OnCommand("commandName")` - Handles commands in 1:1 queue mode (synchronous)
- `@Consumer("topic")` - Subscribes to topics for 1:N pub/sub mode (asynchronous)
- `@OnEvent` - Handles domain events from other aggregates

**Message Types**:
- `Command` - Input messages that drive state changes
- `DomainMessage` - Extends Command, carries event source and supports async result handling via `EventResultHandler`

**Dependency Injection**:
- `@Inject` - Field injection into domain models
- `@Introduce("message")` - Introduces message sending capability into domain models
- Uses PicoContainer for IoC

### Key Packages

- `com.jdon.annotation` - Framework annotations (@Model, @Consumer, @OnCommand, @Send, @Inject, etc.)
- `com.jdon.domain.message` - Core message classes (Command, DomainMessage, DomainEventHandler)
- `com.jdon.async.disruptor` - LMAX Disruptor integration for high-performance event processing
- `com.jdon.container` - IoC container and dependency injection (PicoContainer wrapper)
- `com.jdon.aop` - AOP proxy and reflection utilities
- `com.jdon.bussinessproxy` - Business proxy for domain model invocation

### Accessory Modules (JdonAccessory/)

- `jdon-hibernate3x` - Hibernate 3.x integration
- `jdon-jdbc` - JDBC templates and data access
- `jdon-remote` - Remote communication support
- `jdon-struts1x` - Struts 1.x integration

### Event Processing Flow

1. Command/Event is sent via `@Send` or injected `DomainEventProduceIF`
2. Messages go through Disruptor's RingBuffer for lock-free async processing
3. `@OnCommand` handlers process in 1:1 queue mode (single thread per aggregate)
4. `@OnEvent` handlers process in 1:N pub/sub mode
5. Results can be retrieved synchronously via `DomainMessage.getEventResult()` or `getBlockEventResult()`

### Configuration

XML-based configuration loaded via `ContainerLoaderXML` with ConfigInfo passing to PicoContainer. Key settings include:
- Disruptor configuration (RingBuffer size, wait strategies)
- Cache configuration for domain models
- Event handler mappings

## Source Structure

```
src/main/java/com/jdon/
├── annotation/          # Framework annotations
├── aop/                 # AOP proxies and interceptors
├── async/               # Async event processing (Disruptor)
├── bussinessproxy/      # Domain model invocation proxies
├── cache/               # Caching utilities
├── components/          # Component definitions
├── container/           # IoC container (PicoContainer wrapper)
├── controller/          # Web controller support
├── domain/              # Domain model and message core
└── util/                # Utility classes
```

## Dependencies

Key external dependencies:
- LMAX Disruptor 3.3.x - RingBuffer implementation
- PicoContainer 1.2 - IoC container
- Javassist - Bytecode manipulation
- Guava - Collections and utilities
- Log4j 2.x - Logging
- JDOM - XML parsing

## Test Examples

Test samples demonstrating patterns are in `src/test/java/com/jdon/sample/test/`:
- `cqrs/` - CQRS pattern examples
- `bankaccount/` - Saga pattern example with distributed transactions
- `dci/` - Data-Context-Interaction pattern