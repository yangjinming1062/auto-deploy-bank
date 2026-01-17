# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FLARE (Forward-Looking Active REtrieval augmented generation) is a research implementation from the paper "Active Retrieval Augmented Generation" (arXiv:2305.06983). It implements active retrieval-augmented generation that anticipates future content to use as retrieval queries.

## Development Commands

### Environment Setup
```bash
# Create conda environment
conda create -n flare python=3.8
conda activate flare

# Install dependencies from setup.sh
./setup.sh
# This installs: PyTorch 1.12.1, transformers==4.24.0, beir==1.0.1, spacy==3.5.0, and downloads en_core_web_sm
```

### Data Preparation
```bash
# Download Wikipedia dump for retrieval corpus
mkdir -p data/dpr
wget -O data/dpr/psgs_w100.tsv.gz https://dl.fbaipublicfiles.com/dpr/wikipedia_split/psgs_w100.tsv.gz
cd data/dpr && gzip -d psgs_w100.tsv.gz && cd ../..

# Build Elasticsearch index (required for Wikipedia-based retrieval)
wget -O elasticsearch-7.17.9.tar.gz https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.9.tar.gz
tar zxvf elasticsearch-7.17.9.tar.gz
cd elasticsearch-7.17.9 && nohup bin/elasticsearch &
python prep.py --task build_elasticsearch --inp data/dpr/psgs_w100.tsv wikipedia_dpr
```

### Run FLARE Experiments
```bash
# Configure OpenAI keys in keys.sh before running
./openai.sh 2wikihop configs/2wikihop_flare_config.json
./openai.sh wikiasp configs/wikiasp_flare_config.json

# Debug mode (walks through one example at a time)
debug=true ./openai.sh 2wikihop configs/2wikihop_flare_config.json

# Evaluate results
python prep.py --task eval --inp "output/2wikihop/text-davinci-003/*.jsonl" --dataset 2wikihop
```

### Bing Search Setup (for WikiAsp experiments)
```bash
export BING_SEARCH_KEY=$YOUR_KEY
python bing_search_cache_server.py &> bing_log.out &
```

## Architecture

### Core Components

**src/openai_api.py** - Main experiment driver
- `QueryAgent` class: Handles iterative retrieval-augmented generation with look-ahead prediction
- `KeyManager` class: Manages OpenAI API key rotation across multiple keys
- Supports both chat models (GPT-3.5-turbo) and completion models (text-davinci-003)
- Implements look-ahead retrieval that predicts upcoming sentences to generate retrieval queries
- Handles batching and multiprocessing for parallel API calls

**src/retriever.py** - Retrieval system
- `BM25` class: Wrapper for retrieval via Elasticsearch or Bing
- Patches BEIR's BM25Search and ElasticSearch classes with custom search methods
- `SearchEngineConnector`: Bing web search adapter

**src/datasets.py** - Dataset loaders
- `StrategyQA`, `WikiMultiHopQA`, `WikiAsp`, `ASQA` classes
- Inherit from `BaseDataset` providing entity F1, exact match, and F1 scoring
- Handle few-shot prompt formatting

**src/templates.py** - Prompt management
- `CtxPrompt` class: Builds retrieval-augmented prompts with context
- `ApiReturn` class: API response wrapper with token probabilities
- Handles look-ahead sentence filtering and masking

**src/utils.py** - Utilities
- `openai_api_call()`: Retries with exponential backoff on rate limits
- `Utils`: Model type detection (chat vs completion)

**prep.py** - Utility script
- `eval()`: Evaluates predictions with dataset-specific metrics
- `build_elasticsearch()`: Indexes corpus documents
- `jsonl_to_keyvalue()`: Converts predictions to key-value format

### Data Flow

1. `openai.sh` sets dataset parameters and calls `src.openai_api.py`
2. Dataset loader (`src/datasets.py`) loads and formats examples
3. `QueryAgent` generates text iteratively:
   - Generates look-ahead tokens (configurable steps or until boundary)
   - Filters/masks low-confidence tokens to form retrieval queries
   - Retrieves documents via BM25/Elasticsearch
   - Continues generation with retrieved context
4. Results written to JSONL files with traces for analysis

### Configuration (configs/*.json)

Key retrieval parameters:
- `look_ahead_steps`: Number of tokens to generate before retrieval
- `look_ahead_filter_prob`: Threshold to filter tokens as queries
- `frequency`: Token interval for regular retrieval
- `boundary`: Stop token that triggers retrieval
- `topk`: Number of documents to retrieve

## Key Files

- `keys.sh`: OpenAI API keys (NEVER commit)
- `openai.sh`: Main entry point for experiments
- `configs/`: FLARE configurations per dataset
- `prep.py`: Index building and evaluation