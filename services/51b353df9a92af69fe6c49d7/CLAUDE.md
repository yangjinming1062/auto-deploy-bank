# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bytedesk is an AI-powered omnichannel customer service platform ("Chat as a Service") built on a Java 17 modular monolith architecture. It provides real-time messaging, team collaboration, knowledge base management, and AI agent capabilities.

**License**: AGPL v3 (open source version) / Business Source License 1.1 (certain enterprise components). Resale is prohibited without permission.

## Build Commands

```bash
# Full build (from root directory)
mvn clean install

# Build skipping tests
mvn clean install -DskipTests

# Run tests
mvn test

# Run a single test class
mvn test -Dtest=QueueTest

# Run a single test method
mvn test -Dtest=QueueTest#testMassVisitorRequests

# Generate JavaDoc (outputs to starter/src/main/resources/static/apidoc)
mvn javadoc:javadoc

# Run locally with default profile (noai - AI disabled)
cd starter && mvn spring-boot:run

# Run locally with AI enabled (uses OpenAI/ZhipuAI/DeepSeek/etc)
cd starter && mvn spring-boot:run -Dspring-boot.run.profiles=open
```

## Docker Development Environment

```bash
cd deploy/docker
# With AI support (ZhipuAI by default, no Ollama)
docker compose -p bytedesk -f docker-compose.yaml up -d

# With Ollama included
docker compose -p bytedesk -f docker-compose-ollama.yaml up -d

# Without AI features
docker compose -p bytedesk -f docker-compose-noai.yaml up -d
```

Default access: http://127.0.0.1:9003/ | admin@email.com / admin

## Architecture

### Maven Monorepo Structure

```
bytedesk/
├── starter/              # Main entry point, Spring Boot application assembly
├── modules/              # Core business modules (open source)
│   ├── ai/               # AI provider integrations, RAG, function calling, MCP server
│   ├── call/             # Call center integration (FreeSWITCH)
│   ├── core/             # Messaging (MQTT/WebSocket), user management, base entities
│   ├── forum/            # Forum/bbs module
│   ├── kbase/            # Knowledge base, FAQ, HelpCenter, RAG
│   ├── service/          # Customer service routing, agent workbench, seating
│   ├── social/           # Social features, messaging
│   ├── team/             # Organization structure, roles, permissions
│   ├── ticket/           # Ticket management, SLA tracking
│   └── voc/              # Voice of customer, feedback, surveys
├── channels/             # External platform integrations (commented out in pom.xml)
│                         # Planned: WeChat, Douyin, Telegram, WhatsApp, etc.
├── plugins/              # Optional extensions
│   └── kanban/           # Kanban board plugin
├── demos/                # Example applications (booking, consumer, shopping)
└── deploy/               # Docker/K8s deployment configurations
```

### Key Technology Stack

- **Framework**: Spring Boot 3.5.0, SOFA Boot 4.2.0
- **Messaging**: Netty-based MQTT server, STOMP/WebSocket over Jetty
- **Async Messaging**: ActiveMQ Artemis (JMS) for event-driven architecture
- **AI**: Spring AI with Ollama, DeepSeek, ZhipuAI, OpenAI, Anthropic, DashScope support
- **Database**: MySQL with Liquibase migrations, Spring Data JPA, QueryDSL
- **Search/Cache**: Elasticsearch (vector store for RAG), Redis, Caffeine (L1 cache)
- **Workflow**: Flowable 7.1.0 (BPMN), Cola State Machine
- **API Docs**: SpringDoc OpenAPI (Swagger UI at `/swagger-ui.html`)

### Communication Patterns

- **Real-time messaging**: Netty-based MQTT server (port 9885) and Spring WebSocket with STOMP (`/ws` endpoint)
- **Async messaging**: JMS via ActiveMQ Artemis for event-driven architecture
- **Spring Events**: Extensive use for decoupling (e.g., `LlmProviderUpdateEvent`, `MessageCreateEvent`, domain events with entity listeners)

### Profile Configuration

Two main profiles:
- **`noai`** (default): AI features disabled, suitable for basic IM/customer service
- **`open`**: Enables AI features with LLM providers

Profile-specific configs:
- `application-noai.properties`: ~46KB of configuration
- `application-open.properties`: ~45KB of configuration (includes AI settings)

## Important Conventions

### Code Patterns
- Uses **Lombok** for boilerplate reduction
- **ModelMapper** for DTO mapping
- REST endpoints return `JsonResult<T>` wrapper structure
- Rich domain events with entity listeners (e.g., `BookingEntityListener`)

### Module Dependencies
- `starter` aggregates all modules into a single executable JAR
- Modules are self-contained with controllers, services, repositories
- Event-driven decoupling via Spring Events
- Channels modules depend on core modules and can be enabled by uncommenting in `channels/pom.xml`

### API Conventions
- Admin API: `/admin/api/v1/...`
- Visitor API: `/visitor/api/v1/...`
- REST API: `/api/v1/...`
- WebSocket: `/ws` endpoint with STOMP
- Module-specific paths: `/ai/`, `/kbase/`, `/service/`, `/team/`, `/ticket/`, `/voc/`

### Configuration
- Main config: `starter/src/main/resources/application.properties`
- Profile configs: `application-noai.properties`, `application-open.properties`
- Liquibase changelogs: `modules/*/src/main/resources/db/changelog/`
- Environment variables override properties in Docker deployments
- Default port: 9003 (HTTP), 9885 (WebSocket/MQTT)
- GeoIP database: `ip2region.xdb` for IP-based location

### Workflows and Processes
- BPMN workflows in `starter/src/main/resources/workflows/`
- Flowable 7.1.0 for process management
- Cola State Machine for stateful transitions

## Adding New Features

1. Create new module under `modules/` for significant functionality
2. Add module to root `pom.xml` modules list and `modules/pom.xml`
3. Update `starter/pom.xml` with module dependency
4. Define DTOs in module, REST controllers expose endpoints
5. Use Spring Events for cross-module communication
6. Add Liquibase changelog for schema changes in module's `db/changelog/`
7. Create entity listeners for domain events

For channel integrations, uncomment the module in `channels/pom.xml` modules section.

## Testing Notes

Tests use JUnit 5 with Spring Boot Test annotations (`@SpringBootTest`, `@AutoConfigureMockMvc`). Mock services with Mockito. Integration tests require infrastructure (MySQL, Redis, Artemis) to be running. The `demos/` module contains example code with booking, consumer, and shopping entities demonstrating the codebase patterns.

## License Notes

- Resale or SaaS deployment is prohibited without permission
- Enterprise modules under Business Source License 1.1
- Contact: 270580156@qq.com