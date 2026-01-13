# Stage 1: Build the virtual environment
FROM python:3.9 as builder

# Install system dependencies needed for lxml and other packages
RUN apt-get update && apt-get install -y curl build-essential libxml2-dev libxslt-dev && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry==1.7.1

# Configure poetry to create the virtualenv in the project's root
WORKDIR /app
RUN poetry config virtualenvs.in-project true

# Copy dependency files and install them into the virtualenv
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Stage 2: Create the final application image
FROM python:3.9-slim

WORKDIR /app

# Copy the virtualenv from the builder stage
COPY --from=builder /app/.venv ./.venv

# Copy the application code
COPY griptape/ griptape/
COPY app/ app/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Expose the internal port
EXPOSE 8000
