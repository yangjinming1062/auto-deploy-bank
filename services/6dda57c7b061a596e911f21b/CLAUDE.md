# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenAGI is a Python package for creating AI agents. Agents follow the ReAct pattern (Reasoning + Acting) and can use external tools to complete tasks. The project includes an agent hub (openagi-beta.vercel.app) for sharing and downloading agents.

**Note**: For building agents in AIOS, migrate to [Cerebrum](https://github.com/agiresearch/Cerebrum) (latest SDK).

## Common Commands

### Development Setup
```bash
# Install in development mode
pip install -e .

# Install pre-commit hooks (recommended)
pre-commit install

# Install dev dependencies
pip install -r requirements-dev.txt
```

### Testing
```bash
# Run all tests from repository root
pytest tests/ -v

# Run tests from pyopenagi directory (as documented in CONTRIBUTING.md)
cd pyopenagi && pytest -v tests

# Run specific test
pytest tests/test_agent_creation.py::test_agent_creation -v
```

### Agent Management
```bash
# Upload agent to hub
python pyopenagi/agents/interact.py --mode upload --agent <author_name/agent_name>

# Download agent from hub
python pyopenagi/agents/interact.py --mode download --agent <author_name/agent_name>
```

### Code Quality
```bash
# Run pre-commit hooks on all files
pre-commit run --all-files
```

## High-Level Architecture

### Core Components

1. **Agent Layer** (`pyopenagi/agents/`)
   - **BaseAgent** (base_agent.py): Abstract base class defining agent lifecycle, tool loading, workflow management, and LLM interaction
   - **ReactAgent** (react_agent.py): Main implementation using ReAct pattern with automatic/manual workflow modes
   - **AgentProcess** (agent_process.py): Manages agent state, timing, and process lifecycle
   - **Example Agents** (agents/example/): Reference implementations (academic_agent, story_teller, travel_agent, etc.)

2. **Tool Layer** (`pyopenagi/tools/`)
   - **BaseTool**, **BaseRapidAPITool**, **BaseHuggingfaceTool**: Base classes for tool implementations
   - Tool categories: arxiv, bing, currency_converter, google, imdb, openai, shazam, trip_advisor, wolfram, etc.
   - Each tool provides function-calling format for LLM integration

3. **Manager** (`pyopenagi/manager/`)
   - **AgentManager**: Handles agent upload/download from hub with caching and dependency management

4. **Utils** (`pyopenagi/utils/`)
   - **chat_template.py**: Query/Response template classes for LLM communication
   - **logger.py**: AgentLogger for execution monitoring
   - **commands/**: CLI command implementations

### Agent Structure

Agents follow this directory structure:
```
pyopenagi/agents/
  author/
    agent_name/
      agent.py          # Main agent implementation (extends ReactAgent)
      config.json       # Agent configuration
      meta_requirements.txt  # Dependencies
```

### Key Files

- **pyopenagi/agents/interact.py**: CLI interface for agent hub operations (upload/download/list)
- **pyopenagi/agents/base_agent.py**: Core agent logic, tool management, workflow execution
- **pyopenagi/agents/react_agent.py**: ReAct pattern implementation with workflow planning
- **tests/**: Test suite including agent creation and tool tests

### Agent Workflow

1. BaseAgent loads configuration and tools
2. ReactAgent builds system instruction with tool descriptions
3. Automatic mode: LLM generates JSON workflow, then executes step-by-step
4. Manual mode: Workflow is pre-defined by agent implementation
5. Each step: LLM generates response, tools are called if specified, observations are collected
6. Results are logged with timing metrics

### Integration Points

- **AIOS**: Uses global hooks (aios.hooks.stores._global.global_llm_req_queue_add_message)
- **Tool APIs**: Integrates with RapidAPI, HuggingFace, and custom APIs
- **Agent Hub**: Upload/download agents via REST API (openagi-beta.vercel.app)

## Important Notes from Documentation

### tools.md
- **Wolfram Alpha**: Requires WOLFRAM_ALPHA_APPID environment variable
- **Rapid API**: Requires RAPID_API_KEY environment variable
- Current tools: Words API, Moon Phase, Trip Advisor, Shazam, IMDB

### CONTRIBUTING.md
- Use pre-commit hooks for code formatting
- Follow conventional commit message format: `<type>: <subject>`
- Commit types: feat, fix, docs, style, refactor, perf, test, chore, revert
- Create pull requests to `dev` branch for new features

### pyproject.toml
- Build system: hatchling
- Python versions: >=3.9, supports 3.9-3.11
- Dynamic dependencies from requirements.txt