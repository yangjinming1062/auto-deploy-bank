# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EvoMaster is an AI-driven tool for automatically generating system-level test cases for web/enterprise applications. It uses evolutionary algorithms and dynamic program analysis to generate test cases that maximize code coverage and fault detection. It supports REST, GraphQL, and RPC APIs in both black-box and white-box testing modes.

## Build Commands

**Full build without tests:**
```bash
mvn clean install -DskipTests
```

**Full build with all tests (requires Docker running):**
```bash
mvn clean verify --fae
```

**Run single unit test:**
```bash
mvn test -Dtest=ClassName
```

**Run single integration test (E2E):**
```bash
mvn verify -Dtest=ClassNameIT -pl core-tests/e2e-tests/...
```

**Debug a specific test:**
```bash
mvn -B install -Dtest=TestName -Dsurefire.failIfNoSpecifiedTests=false -DredirectTestOutputToFile=false
```

**Build JavaScript test utils:**
```bash
cd test-utils/test-utils-js && npm ci && npm test
```

**Build Python test utils:**
```bash
cd test-utils/test-utils-py && pip install -r ./src/main/resources/requirements.txt && python -m unittest discover -s ./src/test/ -p '*_test.py'
```

## JDK Requirements

- **Build JDK**: 17
- **Driver library**: Must remain JDK 8 compatible (configured in Maven)
- Running with JDK 17+ requires `--add-opens` flags due to module system restrictions

## Architecture

### Module Structure

- **core/**: Main EvoMaster engine in Kotlin - contains the search algorithm, test generation, and output exporters
- **client-java/**: Java controller library for white-box testing - shaded uber-jar to avoid dependency conflicts
- **core-tests/e2e-tests/**: End-to-end test cases using artificial SUTs
- **core-tests/integration-tests/**: Integration tests
- **test-utils/**: Test utilities for generated tests (Java, JavaScript, Python)

### Core Package Organization (org.evomaster.core)

- **search/**: Evolutionary algorithm components - `algorithms/`, `gene/`, `action/`
- **problem/**: API problem definitions - REST, GraphQL, RPC
- **output/**: Test code generators - Python, Java, Kotlin, JavaScript
- **remote/**: Communication with SUT controller
- **config/**: Configuration management
- **sql/**, **mongo/**: Database interaction handlers
- **taint/**: Taint analysis for test generation
- **parser/**: Schema parsers (OpenAPI/Swagger)
- **utils/**: Utility functions

### Client Library (org.evomaster.client.java)

- **controller/**: Main controller for SUT instrumentation
- **instrumentation/**: Bytecode manipulation for coverage tracking
- **sql/**: SQL database handling
- **controller-api/**: REST API for controller communication

## Key Development Patterns

### Dependency Injection
Uses **Guice** with **Governator** extension. All injectable services are singletons under `*.service` packages. No auto-discovery - beans registered manually for different contexts (e.g., REST vs GraphQL).

### Logging
Use SLF4J LoggerFactory, not `System.out`:
- Kotlin: `companion object { private val log: Logger = LoggerFactory.getLogger(Foo::class.java) }`
- Java: `private static Logger log = LoggerFactory.getLogger(Foo.class);`
- Use `log.debug("msg {} {}", arg1, arg2)` for parameterized logging (avoid string concatenation)

### Randomness
All randomness must come from the `Randomness` class. Never use `java.util.Random` directly. E2E tests run twice with verbose logging to verify determinism.

### Testing Conventions
- Unit tests: `*Test.java`/`*Test.kt` in `src/test/`
- Integration tests: `*IT.java`/`*IT.kt` in `src/test/` (run by failsafe plugin)
- E2E tests: Located in `core-tests/e2e-tests/` module
- Flaky tests should be wrapped in `handleFlaky()` call

### Code Style
- Opening braces `{` on same line as code (not own line)
- No automated formatter currently enforced
- Classes/methods: Max ~1000 lines / ~100 lines respectively

### Package Naming
All code in `org.evomaster.*`. Module names use dashes (e.g., `client-java`), mapped to package names with dots (e.g., `org.evomaster.client.java`). No dashes or uppercase in package names.

## Configuration

Main configuration class: `EMConfig.kt` (~1200 lines). Handles all CLI options and internal settings.

## Common Tasks

### Adding a new dependency
1. Add version to root `pom.xml` in `<dependencyManagement>`
2. Add dependency reference to module's `pom.xml` (no version)
3. For client-java/controller: may need to shade the library

### Adding a new E2E test
1. Create SUT under `core-tests/e2e-tests/`
2. Write driver extending `EvoMasterController`
3. Add E2E test case under same module

### Understanding search algorithm
Start with `search/algorithms/` - particularly `MonoSimple.kt` for the main evolutionary algorithm loop. `Individual.kt` represents a candidate test suite, `EvaluatedIndividual.kt` tracks fitness and coverage.