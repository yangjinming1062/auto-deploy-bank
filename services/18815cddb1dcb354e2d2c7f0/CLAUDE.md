# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UNO (Less-to-More Generalization) is a multi-image conditioned subject-to-image generation model from ByteDance. It builds on FLUX.1-dev and uses LoRA-based training to achieve high subject consistency across single and multi-subject generation scenarios. The model leverages in-context generation capabilities of diffusion transformers to synthesize paired training data.

## Commands

### Installation
```bash
pip install -e .              # For inference/demo only
pip install -e .[train]       # Include training dependencies (accelerate, deepspeed)
```

### Inference
```bash
python inference.py --prompt "A clock on the beach" --image_paths "assets/clock.png" --width 704 --height 704
python inference.py --eval_json_path ./datasets/dreambench_singleip.json  # Evaluate on dreambench
```

### Gradio Demo
```bash
python app.py                           # Standard mode (higher memory)
python app.py --offload --name flux-dev-fp8  # Memory-optimized mode (~16GB VRAM)
```

### Training
```bash
# Prepare UNO-1M dataset first (see README.md for instructions)
python uno/utils/filter_uno_1m_dataset.py ./datasets/UNO-1M/uno_1m_total_labels.json ./datasets/UNO-1M/uno_1m_total_labels_convert.json 4
accelerate launch train.py --train_data_json ./datasets/UNO-1M/uno_1m_total_labels_convert.json
```

### Linting
```bash
ruff check uno/
```

## Architecture

### Data Flow (Inference)
1. **Reference Images** (`pipeline.py:preprocess_ref`) - Resize and center-crop reference images (512px for single subject, 320px for multi-subject)
2. **Latent Encoding** - Autoencoder encodes reference images to latent space
3. **Condition Preparation** (`sampling.py:prepare_multi_ip`) - Creates concatenated token sequences with positional embeddings for:
   - Text tokens (T5-XXL)
   - Image tokens (target output)
   - Reference image tokens (shifted position embeddings)
4. **Denoising** (`sampling.py:denoise`) - Iterative flow matching over timesteps with classifier-free guidance
5. **Output Decoding** - VAE decoder reconstructs final image from latents

### Model Components (`uno/flux/`)

| File | Purpose |
|------|---------|
| `model.py` | Main Flux transformer with double-stream and single-stream blocks. Handles `ref_img`/`ref_img_ids` concatenation for multi-image conditioning |
| `pipeline.py:UNOPipeline` | High-level inference interface. Manages model loading, offloading, and LoRA injection |
| `sampling.py` | Sampling utilities: `get_noise`, `get_schedule`, `prepare_multi_ip`, `denoise`, `unpack` |
| `util.py` | Model loading: `load_flow_model`, `load_ae`, `load_t5`, `load_clip`, `set_lora` |
| `modules/layers.py` | Attention processors including LoRA variants (`DoubleStreamBlockLoraProcessor`, `SingleStreamBlockLoraProcessor`) |
| `modules/conditioner.py` | HFEmbedder wrapper for T5/CLIP text encoders |

### Key Data Structures

- **FluxParams** (`model.py:24-37`): Model configuration (19 double blocks, 38 single blocks, 3072 hidden dim, 24 heads)
- **ModelSpec** (`util.py:103-115`): Registry mapping model types (`flux-dev`, `flux-dev-fp8`, `flux-schnell`) to configs
- **InferenceArgs**/`TrainArgs**: Dataclasses for CLI argument parsing using `HfArgumentParser`

### Training Pipeline (`train.py`)

1. **Model Initialization**: Load base FLUX, freeze all components except LoRA layers
2. **LoRA Injection** (`util.py:set_lora`): Apply LoRA to specified transformer block indices
3. **Data Loading**: `FluxPairedDatasetV2` with aspect-ratio bucketing (11 predefined buckets)
4. **Training Loop**:
   - VAE encoding of target and reference images
   - Flow matching loss: MSE between predicted and target noise
   - EMA support for model weights
   - DeepSpeed ZeRO optimization for T5/CLIP (offloaded to CPU)
   - Periodic validation with image generation logging to wandb

## Model Checkpoints

Models downloaded from HuggingFace (`black-forest-labs/FLUX.1-dev`, `bytedance-research/UNO`). Set `FLUX_DEV`, `AE`, `T5`, `CLIP`, `LORA` environment variables to use local checkpoints.

## Code Conventions

- 4-space indentation, 120 character line length
- ruff for linting (E4, E7, E9, F, I rules)
- Type hints using `TYPE_CHECKING` for lazy imports
- safetensors for checkpoint serialization