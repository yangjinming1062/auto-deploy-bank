# Moon Dev AI Trading System Dockerfile
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    gcc \
    g++ \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy requirements first for better caching
COPY requirements-fastapi.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-fastapi.txt

# Copy application code
COPY . .

# Create required directories for dashboard
RUN mkdir -p /app/src/data/rbi_pp_multi/static /app/src/data/rbi_pp_multi/templates

# Expose port 8002 (backtest dashboard)
EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8002/ || exit 1

# Run the backtest dashboard on port 8002
CMD ["uvicorn", "src.scripts.backtestdashboard:app", "--host", "0.0.0.0", "--port", "8002"]