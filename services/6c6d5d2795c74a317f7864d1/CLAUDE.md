# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Outlines is a Python library for **structured generation with Large Language Models (LLMs)**. It guarantees structured outputs during generation by constraining model outputs according to specified schemas, types, or patterns. The library works with 17+ different model providers including OpenAI, Anthropic, vLLM, Ollama, transformers, and more.

**Key principle**: Instead of post-processing unconstrained outputs, Outlines enforces structure during generation via logits processors.

## Architecture

The codebase follows a clean separation of concerns with six main components:

### 1. Models (`outlines/models/`)
**17 model integrations** grouped by provider:
- **API-based models**: `anthropic.py`, `openai.py`, `gemini.py`, `mistral.py`, `dottxt.py`
- **Local models**: `transformers.py`, `llamacpp.py`, `mlxlm.py`
- **Server models**: `vllm.py`, `tgi.py`, `ollama.py`, `sglang.py`
- **Offline**: `vllm_offline.py`

Each model implements either:
- `SteerableModel` - Fully controllable (transformers, llamacpp, mlxlm)
- `BlackBoxModel` - API-based (OpenAI, Anthropic, etc.)
- `AsyncBlackBoxModel` - Asynchronous variants

**Entry point**: `from_transformers()`, `from_openai()`, `from_vllm()`, etc.

### 2. Backends (`outlines/backends/`)
**Three backend implementations** that compile output types into logits processors:
- **outlines_core** (default for JSON/Regex) - Fast, Rust-based
- **xgrammar** - Alternative implementation
- **llguidance** (default for CFG) - Python-based

Backends translate type specifications (Regex, CFG, JsonSchema) into sequences of allowed tokens that guide generation.

### 3. Types (`outlines/types/`)
**Structured output specifications** built on a Domain-Specific Language (DSL):
- **Regex** - Pattern matching (email, UUID, IPv4, etc.)
- **CFG** - Context-free grammars for complex structures
- **JsonSchema** - JSON schema validation
- **Choice** - Enumerated values (Literal types)

**Built-in types**: `string`, `integer`, `boolean`, `number`, `date`, `time`, `email`, `isbn`, etc.
**DSL helpers**: `optional()`, `either()`, `exactly()`, `at_least()`, `one_or_more()`, etc.

### 4. Generator (`outlines/generator.py`)
**Orchestration layer** that:
- Combines a model + output type into a reusable generator
- Provides `generate()`, `batch()`, `stream()`, `astream()` methods
- Handles both steerable and black-box models uniformly

### 5. Templates (`outlines/templates.py`)
**Jinja2-based prompt templating**:
- Separate prompt logic from code
- Supports multi-modal inputs (text, images, audio, video)
- Variables: `{{ variable_name }}`
- File-based templates via `Template.from_file()`

### 6. Applications (`outlines/applications.py`)
**Encapsulated patterns** that combine templates + types into reusable functions for common use cases.

## Common Development Tasks

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=outlines

# Run specific test file
pytest tests/test_generator.py

# Run with verbose output
pytest -v

# Run GPU tests (if available)
pytest --gpu  # or use test-gpu extra
```

### Code Quality
```bash
# Lint with ruff
ruff check outlines/

# Format with ruff
ruff format outlines/

# Type check with mypy
mypy outlines/

# Run pre-commit on all files
pre-commit run --all-files

# Install pre-commit hooks
pre-commit install
```

### Building & Installation
```bash
# Development install
pip install -e .

# Install with all extras
pip install "outlines[transformers,openai,anthropic,vllm,llamacpp]"

# Build package
python -m build
```

### Documentation
```bash
# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build

# Generate API reference
python scripts/gen_ref_pages.py
```

## Key Files

- `outlines/__init__.py` - Main API exports
- `outlines/generator.py` - Generator orchestration logic
- `outlines/backends/__init__.py` - Backend selection and routing
- `outlines/models/__init__.py` - Model provider integrations
- `outlines/types/__init__.py` - Output type system
- `pyproject.toml` - Dependencies, build config, pytest, mypy, coverage
- `.pre-commit-config.yaml` - Pre-commit hooks (ruff, mypy)
- `tests/` - Test suite structure mirrors main code

## Output Type System

Outlines supports multiple ways to specify structured outputs:

1. **Python types**: `int`, `str`, `bool`, `Literal["Yes", "No"]`
2. **Pydantic models**: Full JSON schema generation
3. **Regex patterns**: `outlines.regex(r"\d+")`
4. **Context-free grammars**: `outlines.cfg("""
    start -> "yes" | "no"
""")`
5. **Function signatures**: Automatic parameter extraction
6. **Built-in types**: `outlines.email`, `outlines.uuid4`, etc.

## Model Integration Pattern

Each model provider follows a consistent pattern:
```python
# Define model
model = outlines.from_transformers(
    AutoModelForCausalLM.from_pretrained(...),
    AutoTokenizer.from_pretrained(...)
)

# Use with output type
result = model(prompt, output_type, max_new_tokens=200)
```

## Important Notes

- **Backend selection**: Automatically chooses best backend for output type, but can be overridden with `backend="xgrammar"`
- **Caching**: Results cached in `outlines/caching.py` - clear with `outlines.clear_cache()`
- **Multi-modal**: `Vision`, `Audio`, `Video`, `Image` classes in `outlines/inputs.py`
- **Async support**: All API-based models have async variants (prefixed with `Async`)
- **Python version**: Supports Python 3.9-3.12
- **GPU testing**: Some tests require GPU or specific platforms (see `pyproject.toml` coverage omit list)

## Testing Strategy

Tests follow a **feature-based structure**:
- `test_generator.py` - Core generator logic
- `test_templates.py` - Prompt templating
- `test_cache.py` - Caching behavior
- `test_applications.py` - Encapsulated patterns
- `test_inputs.py` - Multi-modal inputs

**Platform-specific tests** are omitted from coverage (see `pyproject.toml` coverage settings).

## Dependencies

**Core dependencies**:
- `pydantic>=2.0` - Schema validation
- `jinja2` - Template engine
- `outlines_core==0.2.11` - Rust-based logits processing

**Optional extras** (install as needed):
- `transformers` - HuggingFace models
- `openai`, `anthropic`, `mistralai`, `gemini` - API providers
- `vllm`, `tgi`, `ollama`, `sglang` - Server backends
- `llama-cpp-python`, `mlx-lm` - Local inference
- `pytest`, `pytest-cov` - Testing
- `ruff`, `mypy` - Code quality