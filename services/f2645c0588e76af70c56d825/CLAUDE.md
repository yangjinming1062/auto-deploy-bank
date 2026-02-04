# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GLEE (General Object Foundation Model for Images and Videos at Scale) is a CVPR 2024 computer vision foundation model that unifies object detection, instance segmentation, grounding, multi-target tracking, video instance segmentation (VIS), video object segmentation (VOS), and interactive segmentation across images and videos. Built on Detectron2.

Key capabilities:
- Object detection and instance segmentation (COCO, LVIS, Objects365, OpenImages)
- Referring expression comprehension/segmentation (RefCOCO series)
- Video instance segmentation (YouTube-VIS, OVIS) and tracking (TAO, BURST)
- Open-vocabulary object perception via CLIP text prompts
- Interactive segmentation via visual prompts (points, boxes, scribbles)

## Installation

```bash
# Core dependencies
pip install shapely==1.7.1 lvis scipy fairscale einops xformers tensorboard \
  opencv-python-headless timm ftfy transformers==4.36.0

# Install detectron2 in editable mode
pip install -e .

# Install cocoapi
pip install git+https://github.com/wjf5203/cocoapi.git#"egg=pycocotools&subdirectory=PythonAPI" --user

# Download CLIP text encoder (required)
wget -P projects/GLEE/clip_vit_base_patch32/ \
  https://huggingface.co/spaces/Junfeng5/GLEE_demo/resolve/main/GLEE/clip_vit_base_patch32/pytorch_model.bin

# Compile custom CUDA ops for deformable attention
cd projects/GLEE/glee/models/pixel_decoder/ops/
python3 setup.py build install --user
```

## Common Commands

### Training

```bash
# Single machine training (8 GPUs)
python3 projects/GLEE/train_net.py --config-file projects/GLEE/configs/images/Lite/Stage2_joint_training_CLIPteacher_R50.yaml --num-gpus 8

# Multi-machine distributed training
python3 launch.py --nn <num_machines> --port <PORT> --worker_rank <Global_Rank> \
  --master_address $<MASTER_ADDRESS> --config-file projects/GLEE/configs/images/Lite/Stage2_joint_training_CLIPteacher_R50.yaml

# Video task fine-tuning from image model
python3 projects/GLEE/train_net.py --config-file projects/GLEE/configs/videos/Lite/ytvis19_base.yaml --num-gpus 8 \
  MODEL.WEIGHTS /path/to/GLEE_Lite_joint.pth
```

### Evaluation

```bash
# Image-level tasks
python3 projects/GLEE/train_net.py --config-file projects/GLEE/configs/images/Lite/Stage2_joint_training_CLIPteacher_R50.yaml \
  --num-gpus 8 --eval-only MODEL.WEIGHTS /path/to/GLEE_Lite_joint.pth DATASETS.TEST '("coco_2017_val",)'

# Multi-dataset evaluation
python3 projects/GLEE/train_net.py --config-file projects/GLEE/configs/images/Lite/Stage2_joint_training_CLIPteacher_R50.yaml \
  --num-gpus 8 --eval-only MODEL.WEIGHTS /path/to/GLEE_Lite_joint.pth \
  DATASETS.TEST '("coco_2017_val","lvis_v1_val","objects365_v2_val","refcoco-unc-val",)'

# Video tasks (results.zip for Codalab submission)
python3 projects/GLEE/train_net.py --config-file projects/GLEE/configs/videos/Lite/ytvis19_base.yaml \
  --eval-only --num-gpus 8 MODEL.WEIGHTS /path/to/GLEE_Lite_joint.pth
```

### Demo

```bash
# Run Gradio demo locally
python app.py
```

## Architecture

### Core Components

**GLEE Meta-Architecture** (`projects/GLEE/glee/GLEE.py`):
- Main class registered with `@META_ARCH_REGISTRY.register()`
- Handles task routing via `get_task_name()` method
- Maintains category name mappings for 16+ datasets
- Implements category sampling for large-vocabulary training
- Manages visual prompt integration (points, boxes, scribbles)

**GLEE_Model** (`projects/GLEE/glee/models/glee_model.py`):
- Neural network combining:
  - **Backbone**: ResNet-50, Swin-Large, or EVA02-Large via detectron2's `build_backbone`
  - **Text encoder**: CLIP (clip_frozen, clip_unfrozen, or clip_teacher variants)
  - **Pixel decoder**: MaskDINO-style encoder with custom deformable attention ops
  - **Transformer decoder**: DINO-style decoder with language-guided query fusion

