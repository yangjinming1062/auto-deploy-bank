# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the official implementation of **Score Jacobian Chaining (SJC)**, a method for lifting pretrained 2D diffusion models (like Stable Diffusion) for 3D generation. The code optimizes a voxel-based Neural Radiance Field (NeRF) to be consistent with the score (gradients) of a pretrained diffusion model.

## Setup

1. Install dependencies:
   ```bash
   pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
   pip install -r requirements.txt
   ```
2. Install the required `taming-transformers` library:
   ```bash
   git clone --depth 1 git@github.com:CompVis/taming-transformers.git && pip install -e taming-transformers
   ```
3. Download the model checkpoints from [the project website](https://dl.ttic.edu/pals/sjc/release.tar) (12GB) and update `env.json` to point to the `data_root` directory containing the extracted checkpoints.

## Running Experiments

Do not run experiments in the root directory. Create a separate directory:

```bash
mkdir exp
cd exp
```

Run the main SJC generation script:

```bash
python /path/to/sjc/run_sjc.py \
--sd.prompt "A zoomed out high quality photo of Temple of Heaven" \
--n_steps 10000 \
--lr 0.05 \
--sd.scale 100.0 \
--emptiness_weight 10000 \
--emptiness_step 0.5 \
--emptiness_multiplier 20.0 \
--depth_weight 0 \
--var_red False
```

## Architecture

- **Entry Point**: `run_sjc.py` orchestrates the 3D generation loop.
- **Models**: Adapters for different diffusion models are in `adapt.py` and its variants (`adapt_sd.py`, `adapt_gddpm.py`, etc.). `ScoreAdapter` in `adapt.py` defines the interface.
- **Rendering**: Voxel-based NeRF implementation is in `voxnerf/`.
- **Camera/Pose**: `pose.py` handles camera configuration and sampling.
- **Configuration**: Uses `my.config.BaseConf` with Pydantic for configuration management (via `run_sjc.py` config classes).