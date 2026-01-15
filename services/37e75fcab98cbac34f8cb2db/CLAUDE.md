# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Auto-evaluator** is an LLM question-answering system evaluation tool. It:
1. Auto-generates QA test sets from documents using LangChain's `QAGenerationChain`
2. Runs QA chains on the test set and uses model-graded evaluation to assess answer quality
3. Compares retrieval relevance and answer similarity scores across different configurations

## Commands

### Backend (api/)
```bash
cd api
pip install -r requirements.txt
uvicorn evaluator_app:app  # Runs on localhost:8000
```

Test API locally:
```bash
curl -X POST -F "files=@docs/karpathy-lex-pod/karpathy-pod.txt" \
  -F "num_eval_questions=1" -F "chunk_chars=1000" -F "overlap=100" \
  -F "split_method=RecursiveTextSplitter" -F "retriever_type=similarity-search" \
  -F "embeddings=OpenAI" -F "model_version=gpt-3.5-turbo" \
  -F "grade_prompt=Fast" -F "num_neighbors=3" \
  http://localhost:8000/evaluator-stream
```

### Frontend (nextjs/)
```bash
cd nextjs
yarn install
yarn dev  # Runs on localhost:3000
```

### Streamlit App (streamlit/)
```bash
cd streamlit
pip install -r requirements.txt
streamlit run auto-evaluator.py
```

## Architecture

### Backend (api/)

**`evaluator_app.py`** - Main FastAPI application:
- `/evaluator-stream` endpoint accepts multipart form data with files and config parameters
- Returns Server-Sent Events (SSE) streaming evaluation results
- Key functions:
  - `generate_eval()` - Creates QA pairs from document chunks using `QAGenerationChain`
  - `split_texts()` - Splits documents using `RecursiveCharacterTextSplitter` or `CharacterTextSplitter`
  - `make_llm()` - Factory for LLMs (OpenAI, Anthropic, Replicate, MosaicML)
  - `make_retriever()` - Creates retrievers (FAISS, SVM, TF-IDF) with specified embeddings
  - `make_chain()` - Builds `RetrievalQA` chains
  - `run_eval()` - Executes single question through chain and grades results
  - `grade_model_answer()` / `grade_model_retrieval()` - Uses `QAEvalChain` with GPT-4 for grading

**`text_utils.py`** - Prompt templates:
- `GRADE_ANSWER_PROMPT*` - Grading prompts for answer quality (Fast, Descriptive, Bias Check variants)
- `GRADE_DOCS_PROMPT*` - Grading prompts for retrieval relevance
- `QA_CHAIN_PROMPT` - Prompt for QA chain to synthesize answers from context

### Frontend (nextjs/)

**`pages/`** - Route structure:
- `index.tsx` - Demo page with pre-loaded Karpathy podcast data
- `playground/index.tsx` - Playground for custom document uploads

**`components/`**:
- `Playground.tsx` - Main experiment UI; handles file upload, form submission, SSE streaming, and results display
- `Demo.tsx` - Pre-configured demo mode
- `Sidebar.tsx` - Configuration form (chunk size, overlap, retriever, model, etc.)
- `ExperimentSummaryTable.tsx` - Results table with scoring
- `SummaryChart.tsx` - Nivo scatterplot comparing experiments

**`utils/variables.ts`**:
- `API_URL` points to backend via `NEXT_PUBLIC_API_URL` env var

### Streamlit (streamlit/)

Older Streamlit frontend with Pinecone integration for testing metadata filtering:
- `auto-evaluator.py` - Main app
- `self_query_retriever_lex.py` - Self-querying retriever example
- `kor_retriever_lex.py` - Kor schema-based filtering example

## Environment Variables

**api/.env**:
```
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

**nextjs/.env.local**:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Key Dependencies

- **LangChain** - LLM chains, retrievers, document loading
- **FastAPI + uvicorn** - Backend server with SSE support
- **Next.js + Mantine** - React frontend with UI components
- **FAISS** - Vector store for similarity search
- **OpenAI Embeddings** - Default embedding method
- **GPT-4** - Used as grader for evaluation (hardcoded in grading functions)