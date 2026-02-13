FROM python:3.13-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV EXIFTOOL_PATH=/usr/bin/exiftool
ENV FFMPEG_PATH=/usr/bin/ffmpeg
ENV PORT=8080

# Install runtime dependencies and curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    exiftool \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy full source for build
COPY packages/markitdown packages/markitdown
COPY packages/markitdown-mcp packages/markitdown-mcp

# Install markitdown package with all dependencies
RUN pip install --no-cache-dir \
    -e /app/packages/markitdown[all] \
    -e /app/packages/markitdown-mcp

# Install MCP server dependencies and Flask for web service
RUN pip install --no-cache-dir mcp starlette uvicorn flask

# Default USERID and GROUPID
ARG USERID=nobody
ARG GROUPID=nogroup

COPY . .

# Set ownership for the application directory
RUN chown -R $USERID:$GROUPID /app

USER $USERID:$GROUPID

EXPOSE 8080

# Health check - verify Flask service is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run Flask web service on port 8080
CMD ["python", "app.py"]