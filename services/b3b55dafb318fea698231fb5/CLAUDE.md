# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Brainstore is a proof-of-concept AI agent with persistent memory. It answers questions by:
1. First checking its vector memory (ChromaDB) for relevant information
2. If insufficient data exists, it browses the web to learn, then saves the learned information to memory

## Commands

```bash
npm run agent    # Compile TypeScript and run the agent
npx tsc          # Compile TypeScript only
```

## Architecture

**Main entry point:** `index.ts` - Handles CLI interaction, ChromaDB client initialization, and orchestrates the question-answering flow.

**Core logic (`utils/index.ts`):**
- `checkForBrain()` - Creates or retrieves ChromaDB collection for memory storage
- `answerFromMemory()` - Searches vector store for relevant memories and generates answers using GPT + RAG pattern
- `answerFromSearch()` - Uses LangChain agent with WebBrowser tool and SerpAPI to research and learn new information
- `addMemory()` - Stores learned information in ChromaDB for future retrieval

**Data flow:** User input → Check memory → (if insufficient) Web search → Save memory → Respond

## Dependencies

- **ChromaDB** - Local vector database for memory storage (requires Docker)
- **LangChain** - AI agent framework with tools (WebBrowser, Calculator, SerpAPI)
- **OpenAI** - GPT models for embeddings and LLM responses
- **ESM** - Uses ES modules (`"type": "module"` in package.json)

## Configuration

Required environment variables in `.env`:
- `OPENAI_API_KEY` - OpenAI API key (required)
- `COLLECTION_NAME` - ChromaDB collection name (default: ai-brainstore)
- `REVIEW_MEMORIES` - Whether to manually review before saving (true/false)
- `SERPAPI_API_KEY` - Optional but recommended for better web search

## Running ChromaDB

```bash
git clone https://github.com/chroma-core/chroma.git
cd chroma
docker-compose up -d --build
```