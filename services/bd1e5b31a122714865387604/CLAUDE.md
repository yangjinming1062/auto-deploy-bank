# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LatentSync is an end-to-end lip-sync method based on audio-conditioned latent diffusion using Stable Diffusion. It lip-syncs videos by:
1. Extracting audio embeddings using OpenAI Whisper (mel spectrogram to features)
2. Conditioning a 3D U-Net on audio via cross-attention layers
3. Using one-step sampling to predict clean latents from noise
4. Reconstructing frames with VAE decode, applying TREPA, LPIPS, and SyncNet losses

## Commonly Used Commands

### Environment Setup
```bash
source setup_env.sh
```
Creates conda environment `latentsync`, installs dependencies, and downloads Whisper/U-Net checkpoints. For training, also download:

```bash
huggingface-cli download ByteDance/LatentSync-1.6 stable_syncnet.pt --local-dir checkpoints
```

### Inference

**Minimum VRAM:** 8 GB (v1.5) / 18 GB (v1.6)

```bash
# Gradio UI
python gradio_app.py

# CLI (example with demo assets)
./inference.sh

# Custom inference
python -m scripts.inference \
    --unet_config_path "configs/unet/stage2_512.yaml" \
    --inference_ckpt_path "checkpoints/latentsync_unet.pt" \
    --inference_steps 20 \
    --guidance_scale 1.5 \
    --enable_deepcache \
    --video_path "path/to/video.mp4" \
    --audio_path "path/to/audio.wav" \
    --video_out_path "output.mp4"

# Key parameters:
#   --inference_steps [20-50]: Higher = better visual quality, slower
#   --guidance_scale [1.0-3.0]: Higher = better lip-sync, may cause distortion
#   --enable_deepcache: Use DeepCache for faster inference (~2x speedup)
```

### Training

**U-Net Training:**
```bash
# Multi-GPU distributed training
./train_unet.sh

# With custom config
torchrun --nnodes=1 --nproc_per_node=1 --master_port=25679 -m scripts.train_unet \
    --unet_config_path "configs/unet/stage1_512.yaml"
```
**U-Net Configs (VRAM requirements):**

| Config | VRAM | Use Case |
|--------|------|----------|
| `stage1.yaml` | 23 GB | Initial training |
| `stage2.yaml` | 30 GB | Full training (optimal) |
| `stage2_efficient.yaml` | 20 GB | Consumer GPUs (RTX 3090) |
| `stage1_512.yaml` | 30 GB | 512px resolution |
| `stage2_512.yaml` | 55 GB | 512px full training |

All configs in `configs/unet/`.

**SyncNet Training:**
```bash
./train_syncnet.sh

torchrun --nnodes=1 --nproc_per_node=1 --master_port=25678 -m scripts.train_syncnet \
    --config_path "configs/syncnet/syncnet_16_pixel_attn.yaml"
```

### Data Processing Pipeline
```bash
./data_processing_pipeline.sh
```
Modifies parameters: `--total_num_workers`, `--per_gpu_num_workers`, `--resolution`, `--sync_conf_threshold`, `--input_dir`. Outputs go to `high_visual_quality/` directory.

### Evaluation
```bash
# Sync confidence score of generated video
./eval/eval_sync_conf.sh

# SyncNet accuracy on dataset
./eval/eval_syncnet_acc.sh
```

## Architecture

```
LatentSync/
├── latentsync/
│   ├── models/
│   │   ├── unet.py              # UNet3DConditionModel - 3D U-Net with cross-attention
│   │   ├── stable_syncnet.py    # StableSyncNet - audio-visual sync discriminator
│   │   ├── motion_module.py     # Temporal self-attention for video generation
│   │   └── attention.py         # Custom attention blocks
│   ├── pipelines/
│   │   └── lipsync_pipeline.py  # Inference pipeline: reads video/audio, runs diffusion
│   ├── data/
│   │   ├── unet_dataset.py      # Training dataset with masked frames
│   │   └── syncnet_dataset.py   # SyncNet training data
│   ├── whisper/
│   │   ├── whisper/             # OpenAI Whisper model (frozen)
│   │   └── audio2feature.py     # Audio to mel spectrogram embeddings
│   ├── utils/
│   │   ├── face_detector.py     # Face detection via InsightFace
│   │   ├── affine_transform.py  # Face alignment using landmarks
│   │   └── av_reader.py         # Video/audio loading
│   └── trepa/
│       └── loss.py              # TREPA temporal perceptual loss
├── eval/
│   ├── syncnet/                 # SyncNet evaluation tools
│   └── eval_sync_conf.py        # Sync confidence scoring
├── preprocess/                  # Data pipeline stages (fps resampling, scene detection, etc.)
├── configs/
│   ├── unet/                    # U-Net training configs (stage1, stage2 variants)
│   └── syncnet/                 # SyncNet architecture configs
└── scripts/
    ├── train_unet.py
    ├── train_syncnet.py
    └── inference.py
```

## Key Configuration Points

- **U-Net input**: 13 channels = noised_latent(4) + mask(1) + masked_latent(4) + ref_latent(4)
- **VAE**: `stabilityai/sd-vae-ft-mse`, scaling_factor=0.18215, shift_factor=0
- **Whisper model**: `tiny.pt` (384 dim) or `small.pt` (768 dim) based on `cross_attention_dim`
- **SyncNet**: Used for both training supervision (cosine loss) and evaluation; runs in pixel or latent space

## Training Details

- **Distributed training**: Uses `torchrun` with DDP; `init_dist()` handles setup
- **Mixed precision**: Enabled via `GradScaler` when `mixed_precision_training: true`
- **Gradient checkpointing**: Enabled via `enable_gradient_checkpointing: true`
- **Loss components**: recon_loss + sync_loss + lpips_loss + trepa_loss (weights in config)
- **Validation**: Saves validation videos and sync confidence charts periodically

## Checkpoints Structure
```
checkpoints/
├── latentsync_unet.pt          # Main U-Net model
├── stable_syncnet.pt           # SyncNet for training supervision
├── whisper/
│   ├── tiny.pt                 # Whisper audio encoder (384-dim, default)
│   └── small.pt                # Whisper audio encoder (768-dim)
└── auxiliary/syncnet_v2.model  # SyncNet for evaluation
```