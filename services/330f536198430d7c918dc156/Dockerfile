FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/330f536198430d7c918dc156

# Copy requirements first for better layer caching
COPY 010_sql_database_agent_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY 010_sql_database_agent_app/ ./010_sql_database_agent_app/
COPY data/ ./data/
COPY .streamlit/ ./.streamlit/

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "010_sql_database_agent_app/app.py", "--server.port", "8501", "--server.headless", "true"]