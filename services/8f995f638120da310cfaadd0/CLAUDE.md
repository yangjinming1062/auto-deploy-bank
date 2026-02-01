# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Infinity is a Bitwise Visual AutoRegressive (VAR) Modeling system for high-resolution text-to-image synthesis. Key innovations:
- **Infinite-Vocabulary Tokenizer**: Bitwise multi-scale residual quantizer with configurable vocab sizes ($V_d=2^{16}, 2^{24}, 2^{32}, 2^{64}$)
- **Infinite-Vocabulary Classifier**: Predicts $d$ bits instead of $2^d$ indices, reducing parameters from 8.8T to 0.13M (d=32, h=2048)
- **Bitwise Self-Correction (BSC)**: Applies noise to intermediate features during training to mitigate train-test discrepancy

Model sizes: 125M, 1B, 2B, 8B parameters. Resolutions: 256×256 (0.06M), 512×512 (0.25M), 1024×1024 (1M pixels).

## Commands

### Installation
```bash
pip3 install -r requirements.txt  # Requires torch>=2.5.1 for FlexAttention
```

### Training
```bash
# Single node training (development)
SINGLE=1 bash scripts/train.sh

# Multi-node distributed training
bash scripts/train.sh

# Fine-tuning from pretrained checkpoint
# Add --rush_resume=[path/to/infinity_2b_reg.pth] to train.sh
```

### Evaluation
```bash
bash scripts/eval.sh  # Supports GenEval, ImageReward, HPSv2.1, FID, validation loss

# Individual benchmarks:
test_gen_eval      # Object composition and spatial relationships
infer_eval_hpsv21  # Human preference scoring v2.1
infer_eval_image_reward  # ImageReward model scoring
test_fid           # Fréchet Inception Distance
test_val_loss      # Validation loss computation
```

### Inference
```bash
# Command line
python3 tools/comprehensive_infer.py --cfg 4 --pn 1M --model_path weights/infinity_2b_reg.pth ...

# Interactive Jupyter notebooks
jupyter notebook tools/interactive_infer.ipynb       # Infinity-2B
jupyter notebook tools/interactive_infer_8b.ipynb    # Infinity-8B

# Docker reproduction
docker build -t my-flash-attn-env .
python tools/reproduce.py
```

### Configuration
Set API tokens and cache paths in `conf.py`:
```python
HF_TOKEN = '[YOUR HF_TOKEN]'
HF_HOME = '[YOUR HF_HOME]'
GPT_AK = '[YOUR GPT_AK]'  # OpenAI API key for prompt rewriting
```

## Architecture

### Core Components (`infinity/`)

- **models/infinity.py**: Main `Infinity` transformer with next-scale prediction autoregressive head, RoPE 2D positional encoding, AdaLin normalization
- **models/bsq_vae/**: Bitwise Scalar Quantization VAE (`vae.py`) with multi-scale residual quantizer (`multiscale_bsq.py`)
- **models/bitwise_self_correction.py**: BSC module applying noise to intermediate features during training
- **models/ema.py**: Exponential Moving Average for model weights
- **models/t5.py**: T5 text encoder wrapper (Flan-T5-XL by default)
- **dataset/dataset_t2i_iterable.py**: Streaming-compatible iterable dataset for >100M examples
- **utils/dynamic_resolution.py**: Aspect ratio templates and scale schedules for progressive generation
- **utils/dist.py**: DDP/FSDP distributed training setup and utilities
- **utils/save_and_load.py**: Checkpoint management with auto-resume from `local_output/ckpt*.pth`

### Inference Flow

`predict.py` → `tools/run_infinity.py` → `gen_one_img()`:
1. Encode prompt with T5-XL text encoder → (k, v, cu_seqlens_k, Ltext)
2. Progressive autoregressive generation across scale schedule with classifier-free guidance
3. Decode tokens through VAE decoder to produce final image

### Dynamic Resolution

Aspect ratio templates (`h_div_w` values): 1.000, 1.250, 1.333, 1.500, 1.750, 2.000, 2.500, 3.000 (plus inverses). Each maps to multi-scale token schedules that progressively increase resolution during generation.

### Training Pipeline (`train.py` → `trainer.py`)

1. `build_everything_from_args()`: Initializes VAE, GPT, optimizer, dataloaders
2. `main_train()`: Epoch loop with evaluation checkpoints
3. `train_one_ep()`: Iterates through dataloader, calls `trainer.train_step()`
4. `InfinityTrainer.train_step()`: Forward pass with VAE encoding, BSC, GPT inference, loss computation, backward pass

### Key Classes

- **InfinityTrainer** (`trainer.py`): Handles training loop, EMA updates, checkpointing, distributed sync
- **Infinity** (`infinity/models/infinity.py`): Transformer with next-scale prediction autoregressive head

## Model Configurations

| Model | Depth | Embed Dim | Args Model Name |
|-------|-------|-----------|-----------------|
| 125M  | 12    | 768       | `layer12c4`     |
| 1B    | 24    | 1536      | `layer24c4`     |
| 2B    | 32    | 2048      | `2bc8`          |
| 8B    | 40    | 2688      | `2bc8` (scaled) |

### Resolution (`--pn`) and VAE (`--vae_type`)

**Pixel number (`--pn`)** controls output resolution:
- `0.06M`: ~256×256 (13 scales)
- `0.25M`: ~512×512 (13 scales)
- `1M`: ~1024×1024 (13 scales)

**VAE type (`--vae_type`)** sets vocabulary size: 16 (2^16), 24 (2^24), 32 (2^32, recommended), 64 (2^64)

## Distributed Training

- Uses `torchrun` for multi-node training
- Supports **DDP** (`zero=0`) and **FSDP** (`zero=2/3`)
- Auto-resumes from `local_output/ckpt*.pth` on interruption
- Checkpoints saved to both `bed` (remote) and `local_output/` (local)

## Key Arguments

| Argument | Description |
|----------|-------------|
| `--fp16=2` | bf16 mixed precision (2=bf16, 1=fp16) |
| `--use_flex_attn` | Enable FlexAttention for speedup |
| `--tfast` | torch.compile the transformer |
| `--ema_ratio` | Exponential moving average ratio |
| `--use_bit_label` | Use bit-level cross-entropy loss |
| `--use_fsdp_model_ema` | EMA with FSDP |
| `--online_t5` | Use T5 encoder online vs pre-computed features |

## Weights

Required checkpoints (download from HuggingFace FoundationVision/Infinity):
- VAE: `infinity_vae_d32reg.pth` or `infinity_vae_d64.pth`
- Transformer: `infinity_2b_reg.pth` for 2B model
- Text Encoder: `google/flan-t5-xl`

## Data Format

Training dataset: JSONL files named `[h_div_w_template]_[num_examples].jsonl`
```json
{"image_path": "path/to/image", "h_div_w": 1.0, "long_caption": "...", "long_caption_type": "InternVL 2.0"}
```

Optional fields: `text` and `short_caption_type` for short caption training.