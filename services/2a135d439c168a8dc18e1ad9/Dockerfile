# Build stage
FROM node:20-alpine AS builder

WORKDIR /home/ubuntu/deploy-projects/2a135d439c168a8dc18e1ad9

# Install build tools
RUN apk add --no-cache python3 make g++ libc6-compat

# Copy package files for dependency installation
COPY package*.json ./
COPY package-lock.json* ./

# Install all dependencies (including dev for build, skip native module scripts)
RUN npm ci --ignore-scripts

# Copy source code
COPY . .

# Build the project (with legacy OpenSSL provider for older webpack)
ENV NODE_OPTIONS=--openssl-legacy-provider
RUN npm run build

# Production stage
FROM node:20-alpine AS production

WORKDIR /home/ubuntu/deploy-projects/2a135d439c168a8dc18e1ad9

# Install runtime dependencies only
RUN apk add --no-cache netcat-openbsd

# Copy installed dependencies from builder
COPY --from=builder /home/ubuntu/deploy-projects/2a135d439c168a8dc18e1ad9/node_modules node_modules

# Copy built output from builder
COPY --from=builder /home/ubuntu/deploy-projects/2a135d439c168a8dc18e1ad9/out out

# Copy server script
COPY --from=builder /home/ubuntu/deploy-projects/2a135d439c168a8dc18e1ad9/server.js server.js

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose the server port
EXPOSE 3000

# Start the HTTP + WebSocket server for the notebook kernel
CMD node server.js