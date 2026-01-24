# Build stage
FROM node:20 AS builder

WORKDIR /app

# Copy package files first for better layer caching
COPY package*.json ./

# Install dependencies (including dev for build)
RUN npm ci

# Copy source code
COPY . .

# Build the Remix app
RUN npm run build

# Production stage - using full node image for glibc compatibility with wrangler
FROM node:20

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies and wrangler for local dev
RUN npm ci --only=production && npm install wrangler@latest

# Copy built assets from builder stage
COPY --from=builder /app/build ./build
COPY --from=builder /app/public ./public
COPY --from=builder /app/wrangler*.toml ./
# Copy .dev.vars if it exists, otherwise create an empty one
RUN if [ -f /app/.dev.vars ]; then cp /app/.dev.vars ./.dev.vars; else touch .dev.vars; fi
COPY --from=builder /app/drizzle.config.ts ./
COPY --from=builder /app/app ./app

# Set environment variables
ENV NODE_ENV=production
ENV PORT=8787

# Expose the internal port
EXPOSE 8787

# Start command - use wrangler dev with local mode
# Using --local flag to run without connecting to Cloudflare
CMD ["npx", "wrangler", "dev", "-c", "wrangler.development.toml", "./build/index.js", "--local", "--ip", "0.0.0.0", "--port", "8787", "--log-level", "info"]