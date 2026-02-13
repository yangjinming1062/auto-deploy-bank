# Copyright (c) Microsoft. All rights reserved.

FROM python:3.12-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy pyproject.toml first for dependency installation (better layer caching)
COPY pyproject.toml ./

# Install flit and build the package
RUN pip install flit-core>=3.9,<4.0
RUN flit install --deps production --symlink

# Copy remaining source code
COPY semantic_kernel ./semantic_kernel
COPY samples ./samples

# Expose internal port
EXPOSE 5001

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Run the FastAPI service using uvicorn
CMD ["uvicorn", "samples.demos.service.main:app", "--host", "0.0.0.0", "--port", "5001"]