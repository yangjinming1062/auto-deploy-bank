# Python FaaS Service Dockerfile
# Uses Deno with Pyodide for WebAssembly Python execution

FROM denoland/deno:1.45.5

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV DENO_DIR=/tmp/.deno
ENV DENO_NO_UPDATE_CHECK=1
ENV FAAS_WORKSPACE=/tmp/faas-workspace
ENV FAAS_PORT=8000
ENV FAAS_TIMEOUT=30000
ENV FAAS_LANGUAGE=python
ENV PYODIDE_VERSION=0.26.2

# Pool configuration
ENV FAAS_POOL_MIN_SIZE=2
ENV FAAS_POOL_MAX_SIZE=8
ENV FAAS_POOL_IDLE_TIMEOUT=300000
ENV FAAS_MAX_EXECUTION_TIME=30000
ENV FAAS_PRELOAD_TIMEOUT=60000

# Python packages versions
ENV NUMPY_VERSION=>=1.24.0
ENV PANDAS_VERSION=>=1.5.0
ENV JSONSCHEMA_VERSION=>=4.0.0
ENV SCIPY_VERSION=>=1.10.0
ENV SKLEARN_VERSION=>=1.3.0

WORKDIR /app

# Copy server scripts
COPY release/deployment/docker-compose/bootstrap/python-faas/deno.json ./
COPY release/deployment/docker-compose/bootstrap/python-faas/pyodide_faas_server.ts ./
COPY release/deployment/docker-compose/bootstrap/python-faas/pyodide_pool_manager.ts ./
COPY release/deployment/docker-compose/bootstrap/python-faas/entrypoint.sh ./
COPY release/deployment/docker-compose/bootstrap/python-faas/healthcheck.sh ./

# Vendor dependencies
RUN mkdir -p /tmp/faas-workspace/vendor && \
    deno vendor jsr:@eyurtsev/pyodide-sandbox@0.0.3 --output=/tmp/faas-workspace/vendor && \
    echo '{"imports":{"https://jsr.io/":"./jsr.io/"},"scopes":{"./jsr.io/":{"jsr:@eyurtsev/pyodide-sandbox@0.0.3":"./jsr.io/@eyurtsev/pyodide-sandbox/0.0.3/main.ts","jsr:@std/path@^1.0.8":"./jsr.io/@std/path/1.1.2/mod.ts","jsr:/@std/cli@^1.0.16/parse-args":"./jsr.io/@std/cli/1.0.23/parse_args.ts","jsr:@std/internal@^1.0.10/os":"./jsr.io/@std/internal/1.0.12/os.ts"}}}' > /tmp/faas-workspace/vendor/import_map.json

# Ensure scripts are executable
RUN chmod +x entrypoint.sh healthcheck.sh

# Create non-root user
RUN groupadd -r faas && useradd -r -g faas faas && \
    mkdir -p /tmp/faas-workspace && \
    chown -R faas:faas /app /tmp/faas-workspace

USER faas

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the FaaS server
CMD ["deno", "run", "--allow-net=0.0.0.0:8000", "--allow-env", "--allow-read=/app,/tmp", "--allow-write=/tmp", "--allow-run=deno", "/app/pyodide_faas_server.ts"]