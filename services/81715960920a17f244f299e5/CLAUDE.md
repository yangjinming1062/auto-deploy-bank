# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of 150+ Python scripts for financial/stock market analysis, providing tools for data collection, technical analysis, machine learning predictions, and portfolio strategy testing. Each script is standalone and can be executed independently.

## Repository Structure

The codebase is organized into 6 main modules:

- **find_stocks** (12 scripts): Stock screening based on technical/fundamental analysis (IBD RS Rating, RSI, FinViz data, sentiment analysis)
- **machine_learning** (16 scripts): ML models for stock prediction and classification (LSTM, ARIMA, Prophet, neural networks, clustering)
- **portfolio_strategies** (25 scripts): Trading strategies, backtesting, and portfolio optimization (backtrader, Monte Carlo, risk management)
- **stock_analysis** (20 scripts): Individual stock assessment tools (CAPM, valuation, sentiment analysis, seasonal patterns)
- **stock_data** (22 scripts): Data collection via APIs and web scraping (yfinance, FinViz, Reddit, Twilio alerts)
- **technical_indicators** (80+ scripts): Visual implementations of technical indicators (RSI, MACD, Bollinger Bands, EMA, etc.)

Core shared modules:
- **ta_functions.py**: Core technical analysis functions (SMA, EMA, RSI, MACD, Bollinger Bands, etc.)
- **tickers.py**: Functions to fetch tickers from S&P 500, NASDAQ, NYSE, Dow Jones, AMEX
- **CSV files**: Pre-downloaded ticker lists for major exchanges

## Installation & Setup

```bash
# Install dependencies
pip install -r requirements.txt

# The project uses yfinance with pandas_datareader override
# Some scripts require chromedriver for selenium (already included)
```

## Common Operations

All scripts are standalone. Run any script directly:

```bash
# Run a single script
python script_name.py

# Example scripts
python stock_data/yf_intraday_data.py
python machine_learning/lstm_prediction.py
python find_stocks/finviz_growth_screener.py
python portfolio_strategies/backtrader_backtest.py
```

## Key Dependencies

- **Data Collection**: yfinance, pandas_datareader, requests, beautifulsoup4, selenium
- **Analysis**: pandas, numpy, ta (technical analysis library)
- **Visualization**: matplotlib, mplfinance, seaborn
- **Machine Learning**: scikit-learn, tensorflow, keras, statsmodels, prophet
- **Backtesting**: backtrader, pyfolio
- **Communication**: twilio (SMS), schedule, Flask

## Architecture Notes

- Scripts typically follow pattern: import dependencies → define functions → main execution block with `if __name__ == "__main__"`
- Data is primarily fetched via yfinance API, FinViz web scraping, or Wikipedia/NASDAQ sources
- Technical indicators use pandas rolling operations for time series calculations
- Web scraping scripts use BeautifulSoup and selenium with chromedriver
- No test suite exists; validation requires running scripts manually
- Some scripts require API keys for external services (Twilio, Twitter, etc.)

## Development Guidance

- When modifying scripts, maintain the standalone execution pattern
- Many technical indicators are duplicated across modules; consider centralizing in ta_functions.py
- Selenium scripts depend on the included chromedriver binary
- Be cautious with rate limiting when web scraping FinViz and other financial sites
- Stock data can be voluminous; scripts may create large CSV files
- Educational/disclaimer context: This is for learning purposes only, not professional investment advice

## File Locations

- Entry points: All Python files in subdirectories are executable
- Shared utilities: ta_functions.py, tickers.py
- Ticker data: *.csv files (S&P 500, NASDAQ, NYSE, Russell 3000, AMEX)
- Dependencies: requirements.txt