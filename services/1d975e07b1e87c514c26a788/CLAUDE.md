# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

D-NeRF is a Neural Radiance Fields implementation for modeling dynamic scenes with non-rigid geometries. It synthesizes novel views at arbitrary time points from sparse monocular views. The code extends NeRF-pytorch with temporal deformation capabilities.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt
cd torchsearchsorted && pip install .  # Custom CUDA kernel for searchsorted

# Train a model (e.g., mutant scene)
export PYTHONPATH=/path/to/D-NeRF
export CUDA_VISIBLE_DEVICES=0
python run_dnerf.py --config configs/mutant.txt

# Render from trained model (requires pretrained weights in ./logs/)
python run_dnerf.py --config configs/mutant.txt --render_only --render_test

# Render test set only
python run_dnerf.py --config configs/mutant.txt --render_only --render_test
```

## Architecture

### Core Pipeline

1. **Data Loading** (`load_blender.py`): Loads Blender-format datasets with transforms JSON files containing camera poses, images, and time values for each frame.

2. **NeRF Models** (`run_dnerf.py`):
   - `NeRFOriginal`: Standard NeRF with 8-layer MLP, outputs RGB + density
   - `DirectTemporalNeRF`: Extends NeRF with time-conditioned deformation that warps points from canonical (t=0) space to observation space; zero_canonical=True means t=0 is canonical space

3. **Rendering** (`run_dnerf_helpers.py`):
   - `render_rays()`: Volumetric rendering along rays using numerical integration
   - `render()`: High-level rendering for full images with ray batching
   - `sample_pdf()`: Hierarchical sampling (coarse-to-fine) using the custom `searchsorted` function
   - `raw2outputs()`: Converts raw model predictions (RGB + density) to accumulated color, disparity, and opacity

4. **Custom CUDA Extension** (`torchsearchsorted/`): Fast searchsorted implementation for PDF sampling, required by hierarchical sampling in `sample_pdf()`.

### Key Data Flow

1. Images + poses + times loaded from `data/{scene}/transforms_{train,val,test}.json`
2. Rays sampled per image: origin, direction, time
3. Points sampled along rays (coarse + optional fine)
4. Network predicts density + RGB per point, with temporal deformation
5. Volumetric rendering accumulates color along each ray

### Positional Encoding

Both spatial coordinates (3D) and view directions (3D) pass through `Embedder` for sinusoidal positional encoding (multires=10 by default). Time uses 1D positional encoding.

## Configuration

Experiments use `.txt` config files in `configs/`. Key parameters:
- `nerf_type`: "original" or "direct_temporal"
- `N_samples`: Coarse samples per ray (64)
- `N_importance`: Fine samples per ray (128 for dnerf)
- `N_rand`: Random rays per batch
- `use_viewdirs`: Whether to use viewing directions (enabled for most experiments)
- `not_zero_canonical`: If True, t=0 is not canonical space

## Checkpoints & Logs

- Saved to `./logs/{expname}/` as `.tar` files
- Contains: global_step, model weights, optimizer state, AMP state
- TensorBoard logs in `./logs/summaries/{expname}/`