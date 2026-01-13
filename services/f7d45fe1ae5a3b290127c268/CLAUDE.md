# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Backend (Python)

- **Install dependencies:** `poetry install -E extra_proxy -E proxy`
- **Run tests:** `cd tests && poetry run pytest .`
- **Linting:** `poetry run flake8` and `poetry run mypy`
- **Run the proxy server:** `uvicorn litellm.proxy.proxy_server:app --host localhost --port 4000 --reload`

### Frontend (Next.js)

- **Navigate to UI directory:** `cd ui/litellm-dashboard`
- **Install dependencies:** `npm install`
- **Run the dev server:** `npm run dev`
- **Build the UI:** `npm run build`
- **Lint the UI:** `npm run lint`

### Docker

- **Build Docker image:** `docker build -f docker/Dockerfile.non_root -t litellm_test_image .`
- **Run Docker image:**
```bash
docker run \
    -v $(pwd)/proxy_config.yaml:/app/config.yaml \
    -e DATABASE_URL="postgresql://xxxxxxxx" \
    -e LITELLM_MASTER_KEY="sk-1234" \
    -p 4000:4000 \
    litellm_test_image \
    --config /app/config.yaml --detailed_debug
```

## High-level Architecture

- **LiteLLM** is a Python library that provides a unified interface for interacting with various Large Language Model (LLM) APIs.
- The project consists of a **Python backend** that acts as a proxy to different LLM providers and a **Next.js frontend** for a user dashboard.
- The backend is built with **FastAPI** and uses **Poetry** for dependency management.
- The frontend is located in the `ui/litellm-dashboard` directory and is built with **Next.js** and **Tailwind CSS**.
- Configuration is managed through a `config.yaml` file.
- The application can be connected to a **PostgreSQL** database for API key management and other features.
- The `litellm` directory contains the core Python library, while the `litellm/proxy` directory contains the proxy server implementation.
