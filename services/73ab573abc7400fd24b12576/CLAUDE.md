# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HealthGPT is a medical Large Vision-Language Model (LVLM) that unifies visual comprehension and generation capabilities. It employs H-LoRA (heterogeneous Low-Rank Adaptation) and a three-stage learning strategy to enable a pre-trained LLM to follow both visual comprehension and generation instructions.

## Environment Setup

```bash
# Create conda environment
conda create -n HealthGPT python=3.10
conda activate HealthGPT
pip install -r requirements.txt
```

For Qwen2.5 model support, use `requirements_qwen_2_5.txt` instead.

## Key Dependencies

- torch, torchvision, transformers
- peft (for LoRA/H-LoRA)
- gradio (web UI)
- timm (vision models)
- einops, accelerate, bitsandbytes
- omegaconf, pytorch_lightning, scikit-image (for VQGAN)

## Model Configurations

Three model variants are supported:

| Variant | Base LLM | ViT Encoder | H-LoRA r/alpha | Use Case |
|---------|----------|-------------|----------------|----------|
| HealthGPT-M3 | Phi-3-mini-4k-instruct | clip-vit-large-patch14-336 | 64/128 | Comprehension, Generation |
| HealthGPT-L14 | Phi-4 | clip-vit-large-patch14-336 | 32/64 | Comprehension only |
| HealthGPT-XL32 | Qwen2.5-32B-Instruct | clip-vit-large-patch14-336 | - | Comprehension |

## Required Model Weights

Download and place in specified directories:
- CLIP ViT: `openai/clip-vit-large-patch14-336` (from HuggingFace)
- Base LLMs: `microsoft/Phi-3-mini-4k-instruct`, `microsoft/phi-4`, or `Qwen/Qwen2.5-32B-Instruct`
- VQGAN: `last.ckpt` and `model.yaml` in `taming_transformers/ckpt/`
- H-LoRA weights: Download from HuggingFace (`lintw/HealthGPT-M3`, `lintw/HealthGPT-L14`)

## Running Inference

### Comprehension (Visual Question Answering)
```bash
cd llava/demo
bash com_infer.sh
# or directly
python3 com_infer.py \
    --model_name_or_path "microsoft/Phi-3-mini-4k-instruct" \
    --dtype "FP16" \
    --hlora_r "64" \
    --hlora_alpha "128" \
    --hlora_nums "4" \
    --vq_idx_nums "8192" \
    --instruct_template "phi3_instruct" \
    --vit_path "openai/clip-vit-large-patch14-336/" \
    --hlora_path "path/to/com_hlora_weights.bin" \
    --question "Your question" \
    --img_path "path/to/image.jpg"
```

For Phi-4 use `com_infer_phi4.py` with `instruct_template="phi4_instruct"`.

### Generation (Image Reconstruction)
```bash
python3 gen_infer.py \
    --hlora_path "path/to/gen_hlora_weights.bin" \
    --fusion_layer_path "path/to/fusion_layer_weights.bin" \
    --question "Reconstruct the image." \
    --img_path "path/to/image.jpg" \
    --save_path "output.jpg"
```

### Gradio Web Interface
```bash
python app.py
# Access at http://0.0.0.0:5011
```

## Architecture Summary

```
HealthGPT
├── app.py              # Gradio UI entry point
├── model.py            # HealthGPT and HealthGPT_Agent classes
├── config.py           # Config dataclasses for M3/L14 variants
├── llava/
│   ├── model/
│   │   ├── language_model/     # LlavaPhiForCausalLM, LlavaQwen, etc.
│   │   ├── multimodal_encoder/ # CLIP vision tower
│   │   ├── multimodal_projector/ # MLP projector (mlp2x_gelu)
│   │   └── llava_arch.py       # Core LVLM integration logic
│   ├── demo/            # Inference scripts (com_infer.py, gen_infer.py)
│   ├── peft/            # Custom H-LoRA implementation
│   └── conversation.py  # Conversation templates
└── taming_transformers/ # VQGAN for image generation
    ├── idx2img.py       # Convert VQ indices to images
    └── ckpt/            # VQGAN weights (last.ckpt, model.yaml)
```

### Key Classes

- **HealthGPT**: Main model class handling loading, inference, and generation
- **HealthGPT_Agent**: Agent class managing model switching and processing
- **LlavaPhiForCausalLM**: LLM wrapper extending Phi3ForCausalLM with vision capabilities
- **VQModel/GumbelVQ**: VQGAN decoder for image generation from discrete indices

### H-LoRA Configuration

H-LoRA uses `lora_nums=4` (4 adapters) with different ranks:
- Comprehension: `hlora_r=64`, `hlora_alpha=128`
- Generation: `hlora_r=256`, `hlora_alpha=512`

Special tokens `<idx_0>...<idx_8191>`, `<start_index>`, `<end_index>`, `<pixel_newline>` are added for unified vision-language tasks.

## Code Patterns

- All config classes use hardcoded relative paths (e.g., `./Phi-3-mini-4k-instruct`); update these for local usage
- The agent reloads models on config changes to avoid memory conflicts
- VQGAN is loaded globally in `taming_transformers/idx2img.py` for reuse
- Image inputs are expanded to squares before processing via `expand2square()`