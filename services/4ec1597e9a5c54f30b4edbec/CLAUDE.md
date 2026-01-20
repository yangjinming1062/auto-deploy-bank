# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Prompt-Free Diffusion is a text-to-image diffusion model that generates images from visual reference inputs rather than text prompts. At its core is the **SeeCoder** (Semantic Context Encoder), which replaces traditional CLIP text encoders. Models can be loaded from `.safetensors`, `.pth`, or `.ckpt` files.

## Setup

```bash
conda create -n prompt-free-diffusion python=3.10
conda activate prompt-free-diffusion
pip install torch==2.0.0+cu117 torchvision==0.15.1 --extra-index-url https://download.pytorch.org/whl/cu117
pip install -r requirements.txt
```

## Running the Application

Start the Gradio WebUI:
```bash
python app.py
```

The WebUI launches on `0.0.0.0:11234`. It loads default models (SeeCoder, Deliberate-v2.0, canny ControlNet) on startup.

## Architecture

### Model Registry Pattern
The codebase uses a decorator-based registry system (`@register(name)`) in `lib/model_zoo/common/get_model.py`. Models are registered and instantiated via `get_model()(cfg)`.

### Key Model Components (lib/model_zoo/)

| File | Model | Purpose |
|------|-------|---------|
| `pfd.py` | `PromptFreeDiffusion` | Main diffusion model orchestrating VAE, SeeCoder, and diffuser |
| `seecoder.py` | `SemanticContextEncoder` | Image-only context encoder (replaces CLIP text encoder) |
| `openaimodel.py` | UNet-based | Core diffusion backbone (diffuser) |
| `autokl.py` | `AutoencoderKL` | VAE for image/latent encoding |
| `controlnet.py` | ControlNet | Optional control guidance (canny, depth, pose, etc.) |
| `ddim.py` | `DDIMSampler` | DDIM sampling for inference |

### Configuration System

Models are defined in YAML configs (`configs/model/`) with inheritance via `super_cfg`:

```yaml
pfd_seecoder_with_controlnet:
  super_cfg: pfd_seecoder
  type: pfd_with_control  # Maps to PromptFreeDiffusion_with_control class
  args:
    ctl_cfg: MODEL(controlnet)
```

Config resolution uses special tokens:
- `MODEL(name)`: Resolves to registered model config
- `SAME(path)`: References another config value
- `SEARCH(path)`: Depth-first search for config values

### Inference Flow (app.py)

1. Input image → SeeCoder → Context embedding `c`
2. Optional: Control input → ControlNet + preprocess → Conditioning `cc`
3. DDIM sampling loop uses `c` (and `cc` if applicable) for image generation
4. VAE decodes latent → final image output

## Model Paths

Default model locations (`app.py`):
- **Context Encoders**: `pretrained/pfd/seecoder/seecoder-*.safetensors`
- **Diffusers**: `pretrained/pfd/diffuser/SD-v1-5.safetensors` (and other base models)
- **ControlNets**: `pretrained/controlnet/control_*.safetensors`
- **Preprocess models**: `pretrained/controlnet/preprocess/*/*.pth`

Download all models from [HuggingFace](https://huggingface.co/shi-labs/prompt-free-diffusion).

## Model Conversion Tools

`tools/model_conversion.py` and `tools/get_controlnet.py` convert models between formats:
- SD WebUI ↔ PFD format
- Diffuser library ↔ PFD format

These require modifying hardcoded input/output paths.