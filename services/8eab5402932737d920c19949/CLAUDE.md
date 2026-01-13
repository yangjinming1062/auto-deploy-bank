# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Development Server
To run the development server, use the following command. This will start the server with your local changes.
```bash
python3 -m maloja run
```
You can also run the server in a Docker container using the provided script:
```bash
sh ./dev/run_docker.sh
```

### Building the project
To build the project, use the following command:
```bash
pip install .
```

### Testing
To run the stress test, execute the following script:
```bash
python3 dev/testing/stresstest.py
```

## Code Architecture

Maloja is a self-hosted music scrobble database written in Python.

- **Frontend**: The frontend is built with HTML, CSS, and JavaScript. The templates are in the `maloja/templates` directory.
- **Backend**: The backend is a Python application using the Bottle framework. The main application logic is in the `maloja` directory.
- **Data**: Maloja stores its data in a SQLite database. The database schema is defined in `maloja/db.py`.
- **Dependencies**: The project's dependencies are listed in `pyproject.toml` and installed using `pip`.
- **Configuration**: The main configuration is handled by `maloja/workflow/setup.py` and the user can override the settings using a `settings.ini` file.
