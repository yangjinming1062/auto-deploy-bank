# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tanuki.py is a Python library that enables building LLM-powered applications with automatic model distillation for cost and latency optimization. Key features:
- Decorator-based API (`@tanuki.patch`, `@tanuki.align`)
- Type-aware output validation via Pydantic
- Automatic model distillation (GPT-4 → GPT-3.5) for ~90% cost reduction
- Multiple LLM provider support (OpenAI, AWS Bedrock, Together AI, Anyscale)
- RAG support with embedding outputs

## Commands

```bash
# Installation
pip install -e .                                    # Base install
pip install -r dev.requirements.txt                # With dev deps
pip install -e ".[aws_bedrock]"                    # AWS Bedrock support
pip install -e ".[together_ai]"                    # Together AI support

# Testing
pytest tests/                                       # All tests
pytest tests/test_patch/                            # Specific directory

# Code quality
black src/tanuki/                                   # Format code (line-length: 88)

# Building
python3 -m build                                    # Build distribution
```

## Architecture

### Core Concepts

** `@tanuki.patch` decorator**: Converts a function stub into an LLM-powered function with typed outputs. Key configuration options:
- `teacher_models`: Override default teacher models (GPT-4)
- `student_model`: Override default student model (GPT-3.5-turbo-1106)
- `ignore_finetuning`: Always use teacher model
- `ignore_data_storage`: Skip data collection for lower latency
- `generation_params`: LLM generation parameters

** `@tanuki.align` decorator**: Registers expected input-output pairs (Test-Driven Alignment) via `assert` statements. Align functions must be executed at least once before patched functions.

### Data Flow

```
User Function (patched)
    ↓
Register.load_function_description()
    ↓
Validator (type validation via Pydantic)
    ↓
LanguageModelManager (routes to provider)
    ├── OpenAI_API
    ├── AWS_Bedrock_API
    ├── TogetherAI_API
    └── Anyscale_API
    ↓
FunctionModeler (manages alignment & distillation)
    ↓
Trackers → Persistence Layer (Filesystem/Redis/S3 + Bloom filter)
```

### Key Modules

| Path | Purpose |
|------|---------|
| `src/tanuki/__init__.py` | Public API, `@patch`/`@align` decorators |
| `src/tanuki/function_modeler.py` | Core function modeling, alignment storage |
| `src/tanuki/validator.py` | Type validation for inputs/outputs |
| `src/tanuki/register.py` | Function registration |
| `src/tanuki/language_models/` | LLM provider integrations |
| `src/tanuki/models/` | Data models (Pydantic) |
| `src/tanuki/trackers/` | Data tracking and logging |
| `src/tanuki/persistence/` | Storage layer (Filesystem, Redis, S3) |

### Persistence

Alignment data is stored in `.align/` directory:
- Format: JSONL files named by function hash
- Datasets: `PATCHES`, `SYMBOLIC_ALIGNMENTS`, `POSITIVE_EMBEDDABLE_ALIGNMENTS`, `NEGATIVE_EMBEDDABLE_ALIGNMENTS`
- Bloom filter deduplication (10,000 items, 1% false positive rate)

### Supported Providers

- **OpenAI**: GPT-4, GPT-3.5-turbo (primary, with finetuning)
- **AWS Bedrock**: Llama, Claude, Titan
- **Together AI**: Various open-source models
- **Anyscale**: Managed model serving

## Type System

Use Python type hints with Pydantic for complex constraints:
```python
@dataclass
class ActionItem:
    goal: str = Field(description="What task must be completed")
    deadline: datetime = Field(description="Due date")

@tanuki.patch
def action_items(input: str) -> List[ActionItem]:
    """Generate action items"""

@tanuki.align
def align_action_items():
    assert action_items("Get presentation ready by Tuesday") == [...]
```

## Testing Patterns

Tests use pytest. Align functions serve as both tests and training data:
```python
@tanuki.align
def align_classify_sentiment():
    assert classify_sentiment("I love you") == 'Good'
    assert classify_sentiment("I hate you") == 'Bad'

# Can also run as pytest tests
def test_classify_sentiment():
    assert classify_sentiment("I like you") >= 7
```

## Environment Variables

- `OPENAI_API_KEY`: Required for OpenAI provider
- `TANUKI_LOG_DIR`: Directory for alignment logs (default: `.align/`)

## Distillation Process

1. Collect alignment examples from `@align` functions and runtime executions
2. After ~200 executions (configurable), trigger finetuning
3. Train GPT-3.5 student on GPT-4 teacher outputs
4. Switch to distilled model for faster/cheaper inference