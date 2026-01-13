# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

DeepKE is a deep learning-based knowledge extraction toolkit for knowledge graph construction. It supports multiple extraction tasks (NER, RE, AE, EE, Triple) across various scenarios including standard supervised learning, few-shot learning, document-level, and multimodal settings.

## Project Structure

- **src/deepke/** - Main source code organized by task type
  - `name_entity_re/` - Named Entity Recognition (NER)
  - `relation_extraction/` - Relation Extraction (RE)
  - `attribution_extraction/` - Attribute Extraction (AE)
  - `event_extraction/` - Event Extraction (EE)
  - `triple_extraction/` - Triple extraction models (ASP, PRGC, PURE)

- **example/** - Task-specific examples with runnable scripts
  - `ner/` - NER examples (standard, few-shot, multimodal, cross)
  - `re/` - RE examples (standard, few-shot, document, multimodal)
  - `ae/` - AE examples (standard)
  - `ee/` - EE examples (standard)
  - `llm/` - Large Language Model based knowledge extraction
  - `triple/` - Triple extraction examples (ASP, PRGC, PURE, cnschema)

- **mcp-tools/** - MCP (Model Calling Protocol) service tools for LLM integration

## Environment Setup

### For DeepKE (Traditional Models)
```bash
# Python 3.8 required
conda create -n deepke python=3.8
conda activate deepke
pip install -r requirements.txt
python setup.py install
python setup.py develop
```

### For DeepKE-LLM
```bash
# Python 3.9 required
conda create -n deepke-llm python=3.9
conda activate deepke-llm
cd example/llm
pip install -r requirements.txt
```

### Docker Setup
```bash
docker pull zjunlp/deepke:latest
docker run -it zjunlp/deepke:latest /bin/bash
```

## Common Development Tasks

### Training a Model
Each task example contains training scripts:
```bash
cd example/<task>/<scenario>
# Download dataset (if needed)
wget 121.41.117.246:8080/Data/<task>/<scenario>/data.tar.gz
tar -xzvf data.tar.gz

# Train
python run.py  # For BERT-based models
python run_bert.py  # Or specific model scripts
```

### Running Prediction
```bash
cd example/<task>/<scenario>
python predict.py
```

### Configuration
DeepKE uses Hydra for configuration management:
- **config.yaml** - Main configuration
- **train.yaml** - Training parameters
- **predict.yaml** - Prediction parameters
- Configs are in `conf/` directory of each example

Parameters like model paths, data directories, and hyperparameters can be modified in these YAML files.

### Key Configuration Paths
- `data_dir` - Dataset location (default: "data/")
- `model_name` - Model type (e.g., 'bert', 'lstmcrf', 'w2ner')
- `load_path` - Path to load pretrained model
- `save_path` - Path to save trained model
- `write_path` - Output path for predictions

## Architecture Patterns

### Task Organization
Each task follows a consistent pattern:
- **Standard** - Fully supervised learning with pretrained transformers (BERT, etc.)
- **Few-shot** - Low-resource learning with meta-learning approaches
- **Document** - Document-level relation extraction
- **Multimodal** - Vision + text knowledge extraction
- **Cross** - Cross-lingual or cross-domain extraction

### Code Structure
Each task directory contains:
- `models/` - PyTorch model definitions
- `module/` - Training and inference modules
- `tools/` - Utility functions
- `utils/` - Helper functions
- `conf/` - Hydra configuration files

### Model Training Pattern
Most training scripts follow this structure:
1. Load configuration via Hydra
2. Initialize tokenizer and model
3. Load and preprocess data
4. Train model with validation
5. Save checkpoints and logs

Example from `run_bert.py`:
- Extends `BertForTokenClassification` for NER
- Uses `TrainNer` class with custom forward pass
- Handles valid_ids for proper BERT tokenization
- Supports gradient accumulation and mixed precision

## Testing Individual Models

### Test a Specific Model
```bash
# Enter the specific example directory
cd example/ner/standard

# Modify conf/predict.yaml to set:
# - load_path: absolute path to trained model
# - write_path: where to save predictions

# Run prediction
python predict.py
```

### Debug Training
```bash
# Enable wandb for visual logging
wandb login
python run_bert.py

# Or run with ipdb for debugging
python -m ipdb run_bert.py
```

## LLM Integration (DeepKE-LLM)

The `example/llm/` directory contains multiple LLM-based approaches:
- **OneKE** - Bilingual schema-based IE model
- **LLaMA-series** - LoRA fine-tuning for instruction-based KG construction
- **ChatGLM** - P-tuning and LoRA approaches
- **GPT-series** - In-context learning and data augmentation

Each LLM example has its own requirements and setup instructions in its README.

## MCP Tools

The `mcp-tools/` directory provides MCP (Model Calling Protocol) service interfaces for integrating DeepKE with LLMs:

```bash
# Setup
pip install uv
cd mcp-tools
uv venv
source .venv/bin/activate
uv add "mcp[cli]" httpx openai pyyaml

# Configure .env with DeepKE paths
DEEPKE_PATH=".."
CONDA_PY="/path/to/conda/envs/deepke/bin/"

# Run MCP server
python run.py
```

MCP provides these endpoints:
- `deepke_ner()` - NER prediction
- `deepke_re()` - RE prediction
- `deepke_ae()` - AE prediction
- `deepke_ee()` - EE prediction

## Data Formats

### NER Data (.txt)
Tab-separated: `token   label`

### RE Data (.csv)
Columns: `sentence, relation, head, head_offset, tail, tail_offset`

### AE Data (.csv)
Columns: `sentence, attribute, entity, entity_offset, value, value_offset`

### EE Data (.tsv)
Event extraction with trigger words and arguments

## Requirements and Dependencies

### Main DeepKE Requirements
- Python 3.8
- torch>=1.5,<=1.11
- transformers==4.26.0
- hydra-core==1.0.6
- wandb==0.12.7
- Other dependencies in requirements.txt

### DeepKE-LLM Requirements
- Python 3.9
- Separate requirements in `example/llm/requirements.txt`

## Development Guidelines

From CONTRIBUTING.md:
1. Keep code simple and readable for non-engineers
2. Use f-strings for string formatting
3. Test code with flake8
4. Submit issues before submitting PRs

## Tips

1. **Mirror Sources**: Use THU mirror in China for Anaconda, aliyun for pip
2. **Pretrained Models**: Download and store in `pretrained/` folder to avoid slow downloads
3. **Version Compatibility**: Ensure exact versions in requirements.txt
4. **Path Issues**: Use `\\` in Windows paths
5. **Hydra Working Directory**: Use `utils.get_original_cwd()` to get original project root

## Citation

If using this repository, cite:
```bibtex
@inproceedings{EMNLP2022_Demo_DeepKE,
  author    = {Ningyu Zhang and Xin Xu and Liankuan Tao and Haiyang Yu and Hongbin Ye and Shuofei Qiao and Xin Xie and Xiang Chen and Zhoubo Li and Lei Li},
  title     = {DeepKE: {A} Deep Learning Based Knowledge Extraction Toolkit for Knowledge Base Population},
  booktitle = {{EMNLP} (Demos)},
  pages     = {98--108},
  publisher = {Association for Computational Linguistics},
  year      = {2022},
}
```