# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ToolBench is a large-scale dataset and framework for training Large Language Models (LLMs) to use real-world tools and APIs. It contains 3,451 tools with 16,464 APIs, and provides infrastructure for:

- **Training**: Fine-tuning LLaMA models (ToolLLaMA) using instruction tuning data
- **Inference**: Running tool-use pipelines with multiple reasoning methods (CoT, DFS, DFSDT)
- **Evaluation**: Automated evaluation using ToolEval for pass rate and preference metrics
- **Web Interface**: Gradio-based web UI and FastAPI server for interactive use

## Architecture

### Core Components

**Training (`toolbench/train/`)**
- `train_mem.py`: Full model training on 2x A100 GPUs with FSDP
- `train_lora.py`: LoRA fine-tuning using DeepSpeed for resource-efficient training
- `train.py`: Base training script (legacy)

**Inference (`toolbench/inference/`)**
- `qa_pipeline.py`: Main inference pipeline for ToolLLaMA and OpenAI models
- `qa_pipeline_open_domain.py`: Open-domain inference with retriever
- `server.py`: FastAPI server for web interface
- `toolbench_server.py`: Backend server for Web UI

**LLM Integration (`toolbench/inference/LLM/`)**
- `tool_llama_model.py`: ToolLLaMA full model
- `tool_llama_lora_model.py`: ToolLLaMA LoRA model
- `chatgpt_function_model.py`: OpenAI ChatGPT function calling
- `davinci_model.py`: OpenAI Text-Davinci-003
- `retriever.py`: Tool retriever for open-domain tool selection

**Algorithm Modules (`toolbench/inference/Algorithms/`)**
- `DFS.py`: Depth-First Search with DFSDT reasoning
- `single_chain`: Single-tool chain reasoning
- `base_search.py`: Base search algorithm

**Evaluation (`toolbench/tooleval/`)**
- `eval_pass_rate.py`: Evaluate success rate of tool usage
- `eval_preference.py`: Compare model outputs using ChatGPT evaluator
- `convert_to_answer_format.py`: Format model predictions for evaluation

**Preprocessing (`preprocess/`)**
- `preprocess_toolllama_data.py`: Convert raw data to training format
- `preprocess_retriever_data.py`: Prepare data for retriever training

**RapidAPI Integration (`toolbench/inference/Downstream_tasks/`)**
- `rapidapi.py`: Wrapper for RapidAPI-based tool execution
- `base_env.py`: Base environment class for tool execution

### Data Structure

- `data/instruction/`: Input instructions (G1/G2/G3 for different complexity levels)
- `data/answer/`: Annotated solution paths and reasoning traces
- `data/toolenv/tools/`: Tool definitions and API documentation (3,451 tools across categories)
- `data/retrieval/`: Retriever training data and corpus
- `data/test_instruction/`: Test queries for evaluation
- `ds_configs/stage2.json`, `stage3.json`: DeepSpeed configuration for training

### Key Scripts (`scripts/`)

- `preprocess_toolllama_data.sh`: Preprocess training data
- `train_toolllama_lora.sh`: Train LoRA model
- `train_retriever.sh`: Train tool retriever
- `inference_toolllama_lora_pipeline.sh`: Run inference with ToolLLaMA-LoRA
- `inference_chatgpt_pipeline_w_rapidapi_key.sh`: Inference with ChatGPT using RapidAPI

## Setup & Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Download dataset
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1XFjDxVZdUY7TXYF2yvzx3pJlS2fy78jk&confirm=yes' -O data.zip
unzip data.zip

# Set environment
export PYTHONPATH=./
```

## Common Development Tasks

### Data Preprocessing

**Preprocess ToolLLaMA training data:**
```bash
export PYTHONPATH=./
python preprocess/preprocess_toolllama_data.py \
    --tool_data_dir data/answer/G1_answer \
    --method DFS_woFilter_w2 \
    --output_file data/answer/toolllama_G1_dfs.json
```

**Preprocess retriever data:**
```bash
export PYTHONPATH=./
python preprocess/preprocess_retriever_data.py \
    --query_file data/instruction/G1_query.json \
    --index_file data/test_query_ids/G1_instruction_test_query_ids.json \
    --dataset_name G1 \
    --output_dir data/retrieval/G1
```

### Training

**Train Tool Retriever:**
```bash
export PYTHONPATH=./
python toolbench/retrieval/train.py \
    --data_path data/retrieval/G1/ \
    --model_name bert-base-uncased \
    --output_path retrieval_model \
    --num_epochs 5 \
    --train_batch_size 32 \
    --learning_rate 2e-5 \
    --warmup_steps 500 \
    --max_seq_length 256
