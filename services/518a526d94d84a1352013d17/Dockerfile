FROM python:3.12-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/518a526d94d84a1352013d17

# Copy requirements first for better caching
COPY server/requirements.txt server/

# Install Python dependencies
RUN pip install --no-cache-dir -r server/requirements.txt

# Copy entire project
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEFAULT_PORT=57988
ENV UI_DIST_DIR=/home/ubuntu/deploy-projects/518a526d94d84a1352013d17/react/dist
ENV PYTHONPATH=/home/ubuntu/deploy-projects/518a526d94d84a1352013d17/server:$PYTHONPATH

# Expose the port
EXPOSE 57988

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:57988/ || exit 1

# Run the application using uvicorn from the server directory
CMD ["uvicorn", "server.main:socket_app", "--host", "0.0.0.0", "--port", "57988"]