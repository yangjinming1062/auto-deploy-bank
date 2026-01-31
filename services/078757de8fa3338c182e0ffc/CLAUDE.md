# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BAGEL is a unified multimodal foundation model (7B active, 14B total parameters) with Mixture-of-Transformer-Experts (MoT) architecture. It supports three core capabilities:
- **Visual Understanding (VLM)**: Image/video question answering, multimodal reasoning
- **Text-to-Image Generation**: High-quality image synthesis from text prompts
- **Image Editing**: Free-form visual manipulation with in-context conditioning

## Commands

### Setup
```bash
conda create -n bagel python=3.10 -y
conda activate bagel
pip install -r requirements.txt
pip install flash_attn==2.5.8 --no-build-isolation

# Download pretrained checkpoint
python -c "from huggingface_hub import snapshot_download; snapshot_download(cache_dir='models/BAGEL-7B-MoT/cache', local_dir='models/BAGEL-7B-MoT', repo_id='ByteDance-Seed/BAGEL-7B-MoT', local_dir_use_symlinks=False, resume_download=True, allow_patterns=['*.json', '*.safetensors', '*.bin', '*.py', '*.md', '*.txt'])"
```

### Inference
```bash
# Full GPU (32GB+ VRAM)
python app.py

# NF4 quantization (12-32GB VRAM)
python app.py --mode 2

# INT8 quantization (22-32GB VRAM)
python app.py --mode 3

# Chinese UI with NF4 quantization
python app.py --mode 2 --zh
```

### Training
```bash
# Using the train script wrapper
bash scripts/train.sh

# Or direct torchrun
torchrun --nnodes=$num_nodes --node_rank=$node_rank --nproc_per_node=8 \
  --master_addr=$master_addr --master_port=$master_port \
  train/pretrain_unified_navit.py \
  --dataset_config_file ./data/configs/example.yaml \
  --llm_path $llm_path --vae_path $vae_path --vit_path $vit_path \
  --layer_module Qwen2MoTDecoderLayer --use_flex True \
  --results_dir $output_path --checkpoint_dir $ckpt_path \
  --max_latent_size 64
```

Key hyperparameters: `--lr 2e-5`, `--num_worker 1`, `--finetune_from_hf True`, `--visual_gen/visual_und` flags for task-specific training.

### Evaluation
```bash
# VLM benchmarks
bash scripts/eval/run_eval_vlm.sh

# GenEval (image generation)
bash scripts/eval/run_geneval.sh

# Image editing benchmarks
bash scripts/eval/run_gedit.sh       # GEdit-Bench
bash scripts/eval/run_imgedit.sh     # ImgEdit-Bench
bash scripts/eval/run_kris.sh        # KRIS-Bench (reasoning)
bash scripts/eval/run_rise.sh        # RISEBench
bash scripts/eval/run_wise.sh        # WISE (image quality)
```

## Architecture

### Core Model (`modeling/bagel/`)
- **bagel.py**: Main `Bagel` class with dual-branch architecture (visual_gen + visual_und). Handles interleaved multimodal sequences, preparation methods for VAE/ViT inputs, and cache management.
- **qwen2_navit.py**: `Qwen2MoTDecoderLayer` - MoT decoder layer with token-level routing for experts. Also contains `NaiveCache` for KV cache management during inference.
- **siglip_navit.py**: SigLIP ViT encoder adapted for visual understanding.

### Autoencoder (`modeling/autoencoder.py`)
VAE for latent diffusion in image generation. Loaded via `load_ae()`.

### Inference Engine (`inferencer.py`)
`InterleaveInferencer` class manages multimodal generation:
- Text/image context updates via `update_context_text/image()`
- Image generation with CFG support (`gen_image()`)
- Text generation (`gen_text()`)
- Full interleaved inference (`interleave_inference()`)

Key parameters: `cfg_text_scale` (4.0-8.0), `cfg_image_scale` (1.0-2.0), `cfg_interval`, `cfg_renorm_type`, `timestep_shift`, `num_timesteps`.

### Training (`train/`)
- **pretrain_unified_navit.py**: Main training script using FSDP with hybrid sharding (`HYBRID_SHARD`, 8 shards per rank). Handles both pre-training and fine-tuning workflows.
- **fsdp_utils.py**: FSDP checkpointing and EMA (Exponential Moving Average) utilities.
- **dataset_base.py**: `PackedDataset` with FLEX packing for efficient batch compilation (set `use_flex=True` in training).

### Data Configuration (`data/configs/*.yaml`)
YAML configs define dataset names, transform arguments, sampling weights. Each dataset type:
- `t2i_pretrain`: Text-to-image (parquet)
- `unified_edit`: Image editing (parquet)
- `vlm_sft`: VLM supervised fine-tuning (JSONL + images)

The `num_used_data` sum must exceed `NUM_GPUS × NUM_WORKERS`.

**Note**: For fine-tuning BAGEL, set `max_latent_size=64` to ensure correct pretrained weights loading. For T2I-only fine-tuning, set `visual_und=False`. For VLM-only fine-tuning, set `visual_gen=False`.

## Key Files

| Path | Purpose |
|------|---------|
| `app.py` | Gradio web UI with T2I, editing, VLM tabs |
| `inferencer.py` | Core inference with CFG support |
| `train/pretrain_unified_navit.py` | Distributed training entry point |
| `data/dataset_base.py` | Packed dataset with FLEX packing |
| `modeling/bagel/qwen2_navit.py` | MoT decoder, NaiveCache |
| `modeling/autoencoder.py` | VAE loading and decode |
| `data/transforms.py` | `ImageTransform` for VAE/ViT preprocessing |

## Inference Hyperparameters (from README.md)

- **cfg_text_scale**: Text guidance strength (1.0=disabled, 4.0-8.0=typical)
- **cfg_image_scale**: Image preservation strength (1.0-2.0)
- **cfg_interval**: CFG application range `[0.4, 1.0]` typical
- **timestep_shift**: Higher=layout-focused, lower=detail-focused
- **cfg_renorm_type**: `global` (best for T2I), `text_channel` (best for editing), `channel`
- **cfg_renorm_min**: 0.0 default, increase to 1.0 to disable renorm

If images appear blurry: use `global` renorm, decrease CFG scale or renorm_min.

### Thinking Mode (Chain-of-Thought)

Enable with `think=True` for enhanced reasoning during inference:

```python
result = inferencer(text=prompt, think=True,
    max_think_token_n=1024,    # Max tokens for thinking (64-4000)
    do_sample=False,           # Enable sampling for text
    text_temperature=0.3,      # Controls randomness (0.1-1.0)
)
```

System prompts:
- **Generation**: "You should first think about the planning process in the mind and then generate the image."
- **Understanding**: "You should first think about the reasoning process in the mind and then provide the user with the answer."

## Model Download
- **HuggingFace**: `ByteDance-Seed/BAGEL-7B-MoT`
- **Website**: https://bagel-ai.org/
- **Demo**: https://demo.bagel-ai.org/