# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

### Setup
To set up a development environment, clone the repository and install ParlAI in editable mode:
```bash
git clone https://github.com/facebookresearch/ParlAI.git ~/ParlAI
cd ~/ParlAI; python setup.py develop
```
It is recommended to do this within a virtual environment.

### Formatting and Linting
The project uses `pre-commit` for code formatting and linting. To run it:
```bash
bash autoformat.sh
```

### Testing
The test suite is run using `pytest`.
- To run unit tests:
  ```bash
  python -m pytest -m unit
  ```
- To run data tests (e.g., after adding a new dataset):
  ```bash
  python -m pytest -m data
  ```

### Training and Evaluation
The framework provides scripts for training and evaluating models.
- **Display data:**
  ```bash
  parlai display_data -t <task_name>
  ```
- **Evaluate a model:**
  ```bash
  parlai eval_model -m <model_name> -t <task_name> -dt <datatype>
  ```
- **Train a model:**
  ```bash
  parlai train_model -t <task_name> -m <model_name> [options]
  ```

## High-Level Code Architecture

ParlAI is organized into several main directories:

- **`parlai/core`**: Contains the primary code for the framework, including the main abstractions like `World`, `Agent`, `Teacher`, `Action`, and `Observation`.
- **`parlai/agents`**: Contains agents that can interact with the different tasks (e.g., machine learning models, retrieval models).
- **`parlai/scripts`**: Contains a number of useful scripts for training, evaluating, and interacting with models.
- **`parlai/tasks`**: Contains the code for the hundreds of dialogue and question-answering tasks available within ParlAI. Each task has a "teacher" agent that serves up the data.
- **`parlai/zoo`**: Contains code to directly download and use pretrained models from the ParlAI model zoo.
- **`parlai/crowdsourcing`**: Contains code for running crowdsourcing tasks, such as on Amazon Mechanical Turk.
- **`parlai/chat_service`**: Contains code for interfacing with chat services like Facebook Messenger.
