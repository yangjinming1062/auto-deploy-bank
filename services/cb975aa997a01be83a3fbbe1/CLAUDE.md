# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository implements 1D visual tokenization and generation models:
- **TiTok**: Compresses 256×256 images into as few as 32 tokens using a 1D tokenizer
- **RAR**: Randomized Autoregressive visual generation with bidirectional context learning
- **MaskGen/TA-TiTok**: Text-to-image masked generation with text-aware tokenization
- **MaskGit**: Masked image generation transformer

## Installation

```bash
pip install -r requirements.txt
```

## Common Commands

### Training

All training scripts use HuggingFace Accelerate for distributed training. Multi-GPU training requires `torchrun`:

```bash
# Single-node multi-GPU training
WANDB_MODE=offline accelerate launch --num_machines=1 --num_processes=8 --machine_rank=0 \
  --main_process_ip=127.0.0.1 --main_process_port=9999 --same_network \
  scripts/train_titok.py config=configs/training/TiTok/stage1/titok_b64.yaml

# Multi-node training
WANDB_MODE=offline accelerate launch --num_machines=4 --num_processes=32 \
  --machine_rank=${MACHINE_RANK} --main_process_ip=${ROOT_IP} --main_process_port=${ROOT_PORT} \
  --same_network scripts/train_rar.py config=configs/training/generator/rar.yaml
```

Key training scripts:
- `scripts/train_titok.py` - TiTok tokenizer training (stage 1 & 2)
- `scripts/train_rar.py` - RAR generator training
- `scripts/train_maskgen.py` - MaskGen text-to-image generation
- `scripts/train_maskgit.py` - MaskGit generator training
- `scripts/train_tatitok.py` - TA-TiTok text-aware tokenizer training

### Sampling/Inference

```bash
# Multi-GPU sampling with torchrun
torchrun --nnodes=1 --nproc_per_node=8 --rdzv-endpoint=localhost:9999 \
  sample_imagenet_rar.py config=configs/training/generator/rar.yaml
```

### Model Configuration

Configs are YAML files using OmegaConf. Override via CLI:
```bash
python script.py config=path/to/config.yaml experiment.output_dir=my_output model.param=value
```

### Data Preparation

- Uses WebDataset format (`*.tar` files)
- Convert ImageNet to wds format using `data/convert_imagenet_to_wds.py`
- Pretokenized data (JSONL format) supported for faster training - see `scripts/pretokenization.py`
- MaskGIT-VQGAN weight (`maskgit-vqgan-imagenet-f16-256.bin`) auto-downloaded during training

## Architecture

```
modeling/
├── titok.py           # TiTok 1D tokenizer (main model class)
├── rar.py             # RAR autoregressive generator
├── maskgen.py         # MaskGen text-to-image model
├── maskgit.py         # MaskGit transformer (ImageBert, UViTBert)
├── tatitok.py         # Text-aware TiTok variant
├── pretokenization.py # Dataset pretokenization utility
└── modules/
    ├── blocks.py      # TiTokEncoder, TiTokDecoder, transformer blocks
    ├── losses.py      # Reconstruction, MLM, AR loss functions
    ├── discriminator.py # VQGAN discriminator
    ├── ema_model.py   # Exponential moving average wrapper
    └── maskgit_vqgan.py # MaskGIT-VQGAN encoder/decoder/quantizer

modeling/quantizer/
└── quantizer.py       # VectorQuantizer, DiagonalGaussianDistribution

utils/
├── train_utils.py     # Core training utilities (model creation, optimizer, dataloader)
├── lr_schedulers.py   # Cosine scheduler with warmup
└── viz_utils.py       # Visualization utilities

evaluator/
├── evaluator.py       # VQGANEvaluator (FID, Inception Score)
└── inception.py       # Inception network for evaluation

data/
└── webdataset_reader.py # WebDataset loaders
```

## Key Training Patterns

- **Two-stage training**: TiTok uses stage 1 (encoder training) and stage 2 (decoder finetuning)
- **EMA**: Models use exponential moving average (toggle with `config.training.use_ema`)
- **Mixed precision**: fp16/bf16 supported via `config.training.mixed_precision`
- **Checkpoint resume**: Auto-resumes from `output_dir/checkpoint_*`
- **TF32**: Enable with `config.training.enable_tf32` for Ampere GPUs

## Model Hub Integration

Models support HuggingFace HubMixin for easy loading:
```python
from modeling.titok import TiTok
tokenizer = TiTok.from_pretrained("yucornetto/tokenizer_titok_l32_imagenet")
```

## Evaluation

For FID evaluation, use OpenAI's guided-diffusion evaluator:
```bash
python3 guided-diffusion/evaluations/evaluator.py VIRTUAL_imagenet256_labeled.npz generated_samples.npz
```