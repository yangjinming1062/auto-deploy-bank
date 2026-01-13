FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies including curl for healthcheck and SQLite3 dev headers for pysqlite3
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Install the package in editable mode
RUN pip install -e .

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose the internal port
EXPOSE 8079

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8079/docs || exit 1

# Run the FastAPI server
CMD ["uvicorn", "oscopilot.tool_repository.manager.api_server:app", "--host", "0.0.0.0", "--port", "8079"]