# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A collection of **LangChain-powered Streamlit micro-apps**. Each app demonstrates a different LLM use case (search, summarization, Q&A) and is self-contained with its own dependencies.

## Architecture

**Two app patterns exist:**

1. **Standalone apps** - Single-file apps (`<app-dir>/streamlit_app.py`) for isolated demos
2. **All-in-one app** (`all-in-one/`) - Multi-page Streamlit app combining multiple use cases using `st.pages()` pattern. Entry point is `Home.py` with additional pages in the `pages/` subdirectory.

All apps share common patterns: sidebar configuration, session state caching, spinner-based loading, and success/error output.

## Commands

```bash
cd <app-directory>
pip install -r requirements.txt  # Per-app dependencies
streamlit run streamlit_app.py   # Or streamlit run Home.py for all-in-one
```

## Common App Patterns

**API key input**: Sidebar with `st.text_input(..., type="password")`

**Session state caching** (for vector stores/documents):
```python
if 'retriever' not in st.session_state:
    st.session_state.retriever = None
```

**Pattern for document-based apps**:
1. Upload file → save to temp file
2. Load with `PyPDFLoader` or `UnstructuredLoader`
3. Create embeddings (`OpenAIEmbeddings`)
4. Store in vector DB (`Chroma`, `Pinecone`)
5. Run chain (`load_summarize_chain`, `RetrievalQA`)

**Pattern for agent-based apps**:
```python
llm = ChatOpenAI(temperature=0, openai_api_key=api_key, verbose=True)
tools = load_tools(["google-serper"], llm, serper_api_key=api_key)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
result = agent.run(query)
```

## Key Dependencies

- `streamlit==1.33.0` - UI framework
- `langchain==0.1.19` - Core framework
- `langchain-openai==0.1.6` - OpenAI integration
- `langchain-chroma==0.1.0`, `langchain-community==0.0.38` - Vector stores and utilities
- `pypdf==4.2.0`, `unstructured==0.13.7` - Document loaders
- `google-search-results==2.4.2` - SerpApi/Serper for search
- `pdf2image==1.17.0`, `pytesseract==0.3.10` - OCR for PDFs

## Required API Keys

- **OpenAI** (`OPENAI_API_KEY`) - Most apps
- **Serper** (`serper.dev`) - Search/news apps
- **Pinecone** - Vector database apps
- **Google Gemini** (`GOOGLE_API_KEY`) - Gemini apps
- **Helicone** (`HELICONE_API_KEY`) - Observability demo

## Deployment

Apps are configured for Railway deployment via `railway.json` using Nixpacks builder. Each app directory can be deployed independently.