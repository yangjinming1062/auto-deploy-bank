# Multi-stage build for VectorAdmin
# This Dockerfile serves as an entry point for the full application
# Individual services use their own Dockerfiles in their respective directories

FROM ubuntu:jammy-20230522 AS base

# Install system dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
        curl gnupg python3 python3-pip tzdata netcat \
        ca-certificates fonts-liberation && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/keyrings/nodesource.list && \
    apt-get update && \
    apt-get install -yq --no-install-recommends nodejs && \
    curl -LO https://github.com/yarnpkg/yarn/releases/download/v1.22.19/yarn_1.22.19_all.deb \
        && dpkg -i yarn_1.22.19_all.deb \
        && rm yarn_1.22.19_all.deb && \
    rm -rf /var/lib/apt/lists/*

# Create application directory structure
RUN mkdir -p /app/frontend /app/backend /app/workers /app/document-processor

WORKDIR /app

# Install frontend dependencies
FROM base AS frontend-deps
COPY ./frontend/package.json ./frontend/yarn.lock ./frontend/
RUN cd ./frontend/ && yarn install --network-timeout 100000 && yarn cache clean

# Install backend dependencies
FROM base AS backend-deps
COPY ./backend/package.json ./backend/yarn.lock ./backend/
RUN cd ./backend/ && yarn install --production --network-timeout 100000 && yarn cache clean

# Build frontend
FROM frontend-deps AS build-frontend
COPY ./frontend/ ./frontend/
RUN cd ./frontend/ && yarn build && yarn cache clean

# Production stage - combines all services
FROM base AS production
COPY ./backend/ ./backend/
COPY --from=build-frontend /app/frontend/dist ./backend/public
COPY ./workers/ ./workers/
COPY ./document-processor/ ./document-processor/

# Install backend dependencies
RUN cd /app/backend && \
    yarn install --production --network-timeout 100000 && \
    yarn cache clean

# Install worker dependencies
RUN cd /app/workers && \
    yarn install --production --network-timeout 100000 && \
    yarn cache clean

# Install document-processor dependencies
RUN cd /app/document-processor && \
    python3 -m virtualenv v-env && \
    . v-env/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Setup environment
ENV NODE_ENV=production
ENV PATH=/app/document-processor/v-env/bin:$PATH

# Expose all service ports
EXPOSE 3001 3355 8888

# Use the docker entrypoint script if available
COPY ./docker/docker-entrypoint.sh /usr/local/bin/ 2>/dev/null || true
COPY ./docker/docker-healthcheck.sh /usr/local/bin/ 2>/dev/null || true
RUN chmod +x /usr/local/bin/docker-entrypoint.sh 2>/dev/null || true
RUN chmod +x /usr/local/bin/docker-healthcheck.sh 2>/dev/null || true

# Health check
HEALTHCHECK --interval=1m --timeout=10s --start-period=1m \
    CMD /usr/local/bin/docker-healthcheck.sh 2>/dev/null || exit 1

# Entry point
ENTRYPOINT ["/bin/bash", "/usr/local/bin/docker-entrypoint.sh"]