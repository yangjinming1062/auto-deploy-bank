# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains implementations of **LLaMA-Adapter**, a parameter-efficient fine-tuning method for LLaMA models. It includes multiple variants:

- **LLaMA-Adapter V1** (`alpaca_finetuning_v1/`): Original adapter-based fine-tuning (1.2M parameters, ~1 hour training)
- **LLaMA-Adapter V2 Chat 65B** (`llama_adapter_v2_chat65b/`): Text-only dialog model with 65B parameters
- **LLaMA-Adapter V2 Multimodal** (`llama_adapter_v2_multimodal7b/`): Image-text instruction-following model
- **ImageBind-LLM** (`imagebind_LLM/`): Multi-modal LLM supporting image, audio, video, depth, thermal, IMU, and 3D point clouds
- **Gorilla** (`gorilla/`): Reproduces Gorilla (API generation) using both full fine-tune and LLaMA-Adapter

## Environment Setup

### Base Setup (for V1)
```bash
conda create -n llama_adapter -y python=3.8
conda activate llama_adapter
conda install pytorch cudatoolkit -c pytorch -y
pip install -r requirements.txt
pip install -e .
```

### Model-Specific Setups

**For V2 Multimodal:**
```bash
conda create -n llama_adapter_v2 python=3.8 -y
pip install -r requirements.txt
```

**For ImageBind-LLM:**
```bash
conda create -n imagebind_LLM python=3.9 -y
conda activate imagebind_LLM
cd ImageBind && pip install -r requirements.txt
cd ../ && pip install -r requirements.txt
# Download and merge Chinese LLaMA delta
python get_chinese_llama.py --llama_dir=/path/to/llama_model_weights
```

**For Gorilla:**
```bash
conda create -n minigpt python=3.10 -y
conda activate minigpt
pip install -r requirements.txt
# Compile apex manually (required for Gorilla)
```

### Pre-commit Hooks

The repository uses pre-commit hooks for code formatting:
```bash
pip install pre-commit
pre-commit install
```

Hooks include:
- trailing-whitespace
- end-of-file-fixer
- check-yaml
- isort (import sorting)
- black (code formatting, line-length=120)
- ruff (linting, max-complexity=10)

## Model Weights

