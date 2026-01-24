FROM python:3.11-slim

WORKDIR /home/ubuntu/deploy-projects/c4665093af648861ae72bb17

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy requirements and install dependencies
COPY AgentGraph-Intelligent-Q&A-and-RAG-System/requirements.txt /tmp/requirements.txt
# Remove gradio line from requirements to install compatible version
RUN grep -v "^gradio==" /tmp/requirements.txt > /tmp/requirements_clean.txt && \
    pip install --no-cache-dir -r /tmp/requirements_clean.txt
# Install compatible gradio version with huggingface_hub that has HfFolder
RUN pip install --no-cache-dir "gradio==4.43.0" "huggingface_hub==0.23.5" "httpx<0.28.0"

# Copy application code
COPY AgentGraph-Intelligent-Q&A-and-RAG-System/ .

# Expose Gradio port
EXPOSE 7860

# Start the application
CMD ["python", "src/app.py"]