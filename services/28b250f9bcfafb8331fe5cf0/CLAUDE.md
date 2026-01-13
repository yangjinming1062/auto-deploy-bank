# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

- **Run tests:** `py.test -v`
- **Run tests with coverage:** `py.test --cov-report term-missing --cov=gns3server`
- **Install dependencies:** `pip install -r requirements.txt` and `pip install -r dev-requirements.txt`
- **Run the server in development mode:** `bash scripts/docker_dev_server.sh`
- **Install the server from source:** `sudo python3 setup.py install`

## Architecture

The GNS3 server is a Python application that manages emulators and network topologies. It exposes a REST API for clients like the GNS3 GUI and the GNS3 Web UI.

- **`gns3server/`**: The main server application.
  - **`controller/`**: Core logic for managing projects, nodes, links, and emulators.
  - **`compute/`**: Manages compute resources (local or remote).
  - **`web/`**: The web server and REST API implementation (using aiohttp).
  - **`schemas/`**: Defines the data schemas for the REST API.
  - **`main.py`**: The main entry point for the server application.
- **`tests/`**: Contains the test suite for the server.
- **`scripts/`**: Utility scripts, including the development server script.
- **`init/`**: Init scripts for running the server as a daemon.

## Development

- The server is built using Python 3 and `asyncio`.
- The web server is implemented using `aiohttp`.
- The REST API is the primary way to interact with the server.
- Before committing any changes, please make sure all tests pass.