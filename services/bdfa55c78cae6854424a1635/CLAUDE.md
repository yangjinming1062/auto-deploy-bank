# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **Chainlit Cookbook** - a collection of example/demo projects showcasing Chainlit's chatbot UI capabilities. Each folder is a self-contained, independent demo project demonstrating different integrations and use cases.

## Running Demos

Each demo folder follows a consistent pattern. To run any demo:

```bash
cd <demo-folder>
pip install -r requirements.txt
cp .env.example .env  # Copy and fill in API keys
chainlit run app.py -w  # Watch mode with auto-reload
```

## Common Demo Structure

- `app.py` - Main Chainlit application entry point
- `requirements.txt` - Python dependencies
- `.env.example` - Template for environment variables (API keys, etc.)
- `README.md` - Demo-specific documentation
- `chainlit.md` - Optional Chainlit UI config (order, tags, settings)
- `public/` - Static assets (images, etc.)

## Key Chainlit Patterns

Most demos use these Chainlit decorators:
- `@cl.on_chat_start` - Initialize chat session, set up user session state
- `@cl.on_message` - Handle incoming messages
- `@cl.password_auth_callback` - Custom authentication
- `@cl.on_chat_resume` - Handle chat resumption (persisted conversations)

Stream responses using `cl.Message` and `msg.stream_token()` for real-time updates.

## Frontend Demos

Some demos (custom-frontend, react-native-chat) include separate frontend applications:
- `frontend/` - React/Vite frontend
- `backend/` - Chainlit backend server
- Run backend with `uvicorn app:app --host 0.0.0.0 --port 80`
- Run frontend with `npm run dev`

## Common Dependencies

Many demos use:
- `chainlit` - Core framework
- `langchain`, `langgraph` - LLM orchestration
- `anthropic`, `openai` - LLM providers
- `python-dotenv` - Environment variable management

## Demo Categories

- **Simple demos**: anthropic-chat, openai-concurrent-functions, deepseek-r1
- **Framework integration**: langgraph-memory, langgraph-tavily, llama-index
- **Data/Vector stores**: chroma-qa-chat, pinecone, pdf-qa, azure-openai-pinecone-pdf-qa
- **MCP integration**: mcp, mcp-linear
- **Frontend customization**: custom-frontend, custom-element, react-native-chat
- **Advanced**: openai-functions-streaming, anthropic-functions-streaming, extended-thinking-in-the-ui