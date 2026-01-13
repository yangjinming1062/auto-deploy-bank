# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

- To run the application: `python web2py.py`
- To run tests: `make tests` which executes `python web2py.py --verbose --run_system_tests`
- To run tests with coverage: `make coverage`

## High-level Code Architecture

This is a web2py application. The main components are:

- `web2py.py`: The main script to run the application.
- `gluon/`: The core web2py framework libraries.
- `applications/`: This directory contains the different applications.
    - `admin/`: The web-based IDE.
    - `examples/`: Example applications.
    - `welcome/`: The scaffolding application.
- `README.markdown`: Contains general information about the project.
- `Makefile`: Contains build and test commands.
