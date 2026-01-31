# Build stage
FROM node:20-slim AS builder

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# Copy monorepo configuration files
COPY pnpm-workspace.yaml ./
COPY package.json pnpm-lock.yaml ./

# Copy all packages (including website)
COPY packages/ ./packages/
COPY scripts/ ./scripts/
COPY website/ ./website/

# Install dependencies (skip prepare hook)
RUN pnpm install --frozen-lockfile --ignore-scripts

# Create symlink for @rspress/config from scripts/config
RUN mkdir -p /app/node_modules/@rspress && ln -sf /app/scripts/config /app/node_modules/@rspress/config && \
    mkdir -p /app/node_modules/@rspress/config/tsconfig && \
    cp /app/node_modules/@rspress/config/tsconfig.json /app/node_modules/@rspress/config/tsconfig/tsconfig.json

# Build all packages first (excluding website) - needed by the website
RUN pnpm --filter '@rspress/*' --filter '!@rspress/docs' run build

# Build the website
WORKDIR /app/website
RUN pnpm run build

# Production stage - serve static files
FROM node:20-slim

# Install serve and wget for healthcheck
RUN npm install -g serve && apt-get update && apt-get install -y --no-install-recommends wget && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy built artifacts from builder
COPY --from=builder /app/website/doc_build ./doc_build

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose the port
EXPOSE 3000

# Run serve to serve static files in foreground
CMD ["serve", "-p", "3000", "-s", "doc_build", "--no-clipboard"]