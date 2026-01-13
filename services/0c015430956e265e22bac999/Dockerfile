FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy project files - use app/api dependencies
WORKDIR /app
COPY agentops /app/agentops
COPY app /app/app
# Copy jockey next to pyproject.toml (in same directory)
RUN cp -r /app/app/deploy/jockey /app/

# Create requirements.txt with all dependencies
RUN echo "fastapi>=0.110.0\nuvicorn[standard]>=0.27.0\nhttpx>=0.27.0\npython-dotenv>=1.0.0\nWerkzeug>=3.0.3\ntokencost>=0.1.26\nsentry-sdk>=1.39.1\njsonschema\npyjwt>=2.8.0\ntermcolor>=2.0.0\nuvloop>=0.19.0\nhttpcore>=1.0.5\nsupabase>=2.12.0\nopentelemetry-semantic-conventions>=0.43b0\nopentelemetry-semantic-conventions-ai>=0.4.2\nclickhouse-connect>=0.8.15\nclickhouse-driver>=0.2.9\ndotenv>=0.9.9\nopentelemetry-api==1.29.0\nopentelemetry-sdk==1.29.0\npsycopg-pool>=3.2.6\npsycopg[binary]>=3.2.5\npydantic>=2.10.6\nboto3>=1.37.22\nredis>=5.2.1\njinja2>=3.1.6\nsqlalchemy>=2.0.40\ngreenlet>=3.1.1\nstripe\ngotrue>=2.12.4\npsutil>=5.9.8\nrequests>=2.0.0\nPyYAML>=5.3\npackaging>=21.0\nhttpx>=0.24.0\naiohttp>=3.8.0\nopentelemetry-exporter-otlp-proto-http==1.29.0\nordered-set>=4.0.0\nwrapt>=1.0.0\nopentelemetry-instrumentation==0.50b0\nopentelemetry-semantic-conventions==0.50b0\n" > /app/requirements.txt

# Create virtual environment and install all dependencies using uv
RUN bash -c "uv venv && . .venv/bin/activate && uv pip install -r /app/requirements.txt --default-index https://pypi.org/simple/"

# Set the module path for uvicorn
ENV PYTHONPATH=/app
WORKDIR /app

# Expose port 8000
EXPOSE 8000

# Start the FastAPI application
CMD ["uv", "run", "uvicorn", "app.api.agentops.app:app", "--host", "0.0.0.0", "--port", "8000"]