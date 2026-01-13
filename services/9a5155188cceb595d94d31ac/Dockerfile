# Multi-stage build for AnythingLLM
# Stage 1: Build frontend
FROM node:20-alpine AS frontend-build

WORKDIR /build/frontend

# Copy frontend package files
COPY frontend/package*.json frontend/yarn.lock ./
RUN yarn install --network-timeout 100000

# Copy and build frontend
COPY frontend/ .
RUN yarn build

# Stage 2: Build backend with all dependencies
FROM node:20-alpine

# Install system dependencies for puppeteer and other native modules
RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    freetype-dev \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    git \
    curl \
    openssl \
    python3 \
    make \
    g++ \
    && rm -rf /var/cache/apk/*

# Set Puppeteer to use system Chrome
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

WORKDIR /app

# Copy server package files and install dependencies
COPY server/package*.json server/yarn.lock ./
RUN yarn install --production --network-timeout 100000

# Copy collector package files and install dependencies
COPY collector/package*.json collector/yarn.lock ./collector/
WORKDIR /app/collector
RUN yarn install --production --network-timeout 100000
WORKDIR /app

# Copy source code
COPY server/ ./server/
COPY collector/ ./collector/

# Copy built frontend from previous stage
COPY --from=frontend-build /build/frontend/dist ./server/public

# Create storage directory
RUN mkdir -p /app/server/storage

# Set environment variables
ENV NODE_ENV=production
ENV SERVER_PORT=3001
ENV STORAGE_DIR=/app/server/storage
ENV ANYTHING_LLM_RUNTIME=docker

# Generate Prisma client before starting
RUN cd /app/server && npx -y prisma@5.3.1 generate

# Health check
HEALTHCHECK --interval=1m --timeout=10s --start-period=1m \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3001/api/ping || exit 1

# Create entrypoint script
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'set -e' >> /entrypoint.sh && \
    echo 'cd /app/server || exit 1' >> /entrypoint.sh && \
    echo 'node index.js &' >> /entrypoint.sh && \
    echo 'SERVER_PID=$!' >> /entrypoint.sh && \
    echo 'sleep 2' >> /entrypoint.sh && \
    echo 'cd /app/collector || exit 1' >> /entrypoint.sh && \
    echo 'node index.js &' >> /entrypoint.sh && \
    echo 'COLLECTOR_PID=$!' >> /entrypoint.sh && \
    echo 'echo "Started server (PID: $SERVER_PID) and collector (PID: $COLLECTOR_PID)"' >> /entrypoint.sh && \
    echo 'trap "kill $SERVER_PID $COLLECTOR_PID; exit" TERM INT' >> /entrypoint.sh && \
    echo 'wait $SERVER_PID $COLLECTOR_PID' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Start the server and collector services
CMD ["/entrypoint.sh"]