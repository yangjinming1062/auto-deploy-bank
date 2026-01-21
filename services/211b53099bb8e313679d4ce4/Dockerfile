FROM node:20-alpine AS builder

WORKDIR /app

# Copy entire monorepo
COPY . .

# Install dependencies using corepack
RUN corepack enable && corepack prepare yarn@4.9.1 --activate
RUN yarn install

# Install build dependencies for native modules (gcc, make, python3, curl for napi-rs and rustup)
RUN apk add --no-cache python3 make g++ libc-dev curl

# Install Rust for building native modules with musl target for Alpine
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable --target x86_64-unknown-linux-musl
ENV PATH="$HOME/.cargo/bin:$PATH"

# Build native module using napi (link all Rust tools to PATH so napi can find them)
# Build with --esm flag for ESM compatibility
RUN cp /root/.cargo/bin/* /usr/local/bin/ && cd /app/packages/backend/native && \
    /app/node_modules/.bin/napi build --release --strip --no-const-enum --esm

# Build the server
# DATABASE_URL needed for Prisma client generation (uses dummy URL during build)
ENV DATABASE_URL="postgresql://localhost:5432/open_agent"
RUN cd packages/backend/server && yarn prisma generate && yarn build

# Build the frontend app
RUN cd packages/frontend/app && yarn build

# Production stage
FROM node:20-alpine AS production

RUN apk add --no-cache jemalloc shadow netcat-openbsd

WORKDIR /app

# Create non-root user
RUN groupadd -g 1001 nodejs && useradd -u 1001 -g nodejs -s /bin/bash -m nodejs

# Copy built application from builder
COPY --from=builder /app/packages/backend/server/dist ./dist
COPY --from=builder /app/packages/backend/server/package.json ./package.json
COPY --from=builder /app/packages/backend/server/schema.prisma ./schema.prisma
COPY --from=builder /app/packages/backend/server/migrations ./migrations
# Copy workspace node_modules (yarn workspaces use hoisted node_modules at root)
# Note: This creates symlinks for workspace packages
COPY --from=builder /app/node_modules ./node_modules
# Copy entire native package to override the workspace symlink with actual files
# This ensures the built files are used, not the source symlinks
COPY --from=builder /app/packages/backend/native/. ./node_modules/@afk/server-native/
# Copy frontend build output to static directory (server expects static files at projectRoot/static)
COPY --from=builder /app/packages/frontend/app/dist ./static
# Copy scripts folder for user management (from root and backend server)
COPY --from=builder /app/scripts ./scripts
COPY --from=builder /app/packages/backend/server/scripts ./server-scripts

# Replace index.js with ESM-compatible version using createRequire
RUN cat > ./node_modules/@afk/server-native/index.js << 'ESMEOF'
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const binding = require('./server-native.node');
export default binding;
ESMEOF

# Set ownership
RUN chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs

# Environment variables
ENV NODE_ENV=production
ENV OPEN_AGENT_ENV=production
ENV LD_PRELOAD=libjemalloc.so.2

# Expose the internal port
EXPOSE 3010

# Health check - use TCP check on port 3010
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD nc -z localhost 3010 || exit 1

# Start the server
CMD ["node", "dist/main.mjs"]