# Streamlit SQL Database Agent App
FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/330f536198430d7c918dc156

# Copy requirements first for better caching
COPY 010_sql_database_agent_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY 010_sql_database_agent_app/ .
COPY data ./data
COPY .streamlit ./streamlit

# Expose the Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]