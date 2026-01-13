# Multi-stage build for Node.js backend
FROM node:20-bullseye AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY backend/package.json backend/yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy source code
COPY backend/ .

# Generate Prisma client
RUN npx prisma generate

# Frontend build stage
FROM node:20-alpine AS frontend-builder

# Set working directory for frontend
WORKDIR /frontend

# Copy frontend package files
COPY ../frontend/package.json ../frontend/yarn.lock ./

# Install frontend dependencies
RUN yarn install --frozen-lockfile

# Copy frontend source code
COPY ../frontend/ .

# Build the frontend
RUN yarn build

# Production stage
FROM node:20-bullseye AS production

# Set working directory
WORKDIR /app

# Set NODE_ENV
ENV NODE_ENV=production
ENV PORT=3001

# Install dumb-init for proper signal handling
RUN apt-get update && apt-get install -y --no-install-recommends dumb-init && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 1001 nodejs && useradd -r -u 1001 -g nodejs vectoradmin

# Copy built application from builder stage
COPY --from=builder --chown=vectoradmin:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=vectoradmin:nodejs /app/prisma ./prisma
COPY --from=builder --chown=vectoradmin:nodejs /app/index.js ./
COPY --from=builder --chown=vectoradmin:nodejs /app/endpoints ./endpoints
COPY --from=builder --chown=vectoradmin:nodejs /app/utils ./utils
COPY --from=builder --chown=vectoradmin:nodejs /app/models ./models

# Copy frontend build to public directory
COPY --from=frontend-builder --chown=vectoradmin:nodejs /frontend/dist ./public

# Create necessary directories
RUN mkdir -p storage/vector-cache && \
    chown -R vectoradmin:nodejs storage

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Running database migrations..."\n\
npx prisma migrate deploy\n\
echo "Starting server..."\n\
exec dumb-init node index.js\n\
' > /app/start.sh && chmod +x /app/start.sh

# Switch to non-root user
USER vectoradmin

# Expose port
EXPOSE 3001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3001/api/ping', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Use startup script
CMD ["/app/start.sh"]