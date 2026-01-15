# Build stage
FROM node:20-bookworm-slim AS builder

WORKDIR /app

# Install system dependencies needed for Prisma
# libssl1.1 is needed for Prisma engine on Debian bookworm
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates wget \
    && wget -q -O /tmp/libssl1.1.deb https://packages.debian.org/pool/main/o/openssl/libssl1.1/libssl1.1_1.1.1n-0+deb11u6_amd64.deb \
    && dpkg -i /tmp/libssl1.1.deb || true \
    && apt-get install -f -y --no-install-recommends \
    && rm -f /tmp/libssl1.1.deb \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps --ignore-scripts

# Copy source code
COPY . .

# Generate Prisma client for server
RUN npx nx run server/db:generate

# Build the server directly
RUN npx nx build @magickml/server

# Production stage
FROM node:20-bookworm-slim AS production

WORKDIR /app

# Install system dependencies needed for Prisma
# libssl1.1 is needed for Prisma engine on Debian bookworm
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates wget \
    && wget -q -O /tmp/libssl1.1.deb https://packages.debian.org/pool/main/o/openssl/libssl1.1/libssl1.1_1.1.1n-0+deb11u6_amd64.deb \
    && dpkg -i /tmp/libssl1.1.deb || true \
    && apt-get install -f -y --no-install-recommends \
    && rm -f /tmp/libssl1.1.deb \
    && rm -rf /var/lib/apt/lists/*

# Install production dependencies only
COPY package*.json ./
RUN npm install --legacy-peer-deps --ignore-scripts --only=production && npm cache clean --force

# Copy built artifacts from builder
COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/node_modules /app/node_modules
COPY --from=builder /app/packages /app/packages
COPY --from=builder /app/apps/server/src/certs /app/apps/server/src/certs
COPY --from=builder /app/instrument.js /app/instrument.js
COPY --from=builder /app/package.json /app/package.json

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3030

# Expose the internal port
EXPOSE 3030

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3030/ || exit 1

# Start the server
CMD ["npm", "run", "start-server"]