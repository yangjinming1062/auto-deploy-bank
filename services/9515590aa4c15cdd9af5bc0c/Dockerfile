# TensorFlow.js Dockerfile
# Note: Full Bazel builds require glibc and complex setup, using simplified container for service

FROM node:20

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    make \
    g++ \
    git \
    ca-certificates \
    unzip \
    zip \
    tar \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy package files first for better caching
COPY package.json yarn.lock ./
COPY tfjs/package.json ./tfjs/
COPY link-package/package.json ./link-package/

# Install Node dependencies
RUN yarn install --frozen-lockfile

# Copy source code
COPY . .

# Copy health check server script
COPY healthcheck.js ./

# Set environment variables
ENV NODE_ENV=production
ENV PORT=8100

# Expose the port
EXPOSE 8100

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:8100/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1)).on('error', () => process.exit(1))"

# Start the service
CMD ["node", "healthcheck.js"]