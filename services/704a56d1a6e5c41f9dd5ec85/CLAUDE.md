# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LazyLLM is a low-code development tool for building multi-agent LLM applications. It follows a **prototype building -> data feedback -> iterative optimization** workflow, allowing developers to create complex AI applications at low cost.

## Common Commands

### Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install all dependencies (for finetuning, deployment, RAG)
pip install -r requirements.full.txt

# Install via pip
pip3 install lazyllm

# Install all dependencies after pip install
lazyllm install full
```

### Building and Linting

```bash
# Build package
poetry build

# Run linter
flake8 .

# Check requirements sync
python scripts/check_requirements.py
```

### Testing

```bash
# Run basic tests
python -m pytest tests/basic_tests/ -v

# Run all tests with coverage
python -m pytest tests/ --cov=lazyllm --cov-report=html -v

# Run specific test suite
python -m pytest tests/advanced_tests/standard_test/ -v
python -m pytest tests/advanced_tests/full_test/ -v
python -m pytest tests/charge_tests/ -v
python -m pytest tests/doc_check/ -v

# Run single test file
python -m pytest tests/basic_tests/test_module.py -v

# Run with reruns and last-failed tracking
python -m pytest --lf --last-failed-no-failures=all --durations=0 --reruns=2 -v
```

### CLI Commands

```bash
# Quick chatbot with online model
lazyllm run chatbot

# Chatbot with specific model
lazyllm run chatbot --model=internlm2-chat-7b
lazyllm run chatbot --model=gpt-4 --source=openai

# RAG application
lazyllm run rag --documents=/path/to/documents
lazyllm run rag --documents=/path/to/documents --model=internlm2-chat-7b

# Services
lazyllm run training_service
lazyllm run infer_service

# Deploy model
lazyllm deploy modelname

# Install packages
lazyllm install full
lazyllm install standard
lazyllm install package_name

# MCP Server
lazyllm deploy mcp_server <command> [args]
```

## Architecture

LazyLLM uses a layered architecture with four main abstractions:

### 1. **Components** (`lazyllm/components/`)
Smallest execution units that can be functions or bash commands. Categories include:
- **finetune/**: Fine-tuning components (collie, peft)
- **deploy/**: Deployment components (vllm, lightllm, lmdeploy)
- **validate/**: Validation components
- **prompter/**: Prompt formatting (ChatPrompter, AlpacaPrompter)
- **formatter/**: Output formatting (JsonFormatter, FileFormatter)
- **text_to_speech/**: TTS components (ChatTTS)
- **speech_to_text/**: STT components (SenseVoice)
- **stable_diffusion/**: Image generation
- **embedding/**: Embedding models

### 2. **Modules** (`lazyllm/module/`)
Top-level components with four key capabilities: training, deployment, inference, evaluation.

Key module types:
- **TrainableModule**: Trainable models (internlm2-chat-7b, etc.)
- **OnlineChatModule**: Online LLM services (GPT, SenseNova, Kimi, etc.)
- **OnlineEmbeddingModule**: Online embedding services
- **ActionModule**: Wraps functions/modules/flows
- **UrlModule**: Wraps external URLs
- **ServerModule**: Wraps functions/flows as API services
- **WebModule**: Multi-round dialogue interface
- **TrialModule**: Model evaluation

### 3. **Flow** (`lazyllm/flow/`)
Defines data stream between callable objects. Enables building complex applications by composing modules.

Flow types:
- **pipeline()**: Sequential execution
- **parallel()**: Parallel execution with sum/group
- **diverter()**: Branching control
- **warp()**: Wraps modules for parallel execution
- **ifs()**: Conditional execution
- **loop()**: Iteration control

Example flow usage:
```python
with pipeline() as ppl:
    ppl.llm = TrainableModule('model')
    ppl.output = ppl.llm | formatter

with parallel().sum as ppl.prl:
    prl.retriever1 = Retriever(documents, ...)
    prl.retriever2 = Retriever(documents, ...)
```

### 4. **Launchers** (`lazyllm/launcher.py`)
Execute components across different platforms:
- **EmptyLauncher**: Local execution (bare metal, dev machines)
- **RemoteLauncher**: Remote execution (Slurm, SenseCore)
- **ScoLauncher**: SenseCore cloud execution

### Engine System (`lazyllm/engine/`)
- **LightEngine**: Graph-based execution engine for running nodes and edges
- **node.py**: Node representation and management
- **scripts/**: Execution scripts for various platforms

### Tools (`lazyllm/tools/`)
High-level tools for common AI tasks:
- **rag/**: RAG components (Document, Retriever, Reranker, SentenceSplitter)
- **agent/**: Agent implementations (FunctionCallAgent, ReactAgent, PlanAndSolveAgent, ReWOOAgent)
- **eval/**: Evaluation tools
- **services/**: Inference and training services
- **mcp/**: Model Context Protocol integration
- **webpages/**: Web interface components

## Key Files

- `lazyllm/__init__.py`: Main exports and package initialization
- `lazyllm/configs.py`: Configuration management
- `lazyllm/launcher.py`: Cross-platform execution system
- `pyproject.toml`: Dependencies and build configuration (Poetry)
- `.flake8`: Linting rules (max line length 121, complexity 12)

## Testing Structure

Tests are organized into suites:
- **basic_tests/**: Core functionality tests
- **advanced_tests/standard_test/**: Standard advanced features
- **advanced_tests/full_test/**: Full feature set with optional deps
- **charge_tests/**: Load and performance tests
- **doc_check/**: Documentation and API tests

## Environment Variables

Key environment variables:
- `LAZYLLM_SCO_ENV_NAME=lazyllm`: SenseCore environment
- `LAZYLLM_DEFAULT_LAUNCHER=sco`: Default launcher type
- `LAZYLLM_DATA_PATH`: Path to data directory
- `LAZYLLM_MODEL_PATH`: Path to model directory
- `LAZYLLM_HOME`: LazyLLM home directory
- `LAZYLLM_OPENAI_API_KEY`: OpenAI API key
- `LAZYLLM_ON_CLOUDPICKLE`: Enable cloudpickle serialization

## Configuration

Configuration is managed via `lazyllm/configs.py` with a `config.done()` pattern. Config files are stored in `~/.lazyllm/config.json`.

## Development Notes

- **Package manager**: Poetry (see pyproject.toml)
- **Python version**: ^3.10
- **Max line length**: 121 characters
- **Max complexity**: 12
- **CI requires 'lint_pass' label** before running full test suite
- **Test isolation**: Tests use pytest fixtures and conftest.py
- **Documentation**: See README.md and docs/ directory