# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-Modality Arena is an evaluation platform for Large Vision-Language Models (LVLMs). It provides comprehensive benchmarks to evaluate multimodal models across various capabilities including visual perception, reasoning, commonsense, knowledge acquisition, and object hallucination.

## Environment Setup

```bash
# Create conda environment
conda create -n lvlm_eval python=3.8 -y
conda activate lvlm_eval
pip install -r requirements.txt

# Or for Multi_turn_Reasoning
conda env create -f environment.yml
```

## Model Checkpoints Directory

Set `DATA_DIR` environment variable or modify path in:
- `tiny_lvlm_evaluation/models/__init__.py`: `DATA_DIR = '/nvme/share/VLP_web_data'`
- `LVLM_evaluation/Multi_turn_Reasoning/*/models/__init__.py`

Expected structure:
```
/path/to/DATA_DIR
├── llama_checkpoints/7B/
│   ├── checklist.chk
│   ├── consolidated.00.pth
│   └── params.json
├── MiniGPT-4/
│   ├── alignment.txt
│   └── pretrained_minigpt4_7b.pth
├── VPGTrans_Vicuna/
├── otter-9b-hf/
└── PandaGPT/
    ├── imagebind_ckpt/
    ├── vicuna_ckpt/
    └── pandagpt_ckpt/
```

## Running Evaluations

### Tiny LVLM Evaluation (50 samples per dataset - recommended for testing)
```bash
cd tiny_lvlm_evaluation
python eval_tiny.py \
    --model-name $MODEL \
    --device $CUDA_DEVICE_INDEX \
    --batch-size $EVAL_BATCH_SIZE \
    --dataset-names $DATASET_NAMES \
    --sampled-root $SAMPLED_DATASET_DIR \
    --answer_path $SAVE_DIR
```

### Full LVLM Evaluation
```bash
cd LVLM_evaluation/Multi_turn_Reasoning
python eval.py \
    --model_name $MODEL \
    --device $CUDA_DEVICE_INDEX \
    --batch_size $EVAL_BATCH_SIZE \
    --dataset_name $DATASET \
    --answer_path $SAVE_DIR
```

### Medical LVLM Evaluation (OmniMedVQA)
```bash
cd MedicalEval/Prefix_based_Score
bash scripts/run_eval_loss.sh  # Modify MODEL and data path first
```

## Supported Models

Model names for `--model-name` argument:
- `BLIP2`
- `MiniGPT-4`
- `InstructBLIP`
- `LLaVA`
- `LLaMA-Adapter-v2`
- `mPLUG-Owl`
- `Otter`
- `Otter-Image`
- `VPGTrans`
- `PandaGPT`
- `OFv2_*` (version variants)
- `LaVIN`
- `Lynx`
- `Cheetah`
- `BLIVA`
- `MIC`

## Architecture

### Model Interface Pattern
All models implement a `TestXxx` class interface in `tiny_lvlm_evaluation/models/test_*.py`:

```python
class TestModel:
    def __init__(self, device=None)
    def move_to_device(self, device=None)
    def generate(self, image, question, max_new_tokens=128) -> str
    def batch_generate(self, image_list, question_list, max_new_tokens=128) -> list
```

### Evaluation Pipeline
1. `eval_tiny.py` → calls `get_model()` from `models/__init__.py`
2. `get_model()` instantiates the appropriate `TestXxx` class
3. Dataset is loaded via `task_datasets` with `GeneralDataset`
4. Task-specific eval function from `utils.dataset_task_dict` processes results
5. Results saved to `answer_path/{model_name}/{timestamp}/result.json`

### Key Directories
- `tiny_lvlm_evaluation/models/` - Model testers (TestXxx classes)
- `tiny_lvlm_evaluation/task_datasets/` - Dataset implementations
- `LVLM_evaluation/Multi_turn_Reasoning/lib/` - Model-specific loading libraries
- `LVLM_evaluation/Multi_turn_Reasoning/instruct_blip/` - InstructBLIP model implementation
- `MedicalEval/` - Medical domain LVLM evaluation

### Model Loading Libraries
Located in `LVLM_evaluation/Multi_turn_Reasoning/lib/`:
- `blip2_lib.py` - BLIP2 loading
- `instructblip_lib.py` - InstructBLIP loading
- `llama_adapter.py` - LLaMA-Adapter-v2 loading
- `llava_lib.py` - LLaVA loading
- `minigpt4_lib.py` - MiniGPT-4 loading
- `mplugowl_lib.py` - mPLUG-Owl loading
- `otter_lib.py` - Otter loading
- `vgtrans_lib.py` - VPGTrans loading

## Prompt Engineering

Question prompts follow dataset-specific formats. Common patterns:
```python
# VQA
f"Question: {question} Short answer:"

# Classification
"Classify the main object in the image."

# Yes/No
"Question: {question}\nChoose the best answer:\n- Yes\n- No\nAnswer:"
```

## Common Development Tasks

### Adding a New Model
1. Create `test_newmodel.py` in `tiny_lvlm_evaluation/models/`
2. Implement `TestNewModel` class with required interface
3. Add to `get_model()` factory in `tiny_lvlm_evaluation/models/__init__.py`

### Running Single Dataset
```bash
python eval_tiny.py --dataset-names GQA
```

### Using Sampled Data
```bash
python eval_tiny.py --use-sampled --sampled-root tiny_lvlm_datasets
```

### Checkpoint Downloads
- LLaMA weights: Requires form at https://forms.gle/jk851eBVbX1m5TAv5
- MiniGPT-4: https://drive.google.com/file/d/1RY9jV0dyqLX-o38LrumkKRh6Jtaop58R
- VPGTrans: https://drive.google.com/drive/folders/1YpBaEBNL-2a5DrU3h2mMtvqkkeBQaRWp
- Otter: https://huggingface.co/BellXP/otter-9b-hf