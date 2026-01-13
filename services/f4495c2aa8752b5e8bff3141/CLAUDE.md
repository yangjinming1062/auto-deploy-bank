# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Python Backend

```bash
# Setup environment
conda create -n oscopilot_env python=3.10 -y
conda activate oscopilot_env
pip install -e .

# Configure environment
cp .env_template .env
# Edit .env and add your OpenAI API key

# Run FRIDAY agent
python quick_start.py
# or use CLI:
friday

# Run self-learning example
python course_learning.py

# Run tests
pytest test/
```

### Frontend (Electron + React)

```bash
cd fronted

# Install dependencies
npm install

# Development mode (runs React + Electron together)
npm start

# Build for production
npm run build

# Run only React dev server
npm run dev:react

# Run only Electron app (requires React dev server running)
npm run dev:app
```

### Documentation

```bash
cd docs
make html  # Build Sphinx documentation
```

### Testing Examples

```bash
# Test basic functionality
python quick_start.py

# Test vision capabilities
python examples/friday_vision/quick_start.py

# Test self-learning
python course_learning.py

# Test GAIA benchmark
python examples/GAIA/quick_start.py
```

## Architecture Overview

OS-Copilot is a Python framework for building generalist AI computer agents (FRIDAY) that interact with operating systems, applications, and perform automated tasks.

### Core Components

**Agent System** (`oscopilot/agents/`):
- **friday_agent.py** - Original FRIDAY agent implementation
- **friday2_agent.py** - Newer version with enhancements
- **self_learning.py** - Self-improvement and learning capabilities
- **prompt.py** - LLM prompt templates

**Module System** (`oscopilot/modules/`):
- **planner/** - Task planning and decomposition
- **retriever/** - Information retrieval and memory
- **executor/** - Task execution and tool management
- **learner/** - Learning mechanisms for self-improvement

**Environment Interfaces** (`oscopilot/environments/`):
- **bash_env.py** - Bash terminal interaction
- **py_jupyter_env.py** - Jupyter notebook interface
- **subprocess_env.py** - Subprocess management

**Tool Repository** (`oscopilot/tool_repository/`):
- **basic_tools/** - Core OS interaction tools
- **api_tools/** - External API integrations
- **generated_tools/** - Dynamically generated tools
- **manager/** - Tool lifecycle management

### Frontend (`fronted/`)

Electron-based desktop application with React UI for controlling FRIDAY agents. Features:
- React 18 with Material-UI components
- Real-time agent interaction
- Built with `npm start` for development

### Examples Directory

Demonstrations and benchmarks:
- **friday_vision/** - Vision-enabled FRIDAY agent
- **GAIA/** - GAIA benchmark tasks
- **SheetCopilot/** - Excel automation
- **light_friday/** - Lightweight version
- **LLAMA3/** - Llama model integration

## Entry Points

- **`quick_start.py`** - Primary entry point for FRIDAY agent
- **`course_learning.py`** - Self-learning demonstration
- **`friday` CLI command** - Installed via setup.py entry points
- **`fronted/package.json`** - Frontend application entry

## Important Project Information

- **Agent Name**: FRIDAY (an embodied conversational agent)
- **Language**: Python 3.10+ required
- **Main Dependencies**: OpenAI, LangChain, FastAPI, Electron
- **Key Capability**: Self-improving agents that can interact with OS elements
- **Current Limitation**: Single-round conversations only (no multi-turn)
- **Platform Support**: Linux and macOS
- **Frontend**: Electron desktop app with React UI

## Environment Configuration

1. Copy `.env_template` to `.env`
2. Add OpenAI API key: `OPENAI_API_KEY=your_key_here`
3. Optional: Add other API keys as needed for specific tools

## Self-Learning System

FRIDAY agents can learn and improve from experience through:
- Experience recording and analysis
- Pattern recognition in task execution
- Tool usage optimization
- Self-directed improvement (see `course_learning.py`)

## Tutorial Structure

The project follows a tiered tutorial system:
- **Beginner**: Installation and getting started
- **Intermediate**: Adding tools, API deployment, Excel automation
- **Advanced**: Custom API tools design

See `docs/roadmap.md` for planned features and current development status.
