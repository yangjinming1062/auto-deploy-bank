FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ZENML_CONTAINER=1

# Set work directory
WORKDIR /zenml

# Install uv
RUN pip install uv

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy dependency files
COPY pyproject.toml ./

# Copy __init__.py file first to allow package discovery
COPY src/zenml/__init__.py ./src/zenml/

# Copy entire source
COPY . .

# Install dependencies and application
RUN /opt/venv/bin/pip install --upgrade pip setuptools && \
    /opt/venv/bin/pip install .[server] && \
    /opt/venv/bin/pip install -e . && \
    /opt/venv/bin/pip freeze > requirements.txt

# Create symbolic link for dashboard files
RUN ln -s /zenml/src/zenml/deployers/server/dashboard /zenml/src/zenml/zen_server/dashboard

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "zenml.zen_server.zen_server_api:app", "--host", "0.0.0.0", "--port", "8000"]