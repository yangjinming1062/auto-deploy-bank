# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**LEO** is an embodied multi-modal generalist agent (ICML 2024) capable of grounding, reasoning, chatting, planning, and acting in 3D worlds. The model uses a two-stage training scheme: (1) **3D vision-language alignment** and (2) **3D vision-language-action instruction tuning**.

## Common Commands

### Installation
```shell
# Create conda environment
conda create -n leo python=3.9
conda activate leo

# Install PyTorch (example version)
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch

# Install dependencies
pip install -r requirements.txt
pip install peft==0.5.0 --no-deps

# Install point cloud backbones
cd model/pointnetpp && python setup.py install
cd ../pointnext/cpp/pointnet2_batch && python setup.py build_ext --inplace
```

### Training
All training runs through `launch.py` with three launch modes:

```shell
# Python mode (single GPU)
python launch.py --mode python --config configs/default.yaml task=align note=align_lora

# Accelerate mode (multi-GPU)
python launch.py --mode accelerate --config configs/default.yaml task=align

# SLURM submitit mode (cluster, default)
python launch.py --mode submitit \
    --config configs/default.yaml \
    --name leo_tuning \
    --qos lv0b \
    --time 48 \
    --num_nodes 1 \
    --partition HGX \
    --gpu_per_node 4 \
    task=align \
    note=align_lora
```

Key Hydra overrides:
- `task=[align|tuning_noact|tuning_scannet|tuning_scanqa|tuning_sqa3d|tuning_vla]`
- `note=<experiment_name>`
- `pretrained_ckpt_path=<path>` - load checkpoint from folder containing `pytorch_model.bin`
- `logger.entity=<wandb_entity>`

### Inference
```shell
python launch.py --mode python \
    --run_file inference.py \
    --config configs/default.yaml \
    note=tuning_noact
```

Modify `probe` in `configs/default.yaml` to customize inference inputs.

## Architecture

### Core Components

**Model (`model/leo_agent.py`):** `LeoAgent` class encapsulates the full architecture:
- **LLM Backend:** Vicuna 7B/13B (frozen, with optional LoRA)
- **2D Encoder:** Configurable vision encoder (e.g., ConvNeXt)
- **3D Encoder:** Point cloud backbone (PointNet++, PointBERT, PointNext)
- **Projection Layers:** Linear layers mapping 2D/3D features to LLM hidden size
- **Prompt Template:** `<role_prompt><situation><img_tokens><objects_prompt><obj_tokens><task_prompt>`

**Training (`trainer/leo_trainer.py`):** `LeoTrainer` class handles:
- Distributed training via `accelerate`
- Gradient accumulation and checkpointing
- Multi-task evaluation with separate evaluators per task
- Best model saving based on validation metrics

**Datasets (`data/datasets.py`):** `LeoMix` aggregates multiple datasets:
- Text tasks: `LeoCap3D`, `LeoScan2Cap`, `LeoScanQA`, `LeoSQA3D`, `Leo3RScanQA`, `Leo3RScanPlan`, `Leo3RScanDialog`, `LeoSceneCap`, `LeoObjSceneCap`
- EAI tasks: `LeoMP3DObjNav` (navigation), `LeoCLIPort` (manipulation)
- 3D LLM tasks: `LeoSceneCap3DLLM`, `LeoQA3DLLM`, `LeoPlan3DLLM`, `LeoDialog3DLLM`

**Evaluation (`evaluator/`):** Task-specific evaluators:
- `cap_eval.py`: CIDEr, BLEU for captioning
- `scanqa_eval.py`: Accuracy for QA
- `sqa3d_eval.py`: SQA3D metrics
- N-gram metrics: BLEU, CIDEr, ROUGE, METEOR

### Configuration Structure

Hydra configs in `configs/`:
- `default.yaml`: Main config composing sub-configs
- `data/default.yaml`: Dataset paths (scan_family_base, rscan_base, alignment_base, instruction_base)
- `task/*.yaml`: Task definitions (training epochs, mix ratio, dataloader args)
- `llm/*.yaml`: LLM config (vicuna7b, vicuna13b)
- `vision3d/ose3d_pointnetpp.yaml`: 3D encoder config
- `vision2d/convnext.yaml`: 2D encoder config

### Data Flow

1. `launch.py` → parses args → calls launch mode function
2. `run.py` → Hydra main entry → `LeoTrainer.run()`
3. `LeoTrainer` → builds model, dataloaders, evaluators → training loop
4. `LeoAgent.forward()` → encodes 2D/3D → builds sequence → LLM forward → loss
5. Datasets → load point clouds (`.pth`), annotations (`.json`) → preprocess → `data_dict`
6. Evaluators → gather predictions → compute metrics

### Key Data Structures

**Point cloud format:** `(N, 6)` array with `[x, y, z, r, g, b]` (RGB normalized to [-1, 1])
**Bbox format:** `(6,)` with `[cx, cy, cz, w, h, d]`
**Object tokens:** Encoded by 3D backbone, projected to LLM hidden dim
**Image tokens:** Encoded by 2D backbone, projected to LLM hidden dim

### Checkpoint Format

Checkpoints saved as `pytorch_model.bin` containing model state dict (filtered to learnable params when saving with `model_only=True`).

## Environment Variables

- `TOKENIZERS_PARALLELISM=true` - suppress HF tokenizer warnings (set in `run.py`)
- Set data paths in `configs/data/default.yaml` before running

## Important Files

- `inference.py`: Standalone inference script
- `model/pcd_backbone.py`: 3D backbone factory
- `model/build.py`: Module builder using hydra
- `data/build.py`: Dataset/dataloader builder
- `evaluator/build.py`: Evaluator builder
- `trainer/build.py`: Optimizer/scheduler builder
- `common/misc.py`: Custom accelerator modifications (gather_for_metrics, get_state_dict)
- `scripts/*.sh`: Example training scripts for different configurations