# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Setup
```bash
# Install dev dependencies
pip install -r dev-requirements.txt

# Enable pre-commit hooks
pre-commit install
```

### Code Quality
```bash
# Run all pre-commit checks
pre-commit run --all-files

# Format code with black
tox -e black -- <files>

# Lint with ruff (auto-fix mode)
tox -e ruff -- check --force-exclude --fix
```

### Testing
```bash
# Run all tests (requires deployment.json)
pytest

# Run only changed samples
pytest --changelog

# Run a specific test file
pytest scenarios/projects/basic/test_basic_import.py
```

**Note:** Most tests require a `deployment.json` file in the root directory, which is the output of running `az deployment sub create -o json`. This file is gitignored.

## Repository Structure

This is a **sample repository** demonstrating Azure AI scenarios, not a library. Samples are organized by scenario type under `scenarios/`:

| Scenario | Purpose |
|----------|---------|
| `Agents` | Azure AI Agent Service with tools, threads, and runs |
| `Assistants` | Assistant API patterns (function calling, multi-agent) |
| `GPT-4V` | Vision/multimodal capabilities |
| `evaluate` | AI judge evaluators, RAG evaluation, simulators |
| `agent-tracing` | Tracing integration (LangChain, LangGraph, OpenAI Agents) |
| `rag` | Retrieval Augmented Generation patterns |
| `langchain` / `llama-index` | Framework integrations |
| `model-catalog` | Model deployment and usage patterns |

Each scenario contains multiple samples. Each sample is self-contained with its own `requirements.txt` or `pyproject.toml`.

## Sample Conventions

When creating new samples:
1. Create a separate directory under the appropriate scenario
2. Include a `README.md` using the template at `.infra/templates/README-template.md`
3. For Python samples, use Jupyter notebooks from `.infra/templates/template.ipynb`
4. Add YAML frontmatter to README for discoverability:
```yaml
---
page_type: sample
languages:
- python
products:
- azure-openai
description: Brief description.
---
```

## Code Standards

- **Formatter**: Black (line-length: 120)
- **Linter**: Ruff with extensive rule set (B, C4, PT, RET, SIM, ARG, PTH, RUF, PLE, ANN)
- **Notebooks**: Use `nb-clean` to strip outputs/metadata before committing
- **Secrets**: Custom hook detects Azure secrets; use empty string placeholders:
```python
os.environ["AZURE_SUBSCRIPTION_ID"] = ""  # Avoids secret detection
```

## Testing Infrastructure

Custom pytest fixtures in `conftest.py`:
- `deployment_outputs`: Loads Azure deployment outputs from `deployment.json`
- `azure_ai_project`: Dictionary with subscription_id, resource_group_name, project_name
- `azure_ai_project_connection_string`: Formatted connection string for SDK clients
- `azure_openai_endpoint` / `azure_openai_gpt4_deployment`: OpenAI resource details

A custom pytest plugin (`.infra/pytest_plugins/changed_samples`) enables running only changed samples via `--changelog` flag.