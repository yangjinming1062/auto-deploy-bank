# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project, Chuanhu ChatGPT, is a web-based graphical user interface for the ChatGPT API. It is built using Python and the Gradio library.

Key features include:
*   Real-time conversation.
*   Saving conversation history.
*   Preset prompt sets.
*   Web search integration.
*   Ability to answer questions based on files.
*   Rendering of LaTeX, tables, and code with syntax highlighting.

## Code Architecture

*   **Main Application:** `ChuanhuChatbot.py` is the entry point of the application. It initializes the Gradio interface and handles the main logic.
*   **Configuration:** The application is configured through a `config.json` file. An example is provided in `config_example.json`. This file is used for API keys, user authentication, and other settings.
*   **Modules (`/modules`):**
    *   `chat_func.py`: Core chat functionalities.
    *   `config.py`: Handles loading and managing configurations from `config.json`.
    *   `openai_func.py`: Manages interactions with the OpenAI API.
    *   `llama_func.py`: Contains functions related to Llama models.
    *   `pdf_func.py`: Provides PDF processing capabilities.
    *   `presets.py`: Manages prompt presets.
    *   `shared.py`: Contains shared state or utility functions used across modules.
    *   `utils.py`: A collection of general utility functions.
*   **Frontend Assets (`/assets`):** Contains custom CSS and JavaScript for the web interface.
*   **Templates (`/templates`):** Stores prompt templates in JSON and CSV formats.

## Common Commands

### Local Development

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the application:**
    ```bash
    python ChuanhuChatbot.py
    ```
    The application will be available at `http://localhost:7860`.

### Docker

*   **Build the Docker image:**
    ```bash
    docker build -t chuanhuchatgpt:latest .
    ```

*   **Run the Docker container:**
    ```bash
    docker run -d --name chatgpt \
        -e my_api_key="YOUR_API_KEY" \
        -e USERNAME="your_username" \
        -e PASSWORD="your_password" \
        -v ~/chatGPThistory:/app/history \
        -p 7860:7860 \
        tuchuanhuhuhu/chuanhuchatgpt:latest
    ```

### Running Tests

There are no dedicated test commands mentioned in the documentation.
