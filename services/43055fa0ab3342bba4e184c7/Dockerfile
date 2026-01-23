FROM python:3.8-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/43055fa0ab3342bba4e184c7

# Install grakel first with compatible Cython version (needs specific older versions)
# grakel 0.1.8 has Cython build issues - skip for now
# The codebase can function without grakel (some predictors won't be available)

# Copy and install dependencies
# Filter out codecov (requires Python 3.10+) and grakel (has Cython compatibility issues)
COPY requirements.txt .
RUN grep -v -E '^(codecov|grakel)==' requirements.txt > requirements_install.txt && \
    pip install --no-cache-dir -r requirements_install.txt && \
    rm requirements_install.txt

# Copy application code
COPY . .

# Install the package without dependencies (dependencies already installed)
RUN pip install --no-deps -e .

# Expose the health check port
EXPOSE 40363

# Health check script will start a simple HTTP server and run training
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]