# Builder stage
FROM node:20-alpine AS builder

WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy monorepo configuration files
COPY package.json pnpm-lock.yaml ./
COPY pnpm-workspace.yaml turbo.json ./
COPY tsconfig.base.json ./

# Copy patches
COPY patches/ ./patches/

# Copy all workspace directories (monorepo structure)
COPY apps/ ./apps/
COPY libs/ ./libs/
COPY tools/ ./tools/
COPY docs/ ./docs/
COPY e2e/ ./e2e/
COPY tests/ ./tests/

# Install dependencies (use no-frozen-lockfile to handle autoInstallPeers, ignore-scripts for native modules)
RUN pnpm install --no-frozen-lockfile --ignore-scripts

# Build library dependencies first (required for web-tools to work)
# Run from root to ensure tsconfig paths resolve correctly
RUN pnpm turbo build --filter="./libs/**" --filter="!./libs/ui/examples/**" --filter="!./libs/ethereum-provider"

# Build ethereum-provider separately (it has path resolution issues)
RUN pnpm turbo build --filter="@ledgerhq/ethereum-provider"

# Build the application
WORKDIR /app/apps/web-tools
RUN pnpm build

# Production stage
FROM node:20-alpine AS runner

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy monorepo configuration files
COPY package.json pnpm-lock.yaml ./
COPY pnpm-workspace.yaml ./

# Copy patches
COPY patches/ ./patches/

# Copy all workspace directories (monorepo structure)
COPY apps/ ./apps/
COPY libs/ ./libs/
COPY tools/ ./tools/
COPY docs/ ./docs/
COPY e2e/ ./e2e/
COPY tests/ ./tests/

# Install dependencies (use --ignore-scripts to skip native module builds)
RUN pnpm install --prod --no-frozen-lockfile --ignore-scripts && \
    pnpm cache clean

# Copy built application from builder stage
COPY --from=builder /app/apps/web-tools/.next ./apps/web-tools/.next
COPY --from=builder /app/apps/web-tools/public ./apps/web-tools/public
COPY --from=builder /app/apps/web-tools/package.json ./apps/web-tools/package.json

# Set permissions
RUN chown -R nextjs:nodejs /app

# Change to web-tools directory
WORKDIR /app/apps/web-tools

USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

# Start the application
CMD ["pnpm", "start"]