FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for healthcheck and general usage
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:40437/health || exit 1

# Expose port
EXPOSE 40437

# Run the application
CMD ["python", "-m", "uvicorn", "web_api:app", "--host", "0.0.0.0", "--port", "40437"]