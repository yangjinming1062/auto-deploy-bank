# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ModSimPy is the supporting code library for the book "Modeling and Simulation in Python" by Allen Downey. It provides tools for physical modeling and simulation including discrete models, first-order systems (disease spread, thermal systems, pharmacokinetics), and second-order systems (mechanics, celestial mechanics, rigid bodies).

## Common Commands

```bash
# Install development dependencies
make requirements

# Run tests (executes pytest with nbmake on chapter notebooks)
make tests

# Check code formatting
make lint

# Format code with black
make format

# Clean compiled Python files
make clean
```

## Architecture

- **modsim/modsim.py**: Core library (~900 lines) containing simulation functions and utilities. Imports from standard scientific Python stack (numpy, scipy, matplotlib, pandas, sympy, pint).

- **modsim/__init__.py**: Package initialization that imports everything from modsim.py for `from modsim import *` syntax.

- **chapters/chap*.ipynb**: Jupyter notebooks for each of the 27 chapters containing examples and exercises.

- **chapters/chap*.py**: Standalone Python companion files for some chapters (e.g., chap03.py, chap06.py, etc.).

- **examples/*.ipynb**: Additional example notebooks (bungee, HIV model, glucose, orbit, queue, etc.).

- **data/**: CSV and HTML data files used throughout examples (population estimates, baseball drag, glucose-insulin data, etc.).

## Dependencies

Core dependencies are specified in requirements.txt (numpy, matplotlib, pandas, scipy, sympy, pint, jupyter, beautifulsoup4, html5lib, lxml, pytables). Development dependencies are in requirements-dev.txt (pytest, nbmake, pandoc, pypandoc).