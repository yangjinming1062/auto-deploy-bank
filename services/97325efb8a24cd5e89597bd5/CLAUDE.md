# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **W&B AI Academy** - an educational repository containing materials for learning AI/ML, organized by topic. Each subdirectory is a self-contained course with notebooks, Python examples, and documentation.

## Repository Structure

This is an educational repository with self-contained ML/LLM courses in separate directories. Each course has its own `README.md`, `requirements.txt`, and typically contains:
- `notebooks/` - Jupyter notebooks (primary learning format)
- `src/` - Python application code
- `data/` - Course datasets

## Common Commands

### Install Course Dependencies
```bash
cd <course-directory>
pip install -r requirements.txt
```

### Run Notebooks
- **Local**: Open with Jupyter or VS Code
- **Colab**: Use the "Open in Colab" badge in course READMEs

## Docker

```bash
docker build -t wandb-edu .
docker run -it wandb-edu
```

## Key Libraries

- **wandb** - Experiment tracking (required by most courses)
- **langchain** - LLM application framework
- **openai** - OpenAI API client
- **PyTorch Lightning** - Deep learning (lightning/ course)
- **Keras** - Deep learning (keras/ course)