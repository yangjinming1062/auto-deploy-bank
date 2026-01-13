# Build local monorepo image
# docker build --no-cache -t flowise .

# Run image
# docker run -d -p 3000:3000 flowise

FROM node:20-alpine AS builder

# Install system dependencies and build tools
RUN apk update && \
    apk add --no-cache \
        libc6-compat \
        python3 \
        make \
        g++ \
        build-base \
        cairo-dev \
        pango-dev \
        chromium \
        curl && \
    npm install -g pnpm

ENV PUPPETEER_SKIP_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

ENV NODE_OPTIONS=--max-old-space-size=8192
ENV NODE_ENV=production
ENV PORT=3000

WORKDIR /usr/src/flowise

# Copy all necessary files for installation
COPY package.json pnpm-lock.yaml ./
COPY pnpm-workspace.yaml ./
COPY turbo.json ./
COPY packages ./packages

# Install dependencies with no-frozen-lockfile to ensure workspace packages are linked
RUN pnpm install --no-frozen-lockfile

# Build all packages
RUN pnpm build

# Production stage
FROM node:20-alpine

# Install runtime dependencies only
RUN apk update && \
    apk add --no-cache \
        libc6-compat \
        chromium \
        curl && \
    npm install -g pnpm

# Set environment variables
ENV PUPPETEER_SKIP_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
ENV NODE_ENV=production
ENV PORT=3000

WORKDIR /usr/src/flowise

# Copy built application from builder stage
COPY --from=builder /usr/src/flowise ./

# Make run scripts executable
RUN chmod +x /usr/src/flowise/packages/server/bin/run

# Switch to non-root user (node user already exists in node:20-alpine)
USER node

# Create necessary directories for the application
RUN mkdir -p /home/node/.flowise/logs /home/node/.flowise/database /home/node/.flowise/storage /home/node/.flowise/temp

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:3000/api/v1/ping || exit 1

CMD [ "pnpm", "start" ]