# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a comprehensive collection of Vertex AI MLOps workflows and examples for Google Cloud machine learning operations. The repository is primarily composed of Jupyter notebooks (`.ipynb`) that demonstrate end-to-end ML workflows, with supporting Python modules and configuration files.

## Key Dependencies

**Python 3.13.3** is the standard version. Core packages include:
- `google-cloud-aiplatform` - Vertex AI SDK
- `google-genai` - Google GenAI SDK
- `google-cloud-bigquery` - BigQuery client
- `kfp` - Kubeflow Pipelines
- `bigframes` - BigQuery DataFrames
- `scikit-learn`, `xgboost`, `tensorflow`, `pytorch` - ML frameworks
- `pydantic` - Data validation
- `mlflow` - Experiment tracking

## Development Commands

This repository uses Poetry for dependency management with taskipy for tasks:

```bash
# Setup development environment
pyenv install 3.13.3
pyenv local 3.13.3
python -m venv .venv
source .venv/bin/activate
poetry install

# Generate requirements files (common pattern across subdirectories)
task req_full          # Full requirements.txt from poetry.lock
task req_brief         # Top-level packages only
task req_colab         # Brief requirements for Colab (no ipython/ipykernel)
task reqs              # Builds full + brief
task reqs_all          # Builds all three variants

# Register poetry env as Jupyter kernel
task kernel
```

## Repository Structure

The repository is organized into major directories that serve different purposes:

- **MLOps/** - MLOps workflows including Pipelines, Feature Store, Model Evaluation, Model Monitoring, Experiment Tracking, and Serving
- **Applied GenAI/** - Generative AI workflows for chunking, embeddings, retrieval, ranking, generation, validation, and RAG systems
- **Applied ML/** - Applied ML solutions including Forecasting, AI Agents (ADK-based), Anomaly Detection, and Optimization
- **Framework Workflows/** - Framework-specific training workflows for CatBoost, Keras, PyTorch, BQML, etc.
- **Core/** - Template files and common utilities used across the repository

## Notebook Pattern

Notebooks follow a consistent pattern:
1. Each directory has a `readme.md` with navigation and context
2. Tracking pixels are embedded in all markdown and notebook files
3. Most notebooks are self-contained and install their dependencies inline
4. The `core/notebook-template/` directory contains the standard template structure

## Project Configuration

Each project directory typically contains:
- `pyproject.toml` - Poetry configuration with dependency definitions
- `requirements.txt` - Full dependencies (generated)
- `requirements-brief.txt` - Top-level packages (generated)
- `requirements-colab.txt` - Colab-compatible deps (no ipython/ipykernel)
- `.python-version` - Python version specification (usually 3.13.3)

## Key SDK Patterns

**Vertex AI Initialization:**
```python
from google.cloud import aiplatform
aiplatform.init(project=PROJECT, location=REGION)
```

**GenAI with Gemini:**
```python
from google import genai
client = genai.Client(vertexai=True, project=PROJECT, location=REGION)
```

**Kubeflow Pipelines:**
```python
import kfp
from kfp import dsl
```

## Google Cloud Setup

Notebooks are designed to run on minimal compute (like `n1-standard-2`) with heavy work delegated to Vertex AI, BigQuery, and other GCP services. Most examples require:
- A GCP project with Vertex AI API enabled
- Appropriate IAM permissions
- BigQuery dataset access for data sources

## Legacy Content

Older content is being migrated to `legacy/` subdirectories within respective folders as the repository evolves toward an MLOps-focused structure.