FROM python:3.10-slim

# Install curl and git (required for pip install from git)
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/root/.cache/huggingface
ENV TRANSFORMERS_CACHE=./

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/afa55d93bacd8f3f83837ef4

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY webui ./webui
COPY modeling_chatglm.py ./webui/
COPY tokenization_chatglm.py ./webui/
COPY configuration_chatglm.py ./webui/

# Expose internal port
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
WORKDIR /home/ubuntu/deploy-projects/afa55d93bacd8f3f83837ef4/webui
CMD ["streamlit", "run", "web_feadback.py", "--server.port", "8501", "--server.headless", "true"]