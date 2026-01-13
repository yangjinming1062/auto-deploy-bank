# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

- **Run tests:**
  - `pytest greykite/tests` (run tests with default Python)
  - `tox` (run tests on every Python version)
- **Check code style:** `flake8 greykite --exclude=tests --ignore W503,W504,F541,E226,E126,E402,E123,E121,E741`
- **Check code coverage:** `coverage run --source greykite -m pytest greykite/tests`
- **Generate documentation:** `make docs`
- **Install dependencies:** `pip install -r requirements-dev.txt`
- **Install the package:** `python setup.py install`

## High-level code architecture

The `greykite` library is a forecasting and anomaly detection library. The flagship algorithm is called **Silverkite**.

The main components of the library are:

- **`greykite/algo`**: Contains the core forecasting and anomaly detection algorithms, including Silverkite.
- **`greykite/common`**: Contains common utilities and data loaders.
- **`greykite/framework`**: Provides a framework for building and evaluating forecasting models.
- **`greykite/sklearn`**: Contains scikit-learn compatible components.
- **`greykite/detection`**: Contains algorithms and utilities for anomaly detection.

The library is designed to be flexible and extensible. It allows users to define their own regressors and use a variety of machine learning models for forecasting. The `README.rst` file provides a good overview of the library's features and usage.
