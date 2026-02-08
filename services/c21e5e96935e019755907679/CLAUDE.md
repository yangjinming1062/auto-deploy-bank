# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tock (The Open Conversation Kit) is an open-source conversational AI platform with:
- **NLU Engine**: Natural Language Processing with OpenNlp, Rasa models, and entity extraction
- **Tock Studio**: Web UI for building stories, training models, and analytics
- **Multi-channel Connectors**: Messenger, WhatsApp, Slack, Google Assistant, Teams, Twitter, etc.
- **Bot API Mode**: REST/websocket/webhook APIs for bot development in any language
- **Gen AI Orchestrator**: LLM orchestration for RAG, embeddings, and guardrails

## Build Commands

### Kotlin/Java Backend

```bash
# Build the entire project
mvn install -Dktlint.fail=false

# Run tests (unit tests only, excludes integration tests)
mvn test

# Run tests for a specific module
mvn test -pl bot/engine

# Format Kotlin code with ktlint
mvn antrun:run@ktlint-format
```

### Frontend (Angular)

```bash
cd bot/admin/web
npm install
npm run start      # Development server
npm run test       # Run unit tests
npm run lint       # Lint with ESLint
npm run build      # Production build
```

### Python (Gen AI Orchestrator)

```bash
cd gen-ai/orchestrator-server/src/main/python/server
poetry install
poetry install --with dev
tox run                       # Run tests with coverage
pip-audit                     # Check for vulnerable dependencies
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Architecture

### Core Modules

- **shared**: Vert.x utilities, Jackson bindings, MongoDB/KMongo, security providers (AWS, GitHub)
- **util**: General utilities (AWS tools, GCP tools, env tools)
- **stt**: Speech-to-text implementations (Google Speech, Noop)
- **translator**: i18n translation (Google Translate, DeepL, Noop)
- **nlp**: NLU engine, model training, Tock Studio NLP front/admin
- **bot**: Bot engine, connectors, admin interface
- **gen-ai**: LLM orchestration (RAG, embeddings, guardrails via FastAPI/LangChain)

### Key Technology Stack

- **Kotlin 2.2.20** with coroutines
- **Vert.x 5.0** for async I/O
- **MongoDB** with Change Streams (replica set required)
- **Kodein 4.1** for dependency injection
- **Jackson 2.20** for JSON serialization
- **Retrofit 3.0 + OkHttp 5.2** for HTTP clients
- **JUnit 6.0** + MockK for testing
- **Python 3.10+ + FastAPI + LangChain** for Gen AI orchestrator

### Dependency Injection (Kodein Pattern)

Most modules define a Kodein `Module` with bindings. The shared injector (`injector`) is used across the application:

```kotlin
// Shared module sets up base bindings
val sharedModule = Kodein.Module {
    bind<Executor>() with provider { vertxExecutor() }
    bind<TockCache>() with provider { MongoCache }
    bind<VertxProvider>() with provider { TockVertxProvider }
    // ...
}

// Other modules extend with their own bindings
val myModule = Kodein.Module {
    bind<MyService>() with singleton { MyServiceImpl(injector.provide()) }
}

// Access injected services
val service: MyService get() = injector.provide()
```

### Vert.x and Coroutine Patterns

Tock uses Vert.x with Kotlin coroutines extensively:

```kotlin
// Vert.x verticle deployment
class MyVerticle : Verticle {
    override suspend fun start() {
        val client = injector.provide<WebClient>()
        client.get("/api").sendJsonAwait(payload)
    }
}

// Executor for coroutines
fun vertxExecutor(): Executor = VertxExecutor(vertx)
```

### Deployment Modes

1. **NLU-only**: Just the NLP API without conversational components
2. **Bot API** (recommended): Connect via REST/WebSocket/Webhook to Tock Studio
3. **Bot Integrated**: Direct MongoDB access (historical mode)

## Bot Development

### Story Definition Pattern

Stories are the core unit of bot conversations. Extend `StoryDefinitionBase`:

```kotlin
class MyStoryHandler : StoryDefinitionBase() {
    override fun startingSteps(): List<Step> = listOf(
        botStep {
            end("Hello! How can I help?")
        }
    )

