# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a collection of **LangChain experiments** demonstrating various LLM-powered applications. Each experiment is in a separate subdirectory with its own README and code. The repository showcases how to build applications with LangChain using different models (OpenAI GPT, Falcon-7B), vector databases (FAISS, Pinecone, pgvector), and integrations (Slack, YouTube, LangSmith).

## Common Commands

### Setup
```bash
# Create and activate Python virtual environment
python3 -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp example.env .env
# Edit .env with your API keys
```

### Run Experiments

Each experiment directory contains standalone Python scripts:

```bash
# OpenAI Function Calling
python openai-functions/openai_function_calling.py

# YouTube Transcript Analysis
python youtube/youtube_llm.py

# Pandas DataFrame Agent
python pandas-agent/src/pandas_agent.py

# Falcon Model vs OpenAI
python models/falcon_model.py

# Slack Bot (requires Flask server)
gunicorn --bind=0.0.0.0 --timeout 600 --chdir slack app:flask_app

# LangSmith Tutorial
python langsmith-tutorial/src/langsmith-tutorial.py

# Vector Databases
python pgvector/pgvector_quickstart.py
python pgvector/pgvector_service.py

# Audio Transcription & Summarization
python summaries/summary-app.py

# Simple QuickStart
python introduction/quickstart_guide.py
```

## Architecture & Structure

### Directory Layout
- **Root**: Main README, requirements.txt, environment templates
- **introduction/**: Basic LangChain quickstart tutorial
- **openai-functions/**: OpenAI function calling feature examples
- **pandas-agent/**: LangChain agents for data analysis
- **youtube/**: YouTube transcript processing with FAISS
- **models/**: Model comparison (Falcon-7B vs OpenAI)
- **slack/**: Slack bot integration with Bolt/Flask
- **langsmith-tutorial/**: LangSmith monitoring and evaluation
- **pgvector/**: Vector databases (Pinecone & PostgreSQL pgvector)
- **summaries/**: Audio transcription and PDF summary generation
- **data/**: Sample text files (Christmas Carol, Romeo & Juliet)
- **summaries/**: Output directory for generated summaries

### Key Technologies

**LLM Integration:**
- OpenAI (GPT-3.5, GPT-4, text-davinci-003)
- HuggingFace Hub (Falcon-7B)
- LangChain framework

**Vector Stores:**
- FAISS (in-memory)
- Pinecone (cloud vector database)
- pgvector (PostgreSQL extension)

**Agent Types:**
- Zero-shot ReAct
- Conversational ReAct
- Pandas DataFrame Agent
- OpenAI Functions Agent

**Integration Platforms:**
- Slack (Bolt SDK, Flask)
- YouTube (transcript extraction)
- LangSmith (evaluation & monitoring)

### Dependencies

Core packages in requirements.txt:
- `langchain` - Core framework
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management
- `youtube-transcript-api` - YouTube transcript extraction
- `chromadb` - Vector database
- `faiss-cpu` - Similarity search
- `pinecone-client` - Pinecone vector database
- `psycopg2` & `pgvector` - PostgreSQL vector extension
- `slack-sdk` & `slack-bolt` - Slack integration
- `google-api-python-client` & `google-search-results` - Google/SerpAPI

## Environment Variables

Required in `.env` file:
```bash
OPENAI_API_KEY="your-key"              # For OpenAI models
HUGGINGFACEHUB_API_TOKEN="your-key"    # For Falcon model
PINECONE_API_KEY="your-key"            # For Pinecone
PINECONE_ENV="your-env"                # For Pinecone
SLACK_BOT_TOKEN="xoxb-..."             # For Slack bot
SLACK_SIGNING_SECRET="..."             # For Slack bot
SLACK_BOT_USER_ID="..."                # For Slack bot
```

## Experiment Details

### YouTube Experiment (youtube/)
- Loads video transcripts using `YoutubeLoader`
- Splits text into chunks with `RecursiveCharacterTextSplitter`
- Creates FAISS vector store from embeddings
- Answers questions via similarity search
- Key files: `youtube_llm.py`, `youtube_chat.py`

### OpenAI Functions (openai-functions/)
- Demonstrates structured output with function calling
- Compares ChatGPT with/without function calling
- Shows airport customer service chatbot
- Uses `gpt-4-0613` and `gpt-3.5-turbo-0613` models
- Key file: `openai_function_calling.py`

### Pandas Agent (pandas-agent/)
- Interactive data analysis with `create_pandas_dataframe_agent`
- Uses SerpAPI and llm-math tools
- Processes data science salaries dataset
- Supports single and multi-dataframe operations
- Key file: `pandas_agent.py`

### Slack Bot (slack/)
- Flask application with Slack Bolt adapter
- Handles app mentions and responds with OpenAI
- Deployable with gunicorn (see startup.txt)
- Uses ngrok for local development
- Key files: `app.py`, `functions.py`

### LangSmith (langsmith-tutorial/)
- Application monitoring and evaluation
- Creates datasets from various sources (CSV, DataFrame, runs)
- Uses QA evaluators (context_qa, qa, cot_qa)
- Custom evaluation criteria (cosine distance, string distance)
- Key file: `src/langsmith-tutorial.py`

### Vector Databases (pgvector/)
- Compares Pinecone vs PostgreSQL pgvector
- Loads text documents, creates embeddings, performs similarity search
- Demonstrates vector store integration with LangChain
- Key files: `pgvector_quickstart.py`, `pgvector_service.py`

### Models Comparison (models/)
- Loads Falcon-7B from HuggingFace Hub
- Compares summarization vs OpenAI text-davinci-003
- Tests on YouTube video transcripts
- Key file: `falcon_model.py`

### Audio Summarization (summaries/)
- Transcribes audio with OpenAI Whisper
- Summarizes with LangChain's `load_summarize_chain`
- Exports to PDF with ReportLab
- Key file: `summary-app.py`

## Development Notes

- Each experiment is independent with its own dependencies
- Most scripts use `python-dotenv` to load `.env` files
- No test suite - experiments run standalone
- Python 3.6+ required, 3.9+ recommended for newer LangChain features
- GPU not required (Falcon-7B can be run via API)
- Video tutorials available at: youtube.com/@daveebbelaar