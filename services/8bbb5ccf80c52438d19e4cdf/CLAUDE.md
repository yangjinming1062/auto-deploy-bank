# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

InfiniteYou (InfU) is a framework for identity-preserved image generation using Diffusion Transformers (DiTs), built on FLUX.1-dev. It features InfuseNet, a component that injects identity features into DiT base models via residual connections. Published at ICCV 2025.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# CLI inference
python test.py --id_image ./assets/examples/man.jpg --prompt "A man, portrait, cinematic" --out_results_dir ./results

# Run Gradio demo
python app.py

# Single test example with memory optimization
python test.py --id_image ./assets/examples/man.jpg --prompt "A man, portrait, cinematic" --cpu_offload --quantize_8bit
```

## Architecture

```
app.py          → Gradio web UI, manages pipeline lifecycle and caching
test.py         → CLI entrypoint for inference
pipelines/
├── pipeline_infu_flux.py    → Main pipeline: orchestrates ID embedding extraction (face detection → ArcFace → resampler)
├── pipeline_flux_infusenet.py → Diffusers FluxControlNetPipeline wrapper for denoising loop
└── resampler.py             → Perceiver-based embedding projector (8 queries, depth=4)
```

**Inference flow**: ID image → InsightFace detection → ArcFace embedding → Resampler → InfuseNet → FLUX.1-dev Transformer → VAE decode

## Model Configuration

| Model Version | Description | Use Case |
|--------------|-------------|----------|
| `aes_stage2` | Stage-2 SFT model | Default; better text-image alignment and aesthetics |
| `sim_stage1` | Stage-1 pre-SFT | Higher identity similarity |

Key parameters:
- `--infusenet_conditioning_scale` (default: 1.0) - ID influence strength
- `--infusenet_guidance_start` (default: 0.0) - When to start applying identity guidance

## Memory Optimization

| Mode | Peak VRAM |
|------|-----------|
| Default (bf16) | ~43GB |
| `--cpu_offload` | ~30GB |
| `--quantize_8bit` | ~24GB |
| Both combined | ~16GB |

## Key Dependencies

- `diffusers==0.31.0` - Diffusion pipeline base
- `insightface==0.7.3` - Face detection/alignment
- `optimum-quanto==0.2.7` - 8-bit quantization
- `gradio==5.23.1` - Web UI framework

## Models & Downloads

Models are downloaded automatically from HuggingFace:
- `ByteDance/InfiniteYou` → `./models/InfiniteYou/`
- `black-forest-labs/FLUX.1-dev` → `./models/FLUX.1-dev/`

Accept FLUX.1-dev license at https://huggingface.co/black-forest-labs/FLUX.1-dev before first run.