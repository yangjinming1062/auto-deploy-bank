# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

3DTrajMaster is a research project (ICLR 2025) for controlling multi-entity 3D trajectories in text-to-video generation, built on top of CogVideoX. It enables controlling 6DoF (degree of freedom) entity motion in 3D space with entity-specific 3D trajectories.

## Development Commands

### Environment Setup
```bash
cd CogVideo
conda create -n 3dtrajmaster python=3.10
conda activate 3dtrajmaster
pip install -r requirements.txt
```

### Inference
Run inference with the trained model:
```bash
cd CogVideo/inference
python 3dtrajmaster_inference.py \
    --model_path ../weights/cogvideox-5b \
    --ckpt_path ../weights/injector \
    --lora_path ../weights/lora \
    --lora_scale 0.6 \
    --annealed_sample_step 20 \
    --seed 24 \
    --output_path output_example
```

### Training (Two-Stage Process)

**Stage 1 - Train LoRA:**
```bash
cd CogVideo/finetune
bash finetune_single_rank_lora.sh
```

**Stage 2 - Train Injector:**
```bash
bash finetune_single_rank_injector.sh
```

Key training arguments:
- `--block_interval`: Insert injector every N transformer blocks (default: 2)
- `--finetune_init`: Use for initial fine-tuning; omit when resuming from checkpoint
- `--resume_from_checkpoint $TRANSFORMER_PATH`: Resume training from pretrained injector checkpoint

### Dataset Utilities
```bash
cd dataset
python load_dataset.py           # Load and visualize dataset samples
python vis_trajectory.py         # Visualize 6DoF pose sequences via Open3D
```

### Evaluation
```bash
# 3D Trajectory Evaluation (GVHMR)
cd eval/GVHMR
# Follow INSTALL.md for setup
python tools/demo/demo_folder.py -f eval_sets -d outputs/eval_sets_gvhmr -s
python tools/eval_pose.py -f outputs/eval_sets_gvhmr

# Visual Quality Metrics (FVD, FID, CLIP-SIM)
cd eval/common_metrics_on_video_quality
bash eval_visual.sh
```

## Code Architecture

### Core Components (CogVideo/finetune/models/)

**Transformer Model:**
- `cogvideox_transformer_3d.py`: Modified CogVideoXTransformer3DModel with 3D motion injection support
- `CogVideoXBlock`: Transformer block with optional trajectory injection via `attn1_injector`
- Key modification: `block_interval` parameter controls injector insertion frequency

**Custom Pipeline:**
- `pipeline_cogvideox.py`: Extended DiffusionPipeline handling `pose_embeds` and `prompts_list` inputs
- Accepts `annealed_sample_step` for guided sampling
- Uses `CogVideoXDPMScheduler` with trailing timestep spacing

**Attention Processor:**
- `attention_processor.py`: Standard CogVideoX attention processors
- `attention.py`: Core attention implementation with QK normalization support

**Embeddings:**
- `embeddings.py`: Video patch embeddings, timestep embeddings, 3D rotary position embeddings

### Inference Flow (3dtrajmaster_inference.py)

1. Load CogVideoX pipeline with custom transformer (bfloat16)
2. Fuse LoRA weights if provided
3. Load 3D poses from 360°-Motion Dataset via `get_pose_embeds()`
4. Process entity prompts and location context
5. Generate video with trajectory guidance via pipeline

### Dataset Format (360°-Motion Dataset)
```
480_720/
  Desert/
    location_data.json
    D_loc1_66_t1n36_0042_Hemi12_1/
      D_loc1_66_t1n36_0042_Hemi12_1.json  # Object poses per frame
  HDRI/
    loc1 (snowy street)/
    loc2 (park)/
    ...
  Hemi12_transforms.json  # 12 camera poses
  CharacterInfo.json
```

### Key File Locations

| Component | Path |
|-----------|------|
| Custom transformer | `CogVideo/finetune/models/cogvideox_transformer_3d.py` |
| Custom pipeline | `CogVideo/finetune/models/pipeline_cogvideox.py` |
| LoRA training script | `CogVideo/finetune/train_cogvideox_lora.py` |
| Injector training script | `CogVideo/finetune/train_cogvideox_injector.py` |
| Inference script | `CogVideo/inference/3dtrajmaster_inference.py` |
| Test prompts | `CogVideo/inference/test_sets.json` |
| Model configuration | `CogVideo/pyproject.toml` (ruff: line-length=119) |

## Model Weights

Download from [HuggingFace KwaiVGI/3DTrajMaster](https://huggingface.co/KwaiVGI/3DTrajMaster):
- `cogvideox-5b/`: Base CogVideoX-5B checkpoint
- `injector/`: Trained trajectory injector module
- `lora/`: Trained LoRA adapter

Place in `CogVideo/weights/` directory.