**All models require LLaMA backbone weights** obtained from [this form](https://forms.gle/jk851eBVbX1m5TAv5). Organize as:
```
/path/to/llama_model_weights/
├── 7B/
│   ├── checklist.chk
│   ├── consolidated.00.pth
│   └── params.json
└── tokenizer.model
```

## Common Commands

### LLaMA-Adapter V1 (Text-only)

**Fine-tuning:**
```bash
cd alpaca_finetuning_v1
torchrun --nproc_per_node 8 finetuning.py \
    --model Llama7B_adapter \
    --llama_model_path $TARGET_FOLDER/ \
    --data_path $DATA_PATH/alpaca_data.json \
    --adapter_layer 30 \
    --adapter_len 10 \
    --max_seq_len 512 \
    --batch_size 4 \
    --epochs 5 \
    --warmup_epochs 2 \
    --blr 9e-3 \
    --weight_decay 0.02 \
    --output_dir ./checkpoint/
```

**Extract adapter weights:**
```bash
python extract_adapter_from_checkpoint.py --model_path ./checkpoint/{exp_name}/{pth_file}
```

**Inference:**
```bash
torchrun --nproc_per_node 1 example.py \
    --ckpt_dir $TARGET_FOLDER/7B \
    --tokenizer_path $TARGET_FOLDER/tokenizer.model \
    --adapter_path $ADAPTER_PATH
```

### LLaMA-Adapter V2 Multimodal

**Pre-training:**
```bash
. exps/pretrain.sh /path/to/llama_model_weights /path/to/pretrain-data-config.yaml /output/path
```

**Fine-tuning:**
```bash
. exps/finetune.sh \
 /path/to/llama_model_weights /path/to/pre-trained/checkpoint.pth \
 /path/to/finetune-data-config.yaml /output/path
```

**Inference (Python API):**
```python
import cv2
import llama
import torch
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
llama_dir = "/path/to/LLaMA/"
model, preprocess = llama.load("BIAS-7B", llama_dir, llama_type="7B", device=device)
model.eval()

prompt = llama.format_prompt("Please introduce this painting.")
img = Image.fromarray(cv2.imread("image.png"))
img = preprocess(img).unsqueeze(0).to(device)

result = model.generate(img, [prompt])[0]
print(result)
```

**Local Demo:**
```bash
python gradio_app.py
```

### ImageBind-LLM (Multi-modal)

**Pre-training:**
```bash
. exps/pretrain.sh /path/to/llama_model_weights /path/to/pretrain-data-config.yaml /output/path
```

**Fine-tuning:**
```bash
. exps/finetune.sh \
 /path/to/llama_model_weights /path/to/pre-trained/checkpoint.pth \
 /path/to/finetune-data-config.yaml /output/path
```

**Inference (multi-modal):**
```python
import ImageBind.data as data
import llama

llama_dir = "/path/to/LLaMA"
model = llama.load("7B", llama_dir, knn=True)
model.eval()

inputs = {}
image = data.load_and_transform_vision_data(["examples/girl.jpg"], device='cuda')
inputs['Image'] = [image, 1]
audio = data.load_and_transform_audio_data(['examples/girl_bgm.wav'], device='cuda')
inputs['Audio'] = [audio, 1]

results = model.generate(
    inputs,
    [llama.format_prompt("Guess the girl's mood based on the background music and explain the reason?")],
    max_gen_len=256
)
```

**Local Demo:**
```bash
python gradio_app.py --llama_dir /path/to/llama_model_weights
```

### Gorilla (API Generation)

**Full Fine-tune:**
```bash
cd finetune
bash scripts/finetune/finetune_7B_gorilla_{tf,hf,th}.sh sdp 1
```

**LLaMA-Adapter Fine-tune:**
```bash
cd alpaca_finetuning_v1
bash finetune_{tf,hf,th}.sh
```

**Inference:**
```bash
cd inference
torchrun --nproc_per_node 1 gorilla_inference_llama_adapter_v1.py \
    --ckpt_dir {path/to/llama} \
    --tokenizer_path {path/to/llama}/tokenizer.model \
    --adapter_path ../alpaca_finetuning_v1/checkpoint/{exp_name}/{adapter_pth_file} \
    --dataset_path ../gorilla-main/eval/eval-data/questions/{tensorflowhub, huggingface, torchhub}/questions_{tensorflowhub, huggingface, torchhub}_0_shot.jsonl
```

## Architecture

### Core Adapter Design

LLaMA-Adapter uses **prefix tuning** by inserting learnable tokens (adapter_len=10) at layer 30 (adapter_layer=30) of the transformer. The architecture introduces:

1. **Adapter Query**: Learnable embeddings that interact with frozen LLaMA features via attention
2. **Zero-init Attention**: Gating mechanism (initialized to zero) that progressively incorporates instructional signals
3. **Efficiency**: Only ~1.2M parameters vs 13GB for full fine-tuning

### Multi-modal Extensions

**V2 Multimodal:**
- Extends V1 with bias, norm, and projection layers
- Integrates CLIP-ViT-L/14 for vision encoding
- Supports image-conditioned instruction following

**ImageBind-LLM:**
- Uses ImageBind for multi-modal encoding (image, audio, video, depth, thermal, IMU)
- Integrates Open-Chinese-LLaMA for multilingual support
- Supports 3D point clouds via Point-Bind
- Can generate images using diffusion models

### Model Variants

| Model | Parameters | Storage | Training Time | Modality |
|-------|-----------|---------|---------------|----------|
| Alpaca | 7B | 13GB | 3 hours | Text |
| LLaMA-Adapter V1 | 1.2M | 4.7MB | 1 hour | Text |
| LLaMA-Adapter V2 | Varies | Varies | Varies | Text + Image |
| ImageBind-LLM | Varies | Varies | Varies | ImageBind modalities |

## Key Files

- `llama/`: Core LLaMA transformer implementation
- `alpaca_finetuning_v1/`: V1 fine-tuning code
- `llama_adapter_v2_multimodal7b/`: V2 multimodal model
- `imagebind_LLM/`: Multi-modal ImageBind implementation
- `gorilla/`: Gorilla reproduction
- `docs/`: Documentation and images
- `example.py`: V1 inference example
- `pyproject.toml`: Code formatting config (black, isort, ruff)
- `.pre-commit-config.yaml`: Pre-commit hooks

## Development Notes

- All training uses `torchrun` for distributed training
- Model parallelism via `fairscale`
- Adapter weights can be extracted from checkpoints using provided scripts
- Pre-trained weights available in GitHub Releases and Hugging Face
- Requires LLaMA tokenizer.model (not included in repo)
- Each subproject has its own requirements.txt and README
- Configuration files use YAML for multi-dataset training