# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the code repository for the book **Hands-On Data Analysis with Pandas** (1st edition, published by Packt). It teaches data analysis using Python, pandas, matplotlib, seaborn, and scikit-learn through Jupyter notebooks organized into 12 chapters.

## Environment Setup

**Python 3.6 or 3.7 required** (book was written for these versions).

**Using Conda (recommended):**
```bash
conda env create -f environment.yml
conda activate book_env
```

**Using pip:**
```bash
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

**Verify installation:**
```bash
cd ch_01 && python check_environment.py
```

## Running Notebooks

Launch JupyterLab with the environment activated:
```bash
jupyter lab
```

The notebook for checking your setup is at `ch_01/checking_your_setup.ipynb`.

## Dependencies

Core packages used throughout the book:
- pandas (0.23.4)
- numpy (1.16.3)
- matplotlib (3.0.3)
- seaborn (0.9.0)
- scikit-learn (0.20.3)
- scipy (1.2.1)
- statsmodels (0.9.0)
- sqlalchemy (1.3.3)
- pandas-datareader (0.7.0)
- requests (2.21.0)
- imbalanced-learn (0.4.3)
- graphviz (0.10.1)

Custom packages (installed from GitHub):
- `stock-analysis` - for financial analysis (Chapter 7)
- `login-attempt-simulator` - for simulating login data (Chapters 8, 11)
- `ml-utils` - machine learning utilities (Chapters 9-11)

## Repository Structure

- `ch_01` - `ch_12/`: Chapter materials with notebooks and data
  - Each chapter folder contains numbered notebooks (e.g., `1-pandas_data_structures.ipynb`)
  - `data/`: Data files used in that chapter
  - `exercises/`: Exercise notebooks and solution notebooks
- `solutions/`: Complete solutions for chapters 1-11 exercises
- `appendix/`: Workflow diagrams (data analysis, ML, choosing plots)

## Common Tasks

**Run a single notebook:**
```bash
jupyter nbconvert --to notebook --execute my_notebook.ipynb --output executed_notebook.ipynb
```

**Check environment is correctly set up:**
```bash
python ch_01/check_environment.py
```

## Key Concepts Covered

- Data wrangling with pandas (DataFrames, reshaping, cleaning)
- Exploratory data analysis (summary statistics, aggregation)
- Data visualization (pandas, matplotlib, seaborn)
- Working with time series data
- Querying and merging DataFrames
- Financial data analysis (stock market, Bitcoin)
- Rule-based anomaly detection
- Machine learning with scikit-learn (classification, regression, clustering)
- Anomaly detection using ML techniques
- Building reusable Python packages for analysis

## Data Sources Referenced

- `seaborn` and `sklearn` built-in datasets
- Weather API (OpenWeatherMap) - Chapter 3
- Financial data via `pandas-datareader` - Chapter 4, 7
- Simulated login attempt data - Chapter 8, 11