# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is Microsoft's **unilm** (Unified Language Model) repository - a collection of foundation models for AI across **language**, **vision**, **speech**, and **multimodal** domains. Each model is self-contained in its own subdirectory with independent setup, training scripts, and documentation.

**Major Model Categories:**
- **Language/Multilingual**: UniLM, InfoXLM, DeltaLM, MiniLM, E5, EdgeLM, SimLM, AdaLM
- **Vision**: BEiT, BEiT-2, BEiT-3, DiT, TextDiffuser
- **Speech**: WavLM, VALL-E, SpeechT5, SpeechLM
- **Multimodal**: Kosmos-1/2/2.5, LayoutLM v1/v2/v3, LayoutXLM, MarkupLM, XDoc, VLMo, VL-BEiT
- **Foundation Architectures**: TorchScale (see https://github.com/microsoft/torchscale)

## Common Development Commands

Each model directory has its own `requirements.txt` and setup instructions. Standard patterns:

```bash
# Install dependencies (run from the specific model directory)
pip install -r requirements.txt

# Distributed training (common pattern across models)
python -m torch.distributed.launch --nproc_per_node=8 --master_port=4398 run_*.py [args]

# Mixed-precision training requires NVIDIA apex
git clone https://github.com/NVIDIA/apex
cd apex && pip install -v --disable-pip-version-check --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./
```

**Note:** Docker is commonly used for development. See individual model READMEs for recommended Docker images (typically `nvcr.io/nvidia/pytorch:*`).

## Architecture Patterns

### Shared Dependencies
- **TorchScale** (`kosmos-2/torchscale/`): Foundation Transformer architectures (DeepNet, Magneto, X-MoE, etc.)
- **fairseq**: Used by speech models (speechlm, speecht5) and some NLP models - appears as git submodule
- **timm**: PyTorch Image Models library for vision transformers
- **detectron2**: Object detection framework used by DiT, LayoutLMv3 for layout analysis

### Document AI Model Family
Models like LayoutLMv3, DiT, and BEiT share components. LayoutLMv3's README acknowledges dependencies on transformers, layoutlmv2, layoutlmft, beit, and dit.

### Checkpoint Distribution
- Most pretrained models are hosted on [HuggingFace](https://huggingface.co/microsoft)
- Some models use Azure Blob Storage links (base64-encoded in READMEs)
- Model weights are typically PyTorch `.bin` or `.pth` files

## Working with Submodules

Three fairseq submodules exist:
```
deltalm/fairseq -> facebookresearch/fairseq
speechlm/fairseq -> facebookresearch/fairseq
speecht5/fairseq -> facebookresearch/fairseq
```

Initialize with: `git submodule update --init --recursive`

## Key Contacts

- **General issues**: Submit GitHub issues to the model-specific directory
- **Furu Wei** (fuwei@microsoft.com): Primary contact for the project
- Model-specific contacts listed in each model's README.md