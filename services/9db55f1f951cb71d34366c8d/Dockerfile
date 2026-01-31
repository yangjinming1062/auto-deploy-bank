# Build stage
FROM node:20-alpine AS builder

# Install Rush and pnpm globally
RUN npm install -g @microsoft/rush pnpm

WORKDIR /app

# Copy monorepo config and install dependencies
COPY rush.json ./
COPY apps/ apps/
COPY common/ common/
COPY config/ config/
COPY e2e/ e2e/
COPY packages/ packages/

# Install all dependencies and build
RUN rush install && \
    rush build --to @flowgram.ai/runtime-nodejs

# Production stage
FROM node:20-alpine

WORKDIR /app

# Install pnpm for running the app
RUN npm install -g pnpm

# Copy built artifacts for runtime-nodejs
COPY --from=builder /app/packages/runtime/nodejs/dist ./packages/runtime/nodejs/dist
COPY --from=builder /app/packages/runtime/nodejs/package.json ./packages/runtime/nodejs/package.json

# Copy node_modules for runtime-nodejs (pnpm symlinks reference common/temp/node_modules)
COPY --from=builder /app/packages/runtime/nodejs/node_modules ./packages/runtime/nodejs/node_modules

# Copy workspace dependencies
COPY --from=builder /app/packages/runtime/interface ./packages/runtime/interface
COPY --from=builder /app/packages/runtime/js-core ./packages/runtime/js-core

# Copy the pnpm store that symlinks point to
COPY --from=builder /app/common/temp/node_modules ./common/temp/node_modules

# Set environment variables
ENV NODE_ENV=production
ENV PORT=4000
ENV HOST=0.0.0.0

# Expose the service port
EXPOSE 4000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:4000/info || exit 1

# Start the application
CMD ["node", "packages/runtime/nodejs/dist/index.js"]