# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a machine learning educational repository containing Jupyter notebooks and Python modules documenting personal learning on data science and ML topics. The content strikes a balance between mathematical explanations, implementations from scratch using NumPy/SciPy/Pandas, and open-source library usage (scikit-learn, Hugging Face, XGBoost, PyTorch, etc.).

## Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests
Tests are located in specific modules and use either `unittest` or `pytest`.

```bash
# Run all tests in a module using pytest
pytest data_science_is_software/tests/

# Run unittest tests
python python/test.py
```

### Convert Notebooks to HTML
The repository includes a script to recursively convert all Jupyter notebooks to static HTML files:
```bash
python convert_to_html.py
```

### View Notebooks
Launch Jupyter Notebook or Lab:
```bash
jupyter notebook
# or
jupyter lab
```

## Repository Structure

The repository is organized by machine learning topic as top-level directories:

- **deep_learning/** - Neural networks, transformers, contrastive learning, LLMs
- **recsys/** - Recommendation systems (ALS, BPR, WARP, ANN benchmarks)
- **clustering/** - K-means, GMM, LDA topic modeling
- **model_selection/** - Cross-validation, metrics, hyperparameter tuning
- **trees/** - Decision trees, Random Forest, XGBoost, LightGBM
- **keras/** - Keras/TensorFlow implementations
- **text_classification/** - Naive Bayes, logistic regression, chi-square
- **time_series/** - Exponential smoothing, supervised time series
- **big_data/** - PySpark, H2O examples
- **ab_tests/** - A/B testing, causal inference
- **model_deployment/** - FastAPI, AWS S3, inference optimization
- **python/** - Python programming tutorials (parallel, pandas, decorators)

### Notebook Format

Most content is in `.ipynb` files. Some notebooks include supporting Python modules (typically in a `__init__.py` file alongside the notebook) for reusable code.

### Data Files

Some modules expect data files in subdirectories like `data/raw/`. These are typically gitignored and should be downloaded from the referenced data sources in the notebooks.