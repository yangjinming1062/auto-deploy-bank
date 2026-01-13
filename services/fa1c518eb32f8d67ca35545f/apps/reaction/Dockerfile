# Dockerfile for Reaction Commerce API
FROM node:20-slim

# Install dependencies needed for pnpm and git
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install pnpm
RUN npm install -g pnpm@8.15.1

WORKDIR /usr/local/src/app

# Copy workspace configuration
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

# Copy all source code before installing
COPY apps ./apps
COPY packages ./packages

# Install dependencies
RUN pnpm install --no-frozen-lockfile

# Build packages if needed
RUN pnpm run build:packages

# Create non-root user and required directories
RUN groupadd -g 1001 nodejs && \
    useradd -u 1001 -g nodejs -m -s /bin/bash reaction && \
    mkdir -p /usr/local/src/app/uploads /usr/local/src/app/public && \
    chown -R reaction:nodejs /usr/local/src/app/uploads /usr/local/src/app/public

USER reaction

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

# Use tini to handle signals properly
# Note: tini is already installed in node:20-slim
CMD ["node", "./apps/reaction/src/index.js"]
