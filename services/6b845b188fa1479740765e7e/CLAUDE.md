# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PaSa is an LLM-powered academic paper search agent that autonomously searches for and selects relevant papers based on user queries. It uses a two-agent system:
- **Crawler**: Generates search queries and expands citation networks
- **Selector**: Scores paper relevance to filter results

## Commands

### Installation
```bash
# Requires custom transformers fork for flash attention support
git clone git@github.com:hyc2026/transformers.git
cd transformers && pip install -e .
cd ..

pip install -r requirements.txt
```

**Required**: Set `GOOGLE_KEY` in `utils.py` with your serper.dev API key for Google Search.

### Running the Paper Search Agent
```bash
python run_paper_agent.py
```

Optional arguments:
- `--input_file`: Path to input queries (default: `data/RealScholarQuery/test.jsonl`)
- `--crawler_path`: Path to crawler model checkpoint
- `--selector_path`: Path to selector model checkpoint
- `--output_folder`: Output directory for results
- `--expand_layers`: Number of citation expansion layers (default: 2)
- `--search_queries`: Number of search queries per layer (default: 5)
- `--search_papers`: Papers to retrieve per query (default: 10)
- `--expand_papers`: Papers to expand per layer (default: 20)
- `--threads_num`: Parallel threads (default: 20)

### Evaluating Results
```bash
python metrics.py --output_folder results
# For ensemble evaluation, add: --output_folder_ensemble <ensemble_folder>
```

### Training Your Own Agent
Training requires additional cloned repositories and GPU resources.

**Installation:**
```bash
git clone git@github.com:hyc2026/trl.git
cd trl && pip install -e ..
git clone git@github.com:hyc2026/transformers.git
cd ../transformers && pip install -e ..
```

**Selector SFT Training:**
```bash
cd trl
accelerate launch \
    --config_file examples/accelerate_configs/deepspeed_zero3.yaml \
    --num_processes 8 --main_process_port 2501 \
    examples/scripts/sft.py \
    --model_name_or_path Qwen2.5-7B-Instruct \
    --dataset_name ../data/sft_selector/train.jsonl \
    --learning_rate 1.0e-5 --num_train_epochs 1 --bf16 True \
    --per_device_train_batch_size 4 --gradient_accumulation_steps 1 \
    --gradient_checkpointing --logging_steps 50 --save_steps 2000 \
    --max_seq_length 1024 --output_dir ../results/sft_selector \
    --attn_implementation "flash_attention_2"
```

**Crawler SFT Training:**
```bash
cd trl
accelerate launch \
    --config_file examples/accelerate_configs/deepspeed_zero3.yaml \
    --num_processes 8 --main_process_port 2501 \
    examples/scripts/sft.py \
    --model_name_or_path Qwen2.5-7B-Instruct \
    --dataset_name ../data/sft_crawler/train.jsonl \
    --learning_rate 1.0e-5 --num_train_epochs 1 --bf16 True \
    --per_device_train_batch_size 4 --gradient_accumulation_steps 1 \
    --gradient_checkpointing --logging_steps 50 --save_steps 2000 \
    --max_seq_length 1024 --output_dir ../results/sft_crawler \
    --attn_implementation "flash_attention_2"
```

**Crawler PPO Training:**
```bash
cd trl
accelerate launch \
    --config_file examples/accelerate_configs/deepspeed_zero3_multi.yaml \
    --main_process_port 2501 \
    examples/scripts/ppo/ppo_tldr.py \
    --dataset_name ../data/AutoScholarQuery/train.jsonl \
    --dataset_test_split validation \
    --output_dir ../results/ppo_crawler \
    --learning_rate 1e-6 --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 4 --total_episodes 16000 \
    --paper_db ../data/paper_database/cs_paper_2nd.zip \
    --paper_id ../data/paper_database/id2paper.json \
    --model_name_or_path ../output/sft_crawler \
    --sft_model_path ../output/sft_crawler \
    --reward_model_path ../output/sft_crawler \
    --attn_implementation "flash_attention_2" --response_length 1024 \
    --expand_select_score 1.5 --expand_cost 0.1 \
    --search_select_score 1.5 --search_cost 0.1 \
    --use_selector True
```

## Architecture

### Core Components

**PaperAgent** (`paper_agent.py`): Main orchestrator that coordinates the search and expand pipeline.
- `search()`: Generates queries via Crawler and searches Google for papers
- `expand(depth)`: Crawls citations from found papers
- `run()`: Executes the full search + expand pipeline for configured layers

**Agent** (`models.py`): LLM wrapper using Hugging Face Transformers with chat template support.
- `infer(prompt)`: Single inference call
- `batch_infer(prompts)`: Batched inference
- `infer_score(prompts)`: Returns probability of "True" for relevance scoring

**PaperNode** (`paper_node.py`): Tree node representing a paper with metadata, child nodes, and citations.

**Utils** (`utils.py`): Search and parsing utilities.
- `google_search_arxiv_id()`: Google Search API via serper.dev
- `search_paper_by_arxiv_id()` / `search_paper_by_title()`: Fetch paper metadata
- `search_section_by_arxiv_id()`: Extract citations from paper sections via ar5iv
- `parse_html()`: Parse ar5iv HTML to extract sections and citations

### Data Flow

1. User query → Crawler generates search queries
2. Queries → Google Search → arXiv ID extraction
3. arXiv IDs → Paper metadata + Selector scoring
4. Selected papers → Section citation extraction
5. Citations → New papers → Repeat for N expand layers

### Key Configuration

- **Google Search API**: Requires serper.dev API key (set `GOOGLE_KEY` in `utils.py`)
- **Models**: Qwen2.5-7B-Instruct fine-tuned checkpoints (`pasa-7b-crawler`, `pasa-7b-selector`)
- **Paper Database**: Local CS paper database + arXiv API fallback

### Data Directory Structure
```
data/
├── AutoScholarQuery/
│   ├── dev.jsonl
│   ├── test.jsonl
│   └── train.jsonl
├── paper_database/
│   ├── cs_paper_2nd.zip
│   └── id2paper.json
├── RealScholarQuery/
│   └── test.jsonl
├── sft_crawler/
│   └── train.jsonl
└── sft_selector/
    ├── test.jsonl
    └── train.jsonl
```

### Model Checkpoint Structure
```
checkpoints/
├── pasa-7b-crawler/
└── pasa-7b-selector/
```

### Prompt Templates (`agent_prompt.json`)

- `generate_query`: Creates search query variants
- `select_section`: Determines which sections to crawl for citations
- `get_selected` / `get_value`: Evaluates paper relevance (True/False output)