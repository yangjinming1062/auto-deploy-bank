# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NBA Game Predictor - An end-to-end ML project predicting NBA game winners using gradient boosting models (XGBoost, LightGBM). Deployed as a Streamlit web app.

**Note:** Hopsworks feature store integration is suspended (Oct 2024) due to stability issues. Data and models now use local file storage.

## Common Commands

### Installation
```bash
pip install -r requirements.txt.main
```
Python 3.9.13 recommended. Use `requirements.txt` (minimal) only for Streamlit Cloud.

### Running the App
```bash
streamlit run src/streamlit_app.py
```

### Running Production Notebooks
```bash
# Daily feature pipeline (scrape new games, update rolling stats):
jupyter nbconvert --to notebook --execute notebooks/09_production_features_pipeline.ipynb

# Full model training pipeline:
jupyter nbconvert --to notebook --execute notebooks/10_model_training_pipeline.ipynb

# Model testing with Optuna hyperparameter tuning:
jupyter nbconvert --to notebook --execute notebooks/07_optuna_objectives.ipynb
```

### Automation
Daily production pipeline runs automatically at 8am via `.github/workflows/production-features-pipeline.yml`.

## Architecture

### Data Files
- `data/games.csv` - Raw historical NBA game data
- `data/games_engineered.csv` - Features after processing
- `data/games_dashboard.csv` - Dashboard metrics for display
- `models/model.pkl` - Trained sklearn CalibratedClassifierCV model

### Feature Engineering (`src/feature_engineering.py`)

The `process_features()` function applies transformations in order:
1. **fix_datatypes()** - Memory optimization, date conversion
2. **add_date_features()** - Extracts month from game date
3. **remove_playoff_games()** - Filters to regular season only
4. **add_rolling_home_visitor()** - Rolling stats for home/away performance (3, 7, 10 game windows)
5. **process_games_consecutively()** - Splits games into team-centric records
6. **add_matchups()** - Head-to-head rolling win percentages
7. **add_past_performance_all()** - Rolling stats regardless of home/away (3, 7, 10, 15 game windows)
8. **process_x_minus_league_avg()** - Subtracts league average from team rolling stats
9. **process_x_minus_y()** - Home team stats minus visitor team stats

**Critical:** `remove_non_rolling()` filters out non-rolling features to prevent data leakage (stats from the actual game not known before it starts).

### Model Training (`src/optuna_objectives.py`)
- **Optuna** for hyperparameter optimization
- **XGBoost objective**: Tunes `max_depth`, `learning_rate`, `alpha`, `gamma`, etc.
- **LightGBM objective**: Tunes `num_leaves`, `lambda_l1/l2`, `feature_fraction`, etc.
- **CalibratedClassifierCV** ensures probability calibration (Brier score optimization)
- Primary metric: ROC-AUC during training; secondary: Accuracy, Brier Score

### Web Scraping (`src/webscraping.py`)
Two modes available:
- **ScrapingAnt** (cloud API, used in production) - Handles proxy servers
- **Selenium** (local browser) - For local development

Functions:
- `get_new_games()` - Scrapes completed games from nba.com/stats/teams/boxscores
- `get_todays_matchups()` - Scrapes upcoming games from nba.com/schedule

### Key Constants (`src/constants.py`)
- `SHORT_INTEGER_FIELDS`: PTS, AST, REB (home/away) - stored as int16
- `HOME_VISITOR_ROLL_LIST = [3, 7, 10]` - Rolling window sizes for home/away stats
- `ALL_ROLL_LIST = [3, 7, 10, 15]` - Rolling window sizes for all games
- `NBA_TEAMS_NAMES` - Team ID to full name mapping

## Key Source Files

| File | Purpose |
|------|---------|
| `src/streamlit_app.py` | Main web application |
| `src/feature_engineering.py` | Core feature transformations |
| `src/optuna_objectives.py` | Optuna hyperparameter tuning |
| `src/model_training.py` | Model evaluation and calibration |
| `src/webscraping.py` | NBA.com data scraping |
| `src/data_processing.py` | Raw data cleaning |
| `src/constants.py` | Centralized configuration |

## Development Notes

- **Import patterns**: Code uses try/except for imports to support both repo root (`from src.module import X`) and `src/` directory execution (`from module import X`)
- **Model serialization**: Uses joblib for model persistence in `models/model.pkl`
- **Model accuracy**: ~61.5% on 2022-23 season (baseline "home team always wins" = 57%)
- **Feature count**: Hundreds of features computed; only rolling averages and streaks used at prediction time