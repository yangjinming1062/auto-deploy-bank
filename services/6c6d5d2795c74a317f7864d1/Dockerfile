FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV SETUPTOOLS_SCM_PRETEND_VERSION_FOR_OUTLINES=0.0.0

# Set working directory
WORKDIR /app

# Copy the source code first
COPY outlines/ ./outlines/
COPY pyproject.toml .
COPY healthcheck.py .

# Install the package in development mode
RUN pip install --no-cache-dir -e .

# Expose port 41214 (for consistency with service requirements)
EXPOSE 41214

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:41214/health || exit 1

# Run health check server
CMD ["python", "healthcheck.py"]