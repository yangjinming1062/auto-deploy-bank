# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Lumina-T2X is a **multi-modal generation framework** that transforms text into images, videos, audio, and music using Flow-based Large Diffusion Transformers. It's a **monorepo** containing multiple independent projects with shared infrastructure components.

## Codebase Structure

This is a monorepo with **10 major components** organized as follows:

### Core Framework Modules (Production-Ready)
- `lumina_next_t2i_mini/` - **Recommended starting point** - Simplified 2B Next-DiT model with full functionality
- `lumina_next_t2i/` - Next-generation 2B model with 2K resolution support
- `lumina_t2i/` - Original 5B Flag-DiT model
- `lumina_audio/` - Text-to-Audio generation
- `lumina_music/` - Text-to-Music generation
- `lumina_next_compositional_generation/` - Compositional generation with multiple captions

### Research Implementations
- `Flag-DiT-ImageNet/` - Flag-DiT research on ImageNet
- `Next-DiT-ImageNet/` - Next-DiT research on ImageNet
- `Next-DiT-MoE/` - Next-DiT with Mixture of Experts

### Utilities
- `visual_anagrams/` - Visual anagrams generation application
- `assets/` - Static assets (logos, images, demos)

### Shared Infrastructure
Each module contains similar structure with shared patterns:
- `transport/` - Flow matching and ODE solvers (Euler, DOPRI5, DOPRI8)
- `parallel.py` - FSDP distributed training utilities
- `models/components.py` - Reusable components (norms, embeddings)
- `configs/` - Configuration-driven design (YAML files)

## Common Development Commands

### Installation & Setup

```bash
# Clone repository
git clone https://github.com/Alpha-VLLM/Lumina-T2X

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run pre-commit checks
pre-commit
```

### Installing Dependencies

```bash
# Core dependencies
pip install diffusers fairscale accelerate tensorboard transformers gradio torchdiffeq click

# Audio/music specific
pip install soundfile omegaconf torchdyn pytorch_lightning pytorch_memlab einops ninja torchlibrosa protobuf sentencepiece gradio transformers

# Optional: FlashAttention for speed
pip install flash-attn --no-build-isolation

# Optional: NVIDIA Apex (for fused layer norm)
pip install ninja
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --config-settings "--build-option=--cpp_ext" --config-settings "--build-option=--cuda_ext" ./
```

### Running Inference

Each module has dedicated entry points:

```bash
# Lumina-T2I entry point
lumina infer --text "A beautiful sunset" --output_path "output.png"
lumina convert "/path/to/model.pth" "/path/to/output/"  # Convert .pth to .safetensors

# Lumina-Next-T2I entry point
lumina_next infer --text "A beautiful sunset" --output_path "output.png"
lumina_next convert "/path/to/model.pth" "/path/to/output/"
```

### Interactive Web Demo

```bash
# Lumina-Next-T2I-Mini (recommended)
cd lumina_next_t2i_mini
python -u demo.py --ckpt "/path/to/ckpt"

# With custom settings
python -u demo.py --ckpt "/path/to/ckpt" --precision fp32 --ema --use_flash_attn False

# For other modules
cd lumina_next_t2i
python -u demo.py --ckpt "/path/to/ckpt"

cd lumina_t2i
python demo.py --ckpt "/path/to/ckpt"
```

### Training

```bash
# Navigate to specific module
cd lumina_next_t2i_mini  # Recommended for training
# OR
cd lumina_next_t2i
# OR
cd lumina_t2i

# Run training (FSDP-based, requires multiple GPUs)
python -u train.py \
    --config /path/to/config.yaml \
    --fsdp \
    --use_flash_attn \
    --num_epochs 100 \
    --save_every 1000 \
    --ckpt /path/to/checkpoints
```

### Sample Generation Scripts

```bash
# Direct inference scripts (customizable)
bash lumina_next_t2i_mini/scripts/sample.sh
bash lumina_next_t2i_mini/scripts/sample_img2img.sh  # img2img translation
bash lumina_next_t2i_mini/scripts/sample_sd3.sh      # SD3 support

# Check sample.py for argument customization
python lumina_next_t2i_mini/sample.py --help
```

### Code Quality

```bash
# Format code
black --line-length 120 .
isort .

# Or run via pre-commit
pre-commit run --all-files
```

### Downloading Models

