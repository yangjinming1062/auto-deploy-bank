# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **research project** comparing Cache-Augmented Generation (CAG) vs. Retrieval-Augmented Generation (RAG) for question-answering tasks using LLMs. The codebase implements experiments from the paper "Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks" (arXiv:2412.15605), accepted at ACM Web Conference 2025.

**Key Innovation**: CAG preloads all knowledge into the LLM's context window and caches the KV cache at inference time, eliminating retrieval latency and errors. See `README.md:1-24` for full motivation and limitations.

## Quick Start

### Setup
```bash
# 1. Install dependencies
pip install -r ./requirements.txt

# 2. Download datasets (SQuAD and HotpotQA from Kaggle)
sh ./downloads.sh
# or using PDM:
pdm download

# 3. Configure API keys
cp ./.env.template ./.env
# Edit .env with: GOOGLE_API_KEY, OPENAI_API_KEY, JINA_API_KEY, HF_TOKEN
```

### Running Experiments

#### CAG Experiments (kvcache.py)
```bash
python ./kvcache.py \
  --kvcache file \
  --dataset "squad-train" \
  --similarity bertscore \
  --maxKnowledge 5 \
  --maxParagraph 100 \
  --maxQuestion 1000 \
  --modelname "meta-llama/Llama-3.1-8B-Instruct" \
  --randomSeed 0 \
  --output "./results_kvcache.txt"
```

#### RAG Experiments (rag.py)
```bash
python ./rag.py \
  --index "bm25" \
  --dataset "hotpotqa-train" \
  --similarity bertscore \
  --maxKnowledge 80 \
  --maxParagraph 100 \
  --maxQuestion 80 \
  --topk 3 \
  --modelname "meta-llama/Llama-3.1-8B-Instruct" \
  --randomSeed 0 \
  --output "./rag_results.txt"
```

### Docker
```bash
# Build
docker build -t my-cag-app .

# Run (GPU)
docker run --gpus all -it --rm my-cag-app

# Run (CPU)
docker run -it --rm my-cag-app

# Override default command to run rag.py instead
docker run --gpus all -it --rm my-cag-app python ./rag.py --index "bm25" --dataset "hotpotqa-train" --similarity bertscore --maxKnowledge 80 --maxParagraph 100 --maxQuestion 80 --topk 3 --modelname "meta-llama/Llama-3.1-8B-Instruct" --randomSeed 0 --output "./rag_results.txt"
```

## Codebase Architecture

This is a research prototype with a simple structure focused on comparative experiments.

### Core Implementation Files

- **`kvcache.py`** (359 lines) - CAG implementation
  - Loads Llama models with 4-bit quantization
  - Preprocesses knowledge into KV cache
  - Generates responses using cached KV values
  - Main function: `kvcache_test()`

- **`rag.py`** (326 lines) - RAG implementation for comparison
  - Implements multiple retrievers: OpenAI, Gemini, BM25, Jina
  - Dynamic retrieval at inference time
  - Main function: `rag_test()`

### Library Module (`cag/`)

- **`cag/dataset.py`** - Dataset loading and preprocessing
  - `squad()` - SQuAD v1.1 parser
  - `hotpotqa()` - HotpotQA parser
  - `kis()` - Custom CSV parser
  - Returns: `(knowledge_texts, question_answer_pairs)`

- **`cag/similarity.py`** - Evaluation metrics
  - `bert()` - BERT-score semantic similarity using `sentence-transformers/all-MiniLM-L6-v2`

- **`config.py`** - Simple configuration (Enum pattern)

### Automation Scripts (`scripts/`)

- **`run.sh`** - Generic experiment runner (commented examples)
- **`random-squad.sh`** - Batch experiments on SQuAD with k=3,5,7
- **`random-hotpot-k*-sh`** - Batch experiments on HotpotQA with various k values (16-80)
  - Automatically generates random seeds for reproducibility
  - Logs output to `./log/` directory

### Data Directories

