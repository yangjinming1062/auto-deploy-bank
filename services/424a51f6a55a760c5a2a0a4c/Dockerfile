# Build stage
FROM node:20-alpine AS builder

# Install build dependencies for canvas native bindings
RUN apk add --no-cache python3 make g++ libc6-compat pkgconf pixman-dev cairo-dev jpeg-dev giflib-dev libjpeg-turbo-dev pango-dev gobject-introspection-dev

# Install Rush and PNPM globally
RUN npm install --global @microsoft/rush pnpm

WORKDIR /app

# Copy package files first for better caching
COPY package.json pnpm-lock.yaml ./
COPY rush.json ./
COPY common/ ./common/

# Copy package configs
COPY packages/ ./packages/
COPY docs/ ./docs/
COPY tools/ ./tools/
COPY share/ ./share/

# Install dependencies
RUN rush update

# Build all packages
RUN rush build

# Production stage
FROM node:20-alpine

# Install build dependencies for canvas native bindings
RUN apk add --no-cache python3 make g++ libc6-compat pkgconf pixman-dev cairo-dev jpeg-dev giflib-dev libjpeg-turbo-dev pango-dev gobject-introspection-dev

# Install PNPM for running serve
RUN npm install --global pnpm

WORKDIR /app

# Copy built packages from builder
COPY --from=builder /app/common ./common
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/docs ./docs
COPY --from=builder /app/tools ./tools
COPY --from=builder /app/share ./share
COPY --from=builder /app/rush.json .
COPY --from=builder /app/package.json .
COPY --from=builder /app/pnpm-lock.yaml .

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3020

# Expose the internal port
EXPOSE 3020

# Start the docs site
WORKDIR /app/docs
CMD ["npx", "vite", "--host", "0.0.0.0", "--port", "3020", "--no-open"]