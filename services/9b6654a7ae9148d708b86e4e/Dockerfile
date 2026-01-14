FROM public.ecr.aws/docker/library/python:3.12-slim

# Set working directory
WORKDIR /app

# Install curl for healthcheck and other utilities
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create non-root user for security
RUN useradd -m -u 1000 bedrock_agentcore
USER bedrock_agentcore

# Expose the internal port
EXPOSE 8080

# Copy application code
COPY main.py .
COPY .env.example .env.example
COPY pyproject.toml .
COPY .bedrock_agentcore.yaml .
COPY create_user_account.py .

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application
CMD ["python", "main.py"]