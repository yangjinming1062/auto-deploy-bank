# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a **security research repository** demonstrating indirect prompt injection vulnerabilities in Large Language Models (LLMs). The codebase contains proof-of-concept attacks and demonstrations for academic research purposes, published alongside a research paper on ArXiv.

**⚠️ Important Context**: This repository contains demonstrations of prompt injection attacks. It is intended for security research, education, and understanding these vulnerabilities to develop defenses. The code demonstrates attack vectors but is not designed to cause harm—it's a controlled research environment.

## Project Type

- **Language**: Python 3
- **Dependencies**: OpenAI API, LangChain, Rich (for console output)
- **Architecture**: Modular scenario-based testing framework

## Common Development Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key (required)
export OPENAI_API_KEY="your-api-key-here"
```

### Running Scenarios

**Interactive mode with menu:**
```bash
python main.py
# Select scenario number from the menu
# Choose 0 to run all scenarios automatically
```

**Run single scenario directly:**
```bash
# Example: Run remote control demonstration
python -m scenarios.gpt4.remote_control
```

**Run with verbose output:**
```bash
# In Python code:
RemoteControlGPT4(verbose=True).run()
```

## Code Architecture

### Core Framework (`scenarios/common/`)

The project uses an **abstract base class pattern** for scenarios:

- **`scenario.py`**: Contains two main classes
  - `Scenario`: Base class for all test scenarios
  - `ChatMLAppScenario`: Extends Scenario for LLM-powered apps using ChatML protocol

- **`chat_app.py`**: Implements `ChatMLApp` class that:
  - Manages OpenAI API interactions
  - Handles tool definitions (view, memory, fetch, e-mail, search)
  - Maintains conversation state
  - Implements the ChatML protocol for tool usage

### Scenario Organization

Scenarios are organized by attack type and LLM model:

**`scenarios/gpt4/`**: GPT-4 based demonstrations
- `remote-control.py`: Remote command & control of compromised LLM
- `data_exfiltration.py`: Leaking user data
- `persistence.py`: Maintaining compromise across sessions
- `spread.py`: Injecting other LLMs via email
- `multi_stage.py`: Multi-stage payload attacks

**`scenarios/gpt3langchain/`**: GPT-3 + LangChain demonstrations
- Similar scenarios to gpt4/ but using LangChain framework
- Additional files: `remote-control.py`, `spread.py`, `data_exfiltration.py`, `multi_stage.py`, `persistence.py`

**`scenarios/code-completion/`**: Code completion engine attacks
- `autocomplete.py`: Attack demonstrations for IDE autocomplete
- `advanced-example/`: Multi-file attack examples with injection payloads

**`scenarios/puzzle/`**: Web server scenarios
- `server.py`: WSGI-based server for puzzle demonstrations
- `wsgi.py`: WSGI application interface

### Entry Point (`main.py`)

Auto-discovers scenarios using `find_subclasses()`:
- Scans all Python files in `scenarios/` directory
- Identifies classes extending `ChatMLAppScenario`
- Provides interactive menu to run scenarios
- Can run all scenarios non-interactively (option 0)

## Key Files

- **`requirements.txt`**: Python dependencies
  - langchain~=0.0.89
  - rich~=13.3.1
  - openai~=0.27.4

- **`main.py`**: Scenario discovery and execution framework

- **`README.md`**: Comprehensive documentation of attack types and research context

## Implementation Pattern

All scenarios follow this pattern:

```python
class ScenarioName(ChatMLAppScenario):
    name = "Human-readable name"
    description = "What this demonstrates"
    target = "Target system description"
    model = "gpt-4"  # or gpt-3.5-turbo

    def _run(self):
        # Setup injection payload
        self.app.ask(injection)

        # Configure simulated environment
        self.app.view = website_content
        self.app.fetch = {url: payload}

        # Trigger attack
        response = self.prompt_user("Question: ", default="...")

        # Verify success
        assert "expected_output" in response
```

## Environment Variables

- **`OPENAI_API_KEY`**: Required. OpenAI API key for model access

## Important Notes

1. **Security Research**: This is academic research code. The "attacks" are controlled demonstrations.

2. **API Costs**: Running scenarios incurs OpenAI API costs. Be mindful of token usage.

3. **Interactive vs Non-Interactive**:
   - Interactive mode: Prompts for user input during execution
   - Non-interactive: Runs with default inputs, suitable for automated testing

4. **Model Versions**: Scenarios specify which model to use (gpt-3.5-turbo or gpt-4)

5. **No Tests**: This repository doesn't have a formal test suite. Scenarios themselves serve as demonstrations.

6. **Research Context**: Refer to the paper on ArXiv (linked in README.md) for full methodology and findings.

## Related Documentation

- **README.md**: Full research description, attack explanations, diagrams
- **diagrams/**: Visual representations of attack flows
- **Research Paper**: https://arxiv.org/abs/2302.12173

## License

MIT License (c) 2023 Kai Greshake