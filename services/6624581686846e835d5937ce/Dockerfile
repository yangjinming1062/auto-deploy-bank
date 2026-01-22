# Multi-stage build for Next.js static export application
FROM node:20-alpine AS builder

# Install dependencies
WORKDIR /app

# Copy package files
COPY package.json yarn.lock .yarnrc.yml ./

# Configure Yarn Berry and install dependencies
RUN corepack enable && \
    yarn install --immutable

# Copy project files
COPY . .

# Set build environment variables
ENV ANALYZE=false
ENV BUILD_ENV=development
ENV NODE_ENV=production

# Build the application with static export and image optimization
RUN yarn build:release

# Production stage - use serve for static files
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

# Enable corepack and install serve for static file serving
RUN corepack enable && yarn global add serve

# Create non-root user for security
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built static files from builder
# Static export outputs to client/www/next-build per next.config.mjs
COPY --from=builder /app/client/www/next-build /app
COPY --from=builder /app/public /app/public

# Change ownership to non-root user
RUN chown -R nextjs:nodejs /app

USER nextjs

EXPOSE 3000

# Start the static file server
CMD ["serve", "-s", "/app", "-l", "3000"]