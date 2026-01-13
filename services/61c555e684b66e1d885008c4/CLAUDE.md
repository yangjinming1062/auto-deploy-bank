# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Llama Cookbook** - Official Meta companion project for Llama model family (Llama 2, 3, 3.1, 3.2, 3.3, and 4). This repository provides examples, tutorials, and utilities for:
- Fine-tuning Llama models (PEFT, LoRA, full fine-tuning)
- Inference (local and cloud providers)
- RAG (Retrieval-Augmented Generation) applications
- End-to-end use cases (agents, chatbots, code assistants)
- Third-party platform integrations

This is **both a library and documentation repository**. The `src/` directory contains the core Python package, while `getting-started/`, `end-to-end-use-cases/`, and `3p-integrations/` provide comprehensive examples and tutorials.

## Repository Architecture

This repository is organized into **four main sections**:

### 1. `src/llama_cookbook/` - Core Library
Main Python package providing utilities for Llama development:
- **`finetuning.py`** - Primary fine-tuning orchestration script (main entry point)
- **`inference/`** - Core inference utilities:
  - `llm.py` - Main LLM wrapper class
  - `model_utils.py` - Model loading and utilities
  - `chat_utils.py` - Chat completion utilities
  - `checkpoint_converter_fsdp_hf.py` - FSDP to HF checkpoint conversion
- **`utils/`** - Training utilities:
  - `train_utils.py` - Training loop utilities
  - `dataset_utils.py` - Dataset preparation
  - `fsdp_utils.py` - FSDP (Fully Sharded Data Parallel) utilities
  - `config_utils.py` - Configuration management
- **`data/`** - Data processing:
  - `sampler.py` - Data sampling utilities
  - `concatenator.py` - Data concatenation
  - `llama_guard/` - Llama Guard safety tools
- **`tools/`** - Utility scripts:
  - `convert_hf_weights_to_llama.py` - Weight conversion
  - `compare_llama_weights.py` - Weight comparison
- **`model_checkpointing/`** - Model checkpoint management

### 2. `getting-started/` - Tutorials and Reference
Jupyter notebooks and documentation for core features:
- **`build_with_llama_api.ipynb`** - Llama API integration (latest Llama 4)
- **`build_with_llama_4.ipynb`** - Llama 4 (5M context with Scout model)
- **`finetuning/`** - Fine-tuning guides (supervised, PEFT, LoRA, vision)
- **`inference/`** - Local and API inference examples
- **`responsible_ai/`** - Safety tools (Llama Guard, Prompt Guard)
- **`RAG/`** - Retrieval-Augmented Generation examples
- **`distillation/`** - Model distillation guides

### 3. `end-to-end-use-cases/` - Complete Applications
25+ fully functional applications:
- **Agents**: Calendar assistant, email agent, GitHub triage
- **Chatbots**: Customer service, WhatsApp Llama 4 bot
- **RAG Systems**: Contextual chunking, multimodal RAG, research paper analyzer
- **Benchmarks**: LLM eval harness, inference benchmarks (cloud/on-prem)
- **Multimodal**: NotebookLlama, book character mindmap
- **Code**: Coding assistant, text-to-SQL

Each use case has its own README with setup and usage instructions.

### 4. `3p-integrations/` - Platform Integrations
Third-party service integrations:
- **Cloud Providers**: AWS, Azure, GCP
- **Inference Platforms**: Groq, TogetherAI, Lamini
- **Frameworks**: LangChain, LlamaIndex
- **Serving**: vLLM, TGI, Modal
- **Groq Templates**: 8+ example templates (chatbots, RAG, function calling, SQL)

## Common Commands

### Development Setup

Install the package with all optional dependencies for development:
```bash
pip install -U pip setuptools
pip install --extra-index-url https://download.pytorch.org/whl/test/cu118 -e .[tests,auditnlg,vllm]
```

Install with tests only:
```bash
pip install --extra-index-url https://download.pytorch.org/whl/test/cu118 llama-cookbook[tests]
```

**Optional dependency groups** (from pyproject.toml):
- `tests`: pytest and test utilities
- `vllm`: vLLM integration
- `auditnlg`: Safety/sensitive topic checking
- `langchain`: LangChain integration

### Testing

Run all tests:
```bash
python -m pytest src/tests/
```

Run a specific test file:
```bash
python -m pytest src/tests/test_finetuning.py
```

Run a specific test by name:
```bash
python -m pytest src/tests/test_finetuning.py -k test_finetuning_peft
```

**Test markers**: `skip_missing_tokenizer` - skips tests requiring Hugging Face model access (run `huggingface-cli login` to unskip).

**CI tests** (GitHub Actions):
- CPU tests: `.github/workflows/pytest_cpu_gha_runner.yaml`
- Runs on ubuntu-24.04
- Triggered on pull requests to main branch
- Installs with `pip install --extra-index-url https://download.pytorch.org/whl/test/cu118 -e .[tests]`
- Test results published with JUnit XML

### Code Formatting

The project uses **black** for code formatting (already included in requirements.txt):
```bash
black <files>
```

### Building the Package

Uses hatchling build backend:
```bash
pip install -e .  # Editable install
python -m build  # Build distribution
```

## Key Dependencies

**Core requirements** (`requirements.txt`):
- PyTorch >= 2.2
- Transformers >= 4.45.1
- PEFT, LoRA, bitsandbytes for fine-tuning
- accelerate, datasets, sentence-transformers
- gradio, matplotlib for visualization

**Optional extras**:
- vllm: High-throughput inference
- auditnlg: Safety/sensitive topic checking
- langchain: LangChain integration
- tests: pytest and test utilities

