# Multi-stage build for FIND3 Indoor Positioning System
# docker build -t find3 .
# docker run -p 40658:8003 -v /tmp/find3:/data -t find3

# ========================================
# Stage 1: Build Go application
# ========================================
FROM golang:1.21-bullseye AS go-builder

WORKDIR /build

# Copy source code first (includes go.mod)
COPY . .

# Generate go.sum and download dependencies
# Use GOFLAGS to allow automatic toolchain selection
ENV GOFLAGS=-mod=mod
RUN go mod tidy 2>/dev/null || true

# Build the Go applications with CGO enabled for SQLite support
ENV CGO_ENABLED=1
ENV GO111MODULE=on
RUN go build -o /build/find3-server ./server/main
RUN go build -o /build/find3-docs .

# ========================================
# Stage 2: Build Python AI server
# ========================================
FROM python:3.10-slim AS ai-builder

WORKDIR /build

# Copy requirements and install Python dependencies
COPY server/ai/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy AI server source code
COPY server/ai/ /build/ai/

# ========================================
# Stage 3: Final combined runtime with supervisord
# ========================================
FROM ubuntu:22.04 AS runtime

WORKDIR /app

# Install necessary packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    libsqlite3-0 \
    curl \
    python3 \
    python3-pip \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy Go binaries from builder stage and set execute permissions
COPY --from=go-builder /build/find3-server /app/find3-server
COPY --from=go-builder /build/find3-docs /app/find3-docs
RUN chmod +x /app/find3-server /app/find3-docs

# Copy web templates and static files
COPY --from=go-builder /build/server/main/templates /app/templates
COPY --from=go-builder /build/server/main/static /app/static

# Copy documentation files
COPY --from=go-builder /build/doc /app/doc

# Install Python AI server dependencies
COPY --from=ai-builder /build/ai /app/ai
COPY server/ai/requirements.txt /tmp/ai-requirements.txt
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r /tmp/ai-requirements.txt && \
    rm /tmp/ai-requirements.txt

# Create data directory
RUN mkdir -p /app/data

# Copy supervisord configuration
COPY <<'EOF' /etc/supervisor/conf.d/find3.conf
[supervisord]
nodaemon=true
user=root
logfile=/app/supervisor.log
pidfile=/app/supervisor.pid

[program:find3-ai]
command=/usr/bin/python3 server.py
directory=/app/ai/src
autostart=true
autorestart=true
stdout_logfile=/app/ai-server.log
stderr_logfile=/app/ai-server-error.log

[program:find3-main]
command=/bin/sh -c 'if [ "${FIND3_DEBUG}" = "true" ]; then /app/find3-server -debug -data /app/data -port 8003 -ai 8002; else /app/find3-server -data /app/data -port 8003 -ai 8002; fi'
directory=/app
autostart=true
autorestart=true
stdout_logfile=/app/main-server.log
stderr_logfile=/app/main-server-error.log

[program:find3-docs]
command=/app/find3-docs
directory=/app
autostart=true
autorestart=true
stdout_logfile=/app/docs-server.log
stderr_logfile=/app/docs-server-error.log
EOF

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8003/ || exit 1

# Expose main server port
EXPOSE 8003

# Start both services with supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/find3.conf"]