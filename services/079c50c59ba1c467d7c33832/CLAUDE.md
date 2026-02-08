# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SeedVR/SeedVR2 is a high-performance video restoration framework using Diffusion Transformers (DiT). SeedVR handles arbitrary-resolution video restoration; SeedVR2 enables one-step restoration via diffusion adversarial post-training.

**Languages:** Python 3.9/3.10, PyTorch

## Environment Setup

```bash
conda create -n seedvr python=3.10 -y
conda activate seedvr
pip install -r requirements.txt
pip install flash_attn==2.5.9.post1 --no-build-isolation

# Install Apex (required for optimization)
# Either from source or pre-built wheel:
pip install apex-0.1-cp310-cp310-linux_x86_64.whl  # See readme.md for download links
```

## Common Commands

### Inference

```bash
# SeedVR2-3B example
torchrun --nproc-per-node=NUM_GPUS projects/inference_seedvr2_3b.py \
    --video_path INPUT_FOLDER \
    --output_dir OUTPUT_FOLDER \
    --seed 666 \
    --res_h 720 \
    --res_w 1280 \
    --sp_size 1

# SeedVR2-7B
torchrun --nproc-per-node=NUM_GPUS projects/inference_seedvr2_7b.py ...

# SeedVR (3B/7B)
torchrun --nproc-per-node=NUM_GPUS projects/inference_seedvr_3b.py ...
```

Key inference parameters:
- `--sp_size`: Sequence parallel size (1 H100-80G handles ~100 frames at 720p; use 4 for 1080p/2K)
- `--res_h`, `--res_w`: Output resolution

### Development

```bash
# Linting
flake8, black, isort, yapf available in environment

# Testing
pytest
```

## Architecture

### Directory Structure

- `common/`: Shared utilities (config handling, distributed training, logging, diffusion ops)
- `models/`: Core model architectures
  - `dit/` & `dit_v2/`: Diffusion Transformer implementations
  - `video_vae_v3/`: Video VAE models
- `projects/`: Inference scripts (inference_seedvr*.py, inference_seedvr2*.py)
- `configs_3b/` & `configs_7b/`: YAML configurations with inheritance
- `data/`: Data loading and preprocessing transforms

### Configuration System

The project uses **OmegaConf** with custom patterns:

```yaml
# Object instantiation via __object__
__object__:
  path: path.to.module
  name: MyClass
  args: as_config | as_params

# Inheritance
__inherit__: path/to/parent.yaml
```

- `common/config.py`: Contains `load_config()`, `create_object()`, and custom `${eval:...}` resolver
- Configs recursively resolve inheritance and instantiate objects from YAML definitions

### Model Architecture

- **Modular design**: DiT and VAE components are decoupled and configurable via YAML
- **Distributed computing**: Built-in support for Data Parallel and Sequence Parallel (SP) processing
- **High-resolution handling**: Adaptive window attention in SeedVR2, sequence parallelism for multi-GPU

## Model Checkpoints

Download from HuggingFace to `ckpts/` directory:
```python
from huggingface_hub import snapshot_download
snapshot_download(
  repo_id="ByteDance-Seed/SeedVR2-3B",
  local_dir="ckpts/",
  allow_patterns=["*.json", "*.safetensors", "*.pth", "*.bin", "*.py"]
)
```

Available models: SeedVR-3B, SeedVR-7B, SeedVR2-3B, SeedVR2-7B

## Notes

- For wavelet-based color reconstruction, place `color_fix.py` from [sd-webui-stablesr](https://github.com/pkuliyi2015/sd-webui-stablesr/blob/master/srmodule/colorfix.py) into `./projects/video_diffusion_sr/`
- Flash Attention 2.5.9+ is required for memory-efficient DiT inference
- This is a research codebase; inference scripts may have hardcoded paths or settings that need adjustment