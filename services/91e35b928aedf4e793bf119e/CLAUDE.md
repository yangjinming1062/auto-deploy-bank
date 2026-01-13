# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Setup

```bash
# Create and activate virtual environment with Python 3.11
uv venv --python=3.11
source .venv/bin/activate

# Install package in development mode
pip install -e .

# Install pre-commit hooks
uv pip install pre-commit
pre-commit install
```

## Common Commands

### Run the Application
```bash
# Start web interface with default model
python -m docext.app.app

# Start with specific model and configuration
python -m docext.app.app --model_name hosted_vllm/nanonets/Nanonets-OCR-s --max_img_size 1024

# Run with custom ports
python -m docext.app.app --vlm_server_port 8000 --ui_port 7860
```

Key command-line options:
- `--model_name`: Model to use (prefix with `hosted_vllm/` for local vLLM, `ollama/` for Ollama)
- `--max_img_size`: Maximum image size for processing (default: 2048)
- `--concurrency_limit`: Concurrent requests (default: 1)
- `--gpu_memory_utilization`: GPU memory usage (default: 0.9)
- `--max_model_len`: Maximum tokens (default: 15000)
- `--dtype`: Model dtype - bfloat16 or float16 (default: bfloat16)
- `--max_gen_tokens`: Max generation tokens (default: 10000)

See `docext/app/args.py:7-95` for all available options.

### Run Benchmarks
```bash
# Run the IDP leaderboard benchmark
python docext/benchmark/benchmark.py

# Configure benchmark via configs/benchmark.yaml
```

## Code Architecture

docext is an on-premises document intelligence toolkit with three core capabilities:

### 1. PDF/Image to Markdown Conversion
Converts documents to structured markdown with semantic understanding.

**Key Files:**
- `docext/core/pdf2md/pdf2md.py:16-100` - Streaming markdown conversion
- `docext/app/pdf2md.py` - Gradio UI for PDF2MD
- `docext/core/prompts.py` - Prompt templates

**Features:**
- LaTeX equation recognition (inline and block)
- Image descriptions in `<img></img>` tags
- Signature detection in `<signature></signature>` tags
- Watermark detection in `<watermark></watermark>` tags
- Page numbers in `<page_number></page_number>` tags
- Table conversion to HTML
- Form checkbox/radio button conversion to Unicode (☐, ☑, ☒)

### 2. Document Information Extraction
Extracts structured fields from documents with confidence scoring.

**Key Files:**
- `docext/core/extract.py:22-98` - Field extraction logic
- `docext/core/config.py:3-76` - Pre-built templates (invoices, passports)
- `docext/core/extract.py:45-98` - Confidence scoring (High/Low)

**Pre-built Templates:**
- Invoice templates (with seller/buyer info, items, taxes)
- Passport template (name, DOB, passport number, etc.)

**Flow:**
1. `docext/core/extract.py:22-32` - Create field messages
2. `docext/core/client.py` - Send request to VLM
3. `docext/core/confidence.py` - Calculate confidence scores
4. Returns structured DataFrame with fields, answers, and confidence

### 3. Intelligent Document Processing Leaderboard
Benchmark for evaluating VLMs on document tasks.

**Key Files:**
- `docext/benchmark/benchmark.py:1-100` - Main benchmark runner
- `docext/benchmark/tasks.py` - Task definitions (KIE, OCR, VQA, etc.)
- `configs/benchmark.yaml` - Benchmark configuration
- `docext/benchmark/utils.py` - Helper functions

**Evaluation Tasks:**
- KIE (Key Information Extraction)
- OCR (Optical Character Recognition)
- VQA (Visual Question Answering)
- Document Classification
- Long Document Processing
- Table Extraction
- Confidence Score Calibration

## Core Components

### Entry Points
- `docext/app/app.py:350-372` - `docext_app()` is the main entry point
- Command-line: `python -m docext.app.app` (from `setup.py:33-35`)

### Module Structure
```
docext/
├── app/                    # Gradio UI and CLI
│   ├── app.py             # Main web interface
│   ├── args.py            # Argument parsing
│   ├── pdf2md.py          # PDF to markdown UI
│   └── utils.py           # Utility functions
├── core/                   # Core functionality
│   ├── client.py          # HTTP client for VLM requests
│   ├── vllm.py            # vLLM server management
│   ├── extract.py         # Information extraction logic
│   ├── config.py          # Templates and constants
│   ├── pdf2md/            # PDF to markdown conversion
│   ├── utils.py           # Image/file utilities
│   ├── prompts.py         # Prompt templates
│   └── confidence.py      # Confidence scoring
└── benchmark/             # IDP Leaderboard
    ├── benchmark.py       # Benchmark runner
    ├── tasks.py           # Task definitions
    └── ...
```

### Model Support
**Local Models (vLLM - Linux only):**
- Models with `hosted_vllm/` prefix
- Supports AWQ quantization
- Auto-starts vLLM server if not running

**Local Models (Ollama - Linux/MacOS):**
- Models with `ollama/` prefix
- Requires Ollama server on port 11434

**Vendor-Hosted Models:**
- OpenAI, Anthropic, Google Gemini, etc.
- Set API keys via environment variables

## Configuration Files

- `configs/benchmark.yaml` - Benchmark settings (tasks, datasets, models)
- `docext/core/config.py` - Pre-built extraction templates
- `requirements.txt` - Python dependencies

## Environment Variables

- `VLM_MODEL_URL` - Set automatically by app, points to VLM server
- `API_KEY` - For vendor-hosted models (OpenAI, Anthropic, etc.)

## Development Notes

- Pre-commit hooks enforce: trailing-whitespace, end-of-file-fixer, check-yaml, debug-statements, black, mypy, pyupgrade
- Uses `uv` for dependency management
- Python 3.11+ required (setup.py:24)
- No traditional test suite found
- Gradio auth: admin/admin (can change via `--no-share` flag)

## Key Workflows

### Adding a New Document Template
1. Add template fields to `docext/core/config.py:TEMPLATES_FIELDS`
2. Add template tables to `docext/core/config.py:TEMPLATES_TABLES`
3. Fields should include "field_name" and "description" keys

### Modifying Extraction Prompts
- Field extraction prompts: `docext/core/prompts.py` (look for `get_fields_messages`)
- Table extraction prompts: `docext/core/prompts.py` (look for `get_tables_messages`)
- Confidence prompts: `docext/core/confidence.py`

### Adding Benchmark Tasks
1. Define task in `docext/benchmark/tasks.py`
2. Configure dataset paths in `configs/benchmark.yaml`
3. Update task evaluation logic in `docext/benchmark/benchmark.py`

## Important Implementation Details

- Image processing: PDFs converted to images via `docext/core/utils.py:convert_files_to_images`
- Streaming responses: `docext/core/pdf2md/pdf2md.py:16-71` for markdown conversion
- Concurrency: Controlled via `--concurrency_limit` flag
- Memory management: `--max_img_size` and `--gpu_memory_utilization` flags
- Confidence scoring: Binary (High/Low) per extracted field