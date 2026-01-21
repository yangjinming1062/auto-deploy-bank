# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MOFA-Video is an image animation framework that adapts motion from different domains to a frozen Video Diffusion Model (SVD - Stable Video Diffusion). It supports multiple control modes: trajectory-based, keypoint-based (landmark), and hybrid (trajectory + landmark) control.

## Common Commands

### Environment Setup

```bash
# For inference (Hybrid controls)
cd MOFA-Video-Hybrid
conda create -n mofa python==3.10
conda activate mofa
pip install -r requirements.txt
pip install opencv-python-headless
pip install "git+https://github.com/facebookresearch/pytorch3d.git"

# For training
cd Training
conda create -n mofa_train python==3.10
conda activate mofa_train
pip install -r requirements.txt
```

**Important:** Gradio version must be exactly 4.5.0 - other versions may cause errors.

### Running Inference

```bash
# Hybrid controls - Audio-driven facial animation
cd MOFA-Video-Hybrid && python run_gradio_audio_driven.py

# Hybrid controls - Video-driven facial animation
cd MOFA-Video-Hybrid && python run_gradio_video_driven.py

# Keypoint-based animation
cd MOFA-Video-Keypoint && ./inference.sh

# Trajectory-based animation
cd MOFA-Video-Traj && python run_gradio.py
```

### Training

Training uses a two-stage process. First ensure checkpoints are downloaded (see README.md), then:

```bash
# Stage 1: Base MOFA-Adapter training
cd Training && ./train_stage1.sh

# Stage 2: ControlNet fine-tuning (update --controlnet_model_name_or_path first)
cd Training && ./train_stage2.sh
```

## Architecture

The codebase is organized into three inference modules and one training module:

### MOFA-Video-Hybrid
- Main inference module supporting hybrid (trajectory + landmark) control
- Entry points: `run_gradio_audio_driven.py`, `run_gradio_video_driven.py`
- Core pipeline: `pipeline/pipeline.py` - extends Diffusers' `DiffusionPipeline`
- Models:
  - `models/unet_spatio_temporal_condition_controlnet.py` - Modified UNet with ControlNet support
  - `models/traj_ctrlnet.py` - Trajectory control network (FlowControlNet)
  - `models/ldmk_ctrlnet.py` - Landmark control network (FlowControlNet)
- Third-party integrations:
  - `sadtalker_audio2pose/` / `sadtalker_video2pose/` - Face animation models
  - `aniportrait/` - Audio to landmark conversion

### MOFA-Video-Keypoint
- Keypoint-based facial animation with long video generation support
- Uses periodic sampling strategy for extended videos

### MOFA-Video-Traj
- Trajectory-only control with Gradio interface
- Simpler pipeline for trajectory-based animation

### Training
- `train_stage1.py` - Initial MOFA-Adapter training with SVD backbone
- `train_stage2.py` - ControlNet fine-tuning with flow guidance
- `train_utils/dataset.py` - WebVid10M dataset implementation
- `train_utils/unimatch/` - Optical flow estimation (UniMatch)

## Key Model Components

1. **UNetSpatioTemporalConditionControlNetModel**: Extended from Diffusers' UNet with temporal conditioning and ControlNet hooks
2. **FlowControlNet**: Custom ControlNet for sparse motion fields (trajectory/landmark to flow)
3. **CMP (Conditional Motion Propagation)**: Generates dense motion from sparse hints
4. **Custom Scheduling**: Uses `EulerDiscreteScheduler` with modifications in `utils/scheduling_euler_discrete_karras_fix.py`

## Checkpoint Organization

```
./ckpts/
├── stable-video-diffusion-img2vid-xt-1-1/  # SVD backbone from HuggingFace
│   ├── image_encoder/
│   ├── unet/
│   ├── vae/
│   └── svd_xt_1_1.safetensors
├── controlnet/  # Trained MOFA-Adapter
│   ├── config.json
│   └── diffusion_pytorch_model.safetensors
└── cmp/  # CMP checkpoint
    └── ckpt_iter_42000.pth.tar
```

## Dependencies

Key pinned versions:
- `diffusers==0.24.0`
- `gradio==4.5.0` (strict)
- `torch==2.0.1`
- `torchvision==0.15.2`
- `transformers==4.41.1`
- `accelerate==0.30.1`
- `einops==0.8.0`