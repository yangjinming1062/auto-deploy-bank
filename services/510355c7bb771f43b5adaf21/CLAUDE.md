# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

*   **Install dependencies:** `pip install --upgrade -r requirements.txt`
*   **Install in development mode:** `pip install -e .`
*   **Run all tests:** `tests/testall.sh`
*   **Launch the Web UI:** `python examples/web/webui.py`
*   **Run from the command line:** `python examples/cmd/run.py "Your text 1." "Your text 2."`

## High-level code architecture

ChatTTS is a generative speech model for daily dialogue.

*   The main model is trained with Chinese and English audio data of 100,000+ hours.
*   The open-source version on HuggingFace is a 40,000 hours pre-trained model without SFT.

### Directory Structure

*   `ChatTTS/`: The core Python package.
*   `docs/`: Contains documentation in different languages.
*   `examples/`: Contains examples of how to use the model.
*   `tests/`: Contains tests for the model.
*   `tools/`: Contains utility scripts.
