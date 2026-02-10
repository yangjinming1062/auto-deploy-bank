FROM python:3.11-slim

# Install curl for healthcheck and git for ai-data-science-team package
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/330f536198430d7c918dc156

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy requirements first for better caching
COPY 010_sql_database_agent_app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY 010_sql_database_agent_app/ .

# Copy Streamlit config
COPY .streamlit/ .streamlit/

# Copy data directory (contains northwind.db)
COPY data/ data/

# Expose the internal port
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Start the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.headless", "true"]