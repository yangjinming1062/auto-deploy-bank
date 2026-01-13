# Simplified Dockerfile for server with pre-built dist
FROM node:22-alpine

WORKDIR /app

# Install system dependencies for native modules like bcrypt
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    curl

# Copy package files
COPY package.json yarn.lock ./
COPY lerna.json ./
COPY .yarnrc ./
COPY nx.json ./
COPY tsconfig.build.json ./
COPY babel.config.json ./
COPY packages/server/package.json packages/server/
COPY packages/worker/package.json packages/worker/
COPY packages/backend-core/package.json packages/backend-core/
COPY packages/shared-core/package.json packages/shared-core/
COPY packages/types/package.json packages/types/

# Install dependencies
RUN yarn install

# Copy the pre-built dist directory and client files
COPY packages/server/dist ./packages/server/dist
COPY packages/server/builder ./packages/server/builder
COPY packages/worker/dist ./packages/worker/dist

# Create symlink for builder assets (required by server)
RUN ln -sf /app/packages/server/builder /app/builder

# Create a non-root user
RUN addgroup -g 1001 -S budibase && \
    adduser -S budibase -u 1001

WORKDIR /app/packages/server

USER budibase

# Expose the internal port
EXPOSE 4001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:4001/health || exit 1

# Start the server
CMD ["node", "--enable-source-maps", "dist/index.js"]