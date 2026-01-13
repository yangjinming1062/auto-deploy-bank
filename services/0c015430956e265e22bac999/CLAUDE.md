# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Development Setup

```bash
# Install package in editable mode (from repo root)
pip install -e .

# Install with all development dependencies
pip install -e ".[dev]"

# Install with test dependencies
pip install -e ".[test]"

# Install pre-commit hooks
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files
```

### Code Quality

```bash
# Run ruff linter
ruff check

# Run ruff with auto-fix
ruff check --fix

# Format code with ruff
ruff format

# Run type checking
mypy agentops
```

### Testing

```bash
# Run all unit tests
pytest

# Run specific test file
pytest tests/unit/test_llm_event.py -v

# Run tests with coverage
pytest --cov=agentops --cov-report=html

# Run integration tests
pytest tests/integration -v

# Run smoke tests
pytest tests/smoke -v

# Run benchmark tests
pytest tests/benchmark -v

# Run tox for multi-version testing
tox
```

### Examples & Integration Testing

```bash
# Run a specific example (from examples directory)
python examples/openai/openai_example_sync.py

# Run all examples (from examples directory)
for script in $(find . -name "*.py" -type f | grep -v "__pycache__"); do
    python "$script"
done

# Run with validation
AGENTOPS_API_KEY=<key> python examples/openai/openai_example_sync.py
```

### Self-Hosted App Development

The app directory contains the self-hosted AgentOps platform (Dashboard + API):

```bash
# From app/ directory
# Start all services with Docker Compose
docker compose up -d

# Restart services
docker compose down --remove-orphans
docker compose up -d

# View logs
docker compose logs --since=90s api
docker compose logs --since=90s dashboard
docker compose logs --since=90s otelcollector

# Access dashboard
open http://localhost:3000/signin
```

**Note**: The app dashboard is already running per `.cursor/rules/general.mdc`. Do not run `bun dev` or `bun run build`.

## Code Architecture

### Core SDK Structure

The AgentOps SDK is organized into several key areas:

**`agentops/`**
- `__init__.py` - Public API, init() function, thread-safe client management
- `client/` - HTTP client and API communication (api/, http/)
- `instrumentation/providers/` - LLM provider integrations (OpenAI, Anthropic, Google, etc.)
- `integration/` - Framework integrations (LangChain callbacks, DSPy, etc.)
- `sdk/` - Core tracing and decorator system
  - `sdk/decorators/` - @session, @agent, @operation, @workflow, @task decorators
  - `sdk/core.py` - Tracing infrastructure using OpenTelemetry
  - `sdk/processors.py` - Data processing and export
- `semconv/` - OpenTelemetry semantic conventions for AI/ML workflows
- `legacy/` - Backward compatibility layer (v3.x)

### Provider Integration Pattern

Each LLM provider follows a consistent pattern in `agentops/instrumentation/providers/<provider>/`:

1. **`instrumentor.py`** - OpenTelemetry instrumentation hook
2. **`wrappers/`** - Wrapper classes for provider SDK methods
3. **`config.py`** - Provider-specific configuration
4. **`attributes.py`** - Provider-specific attributes
5. **`utils.py`** - Helper utilities

All providers inherit from `BaseProvider` and implement:
- `handle_response()` - Process LLM responses
- `override()` - Patch provider methods
- `undo_override()` - Restore original methods

### Testing Structure

**`tests/`**
- `unit/` - Fast unit tests (default pytest path)
- `integration/` - Integration tests (require API keys)
- `smoke/` - Basic smoke tests
- `benchmark/` - Performance tests
- `core_manual_tests/` - Manual testing (not run in CI)
- `fixtures/` - Shared test fixtures
- `cassettes/` - VCR-recorded HTTP interactions

### Examples Structure

**`examples/`** - Jupyter notebooks and Python scripts demonstrating integrations:
- Framework examples: `ag2/`, `crewai/`, `autogen/`, `langchain/`, `llamaindex/`
- Provider examples: `openai/`, `anthropic/`, `google_genai/`
- LiteLLM examples: `litellm/`
- OpenAI Agents SDK: `openai_agents/`

Each example includes validation using `agentops.validate_trace_spans()`.

## Key Integration Points

### OpenTelemetry Integration

The SDK uses OpenTelemetry for distributed tracing:
- **Tracer**: `agentops.sdk.core.tracer`
- **Spans**: Session, Agent, Workflow, Operation, Task spans
- **Context**: Thread-local trace context via `TraceContext`
- **Exporters**: HTTP OTLP exporter to AgentOps backend

### Decorator System

Decorators create span hierarchies automatically:
```python
@session          # Root span
  @agent          # Agent span
    @operation    # Operation span
      @task       # Task span
```

All decorators support:
- Async/await functions
- Generator functions
- Exception handling
- Custom attributes

### Provider Instrumentation

Providers use wrappers to intercept LLM calls:
1. Import provider module → Instrumentor patches methods
2. LLM call → Wrapper captures request/response
3. Event created → Processed and exported to AgentOps
4. Token usage, costs, errors tracked automatically

## Self-Hosting Architecture

**`app/`** contains the complete self-hosted platform:
- `api/` - FastAPI backend (authentication, billing, data processing)
- `dashboard/` - Next.js frontend (visualization, management)
- `landing/` - Marketing website
- `clickhouse/` - Analytics database migrations
- `supabase/` - Authentication and primary database

Docker Compose stack includes:
- API server
- Dashboard
- OpenTelemetry Collector
- ClickHouse
- Supabase

### Local Development Workflow

```bash
# In app/ directory
supabase start  # Start local Supabase
docker compose up -d  # Start all services

# Generate test trace
AGENTOPS_API_KEY=<key> \
AGENTOPS_API_ENDPOINT=http://localhost:8000 \
AGENTOPS_APP_URL=http://localhost:3000 \
AGENTOPS_EXPORTER_ENDPOINT=http://localhost:4318/v1/traces \
OPENAI_API_KEY=<openai_key> \
python examples/openai/openai_example_sync.py

# Verify in dashboard
open http://localhost:3000/traces?trace_id=<printed_id>
```

## Cursor Rules (Important)

**`app/dashboard/.cursor/rules/general.mdc`**
- Excludes running the app: "No need to run the app. It's already up."

**`app/dashboard/.cursor/rules/design.mdc`**
- Typography: Figtree (UI), Menlo (code)
- Colors: Primary font rgba(20,27,52,1), Secondary rgba(20,27,52,0.74)
- Success: rgba(75,196,152,1), Error: rgba(230,90,126,1)

## Environment Variables

### For SDK Development
```bash
AGENTOPS_API_KEY=<your_api_key>
OPENAI_API_KEY=<openai_key>
ANTHROPIC_API_KEY=<anthropic_key>
```

### For Self-Hosting
```bash
# In app/.env
NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_URL=http://127.0.0.1:54321
CLICKHOUSE_HOST=127.0.0.1
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=password
PROTOCOL=http
```

## Python Version Support

- Minimum: Python 3.9
- Tested: 3.9, 3.10, 3.11, 3.12, 3.13
- Dependencies use version constraints based on Python version
- OpenTelemetry versions vary by Python version

## Development Notes

- **Build System**: hatchling (configured in pyproject.toml)
- **Linting**: ruff (not black) with 120 character line length
- **Testing**: pytest with async support, VCR cassettes for HTTP
- **Pre-commit**: ruff + ruff-format (excludes app/ directory)
- **Type Checking**: mypy for static type validation
- **Concurrency**: Thread-safe client using double-checked locking