# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Next.js 13 chatbot using LangChain to answer questions about LangChain documentation. Uses RAG (Retrieval-Augmented Generation):

1. Documentation is downloaded, parsed, split, and embedded with OpenAI
2. Embeddings stored in HNSWLib vector store (`data/` directory)
3. User questions trigger similarity search
4. Retrieved context + chat history → OpenAI LLM → streaming response

## Common Commands

```bash
yarn                    # Install dependencies
yarn dev                # Start development server
yarn build              # Build for production
yarn start              # Run production server (requires build)
yarn lint               # Lint code
yarn download           # Download LangChain docs to langchain.readthedocs.io/
yarn ingest             # Create vector store in data/ (required before running)
NODE_OPTIONS='--experimental-fetch' yarn ingest  # Node v16 workaround
```

## Architecture

**Data Flow:**
```
User Input → /api/chat (SSE) → makeChain() → HNSWLib.similaritySearch()
                                                    ↓
                              Retrieved Docs → OpenAI LLM → Streaming Response
```

**Key Files:**

- **`pages/index.tsx`** - Chat UI with message state, streaming response handling
- **`pages/api/chat.ts`** - SSE endpoint streaming tokens to client
- **`pages/api/util.ts`** - LangChain chain setup:
  - `CONDENSE_PROMPT` - Rephrases follow-ups into standalone questions
  - `QA_PROMPT` - Generates answers with doc citations
  - `makeChain()` - Creates ChatVectorDBQAChain for RAG
- **`ingest.ts`** - Ingestion pipeline: loads HTML, splits with 1000-char chunks/200-char overlap, saves to HNSWLib

**Tech Stack:**
- Next.js 13.1.6 (Pages Router)
- langchain 0.0.15, hnswlib-node, openai 3.1.0
- @microsoft/fetch-event-source (SSE client)
- React 18.2.0, MUI 5, react-markdown

## Setup

1. `cp .env.example .env` and add `OPENAI_API_KEY`
2. `yarn download && yarn ingest` (creates `data/` vector store)
3. `yarn dev` → open http://localhost:3000

The `data/` directory must exist and contain the vector store before the server runs.

## Technical Notes

- Uses SSE for streaming (avoid Vercel serverless limitations)
- Chat history enables conversational follow-ups via question condenser
- Custom `ReadTheDocsLoader` in `ingest.ts` parses downloaded HTML docs
- Deployment: Use Fly.io (see `fly.toml`, `Dockerfile`) - not Vercel due to SSE/WebSocket constraints