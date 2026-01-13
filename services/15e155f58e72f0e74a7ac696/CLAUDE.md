# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly used commands

- To install dependencies: `pip install -r requirements.txt` (after creating a `requirements.txt` from `setup.py`)
- To run the application: `psdash`
- To run an agent: `psdash -a --register-to [http|https]://[host]:[port] --register-as my-agent-node`
- To run tests: `python setup.py test`

## High-level code architecture

- **psdash**: The core of the application, a system information web dashboard for Linux.
- **Framework**: It's built using Flask, a Python web framework.
- **Data Source**: The application primarily uses the `psutil` library to gather system information.
- **Frontend**: The user interface is based on Bootstrap.
- **Components**:
    - `web.py`: Handles the web interface and routes.
    - `node.py`: Manages agent nodes and communication.
    - `net.py`: Provides network-related information.
    - `log.py`: Manages log file tailing and searching.
    - `helpers.py`: Contains utility functions.
- **Templates**: HTML templates for rendering web pages are located in the `psdash/templates` directory.
- **Static Files**: CSS, JavaScript, and fonts are in the `psdash/static` directory.
- **Multi-node support**: `psdash` supports a multi-node architecture where agents can register to a central server.