```bash
# Using Hugging Face CLI
huggingface-cli download --resume-download Alpha-VLLM/Lumina-Next-SFT --local-dir /path/to/ckpt

# Git clone
git clone https://huggingface.co/Alpha-VLLM/Lumina-Next-SFT

# For Chinese users (WiseModel mirror)
git lfs install
git clone https://www.wisemodel.cn/Alpha-VLLM/Lumina-Next-SFT.git
```

## Architecture & Design Patterns

### Configuration-Driven Design

The codebase extensively uses YAML configuration files:
- **Data configs** (`configs/data/*.yaml`) - Dataset paths, metadata, caching
- **Inference settings** (`configs/infer/*.yaml`) - Model parameters, ODE solver settings, CFG scale
- Each config is loaded at runtime to configure training/inference

Key config parameters:
```yaml
model:
  ckpt: "/path/to/checkpoint"     # Model weights
  ckpt_lm: "/path/to/llm"         # Text encoder (LLaMA/Gemma)

transport:
  path_type: "Linear"             # Flow path (Linear, GVP, VP)
  prediction: "velocity"          # Prediction target
  sample_eps: 0.1                 # Sampling epsilon
  train_eps: 0.2                  # Training epsilon

infer:
  resolution: "1024x1024"         # Output resolution
  num_sampling_steps: 60          # ODE solver steps
  cfg_scale: 4.0                  # Classifier-free guidance
  solver: "euler"                 # ODE solver type (euler, dopri5, dopri8)
```

### Model Architecture Pattern

Each module follows consistent structure:

```
lumina_<modality>/
├── models/
│   ├── components.py      # ParallelTimestepEmbedder, ParallelLabelEmbedder, DiT blocks
│   ├── model.py           # Main DiT model implementation
│   └── diffusion/         # Diffusion-specific modules
├── transport/             # Flow matching core
│   ├── path.py           # Path definitions (Linear, GVP, VP)
│   ├── integrators.py    # ODE solvers (Euler, DOPRI5, DOPRI8)
│   └── transport.py      # Core transport logic
├── data/
│   ├── dataset.py        # Dataset class with caching
│   └── data_reader.py    # Data I/O utilities
├── train.py              # FSDP training script (~700 lines)
├── demo.py               # Gradio demo/inference
├── sample.py             # Sampling utilities
├── entry_point.py        # CLI entry point
├── parallel.py           # FSDP and model parallel utilities
├── utils/                # Helper functions
└── configs/              # YAML configs
```

### Flow-Based Diffusion (Key Innovation)

Unlike traditional DDPM/DDIM, Lumina-T2X uses **flow matching**:
- `transport/path.py` - Defines flow paths between noise and data
- `transport/integrators.py` - ODE solvers for sampling
- `transport/transport.py` - Core flow matching implementation
- Faster convergence and simpler pipeline than traditional diffusion

**Benefits:**
- Faster training convergence
- Stable training dynamics
- Arbitrary resolution generation
- Unified framework for all modalities

### Distributed Training (FSDP)

The codebase uses FullyShardedDataParallel:
- Model sharding across GPUs
- Gradient checkpointing support
- Mixed precision training (bf16/fp16/fp32)
- Requires multiple GPUs for full fine-tuning

Key patterns in `parallel.py`:
- `ColumnParallelLinear`, `RowParallelLinear` - Model parallelism
- `ParallelEmbedding` - Embedding sharding
- FSDP wrapper functions

### VAE Integration

All image/video modules use AutoencoderKL from Diffusers:
- SDXL VAE and FT VAE variants
- Latent space operations for efficiency
- Resolution extrapolation via special tokens

### Text Encoders

- **Lumina-T2I**: LLaMA-7B as text encoder
- **Lumina-Next**: Gemma-2B as text encoder (lighter, faster)
- Support multilingual prompts (Chinese, English, emojis)

## Key Technologies

### Core Stack
- **PyTorch** - Deep learning framework
- **FSDP (FairScale)** - Distributed training
- **Hugging Face Diffusers** - Diffusion model components
- **FlashAttention** - Optimized attention kernels
- **Transformers** - Text encoders (LLaMA, Gemma)
- **TorchDiffeq** - ODE solvers for flow matching

### Modality-Specific
- **Image**: diffusers VAE, SDXL support
- **Video**: 720P generation, arbitrary aspect ratios
- **Audio**: TorchLibrosa, SoundFile
- **Music**: CLAP encoders, music-specific processing
- **3D**: Point cloud generation support

## Model Variants & Recommendations

### For New Users
**Use `lumina_next_t2i_mini/`** - It's the recommended entry point:
- Simplified codebase (trimmed transport, removed unused model-parallel)
- All actual functionality retained
- Supports both Lumina-Next and SD3 training/inference
- Easiest to understand and modify

