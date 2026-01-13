# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Reference

### Common Commands
```bash
# Install in development mode
pip install .[dev]

# Install from source (if building)
pip install .[dev]

# Run formatting and linting
pre-commit run --all-files

# Run unit tests
cd tests
pytest --color=yes --durations=0 --verbose -rF ./

# Run a specific test
pytest tests/test_pipeline.py -v
```

### Development Setup
```bash
# Install pre-commit hooks (required before commits)
pre-commit install

# Check formatting manually
pre-commit run --all-files
```

## High-Level Architecture

DeepSpeed Model Implementations for Inference (MII) is a high-throughput, low-latency LLM inference library that optimizes model serving through several key technologies: Blocked KV Caching, Continuous Batching, Dynamic SplitFuse, and High-Performance CUDA Kernels.

### Core Components

**API Layer** (`mii/api.py`)
- Entry points for users: `pipeline()`, `serve()`, and `client()`
- Handles configuration parsing and deployment orchestration
- `pipeline()` - non-persistent in-process inference
- `serve()` - persistent GRPC/REST server deployment
- `client()` - connect to persistent deployments

**Backend** (`mii/backend/`)
- `server.py` - GRPC server implementation for persistent deployments
- `client.py` - client for communicating with persistent deployments
- Handles model loading, inference execution, and response formatting

**Configuration** (`mii/config.py`)
- `ModelConfig` - model-specific settings (model path, task type, tensor parallelism)
- `MIIConfig` - deployment configuration (port, replicas, hostfile)
- `GenerateParamsConfig` - text generation parameters (max_new_tokens, temperature, top_p, etc.)
- Uses Pydantic for validation

**Batching** (`mii/batching/`)
- `MIIPipeline` and `MIIAsyncPipeline` - continuous batching implementation
- Ragged tensor handling for variable-length sequences
- Handles concurrent request processing

**Modeling** (`mii/modeling/`)
- `models.py` - model loading and initialization
- `tokenizers.py` - tokenizer wrapper with MII-specific handling
- Integrates with DeepSpeed-Inference for optimized execution

**GRPC & REST** (`mii/grpc_related/`)
- Protocol buffer definitions and server implementation
- RESTful API gateway for HTTP-based inference
- Supports both GRPC and REST protocols

**Legacy Support** (`mii/legacy/`)
- Deprecated APIs for backward compatibility
- Older model architectures and tasks
- Examples for BERT, RoBERTa, Stable Diffusion, etc.

### Key Technologies

**Tensor Parallelism**
- Split models across multiple GPUs using DeepSpeed's tensor parallelism
- Configured via `tensor_parallel` parameter
- Supports combining with replicas for maximum scalability

**Continuous Batching**
- Process requests as they arrive without waiting for full batches
- Maximizes GPU utilization
- Handles variable-length sequences efficiently

**Dynamic SplitFuse**
- Optimizes kernel execution and memory access patterns
- Reduces latency while maintaining high throughput

### Supported Models
- Falcon (7B - 180B)
- Llama/Llama-2/Llama-3 (7B - 405B)
- Mistral (7B)
- Mixtral MoE (8x7B)
- OPT (0.1B - 66B)
- Phi-2 (2.7B)
- Qwen/Qwen2 (0.5B - 72B)

## Development Notes

### Testing
- Uses pytest with fixtures defined in `tests/conftest.py`
- GPU tests run on self-hosted runners (A6000, V100)
- CPU-only formatting checks on GitHub Actions
- Test models: facebook/opt-125m (default)

### Code Style
- Formatted with yapf (column limit: 89)
- Linting with flake8 (ignores E,F403,F405,F541,F841,W)
- Spelling checks with codespell
- License headers required on all source files
- Pre-commit hooks enforce style before commits

### Dependencies
- DeepSpeed >= 0.15.0 (core inference engine)
- deepspeed-kernels (CUDA kernels)
- transformers, torch (model loading)
- pydantic >= 2.0.0 (configuration)
- fastapi, grpcio (serving)
- pyzmq (messaging)

### Build System
- setuptools-based build (pyproject.toml specifies build backend)
- Version from version.txt with git hash suffix
- Creates mii/version.py at build time

### Deployment Types
1. **Non-Persistent Pipeline** - in-process, temporary
2. **Persistent Local** - GRPC server on localhost
3. **Azure ML** - cloud deployment (aml_related/)

## Troubleshooting

### Common Issues
- **CUDA errors**: Ensure DeepSpeed-Kernels is compatible with your GPU architecture
- **Port conflicts**: Persistent deployments use port 50050 by default
- **Model loading**: Check Hugging Face model availability and access tokens
- **Memory issues**: Use tensor parallelism or replicas to distribute across GPUs

### Installation Problems
- Requires NVIDIA GPU with compute capability 8.0+ (Ampere+)
- CUDA 11.6+ required
- Pre-compiled wheels available for most environments
- Manual kernel compilation: see DeepSpeed-Kernels documentation

## Contributing Guidelines

### Requirements
- All commits must include DCO sign-off (`git commit -s`)
- Pre-commit hooks must pass
- License headers required on new files
- See CONTRIBUTING.md for full details

### CI/CD
- **formatting.yml** - runs pre-commit on all files
- **nv-a6000-fastgen.yml** - GPU tests on A6000 (main branch)
- **nv-v100-legacy.yml** - GPU tests on V100 (legacy support)
- **release.yml** - packaging and release