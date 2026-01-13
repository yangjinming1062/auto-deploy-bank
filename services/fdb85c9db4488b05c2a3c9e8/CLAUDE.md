# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

### Building the application
To build the web assets, run:
```bash
make install-node
make bundle
```

### Running the application
To run the application in server mode:
```bash
python3 web/pgAdmin4.py
```
Before running for the first time, you may need to set up the configuration database:
```bash
python3 web/setup.py
```

### Running tests
To run all tests:
```bash
make check
```
To run only the Python tests:
```bash
make check-python
```
To run only the Javascript tests:
```bash
make check-js
```
To run the feature tests:
```bash
make check-feature
```

### Linting
To run the linter:
```bash
make linter
```

## Architecture

pgAdmin 4 is a web application with a Python (Flask) backend and a ReactJS frontend. It can be deployed on a web server or as a standalone desktop application using Electron.

- The Python server-side code is located in the `web/` directory.
- The ReactJS client-side code is also in the `web/` directory.
- The Electron runtime is in the `runtime/` directory.
- The application's configuration can be customized by creating a `config_local.py` file in the `web/` directory.
- The `Makefile` at the root of the repository contains many useful targets for building, testing, and packaging the application.
