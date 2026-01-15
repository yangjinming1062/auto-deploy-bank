# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DISC-LawLLM is a legal domain large language model developed by Fudan-DISC lab. It provides intelligent legal services including legal consultation, document drafting, and legal knowledge retrieval. The project includes:

- **Models**: DISC-LawLLM-13B (Baichuan-13B base) and LawLLM-7B (Qwen2.5-instruct 7B base)
- **Training Data**: DISC-Law-SFT dataset (~403K samples) with legal reasoning capabilities
- **Evaluation**: DISC-Law-Eval benchmark with objective (MCQ) and subjective (QA) tasks

## Common Commands

### Setup
```bash
pip install -r requirements.txt
```

### Model Inference
```bash
# Command-line interface
python cli_demo.py

# Web demo (Streamlit)
streamlit run web_demo.py --server.port 8888
```

### Fine-tuning (via LLaMA Factory)
```bash
# Full parameter fine-tuning
llamafactory-cli train lawllm_full_sft.yaml

# LoRA fine-tuning
llamafactory-cli train lawllm_lora_sft.yaml

# Merge LoRA weights
llamafactory-cli export lawllm_merge_lora.yaml
```

### Evaluation
```bash
# Run evaluation (model_name required, tasks: mcq_sing, mcq_mult, qa)
python eval/src/main.py --model_name <model> --tasks mcq_sing mcq_mult qa

# Options: --n-shot, --max-iter, --verbose, --generate-only, --eval-only
```

## Architecture

### Core Components
- `cli_demo.py`: Command-line chat interface using transformers `model.chat()` API
- `web_demo.py`: Streamlit web interface with chat history management
- `lawllm_*.yaml`: LLaMA Factory training configurations

### Evaluation Framework (`eval/src/`)
- `main.py`: Entry point for benchmarking, supports parallel task evaluation
- `models.py`: Model wrapper classes implementing `chat()` and `achat()` methods; few-shot example loading for MCQ formatting
- `eval.py`: Contains `McqRegexEvaluator` (regex-based MCQ answer extraction) and `QaOpenaiEvaluator` (OpenAI-based subjective scoring on accuracy, completeness, clarity)
- `utils.py`: Helper functions for path resolution and result generation

### Dataset Structure
- `eval/datasets/objective/`: CSV files with MCQ tasks (NJE, CPA, PAE, UNGEE, LBK, PFE)
- `eval/datasets/subjective/`: JSON files for QA evaluation
- `eval/stats/`: Pre-computed evaluation results

### Model Requirements
- **DISC-LawLLM-13B**: transformers==4.29.1, uses Baichuan-13B-Base, supports device_map="auto"
- **LawLLM-7B**: Compatible with vllm for faster inference, uses Qwen2.5-7B-Instruct

### Fine-tuning Notes
- Full fine-tuning tested on 8x A100 80GB
- LoRA fine-tuning tested on 4x A100 80GB
- Uses deepspeed configuration files for distributed training
- Uses Qwen chat template for LawLLM-7B