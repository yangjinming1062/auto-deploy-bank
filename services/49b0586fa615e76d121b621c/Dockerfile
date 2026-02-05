FROM python:3.10-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV OMP_NUM_THREADS=1
ENV TOKENIZERS_PARALLELISM=false

WORKDIR /home/ubuntu/deploy-projects/49b0586fa615e76d121b621c

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install streamlit (required for demo)
RUN pip install --no-cache-dir streamlit==1.39.0

# Copy application code
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "demo/run_demo.py", "--server.port=8501", "--server.address=0.0.0.0"]