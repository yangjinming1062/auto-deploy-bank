# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **WorldQuant Alpha Generator** project - a system for generating, testing, and submitting financial alpha factors to the WorldQuant Brain platform. The project has multiple implementations:

- **Naive-Ollama** (recommended): Local LLM-based alpha generation with GPU acceleration
- **Consultant-Naive-Ollama**: Enhanced version with model fleet and orchestration
- **Python/Legacy**: Pre-consultant and consultant implementations
- **Rust**: Alternative Rust implementation
- **Dify Components**: Agent framework integration (agent-dify-api, agent-dify-web)
- **Agent-Next**: Next.js web interface for agent network management

## Common Commands

### Python Projects (agent-dify-api)

```bash
cd agent-dify-api

# Install dependencies with Poetry
poetry self add poetry-plugin-shell
poetry shell
poetry install --with dev

# Run tests
pytest

# Lint with ruff
ruff check .
ruff format .

# Run the API
python app.py
```

### Node.js Projects (agent-next)

```bash
cd agent-next

# Install dependencies
npm install  # or pnpm install

# Development server
npm run dev

# Build for production
npm run build

# Lint
npm run lint
```

### Rust Project

```bash
cd rust

# Build
cargo build --release

# Run
cargo run --release
```

### Docker-based Projects (naive-ollama, consultant-naive-ollama)

```bash
# GPU-enabled deployment
docker-compose -f docker-compose.gpu.yml up -d

# CPU-only deployment
docker-compose up -d

# Production build
docker-compose -f docker-compose.prod.yml build
```

### Python Alpha Scripts (legacy)

```bash
# Install requirements
pip install -r requirements.txt

# Run alpha generator
python alpha_generator.py

# Mine alpha expressions
python alpha_expression_miner.py --expression "expression"

# Submit successful alphas
python successful_alpha_submitter.py
```

## Architecture

### Naive-Ollama System

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Dashboard │    │ Alpha Generator │    │  WorldQuant API │
│   (Flask)       │◄──►│   (Ollama)      │◄──►│   (External)    │
│   Port 5000     │    │   Port 11434    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│ Alpha Orchestrator │◄─────────────┘
                        │   (Python)      │
                        └─────────────────┘
```

### Alpha Expression DSL

WorldQuant alpha expressions use a specific syntax with operators:

- **Time Series**: `ts_mean`, `ts_std_dev`, `ts_zscore`, `ts_rank`, `ts_corr`, `ts_delay`, `ts_decay_linear`
- **Cross Sectional**: `rank`, `normalize`, `winsorize`, `zscore`, `quantile`, `scale`
- **Group Operations**: `group_neutralize`, `group_rank`, `group_mean`, `group_scale`
- **Logical**: `if_else`, `greater`, `less`, `and`, `or`, `trade_when`

### Credential Setup

For WorldQuant integration, create `credential.txt` in the project directory:
```json
["your.email@worldquant.com", "your_password"]
```

### Consultant Templates

Templates are located in `consultant-templates-ollama/`:
- `dynamic_personas.json` - LLM prompts for alpha generation
- `operatorRAW.json` - Available operators
- `enhanced_template_generator_v2.py` - Template generation script

## Key Files

- `naive-ollama/alpha_generator_ollama.py` - Main alpha generation
- `naive-ollama/alpha_orchestrator.py` - Scheduling and orchestration
- `consultant-naive-ollama/alpha_expression_miner.py` - Expression mining
- `cursor_idea_workbench/alpha_analyzer.py` - Alpha expression analysis
- `agent-dify-api/pyproject.toml` - Python dependencies and lint config

## Configuration

Environment variables and configuration files:
- `agent-dify-api/.env.example` - Backend API configuration
- `agent-dify-api/.ruff.toml` - Linting rules (120 char line length, ruff)
- `agent-next/.env.example` - Next.js environment
- `credential.txt` - WorldQuant credentials (format: JSON array)