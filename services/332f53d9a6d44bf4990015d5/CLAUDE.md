# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **AWS AI/ML Workshop Korea** repository - a collection of Korean-language examples and workshops for AWS AI/ML services. It contains three main domains:

1. **genai/** - Generative AI examples using Amazon Bedrock, including RAG, agents, and multi-agent systems
2. **sagemaker/** - SageMaker examples for end-to-end ML workflows (training, deployment, pipelines)
3. **neuron/** - AWS Neuron (Inferentia/Trainium) examples for optimized inference and training

> **Note**: This is a **multi-project repository** with independent examples. Each subproject has its own dependencies, README, and execution patterns. Some deeper projects (e.g., `genai/aws-gen-ai-kr/20_applications/08_bedrock_manus/`) have their own detailed CLAUDE.md files.

## Common Development Commands

### Environment Setup
```bash
# Most examples use pip with requirements.txt
pip install -r requirements.txt

# Some projects use UV for dependency management
cd setup/
./create-uv-env.sh <project-name> 3.12
uv run python main.py
```

### Running Examples
```bash
# Jupyter notebooks (most common pattern)
jupyter lab <notebook>.ipynb
# or
jupyter notebook <notebook>.ipynb

# Python scripts
python main.py
python main.py --user_query "Your query" --session_id "session-1"

# Streamlit UI applications
cd app/
streamlit run app.py
```

### Key Dependencies
- **AWS SDK**: `boto3>=1.40.10`
- **Bedrock**: `bedrock-agentcore`, `strands-agents>=1.7.0`
- **LangChain**: `langchain>=0.3.27`
- **Vector Database**: `opensearch-py`, `langchain-community`
- **LLM Observability**: `aws-opentelemetry-distro==0.12.0`

## Architecture Patterns

### AWS Bedrock Integration
Projects use a consistent Bedrock client pattern:
```python
from local_utils.bedrock import get_bedrock_client

bedrock_client = get_bedrock_client(
    assumed_role=None,  # Optional IAM role ARN
    endpoint_url=None,  # Optional endpoint override
    region=None  # Uses AWS_REGION env var by default
)
```

Models are invoked via the Converse API or LangChain abstractions. Common model IDs:
- `anthropic.claude-3-5-sonnet-20240620-v1:0`
- `anthropic.claude-3-haiku-20240307-v1:0`
- `amazon.titan-embed-text-v2:0` (embeddings)

### RAG Architecture (OpenSearch)
Many examples implement RAG with OpenSearch:
- Semantic search using vector embeddings
- Lexical (keyword) search for hybrid retrieval
- Reciprocal Rank Fusion (RRF) for score fusion
- Custom retrievers in `local_utils/rag.py`

Key classes: `OpenSearchHybridSearchRetriever`, `retriever_utils`

### Agent Framework (Strands SDK)
Agent-based examples use the Strands SDK:
- Agent creation via `strands_utils.get_agent()`
- Multi-agent workflows with Coordinator/Planner/Supervisor pattern
- Streaming responses via `graph.stream_async()`
- Global state management via `_global_node_states`

## Directory Structure

```
genai/
├── aws-gen-ai-kr/
│   ├── 00_setup/              # Environment setup notebooks
│   ├── 01_Generation/         # Text generation examples
│   ├── 12_bedrock_claude3/    # Claude 3 + Converse API
│   ├── 13_agentcore/          # Bedrock AgentCore + Strands SDK tutorials
│   ├── 20_applications/       # Full application examples (RAG, chatbots, agents)
│   ├── 30_fine_tune/          # Model fine-tuning examples
│   └── 40_inference/          # Inference deployment examples
├── workshop/                  # Workshop materials
└── genai-app-demo/            # Demo applications

sagemaker/
├── 01-sagemaker-101/          # Getting started
├── hyperpod/                  # Distributed training
├── sm-pipeline/               # MLOps pipelines
├── sm-kornlp/                 # Korean NLP examples
└── [other topic directories]/

neuron/
├── tutorial/                  # Neuron tutorials
├── hf-optimum/                # HuggingFace Optimum Neuron
├── vLLM/                      # vLLM on Neuron
└── blog/                      # Blog references
```

## Code Conventions

### License Headers
Python files include:
```python
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
```

### AWS Configuration
Projects expect AWS credentials via:
- Environment variables: `AWS_REGION`, `AWS_DEFAULT_REGION`, `AWS_PROFILE`
- IAM roles for Bedrock access
- Optional assumed roles for cross-account access

### Output Utilities
Common helper pattern:
```python
from local_utils import print_ww  # Wide print for Jupyter
```

## Key Utility Modules

- `local_utils/bedrock.py` - Bedrock client creation, model info, converse API utilities
- `local_utils/rag.py` - RAG retrievers, hybrid search, ensemble scoring
- `local_utils/opensearch.py` - OpenSearch client, index management, document operations
- `local_utils/chat.py` - Conversational chat UI and history management
- `src/utils/strands_sdk_utils.py` - Strands SDK agent creation and streaming utilities

## Testing

This repository does not have a unified test suite. Each subproject is independently tested:

```bash
# Korean font verification (common across agent projects)
python setup/test_korean_font.py

# Streaming agent tests (specific projects)
python test_stream_graph.py
```

Check individual project directories for their specific testing patterns.

## Environment Variables

Required for most Bedrock examples:
- `AWS_REGION` or `AWS_DEFAULT_REGION` (e.g., `us-west-2`)
- `AWS_PROFILE` (optional, for named profiles)
- `BEDROCK_MODEL_ID` (optional, defaults to Claude Haiku)

## Korean Language Support

Many examples include Korean language processing. When generating PDFs or visualizations:
- Korean fonts may need installation (`setup/install_korean_font.sh`)
- Use `print_ww()` for wide-format printing in Jupyter (handles Korean characters)
- Font verification: `python setup/test_korean_font.py`