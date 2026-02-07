# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **DAMO-ConvAI** research repository from Alibaba Group, containing ~45 independent research projects focused on Large Language Models (LLMs). Each subdirectory is a self-contained research project with its own README, dependencies, and setup instructions.

### Main Research Themes

- **LLM Training & Alignment**: EPO, SDPO, IOPO (reinforcement learning, preference optimization)
- **Mathematical Reasoning**: MaskedThought (MFT - Masked Thought Fine-Tuning)
- **Multi-Modal Models**: MMEvol, PaCE, OmniCharacter, OpenOmni
- **Dialogue Systems**: Sotopia, API-Bank, dial2vec, dialogue-cse
- **Text-to-SQL Parsing**: Proton, Graphix, s2sql, bird, r2sql, sunsql
- **Long-Context Understanding**: Loong, space-1/2/3
- **Agent Planning**: FlowBench, spectra, deep-thinking
- **Self-Evolution of LLMs**: Awesome-Self-Evolution-of-LLM (survey paper collection)

## Common Commands

### Environment Setup

```bash
# Create conda environment (most projects use python 3.7-3.10)
conda create -n <env_name> python=3.10
conda activate <env_name>

# Install dependencies
pip install -r requirements.txt

# For editable installs (common pattern)
pip install -e .
```

### Model Training (LLaMA-Factory based projects)

Projects using LLaMA-Factory (EPO, SDPO, IOPO):
```bash
# Training
llamafactory-cli train examples/train_full/<config>.yaml

# Inference
llamafactory-cli api examples/inference/<config>.yaml
```

### Evaluation

Many projects use OpenAI API for evaluation:
```bash
# Set API key in config files (typically in config/models/*.yaml or utils/keys.json)
export OPENAI_API_KEY="your-key"

# Run evaluation scripts (project-specific)
python eval_model.py
python run.sh
```

### Redis Setup (required for Sotopia-based projects)

Several dialogue projects require Redis:
```bash
# Install Redis
sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2.23_amd64.deb
./redis-stack-server-7.2.0-v10/bin/redis-stack-server --daemonize yes
```

## Key Dependencies

- **LLaMA-Factory**: Model training framework used by multiple projects
- **vLLM**: High-throughput inference (used for evaluation)
- **Redis/Redis Stack**: Memory backend for dialogue systems
- **PyTorch**: Deep learning framework
- **Transformers**: Hugging Face model library
- **OpenAI API**: Used for evaluation and some data generation

## Project-Specific Notes

### EPO (Explicit Policy Optimization)
- Contains `LLaMA-Factory`, `Sotopia` (benchmark), and `Alfshop` (WebShop/ALFWorld)
- Training data available at HuggingFace: `Tongyi-ConvAI/EPO-RL-data`
- Primary command: `llamafactory-cli train examples/train_epo/llama3_sotopia_pi_rl.yaml`

### MMEvol (Multi-Modal Evolution)
- Requires extensive dataset preparation (see README for data structure)
- Uses VLMEvalKit for evaluation
- Training scripts in `scripts/v1_6/train/`

### Graphix (Text-to-SQL)
- Requires dependency parsing packages (Supar)
- Uses Docker for environment setup (recommended)
- Data preprocessing: `make pre_process`

### Loong (Long-Context Benchmark)
- Evaluation via `src/run.sh`
- Requires vLLM server for open-source models
- Data downloaded from: `http://alibaba-research.oss-cn-beijing.aliyuncs.com/loong/doc.zip`

### API-Bank (Tool-Augmented LLMs)
- Contains 73 API tools and 314 annotated dialogues
- Demo: `python demo.py`
- Evaluation: `python evaluator.py`

## Code Style

- Python-based research code
- Configuration typically in YAML files or Python dictionaries
- Model checkpoints stored in `checkpoints/` or project-specific directories
- Dataset files typically in JSON/JSONL format

## Data Locations

- **HuggingFace datasets**: `Tongyi-ConvAI/` organization (training data for multiple projects)
- **Model checkpoints**: Various, check project READMEs
- **Benchmark data**: Often requires separate download (Google Drive, project pages)

## Notes

- Each subdirectory is largely independent - check the specific project's README for accurate instructions
- Many projects depend on external API keys (OpenAI, etc.)
- GPU requirements vary by project (A100s commonly used for training)
- Some projects use deprecated Python versions (3.7) - check requirements