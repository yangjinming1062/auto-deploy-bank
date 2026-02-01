# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit-based web application for calculating European option prices using three financial models: Black-Scholes, Monte Carlo Simulation, and Binomial Tree Model.

## Commands

### Run the Application
```bash
streamlit run streamlit_app.py
```

### Run with Docker
```bash
docker build -t options-pricing:latest .
docker run -p 8080:8080 options-pricing:latest
```

### Run Tests
```bash
python option_pricing_test.py
```

## Architecture

### Package Structure (`option_pricing/`)

- **`base.py`**: Abstract base class `OptionPricingModel` defining the interface. All pricing models inherit from this class and implement `_calculate_call_option_price()` and `_calculate_put_option_price()` abstract methods.

- **`BlackScholesModel.py`**: Black-Scholes analytical solution using normal distribution (scipy.stats.norm). Accepts spot price, strike price, time to maturity, risk-free rate, and volatility.

- **`MonteCarloSimulation.py`**: Monte Carlo pricing using Brownian motion simulation. Key methods:
  - `simulate_prices()`: Generates price paths using geometric Brownian motion
  - `_calculate_call_option_price()` / `_calculate_put_option_price()`: Computes option prices from simulated terminal prices

- **`BinomialTreeModel.py`**: Binomial lattice pricing with configurable time steps. Uses risk-neutral probabilities and backward induction.

- **`ticker.py`**: `Ticker` utility class for fetching and plotting historical stock data from Yahoo Finance (yfinance). Uses `@st.cache_data` for caching in the Streamlit app.

### Main Application (`streamlit_app.py`)

Streamlit sidebar UI with three tabs corresponding to each pricing model. Uses `@st.cache_data` decorated functions for data fetching. Parameters (strike, risk-free rate, sigma, exercise date) flow from UI to model constructors.

### Data Flow

1. User enters ticker symbol → `get_current_price()` fetches live price
2. User configures parameters in sidebar
3. On button click → `get_historical_data()` fetches historical data (cached)
4. Model instantiated with parameters → calculates call/put prices
5. Results and plots displayed to user