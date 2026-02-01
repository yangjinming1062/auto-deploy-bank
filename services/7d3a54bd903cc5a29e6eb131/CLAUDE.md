# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**LlamaGen** - An autoregressive image generation model that applies the "next-token prediction" paradigm of LLaMA to visual generation. Uses VQ-VAE tokenizers to convert images to discrete tokens, then trains GPT-style transformers to predict tokens autoregressively.

## Development Commands

```bash
# Install dependencies
pip install torch>=2.1.0

# Train VQ-VAE tokenizer
bash scripts/tokenizer/train_vq.sh --cloud-save-path /path/to/cloud_disk --data-path /path/to/imagenet/train --image-size 256 --vq-model VQ-16

# Pre-extract discrete codes for training (required before AR model training)
bash scripts/autoregressive/extract_codes_c2i.sh --vq-ckpt ./pretrained_models/vq_ds16_c2i.pt --data-path /path/to/imagenet/train --code-path /path/to/output --ten-crop --image-size 384

# Train AR model with DDP (for smaller models like GPT-B, L, XL)
bash scripts/autoregressive/train_c2i.sh --cloud-save-path /path/to/cloud_disk --code-path /path/to/codes --image-size 384 --gpt-model GPT-L

# Train AR model with FSDP (for larger models like XXL, 3B)
bash scripts/autoregressive/train_c2i_fsdp.sh --cloud-save-path /path/to/cloud_disk --code-path /path/to/codes --image-size 384 --gpt-model GPT-XXL

# Sampling/inference
bash scripts/autoregressive/sample_c2i.sh --vq-ckpt ./pretrained_models/vq_ds16_c2i.pt --gpt-ckpt ./pretrained_models/c2i_L_384.pt --gpt-model GPT-L --image-size 384

# Run Gradio demo locally
python app.py

# Evaluation
python3 evaluations/c2i/evaluator.py VIRTUAL_imagenet256_labeled.npz samples/xxx.npz
```

## Architecture

### Pipeline Overview
1. **Image Tokenization**: VQ-VAE encoder compresses images to discrete tokens
2. **Autoregressive Generation**: GPT-style transformer predicts tokens conditioned on class/text
3. **Image Reconstruction**: VQ-VAE decoder converts tokens back to images

### Key Modules

| Directory | Purpose |
|-----------|---------|
| `tokenizer/` | VQ-VAE models (vqgan/, vae/, consistencydecoder/) for image tokenization |
| `autoregressive/models/` | GPT model implementations with 2D rotary positional embeddings |
| `autoregressive/train/` | DDP/FSDP training loops for AR models |
| `autoregressive/sample/` | Sampling/inference code with KV-cache support |
| `autoregressive/serve/` | vLLM serving integration for high-throughput inference |
| `dataset/` | Data loaders for ImageNet, COCO, Pexels, OpenImages |
| `utils/` | Distributed training setup, EMA, logging, dropout utilities |
| `language/` | T5 feature extraction for text-conditional generation |

### Model Variants

**Class-conditional (c2i):**
- `GPT-B`: 111M params (12 layers, 768 dim, 12 heads)
- `GPT-L`: 343M params (24 layers, 1024 dim, 16 heads)
- `GPT-XL`: 775M params (36 layers, 1280 dim, 20 heads)
- `GPT-XXL`: 1.4B params (48 layers, 1536 dim, 24 heads)
- `GPT-3B`: 3.1B params (24 layers, 3200 dim, 32 heads)

**Text-conditional (t2i):**
- `GPT-7B`: 6.6B params (32 layers, 4096 dim, 32 heads)

### Key Implementation Details

- **2D Rotary Positional Embeddings**: `precompute_freqs_cis_2d()` in `autoregressive/models/gpt.py` handles spatial position encoding for image tokens
- **KV-Cache**: Enabled in inference for efficient autoregressive decoding
- **FSDP Support**: Larger models (XXL, 3B) use FullyShardedDataParallel via `get_fsdp_wrap_module_list()`
- **Classifier-Free Guidance**: Implemented in `LabelEmbedder` and `CaptionEmbedder` with dropout

## Distributed Training Configuration

Edit these environment variables in training scripts before running:
- `nnodes`: Number of nodes
- `nproc_per_node`: GPUs per node
- `node_rank`: Current node rank
- `master_addr`: Master node IP
- `master_port`: Master node port

## Model Checkpoint Loading

The code handles multiple checkpoint formats:
- DDP: `checkpoint["model"]`
- FSDP: direct state dict
- DeepSpeed: `checkpoint["module"]`
- Legacy: `checkpoint["state_dict"]`

Use `--from-fsdp` flag when loading FSDP checkpoints.