**Training** (`projects/GLEE/train_net.py`):
- Extends `detectron2.engine.DefaultTrainer`
- Custom dataset mappers for each task type
- Multi-dataset sampling via `MultiDatasetSampler`
- Custom optimizer with component-specific LR multipliers

### Directory Structure

```
projects/GLEE/
  glee/
    GLEE.py                    # Meta-architecture (task routing, loss management)
    config.py                  # GLEE-specific config additions
    models/
      glee_model.py            # Core neural network
      criterion.py             # SetCriterion with Hungarian matching
      matcher.py               # HungarianMatcher for label assignment
      pixel_decoder/           # MaskDINO encoder + custom ops (ms_deform_attn)
      transformer_decoder/     # DINO decoder with language fusion
    data/
      datasets/                # Dataset definitions (builtin.py maps names to classes)
      coco_dataset_mapper_uni.py
      joint_image_video_dataset_mapper.py
    modules/
      attention.py, point_features.py, postprocessing.py
  configs/images/              # Image task configs (Lite/Plus/Pro variants)
  configs/videos/              # Video task configs
  train_net.py                 # Training entry point
launch.py                      # Multi-node launcher
```

### Data Flow

1. Input: Images (+ optional text prompts, visual prompts like boxes/points/scribbles)
2. `get_task_name()` determines task from dataset_name field
3. Backbone extracts visual features
4. Text encoder encodes category names/descriptions via CLIP
5. Pixel decoder produces multi-scale features with deformable attention
6. Transformer decoder predicts masks, boxes, and class logits
7. `SetCriterion` computes losses using Hungarian matching

### Task-to-Dataset Mapping

Dataset names determine task type in `GLEE.get_task_name()`:
- `coco`, `lvis`, `obj365`, `openimage`: Object detection/segmentation
- `refcoco*`: Referring expression comprehension
- `ytvis19`, `ytvis21`, `ovis`, `lvvis`: Video instance segmentation
- `burst`, `tao_video`: Multi-object tracking
- `rvos`, `ytbvos`: Referring video object segmentation
- `sa1b`, `grit`, `vg`: Grounding/segmentation data
- `grounding`: Expression-based detection
- `omnilabel`, `odinw`: Zero-shot evaluation

## Model Variants

Three backbone options with corresponding configs:

| Variant | Backbone | Config Pattern |
|---------|----------|----------------|
| Lite | ResNet-50 | `Stage*_R50.yaml` |
| Plus | Swin-Large | `Stage*_SwinL.yaml` |
| Pro | EVA02-Large | `Stage*_EVA02L*.yaml` |

Training stages (must be run sequentially):
1. **Stage1**: Objects365 & OpenImages pretraining
2. **Stage2**: Multi-dataset joint training (15 datasets)
3. **Stage3**: Scale-up with SA1B and GRIT data

## Configuration Patterns

Configs use Hydra/YAML format. Key parameters:
- `DATASETS.TRAIN/TEST`: Dataset tuples, e.g., `("coco_2017_val",)`
- `MODEL.WEIGHTS`: Checkpoint path
- `MODEL.TEXT.ARCH`: `clip_frozen`, `clip_unfrozen`, or `clip_teacher`
- `SOLVER.BASE_LR`: Learning rate (typically 1e-4)
- `SOLVER.IMS_PER_BATCH`: Batch size
- `MODEL.MaskDINO.NUM_OBJECT_QUERIES`: Number of detection queries (300)

## Data Organization

```
datasets/                    # Root for all datasets
  coco/                     # images + annotations/
  lvis/                     # lvis_v1_*.json
  Objects365v2/             # annotations/, images/
  openimages/               # detection/, openimages_v6_train_bbox.json
  visual_genome/            # images/, annotations/
  ytvis_2019/, ytvis_2021/  # train/, val/, annotations/
  ovis/                     # train/, val/, annotations/
  TAO/                      # frames/, TAO_annotations/
  SA1B/                     # images/, sa1b_subtrain_*.json
  refcoco-unc/, refcocog-umd/, refcocoplus-unc/
  bdd100k/                  # images/, labels/
```

## Code Conventions

- Registered with `@META_ARCH_REGISTRY.register()` in detectron2
- Custom evaluators in `detectron2.projects.glee.data`
- CLIP integration via HuggingFace transformers (CLIPTokenizer, CLIPTextModel)
- Custom CUDA ops in `projects/GLEE/glee/models/pixel_decoder/ops/`
- Visual prompts: points, boxes, scribbles passed as `prompt_list` dict with `spatial` key