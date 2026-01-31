FROM node:22-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache python3 make g++ build-base autoconf automake libtool pkgconfig git

# Install pnpm
RUN corepack enable && corepack prepare pnpm@9.10.0 --activate

# Copy root pnpm files
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml ./

# Copy package configuration files
COPY turbo.json ./
COPY tsconfig.json ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Build required packages with error suppression
RUN cd multimodal && pnpm install --frozen-lockfile --ignore-scripts && \
    (cd gui-agent/shared && pnpm run build 2>&1 || true) && \
    (cd gui-agent/action-parser && pnpm run build 2>&1 || true) && \
    (cd gui-agent/agent-sdk && pnpm run build 2>&1 || true) && \
    (cd gui-agent/operator-aio && pnpm run build 2>&1 || true) && \
    (cd gui-agent/operator-browser && pnpm run build 2>&1 || true) && \
    (pnpm run build:omni-tars 2>&1 || true) && \
    (cd omni-tars/omni-agent && pnpm run build 2>&1 || true)

FROM node:22-alpine AS runtime

WORKDIR /app

# Install runtime dependencies
RUN corepack enable && corepack prepare pnpm@9.10.0 --activate

# Copy package files
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml ./
COPY turbo.json ./
COPY tsconfig.json ./

# Install production dependencies
RUN pnpm install --frozen-lockfile --prod --ignore-scripts

# Copy built dist files
COPY --from=builder /app/multimodal/tarko/agent-server-next/dist ./multimodal/tarko/agent-server-next/dist
COPY --from=builder /app/multimodal/tarko/agent-server-next/package.json ./multimodal/tarko/agent-server-next/package.json

# Copy node_modules from multimodal (includes built workspace packages)
COPY --from=builder /app/multimodal/node_modules ./multimodal/node_modules
COPY --from=builder /app/node_modules ./node_modules

# Copy all source
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/multimodal ./multimodal

# Copy entrypoint
COPY entrypoint.js ./entrypoint.js

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Create workspace directory
RUN mkdir -p /workspace/snapshots

# Expose the application port
EXPOSE 3000

# Run the server using entrypoint
CMD ["node", "entrypoint.js"]