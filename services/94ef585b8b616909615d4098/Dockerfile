FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV PATH="$POETRY_VENV/bin:$PATH"

# Install system dependencies
ENV PROTOBUF_VERSION=3.19.4
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install protobuf compiler
RUN wget -O /tmp/protoc.zip https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOBUF_VERSION}/protoc-${PROTOBUF_VERSION}-linux-x86_64.zip && \
    unzip /tmp/protoc.zip -d /usr/local && \
    chmod -R a+rx /usr/local/bin/protoc /usr/local/include/google

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION && \
    mkdir -p $POETRY_VENV

# Set work directory
WORKDIR /app

# Copy project files
COPY python/pyproject.toml python/poetry.lock python/DESCRIPTION.md ./

# Configure Poetry environment and install dependencies
RUN $POETRY_HOME/bin/poetry env use python3 && \
    $POETRY_HOME/bin/poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application
COPY service.py ./
COPY python/whylogs ./whylogs
COPY proto ./proto

# Generate protobuf Python files
RUN /usr/local/bin/protoc -I proto/src --python_out=./whylogs/core/proto proto/src/whylogs_messages.proto && \
    /usr/local/bin/protoc -I proto/v0 --python_out=./whylogs/core/proto/v0 proto/v0/*.proto && \
    $POETRY_HOME/bin/poetry run 2to3 --nobackups --write ./whylogs/core/proto/v0/

# Build whylogs package
RUN $POETRY_HOME/bin/poetry build

# Install service dependencies
RUN $POETRY_HOME/bin/poetry run pip install uvicorn fastapi scikit-learn pandas numpy

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the service
CMD ["/opt/poetry/bin/poetry", "run", "uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]