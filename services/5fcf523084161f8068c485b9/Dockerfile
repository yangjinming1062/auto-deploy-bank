FROM python:3.10-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy application code first
COPY . .

# Install Python dependencies from pyproject.toml
RUN pip install --no-cache-dir -e .

# Install FastAPI and dependencies
RUN pip install --no-cache-dir fastapi uvicorn[standard] python-multipart python-dotenv

# Expose port 54039
EXPOSE 54039

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:54039/ || exit 1

# Run the simple service
CMD ["python", "service.py"]