```

**Train ToolLLaMA (Full Model, 2x A100):**
```bash
export PYTHONPATH=./
torchrun --nproc_per_node=2 --master_port=20001 toolbench/train/train_mem.py \
    --model_name_or_path huggyllama/llama-7b \
    --data_path data/toolllama_G123_dfs_train.json \
    --eval_data_path data/toolllama_G123_dfs_eval.json \
    --conv_template tool-llama-single-round \
    --bf16 True \
    --output_dir toolllama \
    --num_train_epochs 2 \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 8 \
    --learning_rate 5e-5 \
    --fsdp "full_shard auto_wrap" \
    --fsdp_transformer_layer_cls_to_wrap 'LlamaDecoderLayer'
```

**Train ToolLLaMA-LoRA (Resource-Efficient):**
```bash
export PYTHONPATH=./
deepspeed --master_port=20001 toolbench/train/train_lora.py \
    --model_name_or_path huggyllama/llama-7b \
    --data_path data/toolllama_G123_dfs_train.json \
    --eval_data_path data/toolllama_G123_dfs_eval.json \
    --conv_template tool-llama-single-round \
    --bf16 True \
    --output_dir toolllama_lora \
    --num_train_epochs 5 \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 2 \
    --learning_rate 5e-5 \
    --deepspeed ds_configs/stage2.json
```

### Inference

**Run ToolLLaMA Inference:**
```bash
export PYTHONPATH=./
export TOOLBENCH_KEY="your_toolbench_key"

python toolbench/inference/qa_pipeline.py \
    --tool_root_dir data/toolenv/tools/ \
    --backbone_model toolllama \
    --model_path ToolBench/ToolLLaMA-7b \
    --max_observation_length 1024 \
    --observ_compress_method truncate \
    --method DFS_woFilter_w2 \
    --input_query_file data/test_instruction/G1_instruction.json \
    --output_answer_file toolllama_dfs_inference_result \
    --toolbench_key $TOOLBENCH_KEY
```

**Run ToolLLaMA-LoRA Inference:**
```bash
export PYTHONPATH=./
python toolbench/inference/qa_pipeline.py \
    --tool_root_dir data/toolenv/tools/ \
    --backbone_model toolllama \
    --model_path huggyllama/llama-7b \
    --lora \
    --lora_path /path/to/ToolLLaMA-7b-LoRA \
    --max_observation_length 1024 \
    --observ_compress_method truncate \
    --method DFS_woFilter_w2 \
    --input_query_file data/test_instruction/G1_instruction.json \
    --output_answer_file toolllama_lora_dfs_inference_result \
    --toolbench_key $TOOLBENCH_KEY
```

**Open-Domain Inference (with Retriever):**
```bash
export PYTHONPATH=./
python toolbench/inference/qa_pipeline_open_domain.py \
    --tool_root_dir data/toolenv/tools/ \
    --corpus_tsv_path data/retrieval/G1/corpus.tsv \
    --retrieval_model_path /path/to/retrieval_model \
    --retrieved_api_nums 5 \
    --backbone_model toolllama \
    --model_path huggyllama/llama-7b \
    --lora \
    --lora_path /path/to/toolllama_lora \
    --max_observation_length 1024 \
    --observ_compress_method truncate \
    --method DFS_woFilter_w2 \
    --input_query_file data/test_instruction/G1_instruction.json \
    --output_answer_file toolllama_lora_dfs_open_domain_inference_result \
    --toolbench_key $TOOLBENCH_KEY
```

### Evaluation with ToolEval

**Prepare model predictions:**
```bash
# Convert predictions to evaluation format
export RAW_ANSWER_PATH=../../data/reproduction_data/model_predictions/
export CONVERTED_ANSWER_PATH=../../data/reproduction_data/model_predictions_converted/
export MODEL_NAME=chatgpt_cot
export METHOD=CoT

for test_set in G1_instruction G1_category G1_tool G2_category G2_instruction G3_instruction
do
    answer_dir=${RAW_ANSWER_PATH}/${MODEL_NAME}/${test_set}
    output_file=${CONVERTED_ANSWER_PATH}/${MODEL_NAME}/${test_set}.json
    python convert_to_answer_format.py \
        --answer_dir ${answer_dir} \
        --method ${METHOD} \
        --output ${output_file}
done
```

**Evaluate Pass Rate:**
```bash
export CONVERTED_ANSWER_PATH=../../data/reproduction_data/model_predictions_converted/
export SAVE_PATH=pass_rate_results
export CANDIDATE_MODEL=chatgpt_cot
export API_POOL_FILE=path/to/openai_key_json_file.json

python eval_pass_rate.py \
    --converted_answer_path ${CONVERTED_ANSWER_PATH} \
    --save_path ${SAVE_PATH} \
    --reference_model ${CANDIDATE_MODEL} \
    --test_ids ../../data/test_ids/ \
    --max_eval_threads 20 \
    --evaluate_times 7
