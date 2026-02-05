# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WebThinker is a deep research framework that empowers Large Reasoning Models (LRMs) to autonomously search, explore web pages, and draft research reports during their thinking process. It enables end-to-end task execution in a single generation, distinguishing it from typical RAG-based approaches.

## Environment Setup

```bash
conda create -n webthinker python=3.9
conda activate webthinker
pip install -r requirements.txt
```

Key dependencies: torch, transformers, vLLm, sentencepiece, tqdm, nltk, pyext, rank_bm25

## Core Commands

### Problem Solving Mode

Single question:
```bash
python scripts/run_web_thinker.py \
    --single_question "What is OpenAI Deep Research?" \
    --search_engine "serper" \
    --serper_api_key "YOUR_GOOGLE_SERPER_API" \
    --api_base_url "YOUR_API_BASE_URL" \
    --model_name "QwQ-32B" \
    --aux_api_base_url "YOUR_AUX_API_BASE_URL" \
    --aux_model_name "Qwen2.5-32B-Instruct" \
    --tokenizer_path "PATH_TO_TOKENIZER" \
    --aux_tokenizer_path "PATH_TO_AUX_TOKENIZER"
```

Benchmark evaluation (e.g., GAIA):
```bash
python scripts/run_web_thinker.py \
    --dataset_name gaia \
    --split dev \
    --concurrent_limit 32 \
    --max_search_limit 15 \
    --search_engine "serper" \
    --serper_api_key "YOUR_API_KEY" \
    --api_base_url "YOUR_API_BASE_URL" \
    --model_name "QwQ-32B" \
    --aux_api_base_url "YOUR_AUX_API_BASE_URL" \
    --aux_model_name "Qwen2.5-32B-Instruct"
```

### Report Generation Mode

```bash
python scripts/run_web_thinker_report.py \
    --single_question "What are the models of OpenAI?" \
    --search_engine "serper" \
    --serper_api_key "YOUR_API_KEY" \
    --api_base_url "YOUR_API_BASE_URL" \
    --model_name "QwQ-32B" \
    --aux_api_base_url "YOUR_AUX_API_BASE_URL" \
    --aux_model_name "Qwen2.5-32B-Instruct"
```

### Demo

```bash
cd demo && streamlit run_demo.py
```

### Evaluation

Problem solving:
```bash
python scripts/evaluate/evaluate.py \
    --output_path "YOUR_OUTPUT_PATH" \
    --task math \
    --use_llm \
    --api_base_url "YOUR_AUX_API_BASE_URL" \
    --model_name "Qwen2.5-72B-Instruct" \
    --extract_answer
```

Report generation:
```bash
python scripts/evaluate/evaluate_report.py \
    --api-base-url "YOUR_API_BASE_URL" \
    --api-key "YOUR_API_KEY" \
    --models "deepseek/deepseek-r1" \
    --model-to-test-dir "YOUR_MODEL_OUTPUT_DIRECTORY"
```

## Architecture

### Two-Model System

WebThinker uses a dual-model architecture:
- **Main Reasoning Model** (e.g., QwQ-32B, DeepSeek-R1): Performs reasoning, generates search queries, and produces final answers/reports
- **Auxiliary Model** (e.g., Qwen2.5-32B-Instruct): Handles auxiliary tasks like web page reading, report drafting/editing, and evaluation

Models are served via vLLM for efficient inference.

### Special Tokens

The framework uses special tokens for tool interaction:
- `<|begin_search_query|>` / `<|end_search_query|>`: Initiate web search
- `<|begin_search_result|>` / `<|end_search_result|>`: Receive search results
- `<|begin_click_link|>` / `<|end_click_link|>`: Click and navigate to URLs
- `<|begin_click_result|>` / `<|end_click_result|>`: Receive clicked page content

### Key Modules

**Search (`scripts/search/bing_search.py`)**:
- Bing Web Search API and Google Serper API support
- Async content fetching with aiohttp
- Jina AI and WebParserClient (Crawl4AI) for JavaScript-rendered content
- PDF extraction with pdfplumber
- Snippet extraction with F1 scoring against full text

**Prompts (`scripts/prompts/prompts.py`)**:
- `get_deep_web_explorer_instruction`: Analyzes search results and extracts relevant info
- `get_web_page_reader_instruction`: Extracts query-relevant content from pages
- `get_search_intent_instruction` / `get_click_intent_instruction`: Generates intents from reasoning

**Evaluation (`scripts/evaluate/`)**:
- `evaluate.py`: LLM-based answer evaluation with optional answer extraction
- `evaluate_report.py`: Listwise report evaluation using DeepSeek-R1 or GPT-4o

**Runner (`scripts/lcb_runner/`)**:
- Alternative runner supporting multiple model providers (Claude, Gemini, DeepSeek, etc.)
- Benchmark runners for code generation and execution tasks

## Data

Datasets in `data/`:
- `GAIA/`: General AI assistant questions (dev split)
- `GPQA/`: PhD-level science questions
- `WebWalkerQA/`: Web exploration tasks
- `HLE/`: Humanity's Last Exam (hard reasoning problems)
- `Glaive/`: Reasoning-v1-20m for report generation

## Model Serving

Before running WebThinker, serve models using vLLM:
```bash
vllm serve Qwen/QwQ-32B --tensor-parallel-size 4
vllm serve Qwen/Qwen2.5-32B-Instruct --tensor-parallel-size 4
```

For improved web crawling, configure WebParserClient in `scripts/search/bing_search.py` to use [Crawl4AI](https://github.com/unclecode/crawl4ai).

## Output Structure

Model outputs are saved to `outputs/{model_name}/{dataset}.{split}/` with:
- Raw predictions and reasoning traces
- Evaluation results (JSON)
- Generated reports (markdown for report mode)