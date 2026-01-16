FROM python:3.11-slim

# Install curl and Java JDK (required by pyserini/jnius)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl default-jdk-headless && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install FastAPI and uvicorn for the server
RUN pip install --no-cache-dir fastapi uvicorn

# Copy application code
COPY . .

# Install the package
RUN pip install --no-cache-dir -e .

# Expose internal port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run the server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]