# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PuzzleAvatar reconstructs textured 3D clothed humans from unconstrained photo collections using Grounded-SAM for segmentation, multi-concept DreamBooth for view-specific texture generation, and a geometry+texture optimization pipeline based on TeCH/diffusion-based 3D reconstruction.

## Build and Installation

```bash
# Create conda environment
conda create --name PuzzleAvatar python=3.10
conda activate PuzzleAvatar

# Install dependencies
pip install -r requirements.txt

# Build submodules (required for custom CUDA kernels)
cd cores/lib/freqencoder && pip install -e .
cd ../gridencoder && pip install -e .
cd ../../thirdparties/nvdiffrast && pip install -e .
cd ../../thirdparties/peft && pip install -e .

# Install DINO+SAM
bash scripts/install_dino_sam.sh

# Download SMPL-X body data
bash scripts/download_body_data.sh
```

## Running the Pipeline

The main pipeline runs in 4 stages (DINO+SAM → DreamBooth training → Geometry → Texture):

```bash
bash scripts/run.sh <input_dir> <exp_dir> <subject_name>
```

Example:
```bash
bash scripts/run.sh data/human/yuliang results/human/yuliang human_yuliang
```

Individual pipeline steps can also be run separately:

```bash
# Grounded DINO + SAM segmentation
python multi_concepts/grounding_dino_sam.py --in_dir ${INPUT_DIR} --out_dir ${INPUT_DIR} --overwrite
python multi_concepts/islands_all.py --out_dir ${INPUT_DIR} --overwrite

# Multi-concept DreamBooth training
accelerate launch multi_concepts/train.py --pretrained_model_name_or_path stabilityai/stable-diffusion-2-1-base ...

# Geometry optimization
python cores/main_mc.py --config configs/tech_mc_geometry.yaml --exp_dir ${EXP_DIR} ...

# Texture optimization
python cores/main_mc.py --config configs/tech_mc_texture.yaml --exp_dir ${EXP_DIR} ...
```

## Evaluation

```bash
# Render reconstruction results
python -m render.render_batch_result -headless -out_dir ./results/ -split test

# Calculate 3D and 2D metrics
python -m multi_concepts.benchmark -split test
```

## Code Architecture

- **cores/main.py / cores/main_mc.py**: Entry points for geometry/texture optimization. Loads YAML configs and initializes the TeCH-based trainer.
- **cores/lib/**: Core training and rendering library:
  - `trainer.py`: Main training loop, loss computation, logging
  - `renderer.py`: nvdiffrast-based differentiable renderer
  - `provider.py`: Data loading and view sampling
  - `guidance.py`: Stable Diffusion 2-1 guidance with view prompts
  - `dmtet_network.py`: Deformable tetrahedral mesh network
  - `loss_utils.py`: SDS and other loss functions
- **multi_concepts/**: DreamBooth training and SAM-based segmentation:
  - `train.py`: Multi-concept DreamBooth training with PEFT (LoRA/BOFT)
  - `inference.py`: View-specific image generation
  - `grounding_dino_sam.py`: Person segmentation from input images
  - `puzzle_utils.py`: Puzzle assembly utilities
- **configs/**: YAML configuration files defining model architecture, training parameters, and guidance settings.
- **render/**: Rendering scripts for evaluation and visualization.
- **utils/**: Utility functions including body utilities and LDM utilities.

## Configuration System

Configs use yacs CfgNode and merge from `configs/default.yaml` with stage-specific configs (tech_mc_geometry.yaml, tech_mc_texture.yaml). Key config sections: `model`, `train`, `data`, `guidance`.

## Code Style

Formatting tools are configured in `setup.cfg`:
- **yapf**: Facebook style, 100 char column limit
- **autoflake**: Removes unused imports
- **isort**: Organizes imports, 80 char line limit

```bash
# Format code
autoflake --in-place --recursive --remove-all-unused-imports .
yapf -i --style=setup.cfg **/*.py
isort --settings-path=setup.cfg .
```

## Environment Setup

Set paths in `scripts/env.sh` before running:
- `HF_HOME`: HuggingFace cache directory
- `CUDA_HOME`: CUDA installation path
- `OPENAI_API_KEY`: For GPT-4V prompting (stored in OPENAI_API_KEY file)
- `PYOPENGL_PLATFORM`: Set to "osmesa" for headless rendering

## Key Dependencies

- PyTorch + PyTorch Lightning (training)
- nvdiffrast (differentiable rendering)
- diffusers (Stable Diffusion 2-1)
- peft (LoRA/BOFT fine-tuning)
- GroundingDINO + SAM (segmentation)
- Open3D, PyMeshLab (mesh processing)