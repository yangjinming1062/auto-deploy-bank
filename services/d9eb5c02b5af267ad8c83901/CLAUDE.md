# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Travel Agent is a Streamlit web application that uses an LLM-powered agent to plan travel itineraries with real-time data. The agent integrates weather APIs, web search, YouTube videos, and performs cost calculations.

## Commands

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run the application:**
```bash
streamlit run streamlit_app.py
```

**Run with custom port:**
```bash
streamlit run streamlit_app.py --server.port 8080
```

**Quick start script (validates environment and starts app):**
```bash
python run_script.py
```

**Development mode (auto-reload on save):**
```bash
streamlit run streamlit_app.py --server.runOnSave true
```

## Architecture

**Frontend:** Streamlit with session state management for chat history and agent state.

**Agent Framework:** LangGraph StateGraph with the following structure:
- `MessagesState` manages conversation flow
- `llm_decision_step` node processes user queries using GPT-4o
- `ToolNode` executes tool calls and returns results
- Conditional edges determine when to call tools vs end execution

**Tool System:**
- Custom `@tool` decorated functions for arithmetic operations (addition, multiplication, division, subtraction)
- `get_weather` - OpenWeatherMap integration
- `search_google` - Google Serper API (falls back to DuckDuckGo)
- `youtube_search` - YouTube video discovery
- `python_repl` - Complex calculations via Python shell

**Environment Variables (required in `.env` or Streamlit secrets):**
- `OPENAI_API_KEY` - Required for LLM calls
- `SERPER_API_KEY` - Optional, DuckDuckGo used as fallback
- `OPENWEATHERMAP_API_KEY` - Optional, weather feature disabled if missing

## File Structure

- `streamlit_app.py` - Main application (initialization, tools, UI, agent graph)
- `run_script.py` - Bootstrap script for dependency validation and app startup
- `requirements.txt` - All Python dependencies (Streamlit, LangChain, LangGraph, OpenAI, etc.)
- `.devcontainer/` - VS Code Dev Container configuration for development