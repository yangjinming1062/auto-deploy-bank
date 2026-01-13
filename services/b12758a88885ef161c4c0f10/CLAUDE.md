# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

To develop in this codebase, you will need to install the dependencies and run the application.

**Installation:**

1.  Create a new conda environment:
    ```bash
    conda create -n open_manus python=3.12
    conda activate open_manus
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

**Configuration:**

1.  Create a `config.toml` file in the `config` directory:
    ```bash
    cp config/config.example.toml config/config.toml
    ```
2.  Edit `config/config.toml` to add your API keys.

**Running the application:**

*   To run the stable version:
    ```bash
    python main.py
    ```
*   To run the unstable version:
    ```bash
    python run_flow.py
    ```

## Code Architecture

The project is structured as a Python application with the following key directories and files:

*   `main.py`: The main entry point for the application.
*   `run_flow.py`: The entry point for the unstable version of the application.
*   `app/`: Contains the core application logic.
    *   `agent/`: Defines the agent's behavior and decision-making.
    *   `flow/`: Contains the logic for the unstable version of the application.
    *   `llm.py`: Handles interactions with the language model.
    *   `prompt/`: Stores the prompts used to instruct the language model.
    *   `tool/`: Defines the tools that the agent can use.
*   `config/`: Contains configuration files for the application, including API keys.
*   `requirements.txt`: Lists the Python dependencies for the project.
