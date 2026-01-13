# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PuLID (Pure and Lightning ID Customization via Contrastive Alignment) is an identity preservation technique for diffusion models (SDXL and FLUX). The project integrates three main components:
- **PuLID**: Core ID customization module with attention processors and encoders
- **EVA-CLIP**: Vision-language model for ID embeddings
- **FLUX**: Flow-based diffusion model for high-quality generation

## Development Commands

### Environment Setup
```bash
# Create conda environment
conda create --name pulid python=3.10
conda activate pulid

# Install dependencies (choose one)
pip install -r requirements.txt              # For SDXL or FLUX without FP8
pip install -r requirements_fp8.txt          # For FLUX with FP8 support
```

### Linting & Formatting
The project uses `ruff`, `black`, and `isort` for code quality (configured in `pyproject.toml:1-31`):

```bash
# Run linting (configured for Python 3.8+, excludes eva_clip/)
ruff check .

# Format code (120 line length for ruff, 119 for black, excludes eva_clip/)
ruff format .
black .

# Sort imports
isort .
```

### Running the Applications

#### SDXL Versions
```bash
# PuLID v1.0 (SDXL Lightning 4-step)
python app.py

# PuLID v1.1 (improved compatibility and editability)
python app_v1_1.py --base RunDiffusion/Juggernaut-XL-v9
# or
python app_v1_1.py --base Lykon/dreamshaper-xl-lightning
```

#### FLUX Version
```bash
# FLUX dev (supports --fp8 for consumer GPUs, --offload for CPU offloading)
python app_flux.py --version v0.9.1 --device cuda --port 8080

# With FP8 support (requires PyTorch >= 2.4.1)
python app_flux.py --fp8

# With aggressive offloading for 24GB GPUs
python app_flux.py --aggressive_offload

# With CPU offloading to reduce VRAM usage
python app_flux.py --offload
```

## Code Architecture

### Core Components

**`pulid/`** - PuLID ID customization module
- `pipeline.py:32-50` - SDXL v1.0 pipeline initialization with UNet and StableDiffusionXLPipeline
- `pipeline_v1_1.py` - SDXL v1.1 pipeline with improved compatibility
- `pipeline_flux.py` - FLUX integration with offloading support
- `attention_processor.py` - Custom attention processors for ID injection (IDAttnProcessor, AttnProcessor2_0)
- `encoders.py` - IDEncoder for generating identity embeddings from face images
- `encoders_transformer.py` - Transformer-based encoders
- `utils.py` - Utility functions (resize, tensor conversions, seeding)

**`flux/`** - FLUX model implementation
- `model.py` - Flux and FluxParams classes
- `sampling.py` - Denoising, scheduling, and noise generation
- `util.py` - Model loading utilities (load_flow_model, load_ae, load_clip, load_t5)
- `modules/` - Core modules:
  - `autoencoder.py` - AutoEncoder for VAE encoding/decoding
  - `conditioner.py` - HFEmbedder for text conditioning
  - `layers.py` - Transformer layers and blocks

**`eva_clip/`** - EVA-CLIP vision-language model
- Independent CLIP model implementation with pretrained weights
- Used for generating ID embeddings (excluded from linting)

### Key Integration Points

1. **Attention Injection** (`pulid/attention_processor.py`):
   - IDAttnProcessor modifies attention to inject identity information
   - NUM_ZERO and ORTHO/ORTHO_v2 flags control fidelity vs. style trade-off

2. **Model Offloading** (`app_flux.py:107-134`):
   - Sequential GPU/CPU offloading to support limited VRAM
   - Components offloaded: T5, CLIP, PuLID models, DiT, Autoencoder

3. **Face Processing** (`pulid/pipeline.py:13-18`):
   - Uses facexlib and insightface for face detection and restoration
   - FaceRestoreHelper prepares face images for ID encoding

## Important Configuration

### Version Selection
- **v1.0**: Original PuLID, best with SDXL-Lightning-4step
- **v1.1**: Better compatibility, editability, and naturalness (recommended for SDXL)
- **FLUX v0.9.0/0.9.1**: Superior prompt-following with improved ID fidelity in v0.9.1

### Key Parameters
- **ID Scale** (app.py:134): Controls identity strength (0-5, default 0.8)
- **Mode** (app.py:135): 'fidelity' for high ID similarity, 'extremely style' for more stylization
- **Timestep to start inserting ID** (app_flux.py:211): Controls fidelity vs. editability trade-off (0-10)
- **True CFG Scale** (app_flux.py:221): 1=fake CFG (faster), >1=true CFG (better quality in some cases)

## Model Loading

Models are loaded from HuggingFace Hub:
- SDXL Base: `stabilityai/stable-diffusion-xl-base-1.0`
- SDXL Lightning: `ByteDance/SDXL-Lightning`
- FLUX Dev: `black-forest-labs/FLUX.1-dev`
- PuLID Models: `guozinan/PuLID` (pulid_v1.bin, pulid_v1.1.safetensors, pulid_flux_v0.9.1.safetensors)

## Dependencies

Key dependencies (see `requirements.txt:1-18`):
- torch >= 2.0, torchvision >= 0.15
- diffusers 0.25.0, transformers 4.43.3
- gradio >= 4.0.0
- insightface, facexlib (face detection/restoration)
- onnxruntime (optimization)

For FLUX FP8 support, use `requirements_fp8.txt` with PyTorch >= 2.4.1.