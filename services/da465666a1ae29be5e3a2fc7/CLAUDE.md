# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Clevrr Computer is a desktop automation agent that uses PyAutoGUI and LLMs (Gemini/Azure OpenAI) to perform system actions. It features a ReAct-based agent that takes screenshots, analyzes screen content, and executes mouse/keyboard automation.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application (defaults to gemini model with float UI enabled)
python main.py

# Run with OpenAI model
python main.py --model openai

# Disable floating UI
python main.py --float-ui 0
```

## Architecture

```
main.py           # Entry point: Tkinter GUI + argument parsing
utils/agent.py    # Creates ReAct agent using LangChain
utils/tools.py    # get_screen_info tool (screenshot + vision model analysis)
utils/prompt.py   # PromptTemplate composition (PREFIX + EXAMPLES + SUFFIX)
utils/contants.py # Model initialization, UI constants, agent prompts
```

### Key Components

- **Agent**: LangChain `create_react_agent` with two tools:
  - `PythonAstREPLTool`: Executes PyAutoGUI code (via `pg` variable)
  - `get_screen_info`: Takes ruled screenshot, queries vision LLM for coordinates/content

- **Models**: Configured in `contants.py`:
  - `gemini`: `ChatGoogleGenerativeAI` (gemini-1.5-pro-latest) - used for screen analysis
  - `openai`: `AzureChatOpenAI` - used for action reasoning

- **Screen Analysis Flow**:
  1. `get_ruled_screenshot()` overlays coordinate grid on screenshot
  2. Image sent to Gemini with user question
  3. Returns coordinates and screen content for PyAutoGUI actions

## Environment Variables

Required in `.env` file:
- `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`, `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`
- `GOOGLE_API_KEY`

## Important Implementation Details

- `pg.PAUSE = 2`: 2-second delay after all PyAutoGUI actions
- `AgentExecutor` configured with `return_intermediate_steps=True`, `verbose=True`, `handle_parsing_errors=True`
- The agent uses a chain-of-thought approach: one action at a time, verified by screen analysis after each step
- Tkinter GUI is fixed to 30% screen width, full height minus 150px