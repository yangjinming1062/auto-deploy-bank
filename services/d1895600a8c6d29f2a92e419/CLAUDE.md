# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
# OctoBot - Cryptocurrency Trading Bot

OctoBot is a modular, open-source cryptocurrency trading bot with a plugin-based architecture called "tentacles". The core engine coordinates between evaluators, traders, and various interfaces.

## Architecture Overview

The project follows a modular, channel-based architecture:

- **Core Engine** (`octobot/octobot.py`): Main orchestrator that initializes and coordinates all components
- **Tentacles System**: Plugin architecture for strategies, evaluators, and trading modes (managed via `octobot_tentacles_manager`)
- **Channel Communication**: Async-Channel based message passing between producers and consumers
- **Producers** (`octobot/producers/`): Generate market data, evaluations, and trading signals
  - `evaluator_producer.py`: Runs evaluators and generates signals
  - `exchange_producer.py`: Handles exchange market data
  - `interface_producer.py`: Manages user interfaces
  - `service_feed_producer.py`: Processes external service feeds
- **Backtesting** (`octobot/backtesting/`): Historical data simulation engine
- **Strategy Optimizer** (`octobot/strategy_optimizer/`): Automated strategy testing and optimization
- **API Layer** (`octobot/api/`): Public-facing API for external integration

Key dependencies (from `requirements.txt`):
- `OctoBot-Commons`, `OctoBot-Trading`, `OctoBot-Evaluators`: Core OctoBot packages
- `Async-Channel`: Message passing infrastructure
- `ccxt`: Exchange connectivity
- Cython extensions for performance-critical paths

## Common Development Commands

### Installation & Setup
```bash
# Install dependencies
pip install -r requirements.txt
pip install -r dev_requirements.txt

# Build Cython extensions (required for full performance)
make build
# or
python setup.py build_ext --inplace
```

### Running OctoBot
```bash
# Start OctoBot
python start.py

# Start in simulation mode (paper trading)
python start.py -s

# Start backtesting mode
python start.py -b

# Run backtesting with specific data files
python start.py -b -bf /path/to/data1.json /path/to/data2.json

# Start strategy optimizer (long-running process)
python start.py -o TechnicalAnalysisStrategyEvaluator

# Start without web interface
python start.py -nw

# Start without Telegram interface
python start.py -nt

# Run with specific risk level (0-1)
python start.py -r 0.5
```

### Testing
```bash
# Run all tests
pytest tests

# Run with coverage
pytest --cov=. --cov-config=.coveragerc --durations=0 -rw tests

# Run tests and ignore tentacles
pytest --durations=0 -rw --ignore=tentacles/Trading/Exchange tentacles

# Run specific test file
pytest tests/unit_tests/test_configuration_manager.py

# Run specific test
pytest tests/unit_tests/test_configuration_manager.py::test_function_name
```

### Linting & Code Quality
```bash
# Run pylint with project configuration
pylint --rcfile=standard.rc octobot

# Clean build artifacts
make clean
```

### Tentacles Management
```bash
# Install tentacles
python start.py tentacles --install --all

# Update tentacles
python start.py tentacles --update

# List tentacles
python start.py tentacles --list
```

### Build & Distribution
```bash
# Build wheel
python setup.py bdist_wheel

# Build source distribution
python setup.py sdist

# Debug build
make debug
```

## Code Standards & Contribution Guidelines

### PR Requirements
- Create PRs against the `develop` branch (not `master`)
- All new features require unit tests
- Code must be PEP8 conformant (max line length = 100)
- Pylint score should meet `fail-under=10.0` threshold

### OctoBot Coding Style
- Use list comprehensions when they improve clarity
- Prefer `try ... except` over `if` when condition is 99% True
- Use local variables only when they improve code clarity

### Key Files
- `standard.rc`: Pylint configuration
- `setup.py`: Python package setup, Cython extensions
- `setup.cfg`: Pytest configuration
- `.coveragerc`: Coverage reporting configuration
- `start.py`: CLI entry point
- `octobot/constants.py`: Version and configuration constants
- `octobot/cli.py`: Command-line argument parsing

### Version Management
See `DELIVERY.md` for versioning structure:
- Version format: `R.D.MA_MI` (Release.DevelopmentStage.Major.Minor)
- Development stages: 0=alpha, 1=beta, 2=release candidate, 3=final
- Update version in `octobot/constants.py` and `README.md` before tagging