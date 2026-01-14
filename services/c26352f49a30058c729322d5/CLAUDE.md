# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a recommender systems evaluation framework for deep learning and baseline algorithms. It implements and evaluates various recommendation approaches including KNN, matrix factorization, graph-based methods, and neural network models published in top conferences (RecSys, KDD, WWW, SIGIR, IJCAI).

## Commands

**Setup and Installation:**
```bash
# Create virtual environment
virtualenv -p python3 DLevaluation
source DLevaluation/bin/activate

# Install CPU dependencies
pip install -r requirements.txt

# Install GPU dependencies (requires conda)
conda install tensorflow-gpu keras-gpu
pip install -r requirements_gpu.txt

# Compile Cython modules (required after installation)
python run_compile_all_cython.py
```

**Running Experiments:**
```bash
# Example usage (simple recommender usage example)
python run_example_usage.py

# Run experiments for a DL algorithm (e.g., SpectralCF)
# -b: Run baseline hyperparameter tuning
# -a: Train deep learning model with article hyperparameters
# -p: Generate LaTeX result tables
python run_RecSys_18_SpectralCF.py -b True -a True -p True

# CNN embedding experiments
python run_IJCAI_18_ConvNCF_CNN_embeddings.py
```

## Architecture

### Data Layer (`Data_manager/`)
- **DataReader**: Base class for loading datasets. Each dataset (Movielens, Amazon, etc.) has its own reader
- **DataSplitter**: Creates train/validation/test splits (leave-k-out, k-fold)
- **Dataset**: Wraps loaded data, exposes `get_URM_all()`, `get_ICM_from_name()`, etc.
- Data is cached in `Data_manager_split_datasets/` after first load

### Core Framework (`Base/`)
- **BaseRecommender**: Abstract base class for all recommenders
  - Constructor takes `URM_train` (CSR sparse matrix, shape: [n_users, n_items])
  - Optional ICM/UCM for content-based recommenders
  - Key methods: `fit()`, `_compute_item_score(user_id_array)`, `recommend()`, `save_model()`, `load_model()`
- **Evaluation/**: `EvaluatorHoldout` computes metrics (PRECISION, RECALL, MAP, NDCG, MRR, HIT_RATE, diversity, coverage, novelty)
- **Similarity/**: Optimized similarity computation (Cython) for KNN recommenders

### Recommender Categories
| Folder | Algorithms |
|--------|------------|
| `KNN/` | UserKNN, ItemKNN (CF, CBF, hybrid CFCBF) with multiple similarity metrics |
| `GraphBased/` | P3alpha, RP3beta (collaborative graph-based) |
| `MatrixFactorization/` | PureSVD, NMF, IALS, FunkSVD, BPR-MF, AsySVD |
| `SLIM_BPR/`, `SLIM_ElasticNet/` | SLIM with BPR or MSE loss |
| `EASE_R/` | Shallow autoencoder |
| `Conferences/` | Deep learning models from papers (SpectralCF, MultiVAE, NeuMF, etc.) |

### Hyperparameter Tuning (`ParameterTuning/`)
- **SearchBayesianSkopt**: Bayesian optimization using scikit-optimize
- **run_parameter_search.py**: Standard hyperparameter search space for baselines

### Key Data Structures
```python
# User Rating Matrix (URM) - sparse CSR matrix
URM_train.shape  # (n_users, n_items)
URM_train.data   # interaction values

# Item Content Matrix (ICM) - sparse matrix
ICM.shape  # (n_items, n_features)

# User Content Matrix (UCM) - sparse matrix
UCM.shape  # (n_users, n_features)
```

### Results
- Output folder: `result_experiments/{Conference}/{Algorithm}/{Dataset}/`
- Includes: trained models, hyperparameters, LaTeX tables, popularity plots
- Use `ResultFolderLoader` to load and compare results

## Deep Learning Algorithm Structure (Conferences/)

Each DL algorithm has two folders:
- `{Algorithm}_github/`: Original source code (or author-provided)
- `{Algorithm}_our_interface/`: Python wrapper implementing the common recommender interface with `RecommenderWrapper` class