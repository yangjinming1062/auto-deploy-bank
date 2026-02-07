# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DataDreamer is a Python library for prompting, synthetic data generation, and training workflows. It provides a session-based context manager architecture where `Step` and `Trainer` objects transform data within a `DataDreamer` session context.

## Common Commands

```bash
# Lint the project (uses ruff)
./scripts/lint.sh

# Format the project
./scripts/format.sh

# Run tests
./scripts/run.sh --maxfail=25 --durations=0

# Run a specific test file
pytest src/tests/test_datadreamer.py -v

# Run a specific test
pytest src/tests/test_datadreamer.py::test_specific_test -v
```

## Architecture

### Session-Based Workflow
The core pattern uses a `DataDreamer` context manager:
```python
from datadreamer import DataDreamer

with DataDreamer('./output/'):
    # Run steps and trainers here
    # Results are automatically cached and saved
```

### Core Modules

**`src/steps/`** - Data transformation steps that produce output datasets. Key base classes:
- `Step` - Base class for all steps
- `DataSource` - Initial data sources (HFHubDataSource, HFDatasetDataSource, JSONDataSource, etc.)
- `Prompt`, `RAGPrompt`, `FewShotPrompt` - LLM prompting steps
- `Embed`, `Retrieve`, `CosineSimilarity` - NLP task steps

**`src/llms/`** - LLM integrations including OpenAI, Anthropic, HuggingFace, vLLM, LiteLLM wrappers, and more. Base class `LLM` handles caching and common LLM operations.

**`src/trainers/`** - Model training workflows (Supervised Fine-tuning, DPO, PPO, Reward Modeling, etc.)

**`src/datasets/`** - Custom dataset classes wrapping HuggingFace datasets with caching and DataDreamer-specific functionality.

**`src/utils/`** - Utilities for HuggingFace models, training, distributed computing, background processes, and caching.

### Caching Pattern
DataDreamer uses aggressive caching via `SqliteDict` and `FileLock`. The `_Cachable` base class in `src/_cachable/` provides the caching infrastructure. Steps cache outputs to disk and resume from cached state on re-run.

### Key Design Patterns

1. **Step outputs**: Steps produce `OutputDataset` or `OutputIterableDataset` accessible via `step.output['column_name']`
2. **Parallel execution**: Use `concurrent()` and `wait()` from `src/steps/step_background.py` for parallel step execution
3. **Data cards**: Call `step.data_card()` to generate reproducibility metadata
4. **Publishing**: Use `step.publish_to_hf_hub()` to publish datasets to HuggingFace Hub

## Dependencies

- Python 3.10-3.13
- Core: `datasets`, `transformers`, `huggingface-hub`, `openai`, `litellm`, `trl`, `peft`, `accelerate`, `optimum`
- Dev: `pytest`, `pytest-cov`, `mypy`, `ruff` (linting), `Sphinx` (docs)