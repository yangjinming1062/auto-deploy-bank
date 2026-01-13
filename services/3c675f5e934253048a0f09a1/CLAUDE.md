# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

To get started with this project, you'll need to follow these steps:

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up environment variables:**
    Export your OpenAI and Tavily API keys:
    ```bash
    export OPENAI_API_KEY={Your OpenAI API Key here}
    export TAVILY_API_KEY={Your Tavily API Key here}
    ```

3.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    You can then access the web interface at `http://localhost:8000`.

## High-Level Architecture

This project is an autonomous agent designed for comprehensive online research. It follows a "planner" and "execution" agent architecture:

*   **Planner Agent:** Generates a set of research questions based on the user's query.
*   **Execution Agents:** For each research question, these agents crawl online resources to find relevant information.

The agents leverage both `gpt-3.5-turbo` and `gpt-4-turbo` to accomplish research tasks. The system is optimized for cost and speed, with an average research task taking approximately 3 minutes to complete. The architecture is designed to be stable and reliable through parallelized agent work.

The core components of the project are:

*   `main.py`: The main entry point for the FastAPI application.
*   `gpt_researcher/`: This directory contains the core logic for the research agents, including the planner and execution agents.
*   `frontend/`: The web interface for the application (HTML/CSS/JS).
*   `config.json`: The configuration file for the application, where you can customize the LLM and search engine providers.