**CUDA considerations**:
- Uses PyTorch CUDA 11.8 wheels (`cu118`) in CI
- Custom PyTorch wheel index: `https://download.pytorch.org/whl/test/cu118`
- H100 GPUs work better with CUDA >12.0
- Check `nvidia-smi` for your CUDA version

## Primary Entry Points

1. **Fine-tuning**: `src/llama_cookbook/finetuning.py`
   ```bash
   python src/llama_cookbook/finetuning.py <args>
   ```

2. **Interactive Tutorials**: Jupyter notebooks in `getting-started/`
   ```bash
   jupyter notebook getting-started/build_with_llama_api.ipynb
   ```

3. **Utility Scripts**: Located in `src/llama_cookbook/tools/`
   ```bash
   python src/llama_cookbook/tools/convert_hf_weights_to_llama.py <args>
   ```

## Model Support

Supports all Llama models from version 2 through 4:
- **Llama 2**: 7B, 13B, 70B variants
- **Llama 3/3.1/3.2/3.3**: 8B, 70B, instruct, vision, long context
- **Llama 4**: Scout (5M context), Maverick (latest features)

Check model compatibility in individual examples/use cases.

## Key Architectural Patterns

### Model Loading Pattern
Most examples follow this pattern:
1. Load model using `model_utils.py` utilities
2. Apply chat formatting via `prompt_format_utils.py`
3. Generate using `llm.py` or direct Transformers API

### Fine-tuning Pattern
Configuration-driven approach:
1. Use `finetuning.py` as the main entry point
2. Configure training parameters (PEFT, LoRA, full fine-tuning)
3. Load dataset using data utilities
4. Train and save checkpoints for inference

### RAG Pattern
Examples in `getting-started/RAG/` demonstrate:
1. Document loading and chunking
2. Embedding generation (sentence-transformers)
3. Vector database integration (FAISS, Qdrant, Pinecone)
4. Retrieval and generation

## Important Information

### Model Access
- Models available on Hugging Face: https://huggingface.co/meta-llama
- Models with `hf` suffix are already in Hugging Face format
- Original Meta weights require conversion using tools in `src/llama_cookbook/tools/`

### PyTorch Nightlies
To use PyTorch nightlies instead of stable release, follow: https://pytorch.org/get-started/locally/

### Recent Changes
- Repository refactored from `llama-recipes` to `llama-cookbook`
- Directory structure reorganized (see UPDATES.md for details)
- Archive branch available: `archive-main` (pre-refactor snapshot)

## Finding Examples

For specific tasks, search these locations:
- **Fine-tuning examples**: `getting-started/finetuning/` and `end-to-end-use-cases/`
- **Inference setup**: `getting-started/inference/` and `3p-integrations/`
- **RAG applications**: `getting-started/RAG/` and end-to-end RAG examples
- **Agents**: `end-to-end-use-cases/agents/`
- **Cloud deployment**: `3p-integrations/` (AWS, Azure, GCP, Modal)
- **Quick start**: `getting-started/build_with_llama_4.ipynb` or `getting-started/build_with_llama_api.ipynb`

## Testing and CI

- **Framework**: pytest
- **Location**: `src/tests/` (11 test files)
- **CI**: GitHub Actions workflow on ubuntu-24.04
  - Automated CPU testing on PRs
  - Spell-checking for documentation
- **Test Types**: Unit tests for fine-tuning, inference, datasets

## Development Guidelines

1. Clone and install from source with optional dependencies
2. Review `getting-started/` examples to understand patterns
3. Check `src/llama_cookbook/` for reusable utilities
4. Run tests before submitting PRs
5. Follow CONTRIBUTING.md guidelines
6. Add unit tests for new features in `src/tests/`
7. Complete Contributor License Agreement (CLA) for Meta projects
8. Use black for code formatting

## Jupyter Notebooks

Many examples are provided as Jupyter notebooks (`.ipynb` files). These are found in:
- `getting-started/`: Core tutorials
- `3p-integrations/`: Provider-specific examples
- `end-to-end-use-cases/`: Complex applications

Install with `black[jupyter]` to work with notebook formatting.

## Documentation

- **Main README**: `/home/ubuntu/deploy-projects/61c555e684b66e1d885008c4/README.md` - Overview and Llama 4 recipes
- **Contributing**: `/home/ubuntu/deploy-projects/61c555e684b66e1d885008c4/CONTRIBUTING.md` - Development guidelines
- **Section READMEs**: Each main directory has its own README
- **Jupyter Notebooks**: 50+ interactive tutorials and examples throughout

## Contributing

Follow CONTRIBUTING.md guidelines. Key points:
- Fork and create branch from `main`
- Add tests for new features
- Update documentation for API changes
- Ensure tests pass locally before PR
- Complete Contributor License Agreement (CLA)
- Use black for code formatting

This is a **Meta official repository** with strict contribution guidelines.

## Project Metadata

- **Package Name**: `llama-cookbook` (formerly `llama-recipes`)
- **Version**: `0.0.5.post1`
- **Python Version**: Requires Python 3.8+
- **Build System**: hatchling (modern Python build backend)
- **License**: Meta Llama License (varies by model version - see README.md for details)
- **Official Repository**: Meta's companion project for Llama model family
- **Primary Use Cases**:
  - Model fine-tuning (PEFT, LoRA, full fine-tuning)
  - Inference serving (local and cloud)
  - RAG applications
  - Multimodal applications
  - Agent systems

## Additional Important Notes

- Each example/use case may have **additional dependencies** - check individual READMEs
- Some tests require **Hugging Face login** for model access
- **Weights Conversion**: Use tools in `src/llama_cookbook/tools/` for model format conversions
- **RAG Examples**: Use `sentence_transformers` for embeddings (GPU recommended)
- **Vision Models**: Require PyTorch with CUDA support
- **Spell-check CI**: Documentation is automatically spell-checked via GitHub Actions