### For Research
- `lumina_next_t2i/` - Full-featured 2B Next-DiT
- `lumina_t2i/` - Original 5B Flag-DiT
- `Flag-DiT-ImageNet/`, `Next-DiT-ImageNet/` - Research baselines
- `Next-DiT-MoE/` - MoE experiments

### For Specific Applications
- `lumina_audio/` - Text-to-audio generation
- `lumina_music/` - Text-to-music generation
- `lumina_next_compositional_generation/` - Multi-caption compositional generation
- `visual_anagrams/` - Visual anagrams application

## Model Checkpoints

Available on Hugging Face and WiseModel (Chinese mirror):

| Model | Parameters | Resolution | Download |
|-------|-----------|------------|----------|
| Lumina-Next-SFT | 2B | 1024×1024 | [HF](https://huggingface.co/Alpha-VLLM/Lumina-Next-SFT) |
| Lumina-Next-T2I | 2B | 1024×1024 | [HF](https://huggingface.co/Alpha-VLLM/Lumina-Next-T2I) |
| Lumina-T2I | 5B | 1024×1024 | [HF](https://huggingface.co/Alpha-VLLM/Lumina-T2I) |
| Lumina-T2Audio | - | - | [HF](https://huggingface.co/Alpha-VLLM/Lumina-T2Audio) |
| Lumina-T2Music | - | - | [HF](https://huggingface.co/Alpha-VLLM/Lumina-T2Music) |

## Important Notes

### Model Conversion
When loading custom-trained models, convert `.pth` to `.safetensors` first:
```bash
lumina_next convert "/path/to/your/model.pth" "/path/to/output/"
```

### FlashAttention
Install with `--no-build-isolation` flag to avoid compilation issues. Can be disabled with `--use_flash_attn False` if installation fails.

### Apex Installation
Apex is optional but recommended. If installing, ensure full CUDA/C++ build (not Python-only). If you see `fused_layer_norm_cuda` errors, run `pip uninstall apex`.

### NVIDIA Requirements
- CUDA 12.1+ recommended
- `nvcc --version` should work
- GCC 6.0+ required on older distros

### Precision Settings
- Default: bf16 (best for A100/H100)
- fp32: Add `--precision fp32` to training/inference
- Automatic mixed precision supported via FSDP

### FSDP Requirements
- At least 8 GPUs recommended for full fine-tuning of 5B model
- Use gradient checkpointing for memory efficiency
- `lumina_next_t2i_mini` can work with fewer resources

## Documentation

Each module has its own detailed `README.md` with:
- Installation instructions
- Usage examples
- Configuration options
- Training details

Key READMEs:
- `/README.md` - Main project overview with all demos
- `/lumina_next_t2i_mini/README.md` - Simplified entry point guide
- `/lumina_next_t2i/README.md` - Full-featured guide
- `/lumina_t2i/README.md` - Original 5B model guide
- `/lumina_music/README.md` - Text-to-music specifics

## Entry Points Reference

Defined in `pyproject.toml`:
- `lumina` → `lumina_t2i:entry_point` (original 5B)
- `lumina_next` → `lumina_next_t2i:entry_point` (2B)

Commands available via CLI:
- `lumina infer` / `lumina_next infer` - Generate images
- `lumina convert` / `lumina_next convert` - Convert model formats

## High-Level Flow

```
Text Prompt → Text Encoder (LLaMA/Gemma)
                    ↓
            Flow Matching / Transport
                    ↓
            Diffusion Transformer (DiT)
                    ↓
            VAE Decoder (if needed)
                    ↓
            Generated Output (Image/Audio/Video/Music)
```

## Papers & Citations

```bibtex
@article{gao2024lumina-next,
  title={Lumina-Next: Making Lumina-T2X Stronger and Faster with Next-DiT},
  author={Zhuo, Le and Du, Ruoyi and Han, Xiao and Li, Yangguang and Liu, Dongyang and Huang, Rongjie and Liu, Wenze and others},
  journal={arXiv preprint arXiv:2406.18583},
  year={2024}
}

@article{gao2024lumin-t2x,
  title={Lumina-T2X: Transforming Text into Any Modality, Resolution, and Duration via Flow-based Large Diffusion Transformers},
  author={Gao, Peng and Zhuo, Le and Liu, Chris and and Du, Ruoyi and Luo, Xu and Qiu, Longtian and Zhang, Yuhang and others},
  journal={arXiv preprint arXiv:2405.05945},
  year={2024}
}
```