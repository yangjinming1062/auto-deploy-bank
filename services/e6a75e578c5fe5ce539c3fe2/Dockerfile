FROM node:20-alpine AS builder

# Install build dependencies for Electron
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    xvfb \
    libnotify \
    nss \
    clang \
    libc-dev \
    libx11-dev \
    libxrandr-dev \
    libxkbcommon-dev \
    libdrm-dev \
    mesa-dev \
    cups-dev \
    alsa-lib-dev

WORKDIR /app

# Create required directory for electron-builder
RUN mkdir -p release/app

# Copy pnpm lockfile and install dependencies
COPY package.json pnpm-lock.yaml ./
# Modify package.json to skip postinstall, then install
RUN sed -i 's/"postinstall": "electron-builder install-app-deps"/"postinstall": "echo skipped"/' package.json && \
    corepack enable pnpm && \
    pnpm install --frozen-lockfile

# Copy source code and build
COPY . .
RUN pnpm build

# Production stage
FROM node:20-alpine

# Install runtime dependencies including Xvfb for headless display
RUN apk add --no-cache \
    xvfb \
    xvfb-run \
    libnotify \
    nss \
    libstdc++ \
    libx11 \
    libxrandr \
    libxkbcommon \
    mesa \
    libdrm \
    mesa-gbm \
    cups-libs \
    alsa-lib \
    ttf-freefont

WORKDIR /app

# Copy built application from builder
COPY --from=builder /app/release/app ./release/app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

# Set environment variables
ENV NODE_ENV=production
ENV DISPLAY=:99
ENV PATH=/app/node_modules/.bin:${PATH}

# Copy status server script
COPY server.js ./

# Expose port for web-based features
EXPOSE 40635

# Run both the HTTP server and Electron app
CMD ["sh", "-c", "node /app/server.js & xvfb-run -a /app/node_modules/.bin/electron /app/release/app/dist/main/main.mjs"]