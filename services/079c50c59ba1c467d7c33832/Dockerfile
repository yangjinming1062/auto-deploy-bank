# SeedVR2.3B Video Super-Resolution Service
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CUDA_MODULE_LOADING=LAZY

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for web server and CUDA
RUN pip install --no-cache-dir flask gunicorn

# Copy application code
COPY . .

# Create directories for input/output
RUN mkdir -p /app/input /app/output

# Expose port
EXPOSE 40110

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:40110/health || exit 1

# Run the web server with gunicorn for production
CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:40110", "--workers", "1", "--timeout", "300"]