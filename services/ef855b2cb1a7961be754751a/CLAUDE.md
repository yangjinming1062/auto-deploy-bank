# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

- **Linting**: `make lint`
- **Testing**: `make test` or `poetry run pytest -n auto`
- **Generating Documentation**: `make doc-gen`

## High-Level Code Architecture

The project is a Python application called "Podcastfy" that transforms multi-modal content (text, images, URLs) into audio conversations.

- **`podcastfy/client.py`**: The main entry point for the CLI and the `generate_podcast` function. It orchestrates the entire process.
- **`podcastfy/content_generator.py`**: This module is responsible for generating the conversational content using LLMs. It uses LangChain to interact with different models.
- **`podcastfy/content_parser/`**: This directory contains modules for extracting content from different sources like PDFs, websites, and YouTube videos.
- **`podcastfy/text_to_speech.py`**: This module handles the text-to-speech conversion using various providers like ElevenLabs, OpenAI, Google, and Edge.
- **`podcastfy/tts/`**: This directory contains the specific implementations for each TTS provider.
- **`podcastfy/utils/`**: This directory contains utility modules for configuration, logging, etc.
- **`tests/`**: This directory contains the tests for the application. The tests are written using `pytest` and demonstrate how to use the different components of the application.
- **`pyproject.toml`**: This file defines the project's dependencies and metadata.
- **`Makefile`**: This file contains the commands for linting, testing, and generating documentation.
