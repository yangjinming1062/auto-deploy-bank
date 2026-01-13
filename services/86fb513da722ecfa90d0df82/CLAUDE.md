# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **machine learning tutorial repository** with 123+ Jupyter notebooks covering a wide range of ML topics. The repository aims to strike a balance between mathematical notation, educational implementations from scratch using Python's scientific stack (numpy, numba, scipy, pandas, matplotlib, pyspark), and open-source library usage (scikit-learn, fasttext, huggingface, onnx, xgboost, lightgbm, pytorch, keras, tensorflow, gensim, h2o, ortools, ray tune, etc.).

## Common Commands

### Setup and Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Jupyter notebook server
jupyter notebook

# Or with specific port
jupyter notebook --port 8888
```

### Notebook Conversion
```bash
# Convert all notebooks to HTML (generates static HTML files for GitHub Pages)
python convert_to_html.py

# Convert notebooks to Airbnb Knowledge Repo format
python convert_to_knowledge_repo.py --ml_repo . --knowledge_repo knowledge-repo

# Deploy knowledge repo webapp
knowledge_repo --repo knowledge-repo deploy
```

### Testing
```bash
# Run all tests
pytest data_science_is_software/tests/

# Run specific test file
pytest data_science_is_software/tests/test_example.py -v

# Run tests with coverage
pytest data_science_is_software/tests/ --cov=src
```

### Notebook Conversion (Manual)
```bash
# Convert single notebook to HTML
jupyter nbconvert --to html --template full notebook.ipynb

# Convert to PDF
jupyter nbconvert --to pdf notebook.ipynb
```

## Project Structure

The repository is organized by machine learning topic areas:

- **`deep_learning/`** - PyTorch, TensorFlow, transformers, LLMs, GNNs, contrastive learning
- **`model_deployment/`** - FastAPI, Kubernetes, AWS, ONNX, LLM batch inference (Ray/VLLM)
- **`model_selection/`** - Cross-validation, hyperparameter tuning (Ray Tune), evaluation metrics
- **`trees/`** - Decision trees, random forests, gradient boosting (XGBoost, LightGBM)
- **`recsys/`** - Matrix factorization, ALS, BPR, WARP, recommendation systems
- **`clustering/`** - K-means, GMM, topic modeling (LDA), TF-IDF
- **`ab_tests/`** - A/B testing, causal inference, quantile regression
- **`text_classification/`** - Naive Bayes, logistic regression, feature selection
- **`time_series/`** - Exponential smoothing, supervised learning for time series, FFT
- **`keras/`** - High-level deep learning API tutorials
- **`big_data/`** - PySpark, H2O, distributed computing
- **`data_science_is_software/`** - Code examples with tests (data pipelines, best practices)
- **`networkx/`** - Graph algorithms, PageRank, influence maximization
- **`search/`** - Information retrieval, BM25
- **`python/`** - Programming techniques, algorithms, decorators, parallel programming

## Code Architecture

### Notebook Format
- Each topic area contains Jupyter notebooks (`.ipynb`) with accompanying HTML exports (`.html`)
- Notebooks include both mathematical explanations and executable code
- Some notebooks have supplementary Python modules in subdirectories

### Python Modules (data_science_is_software/)
Located in `data_science_is_software/`:
```
data_science_is_software/
├── src/
│   └── features/
│       └── build_features.py    # Data preprocessing pipeline
└── tests/
    ├── __init__.py
    └── test_example.py           # Pytest tests for the module
```

This module demonstrates best practices for data science as software engineering, including:
- Modular code structure
- Unit tests with pytest
- Data pipeline patterns
- Feature engineering workflows

### Model Deployment Examples
- **`model_deployment/fastapi_kubernetes/`** - FastAPI application with single/batch prediction endpoints, Kubernetes deployment configs
- **`model_deployment/transformers/`** - Transformer model deployment with ONNX optimization
- **`model_deployment/llm_batch_inference/`** - LLM inference optimization using Ray and VLLM

### Helper Scripts
- **`convert_to_html.py`** - Recursively converts notebooks to HTML for static hosting
- **`convert_to_knowledge_repo.py`** - Converts notebooks to Airbnb Knowledge Repo format

## Key Technologies

This repository uses a comprehensive ML stack:
- **Deep Learning**: PyTorch 2.x, TensorFlow 2.x, Transformers (Hugging Face), PyTorch Lightning
- **Gradient Boosting**: XGBoost, LightGBM
- **Traditional ML**: scikit-learn
- **Distributed Computing**: PySpark 3.2.2, H2O
- **Graph ML**: NetworkX, DGL
- **Model Deployment**: FastAPI, ONNX Runtime, Kubernetes, AWS (boto3)
- **Parallel Computing**: Ray, joblib
- **Visualization**: matplotlib, seaborn

See `requirements.txt` for complete dependency list with specific versions.

## Important Notes

### Notebook Execution
- Most notebooks can be run independently
- Some may require data files in specific paths (e.g., `data/raw/` in data_science_is_software)
- Check individual notebook headers for specific setup requirements

### Development Patterns
- Focus on educational clarity over production-ready code in notebooks
- The `data_science_is_software/` directory contains more structured, testable code
- Notebooks demonstrate both "from scratch" implementations and library usage

### Repository Maintenance
- `changelog.md` tracks all additions and changes to notebooks
- Notebooks are periodically updated when dependencies change
- Author: Ethen Liu (ethen8181)

## Finding Specific Content

1. **Search by topic**: Browse directories matching your ML topic of interest
2. **Search by technique**: Use file search (e.g., "xgboost", "transformer", "ALS")
3. **Read README sections**: The main README.md provides detailed links to all notebooks organized by topic
4. **Check model_deployment/**: For production-oriented examples and deployment code
5. **Review data_science_is_software/**: For best practices and tested code patterns