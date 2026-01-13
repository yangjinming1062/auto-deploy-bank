# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WebSSH is a web application that acts as an SSH client. It's built with Python, using the tornado framework for the web server, paramiko for the SSH connection, and xterm.js for the frontend terminal emulation.

## Common Commands

### Installation

To install the required dependencies, run:
```bash
pip install -r requirements.txt
pip install pytest pytest-cov codecov flake8 mock
```

### Running the application

To start the development server, run:
```bash
wssh
```
Then open `http://127.0.0.1:8888` in your browser.

### Running Tests

To run the test suite, you can use either `unittest` or `pytest`:

Using `unittest`:
```bash
python -m unittest discover tests
```

Using `pytest`:
```bash
python -m pytest tests
```

## Architecture

The application is divided into a frontend and a backend.

### Backend

The backend is a Python application built with the Tornado web framework.
-   `webssh/main.py`: The main entry point of the application, responsible for setting up the tornado server.
-   `webssh/handler.py`: Contains the `Tornado` request handlers, including the WebSocket handler for communication with the frontend.
-   `webssh/worker.py`: Manages the SSH connection using `paramiko`.
-   `webssh/settings.py`: Contains application settings.
-   `webssh/policy.py`: Handles SSH host key policies.
-   `run.py`: A wrapper script to run the application.

### Frontend

The frontend is composed of HTML, CSS, and JavaScript files located in the `webssh/static` and `webssh/templates` directories.
-   `webssh/templates/index.html`: The main HTML file.
-   `webssh/static/js/main.js`: Contains the main frontend JavaScript logic.
-   `xterm.js` is used for the terminal emulation in the browser.
