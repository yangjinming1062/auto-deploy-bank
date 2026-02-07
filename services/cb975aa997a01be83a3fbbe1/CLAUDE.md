# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains code for 1D visual tokenization and generation models:
- **TiTok**: Compact 1D tokenizer that represents images with as few as 32 tokens
- **TA-TiTok**: Text-aware version of TiTok that handles both discrete and continuous tokens
- **MaskGen**: Text-to-image masked generative model built on TA-TiTok
- **RAR**: Randomized Autoregressive visual generation with LLM compatibility

## Installation

```bash
pip3 install -r requirements.txt
```

## Common Commands

### Training

All training uses `accelerate` for distributed training. Replace model-specific configs and parameters as needed.

```bash
# TiTok Stage 1 (tokenizer training)
WANDB_MODE=offline accelerate launch --num_machines=1 --num_processes=8 \
  --machine_rank=0 --main_process_ip=127.0.0.1 --main_process_port=9999 \
  --same_network scripts/train_titok.py config=configs/training/TiTok/stage1/titok_b64.yaml \
  experiment.project="titok_b64_stage1" \
  experiment.name="titok_b64_stage1_run1" \
  experiment.output_dir="titok_b64_stage1_run1"

# TiTok Stage 2 (decoder finetuning)
# Add: experiment.init_weight=${PATH_TO_STAGE1_WEIGHT}

# TiTok Generator training
WANDB_MODE=offline accelerate launch --num_machines=4 --num_processes=32 \
  --machine_rank=${MACHINE_RANK} --main_process_ip=${ROOT_IP} \
  --main_process_port=${ROOT_PORT} --same_network \
  scripts/train_maskgit.py config=configs/training/generator/maskgit.yaml \
  experiment.project="titok_generation" \
  experiment.name="titok_b64_maskgit" \
  experiment.output_dir="titok_b64_maskgit" \
  experiment.tokenizer_checkpoint=${PATH_TO_STAGE1_or_STAGE2_WEIGHT}

# RAR training
WANDB_MODE=offline accelerate launch --num_machines=4 --num_processes=32 \
  --machine_rank=${MACHINE_RANK} --main_process_ip=${ROOT_IP} \
  --main_process_port=${ROOT_PORT} --same_network \
  scripts/train_rar.py config=configs/training/generator/rar.yaml \
  experiment.project="rar" \
  experiment.name="rar_xxl" \
  experiment.output_dir="rar_xxl" \
  model.generator.hidden_size=1408 \
  model.generator.num_hidden_layers=40

# TA-TiTok training
WANDB_MODE=offline accelerate launch --num_machines=4 --num_processes=8 \
  --machine_rank=0 --main_process_ip=127.0.0.1 --main_process_port=9999 \
  --same_network scripts/train_tatitok.py \
  config=configs/training/TA-TiTok/tatitok_bl32_vae.yaml \
  experiment.project="tatitok_bl32_vae" \
  experiment.name="tatitok_bl32_vae_run1"

# MaskGen training (Stage 1 and Stage 2)
WANDB_MODE=offline accelerate launch --num_machines=4 --num_processes=8 \
  --machine_rank=0 --main_process_ip=127.0.0.1 --main_process_port=9999 \
  --same_network scripts/train_maskgen.py \
  config=configs/training/MaskGen/maskgen_vq_xl_stage1.yaml \
  experiment.project="maskgen_vq_xl_stage1"
```

### Evaluation/Sampling on ImageNet

```bash
# Prepare evaluation tools
git clone https://github.com/openai/guided-diffusion.git
wget https://openaipublic.blob.core.windows.net/diffusion/jul-2021/ref_batches/imagenet/256/VIRTUAL_imagenet256_labeled.npz

# TiTok sampling
torchrun --nnodes=1 --nproc_per_node=8 --rdzv-endpoint=localhost:9999 \
  sample_imagenet_titok.py config=configs/infer/TiTok/titok_l32.yaml \
  experiment.output_dir="titok_l_32"

# RAR sampling
torchrun --nnodes=1 --nproc_per_node=8 --rdzv-endpoint=localhost:9999 \
  sample_imagenet_rar.py config=configs/training/generator/rar.yaml \
  experiment.output_dir="rar_xxl" \
  experiment.generator_checkpoint="rar_xxl.bin" \
  model.generator.hidden_size=1408

# Run FID evaluation
python3 guided-diffusion/evaluations/evaluator.py VIRTUAL_imagenet256_labeled.npz titok_l_32.npz
```

### Pretokenization

```bash
# For faster training, pretokenize dataset
python scripts/pretokenization.py
```

## Code Architecture

### Model Files (`modeling/`)

| File | Purpose |
|------|---------|
| `titok.py` | TiTok 1D tokenizer (VQ or VAE modes) |
| `tatitok.py` | Text-aware TiTok with CLIP text guidance |
| `maskgen.py` | MaskGen VQ/KL generators for text-to-image |
| `maskgit.py` | ImageBert/UViTBert for class-conditional generation |
| `rar.py` | Randomized Autoregressive generator with KV-cache |
| `modules/blocks.py` | Transformer blocks (TiTokEncoder, TiTokDecoder, etc.) |
| `modules/losses.py` | Reconstruction losses, MLM loss, AR loss |
| `modules/maskgit_vqgan.py` | Pixel-level VQGAN for decoder finetuning |
| `quantizer/quantizer.py` | VectorQuantizer, DiagonalGaussianDistribution |

### Training Infrastructure (`scripts/` and `utils/`)

- `scripts/train_*.py`: Training entry points
- `utils/train_utils.py`: Core training utilities (dataloaders, optimizers, schedulers)
- `utils/logger.py`: Logging setup
- `utils/lr_schedulers.py`: Learning rate schedulers
- `data/`: WebDataset readers for ImageNet

### Configuration (`configs/`)

- YAML configs with OmegaConf for structured hyperparameters
- `configs/training/` contains model-specific training configs
- `configs/infer/` contains inference configs
- Override configs via CLI: `script.py config=base.yaml model.param=value`

### Key Configuration Sections

```yaml
experiment:      # Project name, output directory, logging
model:           # Model architecture (vq_model, maskgen, generator)
losses:          # Loss weights
dataset:         # Data paths, preprocessing, augmentation
optimizer:       # AdamW params (lr, betas, weight_decay)
lr_scheduler:    # Cosine/scheduler params
training:        # Batch size, epochs, mixed precision, EMA settings
```

## Model Patterns

### Quantization Modes
- `vq`: Vector quantization with discrete codebook
- `vae`: Diagonal Gaussian distribution (continuous tokens)

### Two-Stage Training
1. **Stage 1**: Train full encoder+quantizer
2. **Stage 2**: Freeze encoder, finetune decoder with pixel VQGAN

### Text Encoding (MaskGen/TA-TiTok)
Uses OpenCLIP ViT-L-14-336 for text encoding, passed as guidance to generator.

### Distributed Training
Uses `accelerate` with:
- Multi-machine GPU training
- Mixed precision (fp16/bf16)
- Gradient checkpointing for memory efficiency
- EMA (Exponential Moving Average) for model smoothing

## Loading Pretrained Models

All models inherit from `PyTorchModelHubMixin` for HF Hub integration:

```python
from modeling.titok import TiTok
tokenizer = TiTok.from_pretrained("yucornetto/tokenizer_titok_l32_imagenet")

from modeling.maskgen import MaskGen_VQ
generator = MaskGen_VQ.from_pretrained("turkeyju/generator_maskgen_vq_xl")
```

Models also support loading from local `.bin` checkpoints via `load_state_dict()`.