# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **Amazon Bedrock AgentCore Samples** repository - a collection of examples, tutorials, and use cases demonstrating how to use Amazon Bedrock AgentCore for building AI agent applications. The project is framework-agnostic and model-agnostic, supporting Strands Agents, CrewAI, LangChain, LlamaIndex, and any other agent framework.

## Repository Structure

- **`01-tutorials/`** - Interactive Jupyter notebook tutorials organized by AgentCore component:
  - Runtime (secure, serverless agent execution)
  - Gateway (API/Lambda to MCP-compatible tool conversion)
  - Memory (managed memory infrastructure)
  - Identity (agent identity and access management)
  - Tools (Code Interpreter and Browser Tool)
  - Observability (tracing, debugging, monitoring)
  - E2E tutorial moving a customer support agent from prototype to production

- **`02-use-cases/`** - Complete end-to-end applications demonstrating real-world implementations

- **`03-integrations/`** - Framework integrations (Strands Agents, LangChain, CrewAI, etc.)

- **`04-infrastructure-as-code/`** - Infrastructure templates for deployment

## Development Setup

**Prerequisites:**
- Python 3.10 or later
- AWS account with credentials configured (`aws configure`)
- Docker or Finch (for local development only)
- Model access to Anthropic Claude 4.0+ in Amazon Bedrock console
- AWS Permissions: `BedrockAgentCoreFullAccess` and `AmazonBedrockFullAccess` managed policies

**Setup Virtual Environment:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Setup Jupyter Kernel:**
```bash
python -m ipykernel install --user --name=notebook-venv --display-name="Python (notebook-venv)"
```

**Run Notebooks:**
```bash
jupyter notebook path/to/notebook.ipynb
```

After opening a notebook, ensure you select the correct kernel: `Kernel` → `Change kernel` → `Python (notebook-venv)`

## Quick Start - Runtime

**Install packages:**
```bash
pip install bedrock-agentcore strands-agents bedrock-agentcore-starter-toolkit
```

**Create an agent (my_agent.py):**
```python
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp()
agent = Agent()

@app.entrypoint
def invoke(payload):
    user_message = payload.get("prompt", "Hello! How can I help you today?")
    result = agent(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    app.run()
```

**Test locally:**
```bash
python my_agent.py
# In another terminal
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello!"}'
```

**Deploy to AWS:**
```bash
agentcore configure -e my_agent.py
agentcore launch
agentcore invoke '{"prompt": "tell me a joke"}'
```

## Common Development Commands

**Linting & Formatting:**
```bash
# Install ruff via uv
uv tool install ruff

# Check code quality
uv tool run ruff check

# Check formatting
uv tool run ruff format --check

# Fix linting issues
uv tool run ruff check --fix
```

**Testing:**
```bash
# Run pytest in a use case directory
cd 02-use-cases/customer-support-assistant
pytest test/ -v
```

**Installing development tools:**
```bash
# Using uv (faster alternative to pip)
uv tool install ruff
uv tool install pytest
```

## Code Architecture Patterns

1. **Framework-Agnostic**: Agents use interfaces that work with any framework (Strands, CrewAI, LangChain, etc.)

2. **Notebook-First**: Tutorials are primarily Jupyter notebooks with accompanying Python utility modules in `utils.py` files

3. **Component-Based**: Each AgentCore component (Runtime, Gateway, Memory, etc.) has dedicated tutorials demonstrating its capabilities

4. **Production-Ready Examples**: Use cases provide complete implementations with proper testing, configuration, and deployment guides

## Key AWS Services & Integrations

- **Amazon Bedrock**: Primary LLM service (supports Anthropic Claude 4.0+)
- **Bedrock AgentCore**: Core infrastructure for agents
- **AWS Lambda**: Serverless function integration
- **Amazon Cognito**: Identity management
- **Amazon SSM**: Parameter store for configuration
- **OpenTelemetry**: Observability and tracing

## Project Dependencies

Key packages include:
- `bedrock-agentcore` - Core AgentCore SDK
- `strands-agents` - Strands Agents framework
- `bedrock-agentcore-starter-toolkit` - Starter templates
- `boto3` - AWS SDK
- `langchain[aws]`, `langgraph` - LangChain ecosystem
- `jupyterlab`, `ipykernel` - Jupyter environment
- `mcp>=1.9.0` - Model Context Protocol

See `requirements.txt` for complete dependency list.

## Testing Strategy

Some use cases include unit tests (e.g., `02-use-cases/customer-support-assistant/test/`). Tests use pytest and focus on:
- Tool functionality
- Agent behavior
- Integration with AWS services

Run tests using `pytest test/` from the specific use case directory.

## CI/CD & Code Quality

GitHub workflows enforce code quality:
- **python-lint.yml**: Runs `ruff check` and `ruff format` on changed Python files
- **js-lint.yml**: JavaScript/TypeScript linting
- **codeql.yml**: CodeQL security analysis
- **dependabot.yml**: Automatic dependency updates
- Security scanning workflows for vulnerability detection

## Framework-Specific Notes

### Strands Agents
- Primary recommended framework for AgentCore
- Clean, simple agent creation API
- Well-integrated with AgentCore features

### LangChain/LangGraph
- Use `langchain[aws]` extras for Bedrock integration
- LangGraph for complex multi-agent workflows
- Observability support via `langsmith[otel]`

### CrewAI
- Multi-agent collaboration patterns
- Role-based agent design
- AgentCore provides infrastructure layer

## Important Configuration Files

- `.bedrock_agentcore.yaml` - Runtime configuration for deployed agents
- `requirements.txt` - Python dependencies
- `pyproject.toml` - May contain tool configurations
- `.github/workflows/` - CI/CD pipelines

## Getting Help

- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [AWS Workshop - Getting Started](https://catalog.us-east-1.prod.workshops.aws/workshops/850fcd5c-fd1f-48d7-932c-ad9babede979/en-US)
- [AWS Workshop - Deep Dive](https://catalog.workshops.aws/agentcore-deep-dive/en-US)
- [Starter Toolkit](https://github.com/aws/bedrock-agentcore-starter-toolkit)
- [Discord Community](https://discord.gg/bedrockagentcore-preview)

## Contributing

See `CONTRIBUTING.md` for contribution guidelines. Key points:
- Work against latest `main` branch
- Ensure local tests pass before PRs
- Open issues to discuss significant changes
- Follow code formatting standards (enforced by CI)
- Use conventional commit messages