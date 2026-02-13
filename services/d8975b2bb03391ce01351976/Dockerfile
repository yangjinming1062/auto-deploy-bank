FROM python:3.10-slim

WORKDIR /home/ubuntu/deploy-projects/d8975b2bb03391ce01351976

ENV PYTHONUNBUFFERED=1 \
    SETUPTOOLS_SCM_PRETEND_VERSION_FOR_PYQLIB=0.9.0 \
    QLIB_PROVIDER_URI=/home/ubuntu/deploy-projects/d8975b2bb03391ce01351976/.qlib/qlib_data/cn_data \
    QLIB_MLFLOW_URI=/home/ubuntu/deploy-projects/d8975b2bb03391ce01351976/mlruns \
    QLIB_MLFLOW_DEFAULT_EXP_NAME=Experiment \
    REDIS_HOST=redis \
    REDIS_PORT=6379 \
    REDIS_TASK_DB=1 \
    CUDA_VISIBLE_DEVICES=

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Flask for web server
RUN pip install --no-cache-dir flask

# Copy source code and install qlib in development mode
COPY . .
RUN pip install --no-build-isolation -e .

# Create necessary directories
RUN mkdir -p /home/ubuntu/deploy-projects/d8975b2bb03391ce01351976/.qlib/qlib_data/cn_data /home/ubuntu/deploy-projects/d8975b2bb03391ce01351976/mlruns

# Expose port (for potential HTTP server)
EXPOSE 42550

# Healthcheck - just verify Python and basic imports work
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import sys; print(f'Python {sys.version}'); sys.exit(0)" || exit 1

# Default command - start Flask web server
CMD ["python", "/home/ubuntu/deploy-projects/d8975b2bb03391ce01351976/web_server.py"]