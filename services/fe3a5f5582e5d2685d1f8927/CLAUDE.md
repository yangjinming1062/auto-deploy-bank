# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RecAI is a Microsoft research project exploring how to integrate Large Language Models (LLMs) into recommender systems (LLM4Rec). The project consists of multiple independent submodules, each addressing a different aspect of LLM-based recommendation.

### Submodules

- **InteRecAgent**: Conversational recommender agent that combines LLM as the brain with traditional recommender models as tools
- **Knowledge_Plugin**: DOKE (Domain-Oriented Knowledge Enhancement) framework for enhancing LLMs with domain-specific knowledge via prompting
- **RecLM-emb**: Embedding-based item retrieval by fine-tuning text embedding models for recommendation tasks
- **RecLM-gen**: Generative recommendation via supervised fine-tuning (SFT) and reinforcement learning (RL)
- **RecLM-cgen**: Constrained generative recommendation with prefix tree constraints to prevent out-of-domain item generation
- **RecExplainer**: LLM-based model explainer for black-box recommender systems
- **RecLM-eval**: Comprehensive evaluation framework for LLM-based recommenders

## Environment Setup

### Common API Configuration

Most modules use OpenAI/Azure OpenAI APIs. Set these environment variables:

```bash
export OPENAI_API_KEY="xxx"
export OPENAI_API_BASE="https://xxx.openai.azure.com/"
export OPENAI_API_VERSION="2023-03-15-preview"
export OPENAI_API_TYPE="azure"  # or "open_ai"
export MODEL="gpt-4"  # deployment name or model name
```

AzureCliCredential login is also supported:
```bash
az login
```

### Conda Environment Setup (per submodule)

Each submodule has its own `requirements.txt`. Create an environment and install:

```bash
conda create -n <env_name> python=3.9
conda activate <env_name>
pip install -r requirements.txt
```

### Common Dependencies Across Modules
- torch, transformers, peft (LoRA fine-tuning), accelerate, openai, vllm
- Some modules require UniRec library (cloned separately and installed locally)

## Submodule-Specific Commands

### InteRecAgent

```bash
cd InteRecAgent
conda create -n interecagent python=3.9
conda activate interecagent
pip install -r requirements.txt

# Download resources from GoogleDrive/RecDrive and place in resources/
export OPENAI_API_KEY="xxx"
export API_TYPE="open_ai"
DOMAIN=game python app.py --engine gpt-4
# Or use run.sh for convenience
```

### Knowledge_Plugin

```bash
cd Knowledge_Plugin
# Step 1: Download and process raw data (step1-Raw_Dataset_Parsing)
# Step 2: Train base recommender model (step2-Base_models)
# Step 3: Extract knowledge
cd Knowledge_Extraction
python extract_I2I.py --dataset ml1m --negative_type pop
python extract_U2I.py --dataset ml1m --negative_type pop
# Step 4: Generate prompts and evaluate
cd DOKE
python generate_prompt.py --config config/ml1m/popneg_his_I2I.json --dataset ml1m
python call_openai.py --prompt out/prompts/ml1m/popneg_his_I2I.json --model ChatGPT --dataset ml1m
bash metric.bash out/result/ml1m/ChatGPT_popneg_his_I2I ml1m
```

### RecLM-emb

```bash
cd RecLM-emb
conda create -n RecLM_emb python=3.10
conda activate RecLM_emb
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
pip install -r requirements.txt

# Prepare data (metadata.json and sequential_data.txt)
bash shell/data_pipeline.sh
bash shell/test_data_pipeline.sh

# Training (single node)
bash shell/run_single_node.sh
# Multi-node training
bash shell/run_multi_node.sh <node_rank> <IP> <port>

# Inference
bash shell/infer_metrics.sh
bash shell/infer_case.sh  # case study
bash shell/demo.sh        # Web GUI
```

### RecLM-gen

