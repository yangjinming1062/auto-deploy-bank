# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

finlab_crypto is a Python library for crypto currency trading strategy backtesting and live trading. It provides:
- Pandas vectorized backtesting using vectorbt as the backend
- TA-Lib wrapper for easily composing strategies
- Backtest visualization and analysis
- Overfitting analysis using Combinatorially Symmetric Cross-Validation (CSCV)
- Live trading integration with Binance

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
coverage run -m unittest discover --pattern *_test.py

# Run tests with Binance API access (for crawler tests)
BINANCE_KEY=<key> BINANCE_SECRET=<secret> coverage run -m unittest discover --pattern *_test.py

# Generate code coverage report
coverage report
```

## Architecture

### Core Modules (finlab_crypto/)

- **__init__.py**: Package entry point. Sets up vectorbt defaults (cash=100$, fees=0.1%, slippage=0.1%). The `setup()` function creates `./history/` directory for caching data.
- **strategy.py**: Contains `Strategy` and `Filter` classes used as decorators. Strategies return `(entries, exits, figures)` tuples. Filters return `(signals, figures)` tuples.
- **crawler.py**: Data fetching from Binance/Bitmex APIs. `get_all_binance()` fetches complete history, `get_nbars_binance()` fetches recent N bars. Data saved to `./history/`.
- **online.py**: Live trading integration with Binance. Key classes:
  - `TradingMethod`: Encapsulates a strategy for live trading
  - `TradingPortfolio`: Manages Binance connection and order execution
- **overfitting.py**: CSCV algorithm for estimating probability of overfitting
- **utility.py**: Backtesting helpers including `enumerate_signal()`, `stop_early()`, and plotting functions
- **chart.py**: Pyecharts-based visualization using vectorbt records
- **indicators.py**: Technical indicator wrappers

### Strategy/Filter Patterns

Strategies use the decorator pattern:
```python
@Strategy(n1=20, n2=60)
def sma_strategy(ohlcv):
    sma1 = ohlcv.close.rolling(sma_strategy.n1).mean()
    sma2 = ohlcv.close.rolling(sma_strategy.n2).mean()
    return (sma1 > sma2), (sma2 > sma1)  # (entries, exits)

# Backtest
portfolio = sma_strategy.backtest(ohlcv, freq='4h', plot=True)
```

Filters layer on top of strategies to add additional entry/exit conditions. They use the same decorator pattern.

### Stop-Loss/Stop-Trailing Variables

Strategy backtest supports special variables:
- `sl_stop`: Stop loss percentage (e.g., 0.1 for 10%)
- `tp_stop`: Take profit percentage
- `ts_stop`: Trailing stop (converted internally to `sl_trail`)
- `sl_trail`: Trailing stop percentage

### Data Format

OHLCV DataFrame has columns: `open`, `high`, `low`, `close`, `volume` with datetime index in UTC.

### Example Strategies and Filters

The `strategies/` and `filters/` directories contain example implementations:
- sma.py, rsi.py, macd.py, bb.py, breakout.py, trend.py, diff.py (strategies)
- sma.py, rsi.py, macd.py, stoch.py, mmi.py (filters)