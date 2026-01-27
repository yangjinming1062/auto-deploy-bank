# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Warren is a Flask web application that predicts stock prices using Facebook's Prophet time series forecasting algorithm. Users enter a stock ticker and receive a next-day price prediction with confidence intervals.

## Commands

**Install dependencies:**
```bash
pip install -r REQUIREMENTS.txt
```

**Run the server:**
```bash
python runserver.py
```

The server runs on `localhost:5555` by default (configurable via `SERVER_HOST` and `SERVER_PORT` environment variables).

## Architecture

**Entry Point:** `runserver.py` - Initializes the Flask app and starts the development server.

**Flask Application:** `src/__init__.py` creates the app instance, then imports `src.views` to register routes.

**Route Handlers:** `src/views.py` defines two endpoints:
- `/` and `/home` - Renders the home page with the stock ticker input form
- `/predict` (POST/GET) - Accepts a ticker symbol, runs the Prophet model, and renders the prediction results

**Core Logic:** `src/utilities.py` implements a class hierarchy for stock prediction:
- `Dataset` - Fetches historical stock data via yfinance (2010-present), cleans it, and adds forecast date
- `FeatureEngineering` (extends Dataset) - Creates lag features (12 periods), imputes missing values, drops unused columns
- `MasterProphet` (extends FeatureEngineering) - Builds Prophet model with regressors, trains on historical data, generates forecasts

**Templates:** `src/templates/` contains Jinja2 HTML templates:
- `index.html` - Home page with ticker input form
- `output.html` - Displays prediction results with confidence intervals

**Static Assets:** `src/static/` holds CSS, fonts, and images.

**Notebooks:** `src/notebooks/` contains exploratory Jupyter notebooks for the Prophet modeling experiments.

## Key Implementation Details

- Stock data is fetched using `yfinance.Ticker` with daily interval from 2010-01-01 to present
- Prophet model uses additive seasonality (yearly + weekly) and includes 12 lag feature regressors
- Forecast date calculation skips weekends (predicts next trading day)
- The last row in the dataset is a placeholder for the next day's prediction