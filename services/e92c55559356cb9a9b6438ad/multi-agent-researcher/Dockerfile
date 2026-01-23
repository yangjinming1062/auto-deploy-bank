FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/e92c55559356cb9a9b6438ad

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY multi_agent_researcher.py .

# Expose Streamlit port
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Start Streamlit application
CMD ["streamlit", "run", "multi_agent_researcher.py", "--server.port=8501", "--server.address=0.0.0.0"]