FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies required by the project
RUN pip install --no-cache-dir faiss-cpu funasr==1.0.24 modelscope

# Copy application code
COPY . .

# Expose Gradio port
EXPOSE 7860

# Run the web application
CMD ["python", "webui.py"]