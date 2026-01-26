# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Kimina-Prover is a large formal reasoning model that proves mathematical theorems in Lean 4. This repository contains demo scripts demonstrating the model's two key capabilities:
- **Lemma Use**: Leveraging provided lemmas to solve mathematical problems
- **Error Fixing**: Multi-turn proof generation with Lean feedback for auto-fix

The codebase is a thin wrapper around vLLM (model serving) and kimina-lean-server (Lean 4 verification).

## Commands

### Setup
```bash
pip install -r requirements.txt
```

### Serve Model
```bash
vllm serve --host 0.0.0.0 --port 8090 AI-MO/Kimina-Prover-Distill-1.7B
```

### Run Demos
```bash
python lemma_use.py                    # Lemma utilization demo
python error_fix.py                    # Multi-turn error fixing demo
```

### Lean Server Setup (for error_fix.py)
The error fixing demo requires kimina-lean-server to be running:
```bash
git clone https://github.com/project-numina/kimina-lean-server
cd kimina-lean-server
pip install -e .
chmod +x setup.sh && ./setup.sh       # Installs mathlib and repl
python -m server                       # Start server on http://127.0.0.1:12332
```

## Architecture

### Core Components

**utils.py** - Utility functions for proof handling and Lean feedback:
- `extract_proof_from_text()` - Parses proofs from model output using regex (`lean4` code blocks with theorem/:= keywords)
- `create_tool_message()` - Formats Lean errors into human-readable feedback with goals state and code snippets
- `parse_client_response()` - Validates proofs, checking for errors and "sorry" statements
- `get_error_node()` - Traverses Lean infotree to find closest error location
- `filter_error_messages()` - Extracts only severity='error' messages (max 3)

**lemma_use.py** - Single-turn proof generation:
- Calls vLLM API with a problem + optional lemma
- Extracts and prints the generated proof

**error_fix.py** - Multi-turn proof verification and fixing:
- Calls model → verifies with Lean server → formats errors → re-calls model with feedback
- Uses `Lean4Client.verify()` with `infotree_type="original"`
- Output saved to `error_fix_output.json`

### API Endpoints

**Model Server** (vLLM on port 8090):
- OpenAI-compatible `/v1/chat/completions` endpoint
- Default model: `AI-MO/Kimina-Prover-Distill-1.7B`

**Lean Server** (kimina-lean-server on port 12332):
- `Lean4Client.verify()` accepts list of `{"custom_id", "proof"}`
- Returns infotree with goalsBefore/goalsAfter for error location