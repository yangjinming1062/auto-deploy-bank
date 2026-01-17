# Dockerfile for llm-apps-course Gradio application
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/97325efb8a24cd5e89597bd5

# Copy and install dependencies
COPY llm-apps-course/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY llm-apps-course/src ./llm-apps-course/src

# Copy patch_wandb.py for test mode
COPY patch_wandb.py /home/ubuntu/deploy-projects/97325efb8a24cd5e89597bd5/

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the Gradio port (default 8884)
EXPOSE 8884

# Run the Gradio app
ENTRYPOINT ["/entrypoint.sh"]