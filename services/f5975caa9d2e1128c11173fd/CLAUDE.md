# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

3D-VLA is a 3D Vision-Language-Action Generative World Model that connects 3D perception, language, and action planning for Embodied AI. It integrates three main components:
1. **Goal Image Generation** - Uses latent diffusion models (LDM) to predict RGB or RGB-D goal images
2. **Goal Point Cloud Generation** - Uses diffusion models to predict 3D point cloud goals
3. **3D Multimodal LLM** - Vision-language-action model built on 3D-LLM and LAVIS

Built on the [LAVIS](https://github.com/salesforce/LAVIS) framework and [3D-LLM](https://github.com/UMass-Foundation-Model/3D-LLM).

## Environment Setup

```bash
conda create -n 3dvla python=3.9
conda activate 3dvla
pip install -r requirements.txt
```

**Note**: For point cloud diffusion, install [xFormers](https://github.com/facebookresearch/xformers) for improved performance.

## Development Commands

### Training

**Goal Image Latent Diffusion Model:**
```bash
bash launcher/train_ldm.sh [NUM_GPUS] [NUM_NODES] [EXP_ID]
```
- Uses `train_ldm_goal_image.py` (1,253 lines)
- Accepts optional `--include_depth` flag in script to train RGB-D model
- Outputs to `lavis/output/LDM/pix2pix/runs/`

**Goal Point Cloud Diffusion:**
```bash
bash launcher/train_pe.sh [NUM_GPUS] [NUM_NODES]
```
- Finetunes pretrained Point-E model
- Uses 2048 points during training, supports up to 8192 during inference

**3D-VLA LLM (Multimodal):**
```bash
bash launcher/train_llm.sh [NUM_GPUS] [NUM_NODES] [JOB_ID]
```
- Uses `train.py` with YAML configs from `lavis/projects/blip2/train/pretrain/`
- Default config: `lavis/projects/blip2/train/pretrain/3d_flant5_robo_pretrain.yaml`

### Single-GPU Training Alternatives

For point cloud and image generation (no torchrun wrapper needed):
```bash
python train_ldm_goal_image.py [arguments]
python train_pe_goal_pcd.py [arguments]
```

For LLM training, use torchrun directly:
```bash
torchrun --nproc_per_node=1 train.py --cfg-path [CONFIG_PATH] --job_id [JOB_ID]
```

### Inference

**Goal Image Generation:**
```bash
python inference_ldm_goal_image.py \
    --ckpt_folder lavis/output/LDM/pix2pix/runs \
    # optional: --include_depth
```

Use Hugging Face models:
```bash
python inference_ldm_goal_image.py \
    --ckpt_folder anyezhy/3dvla-diffusion \
    --image docs/cans.png --text "knock pepsi can over" \
    --save_path result.png

python inference_ldm_goal_image.py \
    --ckpt_folder anyezhy/3dvla-diffusion-depth --include_depth \
    --image docs/bottle.png --text "move water bottle near sponge" \
    --save_path result.png
```

**Goal Point Cloud Generation:**
```bash
python inference_pe_goal_pcd.py \
    --input_npy docs/point_cloud.npy --text "close bottom drawer" \
    --output_dir SAVE_PATH

python inference_pe_goal_pcd.py \
    --input_npy docs/money.npy \
    --text "put the money away in the safe on the bottom shelf"
```

Multi-GPU inference:
```bash
torchrun --nproc_per_node=[NUM_GPUS] --master_port=[PORT] inference_pe_goal_pcd.py [arguments]
```

## Architecture

The codebase follows the LAVIS modular architecture:

- **`lavis/`** - Core framework directory
  - **`models/`** - Model definitions (blip2_models, pointe for Point-E models)
  - **`tasks/`** - Task definitions (vqa.py, base_task.py)
  - **`datasets/`** - Dataset builders and loaders
  - **`processors/`** - Data preprocessing (image, text, point cloud)
  - **`runners/`** - Training loop implementations
  - **`common/`** - Shared utilities (config, dist_utils, logger, registry)
  - **`configs/`** - YAML configuration files
  - **`projects/`** - Project-specific configurations (blip2/train/pretrain/)

- **`train.py`** - Generic LAVIS training entry point (116 lines)
- **`train_ldm_goal_image.py`** - Goal image LDM training (1,253 lines)
- **`train_pe_goal_pcd.py`** - Point cloud diffusion training
- **`inference_*.py`** - Inference scripts for each model type
- **`launcher/`** - Shell scripts for multi-GPU training with torchrun

### Configuration System

Uses OmegaConf for configuration management:
- Model configs: `lavis/configs/models/blip2/*.yaml`
- Dataset configs: `lavis/configs/datasets/*.yaml`
- Training configs: `lavis/projects/blip2/train/pretrain/*.yaml`
- Override configs with `--replace_cfg key1=val1 key2=val2` (train.py)

## Key Model Releases

Available on Hugging Face:
- **Goal Image LDM**: `anyezhy/3dvla-diffusion` - RGB goal image generation
- **Goal RGB-D LDM**: `anyezhy/3dvla-diffusion-depth` - RGB-D goal image generation
- **Goal Point Cloud DM**: `anyeZHY/3dvla-diffusion-pointcloud` - Point cloud goal generation

See `docs/model_card.md` for detailed model information, datasets, and training procedures.

## Important Notes

- All training scripts use `torch.multiprocessing.set_start_method("spawn")`
- Models automatically download from Hugging Face during inference
- Point cloud preprocessing removes table background and normalizes to unit sphere
- LLM training requires custom annotation paths (replace `ANNOTATION_PATH` in scripts)
- Multi-node training requires setting `YOUR_MASTER_IP` and `YOUR_NODE_RANK` in launcher scripts