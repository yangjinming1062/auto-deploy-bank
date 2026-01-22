FROM python:3.12-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/67435417998d5475c587cecb

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV JUPYTER_ALLOW_INSECURE_WRITES=1
# Disable Jupyter authentication for container environment
ENV JUPYTER_TOKEN=''

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Jupyter default port
EXPOSE 8888

# Healthcheck - check if Jupyter is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8888/api/kernelspecs || exit 1

# Start Jupyter Notebook with authentication disabled
CMD ["jupyter", "notebook", "--allow-root", "--no-browser", "--ip", "0.0.0.0", "--port", "8888", "--NotebookApp.token=''", "--NotebookApp.password=''"]