# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

IntroNeuralNetworks is an educational stock price prediction project using neural networks. It demonstrates the complete ML workflow: data acquisition, preprocessing, model training, backtesting, and prediction. This is for learning purposes only—**do not use for live trading**.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run LSTM model (main entry point)
python LSTM_model.py

# Run MLP model
python MLP_model.py

# Download stock price data independently
python get_prices.py

# Backtesting requires calling back_test() directly in Python scripts
```

## Architecture

The pipeline follows this sequence:

1. **Data Acquisition** (`get_prices.py`): Fetches historical stock data from Yahoo Finance via `pandas_datareader` with `fix_yahoo_finance` patch. Outputs `stock_prices.csv`.

2. **Preprocessing** (`preprocessing.py`): The `DataProcessing` class splits data into train/test sets (90/10 split by default) and generates sliding window sequences:
   - `gen_train(seq_len)`: Creates training sequences
   - `gen_test(seq_len)`: Creates test sequences
   - Data is normalized by dividing by 200

3. **Model Training**:
   - `LSTM_model.py`: LSTM neural network (10→20→20→1 units) for sequential pattern recognition
   - `MLP_model.py`: Multilayer Perceptron (100→100→1 dense layers) for baseline comparison

4. **Backtesting** (`backtest.py`): `back_test(strategy, seq_len, ticker, start_date, end_date, dim)` evaluates model predictions against actual prices, reporting average percentage error.

5. **Prediction**: After training, `model.predict()` generates future price estimates.

## Key Patterns

- **Sequence length**: Default `seq_len=10` (10 days of prices to predict the next day)
- **Normalization**: All input/output divided by 200; predictions must be multiplied by 200
- **3D vs 2D input**: LSTM requires `(samples, timesteps, features)` reshape; MLP uses `(samples, features)`
- **Data column**: Only `Adj Close` (column index 1) is used for predictions