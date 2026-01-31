# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VAR (Visual Autoregressive Modeling) introduces a new autoregressive paradigm for image generation that uses **next-scale prediction** (coarse-to-fine) instead of the standard raster-scan "next-token prediction". This GPT-style approach surpasses diffusion models and exhibits power-law scaling laws.

## Architecture

The system has two main components:

### VQVAE (models/vqvae.py, models/quant.py)
- Vector Quantized VAE that encodes images into token pyramids
- Uses `VectorQuantizer2` for discrete tokenization with a vocab size of 4096
- Encoder/Decoder with residual blocks and self-attention
- Operates at multiple scales via `v_patch_nums` (e.g., `(1, 2, 3, 4, 5, 6, 8, 10, 13, 16)`)
- Output: List of token indices per scale, or continuous embeddings

### VAR (models/var.py, models/basic_var.py)
- Autoregressive transformer that predicts tokens scale-by-scale
- Uses AdaLN (Adaptive Layer Normalization) conditioned on class labels
- Supports classifier-free guidance (CFG) during inference
- Key attention mechanisms:
  - Flash Attention and xFormers for efficient attention
  - L2-normalized attention option (`attn_l2_norm`)
  - KV caching for fast autoregressive inference
- Backward-compatible with HuggingFace Hub via `VARHF` class

### Training Components
- **dist.py**: Distributed training utilities (DDP, world size, rank management)
- **trainer.py**: `VARTrainer` class handling forward pass, loss computation, evaluation
- **train.py**: Main training loop with progressive training support
- **utils/arg_util.py**: Comprehensive hyperparameter configuration via `typed-argument-parser`

## Commands

### Installation
```bash
pip3 install -r requirements.txt
# Optional: install flash-attn and xformers for faster attention
```

### Training
All training commands use `torchrun` for distributed training:

```bash
# VAR-d16 (310M params), 256x256
torchrun --nproc_per_node=8 train.py --depth=16 --bs=768 --ep=200 --fp16=1 --data_path=/path/to/imagenet

# VAR-d20 (600M params)
torchrun --nproc_per_node=8 train.py --depth=20 --bs=768 --ep=250 --fp16=1 --data_path=/path/to/imagenet

# VAR-d24 (1.0B params)
torchrun --nproc_per_node=8 train.py --depth=24 --bs=768 --ep=350 --fp16=1 --alng=1e-4 --wpe=0.01 --data_path=/path/to/imagenet

# VAR-d30 (2.0B params)
torchrun --nproc_per_node=8 train.py --depth=30 --bs=1024 --ep=350 --fp16=1 --alng=1e-5 --wpe=0.01 --twde=0.08 --data_path=/path/to/imagenet

# VAR-d36-s for 512x512 (shared AdaLN)
torchrun --nproc_per_node=8 train.py --depth=36 --saln=1 --pn=512 --bs=768 --ep=350 --fp16=1 --data_path=/path/to/imagenet
```

Key training arguments:
- `--depth`: Transformer depth (model size)
- `--bs`: Global batch size
- `--ep`: Number of epochs
- `--fp16`: Use FP16 mixed precision (set to 2 for BF16)
- `--data_path`: Path to ImageNet dataset
- `--pn`: Patch numbers config ('256' or '512' shortcuts, or custom like '1_2_3_4_5_6_8_10_13_16')
- `--saln`: Use shared AdaLN (for high-res models)
- `--tfast`: torch.compile VAR (1: reduce-overhead, 2: max-autotune)

### Inference / Sampling
See `demo_sample.ipynb` for complete examples:

```python
from models import build_vae_var
import torch

# Build models
vae, var = build_vae_var(
    V=4096, Cvae=32, ch=160, share_quant_resi=4,
    device=device, patch_nums=(1, 2, 3, 4, 5, 6, 8, 10, 13, 16),
    num_classes=1000, depth=MODEL_DEPTH,
)

# Load checkpoints
vae.load_state_dict(torch.load('vae_ch160v4096z32.pth', map_location='cpu'))
var.load_state_dict(torch.load(f'var_d{MODEL_DEPTH}.pth', map_location='cpu'))

# Sample with CFG
with torch.inference_mode(), torch.autocast('cuda', enabled=True, dtype=torch.float16):
    recon_B3HW = var.autoregressive_infer_cfg(
        B=batch_size,
        label_B=label_B,  # ImageNet class labels
        cfg=4.0,          # Classifier-free guidance strength
        top_k=900,
        top_p=0.95,
        g_seed=seed,
    )
```

### Checkpoints

Pre-trained checkpoints available on HuggingFace (`FoundationVision/var`):
- `vae_ch160v4096z32.pth` - VQVAE (required)
- `var_d16.pth` - 310M params
- `var_d20.pth` - 600M params
- `var_d24.pth` - 1.0B params
- `var_d30.pth` - 2.0B params
- `var_d36.pth` - 2.3B params (512x512)

Checkpoints are saved to `local_output/ar-ckpt-*.pth` during training.

### TensorBoard
```bash
tensorboard --logdir=local_output/
```

## Model Variants

| Model | Resolution | FID | #params | Notes |
|-------|------------|-----|---------|-------|
| VAR-d16 | 256 | 3.55 | 310M | Lightweight |
| VAR-d20 | 256 | 2.95 | 600M | |
| VAR-d24 | 256 | 2.33 | 1.0B | |
| VAR-d30 | 256 | 1.97 | 2.0B | |
| VAR-d30-re | 256 | **1.80** | 2.0B | Refined |
| VAR-d36 | 512 | **2.63** | 2.3B | High-res |

## Key Code Patterns

### Progressive Training
VAR supports progressive training where the model learns from coarse to fine scales. Set via `--pg` (fraction of training) and `--pg0` (starting scale index).

### Distributed Training
- Uses PyTorch DDP with NCCL backend
- Environment variables `RANK`, `WORLD_SIZE` control distribution
- Auto-resumes from checkpoints on interruption
- Custom `DistInfiniteBatchSampler` for efficient sampling

### Mixed Precision
- AMP optimizer in `utils/amp_sc.py`
- Supports FP16 and BF16 via `--fp16` (1 or 2)
- Automatic loss scaling for gradient stability

### Attention Optimizations
- Flash Attention (flash-attn library) - fastest on Ampere+
- xFormers memory-efficient attention
- Fused MLP via `fused_mlp_func`
- Fused layer norm and dropout+add

Enable with `--fuse=True` and install optional dependencies.

## Data Format

ImageNet expected structure:
```
/path/to/imagenet/
  train/
    n01440764/
      many_images.JPEG
    n01443537/
      many_images.JPEG
    ...
  val/
    n01440764/
      ILSVRC2012_val_00000293.JPEG
    ...
```