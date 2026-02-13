# GraphRAG Unified Search App Dockerfile
FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/19c45fb8b7737bd9928f575f

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="${PATH}:/root/.local/bin"

# Copy dependency files first for better caching
COPY unified-search-app/pyproject.toml unified-search-app/uv.lock ./

# Sync dependencies without installing the project
RUN uv sync --no-install-project

# Copy application code
COPY unified-search-app/. ./unified-search-app/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_APP_HOME=/home/ubuntu/deploy-projects/19c45fb8b7737bd9928f575f/unified-search-app

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit application
WORKDIR /home/ubuntu/deploy-projects/19c45fb8b7737bd9928f575f/unified-search-app
CMD ["uv", "run", "streamlit", "run", "app/home_page.py", "--server.port", "8501", "--server.address", "0.0.0.0"]