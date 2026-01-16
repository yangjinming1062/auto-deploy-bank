# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains Python code examples from the book "Developing Apps with GPT-4 and ChatGPT". Each `Chap*_*` folder is a self-contained example demonstrating OpenAI API usage, ranging from basic chat completions to advanced LLM frameworks (LangChain, LlamaIndex).

## Development Commands

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run examples:**
```bash
python [example_folder]/run.py
```

Some examples also include Jupyter notebooks (`.ipynb` files) as alternatives to `run.py`.

## Required Setup

**API Key:** All examples require an `OPENAI_API_KEY` environment variable. Create a `.env` file with:
```
OPENAI_API_KEY=your-key-here
```

**Docker Services:** The following chapters require additional infrastructure:

| Chapter | Service | Command |
|---------|---------|---------|
| Chap3_03_QuestionAnsweringOnPDF | Redis | `docker-compose up -d` |
| Chap5_04_LlamaIndexCustomization | Weaviate | `docker-compose up -d` |

Or run Weaviate directly: `docker run -p 8080:8080 -p 50051:50051 cr.weaviate.io/semitechnologies/weaviate:1.24.9`

## Architecture Patterns

Examples follow a consistent pattern: `run.py` serves as the entry point that imports local modules (e.g., `intentservice.py`, `dataservice.py`) and orchestrates the workflow. Each chapter folder is independent with its own dependencies referenced in `requirements.txt`.