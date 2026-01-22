FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY scenarios/Assistants/bfsi-bot-in-a-box/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir 'httpx>=0.25.0,<1' 'openai>=1.25.0'

# Copy application code
COPY scenarios/Assistants/bfsi-bot-in-a-box/src/backend/ ./src/backend/
COPY entrypoint.sh /entrypoint.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the internal port (Flask default 5007)
EXPOSE 5007

# Make entrypoint executable
RUN chmod +x /entrypoint.sh

# Change to the backend directory and run the app
WORKDIR /app/src/backend
CMD ["/entrypoint.sh"]