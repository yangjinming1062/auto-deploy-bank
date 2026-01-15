# Copyright (C) 2020-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

FROM python:3.8-slim

WORKDIR /home/ubuntu/deploy-projects/577452c99e3aa86844b69d5e

ENV PYTHONUNBUFFERED=1
ENV GRPC_VERBOSITY=INFO
ENV TF_CPP_MIN_LOG_LEVEL=2
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package in development mode
RUN pip install -e .

EXPOSE 50051

# Generate certificates and start aggregator
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]