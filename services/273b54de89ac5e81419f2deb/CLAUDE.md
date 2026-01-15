# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A generative UI financial agent that uses Vercel AI SDK and LangChain agents to dynamically render UI components based on AI responses. It integrates with Financial Datasets API for real-time stock data and Tavily for web search.

## Commands

### Docker (Recommended)
```bash
docker-compose up  # Starts both frontend and backend
```

### Backend (Python/FastAPI)
```bash
cd backend
poetry install              # Install dependencies
poetry run start            # Run server on port 8000
poetry run pytest tests/    # Run unit tests
make lint                   # Run ruff and mypy
make format                 # Format code with ruff
make test TEST_FILE=<path>  # Run specific test file
```

### Frontend (Next.js)
```bash
cd frontend
yarn install              # Install dependencies
yarn dev                  # Run dev server on port 3000
yarn build                # Build for production
yarn lint                 # Run ESLint
yarn format               # Format with Prettier
```

## Architecture

### Backend (`backend/gen_ui_backend/`)

**Agent Flow (`chain.py`):**
1. User input → `invoke_model` node calls GPT-4o with financial system prompt
2. Model decides whether to use tools or return direct text
3. If tools needed → `invoke_tools` node executes the appropriate tool
4. Results are streamed back to frontend

**Tools (`backend/gen_ui_backend/tools/`):**
- `prices.py`: Stock price data via Financial Datasets API
- `financials/search/`: Company financial statements (income, balance sheet, cash flow)
- `insider_transactions/`: Insider trading activity
- `web_search/tavily/`: General web search

**Server (`server.py`):**
- FastAPI app with LangServe at `/chat` endpoint
- Exposes the LangGraph as a Runnable
- CORS configured for localhost:3000

### Frontend (`frontend/`)

**Generative UI Flow (`app/ai/agent.tsx`):**
1. User message → calls backend `/chat` endpoint via `RemoteRunnable`
2. Streams events and maps tool calls to UI components:
   - `get-prices` → `ChartContainer`
   - `search-line-items` → `LineItemsTable`
   - `search-web` → `WebSearchResults`
   - `insider-transactions` → `InsiderTransactionsTable`
3. AI text is streamed as a separate message component

**Key Components (`components/prebuilt/`):**
- `chat.tsx`: Main chat interface with input and message history
- `chart.tsx` / `chart-container.tsx`: Stock price visualization
- `line-items-table.tsx`: Financial statement data display
- `insider-transactions-table.tsx`: Insider trading table
- `loading-charts.tsx`: Skeleton loaders during streaming

**AI SDK Utilities (`utils/`):**
- `server.tsx`: `streamRunnableUI()` - core function for streaming LangGraph events and rendering generative UI
- `client.tsx`: Client-side AI provider and action hooks

## Key Dependencies

**Backend:**
- `langgraph` - Agent state machine orchestration
- `langchain` / `langchain-openai` - LLM integration
- `fastapi` + `uvicorn` - Web server
- `langserve` - Expose runnables via REST API

**Frontend:**
- `ai` (Vercel AI SDK) - RSC streaming and generative UI
- `@langchain/core` - Type definitions for remote runnables
- `@radix-ui/react-*` - UI component primitives
- `@tremor/react` - Chart components
- `next` (App Router)

## Environment Variables

**Root `.env`:**
- `OPENAI_API_KEY`
- `FINANCIAL_DATASETS_API_KEY`
- `TAVILY_API_KEY`
- `LANGCHAIN_API_KEY` (optional, for tracing)

**Frontend additionally:**
- `NEXT_PUBLIC_BACKEND_URL` (defaults to `http://localhost:8000/chat`)

## API Endpoint

- **Backend:** `http://localhost:8000/chat` (LangServe with chat playground)
- **Frontend:** `http://localhost:3000`
- **API Docs:** `http://localhost:8000/docs`