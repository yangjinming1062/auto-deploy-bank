# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VADER (Video Diffusion Alignment via Reward Gradient) is a research implementation for aligning video diffusion models using reward model gradients. It enables fine-tuning text-to-video models for specific downstream tasks like aesthetic improvement, text-video alignment, and action prediction without requiring supervised datasets.

## Commands

### Common Setup (accelerate)
Before running any training or inference, configure Accelerator:
```bash
accelerate config
```

### VADER-VideoCrafter (Recommended for best performance)

**Installation:**
```bash
cd VADER-VideoCrafter
conda create -n vader_videocrafter python=3.10
conda activate vader_videocrafter
conda install pytorch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 pytorch-cuda=12.1 -c pytorch -c nvidia
conda install xformers -c xformers
pip install -r requirements.txt
git clone https://github.com/tgxs002/HPSv2.git
cd HPSv2/ && pip install -e .
```

**Training:**
```bash
cd VADER-VideoCrafter
sh scripts/run_text2video_train.sh
```

**Inference:**
```bash
cd VADER-VideoCrafter
sh scripts/run_text2video_inference.sh
```

**Key Training Script:** `VADER-VideoCrafter/scripts/main/train_t2v_lora.py`

### VADER-ModelScope

**Installation:**
```bash
cd VADER-ModelScope
conda create -n vader_modelscope python=3.10
conda activate vader_modelscope
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0
pip install -r requirements.txt
git clone https://github.com/tgxs002/HPSv2.git
cd HPSv2/ && pip install -e .
```

**Training:**
```bash
cd VADER-ModelScope
sh run_text2video_train.sh
```

**Inference:**
```bash
cd VADER-ModelScope
sh run_text2Video_inference.sh
```

**Baselines (DPO/DDPO):**
```bash
cd VADER-ModelScope
sh run_t2vid_dpo_train.sh    # DPO training
sh run_t2vid_ddpo_train.sh   # DDPO training
```

**Key Training Script:** `VADER-ModelScope/train_t2v_lora.py`

### VADER-Open-Sora

**Installation:**
```bash
cd VADER-Open-Sora
conda create -n vader_opensora python=3.10
conda activate vader_opensora
conda install pytorch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 pytorch-cuda=12.1 -c pytorch -c nvidia
conda install xformers -c xformers
pip install -v -e .
git clone https://github.com/tgxs002/HPSv2.git
cd HPSv2/ && pip install -e .
```

**Training:**
```bash
cd VADER-Open-Sora
sh scripts/run_text2video_train.sh
```

**Inference:**
```bash
cd VADER-Open-Sora
sh scripts/run_text2video_inference.sh
```

**Key Training Script:** `VADER-Open-Sora/scripts/train_t2v_lora.py`

## Architecture

### Core Components (Shared Across All Model Implementations)

**Location:** `/home/ubuntu/deploy-projects/c8c15630b28dda157c5f37db/Core/`

- **prompts.py**: Prompt generation functions for training. Contains ~50 prompt templates (e.g., `chatgpt_custom_animal`, `chatgpt_custom_instruments`, `nouns_activities`). Functions return `(prompt_text, metadata_dict)`.

- **aesthetic_scorer.py**: CLIP-based aesthetic scorer using MLPDiff head trained on AVA dataset. Scores individual video frames for visual aesthetic quality.

- **actpred_scorer.py**: VideoMAE-based action prediction scorer for text-video alignment. Maps actions to Kinetics-400 class labels and returns loss/score for alignment.

- **compression_scorer.py**: Custom compression quality scorer.

- **weather_scorer.py**: Weather-specific reward scoring.

### Reward Functions

The system supports multiple reward functions selectable via `--reward_fn`:
- `aesthetic`: Image aesthetic scoring (CLIP + MLP)
- `hps`: Human Preference Score v2 (text-video alignment)
- `pick_score`: PickScore for preference alignment
- `actpred`: Action prediction scoring (requires `decode_frame` in `['fml', 'all', 'alt']`)
- `objectDetection`: YOLO/GroundingDINO-based object detection
- `aesthetic_hps`: Combined aesthetic + HPS

### Key Training Concepts

**LoRA Training:** All implementations use Low-Rank Adaptation for efficient fine-tuning. Key parameters:
- `--lora_rank`: Rank of LoRA matrices (8-16 typical)
- `--lora_ckpt_path`: Path to pretrained LoRA weights
- `use_unet_lora`/`use_text_lora`: Which components to adapt

**Backprop Modes (VideoCrafter):** Controls when gradient is gathered during DDIM sampling:
- `last`: Gradient at final DDIM step
- `rand`: Gradient at random step
- `specific`: Gradient at step 15

**Frame Decoding:** Controls which frames to decode for reward computation:
- `-1` (int): Random frame, or specific frame index
- `fml`: First, middle, last frames
- `all`: All frames
- `alt`: Alternate frames

### Model-Specific Structures

**VADER-VideoCrafter:** Built on VideoCrafter2 with custom DDIMSampler for gradient-based training.
- Main training: `scripts/main/train_t2v_lora.py`
- Sampling: `lvdm/models/samplers/ddim.py` (modified for backprop_mode)
- Models: `lvdm/models/` (autoencoder, ddpm3d, attention modules)

**VADER-ModelScope:** Built on ModelScope diffusers with custom pipeline (`ms_custom.py`).
- Main training: `train_t2v_lora.py`
- Custom pipeline: `ms_custom.py` with `train_policy()` method
- Utilities: `utils/lora_handler.py` for LoRA management

**VADER-Open-Sora:** Built on Open-Sora v1.2 with DiT-based architecture.
- Main training: `scripts/train_t2v_lora.py`
- Configs: `configs/opensora-v1-2/vader/` (vader_train.py, vader_inference.py)
- Models: `opensora/models/` (dit, pixart, stdit variants)

### Configuration

- **VideoCrafter**: Command-line arguments via argparse
- **ModelScope**: Hydra config in `config_t2v/config.yaml`
- **Open-Sora**: Hydra configs in `configs/opensora-v1-2/vader/`

### Logging & Checkpoints

- **Weights & Biases**: Enabled via `--use_wandb` with `--wandb_entity` optional
- Checkpoints saved at `--checkpointing_steps` intervals
- Validation videos sampled at `--validation_steps` intervals

## Pretrained Models

- **VideoCrafter2**: `checkpoints/base_512_v2/model.ckpt` (auto-downloaded from HuggingFace)
- **LoRA Weights**: Available on HuggingFace under `zheyangqin/VADER_VideoCrafter_*`
  - `vader_videocrafter_pickscore.pt` (PickScore, lora_rank=16)
  - `vader_videocrafter_hps_aesthetic.pt` (HPS+Aesthetic, lora_rank=8)

## Key Dependencies

- PyTorch 2.x with CUDA 12.1
- diffusers, accelerate, transformers
- xformers for memory-efficient attention
- open_clip_torch (HPSv2)
- wandb for logging
- decord for video loading
- hydra for configuration management