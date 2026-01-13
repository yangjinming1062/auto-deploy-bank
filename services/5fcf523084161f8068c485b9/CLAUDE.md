# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RagaAI Catalyst is a comprehensive platform for managing and optimizing LLM projects. It provides:
- Project and dataset management
- Evaluation framework with metrics (Faithfulness, Hallucination, etc.)
- Tracing for RAG and agentic applications
- Prompt management
- Synthetic data generation
- Guardrail management for deployment
- Red-teaming for security testing

## Common Development Commands

### Setup Environment
```bash
# Create conda environment for testing
conda env create -f tests/environment.yml
conda activate ragaai_pytest_env

# Install package in development mode with dev dependencies
pip install -e ".[dev]"
```

### Code Quality (Ruff)
```bash
# Format code
ruff format .

# Lint with auto-fix
ruff check --fix .
```

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run single test file
pytest tests/test_specific_module.py -v

# Run tests with coverage
pytest tests/ --cov=ragaai_catalyst

# Run and generate formatted test report
python tests/run_pytest_and_print_and_save_results.py
```

### Installation
```bash
# Production install
pip install ragaai-catalyst
```

## Package Architecture

### Main Package Structure
```
ragaai_catalyst/
├── __init__.py              # Public API exports
├── ragaai_catalyst.py       # Core RagaAICatalyst class
├── dataset.py               # Dataset management
├── evaluation.py            # Evaluation framework
├── prompt_manager.py        # Prompt management
├── synthetic_data_generation.py  # Synthetic data generation
├── guardrails_manager.py    # Guardrail management
├── guard_executor.py        # Guardrail execution
├── redteaming/              # Security testing module
│   ├── red_teaming.py       # Main red-teaming interface
│   ├── data_generator/      # Test case and scenario generation
│   ├── utils/               # Utilities and detectors
│   └── config/              # Configuration files
└── tracers/                 # Tracing infrastructure
    ├── agentic_tracing/     # Agentic application tracing
    ├── instrumentators/     # Auto-instrumentation for frameworks
    └── utils/               # Tracing utilities
```

### Key Components

**Core Classes** (from `ragaai_catalyst/__init__.py`):
- `RagaAICatalyst` - Main client class with authentication
- `Dataset` - Dataset management for projects
- `Evaluation` - Evaluation framework for RAG applications
- `PromptManager` - Prompt version management
- `Tracer` - Trace recording for applications
- `GuardrailsManager` - Deployment guardrail configuration
- `GuardExecutor` - Runtime guardrail execution
- `RedTeaming` - Security vulnerability testing

**Tracing System**:
- Auto-instrumentation via `init_tracing()` for frameworks like:
  - LangChain, LangGraph
  - LlamaIndex
  - CrewAI
  - Haystack
  - OpenAI Agents SDK
  - SmolAgents
- Manual tracing with `trace_agent`, `trace_llm`, `trace_tool` decorators
- Custom tracing via `trace_custom()`

## Configuration

### Authentication
All operations require RagaAI Catalyst credentials. Set these environment variables:
```bash
RAGAAI_CATALYST_BASE_URL=https://catalyst.raga.ai/api
RAGAAI_CATALYST_ACCESS_KEY=your_access_key
RAGAAI_CATALYST_SECRET_KEY=your_secret_key
```

Or pass directly to `RagaAICatalyst`:
```python
catalyst = RagaAICatalyst(
    access_key="YOUR_ACCESS_KEY",
    secret_key="YOUR_SECRET_KEY",
    base_url="BASE_URL"
)
```

### Test Environment
Tests require API keys for multiple providers. See `tests/README.md` for the complete `.env` template with keys for:
- OpenAI, Anthropic, Groq, Azure OpenAI
- Google/Gemini, Vertex AI
- RagaAI Catalyst
- Third-party APIs (Tavily, SerperDev)

## Examples

The `examples/` directory contains integrations for major LLM frameworks:
- `langchain/` - Medical RAG example
- `llamaindex_examples/` - Legal research RAG
- `crewai/scifi_writer/` - Multi-agent writing
- `haystack/news_fetching/` - Document processing
- `langgraph/personal_research_assistant/` - Agent workflows
- `openai_agents_sdk/` - Email extraction and YouTube summarization
- `smolagents/most_upvoted_paper/` - Paper discovery
- `custom_agents/travel_agent/` - Custom agent implementation

## Testing Strategy

Tests are in the `tests/` directory and include:
- Unit tests for core components
- Integration tests for key workflows
- Multi-provider LLM testing
- Example validation

Test execution uses:
- `pytest` for test runner
- `pytest-cov` for coverage
- Custom reporting via `tests/run_pytest_and_print_and_save_results.py`

CI runs on Python 3.10-3.13 across Ubuntu, Windows, and macOS.

## Build System

Project uses `pyproject.toml` with:
- `setuptools` as build backend
- `ruff` for formatting and linting (not `black`/`isort`/`flake8`)
- `pytest` for testing
- Python 3.10-3.13.2 support

## Key Implementation Notes

### Version Management
The package uses `setuptools_scm` for version management. The actual version file at `ragaai_catalyst/_version.py` is auto-generated and should not be manually edited.

### Red-teaming Module
Located in `ragaai_catalyst/redteaming/`, this provides:
- Built-in detectors (harmful content, stereotypes, bias)
- Custom detector support
- Automatic test case generation
- Multi-provider LLM support (OpenAI, XAI/Groq, etc.)

### Configuration Files
- `ragaai_catalyst/redteaming/config/detectors.toml` - Detector configurations
- `tests/environment.yml` - Conda test environment
- Various `.toml` files in tracing utils for provider configurations

## Development Workflow

1. Install development dependencies: `pip install -e ".[dev]"`
2. Run code formatting and linting: `ruff format . && ruff check --fix .`
3. Write/update tests for new functionality
4. Run tests: `pytest tests/ -v`
5. Test against multiple Python versions (CI will verify)
6. Update documentation (README.md, docstrings) as needed

## Framework Integration Points

The package integrates with major LLM frameworks through:
- **Auto-instrumentation**: Call `init_tracing(catalyst, tracer)` after framework initialization
- **Manual decorators**: Use `@trace_agent`, `@trace_llm`, `@trace_tool` on functions
- **Callback systems**: Some integrations use framework-specific callbacks (e.g., LangChain callbacks)
- **OpenTelemetry**: Agentic tracing uses OpenTelemetry for distributed tracing