```

**Evaluate Preference (Win Rate):**
```bash
export CONVERTED_ANSWER_PATH=../../data/reproduction_data/model_predictions_converted/
export SAVE_PATH=preference_results
export REFERENCE_MODEL=chatgpt_cot
export CANDIDATE_MODEL=gpt-4-0613_cot
export API_POOL_FILE=path/to/openai_key_json_file.json

python eval_preference.py \
    --converted_answer_path ${CONVERTED_ANSWER_PATH} \
    --reference_model ${REFERENCE_MODEL} \
    --output_model ${CANDIDATE_MODEL} \
    --test_ids ../../data/test_ids/ \
    --save_path ${SAVE_PATH} \
    --pass_rate_result_path ${PASS_TARE_PATH} \
    --max_eval_threads 20 \
    --use_pass_rate true \
    --evaluate_times 7
```

### Running Tests

ToolBench doesn't use a traditional test framework. To test components:

```bash
# Test data preprocessing
python preprocess/preprocess_toolllama_data.py --help

# Test inference pipeline (use small test file)
python toolbench/inference/qa_pipeline.py \
    --tool_root_dir data/toolenv/tools/ \
    --backbone_model toolllama \
    --model_path huggyllama/llama-7b \
    --lora \
    --lora_path /path/to/lora \
    --input_query_file data/instruction/inference_query_demo.json

# Test with single query
export PYTHONPATH=./
python -c "
from toolbench.inference.Downstream_tasks.rapidapi import pipeline_runner
# Add test code here
"
```

### Web Interface

**Start Backend Server:**
```bash
export PYTHONPATH=./
python toolbench/inference/toolbench_server.py \
    --tool_root_dir data/toolenv/tools/ \
    --corpus_tsv_path data/retrieval/G1/corpus.tsv \
    --retrieval_model_path /path/to/retrival_model \
    --retrieved_api_nums 5 \
    --backbone_model toolllama \
    --model_path huggyllama/llama-7b \
    --lora \
    --lora_path /path/to/toolllama_lora \
    --max_observation_length 1024 \
    --method DFS_woFilter_w2
```

**Start Frontend (in separate repo):**
```bash
git clone https://github.com/lilbillybiscuit/chatbot-ui-toolllama
cd chatbot-ui-toolllama
npm install
npm run dev
```

## Important Configuration Files

- `requirements.txt`: Python dependencies (PyTorch, Transformers, FastAPI, DeepSpeed, etc.)
- `ds_configs/stage2.json`: DeepSpeed configuration for LoRA training
- `ds_configs/stage3.json`: DeepSpeed configuration for full model training
- `toolbench/tooleval/requirements.txt`: Minimal dependencies for evaluation only
- `data/toolenv/tools/`: Tool definitions organized by category (3,451 tools)

## Environment Variables

- `PYTHONPATH=.`: Required for all Python scripts
- `TOOLBENCH_KEY`: API key for ToolBench RapidAPI service
- `OPENAI_KEY`: OpenAI API key for ChatGPT/Davinci models
- `RAPIDAPI_KEY`: Custom RapidAPI key for tool execution
- `CUDA_VISIBLE_DEVICES`: GPU selection for training/inference
- `TOOLBENCH_KEY=""`: Empty string for ToolBench evaluation without API calls

## Reasoning Methods

- `CoT@1`: Chain-of-Thought with single attempt
- `DFS_woFilter_w2`: Depth-First Search without filtering (best method)
- `Reflexion@n`: Reflexion-based reasoning with n attempts
- `BFS`: Breadth-First Search
- `UCT_vote`: Upper Confidence bounds applied to Trees voting

## Key Model Configurations

- `backbone_model`: "toolllama", "chatgpt_function", "davinci"
- `model_path`: HuggingFace model name or local path
- `max_observation_length`: 1024 (default)
- `max_sequence_length`: 8192 (default)
- `lora`: Use LoRA fine-tuned model
- `lora_path`: Path to LoRA weights
- `retrieved_api_nums`: Number of APIs to retrieve for open-domain (default: 5)

## Important Notes

1. **Data Download**: Required dataset must be downloaded from Google Drive and extracted to `data/` directory
2. **API Keys**: ToolBench requires either `TOOLBENCH_KEY` or `RAPIDAPI_KEY` for tool execution
3. **Hardware**: Full model training requires 2x A100 80GB GPUs; LoRA training is more resource-efficient
4. **Evaluation**: ToolEval uses ChatGPT for automated evaluation and requires OpenAI API keys
5. **PYTHONPATH**: Must be set to `./` for all Python operations
6. **Tool Categories**: 49 categories of tools in `data/toolenv/tools/` (Sports, Business, Education, etc.)
7. **Test Sets**: G1 (single-tool), G2 (intra-category multi-tool), G3 (intra-collection multi-tool)