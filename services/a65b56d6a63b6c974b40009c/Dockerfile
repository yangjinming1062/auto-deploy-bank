FROM node:20-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    make \
    g++ \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the main application (babel compilation)
RUN npm run build

# Build the client GUI (React with Vite)
WORKDIR /app/client
RUN npm install && npm run build
WORKDIR /app

# Production stage
FROM node:20-slim AS production

# Install runtime dependencies including xvfb for headless display
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    xauth \
    dbus \
    libnotify-bin \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libxshmfence1 \
    libgtk-3-0 \
    libgdk-pixbuf-2.0-0 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (electron is in devDependencies but needed to run)
RUN npm install

# Copy built files from builder
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/client/dist ./client/dist
COPY --from=builder /app/client/index.html ./client/index.html
COPY --from=builder /app/src/public ./dist/public
COPY --from=builder /app/src/adonisrc.json ./dist/adonisrc.json
COPY --from=builder /app/node_modules ./node_modules

# Set environment variables
ENV NODE_ENV=production
ENV DISPLAY=:99

# Copy web server for containerized deployment
COPY server.js ./

# Healthcheck: Verify web server is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000', (r) => process.exit(r.statusCode === 200 ? 0 : 1))" || exit 1

# Run the web server
CMD ["node", "server.js"]