```bash
cd RecLM-gen
# Requires UniRec to be cloned and installed separately
git clone https://github.com/microsoft/UniRec.git
# Install UniRec (modify setup.py torch version constraint first)

# Data preprocessing (requires Amazon data)
./scripts/data_preprocess_amazon.sh data/dataset/sub_movie/

# 1. SASRec Server (teacher model)
./scripts/unirec_train.sh sub_movie
./scripts/unirec_serve.sh sub_movie 12621 1

# 2. SFT Stage
python data_process.py --train_stage SFT ...
./scripts/sft_train.sh
./scripts/sft_merge.sh

# 3. RL Stage (optional)
python data_process.py --train_stage RL ...
./scripts/rl_train.sh
./scripts/rl_merge.sh

# 4. Testing
python -m vllm.entrypoints.openai.api_server --port 13579 --model snap/...
./scripts/tasks_test.sh snap/... 13579 sub_movie
```

### RecLM-cgen

```bash
cd RecLM-cgen
# Similar to RecLM-gen but with constrained generation

# Preprocess data
./scripts/data_preprocess_amazon.sh

# Train teacher (SASRec)
./scripts/unirec_train.sh movies
./scripts/unirec_serve.sh 2068

# Train RecLM-cgen
./scripts/train_RecLM_cgen.sh movies
./scripts/run_SFT_merge.sh

# Test
python task_test.py --use_CBS --CBS_type 2 --topk 10
python task_MR_test.py  # multi-round conversation
```

### RecExplainer

```bash
cd RecExplainer
conda create -n recexplainer python=3.10.14
conda activate recexplainer
pip install -r requirements.txt

# Prepare data (Amazon Video Games + ShareGPT)
bash shell/preprocess_recmodel.sh
bash shell/unirec_prepare_data.sh

# Train target recommender models
bash shell/unirec_sasrec_train.sh
bash shell/unirec_mf_train.sh

# Train RecExplainer
bash shell/recexplainer_data_pipeline.sh
bash shell/train.sh
bash shell/merge.sh

# Evaluate alignment
bash shell/infer_alignment.sh
# Evaluate explanations
bash shell/infer_explan.sh
```

### RecLM-eval

```bash
cd RecLM-eval
conda create -n receval python=3.9
conda activate receval
pip install -r requirements.txt

# Edit openai_api_config.yaml with API key
# Download Steam data to ./data/

# Run evaluation
bash main.sh
# Or specific tasks
python eval.py --task-names ranking retrieval \
    --bench-name steam \
    --model_path_or_name Qwen/Qwen2.5-7B-Instruct
```

## Common Architecture Patterns

### Dataset Formats
- **metadata.json**: Item information with fields like `title`, `tags`, `description`, `price`, `release_date`
- **sequential_data.txt**: User behavior sequences (space-separated user_id item_id1 item_id2 ...)
- **category.pickle/jsonl**: Category-to-item-id mappings
- **pickle intermediate files**: Used by RecLM-gen/cgen for training data

### LLM Fine-tuning Approach
- Uses transformers library with PEFT for LoRA fine-tuning
- Base model + LoRA adapters merged after training
- Supports Mistral, Llama-2/3, Phi3, Vicuna, Qwen chat models
- Training scripts use DeepSpeed for distributed training

### Evaluation Tasks
- Retrieval (item retrieval from corpus)
- Ranking (ranking candidate items)
- Sequential recommendation (next item prediction)
- Explanation generation
- Conversation (chatbot ability)
- Embedding-based methods

### External Dependencies
- **UniRec**: Microsoft's recommendation library for SASRec/MF models (cloned separately)
- **vLLM**: For serving fine-tuned models with OpenAI-compatible API
- **FastChat**: For serving open-source models locally (Vicuna, etc.)

## Key File Locations

- Each submodule has its own `requirements.txt`, `README.md`, and `shell/` or `scripts/` directories
- Preprocessing scripts are typically in `preprocess/` or `shell/` directories
- Training entry points: `train.py`, `main.py`, or scripts in `shell/`/`scripts/`
- Evaluation scripts: `eval.py`, `task_test.py`, or shell scripts
- Configuration files: YAML/JSON files in `config/`, `shell/`, or `scripts/`

## Important Notes

- Each submodule is largely independent; there is no unified build system
- Data preparation is a prerequisite and varies by submodule
- Many modules require pre-trained UniRec models for teacher-student training
- API costs can be significant when using OpenAI for large-scale experiments
- Check individual submodule READMEs for the most accurate, detailed instructions