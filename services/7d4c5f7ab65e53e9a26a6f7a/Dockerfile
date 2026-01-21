# Dockerfile for LLM Q&A System (Alibaba Cloud ACP Course Demo)
# This container runs a Gradio-based web interface for the LLM Q&A demo

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GRADIO_PORT=7860
ENV GRADIO_HOST=0.0.0.0

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/7d4c5f7ab65e53e9a26a6f7a

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Gradio port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the application
CMD ["python", "app.py"]