    override fun starterIntent(): Intent = myIntent
}
```

### StoryHandler Base Classes

For more complex stories, use `SimpleStoryHandler`:

```kotlin
class MyStoryHandler : SimpleStoryHandlerBase(
    story = MyStoryDefinition(),
    handler = SimpleStoryHandlerDefinition(
        action = { bus: MessageBus -> /* do something */ }
    )
)
```

### BotDefinition Pattern

Define available stories in your `BotDefinition`:

```kotlin
class MyBotDefinition : BotDefinitionBase() {
    override fun configuration(): BotConfiguration = ...

    override fun storyDefinitions(): List<StoryDefinition> = listOf(
        GreetingsStoryHandler,
        MyStoryHandler
    )

    override fun findIntent(intentName: String): Intent? = ...
}
```

### Predefined Stories

Special stories executed outside normal flow:
- `unknownStory`: Default when no intent is detected
- `keywordStory`: Bypasses NLP for keyword matches
- `helloStory`: Executed on bot startup
- `goodbyeStory`: Executed on bot exit
- `noInputStory`: Called when user is inactive

## Connector Pattern

Connectors are discovered via Java ServiceLoader. Each connector has a provider file:

**File**: `META-INF/services/ai.tock.bot.connector.ConnectorProvider`

**Example provider**:
```kotlin
class MyConnectorProvider : ConnectorProvider {
    override fun connectorType(): ConnectorType = myConnectorType

    override fun create(connectorController: ConnectorController): Connector {
        return MyConnector(connectorController)
    }
}
```

Key base classes:
- `Connector`: Handles message sending/receiving
- `ConnectorCallback`: Handles responses from the connector
- `ConnectorController`: Manages connector lifecycle and services

Connectors are in `bot/connector-*` directories.

## MongoDB Collections

### tock_bot database
- `bot_configuration`: Bot and connector configurations
- `dialog`: Conversation threads with stories and actions
- `story_configuration`: Story definitions, intents, steps
- `user_timeline`: User analytics data
- `feature`: Bot feature flags

### tock_front database
- `application_definition`: Application/NLU configuration
- `classified_sentence`: Sentences with NLP classifications
- `intent_definition`, `entity_type_definition`: NLU model definitions
- `dictionary_data`: Custom entity values

## Testing

### Kotlin Bot Testing

Use `bot-test` library with JUnit5 `TockJUnit5Extension`:

```kotlin
@RegisterExtension
val ext = TockJUnit5Extension(bot)

@Test
fun `greetings story displays welcome message`() {
    ext.send(locale = Locale.FRENCH) {
        firstAnswer.assertText("Expected response")
    }
}

@Test
fun `dialog test`() {
    ext.send("User message", intent, locale = Locale.FRENCH) {
        firstAnswer.assertText("Response 1")
    }
    ext.send("User response", anotherIntent, locale = Locale.FRENCH) {
        firstBusAnswer.assertText("Response 2")
    }
}
```

### Test Naming Convention

- Unit tests: `*Test.kt`, `*Spec.kt`, or `*Fix.kt`
- Integration tests: `*IntegrationTest.kt` (excluded from `mvn test`)

## Code Style

- **Kotlin**: Follow [ktlint](https://pinterest.github.io/ktlint/) formatting
- **Python**: Black formatter, isort for imports, bandit for security
- **License headers**: Required on all files (Apache 2.0, format: `Copyright (C) 2017/2025 SNCF Connect & Tech`)

## Contribution Guidelines

- Commits must be GPG signed
- PR format: `resolves #ISSUEID Component: title` or `fixes #ISSUEID Component: title`
- Branch format: `ISSUEID_short_title`
- Unit tests required for new features/fixes
- Component prefix in issue title: `[Studio]`, `[Core]`, `[Doc]`, etc.