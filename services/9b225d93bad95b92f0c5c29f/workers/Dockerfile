# Multi-stage build for Node.js workers
FROM node:20-bullseye AS builder

# Set working directory
WORKDIR /app

# Copy worker package files
COPY workers/package.json workers/yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy worker source code
COPY workers/ .

# Copy backend models needed by workers
COPY backend/models ./backend/models
COPY backend/utils ./backend/utils

# Production stage
FROM node:20-bullseye AS production

# Set working directory
WORKDIR /app

# Set NODE_ENV
ENV NODE_ENV=production

# Install dumb-init for proper signal handling
RUN apt-get update && apt-get install -y --no-install-recommends dumb-init && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 1001 nodejs && useradd -r -u 1001 -g nodejs vectoradmin

# Copy built application from builder stage
COPY --from=builder --chown=vectoradmin:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=vectoradmin:nodejs /app/index.js ./
COPY --from=builder --chown=vectoradmin:nodejs /app/utils ./utils
COPY --from=builder --chown=vectoradmin:nodejs /app/functions ./functions
COPY --from=builder --chown=vectoradmin:nodejs /app/backend ./backend

# Switch to non-root user
USER vectoradmin

# Expose port (workers also run an Express server)
EXPOSE 3355

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3355/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start the application
CMD ["dumb-init", "node", "index.js"]