FROM python:3.12-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LANGSMITH_TRACING=true

# Copy requirements and install dependencies
COPY requirements-demo.txt .
RUN pip install --no-cache-dir -r requirements-demo.txt

# Copy the langsmith package source (install in editable mode)
COPY pyproject.toml .
COPY README.md .
COPY langsmith/ ./langsmith/
# Install the langsmith package in editable mode
RUN pip install -e .

# Copy the demo application
COPY demo_app.py .

# Expose the internal port
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the demo application
CMD ["python", "demo_app.py"]