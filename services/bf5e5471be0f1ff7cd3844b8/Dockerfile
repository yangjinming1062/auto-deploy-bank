FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck, procps for health checks, and build dependencies for cryptography package
RUN apt-get update && apt-get install -y curl procps default-mysql-client build-essential libssl-dev libffi-dev python3-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make startup script executable (must be after COPY . to preserve permissions)
RUN chmod +x /app/start.sh

# Create .env file with default values if not exists
RUN if [ ! -f .env ]; then \
    echo "# Environment variables" > .env && \
    echo "OPENAI_API_KEY=" >> .env && \
    echo "MYSQL_HOST=mysql" >> .env && \
    echo "MYSQL_USER=root" >> .env && \
    echo "MYSQL_PASSWORD=rootpassword" >> .env && \
    echo "MYSQL_PORT=3306" >> .env && \
    echo "USE_AZURE=False" >> .env && \
    echo "TEMPERATURE=0" >> .env && \
    echo "FAST_LLM_MODEL=gpt-3.5-turbo" >> .env && \
    echo "SMART_LLM_MODEL=gpt-4" >> .env && \
    echo "FAST_TOKEN_LIMIT=4096" >> .env && \
    echo "SMART_TOKEN_LIMIT=8000" >> .env; \
fi

CMD ["/app/start.sh"]