# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

# OpenContext Dockerfile
# Build: docker build -t opencontext .
# Run: docker run -p 1733:1733 opencontext

FROM python:3.12-slim

# Install system dependencies for Python packages (playwright, image processing, etc.)
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxcb1 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM=1

# Set work directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY config ./config

# Install dependencies using uv
RUN pip install --no-cache-dir uv && \
    uv sync

# Copy remaining application files
COPY opencontext ./opencontext
COPY build.sh .

# Expose the application port
EXPOSE 1733

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:1733/health || exit 1

# Run the application
CMD ["uv", "run", "opencontext", "start", "--port", "1733", "--host", "0.0.0.0"]