- **`datasets/`** - Experimental datasets
  - `squad/` - Stanford Question Answering Dataset
  - `hotpotqa/` - Multi-hop QA dataset
  - Auto-populated by `downloads.sh`

- **`data_cache/`** - KV cache storage (empty, .gitkeep only)

- **`results/`** - Experiment outputs with subdirectories by dataset

- **`random_results/`** - Additional results from batch scripts

## Key Parameters

### CAG (kvcache.py)
- `--kvcache`: "file" (required)
- `--dataset`: "hotpotqa-train" or "squad-train"
- `--maxKnowledge`: Number of documents to include (see token guide below)
- `--maxParagraph`: 100 (default)
- `--maxQuestion`: Number of questions to evaluate
- `--usePrompt`: Flag to disable KV cache acceleration
- `--output`: Results filepath

### RAG (rag.py)
- `--index`: Retrieval method ("openai", "bm25", "gemini", "jina")
- `--dataset`: Same as CAG
- `--maxKnowledge`: Same as CAG
- `--maxQuestion`: Same as CAG
- `--topk`: Number of retrieved documents (1, 3, 5, 10, 20)
- `--output`: Same as CAG

## Token Count Guide (Important!)

### SQuAD Dataset
- k=3 → ~21,000 tokens
- k=4 → ~32,000 tokens
- k=7 → ~50,000 tokens

### HotpotQA Dataset
- k=1 → ~1,400 tokens
- k=16 → ~22,400 tokens
- k=24 → ~33,667 tokens
- k=32 → ~44,800 tokens
- k=48 → ~64,000 tokens
- k=64 → ~85,000 tokens
- k=80 → ~106,000 tokens
- Full dataset → ~10,038,084 tokens

### Dataset Characteristics
- **SQuAD**: 1 document ≈ 150 questions
- **HotpotQA**: 1 document = 1 question

## Configuration & Dependencies

- **Package Manager**: PDM (see `pyproject.toml`)
- **Build System**: Docker (PyTorch 2.5.1 with CUDA 12.1)
- **Models**: Llama-3.1-8B-Instruct (primary), Llama-3.2-1B-Instruct (alternative)
- **Quantization**: 4-bit for memory efficiency
- **Evaluation**: BERT-score semantic similarity

## Important Notes

- **No test framework**: This is a research prototype, not production code
- **Reproducibility**: Always set `--randomSeed` for consistent results
- **Environment variables**: Required keys in `.env` (HF_TOKEN, OPENAI_API_KEY, GOOGLE_API_KEY, JINA_API_KEY)
- **Context window**: CAG requires entire knowledge to fit in context - check token counts above
- **Batch experiments**: Use scripts in `scripts/` directory for automated runs with proper logging
- **Results**: Output files contain BERT-score similarity metrics for comparison
- **Citation**: See `README.md:157-167` for paper citation format

## Common Development Tasks

### Running a single test case
```bash
# Small test on SQuAD
python ./kvcache.py --kvcache file --dataset "squad-train" --similarity bertscore \
  --maxKnowledge 3 --maxParagraph 100 --maxQuestion 50 \
  --modelname "meta-llama/Llama-3.1-8B-Instruct" --randomSeed 42 \
  --output "./test_result.txt"
```

### Batch experiments
```bash
# Run all SQuAD experiments with logging
bash ./scripts/random-squad.sh

# Run HotpotQA with k=16 and k=80
bash ./scripts/random-hotpot-k16-k80.sh

# Monitor logs
tail -f ./log/random-squad-k3.log
```

### Viewing results
```bash
# Compare outputs
diff ./results_kvcache.txt ./rag_results.txt

# Analyze BERT-score metrics
grep "bertscore" ./results/*.txt
```

## Troubleshooting

- **Missing API keys**: Copy `.env.template` to `.env` and populate all required keys
- **CUDA out of memory**: Try smaller models or reduce `maxKnowledge`
- **Dataset not found**: Run `sh ./downloads.sh` to fetch from Kaggle
- **Context too long**: Reduce `maxKnowledge` based on token counts above
- **Docker environment issues**: Ensure `.env` is populated before building image