# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository demonstrates **automated feature engineering using Featuretools** compared against manual feature engineering across three machine learning problems. Each problem is in its own directory with a consistent structure.

### Three Projects

1. **Loan Repayment** (`Loan Repayment/`) - Predicts loan default using Home Credit competition data. 58M rows across 7 tables.
2. **Retail Spending** (`Retail Spending/`) - Predicts customer spending from UCI online retail data. Demonstrates time-series validation.
3. **Engine Life** (`Engine Life/`) - Predicts remaining useful life of engines using NASA Turbofan data.

## Architecture

### Directory Structure

Each project follows this pattern:
```
project/
├── notebooks/          # Jupyter notebooks (Manual & Automated comparisons)
├── notebooks/utils.py  # Shared utility functions
├── scripts/            # Python scripts for batch processing
├── input/              # Data files and metadata
└── images/             # Generated visualizations
```

### Key Patterns

**Entity-Relationship Model for Featuretools:**
- Each project defines entities with relationships in metadata.json
- Entities have indexes (unique identifiers) and optionally time indexes
- Relationships link parent entities to child entities (e.g., app → bureau)

**Feature Engineering Workflow:**
1. Load raw CSV/data files into pandas DataFrames
2. Create Featuretools EntitySet with entities and relationships
3. Run Deep Feature Synthesis (DFS) to generate features
4. Apply feature selection (remove missing, collinear, zero-variance)
5. Train model (LightGBM for classification, RandomForest for regression)
6. Evaluate with cross-validation and feature importance analysis

**Shared Utilities (`utils.py`):**
- `format_data()` / `evaluate()` - Prepare data and run model evaluation
- `plot_feature_importances()` - Visualize top N features with cumulative importance
- `feature_selection()` - Remove high-missing, collinear, and zero-variance features

**Memory Optimization:**
- `convert_types()` in `ft.py` reduces memory by converting int64→int32, float64→float32, objects→category

## Dependencies

Install with: `pip install -r requirements.txt`

Key libraries:
- **featuretools** - Automated feature engineering
- **lightgbm** - Gradient boosting (Loan Repayment)
- **scikit-learn** - RandomForest, cross-validation (Retail, Engine)
- **pandas, numpy** - Data manipulation
- **matplotlib, seaborn** - Visualization

## Running Notebooks

Start Jupyter in any project directory:
```bash
cd "Loan Repayment/notebooks" && jupyter notebook
```

**Execution time:**
- Loan Repayment ft.py script: ~24 hours
- Featuretools on Dask notebooks: a few hours

## Data Sources

- **Loan Repayment**: Kaggle Home Credit Default Risk competition
- **Retail Spending**: UCI Machine Learning Repository (or S3: s3://featurelabs-static/online-retail-logs.csv)
- **Engine Life**: NASA Turbofan Engine Degradation Simulation Dataset

## Code Conventions

- `RSEED = 50` - Global random seed for reproducibility
- LightGBM models use 5-fold CV with early stopping (100 rounds)
- Feature importances normalized to sum to 1
- Column naming: `SK_ID_*` for identifiers, `AMT_*` for amounts, `DAYS_*` for durations