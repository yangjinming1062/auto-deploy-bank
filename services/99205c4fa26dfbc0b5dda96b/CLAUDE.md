# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DeepConf (Deep Think with Confidence) is an efficient parallel thinking framework for LLMs built on vLLM. It supports reasoning tasks (math, science, coding) with two operating modes:
- **Online mode**: Confidence-based early stopping for efficiency
- **Offline mode**: Full batch generation with multiple voting strategies

## Installation

```bash
pip install deepconf
uv pip install -r requirements.txt  # For development
```

Dependencies: vLLM (0.10.2), Dynasor, transformers, pandas, numpy, tqdm

## Common Commands

Run example scripts from the repository root:
```bash
# Online mode with confidence-based early stopping
python examples/example_online.py --qid $QID --rid $RID --dataset brumo_2025.jsonl --total_budget 256 --output_dir online-dpsk

# Baseline (no early exit)
python examples/example_online_baseline.py --qid $QID --rid $RID --dataset brumo_2025.jsonl --total_budget 256 --output_dir baseline-dpsk

# Offline batch mode
python examples/example_offline.py

# Analyze online results
python examples/example_analyze_online.py --output_dir ./online-dpsk/ --max_qid 29 --rids 1
```

## Architecture

```
deepconf/
├── wrapper.py         # Main DeepThinkLLM class - entry point for all operations
├── outputs.py         # DeepThinkOutput dataclass - contains all results
├── utils.py           # Voting functions, confidence computation, trace processing
├── processors.py      # vLLM logits processors for early-stopping
└── __init__.py        # Exports DeepThinkLLM
```

### Key Classes

**DeepThinkLLM** (`wrapper.py`): Wraps vLLM LLM with deep thinking capabilities.
- `__init__(model, **vllm_kwargs)`: Initialize with any vLLM-compatible arguments
- `generate()`: Standard vLLM generation
- `deepthink(prompt, mode, ...)`: Enhanced reasoning with voting

**DeepThinkOutput** (`outputs.py`): Dataclass containing results.
- `final_answer`, `voted_answer`: Selected answers
- `voting_results`: Dict of all voting method results
- `all_traces`, `warmup_traces`, `final_traces`: Generated reasoning traces
- `conf_bar`: Confidence threshold (online mode)

### Core Processing Pipeline

1. **Generation**: vLLM generates multiple reasoning traces with `logprobs=20`
2. **Confidence**: Computed from token logprobs using mean negative log probability
3. **Answer Extraction**: Parses `\boxed{...}` from model output
4. **Voting**: Multiple strategies (majority, weighted by mean/tail/bottom-window confidence)
5. **Early Stopping** (online): Uses sliding window confidence threshold to stop generation early

### Confidence Computation (`utils.py`)

- `compute_confidence()`: Mean negative logprob per token
- `compute_least_grouped()`: Sliding window mean for early-stop threshold
- Voting methods in `compute_all_voting_results()`: majority, weighted variants, top-k filtered

### Logits Processors (`processors.py`)

`WrappedPerReqLogitsProcessor` enables confidence-based early stopping by masking logits when sliding window confidence drops below threshold during generation.