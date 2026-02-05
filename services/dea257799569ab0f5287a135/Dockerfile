FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/dea257799569ab0f5287a135

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy all files needed for package installation
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir -e .

# Copy application code (keep agentflow directory structure)
COPY agentflow/ agentflow/

# Expose the internal port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/task || exit 1

# Start command
CMD ["python", "-c", "from agentflow.server import AgentFlowServer; import asyncio; asyncio.run(AgentFlowServer(host='0.0.0.0', port=8000).run_forever())"]