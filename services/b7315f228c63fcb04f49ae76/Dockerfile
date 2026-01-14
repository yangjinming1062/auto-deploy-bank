# Multi-stage build for Master Password CLI with HTTP API
# Stage 1: Build the mpw CLI tool
FROM alpine:3.18 AS builder

WORKDIR /build

# Install build dependencies
RUN apk add --no-cache \
    bash \
    gcc \
    musl-dev \
    libsodium-dev \
    libxml2-dev \
    make

# Copy build files with correct structure
COPY platform-independent/c/cli/build ./cli/build
COPY platform-independent/c/core/src ./core/src
COPY platform-independent/c/cli/src ./cli/src

# Build mpw CLI using direct compilation
# Working from /build directory, paths are relative to cli/
RUN cd cli && \
    gcc -O3 \
        -D"MP_VERSION=2.7.11" \
        -I"../core/src" -I"src" \
        -D"MPW_SODIUM=1" \
        "../core/src/base64.c" "../core/src/aes.c" "../core/src/mpw-algorithm.c" \
        "../core/src/mpw-algorithm_v0.c" "../core/src/mpw-algorithm_v1.c" "../core/src/mpw-algorithm_v2.c" "../core/src/mpw-algorithm_v3.c" \
        "../core/src/mpw-types.c" "../core/src/mpw-util.c" "../core/src/mpw-marshal-util.c" "../core/src/mpw-marshal.c" "src/mpw-cli-util.c" \
        "src/mpw-cli.c" \
        -lsodium -o "mpw"

# Stage 2: Runtime image with HTTP API
FROM alpine:3.18

# Install runtime dependencies
RUN apk add --no-cache \
    bash \
    python3 \
    libsodium \
    libxml2 \
    ncurses \
    json-c

# Create non-root user for security
RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -s /bin/bash -D appuser

# Copy the built binary from builder stage
COPY --from=builder /build/cli/mpw /usr/local/bin/mpw

# Copy compiled binary for security scanning (as target.jar)
COPY --from=builder /build/cli/mpw /app/target.jar

# Copy the HTTP wrapper script
COPY --chmod=755 mpw-http.py /usr/local/bin/mpw-http.py

# Set working directory
WORKDIR /home/appuser

# Create mpw.d directory for user configuration
RUN mkdir -p /home/appuser/.mpw.d && chown -R appuser:appgroup /home/appuser

# Switch to non-root user
USER appuser

# Set environment variables
ENV MPW_RCDIR=/home/appuser/.mpw.d
ENV MPW_ALGORITHM=v3
ENV MPW_PORT=8080
ENV HOME=/home/appuser

# Expose the HTTP port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# Default command: start HTTP server
CMD ["python3", "/usr/local/bin/mpw-http.py"]